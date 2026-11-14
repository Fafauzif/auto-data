#!/usr/bin/env python3
"""Rebuild the current social, geography and research calculations offline.

Reads source aliases from the inventory and writes isolated results under
.restored/rerun by default. Immutable originals and final reports are not edited.
Python3.10+ standard library only; no network or paid actor access.
"""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')

def read_json(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def safe(path):
 p=(ROOT/path).resolve()
 if not p.is_relative_to(ROOT):raise ValueError('Path outside release')
 return p
def materialize(prefix, dest):
 rows=[json.loads(l) for l in (ROOT/'manifests/source_inventory.jsonl').read_text(encoding='utf-8').splitlines() if l]
 count=0
 for r in rows:
  logical=r['logical_path']
  if not (logical==prefix or logical.startswith(prefix.rstrip('/')+'/')):continue
  target=(dest/logical).resolve()
  if not target.is_relative_to(dest.resolve()):raise ValueError('Unsafe logical source path')
  if target.exists() and target.stat().st_size==r['size_bytes'] and digest(target)==r['sha256']:
   count+=1;continue
  target.parent.mkdir(parents=True,exist_ok=True);tmp=target.with_name(target.name+'.partial')
  paths=[r['storage']['path']] if r['storage']['kind']=='file' else [x['path'] for x in r['storage']['parts']]
  try:
   with tmp.open('wb') as out:
    for path in paths:
     with safe(path).open('rb') as src:shutil.copyfileobj(src,out,8*1024*1024)
   if tmp.stat().st_size!=r['size_bytes'] or digest(tmp)!=r['sha256']:raise ValueError('Materialized source hash mismatch: '+logical)
   tmp.replace(target);count+=1
  finally:
   if tmp.exists():tmp.unlink()
 if not count:raise ValueError('No indexed source for '+prefix)
 return dest/prefix,count

def run(script,*args):
 p=subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True,encoding='utf-8',errors='replace')
 if p.returncode:raise RuntimeError(p.stdout+'\n'+p.stderr)
 return {'script':str(script.relative_to(ROOT)) if script.is_relative_to(ROOT) else script.name,'returncode':p.returncode,'stdout_tail':p.stdout[-1800:]}
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--only',choices=['all','social','geography','research'],default='all')
 ap.add_argument('--output-dir',type=Path,default=ROOT/'.restored/rerun')
 a=ap.parse_args();out=a.output_dir.resolve()
 if out.is_relative_to(ROOT) and not out.is_relative_to(ROOT/'.restored'):raise SystemExit('Inside this repository, outputs must be under ignored .restored/')
 if out==ROOT or out==ROOT.parent:raise SystemExit('Unsafe output directory')
 out.mkdir(parents=True,exist_ok=True);inputs=out/'inputs';results=[]
 if a.only in ['all','social']:
  source,n=materialize('sources/session/uploads',inputs)
  target=out/'social'; target.mkdir(exist_ok=True)
  results.append(run(ROOT/'analysis/social/build_social.py','--input-dir',source,'--output-dir',target))
  pilot=ROOT/'archive/session_work_products/Auto2000_Pilot_Analysis_Followup/PRIVATE_curated_evidence.json'
  results.append(run(ROOT/'analysis/social/curate_social.py','--social-dir',target,'--pilot-cases',pilot))
  results.append(run(ROOT/'analysis/social/maps_deep/build_maps_deep.py','--input',source,'--output',target/'maps_deep'))
  results.append(run(ROOT/'analysis/social/verify_social.py','--input-dir',source,'--social-dir',target))
  metrics=read_json(target/'corpus_metrics.json')
  assert {k:metrics[k]['unique_ids'] for k in ['x','maps','youtube']}=={'x':14291,'maps':8119,'youtube':74}
 if a.only in ['all','geography']:
  source,n=materialize('sources/geography_latest',inputs)
  source=source/'Auto2000_Lanjutan';target=out/'geography';target.mkdir(exist_ok=True)
  results.append(run(ROOT/'analysis/geography/scripts/independent_od_audit.py','--source-root',source,'--output',target))
  results.append(run(ROOT/'analysis/geography/scripts/portfolio_analysis.py','--table',source/'output/tables/branch_decision_table_29.csv','--output',target))
  geo=read_json(target/'raw_independent_audit.json');assert geo['pass'] and geo['paired_strict_origins']==284
 if a.only in ['all','research']:
  target=out/'research';target.mkdir(exist_ok=True)
  script=target/'build_research_integration.py';shutil.copy2(ROOT/'analysis/research/build_research_integration.py',script)
  results.append(run(script,'--legacy-root',ROOT/'archive/legacy_repo','--case-pdf',ROOT/'sources/case/Semifinal_Casebook_IBSC_2026.pdf'))
  result=read_json(target/'integration_research_checks.json');assert all(x['pass'] for x in result['checks'])
 receipt={'passed':True,'selection':a.only,'output_dir':str(out),'network_used':False,'originals_modified':False,'steps':results}
 (out/'RERUN_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'passed':True,'selection':a.only,'output_dir':str(out),'steps':len(results)},indent=2))
if __name__=='__main__':main()
