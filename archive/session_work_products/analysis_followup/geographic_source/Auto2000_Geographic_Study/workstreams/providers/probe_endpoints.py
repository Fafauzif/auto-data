import urllib.request,urllib.parse,json,time,concurrent.futures,pathlib,datetime
ROOT=pathlib.Path(__file__).parent
q='[out:json][timeout:12];nwr["shop"="car_repair"](-7.30,112.72,-7.24,112.78);out center tags;'
urls=['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter','https://overpass.private.coffee/api/interpreter','https://overpass.osm.ch/api/interpreter','https://overpass.openstreetmap.fr/api/interpreter','https://overpass.nchc.org.tw/api/interpreter']
def run(u):
 t=time.time();row={'url':u,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'query':q}
 try:
  req=urllib.request.Request(u+'?'+urllib.parse.urlencode({'data':q}),headers={'User-Agent':'Mozilla/5.0'})
  x=urllib.request.urlopen(req,timeout=18).read();j=json.loads(x);row.update(status='success',bytes=len(x),elements=len(j.get('elements',[])));(ROOT/('probe_'+urllib.parse.urlparse(u).hostname+'.json')).write_bytes(x)
 except Exception as e:row.update(status='failed',error=str(e))
 row['seconds']=round(time.time()-t,2);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 out=list(pool.map(run,urls))
(ROOT/'endpoint_probe_log.json').write_text(json.dumps(out,indent=2))
for r in out:print(r,flush=True)
