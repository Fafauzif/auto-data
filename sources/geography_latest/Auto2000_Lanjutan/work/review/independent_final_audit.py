import csv,json,statistics,collections,math
from pathlib import Path
W=Path(__file__).resolve().parents[1];R=W.parent/'extracted';B=R/'baseline/Auto2000_Geographic_Study';O=Path(__file__).parent
read=lambda p:list(csv.DictReader(open(p,encoding='utf-8-sig')))
checks=[]
def check(n,a,b,tol=1e-8):
 ok=(a==b) if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) else abs(a-b)<tol
 checks.append({'check':n,'actual':a,'expected':b,'pass':ok})
def num(x):return float(x) if x not in ('',None) else None
def eq(a,b):return a==b if a is None or b is None or isinstance(a,str) or isinstance(b,str) else abs(a-b)<1e-8
main=read(B/'workstreams/routing/output/od_pairs.csv');supp=read(B/'workstreams/routing/supplement/supplement_od_pairs.csv');corr=[p for p in read(W/'coordinates/corrected_endpoint_od.csv') if p['direction']=='outbound'];own={'otoxpert:'+x['provider_id'] for x in read(B/'workstreams/context/otoxpert_official_inventory.csv') if x['auto2000_operator']=='True'}
ps=main+supp+corr;by=collections.defaultdict(list)
for p in ps:
 if p.get('duration_seconds') not in ('',None):by[p['market'],p['origin_id']].append(p)
calc={}
for sc,lim in [('all_routed',float('inf')),('snap_le_250m',250)]:
 for (m,o),ls in by.items():
  vv=[p for p in ls if float(p['origin_snap_metres'])<=lim and float(p['destination_snap_metres'])<=lim]
  pools={'auto2000':[p for p in vv if p['kind']=='auto2000'],'oil_network':[p for p in vv if p['kind'] in ['otoxpert','shopanddrive']],'owned_oil_network':[p for p in vv if p['kind']=='auto2000' or p['destination_id'] in own]}
  z={}
  for kind,pool in pools.items():
   pp=sorted(pool,key=lambda p:(float(p['duration_seconds']),p['destination_id']));z[kind+'_seconds']=float(pp[0]['duration_seconds']) if pp else None;z[kind+'_id']=pp[0]['destination_id'] if pp else ''
   if kind=='auto2000':z['second_auto2000_seconds']=float(pp[1]['duration_seconds']) if len(pp)>1 else None
  if all(z[k+'_seconds'] is not None for k in ['auto2000','oil_network','owned_oil_network']):
   z['oil_gap_minutes']=(z['auto2000_seconds']-z['oil_network_seconds'])/60;z['owned_network_gap_minutes']=(z['owned_oil_network_seconds']-z['oil_network_seconds'])/60
  calc[m,o,sc]=z
rows=read(W/'branch_analysis/corrected/origin_channels_recomputed.csv');errors=[]
for r in rows:
 z=calc[r['market'],r['origin_id'],r['scenario']]
 for field in ['auto2000_seconds','auto2000_id','oil_network_seconds','oil_network_id','owned_oil_network_seconds','second_auto2000_seconds']:
  v=num(r[field]) if field.endswith('seconds') else r[field]
  if field=='auto2000_id' and v in r.get('nearest_tied_auto2000_ids','').split(';'):continue
  if not eq(z[field],v):errors.append({'key':[r['market'],r['origin_id'],r['scenario']],'field':field,'actual':v,'expected':z[field]})
check('corrected origin minimum comparisons',len(errors),0)
check('corrected origin rows',len(rows),648)
br=read(W/'branch_analysis/corrected/all_27_branches_recomputed.csv');check('corrected branch count',len({p['branch_id'] for p in br}),29)
strict=[(k,z) for k,z in calc.items() if k[2]=='snap_le_250m' and z.get('oil_gap_minutes') is not None]
markets=[]
for m in ['Surabaya','Medan','Bandung','Palembang']:
 vals=[z for k,z in strict if k[0]==m];out={'market':m,'n':len(vals),'oil_gap_median':statistics.median(z['oil_gap_minutes'] for z in vals),'baseline_tail_gt5':sum(z['oil_gap_minutes']>5 for z in vals),'owned_tail_gt5':sum(z['owned_network_gap_minutes']>5 for z in vals)};markets.append(out)
 if m=='Bandung':check('Bandung corrected gap',out['oil_gap_median'],1.735833333333)
 if m=='Palembang':check('Palembang own-OX tail',out['owned_tail_gt5'],0);check('Palembang baseline tail',out['baseline_tail_gt5'],9)
# Independent access trip optimisation, preserving direction and endpoint screens.
od=read(W/'access/new_bidirectional_od.csv');dest={r['destination_id']:r for r in read(W/'access/new_destinations.csv')};odmap=collections.defaultdict(dict)
for p in od:odmap[p['market'],p['origin_id'],p['destination_id']][p['direction']]=p
check('new OD identifiers unique',len({(p['market'],p['origin_id'],p['destination_id'],p['direction']) for p in od}),len(od));check('new OD count',len(od),5604)
check('new origins count',len({(p['market'],p['origin_id']) for p in od}),66)
trips=read(W/'access/origin_trip_scenarios.csv');terr=[]
for r in trips:
 lim=250 if r['scenario']=='snap_le_250m' else float('inf');mm={}
 for (m,o,d),dd in odmap.items():
  if m!=r['market'] or o!=r['origin_id'] or len(dd)!=2:continue
  if any(num(p['duration_seconds']) is None or max(float(p['origin_snap_metres']),float(p['destination_snap_metres']))>lim for p in dd.values()):continue
  out=float(dd['outbound']['duration_seconds'])/60;ret=float(dd['return']['duration_seconds'])/60
  mm[d]={'out':out,'return':ret,'rt':out+ret,'kind':dest[d]['kind']}
 for group,kinds in [('auto2000',{'auto2000'}),('oil_network',{'otoxpert_auto2000','otoxpert_other','shopanddrive'})]:
  pp=[(d,z) for d,z in mm.items() if z['kind'] in kinds]
  expected_rt=min((z['rt'] for d,z in pp),default=None);expected_out=min((z['out'] for d,z in pp),default=None)
  for field,value in [(group+'_roundtrip_minutes',expected_rt),(group+'_outbound_optimized_minutes',expected_out)]:
   actual=num(r[field])
   if not eq(actual,value):terr.append({'origin':r['origin_id'],'scenario':r['scenario'],'field':field,'actual':actual,'expected':value})
 if num(r['auto2000_roundtrip_minutes']) is not None and num(r['oil_network_roundtrip_minutes']) is not None:
  a=float(r['auto2000_roundtrip_minutes']);b=float(r['oil_network_roundtrip_minutes'])
  for field,value in [('roundtrip_gap_minutes',a-b),('auto_two_visits_vs_competitor_one_visit_gap',2*a-b),('dropoff_collect_customer_road_minutes_same_profile',2*a)]:
   if not eq(num(r[field]),value):terr.append({'origin':r['origin_id'],'field':field,'actual':r[field],'expected':value})
check('new access independent optimisation and trip arithmetic errors',len(terr),0)
report={'checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks),'corrected_minima_comparisons':len(rows)*6,'access_comparisons':len(trips)*7,'corrected_errors':errors[:20],'access_errors':terr[:20],'corrected_market_results':markets}
(O/'FINAL_ARITHMETIC_AUDIT.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
