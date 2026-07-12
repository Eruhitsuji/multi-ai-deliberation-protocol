#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import copy
import yaml

from jsonschema import Draft202012Validator

from generate_validation_receipt_v030_alpha3 import (
    build_receipt,
    canonical_json_bytes,
    sha256_bytes,
)

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_receipt(receipt):
    schema = load(ROOT / "schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml")
    errors = list(Draft202012Validator(schema).iter_errors(receipt))
    assert not errors, errors[0].message if errors else ""


def main() -> int:
    registry_path = ROOT / "registries/v0.3.0-alpha.3/commands.yaml"
    registry_schema_path = ROOT / "schemas/v0.3.0-alpha.3/command-registry.schema.yaml"
    registry_bytes = registry_path.read_bytes()
    registry_schema_bytes = registry_schema_path.read_bytes()
    registry = yaml.safe_load(registry_bytes)
    registry_schema = yaml.safe_load(registry_schema_bytes)

    registry_receipt = build_receipt(
        artifact_value=registry,
        artifact_bytes=registry_bytes,
        artifact_type="COMMAND_REGISTRY",
        artifact_id="COMMANDS-A3",
        artifact_locator="repo://registries/v0.3.0-alpha.3/commands.yaml",
        artifact_version=registry["registry_version"],
        canonicalization="RAW_BYTES",
        schema_value=registry_schema,
        schema_bytes=registry_schema_bytes,
        schema_path="schemas/v0.3.0-alpha.3/command-registry.schema.yaml",
        receipt_id="VAL-REGISTRY-A3",
    )
    validate_receipt(registry_receipt)
    row = registry_receipt["VALIDATION_RECEIPT"]
    assert row["result"] == "PASS"
    assert row["artifact_ref"]["artifact_version"] == "MADP-COMMAND-REGISTRY-v0.2"
    assert row["artifact_ref"]["artifact_sha256"] == sha256_bytes(registry_bytes)

    report = {
        "report_version": "MADP-PROTOCOL-LOAD-REPORT-v2",
        "report_id": "PLR-TEST",
        "revision": 1,
        "status": "INCOMPLETE",
    }
    report_schema = {
        "type": "object",
        "required": ["report_version", "report_id", "revision", "status"],
        "additionalProperties": False,
        "properties": {
            "report_version": {"const": "MADP-PROTOCOL-LOAD-REPORT-v2"},
            "report_id": {"type": "string"},
            "revision": {"type": "integer", "minimum": 1},
            "status": {"enum": ["COMPLETE", "INCOMPLETE"]},
        },
    }
    report_schema_bytes = yaml.safe_dump(report_schema, sort_keys=True).encode("utf-8")
    report_receipt = build_receipt(
        artifact_value=report,
        artifact_bytes=yaml.safe_dump(report, sort_keys=False).encode("utf-8"),
        artifact_type="PROTOCOL_LOAD_REPORT",
        artifact_id="PLR-TEST",
        artifact_locator="trial://TRIAL-001/protocol-load-report",
        artifact_revision=1,
        canonicalization="MADP_CANONICAL_JSON_V1",
        schema_value=report_schema,
        schema_bytes=report_schema_bytes,
        schema_path="schemas/example-report.schema.yaml",
        receipt_id="VAL-REPORT-001",
    )
    validate_receipt(report_receipt)
    assert report_receipt["VALIDATION_RECEIPT"]["artifact_ref"]["artifact_sha256"] == sha256_bytes(
        canonical_json_bytes(report)
    )

    invalid_registry = copy.deepcopy(registry)
    invalid_registry["commands"] = []
    failed = build_receipt(
        artifact_value=invalid_registry,
        artifact_bytes=yaml.safe_dump(invalid_registry).encode("utf-8"),
        artifact_type="COMMAND_REGISTRY",
        artifact_id="COMMANDS-A3-BAD",
        artifact_locator="memory://invalid-registry",
        artifact_version=registry["registry_version"],
        canonicalization="MADP_CANONICAL_JSON_V1",
        schema_value=registry_schema,
        schema_bytes=registry_schema_bytes,
        schema_path="schemas/v0.3.0-alpha.3/command-registry.schema.yaml",
        receipt_id="VAL-REGISTRY-A3-BAD",
    )
    validate_receipt(failed)
    assert failed["VALIDATION_RECEIPT"]["result"] == "FAIL"
    assert failed["VALIDATION_RECEIPT"]["errors"]

    print("MADP-v0.3.0-alpha.3 validation receipt generation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
