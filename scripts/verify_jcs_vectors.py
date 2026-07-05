#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from yaml.constructor import ConstructorError
from yaml.tokens import AliasToken, AnchorToken, TagToken

ROOT = Path(__file__).resolve().parents[1]
VECTOR_ROOT = ROOT / "tests" / "canonicalization"
SAFE_INT_MIN = -9007199254740991
SAFE_INT_MAX = 9007199254740991


class StrictLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ConstructorError("while constructing a mapping", node.start_mark, f"duplicate key: {key!r}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml_strict(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    for token in yaml.scan(text):
        if isinstance(token, (AliasToken, AnchorToken)):
            raise ValueError("YAML_ALIAS_OR_ANCHOR_PROHIBITED")
        if isinstance(token, TagToken):
            raise ValueError("YAML_CUSTOM_TAG_PROHIBITED")
    try:
        return yaml.load(text, Loader=StrictLoader)
    except ConstructorError as exc:
        if "duplicate key" in str(exc):
            raise ValueError("YAML_DUPLICATE_KEY_PROHIBITED") from exc
        raise


def load_manifest(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def reject_unsupported(value: Any, path: str = "$") -> None:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if isinstance(value, int):
        if not (SAFE_INT_MIN <= value <= SAFE_INT_MAX):
            raise ValueError("INTEGER_OUT_OF_SAFE_RANGE")
        return
    if isinstance(value, float):
        raise ValueError("FLOAT_PROHIBITED")
    if isinstance(value, list):
        for index, item in enumerate(value):
            reject_unsupported(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("NON_STRING_KEY_PROHIBITED")
            reject_unsupported(item, f"{path}.{key}")
        return
    raise ValueError(f"UNSUPPORTED_VALUE_TYPE:{type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    reject_unsupported(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_valid_vector(directory: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    input_file = directory / manifest["input_file"]
    canonical_file = directory / manifest["canonical_byte_file"]
    expected = manifest["expected_sha256"]
    expected_len = int(manifest["expected_byte_length"])
    source = load_yaml_strict(input_file)
    computed = canonical_bytes(source)
    stored = canonical_file.read_bytes()
    digest = hashlib.sha256(stored).hexdigest()
    matched = computed == stored and len(stored) == expected_len and digest == expected
    return {
        "vector_id": manifest["vector_id"],
        "vector_type": "VALID",
        "canonical_bytes_match": computed == stored,
        "byte_length": len(stored),
        "expected_byte_length": expected_len,
        "sha256": digest,
        "expected_sha256": expected,
        "matched": matched,
    }


def verify_invalid_vector(directory: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    expected_error = manifest["expected_error"]
    actual_error = None
    try:
        source = load_yaml_strict(directory / manifest["input_file"])
        canonical_bytes(source)
    except Exception as exc:
        actual_error = str(exc).splitlines()[0]
    return {
        "vector_id": manifest["vector_id"],
        "vector_type": "INVALID",
        "expected_error": expected_error,
        "actual_error": actual_error,
        "matched": actual_error == expected_error,
    }


def verify_vector(directory: Path) -> dict[str, Any]:
    manifest = load_manifest(directory / "manifest.yaml")
    if manifest.get("vector_type", "VALID") == "INVALID":
        return verify_invalid_vector(directory, manifest)
    return verify_valid_vector(directory, manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    directories = sorted(path for path in VECTOR_ROOT.iterdir() if path.is_dir())
    if args.target != "all":
        directories = [path for path in directories if path.name == args.target]
    if not directories:
        print(f"vector selection is empty: {args.target}")
        return 2
    results = [verify_vector(directory) for directory in directories]
    failed = [item for item in results if not item["matched"]]
    report = {"report_version": "2", "suite_result": "FAIL" if failed else "PASS", "vectors": results}
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            if item["vector_type"] == "VALID":
                detail = f"sha256={item['sha256']} bytes={item['byte_length']}"
            else:
                detail = f"expected={item['expected_error']} actual={item['actual_error']}"
            print(f"[{item['vector_id']}] {'PASS' if item['matched'] else 'FAIL'} {detail}")
        print(f"suite: {report['suite_result']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
