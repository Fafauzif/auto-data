"""Prespecified descriptive follow-up. Source records stay distinct from derived cells."""
import csv,json,hashlib,datetime,collections,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
receipt=json.loads((OUT/'prespecification_receipt.json').read_text());base=ROOT/'workstreams/reviews/reviews_derived.csv'
assert hashlib.sha256(base.read_bytes()).hexdigest()==receipt['baseline_csv_sha256'],'Frozen first-wave input changed'
with base.open(encoding='utf8',newline='') as f:old=list(csv.DictReader(f))
newpath=OUT/'new_reviews_derived.csv'
new=list(csv.DictReader(newpath.open(encoding='utf8',newline=''))) if newpath.exists() else []
assert not ({r['record_key'] for r in old}&{r['record_key'] for r in new})
for r in old:r['wave']='original210'
for r in new:r['wave']='extension_new'
rows=old+new
statuses=['self_reported_app_job','branch_experience','product_review','prospective_no_job','unknown']
cohorts=collections.defaultdict(list)
for r in rows:cohorts[(r['wave'],r['app'],r['platform'],r['locale'])].append(r)
def export(name,data):
 if not data:return
 with (OUT/name).open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,list(data[0]));w.writeheader();w.writerows(data)
def year(r):return r.get('review_date','')[:4] if len(r.get('review_date',''))>=4 else 'unknown'
t01=[];t02=[];t04=[]
for key,group in sorted(cohorts.items()):
 wave,app,platform,locale=key;meta=dict(wave=wave,app=app,platform=platform,locale=locale,source_record_n=len(group))
 for ratinggroup,pred in [('stars1_3',lambda x:int(x['rating'])<=3),('stars4_5',lambda x:int(x['rating'])>=4)]:
  subset=[r for r in group if pred(r)];count=collections.Counter(r['experience_status'] for r in subset)
  for status in statuses:t01.append({**meta,'rating_group':ratinggroup,'rating_group_n':len(subset),'experience_status':status,'cell_n':count[status],'fraction_within_selected_rating_group':count[status]/len(subset) if subset else None,'unit':'derived_crosstab_cell_not_new_review','population_inference':False})
 for scope,subset in [('all_stars',group),('stars4_5',[r for r in group if int(r['rating'])>=4])]:
  n=len(subset);explicit=sum(r['experience_status']=='self_reported_app_job' for r in subset);unknown=sum(r['experience_status']=='unknown' for r in subset)
  t02.append({**meta,'subset':scope,'subset_n':n,'specific_reported_app_job_n':explicit,'unknown_n':unknown,'explicit_non_app_job_n':n-explicit-unknown,'classification_lower':explicit/n if n else None,'classification_upper':(explicit+unknown)/n if n else None,'bound_width':unknown/n if n else None,'bound_is_confidence_interval':False,'job_completion_estimated':False})
 for period,pred in [('through2024',lambda r:year(r).isdigit() and int(year(r))<=2024),('year2025',lambda r:year(r)=='2025'),('year2026',lambda r:year(r)=='2026'),('unknown_date',lambda r:year(r)=='unknown')]:
  subset=[r for r in group if pred(r)];known=sum(bool(r.get('review_version')) and r.get('review_version') not in ['None','null'] for r in subset)
  t04.append({**meta,'source_review_period':period,'period_n':len(subset),'review_version_present_n':known,'review_version_missing_n':len(subset)-known,'specific_reported_app_job_n':sum(r['experience_status']=='self_reported_app_job' for r in subset),'stars4_5_n':sum(int(r['rating'])>=4 for r in subset),'version_not_inferred_from_date':True})
export('ER_T01_rating_experience_crosstab.csv',t01);export('ER_T02_classification_sensitivity.csv',t02);export('ER_T04_date_version_strata.csv',t04)
# Pair displayed Google cohorts only when app/wave/storefront match and exactly id/en language rows exist.
t03=[]
for wave,app in sorted(set((r['wave'],r['app']) for r in rows)):
 groups={loc:cohorts.get((wave,app,'google_play',loc),[]) for loc in ['id_ID','en_ID']}
 if not all(groups.values()):continue
 a,b=groups['id_ID'],groups['en_ID'];ia={r['review_id'] for r in a};ib={r['review_id'] for r in b};entry={'wave':wave,'app':app,'same_country_parameter':'ID','id_language_n':len(a),'en_language_n':len(b),'shared_review_ids':len(ia&ib),'union_review_ids':len(ia|ib),'id_jaccard':len(ia&ib)/len(ia|ib)}
 for label,part in [('id',a),('en',b)]:
  entry[label+'_rating_counts']=json.dumps(dict(sorted(collections.Counter(r['rating'] for r in part).items())))
  entry[label+'_favorable_rating_n']=sum(int(r['rating'])>=4 for r in part);entry[label+'_source_year2026_n']=sum(year(r)=='2026' for r in part);entry[label+'_known_version_n']=sum(bool(r.get('review_version')) and r.get('review_version') not in ['None','null'] for r in part);entry[label+'_unknown_job_n']=sum(r['experience_status']=='unknown' for r in part)
 entry['rating_share_difference_en_minus_id_pp']=100*(entry['en_favorable_rating_n']/len(b)-entry['id_favorable_rating_n']/len(a));entry['is_causal_language_effect']=False;entry['is_country_satisfaction_comparison']=False;t03.append(entry)
export('ER_T03_original_locale_pair_sensitivity.csv',t03)
# Combined-wave paired source sensitivity; new EN mirrors can pair with existing ID cohort, marked as a wave-crossing comparison.
combined=[]
for app in sorted(set(r['app'] for r in rows)):
 a=[r for r in rows if r['app']==app and r['platform']=='google_play' and r['locale']=='id_ID'];b=[r for r in rows if r['app']==app and r['platform']=='google_play' and r['locale']=='en_ID']
 if not a or not b:continue
 combined.append({'app':app,'id_source_waves':'|'.join(sorted(set(r['wave'] for r in a))),'en_source_waves':'|'.join(sorted(set(r['wave'] for r in b))),'id_n':len(a),'en_n':len(b),'id_rating4_5_n':sum(int(r['rating'])>=4 for r in a),'en_rating4_5_n':sum(int(r['rating'])>=4 for r in b),'id_year2026_n':sum(year(r)=='2026' for r in a),'en_year2026_n':sum(year(r)=='2026' for r in b),'shared_ids':len({r['review_id'] for r in a}&{r['review_id'] for r in b}),'separate_selected_source_sets_no_population_rank':True})
export('ER_T06_combined_pair_context.csv',combined)
digi=[r for r in old if r['app']=='digiroom'];digiperiod=[]
for label,pred in [('before_2025_12_06',lambda r:r['review_date'][:10]<'2025-12-06'),('on_or_after_2025_12_06',lambda r:r['review_date'][:10]>='2025-12-06')]:
 part=[r for r in digi if pred(r)];digiperiod.append({'wave':'original210','app':'digiroom','period':label,'n':len(part),'known_source_version_n':sum(bool(r.get('review_version')) and r.get('review_version') not in ['None','null'] for r in part),'specific_reported_app_job_n':sum(r['experience_status']=='self_reported_app_job' for r in part),'stars4_5_n':sum(int(r['rating'])>=4 for r in part),'period_is_not_build_or_exposure_causality':True})
export('ER_T04_digiroom_relaunch_date_context.csv',digiperiod)
summary={'calculated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'plan_sha256':receipt['plan_sha256'],'original_rows':len(old),'new_rows':len(new),'combined_unique_review_ids':len(rows),'cohorts':len(cohorts),'original_status_counts':dict(collections.Counter(r['experience_status'] for r in old)),'new_status_counts':dict(collections.Counter(r['experience_status'] for r in new)),'original_review_date2026_n':sum(year(r)=='2026' for r in old),'original_date2026_and_known_version_n':sum(year(r)=='2026' and bool(r.get('review_version')) and r.get('review_version') not in ['None','null'] for r in old),'original_known_version_n':sum(bool(r.get('review_version')) and r.get('review_version') not in ['None','null'] for r in old),'no_population_pvalues_or_brand_rank':True,'verified_completed_app_jobs_n':0,'verified_completed_app_jobs_count_interpretation':'No operational completion measurement performed; not proof nobody completed jobs','human_validation':False,'rows_in_output_tables_are_derived_not_new_reviews':True}
(OUT/'analysis_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
