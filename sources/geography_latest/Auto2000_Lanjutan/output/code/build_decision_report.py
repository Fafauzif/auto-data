from pathlib import Path
import json, math, csv, textwrap, html, re
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1]
OUT=R/'report/Auto2000_Keputusan_Cabang_dan_Layanan.pdf'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
W,H=595.276,841.89; M=43; CW=W-2*M
BG=HexColor('#fbfaf6');INK=HexColor('#16373d');TEAL=HexColor('#236a75');RED=HexColor('#c04f36');GRAY=HexColor('#5a686b')
styles={'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=15,textColor=INK,spaceAfter=10),'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,textColor=GRAY),'title':ParagraphStyle('title',fontName='Bold',fontSize=23,leading=28,textColor=INK),'cell':ParagraphStyle('cell',fontName='Body',fontSize=8,leading=11,textColor=INK),'head':ParagraphStyle('head',fontName='Bold',fontSize=8,leading=11,textColor=white)}
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Auto2000 | Keputusan Cabang dan Layanan Berbayar');c.setAuthor('Public-data geographic research')
PAGE=0;spec=[];qa=[]
def clean_text(txt):
 stash={}
 pattern=r'https?://[^\s<]+|[0-9a-f]{32,}|Auto2000|bZ4X|VF3|T570|SOC\d+|XE\d+|JB\d+|OX\d+|g\d+_\d+|built_bridge_\d+_\d+'
 def hide(m):
  k='ZZPROTECT'+chr(65+len(stash)//26)+chr(65+len(stash)%26)+'ZZ';stash[k]=m.group();return k
 txt=re.sub(pattern,hide,str(txt))
 txt=re.sub(r'(?<=[A-Za-zÀ-ÿ])(?=\d)|(?<=\d)(?=[A-Za-zÀ-ÿ])',' ',txt)
 for k,v in stash.items():txt=txt.replace(k,v)
 for a,b in {'sourcefile':'source file','footprintbangunan':'footprint bangunan','jobslot':'job slot','kanalsendiri':'kanal sendiri','jamkerja':'jam kerja','jaringanoli':'jaringan oli','originkota':'origin kota','endpointmodel':'endpoint model','originbaru':'origin baru','tabelkeputusan':'tabel keputusan','insightledger':'insight ledger','notgood':'Not Good','pelangganaktual':'pelanggan aktual','Sumberpublik':'Sumber publik','datalapangan':'data lapangan','diSurabaya':'di Surabaya','diMedan':'di Medan','diBandung':'di Bandung','diPalembang':'di Palembang','seluruhorigin':'seluruh origin','dariJabodetabek':'dari Jabodetabek','dariSurabaya':'dari Surabaya','rutedua':'rute dua','rumahpenulis':'rumah penulis','semuaorigin':'semua origin','barisX':'baris X','barisMaps':'baris Maps','datamentah':'data mentah','perjalananaktual':'perjalanan aktual','publikasiMon':'publikasi Mon','modelprofil':'model profil','contributionmargin':'contribution margin'}.items():txt=txt.replace(a,b)
 return txt

def para(txt,x,y,width,style='body'):
 txt=clean_text(txt);txt=re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#\d+;)', '&amp;', txt);p=Paragraph(txt,styles[style]);w,h=p.wrap(width,1000);p.drawOn(c,x,y-h);return y-h

def page(title,kicker,paras=[],fig=None,caption='',table=None,columns=None,note=None):
 global PAGE
 PAGE+=1;c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(TEAL);c.setFont('Bold',8);c.drawString(M,H-37,'AUTO2000  /  KEPUTUSAN CABANG DAN LAYANAN  /  14 NOV 2026')
 c.setFillColor(RED);c.setFont('Bold',8);c.drawString(M,H-62,kicker.upper())
 y=para(title,M,H-77,CW,'title')-18
 for p in paras:y=para(p,M,y,CW)-9
 if fig:
  p=R/fig
  if not p.exists():raise FileNotFoundError(p)
  img=ImageReader(str(p));iw,ih=img.getSize()
  reserve=0
  if caption:reserve+=Paragraph(clean_text(caption),styles['small']).wrap(CW,1000)[1]+12
  if note:reserve+=Paragraph(clean_text('<b>Keputusan.</b> '+note),styles['body']).wrap(CW,1000)[1]
  if table:
   cc=[[Paragraph(html.escape(clean_text(str(v))),styles['head' if i==0 else 'cell']) for v in row] for i,row in enumerate(table)]
   tt=Table(cc,colWidths=columns or [CW/len(table[0])]*len(table[0]))
   tt.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   reserve+=tt.wrap(CW,1000)[1]+14
  height=min(CW*ih/iw,y-83-reserve,520);width=height*iw/ih
  if height<85:raise RuntimeError(f'Figure too small page{PAGE}: {height}')
  c.drawImage(img,M+(CW-width)/2,y-height,width,height,mask='auto');y-=height+8
  if caption:y=para(caption,M,y,CW,'small')-12
 if table:
  cells=[[Paragraph(html.escape(clean_text(str(v))),styles['head' if i==0 else 'cell']) for v in row] for i,row in enumerate(table)]
  tw=columns or [CW/len(table[0])]*len(table[0]);t=Table(cells,colWidths=tw,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.5,TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#edf1ed'),BG])]))
  aw,hh=t.wrap(CW,1000);t.drawOn(c,M,y-hh);y-=hh+14
 if note:
  y=para('<b>Keputusan.</b> '+note,M,y,CW,'body')
 if y<66:raise RuntimeError(f'Page{PAGE} overflow {y} {title}')
 c.setStrokeColor(HexColor('#d4ddda'));c.line(M,49,W-M,49);c.setFillColor(GRAY);c.setFont('Body',7);c.drawString(M,34,'Sumber publik | Akses model, bukan pelanggan | Akun pelanggan dibedakan dari observasi');c.drawRightString(W-M,34,str(PAGE));c.showPage()
 spec.append({'page':PAGE,'title':title,'kicker':kicker,'paragraphs':paras,'figure':fig,'caption':caption,'table':table,'note':note});qa.append({'page':PAGE,'bottom_y':round(y,1),'layout_bounds_pass':y>=66})

def j(p):return json.loads((R/p).read_text())
def table_csv(p,cols,limit=10):
 d=pd.read_csv(R/p).fillna('');return [cols]+d[cols].head(limit).values.tolist()

I=R.parent/'extracted';WORK=R.parent/'work';BASE=I/'baseline/Auto2000_Geographic_Study'
branches=pd.read_csv(WORK/'branch_analysis/branch_decision_table_29.csv').astype(object).fillna('')
markets=pd.read_csv(WORK/'branch_analysis/corrected/market_recomputed.csv')
se=pd.read_csv(WORK/'customer_journey/social_evidence_ledger.csv').astype(object).fillna('')
def f(x,d=2):return f'{float(x):.{d}f}'.replace('.',',')
def branch(part):return branches[branches.branch_name.str.contains(part,case=False,regex=False)].iloc[0]
def image(name):return 'figures/'+name

page('Menangkan pekerjaan berbayar dengan tujuan bengkel yang tepat dan janji yang selesai','Keputusan utama',[
 '<b>Prioritaskan routing pekerjaan ke kanal Auto2000 yang sudah ada, koreksi destinasi Suci, dan lindungi satu kunjungan yang tuntas. Jangan mulai dari ekspansi atau subsidi pickup merata.</b>',
 'Di Palembang, memasukkan OtoXpert beroperator Auto2000 menghapus seluruh sembilan origin dengan selisih akses oli di atas lima menit. Di Bandung, koreksi Suci mengubah cabang terdekat pada 20 origin. Di Medan, selisih ke jaringan oli hanya 0,35 menit. Tiga hasil ini menuntut intervensi yang berbeda.',
 'Sasaran pekerjaan awal: oli dan filter Toyota Avanza 2019 G 1.3 yang dibayar pelanggan di luar entitlement gratis atau prepaid. Kampas rem depan memakai jalur bengkel dengan parts dan persetujuan pekerjaan tersendiri. Dukungan xEV tetap dijalankan sebagai jalur kasus, demo, dan appraisal.'
],table=[['Tindakan sekarang','Tempat utama'],['Oli Tepat Kanal','OtoXpert Palembang; Rungkut; Ring Road Medan'],['Tujuan Benar Suci','Suci dan catchment Cibiru yang berubah'],['Slot Sampai Serah-Terima','A. Yani, Pancing; bridge Cilandak'],['Sekali Datang','Kantong Soekarno-Hatta yang tersisa']],note='Seluruh angka geografis merujuk origin model. Rekomendasi adalah pilihan tindakan dalam ruang bukti publik, bukan klaim uplift atau laba yang telah terjadi.')

page('Enam insight mengubah pilihan cabang dan intervensi','Ringkasan eksekutif',[
 'Persoalan yang dapat dijawab studi ini bukan seberapa ramai peta bengkel, melainkan kapan Auto2000 harus mengubah penawaran, tujuan kanal, jumlah perjalanan, atau handoff agar pekerjaan berbayar lebih layak dipilih.',
 'Seluruh 27 cabang awal dihitung ulang dari OD mentah. Suci dan Sidoarjo kemudian ditambahkan sebagai skenario koreksi sehingga tabel keputusan mencakup 29 endpoint. Operator, lingkup pekerjaan, alternatif setempat, dan cabang Auto2000 kedua dipisahkan.'
],table=[['Insight','Keputusan yang berubah'],['1. Palembang: sembilan tail oli menjadi nol melalui kanal milik sendiri','Routing OtoXpert dahulu; pickup atau gedung baru bukan pilihan pertama'],['2. Medan: 4,09 menjadi 0,35 menit saat pembanding relevan','Perbaiki penawaran dan konfirmasi Pancing; gunakan Ring Road untuk opsi ekonomis'],['3. A. Yani dan Kertajaya sama-sama 11 origin, tetapi mandatnya berlawanan','Lindungi slot A. Yani; tawarkan Rungkut dari Kertajaya'],['4. Suci mengambil 20 origin dan menurunkan gap Bandung','Koreksi routing sebelum menganggap Cibiru prioritas akses'],['5. Keunggulan lokasi dapat habis oleh kunjungan tambahan','Booking harus berakhir pada persetujuan kerja dan kepastian serah-terima'],['6. xEV harus menuju pemilik kasus, bukan charger terdekat','Demo terkonfirmasi, HHC ke garansi, appraisal ke penawaran nyata']],columns=[CW*.52,CW*.48])

page('Palembang: sembilan origin tertinggal oli dapat dilayani lebih dekat lewat kanal sendiri','Insight 1 / operator mengubah keputusan',[
 'Dengan hanya bengkel umum Auto2000, sembilan dari 69 origin berpasangan memiliki gap oli di atas lima menit. Tujuh berada unik pada catchment Tanjung Api-Api dan satu dibagi dengan Veteran karena waktu terdekatnya persis sama. Plaju tidak memiliki origin pada kategori itu.',
 'Setelah OtoXpert Palembang berlabel operator Auto2000 diperbolehkan, jumlah tersebut menjadi nol. Tujuh origin mencapai paritas dengan jaringan oli pembanding; dua lainnya tinggal sekitar 1,005 menit. Perubahan ini adalah hasil pemilihan endpoint model, bukan dampak komersial yang sudah diukur.'
],fig=image('07_palembang_ox_menutup_gap.png'),caption='Origin yang sama, aturan snap <=250 m. Jaringan pembanding oli: OtoXpert+Shop&Drive; jaringan sendiri: Auto2000+OtoXpert berlabel Auto2000. Sumber: OD mentah dan tabel operator [G1-G3].',note='Jalankan Oli Tepat Kanal Palembang untuk pekerjaan yang sesuai sebelum pickup baru atau perluasan bengkel. Manfaatnya datang dari memakai endpoint yang sudah tersedia.')
page('Untuk oli di utara, kalahnya pickup bukan karena perjalanan tidak penting','Insight 1 / pilihan dan alternatif yang kalah',[
 'Perjalanan tetap penting: titik ketertinggalan terkonsentrasi di utara, tetapi kanal ekonomis yang sudah ada dapat menjawabnya. Membaca Palembang sebagai kota sungai lalu mendahulukan Plaju akan memilih tempat yang salah untuk tujuan mengurangi tail oli.',
 'Tanjung Api-Api tetap dibutuhkan untuk pekerjaan dengan scope bengkel utama. Rekomendasi ini tidak memindahkan seluruh pekerjaan atau menyamakan GP dua kanal. Digiroom harus menampilkan pilihan pekerjaan, operator penerima, lingkup parts, harga yang disetujui, serta cabang yang menerima slot.'
],fig=image('03_palembang_kantong_utara.png'),caption='TAA memiliki7origin unik+1shared pada tail>5menit;Veteran1unik;Plaju0. Ambang5menit adalah kategori analitis, bukan toleransi pelanggan. Peta bukan bukti bahwa jembatan menyebabkan gap. [G1-G3]',table=[['Dipilih','Tidak diprioritaskan','Alasan'],['Oli ke OtoXpert Palembang','Pickup oli merata','Tail model terselesaikan melalui endpoint tersedia'],['Bengkel utama untuk scope yang sesuai','Alih semua pekerjaan ke kanal ekonomis','Fitment, scope dan GP berbeda'],['Kantong utara untuk routing','Plaju sebagai proyek akses pertama','Tidak ada tail>5menit pada catchment Plaju']],columns=[CW*.30,CW*.30,CW*.40])

page('Medan: selisih 4,09 menit menyusut menjadi 0,35; perluasan bukan jawaban awal','Insight 2 / tugas mengubah pembanding',[
 'Pada 78 origin berpasangan yang sama, median gap Auto2000 berubah dari 4,086 menit terhadap kandidat generik menjadi 0,347 menit terhadap jaringan oli terdokumentasi. Sebanyak32 origin bahkan tidak lebih lambat menuju Auto2000. Ini membatalkan alasan perluasan yang hanya bertumpu pada kepadatan kandidat peta.',
 'Pancing terdekat bagi24 origin, dengan gap median0,347 menit dan tanpa tail>5menit. Delapan origin kehilangan akses Auto2000<=15menit jika Pancing dikeluarkan dari model. Prioritasnya adalah menjaga slot dan penyelesaian, bukan mengalihkan beban secara otomatis ke cabang lain.'
],fig=image('01_pembanding_dan_koreksi.png'),caption='Pembanding diganti pada origin berpasangan yang sama; panel Bandung juga menunjukkan koreksi Suci. Penyusutan adalah perbandingan skenario, bukan hasil intervensi. [G1-G3]',note='Pilih Slot Sampai Serah-Terima Pancing. Untuk opsi ekonomis di catchment Gatot Subroto, tampilkan OtoXpert Ring Road Medan sebelum membuat tier atau rute pickup baru.')
page('Medan memerlukan dua tawaran, bukan satu subsidi perjalanan','Insight 2 / cabang dan pekerjaan',[
 'Gatot Subroto terdekat bagi20 origin dan memiliki gap median2,386 menit, tetapi tidak ada tail>5menit. Memperbolehkan OtoXpert Ring Road beroperator Auto2000 membuat median gap jaringan sendiri pada catchment ini mencapai nol. Satu angka kota tidak boleh menggantikan pilihan kanal per pekerjaan.',
 'Untuk oli dan filter yang dibayar sendiri, tawarkan bengkel utama atau kanal ekonomis dengan scope parts yang terlihat. Untuk kampas rem depan, tetapkan kit satu as depan, fitting, inspeksi, pajak dan perubahan scope; jangan memakai harga oli sebagai pembanding pekerjaan rem.'
],table=[['Cabang/catchment','Intervensi bernama','Alternatif yang kalah'],['Pancing','Slot Sampai Serah-Terima: parts, PIC dan slot diterima sebelum berangkat','Ekspansi untuk menyelesaikan gap kota0,35menit'],['Gatot Subroto/Ring Road','Oli Tepat Kanal Ring Road: dua opsi pekerjaan yang operaturnya jelas','Tier ekonomis baru atau pickup massal'],['Pancing untuk rem','Parts Disetujui: fitment VIN/model, kit dan jasa disetujui sebelum slot','Bundel diskon umum tanpa parts siap']],columns=[CW*.25,CW*.43,CW*.32],note='Ketegasan pilihannya berasal dari akses dan kanal yang sudah ada. Harga, kapasitas dan switching tidak direka menjadi hasil.')

page('A. Yani dan Kertajaya sama-sama 11 origin; kesamaan ukuran menyembunyikan mandat berlawanan','Insight 3 / Surabaya',[
 'Pada grid baseline, di A. Yani median gap ke jaringan oli adalah -0,960 menit; di Kertajaya +2,133 menit. Keduanya terdekat bagi11 origin. Ranking jumlah origin saja akan memperlakukan dua posisi kompetitif ini sebagai kebutuhan yang sama.',
 'Cabang Auto2000 kedua menambah median3,757 menit pada origin A. Yani, tetapi hanya0,122 menit pada origin Kertajaya. Karena itu, lindungi slot A. Yani; jangan menganggap overlap di Kertajaya berarti kapasitas kosong atau dasar menutup cabang.'
],fig=image('02_surabaya_dua_mandat.png'),caption='Catchment baseline ketat, identitas cabang dan OD koreksi dipertahankan. Penalti cabang kedua adalah perbandingan lokasi, bukan beban kerja atau kapasitas. [G1-G3]',note='A. Yani mendapat Slot Pasti Harga Disetujui. Kertajaya mendapat pilihan Oli Rungkut, bukan subsidi perjalanan seragam.')
page('Di Kertajaya, Rungkut menghapus tiga tail oli tanpa kanal baru','Insight 3 / tindakan per pekerjaan',[
 'Kertajaya memiliki tiga origin dengan gap oli>5menit. Memasukkan OtoXpert Rungkut beroperator Auto2000 menghapus ketiganya dari kategori tersebut; median gap catchment tersisa sekitar1,080 menit. Penawaran harus mengubah tujuan pekerjaan yang sesuai sebelum pemilik berangkat.',
 'A. Yani tetap menjadi pilihan utama bagi pekerjaan yang lokasinya sudah kompetitif. Keunggulan kecil itu harus dilindungi dengan persetujuan scope dan janji siap ambil. Menambah tombol booking tidak menjamin pekerjaan diterima dan selesai.'
],table=[['Pemilik dan pekerjaan','Tindakan','Pilihan yang kalah'],['Avanza2019G1.3; oli+filter dibayar sendiri di catchment Kertajaya','Tampilkan Kertajaya/Rungkut, parts dan operator; pilih slot diterima','Tier baru dan pickup luas sebelum kanal sendiri dipakai'],['Pemilik sejenis di A. Yani','Lindungi penerimaan dan persetujuan harga sebelum berangkat','Memindahkan ke cabang kedua atas dasar overlap'],['Kampas rem depan','Workshop bay dengan kit+fitment+persetujuan; cakupan opsi jaringan dilabeli','Menjanjikan penggantian kampas rem di rumah hanya dari cakupan THS umum']],columns=[CW*.31,CW*.39,CW*.30],note='THS diprioritaskan untuk oli/filter pada lokasi yang dapat dilayani; inspeksi rem tidak disamakan dengan penggantian kampas rem depan. [JB01-JB04]')

page('Suci yang dikoreksi mengambil 20 origin; prioritas akses Cibiru harus turun','Insight 4 / koreksi mengubah keputusan',[
 'Suci sebelumnya dikeluarkan karena tautan arah resmi mengulang titik Setiabudi. Sumber peta publik alternatif cocok dengan alamat resmi PHH Mustofa6 dan titik Overture dalam sekitar9meter. Sidoarjo juga dipulihkan dari koordinat resmi rusak yang didukung titik nama/alamat sama dalam sekitar23meter.',
 'Rute baru membuat Suci terdekat bagi20 dari78 origin Bandung. Median gap kota turun2,636→1,736 menit; tail>5menit turun21→17. Cibiru turun22→14 origin dan tail4→1. Menganggap Cibiru target pickup utama dari peta lama berarti mendanai sebagian masalah pencatatan lokasi.'
],fig=image('04_suci_mengubah_prioritas.png'),caption='Versi lama, sumber koreksi, road-snap dan OD baru disimpan. Suci merupakan kandidat koordinat fasilitas publik yang dirutekan, bukan gate yang diklaim telah dikunjungi. [K1-K2; G4]',note='Jalankan Tujuan Benar Suci: perbaiki koordinat dan pilihan cabang sebelum menjual intervensi akses baru di timur Bandung.')
page('Soekarno-Hatta menyisakan delapan tail bahkan setelah kanal sendiri ditambahkan','Insight 4 / prioritas yang tetap bertahan',[
 'Soekarno-Hatta tetap terdekat bagi21 origin. Gap median ke jaringan oli4,248 menit dan sembilan dari17 tail Bandung berada di catchment ini. Sesudah OtoXpert beroperator Auto2000 ikut dihitung, delapan tail masih tersisa; median gap jaringan sendiri3,435 menit.',
 'Berbeda dari Palembang, routing kanal sendiri belum menyelesaikan seluruh kantong ini. Pilih Sekali Datang Soekarno-Hatta: oli/filter melalui THS pada lokasi yang sesuai atau slot tunggu onsite dengan parts siap; pekerjaan rem tetap di bay. Pickup berbayar menjadi opsi residual yang harus mengalahkan selisih kontribusi per pekerjaan.'
],table=[['Pilihan','Urutan keputusan','Mengapa alternatif kalah'],['Koreksi Suci','Dikerjakan lebih dahulu pada sistem pemilihan cabang','Biaya gedung/pickup tidak membetulkan destinasi yang salah'],['Sekali Datang Soekarno-Hatta','THS oli sesuai scope; atau tunggu satu kunjungan dengan parts siap','Reroute semua ke Suci/OtoXpert masih meninggalkan8tail'],['Pickup residual','Dibeli per pekerjaan jika batas kontribusi mengizinkan','Subsidi seluruh kota membayar juga pekerjaan yang tidak membutuhkan']],columns=[CW*.28,CW*.38,CW*.34],note='Sidoarjo tidak menang pada grid Surabaya lama yang batasnya lebih utara. Itu bukan kesimpulan tentang seluruh pasar selatan; sensitivitas origin perluasan ditampilkan terpisah. [G4; A1]')

page('OtoXpert hampir tidak menambah cakupan20menit, tetapi manfaat perjalanan Palembang nyata','Bukti pendukung Insight 1 / manfaat marginal',[
 'Tambahan origin dalam cakupan<=20menit hanya0diSurabaya,0Medan,0Bandung dan2Palembang. Namun ukuran cakupan tersebut menyembunyikan penghematan pada origin yang sudah tercakup.',
 'Pada baseline yang sama, penghematan>3menit terjadi pada5,10,3dan10origin; penghematan>5menit pada0,0,2dan7origin. Median penghematan seluruh origin tetap nol di tiap kota. Jadi kanal ini terutama menambah pilihan penawaran, dengan manfaat akses lokal yang kuat di Palembang.'
],fig=image('05_otoxpert_marginal.png'),caption='Ambang10/15/20/30menit dan penghematan>1/>3/>5menit dihitung pada origin berpasangan yang sama. Nilai positif bukan ukuran preferensi atau uplift. Tabel koreksi juga disediakan. [G1-G3]',note='Gunakan kanal ekonomis yang sudah tersedia menurut operator dan pekerjaan. Jangan menyamakan kecilnya perluasan cakupan dengan nolnya manfaat perjalanan.')
page('Logo Toyota dan hubungan Astra bukan perimeter laba Auto2000','Bukti pendukung Insight 1 / operator dan kontribusi',[
 'OtoXpert Dukuh Kupang berlabel Liek Motor, Thamrin Medan Deltamas, Tritura Medan Perintis, dan Antapani Wijaya. Kanal tersebut merupakan alternatif relevan, tetapi bukan otomatis transaksi Auto2000. Shop&Drive juga tidak dimasukkan sebagai GP Auto2000 hanya karena hubungan grup Astra.',
 'Perimeter akses sendiri memakai OtoXpert Rungkut, Ring Road Medan, Peta, Bojongsoang dan Palembang yang berlabel Auto2000. Pilihan kanal harus menampilkan operator penerima dan kontribusi aktual pada akhir pekerjaan, bukan hanya lead yang dipindahkan antar-aplikasi.'
],fig=image('06_operator_alternatif_lokal.png'),caption='Komposisi alternatif lokal dihitung dari endpoint terdekat menurut kanal/operator. Label operator berasal dari direktori, bukan kontrak pembagian GP. [G2; JB01-JB04]',note='Untuk transaksi yang sama, pickup ke bengkel utama hanya mengalahkan kanal sendiri jika kontribusi bersihnya lebih tinggi setelah biaya perjalanan dan subsidi pada pekerjaan baseline dihitung.')
page('Cilandak: satu kunjungan gagal dapat menghapus keunggulan lokasi yang sudah ada','Insight 5 / booking sampai pekerjaan selesai',[
 'Bridge Cilandak-Radio Dalam-Simprug dipilih karena memuat akun positif dan negatif pada pasar yang sama. Satu akun Cilandak tetap memakai dealer setelah servis gratis habis, lalu menyatakan memilih bengkel lain setelah janji selesai penggantian shockbreaker meleset. Akun lain pada cabang sama melaporkan booking, konsultasi sebelum kerja dan follow-up yang baik.',
 'Pada satu origin pada jejak bangunan di bridge, rute ke Cilandak4,857menit dan balik3,088menit: total7,945. Ke jaringan oli terdekat8,875menit. Keunggulan Auto2000 hanya0,930menit. Dalam skenario satu kunjungan tambahan Auto2000, totalnya15,890menit, sehingga menjadi7,015menit lebih lama daripada satu kunjungan alternatif.'
],fig=image('08_satu_kunjungan_tambahan.png'),caption='Rute pergi dan balik diperoleh terpisah. Dua kunjungan merupakan skenario, bukan perjalanan aktual penulis ulasan. Origin bangunan bukan rumah penulis. Akun Cilandak: SOC12-SOC14; rute: built_bridge_2_1. [S1; A1]',note='Pilih Janji Servis Siap Dikerjakan: job, estimasi diterima, parts pendukung, slot mulai, rentang selesai dan PIC harus diterima cabang sebelum instruksi berangkat.')
page('Rating positif pun dapat memuat dua kunjungan; jangan ukur keberhasilan pada booking','Insight 5 / mekanisme positif dan negatif',[
 'Akun Nawilis Radio Dalam berbintang empat menyatakan puas setelah kembali pada hari berikutnya karena kunjungan pertama tidak tertangani. Akun positif lain tetap datang meski rumah jauh. Keduanya menolak jalan pintas bahwa rating tinggi berarti perjalanan sedikit atau jarak selalu menentukan pilihan.',
 'Akun Otoklix Ciputat menggambarkan booking, penjelasan estimasi dan persetujuan perubahan parts/harga yang baik. Akun B-Quik Citra8 justru mengeluhkan perubahan invoice setelah harga awal dan waktu kerja melampaui estimasi. Perbaikan yang dipilih adalah kepastian scope serta serah-terima, bukan klaim bahwa bengkel independen selalu murah atau seluruh booking Auto2000 gagal.'
],fig=None,caption='Peta memuat subset Cilandak/Radio Dalam/Simprug. Akun Jabodetabek lain, termasuk Citra8 dan Ciputat, menjadi pembanding mekanisme dan tidak semuanya masuk window. B-Quik Lebak Bulus dengan flag tutup dikeluarkan. [S1; A1]',table=[['State yang harus terlihat','Syarat untuk melanjutkan'],['Diminta → diterima cabang','Job dan penanggung jawab cocok'],['Estimasi → disetujui','Scope, parts, pajak dan perubahan terpisah'],['Slot → siap dikerjakan','Parts pendukung dan waktu mulai/selesai diterima'],['Selesai → diserahterimakan','Pekerjaan dan biaya aktual tercatat'],['Keluhan → ditutup','PIC dan hasil penyelesaian tercatat']],columns=[CW*.40,CW*.60])

page('Bridge Jabodetabek menyatukan akses dan akun dengan hasil berlawanan','Insight 5 / pasar yang sama',[
 'Cilandak, Radio Dalam dan Simprug menyediakan pembanding proses di pasar yang sama. Titik aktivitas dipilih pada jejak bangunan, bukan dari alamat rumah penulis. Peta memuat subset bridge; akun Citra8 dan Ciputat pada pembahasan sebelumnya dipakai sebagai pembanding mekanisme Jabodetabek, tidak semuanya berada dalam window.'
],fig=image('09_bridge_jakarta_selatan.png'),caption='Dua belas origin bangunan pada bridge. Endpoint kasus dan jaringan oli dibedakan; lokasi ulasan adalah outlet, bukan rumah penulis. Flag B-Quik Lebak Bulus tutup tidak dijadikan alternatif aktif. [S1; A1]',note='Gunakan bridge ini untuk memilih proses yang berhasil: estimasi disetujui, penerimaan cabang, parts dan slot, serta kepastian serah-terima. Tidak ada persentase keluhan yang dipindahkan ke empat kota.')

page('Minggu: arahkan oli ke Fatmawati, bukan ke showroom Cilandak yang buka','Insight 5 / jam fasilitas mengikuti pekerjaan',[
 'Cilandak memublikasikan showroom Minggu09.00–17.00, tetapi bengkel libur. Direktori OtoXpert Fatmawati beroperator Auto2000 memublikasikan Senin–Minggu08.00–18.00. Pada origin bridge yang ditelusuri, selisih perjalanan pulang-perginya hanya0,93menit.',
 'Untuk oli/filter yang sesuai, tampilkan Fatmawati sebagai pilihan beroperator Auto2000 pada hari Minggu, lalu terima slot dan scope lebih dahulu. Tabel minimum perjalanan pergi dapat memilih Pos Pengumben yang beroperator Astrido; pilihan itu tetap terlihat sebagai alternatif, bukan GP Auto2000. Provider dengan jam tidak diketahui tidak dianggap tutup.'
],table=[['Tugas dan waktu','Keputusan routing','Hal yang tidak dijanjikan'],['Oli/filter hari kerja','Bandingkan Cilandak dan kanal ekonomis; quote+slot diterima','Tidak mengklaim satu cabang selalu lebih cepat'],['Oli/filter hari Minggu','Fatmawati pada jam bengkel terdokumentasi, lalu konfirmasi penerimaan','Jam publik bukan slot atau stok yang sudah tersedia'],['Kampas rem depan','Bay dengan kit, fitment dan persetujuan; jadwal sesuai bengkel','Tidak otomatis THS atau slot showroom'],['Kasus xEV','Penerima masalah dan jalur layanan yang tepat','Jam showroom tidak membuktikan kompetensi diagnosis']],columns=[CW*.26,CW*.42,CW*.32],note='Janji Servis Siap Dikerjakan mengikat jam fasilitas, pekerjaan, scope dan PIC. Ini perubahan handoff pada entry yang sudah ada, bukan tombol booking baru. [XE10; G2; A1]')

page('xEV: arahkan masalah ke pemilik kasus, bukan kendaraan ke charger terdekat','Insight 6 / tiga prong tetap terhubung',[
 'Toyota telah memublikasikan HHC, sertifikat dan jalur dealer untuk memvalidasi hasil Not Good serta memberi informasi cakupan garansi. Pancing juga sudah memiliki tautan permintaan test drive Zenix yang membawa model dan branchCodeT570. Menambah direktori charger atau tombol booking generik mengulang titik masuk, tetapi tidak menjamin tujuan pekerjaan dan penerima kasus.',
 'Akun pemilik VF3 di Nawilis Radio Dalam menggambarkan hotline OEM yang menyiapkan reservasi serta penanganan portable charger. Kasus yang selesai ini mendukung nilai rujukan berbasis masalah. Ia tidak membuktikan bahwa bengkel ban dapat memperbaiki baterai traksi Toyota.'
],table=[['Prong / intervensi','Endpoint bernama dan tindakan','Pilihan yang kalah'],['Pertama / Demo Siap Berangkat','Pancing ZenixT570 atau konsultasi Kertajaya; adviser konfirmasi varian, unit, lokasi, slot dan quote','3D/showroom baru sebelum unit dan quote jelas'],['Pemilik / Satu Kasus xEV','Pancing atau Soekarno-Hatta untuk jalur HHC terdokumentasi; sertifikat lalu validasi garansi dengan PIC sama','Charger terdekat sebagai proxy diagnosis'],['Berikutnya / Upgrade Sekali Janji','Adviser Sudirman/OLXmobbi: inspeksi, inspected offer, ekuitas bersih dan quote xEV','Resale-floor atau top-up tanpa kewajiban didanai']],columns=[CW*.25,CW*.45,CW*.30],note='HHC yang tercakup tidak dihitung sebagai pekerjaan berbayar tambahan. Payer, entitlement, garansi/reimbursement, recall dan customer-paid dicatat terpisah. [XE01-XE14; SOC07]')

page('Pilih tujuh endpoint dengan mandat berbeda, bukan tujuh pemenang skor','Shortlist tindakan',[
 'Urutan berikut mengutamakan perbaikan routing dan janji pada jaringan yang sudah ada. Ini bukan ranking permintaan atau kapasitas. Pemilihan kanal terjadi sebelum pelanggan berangkat dan tetap memakai otorisasi lingkup pekerjaan.'
],table=[['Endpoint/catchment','Intervensi bernama','Tujuan dan pekerjaan'],['Tanjung Api-Api → OtoXpert Palembang','Oli Tepat Kanal Palembang','Oli/filter berbayar; hapus tail melalui endpoint sendiri'],['Kertajaya → OtoXpert Rungkut','Pilihan Oli Rungkut','Oli/filter dengan scope terlihat; hindari pickup umum'],['Gatot Subroto → OtoXpert Ring Road','Oli Tepat Kanal Ring Road','Opsi ekonomis operator sendiri sebelum tier baru'],['A. Yani','Slot Pasti Harga Disetujui','Lindungi job yang aksesnya kompetitif dan cabang kedua lebih jauh'],['Pancing','Slot Sampai Serah-Terima','Konfirmasi diterima, parts dan penyelesaian; pertahankan akses15menit'],['Suci','Tujuan Benar Suci','Koreksi lokasi dan pemilihan cabang'],['Soekarno-Hatta','Sekali Datang Soekarno-Hatta','THS oli sesuai scope atau tunggu onsite; rem di bay']],columns=[CW*.31,CW*.30,CW*.39],note='Cilandak menjadi bridge proses dengan bukti pelanggan pasar yang sama, bukan lokasi yang dipilih karena paling banyak keluhan. Seluruh29 endpoint memiliki tabel keputusan tersendiri.')

page('Alternatif berikut kalah untuk tujuan yang sedang diputuskan','Tidak diprioritaskan',[
 'Deprioritas di bawah berlaku pada intervensi dan tujuan analisis. Ia bukan tuduhan bahwa cabang tidak berpotensi secara komersial atau boleh ditutup.'
],table=[['Pilihan yang tidak didahulukan','Pengganti yang dipilih','Alasan berbukti'],['Pickup oli massal Tanjung Api-Api','Routing OtoXpert Palembang','9tailkota→0ketika kanal sendiri masuk'],['Plaju sebagai proyek akses pertama karena narasi sungai','Kantong utara/kanal sendiri','0tail>5menit di Plaju; sebab jembatan tidak ditetapkan dari ilustrasi'],['Pickup/ekspansi Cibiru sebelum koreksi','Tujuan Benar Suci','20origin beralih; tail Cibiru4→1'],['Tier bengkel ekonomis baru','OtoXpert beroperator Auto2000 +parts sesuai scope','Kanal tersedia; manfaat operator dan kontribusi perlu dibedakan'],['Subsidi perjalanan Medan secara merata','Pancing dan Ring Road sesuai job','Gap jaringan oli0,35menit; opsi sendiri tersedia'],['Ranking cabang dari besar catchment saja','Mandat akses, cabang kedua dan pekerjaan','A.Yani/Kertajaya sama11origin tetapi posisi berbeda'],['Booking/charger directory sebagai inti inovasi','Janji servis dan pemilik kasus xEV','Entrybooking/HHC sudah ada; kasus berhasil/gagal membedakan handoff'],['Resale-floor di awal','Inspected offer +netupgradecost','Tidak ada data pendanaan kewajiban jaminan']],columns=[CW*.34,CW*.30,CW*.36])

page('Origin alternatif mempertahankan pilihan kanal, bukan semua besaran menit','Uji ketahanan keputusan',[
 'Sensitivitas menambahkan origin grid bergeser setengah sel dan titik representatif bangunan publik pada kantong keputusan. Bangunan tidak dilabeli rumah atau pemilik Toyota. Origin baru merupakan uji terarah, bukan sampel populasi.',
 'Tanda keunggulan A. Yani tidak konstan: pada enam origin bergeser gap pergi median+0,246menit, sedangkan gap pulang-pergi-0,135menit. Maka mandatnya adalah menjaga penawaran dan penyelesaian di lokasi kompetitif, bukan beriklan selalu paling dekat. Soekarno-Hatta tetap tertinggal pada origin bergeser maupun bangunan; itu memperkuat prioritas satu kunjungan.',
 'Pada enam origin bangunan perluasan selatan, seluruh cabang terdekat menjadi Sidoarjo yang dikoreksi. Median gap pulang-perginya sekitar0,021menit. Nol winner pada grid lama merupakan efek batas studi; Sidoarjo tidak layak dinilai tidak penting dari batas itu.'
],fig=image('10_robustness_origin_keputusan.png'),caption='Origin yang berbeda dilaporkan dengan n dan arah perjalanan sendiri. Perbandingan bukan penambahan pelanggan atau pemindahan bobot populasi. Data mentah dua arah tersedia. [A1; G4]',note='Pertahankan pilihan yang tidak membutuhkan asumsi unggul universal: routing kanal tersedia, tujuan Suci yang benar, dan kepastian satu kunjungan.')

page('Sidoarjo: nol origin lama adalah efek batas, bukan alasan menyingkirkan cabang','Bukti pendukung / batas wilayah',[
 'Koordinat resmi Sidoarjo yang rusak dapat didekode dan dicocokkan dengan nama serta alamat Jenggolo60 pada Overture. Endpoint kemudian dirutekan dua arah. Pada grid lama yang berhenti di utara cabang, ia tidak menjadi pemenang; pada enam titik bangunan perluasan selatan, semuanya memilih Sidoarjo.',
 'Median selisih pulang-pergi terhadap jaringan oli pada enam titik ini hanya0,021menit. Ini mendukung mempertahankan Sidoarjo dalam pemilihan cabang selatan, bukan menghitungnya sebagai pasar baru atau menganggap seluruh penduduk selatan pemilik Toyota.'
],fig=image('11_sidoarjo_batas_jendela.png'),caption='Enam origin tambahan pada footprint sumber publik. Skenario ekstensi tidak dicampur ke denominator59origin Surabaya awal. [K2; A1]',note='Perbaiki koordinat dan cakupan pemilihan cabang; jangan memutuskan ekspansi atau deprioritas selatan dari batas grid lama.')

page('Bandingkan pickup, tunggu onsite dan THS melalui pekerjaan yang sama','Keputusan perjalanan',[
 'Tunggu onsite memerlukan satu rangkaian pergi+balik. Antar lalu ambil memerlukan dua rangkaian jika pemilik melakukan dua perjalanan dengan profil mobil yang sama. Pickup/return atau THS dapat mengurangi perjalanan yang dikemudikan pelanggan, tetapi tidak menghapus perjalanan petugas atau biaya operasi.',
 'Seluruh rute pergi dan balik diperoleh terpisah. Jumlah kunjungan, antrean dan waktu kerja adalah parameter skenario saat tidak diamati. Jangan menggandakan satu rute pergi lalu menyebutnya fakta pulang-pergi.'
],table=[['Opsi','Dipilih untuk','Beban yang harus dibandingkan'],['Tunggu onsite satu kunjungan','Job cepat dengan parts dan slot siap','Rute dua arah +waktu onsite'],['Antar lalu ambil','Scope lebih panjang yang disetujui','Dua rangkaian model; moda aktual bisa berbeda'],['Pickup/return','Kantong residual dengan kontribusi cukup','Perjalanan pelanggan berkurang; biaya driver/logistik tetap'],['THS','Oli/filter di alamat/lokasi layak','Petugas bergerak; tidak otomatis penggantian kampas rem atau diagnosis HV']],note='Soekarno-Hatta memakai Sekali Datang sebelum subsidi pickup luas. Palembang dan Rungkut memakai pilihan kanal sendiri sebelum membeli perjalanan tambahan. [A1; JB01-JB04]')

page('Pickup harus mengalahkan kontribusi kanal sendiri, bukan sekadar menambah booking','Ekonomi keputusan',[
 'Untuk pekerjaan tambahan yang sama, membawanya ke bengkel utama hanya lebih baik daripada kanal sendiri jika gA−cPickup>gOX. Selisih gA−gOX adalah batas biaya pickup per pekerjaan sebelum perbedaan take-up dan kapasitas ikut dihitung. Tidak ada nilai margin Auto2000 yang diisi secara rekaan.',
 'Untuk satu intervensi, gunakan Δkontribusi=B(g−c)−Ec−Dg0−F. B adalah pekerjaan yang benar-benar tambahan; g kontribusi pekerjaan tambahan; c biaya variabel intervensi; E pekerjaan baseline yang ikut memperoleh subsidi; D pekerjaan baseline yang tergeser; g0 kontribusi baseline; F biaya tetap.',
 'Titik impas B=(F+Ec+Dg0)/(g−c), hanya saat g>c. Jika g<=c, menambah volume tidak menutup biaya tetap. Persetujuan scope, penerimaan slot dan status siap ambil dipilih lebih dahulu karena secara langsung menangani mekanisme akun pelanggan tanpa mewajibkan subsidi perjalanan tiap job.'
],table=[['Perubahan','Aturan pencatatan'],['WhatsApp pindah ke Digiroom','Bukan otomatis pekerjaan tambahan'],['Auto2000 utama pindah ke OtoXpert sendiri','Hitung perubahan kontribusi, bukan dua job baru'],['S&D atau operator Toyota lain','Bukan otomatis GP Auto2000'],['Gratis/garansi/recall xEV','Payer dan reimbursement terpisah'],['Test drive/appraisal/request','Tahap proses, bukan delivery/GP']],note='CSV sensitivitas ternormalisasi dan kode aljabar disediakan. Kapasitas, biaya dan peluang take-up tidak dipalsukan menjadi proyeksi.')

page('Kesimpulan lama yang berubah','Catatan revisi',[
 'Laporan awal memisahkan peta lokasi dan daftar batas inferensi dengan baik, tetapi belum cukup memilih tindakan. Paket tindak lanjut ini mengubah unit keputusan dari kota dan jumlah marker menjadi pekerjaan, operator, cabang, jumlah perjalanan dan penyerahan hasil.'
],table=[['Kesimpulan/titik awal','Hasil penghitungan baru','Keputusan sekarang'],['Medan tampak tertinggal4,09menit','Pembanding oli membuatgap0,35menit','Slot Pancing dan kanal Ring Road'],['Palembang utara perlu perbaikan akses','Owned OtoXpert menghapus9tailoli','Routing kanal dahulu, bukan pickup baru'],['OtoXpert terutama menambah penawaran','Cakupan20menit kecil tetapi7originPalembang hemat>5menit','Nilai kanal pada kantong, bukan cakupan saja'],['Suci/Sidoarjo dikeluarkan','Koordinat dapat dikoreksi; Suci mengambil20origin','Koreksi tujuan; turunkan prioritas akses Cibiru'],['A.Yani/Kertajaya sama11origin','Gap dan substitusi internal berbeda; tanda bergantung origin','Mandat berbeda tanpa klaim unggul universal'],['Booking digital sebagai langkah utama','Entrybooking ada; akun positif/negatif membedakan handoff','Janji diterima sampai serah-terima'],['Charger sebagai proxy xEV','Task/referral dan validasi garansi adalah jalur berbeda','Satu Kasus xEV']],columns=[CW*.30,CW*.35,CW*.35])

# Main report ends here; concise methods and traceability follow.
page('Jejak bukti dan batas yang mengubah makna angka','Lampiran / metode ringkas',[
 'Input Filebin45430997byte berhasil dibaca sebagai ZIP dan lolos CRC. Seluruh311entri manifest baseline cocok SHA256; PDF awal cocok hash9561b2c32f7307dc0e82e2858d76f74b1df987a93203f68c8c85b78608fa964c. Baseline dipertahankan utuh.',
 'Geografi awal memakai324origin grid dan82.134pasangan model. Koreksi menambahkan dua endpoint dengan rute baru; perhitungan seluruh27cabang awal dan29endpoint koreksi memakai origin berpasangan yang sama pada tiap skenario. Satu tie TAA/Veteran dipertahankan sebagai7unik+1shared untuk tailTAA, bukan kepemilikan origin yang pasti.',
 'Perbandingan utama memakai jaringan oli/rem yang mendokumentasikan pekerjaan pada level jaringan, bukan seluruh kandidat generik. Fitmentmodel,grade/volume,parts danpajak adalah scopequote, bukan selisih harga yang diklaim telah diukur. Harga paket transmisi tidak dipakai sebagai harga oli/filter.',
 'OSRM adalah model rute profil publik, bukan lalu lintas aktual atau jaminan jalur tercepat global. Bangunan publik dan grid bukan pelanggan. Pekerjaan, kapasitas, switching dan GP tidak diamati dari titik peta. Temuan, akun pelanggan dan rekomendasi ditandai terpisah di ledger.'
],note='Ketegasan laporan berada pada pemilihan tindakan yang paling sesuai dengan bukti, bukan kepastian sebab-akibat atau volume pasar yang direka.')
page('Akun pelanggan dipakai sebagai mekanisme dan sanggahan, bukan persentase lintas kota','Lampiran / social listening',[
 'Audit sumber memuat14.892barisX dengan14.291IDunik;3.976IDulasanMaps dari25listing dengan2.870teks;74itemYouTube dari3video. Satuvideo Neta menyumbang45item, dan tidak ada komentar dari videoToyota yang ditargetkan. Unit tersebut tidak dijumlah menjadi jumlah pemilik kendaraan.',
 'Pembacaan mendalam menghasilkan33kasus ber-ID:23Maps,6X dan4YouTube, dengan parafrasa, file/baris, hash, konteks, valensi serta counterinterpretation. Seluruh74itemYouTube dibaca; tidak diklaim ada coding manual seluruh14.291postX.',
 'Maps berasal dariJabodetabek. Perbandingan positif/negatif Cilandak dan bridge lokal menghubungkan mekanisme dengan akses pada pasar yang sama. Proporsi keluhan tidak dipindahkan keSurabaya,Medan,BandungatauPalembang. Lokasi outlet bukan rumah penulis; tanggalunggah bukan otomatis tanggalkejadian.'
],table=[['Akun yang mengubah desain','Sumber dan peran'],['SOC12/SOC13/SOC14 Cilandak','Persetujuan sebelum kerja berhasil; janji selesai dan penerimaan estimasi dapat gagal'],['SOC01 Otoklix Simprug','Perpindahan pada akhir entitlement; bukan semua perpindahan'],['SOC10 Nawilis Radio Dalam','Puas tetapi datang dua kali'],['SOC15 B-Quik Citra8','Harga awal/invoice/waktu sebagai sanggahan murah selalu menang'],['SOC07 VF3 Nawilis','Hotline+reservasi+portablecharger; bukan kompetensi baterai traksi']],columns=[CW*.40,CW*.60])

# All branches in concise appendix; full job/operator metrics are delivered in CSV.
for off in range(0,len(branches),10):
 rows=[['Cabang / n terdekat','Gap oli / tail>5','Tindakan yang dipilih']]
 for _,z in branches.iloc[off:off+10].iterrows():
  g='-' if z.median_oil_gap_min=='' else f(z.median_oil_gap_min)
  rows.append([z.market+' / '+z.branch_name+' / n='+str(z.nearest_origins_n),g+' / '+str(z.oil_gap_gt5_n),z.recommended_intervention])
 page('Tabel keputusan seluruh29endpoint','Lampiran / cabang '+str(off+1)+'-'+str(min(off+10,len(branches))),[
  'n adalah origin grid terdekat pada skenario ketat, bukan pelanggan. Cabang dengan n0tetap ada dalam matriks jaringan dan dapat menjadi substitusi. CSV lengkap memuat operator, scope pekerjaan, cabang kedua, manfaat marginal dan alternatif yang tidak diprioritaskan.'
 ],table=rows,columns=[CW*.45,CW*.16,CW*.39],note='TAA memiliki satu tie denganVeteran. Cabang yang mendapat lebih sedikit origin tidak otomatis berkapasitas kosong atau tidak layak secara komersial.')

page('Sumber inti dan lokasi bukti','Lampiran / referensi',[
 '<b>G1-G4. Data geografis.</b> baseline/Auto2000_Geographic_Study/workstreams/routing/ berisiODawal,operator dan responscache. work/branch_analysis/ berisi hitungulang, corrected/,29endpoint dan keputusan. work/coordinates/ menyimpan sumber koordinat dan324ODtambahan. work/access/ memuat rute dua arah dan originbaru.',
 '<b>K1. Auto2000 Suci.</b> https://auto2000.co.id/dealer-toyota/bandung/auto2000bandungsuci ; sumber alternatif https://legaleraindonesia.com/tempat/toyota-auto2000-bandung-suci ; titikpeta dan alamat dicocokkan denganOverture.',
 '<b>K2. Auto2000 Sidoarjo.</b> https://auto2000.co.id/dealer-toyota/surabaya/auto2000kabupatensidoarjo ; decoderkoordinat dan rekamOverture tersimpan di coordinate_corrections.csv.',
 '<b>JB01-JB04. Scope pekerjaan.</b> DirektoriOtoXpert https://otoxpert.co.id/workshop ; Shop&Drive https://www.shopanddrive.com/outlet dan promoNovember; THS https://auto2000.co.id/berita-dan-tips/bengkel-mobil-panggilan . Seluruhtanggal/syaratpenawaran ada di coordinate_job_sources.csv.',
 '<b>S1. Akun pelanggan.</b> social_evidence_ledger.csv/.json memuat ID, sumberfile/baris, hash, parafrasa, valensi, konteks dan counterinterpretation. raw_inputs/ mempertahankan ekspor yang diberikan pengguna. Tidak ada actorberbayar atau kontakpelanggan dijalankan.'
],note='Sumber publik diakses14November2026. Catatanmentoring diterapkan sebagai prinsip penulisan keputusan; diagnosis kasusapartemen tidak dipindahkan keAuto2000.')
page('Sumber xEV, perjalanan dan paket reproduksi','Lampiran / referensi dan reproduksi',[
 '<b>XE01-XE14. JalurxEV.</b> xev_sources.csv dan xev_endpoint_paths.csv menyimpan delapan jalur bernama. HHC: https://aftersales.toyota.astra.co.id/hybrid-health-check ; requestZenixPancing: https://auto2000.co.id/testdrive/new-car/innovahybrid?branchCode=T570 . Halaman dan tahap permintaan tidak disamakan dengan unit/slot terkonfirmasi.',
 '<b>A1. Rute dan bangunan.</b> OpenStreetMapcontributors dan OSRM https://project-osrm.org/docs/v5.24.0/api/ ; OvertureMaps release2026-10-21.0 besertaatribusi sumberbangunan. Dua arah disimpan terpisah; originselection,querybounds,sourcehash dan hasilskenerio dipertahankan.',
 '<b>Ekonomi.</b> ECONOMICS.md dan economics.py membuktikan identitas titikimpas; normalised_economic_sensitivity.csv bukan margin atau upliftAuto2000.',
 '<b>Reproduksi.</b> ZIP mempertahankan baseline, data mentah unggahan, hitungulang, sumbertambahan, tabelkeputusan/insightledger, kode, responsrute, figur dan auditindependen. Hasil sudah dikalkulasi; instruksi reproduksi bukan pengganti keputusan laporan.'
],note='Perimeterkontribusi adalahAuto2000. Toyota danAstra lebihluas merupakan perimeterberbeda. SumberCCBY-NC pada materiSPKLU baseline tetap diberi atribusi dan kualifikasi lisensinya.')
c.save()
(R/'report/report_content.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False));(R/'qa/pdf_layout_bounds.json').write_text(json.dumps(qa,indent=2));print(PAGE,OUT)
