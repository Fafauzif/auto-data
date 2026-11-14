# Reproduction guide

## Environment
Use Python3.12 with dependencies in requirements.txt. Full installed dependency snapshot is ENVIRONMENT.txt. No account or paid API is required for the included offline calculations.

## Offline entry points
1. Inspect provider methods, source extracts, provider_inventory.csv and exclusion flags; scripts in workstreams/providers reconstruct filters from selected raw rows.
2. `python workstreams/branches/build_branch_inventory.py` reconstructs the branch fact tables from included JSON; read path defaults first.
3. Routing source scripts and relative input configs live in workstreams/routing. The cached JSON/table outputs are included; see its README for baseline and supplementary commands. Re-running the router may make requests for cache misses. For a strictly offline audit use workstreams/review/independent_checks.py against included OD CSVs.
4. `python scripts/archive_context.py` recalculates national archived-context figures.
5. Context and cartography scripts regenerate figures from tables. The cartography workstream includes the offline HTML generator.
6. `python scripts/build_report.py` regenerates the PDF and page-content/layout receipts after all input tables and figures exist.

## Reacquisition
Provider acquisition has explicit 2026-10-21.0 release/bbox settings. Regional OSM/Overpass attempts are logged but not required to reproduce Overture outputs. Official-page browser/web extraction is documented by source locators and structured facts; no one-click claim is made for re-running those actions. Shop&Drive extractor can reacquire its official embedded location data. Hosted routing and live pages can change, fail or impose new limits. Keep original cached results unchanged when comparing versions.

## Verification
Read QA_SUMMARY.md, independent review and per-workstream receipts. Compare checksums in MANIFEST_SHA256.csv before modifying inputs. The manifest excludes itself and the ZIP to avoid recursive hashes. Alternative scenario rows are repeated calculations on the same observations, not independent samples.
