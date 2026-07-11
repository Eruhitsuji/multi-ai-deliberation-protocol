#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'USAB-QUICK-001','USAB-COMMAND-COMPAT-001','USAB-RELAY-001','USAB-LIMITED-001','USAB-RECOVERY-001','USAB-TEAM-001','USAB-MINUTES-001','USAB-HELP-001'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--release',action='store_true');a=ap.parse_args();problems=[]
    scenarios=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/usability-scenarios.yaml').read_text(encoding='utf-8'))
    results=yaml.safe_load((ROOT/'docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml').read_text(encoding='utf-8'))
    items=scenarios.get('scenarios',[]);ids={x.get('id') for x in items}
    if ids!=REQUIRED:problems.append(f'usability scenario IDs mismatch: {sorted(ids^REQUIRED)}')
    for x in items:
        if not x.get('required_features') or not x.get('success_condition'):problems.append(f'incomplete scenario: {x.get("id")}')
    auto=results.get('automated_walkthrough',{})
    if auto.get('status')!='PASS' or auto.get('scenario_count')!=len(REQUIRED):problems.append('automated walkthrough incomplete')
    if any(v!='PASS' for v in auto.get('checks',{}).values()):problems.append('automated checks not all PASS')
    manual=results.get('manual_trials',{})
    if a.release:
        m=manual.get('metrics',{})
        if manual.get('status')!='PASS':problems.append('manual trials not PASS')
        if (m.get('task_completion_rate') or 0)<.90:problems.append('task completion rate below 90%')
        if m.get('critical_authority_errors')!=0:problems.append('critical authority errors must be zero')
        if (m.get('next_action_understood_rate') or 0)<.90:problems.append('next-action understood rate below 90%')
        if (m.get('median_recovery_attempts') if m.get('median_recovery_attempts') is not None else 99)>1:problems.append('median recovery attempts exceeds one')
        eligible=m.get('eligible_workflow_transitions') or 0; pauses=m.get('unnecessary_user_pauses')
        if eligible<=0 or pauses is None:problems.append('pause denominator or count missing')
        else:
            calculated=pauses/eligible
            if abs(calculated-(m.get('unnecessary_pause_rate') if m.get('unnecessary_pause_rate') is not None else -1))>1e-9:problems.append('unnecessary pause rate does not match counts')
            if calculated>.05:problems.append('unnecessary pause rate exceeds 5%')
        if m.get('critical_unnecessary_pauses')!=0:problems.append('critical unnecessary pauses must be zero')
        if pauses and len(manual.get('pause_classification_records',[]))<pauses:problems.append('pause classification records incomplete')
        if not manual.get('sign_off',{}).get('approved_by'):problems.append('manual sign-off missing')
    if problems:
        for p in problems:print('FAIL:',p,file=sys.stderr)
        return 1
    print('alpha.3 usability checks: PASS'+(' (release)' if a.release else ' (automated)'));return 0
if __name__=='__main__':raise SystemExit(main())
