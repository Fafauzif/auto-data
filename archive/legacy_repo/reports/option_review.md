# Independent review of solution-option scope and duplication

Reviewed 11 November 2026. This is a second-AI analytical review, not human validation, a customer preference study or a selection of a winning strategy. Inputs: 25 competition option cards, 12 market directions, 8 insurance/residual-value cards, source/evidence tables, market survey extraction, the initial and expanded app-review corpus, narrative discovery/fresh-source follow-up, and geographic sensitivity outputs. All 45 option IDs are reviewed individually in `option_review.csv` / `.json`; `build_option_review.py` reproduces that table.

The cards generally already state that benefits are hypothetical and the local gap is unestablished. That is good evidence discipline. The main remaining risk is presenting the volume of cards as the same number of independently differentiated, supported opportunities. Several describe the same mechanism or facets of one customer task. The review dispositions organize those distinctions; they are not attractiveness scores or recommendations to implement.

## Mechanism overlaps to consolidate in presentation

| Option IDs | Shared concept | What to preserve |
|---|---|---|
| OPT-C02 / MO09 | Task context carried into assisted contact | One broad continuity card, with the human-capacity and necessary-requalification rivals. |
| OPT-C05 / MO02 / OPT-C24 | Actual vehicle/cohort protection eligibility | Scheduled-maintenance conditions are a facet of entitlement clarity, not a third unrelated strategy. |
| OPT-C08 / MO10 | Meaning and limits of battery-condition evidence | Customer comprehension differs from an appraiser accepting evidence; keep OPT-C09 distinct on that point. |
| OPT-C10 / MO06 | Indicative versus inspected trade-in price | One broad valuation card; OPT-C11 concerns a different timing condition in the same journey. |
| OPT-C12 / MO08 | Simulation/prequalification versus lender commitment | One finance-status card, with true affordability as a rival. |

These are functional concept overlaps, not claims of identical wording. Other pairs require distinction rather than merging: visit preparation versus booking status; battery-check comprehension versus appraisal use; general record continuity versus a single adviser handoff; home-service suitability versus branch selection; and multi-vehicle ownership versus delegated or concurrent user access. C15's entitlement-aware cost comparison can be a facet of MO11's use-fit direction without turning every cost question into another calculator proposal.

## Existing features are the baseline

Toyota already publishes protection programs and eligible hybrid health checks. Operator pages and current public listings advertise booking, history, finance and assistance capabilities. Comparator or historical evidence cannot establish that Auto2000 lacks those functions. Most competitor cards correctly acknowledge this explicitly.

Saved journey observations UX03–UX04 document a live Auto2000 credit simulation working without mandatory contact or income entry, with insurance timing choices and repeatable outputs. UX02 documents an existing HEV/ICE comparison. These observations rule against a generic “build a calculator because none exists” or “contact is always mandatory for simulation” proposition. They do not settle whether quote assumptions, approval states or household comparisons are understandable. The saved friend-context follow-up JX03 also finds model/variant service-cost guidance with explicit March2024 estimates; that existing source is not a verified current2026 invoice or a full household driving/charging-fit tool.

Accordingly, C17 (branch matching), C20 (home-service fit) and MO04 (powertrain-specific maintenance information) are marked `notgapsupported` as current local deficits. Their underlying jobs remain legitimate. This label means a new missing-capability claim is unsupported, not that the concepts are useless. Existing branch routes, THS and manufacturer schedules must be evaluated before presenting a novel feature. C21 remains scoped to account/setup questions rather than an assertion that all vehicle linking fails.

Five original directions are explicitly exploratory: fleet/private eligibility (C07), household finance-input explanations (C13), onward mobility during repair (C19), connected-service renewal (C22), and purchase/subscription comparison (MO07). Their cited terms can explain a possible mechanism but do not establish current Auto2000 unmet demand. KINTO is an existing arrangement with eligibility/obligation limits; Hyundai renewal terms cannot be presumed to describe Toyota. These options can remain in the user's idea menu with those conditions visible.

## Insurance adds obligations, not eight wholly separate journeys

I01 describes a scoped voluntary insurer product, distinct from an OEM defect warranty. I02 concerns who owns each risk. I03 adds insurer authorization to the broader C02/MO09 context-handoff question; existing AMC/myGarda workflows are its baseline. I07 asks whether users choose a priced syariah alternative, which population share alone cannot answer. I08 is a disclosure facet shared by I02 and the residual-value concepts.

I04 capped top-up, I05 a full customer value floor, and I06 bespoke B2B residual-value risk transfer remain distinct. An insurer recovery limit does not cap an unconditional dealer promise. The available official policy covers specified insured events and objects, not ordinary future resale-price loss; a verified local syariah residual-value underwriting offer remains absent from this evidence. The 51 insurance arithmetic scenarios are synthetic contract illustrations, not observed claims or an actuarial loss distribution.

## Survey counterevidence limits exclusive diagnoses

The market workstream visually checked the Deloitte 2026 SEA consumer study's Indonesia service results. The question-specific bases differ: n=629 for usual provider/relationship questions and n=618 for relevant priority questions, within October–November 2025 fieldwork. They are not an Auto2000 customer census or EV-only sample.

For provider choice (Q17), reported Indonesian priorities include work quality 23%, trust 21%, warranty coverage 18%, convenience 12% and cost 7%. For improvement priority (Q21), transparency of pricing/work is 32% and customer treatment 28%, while online booking and appointment availability each round to 0%. For relationship (Q22), the usual servicing dealership is 46%, the vehicle brand 24% and purchase dealership 20%. These are separate questions, not additive shares of one universal journey.

The results weaken an exclusive “the main problem must be booking, app activity or price” account. They also prevent treating an app review about booking as representative of all owners. Rounded zero is not proof that nobody values booking; EV/app users may differ, and a low-salience prerequisite can still prevent a particular job. Similarly, a general importance response does not prove that Auto2000 currently lacks transparency or that a new explanation will create incremental gross profit. MO01 and protection/relationship options should retain those limits.

## Review text is not task completion or a feature census

In the initial corpus, prospective comments and branch-only experiences coexist with specific app-job claims. REV-0001 rates before the service is experienced; REV-0020 says the reviewer does not yet own a car. REV-0009 concerns workshop amenities. Those records cannot prove app task completion or a software defect. High ratings also coexist with concrete limitations, and some reviews update a problem to resolved. Use the corrected `self_reported_app_job` and `eligible_for_app_task_analysis` fields, not ratings or generic text flags as outcome labels.

The second-AI source audit inspected 30 targeted records across the first 210 rows. It requested correction of a generic BYD charging wishlist, AI work mislabeled as human, and an ambiguous exclusion flag; the reviews workstream applied these changes. This is not a representative reliability estimate or independent verification of customer truth. An English ID-storefront review discusses snow/ice, illustrating why locale does not establish residence. A review saying smart-charging controls were added and a separate wishlist for controls may refer to different versions, models or markets. C21–C23 should not turn either into a universal absence claim.

The narratives also retain positive and contrary Toyota/dealer accounts alongside complaints. Fresh follow-up found context-dependent powertrain decisions, but official-history resale premiums remained unresolved and service-queue evidence was partly historical. These boundaries apply to solution relevance: a plausible mechanism is not a measured local opportunity.

## Geographic results cannot prove a charging-service opportunity

The dataset workstream's SPKLU analysis has 2,454 source station rows and 3,767 charger-box rows; derived distance comparisons are arithmetic, not millions of customer observations. Seventeen source coordinate flags and a five-branch crosscheck showing one material disagreement of approximately 55.3 km limit location-based conclusions. The sensitivity changes the count of 28 Auto2000-name-matched sites with a non-Auto2000 alternative within 5 km from 27 to 28. It is a scenario, not corrected ground truth.

Do not infer a current coverage hole, a nearby functioning charger, driving time, permission to enter, opening hours, compatibility or capacity from those raw coordinates. MO03 is stronger as a question about household charging readiness than as a proposal justified by a map hole. C17/C18 should not acquire a charging-network claim simply because coordinates can be plotted. Independent verification of station identity and access is needed before using a specific locality example.

## Source counts and apparent independence

`option_review.csv` reports cited observation records, matched source URLs and coarse publisher clusters separately. Clusters use the supplied ownership/ecosystem group where available and the source hostname otherwise; they are coarse lineage indicators, not a formal independence audit. Distinct policy-page and PDF URLs from the same insurer therefore remain one hostname cluster. These counts are not customer samples. Examples:

- C08 cites two observations from the same Toyota health-check page.
- C11 cites several linked descriptions of the same partner transaction process; those are not independent successful transactions.
- C25 includes two observations from one Wuling release, and Chery terms are historical/index-limited.
- Deloitte's Indonesian EV article and SEA study share study lineage; their observations or sample sizes cannot be added as independent surveys.
- Market and competition workstreams can cite the same Toyota, OLXmobbi or SEVA source. Agreement between their summaries does not create another source.

Published terms prove represented offers. Current execution, adoption, confusion, commercial effect and customer preferences need their own evidence. An agent's strategic interpretation is a derived claim, not a new empirical observation. The cards should carry their common evidence lineage into any later synthesis.

## Dispositions and user choice

All 45 IDs have one review disposition: eight retain, fourteen distinguish, twelve consolidate, eight exploratory and three not-gap-supported. These labels do not rank commercial merit. “Retain” means conceptually distinct enough to remain an option at its stated evidence level. “Consolidate” means combine duplicate mechanisms in the user's menu. “Distinguish” means preserve a clear actor/task difference rather than inflate or collapse it. “Exploratory” exposes missing local relevance. “Not-gap-supported” prevents treating an existing capability as absent.

The final solution menu should show the customer question, existing capability, specific possible improvement, supporting and contrary evidence, dependencies and unresolved assumptions. The user chooses which concepts to develop. No winning strategy, rollout, budget allocation or implementation is selected by this review.


## Friend-context follow-up boundary

Saved JX02 shows an existing digital health-certificate retrieval route, and JX07 shows BEV trade-in model selection. M2 must therefore be distinguished by evidence acceptance and continuity into appraisal, not by claiming the first certificate or first BEV appraisal. JX05 demonstrates working broad branch/service filters and a guest booking route; R2 remains a question about model/job-specific qualification and fulfilled confirmation. The separate friend challenge register preserves the unmeasured exposure-to-sales chain and the survey-base audit: the supplied Rakuten57/28 awareness values are not independently verified here, and no awareness percentage proves a delivered sale.
