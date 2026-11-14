# Batas ekonomi yang langsung membedakan intervensi

Gunakan perimeter Auto2000, bukan laba seluruh Toyota/Astra. Ketika pekerjaan dialihkan ke OtoXpert operator lain atau Shop&Drive, jangan masukkan seluruh kontribusinya sebagai GP Auto2000. Untuk OtoXpert berlabel Auto2000-operated, gunakan margin yang diakui operator dan pembagian aktual, bukan asumsi sama dengan general workshop.

Misalkan B adalah tambahan pekerjaan yang sungguh direbut dari luar Auto2000, E pekerjaan baseline yang menerima insentif meskipun sebenarnya tetap datang, D pekerjaan lain yang tergeser oleh keterbatasan kapasitas, g GP per pekerjaan tambahan sebelum insentif/operasional tambahan, g0 GP pekerjaan yang tergeser, c biaya tambahan per pekerjaan yang menerima penawaran, dan F biaya tetap intervensi.

Jika B dan E sama-sama menerima biaya c:

Delta kontribusi = B(g-c) - Ec - Dg0 - F.

Intervensi hanya layak secara kontribusi jika g>c dan B > (F+Ec+Dg0)/(g-c). Jika g<=c, penambahan volume tidak menyelamatkan desain tersebut dalam model ini. Jangan mensubsidi pickup atau diskon ke seluruh catchment hanya karena beberapa origin memiliki ketertinggalan akses.

Untuk layanan pickup terbatas ke kantong akses tertentu, maksimum biaya tambahan per pekerjaan yang ditawarkan adalah:

c_max = (Bg - Dg0 - F)/(B+E).

Ini batas pemilihan desain, bukan estimasi biaya pickup aktual. Masukkan biaya driver, repositioning, bahan bakar/tol dan administrasi pada c, bukan hanya jarak mobil pelanggan. Untuk THS, masukkan waktu teknisi dan waktu menuju pekerjaan berikutnya. Pilih pekerjaan yang benar-benar sesuai peralatan dan ruang kerja.

## Perbandingan keputusan

- **Kepastian slot dan persetujuan pekerjaan:** biaya komunikasi/alur kerja terutama masuk F dan administrasi c; tidak perlu subsidi perjalanan universal. Cocok untuk cabang dengan akses relatif sudah kompetitif.
- **Pickup/return:** menghilangkan perjalanan pelanggan tetapi menambah biaya operator. Batasi ke origin dan pekerjaan yang ditargetkan; gunakan batas c_max. Jangan hitung waktu pelanggan yang dihemat sebagai GP Auto2000.
- **THS:** untuk tugas rutin yang dapat dijalankan di lokasi dan setelah kecocokan pekerjaan ditetapkan. Tidak otomatis cocok untuk pembongkaran rem, diagnosis baterai tegangan tinggi atau klaim garansi.
- **Diskon menyeluruh:** E dapat besar karena pekerjaan baseline juga menerima diskon. Jika tidak ada bukti tambahan B, rancangan ini kalah dari penawaran tersasar dengan biaya sama.
- **Cabang baru:** menambah F besar; data akses yang sudah hampir setara tidak memberi dasar untuk mendahulukannya dibanding perbaikan penyelesaian layanan. Ini alasan prioritas, bukan pernyataan bahwa investasi fisik pasti tidak layak.

Pisahkan eksperimen customer-paid petrol dari HHC gratis, servis dalam entitlement, reimbursement warranty dan recall. Klaim warranty yang selesai dapat meningkatkan pengalaman kepemilikan tanpa menciptakan GP customer-paid setara pekerjaan bensin.

`economics.py` menyediakan fungsi dan tabel sensitivitas yang dinormalisasi terhadap g. Tidak ada biaya, margin, kenaikan konversi atau kapasitas Auto2000 yang diisi secara rekaan.
