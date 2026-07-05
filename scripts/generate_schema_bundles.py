#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "schemas" / "v0.3.0-alpha.1"
OUT = ROOT / "schemas" / "generated"

EXPECTED = {
    "session-state-v0.3.0-alpha.1.bundle.schema.yaml": {
        "id": "urn:madp:schema:bundle:session-state:0.3.0-alpha.1",
        "from": [
            "urn:madp:schema:session-state:0.3.0-alpha.1",
            "urn:madp:schema:definitions:0.3.0-alpha.1",
        ],
        "required": "session_state",
    },
    "relay-block-v0.3.0-alpha.1.bundle.schema.yaml": {
        "id": "urn:madp:schema:bundle:relay-block:0.3.0-alpha.1",
        "from": [
            "urn:madp:schema:relay-block:0.3.0-alpha.1",
            "urn:madp:schema:definitions:0.3.0-alpha.1",
        ],
        "required": "relay_block",
    },
}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def check_bundle(path: Path, spec: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return ["missing generated bundle"]
    data = load_yaml(path)
    if data.get("$id") != spec["id"]:
        errors.append("unexpected $id")
    if data.get("x-madp-generated-from") != spec["from"]:
        errors.append("unexpected x-madp-generated-from")
    if spec["required"] not in data.get("required", []):
        errors.append(f"required root missing: {spec['required']}")
    if spec["required"] not in data.get("properties", {}):
        errors.append(f"properties root missing: {spec['required']}")
    if "$defs" not in data:
        errors.append("$defs missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate committed generated bundles")
    args = parser.parse_args()
    failed = False
    for filename, spec in EXPECTED.items():
        path = OUT / filename
        errors = check_bundle(path, spec)
        if errors:
            failed = True
            print(f"DRIFT: {path.relative_to(ROOT)}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {path.relative_to(ROOT)}")
    if not args.check and failed:
        print("automatic regeneration is not yet implemented; fix generated bundles manually or extend this script")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
