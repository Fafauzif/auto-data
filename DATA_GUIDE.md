# Data guide and evidence units

**Count source units before counting cells, labels or derived features.** Rows from different workstreams cannot be added into a customer total. This guide describes the research frozen on 11 November 2026; it does not assert a complete planned crawl, representative samples or causal internal Auto2000 KPIs.

## Directory map

| Location | Use |
|---|---|
| `output/pdf/` and `context/` | Readable expanded findings PDF and the comprehensive updated master AI context. |
| `reports/` | First-wave Word reports, extension synthesis, sixteen insight cards, 27-concept solution menu, 45-draft review, initial hypotheses and separate first-wave/extension QA. |
| `figures/` | Original synthesis charts for the observed financing example, published service survey and coordinate crosscheck. |
| `workstreams/site/` and `data/site_evidence.sqlite` | Final site observation exports, family counts, extraction/version checks and structural database. |
| `workstreams/journeys/` | Twelve initial desktop task cells, seven focused follow-up cells, ten displayed finance scenarios and the inspected T-CARE cost rows. |
| `workstreams/reviews/` | Derived public-app review records, AI coding, summaries, source-access evidence and collection recipes. |
| `workstreams/narratives/` | Discovery/fresh-source annotations, source registers, bibliography, codebook, challenge protocol and findings. |
| `workstreams/market/`, `competition/` | Public terms, evidence/source registers, survey extraction, alternatives and economic calculations. |
| `workstreams/friend_challenge/`, `friend_capabilities/`, `friend_surveys/`, `friend_insurance/` | Supplied-context challenge, corporate capability checks, survey-denominator audit and insurance/obligation checks. |
| `workstreams/datasets/` | Dataset-derived CSV/JSON, analysis scripts, grain checks, figures and source-specific limitations. |
| `workstreams/extension_*` | Additional review, geography, journey, economics, stakeholder, hypothesis and battery analyses. These qualify rather than overwrite the first wave. |
| `workstreams/release_methods/` | Raw-file hash checker/stager, review source metadata, prior-archive checks and release-method notes. |
| `raw_licensed_data/` | Separately attributed raw source datasets and BPS table objects, with a file-level manifest. |
| `previous_releases/` | The two earlier ZIPs, preserved unchanged. These are historical plans/releases, not new observations. |

## Dataset grain and counting rules

### IGAR: large auxiliary raw corpus

`raw_licensed_data/IGAR_CC_BY_4_0/Rating_labeled.csv` and `VADER_labeled.csv` are exact source downloads under **CC BY 4.0**. Each contains **617,722 rows** covering historical government/public-service apps, dated May 2012–March 2023. Their 2025 dataset release date does not make those reviews contemporary.

These are **two label views of the same records**. A join on six shared fields finds **617,703 distinct composite keys** and **19 duplicate excess rows per view**. A composite key is not a verified person or universally unique source identifier. The matching analysis preserves duplicate ordinals rather than multiplying duplicate matches.

The rating file has eight column positions, including its unnamed source index; the VADER file has twelve. Across the two files this gives **20 raw column positions and 12,354,440 row-by-column slots**, approximately **12.35 million cells**. Many fields repeat between views; cells can be missing. This is a storage-shape count, not 12.35 million independent facts, reviews or people.

Use `workstreams/datasets/igar_analysis_summary.json`, `igar_conditional_analysis.json` and the corresponding disagreement CSVs for results. The nontext `IGAR_AUXILIARY_nontext_features.csv.gz` is a derived view of the same corpus, not another sample. Neither star-derived labels nor source VADER labels are human ground truth; their **255,414 disagreements / 617,722 aligned rows = 41.35%** is disagreement, not measured accuracy. This corpus does not expand the current Auto2000 customer evidence.

Source citation, hashes and field screening are in [raw_licensed_data/README.md](raw_licensed_data/README.md), `DATASET_SOURCE_MANIFEST.json` and `IGAR_RAW_SCHEMA_AND_PATTERN_SCREEN.json`. Exact raw text is preserved under the source license; a limited pattern screen is not a guarantee that free text contains no personal self-disclosures.

### Charging and vehicle context

| Dataset | Grain | Limits and main files |
|---|---|---|
| SPKLU V2 | **2,454 author-consolidated station rows**, **3,767 charger-box rows**, joined by station ID | June 2026 source snapshot; CC BY-NC 3.0. Raw source files and dictionary are in `raw_licensed_data/SPKLU_CC_BY_NC_3_0/`. Station, box, charger-unit and connector counts are different levels. No verified live uptime, access or simultaneous capacity. |
| Geographic calculations | **6,019,662 directed station-pair distances** computed from 2,454 × 2,453 | Derived straight-line comparisons, not new observations or driving times. Full matrix discarded. See `spklu_analysis_summary.json`, `auto2000_charging_context.csv` and summary outputs. |
| Coordinate challenge | Five targeted branch crosschecks and a labeled sensitivity scenario | One material conflict of about 55.3 km; scenario is not corrected ground truth. See `five_branch_coordinate_crosscheck.csv`, `auto2000_geo_sensitivity.csv` and `geo_sensitivity_summary.json`. Raw coordinates remain unchanged. |
| BPS/Polri stock | **1,285 numeric province/year/vehicle-type cells**, seven yearly tables for 2019–2025 | Includes national totals; all registered vehicles, not active BEVs or Auto2000 customers. See `bps_vehicle_stock_long.csv` and `bps_metadata.json`. Raw appendix contains decoded table objects with unchanged numbers, not byte-identical website HTML. |
| Market tables | Selected source-transcribed 2025 category/model/brand values and 72 Jan–Sep 2026 category cells | Definitions and graphic/narrative conflicts remain explicit. Read `DATASETS_REPORT.md` and `market_analysis_summary.json`; do not silently substitute differently scoped casebook figures. |

CASA is a separate historical automotive product-review calibration benchmark, not Digiroom task evidence. Derived calibration is included; raw review text is excluded because upstream text rights were not established from conflicting repository/card license signals. The SPKLU noncommercial license does not grant unrestricted commercial deployment rights. No blanket license applies to every file in this archive.

### Direct public customer evidence

| Family | Source units | Files and interpretation |
|---|---|---|
| First-wave app reviews | **210 unique platform review IDs, six apps, 12 app/platform/language cohorts** | `workstreams/reviews/reviews_derived.csv`, `manual_audit.csv`, `review_summary.json`. Store-selected convenience records, not representative samples. Storefront/locale does not verify residence. Historical cohorts do not diagnose the current build. |
| Additional app reviews | **148 new unique IDs from nine additional listing cohorts**, with no overlap against the first 210; **358 combined IDs** | `workstreams/extension_reviews/new_reviews_derived.csv`, source capture index, codebook fields and extension report. New automotive contexts include passenger cars and explicitly separated motorcycle/unknown records. |
| Review provenance | Metadata for the **same 210 IDs**, linked to 12 public page captures | `workstreams/release_methods/review_source_records_nontext.csv` and `review_source_capture_index.csv`. Metadata, coding and repeat checks add zero reviews. Text/source-body hashes permit matching, not reconstruction of omitted text. |
| Narratives | **75 discovery + 20 fresh-source annotations = 95 units**, across **38 distinct source URLs** | `narrative_units.jsonl/.csv`, `validation_units.jsonl/.csv`, source tables and `BIBLIOGRAPHY.md`. Reports, questions, advice, employees and study findings have different roles. Multiple units share threads/accounts; not 95 independent people. |

All first-wave 210 app records were inspected/coded by an AI researcher, with 30 targeted, nonblind second-AI checks. All additional 148 received source-grounded AI coding, with a separate targeted, nonblind 16-record second-AI check. Those checks inspect subsets of the same records; they add no reviews. No human reliability coefficient or independent verification of customer truth exists. `self_reported_app_job` means a specific claimed interaction, not a verified completed service or sale. Ratings, lexical mentions, app-job eligibility and reported outcomes are separate fields. Full current review text, author handles and developer-reply text are excluded from the public evidence exports.

Narrative follow-up targets were frozen before new-source search, but this is a purposive rival search rather than a probability sample or formal causal validation. YouTube watch-page/caption metadata was probed; **zero transcripts were captured**. No bulk transcript or API-comment corpus should be inferred from the collection recipes.

### Website and journey observations

The site sample froze at **345 requested URL records**, with **281 successful raw-HTML responses**. The enlarged queue was interrupted; it was not completed. The successful pages were reprocessed to the final extraction version. See `workstreams/site/page_observations.csv`, `summary.json`, final comparison checks and the packaged structural SQLite database. Earlier extraction versions and QA are history, not extra pages.

The database represents source structure, links and extracted flags. Currency mentions are not reconciled current offers; HTTP success does not establish rendered task success, indexability, customer demand or revenue. Cached full HTML/PDF source bodies and search-index text are excluded. Consequently, an offline reparse requiring those private bodies is not supported solely by the public database.

The UX/JX journey cells are logged-out desktop evaluator observations, not recruited participant tests. Ten finance scenarios are displayed calculator outputs, not ten customers or lender contracts. The T-CARE rows retain the displayed March 2024 estimate basis. No private account, VIN or registration data was supplied to test downstream outcomes. Mobile/native-app behavior and actual branch fulfillment remain unobserved.

The extension adds eight registered checks, including seven live desktop UI groups and one device-capability group, five BEV finance illustrations, 22 further service-estimate rows and a 13-URL registry. Local headless Chromium failed before navigation; the cloud browser lacked device controls and its native DevTools was explicitly blocked. Android emulator tools were absent. These are runtime capability findings, not mobile-product failures. No mobile or native-app execution is claimed.

## Expanded analysis and auxiliary telemetry

The five exact published MAT bundles in `raw_licensed_data/EV_TELEMETRY_CC_BY_NC_3_0/` contain **56,507,201 stored current, voltage, state-of-charge and temperature values**. Separately, they contain **56,599,111 clock values** and **91,910 epoch values**. Do not add clocks to signal counts or treat asynchronous values as synchronized rows. The producer already reduced cardinality; stored values are not independent physical measurements. They describe **one historical Audi e-tron in California**, not five vehicles, five trips, Toyota owners or an Indonesian sample.

The five MAT payloads total **283,141,466 bytes**; adding the exact source README gives **283,242,120 source-payload bytes**. The separate telemetry source manifest covers those files. The earlier 17-entry IGAR/SPKLU/BPS manifest and its receipt remain unchanged as a first-wave record. A full archive manifest lists every file actually delivered. The telemetry source uses **CC BY-NC 3.0** and requires attribution and the noncommercial qualification. Absolute epoch data remain present; the ten inspected numeric fields contain no detected GPS, VIN, owner or contact fields. This is a field screen, not an anonymity certification. The withheld capacity reference is proprietary and BMS-derived; it is not an established independent laboratory ground-truth series.

Read `workstreams/extension_battery/BATTERY_TELEMETRY_REPORT.md`, `BATTERY_SUMMARY.json`, its seven CSV tables and `verify.py`. Current and voltage clocks align in all five bundles; SOC clocks align in two and temperature clocks in none. The 106 segments under a 30-second gap rule are not verified trips. Public reference capacity is missing, so throughput and partial SOC slopes do not establish usable capacity, SOH or certificate accuracy.

The geography extension preserves original coordinates and adds 25 scenarios, 695 anchor-scenario rows, candidate-proxy filters, point-cluster tests and explicit Papua boundary pooling. These are repeated calculations on the same 2,454 source sites. The economics extension supplies 14 commercial mechanisms, dated programme comparisons and constructed risk states; scenarios are not observed claims or forecasts. The stakeholder extension has 26 analytical job units across ten grouped decision-owner roles, plus 18 finer stakeholder lenses. Its 260 matrix cells are an organizing device. The seven external mechanism sources include studies and an instrument; their published participant or listing counts are not newly acquired project rows.

Primary versus public-backup inclusion is explained in `README_PUBLIC_MIRROR.md`. In particular, the public copy omits original IGAR free text and retains the nontext derivative. When a host needs smaller files, the core archive and five complete-MAT telemetry ZIP volumes extract into the same project directory. Those volumes do not restore the omitted IGAR text.

## Trace a conclusion to its source

Start with an insight's evidence references in [INSIGHT_BOOK.json](reports/INSIGHT_BOOK.json). Its `evidence_index` resolves each reference to a relative file, exact record selector, normal source URL and locator. The solution menu supplies its own evidence locators. Keep namespaces: `capabilities:FC01` differs from friend-challenge group `FC01`.

The 40 friend groups/148 scoped subclauses are analytical coverage, not 148 studies or confirmed effects. The original 25 hypotheses retain their wording, rivals and unresolved business mechanisms in `reports/hypothesis_assessment.*`. Operator publications, survey cells, unverified accounts, evaluator observations, auxiliary records and constructed examples must retain their distinct evidentiary status. Repeated pages or workstreams describing the same issuer do not create independent corroboration.

## Reproduce only the supported layer

Read [REPRODUCIBILITY.md](reports/REPRODUCIBILITY.md) and [REPRODUCE_DATASETS.md](workstreams/datasets/REPRODUCE_DATASETS.md) before executing scripts. Included raw files can be hash-checked and staged offline; many arithmetic tables and authored views can be regenerated from packaged inputs. Inspect dependencies and paths first, and preserve an unchanged release copy because build scripts write outputs.

Full live-source reacquisition depends on current access rules, markup, available records and private captures that are deliberately not redistributed. The archive is not a tested one-click environment or a guarantee of identical future web results. Current public publications cannot supply the missing internal delivery, work-order, claim, adoption, retention or realized-profit KPIs. These limits leave user choice open rather than establishing a final strategy.
