#!/usr/bin/env python3
from pathlib import Path
import sys, yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

def main():
    schema=yaml.safe_load((ROOT/'schemas/v0.3.0-alpha.3/migration.schema.yaml').read_text())
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema)
    data=yaml.safe_load((ROOT/'tests/v0.3.0-alpha.3/migration-fixtures.yaml').read_text())
    problems=[]
    for i,case in enumerate(data.get('valid',[]),1):
        errs=list(validator.iter_errors(case))
        if errs: problems.append(f'valid migration {i} failed: {errs[0].message}')
        else:
            r=case['migration_record']
            if r['authority_escalated'] or r['user_approval_inferred'] or not r['source_raw_preserved']:
                problems.append(f'valid migration {i} violates invariants')
    for i,case in enumerate(data.get('invalid',[]),1):
        if not list(validator.iter_errors(case)): problems.append(f'invalid migration {i} unexpectedly passed')
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print('alpha.2 to alpha.3 migration fixtures: PASS')
    return 0
if __name__=='__main__': raise SystemExit(main())
