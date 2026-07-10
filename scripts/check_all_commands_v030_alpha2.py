#!/usr/bin/env python3
from __future__ import annotations

import json
import yaml

from madp_validation import ROOT, load_yaml
from parse_command_v030_alpha2 import normalize

REGISTRY = ROOT / "registries" / "v0.3.0-alpha.2" / "commands.yaml"


def value_for(name: str):
    values = {
        "revision": 1,
        "priority": "HIGH",
        "relay_mode": "TASK_HANDOFF",
        "target_role": "REVIEWER",
        "dry_run": True,
    }
    return values.get(name, f"VALUE-{name.upper()}")


def yaml_command(command: str, arguments: dict) -> str:
    return yaml.safe_dump({"MADP_COMMAND": {"command": command, "arguments": arguments}}, sort_keys=False)


def main() -> int:
    registry = load_yaml(REGISTRY)
    results: list[dict] = []
    failures: list[str] = []

    for entry in registry["commands"]:
        command = entry["command"]
        required = entry.get("required_arguments", [])
        arguments = {name: value_for(name) for name in required}
        result = normalize(yaml_command(command, arguments), command_id=f"CMD-COVER-{command}")
        block = result.get("command_block")
        passed = bool(
            block
            and block.get("command") == command
            and block.get("command_class") == entry["command_class"]
            and block.get("authority_boundary") == entry["default_authority_boundary"]
            and block.get("validation_status") == "SCHEMA_VALID"
        )
        results.append({"command": command, "case": "valid_minimum", "result": "PASS" if passed else "FAIL"})
        if not passed:
            failures.append(f"{command}: minimum valid command failed: {result}")

        if required:
            omitted = required[-1]
            incomplete = {name: value_for(name) for name in required if name != omitted}
            missing_result = normalize(yaml_command(command, incomplete), command_id=f"CMD-MISSING-{command}")
            needs = missing_result.get("command_needs_arguments", {})
            missing_passed = omitted in needs.get("missing", []) and needs.get("command_applied") is False
            results.append({"command": command, "case": f"missing:{omitted}", "result": "PASS" if missing_passed else "FAIL"})
            if not missing_passed:
                failures.append(f"{command}: missing required argument was not rejected: {missing_result}")

    expected_count = 20
    if len(registry["commands"]) != expected_count:
        failures.append(f"registry command count is {len(registry['commands'])}, expected {expected_count}")

    print(json.dumps({"suite": "alpha.2 all-command coverage", "result": "FAIL" if failures else "PASS", "command_count": len(registry["commands"]), "cases": results, "errors": failures}, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
