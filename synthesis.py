"""Fold every report on disk into one document organised by topic.

The digest is per-report and chronological: it tells you what each run found.
This is the other cut — findings regrouped under themes that cross runs, which
is where the useful connections live, since no single run can see the others.

    python synthesis.py            # every report next to the code
    python synthesis.py path\\to\\reports
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path

from pydantic import Field
from pydantic_ai import Agent

from agent import check_backend, get_model
from digest import REQUEST, TITLE, find_reports
from research_models import Nested, SourceRef

# Findings in a rendered report: a bold claim, then its evidence links.
CLAIM = re.compile(r"^\*\*(.+?)\*\*$", re.M)
EVIDENCE = re.compile(r"^- Evidence: \[(.*?)\]\((.*?)\)$", re.M)


class TopicList(Nested):
    """Stage 1: just the topic names.

    Deliberately shallow. One big nested output — topics containing points
    containing sources — is rejected outright by free providers: one caps tool
    grammar size, another refuses the `$defs` that nested models generate, and the
    one that accepts it stalls generating the whole thing at once. Every stage here
    stays small, and the prose stages use no schema at all.
    """

    topics: list[str] = Field(description="Four to six topic names that cross the reports.")


TOPICS_INSTRUCTIONS = """\
You are given the findings of several research reports, condensed to claims and
sources. Choose four to six topics to organise them by.

Good topics cross reports rather than restating one report each, and group findings
that belong together. Return only the topic names, most important first.\
"""

SECTION_INSTRUCTIONS = """\
You are writing one topic of a cross-report synthesis, in markdown.

Cover only your assigned topic, drawing on findings from any report. The value is in
connections no single report could make: where two reports reach the same conclusion
from different directions, where a later report corrects an earlier one, where
findings compound. Merge duplicates into one point rather than repeating them.

Format exactly like this, and output nothing else — no heading for the topic itself,
no preamble:

A short paragraph on what the reports collectively establish about this topic.

**A specific claim, with numbers and dates where they exist.**

Two or three sentences of supporting context.

- Evidence: [Source Title](https://exact-url-from-the-sources)

Rules:
- Three to six claims, most important first.
- Every claim must be followed by at least one Evidence line.
- Every URL must be copied exactly from the sources you were given. Never write a
  URL that is not in that list.
- Prefer concrete facts over general statements.\
"""

CLOSING_INSTRUCTIONS = """\
You are given the findings of several research reports.

Write two markdown lists and nothing else:

## Contradictions and corrections
- Where reports disagree, or where a later report overturned an earlier one. Be
  specific and name the reports. If there are none, say so in one bullet.

## Open questions
- What the reports genuinely do not answer. Not topics you would like more detail
  on — things the material cannot tell you.\
"""


def condense(path: Path) -> tuple[str, dict[str, str]]:
    """Reduce one report to its claims and citations, plus its allowed URL set."""
    text = path.read_text(encoding="utf-8")
    title = TITLE.search(text)
    request = REQUEST.search(text)
    allowed = {url: name for name, url in EVIDENCE.findall(text)}

    lines = [f"### REPORT: {title.group(1) if title else path.name}"]
    if request:
        lines.append(f"Original query: {request.group(1).strip()}")
    # Walk the body so each claim keeps the evidence that follows it.
    current: list[str] = []
    for line in text.splitlines():
        claim = CLAIM.match(line)
        evidence = EVIDENCE.match(line)
        if claim:
            current = [f"- CLAIM: {claim.group(1)}"]
            lines.extend(current)
        elif evidence and current:
            lines.append(f"    SOURCE: {evidence.group(1)} | {evidence.group(2)}")
    return "\n".join(lines), allowed


def keep_real_citations(markdown: str, allowed: dict[str, str]) -> str:
    """Strip Evidence lines whose URL was not in the source material.

    The schema can no longer enforce this, so it is enforced on the text. A
    fabricated citation is worse than a missing one.
    """
    kept = []
    for line in markdown.splitlines():
        evidence = EVIDENCE.match(line.strip())
        if evidence and evidence.group(2) not in allowed:
            continue
        if evidence:
            kept.append(f"- Evidence: [{allowed[evidence.group(2)]}]({evidence.group(2)})")
        else:
            kept.append(line)
    return "\n".join(kept).strip()


async def build(folders: list[Path], out: Path) -> int:
    """Write the topic synthesis. Returns the number of reports folded in.

    One small call to choose topics, then one prose call per topic, then one for
    the closing lists. Small and shallow beats one large nested request.
    """
    reports = [(t, p) for t, p in find_reports(folders) if p.resolve() != out.resolve()]
    if not reports:
        return 0

    blocks, allowed = [], {}
    for _, path in reports:
        block, urls = condense(path)
        blocks.append(block)
        allowed.update(urls)
    material = "\n\n".join(blocks)

    model = get_model()
    topics = (
        await Agent(model, output_type=TopicList, instructions=TOPICS_INSTRUCTIONS).run(material)
    ).output.topics
    print(f"Topics: {', '.join(topics)}", file=sys.stderr)

    writer = Agent(model, instructions=SECTION_INSTRUCTIONS)
    sections = await asyncio.gather(
        *(writer.run(f"YOUR TOPIC: {name}\n\nMATERIAL:\n{material}") for name in topics)
    )
    closing = (await Agent(model, instructions=CLOSING_INSTRUCTIONS).run(material)).output

    parts = [
        "# Research synthesis by topic",
        "",
        f"Findings from {len(reports)} reports, regrouped by theme:",
        "",
        "\n".join(f"- {t}" for t, _ in reports),
    ]
    for name, section in zip(topics, sections):
        parts += ["", f"## {name}", "", keep_real_citations(section.output, allowed)]
    parts += ["", keep_real_citations(closing, allowed)]

    out.write_text("\n".join(parts).strip() + "\n", encoding="utf-8")
    return len(reports)


async def _main(folder: Path) -> None:
    if error := check_backend():
        raise SystemExit(error)
    out = Path("synthesis.md")
    count = await build([folder], out)
    if not count:
        raise SystemExit(f"No reports found in {folder}")
    print(f"Wrote {out} — {count} reports folded into one document")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    asyncio.run(_main(Path(sys.argv[1] if len(sys.argv) > 1 else ".")))
