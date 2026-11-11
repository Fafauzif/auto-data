"""Independent v3 expected-source references; --compare-live checks root reparse read-only. No network."""
import csv,sqlite3,json,re,hashlib,urllib.parse,collections,datetime,argparse
from pathlib import Path
from bs4 import BeautifulSoup
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1]
a=argparse.ArgumentParser();a.add_argument('--compare-live',action='store_true');args=a.parse_args()
fixed=list(csv.DictReader((OUT/'v2_qa.csv').open(encoding='utf8',newline='')))
c=sqlite3.connect('file:'+str(ROOT/'data/site_evidence.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row;c.execute('BEGIN')
t=sqlite3.connect('file:'+str(ROOT/'private_cache/transport.sqlite')+'?mode=ro',uri=True);t.row_factory=sqlite3.Row
rows=[];comparisons=[]
for old in fixed:
 request=t.execute('SELECT * FROM requests WHERE id=?',(old['request_id'],)).fetchone();raw=(ROOT/'private_cache/http'/(request['cache_key']+'.bin')).read_bytes();soup=BeautifulSoup(raw,'lxml')
 title=' '.join(soup.title.get_text(' ',strip=True).split()[:20]) if soup.title else '';h1=len(soup.find_all('h1'));forms=len(soup.find_all('form'))
 cans=[x for x in soup.find_all('link') if 'canonical' in [str(a).lower() for a in x.get('rel',[])]];can=cans[0].get('href','') if cans else ''
 mainlist=soup.find_all('main');inner=mainlist[-1] if mainlist else (soup.body or soup)
 prose=soup.select_one('#detailContentArticle .prose')
 if prose is None and old['family'] in ('editorial','adviser_editorial'):prose=soup.select_one('.prose')
 chosen=prose if prose is not None else inner;selector='editorial_prose' if prose is not None else 'last_main_or_body'
 for n in list(chosen.select('#mobileNavList,[id^=emarsys],[id^=placeholder_emarsys]')):n.decompose()
 maintargets=set()
 for link in chosen.find_all('a',href=True):
  if link.find_parent(['nav','header','footer']):continue
  u=urllib.parse.urlsplit(urllib.parse.urljoin(request['final_url'],link['href']))
  if u.scheme not in ('https','http'):continue
  target=urllib.parse.urlunsplit((u.scheme,u.netloc,u.path,'',''))
  if any(x in (u.hostname or '') for x in ['wa.me','whatsapp.com']):target='https://wa.me/CONTACT_REDACTED'
  maintargets.add(target)
 for n in list(chosen.find_all(['script','style','nav','header','footer','noscript'])):n.decompose()
 text=' '.join(chosen.get_text(' ',strip=True).split());words=re.findall(r'\w+',text.lower());norm=re.sub(r'\b\d{6,}\b',' NUM ',text.lower());norm=re.sub(r'\s+',' ',norm);contenthash=hashlib.sha256(norm.encode()).hexdigest();rp=bool(re.search(r'\bRp[.\s]*[\d.,]+',text,re.I))
 row={'qa_id':old['qa_id'],'url':old['url'],'family':old['family'],'source_request_id':old['request_id'],'source_sha256':hashlib.sha256(raw).hexdigest(),'expected_selector_v3':selector,'expected_words_v3':len(words),'expected_hash_v3':contenthash,'expected_main_link_targets_n':len(maintargets),'expected_rp_mention':rp,'expected_canonical':can,'expected_h1_global':h1,'expected_forms_global':forms,'source_capture_epoch':request['started'],'v2_stored_words_snapshot':old['stored_words'],'restores_nonempty_vs_v2_snapshot':int(old['stored_words'])==0 and len(words)>0,'network_requests':0,'human_validation':False,'production_v3_verified':False};rows.append(row)
 if args.compare_live:
  current=c.execute('SELECT p.*,v.version,v.selector FROM pages p LEFT JOIN extraction_versions v ON v.url=p.url WHERE p.url=?',(old['url'],)).fetchone();actual={x[0] for x in c.execute('SELECT target_url FROM links WHERE page_url=? AND in_main=1',(old['url'],))}
  item={'qa_id':old['qa_id'],'url':old['url'],'published_version':current['version'],'version3':current['version']=='3.0','selector_matches':current['selector']==selector,'words_match':current['main_words']==len(words),'content_hash_matches':current['main_hash']==contenthash,'main_links_match':actual==maintargets,'rp_flag_matches':json.loads(current['topic_flags']).get('rupiah_numeric_mention')==rp,'canonical_matches':current['canonical']==can,'h1_matches':current['h1_count']==h1,'forms_match':current['forms']==forms,'title_cap_matches':current['title']==title,'capture_time_matches_original':current['captured']==request['started'],'source_request_id_matches':current['request_id']==old['request_id'],'source_sha256':row['source_sha256'],'AI_cached_source_check_no_human':True};comparisons.append(item)
c.rollback();c.close();t.close()
with (OUT/'v3_qa_reference.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,rows[0]);w.writeheader();w.writerows(rows)
summary={'fixed_sources':len(rows),'new_network_requests':0,'human_validation':False,'expected_zero_word_selections_v3':sum(x['expected_words_v3']==0 for x in rows),'restored_nonempty_vs_v2_n':sum(x['restores_nonempty_vs_v2_snapshot'] for x in rows),'reference_only':not args.compare_live,'production_v3_verified':False,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
if comparisons:
 fields=[k for k in comparisons[0] if k not in ['qa_id','url','published_version','source_sha256']];summary['published_comparison_pass_counts']={k:sum(x[k] for x in comparisons) for k in fields};summary['production_v3_verified']=all(all(x[k] for k in fields) for x in comparisons)
 with (OUT/'v3_qa_published_comparison.csv').open('w',encoding='utf8',newline='') as f:w=csv.DictWriter(f,comparisons[0]);w.writeheader();w.writerows(comparisons)
(OUT/'v3_qa_reference_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
