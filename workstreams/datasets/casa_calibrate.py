from pathlib import Path
import pandas as pd,numpy as np,json,hashlib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
from sklearn.pipeline import make_pipeline
from acquire import OUT,CACHE
splits={s:pd.read_csv(CACHE/f'indonlu_{s}.csv') for s in ['train','valid','test']}; aspects=[c for c in splits['train'].columns if c!='sentence'];labels=['negative','neutral','positive'];metrics=[];dist=[]
for s,x in splits.items():
 for a in aspects:
  for label,n in x[a].value_counts().items():dist.append({'split':s,'aspect':a,'label':label,'count':int(n),'n_reviews':len(x)})
train=splits['train'].copy(); train['normalized']=train.sentence.str.lower().str.split().str.join(' '); evaltexts=set(splits['valid'].sentence.str.lower().str.split().str.join(' '))|set(splits['test'].sentence.str.lower().str.split().str.join(' ')); train=train.drop_duplicates('normalized');train=train[~train.normalized.isin(evaltexts)]
for a in aspects:
 model=make_pipeline(TfidfVectorizer(ngram_range=(1,2),min_df=2,sublinear_tf=True),LogisticRegression(C=1,class_weight='balanced',max_iter=1500,random_state=29))
 model.fit(train.sentence,train[a])
 for s in ['valid','test']:
  y=splits[s][a]
  for name,pred in [('neutral_baseline',['neutral']*len(y)),('tfidf_logistic',model.predict(splits[s].sentence))]:
   metrics.append({'split':s,'aspect':a,'model':name,'accuracy':accuracy_score(y,pred),'macro_f1':f1_score(y,pred,labels=labels,average='macro',zero_division=0),'nonneutral_f1':f1_score(y,pred,labels=['negative','positive'],average='macro',zero_division=0),'n':len(y),'confusion_labels':labels,'confusion_matrix':confusion_matrix(y,pred,labels=labels).tolist()})
pd.DataFrame(dist).to_csv(OUT/'casa_label_distribution.csv',index=False)
pd.DataFrame([{k:v for k,v in x.items() if k not in ['confusion_matrix','confusion_labels']} for x in metrics]).to_csv(OUT/'casa_baseline_metrics.csv',index=False)
sets={s:set(' '.join(t.lower().split()) for t in x.sentence) for s,x in splits.items()}
summary={'dataset':'IndoNLU CASA','counts':{s:len(x) for s,x in splits.items()},'unique_normalized_texts':{s:len(v) for s,v in sets.items()},'train_valid_text_overlap':len(sets['train']&sets['valid']),'train_test_text_overlap':len(sets['train']&sets['test']),'valid_test_text_overlap':len(sets['valid']&sets['test']),'clean_train_count':len(train),'model_spec':'TFIDF word ngrams(1,2), min_df2, sublinear_tf; LogisticRegression C1 balanced max_iter1500 seed29; no test tuning; train cleaned only; exact normalized duplicates and heldout text overlaps excluded before fitting','metrics':metrics,'limitations':['Historical mixed vehicle product reviews, not Digiroom app outcomes','Test CSV has sentiment labels, despite general repo README masked-label statement; no hidden labels inferred','No current-domain manual review validation; do not deploy as causal/root-cause classifier','Neutral class dominates; accuracy alone is misleading','Original review text remains private due upstream provenance scope']}
(OUT/'casa_calibration.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k!='metrics'},indent=2));print(pd.DataFrame(metrics).query("split=='test'")[['aspect','model','accuracy','macro_f1','nonneutral_f1']].to_string(index=False))
