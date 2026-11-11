"""Independent read-only check of raw release paths/hashes and CSV record units."""
import csv,json,hashlib,datetime
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];RAW=ROOT/'raw_licensed_data'
manifest=json.loads((RAW/'DATASET_SOURCE_MANIFEST.json').read_text());results=[]
for entry in manifest:
 p=RAW/entry['file'];r={'file':entry['file'],'exists':p.is_file(),'manifest_says_unmodified':entry.get('source_bytes_unmodified'),'license_label':entry.get('license')}
 if p.is_file():
  sha=hashlib.sha256()
  with p.open('rb') as f:
   for chunk in iter(lambda:f.read(1024*1024),b''):sha.update(chunk)
  r.update(bytes=p.stat().st_size,bytes_match=p.stat().st_size==entry['bytes'],sha256=sha.hexdigest(),sha256_matches=sha.hexdigest()==entry['sha256'])
  if p.suffix=='.csv':
   with p.open(encoding='utf-8-sig',newline='') as f:
    reader=csv.reader(f);header=next(reader);counts=[0,0]
    for row in reader:
     counts[0]+=1
     if len(row)!=len(header):counts[1]+=1
   r.update(csv_data_rows=counts[0],csv_columns=len(header),csv_bad_width_rows=counts[1],csv_header=header)
  elif p.suffix=='.json':
   try:json.load(p.open(encoding='utf8'));r['json_valid']=True
   except Exception:r['json_valid']=False
 results.append(r)
summary={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_entries':len(results),'all_files_exist':all(r['exists'] for r in results),'all_byte_counts_match':all(r.get('bytes_match') for r in results),'all_hashes_match':all(r.get('sha256_matches') for r in results),'csv_files_checked':sum('csv_data_rows' in r for r in results),'csv_bad_width_rows':sum(r.get('csv_bad_width_rows',0) for r in results),'new_network_requests':0,'human_validation':False,'rows_are_physical_source_file_views_not_independent_people':True,'files':results}
(OUT/'RAW_MANIFEST_QA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='files'},indent=2))
for r in results:
 if 'csv_data_rows' in r:print(r['file'],r['csv_data_rows'],r['csv_columns'],r['csv_bad_width_rows'])
