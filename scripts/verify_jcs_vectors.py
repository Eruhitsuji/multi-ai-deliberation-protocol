#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VECTOR_ROOT = ROOT / "tests" / "canonicalization"
SAFE_INT_MIN = -9007199254740991
SAFE_INT_MAX = 9007199254740991


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def reject_unsupported(value: Any, path: str = "$") -> None:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return
    if isinstance(value, int):
        if not (SAFE_INT_MIN <= value <= SAFE_INT_MAX):
            raise ValueError(f"integer out of MADP_JCS_V1 range at {path}")
        return
    if isinstance(value, float):
        raise ValueError(f"floating point value prohibited at {path}")
    if isinstance(value, list):
        for index, item in enumerate(value):
            reject_unsupported(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError(f"non-string key prohibited at {path}")
            reject_unsupported(item, f"{path}.{key}")
        return
    raise ValueError(f"unsupported value type at {path}: {type(value).__name__}")


def canonical_bytes(value: Any) -> bytes:
    reject_unsupported(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_vector(directory: Path) -> dict[str, Any]:
    manifest = load_yaml(directory / "manifest.yaml")
    input_file = directory / manifest["input_file"]
    canonical_file = directory / manifest["canonical_byte_file"]
    expected = manifest["expected_sha256"]
    expected_len = int(manifest["expected_byte_length"])
    source = load_yaml(input_file)
    computed = canonical_bytes(source)
    stored = canonical_file.read_bytes()
    digest = hashlib.sha256(stored).hexdigest()
    return {
        "vector_id": manifest["vector_id"],
        "canonical_bytes_match": computed == stored,
        "byte_length": len(stored),
        "expected_byte_length": expected_len,
        "sha256": digest,
        "expected_sha256": expected,
        "matched": computed == stored and len(stored) == expected_len and digest == expected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default="all")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    directories = sorted(path for path in VECTOR_ROOT.iterdir() if path.is_dir())
    if args.target != "all":
        directories = [path for path in directories if path.name == args.target]
    results = [verify_vector(directory) for directory in directories]
    failed = [item for item in results if not item["matched"]]
    report = {"report_version": "1", "suite_result": "FAIL" if failed else "PASS", "vectors": results}
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"[{item['vector_id']}] {'PASS' if item['matched'] else 'FAIL'} sha256={item['sha256']} bytes={item['byte_length']}")
        print(f"suite: {report['suite_result']}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
