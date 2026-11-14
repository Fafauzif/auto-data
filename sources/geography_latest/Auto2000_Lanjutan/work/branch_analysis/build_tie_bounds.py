from pathlib import Path
import pandas as pd
R=Path(__file__).resolve().parent
o=pd.read_csv(R/'corrected/origin_channels_recomputed.csv');o=o[o.scenario=='snap_le_250m'];b=pd.read_csv(R/'corrected/all_27_branches_recomputed.csv');b=b[b.scenario=='snap_le_250m'];out=[]
for _,z in b.iterrows():
 possible=o[(o.market==z.market)&o.nearest_tied_auto2000_ids.fillna('').str.split(';').map(lambda x:z.branch_id in x)]
 certain=possible[possible.nearest_tied_auto2000_count==1]
 out.append({'market':z.market,'branch_id':z.branch_id,'branch_name':z.branch_name,'baseline_assigned_n':z.nearest_origins_n,'unique_nearest_lower_n':len(certain),'possibly_nearest_upper_n':len(possible),'tail_gt5_lower_n':int((certain.oil_gap_minutes>5).sum()),'tail_gt5_upper_n':int((possible.oil_gap_minutes>5).sum()),'median_gap_excluding_ties_min':certain.oil_gap_minutes.median(),'median_gap_including_all_ties_min':possible.oil_gap_minutes.median(),'meaning':'Allocation bounds; possible upper counts must not be summed across branches'})
pd.DataFrame(out).to_csv(R/'tie_allocation_bounds.csv',index=False)
