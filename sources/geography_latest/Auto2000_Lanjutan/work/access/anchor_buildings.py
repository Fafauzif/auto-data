from pathlib import Path
import pandas as pd,numpy as np,json
import pyarrow.parquet as pq,pyarrow as pa
from shapely import from_wkb
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parent
q=pd.read_csv(R/'shifted_and_bridge_targets.csv').fillna('');q['best_distance_m']=1e99;q['building_id']='';q['building_geometry']='';q['source_file']='';q['building_longitude']=np.nan;q['building_latitude']=np.nan
selection=[]
for p in sorted((R.parents[1]/'source_building_queries').glob('*_buildings.parquet')):
 t=pq.read_table(p);a=t['bbox'].to_pylist();x=np.array([(z['xmin']+z['xmax'])/2 for z in a]);y=np.array([(z['ymin']+z['ymax'])/2 for z in a]);tree=cKDTree(np.c_[x*np.cos(np.radians(-6)),y]);points=np.c_[q.longitude.to_numpy()*np.cos(np.radians(-6)),q.latitude.to_numpy()];dist,idx=tree.query(points,k=5)
 for i in range(len(q)):
  for j in idx[i]:
   r=t.slice(int(j),1).to_pylist()[0];geom=from_wkb(r['geometry']);rp=geom.representative_point();m=111195*np.hypot((rp.x-q.loc[i,'longitude'])*np.cos(np.radians(rp.y)),rp.y-q.loc[i,'latitude'])
   if m<q.loc[i,'best_distance_m']:
    q.loc[i,['best_distance_m','building_id','building_geometry','source_file','building_longitude','building_latitude']]=[m,r['id'],geom.wkt,p.name,rp.x,rp.y]
    selection.append((i,m,r))
 print(p.name,t.num_rows,flush=True)
rows=[];features=[];kept=[]
for i,z in q.iterrows():
 if z.best_distance_m>400:
  print('No nearbybuilding',z.origin_id,z.best_distance_m);continue
 r=z.to_dict();r['target_longitude']=r['longitude'];r['target_latitude']=r['latitude'];r['longitude']=r.pop('building_longitude');r['latitude']=r.pop('building_latitude');r['origin_id']='built_'+str(r['origin_id']);r['origin_type']='mapped_building_representative_point';rows.append(r)
 source=next(r0 for i0,m0,r0 in selection if i0==i and r0['id']==z.building_id);kept.append(source)
 from shapely.geometry import mapping
 features.append({'type':'Feature','geometry':mapping(from_wkb(source['geometry'])),'properties':{'id':source['id'],'source_datasets':';'.join(sorted(set(s['dataset'] for s in source['sources']))),'origin_id':r['origin_id'],'target_displacement_m':z.best_distance_m,'class':source.get('class'),'subtype':source.get('subtype')}})
built=pd.DataFrame(rows);built.drop(columns=['building_geometry']).to_csv(R/'built_origins.csv',index=False)
shift=q[q.origin_type=='half_cell_shift'].copy();shift['target_longitude']=shift.longitude;shift['target_latitude']=shift.latitude
allorig=pd.concat([shift.drop(columns=['building_geometry','building_longitude','building_latitude','best_distance_m','building_id','source_file']),built.drop(columns=['building_geometry'])],ignore_index=True).fillna('');allorig.to_csv(R/'new_origins.csv',index=False)
(R/'selected_building_footprints.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
pq.write_table(pa.Table.from_pylist(kept),R/'selected_building_source.parquet')
print('new origins',len(allorig),'building origins',len(built),'max displacement',built.best_distance_m.max())
