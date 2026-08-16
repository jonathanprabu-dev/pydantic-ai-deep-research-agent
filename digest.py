"""Build one index over every report in a folder: python digest.py

The research bar has no memory — each run is a fresh web search that cannot see
previous reports. This stitches the reports already on disk into a single
document: the query, the angles, the citation spread, and the executive summary
for each, in the order they were run.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from sources import host_counts

TITLE = re.compile(r"^# Research report: (.+)$", re.M)
REQUEST = re.compile(r"^\*\*Request:\*\* (.+)$", re.M)
GENERATED = re.compile(r"^\*\*Generated:\*\* (.+)$", re.M)
SECTIONS = re.compile(r"^## (.+)$", re.M)
# Everything between the executive summary heading and the next heading.
SUMMARY = re.compile(r"^## Executive summary\s*\n+(.*?)(?=^## )", re.M | re.S)

# Not report sections — the fixed scaffolding every report ends with.
BOILERPLATE = {
    "Executive summary",
    "Risks and uncertainties",
    "Conflicting information",
    "What to watch next",
    "Sources",
}


def describe(path: Path) -> str | None:
    """Render one report's entry, or None if the file isn't a report."""
    text = path.read_text(encoding="utf-8")
    title = TITLE.search(text)
    summary = SUMMARY.search(text)
    if not title or not summary:
        return None

    angles = [s for s in SECTIONS.findall(text) if s not in BOILERPLATE]
    hosts: Counter[str] = host_counts(text)
    top = ", ".join(f"{h} ({n})" for h, n in hosts.most_common(4))
    request = REQUEST.search(text)

    lines = [
        f"## {title.group(1)}",
        "",
        f"`{path.name}`",
        "",
    ]
    if request:
        lines += [f"**Query:** {request.group(1).strip()}", ""]
    lines += [
        f"**Angles:** {' · '.join(angles) if angles else 'none'}",
        "",
        f"**Citations:** {sum(hosts.values())} across {len(hosts)} sites — {top}",
        "",
        summary.group(1).strip(),
        "",
    ]
    return "\n".join(lines)


def find_reports(folders: list[Path], skip: Path | None = None) -> list[tuple[str, Path]]:
    """Return (title, path) for every report across these folders, oldest first.

    Sorted on each report's own Generated stamp: file mtimes reflect when a file
    was copied, not when the research ran.
    """
    found: list[tuple[str, str, Path]] = []
    seen: set[str] = set()
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.md")):
            if skip and path.resolve() == skip.resolve():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            # A real report *begins* with its title. Generated documents like
            # all-reports.md merely contain report headings, and would otherwise
            # be re-ingested as reports themselves.
            title = TITLE.match(text)
            if not title:
                continue
            # research.py always writes report.md too, so the newest report is on
            # disk twice. Keep whichever copy is seen first and skip the duplicate.
            fingerprint = text[:400]
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            stamp = GENERATED.search(text)
            found.append((stamp.group(1).strip() if stamp else "", title.group(1), path))

    found.sort(key=lambda row: row[0])
    return [(title, path) for _, title, path in found]


def build(folders: list[Path], out: Path) -> int:
    """Write the digest over every report in these folders. Returns the count."""
    entries = [e for _, path in find_reports(folders, skip=out) if (e := describe(path))]
    if not entries:
        return 0
    header = [
        "# Research digest",
        "",
        f"{len(entries)} reports, oldest first. Each entry names the full report "
        "on disk; open that for the findings and their evidence.",
        "",
    ]
    out.write_text("\n".join(header) + "\n" + "\n---\n\n".join(entries), encoding="utf-8")
    return len(entries)


def main(folder: Path, out: Path) -> None:
    count = build([folder], out)
    if not count:
        raise SystemExit(f"No reports found in {folder}")
    print(f"Wrote {out} — {count} reports")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "."), Path("digest.md"))
