# More reviews strengthen the measurement warning, not a brand ranking

(certain) The extension adds **148 unique automotive review records from nine permitted public Google Play listing pages**. They have no review-ID overlap with the frozen first 210. The combined context therefore contains **358 unique platform review IDs across 21 app/platform/language cohorts**. These are selected displayed records. They are not 358 verified customers, completed transactions or independent observations of service quality.

The new evidence makes three useful corrections. Favorable stars can accompany a specific constraint. A different language selection can expose a different time period as well as different ratings. A brand app can serve motorcycle parts or branch experiences that do not transfer directly to a Toyota passenger-car ownership question. None of these observations estimates representative complaint prevalence or an incremental business outcome.

## What was added and what stayed frozen

| Public listing cohort added | Indonesian-language records | English-language records | New unique records |
|---|---:|---:|---:|
| myHyundai Indonesia | 0 | 20 | 20 |
| MyWuling+ | 0 | 20 | 20 |
| My Mitsubishi Motors ID | 0 | 20 | 20 |
| Honda e-Care | 20 | 20 | 40 |
| My Suzuki | 20 | 20 | 40 |
| My Chery | 4 | 4 | 8 |
| **Extension total** | **44** | **104** | **148** |

All nine listing requests used the public listing URL with `gl=ID`. The requested language and storefront parameter do not verify a reviewer's residence, nationality or vehicle. All nine listing requests returned HTTP 200. They exposed 148 embedded review appearances, all with distinct IDs and none matching the first wave. My Chery exposed four records per language page; this does not mean the app has only eight reviews. Published listing counters and the retrieved text subset are different units.

The first-wave CSV and annotations remain unchanged. New IDs run from `ER-0001` to `ER-0148`, while old IDs retain the `REV-` namespace. `capture_relations.csv`, `source_capture_index.csv` and `validation.json` reconcile appearances, IDs, capture hashes and request IDs. Each released new record includes its public listing locator and platform review ID. Full source bodies and review text remain private. The public extension includes no reviewer names, handles, images, contact details, review titles or verbatim review excerpts.

## Test 1: favorable stars do not identify a completed app job

(certain) In the frozen Indonesian-language Digiroom Google Play subset, 16 of 20 displayed records have four or five stars. Only seven of those 16 describe a specific app interaction. Five are unknown and four explicitly concern another object or no experienced service job. Under the conservative coding rule, the app-interaction classification range is therefore **7/16 to 12/16**, depending on how all five unknown records are treated. This is a sensitivity range, not a confidence interval or a completion rate.

| Selected favorable subset | Favorable records | Specific app interaction | Unknown | Explicit non-app experience | App-interaction classification range |
|---|---:|---:|---:|---:|---:|
| Digiroom, original Indonesian Google Play | 16 | 7 | 5 | 4 | 43.8% to 75.0% |
| BYD, original Indonesian Google Play | 19 | 5 | 4 | 10 | 26.3% to 47.4% |
| Hyundai, new English Google Play | 12 | 4 | 8 | 0 | 33.3% to 100.0% |
| Chery, new English Google Play | 3 | 0 | 3 | 0 | 0% to 100.0% |

The last two rows demonstrate uncertainty rather than poor performance. Generic praise does not prove non-use, while a specific failed login or booking does qualify as an app-interaction report. No classification in this table establishes that the customer completed a service, bought a vehicle or received a part.

(certain) Among the 45 favorable records in the new extension, nine contain a specific constraint or failure report and seven are mixed accounts. Examples include a five-star Honda activation/booking difficulty (`ER-0074`, 2019), a five-star profile-color mismatch (`ER-0099`, 2023), and a five-star Suzuki pickup-versus-delivery constraint (`ER-0108`, 2026). These are counterexamples to treating a favorable rating as proof that every described task worked. They do not estimate the defect rate of any app.

The useful negative cases also remain visible. `ER-0095` reports quick Honda booking confirmation in 2019. `ER-0109` describes a positive Suzuki parts-purchase experience in 2026. A historical Digiroom account reports access recovering after an update (`REV-0130`). A diagnosis that every digital handoff fails would contradict these source accounts.

## Test 2: language selection changes the evidence frame

(certain) Across all nine apps with matched Indonesian/English Google Play selections, the displayed review-ID sets have zero overlap. This is a source-selection result. It does not establish that language caused satisfaction, that the reviewers belong to different countries, or that these are random samples.

| App and selected language pair | Four/five-star records: Indonesian / English | Records dated 2026: Indonesian / English | Source-wave context |
|---|---:|---:|---|
| BYD | 19/20 / 3/20 | 12/20 / 19/20 | Both original |
| Honda e-Care | 2/20 / 4/20 | 12/20 / 3/20 | Both new |
| My Suzuki | 7/20 / 12/20 | 14/20 / 1/20 | Both new |
| MyWuling+ | 9/20 / 0/20 | 0/20 / 3/20 | Original Indonesian, new English |
| myHyundai Indonesia | 12/20 / 12/20 | 1/20 / 0/20 | Original Indonesian, new English |

The Hyundai pair is useful counterevidence: the favorable count can stay equal even when the records differ. The Suzuki pair combines a large date difference with a rating difference. Sorting brands by these displayed records would mix curation, language, date, platform and task context.

The new Wuling English selection adds three records dated 2026. Two describe specific connected-car difficulties (`ER-0024`, `ER-0040`); the third requests CarPlay/Android Auto (`ER-0032`) and remains unknown for specific app-task experience. The first wave's entirely older Indonesian selection therefore cannot justify saying that all available Wuling feedback is historical. A wish does not prove that a feature is universally absent.

## Test 3: dates and versions limit claims about the relaunched Digiroom

(certain) Of the original 210 records, **87 carry a 2026 review date**, and **71 combine that date with a source-reported review version**. Of the new 148, 36 are dated 2026 and 34 also carry a version. A displayed version is useful context, but the review does not independently verify which build produced every experience described.

| Original Digiroom source-date group | Records | Version present | Specific self-reported app interactions |
|---|---:|---:|---:|
| Before 6 December 2025 | 37 | 24 | 19 |
| On or after 6 December 2025 | 13 | 13 | 6 |
| **Original Digiroom total** | **50** | **37** | **25** |

This is a date-context test, not a before/after effect estimate. The relaunch date does not identify installed-build exposure or comparable customers. The historical records remain useful for describing jobs, earlier problems and recovery, but they do not directly establish current defects. Only six post-boundary records describe specific app interactions; none has an independently verified operational outcome.

One further boundary comes from the existing BYD records. A charging-control wish (`REV-0141`) coexists with another account saying smart-charging controls were added (`REV-0205`). Their dates, platforms and feature variants differ. The defensible research question concerns availability and usefulness for a specific model, build and task, rather than a universal feature-absence assertion.

## Test 4: the app's role and vehicle context change transferability

(certain) Six of the 40 new Suzuki records explicitly concern motorcycles. Three explicitly name or describe a car context. The remaining 31 do not establish vehicle type and remain unspecified. Removing only the motorcycle cases would still leave 31 unknown contexts; they must not automatically become passenger-car evidence. This vehicle-context check was exploratory and added after acquisition, rather than represented as an externally preregistered test.

Suzuki accounts cover parts discovery, stock, payment, shipping, dealer response and workshop administration. A 2026 branch queue account (`ER-0106`) is coded as a branch experience, not an app-task failure. A 2024 Grand Vitara account (`ER-0137`) is explicitly car-related and concerns model availability for booking and unanswered chat. These identify different task and ownership boundaries.

Honda provides another useful distinction. A 2026 account reports a booking cancellation (`ER-0075`), while a 2020 account reports an app request that the dealer could not find (`ER-0083`). These motivate checking request receipt, branch acknowledgment and completion as separate events. They do not show that Auto2000 has the same defect, identify the cause, or prove that every Honda branch behaves similarly.

Chery has only eight new displayed records. Six have insufficient evidence of a specific app interaction. A verification-wait account (`ER-0147`, 2025) is a specific report; an identity/privacy concern (`ER-0142`, 2025) is not proof that a data upload occurred. Listing metadata, feature descriptions and wishes remain separate from experienced outcomes.

## What the evidence supports next

(guessing) A stronger measurement design would attach each user account to a named task, app/build, vehicle, entitlement, branch or fulfillment owner, and an observed outcome. For service booking, distinguish submission, receipt, acknowledgment, confirmed slot, arrival and completed work. For parts, distinguish model identification, availability, payment, dispatch and receipt. For connected-car features, distinguish eligibility, activation and an actual successful action. Public reviews supply possible failure points and counterexamples, not the internal denominators required to choose the highest-value intervention.

## Protocol, codebook and reproducibility

The local analysis plan was timestamped and hashed at 03:43 UTC on 11 November 2026, before these new calculations and acquisitions. The AI researcher already knew the first-wave records, so this is not a blind test or external preregistration. Six prespecified tests cover rating/status cross-tabs, uncertainty, selection, date/version, counterexamples and new-cohort sensitivity. `PRESPECIFIED_COUNTEREXAMPLES.json` fixes ten known old examples before calculation. Original and extension rows stay separate in every main table; matched cross-wave pairs are labeled explicitly.

Primary `experience_status` codes are `self_reported_app_job`, `branch_experience`, `product_review`, `prospective_no_job` and `unknown`. A reported app job includes a failed attempt. Secondary `report_type` codes distinguish success, constraint/failure, recovery, feature request/concern, generic non-job praise and mixed/unclear accounts. Vehicle context records only explicit car or motorcycle evidence; otherwise it stays unspecified. These are source-grounded AI question flags and classifications, not customer outcomes or human-validated labels.

One AI researcher source-inspected all 148 new records. A second AI agent source-inspected the purposeful 16-record subset listed in `SECOND_AI_CHECK_RECEIPT.json`. All 16 source-text hashes matched, and that check found no mandatory classification correction. It was nonblind, with the original codes visible, and did not estimate accuracy or population reliability. Its two explicit caveats concern an unspecified contact-center recovery (`ER-0006`) and a reported shipping constraint (`ER-0108`), neither of which verifies a completed transaction. The earlier 30 targeted checks apply separately to the frozen first-wave 210. There was no human validation, blinded reliability study or independent service-outcome verification. `human_validation`, `independently_verified` and `reviewer_residence_verified` remain false.

`derive_extension.py`, `analyze_followup.py` and `derive_interpretation_checks.py` reproduce the metadata joins and calculations from the frozen annotation inputs and private source records. The private full-text cache is intentionally excluded from the release, so this is not a one-command reproduction of the original capture or semantic judgments. Rerunning public acquisition may expose different selected records. `collect_extension.py` documents the permitted listing method; it does not call disallowed review-pagination routes or Apple RSS. The Google parser's process-wide SSL side effect is immediately restored, and actual requests use the shared TLS-verifying transport.

The source-capture index records the nine listing URLs, actual request IDs, capture times, HTTP results and SHA256 body hashes. All source text hashes match the frozen annotations. Validation checks uniqueness, zero old/new overlap, source timestamp joins, rating range and absence of author/contact/full-text fields. No p-values, population prevalence estimates, pooled brand league table, causal effects or verified completion rates are produced.
