from pathlib import Path
import sys,json,subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
out=Path(__file__).resolve().parent; private=out.parents[1]/'private_cache'/'market_text'
sources={'ipb_utaut':'https://journal.ipb.ac.id/jabm/article/download/61101/31604/364864','ipb_environment':'https://journal.ipb.ac.id/jabm/article/download/52902/28366/284213','deloitte_sea':'https://www.deloitte.com/content/dam/assets-zone1/southeast-asia/en/docs/industries/consumer/2026/sea-cb-2026-sea-automotive-consumer-study.pdf'}
def one(item):
 name,url=item;r=fetch(url,source='market',max_bytes=30000000,timeout=50);meta={'name':name,'url':url,'status':r.status,'request_id':r.request_id,'bytes':len(r.content),'error':r.error,'final_url':r.url}
 if r.status==200 and r.content.startswith(b'%PDF'):
  pdf=private/(name+'.pdf');pdf.write_bytes(r.content);p=subprocess.run(['pdftotext','-layout',str(pdf),str(private/(name+'.txt'))],capture_output=True);meta['pdf_to_text_returncode']=p.returncode
 print(json.dumps(meta),flush=True);return meta
with ThreadPoolExecutor(max_workers=3) as ex:rows=list(ex.map(one,sources.items()))
(out/'primary_retrieval_followup.json').write_text(json.dumps(rows,indent=2))
