# Auto2000: keputusan cabang dan layanan berbayar

Tanggal:14 November2026. Mulai dari `output/report/Auto2000_Keputusan_Cabang_dan_Layanan.pdf`. Enam insight menjawab tindakan, pekerjaan, pemilik, cabang dan alternatif yang kalah.

## Berkas keputusan
- `output/tables/insight_ledger.csv` dan `.json`: enam insight dengan sumber, fakta, tafsir, tindakan dan sanggahan.
- `output/tables/branch_decision_table_29.csv`: seluruh27cabang awal ditambah Suci dan Sidoarjo; operator, pekerjaan, alternatif, cabang kedua dan manfaat marginal.
- `output/tables/shortlist_named_interventions.csv`: tujuh endpoint utama.
- `output/tables/job_protocols.csv`, `journey_protocol.csv`, `xev_endpoint_paths.csv`: scope pekerjaan dan alur penerimaan sampai penyelesaian.
- `output/figures/`: sebelas figur beresolusi tinggi.

## Paket sumber lengkap
- `extracted/`: paket handoff asli dipertahankan utuh, termasuk baseline312berkas, raw_inputs sosial/mentoring/strategi, reanalysis dan apify_optional. Folder apify_optional hanya konfigurasi; tidak dijalankan.
- `work/coordinates/`: koreksi Suci/Sidoarjo,324ODtambahan, bukti scope pekerjaan dan audit minimum generik.
- `work/branch_analysis/`: perhitungan baseline/corrected, seluruh29endpoint, tie dan marginal jaringan.
- `work/access/`:66originbaru,42footprintterpilih,24gridbergeser,5604ODarah,cache,jam Minggu, skenario kunjungan/antrean dan geometri rute.
- `source_building_queries/`: seluruh16querybangunan mentah270953241byte. Bangunan bukan identitas rumah, pemilik Toyota atau permintaan.
- `work/customer_journey/`:33kasus terpilih dengan parafrasa,ID,file/baris/hash dan pembanding positif/negatif.
- `work/xev/`:14sumber resmi,8jalur bernama serta ekonomi tanpa margin/uplift rekaan.
- `work/figures/` dan `work/review/`: kode, registry, audit independen dan receipt PDF final.

## Reproduksi
Gunakan Python3.12 dan dependensi dalam requirements.txt. Path utama relatif terhadap skrip, dengan struktur folder paket tetap.
1. Baca opsi CLI `work/branch_analysis/recompute_branches.py` untuk baseline/koreksi, kemudian `build_decisions.py`.
2. `python work/access/analyse_access.py` menghitung dari OD dua arah yang disertakan. Minimum outbound dan minimum roundtrip merupakan objektif berbeda.
3. `python output/code/integrate_origin_decisions.py` menyatukan uji origin ke keputusan29endpoint.
4. `python work/review/independent_final_audit.py` mengaudit angka secara independen tanpa akuisisi.
5. Kode figur di work/figures menggambar dari tabel. Jalankan `output/code/build_insight_ledger.py`, lalu `output/code/build_decision_report.py` untuk keluaran.
6. `output/code/economics.py` memeriksa aljabar; sensitivitas ternormalisasi bukan proyeksi perusahaan.

Akuisisi internet terpisah dari tahap offline. Semua sumber dan respons yang dipakai tersedia. Reacquisition halaman/rute dapat berubah; jangan menimpa versi asal untuk membandingkan snapshot. Tidak perlu actor berbayar, login, CRM atau kontak pihak lain.

## Arti angka
Origin adalah lokasi perhitungan, bukan pelanggan. Akun pelanggan adalah self-report. Origin bangunan/grid adalah stress test terarah, bukan sampel populasi. Jam publik bukan slot/stock. OSRM bukan lalu lintas aktual. Scope jaringan bukan quote model/VIN tertentu. Perimeter GP utama adalah Auto2000; Toyota/Astra/operator lain berbeda. Tidak ada demand, kapasitas, switching atau GP yang direka.

## Hak dan atribusi
Atribusi baseline dipertahankan, termasuk SPKLU CC BY-NC3.0. Overture Places/Buildings mempertahankan source/license fields; mayoritas bangunan berasal dari Google Open Buildings. OpenStreetMap contributors dan OSRM diberi atribusi. Data sosial mentah adalah unggahan pengguna; paket lengkap bukan izin menyebarkan nama, handle atau isi ulasan secara umum. Laporan memakai parafrasa dan ID kasus. Tidak ada booking, kontak, VIN pelanggan atau actor berbayar yang dijalankan.
