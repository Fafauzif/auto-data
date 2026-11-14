# Temuan keputusan dari origin dan perjalanan dua arah

## Keputusan utama

1. **Jangan membaca nol winner Sidoarjo sebagai cabang tidak relevan.** Enam origin tambahan pada footprint bangunan di selatan window Surabaya seluruhnya memilih Sidoarjo yang telah dikoreksi. Selisih median perjalanan pulang-pergi terhadap jaringan oli hanya +0,021 menit. Batas lama berhenti di lintang-7,38, sedangkan cabang berada sekitar-7,441. Ini koreksi ruang analisis, bukan estimasi basis pelanggan baru.

2. **Kontras A.Yani–Kertajaya bertahan sebagai keputusan layanan, tetapi tanda unggul A.Yani tidak mutlak pada semua origin.** Pada enam titik setengah-sel bergeser dari setiap kelompok, median gap satu arah yang dioptimalkan ulang adalah +0,246menit untuk kelompokA.Yani dan +2,173menit untuk kelompokKertajaya. KelompokA.Yani mendekati paritas; kelompokKertajaya lebih tertinggal. Titik bangunan memberi gap yang sama pada enam titik masing-masing. Nearestbranch boleh berubah ketikaoriginbergeser; tabelmenyimpan nama baru. Tidak menyamakan enam stress-testpoint dengan seluruh11originbaseline atau pemilikToyota.

3. **Soekarno-Hatta tetap kandidat pengurangan beban perjalanan setelah Suci masuk jaringan.** Enam origin bergeser dan enam origin pada bangunan memberi median gap minimum satu arah +3,557menit; median gap pulang-pergi+7,098menit. Ini stress-testterarah pada enam kuantilgapcatchment semula, bukan median seluruhcatchment. Gunakan THS untuk pekerjaan oli/filter sesuai cakupan; remdepan tetap ke bay denganparts/slot disiapkan. TAA tidak otomatis menerima intervensipickup seragam karena OtoXpertAuto2000 sudah menutup tail tertentu.

4. **Satu kunjungan tambahan dapat membalik keunggulan lokasi Cilandak.** Pada building-origin `built_bridge_2_1`, rute Cilandak berangkat4,857menit dan kembali3,088menit, total7,945. OtoXpertFatmawati berangkat4,087 dan kembali4,788,total8,875. Keunggulan Auto2000 hanya0,930menit pulang-pergi. Dua kunjungan Auto2000 melawan satu kunjungan OtoXpert memberi15,890−8,875=+7,015menit. Ini skenario eksplisit, bukan perjalanan aktual penulis ulasan. Gunakan bukti positif/negatif Cilandak sebagai mekanisme konfirmasi/penyelesaian, bukan frekuensi kegagalan.

5. **Minggu harus dirutekan berdasarkan pekerjaan, bukan jam showroom.** Cilandak showroom Minggu09–17, bengkel libur (XE10). OtoXpertFatmawati dioperasikanAuto2000 dengan publikasiMon–Sun08–18. Pada originbridge2_1 lokasinya kalah0,93menit dalam perjalananpulang-pergi, tetapi mempunyai jalur jam kerja oli yang terdokumentasi untuk Minggu. TampilkanFatmawati untuk tugas oli yang sesuai dan konfirmasi slot; jangan mengirim permintaan servis ke showroomCilandak. Provider dengan jam tidak diketahui tidak ditandai tutup.

6. **TAAterburuk yang dilacak tidak membutuhkan cerita umum kota sungai.** Origintail `g08_08` berute keTAA24,153menit/16,785km, sementara OtoXpertPalembang(Auto2000)17,568menit/9,950km. Keduanya menggunakan LumbanMarantiJaya–SematangBorang–Siaran–KopralAnwar–RHAmaluddin–ResidenHajiNajamuddin; routeTAA berlanjut melaluiHMNoerdinPandji/HarunSohar. Nama jalan bukan bukti seluruh penyebab; geometri lengkap tersedia. Tidak menyimpulkan kemacetan atau arah jembatan tanpa data. Routing ke kanal operator sendiri untuk oli lebih langsung daripada subsidi pickup menyeluruh.

## Cakupan tambahan

-66origin:24origin setengah-sel bergeser dari enam kuantilgap untuk empat kelompok cabang;42origin pada representativepoint footprint bangunan, termasuk12bridgeJabodetabek dan6ekstensiSidoarjo.
-Semua target memiliki bangunan terpilih dalam168meter. FootprintOverture2026-10-21.0 umumnya bersumberGoogleOpenBuildings dan tidak memiliki kelasresidensial; sebutstruktur terpetakan, bukanrumah, permukimanterkonfirmasi, atau pemilikToyota.
-5.604ODarah baru; setiap outwarddanreturn dihitungterpisah. Ketidaksimetrianmedian55detik,max668,1detik pada seluruh pasangan. Jangan menggandakan rute satu arah sebagai fakta.
-Perjalanan utama membandingkan semua endpoint jaringan terdokumentasi dalam windowdestinasi lama yang diperluas, ditambah koreksiSuci/Sidoarjo. Bridge memakai semua endpointAuto2000/OtoXpert/S&D terhimpun di bbox106,70–106,88;−6,36–−6,15 dan tiga listingkasusNawilis/Otoklix. Tidak memakai shortlistEuclidean untuk menentukanminimumrute.
-Optimasi minimumoutbound dan minimumroundtrip dipisahkan. Kolom`outbound_optimized_gap_minutes` tepat untuk sensitivitasorigin satuarah. Kolom`roundtrip_gap_minutes` untuk skenariobebanperjalanan. Outbounddurasi dari pemenangroundtrip bukan selalu minimumoutbound.

## Definisi beban perjalanan

Menunggu di lokasi: dua roadlegs, waktu berkomitmen=out+return+queue+service. Dropoff dan ambil: empat roadlegs dengan profiljalan sama; returntransportactual tidakdiamati. Pickup/return: tidak ada roadleg dikemudikan pelanggan; kendaraan tetap menempuhout+return dan logisticsdriver bergantung skema operasional. THS: nol roadlegpelanggan untuk job yangsesuai; teknisi menempuhroadroundtrip. Peralihanbeban bukanpenghapusanbiaya jaringan.

`queue_visit_sensitivity.csv` menggunakan0/15/30/60menitantrean dan satu/dua kunjungan, serta30menitdurasi job sama sebagai sensitivitas berlabel. Tidak diklaim sebagai waktu aktual atau peluangkegagalan. Titikimpas waktu diturunkan langsung dari selisihroundtrip.

## Reproduksi dan sumber

Inputasal ada di `extracted/baseline/Auto2000_Geographic_Study`, koreksi di `work/coordinates/coordinate_corrections.csv`, dan semua queryfootprint mentah di `source_building_queries/`. `selected_building_source.parquet` danGeoJSON mempertahankan sourceID/provenance/geometry untuk42origin. Jalankanprepare_inputs,anchor_buildings,route_new_origins,analyse_access. Akuisisi kembali terpisah melaluiacquire_buildings/fill_building_gaps. RoutecacheJSON, manifestrequest, tabelarah dansourceURL disimpan. Tidak ada actor, login atau kontak keluar.
