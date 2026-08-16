"""Turn a ResearchReport into the markdown the user actually reads."""

from __future__ import annotations

from datetime import datetime, timezone

from research_models import ResearchReport, Section


def _section_markdown(section: Section) -> str:
    lines = [f"## {section.angle}", "", section.summary, ""]
    for finding in section.findings:
        lines.append(f"**{finding.claim}**")
        lines.append("")
        lines.append(finding.detail)
        lines.append("")
        for source in finding.evidence:
            lines.append(f"- Evidence: [{source.title}]({source.url})")
        lines.append("")
    return "\n".join(lines)


def _bullets(items: list[str], empty: str) -> str:
    return "\n".join(f"- {item}" for item in items) if items else f"- {empty}"


def render_markdown(report: ResearchReport) -> str:
    subject = report.subject
    header = [f"# Research report: {subject.display_name}", ""]
    facts = [f"**Request:** {report.query}"]
    if subject.ticker:
        facts.append(f"**Ticker:** {subject.ticker}")
    if subject.sector:
        facts.append(f"**Sector:** {subject.sector}")
    if subject.context_keywords:
        facts.append(f"**Context:** {', '.join(subject.context_keywords)}")
    facts.append(f"**Generated:** {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}")
    header.append("  \n".join(facts))

    if report.skipped_angles:
        header.append(
            "> **Partial report.** These angles could not be researched and are "
            f"missing below: {', '.join(report.skipped_angles)}."
        )

    parts = [
        "\n".join(header),
        "## Executive summary",
        report.synthesis.executive_summary,
        *[_section_markdown(s) for s in report.sections],
        "## Risks and uncertainties",
        _bullets(report.synthesis.risks_and_uncertainties, "None identified."),
        "## Conflicting information",
        _bullets(report.synthesis.conflicting_information, "No conflicts found between sources."),
        "## What to watch next",
        _bullets(report.synthesis.what_to_watch_next, "Nothing specific identified."),
        "## Sources",
        "\n".join(
            f"{i}. [{s.title}]({s.url})" for i, s in enumerate(report.sources, start=1)
        ),
    ]
    return "\n\n".join(parts).strip() + "\n"
