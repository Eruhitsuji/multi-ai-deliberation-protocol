#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
COMMAND_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "command.schema.yaml"
REGISTRY_SCHEMA = ROOT / "schemas" / "v0.3.0-alpha.2" / "command-registry.schema.yaml"
REGISTRY = ROOT / "registries" / "v0.3.0-alpha.2" / "commands.yaml"


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []

    command_schema = load_yaml(COMMAND_SCHEMA)
    registry_schema = load_yaml(REGISTRY_SCHEMA)
    registry = load_yaml(REGISTRY)

    schema_validator = Draft202012Validator(registry_schema)
    schema_errors = sorted(schema_validator.iter_errors(registry), key=lambda error: list(error.path))
    for error in schema_errors:
        location = "/".join(str(part) for part in error.path) or "<root>"
        failures.append(f"registry schema error at {location}: {error.message}")

    command_enum = set(command_schema["$defs"]["commandName"]["enum"])
    registry_commands = [entry.get("command") for entry in registry.get("commands", [])]
    registry_command_set = set(registry_commands)

    if len(registry_commands) != len(registry_command_set):
        failures.append("registry contains duplicate command definitions")

    missing = command_enum - registry_command_set
    extra = registry_command_set - command_enum
    if missing:
        failures.append(f"registry missing command definitions: {sorted(missing)}")
    if extra:
        failures.append(f"registry contains commands not in command schema enum: {sorted(extra)}")

    for entry in registry.get("commands", []):
        command = entry.get("command", "<unknown>")
        required_args = entry.get("required_arguments", [])
        optional_args = entry.get("optional_arguments", [])
        if len(required_args) != len(set(required_args)):
            failures.append(f"{command}: duplicate required_arguments")
        if len(optional_args) != len(set(optional_args)):
            failures.append(f"{command}: duplicate optional_arguments")
        overlap = set(required_args) & set(optional_args)
        if overlap:
            failures.append(f"{command}: arguments listed as both required and optional: {sorted(overlap)}")

        argument_defs = entry.get("arguments", [])
        if argument_defs:
            names = [argument.get("name") for argument in argument_defs]
            if len(names) != len(set(names)):
                failures.append(f"{command}: duplicate argument definitions")
            defined = set(names)
            listed = set(required_args) | set(optional_args)
            undefined = listed - defined
            if undefined:
                failures.append(f"{command}: listed arguments lack definitions: {sorted(undefined)}")

    expected_required = {
        "approve": {"decision", "revision"},
        "todo-add": {"title"},
        "todo-done": {"todo_id", "completion_basis"},
        "external-action": {"action", "scope"},
    }
    by_name = {entry.get("command"): set(entry.get("required_arguments", [])) for entry in registry.get("commands", [])}
    for command, required in expected_required.items():
        actual = by_name.get(command, set())
        if not required <= actual:
            failures.append(f"{command}: missing expected required arguments {sorted(required - actual)}")

    authority_by_name = {entry.get("command"): entry.get("default_authority_boundary") for entry in registry.get("commands", [])}
    if authority_by_name.get("external-action") != "REQUIRES_USER_CONFIRMATION":
        failures.append("external-action must default to REQUIRES_USER_CONFIRMATION")
    if authority_by_name.get("todo-promote") != "REQUIRES_USER_CONFIRMATION":
        failures.append("todo-promote must default to REQUIRES_USER_CONFIRMATION")
    if authority_by_name.get("summarize-state") != "REFERENCE_ONLY":
        failures.append("summarize-state must default to REFERENCE_ONLY")

    if failures:
        print("alpha.2 command registry: FAIL")
        print("\n".join(failures))
        return 1

    print("alpha.2 command registry: PASS")
    print("commands:", len(registry_commands))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
