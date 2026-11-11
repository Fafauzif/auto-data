"""Six concise economics page briefs, derived only from frozen project evidence."""
from pathlib import Path
from datetime import datetime, timezone
import csv, json, hashlib, re

B=Path(__file__).resolve().parent;R=B.parent;W=R.parent
def readcsv(rel):
 with (R/rel).open() as f:return list(csv.DictReader(f))
def readjson(rel):return json.loads((R/rel).read_text())
def src(rel,locator,scope):return dict(path=str((R/rel).resolve()),package_relative_path=rel,locator=locator,scope=scope)
portfolio=readjson('workstreams/extension_economics/portfolio_inputs_and_method.json')
cost=[r for r in readcsv('workstreams/extension_economics/dated_service_estimates.csv') if 'BZ4X' in r['model'] and 8<=int(r['service_event'])<=11]
cost=sorted(cost,key=lambda r:int(r['service_event']))
risk=readjson('workstreams/extension_economics/constructed_aggregate_risk.json')
program=readjson('workstreams/extension_economics/program_distinctions.json')
total=6750
gp=[dict(business_line=name,gross_profit_idr_billion=g,revenue_idr_billion=rev,share_of_case_gp_pct=g/total*100,display_share_pct=round(g/total*100,1)) for name,g,rev in [('Vehicle sales',3600,60000),('Services',1320,2400),('Spare parts',1200,4800),('Body and paint',630,1800)]]
pages=[]
def page(id,headline,body,status,visual,data,highlight,note,sources,limits,bridge,layout='One dominant chart, concise body beside it, source and limit immediately below the chart.'):
 n=len(body.split());assert 60<=n<=90,(id,n)
 pages.append(dict(page_id=id,headline=headline,body=body,body_word_count=n,evidence_label=status,layout=layout,visual=visual,plot_data=data,highlight=highlight,source_note=note,source_paths=sources,limits=limits,bridge_to_next=bridge))

page('EC01',
 'After-sales provides 46.7% of case gross profit from 13.0% of revenue.',
 'The supplied case assigns Rp3,150 billion of gross profit to services, spare parts and body and paint, against Rp9,000 billion of revenue. Vehicle sales remain the largest individual profit pool. This makes the economics of completed ownership jobs material even when they generate fewer app sessions. The four lines belong to one case P&L, not four customer samples. A programme still needs incremental contribution after its own costs.',
 'SUPPLIED CASE ASSUMPTIONS • FY2025 • NOT AUDITED COMPANY ACCOUNTS',
 dict(type='horizontal_bar',category='business_line',value='gross_profit_idr_billion',unit='IDR billion',axis_min=0,axis_max=4000,order=['Vehicle sales','Services','Spare parts','Body and paint'],direct_labels='Gross profit plus share of total case GP; retain one color family for the three after-sales lines.'),
 gp,
 dict(annotation='After-sales: Rp3,150bn, 46.7% of GP',after_sales_gp_idr_billion=3150,total_gp_idr_billion=6750,after_sales_revenue_idr_billion=9000,total_revenue_idr_billion=69000,after_sales_gp_share_pct=3150/6750*100,after_sales_revenue_share_pct=9000/69000*100),
 'Source: supplied IBSC casebook, Exhibit 3, printed/PDF p10. Business-line case assumptions, not audited Auto2000 results.',
 [dict(path=str((W/'upload/Semifinal Casebook IBSC 2026.pdf').resolve()),package_relative_path='../upload/Semifinal Casebook IBSC 2026.pdf',locator='Exhibit3, printed/PDF p10',scope='Supplied FY2025 case P&L'),src('reports/NUMERICAL_QA.md','NQ04–NQ12','Independent arithmetic audit of supplied case values')],
 ['GP differs from operating profit and programme cash flow.','Line-average margins do not identify EV-specific or per-job contribution.','Labor and attached parts can belong to the same work order; do not count them as two customer visits.'],
 'Separate the case profit perimeter from the next page\'s external brand-portfolio sales data.')

scale=portfolio['shapley_scale'];mix=portfolio['shapley_mix'];x0=portfolio['xev_2024'];x1=portfolio['xev_2025']
waterfall=[dict(label='2024 xEV sales',bar_type='total',start_vehicles=0,end_vehicles=x0,value_vehicles=x0),dict(label='Portfolio scale term',bar_type='accounting_change',start_vehicles=x0,end_vehicles=x0+scale,value_vehicles=scale),dict(label='xEV mix term',bar_type='accounting_change',start_vehicles=x0+scale,end_vehicles=x1,value_vehicles=mix),dict(label='2025 xEV sales',bar_type='total',start_vehicles=0,end_vehicles=x1,value_vehicles=x1)]
page('EC02',
 'Toyota and Lexus xEV sales fell 6,025 units as portfolio scale and mix both decreased.',
 'Astra reports 37,693 Toyota and Lexus xEV sales in 2024 and 31,668 in 2025. The symmetric accounting bridge assigns about 5,050 fewer units to the total-portfolio scale term and 975 to its xEV mix term. Averaging both calculation orders removes an arbitrary ordering choice. These terms reconcile the observed change; they do not measure the effects of national demand, Digiroom or any proposed solution.',
 'OBSERVED BRAND-PORTFOLIO COUNTS + DERIVED ACCOUNTING • NOT CAUSAL ATTRIBUTION',
 dict(type='waterfall',category='label',value='value_vehicles',unit='Toyota and Lexus vehicles',axis_min=0,axis_max=42000,labels_decimals=0,change_colors='One restrained change color; totals share a dark neutral.',connector_lines=True),
 waterfall,
 dict(annotation='−5,049.884 scale + −975.116 mix = −6,025 vehicles',scale_term_vehicles=scale,mix_term_vehicles=mix,total_change_vehicles=-6025,interaction_vehicles=portfolio['interaction_units'],method='Two-factor Shapley average: scale=deltaTotal×meanMix; mix=deltaMix×meanTotal.'),
 'Source: Astra AR2025, printed p140/PDF p142. Toyota AND Lexus domestic new sales. Shapley terms are accounting allocations, not causes or Auto2000 volume.',
 [src('workstreams/friend_capabilities/numeric_observations.csv','FC-N12–FC-N15; AR2025p140/PDF142','Original chart transcription'),src('workstreams/extension_economics/portfolio_inputs_and_method.json','All four counts and exact symmetric formula','Derived arithmetic'),src('workstreams/extension_economics/portfolio_decompositions.csv','Both orderings and symmetric average','Ordering sensitivity retained')],
 ['Do not label the scale term a national-market effect.','Do not label the mix term a Digiroom effect.','These are Toyota and Lexus sales flows, not Auto2000 sales or the installed service base.'],
 'Move from new-sales flows to the entitlement rules that govern ownership jobs.')

program_data=[dict(program='T-CARE',covered_scheduled_event_count=7,covered_labor=True,covered_specified_parts=True,first_event=1,last_event=7,maximum_years=3,maximum_km=60000,scope='Eligible purchases from July2022; exclusions and terms apply.'),dict(program='T-CARE Lite',covered_scheduled_event_count=7,covered_labor=True,covered_specified_parts=False,first_event=1,last_event=7,maximum_years=3,maximum_km=60000,scope='Eligible LCGC purchases from January2023. Optional Lite+ parts package is separate.'),dict(program='Legacy GBSB',covered_scheduled_event_count=6,covered_labor=True,covered_specified_parts=True,first_event=1,last_event=6,maximum_years=4,maximum_km=50000,scope='Eligible legacy cohorts; current page identifies January2020–June2022. Model service-book terms apply.')]
page('EC03',
 'A longer programme maximum can cover fewer service events and different parts benefits.',
 'Current Toyota material gives T-CARE seven scheduled labor-and-parts events within three years or 60,000 km. T-CARE Lite covers labor for seven events; its parts package is separate. Legacy GBSB allows six events within four years or 50,000 km. Its published calendar lists events through month 30. Headline years therefore do not identify covered visit count, the customer’s actual payment date or dealer gross profit. Eligibility and specified work still govern.',
 'PUBLISHED PROGRAMME TERMS • ORDINAL EVENTS • NOT PERSONALISED ENTITLEMENT',
 dict(type='ordinal_coverage_matrix',rows='program',columns='Service event1through8',event_axis=[1,2,3,4,5,6,7,8],encode_labor='Upper half of event cell',encode_parts='Lower half; empty means not included in this base programme, not no parts work.',right_labels='Maximum years/km and eligible cohort, separate from the ordinal axis.',do_not_use='Do not draw a continuous four-year free-service bar.'),
 program_data,
 dict(annotation='Seven events / three-year maximum versus six events / four-year maximum',legacy_recommended_months=[1,6,12,18,24,30],legacy_recommended_km=[1000,10000,20000,30000,40000,50000],xtra_note='Eligible events8–11 are customer-paid under the2026XTRAannouncement; warranty increments are a separate benefit.'),
 'Source: Toyota T-CARE programme page;2026XTRAannouncement; legacy GBSB PDF p1. Time/km means whichever first; eligibility, specified work and model terms apply.',
 [src('workstreams/extension_economics/program_distinctions.csv','T-CARE, Lite and GBSB rows; EE-S01/EE-S03/EE-S04','Published programme distinctions'),src('workstreams/extension_economics/legacy_scheduled_calendar.csv','Six recommendations; EE-S11PDF p1','Legacy model/programme table'),src('workstreams/extension_economics/source_checks.csv','EE-S01,EE-S03,EE-S04,EE-S11','Original public URLs and retrieval limits')],
 ['Labour coverage is not universal parts coverage.','Maximum duration is not an observed return date.','A zero customer bill does not reveal OEM reimbursement, dealer direct cost or GP.','Do not transfer legacy terms to a current model without eligibility evidence.'],
 'Show one model\'s dated post-coverage estimates without converting retail fees into dealer margin.',
 layout='One large three-row coverage matrix. Keep event ordinals on the main axis and maximum years/km as a separate right-hand note.')

cost_data=[dict(service_event=int(r['service_event']),labor_estimate_idr=int(r['labor_estimate_idr']),parts_estimate_idr=int(r['parts_estimate_idr']),total_estimate_idr=int(r['total_estimate_idr'])) for r in cost]
page('EC04',
 'The bZ4X tool’s four later-service estimates total Rp9.101 million on a March 2024 basis.',
 'The public Toyota tool lists bZ4X Panoramic View estimates from Rp847,000 at visits 8 and 10 to Rp3,713,000 at visit 11. Labor and parts sum to Rp9,101,000 across the four events. The opened note dates these estimates to March 2024 and allows dealer and additional-work differences. These are useful illustrations of uneven bills, not current invoices, total ownership cost, dealer margin or a forecast of customer spending.',
 'DATED RETAIL ESTIMATES • MARCH2024 BASIS • OBSERVED11NOV2026',
 dict(type='stacked_columns',category='service_event',series=['labor_estimate_idr','parts_estimate_idr'],unit='IDR; display axis as Rp million',axis_min=0,axis_max_idr=4200000,order=[8,9,10,11],direct_labels='Total above each column; legend has labor and parts only.',model='All New BZ4X Battery EV; Panoramic View variant'),
 cost_data,
 dict(annotation='Four-event estimate: Rp9,101,000',labor_sum_idr=sum(r['labor_estimate_idr'] for r in cost_data),parts_sum_idr=sum(r['parts_estimate_idr'] for r in cost_data),total_sum_idr=sum(r['total_estimate_idr'] for r in cost_data),date_badge='MARCH2024 ESTIMATES'),
 'Source: Toyota model/variant cost tool, XT04, observed11Nov2026. Estimates explicitly based on March2024; tax included; dealer/extra-work caveats. Not a current quote or GP.',
 [src('workstreams/extension_journeys/service_estimates_extension.csv','XT04; bZ4X Panoramic View, visits8–11','Observed displayed amounts and date note'),src('workstreams/extension_journeys/observations.json','XT04','Researcher walkthrough; no VIN or submitted request'),src('workstreams/extension_economics/dated_service_estimate_sums.csv','All New BZ4X Battery EV','Recomputed labor/parts totals')],
 ['Do not display these as2026prices.','Do not multiply by case line margins to create EV-specific GP.','No matched BEV-versus-HEV comparison or causal powertrain effect is shown.','FREE/zero parts entries do not establish zero work or zero dealer cost.'],
 'Separate ordinary retail-payment information from a proposed promise about a future resale value.')

offer,floor,cap,retention,limit=160000000,200000000,10000000,10000000,15000000
shortfall=max(0,floor-offer);topup=min(cap,shortfall);recovery=min(limit,max(0,shortfall-retention));residual=shortfall-recovery
contract_data=[dict(design='Capped top-up',valid_offer_idr=offer,topup_idr=topup,customer_credit_idr=offer+topup,minimum_floor_promised=False,full_floor_shortfall_idr=None,conditional_insurer_payment_idr=None,dealer_full_floor_residual_idr=None),dict(design='Full floor with assumed insurer layer',valid_offer_idr=offer,topup_idr=None,customer_credit_idr=floor,minimum_floor_promised=True,full_floor_shortfall_idr=shortfall,conditional_insurer_payment_idr=recovery,dealer_full_floor_residual_idr=residual)]
page('EC05',
 'A Rp10 million top-up leaves a Rp160 million offer below a Rp200 million floor.',
 'In this constructed example, the capped top-up adds Rp10 million to a Rp160 million offer, producing Rp170 million of customer credit. A separate full-floor promise requires Rp200 million. Its Rp40 million shortfall leaves Rp25 million with the dealer after the assumed Rp15 million insurer layer, using a Rp10 million retention. That arithmetic excludes contribution and running costs. No actual policy, underwriting appetite or approved Auto2000 offer is established.',
 'ILLUSTRATIVE CONTRACT ARITHMETIC • NOT AN OFFER, POLICY OR FORECAST',
 dict(type='two_panel_contract_comparison',left='Zero-based customer-credit columns: offer160m, capped credit170m, full-floor credit200m.',right='Full-floor shortfall40m stacked as assumed insurer15m and dealer residual25m.',unit='IDR; display Rp million',axis_min=0,customer_credit_axis_max_idr=220000000,shortfall_axis_max_idr=45000000),
 contract_data,
 dict(annotation='Capped credit Rp170m; full floor leaves Rp25m dealer exposure',floor_idr=floor,valid_offer_idr=offer,topup_cap_idr=cap,assumed_retention_idr=retention,assumed_insurer_per_unit_limit_idr=limit,full_floor_shortfall_idr=shortfall,conditional_recovery_idr=recovery,dealer_residual_idr=residual,assumed_aggregate_limit_exhausted=False),
 'Constructed illustration using declared floor/cap/retention/layer assumptions. All losses assumed eligible and aggregate cover available; premium, expenses and timing excluded. No available policy verified.',
 [src('workstreams/extension_economics/constructed_contract_tail.csv','valid_offer160000000 row','Constructed per-unit arithmetic'),src('workstreams/friend_insurance/analysis.md','Capped top-up and full-floor distinction','Source/contract availability remains unresolved')],
 ['Do not call the capped top-up a guaranteed Rp200m floor.','The insurer layer is assumed, conditional and not a quote.','Dealer residual includes retention and loss beyond the assumed layer.','Contribution is not dealer GP; actual fees and margins remain unknown.'],
 'Test the same promise at portfolio level, where timing and an aggregate limit change the retained obligation.',
 layout='Two panels: customer credit on the left, funding of full-floor shortfall on the right. Print ILLUSTRATIVE beside both panels.')

risk_data=[dict(world='Dispersed' if r['world'].startswith('Losses dispersed') else 'Synchronized',stress_state=r['stress_state'],eligible_units=r['eligible_units'],units_with_low_offer=r['units_with_shortfall'],full_floor_shortfall_idr=r['full_floor_gross_shortfall'],conditional_recovery_before_aggregate_idr=r['conditional_recovery_before_aggregate'],effective_conditional_recovery_idr=r['effective_conditional_recovery'],dealer_residual_idr=r['dealer_residual_after_aggregate'],capped_topup_total_idr=r['capped_topup_total']) for r in risk]
page('EC06',
 'The same pooled offers create higher peak retained losses when low valuations arrive together.',
 'These constructed worlds use the same twenty units and the same pooled low and high offers across two stress states. Dispersion puts ten low offers in each state; synchronization puts all twenty in one. Under the assumed Rp100 million aggregate recovery limit, the highest dealer residual rises from Rp300 million to Rp700 million. No probability is assigned. This exposes a limit of per-unit reasoning without estimating actual correlation, expected loss or insurance availability.',
 'ILLUSTRATIVE JOINT STRESS STATES • NO PROBABILITIES OR EXPECTED-LOSS ESTIMATE',
 dict(type='four_stacked_columns_in_two_panels',panels=['Dispersed','Synchronized'],category='stress_state',series=['effective_conditional_recovery_idr','dealer_residual_idr'],unit='IDR; display Rp million',axis_min=0,axis_max_idr=900000000,direct_labels='Label recovery and dealer amounts; retain the zero column explicitly.',common_y_axis=True),
 risk_data,
 dict(annotation='Peak dealer residual: Rp300m versus Rp700m',per_unit_floor_idr=200000000,low_offer_idr=160000000,high_offer_idr=260000000,units_per_state=20,assumed_retention_idr=10000000,assumed_per_unit_insurer_limit_idr=15000000,assumed_aggregate_insurer_limit_idr=100000000,pooled_low_unit_state_count_per_world=20,pooled_high_unit_state_count_per_world=20,constructed_world_count=2,stress_states_per_world=2,dispersed_peak_dealer_residual_idr=300000000,synchronized_peak_dealer_residual_idr=700000000),
 'Constructed stress arrangement; same pooled unit-state offers,20units/state. Recovery is conditional and capped at assumed Rp100m/state. No probabilities, quote, actual customers or expected-loss estimate.',
 [src('workstreams/extension_economics/constructed_aggregate_risk.json','All four aggregate rows','Constructed states, not observed outcomes'),src('workstreams/extension_economics/constructed_joint_stress_states.csv','80constructed unit-state rows','Each of20units has one low/one high offer in either world'),src('workstreams/extension_economics/checks.json','EE-C04–EE-C08','Pooled-value equality and aggregate identities checked')],
 ['Four states are not four observed markets or four probabilities.','Eighty constructed rows do not describe eighty customers.','The aggregate limit is an added illustrative assumption, not a policy term verified in the market.','A limit on insurer payment does not cap a separate full-floor promise.'],
 'Return to the option menu with contract scope, retained risk and missing evidence visible. No solution is selected.',
 layout='Two small multiples with identical zero-based axes, two states each. Show equal pooled inputs above; put the difference in peak dealer residual below.')

checks=[]
def ck(id,description,actual,expected,tol=1e-8):
 ok=abs(actual-expected)<=tol if isinstance(expected,(int,float)) else actual==expected
 checks.append(dict(check_id=id,description=description,actual=actual,expected=expected,passed=ok))
ck('ES01','CaseGPsum',sum(r['gross_profit_idr_billion'] for r in gp),6750)
ck('ES02','Caseafter-salesGP',sum(r['gross_profit_idr_billion'] for r in gp[1:]),3150)
ck('ES03','DisplayedcaseGPsharesreconcile',sum(r['display_share_pct'] for r in gp),100.)
ck('ES04','Roundedafter-salesGPshare',round(3150/6750*100,1),46.7)
ck('ES05','Roundedafter-salesrevenueshare',round(9000/69000*100,1),13.)
ck('ES06','Symmetricbridge',scale+mix,-6025.)
ck('ES07','Roundedscale−5049.884',round(scale,3),-5049.884)
ck('ES08','Roundedmix−975.116',round(mix,3),-975.116)
ck('ES09','TCAREsevenevents',next(r['covered_scheduled_events'] for r in program if r['program']=='T-CARE'),7)
ck('ES10','GBSBsixevents',next(r['covered_scheduled_events'] for r in program if r['program']=='GBSB'),6)
ck('ES11','bZ4Xfourlaterestimates',len(cost),4)
ck('ES12','bZ4Xsum9101000',sum(r['total_estimate_idr'] for r in cost_data),9101000)
ck('ES13','bZ4Xlabor4349000',sum(r['labor_estimate_idr'] for r in cost_data),4349000)
ck('ES14','bZ4Xparts4752000',sum(r['parts_estimate_idr'] for r in cost_data),4752000)
ck('ES15','Cappedcredit170m',offer+topup,170000000)
ck('ES16','Fullfloorshortfall40m',shortfall,40000000)
ck('ES17','Conditionalrecovery15m',recovery,15000000)
ck('ES18','Dealerresidual25m',residual,25000000)
ck('ES19','Fourconstructedstates',len(risk_data),4)
ck('ES20','Dispersedpeak300m',max(r['dealer_residual_idr'] for r in risk_data if r['world']=='Dispersed'),300000000)
ck('ES21','Synchronizedpeak700m',max(r['dealer_residual_idr'] for r in risk_data if r['world']=='Synchronized'),700000000)
ck('ES22','Sixpageswith60–90wordbodies',len(pages)==6 and all(60<=r['body_word_count']<=90 for r in pages),True)
assert all(r['passed'] for r in checks)
inputs=[W/'upload/Semifinal Casebook IBSC 2026.pdf',R/'workstreams/extension_economics/portfolio_inputs_and_method.json',R/'workstreams/extension_economics/dated_service_estimates.csv',R/'workstreams/extension_economics/program_distinctions.json',R/'workstreams/extension_economics/constructed_aggregate_risk.json']
result=dict(title='Economics story assets for the concise research memo',generated_utc=datetime.now(timezone.utc).isoformat(),page_count=6,central_argument='Profit depends on the completed job, its programme and payer, and retained obligation. App activity and large datasets do not identify those economics.',scope='Six concise visual-page briefs only. No strategy selection, budget, ROI forecast or implementation. The user-provided visual reference contributes design hierarchy only, never case facts.',evidence_audit='Supplied caseP&L, observed external portfolio counts, published programme terms, dated retail estimates and constructed risk states remain explicitly distinct.',pages=pages,checks=checks,input_manifest=[dict(path=str(p),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs])
(B/'economic_story.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
md=['# Six economics pages for the concise research memo','',result['central_argument'],'','| Page | Exact finding headline | Evidence |','|---|---|---|']
for p in pages:md.append(f"| {p['page_id']} | {p['headline']} | {p['evidence_label']} |")
md+=['','The plotting data below come only from frozen research artifacts. Case assumptions, actual source counts, dated estimates and illustrations are not pooled. Every body is60–90words. User reference material supplies visual style only.','']
for p in pages:
 md += [f"## {p['page_id']}: {p['headline']}",'',p['body'],'',f"**Evidence label:** {p['evidence_label']}",'',f"**Layout:** {p['layout']}",'',f"**Visual:** {json.dumps(p['visual'],ensure_ascii=False)}",'', '**Exact plot data:**','', '```json',json.dumps(p['plot_data'],indent=2,ensure_ascii=False),'```','',f"**Highlight:** {p['highlight']['annotation']}",'',f"**Source note:** {p['source_note']}",'', '**Source paths:**']
 for s in p['source_paths']:md.append(f"- `{s['path']}`. {s['locator']}. {s['scope']}.")
 md+=['','**Limits:**']
 for lim in p['limits']:md.append('- '+lim)
 md+=['',f"**Bridge:** {p['bridge_to_next']}",'']
md+=['## Verification','',f"{len(checks)}arithmetic/content checks passed; zero failures. Full values and the input SHA256manifest are in `economic_story.json`. Full methods and excluded detail remain in the research package."]
(B/'economic_story.md').write_text('\n'.join(md)+'\n')
print(json.dumps(dict(pages=6,body_word_counts={p['page_id']:p['body_word_count'] for p in pages},checks=len(checks),failed=sum(not r['passed'] for r in checks)),indent=2))
