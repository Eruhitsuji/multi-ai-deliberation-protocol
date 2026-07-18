#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from pathlib import Path
import sys

from jsonschema import Draft202012Validator

import check_alpha3_core_candidate_experiments as base

ROOT = Path(__file__).resolve().parents[1]
ALPHA3_WORKFLOWS = {"STANDARD_ALPHA3", "ALPHA3_CORE_CANDIDATE"}


def comparison_integrity_errors(document) -> list[str]:
    errors: list[str] = []
    runs = document.get("runs", []) if isinstance(document, dict) else []
    status = document.get("experiment_status") if isinstance(document, dict) else None
    workflow_counts = Counter(
        run.get("workflow") for run in runs if isinstance(run, dict)
    )

    if status in base.READY_STATUSES:
        for workflow in base.EXPECTED_WORKFLOWS:
            if workflow_counts.get(workflow, 0) != 1:
                errors.append("COMPARISON_WORKFLOW_COUNT_MISMATCH")
        alpha3_commits = {
            run.get("tested_commit")
            for run in runs
            if isinstance(run, dict) and run.get("workflow") in ALPHA3_WORKFLOWS
        }
        if len(alpha3_commits) != 1:
            errors.append("ALPHA3_COMMIT_MISMATCH")

    for run in runs:
        if not isinstance(run, dict):
            continue
        blind = run.get("blind_first_round", {})
        responses = [
            response
            for response in blind.get("initial_responses", [])
            if isinstance(response, dict)
        ]
        eligible = [
            response
            for response in responses
            if response.get("captured_before_cross_exposure") is True
            and response.get("exposure_state") == "UNEXPOSED"
        ]
        if blind.get("eligible_initial_response_count") != len(eligible):
            errors.append("BLIND_ELIGIBLE_COUNT_MISMATCH")

        all_groups = {
            response.get("independence_group")
            for response in responses
            if response.get("independence_group")
        }
        if blind.get("independence_group_count") != len(all_groups):
            errors.append("BLIND_INDEPENDENCE_GROUP_COUNT_MISMATCH")

        eligible_groups = {
            response.get("independence_group")
            for response in eligible
            if response.get("independence_group")
        }
        if (
            blind.get("convergence_classification") == "INDEPENDENT_CONVERGENCE"
            and len(eligible_groups) < 2
        ):
            errors.append("INDEPENDENT_CONVERGENCE_ELIGIBLE_GROUP_COUNT")
    return errors


def claim_integrity_errors(document) -> list[str]:
    errors: list[str] = []
    claims = document.get("claims", []) if isinstance(document, dict) else []
    evidence = document.get("evidence", []) if isinstance(document, dict) else []
    migrations = document.get("migration_records", []) if isinstance(document, dict) else []
    evidence_by_id = {
        row.get("evidence_id"): row
        for row in evidence
        if isinstance(row, dict) and row.get("evidence_id")
    }

    for claim in claims:
        if not isinstance(claim, dict):
            continue
        claim_id = claim.get("claim_id")
        for evidence_ref in claim.get("evidence_refs", []):
            row = evidence_by_id.get(evidence_ref)
            if not row:
                continue
            linked = set(row.get("supports_claim_refs", [])) | set(
                row.get("challenges_claim_refs", [])
            )
            if claim_id not in linked:
                errors.append("CLAIM_EVIDENCE_BACKLINK_MISSING")

    for row in evidence:
        if not isinstance(row, dict):
            continue
        overlap = set(row.get("supports_claim_refs", [])) & set(
            row.get("challenges_claim_refs", [])
        )
        if overlap:
            errors.append("EVIDENCE_SUPPORT_CHALLENGE_OVERLAP")

    source_keys = [
        (row.get("source_fact_ref"), row.get("source_fact_revision"))
        for row in migrations
        if isinstance(row, dict)
    ]
    if len(source_keys) != len(set(source_keys)):
        errors.append("DUPLICATE_SOURCE_FACT_MIGRATION")
    return errors


def validate_document(path: Path, kind: str) -> list[str]:
    schema_path = base.COMPARISON_SCHEMA if kind == "comparison" else base.CLAIM_SCHEMA
    schema = base.load(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    document = base.load(path)
    errors: list[str] = []
    schema_error = base.first_error(validator, document)
    if schema_error:
        return [f"SCHEMA: {schema_error}"]
    if kind == "comparison":
        errors.extend(base.comparison_semantic_errors(document))
        errors.extend(comparison_integrity_errors(document))
    else:
        errors.extend(base.claim_semantic_errors(document))
        errors.extend(claim_integrity_errors(document))
    return errors


def expect_error(name: str, artifact, function, expected: str, problems: list[str]):
    actual = function(artifact)
    if expected not in actual:
        problems.append(f"{name} did not produce {expected}: {actual}")


def regression_tests() -> list[str]:
    problems: list[str] = []
    ready = base.build_comparison("READY_VALID")
    degraded = base.build_comparison("DRAFT_DEGRADED")
    claim = base.build_claim()

    for name, artifact, function in (
        ("ready comparison", ready, comparison_integrity_errors),
        ("degraded comparison", degraded, comparison_integrity_errors),
        ("claim package", claim, claim_integrity_errors),
    ):
        errors = function(artifact)
        if errors:
            problems.append(f"valid {name} failed integrity: {errors}")

    duplicate_workflow = deepcopy(ready)
    duplicate = deepcopy(duplicate_workflow["runs"][0])
    duplicate["run_id"] = "MANUAL-DUPLICATE"
    duplicate_workflow["runs"].append(duplicate)
    expect_error(
        "duplicate workflow",
        duplicate_workflow,
        comparison_integrity_errors,
        "COMPARISON_WORKFLOW_COUNT_MISMATCH",
        problems,
    )

    commit_mismatch = deepcopy(ready)
    core = next(
        run for run in commit_mismatch["runs"]
        if run["workflow"] == "ALPHA3_CORE_CANDIDATE"
    )
    core["tested_commit"] = "c" * 40
    expect_error(
        "alpha.3 commit mismatch",
        commit_mismatch,
        comparison_integrity_errors,
        "ALPHA3_COMMIT_MISMATCH",
        problems,
    )

    eligible_count_mismatch = deepcopy(ready)
    core = next(
        run for run in eligible_count_mismatch["runs"]
        if run["workflow"] == "ALPHA3_CORE_CANDIDATE"
    )
    core["blind_first_round"]["eligible_initial_response_count"] = 99
    expect_error(
        "blind eligible count mismatch",
        eligible_count_mismatch,
        comparison_integrity_errors,
        "BLIND_ELIGIBLE_COUNT_MISMATCH",
        problems,
    )

    group_count_mismatch = deepcopy(ready)
    core = next(
        run for run in group_count_mismatch["runs"]
        if run["workflow"] == "ALPHA3_CORE_CANDIDATE"
    )
    core["blind_first_round"]["independence_group_count"] = 99
    expect_error(
        "blind group count mismatch",
        group_count_mismatch,
        comparison_integrity_errors,
        "BLIND_INDEPENDENCE_GROUP_COUNT_MISMATCH",
        problems,
    )

    independent_overclaim = deepcopy(ready)
    core = next(
        run for run in independent_overclaim["runs"]
        if run["workflow"] == "ALPHA3_CORE_CANDIDATE"
    )
    core["participants"][1]["independence_group"] = "IG-A"
    core["blind_first_round"]["initial_responses"][1]["independence_group"] = "IG-A"
    core["blind_first_round"]["independence_group_count"] = 1
    expect_error(
        "independent convergence overclaim",
        independent_overclaim,
        comparison_integrity_errors,
        "INDEPENDENT_CONVERGENCE_ELIGIBLE_GROUP_COUNT",
        problems,
    )

    missing_backlink = deepcopy(claim)
    missing_backlink["claims"][0]["verification_status"] = "SOURCE_MATCHED"
    for evidence in missing_backlink["evidence"]:
        evidence["supports_claim_refs"] = []
    expect_error(
        "claim evidence backlink",
        missing_backlink,
        claim_integrity_errors,
        "CLAIM_EVIDENCE_BACKLINK_MISSING",
        problems,
    )

    duplicate_source = deepcopy(claim)
    duplicate_migration = deepcopy(duplicate_source["migration_records"][0])
    duplicate_migration["migration_id"] = "MIG-FACT-002"
    duplicate_source["migration_records"].append(duplicate_migration)
    expect_error(
        "duplicate source FACT migration",
        duplicate_source,
        claim_integrity_errors,
        "DUPLICATE_SOURCE_FACT_MIGRATION",
        problems,
    )
    return problems


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate Core Candidate comparison and Claim/Evidence integrity."
    )
    parser.add_argument("--comparison", action="append", default=[])
    parser.add_argument("--claim-evidence", action="append", default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    problems = regression_tests()

    template_errors = validate_document(base.TEMPLATE, "comparison")
    if template_errors:
        problems.append(f"comparison template integrity failure: {template_errors}")

    for value in args.comparison:
        path = Path(value)
        errors = validate_document(path, "comparison")
        if errors:
            problems.append(f"comparison artifact {path}: {errors}")
    for value in args.claim_evidence:
        path = Path(value)
        errors = validate_document(path, "claim_evidence")
        if errors:
            problems.append(f"Claim/Evidence artifact {path}: {errors}")

    if problems:
        for problem in problems:
            print("FAIL:", problem, file=sys.stderr)
        return 1
    print(
        "alpha.3 Core Candidate evidence integrity: PASS "
        "(recomputed blind counts, exact workflow coverage, commit parity, "
        "bidirectional evidence links, unique source FACT migration)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
