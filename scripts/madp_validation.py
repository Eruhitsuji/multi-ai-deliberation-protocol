from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "session-state-v0.2.5-draft.schema.yaml"
README_PATH = ROOT / "README.md"
PROTOCOL_PATH = ROOT / "protocol" / "MADP-v0.2.5-draft.md"
GLOSSARY_PATH = ROOT / "protocol" / "GLOSSARY-v0.2.5-draft.md"

CORE_PERMISSION_ACTIONS = {
    "READ_EXTERNAL",
    "SEND_EXTERNAL_DATA",
    "WRITE_FILE",
    "RUN_COMMAND",
    "COMMIT",
    "PUSH",
    "CREATE_PR",
    "SEND_MESSAGE",
    "MODIFY_EXTERNAL_RESOURCE",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_yaml_text(text: str, source: str = "<string>") -> Any:
    try:
        return yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise SystemExit(f"{source}: YAML parse failed: {exc}") from exc


def load_yaml(path: Path) -> Any:
    return load_yaml_text(path.read_text(encoding="utf-8"), rel(path))


def load_schema() -> dict[str, Any]:
    schema = load_yaml(SCHEMA_PATH)
    if not isinstance(schema, dict):
        raise SystemExit(f"{rel(SCHEMA_PATH)}: schema root must be a mapping")
    return schema


def make_validator(schema: dict[str, Any] | None = None) -> Draft202012Validator:
    schema = schema or load_schema()
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def iter_yaml_cases(directory: Path) -> Iterable[Path]:
    if not directory.exists():
        return []
    return (
        path
        for path in sorted(directory.glob("*.y*ml"))
        if not path.name.endswith(".expect.yaml") and not path.name.endswith(".expect.yml")
    )


def sidecar_path(case_path: Path) -> Path:
    return case_path.with_suffix(".expect.yaml")


def load_expected_code(case_path: Path) -> str:
    expected_path = sidecar_path(case_path)
    if not expected_path.exists():
        raise SystemExit(f"{rel(case_path)}: missing sidecar {rel(expected_path)}")
    data = load_yaml(expected_path)
    if not isinstance(data, dict) or not isinstance(data.get("error_code"), str):
        raise SystemExit(f"{rel(expected_path)}: expected mapping with string error_code")
    return data["error_code"]


def read_markdown_code_fences(path: Path, language: str = "yaml") -> Iterable[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"```(?:{language}|yml)\n(.*?)\n```", re.DOTALL)
    for match in pattern.finditer(text):
        line = text[: match.start()].count("\n") + 1
        yield line, match.group(1)


def schema_error_codes(error: ValidationError) -> set[str]:
    codes = {_schema_error_code(error)}
    for child in error.context:
        codes.update(schema_error_codes(child))
    return {code for code in codes if code}


def _schema_error_code(error: ValidationError) -> str:
    path = tuple(str(part) for part in error.absolute_path)
    message = error.message

    if error.validator == "required":
        if "operative_session_state_snapshot" in message:
            return "RELAY_SNAPSHOT_REQUIRED"
        if "user_confirmation" in message:
            return "CONDITION_USER_CONFIRMATION_REQUIRED"
        if "applicability_basis" in message:
            return "CONDITION_APPLICABILITY_BASIS_REQUIRED"
        if "basis" in message:
            return "CONDITION_BASIS_REQUIRED"
        if "reference" in message:
            return "APPROVAL_REFERENCE_REQUIRED"

    if error.validator == "enum" and path[-3:] == ("permission_requests", "0", "status"):
        return "INVALID_PERMISSION_REQUEST_STATUS"

    if error.validator == "enum" and path and path[-1] == "status" and "permission_requests" in path:
        return "INVALID_PERMISSION_REQUEST_STATUS"

    if error.validator == "maxContains" and path and path[-1] == "participants":
        return "MULTIPLE_ACTIVE_FACILITATORS"

    if error.validator in {"const", "not", "type"} and "next_step" in path and "user" in path:
        return "NEXT_STEP_USER_CONTRADICTION"

    if error.validator == "const" and path and path[-1] == "assurance_origin":
        return "INVALID_ASSURANCE_ORIGIN"

    return "SCHEMA_VALIDATION_ERROR"


@dataclass(frozen=True)
class SemanticError:
    code: str
    message: str
    path: str


def semantic_errors(instance: dict[str, Any]) -> list[SemanticError]:
    errors: list[SemanticError] = []
    state = instance.get("session_state")
    if isinstance(state, dict):
        errors.extend(_state_semantic_errors(state, "session_state"))

    relay = instance.get("relay_block")
    if isinstance(relay, dict):
        snapshot = relay.get("operative_session_state_snapshot")
        if isinstance(snapshot, dict):
            meta = snapshot.get("meta", {})
            if relay.get("session_id") != meta.get("session_id"):
                errors.append(
                    SemanticError(
                        "RELAY_SNAPSHOT_MISMATCH",
                        "relay_block.session_id differs from snapshot meta.session_id",
                        "relay_block.session_id",
                    )
                )
            if relay.get("source_state_version") != meta.get("state_version"):
                errors.append(
                    SemanticError(
                        "RELAY_SNAPSHOT_MISMATCH",
                        "relay_block.source_state_version differs from snapshot meta.state_version",
                        "relay_block.source_state_version",
                    )
                )
            errors.extend(_snapshot_semantic_errors(snapshot))

    return errors


def _snapshot_semantic_errors(snapshot: dict[str, Any]) -> list[SemanticError]:
    errors: list[SemanticError] = []
    participants = snapshot.get("participants", [])
    decisions = snapshot.get("decisions", [])
    errors.extend(_participant_errors(participants, "relay_block.operative_session_state_snapshot.participants"))
    errors.extend(_decision_errors(decisions, participants, "relay_block.operative_session_state_snapshot.decisions"))
    return errors


def _state_semantic_errors(state: dict[str, Any], path: str) -> list[SemanticError]:
    errors: list[SemanticError] = []
    participants = state.get("participants", [])
    decisions = state.get("decisions", [])
    errors.extend(_participant_errors(participants, f"{path}.participants"))
    errors.extend(_decision_errors(decisions, participants, f"{path}.decisions"))
    return errors


def _participant_errors(participants: Any, path: str) -> list[SemanticError]:
    if not isinstance(participants, list):
        return []
    active_facilitators = [
        participant
        for participant in participants
        if isinstance(participant, dict)
        and participant.get("role") == "FACILITATOR"
        and participant.get("status") == "ACTIVE"
    ]
    if len(active_facilitators) > 1:
        return [
            SemanticError(
                "MULTIPLE_ACTIVE_FACILITATORS",
                "more than one participant has role FACILITATOR and status ACTIVE",
                path,
            )
        ]
    return []


def _decision_errors(decisions: Any, participants: Any, path: str) -> list[SemanticError]:
    if not isinstance(decisions, list):
        return []
    participants_by_id = {
        participant.get("actor_id"): participant
        for participant in participants
        if isinstance(participant, dict) and participant.get("actor_id")
    }
    decisions_by_id = {
        decision.get("id"): decision
        for decision in decisions
        if isinstance(decision, dict) and decision.get("id")
    }
    errors: list[SemanticError] = []
    for index, decision in enumerate(decisions):
        if not isinstance(decision, dict):
            continue
        approval = decision.get("approval")
        if not isinstance(approval, dict):
            continue
        decision_path = f"{path}.{index}.approval"
        matching = decisions_by_id.get(approval.get("decision_id"))
        if matching is None or approval.get("decision_revision") != matching.get("revision"):
            errors.append(
                SemanticError(
                    "APPROVAL_REVISION_MISMATCH",
                    "approval is not bound to the matching current decision revision",
                    decision_path,
                )
            )
        recorded_by = approval.get("recorded_by")
        recorder = participants_by_id.get(recorded_by)
        if (
            isinstance(recorder, dict)
            and recorder.get("type") == "AI_PARTICIPANT"
            and approval.get("assurance_level") in {"USER_CONFIRMED", "EXTERNALLY_VERIFIED"}
        ):
            errors.append(
                SemanticError(
                    "INVALID_ASSURANCE_ORIGIN",
                    "AI participant recorded approval assurance above UNVERIFIED_ASSERTION",
                    decision_path,
                )
            )
    return errors
