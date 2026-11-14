# Independent review of the achieved study

Review date: 14 November 2026. Reviewer inspected the acquired provider inventory, official branch reconciliation, source methods, routing implementation and the first twelve report pages in `scripts/build_report.py`. This is independent AI review of project outputs, not independent field observation, customer verification or human validation.

## Current assessment

The study's wording has narrowed appropriately from recovered paid jobs to modelled geographic access and testable commercial propositions. The first twelve draft pages correctly distinguish payer from warranty status, source records from customers, generic repair/service candidates from qualified substitutes, and public model durations from actual traffic. No customer-review collection is part of the inspected workstreams.

The source-access fallback is documented honestly: Overture supplied the automotive-place inventory after Overpass access failed. The project must not describe achieved dual-source OSM/Overture place verification. OSM attribution is appropriate for the OSRM road graph, but that is a different evidence layer from the Places inventory.

## Actual issues and required dispositions

| ID | Priority | Issue observed | Required disposition | Current status |
|---|---|---|---|---|
| IR01 | P0 | The generic repair/service pool has no independently documented Toyota/model/job comparator set | Keep candidate access separate from qualified-job access; an empty documented pool means unknown, not zero actual capable workshops | Correctly stated in draft pages 9 and 12; verify final maps/tables retain wording |
| IR02 | P1 | Deterministic 60-record sample contains names suggesting category noise: Castrol - Bike Point; Irfan Busa Helm; Taman Harapan Baru thb Cluster Nirwana; Pasar Patra; officialhondabekasi; paint/PDR specialists | Show concrete examples; do not call source confidence a measured capability probability; retain explicit-car-name sensitivity | Sent to root and provider researcher; examples are anomaly flags, not field-confirmed false positives |
| IR03 | P1 | Three geocoded other-authorised Toyota providers are documented separately but omitted from main routing build_config | Either include in a separate sensitivity/complementary route analysis or disclose the omitted, targeted supplement clearly; avoid complete Toyota-network claims | Sent to root and routing researcher |
| IR04 | P1 | General workshop route eligibility is not evidence for the exact oil/brake/high-voltage job | Apply uncertainty symmetrically to Auto2000 and alternatives | Correctly stated in inspected report |
| IR05 | P1 | 0.08-degree destination margins diagnose only a finite inventory; they do not establish complete outer catchments | Report finite-window boundary limitation; retain core-only comparison | Implemented in code and README; final results pending |
| IR06 | P1 | Branch coordinate exclusions include Suci and Sidoarjo | Identify their direction of possible access bias in relevant local pages; never describe exclusion as closure | Branch methods document; check final local pages |
| IR07 | P1 | Market selection was refined during access tests/source discovery, not frozen prospectively | State purposive selection and post-discovery refinement | Correctly stated in draft page 4 |
| IR08 | P1 | Other-authorised Toyota and OtoXpert operator ownership differ from Auto2000 contribution | Do not convert Toyota-network retention into Auto2000 GP | Correctly stated in draft pages 2 and 8 |
| IR09 | P2 | Regular 9x9 grids have equal weights, not observed residents/owners; degree rectangles differ in area | Label sampled-origin shares and avoid weighted-demand language | Correctly stated in report and routing methods |
| IR10 | P2 | Config stores workspace absolute destination paths | Offline reproduction should rebuild portable config or supply relative paths | Check final reproduction instructions |

## Independent arithmetic review

`independent_checks.py` recalculates inventory counts, identifier uniqueness, eligibility thresholds, duplicate exclusions, global coordinate ranges, official branch routing eligibility and destination-bound compliance from the CSV inputs. The initial pass recorded eighteen successful checks. The routing-output check was pending at that point because the complete run had not yet written outputs; this is not an observed arithmetic failure. Rerun after final outputs exist.

The reviewer script independently recalculates all origin/scenario nearest durations from the achieved OD table and verifies market-level medians, paired medians and the absence of a documented comparable-job pool. It does not reuse the routing implementation's functions.

## Concrete inventory caution

The sample contains potentially non-comparable names despite conservative category/confidence filtering. This is expected to affect both nearest-candidate durations and provider-choice counts. A literal car-name filter is a useful sensitivity but remains insufficient: a car-detailing or body/paint provider may still not perform the chosen oil/brake job. The correct consequence is a bounded interpretation and a prioritised verification task, not a claim that the baseline establishes workshop competition. Name anomalies are not a measured source error rate.

## Acceptance conditions

The study can be accepted as a reproducible exploratory public-data geographic investigation if final output checks pass and the report preserves these limits. It cannot be accepted as a measurement of customer switching, paid-job recovery, branch capacity, service fulfilment, customer willingness to pay or incremental GP. Any market/branch recommendation must remain a proposal for further validation.

## Supplement: screening geography mismatch

The reviewer independently compared both screening CSVs and confirmed that they are **two complementary screens with fifteen units each**, not the same fifteen markets. The context screen uses administrative selections; provider discovery uses bounding boxes. Jakarta core, Bekasi, Bogor and Tangerang are four contextual units that overlap one Jabodetabek discovery window. Denpasar and Pontianak are context-only. Samarinda, Pekanbaru, Cirebon, Jember and Kediri are discovery-only. The nine shared names still do not establish matched spatial coverage.

Root's proposed disposition is acceptable if the report describes the two screens separately, includes a crosswalk, avoids a summed market count and does not rank/join their counts as comparable market totals. This correction is a source-geography distinction, not a cosmetic relabelling.

## Supplement: partial routing audit

The reviewer independently recomputed all nearest-duration values and paired medians for the first two completed markets, using only `csv`, `statistics` and the saved OD rows. Across 45,117 OD rows, 324 origin-scenario rows and 648 nearest-provider minimum comparisons, no arithmetic discrepancy was found. Baseline paired gaps were 3.467 minutes in Surabaya and 3.928 minutes in Medan; the 250-metre snap scenario produced 3.622 and 4.086 minutes across 59 and 78 paired origins respectively. These partial results do not replace a final four-market audit. See `PARTIAL_ROUTE_CHECK.json`.

## Final main-matrix and focal-branch arithmetic audit

The completed main matrix contains 76,221 unique directed OD rows, 324 grid origins and 648 origin/scenario rows. The independent script passed **97 checks with zero discrepancies**, including all pair-minimum calculations, market medians, paired medians and 10/20/30-minute origin counts. Screened paired-origin denominators are 59 in Surabaya, 78 in Medan, 78 in Bandung and 69 in Palembang. Independent checking does not establish that the source places, speeds or model routes are true in the field.

A separate reviewer calculation checked nearest-branch assignment, origins within 20 minutes, loss of 20-minute access after branch removal, and maximum added duration for all 54 branch/scenario rows. **216 branch-influence comparisons passed with zero discrepancies.** Twelve focal branches were selected by explicit nearest-grid-origin/leave-one-out rules. These are finite-grid case investigations, not independently observed customer catchments or operational closure advice.

The main paired median gaps are 3.467, 3.928, 5.177 and 3.317 minutes for Surabaya, Medan, Bandung and Palembang respectively. The 250-metre screen gives 3.622, 4.086, 5.200 and 3.425 minutes. These are small-to-moderate baseline profile-route differences relative to a noisy candidate pool; they cannot support an owner-switching elasticity or an incremental-job estimate.

## Provisional quality assessment before PDF inspection

| Dimension | Score / 10 | Reason and limit |
|---|---:|---|
| Task fulfilment | 8.5 | Broad source collection, four routed windows and twelve focal branches achieved; exact job capability and matched quotes remain unidentified |
| Numerical correctness | 9.5 | Independent recomputation found no arithmetic discrepancy; field truth and public routing-model validity remain outside this check |
| Evidence interpretation | 9.0 | Draft corrects payer/warranty conflation and distinguishes candidate/qualified/modelled layers; final figures must preserve these distinctions |
| Completeness and reproducibility | 8.5 | Raw source extracts, caches, scripts and receipts exist; final archive portability and supplemental-chain work remain to be checked |
| Clarity and usability | Pending | Requires final PDF/maps and archive inspection |
| Presentation quality | Pending | Requires rendered-page visual inspection |

The scores are reviewer judgments, not empirical accuracy estimates. No numerical score overrides an unresolved blocking claim or missing file.

## Final disposition after supplemental work and rendered-PDF inspection

The final supplemental analysis includes 67 official Shop&Drive coordinates, three selected local oil-advertising destinations and three other-authorised Toyota destinations. The omission recorded as IR03 is therefore resolved through a clearly labelled targeted supplement, not an exhaustive competing-network claim. Independent supplemental checking passed 2,635 arithmetic comparisons with no discrepancies, including provider minima, pooled OtoXpert/Shop&Drive minima and paired medians. The snap-screened oil-network gaps are 0.967, 0.347, 2.636 and 2.638 minutes across the same 59/78/78/69 paired origins. These are advertised network pathways, not verified equivalent current jobs.

The reviewer inspected extracted text from the completed 50-page PDF, all fifty rendered-page contact-sheet views and full-page PNGs for pages 2, 5, 14, 16, 30, 35, 44, 45, 49 and 50. There are no blocking observed layout or claim defects. The earlier map-legend omission has been corrected. The PDF's executive brief gives the named oil-network result and capability limitations, while pages 34-35 show category noise and magnitude sensitivity. The two different screening geographies and the achieved-versus-planned scope receipt are explicit. Relative input paths are supplied in `portable_config.json`.

Accepted as an exploratory, reproducible public-data geographic investigation. Some map labels are small at page-fit scale; standalone high-resolution figures and the interactive map mitigate this nonblocking presentation limitation. Source truth, current job fitment, capacity, customer switching and commercial lift remain unidentified. See `FINAL_REVIEW_RECEIPT.json` for the exact reviewed PDF hash, coverage and final reviewer scores. Final archive integrity is a separate root-agent check.


## Final version alignment

The report was subsequently reordered to place the oil-service comparator on pages10-12 and figures were enlarged to use available space. The reviewer re-inspected all50 page contact-sheet views, full pages2/7/10/11/17/33 and the final revised page10/11 renders. The two text fixes clarify that67of425official Shop&Drive listings fall within the study windows and that the page11figure uses81all-routed origins per market while its table uses the250-metre snap screen. No new numerical or layout defect was found. The final accepted PDF SHA256 is `9561b2c32f7307dc0e82e2858d76f74b1df987a93203f68c8c85b78608fa964c`. The final receipt supersedes its earlier PDF hash and records current visual-review coverage.
