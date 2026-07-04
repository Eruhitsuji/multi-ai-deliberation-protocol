from __future__ import annotations

import re
import sys

from madp_validation import load_yaml_text
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
    "protocol/MADP-v0.2.5-rc.2.md",
    "protocol/GLOSSARY-v0.2.5-rc.2.md",
    "schemas/session-state-v0.2.5-rc.2.schema.yaml",
]
DISALLOWED_CANONICAL_PATHS = [
    "protocol/MADP-v0.2.5-draft.md",
    "protocol/GLOSSARY-v0.2.5-draft.md",
    "schemas/session-state-v0.2.5-draft.schema.yaml",
    "protocol/MADP-v0.2.5-rc.1.md",
    "protocol/GLOSSARY-v0.2.5-rc.1.md",
    "schemas/session-state-v0.2.5-rc.1.schema.yaml",
]
PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
YAML_FENCE_RE = re.compile(r"```yaml\n(.*?)\n```", re.DOTALL)
BUNDLE_URL_TEMPLATE = "https://{{MADP_GITHUB_OWNER}}.github.io/{{MADP_GITHUB_REPOSITORY}}/bootstrap/complete-protocol-bundle.txt"


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
        if "MADP-v0.2.5-rc.2" not in text:
            problems.append(f"{rel(path)}: missing MADP-v0.2.5-rc.2")
        if "informative implementation aid" not in text:
            problems.append(f"{rel(path)}: missing informative implementation aid statement")

    load_text = texts.get("load-protocol-from-github.md", "")
    for canonical_path in REQUIRED_CANONICAL_PATHS:
        if not (ROOT / canonical_path).exists():
            problems.append(f"repository path missing: {canonical_path}")
        if canonical_path not in load_text:
            problems.append(f"load-protocol-from-github.md: missing {canonical_path}")
    for disallowed_path in DISALLOWED_CANONICAL_PATHS:
        if disallowed_path in load_text:
            problems.append(f"load-protocol-from-github.md: disallowed non-current canonical path {disallowed_path}")

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
    recovery_text = texts.get("recover-from-load-failure.md", "")
    if BUNDLE_URL_TEMPLATE not in readme_text:
        problems.append("bootstrap/README.md: missing complete bundle URL template")
    if BUNDLE_URL_TEMPLATE not in recovery_text:
        problems.append("recover-from-load-failure.md: missing complete bundle URL template")
    for name, text in {"README.md": readme_text, "recover-from-load-failure.md": recovery_text}.items():
        for line in text.splitlines():
            if "complete-protocol-bundle.txt" in line and "{{MADP_COMMIT_SHA}}" in line:
                problems.append(f"{name}: Pages bundle URL must not use MADP_COMMIT_SHA")
    if "all_required_files_read: false" not in recovery_text:
        problems.append("recover-from-load-failure.md: missing all_required_files_read: false")
    if "PASTED_TEXT" not in recovery_text:
        problems.append("recover-from-load-failure.md: missing PASTED_TEXT access method")
    if "UPLOADED_FILE" not in recovery_text:
        problems.append("recover-from-load-failure.md: missing UPLOADED_FILE access method")
    required_recovery_markers = [
        "Do not begin normal MADP deliberation until all four required files have been completely read.",
        "If only part of the bundle is pasted, keep `all_required_files_read: false`.",
        "Do not fill missing content from general knowledge or inference.",
        "Take `repository_commit` only from `BEGIN_MADP_BUNDLE_METADATA.source_commit`",
        "Do not select a repository commit by searching the canonical file contents for a 40-character hexadecimal string.",
    ]
    for marker in required_recovery_markers:
        if marker not in recovery_text:
            problems.append(f"recover-from-load-failure.md: missing recovery fail-closed instruction {marker!r}")
    if "BEGIN_MADP_BUNDLE_METADATA.source_commit" not in readme_text:
        problems.append("bootstrap/README.md: missing bundle metadata source_commit guidance")
    if "Do not select a repository commit by searching the canonical file contents for a 40-character hexadecimal string." not in readme_text:
        problems.append("bootstrap/README.md: missing 40-character SHA search prohibition")

    join_text = texts.get("join-as-participant.md", "")
    required_join_markers = [
        "exactly one YAML document",
        "Do not emit prose before or after the YAML block",
        "Do not create nested or multiple code fences",
        "structural self-check",
        "parseable as one YAML mapping",
    ]
    for marker in required_join_markers:
        if marker not in join_text:
            problems.append(f"join-as-participant.md: missing serialization instruction {marker!r}")

    shape_match = re.search(r"## Required Response Shape\s+(.*?)(?:\n## |\Z)", join_text, re.DOTALL)
    if not shape_match:
        problems.append("join-as-participant.md: missing Required Response Shape section")
    else:
        fences = YAML_FENCE_RE.findall(shape_match.group(1))
        if not fences:
            problems.append("join-as-participant.md: Required Response Shape has no yaml code fence")
        else:
            data = load_yaml_text(fences[0], "bootstrap/join-as-participant.md Required Response Shape")
            if not isinstance(data, dict) or list(data.keys()) != ["PARTICIPANT_RESPONSE"]:
                problems.append("join-as-participant.md: Required Response Shape top-level key is not only PARTICIPANT_RESPONSE")

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
    if "MADP-v0.2.5-draft" in combined or "0.2.5-draft" in combined:
        problems.append("bootstrap prompts still contain draft version text")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    print("bootstrap prompts: consistency PASS")
    print("bootstrap placeholders:", ", ".join(sorted(placeholders)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
