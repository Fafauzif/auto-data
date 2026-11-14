#!/usr/bin/env python3
"""Offline catalogue, evidence union and case arithmetic for the integrated release.

This does not rerun historical acquisition, infer missing source text, or count
different analytical registers as independent empirical samples.
"""
from pathlib import Path
import argparse, csv, hashlib, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEGACY = ROOT / 'auto-data'

def write_csv(name, rows):
    rows=list(rows)
    if not rows: return
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with (HERE/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    global LEGACY
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--legacy-root',type=Path,default=LEGACY,help='Path to the preserved original repository tree')
    ap.add_argument('--case-pdf',type=Path,default=ROOT/'integration_work/case_source/Semifinal Casebook IBSC 2026.pdf',help='Exact supplied original casebook PDF, if included')
    args=ap.parse_args()
    LEGACY=args.legacy_root.resolve()
    if not (LEGACY/'reports/SOLUTION_MENU.json').exists():
      raise SystemExit('Supply --legacy-root pointing at the preserved original repo tree containing reports/SOLUTION_MENU.json')
    docs=[]
    for p in sorted(LEGACY.rglob('*.md')):
        if '.git' in p.parts:continue
        text=p.read_text(errors='replace', encoding='utf-8')
        docs.append(dict(source_path_in_legacy_repository=str(p.relative_to(LEGACY)),sha256=sha(p),bytes=p.stat().st_size,word_count=len(text.split()),title=next((l.lstrip('# ').strip() for l in text.splitlines() if l.startswith('#')),p.stem),headings_json=json.dumps([l.strip('# ').strip() for l in text.splitlines() if l.startswith('#')],ensure_ascii=False),authority='Historical research frozen 2026-11-11; current release instructions supersede historical task mandates'))
    write_csv('legacy_document_map.csv',docs)
    specs=[
      ('market','workstreams/market/evidence.json',None),
      ('competition','workstreams/competition/evidence_matrix.json',None),
      ('capabilities','workstreams/friend_capabilities/claim_matrix.json',None),
      ('survey_audit','workstreams/friend_surveys/survey_claims.json',None),
      ('insurance','workstreams/friend_insurance/claim_matrix.json',None),
      ('friend_context','workstreams/friend_challenge/claims.json',None),
      ('stakeholders','workstreams/extension_stakeholders/evidence_register.json',None),
      ('original_hypothesis','reports/hypothesis_assessment.json',None),
      ('mechanism_study','workstreams/extension_hypotheses/EXTERNAL_MECHANISM_EVIDENCE.json',None),
      ('legacy_solution','reports/SOLUTION_MENU.json','options'),
    ]
    registers=[];index=[]
    with (HERE/'legacy_evidence_union.jsonl').open('w',encoding='utf-8') as f:
      for ns,rel,key in specs:
        p=LEGACY/rel
        data=json.loads(p.read_text(encoding='utf-8'))
        if key:data=data[key]
        for i,row in enumerate(data):
          local=next((row[k] for k in ['evidence_id','record_id','claim_id','hypothesis_id','solution_id','id'] if row.get(k)),str(i+1))
          out=dict(integrated_id=ns+':'+str(local),record_type='historical_analytical_record_not_independent_observation',namespace=ns,source_path_in_legacy_repository=rel,source_array_index_zero_based=i,source_file_sha256=sha(p),source_record=row)
          f.write(json.dumps(out,ensure_ascii=False)+'\n')
          index.append(dict(integrated_id=out['integrated_id'],namespace=ns,source_path_in_legacy_repository=rel,source_array_index_zero_based=i))
        registers.append(dict(namespace=ns,source_path_in_legacy_repository=rel,records=len(data),sha256=sha(p)))
    write_csv('legacy_evidence_index.csv',index)
    write_csv('legacy_register_inventory.csv',registers)
    app_rows=[]
    for wave,rel in [('first_wave','workstreams/reviews/reviews_derived.csv'),('extension','workstreams/extension_reviews/new_reviews_derived.csv')]:
      with (LEGACY/rel).open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
          app_rows.append(dict(wave=wave,source_path_in_legacy_repository=rel,source_record=row))
    with (HERE/'legacy_app_review_metadata.jsonl').open('w',encoding='utf-8') as f:
      for r in app_rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    narrative_rows=[]
    for wave,rel in [('discovery','workstreams/narratives/narrative_units.jsonl'),('followup','workstreams/narratives/validation_units.jsonl')]:
      for line in (LEGACY/rel).read_text(encoding='utf-8').splitlines():
        if line.strip():narrative_rows.append(dict(wave=wave,source_path_in_legacy_repository=rel,source_record=json.loads(line)))
    with (HERE/'legacy_narrative_metadata.jsonl').open('w',encoding='utf-8') as f:
      for r in narrative_rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
    case=[('Vehicle sales',60000,3600),('Services',2400,1320),('Spare parts',4800,1200),('Body and paint',1800,630)]
    case_rows=[dict(business_line=n,revenue_idr_billion=r,gross_profit_idr_billion=g,gross_margin_pct=g/r*100,gp_share_pct=g/6750*100,scope='Supplied FY2025 case assumptions; all powertrains',source='legacy story_assets/economic_story.json EC01; reported original casebook Exhibit3 p10') for n,r,g in case]
    write_csv('case_business_line_inputs.csv',case_rows)
    original_case=args.case_pdf
    if original_case.exists():
      case_source=dict(filename=original_case.name,bytes=original_case.stat().st_size,sha256=sha(original_case),pages=19,source_role='User supplied competition casebook; primary case baseline, not audited public company accounts',text_extraction='original_casebook.txt',read_status='Full 19-page extracted text inspected by research agent',authority='Original case facts and participant constraints')
      (HERE/'original_casebook_source.json').write_text(json.dumps(case_source,indent=2), encoding='utf-8')
    kpis=[
      ('downloads','500000+','downloads',11,'Cumulative denominator; not active or unique customers'),
      ('monthly_active_users_midpoint',21000,'monthly active users',11,'Case range20000–22000; approximate'),
      ('mau_download_share',4,'percent approximate',11,'Not active share of currently installed devices'),
      ('sessions_per_active_user',1.6,'sessions per month',11,'Case marks this value with an asterisk'),
      ('consumer_traffic_digital_share','10–20','percent',11,'Case traffic scope; not sales conversion'),
      ('mau_primary_service_booking',46,'percent of MAU activity distribution',11,'Different denominator from booking channel mix'),
      ('mau_primary_catalog_prices',22,'percent of MAU activity distribution',11,'Not vehicle-purchase conversion'),
      ('mau_primary_promotions_loyalty',14,'percent of MAU activity distribution',11,'Not incremental contribution'),
      ('mau_primary_tracking',10,'percent of MAU activity distribution',11,'Order and service tracking combined'),
      ('mau_primary_testdrive_tradein',8,'percent of MAU activity distribution',11,'Two tasks combined, not completed transactions'),
      ('bookings_walkin_phone',46,'percent of service bookings',11,'Combined channels'),
      ('bookings_whatsapp',38,'percent of service bookings',11,'Assisted digital channel'),
      ('bookings_digiroom',16,'percent of service bookings',11,'No volume or completion denominator supplied'),
      ('mau_age_18_24',6,'percent of MAU age distribution',11,'Not all Toyota owners'),
      ('mau_age_25_35',37,'percent of MAU age distribution',11,'Not all Toyota owners'),
      ('mau_age_36_50',41,'percent of MAU age distribution',11,'Not all Toyota owners'),
      ('mau_age_51plus',16,'percent of MAU age distribution',11,'Not all Toyota owners'),
      ('investment_cap_2026_2028',150,'IDR billion incremental investment ceiling',6,'Not a target spend or verified approved budget'),
      ('case_national_wholesale_2025',803687,'vehicles',8,'Wholesales, not deliveries to retail customers'),
      ('case_xev_total_2025',175144,'vehicles',8,'HEV+PHEV+BEV in this case'),
      ('case_toyota_wholesale_2025',250431,'vehicles',9,'Toyota, not Auto2000'),
      ('case_toyota_xev_estimate',33950,'vehicles approximate estimated',9,'Do not replace with Toyota+Lexus AR figures'),
      ('case_auto2000_toyota_sales_share','70–80','percent approximate',2,'Case network description; not a dealer-specific conversion factor for every cohort'),
      ('case_xev_share_2025',21.8,'percent of national wholesales',8,'HEV+PHEV+BEV; differs from BEV-only definitions'),
      ('case_bev_units_2025',103931,'vehicles',8,'BEV share59.3%of case EV total and12.9%of national market'),
      ('case_hev_units_2025',65943,'vehicles',8,'HEV share37.7%of case EV total and8.2%of national market'),
      ('case_phev_units_2025',5270,'vehicles',8,'PHEV share3.0%of case EV total and0.7%of national market'),
      ('case_toyota_hybrid_share',51,'percent of hybrid sales',3,'Not Astra Group national share and not Auto2000 customer share'),
      ('case_giias_orders',4250,'SPK orders',9,'GIIAS2025; not completed delivered retail transactions'),
      ('case_giias_order_electrified_share',34,'percent of GIIAS SPK orders',9,'Not national sales mix or delivered vehicle mix'),
    ]
    write_csv('original_case_kpis.csv',[dict(metric=m,value=v,unit=u,casebook_page=p,boundary=b) for m,v,u,p,b in kpis])
    menu=json.loads((LEGACY/'reports/SOLUTION_MENU.json').read_text(encoding='utf-8'))['options']
    bridge=[]
    for r in menu:
      n=int(r['solution_id'][-2:])
      if n in [1,2,3]:prong='Acquisition';treatment='Develop as one fit/cash-flow/confirmed-demonstration pathway'
      elif n in [5,6,7,8,9,10]:prong='Ownership/paid work';treatment='Develop as one eligible job-completion pathway'
      elif n in [12,14,15]:prong='Replacement/trade-in';treatment='Develop around evidence acceptance and an inspected net-upgrade offer'
      elif n in [13,18,19,20,21]:prong='Shared infrastructure';treatment='Enable the three pathways; no separate additive profit pool'
      elif n in [16,17,27]:prong='Replacement/risk';treatment='Defer a launch promise until funded economics and actual contracts; capped incentive remains distinct from a floor'
      else:prong='Conditional adjacent job';treatment='Retain in archive; develop only for a demonstrated segment/job and actual service scope'
      bridge.append(dict(solution_id=r['solution_id'],original_title=r['title'],primary_strategy_location=prong,current_treatment=treatment,source_path_in_legacy_repository='reports/SOLUTION_MENU.json',legacy_status='Frozen alternatives, not originally ranked',current_status='2026-11-14 evidence-led strategic interpretation',customer_question=r['customer_question'],existing_baseline=r['existing_capability_baseline']))
    write_csv('solution_priority_bridge.csv',bridge)
    assertions=[dict(check='case_revenue_total',actual=sum(x[1] for x in case),expected=69000),dict(check='case_gp_total',actual=sum(x[2] for x in case),expected=6750),dict(check='case_after_sales_revenue',actual=sum(x[1] for x in case[1:]),expected=9000),dict(check='case_after_sales_gp',actual=sum(x[2] for x in case[1:]),expected=3150),dict(check='case_operating_profit',actual=6750-4620,expected=2130),dict(check='legacy_app_records',actual=len(app_rows),expected=358),dict(check='legacy_narrative_units',actual=len(narrative_rows),expected=95)]
    assertions.extend([dict(check='legacy_app_unique_record_keys',actual=len({r['source_record']['record_key'] for r in app_rows}),expected=358),dict(check='namespaced_register_ids_unique',actual=len({r['integrated_id'] for r in index}),expected=len(index)),dict(check='legacy_solution_bridge_count',actual=len(bridge),expected=27)])
    for a in assertions:a['pass']=a['actual']==a['expected']
    assert all(a['pass'] for a in assertions)
    (HERE/'integration_research_checks.json').write_text(json.dumps(dict(as_of='2026-11-14',source_freeze='2026-11-11',checks=assertions,registers=registers,document_count=len(docs),union_rows=len(index),units_warning='Registers deliberately preserve overlapping evidence interpretations. Union rows are not independent sources or customers.'),indent=2), encoding='utf-8')

if __name__=='__main__':main()
