#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import argparse
import hashlib
import sys
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_alpha4_core_compact_bundle import check, load_loader, load_report_problems
from generate_alpha4_core_compact_bundle import (
    BUNDLE_FILENAME,
    MANIFEST_FILENAME,
    build_bundle,
    path_inventory_digest,
    selected_loader_paths,
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_artifacts(directory: Path, bundle: bytes, manifest: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / BUNDLE_FILENAME).write_bytes(bundle)
    (directory / MANIFEST_FILENAME).write_text(
        yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )


def make_report(profile: str, repository: str, source_commit: str) -> dict:
    loader = load_loader(ROOT)
    paths = selected_loader_paths(loader, profile)
    verified = profile == "VERIFIED"
    start_paths = loader["load_profiles"][profile]["authorized_start_profiles"]
    digest = path_inventory_digest(paths)
    fake_hash = "a" * 64
    return {
        "report_version": "MADP-PROTOCOL-LOAD-REPORT-v3",
        "report_id": f"PLR-{profile}",
        "revision": 1,
        "supersedes": None,
        "active": True,
        "protocol_version": "MADP-v0.3.0-alpha.4",
        "compatibility_base": "MADP-v0.3.0-alpha.3",
        "load_profile": profile,
        "repository": repository,
        "repository_commit": source_commit,
        "inventory_digest_algorithm": "sha256-newline-paths-v1",
        "source_inventory_digest": digest,
        "status": "COMPLETE",
        "files": [
            {
                "path": path,
                "status": "READ",
                "access_method": "RAW_URL",
                "source_ref": f"https://example.invalid/{source_commit}/{path}",
                "content_sha256": fake_hash if verified else None,
            }
            for path in paths
        ],
        "all_required_files_read": True,
        "schema_validation_capability": "EXECUTED" if verified else "UNAVAILABLE",
        "schema_validation_executed": verified,
        "inferred_unread_content": False,
        "provenance_level": "HASH_VERIFIED" if verified else "SOURCE_REFERENCED",
        "bundle_binding": None,
        "authorized_start_profiles": [
            {
                "path": path,
                "repository": repository,
                "repository_commit": source_commit,
                "source_ref": f"https://example.invalid/{source_commit}/{path}",
                "content_sha256": fake_hash if verified else None,
            }
            for path in start_paths
        ],
        "limitations": [] if verified else ["schema validation was not executed"],
        "next_action": {
            "command": "APPLY_START_PROFILE",
            "accepted_input": start_paths[-1],
        },
    }


def expect_problem(report: dict, needle: str) -> None:
    problems = load_report_problems(report, ROOT)
    if not any(needle in problem for problem in problems):
        raise AssertionError(f"expected {needle!r}; observed {problems!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default="Eruhitsuji/multi-ai-deliberation-protocol")
    parser.add_argument("--source-commit", default="0" * 40)
    args = parser.parse_args()

    bundle_a, manifest_a = build_bundle(args.repository, args.source_commit, ROOT)
    bundle_b, manifest_b = build_bundle(args.repository, args.source_commit, ROOT)
    if bundle_a != bundle_b or manifest_a != manifest_b:
        raise AssertionError("distribution generation is not deterministic")

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        good = base / "good"
        write_artifacts(good, bundle_a, manifest_a)
        problems = check(good, args.repository, args.source_commit, ROOT)
        if problems:
            raise AssertionError(f"valid distribution failed: {problems}")

        appended = base / "appended"
        appended_bundle = bundle_a + b"\nUNAUTHORIZED APPENDED INSTRUCTION\n"
        appended_manifest = deepcopy(manifest_a)
        appended_manifest["bundle_sha256"] = sha256(appended_bundle)
        appended_manifest["bundle_bytes"] = len(appended_bundle)
        write_artifacts(appended, appended_bundle, appended_manifest)
        observed = check(appended, args.repository, args.source_commit, ROOT)
        if "bundle does not match canonical deterministic output" not in observed:
            raise AssertionError(f"appended bundle was not rejected: {observed}")

        changed_manifest_dir = base / "manifest-tamper"
        changed_manifest = deepcopy(manifest_a)
        changed_manifest["proves_model_ingestion"] = True
        write_artifacts(changed_manifest_dir, bundle_a, changed_manifest)
        observed = check(changed_manifest_dir, args.repository, args.source_commit, ROOT)
        if not observed:
            raise AssertionError("authority/evidence manifest tampering was not rejected")

    quick = make_report("QUICK", args.repository, args.source_commit)
    if load_report_problems(quick, ROOT):
        raise AssertionError(f"valid QUICK report failed: {load_report_problems(quick, ROOT)}")

    verified = make_report("VERIFIED", args.repository, args.source_commit)
    if load_report_problems(verified, ROOT):
        raise AssertionError(f"valid VERIFIED report failed: {load_report_problems(verified, ROOT)}")

    missing = deepcopy(quick)
    missing["files"].pop()
    expect_problem(missing, "file inventory or order mismatch")

    wrong_digest = deepcopy(quick)
    wrong_digest["source_inventory_digest"] = "b" * 64
    expect_problem(wrong_digest, "inventory digest mismatch")

    weak_verified = deepcopy(verified)
    weak_verified["provenance_level"] = "SOURCE_REFERENCED"
    expect_problem(weak_verified, "schema failure")

    stale_binding = deepcopy(verified)
    stale_binding["authorized_start_profiles"][0]["repository_commit"] = "f" * 40
    expect_problem(stale_binding, "authorized profile commit mismatch")

    incomplete = deepcopy(quick)
    incomplete["status"] = "INCOMPLETE"
    incomplete["all_required_files_read"] = False
    incomplete["files"][0]["status"] = "FAILED"
    incomplete["next_action"] = {
        "command": "RECOVER_PROTOCOL_SOURCE",
        "accepted_input": "corrected source access",
    }
    if load_report_problems(incomplete, ROOT):
        raise AssertionError(f"honest incomplete report should remain valid: {load_report_problems(incomplete, ROOT)}")

    bundle_bound = make_report("VERIFIED", args.repository, args.source_commit)
    for row in bundle_bound["files"]:
        row["access_method"] = "COMPLETE_BUNDLE"
    bundle_bound["bundle_binding"] = {
        "bundle_version": "MADP-CORE-DISTRIBUTION-BUNDLE-v1",
        "bundle_file": "MADP-v0.3.0-alpha.4-core-distribution.md",
        "bundle_sha256": manifest_a["bundle_sha256"],
        "manifest_sha256": "c" * 64,
        "repository": args.repository,
        "source_commit": args.source_commit,
    }
    if load_report_problems(bundle_bound, ROOT):
        raise AssertionError(f"valid bundle-bound report failed: {load_report_problems(bundle_bound, ROOT)}")

    bundle_mismatch = deepcopy(bundle_bound)
    bundle_mismatch["bundle_binding"]["source_commit"] = "d" * 40
    expect_problem(bundle_mismatch, "bundle binding commit mismatch")

    print("MADP v0.3.0-alpha.4 distribution tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
