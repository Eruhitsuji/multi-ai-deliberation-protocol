#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import copy
import hashlib
import re
import subprocess
import sys
import yaml

from generate_validation_receipt_v030_alpha3 import build_receipt

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml"
RAW_REL = "docs/evaluation/evidence/v0.3.0-alpha.3/.synthetic-release-observation.md"
RAW = ROOT / RAW_REL
CHECKER = ROOT / "scripts/check_alpha3_field_trial.py"
REPORT_SCHEMA_REL = "schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml"
SCENARIOS = [
    "USAB-QUICK-001",
    "USAB-COMMAND-COMPAT-001",
    "USAB-RELAY-001",
    "USAB-LIMITED-001",
    "USAB-RECOVERY-001",
    "USAB-TEAM-001",
    "USAB-MINUTES-001",
    "USAB-HELP-001",
]
VALIDATION_TARGETS = [
    {
        "target_path": "registries/v0.3.0-alpha.2/commands.yaml",
        "schema_path": "schemas/v0.3.0-alpha.2/command-registry.schema.yaml",
        "artifact_type": "COMMAND_REGISTRY",
        "artifact_id": "COMMANDS-A2",
    },
    {
        "target_path": "registries/v0.3.0-alpha.3/commands.yaml",
        "schema_path": "schemas/v0.3.0-alpha.3/command-registry.schema.yaml",
        "artifact_type": "COMMAND_REGISTRY",
        "artifact_id": "COMMANDS-A3",
    },
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def loader_config() -> dict:
    text = (ROOT / "bootstrap/alpha3/load-protocol-from-github.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, "loader frontmatter missing"
    return yaml.safe_load(match.group(1))


def sources_for(profile: str, config: dict) -> list[str]:
    output: list[str] = []
    for set_name in config["load_profiles"][profile]["required_sets"]:
        output.extend(config["source_sets"][set_name])
    return output


def receipt_for_target(target: dict) -> dict:
    artifact_path = ROOT / target["target_path"]
    schema_path = ROOT / target["schema_path"]
    artifact_bytes = artifact_path.read_bytes()
    schema_bytes = schema_path.read_bytes()
    artifact = yaml.safe_load(artifact_bytes)
    schema = yaml.safe_load(schema_bytes)
    suffix = "A2" if target["artifact_id"].endswith("A2") else "A3"
    return build_receipt(
        artifact_value=artifact,
        artifact_bytes=artifact_bytes,
        artifact_type=target["artifact_type"],
        artifact_id=target["artifact_id"],
        artifact_locator=f"repo://{target['target_path']}",
        artifact_version=artifact["registry_version"],
        canonicalization="RAW_BYTES",
        schema_value=schema,
        schema_bytes=schema_bytes,
        schema_path=target["schema_path"],
        receipt_id=f"VAL-REGISTRY-{suffix}",
        executor_type="CI_WORKFLOW",
        executor_name="synthetic-field-trial-release-test",
        executor_version="2",
    )


def build_results() -> dict:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    config = loader_config()
    sources = sources_for("FIELD_TRIAL", config)
    digest = hashlib.sha256(("\n".join(sources) + "\n").encode("utf-8")).hexdigest()
    quick = "bootstrap/alpha3/quick-start.md"
    verified = "bootstrap/alpha3/verified-start.md"
    run_id = "SYNTHETIC-RUN-001"
    report_id = "PLR-SYNTH-001"
    report_receipt_id = "VAL-SYNTH-REPORT"

    target_receipts = [receipt_for_target(target) for target in VALIDATION_TARGETS]
    records = []
    for target, receipt_document in zip(VALIDATION_TARGETS, target_receipts):
        artifact = yaml.safe_load((ROOT / target["target_path"]).read_text(encoding="utf-8"))
        records.append(
            {
                "target_ref": f"repo://{target['target_path']}",
                "target_sha256": sha(ROOT / target["target_path"]),
                "artifact_type": target["artifact_type"],
                "artifact_id": target["artifact_id"],
                "artifact_version": artifact["registry_version"],
                "schema_path": target["schema_path"],
                "schema_sha256": sha(ROOT / target["schema_path"]),
                "receipt_ref": receipt_document["VALIDATION_RECEIPT"]["receipt_id"],
                "result": "PASS",
            }
        )

    report = {
        "report_version": "MADP-PROTOCOL-LOAD-REPORT-v2",
        "report_id": report_id,
        "revision": 1,
        "supersedes": None,
        "active": True,
        "protocol_version": "MADP-v0.3.0-alpha.3",
        "load_profile": "FIELD_TRIAL",
        "repository": "Eruhitsuji/multi-ai-deliberation-protocol",
        "repository_commit": commit,
        "inventory_digest_algorithm": "sha256-newline-paths-v1",
        "source_inventory_digest": digest,
        "capability_preflight": {
            "exact_byte_retrieval": True,
            "sha256_available": True,
            "schema_validator_available": True,
            "complete_bundle_available": True,
            "selected_source_mode": "GITHUB_CONNECTOR",
        },
        "status": "COMPLETE",
        "files": [
            {
                "path": path,
                "status": "READ",
                "access_method": "GITHUB_CONNECTOR",
                "source_ref": f"repo://{commit}/{path}",
                "content_sha256": sha(ROOT / path),
            }
            for path in sources
        ],
        "all_required_files_read": True,
        "schema_validation_capability": "EXECUTED",
        "schema_validation_executed": True,
        "schemas_applicable": [target["schema_path"] for target in VALIDATION_TARGETS],
        "schemas_executed": [target["schema_path"] for target in VALIDATION_TARGETS],
        "schema_validation_records": records,
        "unvalidated_structured_sources": [],
        "inferred_unread_content": False,
        "provenance_level": "HASH_VERIFIED",
        "authorized_start_profiles": [
            {
                "path": quick,
                "repository": "Eruhitsuji/multi-ai-deliberation-protocol",
                "repository_commit": commit,
                "source_ref": f"repo://{commit}/{quick}",
                "content_sha256": sha(ROOT / quick),
            },
            {
                "path": verified,
                "repository": "Eruhitsuji/multi-ai-deliberation-protocol",
                "repository_commit": commit,
                "source_ref": f"repo://{commit}/{verified}",
                "content_sha256": sha(ROOT / verified),
            },
        ],
        "validation_receipt_refs": [
            target_receipts[0]["VALIDATION_RECEIPT"]["receipt_id"],
            target_receipts[1]["VALIDATION_RECEIPT"]["receipt_id"],
            report_receipt_id,
        ],
        "limitations": [],
        "next_action": {"command": "APPLY_START_PROFILE", "accepted_input": quick},
    }
    report_document = {"PROTOCOL_LOAD_REPORT": report}
    report_schema_path = ROOT / REPORT_SCHEMA_REL
    report_receipt = build_receipt(
        artifact_value=report_document,
        artifact_bytes=yaml.safe_dump(report_document, sort_keys=False, allow_unicode=True).encode("utf-8"),
        artifact_type="PROTOCOL_LOAD_REPORT",
        artifact_id=report_id,
        artifact_locator=f"trial://{run_id}/protocol-load-report",
        artifact_revision=1,
        canonicalization="MADP_CANONICAL_JSON_V1",
        schema_value=yaml.safe_load(report_schema_path.read_bytes()),
        schema_bytes=report_schema_path.read_bytes(),
        schema_path=REPORT_SCHEMA_REL,
        receipt_id=report_receipt_id,
        executor_type="CI_WORKFLOW",
        executor_name="synthetic-field-trial-release-test",
        executor_version="2",
    )
    assert report_receipt["VALIDATION_RECEIPT"]["result"] == "PASS"

    rows = [
        {
            "trial_id": f"{run_id}-{scenario_id}",
            "run_id": run_id,
            "scenario_id": scenario_id,
            "observation_refs": ["OBS-SYNTH-PRIMARY"],
            "task_completed": True,
            "next_action_understood": True,
            "recovery_attempts": 0,
            "eligible_workflow_transitions": 1,
            "unnecessary_user_pauses": 0,
            "critical_authority_errors": 0,
            "critical_unnecessary_pauses": 0,
            "expected_behavior": "Synthetic release-path conformance fixture.",
            "actual_behavior": "All run-normalized receipt-bound checks passed.",
            "reviewer": "CI",
            "notes": "Synthetic data; not human field-trial evidence.",
        }
        for scenario_id in SCENARIOS
    ]
    return {
        "protocol_version": "MADP-v0.3.0-alpha.3",
        "results_version": 6,
        "automated_walkthrough": {
            "status": "PASS",
            "scenario_count": 8,
            "checks": {
                "all_scenarios_have_success_condition": "PASS",
                "all_scenarios_map_required_features": "PASS",
                "next_action_coverage": "PASS",
                "authority_invariant_coverage": "PASS",
                "alpha2_command_compatibility_coverage": "PASS",
            },
        },
        "manual_trials": {
            "status": "PASS",
            "field_trial_evidence_version": "MADP-FIELD-TRIAL-EVIDENCE-v2",
            "protocol_load_report_required": True,
            "required_load_report_version": "MADP-PROTOCOL-LOAD-REPORT-v2",
            "required_load_profile": "FIELD_TRIAL",
            "required_provenance": "HASH_VERIFIED",
            "required_receipt_schema": "schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml",
            "evidence_root": "docs/evaluation/evidence/v0.3.0-alpha.3",
            "participants": [
                {
                    "participant_id": "SYNTHETIC-MODEL",
                    "client": "CI",
                    "displayed_model_label": "synthetic",
                    "reasoning_mode": "deterministic",
                }
            ],
            "validation_receipts": [*target_receipts, report_receipt],
            "run_evidence": [
                {
                    "run_id": run_id,
                    "participant_id": "SYNTHETIC-MODEL",
                    "run_index": 1,
                    "tested_commit": commit,
                    "protocol_load_report": report,
                    "protocol_load_report_receipt_id": report_receipt_id,
                    "start_profile_binding": {
                        "repository": "Eruhitsuji/multi-ai-deliberation-protocol",
                        "repository_commit": commit,
                        "path": quick,
                        "source_ref": f"repo://{commit}/{quick}",
                        "source_inventory_digest": digest,
                        "content_sha256": sha(ROOT / quick),
                    },
                    "observations": [
                        {
                            "observation_id": "OBS-SYNTH-PRIMARY",
                            "kind": "PRIMARY_CHAT",
                            "path": RAW_REL,
                            "sha256": sha(RAW),
                        }
                    ],
                }
            ],
            "scenario_results": rows,
            "metrics": {
                "trial_count": 8,
                "task_completion_rate": 1.0,
                "critical_authority_errors": 0,
                "eligible_workflow_transitions": 8,
                "unnecessary_user_pauses": 0,
                "unnecessary_pause_rate": 0.0,
                "critical_unnecessary_pauses": 0,
                "next_action_understood_rate": 1.0,
                "median_recovery_attempts": 0,
            },
            "pause_classification_records": [],
            "sign_off": {
                "approved_by": ["SYNTHETIC-CI"],
                "approved_at": "2000-01-01T00:00:00Z",
            },
        },
        "limitations": ["Synthetic release-path fixture; it does not replace human field-trial evidence."],
    }


def run_checker() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--release"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def main() -> int:
    original = RESULTS.read_bytes()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    raw_existed = RAW.exists()
    raw_original = RAW.read_bytes() if raw_existed else None
    try:
        RAW.write_text(
            "# Synthetic alpha.3 release evidence\n\nThis file exists only while the release-path checker test runs.\n",
            encoding="utf-8",
        )
        document = build_results()
        RESULTS.write_text(yaml.safe_dump(document, sort_keys=False, allow_unicode=True), encoding="utf-8")
        success = run_checker()
        assert success.returncode == 0, success.stderr or success.stdout

        tampered = copy.deepcopy(document)
        tampered["manual_trials"]["run_evidence"][0]["observations"][0]["sha256"] = "0" * 64
        RESULTS.write_text(yaml.safe_dump(tampered, sort_keys=False, allow_unicode=True), encoding="utf-8")
        failure = run_checker()
        assert failure.returncode != 0
        assert "raw observation hash mismatch" in failure.stderr

        unknown = copy.deepcopy(document)
        unknown["manual_trials"]["scenario_results"][0]["observation_refs"] = ["OBS-NOT-FOUND"]
        RESULTS.write_text(yaml.safe_dump(unknown, sort_keys=False, allow_unicode=True), encoding="utf-8")
        failure = run_checker()
        assert failure.returncode != 0
        assert "unknown observation reference" in failure.stderr

        print("MADP-v0.3.0-alpha.3 run-normalized release evidence: PASS")
        return 0
    finally:
        RESULTS.write_bytes(original)
        if raw_existed:
            assert raw_original is not None
            RAW.write_bytes(raw_original)
        elif RAW.exists():
            RAW.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
