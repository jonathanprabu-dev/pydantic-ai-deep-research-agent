"""Research a whole list of accounts, one row at a time, for BDRs and SDRs.

    python account_list.py accounts.xlsx
    python account_list.py accounts.csv --focus "contact center" --limit 10
    python account_list.py accounts.xlsx                 # run again any time: researches only
                                                         # new or unfinished companies
    python account_list.py accounts.xlsx --fresh         # research every company again

Reads a spreadsheet with a company column (and ideally a website column),
researches each company from public Google results, and writes a copy of the
sheet with new columns: what they do, recent news, priorities, team and hiring
signals, likely buying roles, a talking point, and the numbered sources behind
every point.

Same rules as the single-company report:
  - every point must cite a URL that was really in the search results, checked
    in code; points left without a real source are deleted
  - it never looks for, and strips out, email addresses and phone numbers;
    contact data belongs in an enrichment tool (Clay) with verification
  - it never edits the input file; results go to a new file, saved after
    every row so a crash or a quota stop loses nothing

Cost: one model request per row (plus Google searches in Chrome), so a free
OpenRouter key covers roughly 45 accounts a day.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import os
import re
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from agent import REQUESTS_PER_RUN, check_backend, get_model
from browser import SearchBlocked, close_browser, fetch_page, google_search
from pydantic_ai.exceptions import ModelHTTPError

from research import friendly_error, score_source
from research_models import Nested, SearchResult

RESULTS_PER_SEARCH = 8
PAGES_PER_ROW = 3          # full pages read per company, best-ranked first
PAGE_CHARS = 8_000
MAX_POINTS = 3             # per column

# One Google search per entry. {company}, {domain} and {year} are filled in per row.
SEARCHES = {
    "overview": ('site:{domain} about', '"{company}" company overview'),  # (with website, without)
    "news": ('"{company}" news {year}', '"{company}" news {year}'),
    "priorities": ('"{company}" strategy OR expansion OR launch OR partnership {year}',) * 2,
    "team": ('"{company}" hiring OR appoints OR "names new" OR funding',) * 2,
}
FOCUS_SEARCH = '"{company}" {focus}'

COMPANY_HEADERS = ("company", "company name", "account", "account name", "organization", "name")
WEBSITE_HEADERS = ("website", "domain", "company website", "company domain", "url", "web site", "site")

STATUS = "Research Status"
NEW_COLUMNS = [
    STATUS,
    "What They Do",
    "Recent News",
    "Priorities",
    "Team & Hiring Signals",
    "Likely Buying Roles",
    "Talking Point",
    "Sources",
    "Researched On",
]
FOCUS_COLUMN = "Focus Fit"
DONE_STATUSES = ("Done", "Check match", "Thin")

EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE_CANDIDATE = re.compile(r"\+?\(?\d[\d\s().-]{7,}\d")


# ---------------------------------------------------------------- the contract

class CitedPoint(Nested):
    """One short point about the account, with the sources that support it."""

    text: str = Field(description="One or two sentences. Include dates and numbers where the source gives them.")
    source_urls: list[str] = Field(description="URLs copied exactly from the supplied sources.")


class AccountBrief(BaseModel):
    company_matched: bool = Field(
        description="False if the sources seem to describe a different company with a similar name."
    )
    what_they_do: list[CitedPoint] = Field(description="One point: what the company sells and to whom.")
    recent_news: list[CitedPoint] = Field(description="Up to 3 dated items, newest first.")
    priorities: list[CitedPoint] = Field(description="Up to 3 stated priorities, initiatives or launches.")
    team_signals: list[CitedPoint] = Field(description="Up to 3: hiring, leadership changes, funding, expansion.")
    buying_roles: list[CitedPoint] = Field(
        description="Up to 3 job titles (not people's names) likely to care, and why, based on the sources."
    )
    talking_point: list[CitedPoint] = Field(description="One opening line for a BDR, built on one cited fact.")
    focus_fit: list[CitedPoint] = Field(
        default_factory=list, description="Up to 3 points relevant to the focus, if a focus was given."
    )


BRIEF_INSTRUCTIONS = """\
You prepare account research for a sales development rep (BDR) before first outreach.
You are given a company name, its website if known, Google search results, and the
text of a few pages.

Rules you must follow:
- Every point must cite at least one URL copied exactly from the supplied sources.
  Points without a real source are deleted, so never write a URL that is not listed.
- Only state what the sources say. If the evidence is thin, return fewer points or
  empty lists. Never pad and never guess.
- Check identity first: set company_matched=false if the sources seem to be about a
  different company with a similar name (different website, industry or country).
- Never include email addresses, phone numbers or other personal contact details.
- For buying roles give job titles, not people's names, and say in a few words why
  that role would care, based on what the sources say.
- recent_news: newest first, with the date or month when the source gives it.
- talking_point: one plain sentence a BDR could open with, built on one cited fact.
  No hype, no flattery.
- If a focus is given, focus_fit lists only evidence that bears on it; otherwise
  leave focus_fit empty.
Keep every point to one or two sentences.\
"""

_brief_agent: Agent[None, AccountBrief] | None = None


def brief_agent() -> Agent[None, AccountBrief]:
    global _brief_agent
    if _brief_agent is None:
        _brief_agent = Agent(get_model(), output_type=AccountBrief, instructions=BRIEF_INSTRUCTIONS)
    return _brief_agent


# ---------------------------------------------------------------- small helpers

def clean_domain(value: object) -> str:
    """'https://www.Acme.com/about' -> 'acme.com'. Blank or junk -> ''."""
    text = str(value or "").strip().lower()
    if not text or " " in text:
        return ""
    host = urlparse(text if "//" in text else f"//{text}").netloc
    host = host.split("@")[-1].split(":")[0]
    host = host[4:] if host.startswith("www.") else host
    return host if "." in host else ""


def strip_contact_details(text: str) -> str:
    """Remove anything that looks like an email address or a phone number.

    Contact data is out of scope for this tool on purpose; this is the code-level
    backstop behind the instruction.
    """
    text = EMAIL.sub("[removed]", text)

    def phone(match: re.Match[str]) -> str:
        digits = sum(ch.isdigit() for ch in match.group())
        return "[removed]" if digits >= 10 else match.group()

    return PHONE_CANDIDATE.sub(phone, text)


def _on_domain(url: str, domain: str) -> bool:
    host = urlparse(url).netloc.lower()
    return bool(domain) and (host == domain or host.endswith("." + domain))


def build_queries(company: str, domain: str, focus: str) -> dict[str, str]:
    year = date.today().year
    queries = {}
    for name, (with_site, without_site) in SEARCHES.items():
        template = with_site if domain else without_site
        queries[name] = template.format(company=company, domain=domain, year=year)
    if focus:
        queries["focus"] = FOCUS_SEARCH.format(company=company, focus=focus)
    return queries


def keep_real_sources(
    brief: AccountBrief, allowed: dict[str, str]
) -> tuple[dict[str, list[tuple[str, list[int]]]], list[tuple[str, str]]]:
    """Check every citation against the URLs we actually supplied.

    Returns the surviving points per field as (text, source numbers), plus the
    numbered source list those numbers refer to. A point whose citations were
    all invented is dropped, not kept without a source.
    """
    numbered: list[tuple[str, str]] = []
    index: dict[str, int] = {}
    caps = {"what_they_do": 1, "talking_point": 1}
    fields: dict[str, list[tuple[str, list[int]]]] = {}
    for field in (
        "what_they_do", "recent_news", "priorities", "team_signals",
        "buying_roles", "talking_point", "focus_fit",
    ):
        kept = []
        for point in getattr(brief, field):
            urls = [u.strip() for u in point.source_urls if u.strip() in allowed]
            text = strip_contact_details(point.text.strip())
            if not urls or not text:
                continue
            numbers = []
            for url in dict.fromkeys(urls):
                if url not in index:
                    numbered.append((allowed[url] or url, url))
                    index[url] = len(numbered)
                numbers.append(index[url])
            kept.append((text, numbers))
        fields[field] = kept[: caps.get(field, MAX_POINTS)]
    return fields, numbered


def _cell(points: list[tuple[str, list[int]]]) -> str:
    return "\n".join(
        f"• {text} [{', '.join(map(str, nums))}]" for text, nums in points
    )


# ---------------------------------------------------------------- one row

async def research_account(company: str, domain: str, focus: str) -> dict[str, str]:
    """Search, read and brief one company. Returns the new column values."""
    queries = build_queries(company, domain, focus)
    batches = await asyncio.gather(*(google_search(q, RESULTS_PER_SEARCH) for q in queries.values()))

    results: dict[str, SearchResult] = {}
    for batch in batches:
        for r in batch:
            results.setdefault(r.url, r)
    if not results:
        return {STATUS: "Thin: no search results", "Researched On": _today()}

    def rank(r: SearchResult) -> int:
        return score_source(r, prefer_primary=False) + (4 if _on_domain(r.url, domain) else 0)

    top = sorted(results.values(), key=rank, reverse=True)[:PAGES_PER_ROW]
    pages = await asyncio.gather(*(fetch_page(r.url, PAGE_CHARS) for r in top))
    page_text = "\n\n".join(
        f"### PAGE: {r.title}\nURL: {r.url}\n{text}" for r, text in zip(top, pages) if text
    )
    listing = "\n".join(f"- {r.title}\n  URL: {r.url}\n  Snippet: {r.snippet}" for r in results.values())

    prompt = (
        f"Company: {company}\n"
        f"Website: {domain or '(not given)'}\n"
        f"Focus: {focus or '(none)'}\n\n"
        f"SEARCH RESULTS:\n{listing}\n\n"
        f"FULL PAGE TEXT:\n{page_text or '(no pages could be fetched)'}"
    )
    brief = (await brief_agent().run(prompt)).output

    fields, numbered = keep_real_sources(brief, {r.url: r.title for r in results.values()})
    total = sum(len(v) for v in fields.values())

    on_site = any(_on_domain(url, domain) for _, url in numbered)
    if not brief.company_matched or (domain and numbered and not on_site and not fields["what_they_do"]):
        status = "Check match"
    elif total < 3:
        status = "Thin"
    else:
        status = "Done"

    row = {
        STATUS: status,
        "What They Do": _cell(fields["what_they_do"]),
        "Recent News": _cell(fields["recent_news"]),
        "Priorities": _cell(fields["priorities"]),
        "Team & Hiring Signals": _cell(fields["team_signals"]),
        "Likely Buying Roles": _cell(fields["buying_roles"]),
        "Talking Point": _cell(fields["talking_point"]),
        "Sources": "\n".join(f"[{i}] {title} | {url}" for i, (title, url) in enumerate(numbered, 1)),
        "Researched On": _today(),
    }
    if focus:
        row[FOCUS_COLUMN] = _cell(fields["focus_fit"])
    return row


def _today() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------------- the sheet

def read_table(path: Path, sheet: str | None) -> tuple[list[str], list[list[object]]]:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            rows = [r for r in csv.reader(f)]
    elif path.suffix.lower() in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook

        wb = load_workbook(path, read_only=True, data_only=True)
        if sheet and sheet not in wb.sheetnames:
            raise SystemExit(f"No sheet called {sheet!r}. Sheets: {', '.join(wb.sheetnames)}")
        ws = wb[sheet] if sheet else wb.worksheets[0]
        rows = [list(r) for r in ws.iter_rows(values_only=True)]
        wb.close()
    else:
        raise SystemExit("Give a .csv or .xlsx file.")
    rows = [r for r in rows if any(v not in (None, "") for v in r)]
    if not rows:
        raise SystemExit(f"{path.name} is empty.")
    headers = [str(h).strip() if h is not None else "" for h in rows[0]]
    width = len(headers)
    body = [list(r) + [None] * (width - len(r)) for r in rows[1:]]
    return headers, [r[:width] for r in body]


def find_column(headers: list[str], names: tuple[str, ...]) -> int | None:
    lowered = [h.strip().lower() for h in headers]
    for name in names:
        if name in lowered:
            return lowered.index(name)
    return None


def write_table(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    """Save the whole sheet, atomically, so a crash mid-save can't corrupt it."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill

    wb = Workbook()
    ws = wb.active
    ws.title = "Accounts"
    ws.append(headers)
    for row in rows:
        ws.append(row)
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="17324D")
    new_from = len(headers) - len([h for h in headers if h in NEW_COLUMNS or h == FOCUS_COLUMN])
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            if isinstance(cell.value, str) and cell.value[:1] in ("=", "+", "-", "@"):
                cell.data_type = "s"  # text, never a formula
            if cell.column > new_from:
                cell.alignment = Alignment(wrap_text=True, vertical="top")
    for col, header in enumerate(headers, 1):
        letter = ws.cell(row=1, column=col).column_letter
        ws.column_dimensions[letter].width = 60 if header in ("Sources", "Recent News", "Priorities") else (
            45 if col > new_from and header not in (STATUS, "Researched On") else 18
        )
    ws.freeze_panes = "B2"

    about = wb.create_sheet("How to read this")
    for line in (
        ["Every point ends with source numbers, e.g. [1, 3]. They refer to the Sources column in the same row."],
        ["Only sources that really appeared in the search results are kept; points without one are deleted."],
        ["Research Status: Done = researched. Thin = little public information. Check match = the sources may be about a different company; check before using."],
        ["No emails or phone numbers are collected. Contact data comes from Clay (with verification), not from this tool."],
        ["This is public web research. Read the source before quoting a fact to a prospect."],
    ):
        about.append(line)
    about.column_dimensions["A"].width = 120

    fd, tmp = tempfile.mkstemp(suffix=".xlsx", dir=path.parent)
    os.close(fd)
    try:
        wb.save(tmp)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def _same_file(a: Path, b: Path) -> bool:
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b)) or (
        a.exists() and b.exists() and os.path.samefile(a, b)
    )


# ---------------------------------------------------------------- the run

RATE_LIMIT_WAIT = 65   # seconds to wait out a per-minute limit before one retry
RESEARCH_COLUMNS = set(NEW_COLUMNS) | {FOCUS_COLUMN}


def _row_key(company: str, domain: str) -> tuple[str, str]:
    return (" ".join(company.lower().split()), domain)


def _previous_research(
    headers: list[str], rows: list[list[object]]
) -> dict[tuple[str, str], dict[str, object]]:
    """Finished research from an earlier results file, keyed by company + website."""
    company_col = find_column(headers, COMPANY_HEADERS)
    website_col = find_column(headers, WEBSITE_HEADERS)
    if company_col is None or STATUS not in headers:
        return {}
    col = {h: i for i, h in enumerate(headers)}
    found: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        if not str(row[col[STATUS]] or "").startswith(DONE_STATUSES):
            continue
        company = str(row[company_col] or "").strip()
        domain = clean_domain(row[website_col]) if website_col is not None else ""
        found.setdefault(
            _row_key(company, domain),
            {h: row[i] for h, i in col.items() if h in RESEARCH_COLUMNS},
        )
    return found


async def _research_with_retry(company: str, domain: str, focus: str) -> dict[str, str]:
    """Research one row; wait out a per-minute rate limit once instead of failing."""
    try:
        return await research_account(company, domain, focus)
    except ModelHTTPError as exc:
        if exc.status_code != 429 or "out of quota for today" in friendly_error(exc):
            raise
        print(f"   Rate limit for this minute; waiting {RATE_LIMIT_WAIT}s and trying again…", file=sys.stderr)
        await asyncio.sleep(RATE_LIMIT_WAIT)
        return await research_account(company, domain, focus)


async def run_list(
    src: Path, out: Path, *, focus: str = "", limit: int | None = None,
    fresh: bool = False, sheet: str | None = None,
) -> dict[str, int]:
    """Your list is the source of truth; the results file is rebuilt from it each run.

    Companies already researched (in an earlier results file, or in the input
    itself) are copied over, not researched again. New companies, failed rows and
    rows not reached last time are researched. Other columns always come from
    your list, so edits there (a new owner, say) show up in the results.
    """
    if _same_file(src, out):
        raise SystemExit("The output file would overwrite your input. Choose a different --out.")

    headers, rows = read_table(src, sheet)
    company_col = find_column(headers, COMPANY_HEADERS)
    if company_col is None:
        raise SystemExit(
            "No company column found. Name one of the columns: " + ", ".join(f'"{h}"' for h in COMPANY_HEADERS[:4])
        )
    website_col = find_column(headers, WEBSITE_HEADERS)

    previous: dict[tuple[str, str], dict[str, object]] = {}
    if not fresh:
        # Research already in the input (if you gave it a results file) ...
        previous.update(_previous_research(headers, rows))
        # ... and in the results file from the last run, which wins.
        if out.exists():
            old_headers, old_rows = read_table(out, None)
            previous.update(_previous_research(old_headers, old_rows))

    # Rebuild: your columns as they are now, then fresh research columns.
    keep = [i for i, h in enumerate(headers) if h not in RESEARCH_COLUMNS]
    headers = [headers[i] for i in keep]
    rows = [[row[i] for i in keep] for row in rows]
    company_col = find_column(headers, COMPANY_HEADERS)
    website_col = find_column(headers, WEBSITE_HEADERS)
    wanted = list(NEW_COLUMNS)
    if focus or any(v.get(FOCUS_COLUMN) for v in previous.values()):
        wanted.insert(wanted.index("Sources"), FOCUS_COLUMN)
    headers += wanted
    for row in rows:
        row.extend([None] * len(wanted))
    col = {h: i for i, h in enumerate(headers)}

    counts = {"done": 0, "check": 0, "thin": 0, "failed": 0, "skipped": 0, "already": 0, "waiting": 0}
    seen: dict[tuple[str, str], int] = {}
    to_research: list[tuple[int, list[object], str, str]] = []

    for n, row in enumerate(rows, start=2):
        company = str(row[company_col] or "").strip()
        domain = clean_domain(row[website_col]) if website_col is not None else ""
        if not company:
            row[col[STATUS]] = "Skipped: no company name"
            counts["skipped"] += 1
            continue
        key = _row_key(company, domain)
        if key in seen:
            row[col[STATUS]] = f"Skipped: same company as row {seen[key]}"
            counts["skipped"] += 1
            continue
        seen[key] = n
        if key in previous:
            for h, value in previous[key].items():
                if h in col:
                    row[col[h]] = value
            counts["already"] += 1
        else:
            row[col[STATUS]] = "Waiting: not researched yet"
            to_research.append((n, row, company, domain))

    if previous and not fresh:
        reused = counts["already"]
        print(f"Reusing {reused} {'company' if reused == 1 else 'companies'} already researched; "
              f"{len(to_research)} to research now.", file=sys.stderr)
    write_table(out, headers, rows)

    stop_message = ""
    for processed, (n, row, company, domain) in enumerate(to_research, start=1):
        if limit is not None and processed > limit:
            break
        print(f"[{processed}/{len(to_research)}] {company}{f' ({domain})' if domain else ''}…", file=sys.stderr)
        try:
            values = await _research_with_retry(company, domain, focus)
        except SearchBlocked as exc:
            stop_message = ("Google is asking for a check in the Chrome window. Solve it, then run the same "
                            f"command again to carry on. ({exc})")
            row[col[STATUS]] = "Failed: Google check"
            counts["failed"] += 1
            break
        except Exception as exc:
            message = friendly_error(exc).replace(
                f"One research run costs about {REQUESTS_PER_RUN}.", "Each account costs 1 request."
            )
            row[col[STATUS]] = f"Failed: {message[:150]}"
            counts["failed"] += 1
            write_table(out, headers, rows)
            if "out of quota for today" in message:
                stop_message = message + " Run the same command again after the reset to carry on."
                break
            continue

        for key_, value in values.items():
            if key_ in col:
                row[col[key_]] = value
        result = values[STATUS]
        counts["done" if result == "Done" else "check" if result == "Check match" else "thin"] += 1
        write_table(out, headers, rows)  # after every row, so nothing is lost

    counts["waiting"] = sum(1 for row in rows if str(row[col[STATUS]] or "").startswith("Waiting"))
    write_table(out, headers, rows)
    if stop_message:
        print(stop_message, file=sys.stderr)
    return counts


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Research a list of accounts, one row at a time.")
    parser.add_argument("file", type=Path, help="A .csv or .xlsx with a company column (and ideally a website column)")
    parser.add_argument("--out", type=Path, help="Output .xlsx (default: <name>_researched.xlsx next to the input)")
    parser.add_argument("--focus", default="", help='Extra topic to look for, e.g. "contact center"')
    parser.add_argument("--limit", type=int, help="Research at most this many rows in this run")
    parser.add_argument("--fresh", action="store_true",
                        help="Research every company again, ignoring earlier results")
    parser.add_argument("--resume", action="store_true", help=argparse.SUPPRESS)  # old flag; now automatic
    parser.add_argument("--sheet", help="Sheet name in the input workbook (default: the first)")
    args = parser.parse_args()

    if not args.file.is_file():
        raise SystemExit(f"No such file: {args.file}")
    out = args.out or args.file.with_name(f"{args.file.stem}_researched.xlsx")
    if out.suffix.lower() != ".xlsx":
        raise SystemExit("--out must end in .xlsx")
    error = check_backend()
    if error:
        raise SystemExit(error)

    async def go() -> dict[str, int]:
        try:
            return await run_list(args.file, out, focus=args.focus.strip(), limit=args.limit,
                                  fresh=args.fresh, sheet=args.sheet)
        finally:
            await close_browser()

    counts = asyncio.run(go())
    print(
        f"Saved {out}\n"
        f"Done {counts['done']} · Check match {counts['check']} · Thin {counts['thin']} · "
        f"Failed {counts['failed']} · Skipped {counts['skipped']} · Reused {counts['already']}"
        + (f" · Still waiting {counts['waiting']} (run the same command again to carry on)" if counts["waiting"] else "")
    )


if __name__ == "__main__":
    main()
