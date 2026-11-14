from pathlib import Path
import json,pandas as pd,numpy as np
R=Path(__file__).resolve().parent
p=pd.read_csv(R/'new_bidirectional_od.csv');o=pd.read_csv(R/'new_origins.csv');rows=[]
for (market,oid),g in p.groupby(['market','origin_id'],sort=False):
 out=g[g.direction=='outbound'].set_index('destination_id');back=g[g.direction=='return'].set_index('destination_id');idx=out.index.intersection(back.index);a=out.loc[idx].copy()
 a['return_seconds']=back.loc[idx,'duration_seconds'];a['return_metres']=back.loc[idx,'distance_metres'];a['return_origin_snap_metres']=back.loc[idx,'origin_snap_metres'];a['return_destination_snap_metres']=back.loc[idx,'destination_snap_metres'];a['roundtrip_seconds']=a.duration_seconds+a.return_seconds
 base=o[o.origin_id==oid].iloc[0].to_dict()
 for scenario,limit in [('all_routed',float('inf')),('snap_le_250m',250)]:
  valid=a[a.duration_seconds.notna()&a.return_seconds.notna()&(a[['origin_snap_metres','destination_snap_metres','return_origin_snap_metres','return_destination_snap_metres']].max(axis=1)<=limit)]
  r={**base,'scenario':scenario,'paired_destination_records':len(valid)}
  groups={'auto2000':['auto2000'],'owned_network':['auto2000','otoxpert_auto2000'],'oil_network':['shopanddrive','otoxpert_auto2000','otoxpert_other'],'shopanddrive':['shopanddrive'],'otoxpert_auto2000':['otoxpert_auto2000'],'otoxpert_other':['otoxpert_other'],'local_documented':['local_documented']}
  for channel,kinds in groups.items():
   pool=valid[valid.kind.isin(kinds)]
   if len(pool):
    z=pool.loc[pool.roundtrip_seconds.idxmin()];r[channel+'_id']=z.name;r[channel+'_name']=z.destination_name;r[channel+'_out_minutes']=z.duration_seconds/60;r[channel+'_return_minutes']=z.return_seconds/60;r[channel+'_roundtrip_minutes']=z.roundtrip_seconds/60;r[channel+'_max_snap_m']=z[['origin_snap_metres','destination_snap_metres','return_origin_snap_metres','return_destination_snap_metres']].max()
   else:
    for field in ['id','name']:r[channel+'_'+field]=''
    for field in ['out_minutes','return_minutes','roundtrip_minutes','max_snap_m']:r[channel+'_'+field]=np.nan
  valid_out=a[a.duration_seconds.notna()&(a.origin_snap_metres<=limit)&(a.destination_snap_metres<=limit)]
  for channel,kinds in groups.items():
   pool=valid_out[valid_out.kind.isin(kinds)]
   if len(pool):
    z=pool.loc[pool.duration_seconds.idxmin()];r[channel+'_outbound_optimized_minutes']=z.duration_seconds/60;r[channel+'_outbound_optimized_name']=z.destination_name
   else:r[channel+'_outbound_optimized_minutes']=np.nan;r[channel+'_outbound_optimized_name']=''
  r['outbound_optimized_gap_minutes']=r['auto2000_outbound_optimized_minutes']-r['oil_network_outbound_optimized_minutes']
  A=r['auto2000_roundtrip_minutes'];C=r['oil_network_roundtrip_minutes'];r['roundtrip_gap_minutes']=A-C;r['outbound_gap_minutes']=r['auto2000_out_minutes']-r['oil_network_out_minutes'];r['extra_failed_auto_visit_minutes']=A;r['extra_failed_competitor_visit_minutes']=C;r['auto_one_visit_vs_competitor_two_visits_gap']=A-2*C;r['auto_two_visits_vs_competitor_one_visit_gap']=2*A-C
  r['wait_onsite_customer_road_minutes']=A;r['dropoff_collect_customer_road_minutes_same_profile']=2*A;r['pickup_return_customer_self_driven_minutes']=0;r['ths_customer_self_driven_minutes_if_eligible']=0;r['ths_technician_roundtrip_road_minutes']=A
  r['queue_difference_threshold_minutes_competitor_minus_auto']=A-C
  rows.append(r)
d=pd.DataFrame(rows);d.to_csv(R/'origin_trip_scenarios.csv',index=False)
s=[]
for (m,case,typ,scenario),g in d.groupby(['market','case','origin_type','scenario'],sort=False):
 v=g.dropna(subset=['auto2000_roundtrip_minutes','oil_network_roundtrip_minutes']);s.append({'market':m,'case':case,'origin_type':typ,'scenario':scenario,'origins':len(g),'paired_origins':len(v),'median_outbound_gap_minutes':v.outbound_gap_minutes.median(),'median_outbound_optimized_gap_minutes':g.outbound_optimized_gap_minutes.median(),'outbound_optimized_paired_origins':int(g.outbound_optimized_gap_minutes.notna().sum()),'median_roundtrip_gap_minutes':v.roundtrip_gap_minutes.median(),'median_auto_roundtrip_minutes':v.auto2000_roundtrip_minutes.median(),'median_oil_roundtrip_minutes':v.oil_network_roundtrip_minutes.median(),'auto_faster_or_equal_origins':int((v.roundtrip_gap_minutes<=0).sum()),'auto_roundtrip_gap_gt5_origins':int((v.roundtrip_gap_minutes>5).sum()),'auto_roundtrip_gap_gt10_origins':int((v.roundtrip_gap_minutes>10).sum()),'auto_one_visit_beats_competitor_two':int((v.auto_one_visit_vs_competitor_two_visits_gap<0).sum()),'auto_two_visits_loses_to_competitor_one':int((v.auto_two_visits_vs_competitor_one_visit_gap>0).sum()),'nearest_auto_names':';'.join(sorted(set(v.auto2000_name))), 'baseline_median_oneway_gap_same_selected_origins':pd.to_numeric(v.baseline_oil_gap_minutes,errors='coerce').median() if 'baseline_oil_gap_minutes' in v else None})
s=pd.DataFrame(s);s.to_csv(R/'origin_robustness_summary.csv',index=False)
# Actual outbound/return asymmetry, with separate directions retained.
q=p.pivot(index=['market','origin_id','destination_id'],columns='direction',values='duration_seconds').dropna();q['absolute_asymmetry_seconds']=(q.outbound-q['return']).abs();q.to_csv(R/'direction_asymmetry.csv')
qa={'new_directional_od_rows':len(p),'origins':o.origin_id.nunique(),'unique_od_direction_rows':not p.duplicated(['market','origin_id','destination_id','direction']).any(),'roundtrip_joins':len(q),'max_asymmetry_seconds':float(q.absolute_asymmetry_seconds.max()),'median_asymmetry_seconds':float(q.absolute_asymmetry_seconds.median()),'both_directions_acquired':set(p.direction)=={'outbound','return'},'numeric_nonnegative':bool((p.duration_seconds.dropna()>=0).all()),'model':'OSRM publicprofile; hypothetical visit-count/queue scenarios labelled; no observed queue or service duration'}
(R/'ACCESS_QA.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2));print(s.to_string(index=False))
