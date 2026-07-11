#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.3"

SCHEMAS = {
    "deliberation": ROOT / "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "command": ROOT / "schemas/v0.3.0-alpha.3/command.schema.yaml",
    "migration": ROOT / "schemas/v0.3.0-alpha.3/migration.schema.yaml",
    "portability": ROOT / "schemas/v0.3.0-alpha.3/session-portability.schema.yaml",
}

REQUIRED_COMMANDS = {
    "session-start", "session-status", "session-checkpoint-create", "session-resume",
    "session-export", "session-import", "session-import-confirm", "session-end",
    "participant-add", "participant-update-capability", "participant-set-mode",
    "goal-propose", "goal-confirm", "role-assign", "role-pause", "role-retire",
    "relay-create-plain", "response-ingest", "response-normalize",
    "normalization-confirm", "claim-add", "claim-verify", "minutes-generate",
    "minutes-review", "minutes-approve", "minutes-redact", "minutes-export",
    "help", "help-context-create", "team-approval-record",
}

REQUIRED_SKILLS = {
    "madp-start": "router",
    "madp-facilitator": "facilitator",
    "madp-participant": "participant",
    "madp-recorder": "recorder",
    "madp-help": "help",
}

REQUIRED_FILES = [
    "README-v0.3.0-alpha.3.md",
    "README-v0.3.0-alpha.3.ja.md",
    "protocol/MADP-v0.3.0-alpha.3.md",
    "protocol/GLOSSARY-v0.3.0-alpha.3.md",
    "schemas/v0.3.0-alpha.3/deliberation.schema.yaml",
    "schemas/v0.3.0-alpha.3/command.schema.yaml",
    "schemas/v0.3.0-alpha.3/migration.schema.yaml",
    "schemas/v0.3.0-alpha.3/session-portability.schema.yaml",
    "registries/v0.3.0-alpha.3/commands.yaml",
    "bootstrap/alpha3/README.md",
    "bootstrap/alpha3/quick-start.md",
    "bootstrap/alpha3/verified-start.md",
    "bootstrap/alpha3/invite-limited-participant.md",
    "bootstrap/alpha3/help.md",
    "bootstrap/alpha3/start-with-skills.md",
    "docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md",
    "docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md",
    "docs/profiles/MADP_HELP-v0.3.0-alpha.3.md",
    "docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md",
    "docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md",
    "docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md",
    "docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md",
    "docs/evaluation/MADP-v0.3.0-alpha.3-usability-plan.md",
    "docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml",
    "docs/ja/v0.3.0-alpha.3/translation-manifest.yaml",
    "docs/ja/v0.3.0-alpha.3/session-portability.md",
    "docs/ja/v0.3.0-alpha.3/command-system.md",
    "docs/ja/v0.3.0-alpha.3/agent-skills.md",
    "skills/README.md",
    "skills/madp-start/SKILL.md",
    "skills/madp-facilitator/SKILL.md",
    "skills/madp-participant/SKILL.md",
    "skills/madp-recorder/SKILL.md",
    "skills/madp-help/SKILL.md",
    "dist/chatgpt/madp-facilitator-instructions.md",
    "dist/chatgpt/madp-help-instructions.md",
    "docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml",
    "docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml",
    "tests/v0.3.0-alpha.3/fixtures.yaml",
    "tests/v0.3.0-alpha.3/portability-fixtures.yaml",
    "tests/v0.3.0-alpha.3/migration-fixtures.yaml",
    "tests/v0.3.0-alpha.3/usability-scenarios.yaml",
    "scripts/check_alpha3_translation.py",
    "scripts/check_alpha3_migration.py",
    "scripts/check_alpha3_usability.py",
    "scripts/generate_alpha3_release_artifacts.py",
    "scripts/check_generated_alpha3_release_artifacts.py",
    "scripts/check_release_readiness_v030_alpha3.py",
]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def parse_skill(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    return yaml.safe_load(text[4:end]), text[end + 5:]


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

    for fixture_name in ["fixtures.yaml", "portability-fixtures.yaml"]:
        fixture_path = ROOT / "tests/v0.3.0-alpha.3" / fixture_name
        if not fixture_path.is_file() or not validators:
            continue
        fixture_data = load_yaml(fixture_path)
        for index, case in enumerate(fixture_data.get("valid", []), start=1):
            schema_name = case["schema"]
            errors = sorted(validators[schema_name].iter_errors(case["artifact"]), key=lambda e: list(e.path))
            if errors:
                problems.append(f"{fixture_name} valid fixture {index} failed: {errors[0].message}")
        for index, case in enumerate(fixture_data.get("invalid", []), start=1):
            schema_name = case["schema"]
            if not list(validators[schema_name].iter_errors(case["artifact"])):
                problems.append(f"{fixture_name} invalid fixture {index} unexpectedly passed")

    registry_path = ROOT / "registries/v0.3.0-alpha.3/commands.yaml"
    if registry_path.is_file():
        registry = load_yaml(registry_path)
        if registry.get("protocol_version") != VERSION:
            problems.append("command registry protocol_version mismatch")
        if registry.get("registry_version") != "MADP-COMMAND-REGISTRY-v0.3":
            problems.append("command registry version mismatch")
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
            if not item.get("group"):
                problems.append(f"command lacks group: {item.get('command')}")
            if not item.get("prohibited_effects"):
                problems.append(f"command lacks prohibited effects: {item.get('command')}")
        alias_items = registry.get("aliases", [])
        aliases = [item.get("alias") for item in alias_items]
        if len(aliases) != len(set(aliases)):
            problems.append("duplicate command aliases")
        for item in alias_items:
            if item.get("command") not in names:
                problems.append(f"alias points to unknown command: {item}")
        policy = registry.get("alias_policy", {})
        if policy.get("aliases_must_not_change_authority") is not True:
            problems.append("alias authority invariant missing")

        command_schema = load_yaml(SCHEMAS["command"])
        schema_names = set(command_schema["properties"]["command_block"]["properties"]["command"]["enum"])
        if schema_names != set(names):
            problems.append("command schema enum and registry differ")

    for skill_name, role in REQUIRED_SKILLS.items():
        path = ROOT / "skills" / skill_name / "SKILL.md"
        if not path.is_file():
            continue
        try:
            frontmatter, body = parse_skill(path)
        except Exception as exc:
            problems.append(f"invalid skill {skill_name}: {exc}")
            continue
        if frontmatter.get("name") != skill_name:
            problems.append(f"skill name mismatch: {skill_name}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name) or len(skill_name) > 64:
            problems.append(f"invalid Agent Skills name: {skill_name}")
        description = frontmatter.get("description", "")
        if not isinstance(description, str) or not (1 <= len(description) <= 1024):
            problems.append(f"invalid skill description: {skill_name}")
        metadata = frontmatter.get("metadata", {})
        if metadata.get("madp-version") != "0.3.0-alpha.3":
            problems.append(f"skill version drift: {skill_name}")
        if metadata.get("role") != role:
            problems.append(f"skill role mismatch: {skill_name}")
        if len(body.strip()) < 80:
            problems.append(f"skill instructions too short: {skill_name}")
        if frontmatter.get("allowed-tools"):
            problems.append(f"skill pre-approves tools without cross-client guarantees: {skill_name}")

    status_path = ROOT / "docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml"
    if status_path.is_file():
        status = load_yaml(status_path)
        if status.get("protocol_version") != VERSION:
            problems.append("implementation status version mismatch")
        if status.get("implementation_status") != "RELEASE_CANDIDATE_CONTENT_READY":
            problems.append("implementation status must be RELEASE_CANDIDATE_CONTENT_READY")
        if status.get("integration_status") != "IMPLEMENTATION_BRANCH":
            problems.append("implementation branch must identify IMPLEMENTATION_BRANCH")
        if status.get("content_ready") is not True:
            problems.append("release candidate content must be ready")
        if status.get("release_ready") is not False:
            problems.append("implementation branch must not claim final release readiness")
        checks = status.get("automated_checks", {})
        if not checks or any(value != "DONE" for value in checks.values()):
            problems.append("automated implementation checks are not all DONE")
        for key in ["agent_skills_packaging", "session_portability", "command_reorganization"]:
            if checks.get(key) != "DONE":
                problems.append(f"missing completed alpha.3 check: {key}")
        blockers = {item.get("id"): item.get("status") for item in status.get("release_blockers", [])}
        expected = {
            "A3-REL-001": "MANUAL_ACTION_REQUIRED",
            "A3-REL-002": "DONE",
            "A3-REL-003": "DONE",
            "A3-REL-004": "DONE",
            "A3-REL-005": "POST_MERGE_REQUIRED",
        }
        if blockers != expected:
            problems.append(f"release blocker status mismatch: {blockers}")

    trace_path = ROOT / "docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml"
    if trace_path.is_file():
        trace = load_yaml(trace_path)
        entries = trace.get("requirements", [])
        ids = [entry.get("id") for entry in entries]
        if len(ids) != len(set(ids)):
            problems.append("duplicate traceability requirement IDs")
        if len(entries) < 23:
            problems.append("alpha.3 traceability is incomplete")
        required_trace = {"A3-SKILL-002", "A3-PORT-001", "A3-CMD-002"}
        if not required_trace.issubset(set(ids)):
            problems.append("new alpha.3 requirements are missing from traceability")
        for entry in entries:
            if entry.get("status") != "IMPLEMENTED":
                problems.append(f"requirement not implemented: {entry.get('id')}")
            artifact = entry.get("artifact")
            if not artifact or not (ROOT / artifact).is_file():
                problems.append(f"traceability artifact missing for {entry.get('id')}: {artifact}")
            validation = entry.get("validation")
            if not validation or not (ROOT / validation).is_file():
                problems.append(f"traceability validation missing for {entry.get('id')}: {validation}")

    fixture_path = ROOT / "tests/v0.3.0-alpha.3/fixtures.yaml"
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

    portability_path = ROOT / "tests/v0.3.0-alpha.3/portability-fixtures.yaml"
    if portability_path.is_file():
        data = load_yaml(portability_path)
        for case in data.get("valid", []):
            artifact = case.get("artifact", {})
            report = artifact.get("session_import_report")
            if report and (report["canonical_state_modified"] or not report["confirmation_required"]):
                problems.append("valid import report violates confirmation boundary")
            manifest = artifact.get("portable_session_manifest")
            if manifest:
                policy = manifest["import_policy"]
                if policy["may_replace_existing_state"] or not policy["requires_human_confirmation"]:
                    problems.append("valid manifest allows silent state replacement")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("MADP-v0.3.0-alpha.3 integrated implementation checks: PASS")
    print(f"schemas: {len(validators)}")
    print(f"commands: {len(REQUIRED_COMMANDS)}")
    print(f"skills: {len(REQUIRED_SKILLS)}")
    print(f"required_files: {len(REQUIRED_FILES)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
