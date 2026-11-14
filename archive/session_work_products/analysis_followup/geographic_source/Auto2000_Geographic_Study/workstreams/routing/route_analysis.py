#!/usr/bin/env python3
"""Bounded, cached, explicitly sampled OSRM routing comparison. Standard library only.
Input JSON: markets list, each {market,bbox:[w,s,e,n], destinations_csv, grid_n:8}.
Destination CSV fields: destination_id,name,longitude,latitude,kind,capability_status,source_url.
kind: auto2000 / independent / otoxpert / other_authorized / other.
No customer counts, speeds, demand or observed traffic inferred.
"""
import argparse,csv,hashlib,json,math,os,time,statistics,urllib.request,urllib.error
from pathlib import Path

BASE=Path(__file__).resolve().parent

def read_csv(p):
 with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def write_csv(p,rows,fields=None):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if fields is None: fields=list(dict.fromkeys(k for r in rows for k in r))
 with p.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def haversine(a,b):
 x,y=map(math.radians,a);u,v=map(math.radians,b)
 return 6371008.8*2*math.asin(min(1,math.sqrt(math.sin((y-v)/2)**2+math.cos(y)*math.cos(v)*math.sin((x-u)/2)**2)))
def grid(bbox,n):
 w,s,e,no=bbox
 # cell centres, not administrative centroids or sampled customer homes
 return [{'origin_id':f'g{i:02d}_{j:02d}','longitude':w+(i+.5)*(e-w)/n,'latitude':s+(j+.5)*(no-s)/n,'origin_type':'regular_grid_cell_centre'} for j in range(n) for i in range(n)]
class Client:
 def __init__(self,base,cache,pause=1.1):
  self.base=base.rstrip('/');self.cache=Path(cache);self.cache.mkdir(parents=True,exist_ok=True);self.pause=pause;self.last=0;self.log=[]
 def get(self,path):
  url=self.base+path;k=hashlib.sha256(url.encode()).hexdigest();p=self.cache/(k+'.json')
  if p.exists():
   x=json.loads(p.read_text());self.log.append({'url':url,'cache_file':str(p),'cached':True,'status':'Ok'});return x
  err=''
  for attempt in range(3):
   time.sleep(max(0,self.pause-(time.monotonic()-self.last)));self.last=time.monotonic()
   try:
    req=urllib.request.Request(url,headers={'User-Agent':'Auto2000-Geographic-Research/1.0 (bounded academic/public-data analysis)'})
    with urllib.request.urlopen(req,timeout=90) as r:raw=r.read();status=r.status
    x=json.loads(raw)
    if x.get('code')!='Ok':raise RuntimeError(json.dumps(x)[:500])
    p.write_bytes(raw)
    self.log.append({'url':url,'cache_file':str(p),'cached':False,'status':status,'retrieved_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    return x
   except Exception as e:
    err=str(e);self.log.append({'url':url,'cached':False,'status':'failed','attempt':attempt+1,'error':err});time.sleep(2*(attempt+1))
  raise RuntimeError(err)
 def table(self,origins,dests):
  coords=origins+dests
  coordinate=';'.join(f"{float(x['longitude']):.7f},{float(x['latitude']):.7f}" for x in coords)
  sources=';'.join(map(str,range(len(origins))));destinations=';'.join(map(str,range(len(origins),len(coords))))
  return self.get(f'/table/v1/driving/{coordinate}?sources={sources}&destinations={destinations}&annotations=duration,distance')
 def route(self,origin,dest):
  return self.get(f"/route/v1/driving/{origin['longitude']},{origin['latitude']};{dest['longitude']},{dest['latitude']}?overview=full&geometries=geojson&steps=false")

def analyse(config,out,client):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);allpairs=[];allorig=[];allsummary=[];allsnap=[];failures=[];selected=[];routefeatures=[];configbase=Path(config).resolve().parent
 cfg=json.loads(Path(config).read_text())
 for market in cfg['markets']:
  name=market['market'];n=market.get('grid_n',8);origins=grid(market['bbox'],n)
  dpath=Path(market['destinations_csv']);dpath=dpath if dpath.is_absolute() else configbase/dpath
  dests=read_csv(dpath)
  if not dests: failures.append({'market':name,'error':'No destinations'});continue
  ids=[d['destination_id'] for d in dests]
  if len(ids)!=len(set(ids)):raise ValueError(f'duplicate destinations: {name}')
  for o in origins:o['market']=name
  for d in dests:
   d['inside_origin_bbox']=market['bbox'][0]<=float(d['longitude'])<=market['bbox'][2] and market['bbox'][1]<=float(d['latitude'])<=market['bbox'][3]
  allorig.extend(origins);pairs=[]
  for si in range(0,len(origins),27):
   oo=origins[si:si+27]
   for di in range(0,len(dests),70):
    dd=dests[di:di+70]
    try:x=client.table(oo,dd)
    except Exception as e:
     failures.append({'market':name,'origin_start':si,'dest_start':di,'error':str(e)});continue
    for ix,o in enumerate(oo):
     sw=x['sources'][ix];sn=sw.get('distance',0)
     if di==0:allsnap.append({'market':name,'record_type':'origin','record_id':o['origin_id'],'snap_metres':sn,'snap_longitude':sw['location'][0],'snap_latitude':sw['location'][1]})
     for jx,d in enumerate(dd):
      dw=x['destinations'][jx];dur=x['durations'][ix][jx];dist=x['distances'][ix][jx]
      if si==0:allsnap.append({'market':name,'record_type':'destination','record_id':d['destination_id'],'snap_metres':dw.get('distance',0),'snap_longitude':dw['location'][0],'snap_latitude':dw['location'][1]})
      pair={'market':name,'origin_id':o['origin_id'],'destination_id':d['destination_id'],'destination_name':d['name'],'kind':d['kind'],'capability_status':d.get('capability_status','unverified'),'destination_inside_origin_bbox':d['inside_origin_bbox'],'duration_seconds':dur,'distance_metres':dist,'origin_snap_metres':sn,'destination_snap_metres':dw.get('distance',0),'route_status':'routed' if dur is not None else 'unreachable','straight_line_metres':round(haversine((o['longitude'],o['latitude']),(float(d['longitude']),float(d['latitude']))),2)}
      pairs.append(pair)
  allpairs.extend(pairs)
  for o in origins:
   op=[p for p in pairs if p['origin_id']==o['origin_id'] and p['duration_seconds'] is not None]
   # Strict snap screen reported as a scenario, not proof of a wrong location
   for scenario,maxsnap in [('all_routed',float('inf')),('snap_le_250m',250)]:
    pp=[p for p in op if p['origin_snap_metres']<=maxsnap and p['destination_snap_metres']<=maxsnap]
    row={'market':name,'origin_id':o['origin_id'],'scenario':scenario,'longitude':o['longitude'],'latitude':o['latitude'],'pair_rows_expected':len(dests),'pair_rows_observed':len([p for p in pairs if p['origin_id']==o['origin_id']]),'routed_candidates':len(pp),'matrix_complete':len([p for p in pairs if p['origin_id']==o['origin_id']])==len(dests),'job_comparable_alternative_identified':any(d.get('capability_status')=='documented' and d['kind']!='auto2000' for d in dests)}
    for group,kinds in [('auto2000',{'auto2000'}),('independent',{'independent'}),('non_auto2000',{'independent','otoxpert','other_authorized','other'}),('documented_alternative',{'independent','otoxpert','other_authorized','other'}),('otoxpert',{'otoxpert'})]:
     pool=[p for p in pp if p['kind'] in kinds and (group!='documented_alternative' or p['capability_status']=='documented')]
     if pool:
      best=min(pool,key=lambda p:p['duration_seconds'])
      row[group+'_nearest_seconds']=best['duration_seconds'];row[group+'_nearest_metres']=best['distance_metres'];row[group+'_destination_id']=best['destination_id'];row[group+'_nearest_outside_origin_bbox']=not best['destination_inside_origin_bbox']
      core=[p for p in pool if p['destination_inside_origin_bbox']]
      row[group+'_core_only_nearest_seconds']=min(p['duration_seconds'] for p in core) if core else None
      row[group+'_expanded_minus_core_seconds']=best['duration_seconds']-row[group+'_core_only_nearest_seconds'] if core else None
      for threshold in (10,20,30):row[f'{group}_count_le_{threshold}min']=sum(p['duration_seconds']<=threshold*60 for p in pool)
     else:
      row[group+'_nearest_seconds']=None;row[group+'_nearest_metres']=None;row[group+'_destination_id']='';row[group+'_nearest_outside_origin_bbox']=None;row[group+'_core_only_nearest_seconds']=None;row[group+'_expanded_minus_core_seconds']=None
      for threshold in (10,20,30):row[f'{group}_count_le_{threshold}min']=0
    if row['auto2000_nearest_seconds'] is not None and row['independent_nearest_seconds'] is not None:row['auto2000_minus_mapped_independent_seconds']=row['auto2000_nearest_seconds']-row['independent_nearest_seconds']
    else:row['auto2000_minus_mapped_independent_seconds']=None
    allsummary.append(row)
  # Illustrative paths: extreme and median travel gaps, not all journeys
  mr=[r for r in allsummary if r['market']==name and r['scenario']=='all_routed' and r['auto2000_minus_mapped_independent_seconds'] is not None]
  if mr and cfg.get('illustrative_routes',True):
   mr.sort(key=lambda r:r['auto2000_minus_mapped_independent_seconds'])
   for label,r in [('minimum_gap',mr[0]),('median_gap',mr[len(mr)//2]),('maximum_gap',mr[-1])]:
    o=next(z for z in origins if z['origin_id']==r['origin_id'])
    for kind in ('auto2000','independent'):
     d=next(z for z in dests if z['destination_id']==r[kind+'_destination_id'])
     try:
      rr=client.route(o,d)['routes'][0]
      routefeatures.append({'type':'Feature','geometry':rr['geometry'],'properties':{'market':name,'example':label,'kind':kind,'origin_id':o['origin_id'],'destination_id':d['destination_id'],'destination_name':d['name'],'duration_seconds':rr['duration'],'distance_metres':rr['distance'],'weight':rr.get('weight'),'weight_name':rr.get('weight_name')}})
     except Exception as e:failures.append({'market':name,'example':label,'kind':kind,'error':str(e)})
  print(f'{name}: {len(origins)} origins x {len(dests)} destinations; {len(pairs)} pair rows',flush=True)
 aggregates=[]
 for name in dict.fromkeys(r['market'] for r in allsummary):
  for scenario in ('all_routed','snap_le_250m'):
   rows=[r for r in allsummary if r['market']==name and r['scenario']==scenario]
   a={'market':name,'scenario':scenario,'grid_origins':len(rows),'complete_matrix_origins':sum(r['matrix_complete'] for r in rows)}
   for group in ('auto2000','independent','non_auto2000','documented_alternative','otoxpert'):
    v=[r[group+'_nearest_seconds']/60 for r in rows if r[group+'_nearest_seconds'] is not None]
    a[group+'_valid_origins']=len(v);a[group+'_median_minutes']=statistics.median(v) if v else None
    for th in (10,20,30):a[f'{group}_origins_le_{th}min']=sum(x<=th for x in v)
    a[group+'_nearest_outside_origin_bbox_origins']=sum(r.get(group+'_nearest_outside_origin_bbox')==True for r in rows)
   delta=[r['auto2000_minus_mapped_independent_seconds']/60 for r in rows if r['auto2000_minus_mapped_independent_seconds'] is not None]
   a['paired_origins']=len(delta);a['median_paired_additional_minutes']=statistics.median(delta) if delta else None;a['origins_auto2000_faster']=sum(d<0 for d in delta);a['origins_auto2000_slower']=sum(d>0 for d in delta)
   aggregates.append(a)
 write_csv(out/'market_summary.csv',aggregates)
 write_csv(out/'origins.csv',allorig);write_csv(out/'od_pairs.csv',allpairs);write_csv(out/'origin_accessibility.csv',allsummary);write_csv(out/'snapping.csv',allsnap);write_csv(out/'failures.csv',failures,['market','origin_start','dest_start','example','kind','error'])
 (out/'illustrative_routes.geojson').write_text(json.dumps({'type':'FeatureCollection','features':routefeatures}))
 (out/'acquisition_log.json').write_text(json.dumps(client.log,indent=2))
 (out/'run_receipt.json').write_text(json.dumps({'config':str(config),'config_sha256':hashlib.sha256(Path(config).read_bytes()).hexdigest(),'origins':len(allorig),'od_pairs':len(allpairs),'summary_rows':len(allsummary),'requests_logged':len(client.log),'failures':len(failures),'date_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'routing':'OSRM public driving profile; duration values, not route weight; modelled baseline not live traffic','scope':'Finite listed destinations only; mapped independent garages not verified comparable-job providers; regular grid not population/customer sample'},indent=2))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--output',default=str(BASE/'output'));ap.add_argument('--cache',default=str(BASE/'cache'));ap.add_argument('--endpoint',default='https://router.project-osrm.org');ap.add_argument('--pause',type=float,default=1.1);a=ap.parse_args()
 analyse(a.config,a.output,Client(a.endpoint,a.cache,a.pause))
