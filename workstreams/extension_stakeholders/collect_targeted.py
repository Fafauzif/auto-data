from pathlib import Path
import sys,json,re,concurrent.futures,urllib.robotparser
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'shared'))
from public_http import fetch
from bs4 import BeautifulSoup
OUT=Path(__file__).resolve().parent
PRIVATE=ROOT/'private_cache'/'extension_stakeholders';PRIVATE.mkdir(exist_ok=True)
items=[
('ES01','Toyota G-Fleet','https://www.toyota.astra.co.id/g-fleet'),
('ES02','Toyota OtoXpert and T-OPT pre-Eid 2026','https://pressroom.toyota.astra.co.id/persiapan-mudik-lebaran-dengan-biaya-lebih-terjangkau-berkualitas-dan-bergaransi-manfaatkan-layanan'),
('ES03','T-OPT INAPA May 2026','https://pressroom.toyota.astra.co.id/t-opt-hadir-di-inapa-2026-spare-parts-alternatif-dengan-kualitas-terpercaya-dan-harga-lebih'),
('ES04','Honda maintenance packages current page','https://www.honda-indonesia.com/index.php/aftersales/packages'),
('ES05','Honda service legacy package page','https://www.honda-indonesia.com/honda-service'),
('ES06','BYD Indonesia warranty','https://www.byd.com/id/aftersales/warranty'),
('ES07','BYD European battery extension January 2026','https://media.byd.com/byd-extends-warranty-of-blade-battery-to-eight-years-or-250000km/?lang=eng'),
('ES08','Outlander PHEV 2020 owners manual','https://microsite.mitsubishi-motors.co.id/owner-manual/media/file/originals/post/2021/12/09/owners-manual-outlander-phev-20-model-year-compressed.pdf'),
('ES09','Hyundai Indonesia Promise used-car comparison','https://www.hyundai.com/id/en/build-a-car/hyundai-promise'),
('ES10','Toyota Special Service Campaign VIN route','https://ssc.toyota.astra.co.id/'),
('ES11','Toyota Special Service Campaign FAQ','https://ssc.toyota.astra.co.id/faq'),
('ES12','Toyota warranty scope and second owner GIIAS 2026','https://www.toyota.astra.co.id/corporate-information/news-promo/read/giias-2026-belajar-aturan-dasar-warranty-toyota-di-indonesia-apa-saja-jenis-kerusakan-yang-tidak-bisa-diklaim'),
('ES13','Toyota T-CARE XTRA GIIAS 2026','https://www.toyota.astra.co.id/corporate-information/news-promo/read/giias-2026-toyota-perkuat-layanan-purnajual-lewat-t-care-xtra-berikan-perlindungan-kendaraan-hingga-6-tahun'),
('ES14','Toyota Hilux Rangga G-Fleet rollout limitation','https://www.toyota.astra.co.id/product/all-new-hilux-rangga'),
('ES15','Mitsubishi L100 EV commercial product page','https://www.mitsubishi-motors.co.id/our-cars/l100-ev'),
('ES16','Mitsubishi L100 EV 2024 commercial offer','https://www.mitsubishi-motors.co.id/siaran-pers/mmksi-hadirkan-masa-depan-kendaraan-komersial-di-giicomvec-2024'),
('ES17','Toyota April 2026 safety recall notice','https://pressroom.toyota.astra.co.id/berikan-peace-mind-pelanggan-toyota-land-cruiser-300-dan-lexus-lx-tahun-produksi-tertentu'),
('ES18','Garda Oto claim approval process baseline','https://www.asuransiastra.com/featured/rahasia-klaim-cepat-garda-oto/'),
]
hosts={urlsplit(u).netloc:urlsplit(u).scheme+'://'+urlsplit(u).netloc+'/robots.txt' for _,_,u in items}
robots={}
for host,u in hosts.items():
 r=fetch(u,source='extension_stakeholders_robots',timeout=25)
 rp=urllib.robotparser.RobotFileParser();rp.parse(r.text.splitlines())
 robots[host]={'url':u,'status':r.status,'request_id':r.request_id,'parser':rp,'stop':r.status in (401,403,429,503) or r.status==0}
def one(item):
 ident,title,url=item;rb=robots[urlsplit(url).netloc]
 row={'source_id':ident,'title':title,'url':url,'retrieved_utc':'2026-11-11','robots_status':rb['status'],'robots_request_id':rb['request_id']}
 if rb['stop'] or (rb['status']==200 and not rb['parser'].can_fetch('Auto2000CaseResearch',url)):
  row.update(status='not_fetched_robots_boundary',direct_content_verified=False);return row
 r=fetch(url,source='extension_stakeholders',timeout=35)
 row.update(status=r.status,request_id=r.request_id,cache_hit=r.cache_hit,final_url=r.url,bytes=len(r.content),error=r.error)
 if r.status!=200 or r.error:
  row['direct_content_verified']=False;return row
 if r.content.startswith(b'%PDF'):
  pdf=PRIVATE/(ident+'.pdf');pdf.write_bytes(r.content)
  import subprocess
  subprocess.run(['pdftotext','-layout',str(pdf),str(PRIVATE/(ident+'.txt'))],check=False)
  text=(PRIVATE/(ident+'.txt')).read_text(errors='replace')
 else:
  soup=BeautifulSoup(r.content,'html.parser')
  for el in soup.select('script,style,nav,header,footer'):el.decompose()
  text=soup.get_text(' ',strip=True)
  (PRIVATE/(ident+'.txt')).write_text(text)
 row.update(direct_content_verified=len(text)>500,extracted_characters=len(text),private_text_path=str(PRIVATE/(ident+'.txt')))
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex: rows=list(ex.map(one,items))
(OUT/'source_register.json').write_text(json.dumps(rows,indent=2))
print(json.dumps([{k:r.get(k) for k in ('source_id','status','cache_hit','bytes','extracted_characters','direct_content_verified')} for r in rows],indent=2))
