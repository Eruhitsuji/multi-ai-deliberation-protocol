from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import re
import sys

from madp_validation import ROOT, load_yaml_text

VERSION = "MADP-v0.3.0-alpha.1"
FILES = [
    "README-v0.3.0-alpha.1.md",
    "protocol/MADP-v0.3.0-alpha.1.md",
    "protocol/GLOSSARY-v0.3.0-alpha.1.md",
    "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml",
    "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml",
]
PROMPTS = [
    "README.md",
    "load-protocol-from-github.md",
    "start-facilitator.md",
    "join-as-participant.md",
    "recover-from-load-failure.md",
]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_yaml(path: Path):
    return load_yaml_text(path.read_text(encoding="utf-8"), str(path))


def expected_bundle(repository: str, commit: str) -> str:
    lines = [
        "BEGIN_MADP_BUNDLE_METADATA",
        "bundle_format: MADP_COMPLETE_PROTOCOL_BUNDLE_V1",
        f"protocol_version: {VERSION}",
        f"source_repository: {repository}",
        f"source_commit: {commit}",
        f"canonical_file_count: {len(FILES)}",
        "END_MADP_BUNDLE_METADATA",
        "",
    ]
    blocks = []
    for name in FILES:
        text = (ROOT / name).read_text(encoding="utf-8")
        if not text.endswith("\n"):
            text += "\n"
        blocks.append(f"BEGIN_FILE: {name}\n{text}END_FILE: {name}")
    return "\n".join(lines) + "\n\n".join(blocks) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("--expect", type=Path)
    args = parser.parse_args()
    problems = []
    bootstrap = args.site_dir / "bootstrap"

    manifest_path = bootstrap / "manifest.yaml"
    manifest = {}
    if not manifest_path.is_file():
        problems.append("missing bootstrap/manifest.yaml")
    else:
        data = load_yaml(manifest_path)
        manifest = data.get("generated_bootstrap", {}) if isinstance(data, dict) else {}

    repository = manifest.get("source_repository")
    commit = manifest.get("source_commit")
    if manifest.get("protocol_version") != VERSION:
        problems.append("manifest protocol_version mismatch")
    if not isinstance(repository, str) or "/" not in repository:
        problems.append("manifest source_repository invalid")
    if not isinstance(commit, str) or not SHA_RE.fullmatch(commit):
        problems.append("manifest source_commit invalid")

    if args.expect and args.expect.is_file():
        expected = load_yaml(args.expect)
        mapping = {"github_repository": "source_repository", "github_sha": "source_commit", "github_run_id": "workflow_run_id", "generated_by": "generated_by"}
        for source, target in mapping.items():
            if source in expected and expected[source] != manifest.get(target):
                problems.append(f"expected {target} mismatch")

    texts = {}
    for name in PROMPTS:
        path = bootstrap / name
        if not path.is_file():
            problems.append(f"missing bootstrap/{name}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        if VERSION not in text:
            problems.append(f"bootstrap/{name}: version mismatch")
        if "{{MADP_GITHUB_OWNER}}" in text or "{{MADP_GITHUB_REPOSITORY}}" in text or "{{MADP_COMMIT_SHA}}" in text:
            problems.append(f"bootstrap/{name}: repository placeholder remains")

    if isinstance(repository, str) and isinstance(commit, str) and "/" in repository:
        owner, repo = repository.split("/", 1)
        load_text = texts.get("load-protocol-from-github.md", "")
        for name in FILES:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{name}"
            if url not in load_text:
                problems.append(f"missing canonical URL: {name}")
        pages_url = f"https://{owner}.github.io/{repo}/bootstrap/complete-protocol-bundle.txt"
        if pages_url not in texts.get("recover-from-load-failure.md", ""):
            problems.append("recovery Pages URL mismatch")

        bundle_path = bootstrap / "complete-protocol-bundle.txt"
        if not bundle_path.is_file():
            problems.append("missing complete protocol bundle")
        else:
            bundle = bundle_path.read_text(encoding="utf-8")
            if bundle != expected_bundle(repository, commit):
                problems.append("complete protocol bundle content mismatch")
            companion_path = bootstrap / "complete-protocol-bundle.manifest.yaml"
            if not companion_path.is_file():
                problems.append("missing complete protocol bundle manifest")
            else:
                data = load_yaml(companion_path)
                companion = data.get("complete_protocol_bundle", {}) if isinstance(data, dict) else {}
                if companion.get("protocol_version") != VERSION:
                    problems.append("bundle manifest version mismatch")
                if companion.get("bundle_sha256") != sha256(bundle):
                    problems.append("bundle manifest digest mismatch")
                paths = [item.get("path") for item in companion.get("files", [])]
                if paths != FILES:
                    problems.append("bundle manifest file list mismatch")

    index = args.site_dir / "index.html"
    if not index.is_file() or VERSION not in index.read_text(encoding="utf-8"):
        problems.append("index.html version mismatch")

    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    print("generated bootstrap: MADP-v0.3.0-alpha.1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
