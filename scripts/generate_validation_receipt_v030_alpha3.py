#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any
import argparse
import hashlib
import importlib.metadata
import json
import sys
import yaml

from jsonschema import Draft202012Validator

VERSION = "MADP-v0.3.0-alpha.3"
RECEIPT_SCHEMA_REL = "schemas/v0.3.0-alpha.3/validation-receipt.schema.yaml"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    """MADP_CANONICAL_JSON_V1: UTF-8 JSON with sorted keys and no insignificant whitespace."""
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def yaml_value(data: bytes) -> Any:
    return yaml.safe_load(data.decode("utf-8"))


def json_pointer(path) -> str:
    if not path:
        return ""
    parts = []
    for item in path:
        token = str(item).replace("~", "~0").replace("/", "~1")
        parts.append(token)
    return "/" + "/".join(parts)


def validate_value(value: Any, schema: dict[str, Any]) -> list[dict[str, str]]:
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(value), key=lambda err: list(err.absolute_path))
    return [
        {"path": json_pointer(error.absolute_path), "message": error.message}
        for error in errors
    ]


def build_receipt(
    *,
    artifact_value: Any,
    artifact_bytes: bytes,
    artifact_type: str,
    artifact_id: str,
    artifact_locator: str,
    canonicalization: str,
    schema_value: dict[str, Any],
    schema_bytes: bytes,
    schema_path: str,
    receipt_id: str,
    artifact_revision: int | None = None,
    artifact_version: str | None = None,
    executor_type: str = "DETERMINISTIC_RUNTIME",
    executor_name: str = "madp-jsonschema-receipt",
    executor_version: str | None = None,
) -> dict[str, Any]:
    if (artifact_revision is None) == (artifact_version is None):
        raise ValueError("provide exactly one of artifact_revision or artifact_version")
    if canonicalization == "RAW_BYTES":
        digest_input = artifact_bytes
    elif canonicalization == "MADP_CANONICAL_JSON_V1":
        digest_input = canonical_json_bytes(artifact_value)
    else:
        raise ValueError(f"unsupported canonicalization: {canonicalization}")

    errors = validate_value(artifact_value, schema_value)
    artifact_ref: dict[str, Any] = {
        "artifact_type": artifact_type,
        "artifact_id": artifact_id,
        "artifact_locator": artifact_locator,
        "canonicalization": canonicalization,
        "artifact_sha256": sha256_bytes(digest_input),
    }
    if artifact_revision is not None:
        artifact_ref["artifact_revision"] = artifact_revision
    else:
        artifact_ref["artifact_version"] = artifact_version

    if executor_version is None:
        try:
            executor_version = importlib.metadata.version("jsonschema")
        except importlib.metadata.PackageNotFoundError:
            executor_version = "unknown"

    return {
        "VALIDATION_RECEIPT": {
            "receipt_id": receipt_id,
            "protocol_version": VERSION,
            "artifact_ref": artifact_ref,
            "schema_ref": {
                "path": schema_path,
                "sha256": sha256_bytes(schema_bytes),
            },
            "executor": {
                "type": executor_type,
                "name": executor_name,
                "version": executor_version,
            },
            "executed": True,
            "result": "PASS" if not errors else "FAIL",
            "errors": errors,
            "limitations": [],
        }
    }


def build_receipt_from_paths(
    *,
    artifact_path: Path,
    schema_path: Path,
    artifact_type: str,
    artifact_id: str,
    artifact_locator: str,
    canonicalization: str,
    receipt_id: str,
    artifact_revision: int | None = None,
    artifact_version: str | None = None,
) -> dict[str, Any]:
    artifact_bytes = artifact_path.read_bytes()
    schema_bytes = schema_path.read_bytes()
    return build_receipt(
        artifact_value=yaml_value(artifact_bytes),
        artifact_bytes=artifact_bytes,
        artifact_type=artifact_type,
        artifact_id=artifact_id,
        artifact_locator=artifact_locator,
        canonicalization=canonicalization,
        schema_value=yaml_value(schema_bytes),
        schema_bytes=schema_bytes,
        schema_path=str(schema_path).replace("\\", "/"),
        receipt_id=receipt_id,
        artifact_revision=artifact_revision,
        artifact_version=artifact_version,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--artifact-type", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--artifact-locator", required=True)
    parser.add_argument(
        "--canonicalization",
        choices=["RAW_BYTES", "MADP_CANONICAL_JSON_V1"],
        default="RAW_BYTES",
    )
    parser.add_argument("--receipt-id", required=True)
    version_group = parser.add_mutually_exclusive_group(required=True)
    version_group.add_argument("--artifact-revision", type=int)
    version_group.add_argument("--artifact-version")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    artifact_path = Path(args.artifact)
    schema_path = Path(args.schema)
    receipt = build_receipt_from_paths(
        artifact_path=artifact_path,
        schema_path=schema_path,
        artifact_type=args.artifact_type,
        artifact_id=args.artifact_id,
        artifact_locator=args.artifact_locator,
        canonicalization=args.canonicalization,
        receipt_id=args.receipt_id,
        artifact_revision=args.artifact_revision,
        artifact_version=args.artifact_version,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        yaml.safe_dump(receipt, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    result = receipt["VALIDATION_RECEIPT"]["result"]
    print(f"validation receipt written: {output} ({result})")
    return 0 if result == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
