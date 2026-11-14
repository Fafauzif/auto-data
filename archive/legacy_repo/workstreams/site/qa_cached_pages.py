from pathlib import Path
import sqlite3,json,csv,re,hashlib,urllib.parse,collections
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
c=sqlite3.connect('file:'+str(ROOT/'data/site_evidence.sqlite')+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
allrows=[dict(r) for r in c.execute('SELECT * FROM pages WHERE status=200 AND error="" ORDER BY family,url')]
groups=collections.defaultdict(list)
for r in allrows:groups[r['family']].append(r)
prior_sample=[]
if (OUT/'qa_records.csv').exists():
 with (OUT/'qa_records.csv').open(encoding='utf8',newline='') as f:prior_sample=[r['url'] for r in csv.DictReader(f)]
sample=[]
for i,(fam,rs) in enumerate(sorted(groups.items())):sample.append(rs[i%len(rs)])
extras=['/berita-dan-tips/aplikasi-auto2000-digiroom','/berita-dan-tips/biaya-balik-nama-bpkb-mobil','/berita-dan-tips/jangan-bingung-soal-patokan-interval-servis-berkala-mobil-toyota-anda','/berita-dan-tips/keuntungan-pakai-mobil-listrik-ulasan','/body-paint-service','/seputar-pertanyaan','/dealer-toyota/malang/auto2000malangsukun','/c/paketservistoyota','/mobil-baru-toyota/p/agya/kredit']
for needle in extras:
 r=next((r for r in allrows if urllib.parse.urlsplit(r['url']).path==needle),None)
 if r and r['url'] not in [r['url'] for r in sample]:sample.append(r)
for r in allrows:
 if len(sample)>=24:break
 if r['url'] not in [r['url'] for r in sample] and r['family'] in ('editorial','local_branch','service_utility'):sample.append(r)
if prior_sample:
 byurl={r['url']:r for r in allrows};sample=[byurl[u] for u in prior_sample if u in byurl]
t=sqlite3.connect('file:'+str(ROOT/'private_cache/transport.sqlite')+'?mode=ro',uri=True);t.row_factory=sqlite3.Row
q=[];details=[]
for i,r in enumerate(sample):
 req=t.execute('SELECT cache_key,final_url FROM requests WHERE id=?',(r['request_id'],)).fetchone()
 path=ROOT/'private_cache/http'/(req['cache_key']+'.bin') if req else None
 if not path or not path.exists():q.append({'qa_id':f'QA-{i+1:02}','url':r['url'],'family':r['family'],'cache_found':False});continue
 raw=path.read_bytes();soup=BeautifulSoup(raw,'lxml');raw_title=' '.join(soup.title.get_text(' ',strip=True).split()) if soup.title else ''
 canonical_tags=[n for n in soup.find_all('link') if 'canonical' in [x.lower() for x in n.get('rel',[])]]
 exactcanonical=canonical_tags[0].get('href','') if canonical_tags else ''
 main=soup.find('main') or soup.find('article') or soup.body or soup
 nested_main_count=len(main.find_all('main'));article_body=soup.select_one('#detailContentArticle .prose') or soup.select_one('#detailContentArticle');article_text=' '.join(article_body.get_text(' ',strip=True).split()) if article_body else '';article_numeric=bool(re.search(r'\bRp[.\s]*[\d.,]+',article_text,re.I));tag=main.name;mainclass=' '.join(main.get('class',[]));nested_nav_links=[];textpreview=' '.join(main.get_text(' ',strip=True).split())
 all_main_a=main.find_all('a',href=True)
 for a in all_main_a:
  par=a.parent
  while par is not None and par is not main:
   if par.name in ('nav','header','footer','script','style','noscript'):
    nested_nav_links.append(a);break
   par=par.parent
 contact_paths=0;contacts=[]
 for a in soup.find_all('a',href=True):
  p=urllib.parse.urlsplit(urllib.parse.urljoin(r['final_url'],a['href']))
  if p.hostname in ('wa.me','api.whatsapp.com','web.whatsapp.com') and re.search(r'\d{8,}',p.path):contact_paths+=1
 raw_h1=len(soup.find_all('h1'));forms=len(soup.find_all('form'));schema_scripts=soup.find_all('script',type='application/ld+json');invalid_schema=0
 for s in schema_scripts:
  try:json.loads(s.string or s.get_text())
  except:invalid_schema+=1
 for n in main.find_all(['script','style','nav','header','footer','noscript']):n.decompose()
 txt=' '.join(main.get_text(' ',strip=True).split());words=re.findall(r'\w+',txt.lower())
 body_price_matches=[m.group(1) for m in re.finditer(r'\bRp\.?\s*([\d]{1,3}(?:[.,]\d{3})+(?:[.,]\d{1,2})?|\d{4,})',txt,re.I)]
 decimals=[v for v in body_price_matches if re.search(r'[.,]\d{1,2}$',v)]
 soft404=any(s in txt.lower() for s in ['halaman tidak ditemukan','page not found','404 not found'])
 record={'qa_id':f'QA-{i+1:02}','url':r['url'],'family':r['family'],'cache_found':True,'request_id':r['request_id'],'raw_sha256':hashlib.sha256(raw).hexdigest(),'main_tag':tag,'main_class':mainclass,'nested_main_count':nested_main_count,'article_body_selector_found':bool(article_body),'article_body_words':len(re.findall(r'\w+',article_text)),'article_body_numeric_rupiah':article_numeric,'stored_main_words':r['main_words'],'recomputed_main_words':len(words),'word_count_matches':len(words)==r['main_words'],'raw_title_words':len(raw_title.split()),'stored_title_words':len(r['title'].split()),'title_20word_rule_matches':r['title']==' '.join(raw_title.split()[:20]),'canonical_exact_rel_count':len(canonical_tags),'canonical_exact_rel_matches':r['canonical']==exactcanonical,'h1_count_matches':r['h1_count']==raw_h1,'forms_count_matches':r['forms']==forms,'nested_removed_nav_links_marked_main':len(nested_nav_links),'contact_number_paths':contact_paths,'currency_decimal_matches':len(decimals),'status200_soft404_marker':soft404,'redirected':r['url']!=r['final_url'],'invalid_schema_scripts':invalid_schema,'text_preview_10words':' '.join(txt.split()[:10]),'ai_review_status':'AI inspection only; no human/browser test; purposive sample'}
 q.append(record)
 details.append({'qa_id':record['qa_id'],'url':r['url'],'nested_removed_nav_link_count':len(nested_nav_links),'main_link_count_before_cleanup':len(all_main_a),'main_link_count_after_cleanup':len(main.find_all('a',href=True)),'amounts_count':len(body_price_matches),'form_main_count':len(main.find_all('form')),'prompt_count':sum(txt.lower().count(x) for x in ['silakan','hubungi','whatsapp','test drive','promo']),'soft404_marker':soft404,'currency_decimal_strings':decimals[:5]})
fields=list(dict.fromkeys(k for r in q for k in r))
with (OUT/'qa_records.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(q)
(OUT/'qa_details.json').write_text(json.dumps(details,ensure_ascii=False,indent=2));(OUT/'qa_snapshot.json').write_text(json.dumps({'snapshot_success_pages':len(allrows),'snapshot_total_pages':c.execute('SELECT COUNT(*) FROM pages').fetchone()[0],'reviewed':len(q),'families':dict(collections.Counter(r['family'] for r in q)),'all_reviews_by':'AI','not_prevalence':'URL-topic/family-purposive snapshot; not sitewide prevalence'},indent=2))
print(json.dumps({'sample':len(q),'family_count':len(set(r['family'] for r in q)),'words_mismatch':sum(not r.get('word_count_matches',False) for r in q),'canonical_mismatch':sum(not r.get('canonical_exact_rel_matches',False) for r in q),'titles_over20raw':sum(r.get('raw_title_words',0)>20 for r in q),'nav_contaminated':sum(r.get('nested_removed_nav_links_marked_main',0)>0 for r in q),'contact_path_pages':sum(r.get('contact_number_paths',0)>0 for r in q),'decimal_pages':sum(r.get('currency_decimal_matches',0)>0 for r in q),'soft404_marker_pages':sum(r.get('status200_soft404_marker',False) for r in q)},indent=2))
for r in q:print(r['qa_id'],r['family'],r.get('main_tag'),r.get('stored_main_words'),r.get('text_preview_10words'),r.get('nested_removed_nav_links_marked_main'),r.get('contact_number_paths'))
