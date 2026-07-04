from __future__ import annotations

import sys

from madp_validation import README_PATH, load_yaml_text, make_validator, read_markdown_code_fences, rel


def main() -> int:
    validator = make_validator()
    checked = 0
    for line, text in read_markdown_code_fences(README_PATH):
        data = load_yaml_text(text, f"{rel(README_PATH)}:{line}")
        if isinstance(data, dict) and "session_state" in data:
            validator.validate(data)
            checked += 1
            print(f"README SESSION_STATE example at line {line}: PASS")
    if checked == 0:
        print(f"{rel(README_PATH)}: no SESSION_STATE examples found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

