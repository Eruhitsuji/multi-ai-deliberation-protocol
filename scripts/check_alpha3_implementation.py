#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.3"

SCHEMAS = {
    "deliberation": ROOT / "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "command": ROOT / "schemas/v0.3.0-alpha.3/command.schema.yaml",
}
REQUIRED_COMMANDS = {
    "participant-add", "participant-update-capability", "participant-set-mode",
    "goal-propose", "goal-confirm", "role-assign", "role-pause", "role-retire",
    "relay-create-plain", "response-ingest", "response-normalize",
    "normalization-confirm", "claim-add", "claim-verify", "minutes-generate",
    "minutes-review", "minutes-approve", "minutes-redact", "help",
    "help-context-create", "session-resume", "team-approval-record",
}
REQUIRED_FILES = [
    "README-v0.3.0-alpha.3.md",
    "protocol/MADP-v0.3.0-alpha.3.md",
    "protocol/GLOSSARY-v0.3.0-alpha.3.md",
    "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "schemas/v0.3.0-alpha.3/command.schema.yaml",
    "registries/v0.3.0-alpha.3/commands.yaml",
    "bootstrap/alpha3/README.md",
    "bootstrap/alpha3/quick-start.md",
    "bootstrap/alpha3/verified-start.md",
    "bootstrap/alpha3/invite-limited-participant.md",
    "bootstrap/alpha3/help.md",
    "docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md",
    "docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md",
    "docs/profiles/MADP_HELP-v0.3.0-alpha.3.md",
    "docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md",
    "skills/madp-facilitator/SKILL.md",
    "skills/madp-help/SKILL.md",
    "dist/chatgpt/madp-facilitator-instructions.md",
    "dist/chatgpt/madp-help-instructions.md",
    "docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml",
    "docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml",
    "tests/v0.3.0-alpha.3/fixtures.yaml",
]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    problems: list[str] = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"missing required file: {relative}")

    validators = {}
    for name, path in SCHEMAS.items():
        schema = load_yaml(path)
        try:
            Draft202012Validator.check_schema(schema)
        except Exception as exc:
            problems.append(f"invalid {name} schema: {exc}")
            continue
        validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())

    fixture_path = ROOT / "tests/v0.3.0-alpha.3/fixtures.yaml"
    if fixture_path.is_file() and validators:
        fixture_data = load_yaml(fixture_path)
        for index, case in enumerate(fixture_data.get("valid", []), start=1):
            schema_name = case["schema"]
            errors = sorted(validators[schema_name].iter_errors(case["artifact"]), key=lambda e: list(e.path))
            if errors:
                problems.append(f"valid fixture {index} failed: {errors[0].message}")
        for index, case in enumerate(fixture_data.get("invalid", []), start=1):
            schema_name = case["schema"]
            if not list(validators[schema_name].iter_errors(case["artifact"])):
                problems.append(f"invalid fixture {index} unexpectedly passed")

    registry_path = ROOT / "registries/v0.3.0-alpha.3/commands.yaml"
    if registry_path.is_file():
        registry = load_yaml(registry_path)
        if registry.get("protocol_version") != VERSION:
            problems.append("command registry protocol_version mismatch")
        names = [item.get("command") for item in registry.get("commands", [])]
        if len(names) != len(set(names)):
            problems.append("duplicate alpha.3 command names")
        missing = sorted(REQUIRED_COMMANDS - set(names))
        extra = sorted(set(names) - REQUIRED_COMMANDS)
        if missing:
            problems.append(f"missing alpha.3 commands: {missing}")
        if extra:
            problems.append(f"unexpected alpha.3 commands: {extra}")
        for item in registry.get("commands", []):
            if not item.get("prohibited_effects"):
                problems.append(f"command lacks prohibited effects: {item.get('command')}")

    status_path = ROOT / "docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml"
    if status_path.is_file():
        status = load_yaml(status_path)
        if status.get("protocol_version") != VERSION:
            problems.append("implementation status version mismatch")
        if status.get("implementation_status") != "DRAFT_IMPLEMENTED":
            problems.append("implementation status must be DRAFT_IMPLEMENTED")
        if status.get("release_ready") is not False:
            problems.append("draft implementation must not be release_ready")
        checks = status.get("automated_checks", {})
        if not checks or any(value != "DONE" for value in checks.values()):
            problems.append("automated implementation checks are not all DONE")
        if not status.get("release_blockers"):
            problems.append("release blockers must be explicit before release")

    trace_path = ROOT / "docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml"
    if trace_path.is_file():
        trace = load_yaml(trace_path)
        entries = trace.get("requirements", [])
        ids = [entry.get("id") for entry in entries]
        if len(ids) != len(set(ids)):
            problems.append("duplicate traceability requirement IDs")
        if len(entries) < 15:
            problems.append("alpha.3 traceability is incomplete")
        for entry in entries:
            if entry.get("status") != "IMPLEMENTED":
                problems.append(f"requirement not implemented: {entry.get('id')}")
            artifact = entry.get("artifact")
            if not artifact or not (ROOT / artifact).is_file():
                problems.append(f"traceability artifact missing for {entry.get('id')}: {artifact}")

    if fixture_path.is_file():
        data = load_yaml(fixture_path)
        for case in data.get("valid", []):
            artifact = case.get("artifact", {})
            participant = artifact.get("participant_profile")
            if participant and participant.get("participation_mode") == "OPINION_ONLY":
                authority = participant["authority"]
                if authority["may_approve"] or authority["may_execute"] or authority["may_update_canonical_state"]:
                    problems.append("OPINION_ONLY fixture has forbidden authority")
                required_forbidden_roles = {"FACILITATOR", "STATE_MAINTAINER", "APPROVER"}
                if not required_forbidden_roles.issubset(set(participant.get("ineligible_roles", []))):
                    problems.append("OPINION_ONLY fixture does not forbid authority roles")
            ledger = artifact.get("claim_ledger")
            if ledger:
                for claim in ledger["claims"]:
                    if claim["importance"] in {"HIGH", "CRITICAL"} and claim["claim_type"] in {"FACT", "SOURCE_CLAIM"}:
                        if claim["verification_status"] == "UNVERIFIED" and claim["usable_for_decision"]:
                            problems.append(f"unverified material claim marked usable: {claim['claim_id']}")
            minutes = artifact.get("session_minutes")
            if minutes and minutes["status"] == "AUTO_GENERATED_DRAFT":
                for decision in minutes["decisions"]:
                    if decision["approval_status"] == "APPROVED" and not decision["approved_by"]:
                        problems.append("approved decision in draft minutes lacks approver")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("MADP-v0.3.0-alpha.3 implementation checks: PASS")
    print(f"schemas: {len(validators)}")
    print(f"commands: {len(REQUIRED_COMMANDS)}")
    print(f"required_files: {len(REQUIRED_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
