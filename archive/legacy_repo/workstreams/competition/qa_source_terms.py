from pathlib import Path
import json,hashlib,csv,re
from html.parser import HTMLParser
out=Path(__file__).resolve().parent;root=out.parents[1]
checks={'T01':['Service History','Service Booking','Monitor Service Progress'],'T02':['60.000','XTRA','Juli 2022'],'T03':['sertifikat','Not Good','25 bulan'],'S01':['Instant Approval','Astra BYD'],'S02':['7 Oktober 2026','KTP pasangan','masa berlaku'],'O01':['7-day','60 minutes'],'O02':['indikatif','Penilaian Aktual','tidak berkewajiban'],'O03':['188','60 menit'],'U01':['OTP','Body & Paint'],'A01':['2 hari','15 menit','799.000.000'],'A02':['50.000','3 tahun'],'B01':['5 hari kerja','10 kendaraan','secara bersamaan'],'B02':['suku cadang asli','perawatan berkala'],'B03':['State of Health','70%','2024'],'H01':['160.000','9.030.000','September 2025'],'H02':['three (3) years','legally separate','Bluelink ready'],'H03':['10 kWh','40KM','5.000'],'W01':['Rp 200.000','Rp 10.000','booking service'],'W02':['30.000','1.000','2023'],'F01':['Tunggu Konfirmasi','dihubungi']}
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,t,a):
  if t in ('script','style'):self.skip+=1
 def handle_endtag(self,t):
  if t in ('script','style'):self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
sources={s['source_id']:s for s in json.loads((out/'sources.json').read_text())}; results=[]
for sid,terms in checks.items():
 s=sources[sid];key=hashlib.sha256(('GET\n'+s['url']+'\n').encode()).hexdigest();file=root/'private_cache/http'/f'{key}.bin'
 if not file.exists():results.append(dict(source_id=sid,check='cached_body',found=False,note='not available'));continue
 p=P();p.feed(file.read_bytes().decode('utf8',errors='replace'));text=' '.join(' '.join(p.parts).split()).lower()
 for term in terms:results.append(dict(source_id=sid,check=term,found=term.lower() in text,note='Exact substring in whitespace-normalized raw HTML text; not rendered-state verification'))
(out/'source_term_checks.json').write_text(json.dumps(results,indent=2));print('checks',len(results),'found',sum(r['found'] for r in results));print([r for r in results if not r['found']])
