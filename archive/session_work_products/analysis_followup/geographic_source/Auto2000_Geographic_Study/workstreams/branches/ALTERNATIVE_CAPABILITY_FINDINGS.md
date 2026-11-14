# Category filtering can miss genuine oil-service alternatives

The first broad competitor screen intentionally favours general-repair categories. That excludes some Shop & Drive records classified by Overture as auto_parts_store, although the chain's own FAQ advertises replacement work, engine oil and oil-filter products and lists Toyota among supported brands. A retailer category is therefore not equivalent to absence of workshop service. Conversely, a chain name alone cannot establish a current job on a particular Toyota model/year. This evidence supports a separate network-advertised oil-service scenario rather than relaxing every candidate's qualification.

## What was directly checked

Eight Shop & Drive locations were selected purposively, two per focal market. Their outlet names and street/unit numbers were checked in the official directory, then linked to matching Overture records. The subsequently retrieved official directory's embedded outletCoordinates supplied preferred routing candidates. The evidence register preserves Overture coordinates and the straight-line disagreements in metres; the chosen Lontar candidate differs by about 227 metres. Provider-published coordinates are not independently validated entrances.

| Market | Official Shop & Drive outlets checked |
|---|---|
| Surabaya | Lontar; Tidar |
| Bandung | Buah Batu; Sudirman |
| Medan | Jamin Ginting; Setiabudi |
| Palembang | Kenten; Plaju |

Three Dokter Mobil local pages were also checked: Lontar, Ngagel and Bandung. Each explicitly advertises oil changes and a local address. Its Cuci Darah treatment may have a different scope from a standard oil-and-filter job, and no selected Toyota model/year fitment or current price was established.

## Stronger historical job evidence has a date boundary

The official Shop & Drive New Year Deals page expressly marks its 1-31 January 2026 promotion expired. Its terms state all Shop & Drive/Super Shop & Drive branches, name Avanza and several other Toyota models for a specified oil-filter offer, and advertise Akebono brake pads with fitting. This provides historical network/model/job evidence. It must not be used as a November price, proof of current stock, current fitting availability or actual branch completion. The contemporary FAQ and outlet identity support a plausible network-advertised alternative, with exact eligibility still unconfirmed.

## Commercial interpretation

Shop & Drive is an Astra Otoparts/franchise brand, not an Auto2000 workshop. Recovering work from it can add Auto2000 contribution while potentially displacing contribution elsewhere in the wider Astra ecosystem. A group-level gain is not established by an Auto2000 gain. Outlet legal operator, ownership and GP recipient remain unverified. Dokter Mobil is a separate non-Auto2000 chain; legal outlet operators also remain unverified.

The eight-location subset is illustrative and incomplete, not the nearest eligible alternative throughout each city. A route to this subset answers how selected advertised alternatives compare, not the time to the nearest confirmed equivalent provider. Any market-wide comparison must preserve that restricted destination universe. The full official Shop & Drive extraction held by the provider workstream is a distinct source layer and not additional independent validation.

## Sources and reproducibility

All sources retrieved 14 November 2026. Public web retrieval may contain cached pages. No customer review, customer account, contact or booking was used.

* Official outlet identities and embedded coordinates: https://www.shopanddrive.com/outlet
* Network offering and Toyota coverage: https://www.shopanddrive.com/faq
* Expired historical terms: https://www.shopanddrive.com/promo/promo-new-year-deals
* Local oil advertisement and address: https://www.doktermobil.com/lontar/
* Local oil advertisement and address: https://www.doktermobil.com/ngagel/
* Local oil advertisement and address: https://www.doktermobil.com/bandung/

Run build_alternative_evidence.py after provider_inventory.csv and shopanddrive_official_focal8.csv are present. verified_alternative_evidence.csv and .geojson preserve scope and provenance. supplementary_routing_destinations.csv is the normalized routing handoff. Job-specific, current price and booking confirmation flags are false for all11records.
