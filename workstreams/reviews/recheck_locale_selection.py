import sys,json,re,datetime
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];PRIVATE=ROOT/'private_cache'/'reviews'
sys.path.insert(0,str(ROOT/'shared'));from public_http import fetch
sys.path.insert(0,str(PRIVATE/'deps'));from google_play_scraper.constants.regex import Regex
import ssl;ssl._create_default_https_context=ssl.create_default_context
rows=[]
for lang in ['id','en']:
 url='https://play.google.com/store/apps/details?id=com.byd.bydautolink&hl='+lang+'&gl=ID';r=fetch(url,source='reviews_locale_recheck',cache=False)
 ids=[]
 if r.status==200:
  for match in Regex.SCRIPT.findall(r.text):
   v=Regex.VALUE.findall(match)
   if not v:continue
   def walk(x):
    if isinstance(x,list):
     if len(x)>6 and isinstance(x[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',x[0]) and isinstance(x[1],list) and isinstance(x[2],int) and x[2] in range(1,6) and isinstance(x[4],str):ids.append(x[0])
     else:
      for a in x:walk(a)
   walk(json.loads(v[0]))
 baseline=json.loads((PRIVATE/('byd_auto_play_dataset.json' if lang=='id' else 'byd_auto_play_en_dataset.json')).read_text());old=[]
 def walkold(x):
  if isinstance(x,list):
   if len(x)>6 and isinstance(x[0],str) and re.fullmatch(r'[0-9a-fA-F-]{36}',x[0]) and isinstance(x[1],list) and isinstance(x[2],int) and x[2] in range(1,6) and isinstance(x[4],str):old.append(x[0])
   else:
    for a in x:walkold(a)
 walkold(list(baseline.values()))
 d={'language':lang,'country_parameter':'ID','status':r.status,'source_url':url,'request_id':r.request_id,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review_ids_returned_n':len(ids),'baseline_ids_n':len(old),'overlap_with_same_language_baseline':len(set(ids)&set(old)),'set_equal_to_same_language_baseline':set(ids)==set(old),'is_additional_independent_customer_evidence':False};rows.append(d);print(d,flush=True)
 (OUT/'locale_recheck.json').write_text(json.dumps(rows,indent=2))
