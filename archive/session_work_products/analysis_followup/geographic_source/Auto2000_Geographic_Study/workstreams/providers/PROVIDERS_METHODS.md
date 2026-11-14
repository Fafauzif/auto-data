# Public provider discovery: acquisition and interpretation

## What was collected

The Overture Maps Places release `2026-10-21.0` was queried on 14 November 2026 for fifteen deliberately bounded Indonesian urban windows. The release was selected from the accessible Overture STAC catalog's `latest` field. Acquisition was through the official `overturemaps` Python client and anonymous AWS S3; the explicit environment proxy was necessary because the default S3 client could not resolve its hostname in this runtime.

This is a current-release source inventory, not current field confirmation. An Overture release date, source-specific update date, acquisition date and actual business-operating date are different quantities.

For four deep-dive windows, the destination search rectangle extends 0.08 degrees in each direction beyond the core origin rectangle. The other eleven screening rectangles have no such margin and are not used to claim complete metropolitan catchments. All coordinates and rectangles are WGS84 longitude/latitude. Exact windows appear in `study_windows.json`.

The client reads remotely hosted GeoParquet using the bounding-box filter. It does not download the full worldwide Places dataset. The saved source extracts retain automotive-related records and their source attribution. These are **selected, reserialized upstream rows**, not byte-identical copies of upstream worldwide parquet files. Emails, telephone numbers and social-account fields were deliberately not collected into these extracts because they are unnecessary for geographic analysis. Business name, address, website, geometry, taxonomy, confidence, operating-status and provenance fields are retained.

## Overpass fallback record

Six Overpass endpoints were tested. The main global endpoints returned HTTP 406, 403, 503 or timeouts. A Swiss regional endpoint returned a successful empty response for the Indonesian test window; this was treated as geographic noncoverage and NOT as evidence that Indonesia had no workshops. The exact query, times, status and responses are in `endpoint_probe_log.json` and `probe_*.json`. Overture therefore became the achieved inventory source. No OSM/Overture dual-source corroboration or exhaustive provider census is claimed.

## Broad source extraction

The extraction includes primary categories automotive_repair, automotive_service, auto_body_shop, auto_glass_service, tire_dealer_and_repair, tire_shop, brake_service_and_repair, oil_change, oil_change_station, auto_restoration_service, auto_customization, auto_dealer, used_auto_dealer, commercial_vehicle_dealer, auto_parts_store, motorcycle_repair and motorcycle_dealer. Names matching Auto2000 or OtoXpert are included even when their category differs. The broad extraction is retained so motorcycle, dealer, parts-only and uncertain source records remain inspectable instead of disappearing silently.

## Conservative generic-candidate filter

An eligible generic repair/service candidate must:

1. Have a general repair/service or oil/brake primary category, rather than dealer, parts-only or specialist-only category.
2. Have source confidence at least 0.70.
3. Not have an explicit motorcycle category or selected explicit motorcycle-name indicators (for example AHASS, bengkel motor, sepeda motor, Vespa or Yamaha).
4. Not have an Auto2000/OtoXpert network-name match.
5. Not have a selected car-brand token, because independence or willingness to service Toyota cannot be established from that name.
6. Not have truck/bus/trailer-oriented name indicators.
7. Not be source-labelled closed/permanently_closed.
8. Not be a probable same-name duplicate within 75 metres of a higher-confidence retained record.

The exclusion decision and reasons remain at record level. Source confidence is an Overture/source model field. It is NOT this study's measured probability that a garage exists, is independent, services cars, accepts Toyota or performs an oil or brake job.

**Every candidate remains unverified for a Toyota model and a specific job.** This filter is a conservative heuristic scenario, not a verified competing-workshop sample. Ambiguous names such as 'X Motor' remain ambiguous and receive an explicit flag. Some car garages may be lost through brand exclusions; some motorcycle or non-comparable businesses may remain. False positives and false negatives both matter.

Two sensitivity indicators are supplied: explicit car-name evidence (literal mobil/car/cars) and source confidence at least 0.90. Literal car names provide stronger text evidence for passenger-car orientation, but still do not establish a job, parts, opening hours or operating status. There is no defensible conversion from candidate count into demand, capacity or willingness to switch.

## Deduplication and network-name caution

Within each market, the same normalized business name within 75 metres is flagged as a probable duplicate, preserving every record and its chosen reference. Different names at one coordinate are not automatically duplicates. Overture GERS IDs are source feature identities, not verified physical establishments.

Auto2000-name Places records may represent sales agents, marketing listings, duplicates or actual branches. They are not a branch census. Use the separately researched official branch inventory as network destinations.

## Comparison and selection limits

Raw provider counts across the fifteen screening windows are not a market-attractiveness ranking: rectangles differ in area and the source has unequal mapping completeness. Per-area counts describe mapped candidate density, not actual establishment density or Toyota customer demand. The four deep dives permit comparison of bounded origin samples, not generalization to the entire named metropolitan populations.

## Files and reproducibility

- `acquire_overture.py`: source retrieval; requires internet, overturemaps and pyarrow.
- `build_inventory.py`: deterministic classification and duplicate flags from saved source extracts; requires pyarrow and shapely.
- `provider_qa.py`: input and classification summaries; requires pandas and pyproj.
- `raw/*_automotive_source.parquet`: selected upstream source rows and attribution.
- `provider_inventory.csv` and `.geojson`: normalized complete candidate inventory.
- `screening_metrics.csv`: bounded-window metrics and limitations.
- `PROVIDER_QA.json`: achieved record counts, identifier and coordinate checks, source/license distributions.
- `overture_acquisition_log.json`: per-window request details and output hashes.

Dependencies installed into the temporary `deps` directory and debugging downloads are implementation intermediates and should not be included in the user ZIP. The thirteen collected source columns are the declared source extraction; no missing telephone/email/social field is needed to reproduce the reported geographic outputs.

## Attribution and rights

Overture Maps Foundation and contributing providers. Places release 2026-10-21.0. See https://docs.overturemaps.org/attribution/ and https://docs.overturemaps.org/getting-data/ . Per-record source license fields are preserved, including CDLA-Permissive-2.0, Apache-2.0 and CC0-1.0 where present. Source records commonly originate with Meta; these are not independent field checks by this project. Overture license information does not establish underlying businesses' job capability. OpenStreetMap Overpass API documentation: https://overpass-api.de/ .

## Additional official Shop&Drive layer

A later successful direct retrieval of https://www.shopanddrive.com/outlet yielded 425 business records in the page's inline `var outletCoordinates` JSON. These are observed directory records, not a separately reconciled national outlet total. All have numeric coordinates within Indonesia's broad bounds; no exact duplicate coordinate pairs occur. The directory provides 282 records within the fifteen study rectangles, including 67 within the four expanded deep-dive destination windows: Surabaya 28, Medan 8, Bandung 22 and Palembang 9.

`shopanddrive_official_all.csv` retains all 425 selected business facts; `shopanddrive_official_study.csv` retains the 282 study-window records. `shopanddrive_official_focal8.csv` is a purposive eight-record evidence illustration and MUST NOT be used as a complete network-access inventory. `shopanddrive_source_receipt.json` records the captured page's hash and byte count. The full website HTML is an internal acquisition cache and is not redistributed. `extract_shopanddrive.py` reacquires that page if the cache is absent; otherwise deterministic analysis can use the included structured facts directly.

These are **official-directory coordinate candidates**, not field-verified entrances. The Overture and official coordinates sometimes differ materially; for example the Lontar listing differs by approximately 227 metres. Official branch identity and network-level service descriptions are stronger evidence than a generic Places category, but do not establish stock, current opening, exact Toyota-model oil/filter fitment, today's quote, appointment availability or completed work. The branch workstream documents the scope of network/local service evidence. Shop&Drive is an Astra-related alternative channel; capturing work there does not automatically generate Auto2000 gross profit.
