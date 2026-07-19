#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import argparse
import re
import sys

import yaml
from jsonschema import Draft202012Validator

from check_alpha4_release_candidate import check as check_release_candidate
from generate_alpha4_prerelease_package import (
    ARCHIVE_FILENAME,
    SIDECAR_AUDIT_FILENAME,
    SIDECAR_MANIFEST_FILENAME,
    sha256,
    verify_git_head,
    verify_git_sources,
    verify_repository_sources,
)
from generate_alpha4_publication_handoff import (
    CHECKLIST_FILENAME,
    HANDOFF_FILENAME,
    RELEASE_NOTES_RELATIVE,
    TARGET_TAG,
    build_handoff,
)
from generate_alpha4_release_candidate import RECEIPT_FILENAME

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/v0.3.0-alpha.4/publication-handoff.schema.yaml"


def expand_local_refs(node, root):
    if isinstance(node, dict):
        if set(node) == {"$ref"} and isinstance(node["$ref"], str):
            prefix = "#/$defs/"
            ref = node["$ref"]
            if ref.startswith(prefix):
                target = root.get("$defs", {}).get(ref[len(prefix):])
                if target is None:
                    raise ValueError(f"unresolved local ref: {ref}")
                return expand_local_refs(deepcopy(target), root)
        return {
            key: expand_local_refs(value, root)
            for key, value in node.items()
            if key != "$defs"
        }
    if isinstance(node, list):
        return [expand_local_refs(value, root) for value in node]
    return node


def check(
    directory: Path,
    repository: str,
    source_commit: str,
    source_ref_kind: str,
    branch_name: str,
    target_tag: str,
    root: Path = ROOT,
) -> list[str]:
    problems = check_release_candidate(
        directory,
        repository,
        source_commit,
        source_ref_kind,
        branch_name,
        root=root,
    )
    handoff_path = directory / HANDOFF_FILENAME
    checklist_path = directory / CHECKLIST_FILENAME
    for path in (handoff_path, checklist_path):
        if not path.is_file():
            problems.append(f"missing generated artifact: {path.name}")
    if not handoff_path.is_file() or not checklist_path.is_file():
        return sorted(set(problems))

    try:
        expected_files, expected_handoff = build_handoff(
            repository,
            source_commit,
            source_ref_kind,
            branch_name,
            target_tag,
            root=root,
        )
    except Exception as exc:
        return sorted(set(problems + [f"canonical handoff regeneration failed: {exc}"]))

    for name, expected in expected_files.items():
        path = directory / name
        if not path.is_file():
            problems.append(f"missing canonical handoff artifact: {name}")
        elif path.read_bytes() != expected:
            problems.append(f"handoff artifact does not match canonical output: {name}")

    observed = handoff_path.read_bytes()
    if observed != expected_handoff:
        problems.append("publication handoff does not match canonical output")

    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    expanded = expand_local_refs(schema, schema)
    Draft202012Validator.check_schema(expanded)
    handoff = yaml.safe_load(observed.decode("utf-8"))
    errors = sorted(
        Draft202012Validator(expanded).iter_errors(handoff),
        key=lambda error: list(error.path),
    )
    if errors:
        problems.append(f"handoff schema failure: {errors[0].message}")
        return sorted(set(problems))

    bindings = {
        "repository": repository,
        "source_commit": source_commit,
        "source_ref_kind": source_ref_kind,
        "branch_name": branch_name,
        "target_tag": target_tag,
    }
    for key, expected in bindings.items():
        if handoff.get(key) != expected:
            problems.append(f"handoff binding mismatch: {key}")

    candidate = handoff.get("candidate", {})
    digest_paths = {
        "archive_sha256": ARCHIVE_FILENAME,
        "manifest_sha256": SIDECAR_MANIFEST_FILENAME,
        "audit_sha256": SIDECAR_AUDIT_FILENAME,
        "receipt_sha256": RECEIPT_FILENAME,
    }
    for key, name in digest_paths.items():
        path = directory / name
        if path.is_file() and candidate.get(key) != sha256(path.read_bytes()):
            problems.append(f"handoff candidate digest mismatch: {key}")
    notes = root / RELEASE_NOTES_RELATIVE
    if candidate.get("release_notes_sha256") != sha256(notes.read_bytes()):
        problems.append("handoff release notes digest mismatch")

    for key, value in handoff.get("required_human_actions", {}).items():
        if value is not False:
            problems.append(f"human action must remain unconfirmed: {key}")
    for key, value in handoff.get("boundaries", {}).items():
        if value is not False:
            problems.append(f"handoff boundary must remain false: {key}")

    checklist = checklist_path.read_text(encoding="utf-8")
    for token in (source_commit, target_tag, "MADP-v0.3.0-alpha.2"):
        if token not in checklist:
            problems.append(f"publication checklist missing token: {token}")
    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(
        rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])"
    )
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for path in (handoff_path, checklist_path):
        text = path.read_text(encoding="utf-8")
        if exact_private.search(text):
            problems.append(f"private identifier found in handoff artifact: {path.name}")
        if email.search(text):
            problems.append(f"email address found in handoff artifact: {path.name}")
        if "human-final-authority-input-raw.md" in text:
            problems.append(f"removed private raw path found in handoff artifact: {path.name}")
    if target_tag != TARGET_TAG:
        problems.append("unexpected target tag")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a read-only MADP alpha.4 publication handoff"
    )
    parser.add_argument("directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--source-ref-kind",
        required=True,
        choices=("PULL_REQUEST_HEAD", "MERGED_MAIN"),
    )
    parser.add_argument("--branch-name", required=True)
    parser.add_argument("--target-tag", default=TARGET_TAG)
    args = parser.parse_args()
    try:
        verify_git_head(ROOT, args.source_commit)
        verify_git_sources(ROOT, args.source_commit)
        verify_repository_sources(ROOT, args.source_commit)
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    problems = check(
        args.directory,
        args.repository,
        args.source_commit,
        args.source_ref_kind,
        args.branch_name,
        args.target_tag,
    )
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print("MADP v0.3.0-alpha.4 publication handoff: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
