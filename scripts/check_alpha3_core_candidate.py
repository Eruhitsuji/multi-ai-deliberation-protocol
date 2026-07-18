#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MACROS = {
    "init",
    "register",
    "capture",
    "structure",
    "review",
    "decide",
    "authorize",
    "status",
}


def load_yaml(relative: str):
    path = ROOT / relative
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def command_names(registry) -> set[str]:
    return {
        item.get("command")
        for item in registry.get("commands", [])
        if isinstance(item, dict) and item.get("command")
    }


def referenced_commands(macro: dict) -> set[str]:
    found: set[str] = set()
    for step in macro.get("steps", []):
        if not isinstance(step, dict):
            continue
        if step.get("command"):
            found.add(step["command"])
        for command in step.get("one_of_commands", []):
            found.add(command)
    return found


def main() -> int:
    problems: list[str] = []
    required_files = [
        "docs/planning/DEC-MADP-CORE-001.yaml",
        "docs/planning/MADP-v0.3.0-alpha.3-exploratory-trials-01-30.md",
        "docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md",
        "docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md",
        "registries/v0.3.0-alpha.3/workflow-macros.yaml",
        "LICENSE",
    ]
    for relative in required_files:
        if not (ROOT / relative).is_file():
            problems.append(f"missing Core Candidate artifact: {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    decision = load_yaml("docs/planning/DEC-MADP-CORE-001.yaml")
    if decision.get("decision_id") != "DEC-MADP-CORE-001":
        problems.append("Core decision ID mismatch")
    if decision.get("status") != "ACCEPTED":
        problems.append("Core decision is not accepted")
    version_strategy = decision.get("version_strategy", {})
    if version_strategy.get("alpha3", {}).get("role") != "EXPERIMENTAL_BASELINE":
        problems.append("alpha.3 is not recorded as the experimental baseline")
    if version_strategy.get("alpha4", {}).get("implementation_status") != "DEFERRED":
        problems.append("alpha.4 implementation is not deferred")
    authorization = decision.get("implementation_authorization", {})
    if authorization.get("status") != "AUTHORIZED":
        problems.append("Core Candidate implementation is not authorized")
    for flag in ("release_authorized", "tag_authorized", "publication_authorized"):
        if authorization.get(flag) is not False:
            problems.append(f"{flag} must remain false")

    canonical = load_yaml("registries/v0.3.0-alpha.3/commands.yaml")
    canonical_names = command_names(canonical)
    macro_registry = load_yaml("registries/v0.3.0-alpha.3/workflow-macros.yaml")
    if macro_registry.get("protocol_version") != "MADP-v0.3.0-alpha.3":
        problems.append("workflow macro protocol version mismatch")
    if macro_registry.get("record_canonical_commands") is not True:
        problems.append("workflow macros must record canonical commands")
    if macro_registry.get("macros_are_aliases") is not False:
        problems.append("workflow macros must not be aliases")
    if macro_registry.get("macros_are_atomic") is not False:
        problems.append("workflow macros must not be atomic")

    macros = macro_registry.get("macros", [])
    names = [item.get("macro") for item in macros if isinstance(item, dict)]
    if set(names) != EXPECTED_MACROS or len(names) != len(EXPECTED_MACROS):
        problems.append(f"workflow macro set mismatch: {names!r}")
    for macro in macros:
        if not isinstance(macro, dict) or not macro.get("macro"):
            problems.append("invalid workflow macro entry")
            continue
        unknown = referenced_commands(macro) - canonical_names
        if unknown:
            problems.append(f"macro {macro['macro']} references unknown commands: {sorted(unknown)}")
        if not macro.get("required_invariants"):
            problems.append(f"macro {macro['macro']} has no required invariants")

    by_name = {item["macro"]: item for item in macros if isinstance(item, dict) and item.get("macro")}
    required_gates = {
        "init": {"HUMAN_CONFIRM_EXACT_PLAN_REVISION", "HUMAN_START_SESSION"},
        "capture": {"HUMAN_MANUAL_RELAY"},
        "structure": {"HUMAN_REVIEW_NORMALIZATION_DIFF"},
        "decide": {"HUMAN_REVIEW_EVIDENCE_AND_DISSENT"},
        "authorize": {"SEPARATE_TRUSTED_EXECUTION_CONFIRMATION"},
    }
    for macro_name, expected in required_gates.items():
        actual = {
            step.get("gate")
            for step in by_name.get(macro_name, {}).get("steps", [])
            if isinstance(step, dict) and step.get("gate")
        }
        if not expected.issubset(actual):
            problems.append(f"macro {macro_name} omits required gates: {sorted(expected - actual)}")

    profile_markers = {
        "docs/profiles/MADP_CORE_CANDIDATE-v0.3.0-alpha.3.md": [
            "Human Final Authority",
            "Agreement Is Not Evidence",
            "Blind First Round",
            "`UNKNOWN` must remain `UNKNOWN`",
            "manual copy-and-paste",
            "alpha.4 remains deferred",
        ],
        "docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.3.md": [
            "not a command alias",
            "non-atomic",
            "goal-confirm` never silently performs `session-start",
            "This macro never performs the external action itself",
        ],
        "docs/planning/MADP-v0.3.0-alpha.3-exploratory-trials-01-30.md": [
            "#01-#30",
            "2cf9a9d50eb48f740307a1c9f71d99f6155e36cf73af6fc9722360d6c4c2e2ab",
            "DEC-MADP-CORE-001",
            "not, by itself, formal release evidence",
        ],
    }
    for relative, markers in profile_markers.items():
        body = text(relative)
        for marker in markers:
            if marker not in body:
                problems.append(f"missing marker {marker!r}: {relative}")

    license_text = text("LICENSE")
    if not re.match(r"^MIT License\n", license_text):
        problems.append("repository license is not MIT")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print(
        "alpha.3 Core Candidate experiment: PASS "
        "(decision, 30-trial synthesis, 8 non-atomic macros, Blind First Round, MIT license)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
