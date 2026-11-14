#!/usr/bin/env python3
"""Recalculate descriptive candidate-inclusion sensitivity from acquired OD matrix."""
import csv,json,statistics
from pathlib import Path
B=Path(__file__).resolve().parent
def read(p):
 with open(p,encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def write(p,r):
 with open(p,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for x in r for k in x)));w.writeheader();w.writerows(r)
def main():
 cfg=json.loads((B/'inputs/portable_config.json').read_text());dest={}
 for m in cfg['markets']:
  for d in read((B/'inputs'/m['destinations_csv']) if not Path(m['destinations_csv']).is_absolute() else m['destinations_csv']):dest[(m['market'],d['destination_id'])]=d
 od=read(B/'output/od_pairs.csv');orig=read(B/'output/origins.csv');out=[];agg=[]
 modes=['baseline_candidates','source_confidence_ge_0.9','explicit_car_name','core_destinations_only','snap_le_100m','snap_le_500m','nested_5x5_origins','central_7x7_origins']
 for o in orig:
  ps=[p for p in od if p['market']==o['market'] and p['origin_id']==o['origin_id'] and p['duration_seconds'] not in ('',None)]
  for mode in modes:
   ix,jx=[int(z) for z in o['origin_id'].replace('g','').split('_')]
   if mode=='nested_5x5_origins' and not(ix%2==0 and jx%2==0):continue
   if mode=='central_7x7_origins' and not(1<=ix<=7 and 1<=jx<=7):continue
   pp=ps
   if mode.startswith('snap_le_'):
    lim=int(mode.split('_')[-1][:-1]);pp=[p for p in pp if float(p['origin_snap_metres'])<=lim and float(p['destination_snap_metres'])<=lim]
   if mode=='core_destinations_only':pp=[p for p in pp if p['destination_inside_origin_bbox']=='True']
   auto=[p for p in pp if p['kind']=='auto2000'];other=[p for p in pp if p['kind']=='independent']
   if mode=='source_confidence_ge_0.9':other=[p for p in other if float(dest[(o['market'],p['destination_id'])]['source_confidence'] or 0)>=.9]
   if mode=='explicit_car_name':other=[p for p in other if dest[(o['market'],p['destination_id'])]['explicit_car_name'].lower()=='true']
   a=min((float(p['duration_seconds'])/60 for p in auto),default=None);b=min((float(p['duration_seconds'])/60 for p in other),default=None)
   out.append({'market':o['market'],'origin_id':o['origin_id'],'scenario':mode,'auto2000_minutes':a,'mapped_candidate_minutes':b,'paired_additional_minutes':a-b if a is not None and b is not None else None,'candidate_count':len(other)})
 for market in dict.fromkeys(o['market'] for o in orig):
  for mode in modes:
   rr=[r for r in out if r['market']==market and r['scenario']==mode];aa=[r['auto2000_minutes'] for r in rr if r['auto2000_minutes'] is not None];bb=[r['mapped_candidate_minutes'] for r in rr if r['mapped_candidate_minutes'] is not None];dd=[r['paired_additional_minutes'] for r in rr if r['paired_additional_minutes'] is not None]
   agg.append({'market':market,'scenario':mode,'origins':len(rr),'paired_origins':len(dd),'median_auto2000_minutes':statistics.median(aa) if aa else None,'median_mapped_candidate_minutes':statistics.median(bb) if bb else None,'median_paired_additional_minutes':statistics.median(dd) if dd else None,'auto2000_le_20min':sum(v<=20 for v in aa),'candidate_le_20min':sum(v<=20 for v in bb)})
 write(B/'output/candidate_sensitivity_origins.csv',out);write(B/'output/candidate_sensitivity_summary.csv',agg)
 print(json.dumps(agg,indent=2))
if __name__=='__main__':main()
