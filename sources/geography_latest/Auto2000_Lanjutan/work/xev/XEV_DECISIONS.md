# Keputusan xEV: bawa pekerjaan ke endpoint yang tepat, lalu pertahankan pemilik kasus sampai hasilnya selesai

## Headline yang dapat masuk insight akhir

**HHC sudah menyambungkan hasil baterai ke validasi garansi; Digiroom harus menjaga satu kasus sampai selesai, bukan mengarahkan semua pemilik xEV ke charger terdekat.**

Toyota menyatakan bahwa pengecekan HHC untuk HEV/BEV yang memenuhi ketentuan dilakukan bersama servis berkala, menghasilkan sertifikat, dan bila hasilnya Not Good dealer melakukan validasi serta menjelaskan cakupan garansi. Dengan demikian, satu tugas pemilik bukan sekadar menemukan titik pengecekan. Tugasnya adalah memperoleh pemeriksaan yang sesuai kelayakan, hasil, keputusan cakupan, dan langkah penyelesaian tanpa mengulang penjelasan dari awal. Ini menempatkan mekanisme handoff sebagai rancangan utama untuk xEV; jumlah charger tetap lapisan informasi pendukung. Sumber XE01 dan XE02.

**Tindakan:** bentuk alur **Satu Kasus xEV** dengan satu Service Advisor pemilik kasus, model/VIN dan keluhan yang ikut berpindah, status kelayakan sebelum perjalanan, endpoint kompeten yang disebutkan sebelum pelanggan berangkat, hasil pemeriksaan, keputusan payer/garansi, dan status resolusi. HEV rutin yang memenuhi syarat dapat digabung dengan servis berkala; BEV bermasalah tidak otomatis dialihkan ke layanan rumah.

**Alternatif yang kalah:** direktori charger generik, form booking tambahan tanpa kepastian kemampuan, dan hitungan kunjungan HHC yang dianggap setara tambahan pekerjaan berbayar. Ini kalah karena ketiganya tidak menutup tugas pemilik yang sudah didefinisikan oleh program, sementara hasil baterai bermasalah memerlukan tindak lanjut.

## Endpoint bernama yang dapat dipakai dalam rancangan

| Pasar | Titik masuk yang dipilih | Bukti lokal | Tugas/keputusan |
|---|---|---|---|
| Surabaya | Auto2000 Jemur Sari | Artikel resmi kota secara spesifik menyebut perawatan hybrid | Pemilik Zenix/HEV yang memenuhi syarat: satu konfirmasi servis berkala + HHC, sertifikat dan tindak lanjut |
| Medan | Auto2000 Pancing | Artikel resmi kota menyebut perawatan hybrid; halaman cabang memiliki bengkel dan jalur penawaran | Masukkan HHC ke konfirmasi yang sama, dengan kelayakan model/riwayat, bukan booking kedua |
| Bandung | Auto2000 Soekarno-Hatta | Publikasi adviser cabang menjelaskan HHC untuk HEV/BEV dan sertifikat | Gunakan sebagai titik kontak program yang terdokumentasi; nama endpoint diagnostik harus ditetapkan sebelum perjalanan |
| Palembang | Auto2000 Tanjung Api-Api | Bengkel, adviser dan model xEV dipublikasikan, tanpa roster perbaikan baterai lokal | Intake model/masalah dipertahankan oleh pemilik kasus; tunjuk endpoint diagnosis yang menerima masalahnya sebelum dispatch |
| Jabodetabek bridge | Auto2000 Cilandak | Bengkel dan showroom memiliki jadwal berbeda | Booking mengikuti jam bengkel; pelanggan tidak diarahkan ke showroom Minggu untuk pekerjaan bengkel |

Titik masuk adalah penanggung jawab rute layanan yang direkomendasikan, bukan klaim bahwa semua cabang di atas telah menerima atau memperbaiki kasus baterai tegangan tinggi tertentu. Tabel `xev_endpoint_paths.csv` membedakan level bukti dan menyimpan koordinat serta sumber.

## Prong 1: jangan membangun ulang booking test drive yang sudah membawa model dan cabang

Pemeriksaan read-only pada halaman Pancing menunjukkan tautan test drive Zenix yang benar-benar membawa `innovahybrid?branchCode=T570`. Halaman tersebut meminta lokasi/waktu dan mengatakan tim akan menghubungi untuk konfirmasi serta menyesuaikan unit/varian yang tersedia. Ini lebih kuat daripada sekadar menganggap fitur booking ada di katalog. Sumber XE04 dan XE05.

**Tindakan:** gunakan **Demo Siap Berangkat**. Shortlist Zenix HEV/bZ4X, varian yang ingin dicoba, kebutuhan penggunaan dan cabang tetap melekat pada permintaan yang sudah ada. Pelanggan berangkat setelah adviser mengonfirmasi unit/varian, lokasi, jam dan status penawaran. Untuk Kertajaya, konsultasi hybrid versus BEV sudah dipublikasikan lokal, sehingga jalur ini dapat dipakai tanpa membuat konten produk duplikat. Sumber XE11.

**Alternatif yang kalah:** form test drive generik baru atau showroom 3D sebagai prioritas sebelum kepastian unit/slot. Bukti menunjukkan input model/cabang sudah tersedia; perbaikan yang relevan adalah janji yang diterima cabang dan dapat dipenuhi. Tidak ada klaim bahwa unit demo tertentu tersedia sekarang atau bahwa friksi ini merupakan penyebab dominan seluruh kehilangan penjualan.

**Ukuran bisnis:** completed test drive → penawaran → SPK → delivery. Delivery pertama di Auto2000 ditentukan riwayat beli Auto2000, bukan apakah pemilik pertama kali memiliki mobil listrik. Perpindahan lead WhatsApp ke aplikasi bukan penjualan tambahan dengan sendirinya.

## Prong 3: satukan inspeksi dan penawaran upgrade, bukan menjamin nilai jual masa depan

Publikasi adviser Auto2000 Sudirman menjelaskan rute OLXmobbi: jadwal inspeksi, penawaran, kesepakatan dan transfer nilai mobil lama sebelum pembayaran selisih mobil baru. Angka yang ditampilkan di artikel merupakan ilustrasi. Sumber XE12.

**Tindakan:** bentuk **Upgrade Sekali Janji** untuk pembeli Auto2000 sebelumnya, misalnya pemilik Avanza 2019 yang mempertimbangkan Zenix HEV. Bawa status nilai indikatif versus hasil inspeksi, masa berlaku penawaran, sisa pinjaman, ekuitas bersih dan penawaran mobil baru dalam satu dossier adviser. Jika inspeksi dan test drive dapat dijadwalkan bersama, satukan janji; jika tidak, jelaskan langkah dan endpoint berikutnya sebelum pelanggan berangkat.

**Alternatif yang kalah:** janji floor resale, subsidi trade-in menyeluruh dan klaim bahwa sertifikat baterai pasti menaikkan appraisal. Tidak ada kewajiban pendanaan future-value yang dibuktikan oleh data ini, sementara rute inspeksi dan penawaran sudah terdokumentasi. Sertifikat dapat dilampirkan sebagai informasi, bukan jaminan harga.

## Konfirmasi harus mengikuti tugas dan jam fasilitas

Halaman Cilandak menyatakan showroom Minggu 09.00–17.00 tetapi bengkel libur. Sabtu showroom 08.00–18.00, bengkel 08.00–13.00. Jadi label dealer “buka” tidak cukup untuk menentukan waktu servis. Pancing memublikasikan bengkel 08.00–17.00 setiap hari, sedangkan Tanjung Api-Api mencantumkan akhir pekan 08.00–12.00. Ini fakta jadwal yang dipublikasikan, bukan pengukuran antrean atau ketersediaan slot. Sumber XE04, XE09 dan XE10.

**Tindakan konkret:** pemilih slot harus membaca job dan fasilitas bengkel, bukan jam showroom. THS menggunakan jalur yang memang sudah ada, dengan kecocokan pekerjaan/alat dan konfirmasi dispatch; ketentuan situs memisahkan lead-time booking general repair dan THS. Jangan mengiklankan perbaikan baterai tegangan tinggi melalui THS generik. Sumber XE13 dan XE14.

## Payer dan perimeter

T-CARE XTRA menyatakan servis 8–11 customer-paid dapat menambah perlindungan garansi. Jadi memilih pemilik hanya berdasarkan umur garansi akan kehilangan pemisahan yang relevan. Pisahkan: customer-paid petrol; customer-paid HEV service; HHC yang memenuhi benefit; warranty reimbursement; recall. Catat actual GP/payer sekali per transaksi. OtoXpert operator lain dan Shop&Drive terkait ekosistem yang lebih luas tidak otomatis menghasilkan GP Auto2000. Sumber XE03 serta label operator baseline.

## Ekonomi intervensi

Gunakan `ECONOMICS.md` dan `economics.py` untuk membandingkan desain tanpa mengarang margin atau uplift. Model memasukkan subsidi yang bocor ke pekerjaan baseline serta pekerjaan yang tergeser. Titik impas harus memakai tambahan pekerjaan yang benar-benar direbut, bukan jumlah booking aplikasi yang berpindah kanal. Jika diskon/biaya operasional sudah masuk margin aktual g, jangan kurangi lagi sebagai c.

## Audit proses

14 sumber resmi, 8 jalur endpoint bernama, 0 kontak kepada pihak lain, 0 pengajuan booking, 0 actor berbayar. Koordinat memakai kandidat official-direction baseline. Pemeriksaan test drive hanya membuka tautan dan membaca halaman. Tidak ada VIN, data pelanggan atau login yang dimasukkan. Ringkasan fakta dan locator disimpan; halaman lengkap berhak cipta tidak dimirror.
