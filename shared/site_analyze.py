from pathlib import Path
import sqlite3,json,csv,collections,math
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'workstreams'/'site';out.mkdir(parents=True,exist_ok=True)
c=sqlite3.connect(ROOT/'data/site_evidence.sqlite');c.row_factory=sqlite3.Row
rows=[dict(x) for x in c.execute('select * from pages')];good=[r for r in rows if r['status']==200 and not r['error']]
def export(name,records):
 if not records:return
 with (out/name).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
export('page_observations.csv',rows)
fams=collections.Counter(r['family'] for r in good)
summary={'fetched_urls':len(rows),'successful_raw_html':len(good),'status_counts':dict(collections.Counter(r['status'] for r in rows)),'families':dict(fams),'raw_bytes':sum(r['bytes'] for r in rows),'main_text_words_extracted_private':sum(r['main_words'] for r in good),'raw_missing_canonical':sum(not r['canonical'] for r in good),'missing_h1':sum(r['h1_count']==0 for r in good),'multiple_h1':sum(r['h1_count']>1 for r in good),'unique_main_content_hashes':len(set(r['main_hash'] for r in good)),'link_rows':c.execute('select count(*) from links').fetchone()[0],'link_occurrences':c.execute('select sum(occurrences) from links').fetchone()[0],'raw_amount_mentions_not_offers':c.execute('select count(*) from amounts').fetchone()[0],'limits':['Purposive URL and family selection; percentages apply only to successful sampled HTML','Raw HTML metadata not rendered/indexing/visitor evidence','Main text extraction may retain template content','Currency mentions are not reconciled offers or quoted current prices','Word and link counts do not measure independent information or people']}
(out/'summary.json').write_text(json.dumps(summary,indent=2))
# Exact duplicate extracted-content families
buckets=collections.defaultdict(list)
for r in good:
 if r['main_words']>0:buckets[r['main_hash']].append(r)
dup=[]
for h,group in buckets.items():
 if len(group)>1:
  for r in group:dup.append({'content_hash':h,'group_size':len(group),'family':r['family'],'url':r['url'],'main_words':r['main_words']})
export('exact_content_groups.csv',dup)
# Approximate candidate pairs via SimHash banding, restricted family
bands=collections.defaultdict(list);pairs=set();near=[]
for r in good:
 if r['main_words']<80 or not r['simhash']:continue
 n=int(r['simhash'],16)
 for band in range(4):
  key=(r['family'],band,(n>>(16*band))&65535)
  for other in bands[key]:
   pair=tuple(sorted([r['url'],other['url']]))
   if pair in pairs:continue
   pairs.add(pair);dist=(n^int(other['simhash'],16)).bit_count()
   if dist<=3 and r['main_hash']!=other['main_hash']:near.append({'url_a':pair[0],'url_b':pair[1],'family':r['family'],'hamming_distance':dist,'status':'similarity_candidate_requires_manual_comparison'})
  bands[key].append(r)
export('near_content_candidates.csv',near)
# Currency-bearing page evidence is a lead, not evidence a guide supports a decision
checks=[]
for r in good:
 flags=json.loads(r['topic_flags'] or '{}')
 if r['family'] in ('editorial','adviser_editorial'):
  checks.append({'url':r['url'],'family':r['family'],'title':r['title'],'main_words':r['main_words'],'mentions_hybrid':flags.get('hybrid',False),'mentions_rupiah_numeric':flags.get('rupiah_numeric_mention',False),'title_promises_cost_or_price':any(x in r['title'].lower() for x in ['biaya','harga','cost']),'interpretation':'scope_and_numeric_mentions_only_not_content_quality_score'})
export('editorial_context_checks.csv',checks)
export('source_family_counts.csv',[{'family':k,'successful_pages':v} for k,v in sorted(fams.items())])
summary['empty_selected_raw_text_pages']=sum(r['main_words']==0 for r in good);summary['exact_duplicate_groups']=sum(len(v)>1 for v in buckets.values());summary['near_duplicate_candidate_pairs']=len(near);(out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
