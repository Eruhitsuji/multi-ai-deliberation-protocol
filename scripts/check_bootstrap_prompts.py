from __future__ import annotations

import re
import sys

from madp_validation import ROOT, rel


BOOTSTRAP_DIR = ROOT / "bootstrap"
BOOTSTRAP_FILES = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
REQUIRED_CANONICAL_PATHS = [
    "README.md",
    "protocol/MADP-v0.2.5-draft.md",
    "protocol/GLOSSARY-v0.2.5-draft.md",
    "schemas/session-state-v0.2.5-draft.schema.yaml",
]
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")


def main() -> int:
    problems: list[str] = []
    texts: dict[str, str] = {}

    for name in BOOTSTRAP_FILES:
        path = BOOTSTRAP_DIR / name
        if not path.exists():
            problems.append(f"missing {rel(path)}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        if "bootstrap_version: 0.1" not in text:
            problems.append(f"{rel(path)}: missing bootstrap_version: 0.1")
        if "MADP-v0.2.5-draft" not in text:
            problems.append(f"{rel(path)}: missing MADP-v0.2.5-draft")
        if "informative implementation aid" not in text:
            problems.append(f"{rel(path)}: missing informative implementation aid statement")

    load_text = texts.get("load-protocol-from-github.md", "")
    for canonical_path in REQUIRED_CANONICAL_PATHS:
        if not (ROOT / canonical_path).exists():
            problems.append(f"repository path missing: {canonical_path}")
        if canonical_path not in load_text:
            problems.append(f"load-protocol-from-github.md: missing {canonical_path}")

    raw_urls = re.findall(r"https://raw\.githubusercontent\.com/[^\s)]+", load_text)
    if len(raw_urls) < len(REQUIRED_CANONICAL_PATHS):
        problems.append("load-protocol-from-github.md: expected commit-pinned Raw URLs for all canonical files")
    for url in raw_urls:
        if "{{MADP_COMMIT_SHA}}" not in url:
            problems.append(f"Raw URL is not commit placeholder pinned: {url}")
        if "/main/" in url or "/master/" in url:
            problems.append(f"Raw URL uses movable branch: {url}")

    if "PROTOCOL_LOAD_REPORT" not in load_text:
        problems.append("load-protocol-from-github.md: missing PROTOCOL_LOAD_REPORT")
    if "all_required_files_read: true | false" not in load_text:
        problems.append("load-protocol-from-github.md: missing all_required_files_read output")

    readme_text = texts.get("README.md", "")
    placeholders = set()
    for name, text in texts.items():
        if name == "README.md":
            continue
        placeholders.update(PLACEHOLDER_RE.findall(text))
    for placeholder in sorted(placeholders):
        if placeholder not in readme_text:
            problems.append(f"bootstrap/README.md: missing placeholder documentation for {placeholder}")

    safety_markers = [
        "Do not claim user approval",
        "model convergence",
        "PROPOSE_ONLY",
        "all_required_files_read",
    ]
    combined = "\n".join(texts.values())
    for marker in safety_markers:
        if marker not in combined:
            problems.append(f"bootstrap prompts missing safety marker: {marker}")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print("bootstrap prompts: consistency PASS")
    print("bootstrap placeholders:", ", ".join(sorted(placeholders)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
