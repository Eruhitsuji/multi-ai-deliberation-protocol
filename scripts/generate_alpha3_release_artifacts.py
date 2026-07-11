#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, shutil, zipfile, yaml
ROOT=Path(__file__).resolve().parents[1]
VERSION='MADP-v0.3.0-alpha.3'
LOAD_SET=[
 'README-v0.3.0-alpha.2.md','protocol/MADP-v0.3.0-alpha.2.md','protocol/GLOSSARY-v0.3.0-alpha.2.md','schemas/v0.3.0-alpha.2/command.schema.yaml','schemas/v0.3.0-alpha.2/command-registry.schema.yaml','schemas/v0.3.0-alpha.2/todo.schema.yaml','schemas/v0.3.0-alpha.2/context-package.schema.yaml','schemas/v0.3.0-alpha.2/context-package-receipt.schema.yaml','schemas/v0.3.0-alpha.2/review.schema.yaml','schemas/v0.3.0-alpha.2/relay.schema.yaml','registries/v0.3.0-alpha.2/commands.yaml','docs/profiles/AI_DRIVEN_DEVELOPMENT-v0.3.0-alpha.2.md',
 'README-v0.3.0-alpha.3.md','protocol/MADP-v0.3.0-alpha.3.md','protocol/GLOSSARY-v0.3.0-alpha.3.md',
 'schemas/v0.3.0-alpha.3/deliberation.schema.yaml','schemas/v0.3.0-alpha.3/command.schema.yaml','schemas/v0.3.0-alpha.3/migration.schema.yaml','schemas/v0.3.0-alpha.3/session-portability.schema.yaml',
 'registries/v0.3.0-alpha.3/commands.yaml','docs/profiles/COMMAND_SYSTEM-v0.3.0-alpha.3.md','docs/profiles/SESSION_PORTABILITY-v0.3.0-alpha.3.md','docs/profiles/SKILL_ADAPTERS-v0.3.0-alpha.3.md','docs/profiles/MADP_HELP-v0.3.0-alpha.3.md','docs/profiles/TEAM_DELIBERATION-v0.3.0-alpha.3.md','docs/profiles/MODEL_RESPONSE_COMPARISON-v0.3.0-alpha.3.md','docs/migration/MADP-v0.3.0-alpha.2-to-alpha.3.md',
 'skills/README.md','skills/madp-start/SKILL.md','skills/madp-facilitator/SKILL.md','skills/madp-participant/SKILL.md','skills/madp-recorder/SKILL.md','skills/madp-help/SKILL.md']
SCHEMAS=['deliberation','command','migration','session-portability']
SKILLS=['madp-start','madp-facilitator','madp-participant','madp-recorder','madp-help']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def deterministic_zip(path:Path, entries:list[tuple[str,bytes]]):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,data in sorted(entries):
   info=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,data)
def generate(out:Path,repository:str,commit:str,evidence:Path):
 if len(commit)!=40 or any(c not in '0123456789abcdefABCDEF' for c in commit):raise ValueError('source commit must be 40 hexadecimal characters')
 missing=[x for x in LOAD_SET if not (ROOT/x).is_file()]
 if missing:raise FileNotFoundError('missing load-set files: '+', '.join(missing))
 if not evidence.is_file():raise FileNotFoundError('validation evidence manifest missing')
 ev=yaml.safe_load(evidence.read_text(encoding='utf-8'))
 if ev.get('repository_commit')!=commit or any(x.get('status')!='PASS' for x in ev.get('checks',[])):raise ValueError('validation evidence does not prove this commit')
 out.mkdir(parents=True,exist_ok=True);(out/'schemas').mkdir(exist_ok=True);(out/'chatgpt-skills').mkdir(exist_ok=True);(out/'claude-project/.claude/skills').mkdir(parents=True,exist_ok=True)
 files=[{'path':rel,'sha256':digest(ROOT/rel),'bytes':(ROOT/rel).stat().st_size} for rel in LOAD_SET]
 manifest={'bundle_version':'MADP-ALPHA3-BUNDLE-v2','protocol_version':VERSION,'repository':repository,'source_commit':commit,'command_registry_policy':'ALPHA2_CANONICAL_SUPERSET','canonical_command_count':51,'validation_evidence_sha256':digest(evidence),'files':files}
 (out/'manifest.yaml').write_text(yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True),encoding='utf-8')
 shutil.copy2(evidence,out/'validation-evidence.yaml')
 parts=['BEGIN_MADP_BUNDLE_METADATA',yaml.safe_dump(manifest,sort_keys=False,allow_unicode=True).rstrip(),'END_MADP_BUNDLE_METADATA']
 for rel in LOAD_SET:parts += [f'BEGIN_FILE path={rel}',(ROOT/rel).read_text(encoding='utf-8').rstrip(),f'END_FILE path={rel}']
 (out/'complete-protocol-bundle.txt').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
 owner,repo=repository.split('/',1);rows=[]
 for rel in LOAD_SET:rows.append(f'- `{rel}`\n  https://raw.githubusercontent.com/{owner}/{repo}/{commit}/{rel}')
 verified='---\nbootstrap_version: 0.5\nprotocol_version: '+VERSION+'\nusage_mode: VERIFIED\nrepository_commit: '+commit+'\n---\n\n# Load MADP alpha.3 verified bundle\n\nRead every file below from this immutable commit and report READ, PARTIALLY_READ, or FAILED. Do not infer unread content.\n\n'+'\n'.join(rows)+'\n\nPreserve the alpha.2 canonical command namespace. Do not begin substantive deliberation until session, state revision, goal revision, authority, and validation limitations are explicit.\n'
 (out/'verified-start.md').write_text(verified,encoding='utf-8')
 for name in ['quick-start.md','invite-limited-participant.md','help.md']:shutil.copy2(ROOT/f'bootstrap/alpha3/{name}',out/name)
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
 print(f'alpha.3 release artifacts generated: {len(m["files"])} source files, 5 Skills, 4 schemas');return 0
if __name__=='__main__':raise SystemExit(main())
