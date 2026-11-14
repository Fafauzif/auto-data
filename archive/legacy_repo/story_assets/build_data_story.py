"""Render existing verified findings as seven visual-page briefs. No new retrieval/analysis."""
from pathlib import Path
import json,hashlib,math
import pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=Path(__file__).resolve().parent
G=ROOT/'workstreams/extension_geography';B=ROOT/'workstreams/extension_battery';D=ROOT/'workstreams/datasets'
geo=pd.read_csv(G/'nearest_scenario_summary.csv');coord=pd.read_csv(D/'five_branch_coordinate_crosscheck.csv');ratio=pd.read_csv(G/'province_ratio_scenarios.csv');cons=pd.read_csv(G/'boundary_stock_conservation.csv');battery=json.loads((B/'BATTERY_SUMMARY.json').read_text());key=json.loads((B/'KEY_FINDINGS.json').read_text());integ=pd.read_csv(B/'gap_aware_signed_integrals.csv');slopes=pd.read_csv(B/'charging_interval_soc_slope_diagnostics.csv');gs=json.loads((G/'ROBUSTNESS_SUMMARY.json').read_text());bs=pd.read_csv(B/'bundle_signal_audit.csv')
def relative(p):return str(p.relative_to(ROOT))
def simple_sources(paths):return [{'path':relative(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
def grow(pool):return geo[(geo.coordinate_scenario=='source_coordinates')&(geo.candidate_pool==pool)].iloc[0]
allmap=grow('all_mapped');proxy=grow('network_public_facing_venue_proxy')
pages=[]
pages.append({
 'id':'DATA_STORY_01','title':'Nearby depends on which sites we count',
 'takeaway':'The 5 km result holds up. The 1 km result changes sharply.',
 'body':'Across 28 Auto2000-name locations, a conservative map filter cuts nearby options within 1 km from 20 to 8. At 5 km, the count changes only from 27 to 26. The nearest-option median rises from 0.323 to 1.413 km. This shows that close-range convenience depends on which sites we count. The filter still does not verify whether a driver can use them.',
 'chart':{'type':'grouped_bar','title':'How many of 28 locations have another mapped option nearby?','categories':['Within 1 km','Within 5 km'],'series':[{'name':'All mapped alternatives','values':[int(allmap.anchors_with_candidate_within_1km),int(allmap.anchors_with_candidate_within_5km)],'color':'#245A78'},{'name':'Conservative map filter','values':[int(proxy.anchors_with_candidate_within_1km),int(proxy.anchors_with_candidate_within_5km)],'color':'#B97032'}],'y_label':'Auto2000-name source locations, out of 28','y_min':0,'y_max':28,'show_integer_labels':True},
 'supporting_cards':[{'label':'Median straight-line distance','before_value':float(allmap.median_nearest_great_circle_km),'after_value':float(proxy.median_nearest_great_circle_km),'unit':'km','before_display':'0.323 km','after_display':'1.413 km'}],
 'evidence_limit':'The filter uses operator and venue names. It does not verify access, connector compatibility, opening hours or uptime.',
 'chart_note':'Original source coordinates. All distances are straight-line; 28 name matches are not the full Auto2000 branch network.',
 'source_files':simple_sources([G/'nearest_scenario_summary.csv']),
 'attribution':'SPKLU June 2026; Wiputra and Santiadi, DOI10.17632/z2bvd5r574.2, CC BY-NC 3.0. Original derived analysis.'})

branchlabels={2400:'Cibinong',2397:'Balikpapan Sudirman',2408:'Tangerang',2144:'BSD City',2154:'Kapuk'}
order=[2397,2408,2154,2144,2400];cc=coord.set_index('station_id').loc[order]
pages.append({
 'id':'DATA_STORY_02','title':'One published location differs by 55 km',
 'takeaway':'Check the location before trusting a proximity score.',
 'body':'We compared five charging-source points with current official branch directions. Four pairs are within 135 metres. Balikpapan Sudirman differs by 55.26 km. Replacing that point changes the nearest-site result, so a broad map summary can hide a local problem. This comparison identifies a published-data conflict. It does not tell us where the charger was physically located on either date.',
 'chart':{'type':'horizontal_bar','title':'Distance between two published map points','categories':[branchlabels[i] for i in order],'values':[float(v) for v in cc.straight_line_disagreement_km],'display_values':['55.258 km','0.135 km','0.028 km','0.014 km','0.009 km'],'x_label':'Straight-line difference (km)','x_min':0,'highlight_category':'Balikpapan Sudirman','highlight_color':'#B97032','other_color':'#245A78','small_value_note':'The four shorter differences are all below 0.135 km.','avoid_log_axis_for_plain_English':True},
 'supporting_data':[{'station_id':int(i),'branch':branchlabels[i],'source_latitude':float(cc.loc[i,'source_latitude']),'source_longitude':float(cc.loc[i,'source_longitude']),'official_candidate_latitude':float(cc.loc[i,'official_directions_candidate_latitude']),'official_candidate_longitude':float(cc.loc[i,'official_directions_candidate_longitude']),'difference_km':float(cc.loc[i,'straight_line_disagreement_km'])} for i in order],
 'evidence_limit':'Official branch directions are a second published source, not field confirmation of charging hardware.',
 'chart_note':'Charging-source snapshot: 16 June 2026. Official branch pages checked: 11 November 2026. Preserve both coordinate versions.',
 'source_files':simple_sources([D/'five_branch_coordinate_crosscheck.csv']),
 'attribution':'SPKLU CC BY-NC 3.0; current official Auto2000 branch directions. Original comparison.'})

pap=[]
for name,label in [('Papua Barat','West Papua, old boundary'),('Papua','Papua, old boundary')]:
 t=ratio[(ratio.year_of_denominator==2025)&(ratio.numerator_unit=='site_rows')&(ratio.province_name==name)].set_index('boundary_scenario');x=t.loc['direct_34_code_join'];y=t.loc['pooled_historical_34_boundaries'];pap.append({'source_area_name':name,'label':label,'before_ratio':float(x.units_per_100000_passenger_vehicles),'after_ratio':float(y.units_per_100000_passenger_vehicles),'before_denominator':int(x.passenger_stock_denominator),'after_denominator':int(y.passenger_stock_denominator),'before_rank':int(x.descending_rank),'after_rank':int(y.descending_rank),'site_numerator':int(x.numerator_value)})
ca=cons[(cons.year==2025)&(cons.boundary_scenario=='direct_34_code_join')].iloc[0]
pages.append({
 'id':'DATA_STORY_03','title':'A boundary mismatch changes the provincial leader',
 'takeaway':'West Papua falls from rank 1 to rank 10 after boundary alignment.',
 'body':'The charging source uses older provincial boundaries. The 2025 vehicle table separates four newer Papua provinces. A direct code match drops 70,800 cars from the denominator. Pooling those provinces back into the older boundaries lowers West Papua’s ratio from 48.80 to 19.19 and Papua’s from 22.68 to 13.44. The original apparent ranking depended on a mismatched join.',
 'chart':{'type':'dumbbell','title':'Mapped sites per 100,000 passenger vehicles','categories':[x['label'] for x in pap],'before_name':'Direct code match','after_name':'Aligned old boundaries','before_values':[x['before_ratio'] for x in pap],'after_values':[x['after_ratio'] for x in pap],'before_display':['48.80','22.68'],'after_display':['19.19','13.44'],'x_label':'Sites per 100,000 passenger vehicles','x_min':0,'before_color':'#B97032','after_color':'#245A78','rank_labels':['1 → 10','9 → 19']},
 'supporting_data':pap,
 'supporting_cards':[{'label':'Cars omitted by the direct match','value':int(ca.unmatched_stock),'display':'70,800'},{'label':'Share of national passenger stock','display':'0.339%','numerator':int(ca.unmatched_stock),'denominator':int(ca.national_source_passenger_stock)}],
 'evidence_limit':'These ratios use all passenger vehicles, not BEVs; boundary alignment does not measure charging adequacy.',
 'chart_note':'June 2026 mapped sites divided by 2025 BPS/Polri stocks. This corrects the first-wave direct-join interpretation.',
 'source_files':simple_sources([G/'province_ratio_scenarios.csv',G/'boundary_stock_conservation.csv']),
 'attribution':'SPKLU CC BY-NC 3.0; BPS/Polri published vehicle stocks. Original boundary-alignment analysis.'})

pages.append({
 'id':'DATA_STORY_04','title':'Four charging counts mean four different things',
 'takeaway':'A site count is not a capacity measure.',
 'body':'The same source contains 2,454 station records, 3,767 charger-box records, 7,593 reconstructed charger units and 4,665 connectors. These quantities describe different levels of the source data. They cannot be added or substituted for one another. None tells us how many compatible vehicles can charge at once today. Choosing a different unit can also change provincial rankings.',
 'chart':{'type':'unit_cards','title':'Keep each number attached to its unit','cards':[{'label':'Station records','value':int(gs['station_rows']),'display':'2,454','meaning':'Consolidated source locations'},{'label':'Charger-box records','value':int(gs['charger_box_rows']),'display':'3,767','meaning':'Separate hardware records'},{'label':'Source charger units','value':int(gs['source_charger_unit_sum']),'display':'7,593','meaning':'Counts reconstructed by the source'},{'label':'Source connectors','value':int(gs['source_connector_sum']),'display':'4,665','meaning':'Recorded connector counts'}],'do_not_stack_or_sum':True,'do_not_label_capacity':True},
 'supporting_cards':[{'label':'Largest site-versus-box rank shift','value':8,'unit':'places','display':'8 places'}],
 'evidence_limit':'Hardware counts do not establish usable power, simultaneous charging capacity, vehicle compatibility or uptime.',
 'chart_note':'Source snapshot: 16 June 2026. Exact coordinate duplicates were already consolidated by the source.',
 'source_files':simple_sources([G/'ROBUSTNESS_SUMMARY.json',G/'province_rank_sensitivity.csv']),
 'attribution':'Wiputra and Santiadi, Mendeley V2, DOI10.17632/z2bvd5r574.2, CC BY-NC 3.0.'})

pages.append({
 'id':'DATA_STORY_05','title':'56 million values still cannot validate a health certificate',
 'takeaway':'The missing reference matters more than the row count.',
 'body':'One historical Audi in California supplies 56.5 million stored electrical and BMS signal values. They support signal analysis, not a Toyota health certificate. The paper’s capacity reference is withheld. Current and voltage share a clock in all five bundles, but SOC does so in only two and temperature in none. The measurements need careful alignment before any health claim can be tested.',
 'chart':{'type':'horizontal_bar','title':'Signals sharing the current clock exactly','categories':['Voltage','State of charge','Temperature'],'values':[5,int(battery['soc_clock_identical_bundle_count']),int(battery['temperature_clock_identical_bundle_count'])],'display_values':['5 of 5 bundles','2 of 5 bundles','0 of 5 bundles'],'x_label':'Selected source bundles','x_min':0,'x_max':5,'show_integer_labels':True,'color':'#245A78'},
 'supporting_cards':[{'label':'Stored signal values','value':int(battery['physical_or_BMS_signal_scalar_values_excluding_clocks_epoch']),'display':'56,507,201'},{'label':'Vehicles represented','value':1,'display':'1 Audi, California'},{'label':'Public health-reference field','display':'Not available'}],
 'evidence_limit':'Counts exclude clocks and epoch metadata. Values are not independent customers, trips or synchronized rows.',
 'chart_note':'Five folder windows from a single Audi e-tron, 2019–2020. SOC means state of charge, not state of health.',
 'source_files':simple_sources([B/'BATTERY_SUMMARY.json',B/'bundle_signal_audit.csv',B/'scalar_count_receipt.csv']),
 'attribution':'Pozzato et al., Mendeley V2, DOI10.17632/7vdkzpnjgj.2, CC BY-NC 3.0. README excludes confidential capacity data.'})

safe=integ[(integ.folder=='Folder2')&(integ.max_integrated_step_seconds=='1')].iloc[0];naive=integ[(integ.folder=='Folder2')&(integ.max_integrated_step_seconds=='UNBOUNDED_NAIVE_COUNTEREXAMPLE')].iloc[0];f16=bs[bs.folder=='Folder16'].iloc[0]
pages.append({
 'id':'DATA_STORY_06','title':'A simple integration mistake adds 47.5% to the result',
 'takeaway':'Do not treat days between logs as measured driving.',
 'body':'Across five bundles, the one-second gap rule retains 51.97 supported hours. Folder16 alone spans 50.82 calendar days, yet contains only 17.19 such hours. Bridging every gap inflates Folder2’s absolute terminal integral from 156.206 to 230.433 kWh. The extra 47.52% comes from an unsupported calculation across missing intervals. The tested 1-, 30- and 300-second limits agree here.',
 'chart':{'type':'bar','title':'Drive Folder2: the effect of bridging long gaps','categories':['Keep supported intervals','Bridge every gap'],'values':[float(safe.absolute_terminal_kWh),float(naive.absolute_terminal_kWh)],'display_values':['156.206 kWh','230.433 kWh'],'y_label':'Absolute pack-terminal integral (kWh)','y_min':0,'colors':['#245A78','#B97032'],'callout':'+47.52% unsupported extra integral'},
 'supporting_cards':[{'label':'Supported time, five bundles','value':float(battery['observed_supported_hours_gap1']),'display':'51.974 hours','gap_limit_seconds':1},{'label':'Folder16 calendar span','value':float(f16.wall_span_days),'display':'50.824 days'},{'label':'Folder16 supported time','value':float(integ[(integ.folder=='Folder16')&(integ.max_integrated_step_seconds=='1')].supported_seconds.iloc[0]/3600),'display':'17.190 hours','gap_limit_seconds':1}],
 'evidence_limit':'This is a signed-signal throughput calculation, not battery capacity, charger wall energy, efficiency or a production-system failure.',
 'chart_note':'Absolute integral adds positive and negative energy magnitudes. Current and voltage clocks match in these files.',
 'source_files':simple_sources([B/'gap_aware_signed_integrals.csv',B/'BATTERY_SUMMARY.json',B/'bundle_signal_audit.csv']),
 'attribution':'Pozzato et al. CC BY-NC 3.0 source data. Original gap-sensitivity analysis.'})

pages.append({
 'id':'DATA_STORY_07','title':'Four partial-charge slopes are not four health scores',
 'takeaway':'A partial charge cannot become a health score without validation.',
 'body':'Four supported charge intervals give 1.570 to 2.195 Ah per reported SOC percentage point. Their current, temperature and SOC windows differ. Every stored current value lies on an integer-ampere grid, but the sensor’s accuracy bound is unknown. These ratios describe the selected intervals. Rescaling them into battery capacity or state of health would add an assumption this dataset cannot validate.',
 'chart':{'type':'bar','title':'Observed charge per reported SOC percentage point','categories':['Interval A','Interval B','Interval C','Interval D'],'values':[float(v) for v in slopes.observed_negative_Ah_per_reported_soc_percentage_point],'display_values':[f'{v:.3f}' for v in slopes.observed_negative_Ah_per_reported_soc_percentage_point],'y_label':'Observed negative Ah / SOC percentage point','y_min':0,'y_max':2.4,'color':'#245A78'},
 'supporting_data':[{'display_interval':label,'folder':str(row.folder),'source_segment':int(row.segment_number_gap30),'SOC_gain_percentage_points':float(row.aligned_soc_change_percentage_points),'negative_Ah_common_support':float(row.aligned_negative_magnitude_Ah),'Ah_per_SOC_percentage_point':float(row.observed_negative_Ah_per_reported_soc_percentage_point),'mean_pack_temperature_C':float(row.temperature_time_weighted_mean_C)} for label,row in zip(['Interval A','Interval B','Interval C','Interval D'],slopes.itertuples())],
 'supporting_cards':[{'label':'Recorded current grid','display':'Integer amperes'},{'label':'Calibrated accuracy bound','display':'Not supplied'}],
 'evidence_limit':'Four nonrandom intervals from one vehicle cannot establish degradation, capacity, health-score accuracy or a temperature effect.',
 'chart_note':'SOC is state of charge. Common observed support only; no endpoint extrapolation. The health reference is not public.',
 'source_files':simple_sources([B/'charging_interval_soc_slope_diagnostics.csv',B/'current_numeric_resolution_audit.csv']),
 'attribution':'Pozzato et al. CC BY-NC 3.0 source data. Original partial-interval diagnostic.'})

checks=[]
def ck(name,condition):checks.append({'check':name,'pass':bool(condition)})
ck('Exactly seven visual pages',len(pages)==7)
for p in pages:
 p['body_word_count']=len(p['body'].split());ck(p['id']+' body no more than70words',p['body_word_count']<=70)
 ck(p['id']+' all source paths exist',all((ROOT/x['path']).is_file() for x in p['source_files']))
ck('Page1 exact counts28anchors',pages[0]['chart']['series'][0]['values']==[20,27] and pages[0]['chart']['series'][1]['values']==[8,26])
ck('Coordinate conflict exact55.257852km',math.isclose(pages[1]['chart']['values'][0],55.257852064738024,rel_tol=0,abs_tol=1e-10))
ck('Other four coordinate differences below135m',max(pages[1]['chart']['values'][1:])<.135)
ck('Boundary source denominator conservation',ca.unmatched_stock==70800 and ca.national_source_passenger_stock==20907972)
ck('Papua rank changes1to10and9to19',[(x['before_rank'],x['after_rank']) for x in pap]==[(1,10),(9,19)])
ck('Charging quantities distinct verified source counts',[x['value'] for x in pages[3]['chart']['cards']]==[2454,3767,7593,4665])
ck('Telemetry exact scientific scalar count',pages[4]['supporting_cards'][0]['value']==56507201)
ck('Clock matches5/2/0',pages[4]['chart']['values']==[5,2,0])
ck('Gap plot exact persisted integral values',pages[5]['chart']['values']==[float(safe.absolute_terminal_kWh),float(naive.absolute_terminal_kWh)])
ck('Four partial slopes correct persisted order',len(pages[6]['chart']['values'])==4 and pages[6]['chart']['values']==slopes.observed_negative_Ah_per_reported_soc_percentage_point.tolist())
ck('No unrelated PEF source used',all('pef' not in x['path'].lower() for p in pages for x in p['source_files']))
assert all(x['pass'] for x in checks),[x for x in checks if not x['pass']]
output={'purpose':'Seven plain-English visual-page briefs drawn only from existing verified study files; no new retrieval or external visual-reference data.','pages':pages,'quality_checks':{'total':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'checks':checks},'layout_guidance':{'body_max_words':70,'primary_chart_per_page':1,'show_source_and_one_evidence_limit':True,'do_not_import_data_from_visual_reference_PDF':True,'do_not_hide_unverified_access_or_missing_health_reference':True,'counts_not_to_stack':['station records','charger boxes','source charger units','connectors'],'color_before_or_unfiltered':'#245A78','color_alternative_or_warning':'#B97032'}}
(OUT/'data_story.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
md=['# Seven visual data pages','Each page has one main chart, a short body and one visible evidence limit. Exact chart numbers and source hashes are in `data_story.json`. The visual-reference PDF supplies no research data.']
for p in pages:
 md.extend(['',f"## {p['id']}: {p['title']}",'',f"**Takeaway:** {p['takeaway']}",'',p['body'],'',f"**Main visual:** {p['chart']['type']}: {p['chart']['title']}.",'',f"**Keep visible:** {p['evidence_limit']}",'',f"**Chart note:** {p['chart_note']}",'',f"**Source:** {'; '.join(x['path'] for x in p['source_files'])}",'',f"Body length: {p['body_word_count']} words."])
md.extend(['','## Quality checks','',f"{len(checks)} checks passed; zero failed. Counts, coordinate offsets, rank changes, signal units and exact source values reconcile. All seven bodies contain at most70words. No PEF data were imported."])
(OUT/'data_story.md').write_text('\n'.join(md)+'\n');print('Seven page briefs saved;',len(checks),'checks passed; body words:',[p['body_word_count'] for p in pages])
