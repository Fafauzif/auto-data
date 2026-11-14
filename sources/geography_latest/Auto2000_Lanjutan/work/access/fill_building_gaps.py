import os,json,time,hashlib
from pathlib import Path
import pandas as pd,pyarrow.parquet as pq,pyarrow.fs as fs
import overturemaps.core as core
R=Path(__file__).resolve().parent
D=R.parents[1]/'source_building_queries';D.mkdir(exist_ok=True)
core._s3_filesystem=lambda connect_timeout=None,request_timeout=None:fs.S3FileSystem(anonymous=True,region='us-west-2',connect_timeout=15,request_timeout=60,proxy_options=os.environ.get('HTTPS_PROXY'))
q=pd.read_csv(R/'shifted_and_bridge_targets.csv');b=pd.read_csv(R/'built_origins.csv');have=set(b.origin_id.str.replace('built_','',n=1));logs=[]
for _,z in q[~q.origin_id.isin(have)].iterrows():
 p=D/(str(z.origin_id)+'_buildings.parquet');box=[z.longitude-.004,z.latitude-.004,z.longitude+.004,z.latitude+.004];t=time.time()
 if p.exists():tab=pq.read_table(p)
 else:
  ds,fil=core._prepare_query('building',box,'2026-10-21.0',15,60,True);tab=ds.to_table(columns=[x for x in ['id','geometry','sources','class','subtype','bbox'] if x in ds.schema.names],filter=fil);pq.write_table(tab,p)
 r={'target':z.origin_id,'bbox':box,'rows':tab.num_rows,'seconds':time.time()-t,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};print(json.dumps(r),flush=True);logs.append(r);(R/'building_gap_acquisition_log.json').write_text(json.dumps(logs,indent=2))
