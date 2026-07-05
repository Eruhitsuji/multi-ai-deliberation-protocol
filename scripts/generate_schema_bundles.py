#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "schemas" / "v0.3.0-alpha.1"
OUT = ROOT / "schemas" / "generated"


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_yaml(data: Any) -> str:
    return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000)


def deref(obj: Any, definitions: dict[str, Any]) -> Any:
    if isinstance(obj, dict):
        ref = obj.get("$ref")
        if isinstance(ref, str) and ref.startswith("urn:madp:schema:definitions:0.3.0-alpha.1#/$defs/"):
            key = ref.rsplit("/", 1)[-1]
            return deref(definitions["$defs"][key], definitions)
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            key = ref.rsplit("/", 1)[-1]
            return {"$ref": f"#/$defs/{key}"}
        return {key: deref(value, definitions) for key, value in obj.items()}
    if isinstance(obj, list):
        return [deref(item, definitions) for item in obj]
    return obj


def make_bundle(root_name: str, root_schema_file: str, defs_root: str, bundle_id: str) -> str:
    definitions = load_yaml(SRC / "definitions.schema.yaml")
    root = load_yaml(SRC / root_schema_file)
    bundle = {
        "$schema": root["$schema"],
        "$id": bundle_id,
        "title": root.get("title", "MADP bundle"),
        "x-madp-generated-from": [root["$id"], definitions["$id"]],
        "type": root.get("type", "object"),
        "additionalProperties": root.get("additionalProperties", False),
        "required": root.get("required", [root_name]),
        "properties": {
            root_name: {"$ref": f"#/$defs/{defs_root}"}
        },
        "$defs": definitions["$defs"],
    }
    return dump_yaml(bundle)


def outputs() -> dict[Path, str]:
    return {
        OUT / "session-state-v0.3.0-alpha.1.bundle.schema.yaml": make_bundle(
            "session_state",
            "session-state.schema.yaml",
            "sessionState",
            "urn:madp:schema:bundle:session-state:0.3.0-alpha.1",
        ),
        OUT / "relay-block-v0.3.0-alpha.1.bundle.schema.yaml": make_bundle(
            "relay_block",
            "relay-block.schema.yaml",
            "relayBlock",
            "urn:madp:schema:bundle:relay-block:0.3.0-alpha.1",
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    failed = False
    for path, content in outputs().items():
        if args.check:
            current = path.read_text(encoding="utf-8") if path.exists() else ""
            if current != content:
                failed = True
                print(f"DRIFT: {path.relative_to(ROOT)}")
                for line in difflib.unified_diff(current.splitlines(), content.splitlines(), fromfile="current", tofile="generated", lineterm=""):
                    print(line)
            else:
                print(f"OK: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"WROTE: {path.relative_to(ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
