#!/usr/bin/env python3
"""Dry-run by default: move unchanged old-root files to a sibling backup.

After extracting the release with Replace All, this removes obsolete legacy root
copies. Only explicit known old paths with byte-identical old content qualify.
New release files, modified files, .git and unknown files are never moved.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8_388_608),b''):h.update(b)
 return h.hexdigest()
def main():
 if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--apply',action='store_true');args=ap.parse_args()
 active_file=ROOT/'manifests/release_files.jsonl'
 if not active_file.exists():raise SystemExit('Final release manifest missing. Do not migrate an unfinished release.')
 active={json.loads(s)['path'] for s in active_file.read_text(encoding='utf-8').splitlines() if s}
 old=json.loads((ROOT/'manifests/legacy_root_files.json').read_text(encoding='utf-8'))
 eligible=[];kept=[]
 for row in old:
  rel=row['path'];p=ROOT/rel
  if rel in active or '.git' in Path(rel).parts or not p.is_file():continue
  if p.is_symlink() or not p.resolve().is_relative_to(ROOT):kept.append(rel);continue
  if p.stat().st_size==row['size_bytes'] and sha(p)==row['sha256']:eligible.append(rel)
  else:kept.append(rel)
 backup=ROOT.parent/(ROOT.name+'_legacy_backup_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
 result=dict(mode='apply' if args.apply else 'dry-run',eligible_files=len(eligible),modified_or_unsafe_kept=kept,backup=str(backup),paths=eligible)
 if args.apply:
  backup.mkdir(exist_ok=False)
  for rel in eligible:
   out=backup/rel;out.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(ROOT/rel),out)
  (backup/'MIGRATION_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
