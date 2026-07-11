#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,subprocess,sys,yaml
ROOT=Path(__file__).resolve().parents[1]
KNOWN={'A3-REL-001','A3-REL-002','A3-REL-003','A3-REL-004','A3-REL-005'}
REQUIRED_CHECKS={'A3-CHECK-IMPLEMENTATION','A3-CHECK-MIGRATION','A3-CHECK-TRANSLATION','A3-CHECK-USABILITY','A3-CHECK-PARSER','A3-CHECK-COMMAND-COVERAGE','A3-CHECK-RUNTIME'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tree_hashes(root):return {str(p.relative_to(root)).replace('\\','/'):sha(p) for p in sorted(root.rglob('*')) if p.is_file()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--evidence-manifest',required=True);ap.add_argument('--repository-commit',required=True);ap.add_argument('--release-directory-a',required=True);ap.add_argument('--release-directory-b',required=True);ap.add_argument('--allow-blockers',default='');ap.add_argument('--require-main',action='store_true');a=ap.parse_args();problems=[]
 allow={x for x in a.allow_blockers.split(',') if x};status=yaml.safe_load((ROOT/'docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml').read_text(encoding='utf-8'))
 if status.get('protocol_version')!='MADP-v0.3.0-alpha.3':problems.append('protocol version mismatch')
 if status.get('implementation_status')!='RELEASE_CANDIDATE_CONTENT_READY':problems.append('content status mismatch')
 policy=status.get('validation_policy',{})
 if policy.get('self_attestation_is_release_evidence') is not False or policy.get('machine_generated_evidence_manifest_required') is not True:problems.append('unsafe validation evidence policy')
 if 'automated_checks' in status:problems.append('handwritten automated_checks map cannot be release evidence')
 blockers={x['id']:x['status'] for x in status.get('release_blockers',[])}
 if set(blockers)!=KNOWN:problems.append('release blocker set mismatch')
 active={k for k,v in blockers.items() if v!='DONE'}
 if active!=allow:problems.append(f'unexpected active blockers: {sorted(active)} expected {sorted(allow)}')
 ep=Path(a.evidence_manifest)
 if not ep.is_file():problems.append('validation evidence manifest missing')
 else:
  ev=yaml.safe_load(ep.read_text(encoding='utf-8'))
  if ev.get('evidence_version')!='MADP-ALPHA3-VALIDATION-EVIDENCE-v1' or ev.get('self_attested') is not False:problems.append('invalid evidence format')
  if ev.get('repository_commit')!=a.repository_commit:problems.append('evidence commit mismatch')
  if bool(ev.get('release_mode'))!=bool(a.require_main):problems.append('evidence release mode mismatch')
  scope=ev.get('scope_sha256',{})
  if not scope:problems.append('evidence scope hash set missing')
  for rel,digest in scope.items():
   sp=ROOT/rel
   if not sp.is_file() or sha(sp)!=digest:problems.append(f'evidence scope hash mismatch: {rel}')
  rows={x.get('id'):x for x in ev.get('checks',[])}
  if set(rows)!=REQUIRED_CHECKS:problems.append('evidence check set mismatch')
  for cid,row in rows.items():
   cp=ROOT/row.get('checker_path','')
   if row.get('status')!='PASS' or row.get('return_code')!=0:problems.append(f'evidence check failed: {cid}')
   if not cp.is_file() or sha(cp)!=row.get('checker_sha256'):problems.append(f'checker hash mismatch: {cid}')
   if hashlib.sha256((row.get('stdout') or '').encode()).hexdigest()!=row.get('stdout_sha256'):problems.append(f'stdout evidence hash mismatch: {cid}')
   if hashlib.sha256((row.get('stderr') or '').encode()).hexdigest()!=row.get('stderr_sha256'):problems.append(f'stderr evidence hash mismatch: {cid}')
   for rel,digest in row.get('input_sha256',{}).items():
    p=ROOT/rel
    if not p.is_file() or sha(p)!=digest:problems.append(f'input hash mismatch: {cid}:{rel}')
 da,db=Path(a.release_directory_a),Path(a.release_directory_b)
 if not da.is_dir() or not db.is_dir():problems.append('both generated release directories are required')
 else:
  if tree_hashes(da)!=tree_hashes(db):problems.append('release artifact generation is not reproducible')
  bound=da/'validation-evidence.yaml'
  if not bound.is_file() or not ep.is_file() or sha(bound)!=sha(ep):problems.append('release artifact is not bound to supplied evidence')
  proc=subprocess.run([sys.executable,str(ROOT/'scripts/check_generated_alpha3_release_artifacts.py'),str(da),'--source-commit',a.repository_commit],cwd=ROOT,text=True,capture_output=True)
  if proc.returncode!=0:problems.append('generated artifact validation failed: '+(proc.stderr.strip() or proc.stdout.strip()))
 if a.require_main:
  if status.get('integration_status')!='MERGED_TO_MAIN':problems.append('final audit requires MERGED_TO_MAIN')
  if active:problems.append('final audit cannot have blockers')
  if status.get('release_ready') is not True:problems.append('final audit requires release_ready true')
 else:
  if status.get('integration_status')!='IMPLEMENTATION_BRANCH':problems.append('branch audit requires IMPLEMENTATION_BRANCH')
  if status.get('release_ready') is not False:problems.append('branch must not claim release_ready')
 if problems:
  for p in problems:print('FAIL:',p,file=sys.stderr)
  return 1
 print('MADP-v0.3.0-alpha.3 evidence-backed release audit: PASS'+(' (final main)' if a.require_main else f' (branch; blockers={sorted(allow)})'));return 0
if __name__=='__main__':raise SystemExit(main())
