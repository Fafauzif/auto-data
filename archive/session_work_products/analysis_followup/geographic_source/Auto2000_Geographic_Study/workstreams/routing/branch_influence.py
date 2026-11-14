#!/usr/bin/env python3
"""Finite-inventory branch catchments and leave-one-out access sensitivity.
This is a geographic sensitivity, never a closure, capacity or revenue recommendation.
"""
import csv,json,statistics
from pathlib import Path
from route_analysis import read_csv,write_csv
B=Path(__file__).resolve().parent

def main():
 cfg=json.loads((B/'inputs/portable_config.json').read_text());pairs=read_csv(B/'output/od_pairs.csv');out=[]
 for m in cfg['markets']:
  path=Path(m['destinations_csv']);path=path if path.is_absolute() else B/'inputs'/path
  branches=[d for d in read_csv(path) if d['kind']=='auto2000'];market=m['market'];mp=[p for p in pairs if p['market']==market and p['duration_seconds']!='']
  for scenario,lim in [('all_routed',float('inf')),('snap_le_250m',250)]:
   pp=[p for p in mp if float(p['origin_snap_metres'])<=lim and float(p['destination_snap_metres'])<=lim];origins=sorted(set(p['origin_id'] for p in pp));byorigin={o:[p for p in pp if p['origin_id']==o] for o in origins}
   for b in branches:
    nearest=[];times=[];deltas=[];lost20=0;worsening=[];within20=0
    for o,op in byorigin.items():
     a=[p for p in op if p['kind']=='auto2000'];own=[p for p in a if p['destination_id']==b['destination_id']]
     if own and float(own[0]['duration_seconds'])<=1200:within20+=1
     if not a:continue
     best=min(a,key=lambda p:float(p['duration_seconds']));without=[p for p in a if p['destination_id']!=b['destination_id']]
     if best['destination_id']==b['destination_id']:
      nearest.append(o);times.append(float(best['duration_seconds'])/60)
      alternatives=[p for p in op if p['kind']=='independent']
      if alternatives:deltas.append((float(best['duration_seconds'])-min(float(p['duration_seconds']) for p in alternatives))/60)
     if without:
      new=min(float(p['duration_seconds']) for p in without);old=float(best['duration_seconds']);worsening.append((new-old)/60)
      if old<=1200<new:lost20+=1
     elif float(best['duration_seconds'])<=1200:lost20+=1
    out.append({'market':market,'scenario':scenario,'branch_id':b['destination_id'],'branch_name':b['name'],'latitude':b['latitude'],'longitude':b['longitude'],'valid_grid_origins':len(origins),'origins_nearest_this_branch':len(nearest),'origins_within20min_this_branch':within20,'median_minutes_when_nearest':statistics.median(times) if times else None,'median_paired_gap_vs_mapped_candidates_when_nearest':statistics.median(deltas) if deltas else None,'origins_losing20min_access_if_removed':lost20,'maximum_additional_minutes_if_removed':max(worsening,default=None),'median_additional_minutes_all_origins_if_removed':statistics.median(worsening) if worsening else None,'origins_with_positive_increase_if_removed':sum(v>1/60 for v in worsening),'median_additional_minutes_affected_origins_if_removed':statistics.median([v for v in worsening if v>1/60]) if any(v>1/60 for v in worsening) else None,'interpretation':'Finite-grid leave-one-out access sensitivity; not workload, actual trade area, capacity or closure economics'})
 write_csv(B/'output/branch_influence.csv',out)
 focal=[]
 for market in dict.fromkeys(r['market'] for r in out):
  pool=[r for r in out if r['market']==market and r['scenario']=='snap_le_250m'];pool.sort(key=lambda r:(r['origins_nearest_this_branch'],r['maximum_additional_minutes_if_removed'] or 0),reverse=True)
  for rank,r in enumerate(pool[:3],1):focal.append({**r,'focal_rank_within_market':rank,'selection_rule':'Top3 branches by nearest screened grid origins; ties maximum leave-one-out access increase'})
 write_csv(B/'output/focal12_branches.csv',focal)
 print('Branch influence rows',len(out),'focal branches',len(focal))
if __name__=='__main__':main()
