#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import sys
import yaml
from jsonschema import Draft202012Validator

from generate_alpha3_dynamic_role_plan import ROLE_CAPABILITY, build_plan, correlated

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/v0.3.0-alpha.3/experimental/dynamic-role-plan.schema.yaml"


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def semantic_errors(plan: dict) -> list[str]:
    errors: list[str] = []
    services = plan.get("services", []) if isinstance(plan, dict) else []
    assignments = plan.get("assignments", []) if isinstance(plan, dict) else []
    service_by_id = {item.get("service_id"): item for item in services if isinstance(item, dict)}
    if len(service_by_id) != len(services):
        errors.append("DUPLICATE_SERVICE_ID")
    assignment_ids = [item.get("assignment_id") for item in assignments if isinstance(item, dict)]
    if len(assignment_ids) != len(set(assignment_ids)):
        errors.append("DUPLICATE_ASSIGNMENT_ID")

    for service in services:
        correlations = set(service.get("known_correlations", []))
        if service.get("service_id") in correlations:
            errors.append("SELF_CORRELATION")
        if not correlations.issubset(service_by_id):
            errors.append("UNKNOWN_CORRELATION_SERVICE")

    roles_filled: set[str] = set()
    proposer_services: set[str] = set()
    for assignment in assignments:
        service = service_by_id.get(assignment.get("service_id"))
        if service is None:
            errors.append("ASSIGNMENT_UNKNOWN_SERVICE")
            continue
        role = assignment.get("role")
        roles_filled.add(role)
        if role == "PROPOSER" and assignment.get("phase") == "BLIND_INITIAL":
            proposer_services.add(assignment.get("service_id"))
        if service.get("availability") == "UNAVAILABLE":
            errors.append("ASSIGNED_UNAVAILABLE_SERVICE")
        capability = ROLE_CAPABILITY.get(role)
        if not capability or service.get("capabilities", {}).get(capability) is not True:
            errors.append("ASSIGNMENT_CAPABILITY_MISMATCH")
        if assignment.get("authority") not in {"PROPOSE_ONLY", "OPINION_ONLY", "RECORD_ONLY"}:
            errors.append("ASSIGNMENT_AUTHORITY_INVALID")

    task = plan.get("task", {})
    required_roles = set(task.get("required_roles", []))
    unfilled = set(plan.get("unfilled_roles", []))
    if unfilled != required_roles - roles_filled:
        errors.append("UNFILLED_ROLE_MISMATCH")
    if plan.get("status") in {"READY", "DEGRADED"} and unfilled:
        errors.append("NON_DRAFT_PLAN_HAS_UNFILLED_ROLES")
    if plan.get("status") == "DRAFT" and not unfilled:
        errors.append("DRAFT_WITHOUT_UNFILLED_ROLES")

    blind = plan.get("blind_first_round", {})
    assigned_ids = blind.get("assigned_service_ids", [])
    eligible_ids = blind.get("eligible_service_ids", [])
    if set(assigned_ids) != proposer_services:
        errors.append("BLIND_ASSIGNMENT_MISMATCH")
    if not set(eligible_ids).issubset(set(assigned_ids)):
        errors.append("BLIND_ELIGIBLE_NOT_ASSIGNED")
    actual_eligible: list[str] = []
    for service_id in assigned_ids:
        service = service_by_id.get(service_id)
        if service is None:
            continue
        selected_services = [service_by_id[item] for item in actual_eligible]
        if all(not correlated(service, existing) for existing in selected_services):
            actual_eligible.append(service_id)
    if set(eligible_ids) != set(actual_eligible):
        errors.append("BLIND_ELIGIBLE_RECOMPUTE_MISMATCH")
    actual_groups = {
        service_by_id[item]["independence_group"]
        for item in actual_eligible if item in service_by_id
    }
    if blind.get("independence_group_count") != len(actual_groups):
        errors.append("BLIND_GROUP_COUNT_MISMATCH")

    required = task.get("blind_first_round_required") is True
    requested = task.get("blind_initial_response_count", 0)
    if blind.get("required") is not required or blind.get("requested_response_count") != requested:
        errors.append("BLIND_TASK_BINDING_MISMATCH")
    if required:
        should_be_valid = len(assigned_ids) >= requested and len(actual_eligible) >= requested
        expected_status = "PLAN_VALID" if should_be_valid else "PLAN_DEGRADED"
        if blind.get("status") != expected_status:
            errors.append("BLIND_STATUS_MISMATCH")
        expected_plan_status = "DRAFT" if unfilled else ("READY" if should_be_valid else "DEGRADED")
        if plan.get("status") != expected_plan_status:
            errors.append("PLAN_STATUS_MISMATCH")
    else:
        if requested != 0:
            errors.append("BLIND_NOT_REQUIRED_COUNT_NONZERO")
        if blind.get("status") != "NOT_REQUIRED":
            errors.append("BLIND_NOT_REQUIRED_STATUS")

    try:
        regenerated = build_plan({
            "plan_id": plan.get("plan_id"),
            "task": task,
            "services": services,
        })
    except ValueError:
        regenerated = None
    if regenerated is None or any(
        plan.get(key) != regenerated.get(key)
        for key in ("status", "assignments", "blind_first_round", "unfilled_roles", "warnings", "planner")
    ):
        errors.append("NONDETERMINISTIC_OR_TAMPERED_PLAN")

    if plan.get("human_final_authority") is not True:
        errors.append("HUMAN_FINAL_AUTHORITY_REQUIRED")
    if plan.get("approval_authority_granted") is not False:
        errors.append("APPROVAL_AUTHORITY_MUST_REMAIN_FALSE")
    if plan.get("formal_release_evidence") is not False:
        errors.append("ROLE_PLAN_MUST_REMAIN_NON_RELEASE")
    return sorted(set(errors))


def check(path: Path) -> list[str]:
    schema = load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    plan = load(path)
    schema_errors = sorted(validator.iter_errors(plan), key=lambda error: list(error.path))
    if schema_errors:
        return [f"schema failure: {schema_errors[0].message}"]
    return semantic_errors(plan)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate MADP alpha.3 dynamic role plan")
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        errors = check(args.plan)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("alpha.3 dynamic role plan: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
