import sys,json,re,concurrent.futures
from pathlib import Path
from bs4 import BeautifulSoup
from public_http import fetch,ROOT
urls=['https://auto2000.co.id/dealer-toyota/kabupaten-bogor/auto2000cibinong','https://auto2000.co.id/dealer-toyota/balikpapan/auto2000balikpapansudirman','https://auto2000.co.id/dealer-toyota/tangerang/auto2000tangerang','https://auto2000.co.id/dealer-toyota/tangerang-selatan/auto2000bsdcity','https://auto2000.co.id/dealer-toyota/jakarta-barat/auto2000kapuk']
def probe(url):
 r=fetch(url,source='branch_identity_validation');s=BeautifulSoup(r.content,'lxml');out={'url':url,'final_url':r.url,'status':r.status,'request_id':r.request_id,'geo_schema':[],'map_links':[],'other_coordinate_pattern_count':len(re.findall(r'latitude|longitude',r.text,re.I))}
 for n in s.find_all('script',type='application/ld+json'):
  try:obj=json.loads(n.string or n.get_text())
  except:continue
  def walk(x):
   if isinstance(x,dict):
    if x.get('@type')=='GeoCoordinates':out['geo_schema'].append(x)
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(obj)
 for a in s.find_all(['a','iframe']):
  u=a.get('href',a.get('src',''))
  if 'maps.google' in u or 'google.com/maps' in u:out['map_links'].append(u)
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(probe,urls))
(ROOT/'workstreams/datasets/site_branch_identity_probe.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
