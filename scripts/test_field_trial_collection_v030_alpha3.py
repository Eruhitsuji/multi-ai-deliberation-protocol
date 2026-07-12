#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import copy
import shutil
import subprocess
import sys
import yaml

from test_alpha3_usability_release_evidence import RAW, build_results

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/collect_field_trial_evidence_v030_alpha3.py"
BASE_RESULTS = ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml"
WORK = ROOT / "docs/evaluation/evidence/v0.3.0-alpha.3/.collector-test"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def scenario_rows(observation_id: str) -> list[dict]:
    ids = [
        "USAB-QUICK-001",
        "USAB-COMMAND-COMPAT-001",
        "USAB-RELAY-001",
        "USAB-LIMITED-001",
        "USAB-RECOVERY-001",
        "USAB-TEAM-001",
        "USAB-MINUTES-001",
        "USAB-HELP-001",
    ]
    return [
        {
            "scenario_id": scenario_id,
            "observation_refs": [observation_id],
            "task_completed": True,
            "next_action_understood": True,
            "recovery_attempts": 0,
            "eligible_workflow_transitions": 1,
            "unnecessary_user_pauses": 0,
            "critical_authority_errors": 0,
            "critical_unnecessary_pauses": 0,
            "expected_behavior": "Collector fixture expected behavior.",
            "actual_behavior": "Collector fixture actual behavior.",
            "reviewer": "CI",
            "notes": "Synthetic collector fixture.",
        }
        for scenario_id in ids
    ]


def main() -> int:
    raw_existed = RAW.exists()
    raw_original = RAW.read_bytes() if raw_existed else None
    shutil.rmtree(WORK, ignore_errors=True)
    WORK.mkdir(parents=True)
    try:
        RAW.parent.mkdir(parents=True, exist_ok=True)
        RAW.write_text(
            "# Collector source\n\nSynthetic field-trial collector observation.\n",
            encoding="utf-8",
        )
        source_document = build_results()
        source_manual = source_document["manual_trials"]
        source_run = source_manual["run_evidence"][0]

        report_path = WORK / "load-report.yaml"
        report_path.write_text(
            yaml.safe_dump(
                {"PROTOCOL_LOAD_REPORT": source_run["protocol_load_report"]},
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        observation_source = WORK / "primary-chat.md"
        observation_source.write_text(
            "# Primary chat\n\nSynthetic collector content.\n",
            encoding="utf-8",
        )

        config = {
            "collection_version": "MADP-FIELD-TRIAL-COLLECTION-v1",
            "protocol_version": "MADP-v0.3.0-alpha.3",
            "participant": {
                "participant_id": "COLLECTOR-MODEL",
                "client": "CI",
                "displayed_model_label": "synthetic-collector",
                "reasoning_mode": "deterministic",
                "tool_notes": "",
            },
            "run": {
                "run_id": "COLLECTOR-RUN-01",
                "run_index": 1,
                "tested_commit": source_run["tested_commit"],
                "protocol_load_report_file": str(report_path),
                "start_profile_path": "bootstrap/alpha3/quick-start.md",
            },
            "observations": [
                {
                    "observation_id": "OBS-PRIMARY",
                    "kind": "PRIMARY_CHAT",
                    "source_file": str(observation_source),
                    "destination_name": "primary-chat.md",
                }
            ],
            "scenario_results": scenario_rows("OBS-PRIMARY"),
        }
        config_path = WORK / "collection-config.yaml"
        config_path.write_text(
            yaml.safe_dump(config, sort_keys=False),
            encoding="utf-8",
        )
        package_path = WORK / "package.yaml"
        prepared = run(
            "prepare",
            "--config",
            str(config_path),
            "--output",
            str(package_path),
        )
        assert prepared.returncode == 0, prepared.stderr or prepared.stdout

        checked = run("check", "--package", str(package_path), "--require-ready")
        assert checked.returncode == 0, checked.stderr or checked.stdout
        package = yaml.safe_load(package_path.read_text(encoding="utf-8"))
        assert package["status"] == "READY"
        assert package["run_evidence"]["run_id"] == "COLLECTOR-RUN-01"
        assert len(package["scenario_results"]) == 8

        merged_path = WORK / "merged-results.yaml"
        merged = run(
            "merge",
            "--base-results",
            str(BASE_RESULTS),
            "--package",
            str(package_path),
            "--output",
            str(merged_path),
        )
        assert merged.returncode == 0, merged.stderr or merged.stdout
        merged_document = yaml.safe_load(merged_path.read_text(encoding="utf-8"))
        manual = merged_document["manual_trials"]
        assert manual["status"] == "IN_PROGRESS"
        assert len(manual["run_evidence"]) == 1
        assert manual["metrics"]["trial_count"] == 8
        assert manual["metrics"]["task_completion_rate"] == 1.0

        duplicate_path = WORK / "duplicate-results.yaml"
        duplicate = run(
            "merge",
            "--base-results",
            str(BASE_RESULTS),
            "--package",
            str(package_path),
            "--package",
            str(package_path),
            "--output",
            str(duplicate_path),
        )
        assert duplicate.returncode != 0
        assert "duplicate run_id" in duplicate.stderr

        observation_path = (
            ROOT / package["run_evidence"]["observations"][0]["path"]
        )
        original_observation = observation_path.read_bytes()
        observation_path.write_text("tampered\n", encoding="utf-8")
        tampered = run(
            "check",
            "--package",
            str(package_path),
            "--require-ready",
        )
        assert tampered.returncode != 0
        assert "observation hash mismatch" in tampered.stderr
        observation_path.write_bytes(original_observation)

        draft_config = copy.deepcopy(config)
        draft_config["run"]["run_id"] = "COLLECTOR-RUN-DRAFT"
        draft_config["scenario_results"] = []
        draft_path = WORK / "draft-config.yaml"
        draft_path.write_text(
            yaml.safe_dump(draft_config, sort_keys=False),
            encoding="utf-8",
        )
        draft_package = WORK / "draft-package.yaml"
        draft = run(
            "prepare",
            "--config",
            str(draft_path),
            "--output",
            str(draft_package),
        )
        assert draft.returncode == 0, draft.stderr or draft.stdout
        draft_check = run(
            "check",
            "--package",
            str(draft_package),
            "--require-ready",
        )
        assert draft_check.returncode != 0
        assert "not READY" in draft_check.stderr

        print("MADP-v0.3.0-alpha.3 field-trial collection tooling: PASS")
        return 0
    finally:
        shutil.rmtree(WORK, ignore_errors=True)
        if raw_existed:
            RAW.write_bytes(raw_original)
        elif RAW.exists():
            RAW.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
