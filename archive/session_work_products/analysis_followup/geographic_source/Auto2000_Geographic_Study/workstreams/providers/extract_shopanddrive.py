import pathlib,re,json,csv,hashlib,datetime
R=pathlib.Path(__file__).parent;path=R/'shopanddrive_outlet_private.html'
if not path.exists():
 import urllib.request
 path.write_bytes(urllib.request.urlopen(urllib.request.Request('https://www.shopanddrive.com/outlet',headers={'User-Agent':'Mozilla/5.0'}),timeout=45).read())
s=path.read_text();m=re.search(r'var outletCoordinates\s*=\s*',s);records=json.JSONDecoder().raw_decode(s[m.end():])[0];windows=json.loads((R/'study_windows.json').read_text());rows=[]
for i,r in enumerate(records):
 try:lat=float(r['latitude']);lon=float(r['longitude'])
 except:continue
 matches=[]
 for market,w in windows.items():
  b=w['destination_bbox']
  if b[0]<=lon<=b[2] and b[1]<=lat<=b[3]:matches.append(market)
 row={'provider_id':'SD_OFFICIAL_'+str(i+1).zfill(4),'name':r['name'].strip(),'longitude':lon,'latitude':lat,'address':r.get('address','').strip(),'markets':';'.join(matches),'source_url':'https://www.shopanddrive.com/outlet','source_locator':'JavaScript var outletCoordinates, zero-based index '+str(i),'geocode_status':'Official-directory coordinate candidate; not field-verified entrance','service_evidence_level':'Network oil/filter offering; exact Toyota fitment and slot unconfirmed','retrieved_date':'2026-11-14'};rows.append(row)
for name,rs in [('shopanddrive_official_all.csv',rows),('shopanddrive_official_study.csv',[r for r in rows if r['markets']])]:
 with (R/name).open('w') as f:w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rs)
selected=[]
for market,tokens in {'Surabaya':['Lontar','Tidar'],'Bandung':['Buah Batu','Sudirman'],'Medan':['Jamin Ginting','Setiabudi'],'Palembang':['Kenten','Plaju']}.items():
 for tok in tokens:
  found=[r for r in rows if market in r['markets'].split(';') and tok.lower() in r['name'].lower()]
  for r in found:selected.append(dict(r,market=market))
with (R/'shopanddrive_official_focal8.csv').open('w') as f:w=csv.DictWriter(f,list(selected[0]));w.writeheader();w.writerows(selected)
meta={'source_url':'https://www.shopanddrive.com/outlet','retrieved_date':'2026-11-14','source_html_bytes':path.stat().st_size,'source_html_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_rows':len(records),'valid_coordinate_rows':len(rows),'study_window_rows':sum(bool(r['markets']) for r in rows),'focal_selected_rows':len(selected),'extraction':'Selected business facts from inline JSON var outletCoordinates; telephone field intentionally excluded; full source HTML not redistributed','locator':'HTML line22332 in captured source; upstream markup can change'}
(R/'shopanddrive_source_receipt.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2));print(json.dumps(selected,indent=2))
