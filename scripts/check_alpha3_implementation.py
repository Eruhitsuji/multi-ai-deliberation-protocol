#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import re, runpy, sys, yaml
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
ALPHA2_EXPECTED={'share-context','issue-relay','request-review','summarize-state','check-authority','propose-decision','approve','reject','defer','prioritize','pause','resume','status','todo-add','todo-list','todo-update','todo-done','todo-defer','todo-promote','external-action'}
SCHEMAS={
 'deliberation':ROOT/'schemas/v0.3.0-alpha.3/deliberation.schema.yaml',
 'command':ROOT/'schemas/v0.3.0-alpha.3/command.schema.yaml',
 'migration':ROOT/'schemas/v0.3.0-alpha.3/migration.schema.yaml',
 'portability':ROOT/'schemas/v0.3.0-alpha.3/session-portability.schema.yaml'}
REQUIRED=[
 'LICENSE','README-v0.3.0-alpha.3.md','README-v0.3.0-alpha.3.ja.md','protocol/MADP-v0.3.0-alpha.3.md','protocol/GLOSSARY-v0.3.0-alpha.3.md',
 'docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md','docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md','docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md','docs/profiles/MADP_HELP-v0.3.0-alpha.3.md',
 'registries/v0.3.0-alpha.3/commands.yaml','tests/v0.3.0-alpha.3/fixtures.yaml','tests/v0.3.0-alpha.3/portability-fixtures.yaml','tests/v0.3.0-alpha.3/bootstrap-scenarios.yaml',
 'bootstrap/alpha3/load-protocol-from-github.md','bootstrap/alpha3/quick-start.md','bootstrap/alpha3/verified-start.md',
 'scripts/parse_command_v030_alpha3.py','scripts/apply_command_v030_alpha3.py','scripts/test_command_parser_v030_alpha3.py','scripts/check_all_commands_v030_alpha3.py','scripts/test_command_runtime_v030_alpha3.py',
 'scripts/run_alpha3_validation_evidence.py','docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml','docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml']
SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help']
BOOTSTRAP_SCENARIOS={'BOOT-LOAD-001','BOOT-GATE-MISSING-001','BOOT-GATE-INCOMPLETE-001'}

def semantic_errors(artifact):
 errors=[]
 plan=artifact.get('deliberation_plan') if isinstance(artifact,dict) else None
 if plan and plan.get('goal_status')=='USER_CONFIRMED' and plan.get('confirmed_revision')!=plan.get('revision'):errors.append('GOAL_CONFIRMED_REVISION_MISMATCH')
 pset=artifact.get('participant_profile_set') if isinstance(artifact,dict) else None
 if pset:
  identities={};ids=set()
  for p in pset.get('profiles',[]):
   if p.get('participant_id') in ids:errors.append('DUPLICATE_PARTICIPANT_ID')
   ids.add(p.get('participant_id'))
   if p.get('participant_type') in {'AI_MODEL','AI_ROLE_ACTOR'}:
    key=(p.get('model_provider'),p.get('model_label'),p.get('chat_context_id'))
    prior=identities.setdefault(key,p.get('independence_group'))
    if prior!=p.get('independence_group'):errors.append('SAME_MODEL_CHAT_DIFFERENT_INDEPENDENCE_GROUP')
 return errors

def parse_frontmatter(text):
 m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
 if not m:return None
 data=yaml.safe_load(m.group(1));return data if isinstance(data,dict) else None

def parse_skill_name(text):
 data=parse_frontmatter(text);return data.get('name') if data else None

def main():
 problems=[]
 for r in REQUIRED:
  if not (ROOT/r).is_file():problems.append(f'missing required file: {r}')
 licensep=ROOT/'LICENSE'
 if licensep.is_file() and not licensep.read_text(encoding='utf-8').startswith('MIT License\n'):
  problems.append('repository license must be MIT License')
 validators={}
 for name,path in SCHEMAS.items():
  try:
   schema=yaml.safe_load(path.read_text(encoding='utf-8'));Draft202012Validator.check_schema(schema);validators[name]=Draft202012Validator(schema)
  except Exception as e:problems.append(f'invalid {name} schema: {e}')
 fpath=ROOT/'tests/v0.3.0-alpha.3/fixtures.yaml'
 if fpath.is_file() and 'deliberation' in validators:
  f=yaml.safe_load(fpath.read_text(encoding='utf-8'))
  for i,c in enumerate(f.get('valid',[]),1):
   es=list(validators[c['schema']].iter_errors(c['artifact']))
   if es:problems.append(f'valid fixture {i} failed: {es[0].message}')
   sem=semantic_errors(c['artifact'])
   if sem:problems.append(f'valid fixture {i} semantic failure: {sem}')
  for i,c in enumerate(f.get('invalid',[]),1):
   if not list(validators[c['schema']].iter_errors(c['artifact'])):problems.append(f'invalid fixture {i} unexpectedly passed schema')
  for c in f.get('semantic_invalid',[]):
   schema_errors=list(validators['deliberation'].iter_errors(c['artifact']))
   if schema_errors:problems.append(f"semantic fixture {c['id']} should be schema-valid: {schema_errors[0].message}")
   elif c['expected_error'] not in semantic_errors(c['artifact']):problems.append(f"semantic fixture {c['id']} did not produce {c['expected_error']}")
 ppath=ROOT/'tests/v0.3.0-alpha.3/portability-fixtures.yaml'
 if ppath.is_file() and 'portability' in validators:
  f=yaml.safe_load(ppath.read_text(encoding='utf-8'))
  for i,x in enumerate(f.get('valid',[]),1):
   e=list(validators['portability'].iter_errors(x))
   if e:problems.append(f'valid portability fixture {i} failed: {e[0].message}')
  for i,x in enumerate(f.get('invalid',[]),1):
   if not list(validators['portability'].iter_errors(x)):problems.append(f'invalid portability fixture {i} passed')
 regpath=ROOT/'registries/v0.3.0-alpha.3/commands.yaml'
 if regpath.is_file():
  reg=yaml.safe_load(regpath.read_text(encoding='utf-8'));names=[x['command'] for x in reg.get('commands',[])];name_set=set(names)
  if reg.get('registry_version')!='MADP-COMMAND-REGISTRY-v0.2':problems.append('registry version must be v0.2 successor to alpha.2 v0.1')
  if len(names)!=51 or len(names)!=len(name_set):problems.append('alpha.3 registry must contain 51 unique canonical commands')
  if not ALPHA2_EXPECTED.issubset(name_set):problems.append(f'alpha.2 canonical commands missing: {sorted(ALPHA2_EXPECTED-name_set)}')
  aliases={x['alias']:x['command'] for x in reg.get('aliases',[])}
  collision=set(aliases)&name_set
  if collision:problems.append(f'alias/canonical collision: {sorted(collision)}')
  if {'status','resume','pause'}&set(aliases):problems.append('status/resume/pause must not be aliases')
  if reg.get('composition',{}).get('policy')!='ALPHA2_CANONICAL_SUPERSET':problems.append('command composition policy missing')
  enum=set(yaml.safe_load(SCHEMAS['command'].read_text(encoding='utf-8'))['properties']['command_block']['properties']['command']['enum'])
  if enum!=name_set:problems.append('command schema enum and registry differ')
 loaderp=ROOT/'bootstrap/alpha3/load-protocol-from-github.md'
 if loaderp.is_file():
  loader_text=loaderp.read_text(encoding='utf-8');loader=parse_frontmatter(loader_text) or {};sources=loader.get('required_sources',[])
  generated=runpy.run_path(str(ROOT/'scripts/generate_alpha3_release_artifacts.py'));load_set=generated.get('LOAD_SET',[])
  if loader.get('bootstrap_role')!='PROTOCOL_LOADER' or loader.get('protocol_version')!=VERSION:problems.append('alpha.3 loader metadata mismatch')
  if not sources or len(sources)!=len(set(sources)):problems.append('alpha.3 loader source set is empty or duplicated')
  if sources!=load_set:problems.append('alpha.3 loader source set and release generator load set differ')
  if any(not (ROOT/x).is_file() for x in sources):problems.append('alpha.3 loader references a missing source')
  for marker in ('PROTOCOL_LOAD_REPORT','MADP-PROTOCOL-LOAD-REPORT-v1','PROTOCOL_SOURCE_UNAVAILABLE','{{MADP_COMMIT_SHA}}','Do not substitute `main`'):
   if marker not in loader_text:problems.append(f'alpha.3 loader marker missing: {marker}')
 for name,mode in [('quick-start.md','QUICK'),('verified-start.md','VERIFIED')]:
  q=ROOT/f'bootstrap/alpha3/{name}'
  if q.is_file():
   text=q.read_text(encoding='utf-8');data=parse_frontmatter(text) or {}
   if data.get('protocol_version')!=VERSION or data.get('usage_mode')!=mode:problems.append(f'{name} metadata mismatch')
   if data.get('requires_protocol_load') is not True or data.get('required_load_report')!='PROTOCOL_LOAD_REPORT' or data.get('required_load_status')!='COMPLETE':problems.append(f'{name} load gate metadata mismatch')
   if data.get('required_loader')!='bootstrap/alpha3/load-protocol-from-github.md':problems.append(f'{name} loader path mismatch')
   if 'PROTOCOL_NOT_LOADED' not in text or 'do not start a session' not in text:problems.append(f'{name} fail-closed load gate missing')
 bsp=ROOT/'tests/v0.3.0-alpha.3/bootstrap-scenarios.yaml'
 if bsp.is_file():
  data=yaml.safe_load(bsp.read_text(encoding='utf-8'));items=data.get('scenarios',[]);ids={x.get('id') for x in items}
  if data.get('protocol_version')!=VERSION or ids!=BOOTSTRAP_SCENARIOS:problems.append('bootstrap scenario set mismatch')
  for x in items:
   if not x.get('input_condition') or not x.get('required_features') or not x.get('success_condition'):problems.append(f'incomplete bootstrap scenario: {x.get("id")}')
 for skill in SKILLS:
  sp=ROOT/f'skills/{skill}/SKILL.md';dp=ROOT/f'dist/chatgpt/{skill}-instructions.md'
  if not sp.is_file() or not dp.is_file():problems.append(f'missing symmetric skill adapter: {skill}');continue
  st=sp.read_text(encoding='utf-8');dt=dp.read_text(encoding='utf-8')
  if parse_skill_name(st)!=skill:problems.append(f'invalid Skill frontmatter: {skill}')
  if st!=dt:problems.append(f'ChatGPT adapter drift from canonical Skill: {skill}')
  if VERSION not in st:problems.append(f'Skill version missing: {skill}')
 statusp=ROOT/'docs/planning/MADP-v0.3.0-alpha.3-implementation-status.yaml'
 if statusp.is_file():
  status=yaml.safe_load(statusp.read_text(encoding='utf-8'));policy=status.get('validation_policy',{})
  if policy.get('self_attestation_is_release_evidence') is not False or policy.get('machine_generated_evidence_manifest_required') is not True:problems.append('status validation evidence policy is unsafe')
  if 'automated_checks' in status:problems.append('handwritten automated_checks DONE map is prohibited')
  integration=status.get('integration_status');evaluation=status.get('evaluation_status');release_ready=status.get('release_ready')
  if integration=='IMPLEMENTATION_BRANCH':
   if release_ready is not False:problems.append('implementation branch must not claim release_ready')
  elif integration=='MERGED_TO_MAIN':
   if release_ready is False and evaluation not in {'FIELD_TRIAL_IN_PROGRESS','FIELD_TRIAL_COMPLETE','FINAL_AUDIT_PENDING'}:problems.append('merged non-release state requires a field-trial or final-audit evaluation status')
   if release_ready is True and evaluation!='COMPLETE':problems.append('release-ready main state requires evaluation_status COMPLETE')
  else:problems.append('invalid integration_status')
 tracep=ROOT/'docs/planning/MADP-v0.3.0-alpha.3-traceability.yaml'
 if tracep.is_file():
  trace=yaml.safe_load(tracep.read_text(encoding='utf-8'));ids=[]
  for e in trace.get('requirements',[]):
   ids.append(e.get('id'))
   if e.get('status')!='IMPLEMENTED':problems.append(f"traceability not implemented: {e.get('id')}")
   for key in ('artifact','validation'):
    if not (ROOT/e.get(key,'')).is_file():problems.append(f"traceability {key} missing: {e.get('id')}")
  if len(ids)!=len(set(ids)) or len(ids)<14:problems.append('traceability IDs incomplete or duplicated')
 if problems:
  for p in problems:print('FAIL:',p,file=sys.stderr)
  return 1
 print(f'alpha.3 integrated implementation: PASS ({len(validators)} schemas, 51 commands, 5 symmetric Skills, protocol load gate)');return 0
if __name__=='__main__':raise SystemExit(main())