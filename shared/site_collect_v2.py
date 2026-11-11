from pathlib import Path
import sys,json,csv,hashlib,re,time,sqlite3,threading,concurrent.futures,collections,urllib.parse,argparse
from bs4 import BeautifulSoup
from public_http import fetch,ROOT
P=ROOT/'data';P.mkdir(exist_ok=True);DB=P/'site_evidence.sqlite'
def database():
 c=sqlite3.connect(DB,timeout=30);c.execute('PRAGMA journal_mode=WAL')
 c.executescript('''CREATE TABLE IF NOT EXISTS pages(url TEXT PRIMARY KEY,final_url TEXT,request_id TEXT,status INTEGER,captured REAL,family TEXT,selection TEXT,bytes INTEGER,title TEXT,main_words INTEGER,main_hash TEXT,simhash TEXT,canonical TEXT,h1_count INTEGER,internal_links INTEGER,external_links INTEGER,image_count INTEGER,images_missing_alt INTEGER,schema_types TEXT,forms INTEGER,topic_flags TEXT,date_mentions TEXT,error TEXT); CREATE TABLE IF NOT EXISTS links(page_url TEXT,target_url TEXT,is_internal INTEGER,in_main INTEGER,occurrences INTEGER,PRIMARY KEY(page_url,target_url,in_main)); CREATE TABLE IF NOT EXISTS amounts(page_url TEXT,amount_id INTEGER,value_rupiah INTEGER,scope TEXT,PRIMARY KEY(page_url,amount_id));''');c.execute('CREATE TABLE IF NOT EXISTS extraction_versions(url TEXT PRIMARY KEY,version TEXT,selector TEXT,parsed_epoch REAL)');c.commit();return c
STOP=threading.Event();LOCK=threading.Lock();failures=0

def family(url):
 p=urllib.parse.urlsplit(url).path
 if '/sales-advisor/' in p:return 'adviser_editorial' if '/berita-dan-tips/' in p else 'adviser'
 if p.startswith('/berita-dan-tips/'):return 'editorial'
 if p.startswith('/dealer-toyota'):return 'local_branch'
 if p.startswith('/mobil-baru-toyota/p/'):
  parts=p.strip('/').split('/');return 'product_'+(parts[3] if len(parts)>3 else 'overview')
 if p.startswith('/c/'):return 'catalogue'
 return 'service_utility'

def allowed(url,rules):
 parsed=urllib.parse.urlsplit(url)
 if parsed.hostname!='auto2000.co.id' or parsed.query or parsed.fragment:return False
 path=parsed.path
 return not any(re.match('^'+re.escape(rule).replace(r'\*','.*').replace(r'\$','$'),path) for rule in rules)

def simhash(words):
 w=words[:25000];counts=collections.Counter(' '.join(w[i:i+3]) for i in range(max(0,len(w)-2)));v=[0]*64
 for token,weight in counts.items():
  num=int.from_bytes(hashlib.blake2b(token.encode(),digest_size=8).digest(),'big')
  for j in range(64):v[j]+=weight if num&(1<<j) else -weight
 return format(sum(1<<j for j,n in enumerate(v) if n>=0),'016x')

def collect(item):
 global failures
 if STOP.is_set():return
 url,selection=item;r=fetch(url,source='auto2000_site',timeout=30,max_bytes=8000000)
 fam=family(url);tc=sqlite3.connect(ROOT/'private_cache/transport.sqlite');tr=tc.execute('SELECT started FROM requests WHERE id=?',(r.request_id,)).fetchone();tc.close();captured=tr[0] if tr else time.time();selector='not_parsed';record=[url,r.url,r.request_id,r.status,captured,fam,selection,len(r.content),'',0,'','','',0,0,0,0,0,'[]',0,'{}','[]',r.error]
 links=[];amounts=[]
 if r.status==200 and r.content and not r.error:
  try:
   soup=BeautifulSoup(r.content,'lxml');title=' '.join(soup.title.get_text(' ',strip=True).split()[:20]) if soup.title else ''
   can=soup.find('link',rel=lambda x:x and 'canonical' in x);canonical=can.get('href','') if can else ''
   schemas=[]
   for node in soup.find_all('script',type='application/ld+json'):
    try:
     obj=json.loads(node.string or node.get_text());nodes=obj if isinstance(obj,list) else [obj]
     for n in nodes:
      if isinstance(n,dict):
       typ=n.get('@type');schemas+=typ if isinstance(typ,list) else ([typ] if typ else [])
       for g in n.get('@graph',[]):
        if isinstance(g,dict) and g.get('@type'):schemas.append(str(g['@type']))
    except Exception:pass
   mains=soup.find_all('main');inner=mains[-1] if mains else (soup.body or soup)
   prose=soup.select_one('#detailContentArticle .prose') or (soup.select_one('.prose') if fam in ('editorial','adviser_editorial') else None)
   main=prose or soup.find('article') or inner
   selector='editorial_prose' if prose else ('article' if soup.find('article') else 'last_main_or_body')
   for garbage in list(main.select('#mobileNavList, [id^=emarsys], [id^=placeholder_emarsys]')):garbage.decompose()
   main_ids={id(x) for x in main.find_all('a',href=True) if not x.find_parent(['nav','header','footer'])}
   counter=collections.Counter()
   for a in soup.find_all('a',href=True):
    u=urllib.parse.urljoin(r.url,a['href']);p=urllib.parse.urlsplit(u)
    if p.scheme not in ('http','https'):continue
    # Drop query/fragment in release to avoid contact/session parameters; record structural target only
    target=urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,'',''))
    if any(x in (p.hostname or '') for x in ['wa.me','whatsapp.com']):target='https://wa.me/CONTACT_REDACTED'
    counter[(target,int(p.hostname=='auto2000.co.id'),int(id(a) in main_ids))]+=1
   links=[(url,*k,v) for k,v in counter.items()]
   imgs=soup.find_all('img');missing=sum(not x.get('alt','').strip() for x in imgs)
   h1=len(soup.find_all('h1'));forms=len(soup.find_all('form'))
   for n in main.find_all(['script','style','nav','header','footer','noscript']):n.decompose()
   txt=' '.join(main.get_text(' ',strip=True).split());words=re.findall(r'\w+',txt.lower());norm=re.sub(r'\b\d{6,}\b',' NUM ',txt.lower());norm=re.sub(r'\s+',' ',norm)
   flags={k:bool(re.search(rx,txt,re.I)) for k,rx in {'hybrid':r'hybrid|hibrida','bev':r'\bbev\b|bZ4X|mobil listrik','battery_health':r'health check|kesehatan baterai','trade_in':r'tukar tambah|trade.in','financing':r'cicilan|angsuran|kredit','service':r'servis|service|bengkel','body_paint':r'body.*paint|bodi.*cat','warranty':r'garansi|warranty','charging':r'pengisian|charging|SPKLU','cost':r'biaya|harga|\bRp\b','rupiah_numeric_mention':r'\bRp[.\s]*[\d.,]+','contact':r'WhatsApp|hubungi'}.items()}
   vals=[]
   for m in re.finditer(r'\bRp\.?\s*([\d]{1,3}(?:[.,]\d{3})+(?:[.,]\d{1,2})?|\d{4,})',txt,re.I):
    v=int(re.sub(r'\D','',m.group(1)))
    if v<=1000000000000:vals.append(v)
   amounts=[(url,i,v,'selected_content_text_amount_not_verified_offer') for i,v in enumerate(vals[:100])]
   dates=list(dict.fromkeys(re.findall(r'\b(?:19|20)\d{2}\b',txt)))[:30]
   record[8:22]=[title,len(words),hashlib.sha256(norm.encode()).hexdigest(),simhash(words),canonical,h1,sum(v for (u,i,m),v in counter.items() if i),sum(v for (u,i,m),v in counter.items() if not i),len(imgs),missing,json.dumps(sorted(set(schemas))),forms,json.dumps(flags),json.dumps(dates)]
  except Exception as e:record[-1]='parse_error '+str(e)[:250]
 else:
  with LOCK:
   if r.status in (403,429):failures+=1
   if failures>=2:STOP.set()
 c=database();c.execute('DELETE FROM links WHERE page_url=?',(url,));c.execute('DELETE FROM amounts WHERE page_url=?',(url,));c.execute('INSERT OR REPLACE INTO extraction_versions VALUES(?,?,?,?)',(url,'2.0',selector,time.time()));c.execute('INSERT OR REPLACE INTO pages VALUES('+','.join('?'*23)+')',record)
 if links:c.executemany('INSERT OR REPLACE INTO links VALUES(?,?,?,?,?)',links)
 if amounts:c.executemany('INSERT OR REPLACE INTO amounts VALUES(?,?,?,?)',amounts)
 c.commit();c.close()
 return r.status

def run(limit):
 robot=fetch('https://auto2000.co.id/robots.txt',source='scope');
 if robot.status!=200:raise RuntimeError('robots unavailable no site queue start')
 rules=[x.split(':',1)[1].strip() for x in robot.text.splitlines() if x.lower().startswith('disallow:') and x.split(':',1)[1].strip()]
 (P/'robots_scope.json').write_text(json.dumps({'url':robot.url,'request_id':robot.request_id,'rules':rules},indent=2))
 prior=ROOT.parent/'research_work/results/sitemap_urls.csv';rows=list(csv.DictReader(prior.open(encoding='utf8',newline='')))
 # Inventory is carried forward with full origin; it is not counted as new discovery
 (P/'prior_inventory_provenance.json').write_text(json.dumps({'file':str(prior),'sha256':hashlib.sha256(prior.read_bytes()).hexdigest(),'inherited_records':len(rows),'new_collection':False},indent=2))
 urls=list(dict.fromkeys(x['declared_url'] for x in rows));topical=[];other=[]
 terms=r'hybrid|listrik|baterai|servis|service|garansi|biaya|kredit|cicilan|tukar|body|bodi|cat|spare|suku|bengkel|charging|spklu|test.drive|innova|zenix|yariscross|bz4x|veloz|urban.cruiser|fleet'
 for u in urls:
  if not allowed(u,rules):continue
  (topical if re.search(terms,u,re.I) else other).append(u)
 groups=collections.defaultdict(list)
 for u in topical:groups[family(u)].append(u)
 for k in groups:
  groups[k].sort(key=lambda u:(-sum(t in u.lower() for t in ['2026','2025','hybrid','listrik','garansi','baterai','biaya']),u))
 chosen=[]
 # Deterministic family-balanced allocation. URL topic targeting is purposive, never representative.
 while any(groups.values()):
  for key in sorted(groups):
   if groups[key]:chosen.append((groups[key].pop(0),'topic_targeted_family_round_robin'))
 chosen += [(u,'non_topic_family_coverage') for u in other]
 extras=['https://auto2000.co.id/','https://auto2000.co.id/seputar-pertanyaan','https://auto2000.co.id/body-paint-service','https://auto2000.co.id/berita-dan-tips/aplikasi-auto2000-digiroom']
 chosen=[(u,'purpose_selected_core') for u in extras if allowed(u,rules)]+chosen
 chosen=list(dict((u,(u,s)) for u,s in chosen).values())
 c=database();done={x[0] for x in c.execute('SELECT url FROM pages WHERE status IN(200,404,410) AND error=""')};c.close();queue=[x for x in chosen if x[0] not in done][:max(0,limit-len(done))]
 (P/'site_queue.json').write_text(json.dumps({'limit':limit,'inherited_inventory_unique':len(urls),'selected':len(queue),'done_prior':len(done),'selection':'purposive URL topic family round robin','maxima_not_prevalence_sample':True},indent=2))
 print('QUEUE',len(queue),'done',len(done),flush=True)
 started=time.time()
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
  futures={ex.submit(collect,x):x for x in queue}
  for n,f in enumerate(concurrent.futures.as_completed(futures),1):
   try:st=f.result()
   except Exception as e:st=str(e)
   if n%10==0 or n==1:
    c=database();stats=dict(c.execute('SELECT status,COUNT(*) FROM pages GROUP BY status').fetchall());c.close()
    checkpoint={'processed':n,'status_counts':stats,'elapsed_seconds':time.time()-started,'stop':STOP.is_set(),'limit':limit,'updated_epoch':time.time()};(ROOT/'checkpoints/site_progress.json').write_text(json.dumps(checkpoint,indent=2));print(json.dumps(checkpoint),flush=True)
   if STOP.is_set():
    for future in futures:future.cancel()
    print('Queue stopped after repeated access restrictions',flush=True);break
 print('SITE BATCH DONE',flush=True)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--limit',type=int,default=300);a.add_argument('--reparse',action='store_true');args=a.parse_args()
 if args.reparse:
  c=database();items=[(r[0],r[1]) for r in c.execute('SELECT url,selection FROM pages WHERE status=200')];c.close()
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(collect,items))
  print('CACHED REPARSE',len(items),flush=True)
 else:run(args.limit)
