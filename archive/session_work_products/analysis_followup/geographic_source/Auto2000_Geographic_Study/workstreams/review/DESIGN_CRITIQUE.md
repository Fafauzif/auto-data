# Independent design critique

Prepared 14 November 2026 before this reviewer's inspection of new-study results. This is an independent AI methods review, not field validation or customer research.

## Scope discipline

The primary estimand is modelled geographic accessibility to documented or candidate automotive service providers. The commercial proposition, recovery of paid Toyota workshop jobs, is a downstream hypothesis. The data do not identify the out-of-warranty Toyota owner population, current provider choice, available workshop capacity, willingness to switch, conversion, realised work orders or incremental gross profit. Report conclusions at the level measured.

The user explicitly excluded new customer accounts and reviews. Do not reacquire, code or analyse customer review evidence. Existing review datasets are irrelevant to this analysis unless mentioned solely as excluded scope.

## Blocking design issues (P0)

1. **Candidate garages are not qualified alternatives.** An OSM car-repair tag establishes a mapped category, not the ability to perform the exact Toyota model/year/job. Separate the broad candidate-provider scenario from a documented-capability scenario. Never call the broad pool verified comparable workshops. The strict scenario may be sparse; that is an evidence gap, not absence of capable workshops.
2. **National footprint must come from branch records.** The 28 Auto2000-named SPKLU rows are a purposive charging subset, not the branch network. Missing branch geocodes must remain part of the coverage denominator and exclusions.
3. **Route all plausible alternatives, or disclose pruning bounds.** Selecting the Euclidean-nearest provider then routing only that pair does not identify the nearest provider by road time. A farther point may be reached faster. For any nearest-road claim, route all eligible destinations in the study margin, or use a conservative candidate set and explicitly report the approximation with a validation sample.
4. **No proxy demand denominator.** Origin-grid coverage is a share of sampled origin points. Population-weighted coverage describes residents. Neither is Toyota-owner or eligible paid-job coverage. Do not infer addressable market by multiplying these shares by provincial registered-car totals.
5. **Do not invent time estimates.** Default OSM speed inference or a constant speed generates a scenario, not traffic measurement. Preserve speed rules, road class and default imputation. If hosted routing fails, road-distance results remain useful, but distance divided by arbitrary speed must not appear as verified drive time.
6. **Study extent cannot censor destinations silently.** Include a margin and audit near-boundary origins. A provider just outside an administrative area must remain eligible. Route failures must not become zero travel time, zero alternatives or automatic unserved status.

## High-priority design requirements (P1)

- Freeze market-selection criteria before choosing the final cases. Data feasibility and commercial relevance require separate columns. A transparent purposive case selection does not support generalising descriptive shares to Indonesia.
- Distinguish missing, unknown, no, explicitly excluded and not applicable in the service evidence schema.
- Preserve original and alternative coordinates, branch-centre vs vehicle-entrance status, source date and public verification status. Official map links do not prove field-accurate entrances.
- Origins on water, inaccessible terrain or outside the road network require explicit removal rules. An equal-area grid should use metric spacing, not unadjusted degree spacing across markets.
- Distinguish origin-to-provider routes from provider-to-origin routes. One-way roads can change rankings. Ensure the route direction matches the customer journey.
- Do not count duplicate representations as separate choice. Deduplicate node/way/relation and cross-source candidates using evidence; preserve ambiguous near-neighbours separately with sensitivity analysis.
- Bounded Overpass requests must retain query, endpoint, bounds, retrieval status and date. Coverage differences can reflect mapper activity, not provider density.
- Document Overture/OSM source overlap. Two databases may repeat the same upstream record and are not independent corroboration.
- Opening hours, Toyota specialisation, oil service and brake service cannot be inferred solely from a name. State exact classification rules and example counterexamples.
- Exclude sales-only dealers from the workshop-destination pool unless service is documented. If all branches have a general corporate service statement, label that evidence level rather than claiming branch-job verification.
- Distinguish petrol, HEV/PHEV and BEV jobs. A general Toyota repair listing is insufficient evidence of HV battery diagnostics or a manufacturer warranty route.
- A weak public quote comparison is not evidence of a competitive price gap. Distinguish time-stamped official tariffs, estimates, promotional prices and model-specific final offers.
- Reuse SPKLU and BPS source limitations, especially the June 2026 snapshot, uncertain live access, historical 34-province codes, Papua pooling and unexplained stock discontinuities.

## Adversarial tests required before conclusions

| Test | How to challenge the result | Failure interpretation |
|---|---|---|
| Qualified-provider filter | Compare all car-repair candidates with named/documented Toyota job providers | A large shift means the broad map cannot support equivalent-service claims |
| Nearest-route correctness | For a fixed sample, compare the chosen destination against every eligible destination in a generous margin | Changed destination/rank invalidates an unqualified nearest claim |
| Boundary extension | Expand destination bounds, recompute edge origins | Changes indicate extent-induced gaps |
| Coordinate leverage | Substitute official alternatives and perturb uncertain coordinates within a justified range | Sensitive branch rankings need investigation |
| Origin representation | Shift the grid and compare representative-point origins where available | Changes reveal a modifiable-area/origin effect |
| Routing direction | Compare outbound and reverse journeys for a diagnostic sample | Large asymmetry requires direction-specific reporting |
| Missing-route handling | Recompute summaries with route failures visibly excluded and separately bounded | Conclusions relying on failures are unsupported |
| Unmapped-provider sensitivity | Evaluate explicit additions/removals of a few verified public providers | A sparse inventory can be dominated by missing records |
| Duplicate sensitivity | Compare strict deduplication and unresolved-neighbour scenarios | Choice counts may be unstable even if access is stable |
| Threshold dependence | Show continuous distributions plus 10/20/30-minute thresholds | A binary 20-minute conclusion alone hides marginal cases |
| Market feasibility confounding | Compare screening scores excluding data completeness | A data-rich winner is not necessarily commercially attractive |
| Denominator integrity | Reconcile all origin and destination counts at every filter | Shares must have a recoverable denominator |

## Acceptance checklist for the independent final review

- [ ] Each numerical finding links to an included table and source provenance.
- [ ] Every map identifies bounds, coordinate system or scale, legend, source dates and the measured unit.
- [ ] Every origin has a unique ID and explicit inclusion/routing status.
- [ ] Every provider has a unique project ID, upstream IDs and capability evidence status.
- [ ] All nearest-provider claims pass the route-candidate audit or are labelled approximations.
- [ ] Travel-time assumptions and routing dates are preserved.
- [ ] Missing/failed routes are reported independently.
- [ ] Capability-filtered and broad-provider results remain distinct.
- [ ] No review/customer-account collection entered the analysis.
- [ ] No market-demand, uptake or profit estimate is derived from access alone.
- [ ] All planned-versus-achieved differences are disclosed.
- [ ] Raw/clean/derived data and code are packaged with rights and provenance notes.
- [ ] Interactive maps have clearly stated offline/online dependencies.
- [ ] PDF conclusions distinguish findings, interpretations and proposed tests.

## Critical epistemic boundary

The study observes public representations of places and services, then models travel over a road representation. It does not directly observe service fulfilment. The decisive uncertainty is therefore not only spatial error: it is the relationship between a documented destination and an actually deliverable, appropriately priced job. A successful geographic analysis should make that boundary visible rather than converting complete-looking maps into commercial certainty.
