#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,re,statistics,subprocess,sys,yaml

ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
REQUIRED={'USAB-QUICK-001','USAB-COMMAND-COMPAT-001','USAB-RELAY-001','USAB-LIMITED-001','USAB-RECOVERY-001','USAB-TEAM-001','USAB-MINUTES-001','USAB-HELP-001'}
LOAD_REPORT_VERSION='MADP-PROTOCOL-LOAD-REPORT-v2'
OFFICIAL_REPOSITORY='Eruhitsuji/multi-ai-deliberation-protocol'
ACCESS_METHODS={'RAW_URL','GITHUB_CONNECTOR','PROVIDED_TEXT','COMPLETE_BUNDLE','OTHER'}

def valid_commit(value): return isinstance(value,str) and re.fullmatch(r'[0-9a-fA-F]{40}',value) is not None
def valid_sha256(value): return isinstance(value,str) and re.fullmatch(r'[0-9a-f]{64}',value) is not None
def file_sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory_digest(paths): return hashlib.sha256(('\n'.join(paths)+'\n').encode('utf-8')).hexdigest()

def loader_config():
    text=(ROOT/'bootstrap/alpha3/load-protocol-from-github.md').read_text(encoding='utf-8')
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
    if not m: raise ValueError('loader frontmatter missing')
    return yaml.safe_load(m.group(1))

def sources_for(profile,cfg):
    rows=[]
    for set_name in cfg['load_profiles'][profile]['required_sets']:
        rows.extend(cfg['source_sets'][set_name])
    return rows

def current_commit():
    try:
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    except Exception:
        return None

def equal_number(actual,expected,tol=1e-12):
    return isinstance(actual,(int,float)) and abs(float(actual)-float(expected))<=tol

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--release',action='store_true')
    a=ap.parse_args()
    problems=[]
    scenarios=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/usability-scenarios.yaml').read_text(encoding='utf-8'))
    results=yaml.safe_load((ROOT/'docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml').read_text(encoding='utf-8'))
    items=scenarios.get('scenarios',[])
    ids={x.get('id') for x in items}
    if ids!=REQUIRED: problems.append(f'usability scenario IDs mismatch: {sorted(ids^REQUIRED)}')
    for item in items:
        if not item.get('required_features') or not item.get('success_condition'): problems.append(f'incomplete scenario: {item.get("id")}')
    auto=results.get('automated_walkthrough',{})
    if auto.get('status')!='PASS' or auto.get('scenario_count')!=len(REQUIRED): problems.append('automated walkthrough incomplete')
    if any(v!='PASS' for v in auto.get('checks',{}).values()): problems.append('automated checks not all PASS')

    manual=results.get('manual_trials',{})
    if manual.get('protocol_load_report_required') is not True or manual.get('required_load_report_version')!=LOAD_REPORT_VERSION:
        problems.append('manual trial protocol load requirement missing')
    if manual.get('required_load_profile')!='FIELD_TRIAL' or manual.get('required_provenance')!='HASH_VERIFIED':
        problems.append('manual trial assurance requirements missing')

    if a.release:
        cfg=loader_config()
        expected_sources=sources_for('FIELD_TRIAL',cfg)
        expected_digest=inventory_digest(expected_sources)
        if cfg.get('source_inventory_digests',{}).get('FIELD_TRIAL')!=expected_digest: problems.append('FIELD_TRIAL inventory digest mismatch')
        head=current_commit()
        if not valid_commit(head): problems.append('unable to resolve current repository commit')

        rows=manual.get('scenario_results',[])
        if manual.get('status')!='PASS': problems.append('manual trials not PASS')
        coverage={x.get('scenario_id') for x in rows}
        if not REQUIRED.issubset(coverage): problems.append(f'release trial results missing scenarios: {sorted(REQUIRED-coverage)}')
        if not rows: problems.append('release trial results missing')

        trial_ids=set(); composite=set(); task_values=[]; next_values=[]; recovery_values=[]
        eligible_total=0; unnecessary_total=0; authority_total=0; critical_pause_total=0

        for row in rows:
            trial_id=row.get('trial_id'); participant=row.get('participant_id'); run_index=row.get('run_index'); scenario_id=row.get('scenario_id')
            label=trial_id or scenario_id or 'UNKNOWN'
            if not isinstance(trial_id,str) or not trial_id.strip(): problems.append(f'missing trial_id: {label}')
            elif trial_id in trial_ids: problems.append(f'duplicate trial_id: {trial_id}')
            else: trial_ids.add(trial_id)
            key=(participant,run_index,scenario_id)
            if not participant or not isinstance(run_index,int) or run_index<1 or scenario_id not in REQUIRED:
                problems.append(f'invalid trial identity: {label}')
            elif key in composite: problems.append(f'duplicate participant/run/scenario: {label}')
            else: composite.add(key)

            tested=row.get('tested_commit')
            if not valid_commit(tested): problems.append(f'invalid tested commit: {label}')
            elif head and tested.lower()!=head.lower(): problems.append(f'trial commit is not current checked-out commit: {label}')

            report=row.get('protocol_load_report',{})
            if report.get('report_version')!=LOAD_REPORT_VERSION or report.get('protocol_version')!=VERSION:
                problems.append(f'invalid protocol load report version: {label}')
            if not report.get('report_id') or not isinstance(report.get('revision'),int) or report.get('revision',0)<1:
                problems.append(f'invalid report identity or revision: {label}')
            if report.get('active') is not True: problems.append(f'load report is not active: {label}')
            if report.get('load_profile')!='FIELD_TRIAL': problems.append(f'wrong load profile: {label}')
            if report.get('repository')!=OFFICIAL_REPOSITORY: problems.append(f'wrong repository: {label}')
            if report.get('repository_commit')!=tested: problems.append(f'protocol load report commit mismatch: {label}')
            if report.get('inventory_digest_algorithm')!='sha256-newline-paths-v1' or report.get('source_inventory_digest')!=expected_digest:
                problems.append(f'protocol inventory digest mismatch: {label}')
            if report.get('status')!='COMPLETE' or report.get('all_required_files_read') is not True or report.get('inferred_unread_content') is not False:
                problems.append(f'incomplete protocol load gate: {label}')
            if report.get('schema_validation_capability')!='EXECUTED' or report.get('schema_validation_executed') is not True:
                problems.append(f'schema validation not executed: {label}')
            if report.get('provenance_level')!='HASH_VERIFIED': problems.append(f'load provenance not hash verified: {label}')

            file_rows=report.get('files',[])
            file_paths=[x.get('path') for x in file_rows if isinstance(x,dict)]
            if file_paths!=expected_sources: problems.append(f'protocol file inventory/order mismatch: {label}')
            if len(file_paths)!=len(set(file_paths)): problems.append(f'duplicate protocol file record: {label}')
            for item in file_rows:
                if not isinstance(item,dict): problems.append(f'invalid file record: {label}'); continue
                path=item.get('path')
                if path not in expected_sources: continue
                if item.get('status')!='READ': problems.append(f'file not READ ({path}): {label}')
                if item.get('access_method') not in ACCESS_METHODS: problems.append(f'invalid access method ({path}): {label}')
                if not item.get('source_ref'): problems.append(f'missing source reference ({path}): {label}')
                observed=item.get('content_sha256')
                if not valid_sha256(observed): problems.append(f'invalid content hash ({path}): {label}')
                elif (ROOT/path).is_file() and observed!=file_sha(ROOT/path): problems.append(f'content hash mismatch ({path}): {label}')

            authorized={x.get('path'):x for x in report.get('authorized_start_profiles',[]) if isinstance(x,dict)}
            binding=row.get('start_profile_binding',{})
            profile_path=binding.get('path')
            if profile_path not in {'bootstrap/alpha3/quick-start.md','bootstrap/alpha3/verified-start.md'}:
                problems.append(f'invalid start profile path: {label}')
            auth=authorized.get(profile_path,{})
            if binding.get('repository')!=OFFICIAL_REPOSITORY or binding.get('repository_commit')!=tested:
                problems.append(f'start profile repository/commit mismatch: {label}')
            if binding.get('source_inventory_digest')!=expected_digest or not binding.get('source_ref'):
                problems.append(f'incomplete start profile binding: {label}')
            if auth.get('repository')!=OFFICIAL_REPOSITORY or auth.get('repository_commit')!=tested or not auth.get('source_ref'):
                problems.append(f'load report did not authorize selected profile: {label}')

            required_scalars={'task_completed':bool,'next_action_understood':bool,'recovery_attempts':int,'eligible_workflow_transitions':int,'unnecessary_user_pauses':int,'critical_authority_errors':int,'critical_unnecessary_pauses':int}
            bad=False
            for field,kind in required_scalars.items():
                value=row.get(field)
                if kind is bool:
                    if not isinstance(value,bool): problems.append(f'invalid {field}: {label}'); bad=True
                elif not isinstance(value,int) or value<0:
                    problems.append(f'invalid {field}: {label}'); bad=True
            if not bad:
                task_values.append(1 if row['task_completed'] else 0)
                next_values.append(1 if row['next_action_understood'] else 0)
                recovery_values.append(row['recovery_attempts'])
                eligible_total+=row['eligible_workflow_transitions']
                unnecessary_total+=row['unnecessary_user_pauses']
                authority_total+=row['critical_authority_errors']
                critical_pause_total+=row['critical_unnecessary_pauses']

        if rows and len(task_values)==len(rows):
            calculated={'trial_count':len(rows),'task_completion_rate':sum(task_values)/len(rows),'critical_authority_errors':authority_total,'eligible_workflow_transitions':eligible_total,'unnecessary_user_pauses':unnecessary_total,'unnecessary_pause_rate':unnecessary_total/eligible_total if eligible_total else None,'critical_unnecessary_pauses':critical_pause_total,'next_action_understood_rate':sum(next_values)/len(rows),'median_recovery_attempts':statistics.median(recovery_values)}
            stored=manual.get('metrics',{})
            for key,value in calculated.items():
                if value is None:
                    if stored.get(key) is not None: problems.append(f'metric mismatch: {key}')
                elif not equal_number(stored.get(key),value): problems.append(f'metric mismatch: {key}')
            if calculated['task_completion_rate']<.90: problems.append('task completion rate below 90%')
            if calculated['critical_authority_errors']!=0: problems.append('critical authority errors must be zero')
            if calculated['next_action_understood_rate']<.90: problems.append('next-action understood rate below 90%')
            if calculated['median_recovery_attempts']>1: problems.append('median recovery attempts exceeds one')
            if calculated['eligible_workflow_transitions']<=0: problems.append('pause denominator missing')
            elif calculated['unnecessary_pause_rate']>.05: problems.append('unnecessary pause rate exceeds 5%')
            if calculated['critical_unnecessary_pauses']!=0: problems.append('critical unnecessary pauses must be zero')
            if len(manual.get('pause_classification_records',[]))<unnecessary_total: problems.append('pause classification records incomplete')
        if not manual.get('sign_off',{}).get('approved_by'): problems.append('manual sign-off missing')

    if problems:
        for item in problems: print('FAIL:',item,file=sys.stderr)
        return 1
    print('alpha.3 usability checks: PASS'+(' (release, recomputed multi-run metrics)' if a.release else ' (automated)'))
    return 0

if __name__=='__main__': raise SystemExit(main())
