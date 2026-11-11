# Release readiness check

Local read-only check, apart from this receipt. No new data, network, archive build, report edit, PDF edit or context edit.

Frozen PDF SHA-256: `e46506c9ecce3bf316f844de0700f64b20e8a8605f97316d177a3dc9c94861d1`. All 27 expected final artifacts exist and are nonempty. Explicit local links in READ_FIRST, DATA_GUIDE and REPRODUCIBILITY resolve. The structural site SQLite database passes integrity_check and has no full-HTML or review-text column.

## Archive scope

The archive script includes both historical ZIPs and the current report/context/data tree. It excludes private caches, rendered QA pages, installation caches, live SQLite and WAL/SHM files. A coherent SQLite snapshot replaces the live DB path. The current image candidates are analytical figures; no private screenshot or named original uploaded document is selected.

Final mode retains the two licensed IGAR CSVs and five MAT bundles. Public mode excludes those two IGAR text files. Public-core mode also omits MATs for separate volumes. Source manifests and the public-variant README explain these differences.

## Historical ZIP verification

- Auto2000_Public_Research_Initial_2026.zip: 192,138 bytes; SHA-256 `3c7acc5dee5279e771fccccb323690eb869c1a743b2c0ed520b6318c536c4c80`. Expected hash and outer copy match; ZIP CRC check passes.
- Auto2000_Expanded_Research_Plan_v2.zip: 303,520 bytes; SHA-256 `f5c994ae49661b32ca25618583972e0a0bd891e3f0358785b00c705ae5ea789f`. Expected hash and outer copy match; ZIP CRC check passes.

## Finalization boundary

The existing primary Full ZIP was an older 82,856,836-byte file without the final PDF member. Root confirms it will be rebuilt before delivery. The existing public Core ZIP contains the frozen PDF. Final archive manifests, archive checksums and actual backup/upload receipts remain root-owned.

The script selection simulated 589 full-release files, 587 public files and 582 public-core files before this receipt and later finalization records. These are input candidates, not final archive-member certifications.

No missing build-input artifact was found. Root subsequently confirmed backup receipts and configuration/execution reconciliation; those later updates were not independently rechecked here. This receipt certifies local readiness for the archive build, not delivery or hosting.
