from pathlib import Path
import csv,json
out=Path(__file__).resolve().parent
F=200_000_000; retention=10_000_000; insurer_limit=15_000_000;N=20
rows=[]
for offer in range(80_000_000,240_000_001,10_000_000):
 shortfall=max(0,F-offer)
 for cap in (5_000_000,10_000_000,20_000_000):
  topup=min(cap,shortfall);claim=min(insurer_limit,max(0,shortfall-retention));dealer=shortfall-claim
  rows.append(dict(scenario_id=f'ILL-{len(rows)+1:03}',data_status='constructed deterministic illustration; not observed data or insurance quote',floor=F,valid_offer=offer,topup_cap=cap,topup=topup,capped_credit=offer+topup,capped_credit_meets_floor=offer+topup>=F,full_floor_shortfall=shortfall,assumed_insurer_retention=retention,assumed_insurer_perunit_limit=insurer_limit,conditional_insurer_payment=claim,dealer_full_floor_residual=dealer,eligible_redemptions=N,capped_topup_total=N*topup,full_floor_gross_shortfall=N*shortfall,dealer_residual_total=N*dealer,assumed_coverage='all modeledunits/causes eligible; aggregate limit not exhausted; no expense/premium/timevalue'))
with (out/'illustrative_risk_scenarios.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'risk_math_summary.json').write_text(json.dumps(dict(scenarios=len(rows),observed_records=0,formulae={'shortfall':'max(0,F-valid_offer)','topup':'min(cap,shortfall)','capped_credit':'valid_offer+topup','full_floor_insurance_recovery':'min(perunit_limit,max(0,shortfall-retention)) conditional on coverage and remaining aggregate limit','dealer_net_shortfall':'shortfall-recovery'},missing=['actual offer distributions','redemption/market dependence','actual underwriting appetite','policy pricing','aggregate limits','counterparty default','settlement timing','incremental vehicle GP','partner remarketing contribution','programme operation costs'],risk='An insurer limit caps insurer payment, not an unconditional customer floor obligation. A dealer top-up cap limits customer benefit and cannot be called a full floor.'),indent=2))
assert min(r['topup'] for r in rows)>=0
assert all(r['topup']<=r['topup_cap'] for r in rows)
assert all(r['conditional_insurer_payment']<=insurer_limit for r in rows)
assert all(r['dealer_full_floor_residual']>=0 for r in rows)
print('PASS',len(rows),'illustrative scenarios; no empirical estimate')
