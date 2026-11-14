import sys,json,hashlib,concurrent.futures,subprocess
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
B=Path(__file__).resolve().parent;P=B.parents[1]/'private_cache'/'extension_economics';P.mkdir(parents=True,exist_ok=True)
S=[
('EE-S01','T-CARE current program and model/service tool','https://aftersales.toyota.astra.co.id/t-care'),
('EE-S02','T-CARE FAQ current detailed eligibility','https://aftersales.toyota.astra.co.id/faq?category=t-care'),
('EE-S03','T-CARE and Lite/Lite+ launch scopes','https://pressroom.toyota.astra.co.id/bebas-biaya-servis-berkala-7-kali-dengan-extra-1-tahun-warranty-toyota-perluas-pilihan-program'),
('EE-S04','T-CARE XTRA current Toyota announcement','https://pressroom.toyota.astra.co.id/toyota-perkuat-layanan-purnajual-lewat-t-care-xtra'),
('EE-S05','bZ4X older official brochure','https://www.toyota.astra.co.id/sites/default/files/2022-11/brochures/catalog_bz4x_compressed.pdf'),
('EE-S06','Toyota xEV service interval and job-scope representation','https://pressroom.toyota.astra.co.id/alasan-servis-berkala-penting-untuk-menjaga-kondisi-mobil-bagaimana-dengan-kendaraan-elektrifikasi'),
]
def go(item):
 sid,title,url=item;r=fetch(url,source='extension_economics',timeout=60,max_bytes=25000000);pdf=r.content.startswith(b'%PDF');path=P/(sid+('.pdf' if pdf else '.html'))
 if r.status==200:path.write_bytes(r.content)
 row=dict(source_id=sid,title=title,url=url,final_url=r.url,retrieved_at_utc=datetime.now(timezone.utc).isoformat(),status=r.status,request_id=r.request_id,cache_hit=r.cache_hit,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),private_path=str(path),error=r.error,primary_ownership_cluster='Toyota/TAM',full_text_public_redistribution=False)
 if r.status==200 and pdf:subprocess.run(['pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],check=True)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(go,S))
(B/'source_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
for row in rows:print(json.dumps({k:v for k,v in row.items() if k not in ['private_path']},ensure_ascii=False),flush=True)
