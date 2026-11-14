# Geography integration workstream

Start with [GEOGRAPHY_INTEGRATION_REPORT.md](GEOGRAPHY_INTEGRATION_REPORT.md). It adds an allocation rule distinguishing service preservation from residual travel intervention, checks all 29 endpoint rows from raw OD data and connects selected new branch narratives to the geographic decisions.

## Reading order

1. `GEOGRAPHY_INTEGRATION_REPORT.md`: integrated English interpretation and decisions.
2. `geography_claims.json` or `.csv`: ten indexed claims with evidence status and source locators.
3. `tables/market_portfolio.csv` and `tables/branch_portfolio.csv`: all four windows and 29 endpoints.
4. `tables/raw_independent_audit.json`: the 290 successful field comparisons against raw model rows.
5. `GEOGRAPHY_SOURCE_MAP.csv`: evidence families and their units.

## Offline reproduction

The scripts use Python's standard library only. Pass the preserved latest package root explicitly if the source tree has moved:

```bash
python scripts/independent_od_audit.py --source-root PATH_TO_AUTO2000_LANJUTAN --output tables
python scripts/portfolio_analysis.py --table PATH_TO_AUTO2000_LANJUTAN/output/tables/branch_decision_table_29.csv --output tables
```

No script here acquires routes or alters sources. The intended final default source path is `sources/geography/latest/Auto2000_Lanjutan`, with outputs under `analysis/geography/tables`. A release-specific path adapter may replace that default.

## Interpretation rules

- There are 324 original grid locations, with 284 retained paired origins in the strict four-window comparison. Two scenario rows per original origin preserve excluded/null cases.
- Branch-assigned counts partition the strict model origins. They are not demand, population, customer addresses, traffic or capacity.
- The five-minute tail threshold is an analytical bin rather than a measured willingness-to-travel threshold.
- Stable first-minimum assignment is used only to reproduce the saved branch table. Exact tie IDs remain in `raw_recomputed_origins.csv`; seven unique TAA tail origins plus one shared with Veteran must not become eight unique TAA origins.
- Sidoarjo's zero old-grid assignment must be read with its six-of-six targeted southern-extension result.
- The own-network scenario changes eligible endpoints for an assumed job. It does not establish accepted slots, current fitment, completed jobs or incremental contribution.
- Model route durations are not live traffic. Shifted origins and building anchors are targeted sensitivity tests, not population samples.
- Source-language reports and the full original geography package remain authoritative source artifacts for provenance. This workstream supplies new interpretation and an independent arithmetic audit.
