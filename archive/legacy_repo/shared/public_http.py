"""Shared rate-limited public research transport. Raw response bodies are private cache."""
from pathlib import Path
import sqlite3,time,uuid,hashlib,json,subprocess,tempfile,os
from dataclasses import dataclass
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
DB=ROOT/'private_cache'/'transport.sqlite'; CACHE=ROOT/'private_cache'/'http';CACHE.mkdir(parents=True,exist_ok=True)
def db():
 c=sqlite3.connect(DB,timeout=30);c.execute('PRAGMA journal_mode=WAL')
 c.execute('CREATE TABLE IF NOT EXISTS domains(domain TEXT PRIMARY KEY,last_start REAL)')
 c.execute('CREATE TABLE IF NOT EXISTS leases(id TEXT PRIMARY KEY,domain TEXT,started REAL)')
 c.execute('CREATE TABLE IF NOT EXISTS requests(id TEXT PRIMARY KEY,domain TEXT,url TEXT,method TEXT,status INTEGER,started REAL,elapsed REAL,bytes INTEGER,error TEXT,cache_key TEXT,final_url TEXT)');c.commit();return c
@dataclass
class Response:
 status:int
 content:bytes
 url:str
 request_id:str
 cache_hit:bool=False
 error:str=''
 @property
 def text(self):return self.content.decode('utf8',errors='replace')
 def json(self):return json.loads(self.content)
def fetch(url,method='GET',data=None,headers=None,timeout=35,max_bytes=15000000,cache=True,source='research'):
 domain=urlsplit(url).hostname or '';method=method.upper()
 if method not in ('GET','POST','HEAD'):raise ValueError('Read-only retrieval methods only')
 if method=='POST' and 'play.google.com' not in domain:raise ValueError('POST reserved for public Play review read endpoint')
 payload=data.encode() if isinstance(data,str) else (data or b'')
 key=hashlib.sha256(method.encode()+b'\n'+url.encode()+b'\n'+payload).hexdigest()
 body=CACHE/(key+'.bin');meta=CACHE/(key+'.json')
 if cache and body.exists() and meta.exists():
  m=json.loads(meta.read_text());return Response(m['status'],body.read_bytes(),m['final_url'],m['request_id'],True,m.get('error',''))
 ident=uuid.uuid4().hex
 while True:
  c=db();c.execute('BEGIN IMMEDIATE');now=time.time();c.execute('DELETE FROM leases WHERE started<?',(now-150,))
  n=c.execute('SELECT COUNT(*) FROM leases WHERE domain=?',(domain,)).fetchone()[0]
  last=c.execute('SELECT last_start FROM domains WHERE domain=?',(domain,)).fetchone()
  total=c.execute('SELECT COUNT(*) FROM requests').fetchone()[0]
  if total>=20000:c.rollback();c.close();raise RuntimeError('Global request ceiling reached')
  if n<2 and (not last or now-last[0]>=1):
   c.execute('INSERT INTO leases VALUES(?,?,?)',(ident,domain,now));c.execute('INSERT OR REPLACE INTO domains VALUES(?,?)',(domain,now));c.commit();c.close();break
  c.rollback();c.close();time.sleep(.3)
 start=time.time();status=0;result=b'';error='';final=url
 try:
  with tempfile.TemporaryDirectory(dir=ROOT/'private_cache') as tmp:
   target=Path(tmp)/'body';inp=Path(tmp)/'payload';inp.write_bytes(payload)
   args=['curl','-sS','-L','--max-time',str(timeout),'--max-filesize',str(max_bytes),'-X',method,'-A','Auto2000CaseResearch/1.0 public secondary research','-o',str(target),'-w','%{http_code}\n%{url_effective}',url]
   for k,v in (headers or {}).items():args.extend(['-H',k+': '+v])
   if data is not None:args.extend(['--data-binary','@'+str(inp)])
   p=subprocess.run(args,capture_output=True,timeout=timeout+8)
   info=p.stdout.decode('utf8',errors='replace').splitlines();status=int(info[0]) if info and info[0].isdigit() else 0;final=info[-1] if len(info)>1 else url
   result=target.read_bytes() if target.exists() else b''
   if p.returncode:error=p.stderr.decode('utf8',errors='replace')[:400]
 except Exception as e:error=str(e)[:400]
 finally:
  c=db();c.execute('INSERT INTO requests VALUES(?,?,?,?,?,?,?,?,?,?,?)',(ident,domain,url,method,status,start,time.time()-start,len(result),error,key,final));c.execute('DELETE FROM leases WHERE id=?',(ident,));c.commit();c.close()
 m={'status':status,'request_id':ident,'final_url':final,'url':url,'method':method,'retrieved_utc_epoch':start,'elapsed':time.time()-start,'bytes':len(result),'error':error,'source':source}
 if status==200 and not error:body.write_bytes(result);meta.write_text(json.dumps(m))
 return Response(status,result,final,ident,False,error)
