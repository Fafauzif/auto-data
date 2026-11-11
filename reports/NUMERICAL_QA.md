# Numerical and economic interpretation audit

**The checked arithmetic reconciles. The main risks are denominator changes, confusing an illustration with observations, and attributing an accounting difference to a business cause.** This audit independently recomputed figures from the supplied casebook and the current structured research artifacts. It did not modify another workstream's data or make new downloads.

At the final 11 November 2026 freeze, the audit contains **157 check rows: 140 arithmetic/input checks passed, zero failed, 17 require scope qualifications, and zero remain pending**. These are audit assertions, not source observations. All 51 insurance illustrations were checked separately across eight monetary fields per row. `numerical_qa_summary.json` records exact input hashes and time. The final run was entirely offline. No human review or verified customer outcomes are claimed.

## Findings that matter to the final synthesis

| Topic | Verified calculation or observation | Required interpretation |
|---|---|---|
| Financing cash timing | Rp 154,847,741 → Rp 109,533,402 upfront, a **Rp 45,314,339 decrease**; Rp 9,271,161 → Rp 10,403,402 monthly, a **Rp 1,132,241 increase** | Same vehicle, location, base DP and ADDM; conditional simulator estimates, not approvals or binding quotes |
| Financing denominator | Base DP remains **20% = Rp 95.08 m**. Total initial cash equals **32.57%** or **23.04%** of the Rp 475.4 m vehicle price | Base DP and total upfront cash are different quantities. The difference is not proof of hidden fees |
| Financing time | Each row's remaining instalments equal tenor minus one; the 60-month option has 59 remaining monthly instalments | Do not add 60 monthly instalments to total upfront, which already follows ADDM first-payment timing. Exact coverage, fees and APR remain unidentified |
| Casebook after-sales | Rp 9,000 bn revenue, Rp 3,150 bn GP; **13.0% of revenue, 46.7% of GP, 35.0% combined GM** | Services-only 55% margin is not the combined after-sales margin, an EV-specific margin or a program contribution assumption |
| Casebook profitability | Rp 6,750 bn GP − Rp 4,620 bn unallocated opex = Rp 2,130 bn operating profit; **3.1% operating margin** | Do not equate a proposed program's gross profit with operating profit after its costs |
| Toyota/Lexus portfolio | xEV 37,693 →31,668, **−15.98%**; total sales 291,566 →251,954, **−13.59%** | Toyota and Lexus domestic new sales, not Auto2000 dealer sales or the installed service base |
| Portfolio mix | xEV share 12.93% →12.57%, **−0.36 percentage points** | Smaller share change and larger volume decline answer different questions |
| National/category sensitivity | Case arithmetic recovers Toyota 31.16% overall share. A 10 ppincrease in xEV mix at fixed within-category shares reduces total share by **1.506 pp** | An assumed sensitivity, not a forecast, observed loss or Digiroom effect |
| Insurance illustrations | Every stored shortfall, top-up, customer credit, conditional recovery and dealer residual agrees with independent integer calculations | **51 constructed scenarios and zero observed insurance quotes**. Available cover, pricing and underwriting appetite are unresolved |
| IGAR counts | **617,722 rows per view**,617,703 distinct composite keys,19 excess duplicates per view | Two label views of the same auxiliary government-app corpus, not 1.235 million independent reviews or automotive customers |
| IGAR disagreement |255,414/617,722 = **41.35%** | Weak-label disagreement, not accuracy, verified error or manual ground truth |
| Spatial computations |2,454×2,453 = **6,019,662 directed station-pair computations** | Arithmetic generated from 2,454 source station records; unordered pairs are half as many. No additional independent observations are created |

Evidence: checks NQ01–NQ62, actual supplied casebook printed/PDF 8–11, journeys UX03–UX04, market MC01–MC04, Astra AR 2025 printed 140/PDF 142, insurance ILL-001–ILL-051, and the listed dataset derivative tables.

## The Astra decomposition is an identity, with an ordering choice

Let total sales beT and xEV share bem. The reported identity is:

`xEV change = (T2025−T2024) × m2024 + T2025 × (m2025−m2024)`

This assigns **−5,120.951 units** to the total-sales-scale term and **−904.049 units** to the within-portfolio-mix term, totaling−6,025. Holding the 2024 mix against the 2025 total gives 32,572.049 xEVs. A different valid ordering assigns−4,978.817 and−1,046.183 units instead, also totaling−6,025.

The terms do not identify why either total or mix changed. A statement such as “market weakness caused 85% of the xEV decline” is unsupported. Product availability, prices, geography, model mix, financing and competition remain possible causes. No public panel here identifies Digiroom's share of the change. [NQ30–NQ38]

## A cap on insurer payment does not cap a separate customer promise

For the illustration with floor Rp 200 m, valid offer Rp 160 m, top-up cap Rp 10 m, retention Rp 10 m and conditional insurer layer Rp 15 m:

* A capped top-up gives the customer Rp 170 m, below the full floor.
* A full floor creates Rp 40 mshortfall. The assumed insurer pays Rp 15 m, leaving Rp 25 mwith the dealer before contribution and operating costs.
* Across 20 eligible redemptions, capped top-ups total Rp 200 m; the hypothetical full-floor dealer residual totals Rp 500 m.

The figures reconcile. They do not establish a purchasable Indonesian syariah RVI policy, an insurer's willingness to accept those risks, a distribution agreement or profitability. Contribution, ujrah, dealer marketing compensation, insurer recovery and dealer GP are distinct flows. Neither an inspection certificate nor an ecosystem partner creates a funding source by itself. [NQ39–NQ41,NQ76–NQ77]

The casebook's Rp 150 bnincremental-investment cap covers 2026–2028. It is not an approved allocation or proof that multi-year guarantees cannot create obligations after 2028. [NQ80]

## Survey and source-version qualifications that must survive editing

Deloitte service questions use 629 or 618 respondents depending on the question. Their 28 exported numerical cells are not 28 respondents, and the related question bases must not be added into a larger sample. Q17's values 23%,21% and 18% correctly rank quality, trust and warranty in that question. Q21's printed 0% for online booking or appointment availability is a rounded most-important-factor response, not zero demand, zero usefulness or no actual users. The 28.06% nested charging calculation is approximate and concerns lack of dedicated access, not inability to charge. [NQ21,NQ42–NQ46]

The supplied awareness figures 57% and 28% yield 29 percentage points arithmetically, but the masked original chart was not available for numeric verification. That difference remains supplied-input arithmetic. It is not independently established Digiroom awareness, conversion or incremental sales. PwC's 71% maintenance-cost reason is conditional on EV owners considering a return to ICE; a regional chart base cannot become Indonesia's sample size. [NQ78–NQ79]

The 2026 GAIKINDOcategory chart's 72 cells total 679,202. The separately stated January–September narrative is 679,020, a 182 unitconflict. Both source versions remain visible; no correction was invented. Toyota's reported hybrid concentration calculations also reconcile, but the source category includes mild hybrids and does not reveal Auto2000's mix. [NQ47–NQ52]

IGAR's missing-translation group has 97.25% disagreement but contributes only 2.96% of all disagreements. Present-translation rows still disagree 40.64% of the time. This descriptive association does not identify the correct label or the cause of disagreement. [NQ70–NQ73]

## Final figure and site checks

All three figures received AI visual inspection. Finance values 154.85 m/109.53 m and 9.27 m/10.40 m match the rounded source output. The five coordinate annotations match independently recomputed Haversine separations, including 55.258 km for Balikpapan Sudirman. The logarithmic axis is labelled. It remains a selected source-coordinate disagreement, not field confirmation of an incorrect charger location.

The regenerated service-choice PNG was inspected again by AI. Its title now concerns the stated service-choice reasons, and its eight bars and n=618 caption match Q17. It makes no booking-convenience comparison. NQ69 also confirms that the output is current against the corrected generator. This closes the earlier title-refresh item. [NQ46,NQ57–NQ59,NQ69]

The final site freeze reconciles **345 requested URLs, 281 successful HTML captures, 181,158 selected-text words and 15,323 structural link rows**. The word total was independently summed from the page CSV, and the link total was read from the database in read-only mode. Status and source-family counts also reconcile. The 24 fixed reference selections match production word counts and content hashes, and all 24 published comparisons pass every recorded check. Their summary explicitly records zero new network requests and no human validation. These are offline AI checks against captured source material, not human review. [NQ68,NQ82–NQ87]

These counts do not establish unique customers, independent information, rendered user outcomes or sitewide error prevalence. Selection was purposive, and selected text can retain template content. All 17 scope qualifications remain in force after the release checks close.

## Reproduction

Run `python auto2000_run/reports/numerical_qa.py` from the workspace. It reads source artifacts and the actual supplied casebook, writes only this audit's CSV/JSON files, asserts that arithmetic checks have no failures, and records input SHA256 hashes. No source data, third-party reports or other workstream files are modified. Read `numerical_qa_checks.csv` for the full assertions, evidence references and limitations.
