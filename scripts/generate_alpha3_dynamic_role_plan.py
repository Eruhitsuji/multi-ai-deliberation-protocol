#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import re
import sys
import yaml

PROTOCOL_VERSION = "MADP-v0.3.0-alpha.3"
PLAN_VERSION = "MADP-DYNAMIC-ROLE-PLAN-v1"
ROLE_CAPABILITY = {
    "FACILITATOR": "facilitation",
    "PROPOSER": "generation",
    "CRITIC": "critique",
    "EVIDENCE_REVIEWER": "evidence_review",
    "RECORDER": "recording",
}
ROLE_PHASE = {
    "FACILITATOR": "ALL",
    "PROPOSER": "BLIND_INITIAL",
    "CRITIC": "CROSS_EXPOSURE",
    "EVIDENCE_REVIEWER": "CROSS_EXPOSURE",
    "RECORDER": "ALL",
}
ROLE_AUTHORITY = {
    "FACILITATOR": "PROPOSE_ONLY",
    "PROPOSER": "PROPOSE_ONLY",
    "CRITIC": "OPINION_ONLY",
    "EVIDENCE_REVIEWER": "OPINION_ONLY",
    "RECORDER": "RECORD_ONLY",
}
AVAILABILITY_SCORE = {"AVAILABLE": 20, "LIMITED": 5, "UNAVAILABLE": -10_000}
USAGE_SCORE = {"PREFER": 6, "NORMAL": 3, "MINIMIZE": 0}
COST_SCORE = {"FREE": 3, "SUBSCRIPTION": 2, "METERED": -3, "UNKNOWN": 0}
CAPABILITY_KEYS = {
    "facilitation",
    "generation",
    "critique",
    "evidence_review",
    "recording",
    "exact_file_reading",
    "web_research",
    "code_execution",
    "long_context",
}
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")


def load(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def valid_id(value) -> bool:
    return isinstance(value, str) and bool(ID_RE.fullmatch(value))


def nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def score(service: dict, role: str) -> tuple[int, str]:
    capability = ROLE_CAPABILITY[role]
    if service.get("availability") == "UNAVAILABLE" or not service.get("capabilities", {}).get(capability):
        return (-10_000, service.get("service_id", ""))
    value = (
        AVAILABILITY_SCORE[service["availability"]]
        + USAGE_SCORE[service["usage_preference"]]
        + COST_SCORE[service["cost_mode"]]
    )
    if role == "EVIDENCE_REVIEWER" and service.get("capabilities", {}).get("exact_file_reading"):
        value += 8
    if role == "FACILITATOR" and service.get("capabilities", {}).get("long_context"):
        value += 2
    return (value, service["service_id"])


def ranked_services(services: list[dict], role: str, assignment_counts: dict[str, int] | None = None) -> list[dict]:
    assignment_counts = assignment_counts or {}
    eligible = [item for item in services if score(item, role)[0] > -10_000]
    return sorted(
        eligible,
        key=lambda item: (
            -(score(item, role)[0] - 4 * assignment_counts.get(item["service_id"], 0)),
            item["service_id"],
        ),
    )


def correlated(a: dict, b: dict) -> bool:
    if a["service_id"] == b["service_id"]:
        return True
    if a["independence_group"] == b["independence_group"]:
        return True
    return (
        b["service_id"] in a.get("known_correlations", [])
        or a["service_id"] in b.get("known_correlations", [])
    )


def maximum_independent_subset(ranked: list[dict], limit: int) -> list[dict]:
    """Return the first maximum-cardinality pairwise-non-correlated subset.

    Candidate order is already deterministic. The depth-first search therefore
    preserves the earliest ranked solution when several maximum subsets exist.
    """
    target = min(limit, len(ranked))
    best: list[dict] = []

    def search(start: int, chosen: list[dict]) -> bool:
        nonlocal best
        if len(chosen) > len(best):
            best = list(chosen)
        if len(chosen) >= target:
            return True
        if len(chosen) + (len(ranked) - start) <= len(best):
            return False

        for index in range(start, len(ranked)):
            if len(chosen) + (len(ranked) - index) <= len(best):
                break
            candidate = ranked[index]
            if all(not correlated(candidate, existing) for existing in chosen):
                chosen.append(candidate)
                if search(index + 1, chosen):
                    return True
                chosen.pop()
        return False

    if target > 0:
        search(0, [])
    return best


def choose_blind_services(services: list[dict], count: int) -> tuple[list[dict], list[dict]]:
    ranked = ranked_services(services, "PROPOSER")
    independent_subset = maximum_independent_subset(ranked, count)
    selected = list(independent_subset)
    if len(selected) < count:
        for candidate in ranked:
            if len(selected) >= count:
                break
            if candidate not in selected:
                selected.append(candidate)
    return selected, independent_subset


def validate_input(document: dict) -> list[str]:
    problems: list[str] = []
    if not isinstance(document, dict):
        return ["input must be a mapping"]
    if not valid_id(document.get("plan_id")):
        problems.append("plan_id must be a valid identifier")

    task = document.get("task")
    services = document.get("services")
    if not isinstance(task, dict):
        problems.append("task is required")
    else:
        if not valid_id(task.get("task_id")):
            problems.append("task.task_id must be a valid identifier")
        if not nonempty_string(task.get("title")):
            problems.append("task.title must be a non-empty string")
        roles = task.get("required_roles")
        if not isinstance(roles, list) or not roles:
            problems.append("task.required_roles must be a non-empty list")
        else:
            if any(not isinstance(role, str) for role in roles):
                problems.append("task.required_roles must contain strings")
            unknown_roles = set(role for role in roles if isinstance(role, str)) - set(ROLE_CAPABILITY)
            if unknown_roles:
                problems.append(f"unknown required roles: {sorted(unknown_roles)}")
            if len(roles) != len(set(role for role in roles if isinstance(role, str))):
                problems.append("duplicate required role")
        blind_required = task.get("blind_first_round_required")
        if not isinstance(blind_required, bool):
            problems.append("blind_first_round_required must be boolean")
        count = task.get("blind_initial_response_count")
        if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= 10:
            problems.append("blind_initial_response_count must be an integer from 0 to 10")
        elif blind_required is True and count < 2:
            problems.append("blind_first_round_required needs at least two initial responses")
        elif blind_required is False and count != 0:
            problems.append("blind_initial_response_count must be zero when Blind First Round is not required")

    if not isinstance(services, list) or not services:
        problems.append("services must be a non-empty list")
        return problems

    service_ids: list[str] = []
    for index, item in enumerate(services):
        if not isinstance(item, dict):
            problems.append(f"service at index {index} must be a mapping")
            continue
        service_id = item.get("service_id")
        if not valid_id(service_id):
            problems.append(f"service at index {index} requires a valid service_id")
        else:
            service_ids.append(service_id)

    if len(service_ids) != len(set(service_ids)):
        problems.append("duplicate service_id")
    service_set = set(service_ids)

    for index, item in enumerate(services):
        if not isinstance(item, dict):
            continue
        service_id = item.get("service_id", f"index-{index}")
        for key in ("provider", "model_label"):
            if not nonempty_string(item.get(key)):
                problems.append(f"service {service_id} requires non-empty {key}")
        for key in ("chat_context_id", "independence_group"):
            if not valid_id(item.get(key)):
                problems.append(f"service {service_id} requires valid {key}")
        if item.get("availability") not in AVAILABILITY_SCORE:
            problems.append(f"service {service_id} has invalid availability")
        if item.get("usage_preference") not in USAGE_SCORE:
            problems.append(f"service {service_id} has invalid usage_preference")
        if item.get("cost_mode") not in COST_SCORE:
            problems.append(f"service {service_id} has invalid cost_mode")

        capabilities = item.get("capabilities")
        if not isinstance(capabilities, dict) or set(capabilities) != CAPABILITY_KEYS:
            problems.append(f"service {service_id} capability set mismatch")
        elif any(not isinstance(value, bool) for value in capabilities.values()):
            problems.append(f"service {service_id} capabilities must be boolean")

        correlations = item.get("known_correlations")
        if not isinstance(correlations, list):
            problems.append(f"service {service_id} known_correlations must be a list")
            continue
        if any(not valid_id(value) for value in correlations):
            problems.append(f"service {service_id} has invalid correlation identifier")
            continue
        if len(correlations) != len(set(correlations)):
            problems.append(f"service {service_id} has duplicate correlations")
        unknown = set(correlations) - service_set
        if unknown:
            problems.append(f"service {service_id} references unknown correlations: {sorted(unknown)}")
        if service_id in correlations:
            problems.append(f"service {service_id} must not correlate with itself")
    return problems


def build_plan(document: dict) -> dict:
    problems = validate_input(document)
    if problems:
        raise ValueError("; ".join(problems))
    task = document["task"]
    services = document["services"]
    assignments: list[dict] = []
    warnings: list[str] = []
    unfilled: list[str] = []
    assignment_counts: dict[str, int] = {}

    def record_assignment(row: dict) -> None:
        assignments.append(row)
        service_id = row["service_id"]
        assignment_counts[service_id] = assignment_counts.get(service_id, 0) + 1

    blind_selected: list[dict] = []
    blind_eligible: list[dict] = []
    if task["blind_first_round_required"]:
        blind_selected, blind_eligible = choose_blind_services(services, task["blind_initial_response_count"])
        for index, service in enumerate(blind_selected, 1):
            record_assignment({
                "assignment_id": f"ASSIGN-PROPOSER-{index}",
                "role": "PROPOSER",
                "service_id": service["service_id"],
                "phase": "BLIND_INITIAL",
                "authority": "PROPOSE_ONLY",
                "independent_count_eligible": service in blind_eligible,
                "rationale": "Selected deterministically for Blind First Round generation.",
            })
        if len(blind_selected) < task["blind_initial_response_count"]:
            warnings.append("Insufficient available generation-capable services for requested Blind First Round count.")
        if len(blind_eligible) < task["blind_initial_response_count"]:
            warnings.append("Blind First Round plan is correlated or lacks enough distinct eligible sources.")
    elif "PROPOSER" in task["required_roles"]:
        ranked = ranked_services(services, "PROPOSER")
        if ranked:
            service = ranked[0]
            record_assignment({
                "assignment_id": "ASSIGN-PROPOSER-1",
                "role": "PROPOSER",
                "service_id": service["service_id"],
                "phase": "ALL",
                "authority": "PROPOSE_ONLY",
                "independent_count_eligible": False,
                "rationale": "Selected deterministically for proposal generation.",
            })
        else:
            unfilled.append("PROPOSER")

    for role in task["required_roles"]:
        if role == "PROPOSER":
            if task["blind_first_round_required"] and not blind_selected:
                unfilled.append(role)
            continue
        ranked = ranked_services(services, role, assignment_counts)
        if not ranked:
            unfilled.append(role)
            continue
        service = ranked[0]
        record_assignment({
            "assignment_id": f"ASSIGN-{role}-1",
            "role": role,
            "service_id": service["service_id"],
            "phase": ROLE_PHASE[role],
            "authority": ROLE_AUTHORITY[role],
            "independent_count_eligible": False,
            "rationale": f"Selected deterministically for {role.lower().replace('_', ' ')} capability.",
        })

    if task["blind_first_round_required"]:
        blind_status = (
            "PLAN_VALID"
            if len(blind_selected) >= task["blind_initial_response_count"]
            and len(blind_eligible) >= task["blind_initial_response_count"]
            else "PLAN_DEGRADED"
        )
        blind_reasons = [] if blind_status == "PLAN_VALID" else list(warnings)
    else:
        blind_status = "NOT_REQUIRED"
        blind_reasons = []

    if unfilled:
        status = "DRAFT"
    elif blind_status == "PLAN_DEGRADED":
        status = "DEGRADED"
    else:
        status = "READY"

    return {
        "plan_version": PLAN_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "plan_id": document["plan_id"],
        "status": status,
        "formal_release_evidence": False,
        "human_final_authority": True,
        "approval_authority_granted": False,
        "task": task,
        "services": services,
        "assignments": assignments,
        "blind_first_round": {
            "required": task["blind_first_round_required"],
            "status": blind_status,
            "requested_response_count": task["blind_initial_response_count"],
            "assigned_service_ids": [item["service_id"] for item in blind_selected],
            "eligible_service_ids": [item["service_id"] for item in blind_eligible],
            "independence_group_count": len({item["independence_group"] for item in blind_eligible}),
            "reasons": blind_reasons,
        },
        "unfilled_roles": sorted(set(unfilled)),
        "warnings": warnings,
        "planner": {
            "algorithm": "MADP-DYNAMIC-ROLE-PLANNER-v1",
            "deterministic": True,
            "tie_breaker": "SERVICE_ID_ASCENDING",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate deterministic MADP alpha.3 dynamic role plan")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        plan = build_plan(load(args.input))
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    print(f"generated dynamic role plan: {args.output} status={plan['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
