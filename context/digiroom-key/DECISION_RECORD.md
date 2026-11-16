# Digiroom KEY decision and conversation record

This records the Auto2000 product decisions in order and explains how to resume the work. The [solution overview](digiroom-key-solution-overview.md) is the narrative specification. The [megaprompt](digiroom-key-megaprompt.md) is the build handoff.

## From research to three commercial goals

1. **Acquisition.** Win retail xEV sales from people new to Auto2000. Track first Toyota, first xEV, and first Auto2000 separately. A prospect can already own a Toyota bought elsewhere.
2. **After-sales.** Win back eligible customer-paid workshop jobs that would otherwise go to an independent workshop. Also protect jobs already headed to Auto2000 and support covered or reimbursed xEV ownership work. Each gets its own measure.
3. **Replacement.** Win the next xEV purchase from an existing Auto2000 customer. Trade-in is a route into repeat purchase. Delivery is the endpoint.

The existing prototype contributes garage and seating or luggage checks, weekly energy and ownership-cost scenarios, a branch and visit brief, QR or sharing, a WhatsApp draft, a service enquiry, and a trade-in equity calculator. The acquisition strength is the household’s actual inputs making the drive specific. The demo source and the research source are separate repos.

## How we changed the competition framing

The user wants a solution a judge can see working, then an operating model that explains how to deliver it. The team rejected pilot-first copy, generic framework labels, and screens that announce how tentative they are. The reference style from the Pepsodent Sesuai Saya submission puts the actual customer actions first and the implementation later. The mentoring notes ask for customer- and client-specific insights with consequences for the business decision.

This produced **Sell the Finished Idea**, included in [portable form](skills/sell-the-finished-idea.zip). Use clean, honest customer states and label financial estimates where the figure appears. Keep real operational milestones, assumptions, and controls in the appropriate context. The user dislikes visible phrases such as “needs validation,” “illustrative concept,” and “just a prototype.” [Mentoring notes](../../sources/session/uploads/Mentoring%20Notes%20%E2%80%94%20Problem%20Analysis%20in%20BCC.pdf)

The user’s preferred issue tree begins with **a problem statement**, splits into issue statements, and uses another arrow for root causes. The latest chart adds a solution response after each cause. Classify a lost transaction by its first binding barrier where possible. The [reference issue-tree format](reference/issue-tree-format-reference.png) and [editable KEY chart](diagrams/digiroom-key-issue-tree.tex) accompany the [finished issue tree](diagrams/digiroom-key-issue-tree.pdf).

## E came first — the workshop win-back decision

1. **Trust is job-specific.** The Wuling driver described successful routine dealer service via WhatsApp and used a separate trusted tire shop. This is the clearest customer example of someone retaining the dealer relationship while taking a particular job elsewhere.
2. **The visit can cost too much effort.** The model shows selected access gaps shrink when existing Auto2000-operated OtoXpert outlets are eligible. Soekarno-Hatta review accounts also show how missed or unresolved work can require another trip. Geographic proximity and completion are distinct.
3. **The customer can reject the work proposed.** The Kertajaya Avanza brake account reports a larger replacement proposal at Auto2000 and a cheaper subsequent repair elsewhere. It shows a scope difference with technical equivalence unknown. The Plaju and Pancing accounts add why clear estimates and approval matter. The Yaris driver handled a covered service visit, while their father retained authority over extra spend.

**Decision.** Sell the next job with an exact outlet, confirmed scope and availability, installed price, and approval before changes. Start with Avanza oil and filter. A recurring fault follows a diagnostic path with symptom and repair history. Both create one case record and a completed handover.

**Teammate clarification.** Independent garages are the competitors. Integration is between Digiroom and Auto2000’s own workshop network, including OtoXpert locations that Auto2000 operates. OtoXpert is a brand with multiple dealer operators. Peta and Bojongsoang are Auto2000 examples in Bandung. A separately operated location such as Antapani does not become an Auto2000 offer purely by bearing the OtoXpert brand. [Workshop workflow](diagrams/digiroom-workshop-workflow.pdf) · [Editable workflow](diagrams/digiroom-workshop-workflow.tex)

**Commercial boundary.** The source's HEV service-record recommendation concerns completion and delegated approval. An independent-garage win-back count requires comparable prior outside use as well as a completed paid job. Confirmed eligible locations and modeled origins establish geographic options. They do not supply observed demand, slot availability, vehicle population, or realized contribution.

## Y — the next-vehicle decision

1. **A range is insufficient to act on.** The Yaris driver actually searched resale prices and stopped at a range. The Atto driver’s response to a minimum future value was a stated preference. The current offer moves the former decision forward.
2. **Gross value and buying power are separate.** Calculate inspected offer less applicable fees and official outstanding loan payoff. Then show the available equity or shortfall beside the exact replacement offer.
3. **Multiple actors can derail a deal.** Inspection, payoff, deposit, financing, reservation, and delivery need one adviser-owned record with visible expiry and status.

**Decision.** Adopt the team flowchart’s inspected offer, net equity, finance, reservation, and settlement mechanics. Keep the future resale floor and residual-value insurance as separate commercial options with an explicit promisor, terms, and funding. The concept's core starts with a firm inspected offer and ends with both handovers. [Original teammate flowchart](reference/digiroom-solution-3-teammate-flowchart.pdf)

## K — from existing Life Test to the distinguishing experience

1. **Household fit.** The Air EV and Atto interviews illustrate different real charging routines and fallback needs. A household needs to try its own parking, seating, loading, and driving situation.
2. **Cash commitment.** The Zenix finance example illustrates that upfront and monthly costs move differently. Driver and payer can be different family members, which makes the shareable brief and quote useful.
3. **Real-life drive.** A public account reported wanting to buy and being unable to find a test-drive car. Positive hybrid sale accounts show the value of adviser coordination. Make the preferred vehicle and visit a real operational handoff.

**Decision.** The user accepted teammate feedback that the original boxes sounded like the existing sales process. The distinctive experience is the **family building its own test drive**. Use the three accepted slide lines:

- **Recreate your routine in 3D.** The household recreates its garage and usual passenger and luggage arrangement.
- **Price your own driving week.** The household sees energy cost from its weekly mileage and charging setup alongside the buyer’s dated quote.
- **48-Hour Life Test.** Eligible shortlisted buyers take the confirmed model into their actual routine and return with answers to their saved checks. The branch can also offer a standard drive.

The teammate first suggested the 48-hour test drive in a WhatsApp exchange. The accepted product rationale is giving the car time to earn its place in the household’s actual life. The delivery arrangements belong to branch sales and fleet ownership. The deployed demo already shows household checks and a shareable brief. The take-home flow is part of the new build.

## Naming and final build choices

The team chose **KEY** over FIT, ACT, CAR, and PAS. **K** is Know Your Fit, **E** is Easy Service, and **Y** is Your Next Toyota. The umbrella line is *Know your fit. Book your service. Find your next Toyota.*

The creator wants judges to feel the depth of the product in actual interactions, especially 3D and geography. The accepted choices are a **full role-based demo**, **interactive maps with a bundled fallback**, and **a new KEY context folder plus the updated existing start note**. A universal resale floor is outside the core build, and real operational integrations remain separately governed by access and actual commitments. [Megaprompt](digiroom-key-megaprompt.md)
