#!/usr/bin/env python3
"""Build a bounded-file replacement ZIP and SHA256 manifest from this repo."""
from pathlib import Path
import argparse,hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
IGNORE={'.git','.restored','__pycache__','.venv','node_modules','dist','release-build'}
CAP=90_000_000
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def files():
 for p in sorted(ROOT.rglob('*')):
  r=p.relative_to(ROOT)
  if any(x in IGNORE for x in r.parts) or not p.is_file():continue
  if p.is_symlink():raise ValueError('Do not ship symlinks: '+str(r))
  if p.stat().st_size>CAP:raise ValueError('File above90MB: '+str(r))
  yield p

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,default=ROOT.parent/'Auto2000_Complete_Private_Repository_2026-11-14.zip');ap.add_argument('--manifest-only',action='store_true');a=ap.parse_args()
 dest=a.output.resolve()
 if dest.is_relative_to(ROOT):raise SystemExit('Write delivery ZIP outside the repository')
 m=ROOT/'manifests/release_files.jsonl';rows=[]
 for p in files():
  if p==m:continue
  rows.append({'path':p.relative_to(ROOT).as_posix(),'size_bytes':p.stat().st_size,'sha256':sha(p)})
 m.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
 if a.manifest_only:print(json.dumps({'files':len(rows)+1,'manifest':str(m)}));return
 dest.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
  for p in files():z.write(p,p.relative_to(ROOT).as_posix())
 with zipfile.ZipFile(dest) as z:
  names=z.namelist();assert len(names)==len(set(names))
  assert len(names)==len(rows)+1
  for row in rows:
   h=hashlib.sha256()
   with z.open(row['path']) as f:
    for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
   if h.hexdigest()!=row['sha256']:raise ValueError('ZIPhashmismatch: '+row['path'])
 receipt={'file':dest.name,'size_bytes':dest.stat().st_size,'sha256':sha(dest),'members':len(names),'uncompressed_bytes':sum(r['size_bytes'] for r in rows)+m.stat().st_size,'largest_member_bytes':max(r['size_bytes'] for r in rows),'all_member_hashes_match':True,'member_cap_bytes':CAP,'zip_is_delivery_container_not_tracked_source':True}
 dest.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
