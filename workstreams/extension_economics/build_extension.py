"""Reproduce extension mechanics. Source inputs, constructed cases and symbols stay separate."""
from pathlib import Path
from datetime import datetime, timezone
import csv, json, hashlib, math, collections
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

B=Path(__file__).resolve().parent; R=B.parents[1]; F=B/'figures'; F.mkdir(exist_ok=True)
input_paths=[B/'PRE_SPEC.md',B/'source_checks.json',R/'workstreams/friend_capabilities/numeric_observations.json',R/'workstreams/journeys/tcare_observed_costs.csv']
def save(name,rows):
 (B/f'{name}.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 with (B/f'{name}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# 1. Observed Toyota AND Lexus counts. Symmetric average of the two exact orderings.
ar=json.loads((R/'workstreams/friend_capabilities/numeric_observations.json').read_text())
av={r['observation_id']:r['value'] for r in ar};T0,T1,X0,X1=[av[x] for x in ['FC-N12','FC-N13','FC-N14','FC-N15']]
m0,m1=X0/T0,X1/T1;dt=T1-T0;dm=m1-m0
orders=[dict(order='Scale first, then mix',scale_units=dt*m0,mix_units=T1*dm),dict(order='Mix first, then scale',scale_units=dt*m1,mix_units=T0*dm)]
shscale=dt*(m0+m1)/2;shmix=dm*(T0+T1)/2
orders.append(dict(order='Symmetric Shapley average',scale_units=shscale,mix_units=shmix))
for row in orders:
 row.update(change_units=X1-X0,sum_units=row['scale_units']+row['mix_units'],data_status='Derived accounting from observed portfolio counts; not causal attribution',source_refs='AR2025 printed140/PDF142;FC-N12–FC-N15')
save('portfolio_decompositions',orders)
decomp=dict(total_2024=T0,total_2025=T1,xev_2024=X0,xev_2025=X1,mix_2024=m0,mix_2025=m1,xev_change=X1-X0,interaction_units=dt*dm,shapley_scale=shscale,shapley_mix=shmix,interpretation='Symmetrically splits the interaction between both factors; exact arithmetic, not causes or Auto2000 attribution.')
(B/'portfolio_inputs_and_method.json').write_text(json.dumps(decomp,indent=2)+'\n')

# 2. Current program distinctions and legacy published event calendar.
programs=[
 dict(program='T-CARE',cohort='Eligible purchases from July2022; model exclusions apply',covered_scheduled_events=7,max_years=3,max_km=60000,scheduled_labor='Included subject terms',scheduled_parts='Specified items included subject terms',next_period='XTRA states customer-paid events8–11 when eligible',source='EE-S01;EE-S04',status='Operator published program'),
 dict(program='T-CARE Lite',cohort='Eligible LCGC purchases from January2023',covered_scheduled_events=7,max_years=3,max_km=60000,scheduled_labor='Included subject terms',scheduled_parts='Not the same automatic parts benefit as full T-CARE',next_period='Parts can be customer-paid inside labor-covered window',source='EE-S01;EE-S03',status='Operator published program'),
 dict(program='T-CARE Lite+',cohort='Optional additional package for eligible LCGC; available from April2023',covered_scheduled_events=6,max_years=3,max_km=60000,scheduled_labor='Separate Lite labor program',scheduled_parts='Purchased package for scheduled events2–7',next_period='Prepayment changes customer cash timing, not proof of dealer GP',source='EE-S01;EE-S03',status='Operator published program'),
 dict(program='GBSB',cohort='Current page identifies eligible January2020–June2022 purchases; legacy PDF has model rollout dates',covered_scheduled_events=6,max_years=4,max_km=50000,scheduled_labor='Included subject terms',scheduled_parts='Listed items only; service book governs',next_period='Outside-program event count is not observed paid demand',source='EE-S01;EE-S11 PDF1',status='Current page plus historical primary program PDF'),
 dict(program='T-CARE XTRA',cohort='Eligible post-T-CARE service; current page excludes GBSB',covered_scheduled_events=0,max_years=2,max_km=40000,scheduled_labor='Events8–11 customer-paid in announcement',scheduled_parts='Events8–11 customer-paid in announcement',next_period='Conditional six-month/10,000km warranty increments; not free scheduled-service extension',source='EE-S01;EE-S04',status='Operator published program; eligibility required'),
]
save('program_distinctions',programs)
calendar=[]
for event,month,km in zip(range(1,7),[1,6,12,18,24,30],[1000,10000,20000,30000,40000,50000]):
 calendar.append(dict(service_event=event,recommended_month=month,recommended_km=km,source='EE-S11 PDF1 table',vehicle_scope='Legacy GBSB petrol/diesel tables, not a current BEV manual',time_or_distance='whichever first; model/terms apply',first_event_parts_note='No replacement parts at first event; does not mean no inspection or labor'))
save('legacy_scheduled_calendar',calendar)
windows=[]
for program,n in [('GBSB',6),('T-CARE',7)]:
 for event in range(1,12):
  windows.append(dict(program=program,service_event=event,in_this_base_program_covered_event_window=event<=n,program_event_boundary=n,data_status='Structural ordinal comparison, not customer panel or paid-demand forecast',limitation='Eligibility, specified work, earlier km/time limits and other cover still apply. Outside this program does not identify payer, invoice or GP.'))
save('ordinal_entitlement_windows',windows)

# 3. Previously observed public, dated service-fee estimates; preserve source rows.
with (R/'workstreams/journeys/tcare_observed_costs.csv').open() as f:costs=list(csv.DictReader(f))
extras=list((R/'workstreams/journeys').glob('*extension*cost*.csv'))
newcost=R/'workstreams/extension_journeys/service_estimates_extension.csv'
if newcost.exists():extras.append(newcost)
for extra in sorted(extras):
 input_paths.append(extra)
 with extra.open() as f:costs.extend(csv.DictReader(f))
# Normalize accepted extension column labels without altering raw files.
normal=[]
for r in costs:
 event=r.get('service_number') or r.get('service_no') or r.get('service_visit')
 labor=r.get('labor_estimate_idr') or r.get('labor_idr')
 parts=r.get('parts_estimate_idr') or r.get('parts_idr')
 if event is None or labor is None or parts is None:continue
 normal.append(dict(observation_id=r['observation_id'],source_url=r.get('source_url','https://aftersales.toyota.astra.co.id/t-care'),model=r['model'],variant=r['variant'],service_event=int(event),labor_estimate_idr=int(labor),parts_estimate_idr=int(parts),total_estimate_idr=int(labor)+int(parts),estimate_date_basis=r.get('estimate_date_basis',r.get('estimate_basis','March2024')),data_status='Observed public estimate, dated March2024; not actual invoice/cost/GP',limits='Tax included in inspected note; dealer and extra-work differences. Not personalized entitlement. Zero displayed parts fee is not a count of zero work.'))
# Retain one version of each exact observed model/variant/event row.
normal=list({(r['model'],r['variant'],r['service_event']):r for r in normal}.values())
save('dated_service_estimates',normal)
costtotals=[]
for key,group in __import__('itertools').groupby(sorted(normal,key=lambda r:(r['model'],r['variant'],r['service_event'])),key=lambda r:(r['model'],r['variant'])):
 rows=list(group);paid=[r for r in rows if 8<=r['service_event']<=11]
 if {r['service_event'] for r in paid}!={8,9,10,11}:continue
 costtotals.append(dict(model=key[0],variant=key[1],events='8,9,10,11',labor_estimate_total_idr=sum(r['labor_estimate_idr'] for r in paid),parts_estimate_total_idr=sum(r['parts_estimate_idr'] for r in paid),combined_estimate_total_idr=sum(r['total_estimate_idr'] for r in paid),highest_event_estimate_idr=max(r['total_estimate_idr'] for r in paid),lowest_event_estimate_idr=min(r['total_estimate_idr'] for r in paid),data_status='Derived sum of dated retail estimates; unmatched models, not a powertrain effect',source_refs=';'.join(sorted({r['observation_id'] for r in paid}))))
save('dated_service_estimate_sums',costtotals)

# 4. Contract illustrations reuse the supplied friend's floor/layer amounts.
# Aggregate limit100m and20-unit joint arrangements are added stress assumptions,
# not observed offers, probabilities, policy availability or a proposal to adopt.
FLOOR,CAP,RET,LIM,AGG,N=200_000_000,10_000_000,10_000_000,15_000_000,100_000_000,20
joint=[]
for world in ['Losses dispersed across two stress states','Losses synchronized in one stress state']:
 for state in ['A','B']:
  for unit in range(N):
   low=(unit<10 if state=='A' else unit>=10) if world.startswith('Losses dispersed') else state=='A'
   offer=160_000_000 if low else 260_000_000;s=max(0,FLOOR-offer);rec=min(LIM,max(0,s-RET))
   joint.append(dict(world=world,stress_state=state,constructed_unit=unit+1,valid_offer=offer,floor=FLOOR,shortfall=s,topup=min(CAP,s),conditional_recovery_before_aggregate=rec,data_status='CONSTRUCTED deterministic stress arrangement; no probabilities or observed customers'))
save('constructed_joint_stress_states',joint)
agg=[]
for world in sorted({r['world'] for r in joint}):
 for state in ['A','B']:
  z=[r for r in joint if r['world']==world and r['stress_state']==state];s=sum(r['shortfall'] for r in z);rec=sum(r['conditional_recovery_before_aggregate'] for r in z);effective=min(AGG,rec)
  agg.append(dict(world=world,stress_state=state,eligible_units=N,units_with_shortfall=sum(r['shortfall']>0 for r in z),full_floor_gross_shortfall=s,conditional_recovery_before_aggregate=rec,assumed_aggregate_limit=AGG,effective_conditional_recovery=effective,dealer_residual_after_aggregate=s-effective,dealer_residual_without_binding_aggregate=s-rec,capped_topup_total=sum(r['topup'] for r in z),data_status='CONSTRUCTED stress outcome; not an expected loss or quote'))
save('constructed_aggregate_risk',agg)
tails=[]
for offer in [0,80_000_000,160_000_000,175_000_000,180_000_000,190_000_000,200_000_000,205_000_000]:
 s=max(0,FLOOR-offer);rec=min(LIM,max(0,s-RET));top=min(CAP,s)
 tails.append(dict(valid_offer=offer,full_floor=FLOOR,shortfall=s,topup_cap=CAP,topup=top,capped_customer_credit=offer+top,conditional_insurer_recovery=rec,dealer_residual_full_floor=s-rec,data_status='CONSTRUCTED per-unit contract arithmetic; no quoted cover',aggregate_limit_applied=False))
save('constructed_contract_tail',tails)

# 5. A mutually distinguished economic mechanism registry, deliberately symbolic.
mechanisms=[
 ('EE-M01','Sales','Delivered vehicle flow','Additional deliveries × realized vehicle contribution','Price/model availability/credit approval rather than digital engagement changes deliveries','Completed deliveries, net revenue, direct vehicle cost, discounts','New sales are not installed service base'),
 ('EE-M02','Services','Jobs due × dealer capture','Eligible vehicles × work due × dealer capture × net contribution per work unit','Less work due can mimic defection','Model/age/km/program, due jobs, completed jobs, labor costs','Same visits can contain different work'),
 ('EE-M03','Spare Parts','Attached and standalone parts','Net parts revenue minus attributable direct parts cost','Parts in a service package may already be in another total','SKU/quantity/payer/discount/cost and linkage to work order','Do not count attached parts as another independent customer visit'),
 ('EE-M04','Body & Paint','Collision/repair incidence and claim routing','Repair demand × capture × realized repair contribution','Collision demand and insurer routing differ from scheduled service cadence','Repair scope, authorization, parts/labor, insurer terms, downtime','Lower engine-maintenance needs do not identify body-repair demand'),
 ('EE-M05','All4S','Booking-channel migration','Holding completed work, price and direct cost fixed: incremental transaction GP=0','A channel move is miscounted as new work','Same-customer/work-order linkage and actual outcomes','Cost saving or genuinely induced demand is a separate mechanism'),
 ('EE-M06','Services/Parts/B&P','Payer substitution','Same work with different payer can change realized price, denial risk or collection time','Changing payer alone is credited as an added job','Customer/OEM/insurer allocations and realized reimbursements','Zero customer cash does not imply zero dealer GP'),
 ('EE-M07','Services/Parts','Entitlement boundary','Covered program events versus later customer-paid work','Cohort aging or benefit expiry is mistaken for defection','VIN/model/cohort/eligible work/program status','Maximum years are not actual on-time event count'),
 ('EE-M08','All4S','Mix and realization','DeltaGP = deltaQ×unitGP0 + Q1×deltaUnitGP','Margin percentage or payer mix shifts while job count is unchanged','Matched scope and period, net receipts and direct cost','An exact bridge is not causal attribution'),
 ('EE-M09','All4S','Within-dealer cannibalization','Additional retained contribution less displaced existing contribution','A customer would have used another Auto2000 branch/offer anyway','Dealer-wide outcomes and feasible alternative path','Branch/app credit is not necessarily company incrementality'),
 ('EE-M10','Services/B&P','Binding specialist capacity','Acceptable incremental contribution > displaced alternative contribution + added capacity cost','Positive stand-alone job GP is assumed enough','Real duration, relevant bottleneck and next-best feasible work','No job-hour margins or capacity measured here'),
 ('EE-M11','All4S','Operating profit versus GP','Incremental operating profit = incremental GP − incremental operating expenses','Revenue or GP is presented as net business benefit','Real incremental staffing, partner, marketing and running costs','Classify depreciation consistently; do not subtract capex twice'),
 ('EE-M12','All4S','Timing and cash','Track receipts, costs, investment, guarantee settlement and recoveries by period','A future liability or delayed recovery disappears from a short horizon','Cohort timelines, receivable terms and actual obligations','The2026–2028investment cap is not a proof of later obligation limits'),
 ('EE-M13','Replacement sale/trade-in','Inspection evidence','Permitted condition evidence may change appraisal confidence or executable offer','Digital certificate already exists and adds no valuation information','Appraiser acceptance, matched offers, agreed data access','Certificate retrieval is not price protection or funded risk transfer'),
 ('EE-M14','Replacement sale/trade-in','Contracted downside obligation','Dealer residual = promised shortfall − eligible recoveries','Per-unit/aggregate insurer limits are called complete protection','Signed promise, actual coverage, valuation and aggregate rules','Limit on insurer payment does not cap a separate full-floor promise'),
]
save('commercial_mechanism_registry',[dict(mechanism_id=i,business_lines=l,mechanism=m,relationship=f,rival=r,missing_identifying_inputs=x,interpretive_boundary=b) for i,l,m,f,r,x,b in mechanisms])

# Original observed/derived charts, not publisher images.
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
fig,ax=plt.subplots(figsize=(10,5.7));positions=np.arange(4);heights=[X0,-shscale,-shmix,X1];bottoms=[0,X0+shscale,X1,0]
bars=ax.bar(positions,heights,bottom=bottoms,color=['#204d68','#bd713c','#d39c73','#204d68'],width=.60)
for j,(b,v) in enumerate(zip(bars,[X0,shscale,shmix,X1])):
 y=(b.get_y()+b.get_height()+700 if j in [0,3] else b.get_y()+b.get_height()/2)
 ax.text(b.get_x()+b.get_width()/2,y,f'{v:+,.0f}' if j in [1,2] else f'{v:,.0f}',ha='center',va='center',fontweight='bold',color='black')
ax.set_xticks(positions,['2024 xEV sales','Portfolio scale term','xEV mix term','2025 xEV sales']);ax.set_ylim(0,42500);ax.set_ylabel('Toyota and Lexus vehicles');ax.set_title('An exact accounting bridge for the 6,025-vehicle xEV decline',loc='left',pad=18,fontweight='bold')
fig.text(.02,.025,'Observed counts: Astra AR2025, printed140/PDF142. Derived terms average both factor orderings (Shapley).\nToyota AND Lexus domestic sales; arithmetic allocation, not market/Digiroom causal attribution or Auto2000 volume.',fontsize=8,color='#444')
fig.tight_layout(rect=[0,.11,1,1]);fig.savefig(F/'portfolio_shapley_bridge.png',dpi=220);plt.close(fig)

models=[r for r in costtotals if 'Yaris' in r['model'] or 'bz4x' in r['model'].lower()]
fig,ax=plt.subplots(figsize=(10.8,6.1));width=.34 if len(models)>1 else .6;xs=np.arange(4)
colors=[('#204d68','#9ab5c6'),('#a8582c','#d9ad8d'),('#4b6d56','#abc1b0')]
for idx,t in enumerate(models):
 rows=sorted([r for r in normal if r['model']==t['model'] and r['variant']==t['variant'] and 8<=r['service_event']<=11],key=lambda r:r['service_event'])
 pos=xs+(idx-(len(models)-1)/2)*width
 label='bZ4X' if 'bz4x' in t['model'].lower() else 'Yaris Cross HEV' if 'Yaris' in t['model'] else t['model']
 labor=np.array([r['labor_estimate_idr']/1e6 for r in rows]);parts=np.array([r['parts_estimate_idr']/1e6 for r in rows]);dark,light=colors[idx%len(colors)]
 ax.bar(pos,labor,width*.90,color=dark,label=label+' labor');ax.bar(pos,parts,width*.90,bottom=labor,color=light,label=label+' parts')
 for x,value in zip(pos,labor+parts):ax.text(x,value+.055,f'{value:.3f}',ha='center',fontsize=9)
ax.set_xticks(xs,['Service 8','Service 9','Service 10','Service 11']);ax.set_ylim(0,max(r['total_estimate_idr'] for r in normal if 8<=r['service_event']<=11)/1e6*1.28);ax.set_ylabel('Rp million, published retail estimate');ax.set_title('Post-coverage service estimates vary by model and event',loc='left',fontweight='bold',pad=17);ax.legend(frameon=False,loc='upper left',ncol=2,fontsize=9)
fig.text(.02,.025,'DATED ESTIMATES: March 2024 basis, public Toyota tool observed 11 Nov 2026 (JX03 and XT04).\nTax included; dealer/extra-work differences. Unmatched models/variants. Not current invoices, unit costs, GP or a powertrain effect.',fontsize=8,color='#444')
fig.tight_layout(rect=[0,.13,1,1]);fig.savefig(F/'dated_service_estimate_comparison.png',dpi=220);plt.close(fig)

# Exact identities, without claims about observed business effects.
checks=[]
def ck(id,claim,observed,expected,tol=1e-8):
 ok=(abs(observed-expected)<=tol) if isinstance(observed,(int,float)) else observed==expected
 checks.append(dict(check_id=id,claim=claim,observed=observed,expected=expected,passed=ok))
for row in orders:ck('EE-C01-'+row['order'],'Accounting terms exactly reconcile',row['sum_units'],X1-X0)
ck('EE-C02','Shapley term equals average of order-specific terms',shscale,sum(r['scale_units'] for r in orders[:2])/2)
ck('EE-C03','Shapley mix equals average of order-specific terms',shmix,sum(r['mix_units'] for r in orders[:2])/2)
for col in ['valid_offer','shortfall','conditional_recovery_before_aggregate']:
 pools=[sorted(r[col] for r in joint if r['world']==world) for world in sorted({r['world'] for r in joint})]
 ck('EE-C04-'+col,'Same pooled unit-state values under both joint arrangements',pools[0],pools[1])
for world in sorted({r['world'] for r in joint}):
 ck('EE-C05-'+world,'Each constructed unit has one low and one high offer across stress states',all(sorted(r['valid_offer'] for r in joint if r['world']==world and r['constructed_unit']==u)==[160000000,260000000] for u in range(1,N+1)),True)
for r in agg:
 ck('EE-C06-'+r['world']+r['stress_state'],'Gross shortfall equals recovery plus dealer residual',r['effective_conditional_recovery']+r['dealer_residual_after_aggregate'],r['full_floor_gross_shortfall'])
ck('EE-C07','Constructed maximum dealer residual dispersed300m',max(r['dealer_residual_after_aggregate'] for r in agg if r['world'].startswith('Losses dispersed')),300000000)
ck('EE-C08','Constructed maximum dealer residual synchronized700m',max(r['dealer_residual_after_aggregate'] for r in agg if r['world'].startswith('Losses synchronized')),700000000)
yaris=next(r for r in costtotals if 'Yaris' in r['model']);ck('EE-C09','Four Yaris dated estimates total8.5m',yaris['combined_estimate_total_idr'],8500000)
if any('bz4x' in r['model'].lower() for r in costtotals):
 bz=next(r for r in costtotals if 'bz4x' in r['model'].lower());ck('EE-C10','Four bZ4X dated estimates total9.101m',bz['combined_estimate_total_idr'],9101000)
ck('EE-C11','Legacy six-event table ends at recommended month30',calendar[-1]['recommended_month'],30)
save('checks',checks)
assert all(r['passed'] for r in checks),'Mechanism calculation check failed'
source_checks=json.loads((B/'source_checks.json').read_text())
for row in source_checks:
 sid=row['source_id'];row['content_validity']='valid public source checked'
 if sid=='EE-S05':row['content_validity']='invalid target: historical brochure URL redirected to homepage; do not use brochure contents'
 if sid=='EE-S08':row['content_validity']='unavailable target: current linked PDF returned404; separate official original inspected as EE-S11'
 if sid=='EE-S02':row['content_validity']='partial: static FAQ response exposes general/default category, not full dynamic T-CARE details'
 if sid=='EE-S09':row['content_validity']='index only: no detailed model manual retrieved; no authorization token or key used'
source_fields=list(source_checks[0])
with (B/'source_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=source_fields);w.writeheader();w.writerows(source_checks)
(B/'source_checks.json').write_text(json.dumps(source_checks,indent=2)+'\n')
manifest=[dict(path=str(p.relative_to(R.parent)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(input_paths)]
summary=dict(generated_utc=datetime.now(timezone.utc).isoformat(),prespecified_questions=7,focused_source_checks=len(source_checks),source_ownership_clusters=1,program_comparison_rows=len(programs),dated_service_estimate_rows=len(normal),models_with_four_paid_estimate_rows=len(costtotals),constructed_unit_state_rows=len(joint),constructed_aggregate_states=len(agg),commercial_mechanisms=len(mechanisms),checks=len(checks),failed_checks=sum(not r['passed'] for r in checks),forecast_or_causal_uplift_estimates=0,input_manifest=manifest)
(B/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='input_manifest'},indent=2));print(json.dumps(decomp,indent=2));print('Estimate sums',costtotals)
