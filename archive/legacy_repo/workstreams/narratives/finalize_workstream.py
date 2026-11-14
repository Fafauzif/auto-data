from pathlib import Path
import json,csv,collections,hashlib
P=Path(__file__).parent
load=lambda f:[json.loads(x) for x in (P/f).read_text().splitlines() if x]
sources=load('sources.jsonl')+load('validation_sources.jsonl'); units=load('narrative_units.jsonl')+load('validation_units.jsonl')
ids={s['source_id'] for s in sources}
assert len(ids)==len(sources)
assert len({u['record_id'] for u in units})==len(units)
assert all(u['source_id'] in ids for u in units)
assert all(u['source_url']==next(s['url'] for s in sources if s['source_id']==u['source_id']) for u in units)
bib=['# Source bibliography','', 'URLs identify public source documents, not verified customer identities. Source dates and access limitations are retained below. Multiple annotations from one document are dependent.','']
for s in sources:
 bib += [f"## {s['source_id']}: {s['title']}",'',s['url'],'',f"Content date: {s['content_date']}. Retrieval: {s['retrieval_method']}. Accessed 11 November 2026.",'',s['limitations'],'']
(P/'BIBLIOGRAPHY.md').write_text('\n'.join(bib))
metrics={'source_documents':len(sources),'unique_source_urls':len({s['url'] for s in sources}),'discovery_annotation_units':75,'fresh_followup_annotation_units':20,'total_annotation_units':len(units),'evidence_kind_counts':dict(collections.Counter(u['evidence_kind'] for u in units)),'not_counts_of':'independent customers, completed transactions, verified incidents or causal effects','qa':{'source_joins_valid':True,'ids_unique':True,'all_units_have_normal_source_urls':True,'human_validation':False,'newly_scraped_social_records':0,'transcript_captures':0}}
(P/'combined_metrics.json').write_text(json.dumps(metrics,indent=2))
# CSV definitions: these codes were assigned semantically, not by keyword sentiment.
defs={'booking':'requesting or scheduling service, distinct from a confirmed or completed job','history':'retrieving, reconciling or retaining service records/receipts','warranty':'coverage question, claim or process without adopting eligibility assertions','price':'price/quote/cost concern without validating forum numbers','entitlement':'what a service benefit or offer includes/excludes','eligibility':'model/date/ownership/context conditions for an offer or claim','adviser':'reported interaction with a salesperson or service adviser','charging':'charging fit, access or reported charging experience; no technical verification','fit':'suitability for a stated task, household, trip or preference','counterevidence':'account that limits a broad negative or preferred explanation','misinformation_risk':'unresolved diagnosis, issuer or technical assertion, not a determination of misinformation','local_variation':'reported difference between locations, dealer groups or staff','parts':'availability, price or replacement of a component; technical cause unverified','trust':'uncertainty about source credibility, promise or treatment','workaround':'reported alternative action to achieve the task','response':'time or quality of contact/reply, without verified logs','household':'more than one family actor influences stated choice','used':'used-car purchase/condition context','resale':'stated relevance of future sale/value, not measured premium','time':'reported waiting or time tradeoff; not independently measured','geography':'location/distance constrains the task','knowledge':'request for, or perceived adequacy of, explanation','escalation':'moving a request to another party or public channel','diagnosis':'finding/explaining a vehicle issue; forum guesses not adopted'}
allcodes=sorted({c for u in units for c in u['aspect_codes']})
with (P/'codebook.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['code','definition','method']);w.writerows((c,defs.get(c,'Manual contextual tag: '+c.replace('_',' ')+'. Interpret only with the linked narrative.'),'single_AI_semantic_source_inspection') for c in allcodes)
print(json.dumps(metrics,indent=2))
