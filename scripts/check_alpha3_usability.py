#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={'USAB-QUICK-001','USAB-RELAY-001','USAB-LIMITED-001','USAB-RECOVERY-001','USAB-TEAM-001','USAB-MINUTES-001','USAB-HELP-001'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--release',action='store_true'); args=ap.parse_args()
    scenarios=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/usability-scenarios.yaml').read_text())
    results=yaml.safe_load((ROOT/'docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml').read_text())
    problems=[]
    items=scenarios.get('scenarios',[]); ids={i.get('id') for i in items}
    if ids!=REQUIRED: problems.append(f'usability scenario IDs mismatch: {sorted(ids)}')
    for i in items:
        if not i.get('required_features') or not i.get('success_condition'): problems.append(f'incomplete usability scenario: {i.get("id")}')
    auto=results.get('automated_walkthrough',{})
    if auto.get('status')!='PASS' or auto.get('scenario_count')!=len(REQUIRED): problems.append('automated usability walkthrough incomplete')
    checks=auto.get('checks',{})
    if not checks or any(v!='PASS' for v in checks.values()): problems.append('automated usability checks not all PASS')
    manual=results.get('manual_trials',{})
    if args.release:
        if manual.get('status')!='PASS': problems.append('manual usability trials have not passed')
        metrics=manual.get('metrics',{})
        if (metrics.get('task_completion_rate') or 0)<0.90: problems.append('task completion rate below 90%')
        if metrics.get('critical_authority_errors')!=0: problems.append('critical authority errors must be zero')
        if metrics.get('unnecessary_user_pauses')!=0: problems.append('unnecessary user pauses must be zero')
        if (metrics.get('next_action_understood_rate') or 0)<0.90: problems.append('next-action understood rate below 90%')
        if (metrics.get('median_recovery_attempts') or 99)>1: problems.append('median recovery attempts exceeds one')
        if not manual.get('sign_off',{}).get('approved_by'): problems.append('manual usability sign-off missing')
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print('alpha.3 usability implementation checks: PASS' + (' (release gate)' if args.release else ' (automated gate)'))
    return 0
if __name__=='__main__': raise SystemExit(main())
