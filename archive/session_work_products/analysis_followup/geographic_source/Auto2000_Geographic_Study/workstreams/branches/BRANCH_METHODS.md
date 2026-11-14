# Official branch inventory: facts, exclusions and interpretation

Acquisition date: 14 November 2026. Existing archive left unchanged. Direct requests to Auto2000 directory, sitemap and Surabaya directory returned HTTP 403. Public web retrieval supplied official city-directory service cards. These retrievals can be cached; retrieval today does not establish operational status today. No customer reviews were retained or analysed. Full copyrighted page bodies are not redistributed.

The national directory's city links were followed. The acquisition supplied 155 service cards under 48 directory labels. These are 131 unique name-and-coordinate entries after deduplicating 24 repeated occurrences. The Kab. Probolinggo and Kab. Malang directories unexpectedly repeat the Surabaya cards, while the Kab. Tangerang directory repeats Serang entries. A directory label is therefore not an administrative location. The inventory is an acquired directory view, not a reconciled national network total. Entries absent because a city page supplied no parseable cards remain unobserved rather than closed or nonexistent.

## Coordinate method

Coordinates were read from the exact Google direction/place links published by the official provider. No Google reviews or place database were scraped. For place links, !3d and !4d destination coordinates were used rather than @ camera-centre coordinates. These are provider-published map candidates, not field-confirmed entrances or validated workshop hardware positions.

General workshop eligibility requires the official service card to advertise Bengkel & Suku Cadang and a plausible, nonconflicted coordinate. Body-and-paint-only and showroom-only entries are not general workshop destinations. Job/model-specific capability and current appointment capacity remain unverified for every branch. Directory open/closed badges were not treated as enduring opening schedules.

## Material exclusions

* Auto2000 Suci, Bandung: its PHH Mustofa address conflicts with a map direction identical to Setiabudi. The separate Suci branch page repeats that direction. Both original coordinates remain in the facts; Suci excluded from main routing. Its exclusion can overstate distance in eastern Bandung, so a sensitivity or explicit limitation is required.
* Auto2000 Sidoarjo: the official directory and branch page encode 1127197388267770,-7441297706613890, outside geographic coordinate ranges. No decimal relocation or swapping is silently applied. This location is excluded from routing; workshop hours are also unavailable on the branch page.
* Auto2000 Virtual Branch: an unnamed entry in Jakarta Utara has no physical address. Directory prose identifies a virtual branch. A plausible map coordinate does not turn it into a workshop.
* Additional invalid official coordinates elsewhere remain excluded in branch_inventory_summary.json. These are data-quality exclusions rather than proof of closed facilities.

## Other authorised Toyota providers

Three additional providers have official location and service evidence with geocoded official place-link candidates: Tunas Toyota Cimindi and Plaza Toyota Bandung; Deltamas Balaikota Medan. Liek Motor Indrapura has documented 3S evidence but is not geocoded here. This targeted supplement is not a census of non-Auto2000 Toyota workshops. Therefore nearest Auto2000 versus mapped garage comparisons do not identify Toyota-network retention or channel switching. OtoXpert requires operator-specific attribution: another dealer's outlet does not automatically generate Auto2000 gross profit.

## Reproducibility

Run build_branch_inventory.py to regenerate reconciled CSV/GeoJSON/routing outputs from official_branch_facts.json. This is offline reproduction of acquired facts. Web reacquisition remains conditional on availability and markup. directory_source_register.csv preserves source URLs, retrieval route and cache recency. The original fact extraction is retained to audit deduplication and exclusions.

## Targeted non-dealer service-chain qualification

A supplementary 11-location evidence register was assembled after the broad category-based candidate screen: eight exact Shop & Drive outlet identities (two per focal market) and three Dokter Mobil locations. This purposive subset does not estimate chain coverage or workshop market share. Shop & Drive official directory identifies the local outlet; its FAQ advertises replacement work, oil and oil-filter products, and names Toyota among supported brands. Capability is therefore network-advertised, not confirmed for the selected vehicle model/year, stock or appointment today.

The official January 2026 Shop & Drive promotion provides historical model/job evidence: a specified oil-filter offer names Avanza and several other Toyota models; brake-pad fitting is also advertised. The page expressly marks the promotion ended. It is not a current price or offer. Do not apply its historical terms to current branch quotations. This stronger historical evidence does not resolve present availability.

Dokter Mobil Bandung, Lontar and Ngagel official local/city pages advertise oil-change service, but its Cuci Darah treatment must not be assumed equivalent to a standard scoped oil-filter replacement. Specific Toyota fitment and current pricing remain unverified. Some chains are labelled auto_parts_store in Overture despite their service advertising; a conservative category filter can therefore exclude genuine service alternatives. This is a false-negative risk to test, not justification to include every chain-looking record.

Coordinates in verified_alternative_evidence.csv were initially exact-name/address-matched Overture candidates. If official Shop & Drive embedded coordinates become available, use those in a separate updated field or routing file; preserve the original matched coordinates and disagreement rather than silently overwriting evidence. No customer accounts or reviews were analysed. Shop & Drive belongs to the Astra Otoparts/franchise ecosystem; it is not an Auto2000 workshop, and outlet-level GP recipient is not established here.

Primary sources: https://www.shopanddrive.com/outlet ; https://www.shopanddrive.com/faq ; https://www.shopanddrive.com/promo/promo-new-year-deals ; https://www.doktermobil.com/lontar/ ; https://www.doktermobil.com/ngagel/ ; https://www.doktermobil.com/bandung/ . All retrieved 14 November 2026 through public web retrieval; crawl ages vary.
