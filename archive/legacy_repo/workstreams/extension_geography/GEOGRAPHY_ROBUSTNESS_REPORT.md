# Mapped proximity is robust at 5 km, but it does not establish a usable charging alternative

The earlier charging-directory argument needs a narrower conclusion. Across the 28 Auto2000-name records in this source, nearby mapped locations remain common after removing many questionable alternatives. However, the one-kilometre result changes sharply, and current access cannot be established for any candidate from this dataset. The evidence leaves the incremental customer value of a directory unproved. It does not prove that a directory has little value.

This extension uses existing data only. It adds 25 nearest-alternative scenarios, 695 anchor-scenario rows, provincial unit/boundary/year sensitivities, near-coordinate clustering, a prospective analysis specification and an independent methods challenge. These are derived calculations, not additional scraped reviews, charging sites or customer observations. The specification was written before the new scenario outcomes were computed, with the known first-wave findings and preliminary schema/boundary observations disclosed in `PREREGISTRATION.md`.

## 1. Candidate filtering barely changes the 5 km headline but changes close-range convenience

The source has no verified access, opening-hours, connector-compatibility or live operational field. Its provider and venue classifications derive primarily from location names. All 2,454 rows have `status_active=1` because the source included stations reported active. That is an inclusion characteristic, not a June-to-November uptime audit.

The alternative pools exclude all 28 Auto2000-name anchors. The Toyota-oriented rule retains explicit Toyota-and-Lexus restrictions for a Toyota driver but excludes other explicit restrictions. The network proxy retains PLN/SPKLU and independent CPO classifications, removing dealers, unknown providers and explicit restrictions. Its conservative venue subset retains utility facilities, retail/F&B, malls, rest areas, public/tourism spaces and transport facilities. These remain name-derived proxies. A utility location may still have gates, and a mall may require parking or payment.

| Original source coordinates | Candidate sites | Anchors within 1 km | Within 3 km | Within 5 km | Median nearest distance |
|---|---:|---:|---:|---:|---:|
| All mapped non-Auto2000 alternatives | 2,426 | 20/28 | 26/28 | 27/28 | 0.323 km |
| Remove explicit restriction wording | 2,299 | 18/28 | 26/28 | 27/28 | 0.705 km |
| Toyota-compatible restriction wording | 2,329 | 18/28 | 26/28 | 27/28 | 0.705 km |
| PLN/CPO network proxy | 2,076 | 15/28 | 26/28 | 26/28 | 0.837 km |
| Network plus conservative venue proxy | 1,051 | 8/28 | 25/28 | 26/28 | 1.413 km |

The strict proxy raises the median distance 4.38-fold and moves five anchors at least 2 km farther from their nearest retained candidate. The prospectively specified descriptive falsification rules did not trigger: 26 anchors retained a candidate within 5 km, above the 21-anchor threshold, and five rather than six experienced increases of at least 2 km. These analyst-set thresholds describe robustness. They are not validated customer-value thresholds, population tests or proof of strategic attractiveness. The continuous changes and the one-kilometre contrast matter more than a binary pass label.

The largest change occurs at Auto 2000 Amplas Medan: its all-mapped alternative is 3.299 km away, while the conservative proxy's nearest location is 7.734 km away. Kelapa Gading changes from 0.151 to 3.458 km. Tanjung Api-Api changes from 0.215 to 2.658 km. HR Mohammad Surabaya rises by 1.996 km, just below the specified 2 km threshold. This last case illustrates why the threshold should not hide nearly equivalent cases.

There are 140 explicit restriction-marker names, including 43 Toyota-and-Lexus restrictions. Thirteen of those 43 are Auto2000-name anchors, leaving 30 additional candidates under the Toyota-oriented rule. Excluding all brand restrictions therefore excludes some potentially compatible locations for the target driver. Conversely, allowing Toyota wording establishes neither connector compatibility nor admission today.

The count of anchors with **confirmed currently accessible** alternatives is not identified. A lower bound supported by verified-access evidence is zero; that means the evidence does not verify access, not that zero sites are usable. Conditional on the source coordinates and listed locations, the all-mapped 27/28 is only an optimistic upper bound for usable listed alternatives within 5 km. Unlisted alternatives may exist.

## 2. Known coordinate problems affect the outlier, while the access-proxy contrast remains

Removing all 17 source-coordinate-flagged candidate rows changes none of the 28 nearest-candidate distances in any pool. This does not validate the retained coordinates. The known Balikpapan discrepancy was not caught by that broad source flag.

Substituting the five independently collected official branch-direction candidate coordinates changes the all-mapped result to 28/28 within 5 km and a 0.285 km median. The conservative pool gives 27/28 within 5 km, 9/28 within 1 km and a 1.254 km median. The Balikpapan extreme disappears, but the short-distance filtering penalty remains. These are labelled substitution scenarios. An official branch direction is not field confirmation of the charging hardware location or a correction of historical reality.

Omitting the conflicted Balikpapan anchor instead gives 27/27 within 5 km for the all-mapped pool and 26/27 for the conservative proxy. The remaining conservative-pool maximum is Amplas Medan at 7.734 km. This shows that the strict-pool exception does not depend solely on the suspect Balikpapan coordinate.

All new distances are independently calculated great-circle distances. For correctly identified locations, these provide lower bounds on road travel distance. They cannot be converted into driving minutes, taxi cost, detours, queue time or charging time without additional route and operational information. The source's original nearest-road field solves a different unfiltered nearest-site problem and was not reused as a filtered-route result.

## 3. Sites, boxes, reconstructed units and near-coordinate clusters are different quantities

| Recorded quantity | Count | Interpretation |
|---|---:|---|
| Consolidated station rows | 2,454 | Source station identifiers |
| Exact distinct coordinate pairs | 2,454 | No residual identical-coordinate row pairs |
| Charger-box rows | 3,767 | Distinct source hardware records |
| Source reconstructed charger units | 7,593 | Source counts summed across boxes |
| Source connectors | 4,665 | Source connector counts, not simultaneous service capacity |
| Original source entries represented | 3,029 | Historical entries consolidated into current station rows |

The source already consolidated its exact co-location groups. Fifty-three surviving rows have a co-location flag. Subtracting those 53 again would double-deduplicate the source.

Connected-component grouping within 20, 50 and 100 metres yields 2,433, 2,418 and 2,376 location clusters, respectively. The reductions from the site count are 0.86%, 1.47% and 3.18%. These are proximity components, not verified duplicate facilities. The 100-metre rule places 152 rows in multi-site components and creates 14 components containing more than one province label. Fifteen cross-province station pairs are within 100 metres. Border-adjacent facilities and administrative/coordinate disagreements are both possible. No boundary adjudication was performed. Province-specific component counts therefore cannot simply be added and treated as the same quantity as global components.

Changing from sites to charger-box rows also changes provincial rankings. With the same pooled 2025 passenger-stock denominator, Kalimantan Selatan moves from rank 25 to 17, while Kalimantan Barat moves from 7 to 13. DKI Jakarta moves from 8 to 3. These results reflect different hardware-record intensity per mapped site. They do not establish power, compatibility, concurrent capacity or adequacy. The maximum absolute rank shift is eight places.

## 4. The 2025 Papua denominator needs explicit boundary pooling

This is a correction to the interpretation of the first-wave direct 34-code join. The charging source uses 34 historical provinces. BPS publishes separate nonmissing 2025 passenger stocks for Papua Barat Daya, Papua Selatan, Papua Tengah and Papua Pegunungan. The direct join omits 70,800 passenger vehicles, 0.339% of the national published 20,907,972 total.

The old-boundary scenario pools code 92 into 91, and codes 95/96/97 into 94. It conserves the full national stock. This is a boundary-alignment scenario, conditional on the charging source's stated historical coverage; a source row's province label is not itself a spatial boundary validation.

| Historical source area | Direct-join denominator | Pooled denominator | Direct sites per 100,000 cars | Pooled ratio | Rank before/after |
|---|---:|---:|---:|---:|---:|
| Papua Barat | 16,392 | 41,685 | 48.80 | 19.19 | 1 → 10 |
| Papua | 66,130 | 111,637 | 22.68 | 13.44 | 9 → 19 |

The aligned ratios are 60.68% and 40.76% lower, respectively. Other province-level ratios are unchanged, although their relative rankings can shift. A direct-join map would otherwise suggest that Papua Barat leads this all-car-normalized measure. That conclusion depends on mismatched boundaries and should not be carried forward.

The 2023–24 BPS tables have missing child-province values and published parent totals, so pooling nonmissing values produces the same numerical denominator as the direct join for those years. Missing values do not mean that the child provinces had no vehicles. The year-specific reporting pattern must be preserved.

## 5. Denominator-year changes can dominate the apparent geography

Holding the June 2026 charging-site numerator fixed, the Jawa Timur ratio is 9.708 per 100,000 using the 2022 stock and 3.543 using the 2025 stock. This is not a change in charging infrastructure. It is driven by denominator changes, including the already noted 2022–23 discontinuity. DKI Jakarta changes from 13.173 to 21.267 under the same exercise; its passenger-stock denominator falls from 3.773 million in 2022 to 2.272 million in 2023.

An explicitly exploratory diagnostic identifies eight historical-boundary provinces with absolute published stock changes greater than 25% in 2022–23. Banten rises 282.0%, Jawa Timur 166.7% and Papua 163.7%; DKI Jakarta falls 39.8% and Jawa Barat falls 25.9%. These are changes in the published series. They do not establish organic fleet growth, re-registration flows, a known methodological break or a proven BPS error. The source evidence available here does not explain them. It is therefore unsafe to use these stock changes as a smooth demand-growth signal.

Removing source-coordinate-flagged sites makes modest changes to province ranks, with a maximum absolute shift of two places for the all-site ratio. That limited sensitivity is reassuring only about this particular flag-removal test. It cannot resolve unflagged city-scale errors, changing boundaries or access uncertainty.

## Implication and next evidence

The defensible statement is that many Auto2000-name source locations have other mapped charging locations nearby, including under conservative operator/venue filters. The stronger statement that customers already have a convenient usable alternative remains unsupported. Short-distance convenience, access rules, accurate directions, vehicle eligibility and current operating conditions are plausible information gaps. Whether solving them creates incremental Digiroom value requires observing those gaps and customers' use of existing official services, not another count of map points.

The next discriminating research would validate current admission, connectors, hours and route distance at the filtered-out or materially farther alternatives around the six largest distance-penalty anchors, including the 1.996 km near-threshold case. A customer task comparison against existing directories could then measure wrong-destination risk, decision time and successful arrival. Those tests are proposed research, not performed observations or an implementation recommendation. Current data cannot support BEV demand, uptime, plug-capacity, willingness-to-pay or commercial ROI claims.

## Reproduction and attribution

Run `python workstreams/extension_geography/robustness.py` from the package root with Python, pandas, numpy and matplotlib installed. The script reads existing raw SPKLU files and existing BPS/official-direction tables; it makes no network requests. `ROBUSTNESS_SUMMARY.json` records SHA-256 hashes. `station_classification_receipt.csv` makes every heuristic membership visible. The anchor scenario table and province scenario tables preserve original and alternative scenarios rather than overwriting the first wave.

SPKLU source: Wiputra, R. and Santiadi, S. (2026), *A Geospatial Dataset of Public Electric Vehicle Charging Infrastructure in Indonesia*, Mendeley Data V2, snapshot 16 June 2026, DOI [10.17632/z2bvd5r574.2](https://doi.org/10.17632/z2bvd5r574.2), CC BY-NC 3.0. This extension is an original derived analysis and retains that noncommercial source qualification. BPS/Polri annual source URLs are preserved per row in `workstreams/datasets/bps_vehicle_stock_long.csv`. Official branch page/map URLs and capture request IDs are in `workstreams/datasets/five_branch_coordinate_crosscheck.csv`. Names and classifications do not establish an exhaustive branch or charging network. The figures have been visually inspected by the analysis agent; no human field validation is claimed.
