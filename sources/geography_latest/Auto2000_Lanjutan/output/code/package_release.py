from pathlib import Path
import shutil,zipfile,csv,json,hashlib,ast
ROOT=Path(__file__).resolve().parents[2];D=ROOT.parent/'insight_deliverables';D.mkdir(exist_ok=True);stage=D/'Auto2000_Lanjutan'
if stage.exists():shutil.rmtree(stage)
stage.mkdir()
def ignore(path,names):return [n for n in names if n=='__pycache__' or n.endswith('.pyc') or (Path(path).name=='review' and n.endswith('.png'))]
for folder in ['extracted','work','output','source_building_queries']:shutil.copytree(ROOT/folder,stage/folder,ignore=ignore)
for file in ['README.md','requirements.txt','ENVIRONMENT.txt']:shutil.copy2(ROOT/file,stage/file)
rows=[]
for p in sorted(stage.rglob('*')):
 if p.is_file() and p.name!='RELEASE_MANIFEST_SHA256.csv':rows.append({'path':str(p.relative_to(stage)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (stage/'RELEASE_MANIFEST_SHA256.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(rows)
zpath=D/'Auto2000_Keputusan_Lanjutan_Sumber_Lengkap.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(stage.rglob('*')):
  if p.is_file():z.write(p,arcname='Auto2000_Lanjutan/'+str(p.relative_to(stage)))
# Full CRC and independent extraction/hash checks, not just ZIP metadata.
check=D/'extraction_check'
if check.exists():shutil.rmtree(check)
with zipfile.ZipFile(zpath) as z:assert z.testzip() is None;z.extractall(check)
x=check/'Auto2000_Lanjutan'
for r in rows:
 p=x/r['path'];assert p.stat().st_size==r['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
for p in x.rglob('*.py'):ast.parse(p.read_text())
# The accepted report version must match the packaged file.
pdf=stage/'output/report/Auto2000_Keputusan_Cabang_dan_Layanan.pdf';expected='179d0bd510e135f4917ffbb8b42ec4cc5ccc9569b38e220fb887462ad7886d55';assert hashlib.sha256(pdf.read_bytes()).hexdigest()==expected
shutil.copy2(pdf,D/pdf.name)
# Lightweight decision/table/code pack for easy inspection, clearly not the complete source archive.
compact=D/'Auto2000_Keputusan_dan_Tabel_Ringkas.zip'
with zipfile.ZipFile(compact,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for folder in ['report','tables','figures','qa']:
  for p in (ROOT/'output'/folder).rglob('*'):
   if p.is_file():z.write(p,arcname='Keputusan_dan_Tabel/'+str(p.relative_to(ROOT/'output')))
 z.writestr('Keputusan_dan_Tabel/README.txt','Paket ringkas untuk membaca keputusan, tabel dan figur. Sumber mentah/kode lengkap berada pada Auto2000_Keputusan_Lanjutan_Sumber_Lengkap.zip. Paket ini bukan pengganti sumber lengkap.')
receipt={'files':len(rows)+1,'archive_bytes':zpath.stat().st_size,'archive_sha256':hashlib.sha256(zpath.read_bytes()).hexdigest(),'all_crc_pass':True,'extracted_hashes_pass':True,'pdf_sha256':expected,'full_building_queries_bytes':sum(p.stat().st_size for p in (stage/'source_building_queries').glob('*.parquet')),'compact_bytes':compact.stat().st_size}
(D/'RELEASE_RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
