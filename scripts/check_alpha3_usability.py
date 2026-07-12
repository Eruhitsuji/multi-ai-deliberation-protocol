#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import hashlib
import re
import statistics
import subprocess
import sys
import yaml

from jsonschema import Draft202012Validator

from generate_validation_receipt_v030_alpha3 import (
    canonical_json_bytes,
    sha256_bytes,
    validate_value,
)

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.3"
REQUIRED = {
    "USAB-QUICK-001",
    "USAB-COMMAND-COMPAT-001",
    "USAB-RELAY-001",
    "USAB-LIMITED-001",
    "USAB-RECOVERY-001",
    "USAB-TEAM-001",
    "USAB-MINUTES-001",
    "USAB-HELP-001",
}
LOAD_REPORT_VERSION = "MADP-PROTOCOL-LOAD-REPORT-v2"
OFFICIAL_REPOSITORY = "Eruhitsuji/multi-ai-deliberation-protocol"
ACCESS_METHODS = {"RAW_URL", "GITHUB_CONNECTOR", "PROVIDED_TEXT", "COMPLETE_BUNDLE", "OTHER"}
REPORT_SCHEMA_REL = "schemas/v0.3.0-alpha.3/protocol-load-report.schema.yaml"
RECEIPT_SCHEMA_REL = "schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml"
REQUIRED_VALIDATION_PAIRS = {
    (
        "registries/v0.3.0-alpha.2/commands.yaml",
        "schemas/v0.3.0-alpha.2/command-registry.schema.yaml",
    ),
    (
        "registries/v0.3.0-alpha.3/commands.yaml",
        "schemas/v0.3.0-alpha.3/command-registry.schema.yaml",
    ),
}


def valid_commit(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-fA-F]{40}", value) is not None


def valid_sha256(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def file_sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_digest(paths):
    return hashlib.sha256(("\n".join(paths) + "\n").encode("utf-8")).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def loader_config():
    text = (ROOT / "bootstrap/alpha3/load-protocol-from-github.md").read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise ValueError("loader frontmatter missing")
    return yaml.safe_load(match.group(1))


def sources_for(profile, config):
    rows = []
    for set_name in config["load_profiles"][profile]["required_sets"]:
        rows.extend(config["source_sets"][set_name])
    return rows


def current_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:
        return None


def equal_number(actual, expected, tol=1e-12):
    return isinstance(actual, (int, float)) and abs(float(actual) - float(expected)) <= tol


def inside_root(relative: str) -> Path | None:
    if not isinstance(relative, str) or not relative or relative.startswith(("http://", "https://", "artifact://", "trial://", "repo://")):
        return None
    candidate = (ROOT / relative).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate


def receipt_map(documents, problems):
    mapping = {}
    receipt_schema = load_yaml(ROOT / RECEIPT_SCHEMA_REL)
    validator = Draft202012Validator(receipt_schema)
    for index, document in enumerate(documents, 1):
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))
        if errors:
            problems.append(f"validation receipt {index} schema failure: {errors[0].message}")
            continue
        row = document["VALIDATION_RECEIPT"]
        receipt_id = row["receipt_id"]
        if receipt_id in mapping:
            problems.append(f"duplicate validation receipt: {receipt_id}")
        else:
            mapping[receipt_id] = row
    return mapping


def verify_receipt(
    *,
    receipt,
    artifact_value,
    artifact_bytes,
    artifact_type,
    artifact_id,
    artifact_locator,
    schema_path,
    artifact_revision=None,
    artifact_version=None,
):
    problems = []
    artifact_ref = receipt.get("artifact_ref", {})
    schema_ref = receipt.get("schema_ref", {})
    if receipt.get("result") != "PASS" or receipt.get("executed") is not True:
        problems.append("receipt is not an executed PASS")
    if artifact_ref.get("artifact_type") != artifact_type:
        problems.append("artifact type mismatch")
    if artifact_ref.get("artifact_id") != artifact_id:
        problems.append("artifact ID mismatch")
    if artifact_ref.get("artifact_locator") != artifact_locator:
        problems.append("artifact locator mismatch")
    if artifact_revision is not None:
        if artifact_ref.get("artifact_revision") != artifact_revision or "artifact_version" in artifact_ref:
            problems.append("artifact revision mismatch")
    if artifact_version is not None:
        if artifact_ref.get("artifact_version") != artifact_version or "artifact_revision" in artifact_ref:
            problems.append("artifact version mismatch")

    canonicalization = artifact_ref.get("canonicalization")
    if canonicalization == "RAW_BYTES":
        expected_artifact_hash = sha256_bytes(artifact_bytes)
    elif canonicalization == "MADP_CANONICAL_JSON_V1":
        expected_artifact_hash = sha256_bytes(canonical_json_bytes(artifact_value))
    else:
        expected_artifact_hash = None
        problems.append("unsupported receipt canonicalization")
    if expected_artifact_hash and artifact_ref.get("artifact_sha256") != expected_artifact_hash:
        problems.append("artifact hash mismatch")

    schema_file = ROOT / schema_path
    if not schema_file.is_file():
        problems.append("schema file missing")
        return problems
    schema_bytes = schema_file.read_bytes()
    schema_value = yaml.safe_load(schema_bytes)
    if schema_ref.get("path") != schema_path:
        problems.append("schema path mismatch")
    if schema_ref.get("sha256") != sha256_bytes(schema_bytes):
        problems.append("schema hash mismatch")
    errors = validate_value(artifact_value, schema_value)
    if errors:
        problems.append("artifact does not validate against schema")
    if receipt.get("errors") != []:
        problems.append("PASS receipt contains errors")
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    problems = []

    scenarios = load_yaml(ROOT / "tests/v0.3.0-alpha.3/usability-scenarios.yaml")
    results = load_yaml(ROOT / "docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml")
    items = scenarios.get("scenarios", [])
    ids = {item.get("id") for item in items}
    if ids != REQUIRED:
        problems.append(f"usability scenario IDs mismatch: {sorted(ids ^ REQUIRED)}")
    for item in items:
        if not item.get("required_features") or not item.get("success_condition"):
            problems.append(f"incomplete scenario: {item.get('id')}")

    if results.get("results_version") != 5:
        problems.append("usability results_version must be 5")
    automated = results.get("automated_walkthrough", {})
    if automated.get("status") != "PASS" or automated.get("scenario_count") != len(REQUIRED):
        problems.append("automated walkthrough incomplete")
    if any(value != "PASS" for value in automated.get("checks", {}).values()):
        problems.append("automated checks not all PASS")

    manual = results.get("manual_trials", {})
    if manual.get("protocol_load_report_required") is not True or manual.get("required_load_report_version") != LOAD_REPORT_VERSION:
        problems.append("manual trial protocol load requirement missing")
    if manual.get("required_load_profile") != "FIELD_TRIAL" or manual.get("required_provenance") != "HASH_VERIFIED":
        problems.append("manual trial assurance requirements missing")
    if manual.get("required_receipt_schema") != RECEIPT_SCHEMA_REL:
        problems.append("manual trial receipt requirement missing")

    if args.release:
        config = loader_config()
        expected_sources = sources_for("FIELD_TRIAL", config)
        expected_digest = inventory_digest(expected_sources)
        if config.get("source_inventory_digests", {}).get("FIELD_TRIAL") != expected_digest:
            problems.append("FIELD_TRIAL inventory digest mismatch")
        head = current_commit()
        if not valid_commit(head):
            problems.append("unable to resolve current repository commit")

        receipts = receipt_map(manual.get("validation_receipts", []), problems)
        used_receipts = set()
        rows = manual.get("scenario_results", [])
        if manual.get("status") != "PASS":
            problems.append("manual trials not PASS")
        coverage = {row.get("scenario_id") for row in rows}
        if not REQUIRED.issubset(coverage):
            problems.append(f"release trial results missing scenarios: {sorted(REQUIRED - coverage)}")
        if not rows:
            problems.append("release trial results missing")

        report_schema = load_yaml(ROOT / REPORT_SCHEMA_REL)
        report_validator = Draft202012Validator(report_schema)
        trial_ids = set()
        composite = set()
        task_values = []
        next_values = []
        recovery_values = []
        eligible_total = unnecessary_total = authority_total = critical_pause_total = 0

        for row in rows:
            trial_id = row.get("trial_id")
            participant = row.get("participant_id")
            run_index = row.get("run_index")
            scenario_id = row.get("scenario_id")
            label = trial_id or scenario_id or "UNKNOWN"
            if not isinstance(trial_id, str) or not trial_id.strip():
                problems.append(f"missing trial_id: {label}")
            elif trial_id in trial_ids:
                problems.append(f"duplicate trial_id: {trial_id}")
            else:
                trial_ids.add(trial_id)
            key = (participant, run_index, scenario_id)
            if not participant or not isinstance(run_index, int) or run_index < 1 or scenario_id not in REQUIRED:
                problems.append(f"invalid trial identity: {label}")
            elif key in composite:
                problems.append(f"duplicate participant/run/scenario: {label}")
            else:
                composite.add(key)

            tested = row.get("tested_commit")
            if not valid_commit(tested):
                problems.append(f"invalid tested commit: {label}")
            elif head and tested.lower() != head.lower():
                problems.append(f"trial commit is not current checked-out commit: {label}")

            report = row.get("protocol_load_report", {})
            report_document = {"PROTOCOL_LOAD_REPORT": report}
            report_errors = sorted(report_validator.iter_errors(report_document), key=lambda error: list(error.absolute_path))
            if report_errors:
                problems.append(f"protocol load report schema failure ({label}): {report_errors[0].message}")
            if report.get("report_version") != LOAD_REPORT_VERSION or report.get("protocol_version") != VERSION:
                problems.append(f"invalid protocol load report version: {label}")
            if not report.get("report_id") or not isinstance(report.get("revision"), int) or report.get("revision", 0) < 1:
                problems.append(f"invalid report identity or revision: {label}")
            if report.get("active") is not True:
                problems.append(f"load report is not active: {label}")
            if report.get("load_profile") != "FIELD_TRIAL":
                problems.append(f"wrong load profile: {label}")
            if report.get("repository") != OFFICIAL_REPOSITORY:
                problems.append(f"wrong repository: {label}")
            if report.get("repository_commit") != tested:
                problems.append(f"protocol load report commit mismatch: {label}")
            if report.get("inventory_digest_algorithm") != "sha256-newline-paths-v1" or report.get("source_inventory_digest") != expected_digest:
                problems.append(f"protocol inventory digest mismatch: {label}")
            if report.get("status") != "COMPLETE" or report.get("all_required_files_read") is not True or report.get("inferred_unread_content") is not False:
                problems.append(f"incomplete protocol load gate: {label}")
            if report.get("schema_validation_capability") != "EXECUTED" or report.get("schema_validation_executed") is not True:
                problems.append(f"schema validation not executed: {label}")
            if report.get("provenance_level") != "HASH_VERIFIED":
                problems.append(f"load provenance not hash verified: {label}")

            file_rows = report.get("files", [])
            file_paths = [item.get("path") for item in file_rows if isinstance(item, dict)]
            if file_paths != expected_sources:
                problems.append(f"protocol file inventory/order mismatch: {label}")
            if len(file_paths) != len(set(file_paths)):
                problems.append(f"duplicate protocol file record: {label}")
            for item in file_rows:
                if not isinstance(item, dict):
                    problems.append(f"invalid file record: {label}")
                    continue
                path = item.get("path")
                if path not in expected_sources:
                    continue
                if item.get("status") != "READ":
                    problems.append(f"file not READ ({path}): {label}")
                if item.get("access_method") not in ACCESS_METHODS:
                    problems.append(f"invalid access method ({path}): {label}")
                if not item.get("source_ref"):
                    problems.append(f"missing source reference ({path}): {label}")
                observed = item.get("content_sha256")
                if not valid_sha256(observed):
                    problems.append(f"invalid content hash ({path}): {label}")
                elif (ROOT / path).is_file() and observed != file_sha(ROOT / path):
                    problems.append(f"content hash mismatch ({path}): {label}")

            receipt_refs = report.get("validation_receipt_refs", [])
            if len(receipt_refs) != len(set(receipt_refs)):
                problems.append(f"duplicate receipt reference: {label}")
            for receipt_id in receipt_refs:
                if receipt_id not in receipts:
                    problems.append(f"unresolved receipt reference ({receipt_id}): {label}")

            report_receipt_id = row.get("protocol_load_report_receipt_id")
            if report_receipt_id not in receipt_refs:
                problems.append(f"report receipt is not referenced by load report: {label}")
            report_receipt = receipts.get(report_receipt_id)
            if report_receipt:
                used_receipts.add(report_receipt_id)
                for issue in verify_receipt(
                    receipt=report_receipt,
                    artifact_value=report_document,
                    artifact_bytes=yaml.safe_dump(report_document, sort_keys=False, allow_unicode=True).encode("utf-8"),
                    artifact_type="PROTOCOL_LOAD_REPORT",
                    artifact_id=report.get("report_id"),
                    artifact_locator=f"trial://{trial_id}/protocol-load-report",
                    artifact_revision=report.get("revision"),
                    schema_path=REPORT_SCHEMA_REL,
                ):
                    problems.append(f"load report receipt {issue}: {label}")

            records = report.get("schema_validation_records", [])
            record_pairs = set()
            record_schemas = []
            executed_schemas = []
            for record in records:
                if not isinstance(record, dict):
                    problems.append(f"invalid schema validation record: {label}")
                    continue
                target_ref = record.get("target_ref")
                schema_path = record.get("schema_path")
                receipt_id = record.get("receipt_ref")
                if not isinstance(target_ref, str) or not target_ref.startswith("repo://"):
                    problems.append(f"validation target is not repository-bound: {label}")
                    continue
                target_path = target_ref[len("repo://"):]
                pair = (target_path, schema_path)
                if pair in record_pairs:
                    problems.append(f"duplicate schema validation pair {pair}: {label}")
                record_pairs.add(pair)
                record_schemas.append(schema_path)
                if record.get("result") == "PASS":
                    executed_schemas.append(schema_path)
                if target_path not in expected_sources or schema_path not in expected_sources:
                    problems.append(f"validation pair outside FIELD_TRIAL inventory {pair}: {label}")
                    continue
                target_file = ROOT / target_path
                schema_file = ROOT / schema_path
                if not target_file.is_file() or not schema_file.is_file():
                    problems.append(f"validation target/schema missing {pair}: {label}")
                    continue
                if record.get("target_sha256") != file_sha(target_file):
                    problems.append(f"validation target hash mismatch {target_path}: {label}")
                if record.get("schema_sha256") != file_sha(schema_file):
                    problems.append(f"validation schema hash mismatch {schema_path}: {label}")
                if receipt_id not in receipt_refs:
                    problems.append(f"validation record receipt not referenced ({receipt_id}): {label}")
                receipt = receipts.get(receipt_id)
                if receipt:
                    used_receipts.add(receipt_id)
                    artifact_value = load_yaml(target_file)
                    artifact_version = record.get("artifact_version")
                    if isinstance(artifact_value, dict) and isinstance(artifact_value.get("registry_version"), str):
                        if artifact_version != artifact_value["registry_version"]:
                            problems.append(f"validation record artifact version mismatch {target_path}: {label}")
                    for issue in verify_receipt(
                        receipt=receipt,
                        artifact_value=artifact_value,
                        artifact_bytes=target_file.read_bytes(),
                        artifact_type=record.get("artifact_type"),
                        artifact_id=record.get("artifact_id"),
                        artifact_locator=target_ref,
                        artifact_version=artifact_version,
                        schema_path=schema_path,
                    ):
                        problems.append(f"schema validation receipt {issue} ({pair}): {label}")

            if set(record_schemas) != set(report.get("schemas_applicable", [])):
                problems.append(f"schemas_applicable does not match validation records: {label}")
            if set(executed_schemas) != set(report.get("schemas_executed", [])):
                problems.append(f"schemas_executed does not match PASS records: {label}")
            if report.get("unvalidated_structured_sources") != []:
                problems.append(f"unvalidated structured source remains: {label}")
            if not REQUIRED_VALIDATION_PAIRS.issubset(record_pairs):
                problems.append(f"required registry validation records missing: {label}")

            authorized = {
                item.get("path"): item
                for item in report.get("authorized_start_profiles", [])
                if isinstance(item, dict)
            }
            binding = row.get("start_profile_binding", {})
            profile_path = binding.get("path")
            if profile_path not in {"bootstrap/alpha3/quick-start.md", "bootstrap/alpha3/verified-start.md"}:
                problems.append(f"invalid start profile path: {label}")
            auth = authorized.get(profile_path, {})
            profile_file = ROOT / str(profile_path)
            profile_hash = file_sha(profile_file) if profile_file.is_file() else None
            if binding.get("repository") != OFFICIAL_REPOSITORY or binding.get("repository_commit") != tested:
                problems.append(f"start profile repository/commit mismatch: {label}")
            if binding.get("source_inventory_digest") != expected_digest or not binding.get("source_ref"):
                problems.append(f"incomplete start profile binding: {label}")
            if binding.get("content_sha256") != profile_hash:
                problems.append(f"start profile binding hash mismatch: {label}")
            if auth.get("repository") != OFFICIAL_REPOSITORY or auth.get("repository_commit") != tested or not auth.get("source_ref"):
                problems.append(f"load report did not authorize selected profile: {label}")
            if auth.get("content_sha256") != profile_hash:
                problems.append(f"authorized profile hash mismatch: {label}")

            raw_ref = row.get("raw_observation_ref")
            raw_path = inside_root(raw_ref)
            if raw_path is None or not raw_path.is_file():
                problems.append(f"raw observation file missing or outside repository: {label}")
            elif row.get("raw_observation_sha256") != file_sha(raw_path):
                problems.append(f"raw observation hash mismatch: {label}")

            required_scalars = {
                "task_completed": bool,
                "next_action_understood": bool,
                "recovery_attempts": int,
                "eligible_workflow_transitions": int,
                "unnecessary_user_pauses": int,
                "critical_authority_errors": int,
                "critical_unnecessary_pauses": int,
            }
            bad = False
            for field, kind in required_scalars.items():
                value = row.get(field)
                if kind is bool:
                    if not isinstance(value, bool):
                        problems.append(f"invalid {field}: {label}")
                        bad = True
                elif not isinstance(value, int) or value < 0:
                    problems.append(f"invalid {field}: {label}")
                    bad = True
            if not bad:
                task_values.append(1 if row["task_completed"] else 0)
                next_values.append(1 if row["next_action_understood"] else 0)
                recovery_values.append(row["recovery_attempts"])
                eligible_total += row["eligible_workflow_transitions"]
                unnecessary_total += row["unnecessary_user_pauses"]
                authority_total += row["critical_authority_errors"]
                critical_pause_total += row["critical_unnecessary_pauses"]

        if set(receipts) != used_receipts:
            problems.append(f"unused or unbound validation receipts: {sorted(set(receipts) - used_receipts)}")

        if rows and len(task_values) == len(rows):
            calculated = {
                "trial_count": len(rows),
                "task_completion_rate": sum(task_values) / len(rows),
                "critical_authority_errors": authority_total,
                "eligible_workflow_transitions": eligible_total,
                "unnecessary_user_pauses": unnecessary_total,
                "unnecessary_pause_rate": unnecessary_total / eligible_total if eligible_total else None,
                "critical_unnecessary_pauses": critical_pause_total,
                "next_action_understood_rate": sum(next_values) / len(rows),
                "median_recovery_attempts": statistics.median(recovery_values),
            }
            stored = manual.get("metrics", {})
            for key, value in calculated.items():
                if value is None:
                    if stored.get(key) is not None:
                        problems.append(f"metric mismatch: {key}")
                elif not equal_number(stored.get(key), value):
                    problems.append(f"metric mismatch: {key}")
            if calculated["task_completion_rate"] < 0.90:
                problems.append("task completion rate below 90%")
            if calculated["critical_authority_errors"] != 0:
                problems.append("critical authority errors must be zero")
            if calculated["next_action_understood_rate"] < 0.90:
                problems.append("next-action understood rate below 90%")
            if calculated["median_recovery_attempts"] > 1:
                problems.append("median recovery attempts exceeds one")
            if calculated["eligible_workflow_transitions"] <= 0:
                problems.append("pause denominator missing")
            elif calculated["unnecessary_pause_rate"] > 0.05:
                problems.append("unnecessary pause rate exceeds 5%")
            if calculated["critical_unnecessary_pauses"] != 0:
                problems.append("critical unnecessary pauses must be zero")
            if len(manual.get("pause_classification_records", [])) < unnecessary_total:
                problems.append("pause classification records incomplete")
        if not manual.get("sign_off", {}).get("approved_by"):
            problems.append("manual sign-off missing")

    if problems:
        for item in problems:
            print("FAIL:", item, file=sys.stderr)
        return 1
    print("alpha.3 usability checks: PASS" + (" (release, recomputed receipt-bound multi-run metrics)" if args.release else " (automated)"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
