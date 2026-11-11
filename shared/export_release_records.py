"""Export non-text capture records and a reconstructed pending queue, offline."""
from pathlib import Path
import csv, json, sqlite3, hashlib, datetime, urllib.parse, re, collections
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'
def clean_url(url):
    p=urllib.parse.urlsplit(url)
    query=urllib.parse.parse_qsl(p.query,keep_blank_values=True)
    secret=re.compile(r'token|secret|password|session|cookie|signature|credential|auth',re.I)
    query=[(k,'REDACTED' if secret.search(k) else v) for k,v in query]
    host=p.netloc.rsplit('@',1)[-1]
    return urllib.parse.urlunsplit((p.scheme,host,p.path,urllib.parse.urlencode(query),''))
def write_csv(path,rows,fields):
    with path.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
transport=sqlite3.connect(f'file:{ROOT}/private_cache/transport.sqlite?mode=ro',uri=True)
transport.row_factory=sqlite3.Row
captures=[]
for row in transport.execute('SELECT * FROM requests ORDER BY started,id'):
    r=dict(row);body=ROOT/'private_cache/http'/(r['cache_key']+'.bin')
    captures.append({'request_id':r['id'],'requested_url':clean_url(r['url']),
      'final_url':clean_url(r['final_url']),'domain':r['domain'],'method':r['method'],
      'http_status':r['status'],'started_utc':datetime.datetime.fromtimestamp(r['started'],datetime.timezone.utc).isoformat(),
      'elapsed_seconds':r['elapsed'],'response_bytes':r['bytes'],
      'transport_error_present':bool(r['error']),
      'cached_body_sha256':hashlib.sha256(body.read_bytes()).hexdigest() if body.exists() else '',
      'body_redistributed':False})
transport.close()
write_csv(OUT/'public_http_capture_index.csv',captures,list(captures[0]))

# Load exactly the two pure selection functions, without importing the HTML
# parser or transport. This keeps this offline export standard-library only.
import ast
tree=ast.parse((ROOT/'shared/site_collect_v3.py').read_text())
nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('family','allowed')]
assert len(nodes)==2
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(ROOT/'shared/site_collect_v3.py'),'exec'))
rules=json.loads((OUT/'robots_scope.json').read_text())['rules']
with (OUT/'sitemap_urls.csv').open(encoding='utf8',newline='') as f:inventory=list(csv.DictReader(f))
urls=list(dict.fromkeys(x['declared_url'] for x in inventory))
terms=r'hybrid|listrik|baterai|servis|service|garansi|biaya|kredit|cicilan|tukar|body|bodi|cat|spare|suku|bengkel|charging|spklu|test.drive|innova|zenix|yariscross|bz4x|veloz|urban.cruiser|fleet'
groups=collections.defaultdict(list);other=[]
for u in urls:
    if allowed(u,rules):
        if re.search(terms,u,re.I):groups[family(u)].append(u)
        else:other.append(u)
for key in groups:
    groups[key].sort(key=lambda u:(-sum(t in u.lower() for t in ['2026','2025','hybrid','listrik','garansi','baterai','biaya']),u))
chosen=[]
while any(groups.values()):
    for key in sorted(groups):
        if groups[key]:chosen.append((groups[key].pop(0),'topic_targeted_family_round_robin'))
chosen += [(u,'non_topic_family_coverage') for u in other]
extras=['https://auto2000.co.id/','https://auto2000.co.id/seputar-pertanyaan','https://auto2000.co.id/body-paint-service','https://auto2000.co.id/berita-dan-tips/aplikasi-auto2000-digiroom']
chosen=[(u,'purpose_selected_core') for u in extras if allowed(u,rules)]+chosen
chosen=list(dict((u,(u,s)) for u,s in chosen).values())
c=sqlite3.connect(f'file:{ROOT}/data/site_evidence.sqlite?mode=ro',uri=True)
observed={u:{'status':st,'error':er} for u,st,er in c.execute('SELECT url,status,error FROM pages')};c.close()
done={u for u,r in observed.items() if r['status'] in (200,404,410) and not r['error']}
remaining=[(u,s) for u,s in chosen if u not in done][:max(0,1200-len(done))]
pending=[{'resume_order':n,'url':u,'family':family(u),'selection':s,
          'prior_status':observed.get(u,{}).get('status',''),
          'queue_state':'retry_transport_or_temporary_status' if u in observed else 'not_requested'}
          for n,(u,s) in enumerate(remaining,1)]
write_csv(OUT/'site_pending_queue.csv',pending,['resume_order','url','family','selection','prior_status','queue_state'])
summary={'offline_generated':True,'http_calls':0,'requested_url_records':len(observed),
  'completed_status_policy':[200,404,410],'completed_without_error':len(done),
  'limit_including_completed':1200,'pending_reconstructed':len(pending),
  'inventory_unique_urls':len(urls),'capture_index_rows':len(captures),
  'capture_rows_are_requests_not_unique_sources':True,
  'queue_note':'Reconstructed deterministically after interruption from v3 selection, saved robots rules and final status records. Not a claim that pending URLs were fetched. Recheck source rules before future network work.'}
(OUT/'release_capture_and_queue_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
