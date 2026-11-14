#!/usr/bin/env python3
"""Data-integrity and geometry checks of acquired routing outputs."""
import csv,json,math
from pathlib import Path
from route_analysis import haversine
B=Path(__file__).resolve().parent
def rows(p):
 with open(p,encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def check(name,ok,detail=''):
 return {'check':name,'passed':bool(ok),'detail':detail}
def main():
 o=rows(B/'output/origins.csv');p=rows(B/'output/od_pairs.csv');s=rows(B/'output/origin_accessibility.csv');sn=rows(B/'output/snapping.csv');r=json.loads((B/'output/illustrative_routes.geojson').read_text());tests=[]
 tests.append(check('Origin identifiers unique within market',len({(x['market'],x['origin_id']) for x in o})==len(o),len(o)))
 tests.append(check('OD identifiers unique',len({(x['market'],x['origin_id'],x['destination_id']) for x in p})==len(p),len(p)))
 tests.append(check('Every acquired duration is nonnegative',all(float(x['duration_seconds'])>=0 for x in p if x['duration_seconds']!='')))
 tests.append(check('Every acquired distance is nonnegative',all(float(x['distance_metres'])>=0 for x in p if x['distance_metres']!='')))
 tests.append(check('All matrix batches complete for all origins',all(x['matrix_complete']=='True' for x in s)))
 tests.append(check('Route-status null handling consistent',all((x['duration_seconds']=='')==(x['route_status']=='unreachable') for x in p)))
 violation=[x for x in p if x['distance_metres'] and float(x['distance_metres'])+float(x['origin_snap_metres'])+float(x['destination_snap_metres'])+30 < float(x['straight_line_metres'])*.99]
 tests.append(check('Road distance plus snapping bounds straight-line distance (1pct+30m tolerance)',not violation,len(violation)))
 for group in ['auto2000','independent','otoxpert','non_auto2000','documented_alternative']:
  tests.append(check(f'{group}:10<=20<=30minute reachable-count monotonicity',all(int(x[f'{group}_count_le_10min'])<=int(x[f'{group}_count_le_20min'])<=int(x[f'{group}_count_le_30min']) for x in s)))
  a={(x['market'],x['origin_id']):x for x in s if x['scenario']=='all_routed'};strict=[x for x in s if x['scenario']=='snap_le_250m']
  bad=[]
  for x in strict:
   baseline=a[(x['market'],x['origin_id'])][group+'_nearest_seconds'];v=x[group+'_nearest_seconds']
   if v and baseline and float(v)<float(baseline)-1e-6:bad.append(x)
  tests.append(check(f'{group}:removing long snaps cannot improve nearest time',not bad,len(bad)))
  tests.append(check(f'{group}:expanding destinations cannot worsen nearest time',all(not x.get(group+'_expanded_minus_core_seconds') or float(x[group+'_expanded_minus_core_seconds'])<=1e-6 for x in s)))
 lengths=[]
 for f in r['features']:
  coords=f['geometry']['coordinates'];geolen=sum(haversine(a,b) for a,b in zip(coords,coords[1:]));lengths.append(abs(geolen-f['properties']['distance_metres'])/max(1,f['properties']['distance_metres']))
 tests.append(check('Illustrative route geometry agrees with supplied distance within5pct',all(x<=.05 for x in lengths),max(lengths,default=None)))
 tests.append(check('No job-qualified alternative inferred from empty evidence',all(x['job_comparable_alternative_identified']=='False' and x['documented_alternative_nearest_seconds']=='' for x in s)))
 receipt={'checks':tests,'passed':sum(x['passed'] for x in tests),'failed':sum(not x['passed'] for x in tests),'limitations':'Arithmetic/network checks only; not field verification, customer evidence or actual traffic validation.'}
 (B/'output/QA_RECEIPT.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
