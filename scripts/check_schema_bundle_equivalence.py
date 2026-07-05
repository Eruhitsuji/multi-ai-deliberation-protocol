#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "schemas" / "v0.3.0-alpha.1"
GENERATED = ROOT / "schemas" / "generated"
FIXTURES = ROOT / "tests" / "migration"


def load(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def source_validator(root_file: str) -> Draft202012Validator:
    definitions = load(SRC / "definitions.schema.yaml")
    root = load(SRC / root_file)
    registry = Registry().with_resources(
        [
            (definitions["$id"], Resource.from_contents(definitions)),
            (root["$id"], Resource.from_contents(root)),
        ]
    )
    return Draft202012Validator(root, registry=registry)


def valid(validator: Draft202012Validator, instance: Any) -> bool:
    return not any(validator.iter_errors(instance))


def main() -> int:
    validators = {
        "session_state": (
            source_validator("session-state.schema.yaml"),
            Draft202012Validator(load(GENERATED / "session-state-v0.3.0-alpha.1.bundle.schema.yaml")),
        ),
        "relay_block": (
            source_validator("relay-block.schema.yaml"),
            Draft202012Validator(load(GENERATED / "relay-block-v0.3.0-alpha.1.bundle.schema.yaml")),
        ),
    }
    rows = []
    failed = False
    for directory in sorted(path for path in FIXTURES.iterdir() if path.is_dir()):
        manifest = load(directory / "manifest.yaml")
        for check in manifest.get("checks", []):
            schema_name = check.get("schema")
            if schema_name not in validators:
                continue
            instance = load(directory / check["file"])
            source_result = valid(validators[schema_name][0], instance)
            generated_result = valid(validators[schema_name][1], instance)
            matched = source_result == generated_result
            failed = failed or not matched
            rows.append(
                {
                    "fixture_id": manifest.get("fixture_id"),
                    "file": check["file"],
                    "schema": schema_name,
                    "source_valid": source_result,
                    "generated_valid": generated_result,
                    "matched": matched,
                }
            )
    report = {"report_version": "1", "suite_result": "FAIL" if failed else "PASS", "checks": rows}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
