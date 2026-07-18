#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
COMPARISON_SCHEMA = ROOT / "schemas/v0.3.0-alpha.3/experimental/core-candidate-comparison.schema.yaml"
CLAIM_SCHEMA = ROOT / "schemas/v0.3.0-alpha.3/experimental/claim-evidence-candidate.schema.yaml"
FIXTURES = ROOT / "tests/v0.3.0-alpha.3/core-candidate-experiment-fixtures.yaml"
TEMPLATE = ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-core-candidate-comparison-template.yaml"

EXPECTED_WORKFLOWS = {
    "MANUAL_MULTI_AI",
    "STANDARD_ALPHA3",
    "ALPHA3_CORE_CANDIDATE",
    "MARKDOWN_VALIDATOR",
}
READY_STATUSES = {"READY_FOR_REVIEW", "HUMAN_REVIEWED"}
UPGRADE_ORDER = {"UNCHECKED": 0, "SOURCE_MATCHED": 1, "CORROBORATED": 2}


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def first_error(validator, artifact):
    errors = sorted(validator.iter_errors(artifact), key=lambda error: list(error.path))
    return errors[0].message if errors else None


def h(char: str) -> str:
    return char * 64


def participant(participant_id: str, group: str):
    return {
        "participant_id": participant_id,
        "service": "Fixture Service",
        "model_label": "Fixture Model",
        "chat_context_id": f"CHAT-{participant_id}",
        "independence_group": group,
        "correlation_status": "DISTINCT_CONTEXT_KNOWN",
    }


def initial_response(response_id: str, participant_id: str, group: str, digest_char: str):
    return {
        "response_id": response_id,
        "participant_id": participant_id,
        "independence_group": group,
        "raw_response_ref": f"raw/{response_id}.md",
        "raw_response_sha256": h(digest_char),
        "captured_before_cross_exposure": True,
        "exposure_state": "UNEXPOSED",
        "exposed_response_refs": [],
    }


def metrics():
    return {
        "completion_time_seconds": 120,
        "human_actions": 4,
        "canonical_commands": 0,
        "corrections": 0,
        "unclear_next_actions": 0,
        "authority_errors": 0,
        "stale_revision_errors": 0,
        "user_burden": 2,
    }


def result(decision_ref: str, conformance: str = "NOT_EVALUATED"):
    return {
        "task_completed": True,
        "raw_records_preserved": True,
        "authority_boundary_recorded": True,
        "material_dissent_count": 0,
        "dissent_preserved_count": 0,
        "decision_reconstruction": "PASS",
        "core_conformance": conformance,
        "decision_record_ref": decision_ref,
        "notes": "",
    }


def nonblind(required: bool):
    return {
        "required": required,
        "status": "NOT_PERFORMED",
        "information_set_hash": None,
        "initial_responses": [],
        "eligible_initial_response_count": 0,
        "independence_group_count": 0,
        "convergence_classification": "NOT_EVALUATED",
        "conformance_eligible": False,
        "reasons": ["Blind round not performed."],
    }


def valid_blind():
    return {
        "required": True,
        "status": "VALID",
        "information_set_hash": h("c"),
        "initial_responses": [
            initial_response("R-A", "P-A", "IG-A", "a"),
            initial_response("R-B", "P-B", "IG-B", "b"),
        ],
        "eligible_initial_response_count": 2,
        "independence_group_count": 2,
        "convergence_classification": "INDEPENDENT_CONVERGENCE",
        "conformance_eligible": True,
        "reasons": [],
    }


def degraded_blind():
    response = initial_response("R-X", "P-CORE-DEG", "IG-1", "f")
    response.update(
        {
            "captured_before_cross_exposure": False,
            "exposure_state": "EXPOSED",
            "exposed_response_refs": ["R-OTHER"],
        }
    )
    return {
        "required": True,
        "status": "ANCHORING_EXPOSED",
        "information_set_hash": h("f"),
        "initial_responses": [response],
        "eligible_initial_response_count": 0,
        "independence_group_count": 1,
        "convergence_classification": "CORRELATED_CONVERGENCE",
        "conformance_eligible": False,
        "reasons": ["Prior conclusion exposed."],
    }


def run(run_id: str, workflow: str, *, alpha3: bool = False, core: bool = False):
    if core:
        participants = [participant("P-A", "IG-A"), participant("P-B", "IG-B")]
        blind = valid_blind()
    else:
        participants = [participant(f"P-{run_id}", "IG-1")]
        blind = nonblind(False)
    return {
        "run_id": run_id,
        "workflow": workflow,
        "tested_commit": "b" * 40 if alpha3 else None,
        "protocol_binding": {
            "status": "BOUND" if alpha3 else "NOT_APPLICABLE",
            "source_ref": "repo://fixture" if alpha3 else "local-workflow",
            "source_digest": h("d") if alpha3 else None,
        },
        "participants": participants,
        "blind_first_round": blind,
        "metrics": metrics(),
        "result": result(f"DEC-{run_id}", "CONFORMING" if core else "NOT_EVALUATED"),
    }


def comparison_base(experiment_id: str, status: str, runs):
    return {
        "experiment_version": "MADP-CORE-CANDIDATE-COMPARISON-v1",
        "protocol_version": "MADP-v0.3.0-alpha.3",
        "experiment_id": experiment_id,
        "experiment_status": status,
        "decision_ref": "docs/planning/DEC-MADP-CORE-001.yaml",
        "formal_release_evidence": False,
        "task": {
            "task_id": "TASK-1",
            "title": "Bounded decision",
            "prompt_sha256": h("e") if status in READY_STATUSES else None,
            "authority_boundary": "PROPOSE_ONLY",
            "acceptance_criteria": ["Record a human decision."],
        },
        "runs": runs,
        "conclusion": {
            "review_status": "NOT_REVIEWED",
            "alpha4_recommendation": "NOT_EVALUATED",
            "alpha4_authorized": False,
            "reviewer": None,
            "rationale": None,
        },
    }


def build_comparison(builder: str):
    if builder == "READY_VALID":
        return comparison_base(
            "EXP-VALID",
            "READY_FOR_REVIEW",
            [
                run("MANUAL", "MANUAL_MULTI_AI"),
                run("A3", "STANDARD_ALPHA3", alpha3=True),
                run("CORE", "ALPHA3_CORE_CANDIDATE", alpha3=True, core=True),
                run("MD", "MARKDOWN_VALIDATOR"),
            ],
        )
    if builder == "DRAFT_DEGRADED":
        core_run = run("CORE-DEG", "ALPHA3_CORE_CANDIDATE")
        core_run["participants"] = [participant("P-CORE-DEG", "IG-1")]
        core_run["blind_first_round"] = degraded_blind()
        core_run["result"] = result("DEC-CORE-DEG", "DEGRADED")
        return comparison_base("EXP-DEGRADED", "DRAFT", [core_run])
    raise ValueError(f"unknown comparison builder: {builder}")


def build_claim():
    return {
        "artifact_version": "MADP-CLAIM-EVIDENCE-CANDIDATE-v1",
        "protocol_version": "MADP-v0.3.0-alpha.3",
        "package_id": "CE-VALID",
        "record_status": "HUMAN_REVIEWED",
        "existing_fact_records_preserved": True,
        "speech_form_separated_from_verification": True,
        "claims": [
            {
                "claim_id": "CLM-001",
                "revision": 1,
                "source_state_version": 7,
                "statement": "The selected workflow reduces unclear next actions.",
                "claim_kind": "MODEL_INFERENCE",
                "verification_status": "CORROBORATED",
                "raw_response_refs": ["RAW-001", "RAW-002"],
                "evidence_refs": ["EV-001", "EV-002"],
                "dissent_refs": ["DIS-001"],
            }
        ],
        "evidence": [
            {
                "evidence_id": "EV-001",
                "source_ref": "raw/metrics-run-a.yaml",
                "source_digest": h("d"),
                "assessment": {
                    "source_role": "DIRECT_RECORD",
                    "claim_fit": "DIRECT",
                    "freshness": "CURRENT",
                    "traceability": "SNAPSHOT_HASHED",
                    "source_independence": "SINGLE_SOURCE",
                },
                "supports_claim_refs": ["CLM-001"],
                "challenges_claim_refs": [],
            },
            {
                "evidence_id": "EV-002",
                "source_ref": "raw/metrics-run-b.yaml",
                "source_digest": h("e"),
                "assessment": {
                    "source_role": "DIRECT_RECORD",
                    "claim_fit": "DIRECT",
                    "freshness": "CURRENT",
                    "traceability": "SNAPSHOT_HASHED",
                    "source_independence": "INDEPENDENTLY_CORROBORATED",
                },
                "supports_claim_refs": ["CLM-001"],
                "challenges_claim_refs": [],
            },
        ],
        "migration_records": [
            {
                "migration_id": "MIG-FACT-001",
                "source_fact_ref": "FACT-001@1",
                "source_fact_revision": 1,
                "source_fact_preserved": True,
                "target_claim_ref": "CLM-001",
                "mapping_status": "PARTIAL",
                "ambiguities": [
                    "Legacy FACT combined assertion form and verification state."
                ],
                "verification_status_before": "UNCHECKED",
                "verification_status_after": "CORROBORATED",
                "verification_change_basis": "EVIDENCE_REVIEWED",
                "human_review_required": True,
            }
        ],
    }


def apply_mutation(section: str, artifact, mutation: str | None):
    if not mutation:
        return artifact
    artifact = deepcopy(artifact)
    if section == "comparison":
        if mutation == "FORMAL_RELEASE_EVIDENCE_TRUE":
            artifact["formal_release_evidence"] = True
        elif mutation == "BLIND_EXPOSED_AS_VALID":
            blind = artifact["runs"][0]["blind_first_round"]
            blind["status"] = "VALID"
            blind["conformance_eligible"] = True
            blind["eligible_initial_response_count"] = 1
        elif mutation == "REMOVE_MARKDOWN_WORKFLOW":
            artifact["runs"] = [
                item for item in artifact["runs"]
                if item["workflow"] != "MARKDOWN_VALIDATOR"
            ]
        elif mutation == "INDEPENDENT_CONVERGENCE_ONE_GROUP":
            core = next(
                item for item in artifact["runs"]
                if item["workflow"] == "ALPHA3_CORE_CANDIDATE"
            )
            core["blind_first_round"]["independence_group_count"] = 1
        else:
            raise ValueError(f"unknown comparison mutation: {mutation}")
    else:
        migration = artifact["migration_records"][0]
        if mutation == "FACT_NOT_PRESERVED":
            artifact["existing_fact_records_preserved"] = False
        elif mutation == "UNKNOWN_EVIDENCE_REF":
            artifact["claims"][0]["evidence_refs"].append("EV-MISSING")
        elif mutation == "UPGRADE_MARKED_PRESERVED":
            migration["verification_change_basis"] = "PRESERVED"
        elif mutation == "EXACT_WITH_AMBIGUITY":
            migration["mapping_status"] = "EXACT"
        elif mutation == "QUARANTINE_WITHOUT_REVIEW":
            migration["mapping_status"] = "QUARANTINED"
            migration["human_review_required"] = False
        else:
            raise ValueError(f"unknown claim mutation: {mutation}")
    return artifact


def build_fixture(section: str, case):
    builder = case.get("builder")
    artifact = build_comparison(builder) if section == "comparison" else build_claim()
    return apply_mutation(section, artifact, case.get("mutation"))


def comparison_semantic_errors(document) -> list[str]:
    errors: list[str] = []
    runs = document.get("runs", []) if isinstance(document, dict) else []
    run_ids = [run.get("run_id") for run in runs if isinstance(run, dict)]
    if len(run_ids) != len(set(run_ids)):
        errors.append("DUPLICATE_RUN_ID")

    status = document.get("experiment_status")
    workflows = {run.get("workflow") for run in runs if isinstance(run, dict)}
    if status in READY_STATUSES:
        if workflows != EXPECTED_WORKFLOWS:
            errors.append("MISSING_COMPARISON_WORKFLOW")
        if document.get("task", {}).get("prompt_sha256") is None:
            errors.append("READY_TASK_PROMPT_HASH_REQUIRED")

    for item in runs:
        if not isinstance(item, dict):
            continue
        workflow = item.get("workflow")
        participants = item.get("participants", [])
        participant_ids = [row.get("participant_id") for row in participants if isinstance(row, dict)]
        if len(participant_ids) != len(set(participant_ids)):
            errors.append("DUPLICATE_PARTICIPANT_ID")
        participant_groups = {
            row.get("participant_id"): row.get("independence_group")
            for row in participants if isinstance(row, dict)
        }

        if status in READY_STATUSES:
            if not participants:
                errors.append("READY_RUN_PARTICIPANTS_REQUIRED")
            if any(value is None for value in item.get("metrics", {}).values()):
                errors.append("INCOMPLETE_READY_METRICS")
            result_row = item.get("result", {})
            required_values = (
                result_row.get("task_completed"),
                result_row.get("raw_records_preserved"),
                result_row.get("authority_boundary_recorded"),
                result_row.get("material_dissent_count"),
                result_row.get("dissent_preserved_count"),
                result_row.get("decision_reconstruction"),
            )
            if any(value is None for value in required_values):
                errors.append("INCOMPLETE_READY_RESULT")
            if workflow in {"STANDARD_ALPHA3", "ALPHA3_CORE_CANDIDATE"}:
                binding = item.get("protocol_binding", {})
                if item.get("tested_commit") is None:
                    errors.append("READY_ALPHA3_TESTED_COMMIT_REQUIRED")
                if binding.get("status") != "BOUND" or binding.get("source_digest") is None:
                    errors.append("READY_ALPHA3_PROTOCOL_BINDING_REQUIRED")

        binding = item.get("protocol_binding", {})
        if binding.get("status") == "BOUND" and binding.get("source_digest") is None:
            errors.append("BOUND_PROTOCOL_DIGEST_REQUIRED")

        blind = item.get("blind_first_round", {})
        responses = blind.get("initial_responses", [])
        response_ids = [row.get("response_id") for row in responses if isinstance(row, dict)]
        if len(response_ids) != len(set(response_ids)):
            errors.append("DUPLICATE_INITIAL_RESPONSE_ID")
        eligible = []
        for response in responses:
            participant_id = response.get("participant_id")
            if participant_id not in participant_groups:
                errors.append("BLIND_RESPONSE_UNKNOWN_PARTICIPANT")
            elif participant_groups[participant_id] != response.get("independence_group"):
                errors.append("BLIND_RESPONSE_GROUP_MISMATCH")
            if (
                response.get("captured_before_cross_exposure") is True
                and response.get("exposure_state") == "UNEXPOSED"
            ):
                eligible.append(response)

        blind_status = blind.get("status")
        if blind_status == "VALID":
            if len(responses) < 2 or blind.get("eligible_initial_response_count", 0) < 2:
                errors.append("BLIND_VALID_ELIGIBLE_COUNT")
            if blind.get("eligible_initial_response_count") != len(eligible):
                errors.append("BLIND_VALID_ELIGIBLE_COUNT")
            if len(eligible) != len(responses):
                errors.append("BLIND_VALID_EXPOSURE_MISMATCH")
            if blind.get("conformance_eligible") is not True:
                errors.append("BLIND_VALID_CONFORMANCE_FLAG")
        elif blind.get("conformance_eligible") is True:
            errors.append("BLIND_NONVALID_CONFORMANCE")

        if (
            blind.get("convergence_classification") == "INDEPENDENT_CONVERGENCE"
            and blind.get("independence_group_count", 0) < 2
        ):
            errors.append("INDEPENDENT_CONVERGENCE_GROUP_COUNT")

        result_row = item.get("result", {})
        material = result_row.get("material_dissent_count")
        preserved = result_row.get("dissent_preserved_count")
        if material is not None and preserved is not None and preserved > material:
            errors.append("DISSENT_PRESERVED_EXCEEDS_MATERIAL")
        if result_row.get("task_completed") is True and not result_row.get("decision_record_ref"):
            errors.append("COMPLETED_DECISION_REF_MISSING")

        if workflow == "ALPHA3_CORE_CANDIDATE":
            if blind.get("required") is not True:
                errors.append("CORE_BLIND_REQUIRED")
            if result_row.get("core_conformance") == "CONFORMING":
                if blind_status != "VALID" or blind.get("conformance_eligible") is not True:
                    errors.append("CORE_CONFORMING_BLIND_INVALID")
                if result_row.get("raw_records_preserved") is not True:
                    errors.append("CORE_CONFORMING_RAW_RECORD_MISSING")
                if result_row.get("authority_boundary_recorded") is not True:
                    errors.append("CORE_CONFORMING_AUTHORITY_MISSING")

    conclusion = document.get("conclusion", {}) if isinstance(document, dict) else {}
    if status == "HUMAN_REVIEWED":
        if conclusion.get("review_status") != "HUMAN_REVIEWED":
            errors.append("REVIEW_STATUS_MISMATCH")
        if not conclusion.get("reviewer") or not conclusion.get("rationale"):
            errors.append("HUMAN_REVIEW_FIELDS_REQUIRED")
    elif conclusion.get("review_status") == "HUMAN_REVIEWED":
        errors.append("REVIEW_STATUS_MISMATCH")
    return errors


def claim_semantic_errors(document) -> list[str]:
    errors: list[str] = []
    claims = document.get("claims", []) if isinstance(document, dict) else []
    evidence = document.get("evidence", []) if isinstance(document, dict) else []
    migrations = document.get("migration_records", []) if isinstance(document, dict) else []

    claim_ids = [item.get("claim_id") for item in claims if isinstance(item, dict)]
    evidence_ids = [item.get("evidence_id") for item in evidence if isinstance(item, dict)]
    migration_ids = [item.get("migration_id") for item in migrations if isinstance(item, dict)]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("DUPLICATE_CLAIM_ID")
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("DUPLICATE_EVIDENCE_ID")
    if len(migration_ids) != len(set(migration_ids)):
        errors.append("DUPLICATE_MIGRATION_ID")

    claim_set = set(claim_ids)
    evidence_set = set(evidence_ids)
    evidence_by_id = {
        item.get("evidence_id"): item for item in evidence if isinstance(item, dict)
    }

    for claim in claims:
        refs = set(claim.get("evidence_refs", []))
        if not refs.issubset(evidence_set):
            errors.append("UNKNOWN_EVIDENCE_REF")
        if claim.get("verification_status") == "SOURCE_MATCHED" and not refs:
            errors.append("SOURCE_MATCHED_REQUIRES_EVIDENCE")
        if claim.get("verification_status") == "CORROBORATED":
            supporting = [
                evidence_by_id[ref]
                for ref in refs
                if ref in evidence_by_id
                and claim.get("claim_id") in evidence_by_id[ref].get("supports_claim_refs", [])
            ]
            if not any(
                row.get("assessment", {}).get("source_independence")
                == "INDEPENDENTLY_CORROBORATED"
                for row in supporting
            ):
                errors.append("CORROBORATED_REQUIRES_INDEPENDENT_EVIDENCE")

    for row in evidence:
        refs = set(row.get("supports_claim_refs", [])) | set(row.get("challenges_claim_refs", []))
        if not refs.issubset(claim_set):
            errors.append("EVIDENCE_UNKNOWN_CLAIM_REF")
        if (
            row.get("assessment", {}).get("traceability") == "SNAPSHOT_HASHED"
            and row.get("source_digest") is None
        ):
            errors.append("HASHED_TRACEABILITY_REQUIRES_DIGEST")

    for migration in migrations:
        if migration.get("target_claim_ref") not in claim_set:
            errors.append("MIGRATION_UNKNOWN_TARGET_CLAIM")
        mapping = migration.get("mapping_status")
        ambiguities = migration.get("ambiguities", [])
        human_review = migration.get("human_review_required")
        if mapping == "EXACT" and ambiguities:
            errors.append("EXACT_MAPPING_HAS_AMBIGUITIES")
        if mapping in {"PARTIAL", "QUARANTINED"} and human_review is not True:
            errors.append(
                "QUARANTINED_REQUIRES_HUMAN_REVIEW"
                if mapping == "QUARANTINED"
                else "PARTIAL_MAPPING_REQUIRES_HUMAN_REVIEW"
            )

        before = migration.get("verification_status_before")
        after = migration.get("verification_status_after")
        basis = migration.get("verification_change_basis")
        if before != after and basis == "PRESERVED":
            errors.append("VERIFICATION_CHANGE_MARKED_PRESERVED")
        if (
            before in UPGRADE_ORDER
            and after in UPGRADE_ORDER
            and UPGRADE_ORDER[after] > UPGRADE_ORDER[before]
            and basis != "EVIDENCE_REVIEWED"
        ):
            errors.append("VERIFICATION_UPGRADE_WITHOUT_EVIDENCE_REVIEW")
        if basis == "DOWNGRADED_FOR_UNCERTAINTY" and after not in {
            "UNCHECKED", "DISPUTED", "REFUTED", "OUTDATED"
        }:
            errors.append("INVALID_UNCERTAINTY_DOWNGRADE")
    return errors


def main() -> int:
    problems: list[str] = []
    required = [
        COMPARISON_SCHEMA,
        CLAIM_SCHEMA,
        FIXTURES,
        TEMPLATE,
        ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-core-candidate-comparative-evaluation.md",
        ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-blind-first-round-operational-test.md",
        ROOT / "docs/migration/MADP-v0.3.0-alpha.3-claim-evidence-candidate-migration.md",
    ]
    for path in required:
        if not path.is_file():
            problems.append(f"missing Core Candidate experiment file: {path.relative_to(ROOT)}")
    if problems:
        for problem in problems:
            print("FAIL:", problem, file=sys.stderr)
        return 1

    validators = {}
    for name, path in (("comparison", COMPARISON_SCHEMA), ("claim_evidence", CLAIM_SCHEMA)):
        try:
            schema = load(path)
            Draft202012Validator.check_schema(schema)
            validators[name] = Draft202012Validator(schema)
        except Exception as exc:
            problems.append(f"invalid {name} schema: {exc}")

    fixture_data = load(FIXTURES)
    if fixture_data.get("fixture_version") != "MADP-CORE-CANDIDATE-EXPERIMENT-FIXTURES-v1":
        problems.append("fixture version mismatch")
    semantic_functions = {
        "comparison": comparison_semantic_errors,
        "claim_evidence": claim_semantic_errors,
    }
    for section, validator in validators.items():
        for case in fixture_data.get(section, {}).get("valid", []):
            artifact = build_fixture(section, case)
            error = first_error(validator, artifact)
            if error:
                problems.append(f"valid fixture {case.get('id')} failed schema: {error}")
            semantic = semantic_functions[section](artifact)
            if semantic:
                problems.append(f"valid fixture {case.get('id')} failed semantics: {semantic}")
        for case in fixture_data.get(section, {}).get("invalid_schema", []):
            artifact = build_fixture(section, case)
            if first_error(validator, artifact) is None:
                problems.append(f"invalid schema fixture unexpectedly passed: {case.get('id')}")
        for case in fixture_data.get(section, {}).get("invalid_semantic", []):
            artifact = build_fixture(section, case)
            schema_error = first_error(validator, artifact)
            if schema_error:
                problems.append(
                    f"semantic fixture must remain schema-valid: {case.get('id')}: {schema_error}"
                )
                continue
            semantic = semantic_functions[section](artifact)
            if case.get("expected_error") not in semantic:
                problems.append(
                    f"semantic fixture {case.get('id')} did not produce "
                    f"{case.get('expected_error')}: {semantic}"
                )

    template = load(TEMPLATE)
    if "comparison" in validators:
        error = first_error(validators["comparison"], template)
        if error:
            problems.append(f"comparison template failed schema: {error}")
        semantic = comparison_semantic_errors(template)
        if semantic:
            problems.append(f"comparison DRAFT template failed semantics: {semantic}")

    docs = {
        "docs/evaluation/MADP-v0.3.0-alpha.3-core-candidate-comparative-evaluation.md": [
            "MANUAL_MULTI_AI",
            "STANDARD_ALPHA3",
            "ALPHA3_CORE_CANDIDATE",
            "MARKDOWN_VALIDATOR",
            "does not complete `A3-REL-001`",
            "alpha.4 remains deferred",
        ],
        "docs/evaluation/MADP-v0.3.0-alpha.3-blind-first-round-operational-test.md": [
            "VALID",
            "PARTIALLY_COMPROMISED",
            "ANCHORING_EXPOSED",
            "NOT_PERFORMED",
            "direct cross-participant exposure",
        ],
        "docs/migration/MADP-v0.3.0-alpha.3-claim-evidence-candidate-migration.md": [
            "existing `FACT` records remain intact",
            "no automatic verification upgrade",
            "QUARANTINED",
            "UNKNOWN remains UNKNOWN",
        ],
    }
    for relative, markers in docs.items():
        body = (ROOT / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in body:
                problems.append(f"missing marker {marker!r}: {relative}")

    if problems:
        for problem in problems:
            print("FAIL:", problem, file=sys.stderr)
        return 1
    print(
        "alpha.3 Core Candidate operational experiments: PASS "
        "(2 experimental schemas, Blind First Round semantics, 4-workflow comparison, "
        "Claim/Evidence migration invariants)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
