from pathlib import Path
import json,csv
out=Path(__file__).resolve().parent
v=json.loads((out/'direct_verification.json').read_text()); byid={r['source_id']:r for r in v if r.get('source_id')}
rows=json.loads((out/'evidence_matrix.json').read_text())
for r in rows:
 x=byid.get(r['source_id'],{})
 r.update(raw_http_status=x.get('status'),raw_request_id=x.get('request_id'),raw_final_url=x.get('final_url'),raw_body_sha256=x.get('body_sha256'),raw_text_word_count=x.get('visible_text_words'),raw_verification_note=('HTTP 200 is transport success only, not rendered functionality' if x.get('status')==200 else x.get('reason',x.get('method','unavailable'))))
with (out/'evidence_matrix.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'evidence_matrix.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
summary=json.loads((out/'summary.json').read_text());summary.update(core_ecosystems=11,provisional_ecosystems=['MG'],raw_source_fetches=sum(x.get('method')=='raw_http' for x in v),raw_source_http_200=sum(x.get('method')=='raw_http' and x.get('status')==200 for x in v),raw_shell_or_empty=sum(x.get('method')=='raw_http' and x.get('status')==200 and x.get('visible_text_words',0)==0 for x in v),source_url_catalog_entries=len(json.loads((out/'sources.json').read_text())),direct_method='robots reviewed per host; selected domain queues stopped on robots403/503; successful raw source bodies private cache')
(out/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
