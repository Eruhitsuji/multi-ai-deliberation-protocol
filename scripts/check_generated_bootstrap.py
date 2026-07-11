from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys

from madp_validation import load_yaml_text

VERSION = "MADP-v0.3.0-alpha.2"
FILES = [
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
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    problems: list[str] = []
    bootstrap = args.site_dir / "bootstrap"

    manifest = load_yaml_text((bootstrap / "manifest.yaml").read_text(encoding="utf-8"), "manifest")["generated_bootstrap"]
    repository = manifest.get("source_repository")
    commit = manifest.get("source_commit")
    if manifest.get("protocol_version") != VERSION:
        problems.append("manifest protocol_version mismatch")
    if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
        problems.append("manifest source_commit invalid")
    if not isinstance(repository, str) or "/" not in repository:
        problems.append("manifest source_repository invalid")
        owner = repo = ""
    else:
        owner, repo = repository.split("/", 1)

    load_text = (bootstrap / "load-protocol-from-github.md").read_text(encoding="utf-8")
    for name in FILES:
        expected_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{name}"
        if expected_url not in load_text:
            problems.append(f"missing canonical URL: {name}")

    bundle = (bootstrap / "complete-protocol-bundle.txt").read_text(encoding="utf-8")
    if f"protocol_version: {VERSION}" not in bundle:
        problems.append("bundle version mismatch")
    if f"canonical_file_count: {len(FILES)}" not in bundle:
        problems.append("bundle file count mismatch")
    for name in FILES:
        if f"BEGIN_FILE: {name}" not in bundle or f"END_FILE: {name}" not in bundle:
            problems.append(f"bundle missing file boundary: {name}")

    companion = load_yaml_text((bootstrap / "complete-protocol-bundle.manifest.yaml").read_text(encoding="utf-8"), "bundle manifest")["complete_protocol_bundle"]
    if companion.get("bundle_sha256") != sha256(bundle):
        problems.append("bundle digest mismatch")
    if [item.get("path") for item in companion.get("files", [])] != FILES:
        problems.append("bundle manifest file list mismatch")

    index = (args.site_dir / "index.html").read_text(encoding="utf-8")
    if VERSION not in index:
        problems.append("index version mismatch")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print(f"generated bootstrap: {VERSION} PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
