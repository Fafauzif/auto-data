import sys,json,hashlib,subprocess,concurrent.futures
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
B=Path(__file__).resolve().parent;P=B.parents[1]/'private_cache'/'extension_economics'
rows=json.loads((B/'source_checks.json').read_text())
S=[('EE-S07','Public T-CARE page script for published model estimates','https://aftersales.toyota.astra.co.id/_next/static/chunks/pages/t-care-d4082439604514ff.js'),('EE-S08','GBSB PDF linked by current program page','https://aftersales.toyota.astra.co.id/assets/Informasi-Program-Gratis-Biaya-Servis-Berkala.pdf'),('EE-S09','Indonesian owner manual index','https://www.toyota.astra.co.id/ownership')]
def go(t):
 sid,title,url=t;r=fetch(url,source='extension_economics',timeout=60,max_bytes=25000000);pdf=r.content.startswith(b'%PDF');ext='.pdf' if pdf else '.js' if url.endswith('.js') else '.html';p=P/(sid+ext)
 if r.status==200:p.write_bytes(r.content)
 m=dict(source_id=sid,title=title,url=url,final_url=r.url,status=r.status,request_id=r.request_id,cache_hit=r.cache_hit,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_at_utc=datetime.now(timezone.utc).isoformat(),private_path=str(p),error=r.error,primary_ownership_cluster='Toyota/TAM',full_text_public_redistribution=False)
 if pdf and r.status==200:subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 return m
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:new=list(ex.map(go,S))
rows+=new;(B/'source_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
for r in new:print(r['source_id'],r['status'],r['bytes'],r['final_url'],flush=True)
