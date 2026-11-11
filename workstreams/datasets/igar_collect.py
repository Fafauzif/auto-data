import sys,json,hashlib,datetime
from acquire import CACHE,OUT,fetch
items=json.load(open(CACHE/'igar_files.json'))
for item in items:
 name=item['filename'];url=item['content_details']['download_url'];r=fetch(url,timeout=180,max_bytes=150000000,source='datasets_igar')
 sha=hashlib.sha256(r.content).hexdigest();rec={'name':name,'source_dataset':'10.17632/7zryc6k76z.2','source_url':url,'status':r.status,'error':r.error,'bytes':len(r.content),'source_sha256':item['content_details']['sha256_hash'],'retrieved_sha256':sha,'hash_matches':sha==item['content_details']['sha256_hash'],'request_id':r.request_id,'license':'CC BY4.0','retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with (OUT/'igar_acquisition_log.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec),flush=True)
 if r.status==200 and not r.error:
  assert rec['hash_matches'];(CACHE/name).write_bytes(r.content)
