"""Export original non-text review fields, source capture hashes and locators; no new network."""
import csv,json,sqlite3,hashlib,datetime,re
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];REV=ROOT/'workstreams'/'reviews';PRIVATE=ROOT/'private_cache'/'reviews'
with (REV/'reviews_derived.csv').open(encoding='utf8',newline='') as f:derived=list(csv.DictReader(f))
raw={x['record_key']:x for x in json.loads((PRIVATE/'normalized_reviews.json').read_text())}
source_log=[]
for fn in ['collection_log.json','locale_probe_log.json']:
 source_log.extend(json.loads((REV/fn).read_text()))
lookup={x['url']:x for x in source_log if x.get('url') and x.get('status')==200}
conn=sqlite3.connect(ROOT/'private_cache'/'transport.sqlite');conn.row_factory=sqlite3.Row
transport={x['id']:dict(x) for x in conn.execute('SELECT * FROM requests')};conn.close()
epochs={}
for p in PRIVATE.glob('*_play*dataset.json'):
 data=json.loads(p.read_text())
 def walk(x):
  if isinstance(x,list):
   if len(x)>6 and isinstance(x[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',x[0]) and isinstance(x[1],list) and isinstance(x[2],int) and x[2] in range(1,6) and isinstance(x[4],str):
    epochs['google_play:'+x[0]]=x[5][0]
   else:
    for z in x:walk(z)
 walk(list(data.values()))
rows=[];sources={};missing=[]
for d in derived:
 r=raw[d['record_key']];log=lookup.get(d['source_url']);request=transport.get(log.get('request_id')) if log else None
 if not request:missing.append(d['evidence_id'])
 body=ROOT/'private_cache'/'http'/(request['cache_key']+'.bin') if request else None
 bodyhash=hashlib.sha256(body.read_bytes()).hexdigest() if body and body.exists() else None
 epoch=epochs.get(d['record_key']);published=datetime.datetime.fromtimestamp(epoch,datetime.timezone.utc).isoformat() if epoch is not None else d['review_date']
 capture=datetime.datetime.fromtimestamp(request['started'],datetime.timezone.utc).isoformat() if request else None
 sourceid='REV-SRC-'+hashlib.sha256(d['source_url'].encode()).hexdigest()[:10]
 row={'evidence_id':d['evidence_id'],'source_record_id':d['review_id'],'platform':d['platform'],'app':d['app'],'requested_locale':d['locale'],'source_url':d['source_url'],'source_id':sourceid,'source_request_id':request['id'] if request else None,'source_capture_utc':capture,'source_capture_sha256':bodyhash,'published_timestamp_source_epoch':epoch,'published_timestamp_utc':published,'rating_source_value':r.get('score'),'review_created_version_source_value':r.get('reviewCreatedVersion'),'thumbs_up_source_value':r.get('thumbsUpCount'),'developer_reply_present':bool(r.get('replyContent')),'text_sha256':hashlib.sha256(str(r.get('content') or '').encode()).hexdigest(),'source_text_republished':False,'author_identity_republished':False,'reviewer_residence_verified':False,'record_unit':'one_platform_review_id'}
 rows.append(row)
 sources[sourceid]={'source_id':sourceid,'source_url':d['source_url'],'platform':d['platform'],'app':d['app'],'requested_locale':d['locale'],'source_request_id':row['source_request_id'],'source_capture_utc':capture,'source_capture_sha256':bodyhash,'review_record_n':sum(x['source_url']==d['source_url'] for x in derived),'full_raw_html_public_release':False,'reacquisition_route':'allowed_public_listing_HTML_only'}
with (OUT/'review_source_records_nontext.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
with (OUT/'review_source_capture_index.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,list(sources.values())[0].keys());w.writeheader();w.writerows(sources.values())
report={'source_records':len(rows),'unique_platform_review_ids':len(set(x['platform']+':'+str(x['source_record_id']) for x in rows)),'unique_public_page_captures':len(sources),'google_timestamp_epochs_recovered':sum(x['published_timestamp_source_epoch'] is not None for x in rows),'all_have_capture_hash':all(x['source_capture_sha256'] for x in rows),'missing_source_provenance':missing,'no_review_text_or_author_fields_exported':True,'duplicate_text_hash_records':len(rows)-len(set(x['text_sha256'] for x in rows)),'counts_are_not_independent_people':True}
(OUT/'review_source_metadata_validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
