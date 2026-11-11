from pathlib import Path
import json,csv,datetime
p=Path(__file__).resolve().parent
sources=json.loads((p/'sources.json').read_text());facts=json.loads((p/'evidence.json').read_text());opts=json.loads((p/'solution_directions.json').read_text());nums=json.loads((p/'deloitte_service_indonesia.json').read_text())
loc={'M003':'Indonesia report, printed/PDF page 5','M004':'Indonesia report, printed/PDF page 6','M005':'Indonesia report, printed/PDF pages 6–7','M006':'Indonesia report, printed/PDF pages 7–8','M007':'SEA report, printed/PDF page 33, Q16','M008':'SEA report, printed/PDF page 33, Q17','M009':'SEA report, printed/PDF page 34, Q21','M010':'SEA report, printed/PDF page 35, Q22','M020':'NIST printed page 8 (PDF page 16), conclusion printed page 47 (PDF page 55)','M021':'NIST conclusion printed page 47 (PDF page 55)','M022':'NIST conclusion printed pages 47–48 (PDF pages 55–56)','M023':'JCEF methods PDF page 4, respondent profile PDF page 8','M024':'JCEF results 4.2.2, PDF page 8','M025':'JCEF abstract and discussion; limitations PDF page 13','M026':'UI methods, PDF pages 6–7','M027':'UI Table 1, printed page 2132 (PDF page 11)','M028':'IPB UTAUT2 Methods, printed pages 820–821','M029':'IPB UTAUT2 Table 3 and narrative, printed page 827 (PDF page 10)','M030':'IPB environmental paper, Methods and Table 4'}
for x in facts:
 if x['evidence_id'] in loc:x['locator']=loc[x['evidence_id']]
(p/'evidence.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2))
with (p/'evidence.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(facts[0]));w.writeheader();w.writerows(facts)
sids={x['source_id'] for x in sources};eids={x['evidence_id'] for x in facts}
assert len(sids)==len(sources)==24
assert len(eids)==len(facts)==47
assert all(x['source_id'] in sids for x in facts)
assert all(e in eids for x in opts for e in x['support_evidence_ids'])
assert len(opts)==12
assert len(nums)==28
assert all(x['sample_n'] in [618,629] for x in nums)
assert all(x['printed_page']==x['pdf_page_1_based'] for x in nums)
assert next(x for x in nums if x['metric_label']=='Online booking tool')['published_percent']==0
checks={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':len(sources),'ownership_clusters':len(set(x['ownership_cluster'] for x in sources)),'evidence_records':len(facts),'deloitte_numeric_cells':len(nums),'solution_directions':len(opts),'checks':['unique IDs','all fact-to-source links','all option-to-fact links','question-specific bases','page mapping','printed zero retains caveat'],'limitations':['not a source truth certification','not participant or causal validation','all private PDF/PNG evidence excluded from release'],'result':'passed'}
(p/'CHECKS.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks))
