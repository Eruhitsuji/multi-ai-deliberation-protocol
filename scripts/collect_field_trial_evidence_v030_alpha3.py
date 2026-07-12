#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import copy
import re
import shutil
import statistics
import sys
import yaml

from jsonschema import Draft202012Validator

from check_alpha3_field_trial import (
    OFFICIAL_REPOSITORY,
    REPORT_SCHEMA_REL,
    RESULTS_SCHEMA_REL,
    ROOT,
    VERSION,
    current_commit,
    file_sha,
    inventory_digest,
    load_yaml,
    loader_config,
    receipt_map,
    sources_for,
    validate_run,
)
from generate_validation_receipt_v030_alpha3 import build_receipt

COLLECTION_VERSION = "MADP-FIELD-TRIAL-COLLECTION-v1"
PACKAGE_SCHEMA_REL = "schemas/v0.3.0-alpha.3/field-trial-collection.schema.yaml"
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
PROFILE_PATHS = {
    "bootstrap/alpha3/quick-start.md",
    "bootstrap/alpha3/verified-start.md",
}
ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
SHA40 = re.compile(r"^[0-9a-f]{40}$")
INTEGER_FIELDS = (
    "recovery_attempts",
    "eligible_workflow_transitions",
    "unnecessary_user_pauses",
    "critical_authority_errors",
    "critical_unnecessary_pauses",
)
BOOLEAN_FIELDS = ("task_completed", "next_action_understood")
TEXT_FIELDS = ("expected_behavior", "actual_behavior", "reviewer")


def validate_schema(document: Any, schema_rel: str, label: str) -> None:
    schema = load_yaml(ROOT / schema_rel)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        location = "/" + "/".join(str(item) for item in errors[0].absolute_path)
        raise ValueError(f"{label} schema failure at {location}: {errors[0].message}")


def require_id(value: Any, field: str) -> str:
    if not isinstance(value, str) or not ID_PATTERN.fullmatch(value):
        raise ValueError(f"invalid {field}: {value!r}")
    return value


def resolve_input(config_path: Path, value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"missing {field}")
    path = Path(value)
    if not path.is_absolute():
        path = (config_path.parent / path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"{field} does not exist: {path}")
    return path


def resolve_repo_path(relative: Any, field: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"invalid repository-relative {field}: {relative!r}")
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"{field} escapes repository: {relative}") from exc
    return candidate


def repo_relative(path: Path) -> str:
    try:
        relative = path.resolve().relative_to(ROOT.resolve())
    except ValueError as exc:
        raise ValueError(f"output must remain inside repository: {path}") from exc
    return str(relative).replace("\\", "/")


def unwrap_report(value: Any) -> dict[str, Any]:
    if isinstance(value, dict) and isinstance(value.get("PROTOCOL_LOAD_REPORT"), dict):
        return copy.deepcopy(value["PROTOCOL_LOAD_REPORT"])
    if isinstance(value, dict):
        return copy.deepcopy(value)
    raise ValueError("protocol load report must be a mapping")


def normalize_receipt_refs(
    report: dict[str, Any],
    run_id: str,
) -> tuple[str, list[str]]:
    report_receipt_id = require_id(f"VAL-{run_id}-REPORT", "report receipt ID")
    records = report.get("schema_validation_records", [])
    if not isinstance(records, list):
        raise ValueError("schema_validation_records must be an array")
    record_refs = []
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("schema validation record must be a mapping")
        record_refs.append(require_id(record.get("receipt_ref"), "receipt_ref"))
    desired = list(dict.fromkeys([*record_refs, report_receipt_id]))
    normalizations: list[str] = []
    if report.get("validation_receipt_refs") != desired:
        report["validation_receipt_refs"] = desired
        normalizations.append("REBUILT_VALIDATION_RECEIPT_REFERENCE_SET")
    return report_receipt_id, normalizations


def repository_receipts(report: dict[str, Any]) -> list[dict[str, Any]]:
    documents: list[dict[str, Any]] = []
    for record in report.get("schema_validation_records", []):
        receipt_id = require_id(record.get("receipt_ref"), "receipt_ref")
        target_ref = record.get("target_ref")
        if not isinstance(target_ref, str) or not target_ref.startswith("repo://"):
            raise ValueError(f"invalid validation target: {target_ref}")
        target_rel = target_ref[len("repo://") :]
        target_path = resolve_repo_path(target_rel, "validation target")
        schema_rel = record.get("schema_path")
        schema_path = resolve_repo_path(schema_rel, "validation schema")
        if not target_path.is_file() or not schema_path.is_file():
            raise FileNotFoundError(
                f"validation target or schema missing: {target_ref}, {schema_rel}"
            )
        document = build_receipt(
            artifact_value=load_yaml(target_path),
            artifact_bytes=target_path.read_bytes(),
            artifact_type=record.get("artifact_type"),
            artifact_id=record.get("artifact_id"),
            artifact_locator=target_ref,
            artifact_version=record.get("artifact_version"),
            canonicalization="RAW_BYTES",
            schema_value=load_yaml(schema_path),
            schema_bytes=schema_path.read_bytes(),
            schema_path=str(schema_rel),
            receipt_id=receipt_id,
            executor_type="DETERMINISTIC_RUNTIME",
            executor_name="madp-field-trial-collector",
            executor_version="2",
        )
        if document["VALIDATION_RECEIPT"]["result"] != "PASS":
            raise ValueError(f"repository validation receipt failed: {receipt_id}")
        documents.append(document)
    return documents


def report_receipt(
    report: dict[str, Any],
    run_id: str,
    receipt_id: str,
) -> dict[str, Any]:
    wrapper = {"PROTOCOL_LOAD_REPORT": report}
    schema_path = ROOT / REPORT_SCHEMA_REL
    document = build_receipt(
        artifact_value=wrapper,
        artifact_bytes=yaml.safe_dump(
            wrapper,
            sort_keys=False,
            allow_unicode=True,
        ).encode("utf-8"),
        artifact_type="PROTOCOL_LOAD_REPORT",
        artifact_id=report["report_id"],
        artifact_locator=f"trial://{run_id}/protocol-load-report",
        artifact_revision=report["revision"],
        canonicalization="MADP_CANONICAL_JSON_V1",
        schema_value=load_yaml(schema_path),
        schema_bytes=schema_path.read_bytes(),
        schema_path=REPORT_SCHEMA_REL,
        receipt_id=receipt_id,
        executor_type="DETERMINISTIC_RUNTIME",
        executor_name="madp-field-trial-collector",
        executor_version="2",
    )
    if document["VALIDATION_RECEIPT"]["result"] != "PASS":
        raise ValueError("normalized protocol load report failed schema validation")
    return document


def collect_observations(
    config_path: Path,
    rows: Any,
    output_directory: Path,
) -> list[dict[str, Any]]:
    if not isinstance(rows, list) or not rows:
        raise ValueError("observations must be a non-empty array")
    destination_root = output_directory / "observations"
    destination_root.mkdir(parents=True, exist_ok=True)
    output: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_destinations: set[Path] = set()
    allowed = {
        "PRIMARY_CHAT",
        "RELAY_PACKET",
        "RELAY_RAW_RESPONSE",
        "SESSION_EXPORT",
        "IMPORT_CHAT",
        "LOAD_REPORT",
        "OTHER",
    }
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("observation entry must be a mapping")
        observation_id = require_id(row.get("observation_id"), "observation_id")
        if observation_id in seen_ids:
            raise ValueError(f"duplicate observation_id: {observation_id}")
        seen_ids.add(observation_id)
        if row.get("kind") not in allowed:
            raise ValueError(f"invalid observation kind: {row.get('kind')}")
        source = resolve_input(
            config_path,
            row.get("source_file"),
            "observation source_file",
        )
        destination_name = row.get("destination_name") or (
            f"{observation_id}{source.suffix or '.txt'}"
        )
        if Path(destination_name).name != destination_name:
            raise ValueError(f"unsafe destination_name: {destination_name}")
        destination = (destination_root / destination_name).resolve()
        if destination in seen_destinations:
            raise ValueError(f"duplicate observation destination: {destination_name}")
        seen_destinations.add(destination)
        repo_relative(destination)
        if source.resolve() != destination:
            shutil.copyfile(source, destination)
        output.append(
            {
                "observation_id": observation_id,
                "kind": row["kind"],
                "path": repo_relative(destination),
                "sha256": file_sha(destination),
            }
        )
    return output


def scenario_ready(row: dict[str, Any], observation_ids: set[str]) -> bool:
    refs = row.get("observation_refs")
    if (
        not isinstance(refs, list)
        or not refs
        or len(refs) != len(set(refs))
        or any(ref not in observation_ids for ref in refs)
    ):
        return False
    for field in BOOLEAN_FIELDS:
        if not isinstance(row.get(field), bool):
            return False
    for field in INTEGER_FIELDS:
        value = row.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            return False
    for field in TEXT_FIELDS:
        value = row.get(field)
        if not isinstance(value, str) or not value:
            return False
    return isinstance(row.get("notes"), str)


def build_scenarios(
    config: dict[str, Any],
    run_id: str,
    observation_ids: set[str],
) -> tuple[list[dict[str, Any]], str]:
    supplied = config.get("scenario_results", [])
    if not isinstance(supplied, list):
        raise ValueError("scenario_results must be an array")
    by_id: dict[str, dict[str, Any]] = {}
    for row in supplied:
        if not isinstance(row, dict):
            raise ValueError("scenario result must be a mapping")
        scenario_id = row.get("scenario_id")
        if scenario_id not in SCENARIOS or scenario_id in by_id:
            raise ValueError(f"invalid or duplicate scenario_id: {scenario_id}")
        by_id[scenario_id] = row
    fields = [
        *BOOLEAN_FIELDS,
        *INTEGER_FIELDS,
        *TEXT_FIELDS,
        "notes",
    ]
    output: list[dict[str, Any]] = []
    for scenario_id in SCENARIOS:
        source = by_id.get(scenario_id, {})
        row = {
            "trial_id": source.get("trial_id") or f"{run_id}-{scenario_id}",
            "run_id": run_id,
            "scenario_id": scenario_id,
            "observation_refs": source.get("observation_refs", []),
        }
        for field in fields:
            row[field] = source.get(field)
        output.append(row)
    status = (
        "READY"
        if all(scenario_ready(row, observation_ids) for row in output)
        else "DRAFT"
    )
    return output, status


def semantic_validate_package(
    package: dict[str, Any],
    *,
    require_ready: bool = False,
) -> dict[str, Any]:
    validate_schema(package, PACKAGE_SCHEMA_REL, "collection package")
    status = package.get("status")
    if require_ready and status != "READY":
        raise ValueError("collection package is not READY")

    participant = package["participant"]
    participant_id = participant["participant_id"]
    run = package["run_evidence"]
    run_id = run["run_id"]
    if run["participant_id"] != participant_id:
        raise ValueError("package participant does not match run participant")

    head = current_commit()
    if not isinstance(head, str) or not SHA40.fullmatch(head):
        raise ValueError("unable to resolve current checked-out commit")
    expected_sources = sources_for("FIELD_TRIAL", loader_config())
    expected_digest = inventory_digest(expected_sources)
    problems: list[str] = []
    receipts = receipt_map(package["validation_receipts"], problems)
    used_receipts: set[str] = set()
    observations = validate_run(
        run=run,
        participants={participant_id},
        receipts=receipts,
        used_receipts=used_receipts,
        expected_sources=expected_sources,
        expected_digest=expected_digest,
        head=head,
        report_validator=Draft202012Validator(load_yaml(ROOT / REPORT_SCHEMA_REL)),
        problems=problems,
    )
    if set(receipts) != used_receipts:
        problems.append(
            f"unused validation receipts: {sorted(set(receipts) - used_receipts)}"
        )
    if problems:
        raise ValueError("; ".join(problems))

    rows = package["scenario_results"]
    scenario_ids: set[str] = set()
    trial_ids: set[str] = set()
    all_ready = True
    for row in rows:
        scenario_id = row["scenario_id"]
        if scenario_id in scenario_ids:
            raise ValueError(f"duplicate scenario_id: {scenario_id}")
        scenario_ids.add(scenario_id)
        trial_id = row["trial_id"]
        if trial_id in trial_ids:
            raise ValueError(f"duplicate trial_id: {trial_id}")
        trial_ids.add(trial_id)
        if row["run_id"] != run_id:
            raise ValueError(
                f"scenario run_id mismatch ({row['run_id']}): {scenario_id}"
            )
        refs = row.get("observation_refs", [])
        for observation_id in refs:
            if observation_id not in observations:
                raise ValueError(
                    f"unknown observation reference ({observation_id}): {scenario_id}"
                )
        all_ready = all_ready and scenario_ready(row, set(observations))
    if scenario_ids != set(SCENARIOS):
        raise ValueError(
            f"scenario coverage mismatch: {sorted(set(SCENARIOS) ^ scenario_ids)}"
        )
    inferred_status = "READY" if all_ready else "DRAFT"
    if status != inferred_status:
        raise ValueError(
            f"collection package status mismatch: {status} != {inferred_status}"
        )
    if require_ready and inferred_status != "READY":
        raise ValueError("collection package is not READY")
    return package


def prepare(config_path: Path, output_path: Path) -> dict[str, Any]:
    config = load_yaml(config_path)
    if (
        not isinstance(config, dict)
        or config.get("collection_version") != COLLECTION_VERSION
    ):
        raise ValueError(f"collection_version must be {COLLECTION_VERSION}")
    if config.get("protocol_version") != VERSION:
        raise ValueError("protocol_version mismatch")

    participant = config.get("participant")
    run_config = config.get("run")
    if not isinstance(participant, dict) or not isinstance(run_config, dict):
        raise ValueError("participant and run mappings are required")
    participant_id = require_id(participant.get("participant_id"), "participant_id")
    for field in ("client", "displayed_model_label", "reasoning_mode"):
        if not isinstance(participant.get(field), str) or not participant[field]:
            raise ValueError(f"participant {field} is required")

    run_id = require_id(run_config.get("run_id"), "run_id")
    run_index = run_config.get("run_index")
    if not isinstance(run_index, int) or isinstance(run_index, bool) or run_index < 1:
        raise ValueError("run_index must be >= 1")
    tested_commit = run_config.get("tested_commit")
    if not isinstance(tested_commit, str) or not SHA40.fullmatch(tested_commit):
        raise ValueError("tested_commit must be a lowercase 40-character commit")
    if tested_commit != current_commit():
        raise ValueError("tested_commit does not equal checked-out commit")

    report_path = resolve_input(
        config_path,
        run_config.get("protocol_load_report_file"),
        "protocol_load_report_file",
    )
    report = unwrap_report(load_yaml(report_path))
    report_receipt_id, normalizations = normalize_receipt_refs(report, run_id)

    profile_path = run_config.get("start_profile_path")
    if profile_path not in PROFILE_PATHS:
        raise ValueError(f"invalid start_profile_path: {profile_path}")
    expected_sources = sources_for("FIELD_TRIAL", loader_config())
    expected_digest = inventory_digest(expected_sources)
    authorized = {
        item.get("path"): item
        for item in report.get("authorized_start_profiles", [])
        if isinstance(item, dict)
    }
    auth = authorized.get(profile_path)
    profile_file = ROOT / profile_path
    if (
        not auth
        or not profile_file.is_file()
        or auth.get("content_sha256") != file_sha(profile_file)
    ):
        raise ValueError(
            "selected start profile is not authorized with the current hash"
        )
    binding = {
        "repository": OFFICIAL_REPOSITORY,
        "repository_commit": tested_commit,
        "path": profile_path,
        "source_ref": auth["source_ref"],
        "source_inventory_digest": expected_digest,
        "content_sha256": file_sha(profile_file),
    }

    output_path = output_path.resolve()
    repo_relative(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    observations = collect_observations(
        config_path,
        config.get("observations"),
        output_path.parent,
    )
    scenarios, status = build_scenarios(
        config,
        run_id,
        {item["observation_id"] for item in observations},
    )
    receipt_documents = repository_receipts(report)
    receipt_documents.append(report_receipt(report, run_id, report_receipt_id))
    run = {
        "run_id": run_id,
        "participant_id": participant_id,
        "run_index": run_index,
        "tested_commit": tested_commit,
        "protocol_load_report": report,
        "protocol_load_report_receipt_id": report_receipt_id,
        "start_profile_binding": binding,
        "observations": observations,
    }
    package = {
        "collection_package_version": COLLECTION_VERSION,
        "protocol_version": VERSION,
        "status": status,
        "participant": participant,
        "validation_receipts": receipt_documents,
        "run_evidence": run,
        "scenario_results": scenarios,
        "normalizations": normalizations,
    }
    semantic_validate_package(package)
    output_path.write_text(
        yaml.safe_dump(package, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return package


def validate_package(path: Path, require_ready: bool = False) -> dict[str, Any]:
    package = load_yaml(path)
    if not isinstance(package, dict):
        raise ValueError("collection package must be a mapping")
    return semantic_validate_package(package, require_ready=require_ready)


def metrics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(rows)
    eligible = sum(row["eligible_workflow_transitions"] for row in rows)
    unnecessary = sum(row["unnecessary_user_pauses"] for row in rows)
    return {
        "trial_count": count,
        "task_completion_rate": (
            sum(row["task_completed"] for row in rows) / count if count else None
        ),
        "critical_authority_errors": sum(
            row["critical_authority_errors"] for row in rows
        ),
        "eligible_workflow_transitions": eligible,
        "unnecessary_user_pauses": unnecessary,
        "unnecessary_pause_rate": (
            unnecessary / eligible if eligible else None
        ),
        "critical_unnecessary_pauses": sum(
            row["critical_unnecessary_pauses"] for row in rows
        ),
        "next_action_understood_rate": (
            sum(row["next_action_understood"] for row in rows) / count
            if count
            else None
        ),
        "median_recovery_attempts": (
            statistics.median(row["recovery_attempts"] for row in rows)
            if count
            else None
        ),
    }


def unique_index(
    rows: Any,
    key: str,
    label: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{label} must be an array")
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{label} entry must be a mapping")
        value = row.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"{label} entry missing {key}")
        if value in output:
            raise ValueError(f"duplicate {label} {key}: {value}")
        output[value] = row
    return output


def validate_results_for_collection(document: dict[str, Any]) -> None:
    validate_schema(document, RESULTS_SCHEMA_REL, "field-trial results")
    if document.get("results_version") != 6:
        raise ValueError("base results must use results_version 6")
    manual = document["manual_trials"]
    sign_off = manual.get("sign_off", {})
    if (
        manual.get("status") == "PASS"
        or sign_off.get("approved_by")
        or sign_off.get("approved_at") is not None
    ):
        raise ValueError("cannot merge into signed or PASS field-trial results")

    participants = unique_index(
        manual.get("participants", []),
        "participant_id",
        "participants",
    )
    receipt_documents = manual.get("validation_receipts", [])
    problems: list[str] = []
    receipts = receipt_map(receipt_documents, problems)
    if len(receipts) != len(receipt_documents):
        problems.append("duplicate or invalid validation receipts")
    runs = unique_index(manual.get("run_evidence", []), "run_id", "run evidence")
    trials = unique_index(
        manual.get("scenario_results", []),
        "trial_id",
        "scenario results",
    )

    head = current_commit()
    if not isinstance(head, str) or not SHA40.fullmatch(head):
        raise ValueError("unable to resolve current checked-out commit")
    expected_sources = sources_for("FIELD_TRIAL", loader_config())
    expected_digest = inventory_digest(expected_sources)
    used_receipts: set[str] = set()
    identities: set[tuple[str, int]] = set()
    observations_by_run: dict[str, dict[str, dict[str, Any]]] = {}
    for run_id, run in runs.items():
        identity = (run.get("participant_id"), run.get("run_index"))
        if identity in identities:
            problems.append(f"duplicate participant/run index: {identity}")
        identities.add(identity)
        observations_by_run[run_id] = validate_run(
            run=run,
            participants=set(participants),
            receipts=receipts,
            used_receipts=used_receipts,
            expected_sources=expected_sources,
            expected_digest=expected_digest,
            head=head,
            report_validator=Draft202012Validator(
                load_yaml(ROOT / REPORT_SCHEMA_REL)
            ),
            problems=problems,
        )

    run_scenarios: set[tuple[str, str]] = set()
    used_runs: set[str] = set()
    for trial_id, row in trials.items():
        run_id = row.get("run_id")
        if run_id not in runs:
            problems.append(f"unknown run_id ({run_id}): {trial_id}")
            continue
        used_runs.add(run_id)
        key = (run_id, row.get("scenario_id"))
        if key in run_scenarios:
            problems.append(f"duplicate run/scenario: {key}")
        run_scenarios.add(key)
        for observation_id in row.get("observation_refs", []):
            if observation_id not in observations_by_run.get(run_id, {}):
                problems.append(
                    f"unknown observation reference ({observation_id}): {trial_id}"
                )
    if set(runs) != used_runs:
        problems.append(
            f"run evidence without scenario result: {sorted(set(runs) - used_runs)}"
        )
    if set(receipts) != used_receipts:
        problems.append(
            f"unused validation receipts: {sorted(set(receipts) - used_receipts)}"
        )
    if problems:
        raise ValueError("; ".join(problems))


def merge(
    base_path: Path,
    package_paths: list[Path],
    output_path: Path,
) -> dict[str, Any]:
    document = load_yaml(base_path)
    if not isinstance(document, dict):
        raise ValueError("base results must be a mapping")
    validate_results_for_collection(document)
    manual = document["manual_trials"]

    participants = unique_index(
        manual.get("participants", []),
        "participant_id",
        "participants",
    )
    receipt_documents = manual.get("validation_receipts", [])
    receipts = {
        item["VALIDATION_RECEIPT"]["receipt_id"]: item
        for item in receipt_documents
    }
    runs = unique_index(manual.get("run_evidence", []), "run_id", "run evidence")
    scenarios = unique_index(
        manual.get("scenario_results", []),
        "trial_id",
        "scenario results",
    )
    identities = {
        (run["participant_id"], run["run_index"]) for run in runs.values()
    }
    run_scenarios = {
        (row["run_id"], row["scenario_id"]) for row in scenarios.values()
    }

    for package_path in package_paths:
        package = validate_package(package_path, require_ready=True)
        participant = package["participant"]
        participant_id = participant["participant_id"]
        if (
            participant_id in participants
            and participants[participant_id] != participant
        ):
            raise ValueError(f"conflicting participant: {participant_id}")
        participants[participant_id] = participant

        for receipt in package["validation_receipts"]:
            receipt_id = receipt["VALIDATION_RECEIPT"]["receipt_id"]
            if receipt_id in receipts and receipts[receipt_id] != receipt:
                raise ValueError(f"conflicting receipt: {receipt_id}")
            receipts[receipt_id] = receipt

        run = package["run_evidence"]
        run_id = run["run_id"]
        identity = (run["participant_id"], run["run_index"])
        if run_id in runs:
            raise ValueError(f"duplicate run_id: {run_id}")
        if identity in identities:
            raise ValueError(f"duplicate participant/run index: {identity}")
        identities.add(identity)
        runs[run_id] = run

        for row in package["scenario_results"]:
            trial_id = row["trial_id"]
            key = (row["run_id"], row["scenario_id"])
            if trial_id in scenarios:
                raise ValueError(f"duplicate trial_id: {trial_id}")
            if key in run_scenarios:
                raise ValueError(f"duplicate run/scenario: {key}")
            run_scenarios.add(key)
            scenarios[trial_id] = row

    ordered_participants = [
        participants[key] for key in sorted(participants)
    ]
    ordered_receipts = [
        receipts[key] for key in sorted(receipts)
    ]
    ordered_runs = [runs[key] for key in sorted(runs)]
    scenario_order = {scenario_id: index for index, scenario_id in enumerate(SCENARIOS)}
    ordered_rows = sorted(
        scenarios.values(),
        key=lambda row: (
            row["run_id"],
            scenario_order.get(row["scenario_id"], len(SCENARIOS)),
            row["trial_id"],
        ),
    )
    manual.update(
        {
            "status": "IN_PROGRESS",
            "participants": ordered_participants,
            "validation_receipts": ordered_receipts,
            "run_evidence": ordered_runs,
            "scenario_results": ordered_rows,
            "metrics": metrics(ordered_rows),
            "sign_off": {"approved_by": [], "approved_at": None},
        }
    )
    validate_results_for_collection(document)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        yaml.safe_dump(document, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return document


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)

    prepare_parser = commands.add_parser("prepare")
    prepare_parser.add_argument("--config", required=True)
    prepare_parser.add_argument("--output", required=True)

    check_parser = commands.add_parser("check")
    check_parser.add_argument("--package", required=True)
    check_parser.add_argument("--require-ready", action="store_true")

    merge_parser = commands.add_parser("merge")
    merge_parser.add_argument("--base-results", required=True)
    merge_parser.add_argument("--package", action="append", required=True)
    merge_parser.add_argument("--output", required=True)

    args = parser.parse_args()
    try:
        if args.command == "prepare":
            package = prepare(Path(args.config), Path(args.output))
            print(
                f"field-trial collection package written: "
                f"{args.output} ({package['status']})"
            )
        elif args.command == "check":
            package = validate_package(Path(args.package), args.require_ready)
            print(f"field-trial collection package: PASS ({package['status']})")
        else:
            document = merge(
                Path(args.base_results),
                [Path(item) for item in args.package],
                Path(args.output),
            )
            print(
                f"field-trial results merged: "
                f"{len(document['manual_trials']['run_evidence'])} runs, "
                f"{len(document['manual_trials']['scenario_results'])} scenarios"
            )
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
