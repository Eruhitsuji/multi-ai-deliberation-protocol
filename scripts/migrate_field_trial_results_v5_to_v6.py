#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import copy
import re
import sys
import yaml

from jsonschema import Draft202012Validator

VERSION = "MADP-v0.3.0-alpha.3"
TARGET_RESULTS_VERSION = 6
TARGET_EVIDENCE_VERSION = "MADP-FIELD-TRIAL-EVIDENCE-v2"


def safe_id(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._:-]+", "-", value.strip())
    value = value.strip("-")
    return value or "RUN"


def run_id_for(row: dict[str, Any]) -> str:
    if isinstance(row.get("run_id"), str) and row["run_id"].strip():
        return row["run_id"].strip()
    participant = safe_id(str(row.get("participant_id") or "PARTICIPANT"))
    index = row.get("run_index")
    if not isinstance(index, int) or index < 1:
        raise ValueError(f"invalid run_index for {participant}")
    return f"{participant}-R{index:02d}"


def canonical_run_payload(row: dict[str, Any]) -> dict[str, Any]:
    required = [
        "participant_id",
        "run_index",
        "tested_commit",
        "protocol_load_report",
        "protocol_load_report_receipt_id",
        "start_profile_binding",
    ]
    missing = [name for name in required if name not in row]
    if missing:
        raise ValueError(f"legacy row missing run fields: {missing}")
    return {name: copy.deepcopy(row[name]) for name in required}


def observation_kind(path: str) -> str:
    lower = path.lower()
    if "relay-packet" in lower:
        return "RELAY_PACKET"
    if "relay" in lower and ("raw" in lower or "response" in lower):
        return "RELAY_RAW_RESPONSE"
    if "session-export" in lower or "export" in lower:
        return "SESSION_EXPORT"
    if "import" in lower:
        return "IMPORT_CHAT"
    return "PRIMARY_CHAT"


def migrate_v5_to_v6(document: dict[str, Any]) -> dict[str, Any]:
    if document.get("protocol_version") != VERSION:
        raise ValueError("protocol version mismatch")
    if document.get("results_version") == TARGET_RESULTS_VERSION:
        return copy.deepcopy(document)
    if document.get("results_version") != 5:
        raise ValueError("only results_version 5 can be migrated")

    output = copy.deepcopy(document)
    output["results_version"] = TARGET_RESULTS_VERSION
    manual = output.setdefault("manual_trials", {})
    legacy_rows = manual.get("scenario_results", [])
    runs: dict[str, dict[str, Any]] = {}
    observation_keys: dict[str, dict[tuple[str, str], str]] = {}
    new_rows = []

    for row in legacy_rows:
        if not isinstance(row, dict):
            raise ValueError("scenario_results entries must be objects")
        run_id = run_id_for(row)
        payload = canonical_run_payload(row)
        if run_id not in runs:
            runs[run_id] = {
                "run_id": run_id,
                **payload,
                "observations": [],
            }
            observation_keys[run_id] = {}
        else:
            existing = {key: runs[run_id][key] for key in payload}
            if existing != payload:
                raise ValueError(f"conflicting run-level evidence for {run_id}")

        raw_ref = row.get("raw_observation_ref")
        raw_sha = row.get("raw_observation_sha256")
        if not isinstance(raw_ref, str) or not raw_ref:
            raise ValueError(f"missing raw_observation_ref for {row.get('trial_id')}")
        if not isinstance(raw_sha, str) or not raw_sha:
            raise ValueError(f"missing raw_observation_sha256 for {row.get('trial_id')}")
        key = (raw_ref, raw_sha)
        observation_id = observation_keys[run_id].get(key)
        if observation_id is None:
            observation_id = f"OBS-{safe_id(run_id)}-{len(observation_keys[run_id]) + 1:02d}"
            observation_keys[run_id][key] = observation_id
            runs[run_id]["observations"].append(
                {
                    "observation_id": observation_id,
                    "kind": observation_kind(raw_ref),
                    "path": raw_ref,
                    "sha256": raw_sha,
                }
            )

        scenario = {
            key: copy.deepcopy(value)
            for key, value in row.items()
            if key
            not in {
                "participant_id",
                "run_index",
                "tested_commit",
                "protocol_load_report",
                "protocol_load_report_receipt_id",
                "start_profile_binding",
                "raw_observation_ref",
                "raw_observation_sha256",
                "run_id",
            }
        }
        scenario["run_id"] = run_id
        scenario["observation_refs"] = [observation_id]
        ordered = {
            "trial_id": scenario.pop("trial_id"),
            "run_id": scenario.pop("run_id"),
            "scenario_id": scenario.pop("scenario_id"),
            "observation_refs": scenario.pop("observation_refs"),
            **scenario,
        }
        new_rows.append(ordered)

    manual["field_trial_evidence_version"] = TARGET_EVIDENCE_VERSION
    manual["run_evidence"] = list(runs.values())
    manual["scenario_results"] = new_rows
    return output


def validate_output(document: dict[str, Any], schema_path: Path) -> None:
    schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda error: list(error.absolute_path))
    if errors:
        location = "/" + "/".join(str(item) for item in errors[0].absolute_path)
        raise ValueError(f"migrated evidence schema failure at {location}: {errors[0].message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--schema",
        default="schemas/v0.3.0-alpha.3/field-trial-evidence.schema.yaml",
    )
    args = parser.parse_args()
    source = Path(args.input)
    document = yaml.safe_load(source.read_text(encoding="utf-8"))
    migrated = migrate_v5_to_v6(document)
    validate_output(migrated, Path(args.schema))
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(yaml.safe_dump(migrated, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"field-trial evidence migrated: {source} -> {target} (results_version 6)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
