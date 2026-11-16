#!/usr/bin/env python3
"""Check source-resolving analytical and continuation invariants. Offline/stdlib."""
from pathlib import Path
import json,csv,hashlib,sys
R=Path(__file__).resolve().parents[1]
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
def js(p):return json.loads((R/p).read_text(encoding='utf-8'))
def jl(p):return [json.loads(l) for l in (R/p).read_text(encoding='utf-8').splitlines() if l]
def main():
 checks=[]
 def check(name,condition):
  if not condition:raise AssertionError(name)
  checks.append(name)
 metrics=js('analysis/social/corpus_metrics.json')
 check('social distinct record and raw-row totals reconcile',sum(v['unique_ids'] for v in metrics.values())==22484 and sum(v['source_rows'] for v in metrics.values())==23351)
 for plat,n in [('x',14291),('maps',8119),('youtube',74)]:
  rows=jl('analysis/social/cleaned/'+plat+'.jsonl')
  check(plat+' primary key uniqueness and complete-body preservation',len(rows)==n and len({r['record_id'] for r in rows})==n and all('text_original' in r for r in rows))
 check('Maps collection design retained',metrics['maps']['diagnostic_and_non_diagnostic_overlap_ids']==266 and metrics['maps']['places']==37)
 check('YouTube actual video/comment hierarchy reconciles',len(metrics['youtube']['videos'])==3 and sum(r['top_level'] for r in metrics['youtube']['videos'])==56 and sum(r['replies'] for r in metrics['youtube']['videos'])==18)
 maps=js('analysis/social/maps_deep/curated_maps_evidence.json');mp={r['evidence_id']:r for r in maps}
 check('Maps curated evidence mapping corrections retained',len(mp)==34 and mp['M19']['branch']=='Auto2000 Kertajaya' and mp['M21']['review_id']=='ChZDSUhNMG9nS0VJQ0FnSURqbDhDVU1REAE')
 geo=js('analysis/geography/tables/raw_independent_audit.json')
 check('raw geography paired-key audit passed',geo['pass'] and geo['errors_n']==0 and geo['branch_checks']==290 and geo['paired_strict_origins']==284 and geo['raw_unique_outbound_pair_keys']==82296)
 with (R/'analysis/geography/tables/market_portfolio.csv').open(encoding='utf-8',newline='') as f:g=list(csv.DictReader(f))
 check('current geography portfolio totals and concentration reconcile',sum(int(x['oil_tail_before_owned_network_n']) for x in g)==39 and sum(int(x['oil_tail_after_owned_network_n']) for x in g)==20 and next(x for x in g if x['market']=='Bandung')['oil_tail_after_owned_network_n']=='14')
 legacy=jl('analysis/research/legacy_evidence_union.jsonl');index={r['integrated_id']:r for r in legacy}
 check('legacy analytical register IDs namespaced and unique',len(index)==319)
 crosswalk=js('analysis/research/master_report_reference_crosswalk.json')
 for group in crosswalk:
  for row in group['union_records']:
   original=R/'archive/legacy_repo'/row['source_path_in_legacy_repository'];b=original.read_bytes()
   check('reference '+group['report_reference_id']+' resolves '+row['integrated_id'],row['integrated_id'] in index and hashlib.sha256(b).hexdigest()==row['source_file_sha256'])
 catalogue={r['evidence_ref']:r for r in js('data/evidence_catalogue.json')}
 for ref,row in catalogue.items():check('evidence locator paths exist '+ref,all((R/p).is_file() for p in row['paths']))
 for item in js('data/insights.json'):check('insight '+item['insight_id']+' resolves its evidence',all(x in catalogue for x in item['evidence_refs']))
 faq=js('context/CONTINUATION_FAQ.json')
 check('continuation context questions resolve evidence and authority',len(faq)>=24 and all(all((R/p).is_file() for p in row['paths']) for row in faq) and js('context/SESSION_DECISIONS.json')['private_repository'])
 case=R/'sources/case/Semifinal_Casebook_IBSC_2026.pdf'
 check('original casebook hash retained',hashlib.sha256(case.read_bytes()).hexdigest()=='237a96926c9da3ca8ffc5b4a311dbf41a9e12f6177a65b42e35d1e9a06df72dd')
 check('case arithmetic and prior research checks passed',all(x['pass'] for x in js('analysis/research/integration_research_checks.json')['checks']))
 insight_ids={item['insight_id'] for item in js('data/insights.json')}
 check('ten baseline insights, interview pilot insight and current mandate retained',{f'I{index:02}' for index in range(1,12)}<=insight_ids and all((R/p).is_file() for p in ['AGENTS.md','PROJECT_CONTEXT.md','reports/INTEGRATED_REPORT.md']))
 print(json.dumps({'passed':True,'checks_n':len(checks),'checks':checks},indent=2))
if __name__=='__main__':main()
