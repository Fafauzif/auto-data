from pathlib import Path
import pandas as pd,json
R=Path(__file__).resolve().parent
b=pd.read_csv(R/'corrected/all_27_branches_recomputed.csv');b=b[b.scenario=='snap_le_250m'].copy()
rows=[]
for _,r in b.iterrows():
 name=r.branch_name; n=int(r.nearest_origins_n)
 action='Paket Oli Terjadwal '+name.replace('Auto2000 ','');objective='penawaran dan kepastian penyelesaian';priority='pendukung';loser='Pickup menyeluruh lebih dulu tidak ditopang kantong selisih yang besar di catchment ini.';segment='Pemilik Toyota Avanza 2019 G 1.3 yang membayar oli+filter sendiri, di luar entitlement gratis/prepaid, terutama pekerjaan terakhir di luar Auto2000.'
 reason=f"{n} origin terdekat; median gap oli {r.median_oil_gap_min:.3f} menit; {int(r.oil_gap_gt5_n)} origin gap>5 menit."
 if 'A. Yani' in name:
  action='Oli Pasti Selesai A. Yani';priority='shortlist utama';reason+=' Akses lebih cepat daripada jaringan oli; kehilangan cabang menambah median3,757menit pada catchment.';loser='Perluasan fisik atau subsidi pickup massal kalah terhadap penawaran/konfirmasi/persetujuan kerja di cabang yang sudah unggul akses.'
 elif 'Pancing' in name:
  action='Slot Sampai Serah-Terima Pancing';priority='shortlist utama';objective='penawaran dan perlindungan keandalan slot';reason+=' Delapan origin kehilangan akses<=15menit bila Pancing dihilangkan; jaringan sendiri lain bukan pengganti mudah.';loser='Memindahkan layanan ke cabang lain atau membangun kanal baru untuk menyelesaikan selisih kota0,347menit tidak lebih kuat daripada melindungi slot Pancing.'
 elif 'Kertajaya' in name:
  action='Pilihan Oli Rungkut dari Kertajaya';priority='shortlist utama';objective='routing pekerjaan oli ke kanal Auto2000 yang sudah tersedia';reason+=f" OtoXpert-owned menghapus {int(r.oil_gap_gt5_n-r.owned_network_gap_gt5_n)} dari{int(r.oil_gap_gt5_n)} tail>5menit; median gap tersisa{r.median_owned_network_gap_min:.3f}menit.";loser='Pickup atau tier ekonomis baru kalah terhadap menawarkan OtoXpert Rungkut sebelum pelanggan berangkat; tetap tawarkan cabang utama untuk scope yang tidak sesuai.'
 elif 'Gatot Subroto' in name:
  action='Oli Tepat Kanal Ring Road';priority='shortlist utama';objective='pilihan kanal ekonomis operator Auto2000';reason+=f" Median gap menjadi{r.median_owned_network_gap_min:.3f}menit setelah OtoXpert Ring Road Medan diperbolehkan.";loser='Perluasan jaringan bengkel ekonomis baru kalah terhadap pemanfaatan kanal Ring Road yang tersedia.'
 elif 'Tanjung Api' in name:
  action='Oli Tepat Kanal Palembang';priority='shortlist utama';objective='alih tujuan pekerjaan oli ke OtoXpert Palembang sebelum perjalanan';reason+=f" Semua{int(r.oil_gap_gt5_n)} tail catchment turun<=5menit melalui OtoXpert-owned; median gap tersisa{r.median_owned_network_gap_min:.3f}menit.";loser='Pickup Tanjung Api-Api atau intervensi jembatan Plaju lebih dulu kalah terhadap router pekerjaan/operator yang menghilangkan seluruh tail kota pada data ini.'
 elif 'Soekarno' in name:
  action='Sekali Datang Soekarno-Hatta';priority='shortlist utama';objective='kurangi jumlah perjalanan untuk kantong ketertinggalan tersisa';reason+=f" Setelah koreksi Suci dan OtoXpert-owned, masih{int(r.owned_network_gap_gt5_n)} tail>5menit; median gap tersisa{r.median_owned_network_gap_min:.3f}menit.";loser='Hanya mengalihkan seluruh permintaan ke Suci/OtoXpert tidak menyelesaikan8origin tail; tunggu onsite/THS oli sesuai cakupan mengurangi perjalanan sebelum subsidi pickup umum.'
 elif name=='Auto2000 Suci':
  action='Tujuan Benar Suci';priority='shortlist utama';objective='perbaiki koordinat dan branch selection';reason+=' Koreksi publik mengalihkan20origin; menurunkan gap median Bandung2,636→1,736menit tanpa gedung baru.';loser='Pickup/ekspansi untuk catchment Cibiru yang semula tampak besar kalah terhadap koreksi destinasi dan branch routing Suci.'
 elif 'Cibiru' in name:
  action='Cabang Tepat Cibiru–Suci';objective='branch routing dan perlindungan tepi catchment';reason+=' Sesudah Suci, origin terdekat22→14, tail4→1; Suci menjadi cabang kedua dominan.';loser='Memprioritaskan pickup massal berdasarkan22origin awal kalah setelah20origin kota dirutekan ulang ke Suci.'
 elif name=='Auto2000 Plaju':
  action='Konfirmasi Satu Kunjungan Plaju';objective='penawaran rutin; bukan hotspot akses';loser='Narasi sungai/jembatan sebagai dasar pilot transport Plaju kalah: nol origin gap>5menit, sedangkan seluruh sembilan tail kota berada TAA/Veteran.'
 elif name=='Auto2000 Veteran':
  action='Triage Oli Veteran–OtoXpert Palembang';objective='routing oli dan perlindungan slot cadangan';reason+=' Satu tail (dua jika tie dialokasikan Veteran) hilang lewat kanal OtoXpert-owned; satu origin kehilangan<=20menit bila Veteran dihilangkan.';loser='Ekspansi fisik untuk tail Veteran kalah terhadap OtoXpert yang tersedia; tetap pertahankan peran cabang untuk scope lainnya.'
 elif 'Medan Marelan' in name:
  action='Jaga Slot Marelan';objective='lindungi lokasi yang sudah unggul akses';reason+=' Gap negatif dan median cabang kedua4,185menit lebih lama; pertahankan service owner dan stock/slot sebelum memindah lokasi.';loser='Mengalihkan pemilik ke cabang pusat demi konsolidasi kalah secara akses lokal.'
 elif 'Soreang' in name:
  action='Jaga Slot Soreang';objective='perlindungan akses perifer';reason+=' Median cabang kedua4,368menit lebih lama; jangan gunakan sedikit origin sebagai alasan menarik layanan.';loser='Sentralisasi ke Soekarno-Hatta tidak menguntungkan waktu akses origin lokal.'
 elif n==0:
  action='Rute Cadangan '+name.replace('Auto2000 ','');objective='cadangan jaringan; tidak dipilih sebagai pilot dari window ini';priority='tidak diprioritaskan dari window';reason='Tidak menjadi cabang terdekat pada origin tersaring dalam window penelitian, bukan bukti tutup, tidak ada pelanggan atau rendah kapasitas.';loser='Memilih cabang ini sebagai pilot berbasis catchment grid saat ini kalah terhadap cabang dengan origin dan masalah teridentifikasi; jangan simpulkan potensi pasar seluruh wilayah.'
 elif int(r.owned_network_gap_gt5_n)>0:
  action='Sekali Datang '+name.replace('Auto2000 ','');objective='kurangi perjalanan pada kantong spesifik';reason+=f" Tail sesudah router OtoXpert-owned masih{int(r.owned_network_gap_gt5_n)}origin.";loser='Subsidi pickup satu kota kalah terhadap menargetkan origin tail dan memastikan harga/parts/slot sebelum berangkat.'
 row=r.to_dict();row.update({'recommended_intervention':action,'decision_objective':objective,'priority_class':priority,'owner_job_segment':segment,'brake_route_rule':'Kampas rem depan tetap jalur bengkel yang mengiklankan rem; Comparator jaringan rem OtoXpert+S&D dengan bukti fitting kampas network-level; sensitivitas OtoXpert-only tersedia. Bukan otomatis THS. Spesifikasi parts/fitment disetujui sebelum berangkat.','evidence_reason':reason,'deprioritised_choice':loser,'commercial_perimeter':'Utama Auto2000; OtoXpert hanya yang berlabel operator Auto2000; S&D Astra Otoparts dan OtoXpert operator lain bukan otomatis GP Auto2000.'})
 rows.append(row)
pd.DataFrame(rows).to_csv(R/'branch_decision_table_29.csv',index=False)
short=pd.DataFrame(rows);short=short[short.priority_class=='shortlist utama'];short.to_csv(R/'shortlist_named_interventions.csv',index=False)
print(short[['branch_name','recommended_intervention','decision_objective']].to_string(index=False))
# Reproducible before/after origin comparison on paired keys.
old=pd.read_csv(R/'origin_channels_recomputed.csv');new=pd.read_csv(R/'corrected/origin_channels_recomputed.csv')
comparison=old.merge(new,on=['market','scenario','origin_id'],suffixes=('_old','_new'))
comparison[comparison.scenario=='snap_le_250m'].to_csv(R/'coordinate_before_after_origins.csv',index=False)
