"""Join explicitly reviewed official outlet identities to exact Overture records.
Offline reconstruction of bounded primary-source research; not a capability census.
"""
import csv,json,pathlib
P=pathlib.Path(__file__).parent
src=list(csv.DictReader(open(P.parent/'providers/provider_inventory.csv')))
by={x['id']:x for x in src}
selected=[
('c65f166e-6c0a-4431-aeaa-718bbdbdc98d','Shop & Drive Lontar','Ruko515 Blok D-E Jl.Lontar Raya10-12','outlet name and street numbers10-12 exact match'),
('578255c5-ec64-4b7a-ad8d-29fa1aa3451a','Shop & Drive Tidar','Jl.Tidar250','brand street and number250 exact match'),
('bc0f33df-d3a3-49a5-99a0-11de90121e46','Shop & Drive Buah Batu','Jl.Buah Batu233','brand street and number233 exact match'),
('7212fce0-e3c2-4e3b-b854-6993ca79e00a','Shop & Drive Sudirman','Jl.Jend.Sudirman529-531','brand street and numbers529-531 exact match'),
('1b5a7d5f-41f7-4412-be38-ea8024b78aa3','Shop & Drive Jamin Ginting','Komp.Jamin Ginting Bisnis Point698/88G','brand complex number698/88G and street exact match'),
('1ce4f01a-4810-4864-b84b-1110f6e8d647','Shop & Drive Setiabudi','Jl.Setia Budi71C','brand street and number71C exact match'),
('56c900fd-b778-4662-b0f2-70076359ccaf','Shop & Drive Kenten','Jl.MP Mangkunegara1543C-D','brand outlet street number1543C-D exact match'),
('68d9cc8c-75d2-4d57-b1d5-c525af324fec','Shop & Drive Plaju','Bumi Patra SriwijayaG12 Jl.Jendral A.Yani','brand outlet complex unitG12 and street exact match'),
]
rows=[]
for oid,name,addr,match in selected:
 x=by[oid]
 rows.append(dict(market=x['market'],name=name,brand='Shop & Drive',overture_id=oid,latitude=x['latitude'],longitude=x['longitude'],official_address=addr,overture_address=x['address'],coordinate_source='Overture2026-10-21.0; matched to official outlet identity',coordinate_confidence='matched_candidate_not_entrance_verified',identity_match=match,evidence_level='current_directory_identity_plus_network_advertising',oil_change_evidence='Network FAQ advertises replacement work and oil; oil-filter products offered; Toyota named among brands',oil_filter_bundle_evidence='Expired Jan2026 all-branch promotion explicitly includes selected Toyota models incl Avanza; no current model-year fitment or stock confirmed',brake_evidence='Expired Jan2026 all-branch promotion advertises Akebono brake pads with fitting; no current model-specific job confirmed',exact_scope='Network-advertised oil-service sensitivity subset; NOT confirmed current job/model eligibility',job_specific_confirmed=False,current_price_confirmed=False,current_booking_confirmed=False,identity_source_url='https://www.shopanddrive.com/outlet',capability_source_url='https://www.shopanddrive.com/faq',historical_job_source_url='https://www.shopanddrive.com/promo/promo-new-year-deals',retrieved_date='2026-11-14',ownership_note='Astra Otoparts network/franchise brand; not Auto2000 workshop; outlet owner and GP recipient unverified'))
for oid,name,url in [('e3e1a407-8315-4e59-a74f-12171f5aabf2','Dokter Mobil Lontar','https://www.doktermobil.com/lontar/'),('b4e89631-90e3-432b-a68b-5bc2b8611a20','Dokter Mobil Ngagel','https://www.doktermobil.com/ngagel/'),('e9cc3312-1f65-4792-8646-c73eaaa78ca0','Dokter Mobil Bandung','https://www.doktermobil.com/bandung/')]:
 x=by[oid]
 rows.append(dict(market=x['market'],name=name,brand='Dokter Mobil',overture_id=oid,latitude=x['latitude'],longitude=x['longitude'],official_address=x['address'],overture_address=x['address'],coordinate_source='Overture2026-10-21.0; matched to official branch address',coordinate_confidence='matched_candidate_not_entrance_verified',identity_match='brand and street address number exact match to official branch/city page',evidence_level='local_branch_or_city_oil_advertising',oil_change_evidence='Official local branch/city page advertises engine oil change Cuci Darah',oil_filter_bundle_evidence='Not verified for selected Toyota model/year or equivalent standard oil-filter job',brake_evidence='Not established by reviewed local page',exact_scope='Local oil-change advertising; treatment scope may differ from standard oil-filter job',job_specific_confirmed=False,current_price_confirmed=False,current_booking_confirmed=False,identity_source_url=url,capability_source_url=url,historical_job_source_url='',retrieved_date='2026-11-14',ownership_note='Non-Auto2000 service chain; exact outlet legal operator unverified'))
# Preserve Overture coordinates while preferencing newly acquired official candidates.
from math import radians,sin,cos,asin,sqrt
of=P.parent/'providers/shopanddrive_official_focal8.csv'
if of.exists():
 official=list(csv.DictReader(open(of)))
 assert len(official)==8
 for a,b in zip(rows[:8],official):
  assert a['market']==b['market']
  a['overture_latitude']=a['latitude'];a['overture_longitude']=a['longitude']
  la1,lo1,la2,lo2=map(radians,[float(a['latitude']),float(a['longitude']),float(b['latitude']),float(b['longitude'])])
  a['coordinate_disagreement_m']=6371008.8*2*asin(sqrt(sin((la2-la1)/2)**2+cos(la1)*cos(la2)*sin((lo2-lo1)/2)**2))
  a['latitude']=b['latitude'];a['longitude']=b['longitude']
  a['coordinate_source']='Official Shop & Drive directory embedded outletCoordinates'
  a['coordinate_source_locator']=b['source_locator'];a['coordinate_confidence']='official_candidate_not_entrance_verified'
fields=sorted(set().union(*(x.keys() for x in rows)))
with open(P/'verified_alternative_evidence.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(P/'verified_alternative_evidence.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','geometry':{'type':'Point','coordinates':[float(x['longitude']),float(x['latitude'])]},'properties':x} for x in rows]}))
print(len(rows),'records; none confirmed model-specific current jobs')
