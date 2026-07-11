#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, re, shutil, zipfile, yaml
ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
LOADER_SOURCE=ROOT/'bootstrap/alpha3/load-protocol-from-github.md'
BOOTSTRAP_FILES=['load-protocol-from-github.md','quick-start.md','verified-start.md','invite-limited-participant.md','help.md']
SCHEMAS=['deliberation','command','migration','session-portability']
SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help']

def frontmatter(path:Path):
 text=path.read_text(encoding='utf-8');m=re.match(r'^---\n(.*?)\n---\n',text,re.S)
 if not m:raise ValueError(f'missing YAML frontmatter: {path}')
 data=yaml.safe_load(m.group(1))
 if not isinstance(data,dict):raise ValueError(f'invalid YAML frontmatter: {path}')
 return data

LOAD_SET=list(frontmatter(LOADER_SOURCE).get('required_sources',[]))

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def deterministic_zip(path:Path, entries:list[tuple[str,bytes]]):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(entries):
   info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
def generate(out:Path,repository:str,commit:str,evidence:Path):
 if len(commit)!=40 or any(c not in '0123456789abcdefABCDEF' for c in commit):raise ValueError('source commit must be 40 hexadecimal characters')
 if not LOAD_SET or len(LOAD_SET)!=len(set(LOAD_SET)):raise ValueError('loader required source set is empty or duplicated')
 missing=[x for x in LOAD_SET if not (ROOT/x).is_file()]
 if missing:raise FileNotFoundError('missing load-set files: '+', '.join(missing))
 if not evidence.is_file():raise FileNotFoundError('validation evidence manifest missing')
 ev=yaml.safe_load(evidence.read_text(encoding='utf-8'))
 if ev.get('repository_commit')!=commit or any(x.get('status')!='PASS' for x in ev.get('checks',[])):raise ValueError('validation evidence does not prove this commit')
 owner,repo=repository.split('/',1)
 out.mkdir(parents=True,exist_ok=True);(out/'schemas').mkdir(exist_ok=True);(out/'chatgpt-skills').mkdir(exist_ok=True);(out/'claude-project/.claude/skills').mkdir(parents=True,exist_ok=True)
 loader=LOADER_SOURCE.read_text(encoding='utf-8').replace('{{MADP_GITHUB_OWNER}}',owner).replace('{{MADP_GITHUB_REPOSITORY}}',repo).replace('{{MADP_COMMIT_SHA}}',commit)
 (out/'load-protocol-from-github.md').write_text(loader,encoding='utf-8')
 for name in ['quick-start.md','verified-start.md','invite-limited-participant.md','help.md']:shutil.copy2(ROOT/f'bootstrap/alpha3/{name}',out/name)
 files=[{'path':rel,'sha256':digest(ROOT/rel),'bytes':(ROOT/rel).stat().st_size} for rel in LOAD_SET]
 bootstrap_files=[{'path':name,'sha256':digest(out/name),'bytes':(out/name).stat().st_size} for name in BOOTSTRAP_FILES]
 manifest={'bundle_version':'MADP-ALPHA3-BUNDLE-v3','protocol_version':VERSION,'repository':repository,'source_commit':commit,'protocol_load_report_version':'MADP-PROTOCOL-LOAD-REPORT-v1','required_protocol_source_count':len(LOAD_SET),'command_registry_policy':'ALPHA2_CANONICAL_SUPERSET','canonical_command_count':51,'validation_evidence_sha256':digest(evidence),'files':files,'bootstrap_files':bootstrap_files}
 (out/'manifest.yaml').write_text(yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True),encoding='utf-8')
 shutil.copy2(evidence,out/'validation-evidence.yaml')
 parts=['BEGIN_MADP_BUNDLE_METADATA',yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True).rstrip(),'END_MADP_BUNDLE_METADATA']
 for rel in LOAD_SET:parts += [f'BEGIN_FILE path={rel}',(ROOT/rel).read_text(encoding='utf-8').rstrip(),f'END_FILE path={rel}']
 (out/'complete-protocol-bundle.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
 for name in SCHEMAS:
  src=ROOT/f'schemas/v0.3.0-alpha.3/{name}.schema.yaml';data=yaml.safe_load(src.read_text(encoding='utf-8'))
  def walk(x):
   if isinstance(x,dict):
    for k,v in x.items():
     if k=='$ref' and not str(v).startswith('#'):raise ValueError(f'external ref in {src}: {v}')
     walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(data);(out/f'schemas/{name}.bundle.schema.yaml').write_text(yaml.safe_dump(data,sort_keys=False,allow_unicode=True),encoding='utf-8')
 pack=[]
 for skill in SKILLS:
  data=(ROOT/f'skills/{skill}/SKILL.md').read_bytes();deterministic_zip(out/f'chatgpt-skills/{skill}.zip',[(f'{skill}/SKILL.md',data)]);pack.append((f'{skill}/SKILL.md',data))
  dest=out/f'claude-project/.claude/skills/{skill}';dest.mkdir(parents=True,exist_ok=True);(dest/'SKILL.md').write_bytes(data)
 deterministic_zip(out/'chatgpt-skills/madp-skill-pack.zip',pack)
 return manifest
def main():
 ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('--repository',default='Eruhitsuji/multi-ai-deliberation-protocol');ap.add_argument('--source-commit',required=True);ap.add_argument('--validation-evidence',required=True);a=ap.parse_args()
 try:m=generate(Path(a.output),a.repository,a.source_commit,Path(a.validation_evidence))
 except Exception as e:print('FAIL:',e);return 1
 print(f'alpha.3 release artifacts generated: {len(m["files"])} protocol sources, 5 bootstrap files, 5 Skills, 4 schemas');return 0
if __name__=='__main__':raise SystemExit(main())