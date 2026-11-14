from acquire import OUT,CACHE
import pandas as pd,numpy as np,json,hashlib,collections
r=pd.read_csv(CACHE/'Rating_labeled.csv');v=pd.read_csv(CACHE/'VADER_labeled.csv')
keys=['app','content','score','at','appVersion','translation']
assert len(r)==617722 and len(v)==617722
# Match on six shared fields; no assumption that source row order is stable.
def keyseries(x):
 return x[keys].fillna('<NULL>').astype(str).apply(lambda z:hashlib.sha256(json.dumps(z.tolist(),ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),axis=1)
r['record_key']=keyseries(r);v['record_key']=keyseries(v)
rr=r.record_key.value_counts();vv=v.record_key.value_counts();shared=set(rr.index)&set(vv.index)
# Exact key collisions are duplicate source records; ordinal pairing within each group only.
r['duplicate_ordinal']=r.groupby('record_key').cumcount();v['duplicate_ordinal']=v.groupby('record_key').cumcount()
match=r.merge(v[['record_key','duplicate_ordinal','vader_neg','vader_neu','vader_pos','vader_compound','vader_label','vader_confidence']],on=['record_key','duplicate_ordinal'],how='left',validate='1:1',indicator=True)
assert (match._merge=='both').all()
match['rating_based_label']=match.labelScoreBase.str.lower();match['label_disagrees']=match.rating_based_label!=match.vader_label
match['source_scope']='AUXILIARY_NOT_AUTO2000';match['source_dataset_doi']='10.17632/7zryc6k76z.2';match['record_id']=[hashlib.sha256((k+':'+str(n)).encode()).hexdigest()[:24] for k,n in zip(match.record_key,match.duplicate_ordinal)]
match['review_month']=pd.to_datetime(match['at'],errors='coerce').dt.strftime('%Y-%m');match['content_chars']=match.content.fillna('').str.len();match['translation_missing']=match.translation.isna();match['content_missing']=match.content.isna();match['exact_source_duplicate']=match.record_key.map(rr)>1
features=match[['record_id','app','score','review_month','rating_based_label','vader_label','vader_compound','vader_confidence','label_disagrees','content_chars','content_missing','translation_missing','exact_source_duplicate','source_scope','source_dataset_doi']]
features.to_csv(OUT/'IGAR_AUXILIARY_nontext_features.csv.gz',index=False,compression={'method':'gzip','mtime':0})
pd.crosstab(match.rating_based_label,match.vader_label).to_csv(OUT/'igar_label_agreement_crosstab.csv')
byapp=match.groupby('app').agg(source_rows=('record_id','size'),disagreeing_labels=('label_disagrees','sum'),disagreement_share=('label_disagrees','mean'),missing_translation=('translation_missing','sum'),missing_content=('content_missing','sum'))
byapp.to_csv(OUT/'igar_label_agreement_by_app.csv')
summary={'scope':'AUXILIARY_NOT_AUTO2000','rating_view_rows':len(r),'vader_view_rows':len(v),'shared_composite_keys':len(shared),'unique_rating_composite_keys':r.record_key.nunique(),'unique_vader_composite_keys':v.record_key.nunique(),'matched_rows_including_duplicate_ordinals':len(match),'exact_duplicate_excess_rows_rating':int(len(r)-r.record_key.nunique()),'exact_duplicate_excess_rows_vader':int(len(v)-v.record_key.nunique()),'same_key_count_distributions_equal':rr.sort_index().equals(vv.sort_index()),'label_disagreement_rows':int(match.label_disagrees.sum()),'label_disagreement_share':float(match.label_disagrees.mean()),'missing_content':int(match.content.isna().sum()),'missing_translation':int(match.translation.isna().sum()),'source_date_min':str(pd.to_datetime(match['at'],errors='coerce').min()),'source_date_max':str(pd.to_datetime(match['at'],errors='coerce').max()),'release_feature_rows':len(features),'release_feature_columns':len(features.columns),'true_accuracies_not_measured':True,'ground_truth':'Neither rating-derived nor source VADER is human groundtruth','alignment_keys':keys,'pii_export':'No userhandles, rawtext, translation or exacttimestamp; pseudonymous content-based composite ID and month only','license':'CC BY4.0','citation':'Isnan, M., & Pardamean, B. (2025). IGAR: Indonesian Government App Review Dataset (V2). Mendeley Data. https://doi.org/10.17632/7zryc6k76z.2'}
(OUT/'igar_analysis_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print(byapp.to_string());print(pd.crosstab(match.rating_based_label,match.vader_label).to_string())
