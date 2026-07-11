from __future__ import annotations

import re
import sys

from madp_validation import ROOT, load_yaml_text, rel

BOOTSTRAP_DIR = ROOT / "bootstrap"
VERSION = "MADP-v0.3.0-alpha.2"
BOOTSTRAP_FILES = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
REQUIRED_CANONICAL_PATHS = [
    "README-v0.3.0-alpha.2.md",
    "protocol/MADP-v0.3.0-alpha.2.md",
    "protocol/GLOSSARY-v0.3.0-alpha.2.md",
    "schemas/v0.3.0-alpha.2/command.schema.yaml",
    "schemas/v0.3.0-alpha.2/command-registry.schema.yaml",
    "schemas/v0.3.0-alpha.2/todo.schema.yaml",
    "schemas/v0.3.0-alpha.2/context-package.schema.yaml",
    "schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml",
    "schemas/v0.3.0-alpha.2/review.schema.yaml",
    "schemas/v0.3.0-alpha.2/relay.schema.yaml",
    "registries/v0.3.0-alpha.2/commands.yaml",
    "docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md",
]
DISALLOWED_CURRENT_PATHS = [
    "README-v0.3.0-alpha.1.md",
    "protocol/MADP-v0.3.0-alpha.1.md",
    "protocol/GLOSSARY-v0.3.0-alpha.1.md",
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
        if "bootstrap_version: 0.3" not in text:
            problems.append(f"{rel(path)}: missing bootstrap_version: 0.3")
        if VERSION not in text:
            problems.append(f"{rel(path)}: missing {VERSION}")
        if "informative implementation aid" not in text:
            problems.append(f"{rel(path)}: missing informative implementation aid statement")

    load_text = texts.get("load-protocol-from-github.md", "")
    for canonical_path in REQUIRED_CANONICAL_PATHS:
        if not (ROOT / canonical_path).exists():
            problems.append(f"repository path missing: {canonical_path}")
        if canonical_path not in load_text:
            problems.append(f"load-protocol-from-github.md: missing {canonical_path}")
    for old_path in DISALLOWED_CURRENT_PATHS:
        if old_path in load_text:
            problems.append(f"load-protocol-from-github.md: stale current path {old_path}")

    raw_urls = re.findall(r"https://raw\.githubusercontent\.com/[^\s)]+", load_text)
    if len(raw_urls) < len(REQUIRED_CANONICAL_PATHS):
        problems.append("load-protocol-from-github.md: expected pinned Raw URLs for all canonical files")
    for url in raw_urls:
        if "{{MADP_COMMIT_SHA}}" not in url or "/main/" in url or "/master/" in url:
            problems.append(f"Raw URL is not immutable-commit pinned: {url}")

    if "PROTOCOL_LOAD_REPORT" not in load_text or "all_required_files_read: true | false" not in load_text:
        problems.append("load-protocol-from-github.md: incomplete load-report contract")

    readme_text = texts.get("README.md", "")
    recovery_text = texts.get("recover-from-load-failure.md", "")
    for name, text in {"README.md": readme_text, "recover-from-load-failure.md": recovery_text}.items():
        if BUNDLE_URL_TEMPLATE not in text:
            problems.append(f"bootstrap/{name}: missing complete bundle URL template")
    required_recovery_markers = [
        "Do not begin normal MADP deliberation until all 12 required files have been completely read.",
        "If only part of the bundle is pasted, keep `all_required_files_read: false`.",
        "Do not fill missing content from general knowledge or inference.",
        "BEGIN_MADP_BUNDLE_METADATA.source_commit",
        "PASTED_TEXT",
        "UPLOADED_FILE",
    ]
    for marker in required_recovery_markers:
        if marker not in recovery_text:
            problems.append(f"recover-from-load-failure.md: missing {marker!r}")

    join_text = texts.get("join-as-participant.md", "")
    for marker in ["exactly one YAML document", "Do not emit prose before or after the YAML block", "Do not create nested or multiple code fences", "structural self-check", "parseable as one YAML mapping"]:
        if marker not in join_text:
            problems.append(f"join-as-participant.md: missing {marker!r}")
    shape_match = re.search(r"## Required Response Shape\s+(.*?)(?:\n## |\Z)", join_text, re.DOTALL)
    if not shape_match:
        problems.append("join-as-participant.md: missing Required Response Shape section")
    else:
        fences = YAML_FENCE_RE.findall(shape_match.group(1))
        if not fences:
            problems.append("join-as-participant.md: missing YAML response shape")
        else:
            data = load_yaml_text(fences[0], "bootstrap/join-as-participant.md Required Response Shape")
            if not isinstance(data, dict) or list(data.keys()) != ["PARTICIPANT_RESPONSE"]:
                problems.append("join-as-participant.md: response top-level key mismatch")

    placeholders = set()
    for name, text in texts.items():
        if name != "README.md":
            placeholders.update(PLACEHOLDER_RE.findall(text))
    for placeholder in sorted(placeholders):
        if placeholder not in readme_text:
            problems.append(f"bootstrap/README.md: missing placeholder documentation for {placeholder}")

    combined = "\n".join(texts.values())
    for marker in ["Do not claim user approval", "model convergence", "PROPOSE_ONLY", "all_required_files_read"]:
        if marker not in combined:
            problems.append(f"bootstrap prompts missing safety marker: {marker}")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"bootstrap prompts: {VERSION} consistency PASS")
    print("canonical bootstrap files:", len(REQUIRED_CANONICAL_PATHS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
