"""Independent AI cached-source QA, fixed v1 sample. Read-only DB and no network."""
import csv,sqlite3,json,re,hashlib,datetime,urllib.parse,collections
from pathlib import Path
from bs4 import BeautifulSoup
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
with (OUT/'qa_records.csv').open(encoding='utf8',newline='') as f:sample=list(csv.DictReader(f))
c=sqlite3.connect('file:'+str(ROOT/'data/site_evidence.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;c.execute('BEGIN')
t=sqlite3.connect('file:'+str(ROOT/'private_cache/transport.sqlite')+'?mode=ro',uri=True);t.row_factory=sqlite3.Row
rows=[]
for old in sample:
 r=c.execute('SELECT p.*,v.version,v.selector FROM pages p LEFT JOIN extraction_versions v ON v.url=p.url WHERE p.url=?',(old['url'],)).fetchone()
 if not r:continue
 tr=t.execute('SELECT * FROM requests WHERE id=?',(r['request_id'],)).fetchone();body=ROOT/'private_cache'/'http'/(tr['cache_key']+'.bin')
 raw=body.read_bytes();soup=BeautifulSoup(raw,'lxml')
 prose=soup.select_one('#detailContentArticle .prose')
 if prose is None and r['family'] in ('editorial','adviser_editorial'):prose=soup.select_one('.prose')
 if prose is not None:chosen=prose;expectedselector='editorial_prose'
 else:
  article=soup.find('article')
  if article is not None:chosen=article;expectedselector='article'
  else:
   mains=soup.find_all('main');chosen=mains[-1] if mains else (soup.body or soup);expectedselector='last_main_or_body'
 source_selector_tag=chosen.name;source_selector_id=chosen.get('id','');nested_main=len(chosen.find_all('main'));mobile_removed=len(chosen.select('#mobileNavList'))
 # Inspect source boundaries independently and calculate expected main-target set after omitted containers are removed.
 for item in list(chosen.select('#mobileNavList, [id^=emarsys], [id^=placeholder_emarsys]')):item.decompose()
 source_anchors=list(chosen.find_all('a',href=True));excluded_nav_anchors=sum(bool(a.find_parent(['nav','header','footer'])) for a in source_anchors)
 expectedtargets=set()
 for a in source_anchors:
  if a.find_parent(['nav','header','footer']):continue
  p=urllib.parse.urlsplit(urllib.parse.urljoin(r['final_url'],a['href']))
  if p.scheme not in ('http','https'):continue
  target=urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,'',''))
  if any(x in (p.hostname or '') for x in ['wa.me','whatsapp.com']):target='https://wa.me/CONTACT_REDACTED'
  expectedtargets.add(target)
 links=[dict(x) for x in c.execute('SELECT * FROM links WHERE page_url=?',(r['url'],))];actualtargets={x['target_url'] for x in links if x['in_main']}
 contact_leaks=sum(bool(re.search(r'https?://(?:[^/]*\.)?(?:wa\.me|whatsapp\.com)/[^\s]*\d{8,}',x['target_url'])) for x in links)
 for n in list(chosen.find_all(['script','style','nav','header','footer','noscript'])):n.decompose()
 text=' '.join(chosen.get_text(' ',strip=True).split());words=re.findall(r'\w+',text.lower());norm=re.sub(r'\b\d{6,}\b',' NUM ',text.lower());norm=re.sub(r'\s+',' ',norm)
 flags=json.loads(r['topic_flags']);rp=bool(re.search(r'\bRp[.\s]*[\d.,]+',text,re.I));referencecanonical=soup.find_all('link',rel=lambda x:x and 'canonical' in x)
 exact=[x for x in soup.find_all('link') if 'canonical' in [str(v).lower() for v in x.get('rel',[])]];can=exact[0].get('href','') if exact else ''
 # v2 computes global structural fields before cleanup; reconstruct on a separate soup.
 fresh=BeautifulSoup(raw,'lxml');h1=len(fresh.find_all('h1'));forms=len(fresh.find_all('form'));title=' '.join(fresh.title.get_text(' ',strip=True).split()[:20]) if fresh.title else ''
 rootarticle=fresh.select_one('#detailContentArticle .prose');articletext=' '.join(rootarticle.get_text(' ',strip=True).split()) if rootarticle else None
 numeric_outside_article=None
 if articletext is not None:
  numeric_outside_article=bool(re.search(r'\bRp[.\s]*[\d.,]+',(fresh.find_all('main')[-1] if fresh.find_all('main') else fresh).get_text(' ',strip=True),re.I)) and not bool(re.search(r'\bRp[.\s]*[\d.,]+',articletext,re.I))
 row={'qa_id':old['qa_id'],'url':r['url'],'family':r['family'],'extraction_version':r['version'],'stored_selector':r['selector'],'expected_selector':expectedselector,'selector_matches':r['selector']==expectedselector,'source_selector_tag':source_selector_tag,'source_selector_id':source_selector_id,'nested_main_within_selected':nested_main,'mobile_blocks_removed':mobile_removed,'nav_header_footer_source_anchors_excluded':excluded_nav_anchors,'stored_words':r['main_words'],'reference_words':len(words),'word_count_matches':r['main_words']==len(words),'content_hash_matches':r['main_hash']==hashlib.sha256(norm.encode()).hexdigest(),'main_link_target_set_matches':actualtargets==expectedtargets,'unexpected_main_link_targets':len(actualtargets-expectedtargets),'missing_main_link_targets':len(expectedtargets-actualtargets),'whatsapp_phone_paths_in_export':contact_leaks,'title_cap_matches':r['title']==title,'canonical_exact_rel_matches':r['canonical']==can,'h1_global_matches':r['h1_count']==h1,'forms_global_matches':r['forms']==forms,'rp_flag_matches_selected_content':flags.get('rupiah_numeric_mention')==rp,'numeric_outside_article_but_not_inside':numeric_outside_article,'zero_word_selected_content':not words,'capture_time_matches_transport':r['captured']==tr['started'],'request_id':r['request_id'],'source_sha256':hashlib.sha256(raw).hexdigest(),'content_preview_8words':' '.join(text.split()[:8]),'reviewer':'independent_AI_cached_source_inspection_no_human_or_browser'}
 rows.append(row)
c.rollback();c.close();t.close()
with (OUT/'v2_qa.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
checks=['selector_matches','word_count_matches','content_hash_matches','main_link_target_set_matches','title_cap_matches','canonical_exact_rel_matches','h1_global_matches','forms_global_matches','rp_flag_matches_selected_content','capture_time_matches_transport']
summary={'n_fixed_sample':len(rows),'families':dict(collections.Counter(r['family'] for r in rows)),'version_counts':dict(collections.Counter(r['extraction_version'] for r in rows)),'check_pass_counts':{k:sum(bool(r[k]) for r in rows) for k in checks},'contact_leak_pages':sum(r['whatsapp_phone_paths_in_export']>0 for r in rows),'article_page_numeric_outside_not_inside_n':sum(r['numeric_outside_article_but_not_inside'] is True for r in rows),'zero_word_selected_pages_n':sum(r['zero_word_selected_content'] for r in rows),'snapshot_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'new_network_requests':0,'human_validation':False,'scope':'fixed purposeful24 v1sources; notsiteprevalence'}
(OUT/'v2_qa_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
for r in rows:print(r['qa_id'],r['family'],r['stored_words'],r['stored_selector'],r['content_preview_8words'])
