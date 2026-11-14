# Public journeys: useful self-service exists, with task-specific qualification boundaries

Observed 11 November 2026 in a cloud Chrome browser at 1363 × 936 pixels, logged out. This is a researcher walkthrough of twelve task/scenario cells across Auto2000, Toyota OEM and BYD Indonesia, not twelve unique participants or a representative usability study. Eleven cells use Indonesian public sites; the Google Play destination used the browser's English-US listing. No customer name, phone, email, plate, income, exact personal location or private account was entered. No purchase, lead, booking, contact message, subscription or appraisal was submitted. A search term such as Jakarta or Bekasi was an illustrative city, not the user's location.

## Evidence contract and limits

The linked JSON/CSV files contain evaluator transcriptions of visible browser states, dates, URLs, actions, boundaries and contrary explanations. Exact per-click timestamps were not exported; `generated_at_utc` is file creation time, not an invented timestamp for every observation. Selected screenshots were viewed internally to confirm calculator output and comparison layout; no screenshot files or full third-party page dumps are redistributed. Website responses were not a sample of real user behavior or branch outcomes. No mobile, tablet, native app, assistive-technology, Lighthouse/axe or CrUX measurement was completed. The available Browser extension was not connected; cloud browser controls did not advertise device/viewport configuration. Do not infer a mobile defect or WCAG conformance from this desktop-only work.

A first catalogue comparison action encountered instrument protocol timeouts in frame-tree, DOM snapshot and screenshot operations. This was not a site-served anti-bot message. A fresh tab using the loaded product's actual comparison link worked. We retain the failed attempt without using it to claim comparison is broken. Website hydration also changed transient controls; using settled states avoided interpreting intermediate placeholders as final defects.

## Existing finance self-service materially changes the diagnosis: UX03–UX04

On the Innova Zenix Hybrid product page, the calculator produced financing choices with no name, phone or income. Monthly income was explicitly optional and remained empty. Default illustration: New Innova Zenix 2.0 G HV CVT, Gray Metallic, Jakarta Pusat, listed price Rp475,400,000; base DP 20%, Rp95,080,000; insurance paid upfront and first installment paid at delivery (ADDM). The 60-month option displayed total upfront Rp154,847,741 and Rp9,271,161 per month for the remaining 59 months. A fresh navigation and repeat calculation returned the same table. The complete five-tenor output is in `finance_scenarios.csv`.

Changing only insurance payment to installments, keeping model, location, color, base DP and ADDM unchanged, produced a 60-month option with upfront Rp109,533,402 and Rp10,403,402 per remaining month. The interface discloses these payment timing choices. These are useful observed trade-offs, not lender approvals, contractual offers or audited costs. Exact insurance coverage, rates and component fee accounting were not independently established. Do not label the difference between base DP and total upfront a hidden fee. A useful research question is whether customers qualify their budgets using base DP, total initial cash, monthly commitments, or all three, and whether a concise explanation improves comprehension. This work does not measure that behavior.

This evidence weakens a blanket claim that basic Digiroom financing estimates require contact capture or that Auto2000 needs a basic simulator built from scratch. It leaves questions about discoverability, customer comprehension, model coverage, current lender eligibility, handoff quality and actual transaction impact open. Source: https://auto2000.co.id/mobil-baru-toyota/p/innovahybrid .

## Comparison works but has a specific semantic data issue: UX02

A completed comparison placed G HV CVT hybrid at Rp475.4 million next to G CVT conventional at Rp437.7 million. It presented dimensions, engine, chassis, safety and comfort attributes; e-CVT versus CVT and system/engine power differences were visible. The field describing number of airbags displayed the Boolean value TRUE in each vehicle column, rather than a numeric count. Several other rows explicitly stated information was unavailable. This establishes a particular presentation/data-model concern, not incorrect underlying airbags, site-wide prevalence, or demonstrated customer harm.

The add-card text did not open selection in this walkthrough; the plus icon did. Selecting model, transmission/variant and confirmation then populated the comparison. No participant success rate was measured. The comparison showed technical attributes; it did not itself establish a complete ownership-cost decision for the inspected pair. Source and final state: https://auto2000.co.id/mobil-baru-toyota/komparasi?code=INNOVAHYBRID%3AMAG10GHA%2FT20_T1G3&code=INNOVA%3AMAG10GA%2FT20_T1G3 .

## Qualification is different across jobs, not universally contact-first: UX05–UX09

The hybrid test-drive page allowed a branch search/selection before customer details. Choosing Auto2000 Juanda exposed a calendar with a stated 2–14-day planning window. Choosing 13 November displayed morning/noon and afternoon time windows (08:00–12:00 and 13:00–17:00). We stopped before window confirmation or booking. The page also states the team will contact the customer, so a displayed option must not be described as an actual confirmed capacity reservation. Source: https://auto2000.co.id/testdrive/new-car/INNOVAHYBRID .

Workshop and home-service booking both asked for model, production year, variant and plate in their add-car modal. Service selection remained disabled pending vehicle qualification; branch/time or location/time remained disabled pending service type. We stopped before identity entry. Vehicle qualification may be needed for compatible service duration, branch equipment or entitlement; this test does not show the fields are unnecessary or cause abandonment. Sources: https://auto2000.co.id/layanan-bengkel and https://auto2000.co.id/ths-home-service .

Trade-in similarly required a plate in the add-car step and mileage for an estimate. It included Toyota/non-Toyota choices and described a later inspection and offer process. No estimate was produced, so accuracy, completion and abandonment remain unknown. Source: https://auto2000.co.id/services-toyota/tukar-tambah .

Body-and-paint behaved differently: the branch picker could be explored without entering a car. Its default Jakarta Pusat state reported no branch, but a Bekasi query returned a named Bekasi Timur body-and-paint branch and a Toyota Trust result. Selecting the body-and-paint branch opened a calendar. The displayed November dates appeared disabled; neither actual capacity nor the reason was verified. The successful city search is contrary evidence to interpreting the initial empty state as no service network. The safer question is how clearly a specialist-service search guides a customer from a default city to a suitable branch. Source: https://auto2000.co.id/body-paint-service .

## Competitor comparison suggests mechanisms, not a brand winner: UX10–UX11

BYD's default ATTO 3 test-drive form allowed dealer search by Jakarta before personal details. The intermediate result count briefly appeared zero, then settled to a list showing 104 dealers. Selecting the first displayed dealer, Harmony Sudirman, populated the form. No date/time selector appeared in the inspected selected-dealer state. This describes one OEM request flow for a BEV, whereas Auto2000's inspected flow was a hybrid dealer request; it does not establish which brand gives a better complete experience or faster fulfillment. No contact was entered and Send was never clicked. Source: https://www.byd.com/id/test-asia-driver .

Toyota OEM service booking's first step includes model/type/plate, STNK name, customer name, email and phone before continuing. It explicitly supports a different person delivering the vehicle. That is direct interface evidence that owner, booking user and driver can diverge, not a measure of how often they do. It supplies a concrete question for household and fleet research. No entries or progression were attempted. Source: https://www.toyota.astra.co.id/service-booking .

## Catalogue and app destination: UX01, UX12

The catalogue's upper price slider displayed Rp105,369,999,981,654. It also placed a current-looking bZ4X card at Rp799 million alongside lower-page prose with bZ4X figures above Rp1.2 billion. These observations justify checking source ownership and model/year/location/terms before declaring a price error. The filter was inspected, not systematically exercised. Source: https://auto2000.co.id/c/mobil-baru-toyota .

The website footer points to the Google Play package id.co.astra.ai.dev1. Clicking did not produce a visible new tab in the immediate inventory, so we directly opened the observed target to verify it. It resolves to Digiroom by Auto2000 with PT Astra International as developer, a displayed 9 November 2026 update and 500K+ download threshold. Header and phone-cohort review counts differ; this does not measure MAU. A rendered review/reply chronology also needs reconciliation before calculating response times. No app installation or login occurred, so app/site feature equivalence and deep-link context preservation remain untested. Source: https://play.google.com/store/apps/details?id=id.co.astra.ai.dev1 .

## Decision-relevant hypotheses to retain

1. Existing financing capability may already resolve a basic information need; incremental value may lie in explaining cash timing and aligning the later adviser quote. Test comprehension and quote continuity before assuming a new calculator will help.
2. Service qualification may be operationally necessary while early specialist-branch discovery could be made clearer. Distinguish information needed to estimate from information needed to reserve and fulfill.
3. Model-comparison data semantics may weaken confidence even when the comparison task works. Validate a fresh, template-balanced set and real customer relevance before sizing a commercial effect.
4. A test-drive request and a confirmed appointment are different states. A calendar is not proof of available inventory, and a simpler competitor form is not proof of better fulfillment.
5. The individual using the interface may not be the owner or driver. Current Toyota OEM affordances support testing that role distinction in subsequent evidence.

These are research interpretations and option-generating questions. They are not final strategy selections, Auto2000 implementation instructions or measured causal claims.
