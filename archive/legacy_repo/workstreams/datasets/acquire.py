from pathlib import Path
import sys,json,hashlib,datetime
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'shared'))
from public_http import fetch
OUT=Path(__file__).resolve().parent; CACHE=ROOT/'private_cache'/'datasets';CACHE.mkdir(exist_ok=True)
def get(name,url,max_bytes=15000000):
 r=fetch(url,timeout=45,max_bytes=max_bytes,source='datasets')
 rec={'name':name,'url':url,'final_url':r.url,'request_id':r.request_id,'status':r.status,'error':r.error,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'cache_hit':r.cache_hit,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with (OUT/'acquisition_log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 if r.status==200 and not r.error: (CACHE/name).write_bytes(r.content)
 print(json.dumps(rec),flush=True)
 return r
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('name');p.add_argument('url');p.add_argument('--max-bytes',type=int,default=15000000);a=p.parse_args();get(a.name,a.url,a.max_bytes)
