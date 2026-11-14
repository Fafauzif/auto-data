import pathlib,json,re,csv,math,collections
import pyarrow.parquet as pq
from shapely import from_wkb
R=pathlib.Path(__file__).parent
windows=json.loads((R/'study_windows.json').read_text())
corecats={'automotive_repair','automotive_service','brake_service_and_repair','oil_change','oil_change_station'}
rows=[]
for m,win in windows.items():
 p=R/'raw'/(m.lower().replace(' ','_')+'_automotive_source.parquet')
 if not p.exists():continue
 for r in pq.read_table(p).to_pylist():
  point=from_wkb(r['geometry']); name=(r['names'] or {}).get('primary','') or ''; cat=(r['taxonomy'] or {}).get('primary','') or ''; low=name.lower(); conf=r['confidence'] or 0
  auto=bool(re.search(r'auto\s*2000',low)); oto=bool(re.search(r'oto\s*xpert',low)); motor=cat.startswith('motorcycle') or bool(re.search(r'\b(ahass|motorcycle|bengkel motor|sepeda motor|yamaha|vespa|kawasaki|ducati|benelli|kymco|scooter|scoopy|vario|nmax|aerox|rx king)\b',low)); brand=bool(re.search(r'\b(toyota|daihatsu|mitsubishi|nissan|wuling|hyundai|mazda|isuzu|chery|suzuki|honda|byd|mercedes|bmw|kia)\b',low))
  group='Auto2000 name match' if auto else 'OtoXpert name match' if oto else 'Motorcycle-oriented' if motor else 'Brand-associated candidate' if brand else 'General repair/service candidate' if cat in corecats else 'Specialist repair candidate' if cat in {'auto_body_shop','auto_glass_service','tire_dealer_and_repair','tire_shop','auto_restoration_service','auto_customization'} else 'Dealer/parts candidate'
  excl=[]
  if cat not in corecats:excl.append('not_general_repair_category')
  if motor:excl.append('motorcycle_oriented')
  if auto or oto:excl.append('network_name_match')
  if brand:excl.append('brand_associated_uncertain_independence')
  if re.search(r'\b(truk|truck|bus|trailer)\b',low):excl.append('commercial_vehicle_oriented_name')
  if conf<.7:excl.append('source_confidence_below_0.7')
  if (r['operating_status'] or '').lower() in {'closed','permanently_closed'}:excl.append('source_closed')
  source_datasets=';'.join(sorted({s.get('dataset','') or '' for s in (r['sources'] or [])}));licenses=';'.join(sorted({s.get('license','') or '' for s in (r['sources'] or [])}))
  addr=' | '.join((a.get('freeform') or '') for a in (r['addresses'] or []))
  b=win['core'];incore=b[0]<=point.x<=b[2] and b[1]<=point.y<=b[3]
  row=dict(market=m,id=r['id'],name=name,longitude=point.x,latitude=point.y,primary_category=cat,provider_group=group,eligible_candidate=not excl,exclusion_reasons=';'.join(excl),capability_status='Unverified for Toyota model and specific job',operating_status=r['operating_status'] or 'unknown',confidence=conf,in_core=incore,source_license=licenses,source_release='2026-10-21.0',source_datasets=source_datasets,websites=';'.join(r['websites'] or []),address=addr,duplicate_of='',explicit_car_name=bool(re.search(r'\b(mobil|car|cars)\b',low)),ambiguous_motor_name=bool(re.search(r'\bmotor\b',low) and not motor))
  rows.append(row)
# Flag probable same-name co-locations; retain all records, exclude duplicate from candidate pool.
namegroups=collections.defaultdict(list)
for r in rows:
 norm=re.sub(r'[^a-z0-9]','',r['name'].lower())
 if norm:namegroups[(r['market'],norm)].append(r)
for group in namegroups.values():
 group.sort(key=lambda x:(-x['confidence'],x['id']))
 retained=[]
 for r in group:
  dup=None
  for k in retained:
   dy=(r['latitude']-k['latitude'])*111.2;dx=(r['longitude']-k['longitude'])*111.2*math.cos(math.radians(r['latitude']))
   if math.hypot(dx,dy)<=.075:dup=k;break
  if dup:
   r['duplicate_of']=dup['id'];r['eligible_candidate']=False;r['exclusion_reasons']+=';same_normalized_name_within75m'
  else:retained.append(r)
fields=list(rows[0]) if rows else []
if rows:
 with (R/'provider_inventory.csv').open('w') as f:
  w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
 features=[{'type':'Feature','id':r['id'],'geometry':{'type':'Point','coordinates':[r['longitude'],r['latitude']]},'properties':{k:v for k,v in r.items() if k not in ['longitude','latitude']}} for r in rows]
 (R/'provider_inventory.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
 summary=[]
 for m in windows:
  rs=[r for r in rows if r['market']==m]
  if rs:summary.append({'market':m,'automotive_source_rows':len(rs),'general_repair_category_rows':sum(r['primary_category'] in corecats for r in rs),'eligible_candidate_rows':sum(r['eligible_candidate'] for r in rs),'eligible_core_rows':sum(r['eligible_candidate'] and r['in_core'] for r in rs),'motorcycle_oriented_rows':sum(r['provider_group']=='Motorcycle-oriented' for r in rs),'probable_duplicate_rows':sum(bool(r['duplicate_of']) for r in rs),'auto2000_name_rows':sum(r['provider_group']=='Auto2000 name match' for r in rs),'otoxpert_name_rows':sum(r['provider_group']=='OtoXpert name match' for r in rs),'documented_job_capability_rows':0})
 if summary:
  with (R/'market_provider_summary.csv').open('w') as f:w=csv.DictWriter(f,list(summary[0]));w.writeheader();w.writerows(summary)
 print(json.dumps({'rows':len(rows),'markets':len(summary),'eligible':sum(r['eligible_candidate'] for r in rows),'summary':summary}),flush=True)
