#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, shlex, sys
from pathlib import Path
from typing import Any
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.3"
COMMAND_VERSION = "MADP-COMMAND-v0.2"
REGISTRY_PATH = ROOT / "registries/v0.3.0-alpha.3/commands.yaml"
SCHEMA_PATH = ROOT / "schemas/v0.3.0-alpha.3/command.schema.yaml"
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
REVISION_ARGUMENTS = {"revision", "decision_revision", "source_state_version", "expected_state_version", "report_revision"}
ALLOWED_VALUES = {
    ("prioritize", "priority"): {"HIGH", "MEDIUM", "LOW"},
    ("todo-update", "status"): {"OPEN", "IN_PROGRESS", "BLOCKED", "DEFERRED", "CANCELLED"},
    ("todo-promote", "target_type"): {"PROPOSAL", "ISSUE", "DECISION_CANDIDATE"},
    ("session-import-confirm", "selected_action"): {"CREATE_NEW_SESSION", "RESUME_EXISTING", "MERGE_AS_PROPOSAL", "QUARANTINE", "REJECT"},
    ("normalization-confirm", "status"): {"CONFIRMED", "REJECTED"},
    ("minutes-review", "review_status"): {"HUMAN_REVIEWED", "REJECTED", "CORRECTION_REQUIRED"},
    ("minutes-generate", "detail_level"): {"QUICK", "STANDARD", "AUDIT"},
    ("participant-set-mode", "participation_mode"): {"FULL_CONFORMANCE", "ASSISTED_CONFORMANCE", "OPINION_ONLY", "OBSERVER"},
}

class UniqueKeyLoader(yaml.SafeLoader):
    pass

def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError("mapping", node.start_mark, f"duplicate key: {key}", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping
UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)

def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def registry() -> dict[str, Any]:
    return load_yaml(REGISTRY_PATH)

def command_map() -> dict[str, dict[str, Any]]:
    return {x["command"]: x for x in registry()["commands"]}

def alias_map() -> dict[str, str]:
    return {x["alias"]: x["command"] for x in registry().get("aliases", [])}

def list_arguments(definition: dict[str, Any]) -> set[str]:
    return {k for k, v in definition.get("test_arguments", {}).items() if isinstance(v, list)}

def scalar(value: str) -> Any:
    low = value.lower()
    if low == "true": return True
    if low == "false": return False
    if low in {"null", "none"}: return None
    try: return int(value)
    except ValueError: pass
    if value.startswith("[") or value.startswith("{"):
        try: return json.loads(value)
        except json.JSONDecodeError: pass
    return value

def resolve_name(invoked: str) -> tuple[str | None, bool, str | None]:
    commands = command_map()
    if invoked in commands:
        return invoked, False, None
    target = alias_map().get(invoked)
    if target:
        return target, True, None
    return None, False, f"CMD_UNKNOWN_COMMAND:{invoked}"

def parse_cli(raw: str) -> tuple[str | None, str | None, bool, dict[str, Any], list[str]]:
    try: tokens = shlex.split(raw, posix=True)
    except ValueError as exc: return None, None, False, {}, [f"CMD_PARSE_ERROR:{exc}"]
    if len(tokens) < 2 or tokens[0] != "/madp":
        return None, None, False, {}, ["CMD_PARSE_ERROR:expected /madp <command>"]
    invoked = tokens[1]
    canonical, alias_used, error = resolve_name(invoked)
    if error: return invoked, None, False, {}, [error]
    definition = command_map()[canonical]
    list_args = list_arguments(definition)
    args: dict[str, Any] = {}
    errors: list[str] = []
    i = 2
    while i < len(tokens):
        token = tokens[i]
        if not token.startswith("--") or token == "--":
            errors.append(f"CMD_PARSE_AMBIGUITY:unbound_token:{token}"); i += 1; continue
        option = token[2:]
        if "=" in option:
            key, raw_value = option.split("=", 1)
            if not key or raw_value == "": errors.append(f"CMD_PARSE_ERROR:invalid_option:{token}"); i += 1; continue
            value = scalar(raw_value)
        else:
            key = option
            if i + 1 >= len(tokens) or tokens[i + 1].startswith("--"):
                errors.append(f"CMD_MISSING_REQUIRED_ARGUMENT:{key}"); i += 1; continue
            value = scalar(tokens[i + 1]); i += 1
        if key in list_args:
            args.setdefault(key, [])
            if isinstance(value, list): args[key].extend(value)
            else: args[key].append(value)
        elif key in args:
            errors.append(f"CMD_REPEATED_OPTION:{key}")
        else:
            args[key] = value
        i += 1
    return invoked, canonical, alias_used, args, errors

def strict_yaml_load(raw: str) -> Any:
    for token in yaml.scan(raw):
        if isinstance(token, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken, yaml.tokens.TagToken)):
            raise yaml.YAMLError("YAML anchors, aliases, and custom tags are forbidden")
    return yaml.load(raw, Loader=UniqueKeyLoader)

def parse_yaml_form(raw: str) -> tuple[str | None, str | None, bool, dict[str, Any], list[str]]:
    try: doc = strict_yaml_load(raw)
    except yaml.YAMLError as exc: return None, None, False, {}, [f"CMD_PARSE_ERROR:{exc}"]
    if not isinstance(doc, dict) or set(doc) != {"MADP_COMMAND"}:
        return None, None, False, {}, ["CMD_PARSE_ERROR:expected MADP_COMMAND root"]
    form = doc["MADP_COMMAND"]
    if not isinstance(form, dict): return None, None, False, {}, ["CMD_PARSE_ERROR:MADP_COMMAND must be object"]
    invoked = form.get("command")
    args = form.get("arguments", {})
    if not isinstance(invoked, str) or not invoked: return None, None, False, {}, ["CMD_PARSE_ERROR:command required"]
    if not isinstance(args, dict): return invoked, None, False, {}, ["CMD_PARSE_ERROR:arguments must be object"]
    canonical, alias_used, error = resolve_name(invoked)
    return invoked, canonical, alias_used, args, [error] if error else []

def empty(value: Any) -> bool:
    return value is None or value == "" or value == []

def semantic_errors(command: str, args: dict[str, Any]) -> list[str]:
    errors = []
    for key in REVISION_ARGUMENTS:
        if key in args and (isinstance(args[key], bool) or not isinstance(args[key], int) or args[key] < 0 or (key in {"revision", "decision_revision", "report_revision"} and args[key] < 1)):
            errors.append(f"CMD_REVISION_INVALID:{key}")
    for (cmd, key), allowed in ALLOWED_VALUES.items():
        if command == cmd and key in args and args[key] not in allowed:
            errors.append(f"CMD_ARGUMENT_VALUE_INVALID:{key}")
    if command == "approve" and "decision" in args and (not isinstance(args["decision"], str) or not ID_RE.fullmatch(args["decision"])):
        errors.append("CMD_APPROVAL_DECISION_INVALID")
    return errors

def error_artifact(raw: str, invoked: str | None, canonical: str | None, errors: list[str]) -> dict[str, Any]:
    missing = sorted({e.split(":", 1)[1] for e in errors if e.startswith("CMD_MISSING_REQUIRED_ARGUMENT:")})
    if missing and len(missing) == len(errors) and canonical:
        return {"command_needs_arguments": {"invoked_name": invoked, "command": canonical, "missing": missing, "command_applied": False}}
    return {"command_parse_error": {"input": raw or "<empty>", "invoked_name": invoked, "command": canonical, "reason": "; ".join(errors), "command_applied": False}}

def normalize(raw: str, command_id: str = "CMD-A3-001", issued_by: str = "SYSTEM") -> dict[str, Any]:
    if issued_by not in {"USER", "FACILITATOR", "PARTICIPANT", "HELP_ASSISTANT", "RECORDER", "SYSTEM"}:
        return error_artifact(raw, None, None, ["CMD_ISSUER_INVALID"])
    if raw.lstrip().startswith("/madp"):
        invoked, canonical, alias_used, args, errors = parse_cli(raw)
    else:
        invoked, canonical, alias_used, args, errors = parse_yaml_form(raw)
    if not canonical:
        return error_artifact(raw, invoked, canonical, errors or ["CMD_UNKNOWN_COMMAND"])
    definition = command_map()[canonical]
    known = set(definition.get("required_arguments", [])) | set(definition.get("optional_arguments", []))
    errors.extend(f"CMD_UNKNOWN_OPTION:{k}" for k in args if k not in known)
    errors.extend(f"CMD_MISSING_REQUIRED_ARGUMENT:{k}" for k in definition.get("required_arguments", []) if k not in args or empty(args[k]))
    errors.extend(semantic_errors(canonical, args))
    if errors: return error_artifact(raw, invoked, canonical, errors)
    block = {"command_block": {
        "command_id": command_id,
        "command_version": COMMAND_VERSION,
        "protocol_version": VERSION,
        "command": canonical,
        "invoked_name": invoked,
        "alias_used": alias_used,
        "command_class": definition["command_class"],
        "issued_by": issued_by,
        "issued_at": "UNKNOWN",
        "raw_input": raw,
        "parse_status": "PARSED",
        "validation_status": "NOT_VALIDATED",
        "authority_status": definition["default_authority_boundary"],
        "authority_boundary": definition["default_authority_boundary"],
        "arguments": args,
        "effects": {"intended": [definition["effect_summary"]], "prohibited": definition["prohibited_effects"]},
        "limitations": [],
    }}
    validator = Draft202012Validator(load_yaml(SCHEMA_PATH))
    schema_errors = sorted(validator.iter_errors(block), key=lambda e: list(e.path))
    block["command_block"]["validation_status"] = "SCHEMA_VALID" if not schema_errors else "SCHEMA_INVALID"
    if schema_errors: return error_artifact(raw, invoked, canonical, [f"CMD_SCHEMA_INVALID:{schema_errors[0].message}"])
    return block

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("command", nargs="?"); ap.add_argument("--issued-by", default="SYSTEM"); ap.add_argument("--command-id", default="CMD-A3-001"); ns = ap.parse_args()
    raw = ns.command if ns.command is not None else sys.stdin.read()
    result = normalize(raw, command_id=ns.command_id, issued_by=ns.issued_by)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "command_block" in result else 2

if __name__ == "__main__": raise SystemExit(main())
