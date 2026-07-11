#!/usr/bin/env python3
from parse_command_v030_alpha3 import normalize

def assert_block(raw, command, alias=False, issued_by="USER"):
    result=normalize(raw, issued_by=issued_by)
    assert "command_block" in result, result
    b=result["command_block"]
    assert b["command"]==command and b["alias_used"] is alias and b["validation_status"]=="SCHEMA_VALID", b
    return b

def main():
    assert_block('/madp status', 'status', False)
    assert_block('/madp resume', 'resume', False)
    assert_block('/madp pause', 'pause', False)
    assert_block('/madp start --session_id SESSION-001 --deliberation_plan PLAN-001', 'session-start', True)
    assert_block('/madp session-status --session_id SESSION-001', 'session-status', False)
    assert_block('/madp session-resume --session_id SESSION-001 --expected_state_version 1', 'session-resume', False)
    assert_block('/madp help-exit --help_request_id HELP-001 --source_state_version 1', 'help-exit', False)
    assert_block('MADP_COMMAND:\n  command: save\n  arguments:\n    session_export_request: EXPORT-001\n', 'session-export', True)
    assert "command_parse_error" in normalize('/madp unknown')
    assert "command_needs_arguments" in normalize('/madp approve --decision DEC-001', issued_by='USER')
    assert "command_parse_error" in normalize('/madp goal-confirm --plan_id PLAN-001 --revision 0 --source_state_version 1', issued_by='USER')
    print('MADP-v0.3.0-alpha.3 command parser tests: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
