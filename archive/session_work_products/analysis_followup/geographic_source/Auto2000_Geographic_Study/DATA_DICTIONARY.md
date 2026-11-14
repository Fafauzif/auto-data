# Data dictionary and evidence units

## Primary entities
- Directory card: one returned official city-page service card. Repeated page cards are not extra branches.
- Reconciled Auto2000 entry: unique normalised name+coordinate candidate under the documented reconciliation; not necessarily an independently verified physical site.
- OtoXpert entry: official directory listing with operator label and embedded-map candidate.
- Shop&Drive entry: row of the official directory's structured location data. Published location/operation is not field verification.
- Overture place: unique GERS place ID in a frozen Places release. Selected automotive categories are source classifications, not verified technical capability.
- Grid origin: analyst-generated cell centre; a calculation location, not a person/vehicle/customer.
- OD pair: one modelled origin-destination comparison. Thousands of pairs do not add source observations.
- Route illustration: selected returned path geometry; examples are chosen by gap position, not sampled journeys.
- Programme/network service evidence: published issuer claim, distinct from current outlet/model/job fulfilment.

## Coordinates and boundaries
WGS84 longitude/latitude in decimal degrees. OSRM inputs use longitude,latitude. Distance outputs metres; duration outputs seconds unless a field explicitly ends in minutes. Geographic bounding boxes follow west,south,east,north. Destination rectangles expand origin windows by0.08degrees each side; that is an angular margin, not a guaranteed travel-distance catchment. Local map scale bars are approximate straight-line distance references.

## Provider inventory
`id`: Overture GERS ID. `market`: named analytical window. `primary_category`: source category. `eligible_candidate`: heuristic retained repair/service record; does not mean independently owned, Toyota-compatible or job-qualified. `exclusion_reasons`: transparent filter flags. `confidence`: source classification/place confidence, not car/job probability. `explicit_car_name`: literal word evidence sensitivity. `duplicate_of`: matching decision where used. `in_core`: falls inside origin rectangle. `source_release`, `source_datasets`, `source_license`: upstream provenance; most share meta/Overture origin. No phone/email/contact database is delivered.

## Routing
`kind=independent` is an internal legacy code for the retained generic mapped candidate pool. Interpret it as 'mapped repair/service candidates', not verified independence or competence. `auto2000`: documented general-workshop location; specific job unverified. `otoxpert`: official network listing; outlet/model/stock/slot unconfirmed. Supplementary kinds identify official Shop&Drive, selected DokterMobil, and observed other-authorised Toyota locations.

`duration_seconds`: returned OSRM-profile route duration, not live observed traffic or minimum-time guarantee. `distance_metres`: length of that returned route. `origin_snap_metres`/`destination_snap_metres`: model snapping displacement. `scenario=all_routed`: all successfully routed retained OD options. `scenario=snap_le_250m`: excludes excessive snapping according to implementation. `matrix_complete`: whether every intended destination comparison returned for origin; inspect failures and nulls.

`auto2000_minus_mapped_independent_seconds`: origin-level Auto2000 duration minus mapped-candidate duration. Positive means Auto2000 longer in this model. Median paired gaps do not equal difference of marginal medians in general. `count_le_*min`: count of listed routed destinations inside threshold, not service capacity. `documented_alternative_valid_origins=0`: no identified strict job-capability comparator under study evidence, not zero capable garages.

Official oil-network composite is nearest across collected OtoXpert and Shop&Drive locations only. DokterMobil local oil-service claims are separate because scope may differ. Other authorised Toyota coverage is purposive, not exhaustive.

## Scope exclusions
No demand estimate, owner locations, workshop quality rating, customer sentiment league table, price-premium estimate, live queues, appointment availability, causal switching or profit effect. No synthetic customer observations. See each workstream's methods and source registry for exact transformations.
