#!/usr/bin/env python3
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "tests" / "traceability" / "traceability-matrix-v0.3.0-alpha.1.yaml"


def main() -> int:
    data = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    failures = []
    required = {"requirement_id", "origin", "protocol_clause", "schema_target", "fixtures", "error_codes", "release_gates"}
    for index, entry in enumerate(data.get("entries", []), 1):
        missing = required - set(entry)
        if missing:
            failures.append(f"entry {index}: missing {sorted(missing)}")
        for fixture in entry.get("fixtures", []):
            path = fixture.split("#", 1)[0]
            if path and not (ROOT / path).exists():
                failures.append(f"entry {index}: missing fixture path {path}")
    if failures:
        print("traceability: FAIL")
        print("\n".join(failures))
        return 1
    print("traceability: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
