from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

from madp_validation import ROOT, rel


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _anchor_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def _anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            if heading:
                anchors.add(_anchor_slug(heading))
    return anchors


def main() -> int:
    docs = [ROOT / "README.md", *sorted((ROOT / "protocol").glob("*.md"))]
    problems: list[str] = []
    checked = 0

    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip()
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            checked += 1
            path_part, _, anchor = target.partition("#")
            if path_part:
                candidate = (doc.parent / unquote(path_part)).resolve()
            else:
                candidate = doc.resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                problems.append(f"{rel(doc)} -> {target}: outside repository")
                continue
            if not candidate.exists():
                problems.append(f"{rel(doc)} -> {target}: missing file")
                continue
            if anchor and anchor not in _anchors(candidate):
                problems.append(f"{rel(doc)} -> {target}: missing anchor")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"markdown links: {checked} checked, PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

