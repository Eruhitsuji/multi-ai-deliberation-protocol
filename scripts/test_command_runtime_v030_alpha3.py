#!/usr/bin/env python3
from apply_command_v030_alpha3 import execute, initial_state

def run(raw,state,issuer='USER',expect=None):
    r=execute(raw,state,issued_by=issuer)
    if expect: assert r['result']==expect,(raw,r['result'],r.get('message'))
    assert r['external_actions_performed'] is False
    return r

def main():
    s=initial_state()
    r=run('/madp status',s,'USER','REFERENCE_ONLY'); assert r['state_changed'] is False and r['state']==s
    r=run('/madp pause',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['workflow_status']=='PAUSED'
    r=run('/madp resume',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['workflow_status']=='ACTIVE'
    stale=run(f'/madp session-resume --session_id SESSION-001 --expected_state_version {s["state_version"]-1}',s,'USER','SESSION_REVISION_MISMATCH'); assert stale['state']==s
    r=run(f'/madp goal-confirm --plan_id PLAN-001 --revision 1 --source_state_version {s["state_version"]}',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['plans']['PLAN-001']['confirmed_revision']==1
    bad=run(f'/madp approve --decision DEC-001 --revision 2',s,'USER','APPROVAL_REVISION_MISMATCH'); assert bad['state']==s
    r=run('/madp approve --decision DEC-001 --revision 1',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['decisions']['DEC-001']['status']=='APPROVED'
    missing=run(f'/madp response-normalize --ingest_id ING-404 --source_state_version {s["state_version"]} --normalization_record NORM-001',s,'SYSTEM','INGEST_REQUIRED'); assert missing['state']==s
    r=run(f'/madp response-ingest --session_id SESSION-001 --source_state_version {s["state_version"]} --raw_response_ref artifact://raw/1 --participant_id AI-001',s,'SYSTEM','APPLIED_INTERNAL_STATE'); s=r['state']; iid=r['effect']['ingest_id']
    r=run(f'/madp response-normalize --ingest_id {iid} --source_state_version {s["state_version"]} --normalization_record NORM-001',s,'SYSTEM','APPLIED_INTERNAL_STATE'); s=r['state']
    r=run(f'/madp normalization-confirm --normalization_id NORM-001 --source_state_version {s["state_version"]} --status CONFIRMED',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['normalizations']['NORM-001']['status']=='CONFIRMED'
    before=s
    r=run('/madp minutes-generate --session_id SESSION-001 --source_state_version %d --detail_level STANDARD'%s['state_version'],s,'SYSTEM','APPLIED_INTERNAL_STATE'); s=r['state']; mid=r['effect']['minutes_id']
    rejected=run(f'/madp minutes-approve --minutes_id {mid} --revision 1',s,'USER','MINUTES_REVIEW_REQUIRED'); assert rejected['state']==s
    r=run(f'/madp minutes-review --minutes_id {mid} --revision 1 --review_status HUMAN_REVIEWED',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']
    r=run(f'/madp minutes-approve --minutes_id {mid} --revision 1',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['minutes'][mid]['status']=='APPROVED_RECORD'
    rejected=run('/madp session-import-confirm --import_id IMPORT-001 --report_revision 1 --selected_action CREATE_NEW_SESSION',s,'USER','IMPORT_REPORT_REQUIRED'); assert rejected['state']==s
    r=run('/madp session-import --source_file session.yaml',s,'SYSTEM','APPLIED_INTERNAL_STATE'); s=r['state']; imp=r['effect']
    bad=run(f'/madp session-import-confirm --import_id {imp["import_id"]} --report_revision 2 --selected_action CREATE_NEW_SESSION',s,'USER','IMPORT_REPORT_REVISION_MISMATCH'); assert bad['state']==s
    r=run(f'/madp session-import-confirm --import_id {imp["import_id"]} --report_revision 1 --selected_action CREATE_NEW_SESSION',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']
    r=run('/madp help --question next-action',s,'SYSTEM','HELP_ENTERED'); s=r['state']; hid=r['effect']['help_request_id']; assert s['phase']=='HELP'
    r=run(f'/madp help-exit --help_request_id {hid} --source_state_version {s["state_version"]}',s,'USER','APPLIED_INTERNAL_STATE'); s=r['state']; assert s['phase']=='DELIBERATION'
    denied=run('/madp external-action --action write-file --scope artifact.md',s,'USER','EXTERNAL_EXECUTION_NOT_IMPLEMENTED'); assert denied['state']==s
    denied=run('/madp approve --decision DEC-001 --revision 1',s,'FACILITATOR','CMD_AUTHORITY_DENIED'); assert denied['state']==s
    print('MADP-v0.3.0-alpha.3 command runtime sequencing tests: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
