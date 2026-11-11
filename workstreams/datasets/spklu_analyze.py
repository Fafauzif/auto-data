from acquire import OUT,CACHE
import pandas as pd,numpy as np,json
s=pd.read_csv(CACHE/'spklu_stations.csv'); c=pd.read_csv(CACHE/'spklu_chargers.csv'); b=pd.read_csv(OUT/'bps_vehicle_stock_long.csv')
assert len(s)==2454 and s.station_id.nunique()==2454
assert len(c)==3767
cars=b[(b.year==2025)&b.variable_name_en.str.contains('Passenger Cars')].copy();cars['bps_province_code']=(cars.region_code//100000).astype(int);cars=cars[cars.province_label!='Indonesia']
g=s.groupby(['bps_province_code','province_name']).agg(stations=('station_id','size'),total_chargers=('total_chargers','sum'),total_connectors=('total_connectors','sum'),median_nearest_road_km=('nearest_road_km','median'),sum_source_headline_power_kW_NOT_CAPACITY=('station_power_kW','sum')).reset_index()
g=g.merge(cars[['bps_province_code','province_label','value_units']],on='bps_province_code',how='left',validate='1:1').rename(columns={'value_units':'passenger_vehicle_stock_2025'})
g['stations_per_100000_registered_passenger_vehicles']=100000*g.stations/g.passenger_vehicle_stock_2025
g['national_station_share']=g.stations/g.stations.sum();g['national_car_stock_share']=g.passenger_vehicle_stock_2025/g.passenger_vehicle_stock_2025.sum();g['relative_site_to_car_stock_index']=g.national_station_share/g.national_car_stock_share
g['numerator_snapshot']='2026-06-16';g['denominator_year']=2025;g['interpretation_limit']='All registered passenger vehicles; not BEVs, demand, operational fleet, capacity, queues or uptime; 34-province charging source'
g.to_csv(OUT/'province_charging_vs_registered_cars.csv',index=False)
# Independent all-pair haversine computation, not new observations.
lat=np.deg2rad(s.latitude.to_numpy());lon=np.deg2rad(s.longitude.to_numpy());a=np.sin((lat[:,None]-lat[None,:])/2)**2+np.cos(lat[:,None])*np.cos(lat[None,:])*np.sin((lon[:,None]-lon[None,:])/2)**2
dist=6371.0088*2*np.arcsin(np.sqrt(np.minimum(a,1)));np.fill_diagonal(dist,np.inf)
nearest_idx=dist.argmin(axis=1);own=s.copy();own['computed_nearest_haversine_km']=dist.min(axis=1);own['computed_nearest_station_id']=s.station_id.to_numpy()[nearest_idx];own['computed_nearest_name']=s.location_name.to_numpy()[nearest_idx];own['computed_alternatives_within_5km']=(dist<=5).sum(axis=1)
# Source road-distance fields describe its own limited candidate routing method, not comprehensive routing.
sel=own[(own.operator_brand=='Auto2000')|own.location_name.str.contains('auto.?2000',case=False,regex=True)].copy()
not_auto=~own.index.isin(sel.index);subdist=dist[sel.index][:,not_auto];idx=np.flatnonzero(not_auto)[subdist.argmin(axis=1)]
sel['nearest_non_auto2000_haversine_km']=subdist.min(axis=1);sel['nearest_non_auto2000_name']=s.location_name.to_numpy()[idx]
cols=['station_id','location_name','province_name','regency_city_clean','latitude','longitude','provider_type','operator_brand','station_power_kW','total_chargers','total_connectors','nearest_road_km','computed_nearest_haversine_km','computed_nearest_station_id','computed_nearest_name','computed_alternatives_within_5km','nearest_non_auto2000_haversine_km','nearest_non_auto2000_name','quality_flags']
sel[cols].to_csv(OUT/'auto2000_charging_context.csv',index=False)
pd.crosstab(s.provider_type,s.location_group).to_csv(OUT/'charging_provider_venue_crosstab.csv')
s.groupby('operator_brand',dropna=False).agg(stations=('station_id','size'),median_power_kW=('station_power_kW','median'),median_nearest_road_km=('nearest_road_km','median')).to_csv(OUT/'charging_operator_summary.csv')
quality={'station_rows':len(s),'unique_station_ids':s.station_id.nunique(),'charger_box_rows':len(c),'orphan_charger_station_ids':len(set(c.station_id)-set(s.station_id)),'source_total_chargers':int(s.total_chargers.sum()),'source_total_connectors':int(s.total_connectors.sum()),'station_col_count':len(s.columns),'missing_coordinates':int(s[['latitude','longitude']].isna().any(axis=1).sum()),'source_provider_counts':s.provider_type.value_counts().to_dict(),'matched_bps_provinces':int(g.passenger_vehicle_stock_2025.notna().sum()),'site_to_stock_ratio_limit':'2026 charging sites / 2025 all passenger registered cars, not per-BEV capacity','auto2000_name_matched_rows':len(sel),'auto2000_median_non_auto_nearest_haversine_km':float(sel.nearest_non_auto2000_haversine_km.median()),'auto2000_with_other_charger_site_within5km':int((sel.nearest_non_auto2000_haversine_km<=5).sum()),'distance_comparisons_computed':len(s)*(len(s)-1),'distance_comparisons_are_derived_not_observations':True,'source_road_distance_missing':int(s.nearest_road_km.isna().sum()),'source_road_distance_max_km':float(s.nearest_road_km.max()),'source_coordinates_flags':int(s.quality_flags.fillna('').str.contains('coord',case=False).sum())}
(OUT/'spklu_analysis_summary.json').write_text(json.dumps(quality,indent=2))
print(json.dumps(quality,indent=2));print(g.sort_values('stations',ascending=False)[['province_name','stations','passenger_vehicle_stock_2025','stations_per_100000_registered_passenger_vehicles']].head(10).to_string(index=False));print(sel[cols].to_string(index=False)[:3000])
