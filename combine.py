"""Concatenate every report into one document: python combine.py

Three cuts of the same material, for different jobs:

    digest.py     one summary per report        - what each run found
    synthesis.py  findings regrouped by topic   - what the runs say together
    combine.py    every report in full          - one file to read or print

Nothing here calls a model.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from digest import GENERATED, REQUEST, find_reports


def anchor(title: str) -> str:
    """GitHub-style anchor for a heading, so the contents list can link to it."""
    slug = "".join(c for c in title.lower() if c.isalnum() or c in " -").strip()
    return slug.replace(" ", "-")


def combine(folders: list[Path], out: Path) -> int:
    """Write every report into one file, oldest first. Returns the count."""
    reports = [(t, p) for t, p in find_reports(folders, skip=out)]
    if not reports:
        return 0

    contents = [
        "# Research reports",
        "",
        f"{len(reports)} reports in full, oldest first.",
        "",
        "## Contents",
        "",
    ]
    for i, (title, path) in enumerate(reports, 1):
        stamp = GENERATED.search(path.read_text(encoding="utf-8"))
        when = f" — {stamp.group(1).strip()}" if stamp else ""
        contents.append(f"{i}. [{title}](#{anchor(title)}){when}")

    bodies = []
    for title, path in reports:
        text = path.read_text(encoding="utf-8").strip()
        # Each report already opens with "# Research report: ...", which becomes
        # this document's section heading. Nothing to rewrite.
        bodies.append(f"{text}\n\n*Source file: `{path.name}`*")

    out.write_text("\n".join(contents) + "\n\n---\n\n" + "\n\n---\n\n".join(bodies) + "\n", encoding="utf-8")
    return len(reports)


def report_folders() -> list[Path]:
    """Where reports live: next to the code, and the app's temp folder."""
    temp = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "deep-research-reports"
    return [Path(__file__).parent, temp]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    folders = [Path(sys.argv[1])] if len(sys.argv) > 1 else report_folders()
    destination = Path("all-reports.md")
    count = combine(folders, destination)
    if not count:
        raise SystemExit(f"No reports found in {', '.join(str(f) for f in folders)}")
    size = destination.stat().st_size
    print(f"Wrote {destination} — {count} reports, {size:,} bytes")
