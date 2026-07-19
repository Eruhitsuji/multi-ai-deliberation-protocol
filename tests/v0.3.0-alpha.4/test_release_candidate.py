#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import tempfile
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_alpha4_release_candidate import check
from generate_alpha4_release_candidate import RECEIPT_FILENAME, build_receipt, write_candidate


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Test alpha.4 release-candidate generation")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()

    first = build_receipt(
        args.repository,
        args.source_commit,
        "PULL_REQUEST_HEAD",
        "feature/test-release-candidate",
    )
    second = build_receipt(
        args.repository,
        args.source_commit,
        "PULL_REQUEST_HEAD",
        "feature/test-release-candidate",
    )
    require(first == second, "release candidate generation is not deterministic")

    merged = yaml.safe_load(
        build_receipt(args.repository, args.source_commit, "MERGED_MAIN", "main")[-1]
    )
    require(merged["main_branch_candidate"] is True, "merged-main receipt is not marked as main")
    require(
        merged["status"] == "MERGED_MAIN_CANDIDATE_VALIDATED",
        "merged-main receipt status mismatch",
    )

    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        write_candidate(
            directory,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            "feature/test-release-candidate",
        )
        problems = check(
            directory,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            "feature/test-release-candidate",
        )
        require(not problems, f"valid candidate failed: {problems}")

        receipt_path = directory / RECEIPT_FILENAME
        receipt = yaml.safe_load(receipt_path.read_text(encoding="utf-8"))
        receipt["boundaries"]["tag_authorized"] = True
        receipt_path.write_text(
            yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        problems = check(
            directory,
            args.repository,
            args.source_commit,
            "PULL_REQUEST_HEAD",
            "feature/test-release-candidate",
        )
        require(problems, "authority tampering was not detected")

    try:
        build_receipt(args.repository, args.source_commit, "MERGED_MAIN", "not-main")
    except ValueError:
        pass
    else:
        raise AssertionError("MERGED_MAIN accepted a non-main branch")

    print("alpha.4 release-candidate tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
