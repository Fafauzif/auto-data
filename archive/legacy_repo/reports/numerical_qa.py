"""Independent read-only arithmetic/scope QA of the frozen research artifacts.

Only writes this audit's own outputs. Derived check counts are not observations.
"""
import csv, hashlib, json, math, sqlite3
from pathlib import Path
from datetime import datetime, timezone
import fitz

R=Path(__file__).resolve().parents[1]
O=R/'reports'
inputs=set();checks=[]
def readjson(p):
 p=R/p;inputs.add(p);return json.loads(p.read_text())
def readcsv(p):
 p=R/p;inputs.add(p)
 with p.open() as f:return list(csv.DictReader(f))
def check(id,topic,assertion,observed,expected,refs,limit='',tol=1e-8):
 if isinstance(expected,(int,float)) and not isinstance(expected,bool):ok=abs(float(observed)-expected)<=tol
 else:ok=observed==expected
 checks.append(dict(check_id=id,topic=topic,assertion=assertion,status='PASS' if ok else 'FAIL',observed=json.dumps(observed,ensure_ascii=False),expected=json.dumps(expected,ensure_ascii=False),evidence_refs=refs,scope_limit=limit))
def qualify(id,topic,assertion,refs,limit,status='QUALIFIED'):
 checks.append(dict(check_id=id,topic=topic,assertion=assertion,status=status,observed='Not an identified numeric effect',expected='Use only with the stated scope',evidence_refs=refs,scope_limit=limit))

# Casebook transcription is checked against actual supplied PDF text, not friend text.
case=R.parent/'upload'/'Semifinal Casebook IBSC 2026.pdf';inputs.add(case)
d=fitz.open(case)
for id,page,needles in [('NQ01',8,['803,687','175,144','103,228']),('NQ02',9,['250,431','33,950']),('NQ03',10,['60,000','3,600','2,400','1,320','4,800','1,200','1,800','630','69,000','6,750','4,620','2,130'])]:
 text=d[page-1].get_text();check(id,'Casebook inputs',f'All transcribed arithmetic inputs appear on casebook printed/PDF page {page}',all(x in text for x in needles),True,f'Supplied casebook p{page}','Case data, including estimated Toyota xEV volume; not independent audited operating records.')
revenues=[60000,2400,4800,1800];gp=[3600,1320,1200,630]
check('NQ04','Casebook P&L','Revenue lines sum to69,000bn',sum(revenues),69000,'Casebook p10')
check('NQ05','Casebook P&L','Gross-profit lines sum to6,750bn',sum(gp),6750,'Casebook p10')
check('NQ06','Casebook P&L','After-sales revenue9,000bn',sum(revenues[1:]),9000,'Casebook p10')
check('NQ07','Casebook P&L','After-sales GP3,150bn',sum(gp[1:]),3150,'Casebook p10')
check('NQ08','Casebook P&L','After-sales revenue share rounds13.0%',round(sum(revenues[1:])/sum(revenues)*100,1),13.,'Casebook p10')
check('NQ09','Casebook P&L','After-sales GP share rounds46.7%',round(sum(gp[1:])/sum(gp)*100,1),46.7,'Casebook p10')
check('NQ10','Casebook P&L','Combined after-sales GM35%',sum(gp[1:])/sum(revenues[1:])*100,35.,'Casebook p10','Weighted combined margin, not the55%services-only line margin.')
check('NQ11','Casebook P&L','Operating profit after unallocated opex2,130bn',sum(gp)-4620,2130,'Casebook p10')
check('NQ12','Casebook P&L','Operating margin rounds3.1%',round(2130/69000*100,1),3.1,'Casebook p10')
check('NQ13','Casebook market','Powertrain units reconcile to175,144',103931+65943+5270,175144,'Casebook p8')
check('NQ14','Casebook market','xEV market share rounds21.8%',round(175144/803687*100,1),21.8,'Casebook p8')
check('NQ15','Casebook market','xEV growth rounds69.7%',round((175144/103228-1)*100,1),69.7,'Casebook p8')
qualify('NQ16','Casebook engagement','46%main activity and16%booking channel have different denominators.','Casebook p11','Neither produces completed bookings, work orders or GP when multiplied by MAU. Main activity is not a transaction log.')
qualify('NQ17','Casebook engagement','Approximate21kMAU divided by500k+downloads is not a precisely identified activation rate.','Casebook p11','Downloads are a cumulative threshold and may not be unique people/retained installs. The case itself describes approximately4%;21k/500k=4.2%is conditional arithmetic, not an exact observed rate.')

# Case-based category-mix sensitivity, independently derived.
mc=readjson('workstreams/market/economic_calculations.json');mc={r['calculation_id']:r for r in mc}
a,b,t,e=250431,803687,33950,175144
se=t/e;sc=(a-t)/(b-e);mix=e/b
check('NQ18','Market sensitivity','Weighted segments recover overall Toyota share',mix*se+(1-mix)*sc,a/b,'MC01;Casebook p8–9')
check('NQ19','Market sensitivity','10ppcategory-mix change yields stated overall-share change',.1*(se-sc)*100,mc['MC01']['overall_share_change_pp'],'MC01','Constant within-category shares assumed; percentage-point effect, not percent decline or forecast.')
check('NQ20','Synthetic mechanisms','Both lower due-work and lower capture produce120versus160', [100*1.5*.8,100*2*.6],[120.,120.],'MC02','Constructed counterexample; not100actual vehicles.')
check('NQ21','Nested survey','Rounded nested-share calculation28.06%',.61*(1-.54)*100,mc['MC04']['result_percent'],'MC04;MS02','EV intenders under the common-base interpretation; lack of dedicated access is not inability to charge.')

# Actual current public calculator outputs; compare same vehicle and base DP.
f=readcsv('workstreams/journeys/finance_scenarios.csv')
check('NQ22','Finance','10displayed options across2insurance choices and5tenors',len(f),10,'UX03;UX04')
check('NQ23','Finance','BaseDP20%of475.4m equals95.08m',475400000*.2,95080000,'UX03;UX04','BaseDP differs from total cash required upfront.')
check('NQ24','Finance','All rows preserve model/location/price/baseDP/ADDM/blankincome',[len({r[k] for r in f}) for k in ['model','location','price_idr','base_dp_idr','base_dp_percent','first_instalment','income_entered']],[1]*7,'finance_scenarios.csv')
check('NQ25','Finance','Remaining months equal tenor minus1 for all rows',all(int(r['displayed_remaining_months'])==int(r['tenor_months'])-1 for r in f),True,'UX03;UX04','ADDM first instalment timing; do not multiply monthly amount by60 in addition to full upfront.')
si={r['insurance_payment']:r for r in f if r['tenor_months']=='60'};u=si['upfront'];i=si['instalments']
up=lambda r:int(r['total_upfront_idr']);mo=lambda r:int(r['monthly_idr'])
check('NQ26','Finance','Insurance financing reduces displayed upfront cash by45,314,339',up(u)-up(i),45314339,'UX03;UX04','Conditional simulation; not verified approval, all-in cost or fee itemization.')
check('NQ27','Finance','Insurance financing raises monthly amount by1,132,241',mo(i)-mo(u),1132241,'UX03;UX04')
check('NQ28','Finance','Upfront32.57%and23.04%ofprice differ from baseDP20%', [round(up(u)/475400000*100,2),round(up(i)/475400000*100,2)],[32.57,23.04],'UX03;UX04','No claim that the difference is hidden fees.')
for r in f:
 qualify('NQ29-'+r['insurance_payment']+'-'+r['tenor_months'],'Finance scope',f"{r['insurance_payment']} insurance, {r['tenor_months']}months: binding quote flag is {r['is_binding_quote']}.",'UX03;UX04','Displayed nominal cash flows do not identify APR, exact insurance cover or complete contractual fees.')

# Astra chart arithmetic; both decomposition orderings reconcile but allocate differently.
ar=readjson('workstreams/friend_capabilities/economic_diagnostics.json')
t0,t1,x0,x1=291566,251954,37693,31668;m0=x0/t0;m1=x1/t1
for n,key,value in [('NQ30','xev_change_pct',(x1/x0-1)*100),('NQ31','total_change_pct',(t1/t0-1)*100),('NQ32','xev_mix_2024_pct',m0*100),('NQ33','xev_mix_2025_pct',m1*100),('NQ34','mix_change_percentage_points',(m1-m0)*100)]:
 check(n,'Astra portfolio',key,value,ar[key],'AR2025printed140/PDF142;FC-N12–15','Toyota AND Lexus domestic sales; not Auto2000 or installed-base adoption.')
sc0=(t1-t0)*m0;mx1=t1*(m1-m0);sc1=(t1-t0)*m1;mx0=t0*(m1-m0)
check('NQ35','Astra accounting','Reported ordering scale+mix reconstructs−6,025units',sc0+mx1,x1-x0,'economic_diagnostics.json')
check('NQ36','Astra accounting','2024mix applied to2025total gives32,572.049',t1*m0,ar['accounting_decomposition']['expected_xev_at_2024_mix'],'economic_diagnostics.json','Counterfactual holds mix only; no causal assumption about why total sales changed.')
check('NQ37','Astra accounting','Alternative ordering also reconstructs change',sc1+mx0,x1-x0,'AR2025p140;independent recomputation')
qualify('NQ38','Astra accounting','Scale/mix components depend on the chosen ordering, not identified causes.','NQ35;NQ37',f'Reported ordering units scale={sc0:.3f}, mix={mx1:.3f}; alternative scale={sc1:.3f}, mix={mx0:.3f}. Do not say85%ofdecline was caused by market weakness.')

# Each insurance scenario checked independently using integer arithmetic.
ins=readcsv('workstreams/friend_insurance/illustrative_risk_scenarios.csv')
check('NQ39','Insurance illustration','51deterministic rows, not51customers orquotes',len(ins),51,'illustrative_risk_scenarios.csv')
for r in ins:
 n=lambda key:int(r[key]);s=max(0,n('floor')-n('valid_offer'));top=min(n('topup_cap'),s);rec=min(n('assumed_insurer_perunit_limit'),max(0,s-n('assumed_insurer_retention')));dealer=s-rec;count=n('eligible_redemptions')
 computed=[s,top,n('valid_offer')+top,rec,dealer,count*top,count*s,count*dealer]
 stored=[n(k) for k in ['full_floor_shortfall','topup','capped_credit','conditional_insurer_payment','dealer_full_floor_residual','capped_topup_total','full_floor_gross_shortfall','dealer_residual_total']]
 check('NQ40-'+r['scenario_id'],'Insurance arithmetic','All8shortfall/credit/recovery/aggregate arithmetic fields agree',stored,computed,r['scenario_id'],'Conditional eligible cover, no aggregate exhaustion, premium, expense, time value or insurer default. Not an available insurance quote.')
qualify('NQ41','Insurance economics','Contribution, ujrah, dealer fee, insurer recovery and dealer GP are distinct.','friend_insurance/analysis.md;INSclaimmatrix','No signed dealer compensation, contribution level or underwriting appetite was established. Arithmetic does not demonstrate availability or economic viability.')

# Survey question bases and chart inputs stay separate.
sv=readcsv('workstreams/market/deloitte_service_indonesia.csv')
check('NQ42','Deloitte survey','28numeric cells, not28respondents',len(sv),28,'deloitte_service_indonesia.csv')
for q,base in [('Q16',629),('Q17',618),('Q21',618),('Q22',629)]:
 z=[r for r in sv if r['question']==q]
 check('NQ43-'+q,'Deloitte survey',f'{q}uses its own base{base}',sorted({int(r['sample_n']) for r in z}),[base],'MS03p33–35','These related questions are not independent respondent samples to add together.')
 check('NQ44-'+q,'Deloitte survey',f'{q}rounded published shares sum within1ppof100',abs(sum(int(r['published_percent']) for r in z)-100)<=1,True,'MS03p33–35','Rounded published shares; do not back-calculate exact respondent counts.')
qualify('NQ45','Deloitte survey','Printed0%most-important booking factors do not establish zero demand.','MS03p34Q21','Question is the most-important aspect; rounded0%is not zero users, usage, usefulness or a causal effect.')
q17={r['metric_label']:int(r['published_percent']) for r in sv if r['question']=='Q17'}
check('NQ46','Figure inputs','Q17ranking quality23,trust21,warranty18',sorted(q17.items(),key=lambda x:-x[1])[:3],[('Quality of work',23),('Trust',21),('Warranty coverage',18)],'service_choice_factors.png;MS03Q17')

# Dataset counts, label alignment and geography recomputed from public derivative tables.
ga=readcsv('workstreams/datasets/gaikindo_2025_category_derived.csv')
check('NQ47','GAIKINDO categories','2025category table totals803,687',sum(int(r['units']) for r in ga),803687,'gaikindo_2025_category_derived.csv','Vehicle categories are not powertrain categories.')
g26=readcsv('workstreams/datasets/gaikindo_2026_monthly_category_derived.csv');gt=readcsv('workstreams/datasets/gaikindo_2026_monthly_totals_derived.csv')
check('NQ48','GAIKINDO conflict','72category cells total679,202',sum(int(r['units']) for r in g26),679202,'gaikindo_2026_monthly_category_derived.csv')
check('NQ49','GAIKINDO conflict','Nine monthly totals agree with category table',sum(int(r['monthly_units']) for r in gt),sum(int(r['units']) for r in g26),'gaikindo_2026_monthly_totals_derived.csv')
check('NQ50','GAIKINDO conflict','Chart exceeds narrative679,020by182',sum(int(r['units']) for r in g26)-679020,182,'DATASETS_REPORT.md;GAIKINDOnarrative','Preserved source/version conflict; neither silently repaired nor presented as harmonized.')
h=readcsv('workstreams/datasets/gaikindo_2025_hybrid_selected_models.csv');ms=readjson('workstreams/datasets/market_analysis_summary.json')
toy=[r for r in h if r['brand']=='Toyota'];zen=next(int(r['wholesale_units']) for r in toy if r['model']=='Innova Zenix')
check('NQ51','Hybrid concentration','Zenix share23,934/30,110=79.49%',zen/30110,ms['Toyota_Zenix_share_of_Toyota_hybrid_computed'],'selectedhybridmodels.csv;GAIKINDO-hostedDetik','Toyota source context, not Auto2000; overall source includes mild hybrids.')
check('NQ52','Hybrid concentration','Three selected Toyota models total97.03%ofToyota hybrids',sum(int(r['wholesale_units']) for r in toy)/30110,ms['Toyota_selected_three_models_share_of_Toyota_hybrid'],'gaikindo_2025_hybrid_selected_models.csv')
ig=readjson('workstreams/datasets/igar_analysis_summary.json');ct=readcsv('workstreams/datasets/igar_label_agreement_crosstab.csv')
total=sum(int(r[c]) for r in ct for c in ['negative','neutral','positive']);diag=sum(int(r[r['rating_based_label']]) for r in ct)
check('NQ53','IGAR labels','3x3crosstab accounts for617,722same underlying rows',total,ig['rating_view_rows'],'igar_label_agreement_crosstab.csv','Two label views, not1.235million independent reviews.')
check('NQ54','IGAR labels','Off-diagonal disagreement255,414',total-diag,ig['label_disagreement_rows'],'igar_label_agreement_crosstab.csv')
check('NQ55','IGAR labels','Disagreement41.3477%',(total-diag)/total,ig['label_disagreement_share'],'igar_analysis_summary.json','Disagreement between weak labels, not either method accuracy; not automotive customers.')
check('NQ56','IGAR duplicates','617,722−617,703=19duplicate excess perview',ig['rating_view_rows']-ig['unique_rating_composite_keys'],19,'igar_analysis_summary.json','Composite keys are not verified unique people; preserve duplicate distinction.')
co=readcsv('workstreams/datasets/five_branch_coordinate_crosscheck.csv')
def hav(a,b,c,d):
 a,b,c,d=map(math.radians,[a,b,c,d]);v=math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2
 return 6371.0088*2*math.asin(math.sqrt(min(1.,v)))
for r in co:
 value=hav(*[float(r[k]) for k in ['source_latitude','source_longitude','official_directions_candidate_latitude','official_directions_candidate_longitude']])
 check('NQ57-'+r['station_id'],'Coordinate chart','Independent Haversine matches stored separation',value,float(r['straight_line_disagreement_km']),r['official_page_url'],'Official direction candidate is a comparison, not field-verified charger ground truth.')
gs=readjson('workstreams/datasets/geo_sensitivity_summary.json');gg=readcsv('workstreams/datasets/auto2000_geo_sensitivity.csv')
check('NQ58','Coordinate sensitivity','One of5selected comparisons exceeds1km',sum(float(r['straight_line_disagreement_km'])>1 for r in co),1,'five_branch_coordinate_crosscheck.csv','Five purposively selected cases; not geographic error prevalence.')
check('NQ59','Coordinate sensitivity','Scenario27→28outof28within5km',[sum(float(r[k])<=5 for r in gg) for k in ['original_nearest_nonauto_haversine_km','scenario_nearest_nonauto_haversine_km']],[27,28],'auto2000_geo_sensitivity.csv','Haversine proximity; not route time, access, available chargers or corrected ground truth.')
sp=readjson('workstreams/datasets/spklu_analysis_summary.json')
check('NQ60','Derived volume','2,454×2,453=6,019,662directed pair computations',sp['station_rows']*(sp['station_rows']-1),sp['distance_comparisons_computed'],'spklu_analysis_summary.json','Unique unordered pairs are half this number; neither is new source observations.')
check('NQ61','SPKLU source counts','Provider-type source counts reconcile to2,454',sum(sp['source_provider_counts'].values()),sp['station_rows'],'spklu_analysis_summary.json','Source station records distinct from charger boxes, reconstructed unit counts and connector counts.')
pr=readcsv('workstreams/datasets/province_charging_vs_registered_cars.csv')
check('NQ62','Charging density','Every province density uses registered passenger-car stock',all(abs(int(r['stations'])/float(r['passenger_vehicle_stock_2025'])*100000-float(r['stations_per_100000_registered_passenger_vehicles']))<1e-8 for r in pr),True,'province_charging_vs_registered_cars.csv','2026site numerator/2025allregisteredcars denominator, not per-BEV adequacy or active demand.')

# Review and narrative accounting; no representative-customer inference.
rv=readcsv('workstreams/reviews/reviews_derived.csv');ra=readcsv('workstreams/reviews/manual_audit.csv');vs=readjson('workstreams/reviews/validation.json')
check('NQ63','Review grain','210unique public review records',len({r['record_key'] for r in rv}),210,'reviews_derived.csv','Platform-selected mixed-date/locale corpus, not population complaint prevalence.')
check('NQ64','Review coding','132AI-coded app-job-eligible records',sum(r['eligible_for_app_task_analysis']=='True' for r in rv),vs['eligible_self_reported_app_job_n'],'reviews_derived.csv;manual_audit.csv','AI-coded source reports; no independent task verification or human-validation claim.')
check('NQ65','Review coding','30targeted second-AI checks',sum(r['second_ai_checked']=='True' for r in ra),vs['second_ai_targeted_check_n'],'manual_audit.csv','Targeted nonblind check, not a random holdout or calibrated inter-rater reliability estimate.')
nr=readjson('workstreams/narratives/combined_metrics.json')
check('NQ66','Narrative grain','75discovery+20followup=95annotation units',nr['discovery_annotation_units']+nr['fresh_followup_annotation_units'],nr['total_annotation_units'],'combined_metrics.json','38source documents; not95independent customers or verified incidents.')
check('NQ67','Narrative grain','Evidence-kind counts reconcile to95',sum(nr['evidence_kind_counts'].values()),nr['total_annotation_units'],'combined_metrics.json')
site=readjson('workstreams/site/summary.json')
pages=readcsv('workstreams/site/page_observations.csv')
good=[r for r in pages if r['status']=='200' and not r['error']]
db=R/'data'/'site_evidence.sqlite';inputs.add(db)
with sqlite3.connect(f'file:{db}?mode=ro',uri=True) as con:
 links_n=con.execute('select count(*) from links').fetchone()[0]
check('NQ68','Final site freeze','Frozen source counts reconcile across page CSV and structural-link database',[len(pages),len(good),sum(int(r['main_words']) for r in good),links_n],[345,281,181158,15323],'site/summary.json;page_observations.csv;data/site_evidence.sqlite','Purposive requested URLs and selected raw text, not unique customers, rendered user outcomes or sitewide error prevalence.')

# Figure-state inspection is separately dated because root is updating one title.
figscript=R/'shared'/'make_figures.py';inputs.add(figscript)
for name in ['service_choice_factors.png','finance_cash_tradeoff.png','branch_coordinate_checks.png']:inputs.add(R/'figures'/name)
title_scoped='Quality trust and warranty lead these stated service choice reasons' in figscript.read_text()
image_fresh=(R/'figures'/'service_choice_factors.png').stat().st_mtime>=figscript.stat().st_mtime
if title_scoped and image_fresh:
 check('NQ69','Figure state','Scoped Q17 chart generator and refreshed output timestamp',True,True,'shared/make_figures.py;service_choice_factors.png','Timestamp freshness check, not an automated OCR or new visual inspection. Numeric values independently checked in NQ46.')
else:
 qualify('NQ69','Figure state','Service-choice chart numeric values match Q17; rendered title refresh pending.','shared/make_figures.py;service_choice_factors.png','Script narrows the title to stated reasons; the inspected PNG still has the earlier overbroad title. Rerender required; no data-value correction needed.',status='PENDING')

# Fresh conditional IGAR analysis and friend illustration arithmetic.
igc=readjson('workstreams/datasets/igar_conditional_analysis.json')
tr={r['translation_missing']:r for r in igc['translation_missing']}
check('NQ70','IGAR conditional','Missing/present translation groups reconcile to617,722rows',sum(r['size'] for r in tr.values()),ig['rating_view_rows'],'igar_conditional_analysis.json')
check('NQ71','IGAR conditional','Group disagreements reconcile to255,414',sum(r['sum'] for r in tr.values()),ig['label_disagreement_rows'],'igar_conditional_analysis.json')
for missing in [False,True]:
 row=tr[missing];check('NQ72-'+str(missing),'IGAR conditional','Disagreement mean equals group numerator/denominator',row['sum']/row['size'],row['mean'],'igar_conditional_analysis.json','Observational association; missing translation is not randomized and neither label is ground truth.')
check('NQ73','IGAR conditional','Missing-translation group contributes only2.96%ofall disagreements',round(tr[True]['sum']/ig['label_disagreement_rows']*100,2),2.96,'igar_conditional_analysis.json','97.25%within-group disagreement does not mean this small group explains the overall41.35%rate.')
ll=readjson('workstreams/friend_challenge/logic_tests.json');ll={r['test_id']:r for r in ll}
check('NQ74','Friend illustration','Equal visits with different jobs:200visits,800versus400jobs',[100*2,100*2*4,100*2*2],[ll['L02']['visits_each'],ll['L02']['jobs_A'],ll['L02']['jobs_B']],'friend_challenge:L02','Constructed identity; equal scheduled visit cadence does not imply equal work quantity or margin.')
check('NQ75','Friend illustration','Same job GP500k−300k=200k',ll['L03']['same_job_revenue_IDR']-ll['L03']['same_job_direct_cost_IDR'],ll['L03']['GP_each_channel_IDR'],'friend_challenge:L03','Channel or payer change alone does not change GP when all modeled economics are fixed.')
check('NQ76','Friend illustration','Capped trade-in credit180m+10m=190m',180+min(10,max(0,200-180)),ll['L04']['capped_customer_credit_IDR_m'],'friend_challenge:L04','This benefit remains below a full200m floor.')
check('NQ77','Friend illustration','20×10m top-up maximum200m',20*10,ll['L04']['maximum_capped_topups_IDR_m'],'friend_challenge:L04','Quota bounds this defined capped benefit before operations, not an uncapped full floor.')
qualify('NQ78','Awareness scope','57%minus28%=29percentage points is unverified-input arithmetic.','friend_surveys/SURVEY_CLAIM_AUDIT.md','Awareness values remain supplied figures because full masked original chart was not accessed. Do not present the29pp as independently verified, purchase conversion, Digiroom awareness or incremental sales.')
qualify('NQ79','PwC scope','33%owner return consideration and71%reason have nested conditional bases.','friend_surveys/SURVEY_CLAIM_AUDIT.md','The71%concerns owners considering return; regional chart n158is not an Indonesia denominator. Neither figure measures observed switches or maintenance invoices.')
check('NQ80','Casebook constraint','Actual source states150billion incremental investment cap2026–2028',all(s in d[5].get_text() for s in ['150 billion','2026–2028']),True,'Casebook p6','A cap is not approved spending, an estimated program budget or a bound on every later contingent liability.')
check('NQ81','Casebook BEV context','BYD46,711/103,931 rounds to45%ofBEV sales',round(46711/103931*100),45,'Casebook p4,p8','BEV segment share; not total xEV, all cars, Auto2000 lost sales or a causal Digiroom effect.')
check('NQ82','Final site freeze','Status counts reconcile to345requestedURLs',sum(site['status_counts'].values()),len(pages),'site/summary.json;page_observations.csv','HTTP0 is a recorded transport failure state; not an HTTPserver response.')
check('NQ83','Final site freeze','Successful source-family counts reconcile to281HTMLpages',sum(site['families'].values()),len(good),'site/summary.json','Purposive family mix, not a prevalence-weighted website sample.')
check('NQ84','Final site freeze','Summary words and links match independently read aggregates',[site['main_text_words_extracted_private'],site['link_rows']],[sum(int(r['main_words']) for r in good),links_n],'site/summary.json;page_observations.csv;site_evidence.sqlite','Structural link rows differ from occurrence count and independentinformation count.')
ref=readcsv('workstreams/site/v3_qa_reference.csv');byurl={r['url']:r for r in pages}
check('NQ85','Final site QA','All24fixed reference selections match production word counts and content hashes',sum(int(byurl[r['url']]['main_words'])==int(r['expected_words_v3']) and byurl[r['url']]['main_hash']==r['expected_hash_v3'] for r in ref),24,'site/v3_qa_reference.csv;page_observations.csv','An independentAI cached-source comparison, not human review, fresh visits or randomsiteprevalence.')
pub=readcsv('workstreams/site/v3_qa_published_comparison.csv');qsum=readjson('workstreams/site/v3_qa_reference_summary.json')
fields=['version3','selector_matches','words_match','content_hash_matches','main_links_match','rp_flag_matches','canonical_matches','h1_matches','forms_match','title_cap_matches','capture_time_matches_original','source_request_id_matches','AI_cached_source_check_no_human']
check('NQ86','Final site QA','24published comparisons pass every recorded check',sum(all(r[k]=='True' for k in fields) for r in pub),24,'site/v3_qa_published_comparison.csv','Fixed purposive24-source audit; no human-validation or sitewide accuracy claim.')
check('NQ87','Final site QA','Audit explicitly reports no network requests and no human validation',[qsum['new_network_requests'],qsum['human_validation'],qsum['production_v3_verified']],[0,False,True],'site/v3_qa_reference_summary.json','Offline comparison against captured HTML, not verified customer behavior.')

# Add spaces at numerical boundaries in prose fields without changing IDs or URLs.
import re
for row in checks:
 for key in ['assertion','scope_limit']:
  text=row[key]
  text=re.sub(r'(?<=\d)(?=[A-Za-z])',' ',text)
  text=re.sub(r'(?<=[A-Za-z])(?=\d)',' ',text)
  text=re.sub(r'(?<=%)(?=[A-Za-z])',' ',text)
  text=text.replace('Auto 2000','Auto2000')
  row[key]=text

with (O/'numerical_qa_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
(O/'numerical_qa_checks.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n')
manifest=[dict(path=str(p.relative_to(R.parent)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sorted(inputs)]
summary=dict(generated_at_utc=datetime.now(timezone.utc).isoformat(),check_rows=len(checks),status_counts={s:sum(r['status']==s for r in checks) for s in ['PASS','FAIL','QUALIFIED','PENDING']},input_manifest=manifest,does_not_count_independent_observations=True,modifies_source_data=False,astra_alternative_ordering=dict(scale=sc1,mix=mx0),finance60=dict(upfront_reduction=up(u)-up(i),monthly_increase=mo(i)-mo(u),upfront_pct_price_upfrontinsurance=up(u)/475400000*100,upfront_pct_price_financedinsurance=up(i)/475400000*100))
(O/'numerical_qa_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='input_manifest'},indent=2))
assert not any(r['status']=='FAIL' for r in checks),'Numerical mismatch; inspect checks CSV'
