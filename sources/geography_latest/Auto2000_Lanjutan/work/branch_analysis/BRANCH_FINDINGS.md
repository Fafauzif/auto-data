# Keputusan cabang dari penghitungan ulang OD mentah

## Metode singkat dan perubahan

Seluruh27destinasi Auto2000 dihitung ulang dari76.221OD utama dan5.913OD tambahan, bukan dengan menerima ringkasan sebelumnya sebagai input. Dua endpoint hasil koreksi sumber publik, Suci danSidoarjo, menambah162OD outbound. Versi baseline27tetap utuh; keputusan memakai versi29endpoint. Skenario utama memakai snap keduaendpoint<=250meter. Origin berpasangan sama:59Surabaya,78Medan,78Bandung,69Palembang. Cabang dengan0origin tetap dicatat, tidak diartikan tutup atau tanpa pelanggan.

Kanal dibedakan Auto2000 general; OtoXpert Auto2000-operated; OtoXpert operatorlain; Shop&Drive; DokterMobil; authorisedToyota lain; kandidatgenerik. 'Jaringan oli' adalah OtoXpert+Shop&Drive sebagai offeringnetwork. 'Jaringan milikoperator Auto2000' adalah generalAuto2000+OtoXpert berlabeloperatorAuto2000. OtoXpertlabel bukanangka GP; pekerjaan tetap memerlukanpayer/entitlement yang benar.

Job utama: oli+filterToyotaAvanza2019G1.3; comparator sama dipakai untuk pad depan karena bukti pemasangan kampas S&D terbaru melengkapi bukti brake OtoXpert. Sensitivitas front_brake_oto_only_sensitivity juga disertakan. Geografi dua job boleh sama; fulfilment berbeda: oli dapat masuk THS sesuai akses/lokasi, kampas frontaxle masuk bay denganpartfitment/slot/approval yang dikunci. Tidak dibuat premium harga terukur dari paket berbeda. Sumber jobroot:coordinates/job_protocols.csv dancoordinate_job_sources.csv.

## Temuan yang langsung mengubah pilihan

1. **Suci lebih dahulu daripada pickup Cibiru.** Koreksi koordinat menambah Suci sebagai cabang terdekat20origin. Median gapBandung terhadap jaringanoli turun2,635833→1,735833menit. Tail>5menit21→17. Cibiru22→14origin, gap2,744167→1,384167, tail4→1. Suci mengambil4originAsiaAfrika,8Setiabudi,8Cibiru. Soekarno-Hatta tidak kehilanganorigin. Maka perbaiki destination/branchrouter Suci; jangan gunakan catchmentCibiru lama untuk membenarkan pickupmassal.

2. **Dua catchmentSurabaya sama besar membutuhkan tindakan berlawanan.** A.Yani danKertajaya11origin masing-masing. Gapoli A.Yani−0,960menit, Kertajaya+2,133333. PadaKertajaya, memperbolehkan OtoXpertRungkut yang sudahAuto2000-operated menghapus seluruh3tail>5menit dan menyisakan median1,08menit. Pilih A.Yani untuk 'OliPastiSelesai' (konfirmasi, parts,scopeapproval, serahterima), Kertajaya untuk pilihan routingoliRungkut sebelum pelanggan berangkat. Pickupkedua wilayah atau tierbaru kalah.

3. **HotspotPalembang menyelesaikan dirinya dengan kanal yang sudah ada, bukan cerita jembatan.** GeneralAuto2000 memiliki9tail>5menit. Baselineassignment menempatkan8keTAA dan1keVeteran, Plaju0. Memperbolehkan OtoXpertPalembang Auto2000-operated membuat semua9menjadi<=5menit:7menjadi0karena OtoXpert sendiri alternatifterdekat;2tinggal1,005menit. TAAmedian3,615→0,366667. Pilih 'OliTepatKanalPalembang', bukan pickupPlaju atau pickupTAA universal lebihdulu.

4. **Medan adalah pemilihan penawaran/penyelesaian sebelum perluasanfisik.** Median gapgenerik4,085833→jaringanoli0,346667;32dari78origin tidaklebihlama keAuto2000. Pancing24origin, median+0,346667, tidakada tail>5, dan8origin kehilangan akses15menit bila Pancing dihilangkan. Pilih Pancing untuk slotconfirmed sampai serahterima. PadaGatot20origin, gap2,385833→0denganOtoXpertRingRoadMedan;pilih kanal ekonomis yangada, bukan tierbaru. Seluruh3tailMedan menjadi0tail sesudah routerowned-network.

5. **BandungSoekarno-Hatta adalah sisa kantong yang tidak hilang sesudah dua koreksi murah.** Cabang tetap21origin, gap4,248333;sesudahSuci+OtoXpert-owned masih8tail>5dari14tailBandung. Median gap owned3,435menit. Pilih 'SekaliDatangSoekarno-Hatta' pada8origin itu: cocokkanTHSoli diakses rumah atau tungguonsite satu kunjungan; rembay parts/slot/approvaldahulu. Memaksa semua keSuci atau OtoXpert tidakmenyelesaikan8tail.

6. **Tambahan cakupan20menit kecil tetapi penghematanPalembang nyata pada grid.** OwnOtoXpert menambah0,0,0,2origin<=20menit; pada10menit menambah2,3,3,4;15menit0,0,0,2;30menit0semua. Namun penghematan>3menit terjadi5,10,3,10origin;>5menit0,0,2,7. Palembang14origin memperolehperbaikan>1detik, medianpenghematanpositif5,3525menit. Jadi 'hanya menambah penawaran' terlalu kuat: umumnya dalam footprintlama, tetapi routing mengubah bebanperjalanan untuk sejumlahorigin.

7. **Overlap bukan alasan menutup atau mengalihkan semua pekerjaan.** Soreang5origin danMarelan7origin tampakkecil tetapi median cabangkedua4,368333 dan4,185menit lebihlama. Pancing melindungi8origin pada15menit. Pilihan yang kalah adalah sentralisasi berbasis jumlahorigin atau anggapan kapasitas kosong dari overlap. Keputusan yang dapat dibuat adalah menjaga keandalan slot/partsscope cabanglokal.

## Tie yang mengubah aritmetika headline

Palembangorigin g04_06 memiliki durationAuto2000 yang persis sama menujuTAA danVeteran, gapoli6,253333menit. Urutaninputbaseline memberiTAA25origin/8tail danVeteran25/1tail. Tie-breaklexicographic memberiTAA24/7tail danVeteran26/2tail. Gunakan7–8dari9tailterkaitTAA, bukan angka8tanpaaturan. Plaju0danpenghapusan seluruh9tail olehownedOtoXpert stabil terhadap tie. tie_allocation_bounds.csv memberi rentangassignment tanpa menyumupperbounds.

## Artefak

- all_27_branches_recomputed.csv:54baris baseline27cabang×2skenario.
- corrected/all_27_branches_recomputed.csv:58baris29endpoint×2skenario, dengan semua distribusi/operator/job/secondbranch/marginalthresholds.
- origin_channels_recomputed.csv dan corrected/:rawminima perorigin/skenario,operatorwinner,secondbranch,ownedgap/savings.
- owned_otoxpert_marginal.csv dan corrected/:threshold10/15/20/30 dan gain>1/3/5menit, sebelum/sesudah tail.
- branch_decision_table_29.csv:semua29endpoint bernama,intervensi,tujuan,segmen,alasan,alternatifkalah.
- shortlist_named_interventions.csv:7endpointprioritas yang dibedakan menuruttujuan, bukan compositescore.
- coordinate_before_after_origins.csv:origin yang dipindahkan endpointbarudanperubahannya.
- tie_allocation_bounds.csv:aturanassignment danrentangPalembang.

Nilai menit adalah durasimodelprofilOSRM, bukanobservasilalu lintas atau dampak layanan. Hitungoperasional dan pilihkanal tidakdikonversi menjadi permintaan,uplift,GP atau kapasitas yangtidaktersedia.
