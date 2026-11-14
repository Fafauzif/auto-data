# Six economics pages for the concise research memo

Profit depends on the completed job, its programme and payer, and retained obligation. App activity and large datasets do not identify those economics.

| Page | Exact finding headline | Evidence |
|---|---|---|
| EC01 | After-sales provides 46.7% of case gross profit from 13.0% of revenue. | SUPPLIED CASE ASSUMPTIONS • FY2025 • NOT AUDITED COMPANY ACCOUNTS |
| EC02 | Toyota and Lexus xEV sales fell 6,025 units as portfolio scale and mix both decreased. | OBSERVED BRAND-PORTFOLIO COUNTS + DERIVED ACCOUNTING • NOT CAUSAL ATTRIBUTION |
| EC03 | A longer programme maximum can cover fewer service events and different parts benefits. | PUBLISHED PROGRAMME TERMS • ORDINAL EVENTS • NOT PERSONALISED ENTITLEMENT |
| EC04 | The bZ4X tool’s four later-service estimates total Rp9.101 million on a March 2024 basis. | DATED RETAIL ESTIMATES • MARCH2024 BASIS • OBSERVED11NOV2026 |
| EC05 | A Rp10 million top-up leaves a Rp160 million offer below a Rp200 million floor. | ILLUSTRATIVE CONTRACT ARITHMETIC • NOT AN OFFER, POLICY OR FORECAST |
| EC06 | The same pooled offers create higher peak retained losses when low valuations arrive together. | ILLUSTRATIVE JOINT STRESS STATES • NO PROBABILITIES OR EXPECTED-LOSS ESTIMATE |

The plotting data below come only from frozen research artifacts. Case assumptions, actual source counts, dated estimates and illustrations are not pooled. Every body is60–90words. User reference material supplies visual style only.

## EC01: After-sales provides 46.7% of case gross profit from 13.0% of revenue.

The supplied case assigns Rp3,150 billion of gross profit to services, spare parts and body and paint, against Rp9,000 billion of revenue. Vehicle sales remain the largest individual profit pool. This makes the economics of completed ownership jobs material even when they generate fewer app sessions. The four lines belong to one case P&L, not four customer samples. A programme still needs incremental contribution after its own costs.

**Evidence label:** SUPPLIED CASE ASSUMPTIONS • FY2025 • NOT AUDITED COMPANY ACCOUNTS

**Layout:** One dominant chart, concise body beside it, source and limit immediately below the chart.

**Visual:** {"type": "horizontal_bar", "category": "business_line", "value": "gross_profit_idr_billion", "unit": "IDR billion", "axis_min": 0, "axis_max": 4000, "order": ["Vehicle sales", "Services", "Spare parts", "Body and paint"], "direct_labels": "Gross profit plus share of total case GP; retain one color family for the three after-sales lines."}

**Exact plot data:**

```json
[
  {
    "business_line": "Vehicle sales",
    "gross_profit_idr_billion": 3600,
    "revenue_idr_billion": 60000,
    "share_of_case_gp_pct": 53.333333333333336,
    "display_share_pct": 53.3
  },
  {
    "business_line": "Services",
    "gross_profit_idr_billion": 1320,
    "revenue_idr_billion": 2400,
    "share_of_case_gp_pct": 19.555555555555557,
    "display_share_pct": 19.6
  },
  {
    "business_line": "Spare parts",
    "gross_profit_idr_billion": 1200,
    "revenue_idr_billion": 4800,
    "share_of_case_gp_pct": 17.77777777777778,
    "display_share_pct": 17.8
  },
  {
    "business_line": "Body and paint",
    "gross_profit_idr_billion": 630,
    "revenue_idr_billion": 1800,
    "share_of_case_gp_pct": 9.333333333333334,
    "display_share_pct": 9.3
  }
]
```

**Highlight:** After-sales: Rp3,150bn, 46.7% of GP

**Source note:** Source: supplied IBSC casebook, Exhibit 3, printed/PDF p10. Business-line case assumptions, not audited Auto2000 results.

**Source paths:**
- `/workspace/scratch/70444ed5f561/upload/Semifinal Casebook IBSC 2026.pdf`. Exhibit3, printed/PDF p10. Supplied FY2025 case P&L.
- `/workspace/scratch/70444ed5f561/auto2000_run/reports/NUMERICAL_QA.md`. NQ04–NQ12. Independent arithmetic audit of supplied case values.

**Limits:**
- GP differs from operating profit and programme cash flow.
- Line-average margins do not identify EV-specific or per-job contribution.
- Labor and attached parts can belong to the same work order; do not count them as two customer visits.

**Bridge:** Separate the case profit perimeter from the next page's external brand-portfolio sales data.

## EC02: Toyota and Lexus xEV sales fell 6,025 units as portfolio scale and mix both decreased.

Astra reports 37,693 Toyota and Lexus xEV sales in 2024 and 31,668 in 2025. The symmetric accounting bridge assigns about 5,050 fewer units to the total-portfolio scale term and 975 to its xEV mix term. Averaging both calculation orders removes an arbitrary ordering choice. These terms reconcile the observed change; they do not measure the effects of national demand, Digiroom or any proposed solution.

**Evidence label:** OBSERVED BRAND-PORTFOLIO COUNTS + DERIVED ACCOUNTING • NOT CAUSAL ATTRIBUTION

**Layout:** One dominant chart, concise body beside it, source and limit immediately below the chart.

**Visual:** {"type": "waterfall", "category": "label", "value": "value_vehicles", "unit": "Toyota and Lexus vehicles", "axis_min": 0, "axis_max": 42000, "labels_decimals": 0, "change_colors": "One restrained change color; totals share a dark neutral.", "connector_lines": true}

**Exact plot data:**

```json
[
  {
    "label": "2024 xEV sales",
    "bar_type": "total",
    "start_vehicles": 0,
    "end_vehicles": 37693,
    "value_vehicles": 37693
  },
  {
    "label": "Portfolio scale term",
    "bar_type": "accounting_change",
    "start_vehicles": 37693,
    "end_vehicles": 32643.11622696906,
    "value_vehicles": -5049.883773030939
  },
  {
    "label": "xEV mix term",
    "bar_type": "accounting_change",
    "start_vehicles": 32643.11622696906,
    "end_vehicles": 31668,
    "value_vehicles": -975.1162269690604
  },
  {
    "label": "2025 xEV sales",
    "bar_type": "total",
    "start_vehicles": 0,
    "end_vehicles": 31668,
    "value_vehicles": 31668
  }
]
```

**Highlight:** −5,049.884 scale + −975.116 mix = −6,025 vehicles

**Source note:** Source: Astra AR2025, printed p140/PDF p142. Toyota AND Lexus domestic new sales. Shapley terms are accounting allocations, not causes or Auto2000 volume.

**Source paths:**
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/friend_capabilities/numeric_observations.csv`. FC-N12–FC-N15; AR2025p140/PDF142. Original chart transcription.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/portfolio_inputs_and_method.json`. All four counts and exact symmetric formula. Derived arithmetic.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/portfolio_decompositions.csv`. Both orderings and symmetric average. Ordering sensitivity retained.

**Limits:**
- Do not label the scale term a national-market effect.
- Do not label the mix term a Digiroom effect.
- These are Toyota and Lexus sales flows, not Auto2000 sales or the installed service base.

**Bridge:** Move from new-sales flows to the entitlement rules that govern ownership jobs.

## EC03: A longer programme maximum can cover fewer service events and different parts benefits.

Current Toyota material gives T-CARE seven scheduled labor-and-parts events within three years or 60,000 km. T-CARE Lite covers labor for seven events; its parts package is separate. Legacy GBSB allows six events within four years or 50,000 km. Its published calendar lists events through month 30. Headline years therefore do not identify covered visit count, the customer’s actual payment date or dealer gross profit. Eligibility and specified work still govern.

**Evidence label:** PUBLISHED PROGRAMME TERMS • ORDINAL EVENTS • NOT PERSONALISED ENTITLEMENT

**Layout:** One large three-row coverage matrix. Keep event ordinals on the main axis and maximum years/km as a separate right-hand note.

**Visual:** {"type": "ordinal_coverage_matrix", "rows": "program", "columns": "Service event1through8", "event_axis": [1, 2, 3, 4, 5, 6, 7, 8], "encode_labor": "Upper half of event cell", "encode_parts": "Lower half; empty means not included in this base programme, not no parts work.", "right_labels": "Maximum years/km and eligible cohort, separate from the ordinal axis.", "do_not_use": "Do not draw a continuous four-year free-service bar."}

**Exact plot data:**

```json
[
  {
    "program": "T-CARE",
    "covered_scheduled_event_count": 7,
    "covered_labor": true,
    "covered_specified_parts": true,
    "first_event": 1,
    "last_event": 7,
    "maximum_years": 3,
    "maximum_km": 60000,
    "scope": "Eligible purchases from July2022; exclusions and terms apply."
  },
  {
    "program": "T-CARE Lite",
    "covered_scheduled_event_count": 7,
    "covered_labor": true,
    "covered_specified_parts": false,
    "first_event": 1,
    "last_event": 7,
    "maximum_years": 3,
    "maximum_km": 60000,
    "scope": "Eligible LCGC purchases from January2023. Optional Lite+ parts package is separate."
  },
  {
    "program": "Legacy GBSB",
    "covered_scheduled_event_count": 6,
    "covered_labor": true,
    "covered_specified_parts": true,
    "first_event": 1,
    "last_event": 6,
    "maximum_years": 4,
    "maximum_km": 50000,
    "scope": "Eligible legacy cohorts; current page identifies January2020–June2022. Model service-book terms apply."
  }
]
```

**Highlight:** Seven events / three-year maximum versus six events / four-year maximum

**Source note:** Source: Toyota T-CARE programme page;2026XTRAannouncement; legacy GBSB PDF p1. Time/km means whichever first; eligibility, specified work and model terms apply.

**Source paths:**
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/program_distinctions.csv`. T-CARE, Lite and GBSB rows; EE-S01/EE-S03/EE-S04. Published programme distinctions.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/legacy_scheduled_calendar.csv`. Six recommendations; EE-S11PDF p1. Legacy model/programme table.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/source_checks.csv`. EE-S01,EE-S03,EE-S04,EE-S11. Original public URLs and retrieval limits.

**Limits:**
- Labour coverage is not universal parts coverage.
- Maximum duration is not an observed return date.
- A zero customer bill does not reveal OEM reimbursement, dealer direct cost or GP.
- Do not transfer legacy terms to a current model without eligibility evidence.

**Bridge:** Show one model's dated post-coverage estimates without converting retail fees into dealer margin.

## EC04: The bZ4X tool’s four later-service estimates total Rp9.101 million on a March 2024 basis.

The public Toyota tool lists bZ4X Panoramic View estimates from Rp847,000 at visits 8 and 10 to Rp3,713,000 at visit 11. Labor and parts sum to Rp9,101,000 across the four events. The opened note dates these estimates to March 2024 and allows dealer and additional-work differences. These are useful illustrations of uneven bills, not current invoices, total ownership cost, dealer margin or a forecast of customer spending.

**Evidence label:** DATED RETAIL ESTIMATES • MARCH2024 BASIS • OBSERVED11NOV2026

**Layout:** One dominant chart, concise body beside it, source and limit immediately below the chart.

**Visual:** {"type": "stacked_columns", "category": "service_event", "series": ["labor_estimate_idr", "parts_estimate_idr"], "unit": "IDR; display axis as Rp million", "axis_min": 0, "axis_max_idr": 4200000, "order": [8, 9, 10, 11], "direct_labels": "Total above each column; legend has labor and parts only.", "model": "All New BZ4X Battery EV; Panoramic View variant"}

**Exact plot data:**

```json
[
  {
    "service_event": 8,
    "labor_estimate_idr": 847000,
    "parts_estimate_idr": 0,
    "total_estimate_idr": 847000
  },
  {
    "service_event": 9,
    "labor_estimate_idr": 1582000,
    "parts_estimate_idr": 2112000,
    "total_estimate_idr": 3694000
  },
  {
    "service_event": 10,
    "labor_estimate_idr": 847000,
    "parts_estimate_idr": 0,
    "total_estimate_idr": 847000
  },
  {
    "service_event": 11,
    "labor_estimate_idr": 1073000,
    "parts_estimate_idr": 2640000,
    "total_estimate_idr": 3713000
  }
]
```

**Highlight:** Four-event estimate: Rp9,101,000

**Source note:** Source: Toyota model/variant cost tool, XT04, observed11Nov2026. Estimates explicitly based on March2024; tax included; dealer/extra-work caveats. Not a current quote or GP.

**Source paths:**
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/service_estimates_extension.csv`. XT04; bZ4X Panoramic View, visits8–11. Observed displayed amounts and date note.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_journeys/observations.json`. XT04. Researcher walkthrough; no VIN or submitted request.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/dated_service_estimate_sums.csv`. All New BZ4X Battery EV. Recomputed labor/parts totals.

**Limits:**
- Do not display these as2026prices.
- Do not multiply by case line margins to create EV-specific GP.
- No matched BEV-versus-HEV comparison or causal powertrain effect is shown.
- FREE/zero parts entries do not establish zero work or zero dealer cost.

**Bridge:** Separate ordinary retail-payment information from a proposed promise about a future resale value.

## EC05: A Rp10 million top-up leaves a Rp160 million offer below a Rp200 million floor.

In this constructed example, the capped top-up adds Rp10 million to a Rp160 million offer, producing Rp170 million of customer credit. A separate full-floor promise requires Rp200 million. Its Rp40 million shortfall leaves Rp25 million with the dealer after the assumed Rp15 million insurer layer, using a Rp10 million retention. That arithmetic excludes contribution and running costs. No actual policy, underwriting appetite or approved Auto2000 offer is established.

**Evidence label:** ILLUSTRATIVE CONTRACT ARITHMETIC • NOT AN OFFER, POLICY OR FORECAST

**Layout:** Two panels: customer credit on the left, funding of full-floor shortfall on the right. Print ILLUSTRATIVE beside both panels.

**Visual:** {"type": "two_panel_contract_comparison", "left": "Zero-based customer-credit columns: offer160m, capped credit170m, full-floor credit200m.", "right": "Full-floor shortfall40m stacked as assumed insurer15m and dealer residual25m.", "unit": "IDR; display Rp million", "axis_min": 0, "customer_credit_axis_max_idr": 220000000, "shortfall_axis_max_idr": 45000000}

**Exact plot data:**

```json
[
  {
    "design": "Capped top-up",
    "valid_offer_idr": 160000000,
    "topup_idr": 10000000,
    "customer_credit_idr": 170000000,
    "minimum_floor_promised": false,
    "full_floor_shortfall_idr": null,
    "conditional_insurer_payment_idr": null,
    "dealer_full_floor_residual_idr": null
  },
  {
    "design": "Full floor with assumed insurer layer",
    "valid_offer_idr": 160000000,
    "topup_idr": null,
    "customer_credit_idr": 200000000,
    "minimum_floor_promised": true,
    "full_floor_shortfall_idr": 40000000,
    "conditional_insurer_payment_idr": 15000000,
    "dealer_full_floor_residual_idr": 25000000
  }
]
```

**Highlight:** Capped credit Rp170m; full floor leaves Rp25m dealer exposure

**Source note:** Constructed illustration using declared floor/cap/retention/layer assumptions. All losses assumed eligible and aggregate cover available; premium, expenses and timing excluded. No available policy verified.

**Source paths:**
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/constructed_contract_tail.csv`. valid_offer160000000 row. Constructed per-unit arithmetic.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/friend_insurance/analysis.md`. Capped top-up and full-floor distinction. Source/contract availability remains unresolved.

**Limits:**
- Do not call the capped top-up a guaranteed Rp200m floor.
- The insurer layer is assumed, conditional and not a quote.
- Dealer residual includes retention and loss beyond the assumed layer.
- Contribution is not dealer GP; actual fees and margins remain unknown.

**Bridge:** Test the same promise at portfolio level, where timing and an aggregate limit change the retained obligation.

## EC06: The same pooled offers create higher peak retained losses when low valuations arrive together.

These constructed worlds use the same twenty units and the same pooled low and high offers across two stress states. Dispersion puts ten low offers in each state; synchronization puts all twenty in one. Under the assumed Rp100 million aggregate recovery limit, the highest dealer residual rises from Rp300 million to Rp700 million. No probability is assigned. This exposes a limit of per-unit reasoning without estimating actual correlation, expected loss or insurance availability.

**Evidence label:** ILLUSTRATIVE JOINT STRESS STATES • NO PROBABILITIES OR EXPECTED-LOSS ESTIMATE

**Layout:** Two small multiples with identical zero-based axes, two states each. Show equal pooled inputs above; put the difference in peak dealer residual below.

**Visual:** {"type": "four_stacked_columns_in_two_panels", "panels": ["Dispersed", "Synchronized"], "category": "stress_state", "series": ["effective_conditional_recovery_idr", "dealer_residual_idr"], "unit": "IDR; display Rp million", "axis_min": 0, "axis_max_idr": 900000000, "direct_labels": "Label recovery and dealer amounts; retain the zero column explicitly.", "common_y_axis": true}

**Exact plot data:**

```json
[
  {
    "world": "Dispersed",
    "stress_state": "A",
    "eligible_units": 20,
    "units_with_low_offer": 10,
    "full_floor_shortfall_idr": 400000000,
    "conditional_recovery_before_aggregate_idr": 150000000,
    "effective_conditional_recovery_idr": 100000000,
    "dealer_residual_idr": 300000000,
    "capped_topup_total_idr": 100000000
  },
  {
    "world": "Dispersed",
    "stress_state": "B",
    "eligible_units": 20,
    "units_with_low_offer": 10,
    "full_floor_shortfall_idr": 400000000,
    "conditional_recovery_before_aggregate_idr": 150000000,
    "effective_conditional_recovery_idr": 100000000,
    "dealer_residual_idr": 300000000,
    "capped_topup_total_idr": 100000000
  },
  {
    "world": "Synchronized",
    "stress_state": "A",
    "eligible_units": 20,
    "units_with_low_offer": 20,
    "full_floor_shortfall_idr": 800000000,
    "conditional_recovery_before_aggregate_idr": 300000000,
    "effective_conditional_recovery_idr": 100000000,
    "dealer_residual_idr": 700000000,
    "capped_topup_total_idr": 200000000
  },
  {
    "world": "Synchronized",
    "stress_state": "B",
    "eligible_units": 20,
    "units_with_low_offer": 0,
    "full_floor_shortfall_idr": 0,
    "conditional_recovery_before_aggregate_idr": 0,
    "effective_conditional_recovery_idr": 0,
    "dealer_residual_idr": 0,
    "capped_topup_total_idr": 0
  }
]
```

**Highlight:** Peak dealer residual: Rp300m versus Rp700m

**Source note:** Constructed stress arrangement; same pooled unit-state offers,20units/state. Recovery is conditional and capped at assumed Rp100m/state. No probabilities, quote, actual customers or expected-loss estimate.

**Source paths:**
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/constructed_aggregate_risk.json`. All four aggregate rows. Constructed states, not observed outcomes.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/constructed_joint_stress_states.csv`. 80constructed unit-state rows. Each of20units has one low/one high offer in either world.
- `/workspace/scratch/70444ed5f561/auto2000_run/workstreams/extension_economics/checks.json`. EE-C04–EE-C08. Pooled-value equality and aggregate identities checked.

**Limits:**
- Four states are not four observed markets or four probabilities.
- Eighty constructed rows do not describe eighty customers.
- The aggregate limit is an added illustrative assumption, not a policy term verified in the market.
- A limit on insurer payment does not cap a separate full-floor promise.

**Bridge:** Return to the option menu with contract scope, retained risk and missing evidence visible. No solution is selected.

## Verification

22arithmetic/content checks passed; zero failures. Full values and the input SHA256manifest are in `economic_story.json`. Full methods and excluded detail remain in the research package.
