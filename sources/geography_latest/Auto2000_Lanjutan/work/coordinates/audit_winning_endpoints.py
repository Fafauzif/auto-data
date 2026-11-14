import pathlib,urllib.request,re,json,csv,hashlib
import pandas as pd
R=pathlib.Path(__file__).resolve().parent; B=R.parents[1]/'extracted/baseline/Auto2000_Geographic_Study'
a=pd.read_csv(B/'workstreams/routing/supplement/combined_origin_accessibility.csv');a=a[a.scenario=='snap_le_250m'];d=pd.read_csv(B/'workstreams/routing/inputs/supplement_destinations.csv');counts=a.groupby(['market','shopanddrive_destination_id']).size().rename('nearest_origin_count').reset_index();top=counts.sort_values('nearest_origin_count',ascending=False).groupby('market',sort=False).head(3)
req=urllib.request.Request('https://www.shopanddrive.com/outlet',headers={'User-Agent':'Mozilla/5.0'})
raw=urllib.request.urlopen(req,timeout=45).read();s=raw.decode();m=re.search(r'var outletCoordinates\s*=\s*',s);records=json.JSONDecoder().raw_decode(s[m.end():])[0];out=[]
for _,z in top.iterrows():
 old=d[d.destination_id==z.shopanddrive_destination_id].iloc[0]; hits=[x for x in records if x['name'].strip()==old['name']]
 hits.sort(key=lambda x:(float(x['latitude'])-float(old.latitude))**2+(float(x['longitude'])-float(old.longitude))**2)
 for x in hits[:1]:
  out.append({'market':z.market,'destination_id':z.shopanddrive_destination_id,'name':old['name'],'nearest_origin_count':int(z.nearest_origin_count),'old_latitude':old.latitude,'old_longitude':old.longitude,'current_published_latitude':float(x['latitude']),'current_published_longitude':float(x['longitude']),'current_published_address':x.get('address',''),'same_coordinates':float(x['latitude'])==old.latitude and float(x['longitude'])==old.longitude,'official_directory_still_lists':True,'source_url':'https://www.shopanddrive.com/outlet','source_retrieved_date':'2026-11-14','operating_interpretation':'current directory membership, not observed open/slot/stock','entrance_interpretation':'published site point; OD road snap retained; no gate observation'})
pd.DataFrame(out).to_csv(R/'winning_oil_endpoint_audit.csv',index=False)
(R/'winning_endpoint_source_receipt.json').write_text(json.dumps({'source_url':'https://www.shopanddrive.com/outlet','sha256':hashlib.sha256(raw).hexdigest(),'source_bytes':len(raw),'source_rows':len(records),'audited_top3_each_market':len(out),'all_same_published_coordinates':all(x['same_coordinates'] for x in out),'full_HTML_redistributed':False},indent=2))
print(pd.DataFrame(out)[['market','name','nearest_origin_count','same_coordinates']].to_string(index=False))
