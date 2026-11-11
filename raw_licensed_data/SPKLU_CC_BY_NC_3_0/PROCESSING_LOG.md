# SPKLU dataset - processing log (version 2.0)

- Source: petaspklu.id `/api/v1/spklu/all`, operated by Solopos with underlying data from PT PLN. Retrieved 2026-06-16.
- Raw records: 3,029 stations, 4,707 charger boxes, 9,781 chargers, 5,947 connectors.
- After duplicate resolution: 2,454 unique physical sites, 3,767 charger boxes, 7,593 chargers, 4,665 connectors, 89,871 kW installed as the sum of max_box_power_kW.
- Administrative coverage: 34 provinces under the pre-2022 structure. The crosswalk holds 375 regency or city name entries mapping to 373 distinct 4-digit BPS codes. After duplicate resolution 374 names and 372 codes still carry at least one station.

## Transformations
1. Recomputed station charger and connector totals from the underlying boxes. Raw totals were 0 for every station.
2. Parsed free-text `watt` values into numeric kW and assigned a standardized power tier.
3. Normalized province names to the 34 official 2-digit BPS province codes.
4. Normalized regency names from 'Kab/Kota X' to official style with admin_level, then matched them to 4-digit BPS codes using Permendagri 72/2019 and the emsifa/api-wilayah-indonesia master.
5. Inferred AC or DC from the charger-box name where stated and left it blank otherwise, which applies to 829 of 3,767 boxes.
6. Screened coordinates against provincial bounding boxes. The screen flagged 17 stations for review and deleted none.
7. Resolved duplicates. Identical-coordinate sites were clustered first, covering 53 surviving stations. Within each province, station pairs within 1 km were scored on normalized name similarity at weight 0.4 and address similarity at weight 0.6, each the maximum of token-sort and token-set ratios. Pairs scoring 75 or above were merged by union-find together with the co-location clusters. The lowest station_id survives and keeps its own attribute values. Provenance is written to merged_from_station_ids and n_merged. 366 surviving records absorbed at least one other and the largest cluster covers 14 raw records, reducing 3,029 records to 2,454 sites.
8. Enriched the resolved table spatially. The five nearest stations by haversine distance were queried against the public OSRM Table service on the driving profile over the OpenStreetMap road network. The shortest road distance became nearest_road_km alongside the neighbour's id and name. Station counts within 1, 3 and 5 km came from a straight-line search, with densities computed as count divided by pi*r^2.
9. Joined province indicators and computed coverage metrics. Population is the official SP2020 census and GDP is PDRB ADHB 2025. Per-province BEV counts were unavailable.
10. Derived provider_type, operator_brand and location_type name-first from the station name. The address was consulted only for the high-precision phrases REST AREA, BANDARA and RUMAH SAKIT.

## Quality flags present
- station_charger_count_recomputed: 2,454
- co_located: 53
- coord_review_outside_footprint: 17
- alamat_empty: 3

## Limitations
- provider_type and location_type are heuristic keyword classifications derived from the station name. 'PLN / SPKLU network' is the default for the un-tagged SPKLU brand and may include unlabelled third-party sites. About 21% of sites fall in 'Other / Unclassified' because the name refers only to a specific business or development.
- status_active is uniformly 1. The source publishes active stations only, so this release is a single snapshot with no closures or time series.
- The coordinate check is a plausibility screen rather than point-in-polygon validation. Authoritative validation would require official BPS boundary shapefiles.
- Population is the official SP2020 census, sum-verified to the national total of 270,203,917. GDP is nominal PDRB ADHB 2025 taken from a secondary compilation rather than the primary BPS table. Per-province BEV registrations are unavailable, so chargers_per_1000_bev is empty.
- Duplicate resolution can merge genuinely distinct sites that share very similar names and nearby addresses, and can miss true duplicates named very differently. All merges are logged in merged_from_station_ids.
- Road distances came from the public OSRM demonstration server, which is intended for lightweight use.
- Density radii of 1, 3 and 5 km are a fixed choice of spatial scale.
