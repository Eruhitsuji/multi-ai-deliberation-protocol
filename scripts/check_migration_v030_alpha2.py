#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "migration-v0.3.0-alpha.2"
SOURCE_VERSION = "MADP-v0.3.0-alpha.1"
TARGET_VERSION = "MADP-v0.3.0-alpha.2"


def load(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def check_fixture(directory: Path) -> dict[str, Any]:
    manifest = load(directory / "manifest.yaml")
    source = load(directory / manifest["source"])
    target = load(directory / manifest["expected_target"])
    fixture_id = manifest.get("fixture_id")
    failures: list[str] = []

    if manifest.get("source_protocol_version") != SOURCE_VERSION:
        failures.append("manifest source_protocol_version mismatch")
    if manifest.get("target_protocol_version") != TARGET_VERSION:
        failures.append("manifest target_protocol_version mismatch")

    source_protocol = source.get("session_state", {}).get("meta", {}).get("protocol_version")
    if source_protocol != SOURCE_VERSION:
        failures.append(f"source protocol mismatch: {source_protocol!r}")

    plan = target.get("migration_plan", {})
    if plan.get("source_protocol_version") != SOURCE_VERSION:
        failures.append("target migration_plan source_protocol_version mismatch")
    if plan.get("target_protocol_version") != TARGET_VERSION:
        failures.append("target migration_plan target_protocol_version mismatch")
    if plan.get("migration_status") != "PROPOSED_ONLY":
        failures.append("migration_status must be PROPOSED_ONLY")
    if plan.get("user_confirmation_required") is not True:
        failures.append("user_confirmation_required must be true")

    expected = set(manifest.get("expected_invariants", []) or [])

    if "active_session_auto_upgraded_false" in expected and plan.get("active_session_auto_upgraded") is not False:
        failures.append("active_session_auto_upgraded must be false")

    if "published_alpha1_tag_immutable_true" in expected and plan.get("published_alpha1_tag_immutable") is not True:
        failures.append("published_alpha1_tag_immutable must be true")

    if "relay_mode_defaulted_to_deliberation" in expected:
        relay_mode = target.get("relay_interpretation", {}).get("relay_mode")
        if relay_mode != "DELIBERATION":
            failures.append(f"relay_mode must default to DELIBERATION, got {relay_mode!r}")
        if target.get("relay_interpretation", {}).get("authority_boundary") != "PROPOSE_ONLY":
            failures.append("relay interpretation authority_boundary must be PROPOSE_ONLY")

    if "historical_text_interpreted_as_command_false" in expected and plan.get("historical_text_interpreted_as_command") is not False:
        failures.append("historical_text_interpreted_as_command must be false")

    command = target.get("command_interpretation", {})
    if "command_applied_false" in expected and command.get("command_applied") is not False:
        failures.append("command_applied must be false")
    if "authority_boundary_reference_only" in expected and command.get("authority_boundary") != "REFERENCE_ONLY":
        failures.append("command interpretation authority_boundary must be REFERENCE_ONLY")

    return {
        "fixture_id": fixture_id,
        "result": "FAIL" if failures else "PASS",
        "failures": failures,
    }


def main() -> int:
    results = []
    failed = False
    for directory in sorted(path for path in FIXTURES.iterdir() if path.is_dir()):
        result = check_fixture(directory)
        failed = failed or result["result"] != "PASS"
        results.append(result)

    report = {
        "suite": "alpha.2 migration fixtures",
        "result": "FAIL" if failed else "PASS",
        "fixtures": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
