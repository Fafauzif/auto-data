# Seven visual data pages
Each page has one main chart, a short body and one visible evidence limit. Exact chart numbers and source hashes are in `data_story.json`. The visual-reference PDF supplies no research data.

## DATA_STORY_01: Nearby depends on which sites we count

**Takeaway:** The 5 km result holds up. The 1 km result changes sharply.

Across 28 Auto2000-name locations, a conservative map filter cuts nearby options within 1 km from 20 to 8. At 5 km, the count changes only from 27 to 26. The nearest-option median rises from 0.323 to 1.413 km. This shows that close-range convenience depends on which sites we count. The filter still does not verify whether a driver can use them.

**Main visual:** grouped_bar: How many of 28 locations have another mapped option nearby?.

**Keep visible:** The filter uses operator and venue names. It does not verify access, connector compatibility, opening hours or uptime.

**Chart note:** Original source coordinates. All distances are straight-line; 28 name matches are not the full Auto2000 branch network.

**Source:** workstreams/extension_geography/nearest_scenario_summary.csv

Body length: 61 words.

## DATA_STORY_02: One published location differs by 55 km

**Takeaway:** Check the location before trusting a proximity score.

We compared five charging-source points with current official branch directions. Four pairs are within 135 metres. Balikpapan Sudirman differs by 55.26 km. Replacing that point changes the nearest-site result, so a broad map summary can hide a local problem. This comparison identifies a published-data conflict. It does not tell us where the charger was physically located on either date.

**Main visual:** horizontal_bar: Distance between two published map points.

**Keep visible:** Official branch directions are a second published source, not field confirmation of charging hardware.

**Chart note:** Charging-source snapshot: 16 June 2026. Official branch pages checked: 11 November 2026. Preserve both coordinate versions.

**Source:** workstreams/datasets/five_branch_coordinate_crosscheck.csv

Body length: 59 words.

## DATA_STORY_03: A boundary mismatch changes the provincial leader

**Takeaway:** West Papua falls from rank 1 to rank 10 after boundary alignment.

The charging source uses older provincial boundaries. The 2025 vehicle table separates four newer Papua provinces. A direct code match drops 70,800 cars from the denominator. Pooling those provinces back into the older boundaries lowers West Papua’s ratio from 48.80 to 19.19 and Papua’s from 22.68 to 13.44. The original apparent ranking depended on a mismatched join.

**Main visual:** dumbbell: Mapped sites per 100,000 passenger vehicles.

**Keep visible:** These ratios use all passenger vehicles, not BEVs; boundary alignment does not measure charging adequacy.

**Chart note:** June 2026 mapped sites divided by 2025 BPS/Polri stocks. This corrects the first-wave direct-join interpretation.

**Source:** workstreams/extension_geography/province_ratio_scenarios.csv; workstreams/extension_geography/boundary_stock_conservation.csv

Body length: 57 words.

## DATA_STORY_04: Four charging counts mean four different things

**Takeaway:** A site count is not a capacity measure.

The same source contains 2,454 station records, 3,767 charger-box records, 7,593 reconstructed charger units and 4,665 connectors. These quantities describe different levels of the source data. They cannot be added or substituted for one another. None tells us how many compatible vehicles can charge at once today. Choosing a different unit can also change provincial rankings.

**Main visual:** unit_cards: Keep each number attached to its unit.

**Keep visible:** Hardware counts do not establish usable power, simultaneous charging capacity, vehicle compatibility or uptime.

**Chart note:** Source snapshot: 16 June 2026. Exact coordinate duplicates were already consolidated by the source.

**Source:** workstreams/extension_geography/ROBUSTNESS_SUMMARY.json; workstreams/extension_geography/province_rank_sensitivity.csv

Body length: 56 words.

## DATA_STORY_05: 56 million values still cannot validate a health certificate

**Takeaway:** The missing reference matters more than the row count.

One historical Audi in California supplies 56.5 million stored electrical and BMS signal values. They support signal analysis, not a Toyota health certificate. The paper’s capacity reference is withheld. Current and voltage share a clock in all five bundles, but SOC does so in only two and temperature in none. The measurements need careful alignment before any health claim can be tested.

**Main visual:** horizontal_bar: Signals sharing the current clock exactly.

**Keep visible:** Counts exclude clocks and epoch metadata. Values are not independent customers, trips or synchronized rows.

**Chart note:** Five folder windows from a single Audi e-tron, 2019–2020. SOC means state of charge, not state of health.

**Source:** workstreams/extension_battery/BATTERY_SUMMARY.json; workstreams/extension_battery/bundle_signal_audit.csv; workstreams/extension_battery/scalar_count_receipt.csv

Body length: 62 words.

## DATA_STORY_06: A simple integration mistake adds 47.5% to the result

**Takeaway:** Do not treat days between logs as measured driving.

Across five bundles, the one-second gap rule retains 51.97 supported hours. Folder16 alone spans 50.82 calendar days, yet contains only 17.19 such hours. Bridging every gap inflates Folder2’s absolute terminal integral from 156.206 to 230.433 kWh. The extra 47.52% comes from an unsupported calculation across missing intervals. The tested 1-, 30- and 300-second limits agree here.

**Main visual:** bar: Drive Folder2: the effect of bridging long gaps.

**Keep visible:** This is a signed-signal throughput calculation, not battery capacity, charger wall energy, efficiency or a production-system failure.

**Chart note:** Absolute integral adds positive and negative energy magnitudes. Current and voltage clocks match in these files.

**Source:** workstreams/extension_battery/gap_aware_signed_integrals.csv; workstreams/extension_battery/BATTERY_SUMMARY.json; workstreams/extension_battery/bundle_signal_audit.csv

Body length: 56 words.

## DATA_STORY_07: Four partial-charge slopes are not four health scores

**Takeaway:** A partial charge cannot become a health score without validation.

Four supported charge intervals give 1.570 to 2.195 Ah per reported SOC percentage point. Their current, temperature and SOC windows differ. Every stored current value lies on an integer-ampere grid, but the sensor’s accuracy bound is unknown. These ratios describe the selected intervals. Rescaling them into battery capacity or state of health would add an assumption this dataset cannot validate.

**Main visual:** bar: Observed charge per reported SOC percentage point.

**Keep visible:** Four nonrandom intervals from one vehicle cannot establish degradation, capacity, health-score accuracy or a temperature effect.

**Chart note:** SOC is state of charge. Common observed support only; no endpoint extrapolation. The health reference is not public.

**Source:** workstreams/extension_battery/charging_interval_soc_slope_diagnostics.csv; workstreams/extension_battery/current_numeric_resolution_audit.csv

Body length: 60 words.

## Quality checks

26 checks passed; zero failed. Counts, coordinate offsets, rank changes, signal units and exact source values reconcile. All seven bodies contain at most70words. No PEF data were imported.
