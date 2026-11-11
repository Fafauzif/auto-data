"""Probe allowed public listing language selection; no pagination, no hidden endpoints."""
import sys,json,re,datetime,ssl,urllib.robotparser
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];PRIVATE=ROOT/'private_cache'/'reviews'
sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
sys.path.insert(0,str(PRIVATE/'deps'));from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs
ssl._create_default_https_context=ssl.create_default_context
robot=urllib.robotparser.RobotFileParser();robot.parse((OUT/'play.google.com_robots.txt').read_text().splitlines())
records=[];logs=[]
for name,appid in [('digiroom','id.co.astra.ai.dev1'),('mtoyota','com.toyota.m'),('byd_auto','com.byd.bydautolink')]:
 url='https://play.google.com/store/apps/details?id='+appid+'&hl=en&gl=ID'
 if not robot.can_fetch('Auto2000CaseResearch',url):raise RuntimeError('robots disallowed '+url)
 r=fetch(url,source='reviews_locale_selection_probe');log={'app':name,'status':r.status,'url':url,'request_id':r.request_id,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if r.status==200:
  ds={}
  for match in Regex.SCRIPT.findall(r.text):
   k=Regex.KEY.findall(match);v=Regex.VALUE.findall(match)
   if k and v:ds[k[0]]=json.loads(v[0])
  (PRIVATE/(name+'_play_en_dataset.json')).write_text(json.dumps(ds,ensure_ascii=False))
  # Shape-validated review lists, not fixed callback number, because language cohorts vary.
  candidates=[]
  def walk(x):
   if isinstance(x,list):
    if len(x)>6 and isinstance(x[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',x[0]) and isinstance(x[1],list) and isinstance(x[2],int) and x[2] in range(1,6) and isinstance(x[4],str):candidates.append(x)
    else:
     for a in x:walk(a)
  walk(list(ds.values()))
  for item in candidates:
   row={k:spec.extract_content(item) for k,spec in ElementSpecs.Review.items()};row.update(app=name,app_id=appid,platform='google_play',locale='en_ID',source_url=url,retrieved=log['retrieved_utc'],selection='embedded_public_listing_en_language_probe');records.append(row)
  log['embedded_records']=len(candidates)
 logs.append(log);print(log,flush=True)
 (PRIVATE/'locale_probe_records.json').write_text(json.dumps(records,ensure_ascii=False,default=str,indent=2));(OUT/'locale_probe_log.json').write_text(json.dumps(logs,indent=2))
# Build the exact deduplicated supplement used by analyze_reviews.py.
# Compare with primary Google records, not a prior normalized file that may already contain this supplement.
base=json.loads((PRIVATE/'review_records.json').read_text()) if (PRIVATE/'review_records.json').exists() else []
seen={str(x['platform'])+':'+str(x['reviewId']) for x in base};extra=[]
for row in records:
 key=str(row['platform'])+':'+str(row['reviewId'])
 if key not in seen:extra.append(row);seen.add(key)
(PRIVATE/'locale_unique_extra.json').write_text(json.dumps(extra,ensure_ascii=False,default=str,indent=2))
(OUT/'locale_probe_unique_summary.json').write_text(json.dumps({'retrieved_embedded_records':len(records),'additional_unique_records_against_primary_google':len(extra),'duplicate_or_existing_ids':len(records)-len(extra),'not_independent_people_or_representative_sample':True},indent=2))
