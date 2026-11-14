from pathlib import Path
import sqlite3,hashlib,json,zipfile,sys,datetime
ROOT=Path(__file__).resolve().parents[1]
mode=sys.argv[1] if len(sys.argv)>1 else 'checkpoint'
if mode not in ('checkpoint','final','public','public_core'):raise ValueError('mode must be checkpoint, final, public or public_core')
output=ROOT.parent/({'checkpoint':'Auto2000_Research_Checkpoint_01.zip','final':'Auto2000_Research_Project_Full.zip','public':'Auto2000_Research_Public_Backup.zip','public_core':'Auto2000_Public_Backup_Core.zip'}[mode])
public_variant=mode.startswith('public')
withheld={'raw_licensed_data/IGAR_CC_BY_4_0/Rating_labeled.csv','raw_licensed_data/IGAR_CC_BY_4_0/VADER_labeled.csv'}
# Coherent SQLite snapshot; never copy a live WAL database without backup.
snap=ROOT/'checkpoints/site_evidence_snapshot.sqlite'
source=sqlite3.connect(ROOT/'data/site_evidence.sqlite');dest=sqlite3.connect(snap);source.backup(dest);dest.close();source.close()
manifest=[]
files=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file() or any(x in p.parts for x in ['private_cache','__pycache__','rendered']):continue
 rel=p.relative_to(ROOT)
 if public_variant and str(rel) in withheld:continue
 if mode=='public_core' and p.suffix.lower()=='.mat':continue
 if str(rel) in ['data/site_evidence.sqlite','data/site_evidence.sqlite-wal','data/site_evidence.sqlite-shm','manifest.json'] or p.name.endswith(('-wal','-shm')):continue
 if p.suffix in ['.zip'] and 'previous_releases' not in p.parts:continue
 if p.name.startswith('.'):continue
 file_rel=Path('data/site_evidence.sqlite') if p==snap else rel
 files.append((p,file_rel));manifest.append({'path':str(file_rel),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
metadata={'release_mode':mode,'generated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':manifest,'private_cache_included':False,'licensed_raw_datasets_included':True,'scope':'research diagnosis option menu user selects','igar_original_raw_text_included':not public_variant,'withheld_original_paths':sorted(withheld) if public_variant else [],'telemetry_separate_volumes':mode=='public_core','note':'Raw licensed rows and derived representations count separately. The public mirror omits the two original IGAR text files; its README_PUBLIC_MIRROR.md overrides primary-release inclusion statements in reports and historical QA records. A public_core archive additionally distributes the five MAT files in separately checksummed telemetry ZIP volumes.' if public_variant else 'This is the primary release with original licensed IGAR files. It is intended for the requesting user; the public-host backup is a separately identified variant without those original text files.'}
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,rel in files:z.write(p,'Auto2000_Research_Project/'+str(rel))
 z.writestr('Auto2000_Research_Project/manifest.json',json.dumps(metadata,indent=2))
with zipfile.ZipFile(output) as z:
 assert z.testzip() is None
 print(json.dumps({'file':str(output),'files':len(z.namelist()),'bytes':output.stat().st_size,'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}),flush=True)
