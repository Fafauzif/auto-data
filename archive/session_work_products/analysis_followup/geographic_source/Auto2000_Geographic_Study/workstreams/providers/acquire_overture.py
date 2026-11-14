"""Acquire bounded Overture Places automotive candidates; no job verification implied.
Usage PYTHONPATH=<overture client directory>:<shared deps> python acquire_overture.py
"""
import os,json,time,pathlib,datetime,concurrent.futures,re,csv,hashlib
import overturemaps.core as core,pyarrow as pa,pyarrow.parquet as pq,pyarrow.fs as fs
from shapely import from_wkb
R=pathlib.Path(__file__).parent; (R/'raw').mkdir(exist_ok=True)
RELEASE='2026-10-21.0'
core._s3_filesystem=lambda connect_timeout=None,request_timeout=None:fs.S3FileSystem(anonymous=True,region='us-west-2',connect_timeout=15,request_timeout=60,proxy_options=os.environ.get('HTTPS_PROXY'))
cores={'Surabaya':[112.64,-7.38,112.84,-7.18],'Medan':[98.59,3.48,98.77,3.69],'Bandung':[107.51,-6.99,107.74,-6.82],'Palembang':[104.66,-3.07,104.85,-2.88], 'Jabodetabek':[106.4,-6.8,107.3,-5.95], 'Bandar Lampung':[105.12,-5.55,105.4,-5.28], 'Balikpapan':[116.76,-1.35,117.02,-1.05], 'Banjarmasin':[114.48,-3.46,114.75,-3.2], 'Samarinda':[117.02,-0.65,117.3,-0.36], 'Pekanbaru':[101.3,0.35,101.6,0.65], 'Padang':[100.25,-1.05,100.5,-0.75], 'Cirebon':[108.44,-6.83,108.67,-6.6], 'Malang':[112.5,-8.08,112.75,-7.85], 'Jember':[113.55,-8.3,113.85,-8.05], 'Kediri':[111.9,-7.95,112.15,-7.65]}
windows={m:{'core':b,'destination_bbox':[b[0]-.08,b[1]-.08,b[2]+.08,b[3]+.08] if i<4 else b,'margin_degrees':.08 if i<4 else 0,'role':'deep_dive' if i<4 else 'screening'} for i,(m,b) in enumerate(cores.items())}
(R/'study_windows.json').write_text(json.dumps(windows,indent=2))
cats={'automotive_repair','automotive_service','auto_body_shop','auto_glass_service','tire_dealer_and_repair','tire_shop','brake_service_and_repair','oil_change','oil_change_station','auto_restoration_service','auto_customization','auto_dealer','used_auto_dealer','commercial_vehicle_dealer','auto_parts_store','motorcycle_repair','motorcycle_dealer'}
corecats={'automotive_repair','automotive_service','brake_service_and_repair','oil_change','oil_change_station'}
cols=['id','geometry','confidence','websites','brand','addresses','names','sources','operating_status','basic_category','taxonomy','version','bbox']
def get(m,win):
 t=time.time(); p=R/'raw'/(m.lower().replace(' ','_')+'_automotive_source.parquet');log={'market':m,'bbox':win['destination_bbox'],'release':RELEASE,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  if p.exists(): table=pq.read_table(p);total=None
  else:
   ds,fil=core._prepare_query('place',win['destination_bbox'],RELEASE,15,60,True)
   table=ds.to_table(columns=cols,filter=fil);total=table.num_rows
   rows=table.select(['taxonomy','names']).to_pylist();keep=[]
   for r in rows:
    cat=(r['taxonomy'] or {}).get('primary',''); name=(r['names'] or {}).get('primary','') or ''
    keep.append(cat in cats or bool(re.search(r'auto\s*2000|otoxpert|oto\s*xpert',name,re.I)))
   table=table.filter(pa.array(keep));pq.write_table(table,p)
  log.update(status='success',source_all_place_rows=total,automotive_candidate_rows=table.num_rows,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),seconds=round(time.time()-t,2))
  print(json.dumps(log),flush=True);(R/(m.lower().replace(' ','_')+'_acquisition.json')).write_text(json.dumps(log,indent=2));return log
 except Exception as e:
  log.update(status='failed',error=str(e),seconds=round(time.time()-t,2));print(json.dumps(log),flush=True);(R/(m.lower().replace(' ','_')+'_acquisition.json')).write_text(json.dumps(log,indent=2));return log
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:logs=list(pool.map(lambda x:get(*x),windows.items()))
 (R/'overture_acquisition_log.json').write_text(json.dumps(logs,indent=2))
