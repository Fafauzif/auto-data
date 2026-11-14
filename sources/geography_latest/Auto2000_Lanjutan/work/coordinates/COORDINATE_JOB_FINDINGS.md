# Audit koordinat dan relevansi pekerjaan

## Keputusan yang dapat diambil sekarang

1. Pulihkan Auto2000 Suci dalam skenario jaringan Bandung. Alamat resmi PHH Mustofa6 dan titik alternatif publik(-6.901998,107.648162) sesuai satu record Overture bernama/alamat sama dalam9m. Tautan resmi lama menunjuk lokasi Setiabudi, sehingga pengecualian Suci pada baseline adalah keputusan kualitas data, bukan bukti cabang tidak beroperasi. Halaman cabang resmi masih mengiklankan bengkel, paketservis danTHS, dengan jadwal layanan. Record Overture lain di107.63438 tidak dipilih karena tautanpeta publik dan recordalamat yanglebihtepat menunjuk107.648162.

2. Pulihkan Auto2000 Sidoarjo sebagai skenario titik resmi yang didekode. Digit1127197388267770,-7441297706613890 menjadi lon112.719738826777 danlat-7.44129770661389 setelah pemulihan desimal danurutannya. Record Overture exactname/Jenggolo60 berjarak23m mendukung pilihan ini. Halaman resmi tidak menyediakan jam; jangan mengarang jam atau menandainya tutup.

3. Gunakan titik fasilitas tersebut sebagai kandidat rute yang dapat dilacak, bukan klaim pintumasuk disurvei. OSRM memindahkan titik tujuan Suci30.64m danSidoarjo12.41m ke jaringan jalan. Kedua endpoint lolos layar250m.324barisOD baru mencakup81origin ke masing-masing cabang dan rute balik yang dihitung terpisah. Hasiljaringan sebelum/sesudah dihitung agen branch_analysis.

4. Pertahankan pilihanoperator-aware. Audit ulang direktori Shop&Drive saat ini menemukan identitas dan koordinat12pemenang minyak teratas(3perpasar) tetap sama. Namaoutlet A.YaniBaru mempunyai beberapa kecocokan; pencocokan menggunakan nama+koordinat, bukan nama saja.

5. Hentikan penggunaan kandidat generik sebagai pembanding pekerjaan Toyota. Auditpemenang minimum menemukan11originPalembang memilih perumahanGrandMutiaraRegency atau DipoLokomotifKertapati, serta3originSurabaya memilih pusat sepeda motorALVA. Sumber primer pemerintah/KAI/ALVA danalamat mendukung pengelompokan tersebut. Menghapus hanya3record ini menurunkan mediangapgenerikPalembang3.425→3.317menit, tetapi tidak mengubahmediankotalain. Dengan demikian, kasus ini membuktikan salahjenis endpoint, bukan alasan mengklaim selisihkota sepenuhnya disebabkan kesalahan3record.

## Pekerjaan dan intervensi

Gunakan Toyota Avanza2019 1.3bensin sebagai kendaraan rujukan, dengan payer di luar entitlement servis gratis/prepaid. Paketoli harus menyebut oli,filter,gasket,jasa,pajak secara eksplisit; paketkampasrem harus satuaxledepan dan merekpart yangjelas. Jangan memperlakukan diskonpaket oli+transmisi sebagai harga oilfilterstandar.

Sumber resmi Shop&Drive November2026 saatini memperlihatkan oli/filter dan pemasangan brakepad dalampenawaran jaringan. Bukti lebih baru ini menggantikan kebergantungan pada promoJanuari yangsudahberakhir. Namun,jendela promo berbeda: harga4Literanniversary13–16Novtidak otomatis mencakupfilterB3G1periode4–26Nov; pakettransmisiRp638k bukanjobyangsama; diskonbrakepadPaydaytercantumpada1–3/27–30Nov,sehingga janganmenyatakannya tarifaktif14Nov.

THS Auto2000 telah mendokumentasikan oilfilter di rumah dan booking Digiroom. PilihTHS yangsudahada untuk kantong bebanperjalanan pekerjaanringan, bukanmembangunfiturbookingduplikat. Untukfrontpad, pesanpart/slotworkshop; sumberTHS mendokumentasikan pemeriksaanrem, bukanjanji semua penggantiankampas dapat dilakukan di rumah. Diagnosishighvoltage tetapjalurtersendiri.

T-OPT telah mendokumentasikan keluarga frontdisc padAvanza/Veloz/Rush04465-TT205-8M dan kanalOtoXpert/ToyotaPartShop. HargaRp205600 adalah harga partspublik24Juli2024, bukanquotepasang2026. Keputusan ekonomisnya adalah menawarkan partsyangsesuai melalui kanalexisting, bukan mengarangselisihhargaterukur.

## Berkas
- coordinate_corrections.csv: titiklama/baru, sumber, jarakcorroborasi.
- corrected_endpoint_od.csv:324ODbaru denganarahterpisah.
- cache/ dan routing_acquisition_log.json:responsOSRMtanpabebanbaru.
- coordinate_job_sources.csv dan job_protocols.csv: klaimterbatas, keputusanjob, sumber.
- winning_oil_endpoint_audit.csv:12endpointpemenangdirektori.
- generic_minimum_origin_audit.csv:284originstrictminima; bukan284pelanggan.
- generic_confirmed_noncar_sensitivity.csv: pengaruhhapus3recordpubliknoncar.
- CORRECTION_QA.json:uniqueness/nonnegativity/counts.
