"""Show which sites a report's citations came from: python sources.py report.md

Source quality is the thing worth checking before trusting a report, and it is
much easier to judge from a host histogram than by reading 20 evidence bullets.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

EVIDENCE = re.compile(r"- Evidence: \[.*?\]\((.*?)\)")


def host_counts(markdown: str) -> Counter[str]:
    return Counter(urlparse(url).netloc for url in EVIDENCE.findall(markdown))


def main(path: Path) -> None:
    if not path.is_file():
        raise SystemExit(f"No such report: {path}")
    counts = host_counts(path.read_text(encoding="utf-8"))
    if not counts:
        raise SystemExit(f"{path} has no evidence bullets — is it a report?")
    total = sum(counts.values())
    print(f"{path.name}: {total} citations across {len(counts)} sites\n")
    for host, n in counts.most_common():
        print(f"{n:>3}  {host}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main(Path(sys.argv[1] if len(sys.argv) > 1 else "report.md"))
