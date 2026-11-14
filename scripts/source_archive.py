#!/usr/bin/env python3
"""Verify original inputs or restore a bounded-file split original. Stdlib only."""
from __future__ import annotations
import argparse,hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for data in iter(lambda:f.read(8_388_608),b''):h.update(data)
 return h.hexdigest()
def entries():
 return [json.loads(line) for line in (ROOT/'manifests/source_inventory.jsonl').read_text(encoding='utf-8').splitlines() if line]
def safe(path):
 p=(ROOT/path).resolve()
 if not p.is_relative_to(ROOT):raise ValueError('Path outside repository')
 return p
def verify():
 seen=set();fail=[];count=0
 for row in entries():
  store=row['storage']
  key=json.dumps(store,sort_keys=True)
  if key in seen:continue
  seen.add(key);count+=1
  if store['kind']=='file':
   p=safe(store['path'])
   if not p.is_file() or p.stat().st_size!=row['size_bytes'] or digest(p)!=row['sha256']:fail.append(row['logical_path'])
  else:
   h=hashlib.sha256();n=0
   for part in store['parts']:
    p=safe(part['path'])
    if not p.is_file():fail.append(part['path']);continue
    if p.stat().st_size!=part['size_bytes'] or digest(p)!=part['sha256']:fail.append(part['path'])
    with p.open('rb') as f:
     for data in iter(lambda:f.read(8_388_608),b''):h.update(data);n+=len(data)
   if n!=row['size_bytes'] or h.hexdigest()!=row['sha256']:fail.append(row['logical_path'])
 result=dict(checked_unique_storages=count,failed=fail,passed=not fail)
 print(json.dumps(result,indent=2));return 0 if not fail else 1
def restore(logical):
 rows=[r for r in entries() if r['logical_path']==logical]
 if not rows:raise SystemExit('Logical path not found; inspect manifests/source_inventory.jsonl')
 row=rows[0];s=row['storage'];target=safe(Path('.restored')/logical)
 target.parent.mkdir(parents=True,exist_ok=True)
 if target.exists():
  if digest(target)==row['sha256']:print(target);return
  raise SystemExit('Existing restored file differs; move it before restoring')
 temp=target.with_name(target.name+'.partial')
 try:
  with temp.open('wb') as out:
   paths=[s['path']] if s['kind']=='file' else [x['path'] for x in s['parts']]
   for p in paths:
    with safe(p).open('rb') as src:shutil.copyfileobj(src,out)
  if temp.stat().st_size!=row['size_bytes'] or digest(temp)!=row['sha256']:raise ValueError('Reconstructed hash mismatch')
  temp.rename(target)
 finally:
  if temp.exists():temp.unlink()
 print(target)
def main():
 if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
 p=argparse.ArgumentParser(description=__doc__);s=p.add_subparsers(dest='command',required=True)
 s.add_parser('verify');r=s.add_parser('restore');r.add_argument('logical_path')
 a=p.parse_args();return verify() if a.command=='verify' else restore(a.logical_path)
if __name__=='__main__':sys.exit(main())
