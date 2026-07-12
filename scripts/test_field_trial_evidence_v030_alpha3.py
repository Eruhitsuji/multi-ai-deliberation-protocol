#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import yaml

from jsonschema import Draft202012Validator

from migrate_field_trial_results_v5_to_v6 import migrate_v5_to_v6

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/v0.3.0-alpha.3/field-trial-evidence.schema.yaml"
COLLECTION_TEST = ROOT / "scripts/test_field_trial_collection_v030_alpha3.py"


def legacy_row(trial_id: str, scenario_id: str, raw_ref: str, raw_sha: str) -> dict:
    return {
        "trial_id": trial_id,
        "participant_id": "MODEL-001",
        "run_index": 1,
        "scenario_id": scenario_id,
        "tested_commit": "1" * 40,
        "protocol_load_report": {
            "report_version": "MADP-PROTOCOL-LOAD-REPORT-v2",
            "report_id": "PLR-001",
        },
        "protocol_load_report_receipt_id": "VAL-PLR-001",
        "start_profile_binding": {
            "repository": "Eruhitsuji/multi-ai-deliberation-protocol",
            "repository_commit": "1" * 40,
            "path": "bootstrap/alpha3/quick-start.md",
            "source_ref": "repo://quick-start",
            "source_inventory_digest": "2" * 64,
            "content_sha256": "3" * 64,
        },
        "raw_observation_ref": raw_ref,
        "raw_observation_sha256": raw_sha,
        "task_completed": True,
        "next_action_understood": True,
        "recovery_attempts": 0,
        "eligible_workflow_transitions": 1,
        "unnecessary_user_pauses": 0,
        "critical_authority_errors": 0,
        "critical_unnecessary_pauses": 0,
        "expected_behavior": "expected",
        "actual_behavior": "actual",
        "reviewer": "Reviewer",
        "notes": "",
    }


def legacy_document() -> dict:
    return {
        "protocol_version": "MADP-v0.3.0-alpha.3",
        "results_version": 5,
        "automated_walkthrough": {
            "status": "PASS",
            "scenario_count": 8,
            "checks": {"coverage": "PASS"},
        },
        "manual_trials": {
            "status": "IN_PROGRESS",
            "protocol_load_report_required": True,
            "required_load_report_version": "MADP-PROTOCOL-LOAD-REPORT-v2",
            "required_load_profile": "FIELD_TRIAL",
            "required_provenance": "HASH_VERIFIED",
            "required_receipt_schema": "schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml",
            "evidence_root": "docs/evaluation/evidence/v0.3.0-alpha.3",
            "participants": [
                {
                    "participant_id": "MODEL-001",
                    "client": "Client",
                    "displayed_model_label": "Model",
                    "reasoning_mode": "Mode",
                }
            ],
            "validation_receipts": [],
            "scenario_results": [
                legacy_row(
                    "TRIAL-001",
                    "USAB-QUICK-001",
                    "evidence/primary.md",
                    "4" * 64,
                ),
                legacy_row(
                    "TRIAL-002",
                    "USAB-RELAY-001",
                    "evidence/relay.md",
                    "5" * 64,
                ),
            ],
            "metrics": {
                "trial_count": None,
                "task_completion_rate": None,
                "critical_authority_errors": None,
                "eligible_workflow_transitions": None,
                "unnecessary_user_pauses": None,
                "unnecessary_pause_rate": None,
                "critical_unnecessary_pauses": None,
                "next_action_understood_rate": None,
                "median_recovery_attempts": None,
            },
            "pause_classification_records": [],
            "sign_off": {"approved_by": [], "approved_at": None},
        },
        "limitations": ["fixture"],
    }


def main() -> int:
    migrated = migrate_v5_to_v6(legacy_document())
    assert migrated["results_version"] == 6
    manual = migrated["manual_trials"]
    assert manual["field_trial_evidence_version"] == "MADP-FIELD-TRIAL-EVIDENCE-v2"
    assert len(manual["run_evidence"]) == 1
    assert len(manual["run_evidence"][0]["observations"]) == 2
    assert len(manual["scenario_results"]) == 2
    assert all(
        row["run_id"] == "MODEL-001-R01"
        for row in manual["scenario_results"]
    )
    assert all(
        len(row["observation_refs"]) == 1
        for row in manual["scenario_results"]
    )

    schema = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    errors = list(Draft202012Validator(schema).iter_errors(migrated))
    assert not errors, errors[0].message if errors else ""

    conflicting = legacy_document()
    conflicting["manual_trials"]["scenario_results"][1]["start_profile_binding"][
        "path"
    ] = "bootstrap/alpha3/verified-start.md"
    try:
        migrate_v5_to_v6(conflicting)
    except ValueError as exc:
        assert "conflicting run-level evidence" in str(exc)
    else:
        raise AssertionError("conflicting run-level evidence was accepted")

    already = migrate_v5_to_v6(migrated)
    assert already == migrated

    collection = subprocess.run(
        [sys.executable, str(COLLECTION_TEST)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert collection.returncode == 0, collection.stderr or collection.stdout
    assert "field-trial collection tooling: PASS" in collection.stdout

    print(
        "MADP-v0.3.0-alpha.3 field-trial evidence migration and collection: PASS"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
