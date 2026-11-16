# Auto2000 Digiroom Demo Backlog

The showroom becomes the first of three connected journeys. A shopper uses Life Test to get a confirmed drive and a purchase quote. An owner gets an agreed workshop job and a paid work record. A returning owner turns an inspected trade-in offer into a deal on their next xEV.

**Current build.** Life Test already has garage, family and driving scenarios, an ownership cost and financing planner, branch selection, a downloadable and shareable visit brief, a QR code, and a WhatsApp draft to Tasia. The service call to action opens a scheduled-service or Toyota Home Service enquiry. The planner also lets users enter a trade-in value and outstanding settlement to estimate equity. Those are the starting points for the changes below. [Deployed Digiroom Life Test](https://auto2000demo.vercel.app/)

**Build order.** Finish the Life Test handoff first, add a complete paid workshop job second, and add the inspected upgrade deal third. Give each journey a clear ending the audience can see.

## 1. Buy an xEV — finish the Life Test handoff

| Action | Build | What the customer sees |
|---|---|---|
| **Improve** | Carry the Life Test brief forward from the showroom. Save the selected model and variant, parking or seating checks, weekly driving needs, and the questions the shopper wants answered in person. Give BEV shoppers fields for usable home or public charging and a fallback for a regular trip. Give HEV shoppers fuel-use and everyday fit checks. Carry both sets where relevant for a PHEV. | The adviser gets the shopper’s actual questions. A Zenix Hybrid family sees “Third-row access with child seat fitted” on its visit checklist. |
| **Change** | Turn the existing branch, date preference, and brief into a test-drive request tied to a named adviser. Let the branch confirm the exact demonstrator and time, or offer another date or branch. Preserve the QR, download, and WhatsApp sharing paths as ways to carry the same brief. | “WhatsApp draft ready” when the message is open for review. “Request received” when the request is recorded. “Test drive confirmed” once the branch accepts, with model, time, location, and adviser. A proposed alternative can be accepted from the same record. |
| **Improve** | Connect the existing cost planner to an adviser quote for the selected variant. Show vehicle price, cash due at delivery, monthly payment, term, applicable fees, and financing status. Let the driver share a read-only view with the household buyer. Clearly date estimates and quotes. | The family can open its estimated monthly payment while browsing and return to the adviser’s dated quote after the drive. |
| **Add** | Give the adviser a short checklist for the drive and a place to record which questions were resolved. Continue the request through attended visit, quote, order, and delivery. Capture whether this is the household’s first Auto2000 vehicle purchase separately from its first Toyota or first xEV. | The shopper reopens one record after the drive to see the answer to their question, the quote, and the next step. |

**Show in the demo:** A Zenix Hybrid shopper saves a family-fit question, requests a drive, receives a branch confirmation, and opens the quote after the visit.

## 2. Service my car — turn an enquiry into a confirmed paid job

| Action | Build | What the customer sees |
|---|---|---|
| **Change** | Turn the scheduled-service enquiry into a separate service journey. Start with vehicle, variant, job or symptom, and preferred area. Extend it to accept the same details from a WhatsApp conversation. Use oil and filter for the first routine flow, with a separate diagnostic visit for faults. | An Avanza owner selects oil and filter. An owner with a recurring noise describes the symptom and sees what a diagnostic visit covers. |
| **Add** | Match the job to a capable outlet using vehicle fitment, job capability, operator, and availability. Include Auto2000 workshops and eligible OtoXpert branches operated by Auto2000. Use the existing branch and Toyota Home Service information to surface a home-service option where the job and location qualify. | A shortlist shows who runs each outlet, what each outlet can do, and the earliest available visit. |
| **Add** | Give each routine job an installed price with parts, labor, tax and exclusions, plus the payer split where relevant. Reserve parts and confirm the arrival and collection windows through the outlet. A diagnostic route confirms the visit and its diagnostic scope first, then produces a repair estimate after inspection. | The owner sees an itemized oil-and-filter offer and gets a confirmed slot once the shop has the parts. A fault estimate appears after the inspection. |
| **Add** | Add a workshop record from check-in through ready for collection and paid. Record acceptance of the original scope before work begins. When the adviser finds extra work, send the reason, revised total, and timing to the driver or authorized family member. Store the exact quote version approved before any added work proceeds. The adviser carries the agreed scope and any unresolved symptom into handover. | The person paying can approve or decline the added work remotely. The owner receives the final scope, receipt, and next action for any unresolved issue. |
| **Add** | Capture the last provider for comparable work, job category, operator, and who paid. Record covered and customer-paid amounts separately. | The team can identify a completed paid job won from an independent garage and distinguish it from a customer who already used Auto2000 for the same work. |

**Show in the demo:** An Avanza owner who usually uses a local garage compares an offer from an eligible outlet, gets the parts and slot confirmed, shares an added-work quote with the payer, and receives a receipt.

## 3. Upgrade my Toyota — turn an estimate into a deal on the next car

| Action | Build | What the customer sees |
|---|---|---|
| **Extend** | Use the existing trade-in estimate and equity calculator as the entry point. Add the current vehicle, selected replacement xEV, inspection booking, and document submission. Let the owner share relevant service or hybrid health evidence with the appraiser and see which items were accepted. | The owner goes from a market estimate to an inspection for their own vehicle. |
| **Add** | Display the appraiser’s written buy offer after inspection, with the buyer, conditions, and expiry. Use the lender’s official settlement figure and itemized fees to calculate net trade-in equity. | The owner sees how much trade-in credit is available for the new car or exactly how much negative equity needs to be settled. |
| **Add** | Create one deal summary for the exact replacement unit. Include net equity, cash due, monthly payment, term, any final balloon payment, lender status, and the vehicle reservation. Show deposit and refund terms before payment. | The household can review a single shareable upgrade deal with the confirmed and pending items clearly marked. |
| **Add** | Give one adviser ownership of offer expiry, lender confirmation, unit reservation, old-loan settlement, and the two handovers. Provide an updated offer or a way to pause when the valuation expires, financing changes, or the selected unit goes unavailable. | The owner can accept and track handover or return to the deal later with a clear next step. |

**Show in the demo:** A Yaris Cross Hybrid owner goes from a rough trade-in range through inspection and an official loan payoff to a confirmed deal on the replacement xEV.

## 4. Connect the journeys in the demo

- [ ] **Add three clear entry points.** Use **Explore & test drive**, **Service my car**, and **Upgrade my Toyota**. Give the customer a **My requests** view to reopen a drive, job, or upgrade in progress.
- [ ] **Make the business handoff visible.** Add a compact adviser view or role switch for the walkthrough. The adviser confirms a demonstrator, confirms a service slot and parts reservation, or coordinates the inspected offer. The customer sees that action reflected on their own record.
- [ ] **Use one record per request.** Carry the selected vehicle, branch or adviser, next action, and status across screens. Use time-limited or revocable links for family approvals and quotes. Keep customer or financial details within the authorized view, including when customers share a QR or WhatsApp link.
- [ ] **Use customer-facing states in both languages.** Change the planner’s “Illustrative monthly instalment” label to **Estimated monthly payment**. Use **Awaiting branch confirmation**, **Workshop slot confirmed**, **Review additional work**, **Inspection booked**, or **Offer expires Friday** at the relevant step. Keep the calculator’s assumptions near its figures.
- [ ] **Make the walkthrough self-contained.** Use a consistent set of sample customers, vehicles, quotes, dates, and outlet availability. Let the in-demo adviser action create the next state. Keep real WhatsApp sending behind an explicit action that shows the destination and message. Live branches, lenders, and appraisers provide the authoritative states when connected.
- [ ] **Record the outcomes separately.** Goal 1 ends in a delivered xEV to a customer new to Auto2000. Goal 2 ends in a paid work order, with independent-garage history and recognized contribution recorded. Goal 3 ends in a delivered replacement xEV to an existing customer. Track the intermediate states for each journey so a submitted request and a completed sale stay distinct.

### Later additions

- Add comparisons between real available branches or models with current quotes once those feeds are available. Use branch-supplied parts and slot data for the workshop offer.
- Add inspection, lender payoff, and live inventory connections as part of the upgrade workflow. Keep the inspection-backed upgrade offer as the main path. Treat a guaranteed future resale floor as a separate commercial option with a named payer and defined terms.

[Integrated Auto2000 research](https://github.com/Fafauzif/auto-data/blob/main/reports/INTEGRATED_REPORT.md) · [Interview findings](https://github.com/Fafauzif/auto-data/blob/main/analysis/interviews/INTERVIEW_SYNTHESIS.md)
