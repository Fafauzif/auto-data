from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,os
R=Path(__file__).resolve().parent;B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
# R / work / branch_analysis; parents1 insight_followup
main=pd.read_csv(B/'workstreams/routing/output/od_pairs.csv');supp=pd.read_csv(B/'workstreams/routing/supplement/supplement_od_pairs.csv');ox=pd.read_csv(B/'workstreams/context/otoxpert_official_inventory.csv');orig=pd.read_csv(B/'workstreams/routing/output/origins.csv')
inputs=pd.concat([pd.read_csv(B/f'workstreams/routing/inputs/{m}_destinations.csv').assign(market=m.title()) for m in ['surabaya','medan','bandung','palembang']],ignore_index=True)
CORRECT=os.environ.get('GEOCORRECT')=='1'
OUT=R/'corrected' if CORRECT else R
OUT.mkdir(exist_ok=True)
if CORRECT:
 cc=pd.read_csv(R.parent/'coordinates/corrected_endpoint_od.csv');cc=cc[cc.direction=='outbound'].copy()
 meta=cc[['market','destination_id','destination_name','destination_longitude','destination_latitude']].drop_duplicates().rename(columns={'destination_name':'name','destination_longitude':'longitude','destination_latitude':'latitude'});meta['kind']='auto2000'
 inputs=pd.concat([inputs,meta],ignore_index=True,sort=False);main=pd.concat([main,cc],ignore_index=True,sort=False)
operator={f'otoxpert:{r.provider_id}':r.operator for _,r in ox.iterrows()};own={f'otoxpert:{r.provider_id}':str(r.auto2000_operator).lower()=='true' for _,r in ox.iterrows()}
pairs=pd.concat([main,supp],ignore_index=True,sort=False)
pairs['channel']=pairs.kind
pairs.loc[pairs.kind=='independent','channel']='generic_candidate'
pairs.loc[pairs.kind=='otoxpert','channel']=pairs.loc[pairs.kind=='otoxpert','destination_id'].map(lambda z:'otoxpert_auto2000' if own.get(z,False) else 'otoxpert_other')
pairs['operator']=pairs.destination_id.map(operator).fillna(pairs.channel.map({'auto2000':'Auto2000','shopanddrive':'Astra Otoparts / Shop&Drive','domo':'DokterMobil','generic_candidate':'unknown','other_authorized':'other Toyota authorised'}))
channels=['auto2000','generic_candidate','otoxpert_auto2000','otoxpert_other','shopanddrive','domo','other_authorized']
origin_results=[];branch_results=[];marginal=[];market_results=[];long_winners=[]
for scenario in ['all_routed','snap_le_250m']:
 p=pairs[pairs.duration_seconds.notna()].copy()
 if scenario=='snap_le_250m':p=p[(p.origin_snap_metres<=250)&(p.destination_snap_metres<=250)]
 for market in main.market.unique():
  mp=p[p.market==market];branchids=inputs[(inputs.market.str.lower()==market.lower())&(inputs.kind=='auto2000')].destination_id.tolist()
  local=[]
  for oid,g in mp.groupby('origin_id',sort=True):
   row={'market':market,'scenario':scenario,'origin_id':oid};a=g[g.channel=='auto2000'].sort_values('duration_seconds',kind='mergesort');
   for channel in channels:
    z=g[g.channel==channel].sort_values('duration_seconds',kind='mergesort')
    row[channel+'_seconds']=z.iloc[0].duration_seconds if len(z) else np.nan;row[channel+'_id']=z.iloc[0].destination_id if len(z) else '';row[channel+'_name']=z.iloc[0].destination_name if len(z) else ''
    for th in [10,15,20,30]:row[f'{channel}_count_le_{th}min']=int((z.duration_seconds<=th*60).sum()) if len(z) else np.nan
   row['nearest_tied_auto2000_ids']=';'.join(a.loc[abs(a.duration_seconds-a.iloc[0].duration_seconds)<1e-7,'destination_id']) if len(a) else '';row['nearest_tied_auto2000_count']=int((abs(a.duration_seconds-a.iloc[0].duration_seconds)<1e-7).sum()) if len(a) else 0
   row['second_auto2000_seconds']=a.iloc[1].duration_seconds if len(a)>1 else np.nan;row['second_auto2000_id']=a.iloc[1].destination_id if len(a)>1 else '';row['second_auto2000_name']=a.iloc[1].destination_name if len(a)>1 else ''
   for label,allowed in {'oil_network':['otoxpert_auto2000','otoxpert_other','shopanddrive'],'owned_oil_network':['auto2000','otoxpert_auto2000'],'external_oil_network':['otoxpert_other','shopanddrive'],'brake_network':['otoxpert_auto2000','otoxpert_other'],'brake_network_with_SD':['otoxpert_auto2000','otoxpert_other','shopanddrive'],'owned_brake_network':['auto2000','otoxpert_auto2000']}.items():
    pool=g[g.channel.isin(allowed)].sort_values('duration_seconds',kind='mergesort')
    row[label+'_seconds']=pool.iloc[0].duration_seconds if len(pool) else np.nan;row[label+'_id']=pool.iloc[0].destination_id if len(pool) else '';row[label+'_channel']=pool.iloc[0].channel if len(pool) else '';row[label+'_name']=pool.iloc[0].destination_name if len(pool) else ''
   row['oil_gap_minutes']=round((row['auto2000_seconds']-row['oil_network_seconds'])/60,12);row['generic_gap_minutes']=(row['auto2000_seconds']-row['generic_candidate_seconds'])/60
   row['owned_network_gap_minutes']=round((row['owned_oil_network_seconds']-row['oil_network_seconds'])/60,12)
   row['owned_network_saving_minutes']=(row['auto2000_seconds']-row['owned_oil_network_seconds'])/60
   row['second_branch_penalty_minutes']=(row['second_auto2000_seconds']-row['auto2000_seconds'])/60
   local.append(row)
  od=pd.DataFrame(local);origin_results+=local
  paired=od[od.auto2000_seconds.notna()&od.oil_network_seconds.notna()].copy()
  market_results.append({'market':market,'scenario':scenario,'paired_n':len(paired),'median_generic_gap_min':paired.generic_gap_minutes.median(),'median_oil_gap_min':paired.oil_gap_minutes.median(),'origins_auto2000_not_slower':int((paired.oil_gap_minutes<=0).sum()),'oil_gap_gt5_n':int((paired.oil_gap_minutes>5).sum()),'max_oil_gap_min':paired.oil_gap_minutes.max()})
  change=paired.owned_network_saving_minutes
  mr={'market':market,'scenario':scenario,'paired_n':len(paired),'own_ox_benefit_gt1sec_n':int((change>1/60).sum()),'own_ox_benefit_gt1min_n':int((change>1).sum()),'own_ox_benefit_gt3min_n':int((change>3).sum()),'own_ox_benefit_gt5min_n':int((change>5).sum()),'median_saving_all_min':change.median(),'median_saving_positive_min':change[change>1/60].median(),'max_saving_min':change.max(),'oil_gap_gt5_before_n':int((paired.oil_gap_minutes>5).sum()),'oil_gap_gt5_after_owned_routing_n':int((paired.owned_network_gap_minutes>5).sum()),'median_owned_gap_min':paired.owned_network_gap_minutes.median()}
  for th in [10,15,20,30]:
   old=paired.auto2000_seconds<=th*60;new=paired.owned_oil_network_seconds<=th*60;mr[f'old_le_{th}min']=int(old.sum());mr[f'new_le_{th}min']=int(new.sum());mr[f'added_le_{th}min']=int((new&~old).sum())
  marginal.append(mr)
  for bid in branchids:
   bname=inputs[inputs.destination_id==bid].iloc[0]['name'];catch=paired[paired.auto2000_id==bid].copy();branchraw=mp[(mp.channel=='auto2000')&(mp.destination_id==bid)]
   br={'market':market,'scenario':scenario,'branch_id':bid,'branch_name':bname,'paired_market_n':len(paired),'nearest_origins_n':len(catch),'assigned_origins_with_tied_nearest_branch_n':int((catch.nearest_tied_auto2000_count>1).sum()),'origin_ids':';'.join(catch.origin_id),'median_oil_gap_min':catch.oil_gap_minutes.median(),'p25_oil_gap_min':catch.oil_gap_minutes.quantile(.25),'p75_oil_gap_min':catch.oil_gap_minutes.quantile(.75),'oil_gap_gt5_n':int((catch.oil_gap_minutes>5).sum()),'oil_gap_le0_n':int((catch.oil_gap_minutes<=0).sum()),'median_generic_gap_min':catch.generic_gap_minutes.median(),'median_owned_network_gap_min':catch.owned_network_gap_minutes.median(),'owned_network_gap_gt5_n':int((catch.owned_network_gap_minutes>5).sum()),'own_ox_saves_gt1min_n':int((catch.owned_network_saving_minutes>1).sum()),'own_ox_saves_gt3min_n':int((catch.owned_network_saving_minutes>3).sum()),'own_ox_saves_gt5min_n':int((catch.owned_network_saving_minutes>5).sum()),'median_auto_minutes':catch.auto2000_seconds.median()/60,'median_oil_minutes':catch.oil_network_seconds.median()/60,'second_branch_penalty_median_min':catch.second_branch_penalty_minutes.median(),'second_branch_penalty_max_min':catch.second_branch_penalty_minutes.max(),'dominant_second_branch':catch.second_auto2000_name.mode().iloc[0] if len(catch) else ''}
   for channel in ['otoxpert_auto2000','otoxpert_other','shopanddrive']:br['nearest_oil_'+channel+'_n']=int((catch.oil_network_channel==channel).sum())
   for th in [10,15,20,30]:
    br[f'branch_reach_{th}min_n']=int((branchraw.duration_seconds<=th*60).sum())
    br[f'grid_loses_{th}min_without_branch_n']=int(((catch.auto2000_seconds<=th*60)&(catch.second_auto2000_seconds>th*60)).sum())
   for job,field in [('oil_filter','oil_network_seconds'),('front_brake_pads','brake_network_with_SD_seconds'),('front_brake_oto_only_sensitivity','brake_network_seconds')]:
    x=catch[(catch[field].notna())&(catch.auto2000_seconds.notna())];br[job+'_paired_n']=len(x);br[job+'_median_gap_min']=((x.auto2000_seconds-x[field])/60).median();br[job+'_scope']='network-advertised task; exact model/parts/slot not confirmed'
   branch_results.append(br)
origin=pd.DataFrame(origin_results)
expected=orig[['market','origin_id','longitude','latitude']].drop_duplicates().merge(pd.DataFrame({'scenario':['all_routed','snap_le_250m']}),how='cross')
origin=expected.merge(origin,on=['market','origin_id','scenario'],how='left',indicator=True)
origin['availability_status']=np.where(origin['_merge']=='both','computed_from_retained_OD','unknown_after_snap_filter_or_no_routable_OD')
origin=origin.drop(columns='_merge')
origin.to_csv(OUT/'origin_channels_recomputed.csv',index=False);pd.DataFrame(branch_results).to_csv(OUT/'all_27_branches_recomputed.csv',index=False);pd.DataFrame(market_results).to_csv(OUT/'market_recomputed.csv',index=False);pd.DataFrame(marginal).to_csv(OUT/'owned_otoxpert_marginal.csv',index=False)
pairs[['market','origin_id','destination_id','destination_name','kind','channel','operator','duration_seconds','origin_snap_metres','destination_snap_metres']].to_csv(OUT/'od_channel_classification.csv',index=False)
# Exact original handoff cross-checks; descriptive records use source durations without rounding.
new=pd.DataFrame(branch_results);old=pd.read_csv(R.parents[1]/'extracted/reanalysis/branch_reanalysis.csv');j=new[new.scenario=='snap_le_250m'].merge(old,on=['market','branch_id'],suffixes=('_new','_old'))
check={'branch_rows':len(new),'unique_branches':new.branch_id.nunique(),'market_origin_rows':len(origin),'matched_handoff_branches':len(j),'max_handoff_oil_gap_difference_minutes':float((j.median_oil_gap_min-j.median_oil_network_gap_minutes).abs().max()),'handoff_count_equal':bool((j.nearest_origins_n==j.nearest_grid_origins).all()),'strict_joint_n':pd.DataFrame(market_results).query("scenario=='snap_le_250m'")['paired_n'].tolist(),'corrected_coordinate_scenario':CORRECT,'method':'Full raw OD minima by channel and operator, same paired origin set; no cached summary trusted as calculation input'}
check['handoff_comparison_expectation']='Coordinate scenario intentionally changes branch catchments; these differences are outcomes, not audit failures' if CORRECT else 'Baseline should reproduce handoff assignments and medians'
check['qa_pass']=bool(check['unique_branches']==(29 if CORRECT else 27) and check['market_origin_rows']==648 and check['strict_joint_n']==[59,78,78,69] and (CORRECT or(check['handoff_count_equal'] and check['max_handoff_oil_gap_difference_minutes']<1e-9)))
(OUT/'RECOMPUTE_QA.json').write_text(json.dumps(check,indent=2));print(json.dumps(check,indent=2));print(pd.DataFrame(market_results).to_string(index=False));print(pd.DataFrame(marginal).query("scenario=='snap_le_250m'").to_string(index=False))
