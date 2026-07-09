from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys

from madp_validation import load_yaml_text


VERSION = "MADP-v0.3.0-alpha.2"
FILES = [
    "use-madp-commands.md",
    "share-context-with-ai.md",
    "request-review.md",
]
REQUIRED_MARKERS = {
    "use-madp-commands.md": [
        "COMMAND_BLOCK",
        "COMMAND_PARSE_ERROR",
        "COMMAND_NEEDS_ARGUMENTS",
        "Do not claim user approval",
    ],
    "share-context-with-ai.md": [
        "CONTEXT_PACKAGE",
        "CONTEXT_PACKAGE_RECEIPT",
        "may_execute_external_actions: false",
        "Do not claim user approval",
    ],
    "request-review.md": [
        "REVIEW_REQUEST",
        "REVIEW_RESPONSE",
        "PROPOSE_ONLY",
        "external_actions_performed: false",
    ],
}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check generated MADP alpha.2 bootstrap prompts.")
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args()
    problems: list[str] = []
    bootstrap = args.site_dir / "bootstrap"

    manifest_path = bootstrap / "alpha2-manifest.yaml"
    if not manifest_path.is_file():
        problems.append("missing alpha2 manifest")
        manifest = {}
    else:
        manifest_data = load_yaml_text(manifest_path.read_text(encoding="utf-8"), "alpha2 manifest")
        manifest = manifest_data.get("generated_alpha2_bootstrap", {})

    commit = manifest.get("source_commit")
    if manifest.get("protocol_version") != VERSION:
        problems.append("manifest protocol_version mismatch")
    if manifest.get("status") != "draft implementation aid":
        problems.append("manifest status mismatch")
    if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
        problems.append("manifest source_commit invalid")

    manifest_files = manifest.get("files", [])
    if [item.get("path") for item in manifest_files] != [f"bootstrap/{name}" for name in FILES]:
        problems.append("manifest file list mismatch")

    for item, name in zip(manifest_files, FILES):
        path = bootstrap / name
        if not path.is_file():
            problems.append(f"missing generated prompt: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if VERSION not in text:
            problems.append(f"missing protocol version marker: {name}")
        if "Generated alpha.2 draft prompt" not in text:
            problems.append(f"missing generated metadata: {name}")
        if item.get("sha256") != sha256(text):
            problems.append(f"digest mismatch: {name}")
        for marker in REQUIRED_MARKERS[name]:
            if marker not in text:
                problems.append(f"missing required marker in {name}: {marker}")

    index = (args.site_dir / "index.html").read_text(encoding="utf-8")
    if VERSION not in index:
        problems.append("index version mismatch")
    if "not a release publication" not in index:
        problems.append("index draft status missing")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("generated bootstrap: MADP-v0.3.0-alpha.2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
