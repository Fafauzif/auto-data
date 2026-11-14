import csv,json,statistics,collections,math
from pathlib import Path
R=Path(__file__).resolve().parents[2]/'extracted'; B=R/'baseline/Auto2000_Geographic_Study';O=Path(__file__).parent
read=lambda p:list(csv.DictReader(open(p,encoding='utf-8-sig')))
main=read(B/'workstreams/routing/output/od_pairs.csv');ox=read(B/'workstreams/context/otoxpert_official_inventory.csv'); own={'otoxpert:'+x['provider_id'] for x in ox if x['auto2000_operator']=='True'}
sub=read(B/'workstreams/routing/supplement/supplement_od_pairs.csv');allpairs=main+sub
valid=[p for p in allpairs if p.get('duration_seconds') not in ('',None) and float(p['origin_snap_metres'])<=250 and float(p['destination_snap_metres'])<=250]
by=collections.defaultdict(list)
for p in valid:by[p['market'],p['origin_id']].append(p)
checks=[];branches=collections.defaultdict(list);markets=collections.defaultdict(list);network=collections.defaultdict(list)
for (m,o),ps in by.items():
 a=[p for p in ps if p['kind']=='auto2000'];g=[p for p in ps if p['kind']=='independent'];oil=[p for p in ps if p['kind'] in ['otoxpert','shopanddrive']]
 if not a or not g or not oil:continue
 aa=min(a,key=lambda p:float(p['duration_seconds']));tt=float(aa['duration_seconds']);gg=min(float(p['duration_seconds']) for p in g);oo=min(float(p['duration_seconds']) for p in oil)
 v={'market':m,'origin_id':o,'branch_id':aa['destination_id'],'branch_name':aa.get('destination_name'),'generic_gap_minutes':(tt-gg)/60,'oil_gap_minutes':(tt-oo)/60}
 branches[m,aa['destination_id']].append(v);markets[m].append(v)
 ooa=[float(p['duration_seconds']) for p in ps if p['destination_id'] in own];nextt=min([tt]+ooa)
 network[m].append({'origin_id':o,'base':tt,'combined':nextt,'saving':tt-nextt})
marketrows=[]
for m,vs in markets.items():
 marketrows.append({'market':m,'n':len(vs),'generic_gap_median':statistics.median(v['generic_gap_minutes'] for v in vs),'oil_gap_median':statistics.median(v['oil_gap_minutes'] for v in vs),'gap_gt5':sum(v['oil_gap_minutes']>5 for v in vs),'not_slower':sum(v['oil_gap_minutes']<=0 for v in vs)})
branchrows=[]
for (m,b),vs in branches.items():branchrows.append({'market':m,'branch_id':b,'branch_name':vs[0]['branch_name'],'n':len(vs),'median_oil_gap':statistics.median(v['oil_gap_minutes'] for v in vs),'gap_gt5':sum(v['oil_gap_minutes']>5 for v in vs),'origin_ids':';'.join(v['origin_id'] for v in vs)})
networkrows=[]
for m,vs in network.items():
 z={'market':m,'n':len(vs),'saved_gt1s':sum(v['saving']>1 for v in vs),'saved_gt1min':sum(v['saving']>60 for v in vs),'saved_gt2min':sum(v['saving']>120 for v in vs),'saved_gt5min':sum(v['saving']>300 for v in vs),'median_saved_all_minutes':statistics.median(v['saving']/60 for v in vs),'max_saved_minutes':max(v['saving']/60 for v in vs)}
 for th in [10,15,20,30]:z['additional_origins_le_'+str(th)+'min']=sum(v['combined']<=th*60 and v['base']>th*60 for v in vs)
 networkrows.append(z)
def write(n,rs):
 with (O/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
write('independent_market_seeds.csv',marketrows);write('independent_branch_seeds.csv',branchrows);write('independent_owned_otoxpert_marginal.csv',networkrows)
expected={x['market']:x for x in read(R/'reanalysis/market_reanalysis.csv')}
for r in marketrows:
 e=expected[r['market']]
 for a,b in [('n','paired_grid_origins'),('generic_gap_median','generic_gap_minutes'),('oil_gap_median','documented_oil_network_gap_minutes'),('gap_gt5','oil_gap_gt_5_minutes_origins'),('not_slower','auto2000_not_slower_origins')]:checks.append({'market':r['market'],'field':a,'actual':r[a],'expected':float(e[b]),'pass':abs(r[a]-float(e[b]))<1e-8})
(O/'SEED_AUDIT.json').write_text(json.dumps({'source':'Raw main and supplement OD rows, endpoint snapping<=250m, directly recomputed minima','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':sum(not c['pass'] for c in checks)},indent=2))
print(marketrows);print(networkrows)
