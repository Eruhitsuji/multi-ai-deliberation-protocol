#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

from madp_validation import ROOT, UniqueKeyLoader, load_yaml

VERSION = "MADP-v0.3.0-alpha.2"
COMMAND_VERSION = "MADP-COMMAND-v0.1"
REGISTRY_PATH = ROOT / "registries" / "v0.3.0-alpha.2" / "commands.yaml"
SCHEMA_PATH = ROOT / "schemas" / "v0.3.0-alpha.2" / "command.schema.yaml"
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")

BOOLEAN_ARGUMENTS = {
    ("share-context", "include_files"),
    ("issue-relay", "include_state"),
    ("issue-relay", "include_evidence"),
    ("summarize-state", "include_todos"),
    ("external-action", "dry_run"),
}
ALLOWED_VALUES: dict[tuple[str, str], set[str]] = {
    ("issue-relay", "relay_mode"): {"DELIBERATION", "INFORMATION_TRANSFER", "REVIEW_REQUEST", "TASK_HANDOFF", "EVIDENCE_TRANSFER", "RECOVERY"},
    ("todo-add", "type"): {"DISCUSSION", "DESIGN", "SCHEMA", "IMPLEMENTATION", "VALIDATION", "DOCUMENTATION", "RELEASE", "SAFETY"},
    ("todo-add", "priority"): {"HIGH", "MEDIUM", "LOW"},
    ("todo-add", "owner"): {"USER", "FACILITATOR", "PARTICIPANT", "UNSPECIFIED"},
    ("todo-list", "status"): {"OPEN", "IN_PROGRESS", "BLOCKED", "DONE", "DEFERRED", "CANCELLED"},
    ("todo-list", "priority"): {"HIGH", "MEDIUM", "LOW"},
    ("todo-update", "status"): {"OPEN", "IN_PROGRESS", "BLOCKED", "DONE", "DEFERRED", "CANCELLED"},
    ("todo-update", "priority"): {"HIGH", "MEDIUM", "LOW"},
    ("prioritize", "priority"): {"HIGH", "MEDIUM", "LOW"},
    ("todo-promote", "target_type"): {"PROPOSAL", "ISSUE", "DECISION_CANDIDATE"},
}


def registry_by_name() -> dict[str, dict[str, Any]]:
    registry = load_yaml(REGISTRY_PATH)
    return {entry["command"]: entry for entry in registry["commands"]}


def argument_cardinalities(definition: dict[str, Any]) -> dict[str, str]:
    return {item["name"]: item.get("cardinality", "SCALAR") for item in definition.get("arguments", [])}


def scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    try:
        return int(value)
    except ValueError:
        return value


def add_argument(arguments: dict[str, Any], key: str, value: Any, cardinality: str, errors: list[str]) -> None:
    if cardinality == "LIST":
        arguments.setdefault(key, [])
        if not isinstance(arguments[key], list):
            errors.append(f"CMD_ARGUMENT_CARDINALITY:{key}:expected_list")
            return
        arguments[key].append(value)
        return
    if key in arguments:
        errors.append(f"CMD_REPEATED_OPTION:{key}")
        return
    arguments[key] = value


def parse_cli(raw: str) -> tuple[str | None, dict[str, Any], list[str]]:
    try:
        tokens = shlex.split(raw, posix=True)
    except ValueError as error:
        return None, {}, [f"CMD_PARSE_ERROR:{error}"]
    if len(tokens) < 2 or tokens[0] != "/madp":
        return None, {}, ["CMD_PARSE_ERROR:expected /madp <command>"]

    command = tokens[1]
    definition = registry_by_name().get(command, {})
    cardinalities = argument_cardinalities(definition)
    arguments: dict[str, Any] = {}
    errors: list[str] = []
    index = 2
    while index < len(tokens):
        token = tokens[index]
        if not token.startswith("--") or token == "--":
            errors.append(f"CMD_PARSE_AMBIGUITY:unbound_token:{token}")
            index += 1
            continue
        option = token[2:]
        if "=" in option:
            key, value = option.split("=", 1)
            if not key or value == "":
                errors.append(f"CMD_PARSE_ERROR:invalid_option:{token}")
                index += 1
                continue
            parsed_value: Any = scalar(value)
        else:
            key = option
            if index + 1 < len(tokens) and not tokens[index + 1].startswith("--"):
                parsed_value = scalar(tokens[index + 1])
                index += 1
            elif (command, key) in BOOLEAN_ARGUMENTS:
                parsed_value = True
            else:
                errors.append(f"CMD_MISSING_REQUIRED_ARGUMENT:{key}")
                index += 1
                continue
        add_argument(arguments, key, parsed_value, cardinalities.get(key, "SCALAR"), errors)
        index += 1
    return command, arguments, errors


def strict_yaml_load(raw: str) -> Any:
    for token in yaml.scan(raw):
        if isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)):
            raise yaml.YAMLError("YAML anchors, aliases, and custom tags are forbidden")
    return yaml.load(raw, Loader=UniqueKeyLoader)


def parse_yaml_form(raw: str) -> tuple[str | None, dict[str, Any], list[str]]:
    try:
        document = strict_yaml_load(raw)
    except yaml.YAMLError as error:
        return None, {}, [f"CMD_PARSE_ERROR:{error}"]
    if not isinstance(document, dict) or set(document) != {"MADP_COMMAND"}:
        return None, {}, ["CMD_PARSE_ERROR:expected MADP_COMMAND root"]
    command_form = document["MADP_COMMAND"]
    if not isinstance(command_form, dict):
        return None, {}, ["CMD_PARSE_ERROR:MADP_COMMAND must be an object"]
    command = command_form.get("command")
    arguments = command_form.get("arguments", {})
    if not isinstance(command, str) or not command:
        return None, {}, ["CMD_PARSE_ERROR:command is required"]
    if not isinstance(arguments, dict):
        return command, {}, ["CMD_PARSE_ERROR:arguments must be an object"]

    definition = registry_by_name().get(command, {})
    cardinalities = argument_cardinalities(definition)
    errors: list[str] = []
    normalized: dict[str, Any] = {}
    for key, value in arguments.items():
        if not isinstance(key, str):
            errors.append("CMD_PARSE_ERROR:argument keys must be strings")
            continue
        cardinality = cardinalities.get(key, "SCALAR")
        if cardinality == "LIST":
            normalized[key] = value if isinstance(value, list) else [value]
        elif isinstance(value, list):
            errors.append(f"CMD_ARGUMENT_CARDINALITY:{key}:expected_scalar")
        else:
            normalized[key] = value
    return command, normalized, errors


def empty_value(value: Any) -> bool:
    return value is None or value == "" or value == []


def semantic_errors(command: str, arguments: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key, value in arguments.items():
        allowed = ALLOWED_VALUES.get((command, key))
        values = value if isinstance(value, list) else [value]
        if allowed and any(not isinstance(item, str) or item not in allowed for item in values):
            errors.append(f"CMD_ARGUMENT_VALUE_INVALID:{key}")
    if command == "approve":
        if "decision" in arguments and not empty_value(arguments["decision"]):
            decision = arguments["decision"]
            if not isinstance(decision, str) or not IDENTIFIER_RE.fullmatch(decision):
                errors.append("CMD_APPROVAL_DECISION_INVALID")
        if "revision" in arguments and not empty_value(arguments["revision"]):
            revision = arguments["revision"]
            if isinstance(revision, bool) or not isinstance(revision, int) or revision <= 0:
                errors.append("CMD_APPROVAL_REVISION_INVALID")
    return errors


def error_artifact(raw: str, command: str | None, errors: list[str]) -> dict[str, Any]:
    missing = [item.split(":", 1)[1] for item in errors if item.startswith("CMD_MISSING_REQUIRED_ARGUMENT:")]
    only_missing = bool(errors) and len(missing) == len(errors)
    if only_missing and command:
        return {"command_needs_arguments": {"command": command, "missing": sorted(set(missing)), "command_applied": False}}
    return {
        "command_parse_error": {
            "input": raw if raw else "<empty>",
            "reason": "; ".join(errors) or "CMD_PARSE_ERROR:unknown",
            **({"command": command} if command in registry_by_name() else {}),
            "command_applied": False,
        }
    }


def normalize(raw: str, command_id: str = "CMD-NORMALIZED-001", issued_by: str = "SYSTEM") -> dict[str, Any]:
    stripped = raw.lstrip()
    command, arguments, errors = parse_cli(raw) if stripped.startswith("/madp") else parse_yaml_form(raw)

    registry = registry_by_name()
    if command not in registry:
        errors.append(f"CMD_UNKNOWN_COMMAND:{command}")
        return error_artifact(raw, command, errors)

    definition = registry[command]
    known = set(definition.get("required_arguments", [])) | set(definition.get("optional_arguments", []))
    for key in arguments:
        if key not in known:
            errors.append(f"CMD_UNKNOWN_OPTION:{key}")
    for key in definition.get("required_arguments", []):
        if key not in arguments or empty_value(arguments[key]):
            errors.append(f"CMD_MISSING_REQUIRED_ARGUMENT:{key}")
    errors.extend(semantic_errors(command, arguments))
    if errors:
        return error_artifact(raw, command, errors)

    authority = definition["default_authority_boundary"]
    block = {
        "command_block": {
            "command_id": command_id,
            "command_version": COMMAND_VERSION,
            "protocol_version": VERSION,
            "command": command,
            "command_class": definition["command_class"],
            "issued_by": issued_by,
            "issued_at": "UNKNOWN",
            "raw_input": raw,
            "parse_status": "PARSED",
            "validation_status": "NOT_VALIDATED",
            "authority_status": authority,
            "authority_boundary": authority,
            "arguments": arguments,
            "effects": {"intended": [definition["effect_summary"]], "prohibited": definition.get("prohibited_effects", [])},
        }
    }
    validator = Draft202012Validator(load_yaml(SCHEMA_PATH), format_checker=FormatChecker())
    schema_errors = list(validator.iter_errors(block))
    block["command_block"]["validation_status"] = "SCHEMA_VALID" if not schema_errors else "SCHEMA_INVALID"
    if schema_errors:
        return error_artifact(raw, command, [f"CMD_SCHEMA_INVALID:{error.message}" for error in schema_errors])
    return block


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse and normalize a MADP v0.3.0-alpha.2 command.")
    parser.add_argument("command", nargs="?", help="CLI or YAML command text. Reads stdin when omitted.")
    parser.add_argument("--command-id", default="CMD-NORMALIZED-001")
    parser.add_argument("--issued-by", choices=["USER", "FACILITATOR", "PARTICIPANT", "SYSTEM"], default="SYSTEM")
    args = parser.parse_args()
    raw = args.command if args.command is not None else sys.stdin.read()
    result = normalize(raw, command_id=args.command_id, issued_by=args.issued_by)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "command_block" in result else 2


if __name__ == "__main__":
    raise SystemExit(main())
