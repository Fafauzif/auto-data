import os,json,time,hashlib
from pathlib import Path
import overturemaps.core as core,pyarrow.parquet as pq,pyarrow.fs as fs
R=Path(__file__).resolve().parent
D=R.parents[1]/'source_building_queries';D.mkdir(exist_ok=True)
core._s3_filesystem=lambda connect_timeout=None,request_timeout=None:fs.S3FileSystem(anonymous=True,region='us-west-2',connect_timeout=15,request_timeout=60,proxy_options=os.environ.get('HTTPS_PROXY'))
# Small urban windows only, to anchor grid sensitivity to mapped built structures.
boxes={'bandung_southwest':[107.56,-6.99,107.69,-6.92], 'sidoarjo':[112.69,-7.46,112.76,-7.40], 'surabaya_west':[112.64,-7.38,112.74,-7.29], 'surabaya_south':[112.69,-7.36,112.78,-7.28],'surabaya_east':[112.73,-7.30,112.81,-7.23],'palembang_north':[104.69,-2.98,104.79,-2.88],'bandung_east':[107.64,-6.96,107.75,-6.86],'jakarta_south':[106.75,-6.29,106.84,-6.20]}
logs=[]
for name,b in boxes.items():
 p=D/(name+'_buildings.parquet');t=time.time()
 try:
  if not p.exists():
   ds,fil=core._prepare_query('building',b,'2026-10-21.0',15,60,True)
   cols=[x for x in ['id','geometry','sources','class','subtype','height','num_floors','bbox'] if x in ds.schema.names]
   tab=ds.to_table(columns=cols,filter=fil);pq.write_table(tab,p)
  else:tab=pq.read_table(p)
  x={'name':name,'bbox':b,'rows':tab.num_rows,'release':'2026-10-21.0','seconds':round(time.time()-t,2),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'status':'ok'}
 except Exception as e:x={'name':name,'bbox':b,'error':str(e),'status':'failed'}
 print(json.dumps(x),flush=True);logs.append(x);(R/'building_acquisition_log.json').write_text(json.dumps(logs,indent=2))
