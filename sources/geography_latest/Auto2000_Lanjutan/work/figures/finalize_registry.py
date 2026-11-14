from pathlib import Path
import json
P=Path(__file__).parent/'figure_registry.json';r=json.loads(P.read_text())
notes={
'02_surabaya_dua_mandat.png': 'Koordinat Suci/Sidoarjo dipulihkan; origin berpasangan, snap≤250m. Selisih negatif berarti Auto2000 lebih dekat daripada jaringan oli. Penalti ke Auto2000 kedua adalah substitusi geografis internal, bukan kapasitas kosong, omzet, atau dasar penutupan. Segitiga=cabang; kotak=origin model.',
'03_palembang_kantong_utara.png': 'Sembilan origin berpasangan memiliki gap awal ke jaringan oli >5 menit. TAA memiliki tujuh origin unik dan satu seri dengan Veteran. Urutan baseline mengalokasikan seri ke TAA, sehingga menghasilkan 8/9; Veteran memiliki satu unik dan satu seri; Plaju 0. Peta ini tidak menetapkan sungai atau jembatan sebagai penyebab. Lihat figur07 untuk solusi menggunakan OtoXpert milik Auto2000.',
'04_suci_mengubah_prioritas.png': 'Origin berpasangan Bandung tetap sama(n=78). Suci menggunakan kandidat koordinat alternatif yang sejalan dengan alamat resmi dan Overture. Baseline mengecualikannya karena tautan koordinat menyalin Setiabudi. Koreksi juga memasukkan Sidoarjo ke jendela destinasi Surabaya; hasil lengkap tersedia di CSV.',
'05_otoxpert_marginal.png': 'Bandingkan minimum Auto2000 umum dengan minimum Auto2000 ditambah OtoXpert yang berlabel dioperasikan Auto2000. n=59/78/78/69; snap≤250m; koordinat dikoreksi. Tambahan cakupan 20 menit adalah 0/0/0/2. Penghematan waktu bukan margin tambahan; label operator tidak menunjukkan pembagian GP.',
'06_operator_alternatif_lokal.png': 'Klasifikasi jaringan oli terdekat per origin pada catchment Auto2000 umum terpilih, snap≤250m, koordinat diperbaiki. Shop&Drive dan OtoXpert operator lain bukan otomatis GP Auto2000. Label jaringan menunjukkan penawaran oli, bukan konfirmasi parts, slot, atau model individual.',
'07_palembang_ox_menutup_gap.png': 'Origin berpasangan yang sama(n=69), snap≤250m, koordinat diperbaiki. Sembilan origin awal dengan gap >5 menit menjadi tujuh origin paritas dan dua origin dengan gap 1,005 menit setelah Auto2000 umum digabungkan dengan OtoXpert miliknya. Ini akses model ke penawaran jaringan oli, bukan hasil intervensi yang diobservasi atau bukti kapasitas. Channel tidak dijumlahkan sebagai bisnis baru.',
'11_sidoarjo_batas_jendela.png': 'Enam origin bangunan yang ditambahkan di sekitar Sidoarjo semuanya memiliki Sidoarjo sebagai Auto2000 terdekat setelah koordinat dipulihkan. Median gap pergi+pulang ke jaringan oli sekitar 0,02 menit. Ini uji batas studi, bukan tambahan enam pelanggan atau bukti jumlah permintaan.'}
for x in r:
 k=Path(x['file']).name
 if k in notes:x['caption']=notes[k]
 x['title']=x['title'].replace('seluruhkantong','seluruh kantong').replace('gapoli','gap oli').replace('cabangbaru','cabang baru').replace('sama-sama11origin','sama-sama 11 origin')
P.write_text(json.dumps(r,indent=2,ensure_ascii=False));print('Registry final',len(r))
