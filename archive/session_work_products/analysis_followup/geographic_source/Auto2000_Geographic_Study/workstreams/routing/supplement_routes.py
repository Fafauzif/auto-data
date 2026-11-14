#!/usr/bin/env python3
"""Supplement the frozen mapped-garage comparison with separately documented channels."""
import csv,json,statistics
from pathlib import Path
from route_analysis import Client,grid,read_csv,write_csv
B=Path(__file__).resolve().parent

def run(config,dest_csv,out):
 cfg=json.loads(Path(config).read_text());dest=read_csv(dest_csv);client=Client('https://router.project-osrm.org',B/'cache',1.1);out=Path(out);out.mkdir(parents=True,exist_ok=True);pairs=[];summaries=[];errors=[]
 for m in cfg['markets']:
  origins=grid(m['bbox'],m.get('grid_n',9));dd=[d for d in dest if d['market'].lower()==m['market'].lower()]
  if not dd:continue
  for si in range(0,len(origins),27):
   oo=origins[si:si+27]
   try:x=client.table(oo,dd)
   except Exception as e:errors.append({'market':m['market'],'origin_start':si,'error':str(e)});continue
   for i,o in enumerate(oo):
    for j,d in enumerate(dd):
     pairs.append({'market':m['market'],'origin_id':o['origin_id'],'destination_id':d['destination_id'],'destination_name':d['name'],'kind':d['kind'],'source_url':d['source_url'],'duration_seconds':x['durations'][i][j],'distance_metres':x['distances'][i][j],'origin_snap_metres':x['sources'][i].get('distance',0),'destination_snap_metres':x['destinations'][j].get('distance',0),'capability_status':d.get('capability_status','network_advertised')})
  for o in origins:
   pp=[p for p in pairs if p['market']==m['market'] and p['origin_id']==o['origin_id'] and p['duration_seconds'] is not None]
   for scenario,limit in [('all_routed',float('inf')),('snap_le_250m',250)]:
    valid=[p for p in pp if p['origin_snap_metres']<=limit and p['destination_snap_metres']<=limit];r={'market':m['market'],'origin_id':o['origin_id'],'scenario':scenario,'expected_destinations':len(dd),'observed_pairs':len(pp)}
    for label,kinds in [('shopanddrive',{'shopanddrive'}),('domo',{'domo'}),('oil_chain',{'shopanddrive','domo'}),('other_authorized',{'other_authorized'}),('documented_network_paths',{'shopanddrive','other_authorized'})]:
     pool=[p for p in valid if p['kind'] in kinds]
     if pool:
      z=min(pool,key=lambda p:p['duration_seconds']);r[label+'_nearest_seconds']=z['duration_seconds'];r[label+'_destination_id']=z['destination_id']
     else:r[label+'_nearest_seconds']=None;r[label+'_destination_id']=''
    summaries.append(r)
  print(m['market'],len(origins),'origins',len(dd),'supplementary destinations',flush=True)
 write_csv(out/'supplement_od_pairs.csv',pairs);write_csv(out/'supplement_origin_accessibility.csv',summaries);(out/'supplement_acquisition_log.json').write_text(json.dumps(client.log,indent=2));(out/'supplement_failures.json').write_text(json.dumps(errors,indent=2))
 main=read_csv(B/'output/origin_accessibility.csv');lookup={(r['market'],r['origin_id'],r['scenario']):r for r in summaries};merged=[]
 for r in main:
  t=lookup.get((r['market'],r['origin_id'],r['scenario']),{});r.update({k:v for k,v in t.items() if k not in ('market','origin_id','scenario')});aa=[];oil=[]
  for field in ('auto2000_nearest_seconds','other_authorized_nearest_seconds'):
   if r.get(field) not in ('',None):aa.append(float(r[field]))
  for field in ('shopanddrive_nearest_seconds','otoxpert_nearest_seconds'):
   if r.get(field) not in ('',None):oil.append(float(r[field]))
  r['collected_toyota_authorized_nearest_seconds']=min(aa) if aa else None;r['collected_advertised_oil_channels_nearest_seconds']=min(oil) if oil else None
  # No route-equivalence claim: listed/advertised channels are not verified same-job quotes.
  if r.get('auto2000_nearest_seconds') not in ('',None) and oil:r['auto2000_minus_advertised_oil_channels_seconds']=float(r['auto2000_nearest_seconds'])-min(oil)
  else:r['auto2000_minus_advertised_oil_channels_seconds']=None
  merged.append(r)
 write_csv(out/'combined_origin_accessibility.csv',merged);agg=[]
 for name in dict.fromkeys(r['market'] for r in merged):
  for scenario in ('all_routed','snap_le_250m'):
   rr=[r for r in merged if r['market']==name and r['scenario']==scenario];a={'market':name,'scenario':scenario,'grid_origins':len(rr)}
   for label,field in [('shopanddrive','shopanddrive_nearest_seconds'),('domo','domo_nearest_seconds'),('oil_chain','oil_chain_nearest_seconds'),('auto2000','auto2000_nearest_seconds'),('other_authorized','other_authorized_nearest_seconds'),('collected_authorized','collected_toyota_authorized_nearest_seconds'),('advertised_oil_channels','collected_advertised_oil_channels_nearest_seconds')]:
    v=[float(r[field])/60 for r in rr if r.get(field) not in ('',None)];a[label+'_valid_origins']=len(v);a[label+'_median_minutes']=statistics.median(v) if v else None
    for th in (10,20,30):a[f'{label}_origins_le_{th}min']=sum(x<=th for x in v)
   v=[float(r['auto2000_minus_advertised_oil_channels_seconds'])/60 for r in rr if r['auto2000_minus_advertised_oil_channels_seconds'] not in ('',None)];a['median_paired_auto2000_minus_advertised_oil_minutes']=statistics.median(v) if v else None;agg.append(a)
 write_csv(out/'combined_market_summary.csv',agg)
 print(json.dumps(agg,indent=2))
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('config');a.add_argument('destinations');a.add_argument('--output',default=str(B/'supplement'));z=a.parse_args();run(z.config,z.destinations,z.output)
