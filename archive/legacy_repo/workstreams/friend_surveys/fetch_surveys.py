from pathlib import Path
import sys,json,datetime,hashlib
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
OUT=Path(__file__).resolve().parent;CACHE=ROOT/'private_cache/friend_surveys'
def get(name,url):
 r=fetch(url,timeout=60,max_bytes=25000000,source='friend_surveys');rec={'file':name,'url':url,'status':r.status,'request_id':r.request_id,'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest(),'cache_hit':r.cache_hit,'error':r.error,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with (OUT/'acquisition_log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 if r.status==200 and not r.error:(CACHE/name).write_bytes(r.content)
 print(json.dumps(rec),flush=True);return r
if __name__=='__main__':
 items=[('pwc2024.pdf','https://www.pwc.com/id/en/publications/automotive/indonesia-electric-vehicle-readiness-consumer-insights-2024.pdf'),('pwc2025_asean.html','https://www.pwc.com/id/asean-6-ereadiness-2025'),('rakuten2026.html','https://insight.rakuten.com/how-to-win-the-ev-shift-in-2026/'),('populix_mobil123.html','https://www.mobil123.com/berita/13-tantangan-punya-mobil-dan-motor-listrik-di-indonesia-menurut-pemilik-137158/137158')]
 for n,u in items:get(n,u)
