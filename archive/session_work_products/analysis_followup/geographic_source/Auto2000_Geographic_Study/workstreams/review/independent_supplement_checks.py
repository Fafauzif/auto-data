"""Independent supplemental minima, pooling and median audit. No network."""
import csv,json,statistics,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2];S=R/'workstreams/routing/supplement'
def read(p):
 with open(p) as h:return list(csv.DictReader(h))
od=read(S/'supplement_od_pairs.csv');oa=read(S/'combined_origin_accessibility.csv');ms=read(S/'combined_market_summary.csv');g=collections.defaultdict(list);checks=[]
def ck(name,ok,detail=''):checks.append({'check':name,'pass':bool(ok),'detail':detail})
for p in od:g[p['market'],p['origin_id']].append(p)
ck('supplement rows',len(od)==5913,str(len(od)));ck('unique pairs',len({(p['market'],p['origin_id'],p['destination_id']) for p in od})==len(od));ck('combined origin scenarios',len(oa)==648,str(len(oa)))
for row in oa:
 pp=[p for p in g[row['market'],row['origin_id']] if p['duration_seconds']]
 if row['scenario']=='snap_le_250m':pp=[p for p in pp if float(p['origin_snap_metres'])<=250 and float(p['destination_snap_metres'])<=250]
 for kind in ['shopanddrive','domo','other_authorized']:
  vv=[float(p['duration_seconds']) for p in pp if p['kind']==kind];target=min(vv) if vv else None;actual=float(row[kind+'_nearest_seconds']) if row[kind+'_nearest_seconds'] else None
  ck('min '+kind,(target is None and actual is None) or target is not None and actual is not None and abs(target-actual)<1e-9,row['market']+' '+row['origin_id']+' '+row['scenario'])
 vals=[float(row[k]) for k in ['shopanddrive_nearest_seconds','otoxpert_nearest_seconds'] if row[k]]
 target=min(vals) if vals else None;actual=float(row['collected_advertised_oil_channels_nearest_seconds']) if row['collected_advertised_oil_channels_nearest_seconds'] else None
 ck('min OtoXpert plus ShopDrive',(target is None and actual is None) or target is not None and actual is not None and abs(target-actual)<1e-9,row['market']+' '+row['origin_id']+' '+row['scenario'])
for row in ms:
 rr=[p for p in oa if p['market']==row['market'] and p['scenario']==row['scenario']];gap=[]
 for p in rr:
  if p['auto2000_nearest_seconds'] and p['collected_advertised_oil_channels_nearest_seconds']:gap.append((float(p['auto2000_nearest_seconds'])-float(p['collected_advertised_oil_channels_nearest_seconds']))/60)
 ck('paired median '+row['market']+' '+row['scenario'],abs(statistics.median(gap)-float(row['median_paired_auto2000_minus_advertised_oil_minutes']))<1e-9,'paired n='+str(len(gap)))
 for label,col in [('shopanddrive','shopanddrive_nearest_seconds'),('advertised_oil_channels','collected_advertised_oil_channels_nearest_seconds')]:
  vv=[float(p[col])/60 for p in rr if p[col]]
  ck('channel median '+label+' '+row['market']+' '+row['scenario'],abs(statistics.median(vv)-float(row[label+'_median_minutes']))<1e-9)
  ck('valid n '+label+' '+row['market']+' '+row['scenario'],len(vv)==int(row[label+'_valid_origins']))
res={'type':'Independent AI audit of recorded supplemental route arithmetic, not field/job validation','checks':len(checks),'passed':sum(x['pass'] for x in checks),'failed':[x for x in checks if not x['pass']],'paired_n_by_market_scenario':[{'market':r['market'],'scenario':r['scenario'],'n':sum(bool(p['auto2000_nearest_seconds'] and p['collected_advertised_oil_channels_nearest_seconds']) for p in oa if p['market']==r['market'] and p['scenario']==r['scenario'])} for r in ms]}
(R/'workstreams/review/SUPPLEMENT_CHECK.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
