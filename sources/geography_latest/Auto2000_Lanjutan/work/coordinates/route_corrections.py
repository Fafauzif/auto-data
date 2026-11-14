from pathlib import Path
import sys,csv,json,time
BASE=Path(__file__).resolve().parents[2]/'extracted/baseline/Auto2000_Geographic_Study'
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/'workstreams/routing'))
from route_analysis import Client,read_csv,write_csv
origins=read_csv(BASE/'workstreams/routing/output/origins.csv')
client=Client('https://router.project-osrm.org',OUT/'cache',1.2)
endpoints=[{'market':'Bandung','destination_id':'auto2000:suci_corrected','name':'Auto2000 Suci','latitude':-6.901998,'longitude':107.648162,'source_url':'https://legaleraindonesia.com/tempat/toyota-auto2000-bandung-suci','coordinate_status':'alternate_public_directory_AppleMaps_link_and_Overture_address_match'}, {'market':'Surabaya','destination_id':'auto2000:sidoarjo_corrected','name':'Auto2000 Sidoarjo','latitude':-7.44129770661389,'longitude':112.719738826777,'source_url':'https://auto2000.co.id/dealer-toyota/surabaya/auto2000kabupatensidoarjo','coordinate_status':'decoded_official_decimal_order_and_Overture_address_match'}]
pairs=[]
for d in endpoints:
 oo=[x for x in origins if x['market']==d['market']]
 for direction in ['outbound','return']:
  a,b=(oo,[d]) if direction=='outbound' else ([d],oo)
  x=client.table(a,b)
  for i,o in enumerate(oo):
   si,di=(i,0) if direction=='outbound' else (0,i)
   pairs.append({'market':d['market'],'origin_id':o['origin_id'],'origin_longitude':o['longitude'],'origin_latitude':o['latitude'],'destination_id':d['destination_id'],'destination_name':d['name'],'destination_longitude':d['longitude'],'destination_latitude':d['latitude'],'kind':'auto2000','direction':direction,'duration_seconds':x['durations'][si][di],'distance_metres':x['distances'][si][di],'origin_snap_metres':x['sources'][si]['distance'],'destination_snap_metres':x['destinations'][di]['distance'],'source_url':d['source_url'],'capability_status':'official general workshop; exact job/model/slot unconfirmed'})
  print(d['name'],direction,len(oo),flush=True)
write_csv(OUT/'corrected_endpoint_od.csv',pairs)
write_csv(OUT/'corrected_endpoints.csv',endpoints)
(OUT/'routing_acquisition_log.json').write_text(json.dumps(client.log,indent=2))
