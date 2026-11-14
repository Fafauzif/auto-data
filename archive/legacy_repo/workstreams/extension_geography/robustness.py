"""Offline descriptive robustness analyses. No network. Preserve source/first-wave files."""
from pathlib import Path
import collections, hashlib, json, math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
RAW=ROOT/'raw_licensed_data/SPKLU_CC_BY_NC_3_0'
FIRST=ROOT/'workstreams/datasets'
inputs=[RAW/'data/spklu_stations.csv',RAW/'data/spklu_chargers.csv',RAW/'spklu_data_dictionary.csv',FIRST/'bps_vehicle_stock_long.csv',FIRST/'five_branch_coordinate_crosscheck.csv']
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
s=pd.read_csv(inputs[0]);c=pd.read_csv(inputs[1]);b=pd.read_csv(inputs[3]);checks=pd.read_csv(inputs[4])
assert len(s)==2454 and s.station_id.nunique()==2454 and len(c)==3767
s.index=np.arange(len(s));s['is_auto2000_name']=s.location_name.str.contains(r'auto\s*2000',case=False,regex=True)
assert int(s.is_auto2000_name.sum())==28
s['explicit_restriction_name_flag']=s.location_name.str.contains(r'\b(?:khusus|only|restricted|private|terbatas|internal)\b',case=False,regex=True)
s['toyota_lexus_permitted_name_flag']=s.explicit_restriction_name_flag & s.location_name.str.contains(r'toyota\s*(?:&|and|dan|/)\s*lexus',case=False,regex=True)
s['source_coord_quality_flag']=s.quality_flags.fillna('').str.contains('coord',case=False)
s['source_access_verified']=False  # No such field exists in the source. This is NOT a declaration of inaccessibility.
network=s.provider_type.isin(['PLN / SPKLU network','Independent CPO'])
facing=s.location_type.isin(['PLN / Utility facility','Retail / F&B','Mall / Shopping','Rest area / Toll','Public space / Tourism','Airport / Port / Transit'])
pools={
 'all_mapped':~s.is_auto2000_name,
 'exclude_explicit_restrictions':~s.is_auto2000_name & ~s.explicit_restriction_name_flag,
 'toyota_target_name_compatible':~s.is_auto2000_name & (~s.explicit_restriction_name_flag|s.toyota_lexus_permitted_name_flag),
 'network_proxy':~s.is_auto2000_name & network & ~s.explicit_restriction_name_flag,
 'network_public_facing_venue_proxy':~s.is_auto2000_name & network & facing & ~s.explicit_restriction_name_flag,
}
dc=set(c.loc[c.inferred_current=='DC','station_id']);ac=set(c.loc[c.inferred_current=='AC','station_id'])
s['has_inferred_DC_box']=s.station_id.isin(dc);s['has_inferred_AC_box']=s.station_id.isin(ac)
for k,v in pools.items():s['pool_'+k]=v
classification_cols=['station_id','location_name','province_name','provider_type','operator_brand','location_type','latitude','longitude','is_auto2000_name','explicit_restriction_name_flag','toyota_lexus_permitted_name_flag','source_coord_quality_flag','source_access_verified','has_inferred_DC_box','has_inferred_AC_box']+['pool_'+k for k in pools]
s[classification_cols].to_csv(OUT/'station_classification_receipt.csv',index=False)

def distances(lat,lon):
 la=np.deg2rad(lat);lo=np.deg2rad(lon)
 a=np.sin((la[:,None]-la[None,:])/2)**2+np.cos(la[:,None])*np.cos(la[None,:])*np.sin((lo[:,None]-lo[None,:])/2)**2
 return 6371.0088*2*np.arcsin(np.sqrt(np.clip(a,0,1)))

raw_d=distances(s.latitude.to_numpy(),s.longitude.to_numpy())
official=s[['latitude','longitude']].copy()
for _,r in checks.iterrows():
 idx=s.index[s.station_id==r.station_id];assert len(idx)==1
 official.loc[idx,'latitude']=r.official_directions_candidate_latitude;official.loc[idx,'longitude']=r.official_directions_candidate_longitude
official_d=distances(official.latitude.to_numpy(),official.longitude.to_numpy())
known_conflict=set(checks.loc[checks.straight_line_disagreement_km>1,'station_id'])
assert known_conflict=={2397}
coord_scenarios={
 'source_coordinates':(raw_d,False,False),
 'source_exclude_flagged_candidates':(raw_d,True,False),
 'source_omit_known_conflicted_anchor':(raw_d,False,True),
 'official_five_branch_candidates':(official_d,False,False),
 'official_five_exclude_flagged_candidates':(official_d,True,False),
}
nearest=[];summary=[]
for scen,(d,dropflags,dropanchor) in coord_scenarios.items():
 anchors=s.index[s.is_auto2000_name & (~s.station_id.isin(known_conflict) if dropanchor else True)].to_numpy()
 for pool,mask in pools.items():
  cmask=mask & (~s.source_coord_quality_flag if dropflags else True)
  candidates=s.index[cmask].to_numpy();sub=d[np.ix_(anchors,candidates)];mi=sub.argmin(axis=1);mins=sub[np.arange(len(anchors)),mi]
  for j,i in enumerate(anchors):
   ni=candidates[mi[j]]
   row={'coordinate_scenario':scen,'candidate_pool':pool,'anchor_station_id':int(s.at[i,'station_id']),'anchor_name':s.at[i,'location_name'],'anchor_province':s.at[i,'province_name'],'nearest_candidate_station_id':int(s.at[ni,'station_id']),'nearest_candidate_name':s.at[ni,'location_name'],'nearest_candidate_provider_type':s.at[ni,'provider_type'],'nearest_candidate_location_type':s.at[ni,'location_type'],'nearest_candidate_explicit_restriction_flag':bool(s.at[ni,'explicit_restriction_name_flag']),'nearest_candidate_source_coord_flag':bool(s.at[ni,'source_coord_quality_flag']),'great_circle_lower_bound_km':float(mins[j]),'access_verified':False,'interpretation':'Mapped location only; eligibility, connector, hours, uptime and route remain unverified'}
   for k in (1,3,5):row['candidate_sites_within_'+str(k)+'km']=int((sub[j]<=k).sum())
   nearest.append(row)
  row={'coordinate_scenario':scen,'candidate_pool':pool,'anchor_n':len(anchors),'candidate_site_n':len(candidates),'median_nearest_great_circle_km':float(np.median(mins)),'max_nearest_great_circle_km':float(max(mins))}
  for k in (1,3,5):row['anchors_with_candidate_within_'+str(k)+'km']=int((mins<=k).sum())
  summary.append(row)
nn=pd.DataFrame(nearest);summ=pd.DataFrame(summary)
nn.to_csv(OUT/'anchor_nearest_alternative_scenarios.csv',index=False);summ.to_csv(OUT/'nearest_scenario_summary.csv',index=False)
base=nn[(nn.coordinate_scenario=='source_coordinates') & (nn.candidate_pool=='all_mapped')][['anchor_station_id','great_circle_lower_bound_km']].rename(columns={'great_circle_lower_bound_km':'all_mapped_lower_bound_km'})
delta=nn[nn.coordinate_scenario=='source_coordinates'].merge(base,on='anchor_station_id',validate='m:1')
delta['distance_increase_from_all_mapped_km']=delta.great_circle_lower_bound_km-delta.all_mapped_lower_bound_km
delta.to_csv(OUT/'anchor_pool_distance_penalty.csv',index=False)
fals=summ[(summ.coordinate_scenario=='source_coordinates') & (summ.candidate_pool=='network_public_facing_venue_proxy')].iloc[0]
six=int(((delta.candidate_pool=='network_public_facing_venue_proxy') & (delta.distance_increase_from_all_mapped_km>=2)).sum())

# Exact coordinate duplicates were already resolved by source. Near clustering is a sensitivity only.
def components(threshold):
 parent=np.arange(len(s))
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 def union(a,b):
  ra,rb=find(a),find(b)
  if ra!=rb:parent[max(ra,rb)]=min(ra,rb)
 ii,jj=np.where(np.triu(raw_d<=threshold,1))
 for i,j in zip(ii,jj):union(int(i),int(j))
 return np.array([find(i) for i in range(len(s))]),len(ii)

cluster_rows=[];cluster_summary=[];clustercols=s[['station_id','province_name','bps_province_code']].copy()
for metres in (20,50,100):
 ids,edges=components(metres/1000);sizes=pd.Series(ids).value_counts();clustercols['connected_cluster_'+str(metres)+'m']=s.station_id.to_numpy()[ids]
 cp=pd.DataFrame({'cluster':ids,'province':s.bps_province_code});cross=int((cp.groupby('cluster').province.nunique()>1).sum())
 cluster_summary.append({'threshold_m':metres,'global_connected_components':int(len(sizes)),'components_with_multiple_station_rows':int((sizes>1).sum()),'station_rows_in_multi_station_components':int(sizes[sizes>1].sum()),'max_component_site_rows':int(sizes.max()),'near_pair_edges':int(edges),'cross_province_components':cross,'interpretation':'Proximity components, not verified duplicate facilities; transitive chains allowed'})
 for code,g in s.groupby('bps_province_code'):
  cluster_rows.append({'bps_province_code':int(code),'threshold_m':metres,'within_province_components':int(len(set(ids[g.index]))),'source_site_rows':len(g)})
clustercols.to_csv(OUT/'near_coordinate_component_membership.csv',index=False)
pd.DataFrame(cluster_summary).to_csv(OUT/'coordinate_cluster_sensitivity.csv',index=False)
pd.DataFrame(cluster_rows).to_csv(OUT/'province_coordinate_cluster_units.csv',index=False)

# Provincial unit and denominator scenarios. Hold numerator snapshot fixed across years.
units=s.groupby(['bps_province_code','province_name']).agg(site_rows=('station_id','size'),charger_box_rows=('n_chargerboxes','sum'),source_charger_units=('total_chargers','sum'),source_connectors=('total_connectors','sum'),represented_raw_source_rows=('n_merged','sum'),source_coord_flag_rows=('source_coord_quality_flag','sum'),network_proxy_sites=('pool_network_proxy','sum'),conservative_venue_proxy_sites=('pool_network_public_facing_venue_proxy','sum')).reset_index()
units['sites_excluding_source_coord_flags']=units.site_rows-units.source_coord_flag_rows
for metres in (20,50,100):
 co=pd.DataFrame(cluster_rows);co=co[co.threshold_m==metres][['bps_province_code','within_province_components']].rename(columns={'within_province_components':'coordinate_components_'+str(metres)+'m'})
 units=units.merge(co,on='bps_province_code',validate='1:1')
unitcols=[c for c in units if c not in ['bps_province_code','province_name','source_coord_flag_rows']]
units['box_rows_per_site']=units.charger_box_rows/units.site_rows
units.to_csv(OUT/'province_numerator_unit_sensitivity.csv',index=False)
stocks=b[b.variable_name_en.str.contains('Passenger Cars')].copy();stocks['code']=(stocks.region_code//100000).astype(int);stocks=stocks[stocks.province_label!='Indonesia']
poolmap={92:91,95:94,96:94,97:94}
ratios=[];denaudit=[]
for year in (2022,2023,2024,2025):
 by=stocks[stocks.year==year].copy()
 national=float(b[(b.year==year)&(b.province_label=='Indonesia')&b.variable_name_en.str.contains('Passenger Cars')].value_units.iloc[0])
 for boundary in ('direct_34_code_join','pooled_historical_34_boundaries'):
  by['mapped_code']=by.code.map(poolmap).fillna(by.code).astype(int) if boundary.startswith('pooled') else by.code
  den=by.groupby('mapped_code').value_units.sum(min_count=1)
  matched=float(den.reindex(units.bps_province_code).sum())
  denaudit.append({'year':year,'boundary_scenario':boundary,'national_source_passenger_stock':national,'matched_34_province_stock':matched,'unmatched_stock':national-matched,'full_source_province_stock_sum':float(by.value_units.sum()),'note':'Child-province missing values in 2023–24 do not imply zero fleets; parent reports carry published totals in those tables. Pooling sums nonmissing published cells.'})
  if boundary.startswith('pooled'):assert abs(matched-national)<.1
  for _,u in units.iterrows():
   car=float(den.get(int(u.bps_province_code),np.nan))
   for uc in unitcols:
    ratios.append({'year_of_denominator':year,'boundary_scenario':boundary,'bps_province_code':int(u.bps_province_code),'province_name':u.province_name,'numerator_unit':uc,'numerator_value':int(u[uc]),'passenger_stock_denominator':car,'units_per_100000_passenger_vehicles':100000*float(u[uc])/car if car>0 else np.nan,'source_stock_break_flag':bool(u.bps_province_code==35 and year>=2023),'site_snapshot':'2026-06-16','limit':'Not BEV demand, operational fleet, capacity, access or station growth'})
rt=pd.DataFrame(ratios);rt['descending_rank']=rt.groupby(['year_of_denominator','boundary_scenario','numerator_unit']).units_per_100000_passenger_vehicles.rank(ascending=False,method='min')
rt.to_csv(OUT/'province_ratio_scenarios.csv',index=False);pd.DataFrame(denaudit).to_csv(OUT/'boundary_stock_conservation.csv',index=False)
cur=rt[(rt.year_of_denominator==2025)&(rt.boundary_scenario=='pooled_historical_34_boundaries')]
site=cur[cur.numerator_unit=='site_rows'][['bps_province_code','units_per_100000_passenger_vehicles','descending_rank']].rename(columns={'units_per_100000_passenger_vehicles':'site_ratio','descending_rank':'site_rank'})
ranks=cur.merge(site,on='bps_province_code',validate='m:1');ranks['rank_shift_from_site_unit']=ranks.descending_rank-ranks.site_rank
ranks['ratio_relative_to_site_unit']=ranks.units_per_100000_passenger_vehicles/ranks.site_ratio
ranks.to_csv(OUT/'province_rank_sensitivity.csv',index=False)
stockdetail=stocks[stocks.year.between(2022,2025)][['year','province_label','code','value_units']].copy();stockdetail['historical_34_code']=stockdetail.code.map(poolmap).fillna(stockdetail.code).astype(int);stockdetail.to_csv(OUT/'stock_boundary_audit_cells.csv',index=False)
rolled=stockdetail.groupby(['historical_34_code','year']).value_units.sum(min_count=1).unstack('year')
diagnostics=rolled.rename(columns={y:'stock_'+str(y) for y in rolled.columns}).reset_index().rename(columns={'historical_34_code':'bps_province_code'})
diagnostics=diagnostics.merge(units[['bps_province_code','province_name']],on='bps_province_code',validate='1:1')
for y in (2023,2024,2025):
 diagnostics['published_stock_change_'+str(y)+'_pct']=100*(diagnostics['stock_'+str(y)]/diagnostics['stock_'+str(y-1)]-1)
diagnostics['exploratory_absolute_change_over25pct_2022_2023']=diagnostics.published_stock_change_2023_pct.abs()>25
diagnostics['interpretation']='Published stock discontinuity diagnostic; not verified organic fleet growth or a proven source error. 25% threshold is exploratory.'
diagnostics.to_csv(OUT/'published_stock_discontinuity_diagnostics.csv',index=False)
crosspairs=[]
ii,jj=np.where(np.triu((raw_d<=.1)&(s.bps_province_code.to_numpy()[:,None]!=s.bps_province_code.to_numpy()[None,:]),1))
for i,j in zip(ii,jj):
 crosspairs.append({'station_a_id':int(s.at[i,'station_id']),'station_b_id':int(s.at[j,'station_id']),'station_a_name':s.at[i,'location_name'],'station_b_name':s.at[j,'location_name'],'station_a_province':s.at[i,'province_name'],'station_b_province':s.at[j,'province_name'],'station_a_city':s.at[i,'regency_city_clean'],'station_b_city':s.at[j,'regency_city_clean'],'great_circle_separation_m':float(raw_d[i,j]*1000),'source_coordinate_flag_a':bool(s.at[i,'source_coord_quality_flag']),'source_coordinate_flag_b':bool(s.at[j,'source_coord_quality_flag']),'limit':'Could reflect true border-adjacent locations or coordinate/admin disagreement; not adjudicated'})
pd.DataFrame(crosspairs).to_csv(OUT/'cross_province_near_coordinate_pairs.csv',index=False)

# Original figures: exact displayed units and observational scope in each caption.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.dpi':180})
colors={'source_coordinates':'#245A78','official_five_branch_candidates':'#B97032'}
labels={'all_mapped':'All mapped','exclude_explicit_restrictions':'Remove explicit restrictions','toyota_target_name_compatible':'Toyota-compatible name rules','network_proxy':'PLN / CPO proxy','network_public_facing_venue_proxy':'PLN / CPO + venue proxy'}
fig,axes=plt.subplots(1,2,figsize=(12,6.1),sharey=True);y=np.arange(len(pools))
for ax,km in zip(axes,(1,5)):
 for j,sc in enumerate(colors):
  dat=summ[summ.coordinate_scenario==sc].set_index('candidate_pool').loc[list(pools)]
  vals=dat['anchors_with_candidate_within_'+str(km)+'km'].to_numpy();ax.barh(y+(j-.5)*.32,vals,height=.30,color=colors[sc],label='Original coordinates' if j==0 else 'Five branch-direction candidates')
  for yy,v in zip(y+(j-.5)*.32,vals):ax.text(v+.15,yy,str(v)+'/28',va='center',fontsize=9)
 ax.set_yticks(y,[labels[k] for k in pools]);ax.set_xlim(0,31);ax.set_xlabel('Auto2000-name anchors with a mapped candidate');ax.set_title('Within '+str(km)+' km')
axes[0].invert_yaxis();handles,leglabels=axes[0].get_legend_handles_labels();fig.legend(handles,leglabels,loc='lower center',bbox_to_anchor=(.57,.102),ncol=2,frameon=False)
fig.suptitle('Five-kilometre proximity survives filtering; one-kilometre proximity changes sharply\nAccess itself remains unverified',fontsize=14)
fig.text(.01,.01,'Great-circle distances, not driving time. June 2026 snapshot. No pool confirms access, connector, hours or uptime.\nSPKLU: Wiputra & Santiadi, DOI 10.17632/z2bvd5r574.2, CC BY-NC 3.0. Original derived analysis.',fontsize=8);fig.tight_layout(rect=(0,.17,1,.91));fig.savefig(OUT/'01_nearest_candidate_robustness.png');plt.close(fig)

fig,ax=plt.subplots(figsize=(10,5.6));rr=rt[(rt.year_of_denominator==2025)&(rt.numerator_unit=='site_rows')].pivot(index='province_name',columns='boundary_scenario',values='units_per_100000_passenger_vehicles');show=rr.loc[['Papua Barat','Papua','Jawa Timur','DKI Jakarta','Banten']]
for j,(name,row) in enumerate(show.iterrows()):
 a,bv=row['direct_34_code_join'],row['pooled_historical_34_boundaries'];ax.plot([a,bv],[j,j],color='#999999',lw=2);ax.scatter(a,j,s=60,color='#B97032',label='Direct code join' if j==0 else None);ax.scatter(bv,j,s=55,color='#245A78',label='Historical-boundary pooled' if j==0 else None);ax.text(max(a,bv)+.25,j,f'{a:.2f} → {bv:.2f}',va='center',fontsize=9)
ax.set_yticks(range(len(show)),show.index);ax.invert_yaxis();ax.set_xlim(0,max(show.max())*1.32);ax.set_xlabel('Mapped charging sites per 100,000 passenger vehicles, 2025 stock');ax.set_title('Boundary alignment changes Papua ratios substantially\nOther provinces shown as unchanged comparisons');ax.legend(frameon=False,loc='lower right');fig.text(.01,.01,'June 2026 mapped sites / BPS–Polri 2025 passenger stocks. Four new Papua provinces pool into source-era parent boundaries.\nNo inference about BEV adequacy. SPKLU CC BY-NC 3.0; BPS source cells and transformation recorded.',fontsize=8);fig.tight_layout(rect=(0,.08,1,1));fig.savefig(OUT/'02_boundary_ratio_sensitivity.png');plt.close(fig)

fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5.7),gridspec_kw={'width_ratios':[1,1.2]})
un=units.sort_values('site_rows',ascending=False).head(8);yy=np.arange(len(un));ax1.barh(yy-.17,un.site_rows,.32,label='Site rows',color='#245A78');ax1.barh(yy+.17,un.charger_box_rows,.32,label='Charger-box rows',color='#B97032');ax1.set_yticks(yy,un.province_name);ax1.invert_yaxis();ax1.set_xlabel('Recorded units');ax1.legend(frameon=False,fontsize=9);ax1.set_title('Sites and boxes answer different questions')
ax2.scatter(s.longitude,s.latitude,s=7,c='#8CA5AD',alpha=.5,linewidths=0);a=s[s.is_auto2000_name];ax2.scatter(a.longitude,a.latitude,s=30,c='#B97032',edgecolor='white',linewidth=.4,label='28 Auto2000-name source records');ax2.set_xlabel('Longitude');ax2.set_ylabel('Latitude');ax2.set_xlim(94,142);ax2.set_ylim(-12,7);ax2.set_title('Source locations, not service catchments');ax2.legend(loc='lower left',fontsize=8,frameon=False);ax2.set_aspect(1/np.cos(np.deg2rad(-2)))
fig.text(.01,.01,'No administrative basemap or operational coverage boundary is implied. Source coordinates include known conflicts.\nBoxes are hardware records, not simultaneous capacity. SPKLU June 2026, DOI 10.17632/z2bvd5r574.2, CC BY-NC 3.0.',fontsize=8);fig.tight_layout(rect=(0,.09,1,1));fig.savefig(OUT/'03_units_and_point_locations.png');plt.close(fig)

summary={'source_doi':'10.17632/z2bvd5r574.2','source_license':'CC BY-NC 3.0','snapshot':'2026-06-16','input_sha256':hashes,'station_rows':len(s),'charger_box_rows':len(c),'source_charger_unit_sum':int(c.n_chargers.sum()),'source_connector_sum':int(c.n_connectors.sum()),'represented_raw_source_rows':int(s.n_merged.sum()),'unique_exact_coordinates':len(s[['latitude','longitude']].drop_duplicates()),'already_consolidated_colocation_flag_rows':int((s.colocation_cluster_size>1).sum()),'source_coordinate_flag_rows':int(s.source_coord_quality_flag.sum()),'explicit_restriction_name_rows':int(s.explicit_restriction_name_flag.sum()),'toyota_lexus_permitted_restriction_name_rows':int(s.toyota_lexus_permitted_name_flag.sum()),'all_status_flags_one':bool((s.status_active==1).all()),'verified_current_access_not_identifiable':True,'confirmed_access_nearby_anchor_count_lower_bound':0,'all_mapped_candidate_5km_optimistic_anchor_count':int(summ[(summ.coordinate_scenario=='source_coordinates')&(summ.candidate_pool=='all_mapped')].anchors_with_candidate_within_5km.iloc[0]),'preregistered_proxy_falsification':{'retain_less_than_21_of_28':bool(fals.anchors_with_candidate_within_5km<21),'six_or_more_increase_at_least_2km':bool(six>=6),'actual_conservative_proxy_within5km':int(fals.anchors_with_candidate_within_5km),'actual_anchors_increase_at_least2km':six,'scope':'Tests descriptive mapped proximity only. Customer value and verified usability are not identified.'},'coordinate_clusters':cluster_summary,'cross_province_pairs_within100m':len(crosspairs),'exploratory_provinces_with_absolute_published_stock_change_over25pct_2022_2023':int(diagnostics.exploratory_absolute_change_over25pct_2022_2023.sum()),'boundary_reconciliation':denaudit,'files_generated':[p.name for p in OUT.glob('*.csv')]+[p.name for p in OUT.glob('*.png')],'distance_unit':'Great-circle km, a lower bound on feasible road distance if coordinates are correct; no time/cost estimate','computed_pairwise_matrix_is_not_new_observations':True}
(OUT/'ROBUSTNESS_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['input_sha256','coordinate_clusters','boundary_reconciliation','files_generated']},indent=2));print(summ.to_string(index=False));print('CLUSTERS',cluster_summary);print('BOX_RANK_SHIFT_MAX',int(ranks[ranks.numerator_unit=='charger_box_rows'].rank_shift_from_site_unit.abs().max()))
