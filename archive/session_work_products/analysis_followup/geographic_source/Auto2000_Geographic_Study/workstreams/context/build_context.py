from pathlib import Path
import csv,json,hashlib
P=Path(__file__).parent
D='2026-11-14'
# Facts transcribed from official directory; coordinates are embedded map-link candidates, not field checks.
rows=[
('Thamrin Medan','Deltamas','Medan',1,3.5958000353538124,98.68775621831999,'Mon-Sat 08:30-17:00'),
('Ring Road Medan','Auto2000','Medan',1,3.551358444648945,98.62613937888233,'Mon-Sun 08:00-18:00'),
('Tritura Medan','Perintis','Medan',1,3.5383074486789727,98.69074866024502,'Mon-Sat 08:30-17:00'),
('Padang','Auto2000','Padang',1,-.9450501,100.3699044,'Mon-Sun 08:00-18:00'),
('Pekanbaru','Agung Automall','Pekanbaru',1,.4773720018451019,101.42980527311356,'Mon-Sun 08:00-16:00'),
('Jambi','Agung Automall','Jambi',1,-1.613235881305425,103.61561781282792,'Mon-Sun 08:00-17:00'),
('Palembang','Auto2000','Palembang',1,-2.927153441929458,104.76998568111011,'Mon-Sun 08:00-18:00'),
('Batam','Agung Automall','Batam',1,1.136828451368845,104.0014688434337,'Mon-Sun 08:00-16:00'),
('Kelapa Gading','Auto2000','Jakarta',1,-6.173243109852233,106.89756595928591,'Mon-Sun 08:00-18:00'),
('Fatmawati','Auto2000','Jakarta',1,-6.290985691487656,106.79491103472631,'Mon-Sun 08:00-18:00'),
('Rawasari','Auto2000','Jakarta',2,-6.185757354857489,106.87102744673018,'Mon-Sun 08:00-18:00'),
('Pos Pengumben','Astrido','Jakarta',2,-6.2161598,106.7734466,'Mon-Sun 08:00-18:00'),
('Jatimurni','Tunas Group','Bekasi',2,-6.31904,106.92410,'Mon-Sun 08:00-20:00'),
('Karawang','Auto2000','Karawang',2,-6.316667767858572,107.29377232407815,'Mon-Sun 08:00-18:00'),
('Peta','Auto2000','Bandung',2,-6.937163100221827,107.60054786216769,'Mon-Sun 08:00-18:00'),
('Bojongsoang','Auto2000','Bandung',2,-6.983194031481277,107.63356297442269,'Mon-Sun 08:00-18:00'),
('Tambun','Auto2000','Bekasi',2,-6.255975026608349,107.05841708322806,'Mon-Sun 08:00-18:00'),
('Bogor','Auto2000','Bogor',2,-6.5844525335962585,106.8172988670249,'Mon-Sun 08:00-18:00'),
('Tasikmalaya','Sinarmas','Tasikmalaya',2,-7.302253129852767,108.19367157348981,'Mon-Sat 08:00-16:30'),
('Antapani','Wijaya','Bandung',2,-6.914450913659831,107.65220448538085,'Mon-Sun 08:00-16:00'),
('Semarang','Nasmoco','Semarang',3,-6.986916174588131,110.45550539224016,'Mon-Sun 08:00-16:30'),
('Dukuh Kupang','Liek Motor','Surabaya',3,-7.286958387953755,112.71478975442125,'Mon-Sat 08:00-16:15'),
('Sulfat','Kartika Sari','Malang',3,-7.962368105553717,112.65316883554634,'Mon-Sat 08:00-16:30'),
('Rungkut','Auto2000','Surabaya',3,-7.33160369596501,112.78343903008502,'Mon-Sun 08:00-18:00'),
('Ciater Barat BSD','Auto2000','Tangerang Selatan',3,-6.334254646024867,106.6869007540283,'Mon-Sun 09:00-18:00'),
('Cipondoh','Auto2000','Tangerang',3,-6.186272252970748,106.65571274528271,'Mon-Sun 08:00-18:00'),
('Denpasar','Agung Automall','Denpasar',3,-8.636390907587955,115.1874018199011,'Mon-Sun 08:00-16:00'),
('Banjarmasin','Wiramegah Profitamas','Banjarmasin',3,-3.2814678,114.5896235,'Mon-Sat 08:00-16:30'),
('Balikpapan','Auto2000','Balikpapan',3,-1.2274847329033705,116.8708593189664,'Mon-Sun 08:00-18:00'),
('Samarinda','Graha Mulia Auto','Samarinda',3,-.49975527850243884,117.14781652978397,'Mon-Sun 08:00-18:00'),
('Tikala Manado','Hasjrat Abadi','Manado',4,1.482996959344779,124.84694565889544,'Mon-Sun 08:00-18:00'),
('Samratulangi','Kalla','Palu',4,-.8820910200702996,119.8722714883459,'Mon-Sat 08:00-17:00'),
('Hertasning','Kalla','Gowa',4,-5.184093108716737,119.47054997557778,'Mon-Sun 08:00-17:00'),
('Daya','Kalla','Makassar',4,-5.115263159635955,119.51166227459905,'Mon-Sat 08:00-17:00'),
('Kumala','Kalla','Makassar',4,-5.16998856418988,119.41878543012771,'Mon-Sat 08:00-17:00'),
('Sengkang','Kalla','Wajo',4,-4.1232184,120.0325037,'Mon-Sat 08:00-17:00'),
('Kendari','Kalla','Kendari',4,-3.9774347940232757,122.52364133545798,'Mon-Sat 08:00-17:00')]
cols=['provider_id','name','operator','city','directory_page','latitude','longitude','published_hours','source_url','map_link','retrieved_date','coordinate_status','job_capability_status','auto2000_operator','limitations']
out=[]
for i,(name,op,city,page,lat,lon,hours) in enumerate(rows,1):
 u='https://otoxpert.co.id/workshop'+('' if page==1 else '?page='+str(page))
 out.append(dict(zip(cols,[f'OX{i:03}','OtoXpert '+name,op,city,page,lat,lon,hours,u,f'https://maps.google.com/maps?output=embed&q={lat},{lon}',D,'official_directory_embedded_map_candidate','network_advertised_oil_and_brakes; outlet/model/job_unconfirmed',op=='Auto2000','Official listing, not site visit; hours and capacity unconfirmed; embedded maps could not be rendered'])))
with (P/'otoxpert_official_inventory.csv').open('w') as f:
 w=csv.DictWriter(f,cols);w.writeheader();w.writerows(out)
(P/'otoxpert_official_inventory.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','geometry':{'type':'Point','coordinates':[x['longitude'],x['latitude']]},'properties':x} for x in out]},indent=2))
print('Saved OtoXpert entries',len(out),'Auto2000-operated',sum(x['auto2000_operator'] for x in out))
# Context source register. Facts are paraphrased; no full third-party page bodies redistributed.
sources=[
('CX01','Auto2000 branch directory','Auto2000','https://auto2000.co.id/dealer-toyota','','2026-11-14','Official geographic presence; lists 12 regional groups; branch service tags vary.','turn842069620view2'),
('CX02','OtoXpert workshop directory page1','OtoXpert','https://otoxpert.co.id/workshop','','2026-11-14','Ten directory entries in returned page, plus embedded map URLs.','turn339765246view0'),
('CX03','OtoXpert workshop directory page2','OtoXpert','https://otoxpert.co.id/workshop?page=2','','2026-11-14','Ten directory entries in returned page, plus embedded map URLs.','turn339765246view1'),
('CX04','OtoXpert workshop directory page3','OtoXpert','https://otoxpert.co.id/workshop?page=3','','2026-11-14','Ten directory entries in returned page, plus embedded map URLs.','turn339765246view2'),
('CX05','OtoXpert workshop directory page4','OtoXpert','https://otoxpert.co.id/workshop?page=4','','2026-11-14','Seven directory entries in returned page, plus embedded map URLs.','turn339765246view3'),
('CX06','Ganti Oli','OtoXpert','https://www.otoxpert.co.id/parts-and-services/service/ganti-oli','','2026-11-14','Advertised oil/gasket/filter package from IDR299000, approximately30min; location and vehicle conditions affect price.','turn653153021view2'),
('CX07','Economical workshop and parts alternatives before Eid','Toyota Astra Motor','https://pressroom.toyota.astra.co.id/persiapan-mudik-lebaran-dengan-biaya-lebih-terjangkau-berkualitas-dan-bergaransi-manfaatkan-layanan','2026-03-04','2026-11-14','OtoXpert multibrand light-service alternative; oil/brake work and economical T-OPT filters/pads advertised. Release states40 outlets.','turn653153021view0'),
('CX08','T-OPT product catalogue','Toyota Astra Motor','https://aftersales.toyota.astra.co.id/products/topt','','2026-11-14','Oil filter, brake pad and other product categories listed; model fitment search; page states38 OtoXpert outlets.','turn653153021view1'),
('CX09','T-CARE XTRA','Toyota Astra Motor','https://pressroom.toyota.astra.co.id/toyota-perkuat-layanan-purnajual-lewat-t-care-xtra','2026-08-01','2026-11-14','Customer-paid scheduled services8–11 may earn incremental warranty; maximum total6years/160000km subject to conditions.','turn653153021view3'),
('CX10','Hybrid Health Check','Toyota Astra Motor','https://aftersales.toyota.astra.co.id/hybrid-health-check','','2026-11-14','HEV/BEV models listed; battery check linked to scheduled service and programme eligibility; certificate offered.','turn842069620view0'),
('CX11','Hybrid Health Check FAQ','Toyota Astra Motor','https://itstimeforeveryone.toyota.astra.co.id/news-and-events/faqs-toyota-hybrid-health-check-layanan-gratis-untuk-bev-dan-hev-toyota-usia-35-tahun','2026-10-29','2026-11-14','Year3–5 /50000–100000km description; FAQ subset still hybrid-worded.','turn591321430search1'),
('CX12','Auto2000 Life is Easy','Auto2000','https://auto2000.co.id/berita-dan-tips/auto2000-life-is-easy','2025-05-23','2026-11-14','Historical company-wide network and technician readiness statement; no branch-by-job certification register.','turn842069620view1'),
('CX13','SPKLU geographic dataset V2','Wiputra and Santiadi','https://doi.org/10.17632/z2bvd5r574.2','2026-06-16','2026-11-14','Existing archive source:2454 consolidated charging records. Snapshot not current operation, capacity or demand.','local_repo'),
]
fields=['source_id','title','publisher','url','published_date','retrieved_date','bounded_facts','retrieval_ref']
with (P/'sources.csv').open('w') as f:w=csv.writer(f);w.writerow(fields);w.writerows(sources)
# Fifteen non-overlapping named city/city+county screening definitions, not official metro boundaries.
markets=[
('Jakarta core',['Kota Administrasi Jakarta Selatan','Kota Administrasi Jakarta Pusat','Kota Administrasi Jakarta Barat','Kota Administrasi Jakarta Timur','Kota Administrasi Jakarta Utara'],['Jakarta'],'dense capital core','screen retained: capital core; excluded primary for comparative practical scope, not low opportunity'),
('Surabaya',['Kota Surabaya'],['Surabaya'],'East Java core','primary candidate: Auto2000 and other-operator OtoXpert contrast'),
('Bandung',['Kota Bandung','Kabupaten Bandung','Kabupaten Bandung Barat','Kota Cimahi'],['Bandung'],'basin core and fringe','primary candidate: three economical-channel listings and peripheral destinations'),
('Medan',['Kota Medan','Kabupaten Deli Serdang'],['Medan'],'north Sumatra urban region','primary candidate: three OtoXpert operators and non-Java comparison'),
('Palembang',['Kota Palembang'],['Palembang'],'river city','primary candidate: official branch directory available; river crossings provide road-access contrast'),
('Balikpapan',['Kota Balikpapan'],['Balikpapan'],'coastal Kalimantan','reserve: known historical coordinate conflict; source validation value'),
('Denpasar',['Kota Denpasar','Kabupaten Badung'],['Denpasar'],'tourism-oriented urban corridor','reserve: provider attribution differs from Auto2000'),
('Malang',['Kota Malang','Kabupaten Malang','Kota Batu'],['Malang'],'secondary East Java basin','reserve: urban/rural administrative mix'),
('Bekasi',['Kota Bekasi','Kabupaten Bekasi'],['Bekasi'],'capital-region eastern fringe','reserve: city/county extension; separate from Jakarta core'),
('Bogor',['Kota Bogor','Kabupaten Bogor'],['Bogor'],'capital-region southern fringe','reserve: dispersed administrative geography'),
('Tangerang',['Kota Tangerang','Kota Tangerang Selatan','Kabupaten Tangerang'],['Tangerang','Tangerang Selatan'],'capital-region western fringe','reserve: two Auto2000-operated economical listings'),
('Padang',['Kota Padang'],['Padang'],'west Sumatra coastal city','reserve: smaller urban comparator'),
('Bandar Lampung',['Kota Bandar Lampung'],['Bandar Lampung'],'southern Sumatra city','reserve: no observed OtoXpert directory entry is not proof of absence'),
('Pontianak',['Kota Pontianak'],['Pontianak'],'equatorial river city','reserve: river crossings and no observed economical listing'),
('Banjarmasin',['Kota Banjarmasin','Kota Banjarbaru','Kabupaten Banjar'],['Banjarmasin'],'southern Kalimantan river region','reserve: alternative Toyota operator channel'),
]
base=Path(__file__).resolve().parents[2]/'sources/archive_inputs/raw_licensed_data/SPKLU_CC_BY_NC_3_0/data/spklu_stations.csv'
with base.open() as f:stations=list(csv.DictReader(f))
screen=[]
for m,admins,cities,contrast,status in markets:
 s=[x for x in stations if x['regency_city_clean'] in admins]
 ox=[x for x in out if x['city'] in cities]
 screen.append({'market':m,'administrative_match_definition':';'.join(admins),'auto2000_geographic_presence':'listed in official national directory; branch service verification separate','source_charging_rows':len(s),'source_charging_snapshot':'2026-06-16','observed_otoxpert_directory_entries':len(ox),'observed_auto2000_operated_otoxpert_entries':sum(x['auto2000_operator'] for x in ox),'geographic_contrast':contrast,'screening_recommendation':status,'independent_workshop_completeness':'not assessed in context workstream; discovery agent supplies','routing_feasibility':'not yet assessed in context workstream','toyota_eligible_owner_base':'unknown','workshop_capacity':'unknown','profit_opportunity':'not estimated','caveat':'Administrative selections differ in size; counts are source coverage context, not demand or investment ranking','source_ids':'CX01;CX02;CX03;CX04;CX05;CX13'})
with (P/'screening.csv').open('w') as f:w=csv.DictWriter(f,list(screen[0]));w.writeheader();w.writerows(screen)
# Service-claim facts with bounded branch/vehicle interpretation.
services=[
('SV01','Oil and oil-filter replacement','OtoXpert network','Advertised package includes engine oil, oil gasket and oil filter','from IDR299000','approximately30min advertised','CX06','No model-specific oil volume/grade, outlet stock, final quote or available slot established'),
('SV02','Brake work','OtoXpert network','Toyota advertises brake services at OtoXpert','','','CX07','Brake-pad-only specification, axle, fitment, price, stock and outlet capability unconfirmed'),
('SV03','Oil filter parts','T-OPT catalogue','Oil filter product category and fitment search exist','','','CX08','Catalogue existence not actual outlet stock or accepted fitment'),
('SV04','Brake pad parts','T-OPT catalogue','Brake pad product category exists','','','CX08','Model/variant and axle-specific fitment, stock and installed price not established'),
('SV05','Paid scheduled service','T-CARE XTRA','Services8–11 customer-paid; programme may extend warranty to total6years/160000km','','','CX09','Warranty status and payer are different variables; eligibility depends on vehicle/history/odometer'),
('SV06','Hybrid Health Check','Toyota authorised network','Eligible HEV/BEV programme battery check during scheduled service; certificate provided','programme-eligible check advertised free','','CX10;CX11','No branch-by-job certification or live diagnostic capacity verified; programme text age wording needs eligibility confirmation'),
('SV07','General xEV readiness','Auto2000 network','Company states hybrid-technician readiness and support for Toyota electrified products sold in Indonesia','','','CX12','Corporate claim not branch-specific high-voltage job accreditation'),
('SV08','Economical service routing','OtoXpert operator-specific','Directory identifies Auto2000 and other Toyota-dealer operators','','','CX02;CX03;CX04;CX05','Toyota network retention does not automatically equal Auto2000 contribution'),
]
fields=['evidence_id','job','scope','documented_claim','published_price','published_duration','source_ids','limitations']
with (P/'service_evidence.csv').open('w') as f:w=csv.writer(f);w.writerow(fields);w.writerows(services)
(P/'acquisition_log.json').write_text(json.dumps({'retrieval_date':D,'public_search_and_open':'Web search service used to inspect official pages; reference IDs in sources.csv','direct_network_attempt':{'url':'https://otoxpert.co.id/workshop','outcome':'HTTP403; fallback web retrieval succeeded'},'directory_entries_observed':37,'embedded_coordinate_urls_extracted':37,'embedded_map_render':'Failed redirect/access; coordinates transcribed from official iframe href exposed by click output; not map-render or field verification','raw_web_bodies_redistributed':False,'source_capture_policy':'Structured factual extracts and URLs; no full third-party HTML, images, or downloaded press releases','otoxpert_network_count_disagreement':{'directory_entries_this_run':37,'Toyota_product_page':38,'Toyota_2026_03_04_release':40},'SPKLU_local_source_sha256':hashlib.sha256(base.read_bytes()).hexdigest()},indent=2))
print('Saved sources',len(sources),'markets',len(screen),'service rows',len(services))
