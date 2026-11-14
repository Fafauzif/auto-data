"""New targeted-origin and two-direction routing. Public OSRM profile; no observed traffic."""
from pathlib import Path
import sys,json,time,hashlib,urllib.request,csv,math
import pandas as pd,numpy as np
R=Path(__file__).resolve().parent;B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
(R/'cache').mkdir(exist_ok=True)
log=[];last=0

def get(path):
 global last
 u='https://router.project-osrm.org'+path;p=R/'cache'/(hashlib.sha256(u.encode()).hexdigest()+'.json')
 if p.exists():return json.loads(p.read_text())
 time.sleep(max(0,1.2-(time.monotonic()-last)));last=time.monotonic()
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Auto2000-public-geography-study/2.0'}),timeout=90) as res:d=res.read()
   x=json.loads(d)
   if x.get('code')!='Ok':raise ValueError(str(x)[:200])
   p.write_bytes(d);log.append({'url':u,'cache':p.name,'retrieved_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'status':'ok'});(R/'routing_log.json').write_text(json.dumps(log,indent=2));return x
  except Exception as e:
   log.append({'url':u,'attempt':attempt+1,'status':'error','error':str(e)});(R/'routing_log.json').write_text(json.dumps(log,indent=2));time.sleep(2)
 raise RuntimeError('Routing failed')

def table(src,dst):
 coords=src+dst;s=';'.join(f"{x['longitude']:.7f},{x['latitude']:.7f}" for x in coords);a=';'.join(map(str,range(len(src))));b=';'.join(map(str,range(len(src),len(coords))))
 return get(f'/table/v1/driving/{s}?sources={a}&destinations={b}&annotations=duration,distance')

def build_destinations():
 out=[];ox=pd.read_csv(B/'workstreams/context/otoxpert_official_inventory.csv').set_index('provider_id')
 for m in ['Surabaya','Bandung','Palembang']:
  a=pd.read_csv(B/f'workstreams/routing/inputs/{m.lower()}_destinations.csv');a=a[a.kind!='independent'].copy();a['market']=m
  s=pd.read_csv(B/'workstreams/routing/inputs/supplement_destinations.csv');s=s[(s.market==m)&s.kind.isin(['shopanddrive','other_authorized','domo'])];a=pd.concat([a,s],ignore_index=True)
  for _,r in a.iterrows():
   d=r.to_dict();d['operator']='Auto2000' if r.kind=='auto2000' else 'AstraOtoparts/Shop&Drive' if r.kind=='shopanddrive' else 'other documented network'
   if r.kind=='otoxpert':
    key=r.destination_id.split(':')[-1]
    if key in ox.index:d['operator']=ox.loc[key,'operator'];d['kind']='otoxpert_auto2000' if str(ox.loc[key,'auto2000_operator']).lower()=='true' else 'otoxpert_other'
   out.append(d)
 corr=pd.read_csv(R.parent/'coordinates/coordinate_corrections.csv')
 for _,r in corr.iterrows():out.append({'market':r.market,'destination_id':'corrected_'+r['name'].lower().replace(' ','_'),'name':r['name'],'longitude':r.new_longitude,'latitude':r.new_latitude,'kind':'auto2000','operator':'Auto2000','source_url':r.coordinate_source,'coordinate_status':r.new_status})
 # Bridge includes every collected documented channel in a generous southern Jakarta window.
 w,s,e,n=106.70,-6.36,106.88,-6.15
 a=pd.read_csv(B/'workstreams/branches/routing_destinations.csv');a=a[a.longitude.between(w,e)&a.latitude.between(s,n)]
 for i,r in a.iterrows():out.append({'market':'JakartaBridge','destination_id':'bridge_auto_'+str(i),'name':r['name'],'longitude':r.longitude,'latitude':r.latitude,'kind':'auto2000','operator':'Auto2000','source_url':r.source_url})
 a=pd.read_csv(B/'workstreams/providers/shopanddrive_official_all.csv');a=a[a.longitude.between(w,e)&a.latitude.between(s,n)]
 for _,r in a.iterrows():out.append({'market':'JakartaBridge','destination_id':r.provider_id,'name':r['name'],'longitude':r.longitude,'latitude':r.latitude,'kind':'shopanddrive','operator':'AstraOtoparts/Shop&Drive','source_url':r.source_url})
 for _,r in ox.reset_index().iterrows():
  if w<=r.longitude<=e and s<=r.latitude<=n:out.append({'market':'JakartaBridge','destination_id':r.provider_id,'name':r['name'],'longitude':r.longitude,'latitude':r.latitude,'kind':'otoxpert_auto2000' if str(r.auto2000_operator).lower()=='true' else 'otoxpert_other','operator':r.operator,'source_url':r.source_url})
 seen=set()
 for p in (R.parents[1]/'extracted/raw_inputs').glob('*Google*.json'):
  for r in json.loads(p.read_text()):
   if r['title'] in seen:continue
   seen.add(r['title']);loc=r['location'] or {};name=r['title']
   if r.get('permanentlyClosed') or not loc or not(w<=loc.get('lng',0)<=e and s<=loc.get('lat',0)<=n):continue
   if not any(t in name for t in ['Nawilis Radio Dalam','Otoklix Plus Simprug','Otoklix Ciputat']):continue
   out.append({'market':'JakartaBridge','destination_id':'review_listing_'+r['placeId'],'name':name,'longitude':loc['lng'],'latitude':loc['lat'],'kind':'local_documented','operator':'Nawilis' if 'Nawilis' in name else 'Otoklix','source_url':r['url'],'coordinate_status':'supplied Maps listing; not author residence'})
 df=pd.DataFrame(out).fillna('');df=df.drop_duplicates(['market','name','longitude','latitude']);df.to_csv(R/'new_destinations.csv',index=False);return df

def main():
 origins=pd.read_csv(R/'new_origins.csv').fillna('');dests=build_destinations();pairs=[]
 for m in origins.market.unique():
  oo=origins[origins.market==m].to_dict('records');dd=dests[dests.market==m].to_dict('records')
  for si in range(0,len(oo),20):
   src=oo[si:si+20]
   for di in range(0,len(dd),60):
    ds=dd[di:di+60]
    for direction in ['outbound','return']:
     a,b=(src,ds) if direction=='outbound' else (ds,src);x=table(a,b)
     for i,o in enumerate(src):
      for j,d in enumerate(ds):
       ii,jj=(i,j) if direction=='outbound' else (j,i)
       pairs.append({'market':m,'origin_id':o['origin_id'],'destination_id':d['destination_id'],'destination_name':d['name'],'kind':d['kind'],'operator':d['operator'],'direction':direction,'duration_seconds':x['durations'][ii][jj],'distance_metres':x['distances'][ii][jj],'origin_snap_metres':x['sources'][i]['distance'] if direction=='outbound' else x['destinations'][i]['distance'],'destination_snap_metres':x['destinations'][j]['distance'] if direction=='outbound' else x['sources'][j]['distance']})
    pd.DataFrame(pairs).to_csv(R/'new_bidirectional_od.csv',index=False);print(m,si,len(src),di,len(ds),'done',flush=True)
 print('new directional OD',len(pairs),flush=True)
if __name__=='__main__':main()
