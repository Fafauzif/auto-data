from pathlib import Path
import sys,sqlite3,json,hashlib,time,concurrent.futures
from public_http import ROOT,Response
import site_collect_v3 as collector

def offline_fetch(url,**kwargs):
 key=hashlib.sha256(b'GET\n'+url.encode()+b'\n').hexdigest();b=ROOT/'private_cache/http'/(key+'.bin');m=ROOT/'private_cache/http'/(key+'.json')
 if not b.exists() or not m.exists():raise RuntimeError('Offline cache unavailable; no network request attempted: '+url)
 x=json.loads(m.read_text());return Response(x['status'],b.read_bytes(),x['final_url'],x['request_id'],True,x.get('error',''))
collector.fetch=offline_fetch
c=collector.database();rows=list(c.execute('SELECT url,selection FROM pages WHERE status=200'));c.close()
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(collector.collect,rows))
print('OFFLINE V3 REPARSE',len(rows),'No network calls',flush=True)
