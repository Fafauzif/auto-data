from pathlib import Path
import json,sys,hashlib,datetime,concurrent.futures
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'shared'))
from public_http import fetch
OUT=Path(__file__).resolve().parent
sources=json.loads((OUT/'sources.json').read_text())
class TextReader(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.titleflag=False;self.title='';self.text=[]
 def handle_starttag(self,t,a):
  if t in ('script','style','noscript'):self.skip+=1
  if t=='title':self.titleflag=True
 def handle_endtag(self,t):
  if t in ('script','style','noscript'):self.skip=max(0,self.skip-1)
  if t=='title':self.titleflag=False
 def handle_data(self,d):
  if self.titleflag:self.title+=d
  if not self.skip:self.text.append(d)
def domain_job(items):
 domain=urlsplit(items[0]['url']).netloc;robot_url='https://'+domain+'/robots.txt';rob=fetch(robot_url,source='competition_robots',timeout=25)
 logs=[dict(kind='robots',url=robot_url,status=rob.status,request_id=rob.request_id,bytes=len(rob.content),error=rob.error)]
 if rob.status in (401,403,429) or rob.status>=500 or rob.status==0:
  return logs+[dict(source_id=s['source_id'],url=s['url'],method='not_attempted_domain_access_stop',status=None,reason='robots retrieval blocked or failed; search evidence retained') for s in items]
 rp=RobotFileParser();rp.parse(rob.text.splitlines() if rob.status==200 else [])
 for s in items:
  if not rp.can_fetch('Auto2000CaseResearch',s['url']):
   logs.append(dict(source_id=s['source_id'],url=s['url'],method='not_attempted_robots',status=None));continue
  r=fetch(s['url'],source='competition',timeout=30)
  p=TextReader()
  if r.status==200:p.feed(r.text)
  txt=' '.join(' '.join(p.text).split())
  logs.append(dict(source_id=s['source_id'],url=s['url'],final_url=r.url,method='raw_http',status=r.status,request_id=r.request_id,cache_hit=r.cache_hit,bytes=len(r.content),body_sha256=hashlib.sha256(r.content).hexdigest(),title=p.title.strip(),visible_text_words=len(txt.split()),has_js_shell='JavaScript is required' in txt,has_antibot_text=any(x in txt.lower() for x in ('verify you are human','just a moment','enable javascript and cookies to continue')),error=r.error,captured_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
  if r.status in (401,403,429) or r.status>=500 or not r.status:
   left=items[items.index(s)+1:]
   logs.extend(dict(source_id=k['source_id'],url=k['url'],method='not_attempted_domain_access_stop',status=None) for k in left);break
 return logs
bydomain={}
for s in sources:bydomain.setdefault(urlsplit(s['url']).netloc,[]).append(s)
logs=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for result in pool.map(domain_job,bydomain.values()):
  logs.extend(result);(OUT/'direct_verification.json').write_text(json.dumps(logs,indent=2));print('domains completed; records',len(logs),flush=True)
print('DONE',len(logs))
