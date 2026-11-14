# Primary-source checks and analytic boundaries

Completed 11 November 2026. Raw PDF bytes, extracted text and rendered pages are under `auto2000_run/private_cache/market_text/`, excluded from public release. Source hashes are in sources.json. The shared HTTP transport recorded request IDs in primary_retrieval*.json.

## Deloitte service figures

Original URL: https://www.deloitte.com/content/dam/assets-zone1/southeast-asia/en/docs/industries/consumer/2026/sea-cb-2026-sea-automotive-consumer-study.pdf

The full 23,651,212-byte PDF was fetched successfully; text extraction succeeded. Rendered PDF pages 33, 34 and 35 at 110 dpi and visually inspected all three. The printed numbers equal the one-based PDF page numbers on these pages. The Indonesia table columns, chart legends, values and question bases match the 28-cell derivative table. Printed p37 identifies fieldwork October–November 2025 and n=1,004 for Indonesia overall.

- Q16, p33, n=629: service facility mix. The 80% refers to authorized/new-vehicle dealers, not Auto2000 specifically.
- Q17, p33, n=618: most important provider-choice reason. The correct Indonesia values include quality 23%, trust 21%, warranty 18%, convenience 12%, cost 7%.
- Q21, p34, n=618: most important service aspect. Transparency 32%, treatment 28%, online booking 0% and appointment availability 0% are visually confirmed as printed. Rounded 0% must not be translated into exactly no respondents, no willingness to use or no operational importance.
- Q22, p35, n=629: most trusted relationship. The regular service dealer is the 46% light-blue segment, selling dealer the 20% yellow-green segment, manufacturer the 24% blue segment. They must not be swapped.

Do not sum repeated question bases into people or pool the service bases with EV-intender bases. Do not compute confidence intervals without the sampling/weighting design. Underlying microdata and question-level respondent overlap were not obtained.

## Academic papers

Full PDFs were retrieved and methods/results inspected. Study publication year is not data-gathering year. The Java study was published in 2025 but fielded its choice surveys in Q4 2023. There were 680 four-wheel respondents, each making repeated choices, not 5,440 independent people. The study expressly states raw data are not publicly available and identifies a lack of formal qualitative coding/inter-coder checks. Do not claim model replication or current revealed preference.

The UI paper's 181 respondents came from 580 initial responses with strong eligibility screens. Its label of random sampling does not establish a population frame in this review. Table 1 marks the perception hypothesis supported although the result has the opposite sign to the proposed negative direction. Treat the reported association cautiously; do not reuse it as a causal education effect.

The 2025 IPB UTAUT2 paper contains a material table/narrative discrepancy around habit-to-use significance. Preserve this issue and omit that path from substantive evidence. Its nonsignificant intention-to-use result is a published association, not proof that intentions never translate to behavior. The 2024 IPB paper uses purposive sampling; do not characterize it as representative. Neither study verifies completed vehicle purchases in this review.

## Program and benchmark checks

Toyota Indonesia's age/service eligibility language is not flattened into a new universal rule. Scheduled-service conditions and certificate delivery are distinct from unconditional warranty approval. XTRA's paid-service stage is not the same as covered T-CARE jobs. Dealer reimbursement and EV-specific margins remain unknown.

UK and US mechanisms are clearly foreign benchmarks. Operator announcements establish features and process descriptions, not demonstrated success. Cox/Autotrader and the multiple Toyota or JD Power documents share ownership clusters; repeated pages do not create independent corroboration. KINTO's personal-use and remaining-cost restrictions are retained. No end-to-end customer transaction or appraisal was submitted.

## Calculations

The derivation script asserts weighted-share reconciliation and equal outcomes for the two normalized service-decline cases. These are reproducible arithmetic diagnostics. No stochastic simulation, fitted causal model, projected ROI, customer prevalence estimate or selected investment portfolio was generated. Source-based data, derived arithmetic and synthetic examples are distinguished in the machine-readable outputs.
