from pathlib import Path
import json,csv
root=Path(__file__).resolve().parents[2]
out=Path(__file__).parent

def table(path):
 p=root/path
 if not p.exists():return []
 return list(csv.DictReader(p.open(encoding='utf-8')))
def typed(rows):
 result=[]
 for r in rows:
  row={}
  for k,v in r.items():
   if v is None or v=='':row[k]=None;continue
   try:
    if k.endswith(('_n','_rows','_ids','_reviews','_text','_level')) or k in ['rows','top_level','replies','channel_owner_rows','stars_1','stars_2','stars_3','stars_4','stars_5','unique_reviews','with_text','revenue_idr_billion','gross_profit_idr_billion']:v=int(v)
    elif any(x in k for x in ['_pct','_min','share_of_']):v=float(v)
   except ValueError:pass
   row[k]=v
  result.append(row)
 return result
metrics=json.loads((root/'analysis/social/corpus_metrics.json').read_text(encoding='utf-8'))
coverage=[]
for platform, m in metrics.items():
 coverage.append({'platform':platform,'source_rows':m['source_rows'],'unique_records':m['unique_ids'],'duplicate_excess_rows':m['duplicate_excess_rows'],'record_unit':'post' if platform=='x' else 'comment or reply' if platform=='youtube' else 'review','scope':'Query-selected public posts' if platform=='x' else 'Three selected videos' if platform=='youtube' else '37 selected places; retrieval cohorts retained'})
payload={
 'coverage':coverage,
 'case':typed(table('analysis/research/case_business_line_inputs.csv')),
 'markets':typed(table('analysis/geography/tables/market_portfolio.csv')),
 'branches':typed(table('analysis/geography/tables/branch_portfolio.csv')),
 'maps':typed(table('analysis/social/maps_branch_cohort_summary.csv')),
 'youtube':typed(table('analysis/social/youtube_video_summary.csv')),
}
insights=root/'data/insights.json'
if insights.exists():payload['insights']=json.loads(insights.read_text(encoding='utf-8'))
(out/'workbook_inputs.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2), encoding='utf-8')
print({k:len(v) for k,v in payload.items()})
