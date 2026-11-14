"""Rebuild fact-only inventories from acquired official-directory facts; no network."""
import json,csv,collections,pathlib
P=pathlib.Path(__file__).parent
r=json.loads((P/'official_branch_facts.json').read_text())
g=collections.OrderedDict()
for x in r:
 key=(x['name'],x['latitude'],x['longitude'])
 if key not in g:
  g[key]=dict(x);g[key]['directory_occurrences']=1;g[key]['all_directory_urls']=[x['directory_url']]
 else:
  g[key]['directory_occurrences']+=1;g[key]['all_directory_urls'].append(x['directory_url'])
u=list(g.values())
for i,x in enumerate(u,1):
 x['branch_id']=f'A2-{i:03d}';x['all_directory_urls']=' | '.join(x['all_directory_urls'])
 x['coordinate_status']=x.get('coordinate_status','missing')
 x['independent_field_verification']=False
 x['workshop_scope']='general service and parts advertised; selected job/model not independently confirmed' if x['general_workshop_documented'] else 'not included as general workshop'
def write(name,rows):
 with open(P/name,'w') as f:
  w=csv.DictWriter(f,fieldnames=sorted(set().union(*(x.keys() for x in rows))));w.writeheader();w.writerows(rows)
write('official_branches_unique.csv',u)
write('official_branches.csv',r)
d=[{'market':x['city'],'name':x['name'],'latitude':x['latitude'],'longitude':x['longitude'],'source_url':x['directory_url'],'coordinate_status':x['coordinate_status'],'job_specific_capability':x['job_specific_capability']} for x in u if x['routing_eligible']]
write('routing_destinations.csv',d)
geo={'type':'FeatureCollection','features':[{'type':'Feature','geometry':{'type':'Point','coordinates':[x['longitude'],x['latitude']]},'properties':x} for x in u if x['coordinate_status']=='official_direction_candidate']}
(P/'official_branches_unique.geojson').write_text(json.dumps(geo))
s={'official_directory_cards':len(r),'unique_name_coordinate_entries':len(u),'directory_labels_with_cards':len(set(x['city'] for x in r)),'routing_eligible_general_workshops':len(d),'unique_general_workshop_advertised':sum(x['general_workshop_documented'] for x in u),'coordinate_status':dict(collections.Counter(x['coordinate_status'] for x in u)),'core_routing_counts':dict(collections.Counter(x['market'] for x in d if x['market'] in ['surabaya','medan','bandung','palembang'])),'limits':['Acquired official directory cards, not independently reconciled national network total','City directory label is search page, not validated administrative location','No selected vehicle/job completion, appointment, capacity or battery competence validation','Official direction candidates not field-confirmed entrances','Two apparently local directories repeat Surabaya cards; deduplicate by name and coordinates']}
(P/'branch_inventory_summary.json').write_text(json.dumps(s,indent=2));print(json.dumps(s,indent=2))
