from pathlib import Path
import pandas as pd,json,hashlib
R=Path(__file__).resolve().parent;oo=pd.read_csv(R/'new_origins.csv');dd=pd.read_csv(R/'new_destinations.csv');rows=[]
for m in oo.market.unique():
 o=oo[oo.market==m].to_dict('records');d=dd[dd.market==m].to_dict('records')
 for si in range(0,len(o),20):
  for di in range(0,len(d),60):
   a=o[si:si+20];b=d[di:di+60]
   for direction in ['outbound','return']:
    src,dst=(a,b) if direction=='outbound' else (b,a);coords=src+dst;s=';'.join(f"{x['longitude']:.7f},{x['latitude']:.7f}" for x in coords);i=';'.join(map(str,range(len(src))));j=';'.join(map(str,range(len(src),len(coords))));url='https://router.project-osrm.org'+f'/table/v1/driving/{s}?sources={i}&destinations={j}&annotations=duration,distance';key=hashlib.sha256(url.encode()).hexdigest();p=R/'cache'/(key+'.json');assert p.exists(),p
    rows.append({'market':m,'origin_start':si,'destination_start':di,'direction':direction,'source_count':len(src),'destination_count':len(dst),'url':url,'cache_file':p.name,'response_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(R/'request_manifest.json').write_text(json.dumps(rows,indent=2));print('Requests',len(rows),'cached response hashes verified')
