from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from madp_validation import ROOT, load_expected_code, load_yaml_text, rel


PARTICIPANT_FIXTURE_DIR = ROOT / "tests" / "participant-response"
REQUIRED_FIELDS = {
    "participant_id",
    "role",
    "protocol_version",
    "source_state_version",
    "response_type",
    "authority_boundary",
    "claims",
    "findings",
    "state_change_proposals",
    "risks",
    "limitations",
}


def _line_fences(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("```")]


def _validate_text(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    yaml_open_count = sum(1 for line in stripped.splitlines() if line == "```yaml")
    if yaml_open_count > 1:
        return False, "PARTICIPANT_RESPONSE_MULTIPLE_YAML_FENCES"

    full = re.fullmatch(r"```yaml\n(.*)\n```", stripped, re.DOTALL)
    if not full:
        if "```yaml" in stripped:
            return False, "PARTICIPANT_RESPONSE_PROSE_AROUND_BLOCK"
        return False, "PARTICIPANT_RESPONSE_CODE_FENCE_REQUIRED"

    body = full.group(1)
    if any(line.startswith("```") for line in body.splitlines()):
        return False, "PARTICIPANT_RESPONSE_NESTED_CODE_FENCE"

    if len(_line_fences(stripped)) != 2:
        return False, "PARTICIPANT_RESPONSE_MULTIPLE_CODE_FENCES"

    try:
        data = load_yaml_text(body, "<participant-response>")
    except SystemExit:
        return False, "PARTICIPANT_RESPONSE_YAML_PARSE_ERROR"
    except yaml.YAMLError:
        return False, "PARTICIPANT_RESPONSE_YAML_PARSE_ERROR"

    if not isinstance(data, dict) or list(data.keys()) != ["PARTICIPANT_RESPONSE"]:
        return False, "PARTICIPANT_RESPONSE_TOP_LEVEL_KEY"

    response = data["PARTICIPANT_RESPONSE"]
    if not isinstance(response, dict):
        return False, "PARTICIPANT_RESPONSE_SHAPE_ERROR"
    missing = REQUIRED_FIELDS.difference(response)
    if missing:
        return False, "PARTICIPANT_RESPONSE_SHAPE_ERROR"
    if not isinstance(response.get("claims"), list):
        return False, "PARTICIPANT_RESPONSE_SHAPE_ERROR"

    return True, "PASS"


def _case_files(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted(path for path in directory.glob("*.md") if not path.name.endswith(".expect.md"))


def main() -> int:
    valid_cases = _case_files(PARTICIPANT_FIXTURE_DIR / "valid")
    invalid_cases = _case_files(PARTICIPANT_FIXTURE_DIR / "invalid")
    if not valid_cases:
        print("tests/participant-response/valid: no cases found", file=sys.stderr)
        return 1
    if not invalid_cases:
        print("tests/participant-response/invalid: no cases found", file=sys.stderr)
        return 1

    for case in valid_cases:
        ok, code = _validate_text(case.read_text(encoding="utf-8"))
        if not ok:
            print(f"{rel(case)}: expected PASS, got {code}", file=sys.stderr)
            return 1
        print(f"participant response valid: {rel(case)} PASS")

    for case in invalid_cases:
        ok, code = _validate_text(case.read_text(encoding="utf-8"))
        if ok:
            print(f"{rel(case)}: expected failure, got PASS", file=sys.stderr)
            return 1
        expected = load_expected_code(case)
        if code != expected:
            print(f"{rel(case)}: expected {expected}, got {code}", file=sys.stderr)
            return 1
        print(f"participant response invalid: {rel(case)} PASS ({expected})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
