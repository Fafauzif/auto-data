#!/usr/bin/env python3
"""Preserve original research/session bytes in a private, bounded-file release tree.

Archives supplied during the chat are unpacked recursively, not nested into the
release. Their container hashes and individual member hashes remain indexed.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, shutil, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'integration_work/release_repo'
LIMIT = 90_000_000
CHUNK = 80_000_000

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(8_388_608),b''): h.update(block)
    return h.hexdigest()

class Builder:
    def __init__(self):
        self.rows=[];self.containers=[];self.byhash={};self.old=[]
        OUT.mkdir(parents=True,exist_ok=True)
        (OUT/'manifests').mkdir(exist_ok=True)
    def ingest(self,path,dest,kind,origin,force=False):
        path=Path(path); size=path.stat().st_size; digest=sha(path)
        row=dict(source_kind=kind,source_origin=str(origin),logical_path=str(dest),size_bytes=size,sha256=digest)
        if not force and digest in self.byhash:
            row['storage']=dict(self.byhash[digest]);row['deduplicated']=True
        else:
            target=OUT/dest;target.parent.mkdir(parents=True,exist_ok=True)
            if size>LIMIT:
                parts=[];folder=Path(str(target)+'.parts');folder.mkdir(exist_ok=True)
                with path.open('rb') as f:
                    i=1
                    while data:=f.read(CHUNK):
                        p=folder/f'part-{i:05d}.bin';p.write_bytes(data)
                        parts.append(dict(path=str(p.relative_to(OUT)),size_bytes=len(data),sha256=hashlib.sha256(data).hexdigest()));i+=1
                row['storage']=dict(kind='parts',parts=parts)
                (folder/'RESTORE.json').write_text(json.dumps(dict(original_logical_path=str(dest),original_size_bytes=size,original_sha256=digest,parts=parts),indent=2)+'\n',encoding='utf-8')
            else:
                shutil.copy2(path,target)
                row['storage']=dict(kind='file',path=str(target.relative_to(OUT)))
            self.byhash[digest]=row['storage']
            row['deduplicated']=False
        self.rows.append(row)
    def tree(self,path,prefix,kind,origin=None,force=False):
        path=Path(path)
        for f in sorted(path.rglob('*')):
            rel=f.relative_to(path)
            if not f.is_file() or '.git' in rel.parts or '__pycache__' in rel.parts:continue
            if f.is_symlink():
                raise ValueError(f'Unexpected symlink: {f}')
            self.ingest(f,Path(prefix)/rel,kind,origin or path,force=force)
    def archive(self,path,prefix,kind,origin=None,depth=0):
        if depth>6:raise ValueError('Unexpected deeply nested archive')
        path=Path(path)
        receipt=dict(source_origin=str(origin or path),size_bytes=path.stat().st_size,sha256=sha(path),members=[])
        with zipfile.ZipFile(path) as z:
            for entry in z.infolist():
                if entry.is_dir():continue
                relative=PurePosixPath(entry.filename)
                if relative.is_absolute() or '..' in relative.parts:raise ValueError(entry.filename)
                if '.git' in relative.parts or '__pycache__' in relative.parts:continue
                receipt['members'].append(dict(path=entry.filename,size_bytes=entry.file_size,crc32=f'{entry.CRC:08x}'))
                with tempfile.NamedTemporaryFile(suffix=Path(entry.filename).suffix) as tmp:
                    with z.open(entry) as src:
                        shutil.copyfileobj(src,tmp)
                    tmp.flush()
                    if entry.filename.lower().endswith('.zip') and zipfile.is_zipfile(tmp.name):
                        self.archive(tmp.name,Path(prefix)/(entry.filename+'.unpacked'),kind,str(origin or path)+'!/'+entry.filename,depth+1)
                    else:
                        self.ingest(tmp.name,Path(prefix)/Path(entry.filename),kind,str(origin or path)+'!/'+entry.filename)
        self.containers.append(receipt)
    def write(self):
        p=OUT/'manifests/source_inventory.jsonl'
        p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in self.rows),encoding='utf-8')
        (OUT/'manifests/archive_containers.json').write_text(json.dumps(self.containers,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (OUT/'manifests/legacy_root_files.json').write_text(json.dumps(self.old,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        summary=dict(source_records=len(self.rows),unique_source_hashes=len(self.byhash),original_byte_total=sum(r['size_bytes'] for r in self.rows),container_count=len(self.containers),parted_originals=[dict(logical_path=r['logical_path'],size_bytes=r['size_bytes'],sha256=r['sha256']) for r in self.rows if r['storage']['kind']=='parts' and not r['deduplicated']],private_distribution=True,max_individual_file_bytes=LIMIT)
        (OUT/'manifests/archive_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(summary,ensure_ascii=False,indent=2))

def main():
    global ROOT,OUT
    if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--workspace',type=Path,required=True,help='Historical intake workspace containing auto-data/, upload/ and session products')
    ap.add_argument('--output',type=Path,required=True,help='New release staging directory; do not use an existing completed release')
    ap.add_argument('--latest',type=Path);args=ap.parse_args()
    ROOT=args.workspace.resolve();OUT=args.output.resolve()
    if not (ROOT/'auto-data/READ_FIRST.md').is_file():raise SystemExit('Original intake workspace not found: auto-data/READ_FIRST.md missing')
    b=Builder()
    repo=ROOT/'auto-data'
    for f in sorted(repo.rglob('*')):
        rel=f.relative_to(repo)
        if not f.is_file() or '.git' in rel.parts:continue
        b.old.append(dict(path=rel.as_posix(),size_bytes=f.stat().st_size,sha256=sha(f)))
        b.ingest(f,Path('archive/legacy_repo')/rel,'legacy_repository',f'https://github.com/Fafauzif/auto-data@34498fe033ae4dcd1a52c8d2e039f870b00d08fe/{rel}',force=True)
    b.tree(ROOT/'upload','sources/session/uploads','chat_attachment')
    for folder in sorted(ROOT.glob('Auto2000_*')):
        if folder.is_dir():b.tree(folder,Path('archive/session_work_products')/folder.name,'session_work_product')
    for folder in ('analysis_followup','planning_audit'):
        for f in sorted((ROOT/folder).rglob('*')):
            if f.is_file() and f.suffix.lower()!='.zip':b.ingest(f,Path('archive/session_work_products')/folder/f.relative_to(ROOT/folder),'session_work_product',f)
    for f in sorted(ROOT.iterdir()):
        if f.is_file() and f.suffix.lower() in ('.py','.csv','.json','.txt','.md'):
            b.ingest(f,Path('archive/session_work_products/root')/f.name,'session_work_product',f)
    # Recover every member of all historical ZIPs; identical content is stored
    # once while preserving every original container/member relationship.
    archives=list(ROOT.glob('*.zip'))+list((ROOT/'analysis_followup').glob('*.zip'))+list((ROOT/'planning_audit').glob('*.zip'))
    for f in sorted(archives):b.archive(f,Path('sources/archive_members')/f.stem,'source_archive_member')
    if args.latest:
        b.archive(args.latest,'sources/geography_latest','latest_geography_source','https://filebin.net/auto2000-complete-bccbfeb359e64c/Auto2000_Keputusan_Lanjutan_Sumber_Lengkap.zip')
    for f in sorted((ROOT/'integration_work/intake').glob('*.json')):
        b.ingest(f,Path('sources/intake_receipts')/f.name,'source_receipt',f)
    b.write()

if __name__=='__main__':main()
