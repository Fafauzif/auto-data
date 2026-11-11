from pathlib import Path
import sys,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;CACHE=ROOT/'private_cache/extension_battery';CACHE.mkdir(exist_ok=True)
sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
def get(name,url,max_bytes=15000000):
 p=CACHE/name
 if p.exists():
  content=p.read_bytes();return content
 r=fetch(url,timeout=50,max_bytes=max_bytes,source='extension_battery')
 rec={'name':name,'url':url,'status':r.status,'request_id':r.request_id,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'error':r.error,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with (OUT/'acquisition_log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec),flush=True)
 if r.status==200:p.write_bytes(r.content)
 return r.content if r.status==200 else b''
if __name__=='__main__':
 for name,url in [('catalogue.html','https://data.mendeley.com/datasets/7vdkzpnjgj/2'),('folders.json','https://data.mendeley.com/public-api/datasets/7vdkzpnjgj/folders/2'),('root_files.json','https://data.mendeley.com/public-api/datasets/7vdkzpnjgj/files?folder_id=root&version=2&$start=0&$limit=1000')]:
  raw=get(name,url)
  if name.endswith('json') and raw:
   x=json.loads(raw);print(name,json.dumps(x)[:12000],flush=True)
