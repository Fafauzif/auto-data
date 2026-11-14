# Report and decision workbook reproduction

The integrated report is authored in Markdown and rendered to editable DOCX with `build_report.py`. The Word file is rendered through the primary runtime LibreOffice implementation to create a matching PDF and page images for visual checking. The Markdown remains the source of the narrative.

The workbook is authored with `@oai/artifact-tool` through `build_workbook.mjs`. `workbook_inputs.json` freezes the supporting tables used for this release. It contains three social-platform coverage records, four supplied-case business lines, four market portfolios, 29 branch records, 45 Maps place/cohort rows and three YouTube video rows. The source tables remain authoritative in the analytical folders; regenerate this input after source changes.

## Workbook build

Run from the project root using a Node environment in which `@oai/artifact-tool` resolves. The source environment uses a temporary working directory with `node_modules` linked to the primary runtime dependencies. Set `AUTO2000_PRESENTATION_WORK` to this folder and `AUTO2000_OUTPUT_DIR` to the desired output directory. `AUTO2000_PROJECT_ROOT` is optional and defaults to the current working directory.

```bash
AUTO2000_PRESENTATION_WORK=/absolute/path/to/presentation AUTO2000_OUTPUT_DIR=/absolute/path/to/reports node build_workbook.mjs
```

The builder recalculates the workbook, inspects formula errors, runs zero/positive/missing-input economics checks, restores empty operational assumptions, renders each worksheet opening view and exports the workbook. The independent native-engine check receipt records a separate LibreOffice recalculation of the final workbook. Page and worksheet PNGs are internal QA artifacts.

## Interpretation of the economics model

Completed transactions, incremental share, per-transaction gross profit, programme expenses, displaced contribution and investment cash are editable. Their source values are unavailable in this public-evidence corpus, so they remain blank rather than being filled with invented Auto2000 performance. The supplied case financial exhibit is kept separate. Three-prong results are distinct business-event series; a paid service on a customer's vehicle can be a different event from its sale, but new-to-Auto2000 purchases and existing-customer replacements must not count the same delivered sale twice.

Gross profit per incremental transaction is after ordinary transaction costs and before the additional programme expenses entered below it. Set displaced contribution to zero when it is already captured by the incrementality counterfactual. Shared platform costs should be allocated once. Costs, discounts, inventory exposure and programme liabilities should not be deducted twice or left outside an investment decision merely because they are not present in the source corpus.

The three-year ceiling is the supplied Rp150 billion investment limit, not a proposed spend or an inferred Auto2000 budget approval. No ROI or causal uplift is asserted.

## Delivered repository layout

From the repo root, use `python scripts/presentation/prepare_workbook.py` to refresh frozen workbook inputs from `analysis/`. With `@oai/artifact-tool` available, `node scripts/presentation/build_workbook.mjs` rebuilds the workbook into `reports/` by default. Set the documented environment variables to isolate experimental builds.

Render the narrative with `python scripts/presentation/build_report.py reports/INTEGRATED_REPORT.md OUTPUT.docx`. The original rendering used the supplied documents renderer and LibreOffice; a local LibreOffice PDF export can render the same Word document. Figure files used by the Markdown are in reports/presentation/figures/. The figure script can be rerun with matplotlib.
