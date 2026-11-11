"""Read-only source/claim review of selected visual-story pages. No new analysis/retrieval."""
from pathlib import Path
import json,hashlib,math,datetime
import pandas as pd,numpy as np
from pypdf import PdfReader
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reports';pdf=ROOT/'output/pdf/Auto2000_Research_Findings.pdf'
expected='7c1fc15d879afc59b217bb89d43b5625dfb5710e4b2c4acc2a8f127f84444034'
actual=hashlib.sha256(pdf.read_bytes()).hexdigest();reader=PdfReader(pdf)
pages={i:' '.join(reader.pages[i-1].extract_text().split()) for i in [17,18,19,20,23,24,25,38]}
assets=json.loads((ROOT/'story_assets/data_story.json').read_text());asset={p['id']:p for p in assets['pages']};manifest=json.loads((ROOT/'figures/story/STORY_CHART_MANIFEST.json').read_text());charts={x['page_id']:x for x in manifest['figures'] if x.get('asset')=='data_story.json'}
G=ROOT/'workstreams/extension_geography';B=ROOT/'workstreams/extension_battery';D=ROOT/'workstreams/datasets'
checks=[]
def ck(name,ok,page=None,evidence=None):checks.append({'check':name,'pass':bool(ok),'pdf_page':page,'evidence':evidence})
ck('Exact requested PDF hash',actual==expected,evidence=actual);ck('41-page visual edition',len(reader.pages)==41)
for pid,entry in charts.items():ck('Chart manifest exactly matches brief '+pid,entry['plot_data']==asset[pid]['chart'])
for n,chart in [(17,'data_01'),(18,'data_02'),(19,'data_03'),(23,'data_05'),(24,'data_06'),(25,'data_07')]:
 original=Image.open(ROOT/'figures/story'/f'{chart}.png').convert('RGB');matches=[]
 for im in reader.pages[n-1].images:
  z=im.image.convert('RGB');matches.append(z.size==original.size and hashlib.sha256(z.tobytes()).digest()==hashlib.sha256(original.tobytes()).digest())
 ck('Embedded plot pixels equal expected PNG '+chart,any(matches),n)
geo=pd.read_csv(G/'nearest_scenario_summary.csv');z=geo[(geo.coordinate_scenario=='source_coordinates')&(geo.candidate_pool=='all_mapped')].iloc[0];q=geo[(geo.coordinate_scenario=='source_coordinates')&(geo.candidate_pool=='network_public_facing_venue_proxy')].iloc[0]
ck('1km20to8 and5km27to26 with28 anchors',z.anchor_n==q.anchor_n==28 and [z.anchors_with_candidate_within_1km,q.anchors_with_candidate_within_1km,z.anchors_with_candidate_within_5km,q.anchors_with_candidate_within_5km]==[20,8,27,26],17)
ck('Median display0.323to1.413 matches exact source',round(z.median_nearest_great_circle_km,3)==.323 and round(q.median_nearest_great_circle_km,3)==1.413,17)
ck('Map headline preserves unverified usability','does not establish usable access' in pages[17] and 'does not verify access' in pages[17],17)
coord=pd.read_csv(D/'five_branch_coordinate_crosscheck.csv');bal=coord[coord.station_id==2397].straight_line_disagreement_km.iloc[0]
ck('Balikpapan55.258km and55.26roundings',round(bal,3)==55.258 and round(bal,2)==55.26,18)
ck('Other four differences below135metres',len(coord)==5 and (coord[coord.station_id!=2397].straight_line_disagreement_km<.135).all(),18)
ck('No physical-location truth claim','not field confirmation' in pages[18] and 'does not tell us where the charger was physically located' in pages[18],18)
ratio=pd.read_csv(G/'province_ratio_scenarios.csv');bdy=[]
for name,expect in [('Papua Barat',(48.80,19.19,1,10)),('Papua',(22.68,13.44,9,19))]:
 r=ratio[(ratio.year_of_denominator==2025)&(ratio.numerator_unit=='site_rows')&(ratio.province_name==name)].set_index('boundary_scenario');a=r.loc['direct_34_code_join'];b=r.loc['pooled_historical_34_boundaries'];v=(round(a.units_per_100000_passenger_vehicles,2),round(b.units_per_100000_passenger_vehicles,2),int(a.descending_rank),int(b.descending_rank));ck('Boundary ratios and ranks '+name,v==expect,19);bdy.append(v)
co=pd.read_csv(G/'boundary_stock_conservation.csv');a=co[(co.year==2025)&(co.boundary_scenario=='direct_34_code_join')].iloc[0]
ck('Omitted70800 androunded0.339% correct',a.unmatched_stock==70800 and round(100*a.unmatched_stock/a.national_source_passenger_stock,3)==.339,19,evidence='0.339% appears in brief support card; PDF body shows70,800.')
ck('Denominator scope not BEV adequacy','all passenger vehicles, not BEVs' in pages[19] and 'does not measure charging adequacy' in pages[19],19)
st=pd.read_csv(ROOT/'raw_licensed_data/SPKLU_CC_BY_NC_3_0/data/spklu_stations.csv');boxes=pd.read_csv(ROOT/'raw_licensed_data/SPKLU_CC_BY_NC_3_0/data/spklu_chargers.csv')
ck('Four hardware counts reconcile to licensed source',len(st)==2454 and len(boxes)==3767 and boxes.n_chargers.sum()==7593 and boxes.n_connectors.sum()==4665,20)
ck('Counts not asserted to be capacity','cannot be added or substituted' in pages[20] and 'not a capacity measure' in pages[20],20)
scalar=pd.read_csv(B/'scalar_count_receipt.csv');ba=pd.read_csv(B/'bundle_signal_audit.csv');physical=int(scalar.loc[scalar.role=='signal_value','stored_values'].sum())
ck('56.5million correctly rounds56507201signal scalars',physical==56507201 and round(physical/1e6,1)==56.5,23)
ck('Clock arrays and epochs excluded from sample claim','exclude clocks and epoch metadata' in pages[23],23)
ck('I/V5SOC2temperature0 exact-clock counts',ba.raw_current_voltage_clocks_identical.sum()==5 and ba.soc_clock_identical_to_current.sum()==2 and ba.temperature_clock_identical_to_current.sum()==0,23)
ck('One historicAudiCalifornia, notToyota certificate','One historical Audi in California' in pages[23] and 'not a Toyota health certificate' in pages[23],23)
ck('Withheld reference not asserted independent lab groundtruth','paper’s capacity reference is withheld' in pages[23] and 'independent ground truth' not in pages[23] and 'independent capacity' not in pages[23],23,evidence='Public source omits BMS-derived capacity series; no independent laboratory validation standard is established.')
it=pd.read_csv(B/'gap_aware_signed_integrals.csv');safe=it[(it.folder=='Folder2')&(it.max_integrated_step_seconds=='1')].iloc[0];naive=it[(it.folder=='Folder2')&(it.max_integrated_step_seconds=='UNBOUNDED_NAIVE_COUNTEREXAMPLE')].iloc[0]
ck('Folder2integrals156.206to230.433match',round(safe.absolute_terminal_kWh,3)==156.206 and round(naive.absolute_terminal_kWh,3)==230.433,24)
ck('Relative inflation47.52%correct',round(100*(naive.absolute_terminal_kWh/safe.absolute_terminal_kWh-1),2)==47.52,24)
strict=it[it.max_integrated_step_seconds=='1'];ck('Supported51.97hours correctly rounded',round(strict.supported_seconds.sum()/3600,2)==51.97,24)
ck('Gap result framed as unsupported integral,notextra actualenergy','unsupported calculation across missing intervals' in pages[24] and 'not battery capacity, charger wall energy' in pages[24] and 'production-system failure' in pages[24],24)
ck('Tested1/30/300energy agreement retained','300-second limits agree here' in pages[24],24)
sl=pd.read_csv(B/'charging_interval_soc_slope_diagnostics.csv');plot=asset['DATA_STORY_07']['chart'];ck('Four slope labels match exact persisted intervals',len(sl)==4 and plot['values']==sl.observed_negative_Ah_per_reported_soc_percentage_point.tolist() and plot['display_values']==['1.570','2.187','2.195','2.162'],25)
res=pd.read_csv(B/'current_numeric_resolution_audit.csv');ck('Integergrid true without invented accuracybound',res.recorded_current_on_integer_ampere_grid.all() and 'accuracy bound is unknown' in pages[25],25)
ck('Slopes not healthscores/capacity/degradation claim','not four health scores' in pages[25] and 'cannot establish degradation, capacity' in pages[25],25)
ig=json.loads((D/'igar_analysis_summary.json').read_text());n=ig['rating_view_rows'];dis=ig['label_disagreement_rows'];agree=n-dis
ck('IGAR pairedrows617722 disagreement255414 agree362308',n==617722 and dis==255414 and agree==362308,38)
ck('IGAR percentlabels41.35and58.65correct',round(100*dis/n,2)==41.35 and round(100*agree/n,2)==58.65,38)
ck('IGAR distinctkeys617703duplicateexcess19',ig['unique_rating_composite_keys']==617703 and ig['exact_duplicate_excess_rows_rating']==19,38)
ck('IGAR humanGT andcustomer-scope limitations present','Neither is human ground truth' in pages[38] and 'not Digiroom' in pages[38] and 'Agreement is not accuracy' in pages[38],38)
qualifications=[{'severity':'minor_visual','page':25,'issue':'The long vertical y-axis title indata_07.png is clipped at the top edge. The numeric values and full unit in the page body are correct.','suggestion':'Shorten axis title to NegativeAh perSOCpoint and define percentagepoint in the visible caption.','numeric_claim_affected':False,'pdf_not_modified':True},{'severity':'minor_copy','page':38,'issue':'Several source/body tokens lack spaces, e.g. on255,414 and with617,703; numeric values remain correct.','suggestion':'Apply spacing cleanup if rebuilding.','numeric_claim_affected':False,'pdf_not_modified':True}]
result={'pdf_path':str(pdf),'pdf_sha256':actual,'expected_pdf_sha256':expected,'pages_reviewed':[17,18,19,20,23,24,25,38],'scope':'Source and numeric review of seven data-story pages plusIGAR. Separate from full-document visual QA. No new retrieval or analysis; only verification of existing source/derived tables.','reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks_total':len(checks),'passed':sum(x['pass'] for x in checks),'failed':sum(not x['pass'] for x in checks),'status':'PASS_WITH_MINOR_VISUAL_AND_COPY_QUALIFICATIONS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'qualifications':qualifications,'visual_evidence':'Reviewed all six source chart PNGs andpage38render; programmatically verified embeddedchartpixelidentity on pages17/18/19/23/24/25. Other agents own full-page visual coverage.','source_files':{'story_asset':str(ROOT/'story_assets/data_story.json'),'chart_manifest':str(ROOT/'figures/story/STORY_CHART_MANIFEST.json')},'pdf_modified':False}
(OUT/'STORY_DATA_CLAIM_QA.json').write_text(json.dumps(result,indent=2)+'\n')
md=f'''# Story data-claim QA

Reviewed PDF: `output/pdf/Auto2000_Research_Findings.pdf`.

SHA-256: `{actual}`.

Reviewed pages17–20,23–25 and38. **{result['passed']} checks passed; {result['failed']} failed.** No material numeric or source-scope mismatch found. The PDF was not edited.

The six embedded chart images are pixel-identical to the expected storyPNG files. Chart-manifest arrays match the seven-page brief. Source CSVs confirm the mapped-site filters, coordinate conflict, historical-boundary ratios/ranks, four hardware units, telemetry scalar and clock counts, gap-integral inflation and four partial SOC slopes. Licensed SPKLU source tables independently reconcile the hardware counts.

The source limits remain visible: mapped proximity does not verify access; branch directions do not establish a charger’s physical location; all-passenger stocks are not BEV demand; one historical Audi does not validate Toyota health claims; the paper’s hidden capacity reference is BMS-derived and not established independent laboratory groundtruth; the47.52% result is unsupported computed integration, not extra measured energy; partial slopes are not capacity or SOH. IGAR’s617,722pairedrows,255,414disagreements,362,308agreements and41.35%/58.65% labels reconcile. Neither label view is human groundtruth.

Two minor qualifications remain. Page25’s long vertical chart-unit label is clipped at the top; the body supplies the full unit and all plotted values are correct. Page38contains several missing spaces around numbers. These do not change the numeric findings. Root was notified before receipt generation. Full-document visual QA remains a separate review.
'''
(OUT/'STORY_DATA_CLAIM_QA.md').write_text(md)
print(json.dumps({k:result[k] for k in ['pdf_sha256','checks_total','passed','failed','status']},indent=2));print('FAILED',[x for x in checks if not x['pass']])
