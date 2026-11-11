# Competitive mechanisms and stakeholder dependencies

Research date: 11 November 2026. This workstream studies what public operators actually advertise and condition, rather than ranking whole brands or claiming commercial effectiveness. It collected 45 structured observations from 26 distinct source URLs across 11 core ecosystems plus one provisional MG source family. Nineteen source URLs were opened in the web retrieval tool; other records explicitly retain search-index or full search-content status. Direct HTTP verification is separately logged. A source can contain several observations; these are not independent customers, transactions, or external corroborations.

## Scope and evidence quality

Core groups: Toyota OEM, SEVA, OLXmobbi, Nasmoco, Tunas Toyota, Astrido Toyota, BYD, Hyundai, Wuling, Chery and Honda. MG is provisional because the search index returned unusual same-domain subhosts and the canonical main-host article could not be opened. Nasmoco's directly opened pages returned JavaScript shells, while search-index text exposed capabilities; that limitation is retained. Chery full-page retrieval failed on selected URLs, so its cited historical terms remain index-based. This scope is a purposive comparison, not an exhaustive market census or matched live usability trial.

Files: `evidence_matrix.csv` and `.json` hold record-level evidence and limitations; `sources.json` gives URL, retrieval reference, source date and method; `direct_verification.json` records raw source checks and failures. Raw response bodies belong to the shared private cache and should not be included wholesale in a public ZIP. No forms, OTPs, messages, booking, account access or purchases occurred.

Operator claims can establish a stated promise, eligibility and named responsible actor. They do not establish adoption, customer satisfaction, achieved time, a working integration, operational capacity, conversion or contribution. “Unknown” is not “absent.” Historical offers remain tied to their dates and named models. A generic OEM claim, a dealer form and a financing platform have different mandates; do not use their feature counts as a brand league table.

## 1. Specific observed mechanisms and the comparison they support

| Comparison | Public evidence | Strength / useful mechanism | Counterexample or boundary | Evidence IDs |
|---|---|---|---|---|
| Existing Toyota app coverage | mToyota already advertises service history/progress and purchase-related continuity | Existing capability is a necessary baseline for a proposed Digiroom gap | Published availability says nothing about actual interoperability or account completeness | COMP-001–002; T01 |
| Service entitlement versus warranty continuation | Toyota distinguishes T-Care's included work from conditional XTRA coverage | Program state and vehicle cohort matter | Program maxima are not an unconditional warranty or verified dealer margin | COMP-003–004; T02 |
| Health evidence versus claim approval | Toyota ties a health certificate to eligible periodic service; an adverse result requires dealer validation | Evidence creation and warranty decision are separate steps | Does not prove certificate changes resale value or customer choice | COMP-005–006; T03 |
| Finance tool versus underwriting | SEVA markets a financing route but terms locate financial-service decisions with partners | Useful digital support can coordinate a decision without controlling it | Approval has data and expiry conditions; the platform cannot promise every applicant acceptance | COMP-007–010; S01–S02 |
| Valuation estimate versus actual purchase | OLXmobbi separates indicative valuation from physical verification and final agreement | Makes uncertainty and handoff explicit | Transaction not guaranteed; quoted payment timing starts after agreement/documents | COMP-011–014; O01–O03 |
| Same-brand dealer booking controls | Tunas separates general service/B&P; Astrido distinguishes workshop/home service and lead-time conditions | Dealer-specific tasks and data requirements can be compared | Static page text and hidden validation templates are not completed journeys | COMP-017–020; U01/A01 |
| Connected utility versus dealer commerce | BYD advertises vehicle state, remote functions and OEM-assisted linking | Some app reasons-to-return depend on vehicle integration | Capability differs by model/device; enrollment itself can involve dealer work and waiting | COMP-022–025; B01–B02 |
| Warranty versus digital-service contract | Hyundai distinguishes vehicle/battery terms from a time-limited free connected service | Contract and renewal states affect long-term digital access | No retention, renewal or subscription-price uplift is demonstrated | COMP-027–029; H01–H02 |
| Emergency promise versus physical reach | Hyundai, Wuling and Honda publish differing service radii, hours and scope | Local capability and eligibility define whether a promise is usable | A 24-hour contact route does not imply every technician service everywhere is 24-hour | COMP-030–033/040; H03/W01/F02 |
| Lifetime protection versus transfer/use conditions | Wuling and Chery historical lifetime campaigns have owner, mileage or campaign conditions | Full eligibility can matter more than the headline duration | Historic limited offers do not establish universal current cover or transferable resale protection | COMP-034–037; W02/C01–C02 |
| Booking request versus confirmed capacity | Honda's guide names an awaiting-confirmation state | A clear example of human confirmation within a digital task | No actual waiting time, response quality or reservation fulfillment was measured | COMP-038–039; F01 |

These comparisons do not identify an Auto2000 customer problem on their own. They identify concrete dimensions that the Auto2000 source and journey workstreams can test against a better-defined baseline.

## 2. Bounded analytical findings

### A. A useful dealer interaction can be a verification transition

Observed: health certification, actual used-car appraisal and requested service dates rely on distinct verification or confirmation steps in published operator processes (T03, O02 and F01). Inference: the strategic unit worth investigating is the customer's unresolved decision and its verification state, rather than the mere presence of a calculator, certificate or booking icon. Rival: these handoffs may already work adequately and may be operationally necessary. What remains unknown is whether Auto2000 loses time, trust or transactions at a specific transition. This supports a diagnosis question, not a feature recommendation.

### B. Warranty headlines are not directly comparable ownership propositions

Observed: published protections differ in vehicle/component scope, time/mileage, upkeep, first-owner/use restrictions, geographical support and campaign eligibility. Inference: a comparison that ranks only years can misdescribe the customer proposition. For example, a historical first-owner benefit cannot automatically support a claim about a later used buyer's protection. Rival: actual buyers may understand the terms well or care more about upfront price. Customer choice and monetary value remain unmeasured. The research should preserve these fields instead of collapsing them into a warranty score.

### C. Vehicle-connected engagement has an OEM control boundary

Observed: BYD connected functions depend on vehicle/model/device and OEM-assisted account linking; Hyundai's connected service has its own compatible-vehicle and contract conditions. Inference: using these apps as benchmarks for dealer-app frequency without adjusting for their vehicle-control job risks an invalid comparison. Rival: dealer apps may have equally consequential non-telemetry jobs. The relevant question is whether Auto2000 controls a useful customer decision, or needs an OEM/partner dependency whose availability and economics are unknown.

### D. The ecosystem already contains commercial decision infrastructure

Observed: Toyota's app/aftersales routes, SEVA financing and OLXmobbi appraisal cover parts of purchase and ownership. Inference: there may be opportunities in discovering, explaining or connecting existing capabilities. That is still only a direction to investigate. Rival: current routes are already complementary and coherent, or product price/stock is the actual constraint. We have no evidence of architectural duplication, failed integration or incremental sales caused by combining functions.

### E. A service feature has a local fulfillment shape

Observed: multiple operators condition support on branch geography, hours, mileage, use and underlying coverage. Inference: “available nationwide” or “24/7 support” should be decomposed into contact, verification, dispatch and actual work by location. Rival: the customer may only need a reliable referral and not immediate dispatch. This is especially relevant to fleet/household tasks and specialist repair, but this workstream has not measured Auto2000 branch capacity or underserved demand.

## 3. Seventeen stakeholder lenses: grounded evidence versus inference

A stakeholder lens is analytical interpretation. It must not be written as an interview quote, actual compensation rule or reported internal priority. The supplied case stakeholder comments are separate from the source evidence below.

| Actor | Grounded public evidence | Inference / tension to investigate | Evidence still unavailable |
|---|---|---|---|
| Digital business owner | OEM apps and adjacent platforms advertise overlapping customer jobs (T01/S01) | Value may sit in continuity or context rather than more icons | Incremental outcomes by channel; actual Digiroom integration |
| Sales director | Financing and appraisal decisions have stated prerequisites and responsible partners (S02/O02) | Some sales losses may arise outside app design | Stock, credit denials, fit, qualified leads and delivered GP |
| Branch manager | Appointment and physical-service conditions are explicit in selected dealer pages (A01/U01) | Central promises can create local work; their fit must be checked | Branch policy, capacity, transfers and actual incentive rules |
| Sales adviser | Nasmoco inquiry text distinguishes request type and purchase horizon (N02) | Context could help qualification, but more fields can add effort | Adviser use, duplicate leads, contact timing and net conversion |
| Service adviser | Toyota gives the dealer a validation role after an adverse health result (T03) | Explaining the status of a result can be a consequential task | Customer comprehension, disputes and resolution quality |
| Technician/workshop manager | Original-parts and official-maintenance conditions are stated by selected OEMs (B02/H01) | Promoted demand needs capable workshop fulfillment | Skill/bay utilization, repair time, displaced contribution and safety outcomes |
| Parts team | Selected warranties condition use on original parts (B02/W02) | Correct fit and part availability may affect ownership confidence | Stockouts, fitment errors, returns and realized parts margin |
| Body/paint/insurer liaison | Tunas exposes a distinct B&P request with damage details (U01) | B&P has a different trigger and qualification need from scheduled service | Insurer approval, scope, capacity, actual wait and GP |
| CFO | Public benefits contain conditions; some priced extensions exist (H01/O01) | A promise can have cost and partner exposure without incremental dealer value | Programme cost, uptake, partner share, cannibalization and counterfactual |
| CRM/privacy owner | Account linking/finance requires identity and vehicle data in stated workflows (B01/S02) | Field purpose and timing should be judged against the job, not simply minimized | Consent comprehension, data quality, actual use, field-level abandonment |
| Toyota OEM | mToyota and Toyota's warranty/health programs own named capabilities (T01–T03) | Dealer differentiation must account for shared OEM control | Permissions, service interfaces, usage and actual dealer agreements |
| Finance partner | SEVA terms place financial-service decisions with partners (S02) | Decision support and approval are different promises | Actual underwriting inputs, acceptance, rework and economics |
| Trade-in/appraisal partner | Indicative and inspected values are explicitly distinguished (O02–O03) | A credible estimate may need a visible uncertainty boundary | Actual valuation dispersion, buyer acceptance and residual risk |
| Household buyer/payer/driver | BYD limits concurrent phone use; SEVA references spouse identity for married applicants (B01/S02) | Household roles can diverge, but these terms do not establish coordination pain | Real role distribution, choices and willingness to share tasks/data |
| Existing owner | Benefits depend on service, vehicle and eligibility state (T02/H01/F02) | Needs and useful contact cadence likely vary by cohort | Work due, current capture, non-user experience and retention |
| Fleet administrator/procurement/driver | Selected historical first-private-owner offers exclude commercial use (W02/C01) | Consumer protection headlines may not fit fleet economics | Actual fleet terms, approval chains, downtime and account contribution |
| Competing dealer/OEM/independent provider | Different operator processes and conditional promises are published | Competitors can solve one task better without being better on every task | Matched live outcomes; independent-garage comparative economics |

## 4. Counterexamples and rejected shortcuts

- Existing mToyota service-history and monitoring claims weaken any blanket claim that Toyota has no ownership continuity capability. They do not disprove incompleteness in a particular account.
- SEVA's financing tools weaken a claim that the Astra ecosystem has no financing decision support. Partner terms weaken a claim that such support guarantees finance.
- OLXmobbi inspection/appraisal weakens a claim that no trade-in valuation mechanism exists. Its non-guarantee weakens an automatic resale-value-guarantee story.
- BYD's dealer-assisted linking and device limitations show competitor features come with dependencies. Attractive connected features do not establish frictionless onboarding.
- Honda's awaiting-confirmation guide shows that a digital request followed by human contact can be an intended process. Such a state is not inherently a broken booking.
- Tunas and Astrido expose task-specific service routes. Do not assume an app is the only viable digital channel or that fewer visible fields automatically mean better fulfillment.
- Hyundai emergency geography and Wuling service terms weaken a universal “24-hour nationwide field fulfillment” comparison.
- Historical warranty campaigns should not be treated as current nationwide entitlements. The report retains date, named model and access method instead.

## 5. Research direction menu, without selecting solutions

| Direction to investigate | Supporting mechanism | Rival that could make it unattractive | Evidence needed before user chooses |
|---|---|---|---|
| Decision evidence at a consequential transition | Public verification/confirmation states exist | Existing handoffs are clear and effective | Current Auto2000 transition evidence and reported decision consequence |
| Existing-capability role clarity | Several ecosystem tools already serve related jobs | Roles already complement one another with little burden | Matched customer tasks, required repetition and actual context continuity |
| Eligibility-aware ownership information | Benefits vary by cohort, use and programme | Customers understand or do not value the differences | Current terms, customer questions and relevant decision moments |
| Local task/capability discovery | Field-service boundaries vary by locality and work type | Generic referral/contact is sufficient | Auto2000 task-level capability facts and wrong-routing accounts |
| Household/fleet decision evidence | Some eligibility and account rules distinguish actors/use | No consequential shared decision burden exists | First-person role and choice sequences, not inferred demographics |
| Commercial versus information explanation | Partners control finance/appraisal and vehicles differ | Better information is enough to enable an already viable offer | Affordability, suitability and choice evidence alongside current offer facts |

This workstream does not select a final strategy, estimate causal conversion, propose implementation or run a pilot. Its endpoint is a source-grounded diagnosis aid, counterevidence and differentiated research directions for the user to assess.

## Direct-verification addendum

The shared transport fetched 22 source pages after host-level robots checks; all returned HTTP 200, but the two Nasmoco hosts provided zero extracted visible words and therefore do not validate their indexed functional descriptions. Chery and the provisional MG host queues stopped after robots retrieval returned 503; the Honda main host queue stopped after robots returned 403. Its e-Care documentation subhost was accessible separately. Toyota main-host robots returned 404; the public mToyota page was fetched. No proxy or login alternatives were used. Transport success is distinct from content support, current interactive behavior and customer success. Every matrix record retains both web-retrieval status and the direct-verification status/request ID; never relabel index-only Chery/MG or shell-only Nasmoco descriptions as direct page validation.

Fifty-three targeted term checks across 20 successful, non-empty cached source pages found 52 expected text substrings. The remaining SEVA partner label was absent from text nodes but independently located in an image alt attribute; a separate alt check records this distinction. A successful substring check supports the cited wording, not implementation, truth of a commercial promise or business impact.

Additional counterexamples: Hyundai explicitly gives model-specific general-warranty periods (COMP-043), and Toyota separates LCGC labour-only service entitlement from standard T-Care (COMP-044). An Astrido retrieved navigation value of Rp0 for Hilux Battery EV is retained as an apparent placeholder (COMP-045), not a transaction price. These examples weaken any benchmark that treats competitor content as uniformly precise or collapses model-specific benefits into a brand-level headline.
