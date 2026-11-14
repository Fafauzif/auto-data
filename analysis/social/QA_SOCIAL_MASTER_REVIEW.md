# Social-evidence review of the integrated master report

Reviewed: `integration_work/master_report.md`, against the full social corpora, the 45-entry X/YouTube evidence register and all 34 Maps cases. The reviewer did not edit the master report. Counts, citation mappings and claim scope were checked; source allegations and offline events were not authenticated.

## Corrections required in the master

1. **TRIVA citations in finding 8 are wrong.** Replace `[R1,M21,M22]` with `[R1,M19,M20]`. M19 and M20 are the two Kertajaya TRIVA accounts, both published 12 October 2026. M21 concerns a historical trade-in application/deposit account, and M22 concerns OLXmobbi Tamini reservation/refund. The current caution that review mentions do not prove deployment/adoption is appropriate. These reviews are novelty-check leads, not corroboration of an official TRIVA product claim unless an official source separately establishes that claim.

2. **Define the Digiroom count as matching posts, not 37 literal occurrences.** The implemented check selects unique X post bodies containing the case-insensitive substring `digiroom`. It finds **37 posts**, all by `AUTO2000ID_`. Those bodies contain **45 substring occurrences** because a post can repeat the term. Suggested replacement: “All 37 unique X posts containing the case-insensitive string `digiroom` come from the named Auto2000 brand account. This subset therefore supplies brand communication rather than independent customer task accounts.” The full scope and separate counts are now fields in `corpus_metrics.json`.

3. **Expand the evidence locator range from M01–M30 to M01–M34.** The source table contains 34 unique cases. The added M31–M34 cases concern Tanjung Api Api brake-check concerns and Ahmad Yani access, positive readiness and mixed payer/entitlement examples.

## Material source-table errors found and corrected before release

These changes have already been applied in the social working files, their scripts and rebuilt outputs. Recopy the current `integration_work/social/` tree into staging; do not reuse an earlier staged copy.

- **M21:** the original source mapping incorrectly attached the trade-in interpretation to a Tanjung Api Api reception/administration complaint. The correct review ID is `ChZDSUhNMG9nS0VJQ0FnSURqbDhDVU1REAE`, at **AUTO2000 Gatot Subroto**, published **8 May 2024**. Its body reports a proposed trade-in, an application not being approved, and difficulty recovering a supposedly returnable deposit. The source does not explicitly name credit approval, so both interpretation and Maps report now say “trade-in application not approved”, rather than declaring a credit rejection.
- **M11:** the source body was correct but its interpretation was too broad. The review is at **Toyota Auto2000 Tanjung Api Api**, published **8 April 2023**, and reports a sales-made booking not found and promised tyres not ordered. It does not establish warranty retention, a preferred alternative or uncertainty at collection. The interpretation, mechanism label and relevant Maps report paragraph now describe **booking and stock readiness**.

All other Maps cases were reread against their full source body and branch. No additional material body/interpretation mismatch was found. The 34-case selection remains illustrative and does not establish saturation or population rates.

## Strong addition recommended for finding 9

The master currently supports acquisition mainly with an unspecified-model X test-drive complaint, a single-car stated constraint and a BYD charging account. There are also two **Toyota hybrid purchase accounts** in the supplied Maps data, which make the client-specific link stronger:

> “Setiabudi M15 describes a Yaris Cross HV purchase by a household working in Jakarta and returning to Bandung on weekends; remote handling and completed registration documents reportedly avoided repeated dealership trips. M16 describes a Zenix HV purchase with financing, handover and document follow-through. These are specific hybrid transaction accounts, but neither establishes a first Auto2000 purchase. Their close publication dates and praise for the same adviser also prevent treating them as independent branch-wide validation.”

Cite `[M15,M16]`. The accounts are published 20 and 24 September 2025. They are not evidence of the December 2025 Digiroom relaunch, and neither names Digiroom. Their contribution is an actionable household scheduling and transaction-continuity mechanism.

## Claims checked and supported at their present scope

- X: 14,892 export rows, 14,291 IDs, ten exports; 6,186 replies with 5,704 immediate parents absent.
- Maps: 8,385 rows, 8,119 IDs, 37 places; latest Auto2000 1,915, latest Shop & Drive 932; diagnostic 1,562, overlap 266.
- YouTube: 74 IDs from three videos; 26/3/45 records; 56 top-level comments and 18 replies; no returned Toyota-focused video.
- Combined: 23,351 rows and 22,484 platform-specific IDs, explicitly not people or transactions.
- M01 intended-paid Veloz arrival, M02 unnamed-app booking, M03 walk-in registration, M04 booking comparison, M07 brake-scope dispute, M08 historical unresolved visits and M09 forgotten scope are correctly bounded in the master.
- SX01 does not allocate the combined Rp25m suspension/audio expenditure wholly to Auto2000. SX02 does not infer xEV model or national shortage. SX05 is a stated single-car constraint. SX08 is a publisher-reported recall allegation and not a completed paid-job observation.
- SY02 is a self-reported installation-cost/charging strategy, not a current tariff. SY03 and SY06 are beliefs or rival explanations concerning support continuity, not verified factory, Neta or depreciation facts.
- Pilot cases remain interpretations. Their current parent/root fields take precedence over inherited notes about missing context.

## Rebuild and encoding checks

All four active social Python scripts now explicitly use UTF-8 for every text `open`, `read_text` and `write_text` call. The complete normalizer, both curation pipelines and release verification were rerun successfully after the corrections. `QA_SOCIAL.json` now passes ten checks, including all 22,484 preserved bodies, all source hashes, 34 Maps source mappings, the corrected M11/M21 anchors and the distinction between 37 Digiroom posts and 45 occurrences.
