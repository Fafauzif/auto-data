from pathlib import Path
import pandas as pd,json
import urllib.request,time,hashlib
trace_log=[]
def get(path):
 u='https://router.project-osrm.org'+path;p=R/'cache'/(hashlib.sha256(u.encode()).hexdigest()+'.json')
 if p.exists():x=json.loads(p.read_text())
 else:
  time.sleep(1.2)
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Auto2000-public-geography-study/2.0'}),timeout=90) as r:data=r.read()
  p.write_bytes(data);x=json.loads(data)
 trace_log.append({'url':u,'cache_file':p.name});(R/'trace_acquisition_log.json').write_text(json.dumps(trace_log,indent=2));return x
R=Path(__file__).resolve().parent;B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
a=pd.read_csv(R.parent/'branch_analysis/corrected/origin_channels_recomputed.csv');a=a[(a.scenario=='snap_le_250m')&(a.market=='Palembang')]
orig=pd.read_csv(B/'workstreams/routing/output/origins.csv');d=pd.concat([pd.read_csv(B/'workstreams/routing/inputs/palembang_destinations.csv'),pd.read_csv(B/'workstreams/routing/inputs/supplement_destinations.csv')],ignore_index=True).drop_duplicates('destination_id')
features=[];records=[]
for branch,label in [('Tanjung Api','TAA_tail'),('Plaju','Plaju_control')]:
 pool=a[a.auto2000_name.str.contains(branch,regex=False)].sort_values('oil_gap_minutes');r=pool.iloc[-1];o=orig[(orig.market=='Palembang')&(orig.origin_id==r.origin_id)].iloc[0]
 for channel,field in [('auto2000','auto2000_id'),('oil_network','oil_network_id')]:
  z=d[d.destination_id==r[field]].iloc[0];coords=f'{o.longitude},{o.latitude};{z.longitude},{z.latitude}'
  x=get('/route/v1/driving/'+coords+'?overview=full&geometries=geojson&steps=true');rr=x['routes'][0];names=list(dict.fromkeys(step.get('name','') for leg in rr['legs'] for step in leg['steps'] if step.get('name')))
  record={'case':label,'origin_id':r.origin_id,'origin_longitude':o.longitude,'origin_latitude':o.latitude,'channel':channel,'destination_id':z.destination_id,'destination_name':z['name'],'duration_minutes':rr['duration']/60,'distance_km':rr['distance']/1000,'road_names':' | '.join(names),'road_name_mentions_bridge':any('jembatan' in n.lower() or 'ampera' in n.lower() for n in names),'note':'Roadnameabsence not proof of no crossing; route geometry included. No assumed river cause.'};records.append(record);features.append({'type':'Feature','geometry':rr['geometry'],'properties':record})
(R/'palembang_route_traces.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}));pd.DataFrame(records).to_csv(R/'palembang_route_trace_cases.csv',index=False);print(pd.DataFrame(records).to_string(index=False))
