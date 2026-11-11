from acquire import get,CACHE,OUT
import json,hashlib,csv
folders=json.load(open(CACHE/'mendeley_spklu_folders2.json'));records=[]
for folder in folders:
 url=f'https://data.mendeley.com/public-api/datasets/z2bvd5r574/files?folder_id={folder["id"]}&version=2&$start=0&$limit=1000'
 r=get('spklu_'+folder['name']+'_files.json',url)
 if r.status!=200:continue
 items=r.json()
 for item in items:
  name=item['filename'];r=get(name,item['content_details']['download_url'])
  record={'dataset_doi':'10.17632/z2bvd5r574.2','folder':folder['name'],'filename':name,'source_file_id':item['id'],'source_sha256':item['content_details']['sha256_hash'],'retrieved_sha256':hashlib.sha256(r.content).hexdigest(),'hash_matches':hashlib.sha256(r.content).hexdigest()==item['content_details']['sha256_hash'],'source_url':item['content_details']['download_url'],'status':r.status,'license':'CC BY-NC 3.0'}
  records.append(record)
  (OUT/'spklu_file_provenance.json').write_text(json.dumps(records,indent=2))
  if r.status==200:
   assert record['hash_matches'],name
   print('VERIFIED',name,len(r.content),flush=True)
