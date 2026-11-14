#!/usr/bin/env python3
"""Check exact release bytes and Git-friendly file bounds. Stdlib only."""
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=90_000_000
IGNORED={'.git','.restored','__pycache__','.venv','node_modules'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8_388_608),b''):h.update(b)
 return h.hexdigest()
def main():
 if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
 rows=[json.loads(s) for s in (ROOT/'manifests/release_files.jsonl').read_text(encoding='utf-8').splitlines() if s]
 errors=[]
 for r in rows:
  p=ROOT/r['path']
  if not p.is_file():errors.append(dict(path=r['path'],error='missing'));continue
  if p.stat().st_size!=r['size_bytes'] or sha(p)!=r['sha256']:errors.append(dict(path=r['path'],error='hash_or_size'))
 oversized=[];extra=[];expected={r['path'] for r in rows}|{'manifests/release_files.jsonl'}
 for p in ROOT.rglob('*'):
  rel=p.relative_to(ROOT)
  if any(x in IGNORED for x in rel.parts) or not p.is_file():continue
  if p.stat().st_size>MAX_BYTES:oversized.append(dict(path=str(rel),size_bytes=p.stat().st_size))
  if rel.as_posix() not in expected:extra.append(rel.as_posix())
 print(json.dumps(dict(checked=len(rows),hash_errors=errors,oversized=oversized,extra_files=extra,passed=not errors and not oversized),indent=2))
 return 1 if errors or oversized else 0
if __name__=='__main__':sys.exit(main())
