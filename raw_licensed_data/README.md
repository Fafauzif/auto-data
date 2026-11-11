# Raw external datasets and source table payloads

This folder is an explicitly requested raw-data appendix. The external datasets are not Auto2000 customer data. License terms differ by subfolder; no single blanket project license applies.

## IGAR_CC_BY_4_0

Isnan, M., & Pardamean, B. (2025). *IGAR: Indonesian Government App Review Dataset* (Version 2). Mendeley Data. https://doi.org/10.17632/7zryc6k76z.2 . Source license: Creative Commons Attribution 4.0, https://creativecommons.org/licenses/by/4.0/ .

`Rating_labeled.csv` and `VADER_labeled.csv` are exact unmodified source downloads with verified SHA256. They contain two label views of the same 617,722 records, not 1,235,444 independent reviews. Matching six shared fields finds 617,703 distinct composite record keys and 19 exact duplicate excess records per view. The source timestamps span 11 May 2012 through 26 March 2023. The six applications are government/public-service apps, not Digiroom. This corpus supports an auxiliary labeling-method stress test, not current automotive customer conclusions.

The source columns include app name, review content, translated content, star rating, review timestamp, app version, and algorithmic/rating-derived label fields. No separate reviewer username or handle column occurs. Raw text remains unmodified and can contain users' self-disclosures. `IGAR_RAW_SCHEMA_AND_PATTERN_SCREEN.json` reports limited pattern-screen results; it is not a certification that text contains no personal information. Derived public feature tables outside this folder omit raw text, translations and exact timestamps.

Neither source labeling method is human ground truth. Disagreement does not establish which label is correct.

## SPKLU_CC_BY_NC_3_0

Wiputra, R., & Santiadi, S. (2026). *A Geospatial Dataset of Public Electric Vehicle Charging Infrastructure in Indonesia* (Version 2). Mendeley Data. https://doi.org/10.17632/z2bvd5r574.2 . Source license: Creative Commons Attribution-NonCommercial 3.0, https://creativecommons.org/licenses/by-nc/3.0/ . Use the source and derivatives within that noncommercial license; this package does not grant commercial deployment rights.

Exact source file bytes are preserved. The author's consolidated station table has 2,454 records and the charger-box table 3,767 rows. A snapshot captured 16 June 2026 underlies the release. The original source README, processing log and dictionary describe the unit definitions, deduplication, provider keyword classification, 34-province geography and inference limits. Current live access, physical equipment, simultaneous capacity and charger uptime were not independently verified.

Our analysis separately preserves a material coordinate disagreement for one of five branch crosschecks. Source coordinates in this raw folder have not been overwritten; revised coordinates appear only in a labeled sensitivity scenario.

## BPS_extracted_public_table_payloads

These JSON files contain the original official public table objects decoded from BPS website React Server Component payloads and serialized for inspection. Numeric cells are unchanged, but JSON formatting is transformed; these are not byte-identical original HTML files. The source covers registered motor vehicles by province/type, 2019–2025. Source agency is the Indonesian National Police, distributed by BPS. Source metadata and footnotes remain with each year. No unrestricted license over all BPS wording is asserted. Use the tables with attribution and retain definition/coverage notes.

BPS table origin: https://www.bps.go.id/en/statistics-table/3/VjJ3NGRGa3dkRk5MTlU1bVNFOTVVbmQyVURSTVFUMDkjMyMwMDAw/jumlah-kendaraan-bermotor-menurut-provinsi-dan-jenis-kendaraan--unit-.html?year=2025 . Change the year query for other years. New Papua province values remain pooled under older parent geographies according to the source footnotes. A large East Java series discontinuity makes simple growth inference unsafe.

`DATASET_SOURCE_MANIFEST.json` records paths, sizes, hashes, source identity, licenses and whether bytes are exact or transformed. Source acquisition logs and analysis scripts are in `workstreams/datasets/` in the main package.


## Additional licensed EV telemetry

EV_TELEMETRY_CC_BY_NC_3_0 contains five exact published MAT bundles and the source README from Allam et al. (2023), Real-world electric vehicle data: driving and charging, Mendeley Data V2, https://doi.org/10.17632/7vdkzpnjgj.2, CC BY-NC 3.0. Its own SOURCE_FILE_MANIFEST.json covers the new source bytes. The original 17-entry manifest remains a first-wave record. See workstreams/extension_battery for the numeric-field privacy screen, asynchronous signal units, withheld BMS reference and reproducible analysis. These are auxiliary data from one historical Audi in California, not Toyota/Indonesia customers.
