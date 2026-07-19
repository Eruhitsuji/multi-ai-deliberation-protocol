#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
VERSION = "MADP-v0.3.0-alpha.4"
BRANCH = "feature/v0.3.0-alpha.4-core-usability-slice-1"
BASE_MAIN_COMMIT = "92174e7e651cc5ee7f8797a845cfc33fcd39af9a"

PROTOCOL_PATH = "protocol/MADP-v0.3.0-alpha.4-core-usability.md"
PROFILE_PATH = "docs/profiles/WORKFLOW_MACROS-v0.3.0-alpha.4.md"
REGISTRY_PATH = "registries/v0.3.0-alpha.4/workflow-macros.yaml"
COMMAND_REGISTRY_PATH = "registries/v0.3.0-alpha.3/commands.yaml"
SCHEMA_PATH = "schemas/v0.3.0-alpha.4/core-usability-record.schema.yaml"
FIXTURE_PATH = "tests/v0.3.0-alpha.4/core-usability-fixtures.yaml"
DECISION_PATH = "docs/planning/DEC-MADP-ALPHA4-002.yaml"
STATUS_PATH = "docs/planning/MADP-v0.3.0-alpha.4-implementation-status.yaml"
README_PATH = "README-v0.3.0-alpha.4.md"
RELEASE_PATH = "docs/releases/MADP-v0.3.0-alpha.4.md"
WORKFLOW_PATH = ".github/workflows/validate-alpha4-core-usability.yml"

PUBLIC_ARTIFACTS = (
    PROTOCOL_PATH,
    PROFILE_PATH,
    REGISTRY_PATH,
    SCHEMA_PATH,
    FIXTURE_PATH,
    DECISION_PATH,
    STATUS_PATH,
    README_PATH,
    RELEASE_PATH,
)

REQUIRED_FILES = PUBLIC_ARTIFACTS + (
    COMMAND_REGISTRY_PATH,
    "scripts/check_alpha4_kickoff.py",
    "scripts/check_alpha4_core_usability.py",
    WORKFLOW_PATH,
)

MACRO_ORDER = [
    "init",
    "register",
    "capture",
    "structure",
    "review",
    "decide",
    "authorize",
    "status",
]


def load_yaml(relative: str):
    return yaml.safe_load((ROOT / relative).read_text(encoding="utf-8"))


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def expand_local_refs(node, root):
    if isinstance(node, dict):
        if set(node) == {"$ref"} and isinstance(node["$ref"], str):
            ref = node["$ref"]
            prefix = "#/$defs/"
            if ref.startswith(prefix):
                target = root.get("$defs", {}).get(ref[len(prefix):])
                if target is None:
                    raise ValueError(f"unresolved local ref: {ref}")
                return expand_local_refs(deepcopy(target), root)
        return {
            key: expand_local_refs(value, root)
            for key, value in node.items()
            if key != "$defs"
        }
    if isinstance(node, list):
        return [expand_local_refs(value, root) for value in node]
    return node


def apply_mutations(base, mutations):
    value = deepcopy(base)
    for mutation in mutations:
        path = mutation["path"]
        cursor = value
        for item in path[:-1]:
            cursor = cursor[item]
        cursor[path[-1]] = deepcopy(mutation["value"])
    return value


def unique_ids(items, key):
    values = [item.get(key) for item in items]
    return len(values) == len(set(values))


def macro_steps(macro):
    result = []
    gates = []
    for index, step in enumerate(macro.get("steps", [])):
        if "command" in step:
            result.append((index, {step["command"]}, not step.get("optional", False)))
        elif "one_of_commands" in step:
            result.append((index, set(step["one_of_commands"]), True))
        elif "gate" in step:
            gates.append(step["gate"])
    return result, gates


def macro_trace_errors(artifact, registry_by_name, canonical_commands):
    errors = []
    for trace in artifact.get("macro_trace", []):
        macro_name = trace["macro"]
        macro = registry_by_name.get(macro_name)
        if macro is None:
            errors.append("UNKNOWN_MACRO")
            continue

        accepted = trace["accepted_canonical_commands"]
        if len(accepted) != len(set(accepted)):
            errors.append("DUPLICATE_ACCEPTED_COMMAND")
        if any(command not in canonical_commands for command in accepted):
            errors.append("NONCANONICAL_COMMAND_IN_MACRO_TRACE")

        step_options, required_gates = macro_steps(macro)
        matched_indices = []
        position = 0
        order_valid = True
        for command in accepted:
            match = None
            for offset in range(position, len(step_options)):
                if command in step_options[offset][1]:
                    match = offset
                    break
            if match is None:
                order_valid = False
                break
            matched_indices.append(match)
            position = match + 1
        if not order_valid:
            errors.append("MACRO_COMMAND_ORDER_INVALID")

        if trace["ended_state_version"] < trace["started_state_version"]:
            errors.append("MACRO_STATE_VERSION_REVERSED")

        encountered = set(trace["encountered_gates"])
        if not encountered.issubset(set(required_gates)):
            errors.append("UNKNOWN_MACRO_GATE")

        if trace["completion_status"] == "COMPLETE":
            required_indices = {
                offset
                for offset, (_, _, required) in enumerate(step_options)
                if required
            }
            if not required_indices.issubset(set(matched_indices)):
                errors.append("COMPLETE_MACRO_MISSING_REQUIRED_COMMANDS")
            if not set(required_gates).issubset(encountered):
                errors.append("COMPLETE_MACRO_MISSING_REQUIRED_GATE")
            if trace["stop_reason"] is not None:
                errors.append("COMPLETE_MACRO_HAS_STOP_REASON")
        elif trace["stop_reason"] is None:
            errors.append("INCOMPLETE_MACRO_MISSING_STOP_REASON")
    return errors


def semantic_errors(artifact, registry_by_name, canonical_commands):
    errors = []

    claims = artifact.get("claims", [])
    evidence = artifact.get("evidence", [])
    dissents = artifact.get("dissents", [])
    migrations = artifact.get("migration_records", [])
    decision = artifact.get("decision", {})

    if not unique_ids(artifact.get("macro_trace", []), "macro_execution_id"):
        errors.append("DUPLICATE_MACRO_EXECUTION_ID")
    if not unique_ids(claims, "claim_id"):
        errors.append("DUPLICATE_CLAIM_ID")
    if not unique_ids(evidence, "evidence_id"):
        errors.append("DUPLICATE_EVIDENCE_ID")
    if not unique_ids(dissents, "dissent_id"):
        errors.append("DUPLICATE_DISSENT_ID")
    if not unique_ids(migrations, "migration_id"):
        errors.append("DUPLICATE_MIGRATION_ID")

    claim_by_id = {item["claim_id"]: item for item in claims}
    evidence_by_id = {item["evidence_id"]: item for item in evidence}
    dissent_by_id = {item["dissent_id"]: item for item in dissents}

    for claim in claims:
        for evidence_ref in claim["evidence_refs"]:
            linked = evidence_by_id.get(evidence_ref)
            if linked is None:
                errors.append("DANGLING_CLAIM_EVIDENCE_REF")
            elif (
                claim["claim_id"] not in linked["supports_claim_refs"]
                and claim["claim_id"] not in linked["challenges_claim_refs"]
            ):
                errors.append("MISSING_EVIDENCE_BACKLINK")
        for dissent_ref in claim["dissent_refs"]:
            linked = dissent_by_id.get(dissent_ref)
            if linked is None:
                errors.append("DANGLING_CLAIM_DISSENT_REF")
            elif claim["claim_id"] not in linked["claim_refs"]:
                errors.append("MISSING_DISSENT_BACKLINK")
        fact_ref = claim.get("legacy_fact_ref")
        fact_revision = claim.get("legacy_fact_revision")
        if (fact_ref is None) != (fact_revision is None):
            errors.append("INCOMPLETE_LEGACY_FACT_BINDING")

    for item in evidence:
        linked_claims = item["supports_claim_refs"] + item["challenges_claim_refs"]
        if not linked_claims:
            errors.append("EVIDENCE_WITHOUT_CLAIM_LINK")
        for claim_ref in linked_claims:
            linked = claim_by_id.get(claim_ref)
            if linked is None:
                errors.append("DANGLING_EVIDENCE_CLAIM_REF")
            elif item["evidence_id"] not in linked["evidence_refs"]:
                errors.append("MISSING_CLAIM_BACKLINK")

    for dissent in dissents:
        for claim_ref in dissent["claim_refs"]:
            linked = claim_by_id.get(claim_ref)
            if linked is None:
                errors.append("DANGLING_DISSENT_CLAIM_REF")
            elif dissent["dissent_id"] not in linked["dissent_refs"]:
                errors.append("MISSING_CLAIM_DISSENT_BACKLINK")
        for evidence_ref in dissent["evidence_refs"]:
            if evidence_ref not in evidence_by_id:
                errors.append("DANGLING_DISSENT_EVIDENCE_REF")
        if dissent["disposition"] not in {"NONE", "WITHDRAWN"} and not dissent["disposition_rationale"]:
            errors.append("DISSENT_DISPOSITION_MISSING_RATIONALE")

    acknowledged = set(decision.get("acknowledged_dissent_refs", []))
    unresolved = set(decision.get("unresolved_dissent_refs", []))
    all_dissent_ids = set(dissent_by_id)
    if not acknowledged.issubset(all_dissent_ids):
        errors.append("DANGLING_DECISION_DISSENT_REF")
    if not unresolved.issubset(all_dissent_ids):
        errors.append("DANGLING_DECISION_UNRESOLVED_DISSENT_REF")
    for dissent in dissents:
        dissent_id = dissent["dissent_id"]
        if dissent_id not in acknowledged:
            errors.append("DISSENT_NOT_ACKNOWLEDGED_BY_DECISION")
        if dissent["status"] == "OPEN" and dissent_id not in unresolved:
            errors.append("OPEN_DISSENT_NOT_VISIBLE_IN_DECISION")
        if dissent["status"] != "OPEN" and dissent_id in unresolved:
            errors.append("RESOLVED_DISSENT_LISTED_AS_UNRESOLVED")

    for evidence_ref in decision.get("evidence_refs", []):
        if evidence_ref not in evidence_by_id:
            errors.append("DANGLING_DECISION_EVIDENCE_REF")

    seen_fact_versions = set()
    for migration in migrations:
        target = claim_by_id.get(migration["target_claim_ref"])
        if target is None:
            errors.append("DANGLING_MIGRATION_TARGET")
            continue
        key = (migration["source_fact_ref"], migration["source_fact_revision"])
        if key in seen_fact_versions:
            errors.append("DUPLICATE_SOURCE_FACT_MIGRATION")
        seen_fact_versions.add(key)
        if (
            target.get("legacy_fact_ref") != migration["source_fact_ref"]
            or target.get("legacy_fact_revision") != migration["source_fact_revision"]
        ):
            errors.append("MIGRATION_TARGET_BINDING_MISMATCH")
        if (
            migration["verification_status_before"]
            != migration["verification_status_after"]
            and migration["verification_change_basis"] == "PRESERVED"
        ):
            errors.append("VERIFICATION_CHANGE_BASIS_INVALID")

    errors.extend(macro_trace_errors(artifact, registry_by_name, canonical_commands))
    return sorted(set(errors))


def main() -> int:
    problems = []

    for relative in REQUIRED_FILES:
        if not (ROOT / relative).is_file():
            problems.append(f"missing required file: {relative}")
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    registry = load_yaml(REGISTRY_PATH)
    commands = load_yaml(COMMAND_REGISTRY_PATH)
    decision = load_yaml(DECISION_PATH)
    status = load_yaml(STATUS_PATH)
    fixtures = load_yaml(FIXTURE_PATH)
    schema = load_yaml(SCHEMA_PATH)

    if registry.get("registry_version") != "MADP-WORKFLOW-MACRO-REGISTRY-v0.2":
        problems.append("workflow macro registry version mismatch")
    if registry.get("protocol_version") != VERSION:
        problems.append("workflow macro protocol version mismatch")
    for key, expected in {
        "record_canonical_commands": True,
        "record_macro_trace": True,
        "macros_are_aliases": False,
        "macros_are_atomic": False,
        "authority_expansion": False,
    }.items():
        if registry.get(key) is not expected:
            problems.append(f"workflow macro registry invariant mismatch: {key}")

    macros = registry.get("macros", [])
    macro_names = [item.get("macro") for item in macros]
    if macro_names != MACRO_ORDER:
        problems.append(f"workflow macro order mismatch: {macro_names!r}")
    registry_by_name = {
        item["macro"]: item
        for item in macros
        if isinstance(item, dict) and "macro" in item
    }

    canonical_commands = {
        item.get("command")
        for item in commands.get("commands", [])
        if isinstance(item, dict)
    }
    step_ids = set()
    for macro in macros:
        for step in macro.get("steps", []):
            step_id = step.get("step_id")
            if not step_id or step_id in step_ids:
                problems.append("workflow macro step IDs must be present and unique")
            step_ids.add(step_id)
            listed = []
            if "command" in step:
                listed.append(step["command"])
            listed.extend(step.get("one_of_commands", []))
            for command in listed:
                if command not in canonical_commands:
                    problems.append(
                        f"workflow macro references noncanonical command: {command}"
                    )

    if decision.get("decision_id") != "DEC-MADP-ALPHA4-002":
        problems.append("alpha.4 Core Usability decision ID mismatch")
    if decision.get("status") != "ACCEPTED":
        problems.append("alpha.4 Core Usability decision is not accepted")
    if decision.get("parent_decision_ref") != "docs/planning/DEC-MADP-ALPHA4-001.yaml":
        problems.append("alpha.4 Core Usability parent decision mismatch")
    decision_body = decision.get("decision", {})
    for key, expected in {
        "implementation_slice": "CORE_USABILITY_SLICE_1",
        "target_version": VERSION,
        "implementation_authorized": True,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }.items():
        if decision_body.get(key) != expected:
            problems.append(f"alpha.4 Core Usability decision mismatch: {key}")
    boundary = decision.get("authorization_boundary", {})
    for key in (
        "merge_authorized",
        "tag_authorized",
        "github_release_authorized",
        "pages_publication_authorized",
        "stable_release_authorized",
    ):
        if boundary.get(key) is not False:
            problems.append(f"authorization boundary must remain false: {key}")

    expected_status = {
        "protocol_version": VERSION,
        "implementation_status": "CORE_USABILITY_SLICE_1_READY",
        "integration_status": "IMPLEMENTATION_BRANCH",
        "base_main_commit": BASE_MAIN_COMMIT,
        "branch": BRANCH,
        "content_ready": False,
        "release_ready": False,
        "tagged": False,
        "published": False,
        "stable_release_authorized": False,
        "formal_release_evidence": False,
    }
    for key, expected in expected_status.items():
        if status.get(key) != expected:
            problems.append(f"implementation status mismatch for {key}")

    expanded_schema = expand_local_refs(schema, schema)
    Draft202012Validator.check_schema(expanded_schema)
    validator = Draft202012Validator(expanded_schema)

    base_artifact = fixtures.get("base_valid_artifact")
    base_errors = list(validator.iter_errors(base_artifact))
    if base_errors:
        problems.append(f"base valid artifact failed schema: {base_errors[0].message}")
    else:
        semantic = semantic_errors(base_artifact, registry_by_name, canonical_commands)
        if semantic:
            problems.append(f"base valid artifact failed semantics: {semantic}")

    for case in fixtures.get("schema_invalid_cases", []):
        artifact = apply_mutations(base_artifact, case.get("mutations", []))
        if not list(validator.iter_errors(artifact)):
            problems.append(f"schema-invalid case unexpectedly passed: {case.get('id')}")

    for case in fixtures.get("semantic_invalid_cases", []):
        artifact = apply_mutations(base_artifact, case.get("mutations", []))
        schema_errors = list(validator.iter_errors(artifact))
        if schema_errors:
            problems.append(
                f"semantic-invalid case must remain schema-valid: {case.get('id')}: "
                f"{schema_errors[0].message}"
            )
            continue
        observed = semantic_errors(artifact, registry_by_name, canonical_commands)
        if case.get("expected_error") not in observed:
            problems.append(
                f"semantic-invalid case missed expected error: {case.get('id')}: "
                f"{case.get('expected_error')} not in {observed}"
            )

    protocol = read(PROTOCOL_PATH)
    profile = read(PROFILE_PATH)
    readme = read(README_PATH)
    release = read(RELEASE_PATH)
    for marker in (
        "Agreement among AI systems is not evidence",
        "legacy `FACT` records",
        "Workflow Macros",
        "external action",
    ):
        if marker not in protocol:
            problems.append(f"protocol marker missing: {marker}")
    for marker in (
        "Macros are guided workflows",
        "This macro never performs the external action",
        "Human Final Authority",
    ):
        if marker not in profile:
            problems.append(f"macro profile marker missing: {marker}")
    if "## Known limitations" not in readme:
        problems.append("alpha.4 README lacks known limitations")
    if "## Known limitations" not in release:
        problems.append("alpha.4 release notes lack known limitations")
    if "## Rollback and previous version" not in release:
        problems.append("alpha.4 release notes lack rollback information")

    private_token = "".join(chr(value) for value in (82, 101, 111))
    exact_private = re.compile(
        rf"(?i)(?<![A-Za-z0-9_]){re.escape(private_token)}(?![A-Za-z0-9_])"
    )
    email = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
    for relative in PUBLIC_ARTIFACTS:
        body = read(relative)
        if exact_private.search(body):
            problems.append(f"private identifier found in {relative}")
        if email.search(body):
            problems.append(f"email address found in {relative}")
        if "human-final-authority-input-raw.md" in body:
            problems.append(f"removed private raw path referenced in {relative}")
        if re.search(r"(?i)publish_identifier_mapping\s*:\s*true", body):
            problems.append(f"identifier mapping publication enabled in {relative}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print("MADP v0.3.0-alpha.4 Core Usability Slice 1: PASS")
    print(f"macros={len(macros)}")
    print(f"schema_invalid_cases={len(fixtures.get('schema_invalid_cases', []))}")
    print(f"semantic_invalid_cases={len(fixtures.get('semantic_invalid_cases', []))}")
    print("legacy_fact_records_preserved=true")
    print("human_final_authority_required=true")
    print("local_checkout_required=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
