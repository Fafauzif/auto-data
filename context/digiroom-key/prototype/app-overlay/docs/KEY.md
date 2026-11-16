# Digiroom KEY handoff

## Install the overlay

The base is the supplied `Auto2000-Digiroom-Demo-main.zip`. Extract `digiroom-key-responsive-overlay.zip` directly into the existing project root. Choose **Replace All**. Keep the base archive's original models, fonts, and lockfile. **Files to delete: none.**

From that directory run `npm ci` and `npm run dev` on Node.js 22.12 or later. For a production bundle, run `npm run build` followed by `npm run preview`.

## Alternate paths for judging

| Journey          | Starting point                           | Alternate path                                                                                                                                                                                                                           |
| ---------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Know Your Fit    | Zenix household card and 48-hour request | Choose a standard drive or request the blocked calendar date shown in Sales. Offer a different date, branch or drive, then accept it in Customer. Switch the studio to bZ4X to try an editable charging mix and a fallback charger plan. |
| Easy Service     | Bandung Avanza 2019 oil and filter       | Use the local atlas or list. Try a qualifying Soekarno-Hatta home visit, a brake diagnosis with a technician handoff, or the Yaris Cross Hybrid health check. Issue a newer estimate to see the older approval link expire.              |
| Your Next Toyota | Inspected Yaris Cross Hybrid trade-in    | Raise or lower the payoff to see credit, zero equity or shortfall. Withdraw an unavailable unit and record the deposit refund before reopening. The customer can start a direct repurchase without a trade-in.                           |

## Data and state

There is one active case per journey in the competition account. Requests, payment records, finance decisions, sample hours, demonstrator and vehicle allocations, inspection offers, and quote amounts are local walkthrough records. The authorized payer link resolves in the same browser profile and checks the estimate version. Buyer and payer views model access in the competition account. Live identity, dealer inventory, appointments, parts, lender decisions, deposits, payments, settlement, messaging, and cross-device approval require separate integrations.

Each request carries a stable ID, a current stage and responsible role, a quote version, and a dated history. Storage survives refresh. Reset clears KEY transactions and the in-session KEY draft. The original showroom retains its own independent settings.

## Geography provenance

The overlay uses the corrected **14 November 2026** release from [auto-data at `8cecb64`](https://github.com/Fafauzif/auto-data/tree/8cecb64d8ab26cbb5264c4513805dc0a6436ddbd). The builder joins coordinates by **market + origin_id**, retains corrected Suci and Sidoarjo endpoints, and uses official Auto2000/OtoXpert operator records. Shop & Drive and non-Auto2000 OtoXpert locations remain in the comparison layer. The origin detail presents outbound OSRM times for the three compared endpoints and surfaces tied dealer endpoints. Route shapes are omitted where no authorized route geometry was used.

| Market    | Paired origins | Dealer gap >5 min | With eligible Auto2000-operated OtoXpert |
| --------- | -------------: | ----------------: | ---------------------------------------: |
| Bandung   |             78 |                17 |                                       14 |
| Surabaya  |             59 |                10 |                                        6 |
| Medan     |             78 |                 3 |                                        0 |
| Palembang |             69 |                 9 |                                        0 |
| **Total** |        **284** |            **39** |                                   **20** |

Eight residual model origins are assigned to Soekarno-Hatta. These counts refer to grid origins for a defined oil comparison. They describe modeled driving geometry. They do not estimate owner counts, live traffic, or demand. [Geography report](https://github.com/Fafauzif/auto-data/blob/8cecb64d8ab26cbb5264c4513805dc0a6436ddbd/analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md)

Live layers use standard OpenStreetMap raster tiles. The offline atlas uses clipped Natural Earth 1:10m land, urban footprint, hydrography and administrative line layers. Both views use the same local workshop and model overlays. Point-level comparisons and the offer picker remain usable with tile requests blocked. See [Third-party notices](../THIRD_PARTY_NOTICES.md).

To regenerate local geography, obtain the four Natural Earth GeoJSON inputs at [v5.1.2](https://github.com/nvkelso/natural-earth-vector/tree/v5.1.2/geojson), remove `ne_10m_` from each input filename and run `python tools/build_key_geography.py PATH_TO_AUTO_DATA PATH_TO_NATURAL_EARTH` with GDAL/`ogr2ogr` installed. Runtime builds use the bundled JSON and do not need either input repository. The landing image is rendered from the existing original Zenix GLB using `tools/render_key_vehicle.py`.

## Local verification

```sh
npm ci
npm run typecheck
npm run format:check
npm test
npm run build
npx playwright install chromium --only-shell
npm run test:browser
npm run test:browser:key
npm run test:browser:responsive
```

The KEY suite exercises production output, role handoffs, saved state, quote and receipt downloads, all four map scenarios with tiles blocked, and mobile layout. The original browser suite covers the existing studio and visit flow. The unit tests cover version and role checks, calendar overlaps, funding and equity arithmetic.
