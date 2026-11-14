"""Independently recompute focal-branch geometry from saved OD rows, no network."""
import csv,json,collections
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def read(f):
 with (R/'workstreams/routing/output'/f).open() as h:return list(csv.DictReader(h))
od=read('od_pairs.csv');bi=read('branch_influence.csv');fo=read('focal12_branches.csv');g=collections.defaultdict(list)
for p in od:
 if p['duration_seconds']:g[(p['market'],p['origin_id'])].append(p)
errors=[]
for r in bi:
 limit=250 if r['scenario']=='snap_le_250m' else float('inf');nearest=0;within20=0;loss=0;worsen=[]
 for (market,o),ps in g.items():
  if market!=r['market']:continue
  ps=[p for p in ps if float(p['origin_snap_metres'])<=limit and float(p['destination_snap_metres'])<=limit and p['kind']=='auto2000']
  if not ps:continue
  best=min(ps,key=lambda x:float(x['duration_seconds']));own=[p for p in ps if p['destination_id']==r['branch_id']]
  if best['destination_id']==r['branch_id']:nearest+=1
  if own and float(own[0]['duration_seconds'])<=1200:within20+=1
  wo=[p for p in ps if p['destination_id']!=r['branch_id']]
  if wo:
   new=min(float(p['duration_seconds']) for p in wo);old=float(best['duration_seconds']);worsen.append((new-old)/60)
   if old<=1200<new:loss+=1
  elif float(best['duration_seconds'])<=1200:loss+=1
 for k,v in [('origins_nearest_this_branch',nearest),('origins_within20min_this_branch',within20),('origins_losing20min_access_if_removed',loss)]:
  if int(r[k])!=v:errors.append((r['market'],r['branch_name'],k,v,r[k]))
 if worsen and abs(float(r['maximum_additional_minutes_if_removed'])-max(worsen))>1e-9:errors.append(('maxloss',r))
res={'branch_rows':len(bi),'focal_rows':len(fo),'checks':len(bi)*4,'errors':errors,'interpretation':'Leave-one-out finite-grid geometry, not actual customer catchments or closure economics'}
(R/'workstreams/review/BRANCH_INFLUENCE_CHECK.json').write_text(json.dumps(res,indent=2));print(json.dumps(res))
