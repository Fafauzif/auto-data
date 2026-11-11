# External datasets: findings, counterevidence and strategic implications

Research run: 11 November 2026. The numbers below come from actual downloaded files, inspected schemas and executed calculations. These are contextual and auxiliary datasets, not internal Auto2000 funnel or profit data. Source bytes, parsed tables and computed features have different grains and are counted separately.

## What was actually obtained

| Evidence family | Actual acquired unit and count | Source and release handling |
|---|---|---|
| BPS/Polri registered vehicles | 7 yearly public tables, 2019–2025; 1,285 province/year/vehicle-type numeric cells | Public BPS table payloads decoded from website RSC; original numeric values and metadata retained. Province coverage changes from 35 rows including national total to 39. |
| Indonesian SPKLU | 2,454 author-consolidated station records, 44 columns; 3,767 distinct charger-box IDs; 3 reference tables | Wiputra & Santiadi, Mendeley V2, DOI 10.17632/z2bvd5r574.2; snapshot 16 June 2026; CC BY-NC 3.0. Exact source hashes verified. |
| GAIKINDO market | 2025 category 8 rows; 2026 Jan–Sep category 72 cells; selected 2025 brand/model tables | Numeric graphics manually transcribed and visually checked against actual downloaded images. Public narrative data separately parsed; image-vs-text conflicts retained. No copyrighted full graphics in public report folder. |
| CASA automotive sentiment benchmark | Train 810, validation 90, test 180 product-review records | IndoNLU source files actually downloaded. Raw GitHub LICENSE is Apache 2.0; HF card says MIT. Upstream review licensing not assumed, so raw review text excluded from release; derived calibration retained. |
| IGAR auxiliary labeling stress test | Two label views of 617,722 rows each; 617,703 distinct six-field composite record keys | Isnan & Pardamean, Mendeley V2, DOI 10.17632/7zryc6k76z.2, CC BY 4.0. Timestamps 2012–2023, not contemporary Auto2000 reviews. Exact source hashes verified. |

Raw licensed source data are staged separately under `raw_licensed_data/`; paired label views must never be counted as 1.2 million independent experiences. The 6,019,662 station-to-station distance calculations are derived computations, not 6 million source observations; the matrix was discarded and only useful summaries retained.

## Finding 1: a charging directory must resolve access and data trust before it can claim a differentiated customer benefit

The SPKLU source classifier assigns 15 station records to `operator_brand=Auto2000`. Reviewing the actual station-name field finds 28 Auto2000-named records: the other 13 are classified under Toyota and explicitly include a Toyota/Lexus restriction marker in their names. Therefore, a brand-field filter alone undercounts this observed name subset. Conversely, nearby stations cannot automatically be treated as usable alternatives because brand restrictions, opening hours, compatible connectors, payment, queues and uptime remain unverified.

Our independent haversine calculation finds another non-Auto2000-named mapped site within 5 km for 27 of those 28 records; median nearest straight-line distance is 0.323 km. These are registry-based proximity results, not drive times or adequate capacity. The useful opportunity to test is eligibility-aware, trustworthy information in a transaction or ownership task. A generic map icon alone has no established novelty, incremental engagement or profit effect.

### Five-branch source crosscheck and sensitivity

Five current official Auto2000 direction links were independently retrieved by the parent research process and compared against source coordinates. Four locations agree within 0.135 km. Auto2000 Balikpapan Sudirman has a 55.258 km disagreement between source coordinates and the current official branch direction. This is a material source conflict, not field-confirmed ground truth. Source files were not edited.

In a sensitivity scenario that substitutes only those five branch direction coordinates, the Balikpapan record's nearest other mapped station changes from 18.481 km to 0.081 km, and the 28-record subset changes from 27/28 to 28/28 with another mapped site within 5 km. This shows why a precise map calculation can produce a false scarcity signal when its input coordinates are not verified. The source's broad provincial bounding-box screen did not establish city-level positional accuracy.

**Counterevidence and limit:** a nearby listed charger may be inaccessible, restricted, unavailable or insufficient. Current official branch directions can also differ from an actual charger location or reflect a move afterJune 2026. We have not verified physical hardware, power delivery or public access. This evidence supports an integration/verification requirement, not a claim that charging anxiety is solved.

**Artifacts:** `auto2000_charging_context.csv`, `five_branch_coordinate_crosscheck.csv`, `auto2000_geo_sensitivity.csv`, `geo_sensitivity_summary.json`, `site_branch_identity_probe.json`.

## Finding 2: fleet, sales, population and EV denominators lead to different decisions

BPS's 2025 national passenger-car register is 20,907,972 units. This is all registered passenger cars, not BEVs, active roadworthy vehicles, Toyota owners, Auto2000 customers or service-eligible jobs. The 2026 charging snapshot has 497 consolidated records inDKI Jakarta,437 inJawa Barat and 226 inBanten. Dividing by 2025 registered passenger vehicles produces 21.27,14.66 and 21.19 sites per 100,000 respectively. These ratios describe contextual density, not EV adequacy.

A province with a small passenger-car base can rank high on this ratio despite few absolute sites. That does not overturn a population-based inequity finding: they answer different questions. One denominator should not be chosen merely because it makes a preferred location appear underserved. Future prioritization needs reachable Toyota/BEV demand, actual usability and economics.

The source's 2019–2025 series contains a conspicuous East Java passenger-stock jump from 2,039,556 in 2022 to 5,439,502 in 2023. Provincial sums reconcile to national totals, so this is not a parser summation error. Its cause remains unresolved. We do not interpret this as organic demand growth. BPS notes also keep newer Papua provinces pooled under older parents; the charging dataset uses 34-province geography. Join coverage is explicitly recorded, not hidden.

**Strategic implication to test:** ownership services should follow the installed customer's vehicle/job context, while sales acquisition should follow current competitive offers. National EV new-sales mix cannot stand in for workshop exposure.

**Artifacts:** `bps_vehicle_stock_long.csv`, `bps_metadata.json`, `province_charging_vs_registered_cars.csv`, `charging_count_vs_vehicle_context.png`.

## Finding 3: Toyota's reported hybrid exposure is concentrated, so one generic EV persona can misallocate attention

The GAIKINDO-hosted hybrid article reports 30,110 Toyota hybrid wholesales in 2025 and 23,934 Innova Zenix hybrids. The resulting concentration is 79.49% within the reported Toyota hybrid total. Adding the reported Yaris Cross and Alphard hybrid models brings the three-model share to 97.03%. This is materially different from treating all Indonesian electrified buyers as homogeneous BEV shoppers.

**Boundary:** the page republishes Detik using GAIKINDO figures and includes mild-hybrid Suzuki models in the overall hybrid category. It is not a verified uniform technical HEV-only table. It does not reveal Auto2000's model mix, margins or owners. Preserve the casebook's estimates for competition arithmetic and identify this source as external context.

**Strategic direction to test:** investigate an ownership and replacement proposition tailored to hybrid vehicle/job cohorts alongside a separateBEV purchase-confidence proposition. First verify actual customer mix and existing Toyota service entitlements. The data do not establish which intervention wins or justify a precise ROI.

The 2025 official category graphic totals 803,687 units exactly. The 72 manually transcribed 2026 category cells sum 679,202, whereas GAIKINDO's narrative forJanuary–September states 679,020, a 182-unit difference. The latter is the explicitly stated narrative baseline; the chart table is preserved as an unresolved source/version conflict and not used to claim a reconciled national time series. Do not silently alter chart cells to force the aggregate.

**Artifacts:** `gaikindo_2025_category_derived.csv`, `gaikindo_2026_monthly_category_derived.csv`, `gaikindo_2026_monthly_totals_derived.csv`, `gaikindo_2025_hybrid_selected_models.csv`, `market_analysis_summary.json`.

## Finding 4: labeling choices can change the apparent customer story even when the records are identical

We downloaded bothIGAR label views and matched on app, original content, rating, timestamp, app version and translation, rather than assuming row order. The 617,722 rows align completely, with 617,703 distinct composite keys and 19 duplicate excess records per view. Source timestamps span 11 May 2012–26 March 2023. These are six Indonesian government/public-service applications, not Digiroom, and their age rules out using them as current automotive customer evidence.

Rating-derived and source VADER labels differ on 255,414/617,722 rows, or 41.35%. App-specific disagreement ranges from 32.46% forJMO to 50.63% forMyPertamina. Similar aggregate positive shares can conceal substantial record-level disagreement. Neither label view is human ground truth, so these rates are disagreement, not error, accuracy or validation of either method. Missing translations occur in 7,775 rows and missing original content in 26.

**Method consequence:** do not convert automated sentiment totals into customer root causes. The Auto2000 corpus needs task-level codes, chronology/version checks, manually reviewed examples and competing explanations. External labeled data can calibrate an instrument; it cannot replace current-domain validation.

**Raw-data handling:** the source has no separate reviewer-handle field, but free text is preserved in the explicitly requested raw appendix and can include self-disclosures. The separately published feature table omits original/translated text, exact timestamps and handles, uses pseudonymous IDs, and marks every row `AUXILIARY_NOT_AUTO 2000`. Pattern-screen counts are documented, not presented as proof of complete anonymization.

**Artifacts:** `IGAR_AUXILIARY_nontext_features.csv.gz`, `igar_label_agreement_crosstab.csv`, `igar_label_agreement_by_app.csv`, `igar_analysis_summary.json`, `igar_label_disagreement.png`.

## Finding 5: a small task-specific baseline can outperform generic sentiment shortcuts, but that is not a business validation

CASA contains six aspect labels: fuel, machine, others, part, price and service. An all-neutral baseline reaches 86.67% accuracy on both price and service test labels while finding no positive/negative cases. We evaluated a fixedTFIDF 1–2 gram logistic model trained only on 808 cleaned training texts after excluding one within-train duplicate and a train/test text overlap. No hyperparameter selection used test labels.

On 180 source test records, macroF 1 is 0.860 forprice and 0.835 forservice; the broaderothers aspect is 0.602. These are source-benchmark scores with supplied aspect labels, not current Digiroom performance. Actual downloaded testCSV contains labels despite the repository's generic masked-label statement. The validation sample includes a motorcycle review, reinforcing that these are mixed vehicle-product discussions rather than a clean current four-wheel app corpus.

**Counterevidence:** strong benchmark metrics do not establish reliable causal, complaint or intent extraction on slang, mixed-language Digiroom reviews. Use current reviewed examples before any deployment. Rating-based labels and VADER labels remain weak supervision, not human ground truth.

**Artifacts:** `casa_label_distribution.csv`, `casa_baseline_metrics.csv`, `casa_calibration.json`, `casa_calibrate.py`.

## Hypotheses and what would change the direction

| Working hypothesis | What this work supports | Strong rival or rejection condition | Next decision/test |
|---|---|---|---|
| Verified access/context matters more than another generic charging map | Registry classification and one material coordinate conflict change inferred coverage | Owner interviews/journeys show discovery is the dominant unmet need and existing verified routes are hard to find | Compare current map and partner-routing tasks, verify station terms, then test a minimum information improvement |
| Hybrid ownership andBEV shopping need different propositions | Reported Toyota hybrid concentration and distinct installed-base vs new-sales denominators | Actual Auto2000 mix/profit indicates a different cohort dominates reachable opportunity | Join vehicle cohorts, due jobs and realizedGP before selecting a pilot |
| Information trust deserves an operational owner | Dataset source discrepancies and coordinate/QC failures survive superficial technical checks | Issues are confined to unrelated external data with no customer-facing consequences | Trace actual source-of-truth ownership and measure customer task consequences, without attributing external errors toDigiroom |
| Automated sentiment alone can distort priorities | Two labels on the same auxiliary corpus disagree 41.35%; neutral baseline can look accurate | Current-domain manual coding shows stable task-level extraction and valid outcome links | Use a reviewed codebook, counterexamples, held-out validation and outcome measures |

## Limits and unavailable inputs

No CRM funnel, attribution, current private app logs, dealer reimbursement, actual technician capacity, lender approvals or EV-specific margins were obtained. No causal uplift is proven. GAIKINDO's public file index links lead to an account-gated file portal, so underlying bulkPDFs were not downloaded; public graphics and narratives are bounded alternatives. No account, paid endpoint, captcha bypass or private user document was used in these dataset acquisitions.

Acquisition logs record source URLs, statuses, retrieval time, input hashes and failures. Source files live in private cache and explicitly requested licensed rawdata appendix. Third-party source licenses remain separate from the project's original analysis.
