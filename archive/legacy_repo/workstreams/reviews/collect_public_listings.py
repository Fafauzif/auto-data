import sys,json,datetime,hashlib,re,ssl,importlib,urllib.robotparser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent; PRIVATE=ROOT/'private_cache'/'reviews';PRIVATE.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
sys.path.insert(0,str(PRIVATE/'deps')); from google_play_scraper.features.app import parse_dom
ssl._create_default_https_context=ssl.create_default_context
from google_play_scraper.constants.regex import Regex
from google_play_scraper.constants.element import ElementSpecs
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
APPS=[('digiroom','id.co.astra.ai.dev1','421805050'),('mtoyota','com.toyota.m','1480809215'),('seva','id.seva','1589727482'),('byd_auto','com.byd.bydautolink','1492400299'),('myhyundai_indonesia','id.co.hyundaimotor.mmp',None),('my_wuling','com.yonyou.cip.sgmw',None),('mitsubishi_motors_id','id.co.mmksi.mitsubishimotors',None)]
logs=[]; metas=[]; records=[]; robots={}
for domain in ['play.google.com','itunes.apple.com','apps.apple.com']:
 r=fetch('https://'+domain+'/robots.txt',source='reviews_robots');(OUT/(domain+'_robots.txt')).write_text(r.text)
 logs.append({'kind':'robots','domain':domain,'status':r.status,'request_id':r.request_id,'retrieved':now()})
 robot=urllib.robotparser.RobotFileParser();robot.parse(r.text.splitlines());robots[domain]=robot
 print('robots',domain,r.status,flush=True)
for name,appid,appleid in APPS:
 url='https://play.google.com/store/apps/details?id='+appid+'&hl=id&gl=ID'
 if not robots['play.google.com'].can_fetch('Auto2000CaseResearch',url):raise RuntimeError('robots disallows '+url)
 r=fetch(url,source='reviews_public_listing')
 logs.append({'kind':'google_play_listing','app':name,'url':url,'status':r.status,'request_id':r.request_id,'retrieved':now()})
 if r.status!=200:continue
 try:
  result=parse_dom(r.text,appid,url)
  keep=['title','appId','url','score','ratings','reviews','histogram','installs','minInstalls','maxInstalls','version','updated','released','lastUpdatedOn','developer','adSupported','containsAds','genre','free']
  meta={k:result.get(k) for k in keep};meta.update(app=name,platform='google_play',locale='id_ID',retrieved=now());metas.append(meta)
  ds={}
  for match in Regex.SCRIPT.findall(r.text):
   k=Regex.KEY.findall(match);v=Regex.VALUE.findall(match)
   if k and v:ds[k[0]]=json.loads(v[0])
  (PRIVATE/(name+'_play_dataset.json')).write_text(json.dumps(ds,ensure_ascii=False,default=str))
  # Reviews embedded in public details HTML; same element layout as library's review fields. No disallowed pagination endpoint is requested.
  candidates=[]
  def review_nodes(node):
   if not isinstance(node,list):return
   if len(node)>6 and isinstance(node[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',node[0]) and isinstance(node[1],list) and isinstance(node[2],int) and node[2] in range(1,6) and isinstance(node[4],str):
    candidates.append(node)
   else:
    for child in node:review_nodes(child)
  review_nodes(list(ds.values()))
  logs[-1]['embedded_review_records']=len(candidates)
  if not candidates:logs[-1]['parser_warning']='No shape-validated embedded review records; not proof of zero app reviews'
  for item in candidates:
   row={k:spec.extract_content(item) for k,spec in ElementSpecs.Review.items()}
   row.update(app=name,app_id=appid,platform='google_play',locale='id_ID',source_url=url,retrieved=now(),selection='embedded_public_listing')
   records.append(row)
  print('play',name,'reviews',len([x for x in records if x['app']==name]),'meta_reviews',meta.get('reviews'),flush=True)
 except Exception as e:logs[-1]['parser_error']=str(e)
 (OUT/'listing_metadata.json').write_text(json.dumps(metas,ensure_ascii=False,default=str,indent=2));(PRIVATE/'review_records.json').write_text(json.dumps(records,ensure_ascii=False,default=str,indent=2));(OUT/'collection_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
# App Store public see-all reviews pages: no RSS / batchexecute, no pagination not present in allowed public page.
for name,appid,appleid in APPS:
 if not appleid:continue
 url='https://apps.apple.com/id/app/id'+appleid+'?see-all=reviews'
 if not robots['apps.apple.com'].can_fetch('Auto2000CaseResearch',url):raise RuntimeError('robots disallows '+url)
 r=fetch(url,source='reviews_apple_public')
 logs.append({'kind':'apple_reviews_public','app':name,'url':url,'status':r.status,'request_id':r.request_id,'retrieved':now()})
 if r.status==200:(PRIVATE/(name+'_apple_reviews.html')).write_text(r.text)
 print('apple',name,r.status,len(r.content),flush=True)
 (OUT/'collection_log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2))
