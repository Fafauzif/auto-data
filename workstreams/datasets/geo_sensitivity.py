from acquire import OUT,CACHE
import pandas as pd,numpy as np,json,re
s=pd.read_csv(CACHE/'spklu_stations.csv');a=pd.read_csv(OUT/'auto2000_charging_context.csv');probes=json.load(open(OUT/'site_branch_identity_probe.json'))
ids=[2400,2397,2408,2144,2154];review=[]
def hav(lat,lon,lats,lons):
 a1=np.radians(lat);a2=np.radians(lats);d1=a2-a1;d2=np.radians(lons-lon);v=np.sin(d1/2)**2+np.cos(a1)*np.cos(a2)*np.sin(d2/2)**2;return 6371.0088*2*np.arcsin(np.sqrt(np.clip(v,0,1)))
scenario=s.copy()
for id,p in zip(ids,probes):
 row=s[s.station_id==id].iloc[0];link=p['map_links'][0];lat,lon=map(float,link.rsplit('/',1)[-1].split(','));offset=float(hav(row.latitude,row.longitude,lat,lon));scenario.loc[scenario.station_id==id,['latitude','longitude']]=[lat,lon]
 review.append({'station_id':id,'location_name':row.location_name,'source_latitude':row.latitude,'source_longitude':row.longitude,'official_directions_candidate_latitude':lat,'official_directions_candidate_longitude':lon,'straight_line_disagreement_km':offset,'official_page_url':p['url'],'official_map_url':link,'official_request_id':p['request_id'],'status':'material_conflict' if offset>1 else 'approximate_spatial_agreement','interpretation':'Current official branch map direction, not independent field confirmation of charger location; source16Jun2026 vs officialpage11Nov2026'})
r=pd.DataFrame(review);r.to_csv(OUT/'five_branch_coordinate_crosscheck.csv',index=False)
nonauto=scenario[~scenario.station_id.isin(a.station_id)]
results=[]
for _,row in a.iterrows():
 cand=scenario[scenario.station_id==row.station_id].iloc[0];d=hav(cand.latitude,cand.longitude,nonauto.latitude.to_numpy(),nonauto.longitude.to_numpy());idx=int(d.argmin())
 results.append({'station_id':row.station_id,'location_name':row.location_name,'original_nearest_nonauto_haversine_km':row.nearest_non_auto2000_haversine_km,'scenario_nearest_nonauto_haversine_km':float(d[idx]),'scenario_nearest_name':nonauto.iloc[idx].location_name,'scenario_alternatives_within5km':int((d<=5).sum()),'scenario':'Replace only five matched branch-location coordinates with current official direction candidates; all other sourcecoordinates unchanged','is_verified_actual_charger_location':False})
y=pd.DataFrame(results);y.to_csv(OUT/'auto2000_geo_sensitivity.csv',index=False)
summary={'branch_maps_crosschecked':len(r),'material_coordinate_conflicts_over1km':int((r.straight_line_disagreement_km>1).sum()),'max_coordinate_disagreement_km':float(r.straight_line_disagreement_km.max()),'original_sites_with_nonauto_alternative_within5km':int((y.original_nearest_nonauto_haversine_km<=5).sum()),'scenario_sites_with_nonauto_alternative_within5km':int((y.scenario_nearest_nonauto_haversine_km<=5).sum()),'sites_in_subset':len(y),'original_median_nearest_nonauto_haversine_km':float(y.original_nearest_nonauto_haversine_km.median()),'scenario_median_nearest_nonauto_haversine_km':float(y.scenario_nearest_nonauto_haversine_km.median()),'limitation':'Sensitivity, not correctedgroundtruth. Neighbour coords and station operationalaccess remain unverified. No driving-time/availability conclusion.'}
(OUT/'geo_sensitivity_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(r[['location_name','straight_line_disagreement_km','status']].to_string(index=False));print(y[y.station_id==2397].to_string(index=False))
