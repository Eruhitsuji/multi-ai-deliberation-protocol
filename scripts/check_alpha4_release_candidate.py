#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import argparse
import sys

import yaml
from jsonschema import Draft202012Validator

from check_alpha4_prerelease_package import check as check_package
from generate_alpha4_prerelease_package import (
    verify_git_head,
    verify_git_sources,
    verify_repository_sources,
)
from generate_alpha4_release_candidate import RECEIPT_FILENAME, build_receipt

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/v0.3.0-alpha.4/release-candidate-receipt.schema.yaml"


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
    root: Path = ROOT,
) -> list[str]:
    problems = check_package(directory, repository, source_commit, root=root)
    receipt_path = directory / RECEIPT_FILENAME
    if not receipt_path.is_file():
        return sorted(set(problems + [f"missing generated artifact: {RECEIPT_FILENAME}"]))

    observed = receipt_path.read_bytes()
    try:
        _archive, _manifest, _audit, _archive_sha, expected = build_receipt(
            repository,
            source_commit,
            source_ref_kind,
            branch_name,
            root=root,
        )
    except Exception as exc:
        return sorted(set(problems + [f"canonical receipt regeneration failed: {exc}"]))
    if observed != expected:
        problems.append("release-candidate receipt does not match canonical output")

    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    expanded = expand_local_refs(schema, schema)
    Draft202012Validator.check_schema(expanded)
    receipt = yaml.safe_load(observed.decode("utf-8"))
    errors = sorted(
        Draft202012Validator(expanded).iter_errors(receipt),
        key=lambda error: list(error.path),
    )
    if errors:
        problems.append(f"receipt schema failure: {errors[0].message}")
        return sorted(set(problems))

    if receipt.get("repository") != repository:
        problems.append("receipt repository binding mismatch")
    if receipt.get("source_commit") != source_commit:
        problems.append("receipt source commit binding mismatch")
    if receipt.get("source_ref_kind") != source_ref_kind:
        problems.append("receipt source ref kind mismatch")
    if receipt.get("branch_name") != branch_name:
        problems.append("receipt branch binding mismatch")
    for key, value in receipt.get("checks", {}).items():
        if value != "PASS":
            problems.append(f"receipt check is not PASS: {key}")
    for key, value in receipt.get("boundaries", {}).items():
        if value is not False:
            problems.append(f"receipt authority boundary must remain false: {key}")
    return sorted(set(problems))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MADP alpha.4 release-candidate receipt")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument(
        "--source-ref-kind",
        required=True,
        choices=("PULL_REQUEST_HEAD", "MERGED_MAIN"),
    )
    parser.add_argument("--branch-name", required=True)
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
    )
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1
    print("MADP v0.3.0-alpha.4 release candidate: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
