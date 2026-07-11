#!/usr/bin/env python3
from pathlib import Path
import hashlib,sys,yaml
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'docs/ja/v0.3.0-alpha.3/translation-manifest.yaml'
def git_blob_sha1(data:bytes):return hashlib.sha1(f'blob {len(data)}\0'.encode('ascii')+data).hexdigest()
def main():
 p=[];d=yaml.safe_load(MANIFEST.read_text(encoding='utf-8'))
 if d.get('protocol_version')!='MADP-v0.3.0-alpha.3':p.append('version mismatch')
 if d.get('hash_algorithm')!='git-blob-sha1':p.append('hash algorithm mismatch')
 if d.get('audit_scope')!='SOURCE_FRESHNESS_AND_REQUIRED_MARKERS':p.append('audit scope not explicit')
 if d.get('semantic_equivalence_verified') is not False:p.append('audit must not claim semantic equivalence')
 if len(d.get('limitations',[]))<2:p.append('audit limitations incomplete')
 entries=d.get('entries',[])
 if len(entries)<12:p.append('translation coverage incomplete')
 seen=set()
 for e in entries:
  if e.get('source') in seen:p.append(f"duplicate source: {e.get('source')}")
  seen.add(e.get('source'))
  s=ROOT/e['source'];t=ROOT/e['translation']
  if not s.is_file():p.append(f'missing source: {e["source"]}');continue
  if not t.is_file():p.append(f'missing translation: {e["translation"]}');continue
  if git_blob_sha1(s.read_bytes())!=e.get('source_git_blob_sha1'):p.append(f'stale translation source hash: {e["source"]}')
  if e.get('status')!='COMPLETE':p.append(f'translation incomplete: {e["translation"]}')
  text=t.read_text(encoding='utf-8')
  for marker in e.get('required_markers',[]):
   if marker not in text:p.append(f'missing required marker {marker!r}: {e["translation"]}')
 if p:
  for x in p:print('FAIL:',x,file=sys.stderr)
  return 1
 print(f'alpha.3 translation freshness/marker audit: PASS ({len(entries)} entries; semantic equivalence not asserted)');return 0
if __name__=='__main__':raise SystemExit(main())
