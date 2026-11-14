from pathlib import Path
import json,pandas as pd,numpy as np
from shapely import from_wkb
from scipy.spatial import cKDTree
import pyarrow.parquet as pq
R=Path(__file__).resolve().parent;B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
d=pd.read_csv(R.parent/'branch_analysis/corrected/origin_channels_recomputed.csv');d=d[(d.scenario=='snap_le_250m')&d.oil_gap_minutes.notna()]
targets=[('Surabaya','A. Yani','AYani'),('Surabaya','Kertajaya','Kertajaya'),('Palembang','Tanjung Api','TanjungApiApi'),('Bandung','Soekarno','SoekarnoHatta')]
base=[]
for market,match,label in targets:
 s=d[(d.market==market)&d.auto2000_name.str.contains(match,regex=False)].sort_values('oil_gap_minutes')
 for i,k in enumerate(np.linspace(0,len(s)-1,6).round().astype(int)):
  x=s.iloc[k].to_dict();base.append({'market':market,'case':label,'baseline_origin_id':x['origin_id'],'baseline_longitude':x['longitude'],'baseline_latitude':x['latitude'],'baseline_oil_gap_minutes':x['oil_gap_minutes'],'baseline_nearest_branch':x['auto2000_name'],'baseline_auto2000_seconds':x['auto2000_seconds'],'baseline_oil_seconds':x['oil_network_seconds']})
pd.DataFrame(base).to_csv(R/'selected_baseline_origins.csv',index=False)
# Half a baseline grid-cell shift in both axes; a deliberately new origin layout.
orig=[]
for i,x in enumerate(base):
 m=x['market'];dx={'Surabaya':.20,'Palembang':.19,'Bandung':.23}[m]/18;dy={'Surabaya':.20,'Palembang':.19,'Bandung':.17}[m]/18
 orig.append({**x,'origin_id':f'shift_{x["case"]}_{i:02d}','origin_type':'half_cell_shift','longitude':x['baseline_longitude']+dx,'latitude':x['baseline_latitude']+dy})
# Independent bridge geometry, no assumed review-author homes.
for j,y in enumerate([-6.237,-6.259,-6.281]):
 for i,x in enumerate([106.765,106.780,106.795,106.810]):
  orig.append({'market':'JakartaBridge','case':'Cilandak-RadioDalam-Simprug','baseline_origin_id':'','origin_id':f'bridge_{j}_{i}','origin_type':'bridge_design_grid','longitude':x,'latitude':y})
for j,y in enumerate([-7.425,-7.445]):
 for i,x in enumerate([112.70,112.72,112.74]):orig.append({'market':'Surabaya','case':'Sidoarjo_extension','baseline_origin_id':'','origin_id':f'sidoarjo_{j}_{i}','origin_type':'southern_boundary_extension','longitude':x,'latitude':y})
pd.DataFrame(orig).to_csv(R/'shifted_and_bridge_targets.csv',index=False)
print(len(base),len(orig))
