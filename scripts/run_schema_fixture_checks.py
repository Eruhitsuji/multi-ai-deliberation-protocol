#!/usr/bin/env python3
"""Run schema-layer migration fixture checks for MADP v0.3.0-alpha.1.

This runner validates declared fixture documents with JSON Schema Draft 2020-12.
It does not transform state, enforce AMI semantic invariants, execute quarantine,
check execution gates, or recompute digests.
"""
from __future__ import annotations

import argparse
from importlib.metadata import version as package_version
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "migration"
SCHEMA_DIR = ROOT / "schemas" / "v0.3.0-alpha.1"
SCHEMA_PATHS = {
    "rc2_session_state": ROOT / "schemas" / "session-state-v0.2.5-rc.2.schema.yaml",
    "session_state": SCHEMA_DIR / "session-state.schema.yaml",
    "relay_block": SCHEMA_DIR / "relay-block.schema.yaml",
    "migration_evidence": SCHEMA_DIR / "migration-evidence.schema.yaml",
    "migration_audit": SCHEMA_DIR / "migration-audit.schema.yaml",
}
DEFINITION_PATH = SCHEMA_DIR / "definitions.schema.yaml"


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_validators() -> dict[str, Draft202012Validator]:
    schemas = [load_yaml(DEFINITION_PATH)] + [load_yaml(path) for path in SCHEMA_PATHS.values()]
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    registry = Registry().with_resources(
        [(schema["$id"], Resource.from_contents(schema)) for schema in schemas]
    )
    return {
        name: Draft202012Validator(load_yaml(path), registry=registry)
        for name, path in SCHEMA_PATHS.items()
    }


def error_record(error: Any) -> dict[str, Any]:
    return {
        "instance_path": "/" + "/".join(str(part) for part in error.absolute_path),
        "schema_path": "/" + "/".join(str(part) for part in error.absolute_schema_path),
        "message": error.message,
    }


def run_fixture(directory: Path, validators: dict[str, Draft202012Validator]) -> dict[str, Any]:
    manifest_path = directory / "manifest.yaml"
    if not manifest_path.exists():
        return {"fixture_id": directory.name, "result": "ERROR", "errors": ["manifest.yaml missing"]}

    manifest = load_yaml(manifest_path)
    fixture_id = manifest.get("fixture_id", directory.name)
    errors: list[str] = []
    checks_out: list[dict[str, Any]] = []

    for required in manifest.get("required_files", []):
        if not (directory / required).is_file():
            errors.append(f"required file missing: {required}")

    for check in manifest.get("checks", []):
        filename = check.get("file")
        schema_name = check.get("schema")
        expected = check.get("expect")
        if schema_name not in validators:
            errors.append(f"unknown schema key: {schema_name}")
            continue
        path = directory / str(filename)
        if not path.is_file():
            errors.append(f"check file missing: {filename}")
            continue
        try:
            instance = load_yaml(path)
            validation_errors = sorted(
                validators[schema_name].iter_errors(instance),
                key=lambda item: (list(item.absolute_path), list(item.absolute_schema_path)),
            )
        except Exception as exc:
            errors.append(f"{filename}: {type(exc).__name__}: {exc}")
            continue
        actual = "FAIL" if validation_errors else "PASS"
        matched = actual == expected
        checks_out.append(
            {
                "file": filename,
                "schema": schema_name,
                "expected": expected,
                "actual": actual,
                "matched": matched,
                "validation_errors": [error_record(item) for item in validation_errors],
            }
        )
        if not matched:
            errors.append(f"{filename}: expected {expected}, got {actual}")

    if not manifest.get("checks"):
        return {
            "fixture_id": fixture_id,
            "result": "DEFERRED",
            "checks": [],
            "semantic_status": manifest.get("semantic_status", "DEFERRED"),
            "errors": [],
        }

    return {
        "fixture_id": fixture_id,
        "result": "PASS" if not errors else "FAIL",
        "checks": checks_out,
        "semantic_status": manifest.get("semantic_status", "DEFERRED"),
        "semantic_error": manifest.get("semantic_error"),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", default="all", help="fixture directory name or all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    try:
        validators = build_validators()
    except Exception as exc:
        print(f"schema configuration error: {type(exc).__name__}: {exc}")
        return 3

    directories = sorted(path for path in FIXTURES.iterdir() if path.is_dir())
    if args.target != "all":
        directories = [path for path in directories if path.name == args.target]
    if not directories:
        print(f"fixture selection is empty: {args.target}")
        return 2

    results = [run_fixture(directory, validators) for directory in directories]
    blocking_failures = [item for item in results if item["result"] in {"FAIL", "ERROR"}]
    report = {
        "report_version": "1",
        "suite_result": "FAIL" if blocking_failures else "PASS",
        "validation_receipt": {
            "validator": "python-jsonschema",
            "validator_version": package_version("jsonschema"),
            "draft": "2020-12",
            "schemas": {name: str(path.relative_to(ROOT)) for name, path in SCHEMA_PATHS.items()},
            "fixture_count": len(results),
            "blocking_failure_count": len(blocking_failures),
        },
        "fixtures": results,
        "limitations": [
            "Schema checks do not prove migration transformation correctness.",
            "AMI semantic invariants are evaluated by validate_migration_semantics_v030.py.",
        ],
    }

    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['fixture_id']}] {item['result']} semantic={item['semantic_status']}")
            for check in item.get("checks", []):
                print(
                    f"  {check['file']} :: {check['schema']} "
                    f"expected={check['expected']} actual={check['actual']}"
                )
            for error in item.get("errors", []):
                print(f"  ERROR: {error}")
        receipt = report["validation_receipt"]
        print(
            f"suite: {report['suite_result']} "
            f"fixtures={receipt['fixture_count']} failures={receipt['blocking_failure_count']}"
        )

    return 1 if blocking_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
