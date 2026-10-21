"""Offline test for account_list.py: fake Google, fake pages, scripted model.

    python test_account_list.py

No API key, no Chrome, no network. Checks the rules that matter:
invented citations are dropped, emails and phone numbers are removed, a
look-alike company is flagged, the input file is never touched, a daily-quota
stop keeps finished rows, and --resume carries on from there.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import tempfile
from pathlib import Path

from openpyxl import load_workbook
from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError
from pydantic_ai.messages import ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

import account_list as al
from research_models import SearchResult

SEARCH_LOG: list[str] = []


async def fake_search(query: str, limit: int = 10) -> list[SearchResult]:
    SEARCH_LOG.append(query)
    name = query.split('"')[1] if '"' in query else query.split()[0].replace("site:", "")
    slug = name.lower().replace(" ", "")
    return [
        SearchResult(title=f"{name} newsroom", url=f"https://{slug}.com/news", snippet="Company news."),
        SearchResult(title=f"{name} at Reuters", url=f"https://reuters.com/{slug}", snippet="Coverage."),
    ]


async def fake_fetch(url: str, max_chars: int = 12_000) -> str:
    return f"Page text for {url}. " * 30


QUOTA_ON: set[str] = set()


def scripted_model(messages, info: AgentInfo) -> ModelResponse:
    prompt = messages[-1].parts[-1].content
    company = prompt.split("\n")[0].removeprefix("Company: ")
    if company in QUOTA_ON:
        raise ModelHTTPError(429, "test-model", body={"error": "quota exceeded perDay"})
    slug = company.lower().replace(" ", "")
    real = f"https://reuters.com/{slug}"
    own = f"https://{slug}.com/news"
    fake = "https://made-up.example.com/story"
    brief = {
        "company_matched": company != "Northstar Logistics",
        "what_they_do": [{"text": f"{company} sells contact-centre software.", "source_urls": [own]}],
        "recent_news": [
            {"text": "Opened a new support hub in March 2026.", "source_urls": [real]},
            {"text": "This one cites only a fake URL.", "source_urls": [fake]},
            {"text": "Mixed: one real, one fake.", "source_urls": [fake, real]},
        ],
        "priorities": [{"text": "Call jane.doe@acme.com or +1 (555) 123-4567 today.", "source_urls": [own]}],
        "team_signals": [{"text": "Hiring 40 support agents for 2025-2026.", "source_urls": [real]}],
        "buying_roles": [{"text": "VP of Customer Experience: owns the new hub.", "source_urls": [real]}],
        "talking_point": [{"text": "=HYPERLINK(\"http://x\") Saw the new hub opening.", "source_urls": [real]}],
        "focus_fit": [{"text": "Runs a 300-seat contact centre.", "source_urls": [own]}],
    }
    return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, json.dumps(brief))])


def fingerprint(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_out(path: Path) -> list[dict[str, object]]:
    ws = load_workbook(path)["Accounts"]
    rows = list(ws.iter_rows(values_only=True))
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def check(condition: bool, label: str) -> None:
    print(("PASS  " if condition else "FAIL  ") + label)
    if not condition:
        raise SystemExit(1)


async def main() -> None:
    al.google_search = fake_search
    al.fetch_page = fake_fetch
    al._brief_agent = Agent(FunctionModel(scripted_model), output_type=al.AccountBrief,
                            instructions=al.BRIEF_INSTRUCTIONS)

    work = Path(tempfile.mkdtemp())
    src = work / "accounts.csv"
    with src.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Account ID", "Company Name", "Website", "Owner"])
        w.writerow(["A-1", "Acme Support", "https://www.acmesupport.com/about", "BDR A"])
        w.writerow(["A-2", "Northstar Logistics", "northstar.io", "BDR B"])
        w.writerow(["A-3", "", "blank.com", "BDR A"])
        w.writerow(["A-4", "Acme Support", "acmesupport.com", "BDR B"])
        w.writerow(["A-5", "Cedar Works", "", "BDR A"])
        w.writerow(["A-6", "Bright Call", "brightcall.com", "BDR B"])
    before = fingerprint(src)
    out = work / "accounts_researched.xlsx"

    # Run 1: quota runs out on the last company.
    QUOTA_ON.add("Bright Call")
    counts = await al.run_list(src, out, focus="contact center")
    rows = read_out(out)
    check(fingerprint(src) == before, "input file unchanged")
    check(list(rows[0])[:4] == ["Account ID", "Company Name", "Website", "Owner"], "original columns kept, in order")
    check(rows[0]["Research Status"] == "Done", "row 1 researched")
    news = rows[0]["Recent News"]
    check("fake URL" not in news, "point citing only an invented URL is dropped")
    check("Mixed" in news and "made-up" not in rows[0]["Sources"], "mixed point kept with its real source only")
    check("jane.doe" not in rows[0]["Priorities"] and "555" not in rows[0]["Priorities"], "email and phone removed")
    check("2025-2026" in rows[0]["Team & Hiring Signals"], "year ranges are not mistaken for phone numbers")
    check(rows[0]["Talking Point"].startswith("• =HYPERLINK"), "formula-like text stored as text")
    check(rows[0]["Focus Fit"] and "300-seat" in rows[0]["Focus Fit"], "focus column filled")
    check(all("[" in line for line in rows[0]["Recent News"].splitlines()), "every point carries source numbers")
    check(rows[1]["Research Status"] == "Check match", "look-alike company flagged for a human")
    check(rows[2]["Research Status"] == "Skipped: no company name", "blank company skipped")
    check(rows[3]["Research Status"] == "Skipped: same company as row 2", "repeated company skipped")
    check(any("site:acmesupport.com" in q for q in SEARCH_LOG), "website used to find the company's own pages")
    check(rows[4]["Research Status"] == "Done", "company without a website still researched")
    check(rows[5]["Research Status"].startswith("Failed:") and "quota" in rows[5]["Research Status"],
          "quota stop recorded on the row")
    check(counts["done"] == 2 and counts["check"] == 1 and counts["failed"] == 1, f"counts {counts}")

    ws = load_workbook(out)["Accounts"]
    cell = ws.cell(row=2, column=list(rows[0]).index("Talking Point") + 1)
    check(cell.data_type == "s", "talking point cell is text, not a formula")

    # Refuses to clobber: no --resume, and output == input.
    for kwargs, label in (({}, "existing output needs --resume"), ({"resume": True}, "output can't be the input")):
        try:
            await al.run_list(src, out if not kwargs else src, **kwargs)
            check(False, label)
        except SystemExit:
            check(True, label)

    # Run 2: quota is back; resume does only the unfinished row.
    QUOTA_ON.clear()
    SEARCH_LOG.clear()
    counts = await al.run_list(src, out, focus="contact center", resume=True)
    rows = read_out(out)
    check(rows[5]["Research Status"] == "Done", "resume finished the failed row")
    check(counts["already"] == 3 and counts["done"] == 1, f"resume skipped finished rows {counts}")
    check(all("Acme" not in q for q in SEARCH_LOG), "no repeat searches for finished rows")
    check(fingerprint(src) == before, "input still unchanged")

    # Limit.
    out2 = work / "limited.xlsx"
    counts = await al.run_list(src, out2, limit=1)
    check(counts["done"] + counts["check"] == 1, "--limit stops after N rows")

    # Missing company column.
    bad = work / "bad.csv"
    bad.write_text("Domain,Owner\nacme.com,BDR A\n", encoding="utf-8")
    try:
        await al.run_list(bad, work / "bad_out.xlsx")
        check(False, "missing company column stops the run")
    except SystemExit as exc:
        check("company column" in str(exc), "missing company column stops the run with a clear message")

    print("\nAll checks passed. Sample output:", out)


if __name__ == "__main__":
    asyncio.run(main())
