"""Offline checks of extension outputs only. Never runs collectors or mutates source data."""
from pathlib import Path
from datetime import datetime, timezone, date
import csv,json,hashlib,collections,math
import h5py,numpy as np
from scipy.io import loadmat

R=Path(__file__).resolve().parents[1];O=R/'reports';inputs=set();checks=[]
def js(rel):
 p=R/rel;inputs.add(p);return json.loads(p.read_text())
def cs(rel):
 p=R/rel;inputs.add(p)
 with p.open() as f:return list(csv.DictReader(f))
def ck(id,topic,claim,observed,expected,refs,limit='',tol=1e-8):
 ok=abs(observed-expected)<=tol if isinstance(expected,(int,float)) and not isinstance(expected,bool) else observed==expected
 checks.append(dict(check_id=id,topic=topic,assertion=claim,status='PASS' if ok else 'FAIL',observed=observed,expected=expected,evidence_refs=refs,scope_limit=limit))
def qual(id,topic,claim,refs,limit):
 checks.append(dict(check_id=id,topic=topic,assertion=claim,status='QUALIFIED',observed=None,expected=None,evidence_refs=refs,scope_limit=limit))

# Freeze receipt only: do not rerun or add together prior check files.
oldqa=js('reports/numerical_qa_summary.json')
baseline=dict(assertions=oldqa['check_rows'],status_counts=oldqa['status_counts'],generated_at_utc=oldqa['generated_at_utc'])
assert baseline['assertions']==157 and baseline['status_counts']==dict(PASS=140,FAIL=0,QUALIFIED=17,PENDING=0)

# New public review rows and historically bounded interpretation tests.
old=cs('workstreams/reviews/reviews_derived.csv');new=cs('workstreams/extension_reviews/new_reviews_derived.csv')
rv=js('workstreams/extension_reviews/validation.json');ra=js('workstreams/extension_reviews/analysis_summary.json')
ko={r['record_key'] for r in old};kn={r['record_key'] for r in new}
ck('EXQ01','Reviews','New extension has148unique record keys',len(kn),148,'new_reviews_derived.csv','Selected listings; unique record keys do not identify unique people or verified incidents.')
ck('EXQ02','Reviews','No old/new review-key overlap',len(ko&kn),0,'reviews_derived.csv;new_reviews_derived.csv')
ck('EXQ03','Reviews','Combined public record keys210+148=358',len(ko|kn),358,'reviews_derived.csv;new_reviews_derived.csv')
ck('EXQ04','Reviews','New rows trace to9listing URLs and9capture requests',[len({r['source_url'] for r in new}),len({r['source_request_id'] for r in new})],[9,9],'new_reviews_derived.csv','Pages are not independent respondent samples.')
ck('EXQ05','Reviews','New status category counts reconcile',sum(rv['status_counts'].values()),len(new),'extension_reviews/validation.json')
ck('EXQ06','Reviews','All new ratings fall in1–5',all(1<=int(r['rating'])<=5 for r in new),True,'new_reviews_derived.csv')
ck('EXQ07','Reviews','AI source inspection148and no human/operational verification',[sum(r['source_inspected_by_ai']=='True' for r in new),sum(r['human_validation']=='True' for r in new),sum(r['independently_verified']=='True' for r in new)],[148,0,0],'new_reviews_derived.csv','AI classification is not a verified service outcome.')
digi=[r for r in old if r['app']=='digiroom'];before=[r for r in digi if r['review_date'][:10]<'2025-12-06'];after=[r for r in digi if r['review_date'][:10]>='2025-12-06']
ck('EXQ08','Review dates','First-wave Digiroom50records split37pre/13on-or-after relaunch',[len(digi),len(before),len(after)],[50,37,13],'reviews_derived.csv;ER_T04_digiroom_relaunch_date_context.csv','Review date does not establish installed build, exposure or causal relaunch effect.')
ck('EXQ09','Review dates','Six of13post-date Digiroom records self-report an app job',sum(r['experience_status']=='self_reported_app_job' for r in after),6,'reviews_derived.csv','No independently verified completion rate.')
ck('EXQ10','Review dates','Old corpus has87dated2026and71with a stated version',[sum(r['review_date'].startswith('2026') for r in old),sum(r['review_date'].startswith('2026') and bool(r['review_version']) for r in old)],[87,71],'reviews_derived.csv;extension_reviews/analysis_summary.json')
vc=collections.Counter(r['vehicle_context_reported'] for r in new)
ck('EXQ11','Review context','New vehicle-context labels112unspecified/30cars/6motorcycles',dict(vc),dict(vehicle_unspecified=112,car_explicit=30,motorcycle_explicit=6),'new_reviews_derived.csv','AI reading of explicit context; not verified owner identity.')
second=sum(r.get('second_ai_checked')=='True' for r in new)
qual('EXQ12','Review coding','Targeted second-AI inspections remain separate from human validation.','new_reviews_derived.csv',f'This frozen derivative marks{second}new rows second-AI checked. A separate targeted audit receipt may add checks without overwriting the original annotation table. Neither is random holdout reliability.')

# Geography: independent aggregates and recomputed ratios/ranks, not a rerun.
geo=js('workstreams/extension_geography/ROBUSTNESS_SUMMARY.json');qr=js('workstreams/extension_geography/QA_RECEIPT.json')
g=cs('workstreams/extension_geography/anchor_nearest_alternative_scenarios.csv');ss=cs('workstreams/extension_geography/nearest_scenario_summary.csv')
groups=collections.defaultdict(list)
for r in g:groups[(r['coordinate_scenario'],r['candidate_pool'])].append(r)
ck('EXQ13','Geography receipt','Reported local QA receipt contains32passing checks',[len(qr['checks']),sum(r['pass'] for r in qr['checks'])],[32,32],'extension_geography/QA_RECEIPT.json','Receipt consistency; not32independent source validations or population outcomes.')
ck('EXQ14','Geography grain','25coordinate/pool scenarios and695anchor-scenario rows',[len(groups),len(g),len(ss)],[25,695,25],'anchor_nearest_alternative_scenarios.csv;nearest_scenario_summary.csv','Repeated scenarios on the same28anchors; not695new facilities.')
allmatches=True
for row in ss:
 z=groups[(row['coordinate_scenario'],row['candidate_pool'])];ds=sorted(float(r['great_circle_lower_bound_km']) for r in z);n=len(ds);median=ds[n//2] if n%2 else (ds[n//2-1]+ds[n//2])/2
 allmatches &= n==int(row['anchor_n']) and abs(median-float(row['median_nearest_great_circle_km']))<1e-8
 for rad in [1,3,5]:allmatches &= sum(x<=rad for x in ds)==int(row[f'anchors_with_candidate_within_{rad}km'])
ck('EXQ15','Geography scenarios','All25scenario medians/counts independently match695rows',bool(allmatches),True,'anchor_nearest_alternative_scenarios.csv;nearest_scenario_summary.csv')
src={r['candidate_pool']:r for r in ss if r['coordinate_scenario']=='source_coordinates'}
cons=src['network_public_facing_venue_proxy']
ck('EXQ16','Candidate sensitivity','Source all-mapped versus conservative within1km20→8and5km27→26',[int(src['all_mapped']['anchors_with_candidate_within_1km']),int(cons['anchors_with_candidate_within_1km']),int(src['all_mapped']['anchors_with_candidate_within_5km']),int(cons['anchors_with_candidate_within_5km'])],[20,8,27,26],'nearest_scenario_summary.csv','Provider/venue proxy, not verified public access or route convenience.')
ck('EXQ17','Geography scope','All695scenario rows retain unverified access',all(r['access_verified']=='False' for r in g),True,'anchor_nearest_alternative_scenarios.csv')
bc=cs('workstreams/extension_geography/boundary_stock_conservation.csv')
pooled=[r for r in bc if r['boundary_scenario']=='pooled_historical_34_boundaries'];direct=next(r for r in bc if r['year']=='2025' and r['boundary_scenario']=='direct_34_code_join')
ck('EXQ18','Boundary conservation','All pooled boundary years conserve published national totals',all(float(r['national_source_passenger_stock'])==float(r['matched_34_province_stock']) and float(r['unmatched_stock'])==0 for r in pooled),True,'boundary_stock_conservation.csv')
ck('EXQ19','Boundary omission','2025directjoin omits70,800from20,907,972',float(direct['national_source_passenger_stock'])-float(direct['matched_34_province_stock']),70800.,'boundary_stock_conservation.csv')
ck('EXQ20','Boundary omission','National omission rounds0.339%',round(70800/20907972*100,3),.339,'boundary_stock_conservation.csv','Small national omission can still materially change local ratios/ranks.')
cells=cs('workstreams/extension_geography/stock_boundary_audit_cells.csv')
pc={k:sum(float(r['value_units']) for r in cells if r['year']=='2025' and r['historical_34_code']==k and r['value_units']) for k in ['91','94']}
ck('EXQ21','Papua denominators','Historical91and94pooled denominators41,685and111,637',[pc['91'],pc['94']],[41685.,111637.],'stock_boundary_audit_cells.csv','Published nonmissing cells pooled; missing earlier child cells do not imply zero cars.')
pr=cs('workstreams/extension_geography/province_ratio_scenarios.csv')
ck('EXQ22','Ratios','Every saved scenario ratio matches numerator/stock×100,000',all(abs(float(r['numerator_value'])/float(r['passenger_stock_denominator'])*100000-float(r['units_per_100000_passenger_vehicles']))<1e-7 for r in pr),True,'province_ratio_scenarios.csv','2026mapped numerator and earlier all-car register denominator; not BEV demand or capacity.')
gp=collections.defaultdict(list)
for r in pr:gp[(r['year_of_denominator'],r['boundary_scenario'],r['numerator_unit'])].append(r)
rankok=True
for z in gp.values():
 vals=[float(r['units_per_100000_passenger_vehicles']) for r in z]
 for r in z:
  # Source uses minimum rank for tied values.
  rank=1+sum(v>float(r['units_per_100000_passenger_vehicles']) for v in vals)
  rankok &= rank==float(r['descending_rank'])
ck('EXQ23','Province ranks','Ranks recompute from each matching ratio scenario',bool(rankok),True,'province_ratio_scenarios.csv')
pa={}
for r in pr:
 if r['year_of_denominator']=='2025' and r['numerator_unit']=='site_rows' and r['bps_province_code'] in ['91','94']:
  pa[(r['bps_province_code'],r['boundary_scenario'])]=(round(float(r['units_per_100000_passenger_vehicles']),2),int(float(r['descending_rank'])))
ck('EXQ24','Papua ranks','PapuaBarat site ratio/rank48.80/1→19.19/10',[pa[('91','direct_34_code_join')],pa[('91','pooled_historical_34_boundaries')]],[(48.80,1),(19.19,10)],'province_ratio_scenarios.csv')
ck('EXQ25','Papua ranks','Papua site rank9→19',[pa[('94','direct_34_code_join')][1],pa[('94','pooled_historical_34_boundaries')][1]],[9,19],'province_ratio_scenarios.csv')

# Extension journey finance and context-carry observations.
bf=cs('workstreams/extension_journeys/bev_finance_illustrations.csv');je=js('workstreams/extension_journeys/observations.json')['observations'];jo={r['observation_id']:r for r in je};jss=js('workstreams/extension_journeys/summary.json')
ck('EXQ26','BEV finance','Five conditional calculator rows share799mprice,20%baseDP159.8m',len(bf)==5 and all(int(r['listed_price_idr'])==799000000 and int(r['base_dp_idr'])==159800000 and int(r['dp_percent'])==20 for r in bf),True,'bev_finance_illustrations.csv','Illustrative calculator output, not lender approval or APR estimate.')
ck('EXQ27','BEV finance','All five remaining-payment counts equal tenor minus1',all(int(r['remaining_payments'])==int(r['tenor_months'])-1 for r in bf),True,'bev_finance_illustrations.csv','ADDM timing; baseDP is not total upfront cash.')
b60=next(r for r in bf if r['tenor_months']=='60')
ck('EXQ28','BEV finance','60month output247,187,147upfront/15,581,947monthly/59remaining',[int(b60['total_upfront_idr']),int(b60['monthly_idr']),int(b60['remaining_payments'])],[247187147,15581947,59],'XT02;bev_finance_illustrations.csv')
ck('EXQ29','Journey scope','Eight registered groups contain seven live groups and one untested mobile group',[len(je),sum(r['status']!='not_tested_unsupported' for r in je),sum(r['status']=='not_tested_unsupported' for r in je)],[8,7,1],'extension_journeys/observations.json','Scenario groups, not8independent participants.')
ck('EXQ30','Journey scope','No entered customer identifier and zero submitted leads/outcomes',all(not r['customer_identifiers_entered'] for r in je) and jss['bookings_or_leads_submitted']==0 and jss['observed_customer_outcomes']==0,True,'extension_journeys/observations.json;summary.json','Not a native/mobile or recruited-participant test.')
urls=cs('workstreams/extension_journeys/sources.csv');um={r['source_id']:r['url'] for r in urls}
ck('EXQ31','Handoff context','Two retained-context routes use distinct actual branch/model parameters',['bz4x?branchCode=T151' in um['XTS10'],'hiace?branchCode=T155' in um['XTS12'],'Juanda/bZ4X' in jo['XT08']['observation'],'Cempaka Putih/Hiace' in jo['XT08']['observation']],[True]*4,'XT08;XTS10;XTS12','Two inspected evaluator routes contradict universal loss; not a prevalence estimate or fulfilled reservation.')
se=cs('workstreams/extension_journeys/service_estimates_extension.csv')
ck('EXQ32','Retail estimates','22new program rows reconcile labor+parts tolisted amount',len(se)==22 and all(int(r['labor_estimate_idr'])+int(r['parts_estimate_idr'])==int(r['listed_total_idr']) for r in se),True,'service_estimates_extension.csv','March2024retail estimates, not current invoices or unit GP.')
bz=[r for r in se if 'BZ4X' in r['model'] and 8<=int(r['service_visit'])<=11]
ck('EXQ33','Retail estimates','bZ4X four later-event estimates sum9.101m',sum(int(r['listed_total_idr']) for r in bz),9101000,'XT04;service_estimates_extension.csv')
ag=next(r for r in se if r['model']=='Agya' and r['service_visit']=='2')
ck('EXQ34','Program payment','Agya event2has0displayed labor and564kparts',[int(ag['labor_estimate_idr']),int(ag['parts_estimate_idr'])],[0,564000],'XT04;service_estimates_extension.csv','Zero displayed fee is not zero work or personalized eligibility.')

# New symmetric bridge and constructed joint-risk claims.
ec=js('workstreams/extension_economics/portfolio_inputs_and_method.json')
ck('EXQ35','Symmetric bridge','Shapley scale and mix reconcile−6,025',ec['shapley_scale']+ec['shapley_mix'],-6025.,'portfolio_inputs_and_method.json','Symmetric accounting allocation, not causal attribution.')
ck('EXQ36','Symmetric bridge','Scale term equals total-change times average observed mix',(ec['total_2025']-ec['total_2024'])*(ec['mix_2024']+ec['mix_2025'])/2,ec['shapley_scale'],'portfolio_inputs_and_method.json')
ar=cs('workstreams/extension_economics/constructed_aggregate_risk.csv');worlds=sorted({r['world'] for r in ar})
mx={w:max(int(r['dealer_residual_after_aggregate']) for r in ar if r['world']==w) for w in worlds}
ck('EXQ37','Constructed tail','Constructed dispersed/synchronized peak retained obligations300m/700m',[mx[w] for w in worlds],[300000000,700000000],'constructed_aggregate_risk.csv','No probabilities, forecast, quote, approved policy or observed customer pool.')
qual('EXQ38','Retail-versus-GP','Model fee totals and free-program labels do not identify dealer gross profit.','XT04;EEprogramrecords','Models/variants are unmatched and estimates datedMarch2024; reimbursement, direct costs and displacement remain unmeasured.')

# Foreign mechanism record count and NIST sample scope, from frozen reviewed sources.
external=js('workstreams/extension_hypotheses/EXTERNAL_MECHANISM_EVIDENCE.json')
ck('EXQ39','External source grain','Seven distinct mechanism studies/instruments',len({r['id'] for r in external}),7,'EXTERNAL_MECHANISM_EVIDENCE.json','Not seven raw customer datasets or independent effect estimates.')
nist=next(r for r in external if 'TN.2328' in r['url'])
ck('EXQ40','NIST scope','TN2328record distinguishes1490individuals including490BEVowners',all(t in nist['design'].replace(',','') for t in ['1490','490']),True,'EXT-H-S04;independent methods review','Source-specific US survey.490is a subset, not an additional independent sample; instrument and other analyses remain separate.')

# Independently count actual MAT signal shapes, excluding clocks and epoch fields.
manifest=js('workstreams/extension_battery/SOURCE_FILE_MANIFEST.json');initial=js('workstreams/extension_battery/INITIAL_SIGNAL_AUDIT.json');ini={r['file']:r for r in initial};counted=[]
for m in manifest:
 p=R/'private_cache/extension_battery'/f"{m['folder']}_Raw.mat";inputs.add(p)
 if h5py.is_hdf5(p):
  with h5py.File(p,'r') as f:lens={k:int(np.prod(f['Raw'][k].shape)) for k in f['Raw']}
 else:
  obj=loadmat(p,squeeze_me=True,struct_as_record=False)['Raw'];lens={k:int(np.asarray(getattr(obj,k)).size) for k in obj._fieldnames};del obj
 n=sum(lens[k] for k in ['Curr','Volt','SoC','Temp']);counted.append(dict(file=p.name,actual_signal_values=n,signal_lengths=lens))
 ck('EXQ41-'+m['folder'],'Battery actual counts','ActualMATshapes match four-signal count',n,ini[p.name]['actual_signal_values'],'SOURCE_FILE_MANIFEST.json;INITIAL_SIGNAL_AUDIT.json','Curr/Volt/SoC/Temp scalars, excluding clocks/Epoch; not synchronized rows or independent physical measurements.')
 ck('EXQ42-'+m['folder'],'Battery raw integrity','Local source bytes and hash match published manifest',[p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()],[m['source_size'],m['source_sha256']],m['source_url'])
ck('EXQ43','Battery grain','Fivebundles total56,507,201nonclock signal values',[len(counted),sum(r['actual_signal_values'] for r in counted)],[5,56507201],'ActualMATshapes;SOURCE_FILE_MANIFEST.json','Purposeful subset from oneAudi e-tron/California; not Toyota/Indonesian owner sample.')
ck('EXQ44','Battery asynchronous grain','At least one bundle has different current andSoClengths',any(r['signal_lengths']['Curr']!=r['signal_lengths']['SoC'] for r in counted),True,'ActualMATshapes','Equal lengths would not itself prove clock alignment; row-wise joins require explicit timing rules.')
qual('EXQ45','Battery inference','Battery-capacity accuracy and resale-premium claims remain unidentified.','Battery source/initial audit;EXT-H-S03–04','Hidden capacity reference, proprietary source estimator, asynchronous clocks and source-side reduction prevent treating stored values as independent ground truth. Final derived battery outputs are a separate evidence layer.')

# Frozen second-AI receipt, recorded after the extension's first source inspection.
secondreceipt=js('workstreams/extension_reviews/SECOND_AI_CHECK_RECEIPT.json');new_by_id={r['evidence_id']:r for r in new}
ck('EXQ46','Second AI review','16targeted new records and matching source hashes',[second,len(secondreceipt['records']),sum(r['source_text_sha256']==new_by_id[r['evidence_id']]['source_text_sha256'] for r in secondreceipt['records'])],[16,16,16],'SECOND_AI_CHECK_RECEIPT.json;new_reviews_derived.csv','Targeted, nonblind, nonrandom; separate from earlier30checks on first-wave210.')
ck('EXQ47','Second AI review','Receipt preserves no human/reliability/outcome verification',[secondreceipt['human_validation'],secondreceipt['blinded_random_or_exhaustive_validation'],secondreceipt['reliability_or_accuracy_percentage_estimated'],secondreceipt['independent_customer_outcome_verification']],[False]*4,'SECOND_AI_CHECK_RECEIPT.json')

# Final battery aggregate outputs plus one direct raw integral recomputation.
bat=js('workstreams/extension_battery/BATTERY_SUMMARY.json');sc=cs('workstreams/extension_battery/scalar_count_receipt.csv');bi=cs('workstreams/extension_battery/gap_aware_signed_integrals.csv');seg=cs('workstreams/extension_battery/gap30_segment_metrics.csv');sl=cs('workstreams/extension_battery/charging_interval_soc_slope_diagnostics.csv')
ck('EXQ48','Battery counts','Independent shapes and final summary agree56507201signals',sum(r['actual_signal_values'] for r in counted),bat['physical_or_BMS_signal_scalar_values_excluding_clocks_epoch'],'ActualMATshapes;BATTERY_SUMMARY.json')
ck('EXQ49','Battery time metadata','Clock and Epoch values remain separate from signals',[sum(r['signal_lengths'][k] for r in counted for k in ['TimeCurr','TimeVolt','TimeSoC','TimeTemp','TimeEpoch']),sum(r['signal_lengths']['Epoch'] for r in counted)],[56599111,91910],'ActualMATshapes;scalar_count_receipt.csv')
ck('EXQ50','Battery bytes','Payload bytes283141466and maximum95036227',[sum(m['source_size'] for m in manifest),max(m['source_size'] for m in manifest)],[283141466,95036227],'SOURCE_FILE_MANIFEST.json')
ck('EXQ51','Battery segments','106algorithmic gap30segments agree with source clock-gap counts',[len(seg),sum(r['signals']['Curr']['gap_above_30s']+1 for r in initial)],[106,106],'gap30_segment_metrics.csv;INITIAL_SIGNAL_AUDIT.json','Declared >30s segmentation, not field-verified trips/sessions.')
ck('EXQ52','Battery integral identities','All20saved integral rows reconcile signed and absolute terms',len(bi)==20 and all(abs(float(r['positive_terminal_kWh'])-float(r['negative_magnitude_terminal_kWh'])-float(r['signed_terminal_kWh']))<1e-8 and abs(float(r['positive_terminal_kWh'])+float(r['negative_magnitude_terminal_kWh'])-float(r['absolute_terminal_kWh']))<1e-8 for r in bi),True,'gap_aware_signed_integrals.csv')
ck('EXQ53','Battery retained support','Gap1supported hours sum51.9736656864',sum(float(r['supported_seconds']) for r in bi if r['max_integrated_step_seconds']=='1')/3600,bat['observed_supported_hours_gap1'],'gap_aware_signed_integrals.csv','Retained interval time, not first-to-last calendar exposure or a representative year.')
ck('EXQ54','Battery charging slopes','Four partial charge intervals recompute Ah/SOC-point ratios',len(sl)==4 and all(abs(float(r['aligned_negative_magnitude_Ah'])/float(r['aligned_soc_change_percentage_points'])-float(r['observed_negative_Ah_per_reported_soc_percentage_point']))<1e-9 for r in sl),True,'charging_interval_soc_slope_diagnostics.csv','Partial slopes are not usable capacity, SOH or calibrated degradation estimates.')
ck('EXQ55','Battery charging slopes','Reported slope range1.570124to2.194808matches saved intervals',[min(float(r['observed_negative_Ah_per_reported_soc_percentage_point']) for r in sl),max(float(r['observed_negative_Ah_per_reported_soc_percentage_point']) for r in sl)],bat['observed_Ah_per_SOCpp_range'],'charging_interval_soc_slope_diagnostics.csv')
# Load only Folder2's independent current/voltage triplet; do not execute owner analysis.
fp=R/'private_cache/extension_battery/Folder2_Raw.mat'
with h5py.File(fp,'r') as f:
 tt=np.array(f['Raw']['TimeCurr']).ravel();ii=np.array(f['Raw']['Curr']).ravel();vv=np.array(f['Raw']['Volt']).ravel();tv=np.array(f['Raw']['TimeVolt']).ravel()
dt=np.diff(tt);pp=ii*vv
ck('EXQ56','Direct raw battery check','Folder2actual current and voltage clocks match',bool(np.array_equal(tt,tv)),True,'Folder2_Raw.mat','Does not establish SOC/temperature alignment.')
direct_int={}
for threshold in [1,None]:
 keep=(dt>0) if threshold is None else ((dt>0)&(dt<=threshold))
 absolute=float(np.sum((np.abs(pp[:-1])+np.abs(pp[1:]))*.5*dt*keep)/3600000)
 signed=float(np.sum((ii[:-1]+ii[1:])*.5*dt*keep)/3600)
 key='UNBOUNDED_NAIVE_COUNTEREXAMPLE' if threshold is None else '1';row=next(r for r in bi if r['folder']=='Folder2' and r['max_integrated_step_seconds']==key)
 direct_int[key]=absolute
 ck('EXQ57-'+key,'Direct raw battery check','Independent sampled trapezoid absolute terminal integral',absolute,float(row['absolute_terminal_kWh']),'Folder2_Raw.mat;gap_aware_signed_integrals.csv','Electrical sampled-signal integral, not wall electricity or capacity.',tol=1e-7)
 ck('EXQ58-'+key,'Direct raw battery check','Independent signed current integral inAh',signed,float(row['signed_Ah']),'Folder2_Raw.mat;gap_aware_signed_integrals.csv',tol=1e-7)
ck('EXQ59','Gap sensitivity','Naive Folder2absolute integral excess rounds47.52%',round((direct_int['UNBOUNDED_NAIVE_COUNTEREXAMPLE']/direct_int['1']-1)*100,2),47.52,'Direct raw recomputation','Illustrates unsupported bridging of unobserved gaps; not a measured production-BMS error.')
del tt,ii,vv,tv,dt,pp

failed=[r for r in checks if r['status']=='FAIL']
with (O/'EXTENDED_NUMERICAL_QA_checks.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader()
 for row in checks:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list,tuple)) else v for k,v in row.items()})
result=dict(generated_utc=datetime.now(timezone.utc).isoformat(),frozen_first_wave=baseline,extension_only_assertions=len(checks),extension_status_counts={s:sum(r['status']==s for r in checks) for s in ['PASS','FAIL','QUALIFIED']},combined_assertion_total_reported=False,reason_not_summing='No addition of local19economics or32geography receipts to this independent audit; repeated/proxy checks are not new observations.',checks=checks,battery_actual_shapes=counted,input_manifest=[dict(path=str(p.relative_to(R.parent)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(inputs)],source_mutations=False,new_network_requests=0,human_validation=False)
(O/'EXTENDED_NUMERICAL_QA.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','input_manifest','battery_actual_shapes']},indent=2))
for r in failed:print('FAIL',r['check_id'],r['observed'],r['expected'])
assert not failed,'Inspect extension QA failures; source data were not modified'
