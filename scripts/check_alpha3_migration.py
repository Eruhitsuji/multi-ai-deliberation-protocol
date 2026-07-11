#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
from jsonschema import Draft202012Validator
from migrate_v030_alpha2_to_alpha3 import migrate
ROOT=Path(__file__).resolve().parents[1]

def main():
    problems=[]
    schema=yaml.safe_load((ROOT/'schemas/v0.3.0-alpha.3/migration.schema.yaml').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema); validator=Draft202012Validator(schema)
    fixtures=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/migration-fixtures.yaml').read_text(encoding='utf-8'))
    for i,x in enumerate(fixtures.get('valid',[]),1):
        e=list(validator.iter_errors(x))
        if e: problems.append(f'valid migration fixture {i} failed: {e[0].message}')
    for i,x in enumerate(fixtures.get('invalid',[]),1):
        if not list(validator.iter_errors(x)): problems.append(f'invalid migration fixture {i} passed')
    transforms=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/migration-transformations.yaml').read_text(encoding='utf-8'))
    for case in transforms.get('cases',[]):
        out=migrate(case['source'],case['source_ref']); record={'migration_record':out['migration_record']}
        errors=list(validator.iter_errors(record))
        if errors: problems.append(f"{case['id']} record invalid: {errors[0].message}"); continue
        exp=case['expected']; rec=out['migration_record']
        if rec['migration_outcome']!=exp['outcome']: problems.append(f"{case['id']} outcome mismatch")
        if exp['outcome']=='SUCCESS':
            target=out['target_state']
            if target['session_id']!=exp['session_id'] or target['source_state_version']!=exp['source_state_version']: problems.append(f"{case['id']} lineage mismatch")
            if target['authority_boundary']!=exp['target_authority_boundary']: problems.append(f"{case['id']} authority escalation")
            if target['decisions']['DEC-001']['revision']!=exp['decision_revision']: problems.append(f"{case['id']} decision revision changed")
            original=[x['command'] for x in case['source']['command_history']]
            if original!=exp['preserved_commands']: problems.append(f"{case['id']} command names changed")
        else:
            reasons='; '.join(rec.get('failure_reasons',[]))
            if exp['reason_contains'] not in reasons: problems.append(f"{case['id']} missing failure reason")
            if rec['source_raw_preserved'] is not exp['source_raw_preserved'] or rec['rollback_available'] is not exp['rollback_available']: problems.append(f"{case['id']} preservation facts mismatch")
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print(f"MADP-v0.3.0-alpha.3 migration checks: PASS ({len(transforms['cases'])} transformations)")
    return 0
if __name__=='__main__': raise SystemExit(main())
