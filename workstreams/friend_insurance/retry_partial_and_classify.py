from pathlib import Path
import sys,json,hashlib
out=Path(__file__).resolve().parent;root=out.parents[1];sys.path.insert(0,str(root/'shared'))
from public_http import fetch
x=json.loads((out/'direct_verification.json').read_text());sources={s['source_id']:s for s in json.loads((out/'sources.json').read_text())}
for sid in ('I12','I17'):
 r=fetch(sources[sid]['url'],source='friend_insurance_retry_transient',timeout=60)
 x.append(dict(source_id=sid,url=sources[sid]['url'],method='raw_http_single_timeout_retry',status=r.status,bytes=len(r.content),error=r.error,request_id=r.request_id,body_sha256=hashlib.sha256(r.content).hexdigest(),final_url=r.url))
for r in x:
 if r.get('source_id')=='I01':r.update(content_support_status='script-only Incapsula challenge, not product text; no bypass attempted',has_antibot_text=True)
 if r.get('source_id') and sources[r['source_id']]['url'].lower().endswith('.pdf'):
  r['visible_text_words']=None;r['content_type_note']='PDF bytes; HTML text count deliberately suppressed; content reviewed through PDF web retrieval'
 if r.get('error'):r['content_support_status']='incomplete or failed transport; do not claim complete raw verification'
(out/'direct_verification.json').write_text(json.dumps(x,indent=2));print([(r.get('source_id'),r.get('status'),r.get('bytes'),r.get('error','')) for r in x[-2:]])
