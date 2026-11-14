# Four-page visual story: website journeys

This is an outline for the new visual memo. The uploaded audit is a visual reference only. No new research, invented app UI or mobile/native result is introduced.

For the readable page, use the short body, dominant visual, concise source caption and boundary. Full URLs, evidence-file paths and detailed settings below are editorial provenance, not extra page copy.

## JOURNEY_STORY_01: Useful tools already work before contact

**Existing functions set the baseline for a new idea**

The desktop walkthrough reached five useful entry journeys: vehicle comparison, finance previews, service-cost guidance, a digital-certificate entry and test-drive scheduling previews. Some paths then ask for a plate or VIN; those downstream steps were not tested.

This changes the starting point for the research. A proposed improvement needs to resolve a specific decision or handoff beyond these existing functions. The observations establish reachable page states, not customer comprehension, completed bookings or incremental sales.

**Dominant visual:** five-row evidence map. What the evaluator could reach. Five generous horizontal rows, each with a short task label, observed endpoint and explicit status. This is a research evidence map, not a mock app screen.

| Task | Observed endpoint | Status | Evidence |
|---|---|---|---|
| Compare hybrid and petrol | Comparison table displayed | Observed | UX02 |
| Preview financing | Illustration before name or phone | Observed | UX03, UX04, XT02 |
| Browse service estimates | Model and variant cost guidance | Observed; March 2024 basis | JX03, XT04 |
| Find a digital-certificate entry | VIN validation step | Entry observed; retrieval untested | JX02 |
| Preview a test drive | Branch, date and time windows | Preview observed; confirmation untested | UX05, XT06 |

**Source caption:** Logged-out desktop observations, 11 November 2026. Evidence UX02-UX05, JX02-JX03 and XT02/XT04/XT06. Safe endpoints only.

**Confidence:** Observed specific page states; no customer outcome test.

**Boundary:** Desktop only. Reaching a page is not a completed customer task or a causal business result.

**Primary URLs:**

- https://auto2000.co.id/mobil-baru-toyota/p/innovahybrid
- https://auto2000.co.id/mobil-baru-toyota/p/bz4x
- https://aftersales.toyota.astra.co.id/t-care
- https://aftersales.toyota.astra.co.id/hybrid-health-check/generate-certificate
- https://auto2000.co.id/testdrive/new-car/BZ4X

**Evidence files:**

- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/journeys/journey_observations.json
- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/journeys/friendcontext_JX_observations.json
- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/observations.json

Body words: 73.

## JOURNEY_STORY_02: Insurance timing moves cash between now and later

**The existing calculator already exposes a meaningful tradeoff**

Changing only insurance-payment timing reduced the displayed cash needed upfront by Rp45.31 million, while raising the remaining monthly instalment by Rp1.13 million. The car, city, base down payment and first-instalment timing stayed the same.

The existing calculator therefore already answers a useful budget question. A further explanation could help a buyer understand cash at delivery and later payments. Whether that explanation improves a purchase decision remains untested. These are conditional simulator outputs, not binding lender or insurance quotes.

**Dominant visual:** two-panel bar comparison. Less cash now comes with larger later instalments. Use the same scenario colors and ordering in both panels. Keep separate axes, large direct value labels and readable scenario labels. Do not stack the two financial quantities.

| Scenario | Upfront, Rp million | Monthly, Rp million |
|---|---:|---:|
| Insurance upfront | 154.85 | 9.27 |
| Insurance in instalments | 109.53 | 10.40 |

Same 60-month illustration, with 59 remaining monthly payments. Exact integers and scenario settings are in the JSON.

**Source caption:** Observed Auto2000 simulator, 11 November 2026; UX03-UX04. Same Innova Zenix G HV CVT, Jakarta Pusat, DP 20%, ADDM, optional income blank.

**Confidence:** Observed matched simulator settings; customer comprehension and purchase effect untested.

**Boundary:** The source discloses payment timing. No completed finance application, approved rate or customer effect was measured.

**Primary URLs:**

- https://auto2000.co.id/mobil-baru-toyota/p/innovahybrid

**Evidence files:**

- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/journeys/finance_scenarios.csv

Body words: 78.

## JOURNEY_STORY_03: A BEV page shows a clear label mismatch

**A specific rendered defect gives the research a sharper target**

The selected bZ4X page labels its fuel system as BEV, yet places 7311 under a tank-capacity field measured in litres. The value was visible in both the page and its accessibility tree.

This gives us a precise information-quality issue to investigate. It does not establish the correct engineering value, the underlying cause or whether a customer changed a decision. The useful question is whether specific labels help a buyer understand the relevant vehicle tradeoff.

**Dominant visual:** redrawn observed evidence panel. As displayed for bZ4X A/T. Show two large, clean rows. Emphasize the second label/value pairing with one restrained highlight. Place the exact specification URL and observation date immediately below.

| Translated field label | Displayed value |
|---|---|
| Fuel system | BEV |
| Tank capacity (litres) | 7311 |

**Source caption:** Observed selected bZ4X A/T specification, 11 November 2026; XT05/XTS02. Page and accessibility state checked; no engineering validation.

**Confidence:** Certain about the rendered label/value pair; engineering meaning and customer effect unverified.

**Boundary:** This is one specific page state. No universal website failure or causal customer effect is inferred.

**Primary URLs:**

- https://auto2000.co.id/mobil-baru-toyota/p/bz4x/spesifikasi

**Evidence files:**

- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/observations.json

Body words: 74.

## JOURNEY_STORY_04: Preview works; confirmation remains a later step

**Preserved branch context and tentative windows have different meanings**

The bZ4X journey exposed Juanda's date and time previews before contact. Its FAQ says staff later confirms the schedule and unit availability. That confirmation was not observed because no request was submitted.

Branch context also survived two tested handoffs: Juanda with bZ4X, then Cempaka Putih with Hiace. The second route changed the preceding branch selection. These counterexamples shift the question toward actual availability and fulfilment. They do not establish a universal handoff problem, a confirmed vehicle or a completed visit.

**Dominant visual:** request-state diagram with two-row handoff inset. Observed access stops before the operational promise. Use no more than five short state labels. Label observed, stated and untested states explicitly, with distinct line styles as well as color. The handoff inset supports the baseline; it must not look like a confirmed booking.

| State | Evidence status |
|---|---|
| Choose car and branch | Observed |
| Preview date and time | Observed |
| Submit request | Not performed |
| Staff confirms unit and schedule | Stated in FAQ; not observed |
| Attend test drive | Not observed |

Handoff inset: Juanda/bZ4X stays Juanda/bZ4X; then Cempaka Putih/Hiace becomes Cempaka Putih/Hiace. Both are observed context preservation, not confirmed bookings.

**Source caption:** Logged-out desktop, 11 November 2026; XT06 and XT08. Juanda date/time preview and booking FAQ; two actual branch links checked after loading.

**Confidence:** Observed preview and preserved context; later confirmation is stated by the FAQ, not observed in operation.

**Boundary:** Desktop only. Zero mobile-emulated and native-app journeys: local browser launch blocked by socket permissions; native DevTools blocked by organization policy; no available native emulator identified.

**Primary URLs:**

- https://auto2000.co.id/testdrive/new-car/BZ4X
- https://auto2000.co.id/testdrive/new-car/bz4x?branchCode=T151
- https://auto2000.co.id/testdrive/new-car/hiace?branchCode=T155

**Evidence files:**

- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/observations.json
- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/mobile_feasibility.json
- /workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/mobile_capability_receipt.json

Body words: 80.

