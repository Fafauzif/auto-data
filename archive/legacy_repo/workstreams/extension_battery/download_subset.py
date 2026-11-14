from collect import get,CACHE,OUT
import json,hashlib
from concurrent.futures import ThreadPoolExecutor
selected=['Folder1','Folder2','Folder7','Folder8','Folder16']
def one(folder):
 item=json.loads((CACHE/(folder+'_files.json')).read_text())[0]
 raw=get(folder+'_Raw.mat',item['content_details']['download_url'],max_bytes=150000000)
 rec={'folder':folder,'source_file_id':item['id'],'source_filename':item['filename'],'source_size':item['size'],'source_url':item['content_details']['download_url'],'source_sha256':item['content_details']['sha256_hash'],'retrieved_bytes':len(raw),'retrieved_sha256':hashlib.sha256(raw).hexdigest(),'hash_matches':hashlib.sha256(raw).hexdigest()==item['content_details']['sha256_hash'],'license':'CC BY-NC3.0','source_doi':'10.17632/7vdkzpnjgj.2'}
 print('RESULT',json.dumps(rec),flush=True)
 return rec
with ThreadPoolExecutor(max_workers=2) as ex:r=list(ex.map(one,selected))
(OUT/'SOURCE_FILE_MANIFEST.json').write_text(json.dumps(r,indent=2)+'\n')
