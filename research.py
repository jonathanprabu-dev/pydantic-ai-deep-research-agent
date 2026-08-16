"""The deep research pipeline.

Fixed stages orchestrated in Python, one small typed agent per stage:

    1. discovery  - one Google search on the raw input
    2. plan       - resolve the subject, pick 3-4 non-overlapping angles
    3. deep dives - one Google search + page fetches + analysis per angle, in parallel
    4. synthesis  - the cross-cutting parts, over the finished sections
    5. render     - markdown (see report.py)

Deliberately not one agent holding tools: the stages are fixed, and structured
outputs per stage are what keep every claim tied to a real URL.
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import AsyncIterator
from pathlib import Path
from urllib.parse import urlparse

from pydantic_ai import Agent
from pydantic_ai.exceptions import ModelHTTPError

from agent import REQUESTS_PER_RUN, check_backend, get_model, model_spec
from browser import close_browser, fetch_page, google_search
from report import render_markdown
from research_models import (
    Angle,
    Finding,
    ResearchPlan,
    ResearchReport,
    SearchResult,
    Section,
    Synthesis,
)

ANGLE_COUNT = 4
PAGES_PER_ANGLE = 2
RESULTS_PER_SEARCH = 10

# Filings and company statements beat commentary about them.
PRIMARY_HOSTS = ("sec.gov", "investor.", "ir.", "investors.")
PRIMARY_SUFFIXES = (".gov", "/investor-relations")
REPUTABLE_HOSTS = (
    "reuters.com",
    "apnews.com",
    "bloomberg.com",
    "wsj.com",
    "ft.com",
    "cnbc.com",
    "economist.com",
    "nature.com",
    "science.org",
    "arstechnica.com",
    "theverge.com",
)
LOW_QUALITY_HOSTS = (
    "pinterest.",
    "quora.com",
    "facebook.com",
    "reddit.com",
    "tiktok.com",
    "youtube.com",
    # Self-publishing platforms. A LinkedIn Pulse post ranks like an analyst note
    # and reads like one, but nobody edited it.
    "linkedin.com",
    "scribd.com",
    "slideshare.net",
    "medium.com",
)


PLANNER_INSTRUCTIONS = f"""\
You plan deep research. You are given a user's raw input and the results of one
Google search on it.

First decide what the subject is:
- If it names a public company or an exchange ticker, set kind="ticker" and use the
  search results to resolve the real company name, ticker, sector and the keywords
  that give it context (e.g. NVDA -> NVIDIA Corporation, semiconductors, GPUs, AI).
  Resolve it from the search results in front of you, never from memory.
- Otherwise set kind="query" and describe the topic.

Then pick exactly {ANGLE_COUNT} research angles. They must not overlap: each one
should send you to different sources and answer a different question.

For a company or ticker, use these angles:
  1. SWOT analysis
  2. last 12-month stock performance
  3. competition and market positioning
  4. latest quarterly results and forward guidance
Set prefer_primary_sources=true on angles 2 and 4, which need filings, earnings
releases and investor-relations pages rather than commentary.

For a general query, derive {ANGLE_COUNT} distinct angles from the search snippets
covering the mechanism or substance, the current state of play, the counter-case or
criticism, and what happens next.

Each angle needs a google_query written the way a researcher would actually type it.\
"""

ANALYST_INSTRUCTIONS = """\
You are a research analyst writing one section of a report.

You are given a research angle, a list of search results, and the full text of some
of those pages. Extract the substance: concrete facts, numbers, dates, named parties,
and specific claims. Prefer figures over adjectives.

Rules you must follow:
- Every finding must cite at least one source, and every cited URL must be copied
  exactly from the sources you were given. Never write a URL that is not in that list.
- Prefer primary sources (filings, earnings releases, investor relations, official
  statements) over commentary, especially for anything financial.
- If a page contradicts another, say so in the finding rather than picking a winner.
- If the evidence is thin, write fewer findings. Do not pad, and do not state
  anything the supplied material does not support.\
"""

SYNTHESIS_INSTRUCTIONS = """\
You are given the finished sections of a research report. Write only the
cross-cutting parts: an executive summary, the risks and uncertainties, any places
where sources conflict, and a list of what to watch next.

The executive summary must stand alone for a reader who reads nothing else.
For conflicting information, name the specific disagreement; if the sections do not
conflict, say so plainly in one entry rather than inventing tension.
"what to watch next" should be concrete and checkable - upcoming dates, releases,
decisions, or numbers that would change the picture.\
"""


def friendly_error(exc: Exception) -> str:
    """Turn a provider error into something a person can act on.

    The 429 body is a wall of JSON, and the important part — whether this is a
    *daily* cap, which no amount of retrying will clear, or a passing per-minute
    limit — is buried in it.
    """
    if not isinstance(exc, ModelHTTPError) or exc.status_code != 429:
        return f"Error: {exc}"

    provider, name = model_spec()
    body = str(exc.body).lower()
    daily = "perday" in body or "per day" in body or "per-day" in body

    if provider == "google":
        limits = "20 requests/day on the free tier"
        fix = (
            "Wait for the daily reset (midnight Pacific), use a key from a different "
            "Google Cloud project, or enable billing."
        )
    else:
        limits = "50 requests/day on free models, or 1000 once you've bought credits"
        fix = (
            "Wait for the daily reset, buy $10 of OpenRouter credits to raise the cap, "
            "or switch MODEL in .env to a paid model."
        )

    if daily:
        return (
            f"{name} is out of quota for today ({limits}). One research run costs "
            f"about {REQUESTS_PER_RUN}. {fix}"
        )
    return (
        f"{name} rate-limited the request even after backing off — this is the "
        "per-minute limit, not the daily one. Wait a minute and try again."
    )


def planner_agent() -> Agent[None, ResearchPlan]:
    return Agent(get_model(), output_type=ResearchPlan, instructions=PLANNER_INSTRUCTIONS)


def analyst_agent() -> Agent[None, Section]:
    return Agent(get_model(), output_type=Section, instructions=ANALYST_INSTRUCTIONS)


def synthesis_agent() -> Agent[None, Synthesis]:
    return Agent(get_model(), output_type=Synthesis, instructions=SYNTHESIS_INSTRUCTIONS)


def score_source(result: SearchResult, prefer_primary: bool) -> int:
    """Rank a result so primary sources actually get fetched, not just wished for."""
    host = urlparse(result.url).netloc.lower()
    path = urlparse(result.url).path.lower()
    score = 0
    is_primary = host.startswith(PRIMARY_HOSTS) or any(
        host.endswith(s) or s in path for s in PRIMARY_SUFFIXES
    )
    if is_primary:
        score += 6 if prefer_primary else 3
    if any(h in host for h in REPUTABLE_HOSTS):
        score += 3
    if any(h in host for h in LOW_QUALITY_HOSTS):
        score -= 5
    if result.snippet:
        score += 1
    return score


def _render_sources(results: list[SearchResult]) -> str:
    return "\n".join(
        f"- {r.title}\n  URL: {r.url}\n  Snippet: {r.snippet}" for r in results
    )


def _scope_query(angle_query: str, prefer_primary: bool) -> str:
    """Push financial angles towards filings and company statements."""
    if not prefer_primary:
        return angle_query
    return f"{angle_query} investor relations OR earnings release OR site:sec.gov"


def _keep_real_citations(section: Section, allowed: dict[str, str]) -> Section:
    """Drop any citation whose URL was not among the sources we supplied.

    Instructions alone do not stop a model inventing a plausible URL, and a
    fabricated citation is worse than a missing one.
    """
    findings: list[Finding] = []
    for finding in section.findings:
        evidence = [e for e in finding.evidence if e.url in allowed]
        for item in evidence:
            item.title = allowed[item.url] or item.title
        if evidence:
            findings.append(finding.model_copy(update={"evidence": evidence}))
    return section.model_copy(update={"findings": findings})


async def _research_angle(
    index: int, angle: Angle, subject_name: str
) -> tuple[int, Section | None, list[SearchResult], Exception | None]:
    """Search, fetch and analyse one angle, never raising.

    A run costs a meaningful slice of the daily quota, so one dead angle must not
    throw away the three that worked. The index comes back with the result so the
    report keeps the planned order regardless of finishing order.
    """
    try:
        section, sources = await _run_angle(angle, subject_name)
    except Exception as exc:
        return index, None, [], exc
    return index, section, sources, None


async def _run_angle(angle: Angle, subject_name: str) -> tuple[Section, list[SearchResult]]:
    """Search, fetch and analyse one angle."""
    results = await google_search(
        _scope_query(angle.google_query, angle.prefer_primary_sources), RESULTS_PER_SEARCH
    )
    ranked = sorted(results, key=lambda r: score_source(r, angle.prefer_primary_sources), reverse=True)
    top = ranked[:PAGES_PER_ANGLE]

    pages = await asyncio.gather(*(fetch_page(r.url) for r in top))
    page_text = "\n\n".join(
        f"### PAGE: {r.title}\nURL: {r.url}\n{text}"
        for r, text in zip(top, pages)
        if text
    )

    prompt = (
        f"Subject: {subject_name}\n"
        f"Angle: {angle.name}\n"
        f"Why this angle: {angle.rationale}\n\n"
        f"SEARCH RESULTS:\n{_render_sources(results)}\n\n"
        f"FULL PAGE TEXT:\n{page_text or '(no pages could be fetched)'}"
    )
    section = (await analyst_agent().run(prompt)).output
    allowed = {r.url: r.title for r in results}
    return _keep_real_citations(section, allowed), results


async def run_research(query: str) -> AsyncIterator[tuple[str, ResearchReport | None]]:
    """Run the whole pipeline, yielding (status, report) as it goes.

    The report is None until the final yield. A run takes minutes, so the caller
    needs something to show meanwhile.
    """
    query = query.strip()
    if not query:
        yield "Nothing to research.", None
        return

    yield "Opening Chrome and running the discovery search…", None
    discovery = await google_search(query, RESULTS_PER_SEARCH)

    yield f"Read {len(discovery)} results. Working out the subject and the angles…", None
    plan = (
        await planner_agent().run(
            f"User input: {query}\n\nDISCOVERY SEARCH RESULTS:\n{_render_sources(discovery)}"
        )
    ).output
    subject = plan.subject
    angles = plan.angles[:ANGLE_COUNT]

    kind = "ticker" if subject.kind == "ticker" else "topic"
    yield (
        f"Subject: **{subject.display_name}** ({kind}). "
        f"Researching {len(angles)} angles: {', '.join(a.name for a in angles)}…",
        None,
    )

    tasks = [
        asyncio.create_task(_research_angle(i, a, subject.display_name))
        for i, a in enumerate(angles)
    ]
    done = 0
    completed: list[tuple[int, Section]] = []
    failures: list[str] = []
    last_error: Exception | None = None
    all_sources: list[SearchResult] = list(discovery)
    try:
        for task in asyncio.as_completed(tasks):
            index, section, results, error = await task
            done += 1
            if error is not None:
                failures.append(angles[index].name)
                last_error = error
                yield (
                    f"Finished {done}/{len(angles)} angles — "
                    f"{angles[index].name} failed: {friendly_error(error)}",
                    None,
                )
                continue
            completed.append((index, section))
            all_sources.extend(results)
            yield f"Finished {done}/{len(angles)} angles ({section.angle}).", None
    finally:
        for task in tasks:
            task.cancel()

    if not completed:
        raise RuntimeError(
            "Every angle failed. "
            + (friendly_error(last_error) if last_error else "No sections were produced.")
        )

    # Restore the planned order; as_completed returns them in whatever order they finish.
    completed.sort(key=lambda pair: pair[0])
    sections = [section for _, section in completed]

    yield "Synthesising the report…", None
    sections_text = "\n\n".join(
        f"## {s.angle}\n{s.summary}\n"
        + "\n".join(f"- {f.claim} ({f.detail})" for f in s.findings)
        for s in sections
    )
    synthesis = (
        await synthesis_agent().run(
            f"Subject: {subject.display_name}\nOriginal request: {query}\n\n{sections_text}"
        )
    ).output

    deduped: dict[str, SearchResult] = {}
    for source in all_sources:
        deduped.setdefault(source.url, source)

    yield "Done.", ResearchReport(
        query=query,
        subject=subject,
        sections=sections,
        synthesis=synthesis,
        sources=list(deduped.values()),
        skipped_angles=failures,
    )


async def _main(query: str) -> None:
    error = check_backend()
    if error:
        raise SystemExit(error)
    report = None
    try:
        async for status, result in run_research(query):
            print(f"[{status}]", file=sys.stderr)
            report = result or report
    except Exception as exc:
        raise SystemExit(friendly_error(exc))
    finally:
        await close_browser()
    if report is None:
        raise SystemExit("No report was produced.")
    markdown = render_markdown(report)
    Path(__file__).parent.joinpath("report.md").write_text(markdown, encoding="utf-8")
    print(markdown)


if __name__ == "__main__":
    # Reports and source titles are full Unicode; the Windows console is cp1252.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(_main(" ".join(sys.argv[1:]) or "NVDA"))
