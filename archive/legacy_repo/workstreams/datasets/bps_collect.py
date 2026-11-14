from acquire import get,OUT,CACHE
import re,json,csv
base='https://www.bps.go.id/en/statistics-table/3/VjJ3NGRGa3dkRk5MTlU1bVNFOTVVbmQyVURSTVFUMDkjMyMwMDAw/jumlah-kendaraan-bermotor-menurut-provinsi-dan-jenis-kendaraan--unit-.html?year='
rows=[];metadata=[]
for year in range(2019,2026):
 path=CACHE/('bps_stock_'+str(year)+'.html')
 if year==2024:
  s=(CACHE/'bps_vehicle_stock.html').read_text()
 else:
  r=get(path.name,base+str(year))
  if r.status!=200:continue
  s=r.text
 parts=[]
 for m in re.finditer(r'self\.__next_f\.push\(\[1,("(?:\\.|[^"\\])*")\]\)',s):parts.append(json.loads(m.group(1)))
 text=''.join(parts);i=text.find('{"status":"OK","data-availability"')
 if i<0: print('NO_DATA',year,flush=True);continue
 obj,n=json.JSONDecoder().raw_decode(text[i:]);data=obj['data'][1];actual=data['tahun_data']; assert actual==year,(year,actual)
 meta={k:v for k,v in data.items() if k!='data'};meta['source_url']=base+str(year);metadata.append(meta)
 for item in data['data']:
  for key,val in item['variables'].items():
   raw=val['value_raw'];num=int(raw.replace('.','')) if isinstance(raw,str) and raw.replace('.','').isdigit() else None
   rows.append({'year':year,'province_label':item['label'],'region_code':item['kode_wilayah'],'variable_id':key,'variable_name_en':data['kolom'][key]['nama_variabel_en'],'value_raw':raw,'value_units':num,'source_url':base+str(year)})
 with (OUT/'bps_vehicle_stock_long.csv').open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 (OUT/'bps_metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False))
 print('EXTRACTED',year,len(data['data']),len(rows),flush=True)
