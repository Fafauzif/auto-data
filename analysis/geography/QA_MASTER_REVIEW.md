# Independent review of master-report geography claims

Reviewed file: `integration_work/master_report.md`, 14 November 2026 draft. Reviewer used the saved raw geographic OD records, source methods, latest decision table, this workstream's independent recomputation and the curated Maps evidence. The master report was not edited by this reviewer.

## Verdict

No numerical error was found in the principal geographic claims. The portfolio recommendation is coherently bounded: modeled origin counts are separated from demand, capacity and capital allocation; selected reviews are used as mechanisms rather than complaint prevalence; and the Soekarno-Hatta recommendation does not promise unconditional single-visit repair of complex faults.

Four editorial corrections will improve precision before release. None changes the numerical findings or recommended prioritization.

| Priority | Location | Required clarification or correction |
|---|---|---|
| Medium | Opening geographic paragraph | Both 39 and 20 are calculated **after coordinate correction**. The 39-to-20 change isolates permitting Auto2000-operated OtoXpert within that corrected scenario. Suggested text: “Within the corrected-coordinate scenario, permitting eligible Auto2000-operated OtoXpert changes the four modeled windows from 39 to 20 origins above the five-minute oil-gap threshold.” |
| Medium | Finding 2 and repeated references to “full-scope” | Prefer **general-workshop access/service**. Official branch identity and the general-workshop destination universe do not establish universal fitment, high-voltage diagnostic capability or every possible job at every site. The distinction with the narrower modeled oil task is valid without the broader phrase. |
| Medium | First discussion of geographic thresholds | Explicitly state that **five minutes and 15 minutes are analytical thresholds**, not measured consumer tolerances, agreed service levels or promises of traffic-adjusted travel time. The existing population/demand qualification should remain. |
| Low | Evidence locator M01–M30 | Current `curated_maps_evidence.csv` and JSON contain **34 cases, M01–M34**. Update the locator range so new A. Yani/TAA cases can also be found. |

## Numeric checks

| Master claim | Independent result | Status |
|---|---|---|
| Paired strict geographic origins | Surabaya 59, Medan 78, Bandung 78, Palembang 69; total 284 | Match |
| Oil-tail count before/after owned-channel scenario | Surabaya 10→6, Medan 3→0, Bandung 17→14, Palembang 9→0; total 39→20 | Match |
| Residual geographic concentration | Bandung 14/20 = 70%; Soekarno-Hatta 8/20 = 40% of pooled model origins | Match; not demand shares |
| Pancing removal test | Eight assigned origins lose general-Auto2000 access within 15 model minutes; zero residual oil tails | Match |
| Tanjung Api-Api removal test | Seven origins lose the 15-minute general-workshop threshold; zero residual oil tails | Match |
| Soekarno-Hatta removal test | Zero origins lose that general-workshop threshold; eight residual oil tails | Match |
| Suci correction | Twenty nearest-branch assignments change among 78 paired Bandung origins | Match |
| Sidoarjo | Zero winners on the old grid; six of six targeted southern building origins choose Sidoarjo | Match; targeted extension denominator remains separate |
| TAA/Veteran tie | Seven unique TAA tail origins plus one shared exact-duration origin; do not sum upper bounds across branches | Match |
| Raw data reconstruction | 76,221 main + 5,913 supplementary + 162 corrected outbound records = 82,296 | Match |

## What 82,296 does and does not count

An additional key audit confirms **82,296 distinct `(market, origin_id, destination_id)` outbound comparison keys** in those inputs. They refer to **324 distinct `(market, origin_id)` calculation locations**, with 284 remaining in the strict joint retained comparison. Therefore, the row total is not a duplicated customer count, but neither is it 82,296 independent geographic samples or people. Each original grid location is reused across destination comparisons. The 162 corrected outbound rows add comparisons to Suci and Sidoarjo; their separately calculated reverse rows are outside this outbound row count.

The audit JSON and script now include `raw_unique_outbound_pair_keys=82296` and `raw_unique_market_origin_keys=324`. These extend the original 290 successful branch-field comparisons and do not change their results.

## Review selection and chronology

The master report correctly calls M08 historical diagnostic evidence rather than current branch prevalence. Its actual publication is **16 July 2024**, not 2014. It is a one-star review that contains positive comments about hospitality/punctuality alongside unresolved-work complaints; do not describe it as a high-rated review.

M09 was published **15 October 2025** and belongs to both the recent Auto2000 and lowest-ranking diagnostic runs. It is one review with two collection memberships, not two corroborating observations. M03 was published **30 March 2026** and likewise occurs in both cohorts. Its non-booking context supports walk-in acknowledgement rather than a claim that the app caused the failure. M02 was published **27 June 2025**, appears in the diagnostic cohort only, and does not identify Digiroom; the master correctly avoids attributing it to the December 2025 relaunch.

The branch narratives and model geometry support a **chosen intervention mechanism**, not an estimated frequency, quantified customer-loss rate, or causal effect of geography on those reviewers. No unsupported geographic link to the reviewers' home addresses was found in the master draft.

## Source boundaries to retain

1. The oil comparator is the collected network-advertised OtoXpert/Shop&Drive set, not every capable local garage or an installed-price comparison.
2. Owned OtoXpert refers to the official operator label used in the source snapshot. It is not a discovered GP-sharing agreement.
3. A second branch or an OtoXpert location is a route alternative, not evidence of free capacity or accepted stock/slots.
4. Building-anchor and half-cell-shift results are targeted sensitivity tests. Their denominators should remain separate from the 284 paired baseline origins.
5. An extra visit can consume an access advantage, but the master appropriately distinguishes routine prepared work from complex diagnostics that may require staged resolution.

## Reproducibility

`analysis/geography/scripts/independent_od_audit.py` reconstructs the raw corrected strict scenario using Python's standard library, without network calls. `analysis/geography/scripts/portfolio_analysis.py` rebuilds the portfolio summaries from the saved 29-endpoint table. Original source paths can be supplied explicitly if the release layout differs. Existing numerical results were rerun successfully during this review.
