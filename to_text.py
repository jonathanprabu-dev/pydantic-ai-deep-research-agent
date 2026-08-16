"""Convert a report markdown file to plain text: python to_text.py all-reports.md

Markup is stripped, but citation URLs are kept inline as "Title (url)" — a
report whose sources are unreachable is not worth much.
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

from to_docx import BULLET, HEADING, NUMBERED, RULE

BOLD = re.compile(r"\*\*(.+?)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
CODE = re.compile(r"`(.+?)`")
LINK = re.compile(r"\[(.*?)\]\((.*?)\)")

WIDTH = 96


def _link(match: re.Match[str]) -> str:
    label, url = match.group(1), match.group(2)
    # In-page anchors are meaningless once the markdown is gone — keep the label.
    if url.startswith("#"):
        return label
    return f"{label} ({url})" if label else url


def strip_markup(text: str) -> str:
    """Plain prose, with link targets kept in parentheses."""
    text = LINK.sub(_link, text)
    text = BOLD.sub(r"\1", text)
    text = ITALIC.sub(r"\1", text)
    return CODE.sub(r"\1", text)


def wrap(text: str, indent: str = "") -> list[str]:
    """Wrap prose, but never break a line carrying a URL — it becomes unclickable."""
    if "http" in text or len(text) <= WIDTH:
        return [indent + text]
    return textwrap.wrap(
        text, width=WIDTH, initial_indent=indent, subsequent_indent=indent
    ) or [""]


def convert(markdown: Path, out: Path) -> Path:
    lines: list[str] = []

    for raw in markdown.read_text(encoding="utf-8").splitlines():
        raw = raw.rstrip()

        if not raw:
            lines.append("")
            continue

        if RULE.match(raw):
            lines += ["", "=" * WIDTH, ""]
            continue

        if heading := HEADING.match(raw):
            level, title = len(heading.group(1)), strip_markup(heading.group(2))
            lines.append("")
            if level == 1:
                lines += [title.upper(), "=" * min(len(title), WIDTH)]
            elif level == 2:
                lines += [title, "-" * min(len(title), WIDTH)]
            else:
                lines.append(title)
            lines.append("")
            continue

        if bullet := BULLET.match(raw):
            lines += wrap(f"- {strip_markup(bullet.group(1))}", "  ")
            continue

        if numbered := NUMBERED.match(raw):
            lines += wrap(f"{numbered.group(1)}. {strip_markup(numbered.group(2))}", "  ")
            continue

        lines += wrap(strip_markup(raw))

    # Collapse runs of blank lines left behind by stripped markup.
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    out.write_text(text + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    source = Path(sys.argv[1] if len(sys.argv) > 1 else "all-reports.md")
    if not source.is_file():
        raise SystemExit(f"No such file: {source}")
    written = convert(source, source.with_suffix(".txt"))
    print(f"Wrote {written} — {written.stat().st_size:,} bytes")
