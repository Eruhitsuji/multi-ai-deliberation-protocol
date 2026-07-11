#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, yaml
ROOT=Path(__file__).resolve().parents[1]
KNOWN={'A3-REL-001','A3-REL-002','A3-REL-003','A3-REL-004','A3-REL-005'}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--allow-blockers',default=''); ap.add_argument('--require-main',action='store_true'); args=ap.parse_args()
    allow={x for x in args.allow_blockers.split(',') if x}
    problems=[]
    status=yaml.safe_load((ROOT/'docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml').read_text())
    if status.get('protocol_version')!='MADP-v0.3.0-alpha.3': problems.append('protocol version mismatch')
    if status.get('implementation_status')!='RELEASE_CANDIDATE_CONTENT_READY': problems.append('content is not release-candidate ready')
    checks=status.get('automated_checks',{})
    if not checks or any(v!='DONE' for v in checks.values()): problems.append('automated checks not complete')
    blockers={x['id']:x['status'] for x in status.get('release_blockers',[])}
    if set(blockers)!=KNOWN: problems.append('release blocker set mismatch')
    active={k for k,v in blockers.items() if v!='DONE'}
    if active!=allow: problems.append(f'unexpected active blockers: {sorted(active)} expected {sorted(allow)}')
    if args.require_main:
        if status.get('integration_status')!='MERGED_TO_MAIN': problems.append('final audit requires MERGED_TO_MAIN')
        if active: problems.append('final main audit has active blockers')
        if status.get('release_ready') is not True: problems.append('final main audit requires release_ready true')
    else:
        if status.get('integration_status')!='IMPLEMENTATION_BRANCH': problems.append('branch audit requires IMPLEMENTATION_BRANCH')
        if status.get('release_ready') is not False: problems.append('branch content must not claim release_ready')
    required=[
      'README-v0.3.0-alpha.3.md','README-v0.3.0-alpha.3.ja.md','protocol/MADP-v0.3.0-alpha.3.md','protocol/GLOSSARY-v0.3.0-alpha.3.md',
      'schemas/v0.3.0-alpha.3/deliberation.schema.yaml','schemas/v0.3.0-alpha.3/command.schema.yaml','schemas/v0.3.0-alpha.3/migration.schema.yaml',
      'registries/v0.3.0-alpha.3/commands.yaml','docs/ja/v0.3.0-alpha.3/translation-manifest.yaml','docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md',
      'docs/evaluation/MADP-v0.3.0-alpha.3-usability-results.yaml','scripts/generate_alpha3_release_artifacts.py'
    ]
    for p in required:
        if not (ROOT/p).is_file(): problems.append(f'missing release file: {p}')
    if problems:
        for p in problems: print('FAIL:',p,file=sys.stderr)
        return 1
    print('MADP-v0.3.0-alpha.3 release audit: PASS' + (' (final main)' if args.require_main else f' (branch; allowed blockers={sorted(allow)})'))
    return 0
if __name__=='__main__': raise SystemExit(main())
