#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,re,sys,zipfile,yaml
SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help'];SCHEMAS=['deliberation','command','migration','session-portability']
BOOTSTRAPS=['load-protocol-from-github.md','quick-start.md','verified-start.md','invite-limited-participant.md','help.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frontmatter(path):
 text=path.read_text(encoding='utf-8');m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
 return yaml.safe_load(m.group(1)) if m else {}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('directory');ap.add_argument('--source-commit',required=True);a=ap.parse_args();d=Path(a.directory);p=[]
 req=['manifest.yaml','validation-evidence.yaml','complete-protocol-bundle.txt']+BOOTSTRAPS+[f'schemas/{x}.bundle.schema.yaml' for x in SCHEMAS]+[f'chatgpt-skills/{x}.zip' for x in SKILLS]+['chatgpt-skills/madp-skill-pack.zip']+[f'claude-project/.claude/skills/{x}/SKILL.md' for x in SKILLS]
 for r in req:
  if not (d/r).is_file():p.append(f'missing artifact: {r}')
 if (d/'manifest.yaml').is_file():
  m=yaml.safe_load((d/'manifest.yaml').read_text(encoding='utf-8'))
  if m.get('bundle_version')!='MADP-ALPHA3-BUNDLE-v3':p.append('manifest bundle version mismatch')
  if m.get('protocol_version')!='MADP-v0.3.0-alpha.3' or m.get('source_commit')!=a.source_commit:p.append('manifest provenance mismatch')
  if m.get('protocol_load_report_version')!='MADP-PROTOCOL-LOAD-REPORT-v1':p.append('manifest load report version mismatch')
  if m.get('required_protocol_source_count')!=len(m.get('files',[])):p.append('manifest protocol source count mismatch')
  if m.get('canonical_command_count')!=51 or m.get('command_registry_policy')!='ALPHA2_CANONICAL_SUPERSET':p.append('manifest command policy mismatch')
  if (d/'validation-evidence.yaml').is_file() and m.get('validation_evidence_sha256')!=sha(d/'validation-evidence.yaml'):p.append('evidence digest mismatch')
  b=(d/'complete-protocol-bundle.txt').read_text(encoding='utf-8') if (d/'complete-protocol-bundle.txt').is_file() else ''
  for f in m.get('files',[]):
   if f'BEGIN_FILE path={f["path"]}' not in b or f'END_FILE path={f["path"]}' not in b:p.append(f'bundle boundary missing: {f["path"]}')
  bootstrap_rows={x.get('path'):x for x in m.get('bootstrap_files',[])}
  if set(bootstrap_rows)!=set(BOOTSTRAPS):p.append('manifest bootstrap file set mismatch')
  for name,row in bootstrap_rows.items():
   q=d/name
   if q.is_file() and (row.get('sha256')!=sha(q) or row.get('bytes')!=q.stat().st_size):p.append(f'bootstrap provenance mismatch: {name}')
 loader=d/'load-protocol-from-github.md'
 if loader.is_file():
  data=frontmatter(loader);text=loader.read_text(encoding='utf-8')
  if data.get('bootstrap_role')!='PROTOCOL_LOADER' or data.get('protocol_version')!='MADP-v0.3.0-alpha.3':p.append('generated loader metadata mismatch')
  if data.get('commit_template')!=a.source_commit:p.append('generated loader commit mismatch')
  if '{{MADP_' in text:p.append('generated loader contains unresolved placeholder')
  if a.source_commit not in text:p.append('generated loader does not bind source commit')
 for name in ['quick-start.md','verified-start.md']:
  q=d/name
  if q.is_file():
   data=frontmatter(q);text=q.read_text(encoding='utf-8')
   if data.get('requires_protocol_load') is not True or data.get('required_load_status')!='COMPLETE':p.append(f'load gate metadata missing: {name}')
   if 'PROTOCOL_NOT_LOADED' not in text:p.append(f'load gate failure response missing: {name}')
 for s in SKILLS:
  cp=d/f'claude-project/.claude/skills/{s}/SKILL.md';zp=d/f'chatgpt-skills/{s}.zip'
  if cp.is_file() and zp.is_file():
   with zipfile.ZipFile(zp) as z:
    if z.read(f'{s}/SKILL.md')!=cp.read_bytes():p.append(f'ChatGPT/Claude Skill drift: {s}')
 if (d/'chatgpt-skills/madp-skill-pack.zip').is_file():
  with zipfile.ZipFile(d/'chatgpt-skills/madp-skill-pack.zip') as z:
   if set(z.namelist())!={f'{s}/SKILL.md' for s in SKILLS}:p.append('Skill pack set mismatch')
 for n in SCHEMAS:
  q=d/f'schemas/{n}.bundle.schema.yaml'
  if q.is_file():
   data=yaml.safe_load(q.read_text(encoding='utf-8'))
   def walk(x):
    if isinstance(x,dict):
     for k,v in x.items():
      if k=='$ref' and not str(v).startswith('#'):p.append(f'external ref in {q}: {v}')
      walk(v)
    elif isinstance(x,list):
     for v in x:walk(v)
   walk(data)
 if p:
  for x in p:print('FAIL:',x,file=sys.stderr)
  return 1
 print('generated alpha.3 release artifacts: PASS (commit-pinned loader, 4 schemas, 5 symmetric Skills, evidence bound)');return 0
if __name__=='__main__':raise SystemExit(main())