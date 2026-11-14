from pathlib import Path
import shutil,hashlib,csv,zipfile,json
R=Path(__file__).resolve().parents[1];out=R.parent/'deliverables';out.mkdir(exist_ok=True)
stage=out/'Auto2000_Geographic_Study';
if stage.exists():shutil.rmtree(stage)
def ignore(path,names):
 skips=[]
 for name in names:
  p=Path(path)/name
  if name in ['deps','__pycache__','test_cache','test_output','partial_completed2'] or name.endswith('_private.html') or name in ['surabaya_places.parquet','test_destinations.csv','test_config.json','test_overture.py','probe_overpass.osm.ch.json']:skips.append(name)
  elif name.startswith('overture_') and name.endswith('.py'):skips.append(name)
 return skips
shutil.copytree(R,stage,ignore=ignore)
rows=[]
for p in sorted(stage.rglob('*')):
 if p.is_file() and p.name!='MANIFEST_SHA256.csv':rows.append({'path':str(p.relative_to(stage)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
with (stage/'MANIFEST_SHA256.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(rows)
zip_path=out/'Auto2000_Geographic_Study.zip'
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(stage.rglob('*')):
  if p.is_file():z.write(p,arcname='Auto2000_Geographic_Study/'+str(p.relative_to(stage)))
# Verify CRC and extract into an independent check directory.
check=out/'extraction_check';
if check.exists():shutil.rmtree(check)
with zipfile.ZipFile(zip_path) as z:
 assert z.testzip() is None;z.extractall(check)
root=check/'Auto2000_Geographic_Study'
for row in rows:
 p=root/row['path'];assert p.stat().st_size==row['bytes'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
shutil.copy2(R/'report/Auto2000_Geographic_Workshop_Study.pdf',out/'Auto2000_Geographic_Workshop_Study.pdf')
receipt={'files':len(rows)+1,'zip_bytes':zip_path.stat().st_size,'zip_sha256':hashlib.sha256(zip_path.read_bytes()).hexdigest(),'crc_pass':True,'extracted_hashes_pass':True,'scope':'Relevant redistributable source extracts, results, figures, code and evidence; excluded dependencies/privateHTML/unrelated full-place data/test output'}
(out/'release_receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
