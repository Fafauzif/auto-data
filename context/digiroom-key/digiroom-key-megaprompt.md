# Digiroom KEY — Build the competition demo

You are taking over an existing Auto2000 Digiroom product demo for an Indonesian business case competition. **Deliver the complete product experience in the existing codebase.** A judge should be able to operate every core flow and watch the customer, sales adviser, workshop adviser, and upgrade adviser hand work to each other. Start with the repositories, inspect the existing implementation, then carry the work through build and browser verification.

## Get the source and current decisions

~~~sh
git clone https://github.com/Fafauzif/Auto2000-Digiroom-Demo.git
git clone https://github.com/Fafauzif/auto-data.git
~~~

Use any existing authorized checkout before cloning a duplicate. [Digiroom demo source](https://github.com/Fafauzif/Auto2000-Digiroom-Demo) · [Research and geography source](https://github.com/Fafauzif/auto-data) · [Deployed Life Test](https://auto2000demo.vercel.app/)

The research repo cloned successfully in the previous session. The demo source returned a 404 from that workspace, while the deployed site was accessible. If the demo clone is unavailable to you too, use an authorized checkout or a source ZIP supplied by the user. Report any remaining source-access blocker clearly. Use the deployed demo as a visual and interaction baseline, and work from authorized source for code changes.

Read the demo repo's own instructions, package manifest, routes, assets, and data flow. In auto-data, start with the KEY handoff at context/digiroom-key/START_HERE.md if present, then its solution overview, decision record, evidence index, and issue tree. Read AGENTS.md, PROJECT_CONTEXT.md, and the relevant analysis files for evidence. The updated K scope in the solution overview governs the pitch. This brief adds the agreed build scope, including four workspaces and the map fallback. The earlier backlog maps the deployed starting point and is useful for locating existing features.

## Finish the idea and write it like a real product

Apply **Sell the Finished Idea** across the UI, walkthrough, slide copy, exports, tooltips, and status messages. Use the bundled skill in context/digiroom-key/skills/sell-the-finished-idea.zip if accessible. The rules here apply on their own.

- Show a finished experience immediately. Use concrete actions and outcomes. The owner chooses a job, the workshop confirms the slot, and the payer approves revised work.
- Strip phrases such as **“needs validation,” “illustrative concept,” “just a prototype,” “pilot only,” “subject to validation,” “proof of concept,” “masih perlu diuji,”** and equivalent weakening copy from judge-facing surfaces. Use **Awaiting branch confirmation**, **Estimated monthly payment**, **Parts reserved**, **Awaiting payer approval**, and **Ready for collection** when those states apply.
- Keep information accurate where it affects a decision. The energy calculation is an estimate. A branch action confirms a slot. An appraiser issues the buy offer. A lender controls the finance decision. Keep assumptions near the affected figure and research provenance behind a concise “About this map” or equivalent affordance.
- Use coherent, clearly scoped sample accounts and data for the competition walkthrough. Adviser actions in that environment update the actual in-demo state. Real integrations, approved policies, available units, measured conversion, and funded guarantees require real backing. External bookings, messages, payments, and publication require separate authorization.

## Product goal

**Digiroom KEY. Know your fit. Book your service. Find your next Toyota.**

| Journey | Customer problem | What the product makes possible | Business completion |
|---|---|---|---|
| **K — Know Your Fit** | Household fit, driving economics, and real-life use are hard to assess from a showroom. | Recreate your routine in 3D, price your driving week, and take the same checklist into a branch drive or a 48-Hour Life Test. | An xEV is delivered to a customer new to Auto2000. |
| **E — Easy Service** | Trust is job-specific, the trip takes effort, and customers can reject an unclear or larger quote. | Find an eligible operator and get a comparable installed price, parts and slot confirmation, and written approval of extra scope. | A customer-paid job is completed, with comparable prior independent use captured where relevant. |
| **Y — Your Next Toyota** | A price range leaves trade-in value unsettled. Equity, loan payoff, financing, and unit availability are separate decisions. | Carry an inspection-backed buy offer into one upgrade deal that the household can accept and the adviser can close. | A replacement xEV is delivered to an existing Auto2000 customer. |

The acquisition cohort is new to Auto2000. Store first Toyota, first xEV, and first Auto2000 separately. Existing owners can repurchase with or without a trade-in. An HEV, PHEV, or BEV follows the applicable evidence, eligibility, and workflow for that powertrain.

## K — Build the 3D Life Test into a customer-defined drive

**Hero interaction.** Start with a Zenix Hybrid family. Let a judge adjust garage width and length, open the relevant doors and tailgate, try a passenger and luggage arrangement, and immediately see which questions to check on the real car. Save those checks into a visually strong visit card. Carry that card from the showroom to the sales adviser and the household buyer.

- Preserve and improve the existing Life Test 3D scenes, controls, ownership planner, branch selection, shareable brief, QR or download, and WhatsApp draft where supported. Inspect the real asset rigs before adding animations. Prioritize useful camera presets, controlled orbit, stable touch controls, readable measurements, and a credible scene. If an existing asset supports articulated parts, tie the controls to those parts. Use a clean schematic or image fallback when WebGL or a model asset is unavailable.
- Use vehicle and household dimensions with explicit units. Show approximate clearance as a useful check to take to the actual car. Present known measurements and estimates in context. Give the customer access to controls for parking, seating, luggage, and weekly driving without requiring an adviser or account.
- Let the household estimate its energy cost from weekly distance and relevant fuel or charging assumptions. A BEV check can capture usable home and public charging and an alternate plan for a recurring trip. An HEV emphasizes fuel, parking, and cabin fit. Keep the dated adviser quote separate from the planner assumptions and share both with the buyer or payer.
- Offer **standard drive** and **48-Hour Life Test**. The take-home path is for eligible shortlisted buyers at participating branches with capable demonstrators. The adviser resolves exact model and variant, driver terms, pickup and return windows, and any alternative. The vehicle calendar prevents overlapping reservations and includes return and turnaround. Show handover condition, odometer, and fuel or charge level as part of the sample workflow. The branch-facing checklist carries the agreed eligibility, coverage, use limits, return procedure, and contact details.
- Let the family mark how the car actually worked in their garage and routine. On return, the adviser records the answers and provides a dated variant-specific quote with cash due, instalments, term, fees, and finance status. Show next actions up to delivery. If the desired car or take-home slot is unavailable, offer a named branch, date, or standard drive the owner can accept.

**Key choice.** Auto2000 already offers model-specific test-drive requests and credit simulation. The feature people remember is a household building its own checklist from a 3D recreation and then trying that same routine in the actual car.

## E — Put real geography behind a workshop offer

**Hero interaction.** In Bandung, switch between dealer workshops and the network with eligible Auto2000-operated OtoXpert. Watch modeled origin markers change state, open an origin and see the modeled time comparison, then select a feasible service offer. The workshop adviser confirms parts and slot. The customer receives an additional-work estimate they can send to the payer, then sees the completed job and receipt.

- Implement a real pan-and-zoom map with Bandung as the starting view and Surabaya, Medan, and Palembang available. Use distinguishable layers for Auto2000 general workshops, eligible Auto2000-operated OtoXpert, and the analyzed oil comparison network. Allow the judge to switch map layers, select a real modeled origin, filter by job or location, and inspect the relevant outlet. Make the scenario switch produce a visible and truthful change in the overlay and counts.
- Retain the reviewed figures exactly. There are **284 paired origins**. The over-five-minute oil-gap counts before and after adding eligible Auto2000-operated OtoXpert are **Bandung 17 → 14, Surabaya 10 → 6, Medan 3 → 0, and Palembang 9 → 0**, or **39 → 20 across four markets**. Eight of the remaining modeled origins are assigned to Soekarno-Hatta. The comparison network is the collected oil-service comparator. The results describe travel geometry for a defined job and threshold. Keep modeled origins and quote or slot fixtures distinct; present origin counts as model points rather than customers. Use authorized route geometry for actual polylines. A point or timing comparison works where route geometry is absent.
- Build versioned, attributed overlay files from the geography outputs. Start with analysis/geography/tables/raw_recomputed_origins.csv, raw_recomputed_markets.csv, branch_portfolio.csv, and the [geography report](https://github.com/Fafauzif/auto-data/blob/main/analysis/geography/GEOGRAPHY_INTEGRATION_REPORT.md). Join model points to the source origins by **(market, origin_id)**. Use the latest corrected endpoints and official operator labels. The detailed join paths, licensing reminders, and the verified model baseline are in the handoff's EVIDENCE_TO_FEATURE.md.
- Support live tiles when available and provide a **bundled, attributed geography fallback** that keeps real locations, overlay interactions, counts, and the booking path usable without the tile service. Use published data licensing and provider terms. A network failure during judging should leave a functioning interactive view. Add a list or table view for mobile, keyboard navigation, and users who prefer a non-map interaction.
- Treat independent garages as competitors for the job. Auto2000 and **Auto2000-operated** OtoXpert are the selectable offers in this concept. Check model fitment, capability, operator, parts, hours, eligibility, and slot in that order of scope before confirming. Distinguish a real directory location, research travel times, and the sample slot data. Offer eligible Toyota Home Service where geography and job scope support it.
- Lead with an out-of-entitlement Avanza oil-and-filter job. Show installed price, parts, labor, tax, exclusions, check-in time, and collection window. For a fault, preserve the symptom, prior work, technician handoff, and defined diagnostic appointment. The estimate after inspection states required work, deferrable items, and applicable options. The driver shares a scoped approval request with the authorized payer. Require approval of the revised quote version before added work. Record ready for collection, paid handover, receipt, and next action for any unresolved issue. Include an eligible hybrid owner journey or visible path that handles supported xEV service and entitlements separately.
- The workshop adviser owns the queue, job acceptance, parts reservation, estimate, payer approval, and handover. Capture the prior provider for comparable work and separate customer-paid, covered, and reimbursement-funded amounts. A customer who was already headed to Auto2000 is a separate retention opportunity.

## Y — Turn an appraisal into a replacement deal the owner can close

**Hero interaction.** Start with an existing Yaris Cross Hybrid owner who has a price range. Show the inspector's written offer enter the deal, apply the official old-loan payoff and fees, and see the clear amount of equity, upfront cash, and monthly payment for the chosen replacement. The upgrade adviser aligns lender conditions, the exact available unit, and the inspection offer. The customer tracks settlement and replacement delivery.

- Carry the existing trade-in planner into an inspection request. Show the market estimate, inspection, confirmed buyer offer, its conditions, and expiry as different stages. Let the owner share relevant service or hybrid health records by consent and show which evidence the appraiser accepts.
- Compute **net trade-in equity = inspected buy offer − official loan payoff − applicable trade-in fees**. Show equity available as a credit or an explicit shortfall, with clear totals for positive, zero, and negative equity. Combine it with the dated quote for the replacement unit in the walkthrough, cash due, monthly payments, term, applicable fees, and balloon payment when present.
- Let the upgrade adviser confirm the unit and its reservation expiry, lender decision, deposit terms, old-loan settlement, both handovers, and any refund. Include a meaningful recovery state when an offer expires or a unit becomes unavailable. A replacement order depends on the current accepted terms.
- The team's prior flow includes a possible resale floor and residual-value insurance. The core demo is the **inspection-backed net-upgrade offer**. A future floor belongs to a separate commercial decision with a named entity, funding, conditions, and limits. Show the route for an existing customer to repurchase directly if trade-in is not part of the deal.

## Four connected workspaces

| Workspace | What judges can operate |
|---|---|
| **Customer** | Discover K, E, and Y; open saved requests and vehicle records; share a quote or scope approval; track confirmation, collection, or delivery. |
| **Sales adviser** | Inspect the Life Test brief, manage the demonstrator calendar, confirm or offer an alternative, accept return, and issue the dated quote. |
| **Workshop adviser** | Match the job, confirm slot and parts, manage queue and work order, issue a versioned add-on estimate, follow payer approval, and close the paid handover. |
| **Upgrade adviser** | Coordinate inspection and accepted evidence, apply payoff and fees, confirm financing conditions and reservation, then record settlement and delivery. |

Implement meaningful separate role workspaces, with queues, actionable detail views, relevant empty and error states, and a shared transaction history. Keep a stable transaction identifier, current responsible role, latest permitted state, quote version, time, and next action. A real interaction in one role changes the customer view using shared state; preserve progress on refresh. Match existing repo conventions for persistence. For a local competition demo, use coherent seeded accounts, a deliberate role switch, and a reset-to-start action that requires intent. Put private finance or quote details behind the appropriate view. For any public deployment, keep real credentials, contact details, and customer information out of the demo data.

## Craft and demo flow

- Build on the existing platform and visual language. Use strong Toyota-red accents, restrained chart motion, realistic scale, and a clear status hierarchy. Make the 3D studio and map feel rich while leaving task forms and confirmations easy to read.
- Give the judge a short, replayable route into each of the three signature moments. Show the customer’s action, the counterpart’s response, and the completed commercial event. Avoid long form-filling before the visual reveal; prefill coherent example work when useful.
- Make desktop, a presentation viewport, and typical mobile usable. Support bilingual EN/ID labels, IDR formatting, local dates, keyboard controls, visible focus, and reduced motion. Lazy-load heavy assets and keep role navigation responsive.
- Give calculators, map overlays, and 3D an immediate first render with a graceful fallback. Reuse appropriately licensed assets and preserve attribution. On venue connectivity loss, the bundled map, local sample workflow, and critical vehicle visuals should remain usable.

## Build and verify the handoff

Work in the order the dependencies require: shared routes, roles and state first; K's existing showroom and full drive handoff; E's geographic layers and completed work order; then Y's inspected upgrade and reservation. Finish by tightening the integrated walkthrough. Keep the task in the existing repository conventions. Complete the user-facing flows before decorative polish becomes its own workstream.

Run the repo's build, lint, type checks, and applicable tests. Use targeted tests where existing coverage misses a material regression, including quote version approval, overlapping demonstrator reservations, and the sign of trade-in equity. In a browser, verify the role handoffs and mobile layout, exercise 3D or its fallback, block map tile requests to prove the bundled fallback, and scan visible copy and exports for weakening phrases. Compare all four map counts and denominators to the cited data. Verify that core demo actions never submit a real appointment, payment, or third-party request by accident.

Return a working demo, precise run instructions, a concise judge walkthrough, and the exact verification you ran. Report concrete remaining blockers and distinguish any real backend dependencies from the completed demo interactions. Treat pushes, external sharing, and deployment as separate actions unless the user explicitly requests them.
