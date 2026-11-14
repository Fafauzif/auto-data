#!/usr/bin/env python3
"""Build finite study inventories from official branch and provider inputs.
Provider normalization supports standard Overture/OSM schemas; review output before run.
"""
import csv,json,hashlib,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parent
CORES={'Surabaya':[112.64,-7.38,112.84,-7.18],'Medan':[98.59,3.48,98.77,3.69],'Bandung':[107.51,-6.99,107.74,-6.82],'Palembang':[104.66,-3.07,104.85,-2.88]}
def rows(p):
 with open(p,encoding='utf-8-sig') as f:return list(csv.DictReader(f))
def get(r,*keys):
 return next((r[k] for k in keys if r.get(k) not in ('',None)),None)
def point(r):
 try:return float(get(r,'longitude','lon','lng')),float(get(r,'latitude','lat'))
 except (ValueError,TypeError):return None

def build(providers,branches,otoxpert,out,grid_n,margin):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);pp=rows(providers);bb=rows(branches);oo=rows(otoxpert);config={'markets':[]};logs=[]
 for market,b in CORES.items():
  bounds=[b[0]-margin,b[1]-margin,b[2]+margin,b[3]+margin]
  dests=[];seen=set()
  for group,rr in [('auto2000',bb),('otoxpert',oo),('independent',pp)]:
   for r in rr:
    if group=='independent' and 'eligible_candidate' in r and r['eligible_candidate'].lower()!='true':continue
    xy=point(r)
    if not xy:continue
    x,y=xy
    if not(bounds[0]<=x<=bounds[2] and bounds[1]<=y<=bounds[3]):continue
    # Source says these are candidate auto repair businesses, NOT guaranteed independents.
    # Known Toyota/Auto2000/OtoXpert records removed from alternative garage category.
    name=get(r,'name','primary_name','names.primary') or 'Unnamed mapped provider'
    if group=='independent' and any(t in name.casefold().replace(' ','') for t in ('auto2000','otoxpert')):continue
    key=(group,round(x,6),round(y,6),name.casefold())
    if key in seen:continue
    seen.add(key)
    ident=get(r,'destination_id','provider_id','id','osm_id') or hashlib.sha256(f'{group}|{name}|{x}|{y}'.encode()).hexdigest()[:12]
    ident=group+':'+str(ident)
    if any(d['destination_id']==ident for d in dests):ident+=':'+hashlib.sha256(f'{x}|{y}'.encode()).hexdigest()[:8]
    dests.append({'destination_id':ident,'name':name,'longitude':x,'latitude':y,'kind':group,'capability_status':'unverified','source_url':get(r,'source_url','url','website') or '', 'original_source_id':get(r,'provider_id','id','osm_id') or '', 'original_category':get(r,'primary_category','category','categories','taxonomy','classification') or '', 'source_confidence':r.get('confidence',''),'explicit_car_name':r.get('explicit_car_name',''),'auto2000_operator':r.get('auto2000_operator',''),'provider_operator':r.get('operator',''), 'classification_limit':'conservatively filtered mapped repair candidate; ownership/job fit unverified' if group=='independent' else 'official directory coordinate; outlet/model/job unconfirmed','market':market})
  p=out/(market.lower()+'_destinations.csv')
  with p.open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=list(dests[0]) if dests else ['destination_id','name','longitude','latitude','kind','capability_status','source_url']);w.writeheader();w.writerows(dests)
  config['markets'].append({'market':market,'bbox':b,'destination_bbox':bounds,'grid_n':grid_n,'destinations_csv':p.name})
  logs.append({'market':market,'core_bbox':b,'destination_bbox':bounds,'destinations':len(dests),'auto2000':sum(d['kind']=='auto2000' for d in dests),'otoxpert':sum(d['kind']=='otoxpert' for d in dests),'mapped_garage_candidates':sum(d['kind']=='independent' for d in dests)})
 (out/'config.json').write_text(json.dumps(config,indent=2));(out/'inventory_receipt.json').write_text(json.dumps(logs,indent=2));print(json.dumps(logs,indent=2))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--providers',required=True);a.add_argument('--branches',required=True);a.add_argument('--otoxpert',required=True);a.add_argument('--out',default=str(BASE/'inputs'));a.add_argument('--grid-n',type=int,default=9);a.add_argument('--margin',type=float,default=.08);s=a.parse_args();build(s.providers,s.branches,s.otoxpert,s.out,s.grid_n,s.margin)
