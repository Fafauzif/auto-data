# Extension arithmetic reconciles; the evidence boundaries remain

The offline extension audit contains **69 assertions: 66 passed, zero failed and three retain explicit scope qualifications**. It ran no collectors, made no network requests and changed no source data. It does not claim human validation or verified customer outcomes.

The first-wave receipt remains separate and unchanged: **157 assertions, with 140 passed, 17 qualified, zero failures and zero pending**. The extension audit does not add the economics workstream's 19 checks, geography's 32 checks, or other local receipts into an inflated total. Those receipts and some independent cross-checks address overlapping propositions. No combined assertion total is reported.

## What was independently checked

| Area | Checked result | Meaning and limit |
|---|---|---|
| New public reviews |148 unique new keys, zero overlap with 210 frozen keys, 358 combined; nine listing URLs and nine capture requests | Selected platform records, not representative customers or independently verified incidents |
| Digiroom date context | The first 50 Digiroom records split 37 before and 13 on/after 6 December 2025. Six of the 13 self-report a specific app job | Review date is not installed build, exposure or a relaunch effect; self-report is not completion verification |
| Review recency |87 of the original 210 have 2026 dates; 71 combine that date with a stated review version | Does not make the remaining records invalid, but prevents presenting the entire set as evidence about the current release |
| Review context | New rows contain 112 unspecified vehicle contexts, 30 explicit cars and six explicit motorcycles | AI-coded context is not verified ownership; mixed vehicle roles cannot become one passenger-car sample |
| Targeted second AI check |16 new records and source hashes match the frozen receipt; no human, random/blinded, reliability or customer-outcome claim | Separate from the earlier 30 targeted checks on first-wave records; neither number is added to the review sample |
| Geographic scenarios |25 coordinate/candidate-pool scenarios and 695 anchor-scenario rows; every saved median and 1/3/5 km count recomputes from the detailed rows | Repeated scenarios on the same anchor set, not 695 new facilities or confirmed alternatives |
| Candidate sensitivity | Source-coordinate all-mapped versus conservative-proxy counts change 20→8 within 1 km and 27→26 within 5 km | Provider/venue filtering, not verified access, hours, uptime, compatibility or actual route convenience |
| Boundary conservation | All pooled boundary years conserve national stocks. The 2025 direct join omits 70,800 of 20,907,972 cars, or 0.339% | A small national omission can still change local ratios materially |
| Papua ratios and ranks | Historical-code 91 denominator 41,685 and 94 denominator 111,637; Papua Barat's site ratio/rank changes 48.80/1 to 19.19/10; Papua rank 9→19 | Every ratio and within-scenario rank was recomputed. These are contextual all-car ratios, not BEV demand or capacity |
| BEV finance | Five rows share Rp799 million price and 20% base DP, Rp159.8 million. The 60-month display is Rp 247,187,147 upfront and Rp 15,581,947 monthly for 59 remaining payments | Conditional simulator output; base DP differs from total initial cash. No APR, approval or complete fee estimate inferred |
| Journey context | Two observed routes carry distinct branch/model parameters, T151/bZ4X and T155/Hiace, into the loaded request flow | A bounded counterexample to universal context loss; no fulfilled appointment, conversion or prevalence estimate |
| Programme estimates |22 new labor/parts rows reconcile; bZ4X events 8–11 sum Rp 9.101 m; Agya event 2 shows zero displayed labor and Rp 564,000 parts | March 2024 retail estimates, not current invoices, personalized entitlement, actual cost or dealer GP |
| Symmetric portfolio bridge | Shapley scale and mix terms reconcile exactly to −6,025 vehicles; the scale term independently matches total change times the mean observed mix | Accounting allocation, not causes, national market effects or Auto2000/Digiroom attribution |
| Constructed contract stresses | Peak retained obligations of Rp300 million and Rp700 million reconcile for dispersed and synchronized states under the declared assumptions | Illustrations without probabilities, approved cover, actual customers or an insurer quote |

The geography workstream's 32 local checks all pass as recorded. This audit independently recalculates the central aggregations and ratio/rank relationships rather than counting that receipt as 32 new independent validations.

## Battery counts and integrals received a separate raw-file check

The audit independently opened all five actual MAT/HDF5 payloads and read the variable shapes. Their sizes and SHA256 hashes match the original source manifest. The payloads total **283,141,466 bytes**, with a largest file of 95,036,227 bytes.

The four physical/BMS signal columns contain **56,507,201 stored current, voltage, SOC and temperature scalar values**. Separately, the clocks contain 56,599,111 values and the epoch field contains 91,910. They are not synchronized rows, independent physical measurements, trips, customers or a Toyota/Indonesian sample. Different current and SOC lengths occur in the actual files. Equal lengths would not itself prove equal clocks.

The final 106 gap-based segments reconcile to the declared greater-than 30-second rule. The 20 saved integral rows satisfy signed/absolute identities. Supported intervals under the one-second maximum-step rule total 51.9736656864 hours. Four saved partial charge intervals independently reproduce their Ah-per-reported-SOC-point ratios, including the reported 1.570124–2.194808 range. That arithmetic does not convert them into capacity or state-of-health values.

For a stronger direct check, the audit reopened Folder 2's current, voltage and clocks without executing the battery author's analysis. Its current and voltage clocks match. Independently calculated sampled trapezoids reproduce both signed Ah and absolute terminal kWh for the bounded and deliberately unbounded calculations. The unbounded absolute integral is **47.52% larger**. This is an illustration of integrating across unobserved gaps, not evidence of a production BMS error, charger inefficiency or degraded capacity.

No independent health-reference field is available in the inspected public variables. The underlying source's hidden reference and proprietary estimator remain a separate validity limitation. Arithmetic reconciliation and matching file hashes do not validate a battery certificate, an appraisal premium or transferability to Toyota vehicles.

## Foreign mechanism evidence stays source-specific

The seven external records are studies or instruments, not seven newly acquired customer datasets. The reviewed NIST TN2328 record specifies 1,490 US respondents, including 490 BEV owners. The 490 are a subset, not additional respondents. The separate valuation instrument is not a measured resale-price result, and other NIST analyses are not silently pooled into this sample.

## Reproduction and freeze

Run `python auto2000_run/reports/extended_numerical_qa.py`. It writes only this audit's outputs. `EXTENDED_NUMERICAL_QA.json` contains the full assertions, frozen first-wave receipt, actual battery-shape counts and input SHA256 manifest. `EXTENDED_NUMERICAL_QA_checks.csv` provides the readable assertion table. The final structured result contains zero failures. Source accuracy, causal effects and the three explicit interpretation limits remain outside arithmetic validation.
