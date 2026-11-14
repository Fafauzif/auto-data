"""At most nine prospectively selected allowed public listing pages. No pagination or account access."""
import json,re,sys,ssl,hashlib,datetime,urllib.robotparser,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;PRIVATE=ROOT/'private_cache/extension_reviews';PRIVATE.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
sys.path.insert(0,str(ROOT/'private_cache/reviews/deps'));from google_play_scraper.features.app import parse_dom
ssl._create_default_https_context=ssl.create_default_context
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs
apps=[('myhyundai_indonesia','id.co.hyundaimotor.mmp',['en']),('my_wuling','com.yonyou.cip.sgmw',['en']),('mitsubishi_motors_id','id.co.mmksi.mitsubishimotors',['en']),('honda_ecare','id.co.hpm.ecare',['id','en']),('my_suzuki','com.sim.mysuzuki',['id','en']),('my_chery','com.chery.id.chery',['id','en'])]
robot=fetch('https://play.google.com/robots.txt',cache=False,source='extension_reviews_robots')
(OUT/'play_robots_current.txt').write_text(robot.text)
if robot.status!=200 or robot.error:raise RuntimeError('Robots unavailable; no listing request made')
rp=urllib.robotparser.RobotFileParser();rp.parse(robot.text.splitlines());records=[];logs=[];metadata=[]
for app,appid,languages in apps:
 for lang in languages:
  url='https://play.google.com/store/apps/details?id='+appid+'&hl='+lang+'&gl=ID'
  if not rp.can_fetch('Auto2000CaseResearch',url):raise RuntimeError('Robots disallows proposed public listing; no attempt')
  r=fetch(url,source='extension_reviews_new_public_listing');utc=datetime.datetime.now(datetime.timezone.utc).isoformat();log={'app':app,'app_id':appid,'requested_language':lang,'country_parameter':'ID','url':url,'status':r.status,'error_present':bool(r.error),'request_id':r.request_id,'cache_hit':r.cache_hit,'source_capture_sha256':hashlib.sha256(r.content).hexdigest(),'parser_records':None,'checked_utc':utc}
  if r.status==200 and not r.error:
   ds={}
   for m in Regex.SCRIPT.findall(r.text):
    k=Regex.KEY.findall(m);v=Regex.VALUE.findall(m)
    if k and v:ds[k[0]]=json.loads(v[0])
   (PRIVATE/(app+'_'+lang+'_dataset.json')).write_text(json.dumps(ds,ensure_ascii=False))
   nodes=[]
   def walk(x):
    if not isinstance(x,list):return
    if len(x)>6 and isinstance(x[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',x[0]) and isinstance(x[1],list) and isinstance(x[2],int) and x[2] in range(1,6) and isinstance(x[4],str):nodes.append(x)
    else:
     for child in x:walk(child)
   walk(list(ds.values()));log['parser_records']=len(nodes)
   if not nodes:log['warning']='No embedded review objects; not evidence of zero app reviews'
   for item in nodes:
    row={k:spec.extract_content(item) for k,spec in ElementSpecs.Review.items() if k not in ['userName','userImage','replyContent']};row['developer_reply_present']=bool(item[7] if len(item)>7 else None);row['published_source_epoch']=item[5][0];row['at']=datetime.datetime.fromtimestamp(item[5][0],datetime.timezone.utc).isoformat();row.update(app=app,app_id=appid,platform='google_play',locale=lang+'_ID',source_url=url,source_request_id=r.request_id,source_capture_sha256=log['source_capture_sha256'],wave='extension_new',selection='prespecified_public_listing_counterpart_or_job_matched_new_app');records.append(row)
   m=parse_dom(r.text,appid,url);metadata.append({'app':app,'app_id':appid,'locale':lang+'_ID','source_url':url,'source_request_id':r.request_id,'title':m.get('title'),'developer_company':m.get('developer'),'app_version_snapshot':m.get('version'),'source_update_date':m.get('lastUpdatedOn'),'source_rating_snapshot':m.get('score'),'source_rating_count_snapshot':m.get('ratings'),'source_text_review_count_snapshot':m.get('reviews'),'verified_use_or_residence':False})
  logs.append(log);(OUT/'acquisition_log.json').write_text(json.dumps(logs,indent=2));(OUT/'app_listing_metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2));(PRIVATE/'new_captured_review_records.json').write_text(json.dumps(records,ensure_ascii=False,default=str,indent=2));print({k:log[k] for k in ['app','requested_language','status','parser_records','cache_hit']},flush=True)
  if r.status in (403,429) or r.error:raise RuntimeError('Stopped after source access restriction/transport error; no retries or alternate identity')
print('Captured',len(records),'review appearances from',len(logs),'public listing pages; IDs still need overlap reconciliation',flush=True)
