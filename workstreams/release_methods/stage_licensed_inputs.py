"""Stage already included licensed source CSVs for offline analyses. No network."""
from pathlib import Path
import shutil,hashlib,json,argparse
ROOT=Path(__file__).resolve().parents[2];RAW=ROOT/'raw_licensed_data';CACHE=ROOT/'private_cache'/'datasets'
SOURCES={
 'IGAR_CC_BY_4_0/Rating_labeled.csv':'Rating_labeled.csv',
 'IGAR_CC_BY_4_0/VADER_labeled.csv':'VADER_labeled.csv',
 'SPKLU_CC_BY_NC_3_0/data/spklu_stations.csv':'spklu_stations.csv',
 'SPKLU_CC_BY_NC_3_0/data/spklu_chargers.csv':'spklu_chargers.csv'}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return h.hexdigest()
a=argparse.ArgumentParser();a.add_argument('--dry-run',action='store_true');args=a.parse_args()
manifest={x['file']:x for x in json.loads((RAW/'DATASET_SOURCE_MANIFEST.json').read_text())};results=[]
for src,dst in SOURCES.items():
 source=RAW/src;target=CACHE/dst
 if not source.is_file():raise FileNotFoundError(str(source))
 expected=manifest[src]['sha256']
 if sha(source)!=expected:raise RuntimeError('Source hash mismatch: '+src)
 if args.dry_run:status='would_stage_or_reuse'
 else:
  CACHE.mkdir(parents=True,exist_ok=True)
  if target.exists() and sha(target)==expected:status='reused_matching_private_input'
  else:
   shutil.copyfile(source,target)
   if sha(target)!=expected:raise RuntimeError('Staged hash mismatch: '+dst)
   status='copied_verified_source_to_private_input'
 results.append({'source':src,'private_input_name':dst,'status':status,'bytes':source.stat().st_size})
print(json.dumps({'network_requests':0,'dry_run':args.dry_run,'inputs':results},indent=2))
