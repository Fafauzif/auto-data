# Second-round automotive review evidence

Read `EXTENSION_REVIEW_REPORT.md` first. The extension adds 148 unique platform review IDs from nine allowed public listing pages. Together with the unchanged first wave of 210, the analytical context contains 358 IDs, not verified people or completed jobs.

## Main files

| File | Unit and purpose |
|---|---|
| `new_reviews_derived.csv` | One row per new review ID; nontext metadata, provenance and AI codes |
| `new_ai_annotations.json` | Frozen source-grounded AI judgments, source text hashes and validation flags |
| `source_capture_index.csv` | Nine HTTP captures, their locators, request IDs, timestamps and body hashes |
| `capture_relations.csv` | One row per captured review appearance and its deduplication relation |
| `app_listing_metadata.json` | Snapshot app metadata and published counters; these are not the captured-review denominator |
| `ANALYSIS_PLAN_PRESPECIFIED.md` | Locally timestamped follow-up plan; prior records were already known |
| `prespecification_receipt.json` | Frozen plan and first-wave input hashes |
| `ER_T01_*.csv` to `ER_T06_*.csv` | Derived cross-tab cells, bounds, strata and counterexample records, not additional reviews |
| `EX_Suzuki_vehicle_context_sensitivity.csv` | Exploratory post-acquisition context test, explicitly separate from the prior plan |
| `validation.json` / `analysis_summary.json` | Reconciliation and calculation receipts |
| `play_robots_current.txt` / `acquisition_log.json` | Robots evidence and the nine listing request outcomes |

## Codebook boundaries

`self_reported_app_job` means a source account identifies a specific app interaction. It includes failures and partial progress. `eligible_for_app_task_analysis=true` identifies that classification, not a completed job. Other primary categories are `branch_experience`, `product_review`, `prospective_no_job` and `unknown`.

Secondary `report_type` labels record success, constraint/failure, recovery, a feature request/concern, generic non-job praise, or mixed/unclear content. They are AI interpretations of source statements. They do not verify the claims, technical causes or frequency among users. A generic statement that the app is good or bad stays unknown when it does not identify an app task. A feature wish does not establish that the feature is absent for every model/build.

`vehicle_context_reported` uses explicit car or motorcycle evidence; otherwise it is `vehicle_unspecified`. `locale` is a requested language/storefront pair, not verified residence. `review_version` is source-reported and may be missing. It is never inferred from a date. `source_text_sha256` fingerprints private text without releasing it.

All 148 new records were source-inspected by an AI researcher. A second AI agent completed the targeted, nonblind 16-record source inspection documented in `SECOND_AI_CHECK_RECEIPT.json`, with matching text hashes and no mandatory classification corrections. This is separate from the earlier 30 checks of first-wave records. No human review or blinded reliability validation occurred. `human_validation`, `independently_verified` and `reviewer_residence_verified` are false. `second_ai_checked` is a targeted source-check flag, not a reliability score.

## Reproduce the public calculations

Python 3 standard library is sufficient for these two offline calculations. Run them from the archive root, retaining the workstream directory structure and the frozen first-wave CSV:

```sh
python workstreams/extension_reviews/analyze_followup.py
python workstreams/extension_reviews/derive_interpretation_checks.py
```

They verify the frozen baseline hash and use the released derived CSVs and annotation inputs. They perform no network requests and do not regenerate semantic coding. The output rows are derived statistics, not more original source records.

## Capture and metadata recipes

`collect_extension.py` documents nine specific public listing requests. It checks current robots, uses shared TLS-verifying public transport and parses embedded review objects from permitted listing HTML. It does not use review pagination, Apple RSS, an account, API credentials, identity changes or a proxy. The parser dependency is `google-play-scraper==1.2.7`; its SSL-context import side effect is immediately restored. All actual requests use the shared transport.

Private source bodies and full review text are deliberately excluded from the release. Consequently a clean public download cannot recreate the original capture or run the raw-dependent metadata steps from those private inputs:

```sh
python workstreams/extension_reviews/reconcile_captures.py
python workstreams/extension_reviews/derive_extension.py
```

Those two scripts document review-ID reconciliation and hash-checked metadata derivation. The original environment has the private inputs. A later public listing capture may select different records; the original frozen annotations must not be silently attached to a different capture. The reconciliation script stops if the captured record set differs from the frozen annotation set.

The source index and public metadata permit provenance inspection without exposing raw text. Review IDs are source locators, not reviewer identities. No authors, handles, images, contacts, full text, titles or excerpts are included in the public extension. No population p-values, brand league table, causal uplift or verified service-completion rate are estimated.
