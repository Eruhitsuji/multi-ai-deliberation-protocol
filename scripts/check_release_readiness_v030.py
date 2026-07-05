#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.1"

REQUIRED_FILES = [
    "README-v0.3.0-alpha.1.md",
    "protocol/MADP-v0.3.0-alpha.1.md",
    "protocol/GLOSSARY-v0.3.0-alpha.1.md",
    "schemas/v0.3.0-alpha.1/definitions.schema.yaml",
    "schemas/v0.3.0-alpha.1/session-state.schema.yaml",
    "schemas/v0.3.0-alpha.1/relay-block.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml",
    "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml",
    "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml",
    "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml",
    "bootstrap/complete-protocol-bundle.txt",
    "bootstrap/migration-fixtures-bundle.txt",
    "tests/traceability/traceability-matrix-v0.3.0-alpha.1.yaml",
    "scripts/run_schema_fixture_checks.py",
    "scripts/check_migration_invariants_v030.py",
    "scripts/generate_artifacts.py",
    "scripts/check_schema_bundle_equivalence.py",
    "scripts/verify_jcs_vectors.py",
    "scripts/check_complete_bundle_v030.py",
]

EXPECTED_SCHEMA_IDS = {
    "schemas/v0.3.0-alpha.1/definitions.schema.yaml": "urn:madp:schema:definitions:0.3.0-alpha.1",
    "schemas/v0.3.0-alpha.1/session-state.schema.yaml": "urn:madp:schema:session-state:0.3.0-alpha.1",
    "schemas/v0.3.0-alpha.1/relay-block.schema.yaml": "urn:madp:schema:relay-block:0.3.0-alpha.1",
    "schemas/v0.3.0-alpha.1/migration-evidence.schema.yaml": "urn:madp:schema:migration-evidence:0.3.0-alpha.1",
    "schemas/v0.3.0-alpha.1/migration-audit.schema.yaml": "urn:madp:schema:migration-audit:0.3.0-alpha.1",
    "schemas/generated/session-state-v0.3.0-alpha.1.bundle.schema.yaml": "urn:madp:schema:bundle:session-state:0.3.0-alpha.1",
    "schemas/generated/relay-block-v0.3.0-alpha.1.bundle.schema.yaml": "urn:madp:schema:bundle:relay-block:0.3.0-alpha.1",
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    for relative in REQUIRED_FILES:
        exists = (ROOT / relative).is_file()
        checks.append({"check": "required_file", "target": relative, "passed": exists})
        if not exists:
            errors.append(f"missing required file: {relative}")

    for relative, expected_id in EXPECTED_SCHEMA_IDS.items():
        path = ROOT / relative
        if not path.is_file():
            continue
        actual_id = load_yaml(path).get("$id")
        passed = actual_id == expected_id
        checks.append({"check": "schema_id", "target": relative, "expected": expected_id, "actual": actual_id, "passed": passed})
        if not passed:
            errors.append(f"unexpected schema $id: {relative}: {actual_id!r}")

    migration_root = ROOT / "tests" / "migration"
    fixture_ids: list[str] = []
    for directory in sorted(path for path in migration_root.iterdir() if path.is_dir()):
        manifest_path = directory / "manifest.yaml"
        if not manifest_path.is_file():
            errors.append(f"missing migration manifest: {directory.relative_to(ROOT)}")
            continue
        manifest = load_yaml(manifest_path)
        fixture_id = manifest.get("fixture_id")
        fixture_ids.append(fixture_id)
        if not manifest.get("checks"):
            errors.append(f"fixture has no schema checks: {fixture_id}")
        if "expected_semantic_errors" not in manifest:
            errors.append(f"fixture lacks semantic expectation: {fixture_id}")
    expected_fixture_ids = [f"MIG-FIX-{index:03d}" for index in range(1, 11)]
    fixtures_passed = fixture_ids == expected_fixture_ids
    checks.append({"check": "migration_fixture_set", "expected": expected_fixture_ids, "actual": fixture_ids, "passed": fixtures_passed})
    if not fixtures_passed:
        errors.append("migration fixture set is not exactly MIG-FIX-001 through MIG-FIX-010")

    vector_root = ROOT / "tests" / "canonicalization"
    vector_ids = []
    valid_count = 0
    invalid_count = 0
    for directory in sorted(path for path in vector_root.iterdir() if path.is_dir()):
        manifest = load_yaml(directory / "manifest.yaml")
        vector_ids.append(manifest.get("vector_id"))
        if manifest.get("vector_type", "VALID") == "INVALID":
            invalid_count += 1
            if not manifest.get("expected_error"):
                errors.append(f"invalid vector lacks expected_error: {directory.name}")
        else:
            valid_count += 1
            for key in ("canonical_byte_file", "expected_sha256", "expected_byte_length"):
                if key not in manifest:
                    errors.append(f"valid vector lacks {key}: {directory.name}")
    vector_passed = valid_count >= 1 and invalid_count >= 6 and len(vector_ids) == len(set(vector_ids))
    checks.append({"check": "jcs_vector_coverage", "valid": valid_count, "invalid": invalid_count, "unique_ids": len(vector_ids) == len(set(vector_ids)), "passed": vector_passed})
    if not vector_passed:
        errors.append("JCS vector coverage is below alpha.1 minimum")

    alpha_readme = (ROOT / "README-v0.3.0-alpha.1.md").read_text(encoding="utf-8")
    authority_phrases = [
        "does not authorize",
        "merging to `main`",
        "creating or moving a tag",
        "publishing a GitHub Release",
    ]
    authority_passed = all(phrase in alpha_readme for phrase in authority_phrases)
    checks.append({"check": "authority_boundaries", "passed": authority_passed})
    if not authority_passed:
        errors.append("alpha README authority boundaries are incomplete")

    main_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    main_readme_passed = "Current release candidate: **MADP-v0.2.5-rc.2**" in main_readme
    checks.append({"check": "main_readme_rc2_preserved", "passed": main_readme_passed})
    if not main_readme_passed:
        errors.append("main README no longer identifies rc.2 as current release candidate")

    bootstrap_index = (ROOT / "bootstrap" / "complete-protocol-bundle.txt").read_text(encoding="utf-8")
    bootstrap_passed = (
        "status: GENERATED_DISTRIBUTION_DRAFT_INDEX_ONLY" in bootstrap_index
        and "It is not released or tagged." in bootstrap_index
    )
    checks.append({"check": "bootstrap_alpha_label", "passed": bootstrap_passed})
    if not bootstrap_passed:
        errors.append("bootstrap index alpha/unreleased labeling is incomplete")

    report = {
        "report_version": "1",
        "protocol_version": VERSION,
        "readiness": "READY_FOR_USER_REVIEW" if not errors else "BLOCKED",
        "merge_authorized": False,
        "tag_authorized": False,
        "release_authorized": False,
        "checks": checks,
        "errors": errors,
        "limitations": [
            "This audit checks repository state, not external interoperability.",
            "A passing audit does not grant merge, tag, or release authority.",
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
