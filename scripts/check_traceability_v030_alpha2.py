#!/usr/bin/env python3
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "tests" / "traceability" / "traceability-matrix-v0.3.0-alpha.2.yaml"
PROTOCOL_VERSION = "MADP-v0.3.0-alpha.2"

REQUIRED = {
    "requirement_id",
    "origin",
    "protocol_clause",
    "schema_target",
    "fixtures",
    "error_codes",
    "release_gates",
}

REQUIRED_REQUIREMENTS = {
    "A2-TRC-CMD-001",
    "A2-TRC-CMD-002",
    "A2-TRC-CMD-003",
    "A2-TRC-CMD-004",
    "A2-TRC-CMD-005",
    "A2-TRC-CMD-006",
    "A2-TRC-TODO-001",
    "A2-TRC-TODO-002",
    "A2-TRC-CTX-001",
    "A2-TRC-CTX-002",
    "A2-TRC-REVIEW-001",
    "A2-TRC-BOOT-001",
    "A2-TRC-AIDEV-001",
    "A2-TRC-RELAY-001",
    "A2-TRC-MIG-001",
    "A2-TRC-BUNDLE-001",
}


def main() -> int:
    data = yaml.safe_load(MATRIX.read_text(encoding="utf-8"))
    failures: list[str] = []

    if data.get("protocol_version") != PROTOCOL_VERSION:
        failures.append(f"unexpected protocol_version: {data.get('protocol_version')!r}")

    entries = data.get("entries", [])
    if not isinstance(entries, list) or not entries:
        failures.append("matrix has no entries")
        entries = []

    seen_ids: set[str] = set()
    for index, entry in enumerate(entries, 1):
        missing = REQUIRED - set(entry)
        if missing:
            failures.append(f"entry {index}: missing {sorted(missing)}")

        requirement_id = entry.get("requirement_id")
        if requirement_id in seen_ids:
            failures.append(f"entry {index}: duplicate requirement_id {requirement_id}")
        if isinstance(requirement_id, str):
            seen_ids.add(requirement_id)

        if not entry.get("origin"):
            failures.append(f"entry {index}: origin must not be empty")
        if not entry.get("fixtures"):
            failures.append(f"entry {index}: fixtures must not be empty")
        if not entry.get("release_gates"):
            failures.append(f"entry {index}: release_gates must not be empty")

        target_path = str(entry.get("schema_target", "")).split("#", 1)[0]
        if target_path and not (ROOT / target_path).exists():
            failures.append(f"entry {index}: missing schema target path {target_path}")

        for fixture in entry.get("fixtures", []):
            path = str(fixture).split("#", 1)[0]
            if path and not (ROOT / path).exists():
                failures.append(f"entry {index}: missing fixture path {path}")

    missing_requirements = REQUIRED_REQUIREMENTS - seen_ids
    extra_requirements = seen_ids - REQUIRED_REQUIREMENTS
    if missing_requirements:
        failures.append(f"missing alpha.2 requirement coverage: {sorted(missing_requirements)}")
    if extra_requirements:
        failures.append(f"unregistered alpha.2 requirement coverage: {sorted(extra_requirements)}")
    if len(entries) != len(REQUIRED_REQUIREMENTS):
        failures.append(f"traceability entry count mismatch: {len(entries)} != {len(REQUIRED_REQUIREMENTS)}")

    if failures:
        print("alpha.2 traceability: FAIL")
        print("\n".join(failures))
        return 1

    print("alpha.2 traceability: PASS")
    print("requirements:", len(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
