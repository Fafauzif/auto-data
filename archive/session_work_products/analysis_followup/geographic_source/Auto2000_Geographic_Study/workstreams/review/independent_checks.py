"""Independent arithmetic and inventory checks. No network or source mutation."""
import csv,json,math,statistics,collections,random
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def read(p):
 with open(R/p,encoding='utf-8-sig') as f:return list(csv.DictReader(f))
checks=[]
def check(name,ok,detail):checks.append({'check':name,'pass':bool(ok),'detail':detail})
p=read('workstreams/providers/provider_inventory.csv');e=[x for x in p if x['eligible_candidate']=='True']
check('provider rows',len(p)==45202,str(len(p)))
check('unique source-market IDs',len({(x['market'],x['id']) for x in p})==len(p),'Source identifiers are per market; not people')
check('candidate count',len(e)==3359,str(len(e)))
check('all candidates job unverified',all('Unverified' in x['capability_status'] for x in e),'Capability descriptions retain uncertainty')
check('candidate source-confidence filter',all(float(x['confidence'])>=.7 for x in e),'Source confidence is not study validation probability')
check('candidate duplicate exclusions',all(not x['duplicate_of'] for x in e),'Probable duplicates preserved outside candidate pool')
check('coordinate ranges',all(-180<=float(x['longitude'])<=180 and -90<=float(x['latitude'])<=90 for x in p),'Global range check only')
b=read('workstreams/branches/official_branches_unique.csv');bd=read('workstreams/branches/routing_destinations.csv')
check('branch reconciled count',len(b)==131,str(len(b)))
check('branch routing exclusions',len(bd)==96,str(len(bd)))
check('branch geocode eligibility',all(x['coordinate_status']=='official_direction_candidate' for x in bd),'Official map candidates, no field verification')
sample=random.Random(1911).sample(e,60)
with (R/'workstreams/review/independent_candidate_sample.csv').open('w',newline='') as f:
 fields=['market','id','name','primary_category','confidence','explicit_car_name','ambiguous_motor_name','capability_status'];w=csv.DictWriter(f,fields);w.writeheader();w.writerows({k:x[k] for k in fields} for x in sample)
config=json.loads((R/'workstreams/routing/inputs/config.json').read_text());dests={}
for m in config['markets']:
 fp=Path(m['destinations_csv']);fp=fp if fp.is_absolute() else R/'workstreams/routing/inputs'/fp
 ds=list(csv.DictReader(open(fp)));dests[m['market']]=ds
 check('dest IDs '+m['market'],len({x['destination_id'] for x in ds})==len(ds),str(len(ds)))
 bounds=m['destination_bbox'];check('dest in bounds '+m['market'],all(bounds[0]<=float(x['longitude'])<=bounds[2] and bounds[1]<=float(x['latitude'])<=bounds[3] for x in ds),str(bounds))
out=R/'workstreams/routing/output'
if (out/'od_pairs.csv').exists():
 od=read('workstreams/routing/output/od_pairs.csv');orig=read('workstreams/routing/output/origins.csv');oa=read('workstreams/routing/output/origin_accessibility.csv');ms=read('workstreams/routing/output/market_summary.csv')
 expected=sum(m['grid_n']**2*len(dests[m['market']]) for m in config['markets'])
 check('OD row total',len(od)==expected,f'{len(od)} vs expected {expected}')
 check('OD unique keys',len({(x['market'],x['origin_id'],x['destination_id']) for x in od})==len(od),'One directed row per finite pair')
 check('origin count',len(orig)==sum(m['grid_n']**2 for m in config['markets']),str(len(orig)))
 check('origin scenario row count',len(oa)==2*len(orig),str(len(oa)))
 check('nonnegative duration and distance',all(float(x['duration_seconds'])>=0 and float(x['distance_metres'])>=0 for x in od if x['duration_seconds']), 'Missing routes kept separate')
 keyed=collections.defaultdict(list)
 for x in od:keyed[(x['market'],x['origin_id'])].append(x)
 for x in oa:
  ps=[p for p in keyed[(x['market'],x['origin_id'])] if p['duration_seconds']!='']
  if x['scenario']=='snap_le_250m':ps=[p for p in ps if float(p['origin_snap_metres'])<=250 and float(p['destination_snap_metres'])<=250]
  for label,kind in [('auto2000','auto2000'),('independent','independent')]:
   vv=[float(p['duration_seconds']) for p in ps if p['kind']==kind]
   expected_v=min(vv) if vv else None;actual=float(x[label+'_nearest_seconds']) if x[label+'_nearest_seconds'] else None
   if (expected_v is None)!=(actual is None) or expected_v is not None and abs(expected_v-actual)>1e-8:check('minimum mismatch',False,str((x['market'],x['origin_id'],x['scenario'],kind,expected_v,actual)))
 check('nearest arithmetic',not any(c['check']=='minimum mismatch' for c in checks),'Independently computed all-pair minima for each origin/scenario')
 for x in ms:
  rr=[r for r in oa if r['market']==x['market'] and r['scenario']==x['scenario']]
  dd=[float(r['auto2000_minus_mapped_independent_seconds'])/60 for r in rr if r['auto2000_minus_mapped_independent_seconds']!='']
  actual=float(x['median_paired_additional_minutes']) if x['median_paired_additional_minutes'] else None
  check('median paired '+x['market']+' '+x['scenario'],bool(dd) and abs(statistics.median(dd)-actual)<1e-9,str((len(dd),actual)))
  for label in ['auto2000','independent']:
   vv=[float(r[label+'_nearest_seconds'])/60 for r in rr if r[label+'_nearest_seconds']!=''];av=float(x[label+'_median_minutes']) if x[label+'_median_minutes'] else None
   check('median '+label+' '+x['market']+' '+x['scenario'],bool(vv) and abs(statistics.median(vv)-av)<1e-9,str((len(vv),av)))
   for th in (10,20,30):
    check('threshold '+label+' '+str(th)+' '+x['market']+' '+x['scenario'],sum(v<=th for v in vv)==int(x[label+'_origins_le_'+str(th)+'min']),str(sum(v<=th for v in vv)))
 check('documented capability not identified',all(x['job_comparable_alternative_identified']=='False' for x in oa),'Unknown qualified set, not absence of capable garages')
else:check('routing output available',False,'Pending: rerun reviewer script after routing ends')
receipt={'review_type':'Independent AI arithmetic and inventory review; no human/field validation','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'candidate_audit_sample':{'n':60,'seed':1911,'role':'Name/category anomaly inspection, not measured precision or representative field validation'}}
(R/'workstreams/review/INDEPENDENT_CHECKS.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt,indent=2))
