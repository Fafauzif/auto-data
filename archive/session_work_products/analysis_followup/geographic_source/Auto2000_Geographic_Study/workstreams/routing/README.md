# Road-access analysis

This pipeline measures modelled access from regular grid-cell centres to a finite inventory of mapped destinations. It does not observe customers, Toyota ownership, garage competence, demand, actual traffic, workshop capacity, appointment availability or completed paid work.

## Inputs

`route_analysis.py` uses the Python standard library. A JSON configuration contains `markets`, each with `market`, `bbox` in west/south/east/north longitude/latitude order, `grid_n`, and `destinations_csv`. Destination CSV fields are `destination_id,name,longitude,latitude,kind,capability_status,source_url`. Allowed `kind` values are `auto2000`, `independent`, `otoxpert`, `other_authorized`, `other`.

Destinations should extend beyond the origin rectangle. Every inventoried destination is included; no nearest Euclidean shortlist is substituted for a nearest road-time comparison. An unverified alternative remains a mapped alternative, not a job-qualified substitute.

## Run

`python route_analysis.py inputs/portable_config.json --output output --cache cache`

OSRM requests are cached by full-URL SHA256. Each table request uses at most 27 origins and 70 destinations and is rate-spaced by at least 1.1 seconds. Retries are bounded. The public server is suitable only for this bounded exploratory computation; for extensive repeat analyses, use an appropriate hosted or local service under its current terms.

## Outputs

- `od_pairs.csv`: directed origin-to-destination modelled seconds, road metres, straight-line metres, snap distances and route status.
- `origin_accessibility.csv`: nearest provider, alternative count at 10/20/30 minutes, paired travel burden, full-inventory completeness, and outside-core diagnostics.
- `market_summary.csv`: origin counts and descriptive medians. All denominators are regular grid origins, not people or customers.
- `snapping.csv`: raw returned road-snap positions and distances.
- `illustrative_routes.geojson`: minimum/median/maximum travel-gap examples, not an independent sample.
- `acquisition_log.json`: attempted URLs, dates, cache status and failures.
- `run_receipt.json`: counts, configuration hash and interpretation rules.

`all_routed` includes all returned routable points. `snap_le_250m` excludes an OD pair when either endpoint is snapped more than 250 metres. The latter is an analyst-set diagnostic, not a validated error threshold. Grid centres in water, secured compounds, disconnected spaces or outside settled areas can be distant from a road. Neither scenario turns the grid into a population sample.

Nearest destinations are calculated by returned duration among the routes supplied by the OSRM driving profile, not by OSRM `weight`. This does not guarantee that the selected path is the globally fastest path by duration when the profile routing objective differs from duration. The route profile, road graph and routing objective belong to the service snapshot. These are baseline road-network estimates, not real-time traffic observations. A table response may have null durations for unreachable pairs. A missing API batch is not interpreted as no providers; use `matrix_complete` and failure logs before drawing conclusions.

`documented_alternative` means the source documentation field explicitly says `documented`. It does not independently verify that the same job, parts, price, vehicle and appointment are available today. Empty documented pools are an evidence gap, not proof of absent capability.

## Boundaries

Core-only nearest times and full-inventory nearest times are compared. This diagnoses whether clipping at the origin rectangle would alter selected destinations, but cannot prove the expanded inventory captures every relevant outside destination. A nearest destination near the outer collection boundary needs further inspection.

## Attribution

Road network: OpenStreetMap contributors, ODbL, https://www.openstreetmap.org/copyright . Routing: OSRM, https://project-osrm.org/ . Retain source-specific place attribution in the destination inputs.

## Additional derived analyses

`derive_sensitivity.py` adds source-confidence, explicit-car-name, snap-distance, core-boundary, nested25 and central49 subset scenarios without new routing calls. Nested25 andcentral49 are subsets of the81 original points, not independently generated or shifted grids.

`branch_influence.py` derives27branch finite-grid catchments and12focal branches. Positive additional-time medians exclude increases<=1second. This is geographical leave-one-out sensitivity, not a closure or workload model.

`inputs/config.json` preserves the acquisition configuration and its original workspace paths. `inputs/portable_config.json` references destination filenames relative to its own directory and should be used after extraction. Change endpoint/service setup where required by future server availability.

## Supplement reproduction

`python supplement_routes.py inputs/portable_config.json inputs/supplement_destinations.csv --output supplement`

This routes all official Shop&Drive destinations in the four expanded windows plus separately evidenced DokterMobil and selected other authorised Toyota records. It joins the same original origins. `collected_advertised_oil_channels_nearest_seconds` is the minimum of OtoXpert and Shop&Drive only. DokterMobil is separate. These are advertised channel paths with exact Toyota/model/job/slot unconfirmed. Generic garage inventory and named-network scenarios can overlap and must not be summed as distinct businesses.
