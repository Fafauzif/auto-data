from pathlib import Path
import sys,json,re,subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
out=Path(__file__).resolve().parent
private=out.parents[1]/'private_cache'/'market_text';private.mkdir(parents=True,exist_ok=True)
sources={
'deloitte_id':'https://www.deloitte.com/content/dam/assets-zone1/southeast-asia/en/docs/industries/consumer/2026/id-cb-automotive-ev-adoption-2026.pdf',
'nist':'https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=958584',
'ui_adoption':'https://ijtech.eng.ui.ac.id/download/article/7804',
'java_choice':'https://jurnal.ugm.ac.id/v3/JCEF/article/download/22067/6050/',
'ipb_utaut_wrapper':'https://journal.ipb.ac.id/jabm/article/view/61101/31604',
'ipb_environment_wrapper':'https://journal.ipb.ac.id/jabm/article/view/52902/28366'}
def one(item):
 name,url=item;r=fetch(url,source='market');meta={'name':name,'url':url,'status':r.status,'request_id':r.request_id,'cache_hit':r.cache_hit,'bytes':len(r.content),'error':r.error,'final_url':r.url}
 if r.status==200 and r.content.startswith(b'%PDF'):
  pdf=private/(name+'.pdf');pdf.write_bytes(r.content);p=subprocess.run(['pdftotext','-layout',str(pdf),str(private/(name+'.txt'))],capture_output=True);meta['pdf_to_text_returncode']=p.returncode
 elif r.status==200:
  (private/(name+'.html')).write_text(r.text);meta['pdf_candidates']=re.findall(r'(?:src|href)=["\']([^"\']+(?:pdf|download)[^"\']*)',r.text,re.I)[:15]
 print(json.dumps(meta),flush=True);return meta
with ThreadPoolExecutor(max_workers=4) as ex:rows=list(ex.map(one,sources.items()))
(out/'primary_retrieval.json').write_text(json.dumps(rows,indent=2))
