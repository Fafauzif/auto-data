# An economic model that can be filled without changing its meaning

## The case baseline

Use `case_business_line_inputs.csv` for the original case's FY2025 line values. The original casebook was read in full for this release. Its page 10 gives revenue69,000 and GP6,750 in IDRbn, operating expenses4,620 and operating profit2,130. These are case assumptions across powertrains. Do not apply their average line margins to a job or an xEV product without unit-cost evidence.

The model's primary partition is a mutually exclusive vehicle/job/period/entity/payer cohort. A service work order can contain labor and parts, but is still one visit. The recognized revenue/direct-cost components can be split without counting two completed customer jobs. Separately report completed vehicle deliveries, service work orders, inspected trade-in offers and actual replacement transactions.

## Eligible opportunities and completion

For each cohort c and job j in a period:

`eligible_opportunities[c,j] = reachable_vehicles[c] × due_or_trigger_incidence[c,j] × applicable_eligibility[c,j]`

`completed_jobs[c,j] = eligible_opportunities[c,j] × all_channel_completion_capture[c,j]`

Repeated due events may be modeled as a rate rather than a probability. The count and period must make that explicit. Where opportunities originate as named leads rather than an installed vehicle base, begin with deduplicated eligible cases and retain their source. Do not multiply national car stock, survey intention or grid origins by an invented dealer conversion rate.

## Recognized contribution and incrementality

`job_GP = recognized_job_revenue − recognized_direct_cost`

`incremental_GP = sum(with_change_completed_jobs × with_change_job_GP) − sum(counterfactual_completed_jobs × counterfactual_job_GP)`

`incremental_operating_contribution = incremental_GP − incremental_below_GP_operating_cost`

Direct costs, discounts, benefits, reimbursements and recoveries each receive one location. If feasible displaced jobs are already absent from with-change volumes or included in counterfactual volumes, do not subtract them a second time. If a proposed intervention consumes a constrained resource, compare its realizable contribution with the best displaced feasible work. Record capacity as unknown when no actual bay/technician/job-time data exist.

For the same dealer replacing an otherwise expected ICE sale with an xEV sale, model the realized GP difference rather than booking the entire vehicle GP as incremental. If timing changes, compare matched periods or include the later displaced sale. For conquest from another Toyota dealer, Auto2000 and Toyota brand outcomes differ. For OtoXpert or partner referral, recognized Auto2000 contribution depends on the actual operator/perimeter and contract; customer travel savings alone do not determine dealer accounting.

## A useful no-effect control

Counterfactual100 completed jobs through non-Digiroom routes, with GPu each, become100 completed jobs through Digiroom at the same GPu. Incremental transaction GP is zero. More app bookings can still generate real separately measured operating savings or later outcomes, but those do not arise merely from attribution. This is an identity, not evidence that every app intervention has no value.

## Thresholds instead of unsupported forecasts

`required_incremental_jobs = incremental_cost / net_incremental_contribution_per_job`

`required_gross_recruited_jobs = incremental_cost / (incremental_share × contribution_per_incremental_job)`

These expressions require consistent periods and an incremental-share definition. They do not become a forecast until actual reachable volumes, eligible job incidence, contribution and response assumptions are supplied. Report the threshold and the business inputs that would meet it. A return scenario is explicitly hypothetical; it should never be labeled observed GP impact.

## Three prong-specific outcome chains

| Prong | Meaningful digital events | Commercial endpoint | Main controls |
|---|---|---|---|
| New-to-Auto2000 xEV acquisition | Completed fit/cash-flow brief, accepted adviser handoff, confirmed suitable demonstration | Delivered vehicle with recognized contribution | Product/stock/price, credit, channel substitution, customer prior relationship |
| Ownership and paid-work recovery | Due/trigger eligibility, accepted scope, correct route, confirmed slot/parts, authorized work | Completed work order and recognized payer-specific GP | Entitlements, programme reimbursement, job incidence, operator, capacity, existing captured demand |
| Repeat xEV replacement/trade-in | Consented record use, inspection, accepted evidence, inspected offer, net-upgrade decision | Completed replacement/trade-in transaction | Market value, customer finance balance, offer expiry, counterparty, margin substitution, actual retained risk |

Ordinary petrol paid-job pilots can test the shared workflow, but the main case report must explicitly show how the digital mechanism serves HEV/PHEV/BEV customers. Do not infer BEV scheduled oil demand. A health check, safety campaign or warranty repair is not automatically discretionary paid upsell.

## Interview pilot measurement

For the proposed Yaris Cross Hybrid service test, use verified customer-paid or mixed eligibility to define the commercial cohort. Keep covered completion and reimbursement available as distinct outcomes. Include normal WhatsApp or assisted service in both comparison groups. Measure actual approvals, completed paid work, recognized contribution and meaningful Digiroom return, then reconcile displacement, costs and capacity once. Interview reactions enter the pilot design and hypotheses. Leave completion uplift, per-vehicle economics and guarantee redemption blank until operational observations support them. [Pilot decision](../interviews/pilot_decision.json)

## Cost, investment and future promises

The original case p6 caps incremental investment at IDR150bn during2026–2028. This does not require spending the cap. Show implementation cash, operating cost, direct cost, depreciation and post-horizon obligations on appropriate ledgers. A future price guarantee is not bounded by a three-year software budget merely because it was launched within that budget.

Use staged commitments: establish the existing source/state/permission contract; test a bounded customer/job/branch workflow; expand only when completion and contribution clear the threshold. Measure repeated meaningful digital engagement alongside the completed commercial result, as required by the case. An operational improvement that never gives customers a differentiated digital reason to return is incomplete against the mandate.

## Measurement without an app-attribution trap

Use an opportunity-cohort design including assisted/offline customers. Freeze eligibility before comparing channels. Capture request, receipt, acknowledgment, confirmation, arrival, authorization, completion, cancellation and exception timestamps. Record the actual reason for loss or change. Evaluate a staggered or randomized bounded rollout where feasible, with capacity and seasonality controls. If no credible control is possible, report descriptive changes rather than causal uplift.

The first decision gate is whether the intervention improves the intended transition without increasing rework, wrong routing, unsupported promises or displaced contribution. The second is incremental completed contribution per eligible cohort. Downloads, MAU, sessions, request volume and certificate volume remain supporting measures with their own denominators.
