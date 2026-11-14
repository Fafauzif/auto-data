import sys,json,re,subprocess,hashlib
from pathlib import Path
sys.path.insert(0,'/workspace/scratch/70444ed5f561/auto2000_run/shared')
from public_http import fetch
out=Path(__file__).resolve().parent;private=out.parents[1]/'private_cache'/'friend_capabilities';private.mkdir(parents=True,exist_ok=True)
url='https://www.astra.co.id/en/investor-relations/annually-update'
r=fetch(url,source='friend_capabilities');(private/'annual_index.html').write_text(r.text)
links=re.findall(r'https?[^"\s<>]+',r.text)
print('index',r.status,'pdf_mentions',[(x[:200]) for x in links if '.pdf' in x.lower()][:12],flush=True)
# Candidate derived from the exact known 2024 public-report naming pattern; existence is verified below, not assumed.
url='https://r2.astra.co.id/annual-reports/documents/Astra-Annual-Report-2025.pdf'
r=fetch(url,source='friend_capabilities',timeout=65,max_bytes=100000000)
m={'source_url':url,'status':r.status,'request_id':r.request_id,'bytes':len(r.content),'error':r.error,'final_url':r.url,'discovery':'Candidate from known 2024 official filename pattern; accepted only if valid PDF and report year verified.'}
if r.status==200 and r.content.startswith(b'%PDF'):
 p=private/'astra_ar2025.pdf';p.write_bytes(r.content);m['sha256']=hashlib.sha256(r.content).hexdigest();m['private_path']=str(p)
 subprocess.run(['pdftotext','-layout',str(p),str(private/'astra_ar2025.txt')],check=True)
print(json.dumps(m),flush=True);(out/'astra_retrieval.json').write_text(json.dumps(m,indent=2))
