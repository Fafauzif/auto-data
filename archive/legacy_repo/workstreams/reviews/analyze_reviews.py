import json,csv,re,hashlib,datetime,collections,statistics,secrets
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent;PRIVATE=ROOT/'private_cache'/'reviews'
records=json.loads((PRIVATE/'review_records.json').read_text())
for p in PRIVATE.glob('*_apple_reviews.html'):
 s=p.read_text();m=re.search('<script type="application/json" id="serialized-server-data">(.*?)</script>',s,re.S)
 if not m:continue
 data=json.loads(m[1]);name=p.name.replace('_apple_reviews.html','');(PRIVATE/(name+'_apple_dataset.json')).write_text(json.dumps(data,ensure_ascii=False))
 try:
  page=data['data'][0]['data'];items=page['shelfMapping']['allProductReviews']['items']
  for item in items:
   a=item['review'];records.append({'app':name,'platform':'apple_app_store','locale':'ID_storefront','reviewId':a.get('id'),'userName':a.get('reviewerName'),'content':a.get('contents'),'title':a.get('title'),'score':a.get('rating'),'at':a.get('date'),'replyContent':a.get('response'),'reviewCreatedVersion':None,'source_url':data['data'][0].get('url') or 'https://apps.apple.com/id/app/id'+str(page['lockup']['adamId'])+'?see-all=reviews','selection':'public_see_all_embedded_first_page'})
 except Exception as e:print('apple parse error',name,str(e))
if (PRIVATE/'locale_unique_extra.json').exists():records.extend(json.loads((PRIVATE/'locale_unique_extra.json').read_text()))
# Pseudonymization salt remains private; IDs do not imply cross-platform identity.
saltfile=PRIVATE/'reviewer_salt.txt'
if not saltfile.exists():saltfile.write_text(secrets.token_hex(32))
salt=saltfile.read_text()
unique={}
for r in records:
 key=str(r['platform'])+':'+str(r['reviewId']);r['record_key']=key
 if key not in unique:unique[key]=r
records=list(unique.values());(PRIVATE/'normalized_reviews.json').write_text(json.dumps(records,ensure_ascii=False,default=str,indent=2))
rules={
 'booking':r'booking|book service|book.*servis|jadwal.*servi|jadwat.*seevice|service schedule|appointment|antri|antre',
 'records':r'history|riwayat|historis',
 'access':r'login|log in|register|regist|registrasi|verifikasi|verfikasi|otp|profil|profile|daftar',
 'vehicle_link':r'link|koneksi|connect|kendaraan|data mobil|mycar|vin',
 'remote':r'remote|jarak jauh|t.intouch|t-in|geofenc|lokasi mobil|posisi mobil|kunci|unlock|ac |baterai|battery|charge',
 'human_handoff':r'konfirmasi|comfirasi|confirmation|respon|respond|customer|cs |sales|teknisi|bengkel|dealer',
 'cost':r'harga|biaya|bayar|payment|invoice|kuitansi|part|spare|cicilan|dp|diskon|discount',
 'reliability':r'error|bug|hang|crash|gagal|hilang|lemot|lambat|tidak bisa|gak bisa|ga bisa|nggak bisa|tidak dapat|cannot|can.t|unable|failed|stuck',
 'benefits':r'promo|poin|point|reward|coin|voucher|kupon',
 'vehicle_product':r'mesin|eksterior|aerodinamis|handling|kabin|suspensi|nyaman berkendara|mobil nyaman|harga murah|kualitas|kwalitas'
}
public=[]
for r in records:
 text=str(r.get('title') or '')+' '+str(r.get('content') or '');low=text.lower()
 aspects=[k for k,v in rules.items() if re.search(v,low)]
 date=str(r.get('at') or '');before=date[:10]<'2025-12-06' if date else None
 public.append({'record_key':r['record_key'],'app':r['app'],'platform':r['platform'],'locale':r.get('locale'),'review_id':r['reviewId'],'reviewer_pseudonym':hashlib.sha256((salt+r['platform']+str(r.get('userName'))).encode()).hexdigest()[:16] if r.get('userName') else '', 'review_date':date,'rating':r.get('score'),'review_version':r.get('reviewCreatedVersion'),'developer_reply_present':bool(r.get('replyContent')),'pre_digiroom_relaunch':before if r['app']=='digiroom' else None,'word_count':len(text.split()),'mention_flags':'|'.join(aspects),'selection':r['selection'],'reviewer_residence_verified':False,'source_url':r.get('source_url'),'coding_method':'deterministic_mention_flags_v1_not_sentiment'})
for i,r in enumerate(public,1):r['evidence_id']=f'REV-{i:04d}'
fields=['evidence_id']+[k for k in public[0] if k!='evidence_id']
with (OUT/'reviews_derived.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(public)
(OUT/'mention_rules.json').write_text(json.dumps(rules,indent=2))
summary=[]
for (app,platform,locale), group in __import__('itertools').groupby(sorted(public,key=lambda x:(x['app'],x['platform'],x['locale'])),key=lambda x:(x['app'],x['platform'],x['locale'])):
 rows=list(group);d={'app':app,'platform':platform,'locale':locale,'n_unique_reviews':len(rows),'min_date':min(r['review_date'] for r in rows),'max_date':max(r['review_date'] for r in rows),'ratings':dict(collections.Counter(r['rating'] for r in rows)),'mention_counts':{k:sum(k in r['mention_flags'].split('|') for r in rows) for k in rules},'developer_reply_n':sum(r['developer_reply_present'] for r in rows),'version_available_n':sum(bool(r['review_version']) for r in rows)};summary.append(d)
(OUT/'review_summary.json').write_text(json.dumps({'total_unique_reviews':len(public),'cohorts':summary,'limitations':['nonrepresentative platform-selected public listing samples','all flags are lexical mentions, not validated complaints','ratings are not task completion','locale/storefront is not verified reviewer residence','Google Play rating histogram may not reconcile to current aggregate','historical reviews do not prove current defects','no API pagination or RSS collection']},ensure_ascii=False,indent=2))
print('unique records',len(public),'cohorts',len(summary))
for x in summary:print(x['app'],x['platform'],x['n_unique_reviews'],x['ratings'],x['min_date'],x['max_date'])
