from pathlib import Path
import json, math, csv, textwrap, html
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,Color,white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph,Table,TableStyle
from reportlab.lib.utils import ImageReader
R=Path(__file__).resolve().parents[1]
OUT=R/'report/Auto2000_Geographic_Workshop_Study.pdf'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(n,'/usr/share/fonts/truetype/dejavu/'+f))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
W,H=595.276,841.89; M=43; CW=W-2*M
BG=HexColor('#fbfaf6');INK=HexColor('#16373d');TEAL=HexColor('#236a75');RED=HexColor('#c04f36');GRAY=HexColor('#5a686b')
styles={'body':ParagraphStyle('body',fontName='Body',fontSize=10,leading=15,textColor=INK,spaceAfter=10),'small':ParagraphStyle('small',fontName='Body',fontSize=8,leading=11,textColor=GRAY),'title':ParagraphStyle('title',fontName='Bold',fontSize=23,leading=28,textColor=INK),'cell':ParagraphStyle('cell',fontName='Body',fontSize=8,leading=11,textColor=INK),'head':ParagraphStyle('head',fontName='Bold',fontSize=8,leading=11,textColor=white)}
c=canvas.Canvas(str(OUT),pagesize=(W,H));c.setTitle('Auto2000 | Geography of Paid Workshop Recovery');c.setAuthor('Public-data geographic research')
PAGE=0;spec=[];qa=[]
def para(txt,x,y,width,style='body'):
 p=Paragraph(txt,styles[style]);w,h=p.wrap(width,1000);p.drawOn(c,x,y-h);return y-h

def page(title,kicker,paras=[],fig=None,caption='',table=None,columns=None,note=None):
 global PAGE
 PAGE+=1;c.setFillColor(BG);c.rect(0,0,W,H,fill=1,stroke=0)
 c.setFillColor(TEAL);c.setFont('Bold',8);c.drawString(M,H-37,'AUTO2000  /  GEOGRAPHIC RESEARCH  /  14 NOV 2026')
 c.setFillColor(RED);c.setFont('Bold',8);c.drawString(M,H-62,kicker.upper())
 y=para(title,M,H-77,CW,'title')-18
 for p in paras:y=para(p,M,y,CW)-9
 if fig:
  p=R/fig
  if not p.exists():raise FileNotFoundError(p)
  img=ImageReader(str(p));iw,ih=img.getSize()
  reserve=0
  if caption:reserve+=Paragraph(caption,styles['small']).wrap(CW,1000)[1]+12
  if note:reserve+=Paragraph('<b>Interpretation.</b> '+note,styles['body']).wrap(CW,1000)[1]
  if table:
   cc=[[Paragraph(html.escape(str(v)),styles['head' if i==0 else 'cell']) for v in row] for i,row in enumerate(table)]
   tt=Table(cc,colWidths=columns or [CW/len(table[0])]*len(table[0]))
   tt.setStyle(TableStyle([('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   reserve+=tt.wrap(CW,1000)[1]+14
  height=min(CW*ih/iw,y-83-reserve,520);width=height*iw/ih
  if height<85:raise RuntimeError(f'Figure too small page{PAGE}: {height}')
  c.drawImage(img,M+(CW-width)/2,y-height,width,height,mask='auto');y-=height+8
  if caption:y=para(caption,M,y,CW,'small')-12
 if table:
  cells=[[Paragraph(html.escape(str(v)),styles['head' if i==0 else 'cell']) for v in row] for i,row in enumerate(table)]
  tw=columns or [CW/len(table[0])]*len(table[0]);t=Table(cells,colWidths=tw,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,0),.5,TEAL),('ROWBACKGROUNDS',(0,1),(-1,-1),[HexColor('#edf1ed'),BG])]))
  aw,hh=t.wrap(CW,1000);t.drawOn(c,M,y-hh);y-=hh+14
 if note:
  y=para('<b>Interpretation.</b> '+note,M,y,CW,'body')
 if y<66:raise RuntimeError(f'Page{PAGE} overflow {y} {title}')
 c.setStrokeColor(HexColor('#d4ddda'));c.line(M,49,W-M,49);c.setFillColor(GRAY);c.setFont('Body',7);c.drawString(M,34,'Public sources | Modelled access | No customer-demand or profit estimate');c.drawRightString(W-M,34,str(PAGE));c.showPage()
 spec.append({'page':PAGE,'title':title,'kicker':kicker,'paragraphs':paras,'figure':fig,'caption':caption,'table':table,'note':note});qa.append({'page':PAGE,'bottom_y':round(y,1),'layout_bounds_pass':y>=66})

def j(p):return json.loads((R/p).read_text())
def table_csv(p,cols,limit=10):
 d=pd.read_csv(R/p).fillna('');return [cols]+d[cols].head(limit).values.tolist()

# Dynamic sources loaded only after all workstreams finish.
br=pd.read_csv(R/'workstreams/branches/official_branches_unique.csv');ox=pd.read_csv(R/'workstreams/context/otoxpert_official_inventory.csv');pr=pd.read_csv(R/'workstreams/providers/provider_inventory.csv')
ms=pd.read_csv(R/'workstreams/routing/output/market_summary.csv');oa=pd.read_csv(R/'workstreams/routing/output/origin_accessibility.csv');receipt=j('workstreams/routing/output/run_receipt.json')
main=ms[ms.scenario=='all_routed']; tight=ms[ms.scenario=='snap_le_250m']
providers=pr[pr.eligible_candidate.astype(str).str.lower()=='true']
N=len(br);P=len(pr);K=len(providers);orig=receipt['origins'];pairs=receipt['od_pairs']
figure_registry={}
for f in [R/'workstreams/cartography/figure_registry.json',R/'workstreams/context/figure_registry.json']:
 if f.exists():figure_registry[f.parent.name]=json.loads(f.read_text())

def figmatch(substr):
 files=sorted((R/'figures').glob('*.png'))
 found=[p for p in files if substr in p.stem]
 return str(found[0].relative_to(R)) if found else None

page('Where could Auto2000 recover paid workshop jobs?','Research-led geographic study',[
 'Four urban investigations, a 15-market context screen and a reproducible public-data evidence pack.',
 '<b>The question is geographic plausibility.</b> This study compares documented workshop locations with mapped repair/service candidates and modelled road access. It investigates where a paid-job recovery pilot deserves further evidence, rather than estimating how many customers will switch.',
 f'The run combines {N} reconciled Auto2000 directory entries, {len(ox)} OtoXpert listings, Overture automotive-place extracts and {orig} grid origins. These are different evidence units and must not be added into a customer total.'
],fig='figures/national_charging.png',caption='Archived June 2026 charging context. Orange markers are only the 28 Auto2000-name records in that dataset, not the dealer network. Sources: archive SPKLU V2; Natural Earth.')

srows=[['Study window','Full paired n','Full gap min','Snap-screen n','Snap gap min']]
for _,r in main.iterrows():
 q=tight[tight.market==r.market].iloc[0];srows.append([r.market.title(),int(r.paired_origins),f'{r.median_paired_additional_minutes:.1f}',int(q.paired_origins),f'{q.median_paired_additional_minutes:.1f}'])
page('A map can identify friction; it cannot establish a recovered job','Decision brief',[
 'The defensible result is a set of access comparisons within explicit study windows. The mapped repair/service pool is a candidate inventory, not a verified set of equivalent Toyota jobs. Differences below identify questions for a pilot; they do not measure lost customers.',
 'The separately documented OtoXpert + Shop&amp;Drive oil-network scenario gives snap-screened median paired Auto2000 gaps of about 1.0 minute in Surabaya, 0.3 in Medan and 2.6 in both Bandung and Palembang. These are smaller than the broad candidate gaps below, and suggest that the comparator definition changes the practical story. Exact job equivalence remains unverified.',
 'The minute gap changes materially under stricter provider definitions, so its magnitude is not a stable estimate of competitive disadvantage. The strategy also changes in two ways before any forecast is justified. First, customer-paid work is not synonymous with an expired vehicle warranty. Second, economical workshop and parts routes already exist through OtoXpert and T-OPT. Operator identity matters for whose contribution a recovered job would create.'
],table=srows,note='Full = all routed; snap screen requires both endpoint snaps no more than 250 metres. The paired gap is the median of origin-level Auto2000 minus candidate travel durations. It is not the difference between the two channel medians. Times are OSRM-profile model outputs, not observed traffic. [R1; S1; CX06-CX09]')
page('Define the cohort by payer and entitlement, not age alone','Cohort correction',[
 'The original plan prioritised out-of-warranty petrol Toyota owners. Official T-CARE XTRA terms identify customer-paid scheduled services that can contribute to additional warranty eligibility. A paid job can therefore coexist with warranty coverage.',
 'The practical cohort becomes owners considering a customer-paid job outside relevant free or prepaid service entitlements. Vehicle age, odometer, prior service history and warranty status are separate attributes. Public locations cannot identify this cohort at the origin level.',
 'The primary spatial layer remains general petrol-Toyota workshop access. HEV/PHEV and BEV paths are separate because a general-service listing does not establish local competence for a high-voltage task.'
],table=[['Variable','Treatment'],['Payer / entitlement','Primary eligibility variable; unknown at individual origin'],['Warranty status','Separate; do not infer from payment'],['Prior provider','Required for recovery attribution; not observed'],['Model / job / parts','Required before comparing equivalent offers'],['Capacity and actual slot','Required before promising fulfilment']],note='No paid-job cohort size or switching probability is estimated. [CX09; SV05]')
page('Four access investigations; fifteen markets remain in view','Study design',[
 'The design combines a national contextual footprint with a purposive 15-market screen and four bounded urban windows. Surabaya, Medan, Bandung and Palembang offer verified official-directory evidence, contrasting locations and feasible road-routing comparisons.',
 'This is a comparative case design, not a representative sample of Indonesian motorists. The rectangles are analytical windows, not administrative metro boundaries. Their finite destination pools extend approximately 0.08 degrees beyond each origin window.',
 'Jakarta and other markets remain in the screening dataset. Their exclusion from detailed routing is a scope decision, not evidence of low opportunity. Data availability is documented separately from attractiveness.'
],table=[['Main window','Contrast investigated'],['Surabaya','Multiple branches and economical-channel operators'],['Medan','Non-Java urban access and alternative Toyota channels'],['Bandung','Basin/fringe access and suspect official directions'],['Palembang','River-city road structure and fewer focal branches']],note='The selection was refined after access tests and source discovery. It was not a blind preregistration. [C1; B1; P1]')
page('Selection is transparent, but it is not a demand ranking','Market screening',[
 'The 15-market screen records official geographic presence, archived charging context, observed OtoXpert listings and geographic contrasts. It leaves eligible Toyota-owner stock, workshop capacity and profit opportunity unknown.',
 'There are two complementary screens, each with 15 units: the contextual administrative-area screen and the Overture bounding-box acquisition screen. They are not the same set or geometry. Jabodetabek nests several context cities; some cities occur in only one screen. The crosswalk lists these differences. No combined ranking or total is calculated.'
],fig='figures/context_market_screen.png',caption='Context screen only; counts represent source records under each stated geography, not demand, market attractiveness or a complete provider census. [C1; P1]',note='Future market expansion should follow unresolved strategic questions and evidence quality, not simply the largest dot on this chart.')
page('Three location inventories answer different questions','Evidence architecture',[
 f'The Auto2000 workstream observed 155 directory cards and reconciled them to {N} unique name/coordinate entries. Repeated city-directory content does not establish additional branches. Some listings are showroom-only or body-and-paint locations.',
 f'The OtoXpert directory returned {len(ox)} listings with operator labels. The automotive-place workstream contains {P:,} extracted rows, of which {K:,} pass its candidate filters. Confidence scores, category labels and names do not verify Toyota fitment or a specific job.',
 'The archived SPKLU inventory adds 2,454 charging-site rows from June 2026. It answers a charging-context question and is not a branch inventory or current operation register.'
],table=[['Evidence unit','What it can support','What remains unknown'],['Official service card','Advertised general facility','Specific job, stock, capacity'],['Mapped automotive place','Candidate discovery','Identity, independence, fitment'],['Official OtoXpert listing','Operator and advertised location','Outlet/job fulfilment'],['Charging-site record','Historical mapped presence','Live access, uptime, queue']],columns=[CW*.25,CW*.34,CW*.41])
page('The observed branch footprint requires reconciliation','Official directory audit',[
 'Directory cards were collected across 48 city-directory labels. Some labels repeated other cities\' cards. The run preserves the original observations and a separate reconciled inventory rather than treating the card count as a verified national total.',
 'A general-workshop service tag was required for the main Auto2000 routing pool. A showroom or body-and-paint listing cannot silently serve as a destination for routine mechanical work. Even the retained general-workshop locations are not verified for the selected model/job.'
],fig='figures/context_national_channels.png',caption='Observed unique directory locations and OtoXpert embedded-map coordinate candidates. This is collected coverage, not a certified exhaustive national network. [B1; CX02-CX05]',note='The source map links are coordinate evidence, not field-confirmed entrances. Routing screens reduce but do not eliminate that uncertainty.')
page('An economical channel exists; operator identity changes the implication','OtoXpert',[
 f'The official directory yielded {len(ox)} entries, including 15 labelled Auto2000-operated. Other entries identify different dealer operators. A job retained in the Toyota ecosystem is therefore not automatically a job contributing to Auto2000.',
 'Published network counts also disagree: a March 2026 Toyota release states 40 outlets, the T-OPT page states 38, and this run returned 37 directory listings. These observations are preserved without asserting a reconciled live total.'
],fig='figures/context_otoxpert_operators.png',caption='Operator labels from the 37 observed OtoXpert listings; dates and source discrepancy remain explicit. [CX02-CX08]',note='Pilot design should examine channel economics and existing operator ownership before proposing a new budget network.')
page('Equivalent jobs remain a verification task','Service evidence',[
 'OtoXpert advertises an oil/gasket/filter package from IDR299,000 and an approximate 30-minute service. That is a network-level advertised starting offer, not a current quote for the selected Toyota variant or an available slot.',
 'Toyota also advertises brake work through OtoXpert and oil-filter/brake-pad categories in T-OPT. These sources justify testing existing economical routes. They do not establish actual outlet stock, fitment, installed price or service capacity.',
 'No matched, model-specific branch and independent-garage quotes were obtained in this public-data run. Accordingly, the report makes no measured dealer-price-premium claim and does not present the candidate road-access comparison as a like-for-like job choice.'
],table=[['Job','Evidence obtained','Still required'],['Oil + filter','Network offer; parts categories','Model/year, oil grade/volume, quote'],['Front brake pads','Network brake work; pad catalogue','Axle/fitment, labour, stock, final bill'],['xEV check/diagnosis','Programme and corporate statements','Branch/job eligibility and capability']],columns=[CW*.23,CW*.37,CW*.40],note='The primary deliverable is general-service accessibility with explicit capability uncertainty. [CX06-CX11; SV01-SV07]')
page('A parts-store category can hide a documented service option','Oil-service evidence / classification counterexample',[
 'The generic automotive filter excluded some Shop&amp;Drive records because the source classified them as auto-parts stores. Official issuer information nevertheless advertises oil and oil-filter services and names Toyota among supported brands. Category-only discovery can therefore miss relevant service pathways.',
 'The official Shop&amp;Drive directory supplied 425 structured location records. Supplementary routing adds 5,913 pairs to the main 76,221, totalling 82,134 model comparisons. Of the 425 official Shop&amp;Drive listings, 67 fall within the four expanded deep-dive rectangles: 28 Surabaya, 8 Medan, 22 Bandung and 9 Palembang. These are published coordinate candidates, not field-validated entrances or a claim about current workshop capacity.',
 'This prompted a disclosed supplementary analysis after the main candidate rules were frozen. The supplement improves service relevance but does not prove the exact current Toyota model/year, oil specification, filter fitment, stock or appointment.'
],fig='figures/official_oil_alternatives.png',caption='Collected Auto2000, OtoXpert and official Shop&Drive locations. Shop&Drive is a separate operator channel; ownership and contribution differ. Sources: official directories and network service documentation [S1; B1; CX02-CX08]. Cross-source overlaps are not summed as additional businesses.',note='The classification counterexample challenges a generic map-density narrative in both directions: irrelevant candidates may remain, while relevant service outlets may be excluded.')
combined=pd.read_csv(R/'workstreams/routing/supplement/combined_market_summary.csv')
rows=[['Study window','Auto2000 min','S&D min','OtoXpert + S&D min','Paired gap min']]
for _,z in combined[combined.scenario=='snap_le_250m'].iterrows():
 rows.append([z.market.title(),f'{z.auto2000_median_minutes:.1f}',f'{z.shopanddrive_median_minutes:.1f}',f'{z.advertised_oil_channels_median_minutes:.1f}',f'{z.median_paired_auto2000_minus_advertised_oil_minutes:.1f}'])
page('The documented oil-network scenario changes the comparator','Oil-service evidence / road access',[
 'The supplement routes every official Shop&amp;Drive record inside each expanded window, rather than only a purposively selected pair of outlets. It combines OtoXpert and Shop&amp;Drive as collected network-advertised oil channels while keeping operator identities distinct.',
 'The table applies the 250-metre snap rule. Marginal channel medians can use different valid-origin sets; paired gaps use origins where both options are available under the scenario. Full denominators and all-routed comparisons are retained in the supplementary CSVs.'
],fig='figures/oil_access_comparison.png',caption='Figure: all-routed 81 origins per market. Table: 250-metre snap-screened. Both show modelled access to published network locations, not confirmed equivalent job completion. [R1; S1]',table=rows,columns=[CW*.22,CW*.18,CW*.14,CW*.26,CW*.20])
page('Service advertising improves relevance, not proof of fulfilment','Oil-service evidence / limits and attribution',[
 'The supplementary evidence includes selected Dokter Mobil local pages explicitly advertising oil service and three geocoded other-authorised Toyota locations. Dokter Mobil scope may differ from a conventional oil/filter replacement. Its results remain a separate channel. The other-authorised sample is purposive and not an exhaustive Toyota-network inventory.',
 'An expired January 2026 Shop&amp;Drive campaign named an Avanza oil/filter bundle and brake fitting. It is historical evidence of an advertised offering, not a current price or guarantee of availability. Current network documentation is broader than a live model-specific quote.',
 'Official and Overture coordinates also disagree by about 227 metres for the selected Lontar outlet. Both versions are retained in the evidence table, with the official candidate preferred in the supplement. The near-threshold difference reinforces the need to check entrances before a customer-facing promise.'
],table=[['Evidence level','What it adds','What it does not establish'],['Official outlet identity','Published address/coordinate','Entrance, hours today or capacity'],['Network Toyota/oil/filter claim','Plausible service pathway','Current model/year/parts fit'],['Local oil-service advert','Outlet-level advertised scope','Equivalent bundle and final quote'],['Historical promotion','Dated model-specific advert','Current offer or stock']],columns=[CW*.28,CW*.34,CW*.38],note='S1: https://www.shopanddrive.com/outlet and /faq; outlet and claim locators are preserved in provider and alternative-evidence files. Astra-group affiliation does not automatically make these Auto2000-paid jobs.')


page('The denominator is a grid, not a customer base','Origin design',[
 f'The main routing run uses {orig} regular grid-cell centres across four windows. Each centre represents a sample location, with equal weight. It is not a residence, vehicle, workshop customer or population estimate.',
 'Grid design makes broad access patterns visible without using personal locations. It also samples industrial land, water-adjacent areas and low-density fringe. A road snap can move a sample centre away from its nominal location, so snap distance is retained.',
 'The run reports full-grid results alongside a 250-metre source/destination snap screen. Any additional origin-resolution checks are documented as sensitivities, not independent observations.'
],table=[['Interpretation','Allowed?'],['Share of sampled grid origins within 20 modelled minutes','Yes, with denominator and routing status'],['Share of Toyota owners served','No'],['Number of paid jobs available','No'],['Observed customer inconvenience','No'],['Locations worth investigating','Yes, as a research proposition']],note='Population weighting was not used to imply owner demand. The boundaries and exact origin coordinates are included. [R1]')
page('Route all listed candidates, then examine the model assumptions','Routing method',[
 f'The routing workstream queried OSRM tables across the finite inventoried destination pools. It produced {pairs:,} origin-destination rows, with raw responses, request logs and failed-route records retained.',
 'The nearest destination is selected by returned duration among OSRM-profile routes. Because the profile can optimise a weight distinct from duration, this is not a guarantee of the globally fastest time-minimising path. It is a consistent public model comparison.',
 'Distances and durations come from the routing response. No arbitrary road speed converts straight-line kilometres into minutes. The public service supplies neither observed congestion nor workshop waiting time. A shorter journey may still lead to an unsuitable or unavailable provider.'
],table=[['Check','Implementation'],['Destination search','All retained destinations in the stated window'],['Boundary treatment','Expanded destination window; core comparison retained'],['Snapping','Origin and destination snap distances recorded'],['Failures','Explicit files and completeness flags'],['Reproduction','Cached responses; reacquisition depends on service']],note='No circular straight-line buffer is presented as a travel-time isochrone. [R1; T1]')
page('A clean map cannot repair uncertain service capability','Interpretation ladder',[
 'The study separates four evidentiary steps: a place is listed; a service is advertised; a journey is modelled; a completed comparable job is verified. This run reaches the first three steps to different degrees, but not the fourth.',
 'The mapped candidate pool is deliberately useful for discovery and deliberately insufficient for a definitive substitution claim. A strict requirement for independently documented Toyota/model/job capability leaves no identified comparator set in this collection. This means the comparison is unknown, not that no capable garages exist.',
 'The maps therefore show where to verify alternatives and test a scoped offer. They cannot rank workshop quality, infer owner preferences or measure causation.'
],table=[['Layer','Report wording'],['Overture category/name filter','Mapped repair/service candidate'],['Official general-workshop tag','Documented general workshop'],['OtoXpert network service offer','Network-advertised job; outlet unconfirmed'],['OSRM response','Modelled profile-route access'],['Switching / incremental GP','Not measured']],note='This distinction applies symmetrically: an Auto2000 general-workshop listing also does not verify a particular high-voltage task. [B1; P1; R1; CX10-CX12]')
# Four local investigations: maps, access, counts and illustrative route evidence.
for market in ['surabaya','medan','bandung','palembang']:
 row=main[main.market.str.lower()==market].iloc[0]; sr=tight[tight.market.str.lower()==market].iloc[0]
 sub=oa[(oa.market.str.lower()==market)&(oa.scenario=='all_routed')]
 dest=pd.read_csv(R/f'workstreams/routing/inputs/{market}_destinations.csv')
 counts=dest.kind.value_counts(); ac=int(counts.get('auto2000',0)); ic=int(counts.get('independent',0)); oc=int(counts.get('otoxpert',0))
 place=market.title(); origins=int(row.grid_origins)
 page(f'{place}: study the documented footprint before interpreting density','Local investigation / footprint',[
  f'This window routes {origins} grid origins to {ac} collected Auto2000 general-workshop destinations, {oc} OtoXpert listings and {ic} mapped repair/service candidates. Destination filtering uses coordinates within the expanded rectangle, not the city label of the source page.',
  'The distinction matters at the fringe: a branch listed under another city can still be closer than an in-city branch. The candidate points are retained source records after stated name/category filters, not a complete census of independent garages.'
 ],fig=f'figures/providers_{market}.png',caption='Origin rectangle, expanded destination window and collected points. Map scale is geographic; any grey traces are selected model routes, not the full road network. [B1; P1; R1]',note='Use this map to locate verification work. A dense cluster of markers does not establish interchangeable service, sufficient capacity or customer demand.')
 page(f'{place}: the travel gap varies across sample locations','Local investigation / access',[
  f'Under the 250-metre snap screen, {int(sr.paired_origins)} of {origins} origins have paired durations. Their median Auto2000-minus-candidate gap is {sr.median_paired_additional_minutes:.1f} minutes. Auto2000 is faster at {int(sr.origins_auto2000_faster)} retained origins and slower at {int(sr.origins_auto2000_slower)} under this finite-pool model.',
  'Positive cells indicate a longer modelled journey to the nearest collected Auto2000 general workshop than to a mapped candidate. Negative cells indicate the reverse. Neither sign identifies an owner\'s preferred or technically suitable provider.'
 ],fig=f'figures/gap_{market}.png',caption='250-metre snap-screened paired durations at grid origins; grey crosses identify excluded/unpaired locations. No continuous isochrone is inferred. [R1]',note='The relevant commercial next step is to verify the nearest candidates and compare a real scoped offer at selected positive-gap and low-gap origins.')
 ct=[['Channel','Median min','Origins <=10min','Origins <=20min','Origins <=30min']]
 for kind,label in [('auto2000','Auto2000 general'),('independent','Mapped candidates'),('otoxpert','OtoXpert listings')]:
  value=row.get(kind+'_median_minutes');ct.append([label,f'{value:.1f}' if pd.notna(value) else 'Unknown',int(row.get(kind+'_origins_le_10min',0)),int(row.get(kind+'_origins_le_20min',0)),int(row.get(kind+'_origins_le_30min',0))])
 page(f'{place}: thresholds describe reach, not the size of a prize','Local investigation / comparison',[
  f'The Auto2000 channel median is {row.auto2000_median_minutes:.1f} modelled minutes, compared with {row.independent_median_minutes:.1f} for the candidate pool. These marginal medians differ from the median paired gap because the closest destinations and relative burden vary by origin.',
  f'The stricter 250-metre snap scenario retains {int(sr.paired_origins)} paired origins and gives a median paired gap of {sr.median_paired_additional_minutes:.1f} minutes. Changing the sample through a snap rule can change the result; it does not confirm the excluded locations are invalid customer origins.'
 ],table=ct,columns=[CW*.28,CW*.16,CW*.19,CW*.19,CW*.18],note=f'The denominator is {origins} sampled grid origins for the full run. Differences between channels concern collected locations, not comparable completed jobs. Confidence and literal car-name sensitivities are supplied separately. [R1]')
 routes=j('workstreams/routing/output/illustrative_routes.geojson')['features'];rr=[x['properties'] for x in routes if x['properties']['market'].lower()==market]
 vals=[]
 for example in ['minimum_gap','median_gap','maximum_gap']:
  z=[x for x in rr if x['example']==example]
  if len(z)==2:
   a=next(x for x in z if x['kind']=='auto2000');d=next(x for x in z if x['kind']=='independent');vals.append([example.replace('_',' '),a['origin_id'],f"{a['duration_seconds']/60:.1f}",f"{d['duration_seconds']/60:.1f}"])
 page(f'{place}: inspect routes behind the averages','Local investigation / counterexamples',[
  'The map illustrates the middle paired-gap origin in the all-routed scenario. The table also records the minimum and maximum cases. These are explanatory selections, not sampled customers. High-snap origins can remain in this illustrative scenario even when excluded from the primary screened maps.',
  'Profile-route geometry can expose a detour hidden by straight-line distance. However, a route trace alone does not identify whether a particular bridge, toll, turn restriction or traffic condition caused the gap. Those explanations require route-level checking.'
 ],fig=f'figures/route_detail_{market}.png',caption='All-routed middle-gap case; endpoint snap distances are annotated. Routes illustrate model geometry, not verified customer travel or strict-screen results. Three-case high-resolution panels are included in the ZIP. [R1]',table=[['Selected case','Origin ID','Auto min','Candidate min']]+vals,columns=[CW*.32,CW*.20,CW*.24,CW*.24])

page('Branch overlap is a geographic sensitivity, not spare capacity','Branch-level analysis',[
 'The run also evaluates the 27 Auto2000 destinations inside the four expanded windows. For each, it counts sampled origins for which that branch is nearest, reachable within 20 modelled minutes, and affected when the branch is omitted from the finite destination set.',
 'This leave-one-out calculation diagnoses geographic dependence. It does not simulate a real closure, workload redistribution, spare workshop capacity or revenue effect. Another branch can be geographically close while unable to absorb a particular job.',
 'The 12 focal branches are the top three within each market by nearest screened-grid coverage, with a documented tie-breaker. This is a transparent analytical selection, not a statement that they are the best commercial pilots.'
],fig='figures/branch_influence.png',caption='Focal branches selected using the 250-metre snap-screened finite grid. Counts are sampled origins, not customers or work orders. Full 27-branch results and alternative scenario rows are included. [R1]',note='The focal set provides branch-level research propositions; it is not 12 independently validated field catchments.')
focal=pd.read_csv(R/'workstreams/routing/output/focal12_branches.csv').fillna('')
fr=[['Market / branch','Nearest grid origins','Origins lose <=20min access if omitted']]
for _,z in focal.iterrows():fr.append([z.market+' / '+z.branch_name,int(z.origins_nearest_this_branch),int(z.origins_losing20min_access_if_removed)])
page('Twelve focal branches expose different kinds of geographic dependence','Branch-level comparison',[
 'A branch may serve many nearest sample origins yet have nearby Auto2000 substitutes; another may serve fewer origins but be the only collected branch within the chosen threshold for some locations. Those are different access patterns.',
 'Before selecting a pilot, verify the actual entrance, relevant workshop competence, appointment capacity and owner cohort at each candidate. The table is a prioritisation aid for that verification.'
],table=fr,columns=[CW*.58,CW*.18,CW*.24],note='The denominator varies with the snap screen and available routes. Omission sensitivity concerns collected Auto2000 destinations only, not the complete Toyota network or customer substitution. [R1]')

page('Compare distributions before selecting a market','Cross-market synthesis',[
 'A city-wide median compresses variation across origins. The cumulative curves show how quickly each collected channel becomes reachable across a fixed, equal-weight grid. They do not estimate the share of local motorists using that channel.',
 'Market windows differ in dimensions and urban composition. Cross-market differences therefore combine network structure, observed provider coverage, selected window and routing model. They are suitable for comparative investigation, not an investment league table.'
],fig='figures/travel_cdf.png',caption='Empirical distributions of model durations across sampled origins, separated by channel and market. Failed/unavailable cases remain in the data with explicit status. [R1]',note='Within-market contrasts are generally easier to interpret than a claim that one city has more commercial opportunity than another.')
page('A 20-minute threshold does not create equivalent choice','Reachable choice',[
 'Threshold summaries help identify where the collected Auto2000 network is geographically competitive and where additional travel may deserve investigation. The same threshold is applied to every sampled origin and channel.',
 'Mapped candidate choice can be overstated by specialist or misclassified records and understated by excluded categories. A dedicated oil-service chain may be tagged as an auto-parts store, while a motorcycle business may carry a generic automotive category. The source category is not a service certificate.'
],fig='figures/access_20_minutes.png',caption='Sample origins with a reachable destination within 20 modelled minutes. Counts do not measure opening-hour overlap, appointment availability or verified Toyota job eligibility. [R1; P1]',note='The independent review found potentially non-comparable candidate names. Those records motivate explicit-name and documented-channel sensitivities rather than silent retrospective deletion.')
page('Snapping and boundary assumptions change what is being compared','Robustness / geography',[
 'A grid point can be away from a routable road, and a destination coordinate can lie inside a large site. The analysis retains snap distances and compares the main run against a 250-metre screen. Additional 100/500-metre diagnostics examine threshold dependence.',
 'The destination search extends beyond the origin rectangle. Core-only comparisons show whether omitting those outside destinations would alter the nearest observed option. A fixed margin reduces clipping risk but cannot establish that all relevant providers beyond it are irrelevant.'
],fig='figures/snap_sensitivity.png',caption='Main and snap-screened results may use different retained origin sets. Treat changes as model/sample sensitivity, not statistical confidence intervals. [R1]',note='The study is a finite inventory calculation, not a probability sample. Sampling confidence intervals would obscure the more important inventory and modelling uncertainty.')
page('Capability uncertainty is larger than a clean category label','Robustness / provider evidence',[
 'The candidate filters remove explicit motorcycle/truck/bus and other unsuitable names, require source confidence and select repair/service categories. These rules are transparent screening heuristics, not a calibrated probability of car-service competence.',
 'A deterministic independent review of retained records identified names such as Bike Point, helmet-related businesses and body/paint specialists. These are flags for follow-up rather than field-confirmed false listings. Conversely, documented oil-service outlets can be absent from the generic category pool.'
],fig='figures/candidate_filter_retention.png',caption='Automotive source rows and retained generic repair/service candidates. Counts describe filter behaviour, not workshop market share. [P1; independent review]',note='The strict comparable Toyota/model/job set remains unidentified. The report therefore avoids a measured price-premium, service-quality or switching claim.')
page('The size of the gap depends materially on the candidate definition','Robustness / magnitude',[
 'The baseline comparison gives the largest generic candidate pool. Restricting it to source confidence at least 0.9 or explicit car-name wording lengthens some candidate journeys and reduces the paired Auto2000 gap. This means the magnitude is not robust to provider definition.',
 'These stricter definitions are not validated truth. Generic names can describe capable workshops, and a high-confidence record can still be a motorcycle or specialist business. The useful conclusion is that a precise competitive burden requires verified provider identity and job scope.',
 'All three displayed provider definitions use the same all-routed origin grid. They should not be confused with the separate 250-metre snap screen, which changes the paired sample.'
],fig='figures/candidate_sensitivity_comparison.png',caption='Same main OD matrices, different provider membership. Alternative calculations add no new source observations or customer evidence. [P1; R1; independent review]',note='A single baseline minute gap should not be used as the input to a financial forecast.')

page('xEV support depends on documented local capability','Supporting xEV analysis',[
 'Toyota publishes Hybrid Health Check eligibility and certificate information, including HEV/BEV references. Corporate readiness statements also describe electrified-vehicle support. These establish programme and company-level capability claims, not a branch-by-job high-voltage roster.',
 'No complete local register of battery-diagnostic competence, appointment capacity or applicable warranty handling was obtained. General Toyota workshop proximity cannot be relabelled as verified BEV diagnostic access. The nearest general-service destination is a starting contact, not a promised resolution.',
 'A useful Digiroom ownership path would need to identify the vehicle and concern, check programme eligibility, confirm a competent destination and show case ownership through resolution. This is a proposed verification and fulfilment test, not functionality proven absent from current systems.'
],table=[['Path','Geographic finding','Missing evidence'],['Routine petrol job','General workshop/candidate road access','Equivalent offer and capacity'],['HEV check','Published programme; general locations','Branch-specific eligibility and capability'],['BEV concern','Corporate support; mapped locations','Diagnosis, claim and resolution path']],columns=[CW*.23,CW*.37,CW*.40],note='Some programme wording differs across current pages. Confirm actual vehicle eligibility rather than combining headline ages or years. [CX10-CX12]')
page('Charging remains context, not the centre of the workshop case','Supporting charging analysis',[
 'The June 2026 archive contains 2,454 consolidated station rows and 3,767 charger-box records. These grains cannot be combined into a single number of operating service opportunities. Provider and venue classes include name-based inference.',
 'Earlier archive robustness work found that nearby mapped alternatives often remain within five straight-line kilometres under stricter filters, while close-range counts change markedly. That result does not verify public access, compatibility, queues or current uptime.',
 'Charging geography can help frame a BEV ownership discussion. It does not establish paid workshop demand and should not displace the service-access question simply because a national charging dataset is convenient to analyse.'
],fig='figures/province_charging.png',caption='Top provincial counts in the archived charging-source snapshot. No all-car or BEV denominator is used here. Historical boundary and vehicle-stock discontinuities remain in the archive notes. [A1]',note='The national charging map is an historical context layer, not a November 2026 live availability tool.')
page('The strategy should follow the observed constraint','Commercial interpretation',[
 'The documented oil-network comparison is close to geographic parity in the Medan sample, with a median paired gap of about 0.3 minute. It does not support treating all four markets as one large access-deficit problem. The geographic study supports different tests in different catchments. Where a collected Auto2000 workshop is accessible, a scoped and transparent offer may be worth testing after capability and capacity checks. Where access is materially worse, a price-only intervention may leave the travel burden unresolved.',
 'Existing OtoXpert routes and economical parts should be considered before inventing a new tier. But an operator outside Auto2000 can retain work within Toyota while producing a different Auto2000 financial result. Operator-specific contribution must be checked.',
 'No geographic result proves that customers perceive a premium, distrust the dealer, value pickup or would change provider. Those remain rival explanations for a subsequent pilot. The current run deliberately excludes new customer-account/review research.'
],table=[['Access pattern','Next discriminating test'],['Low modelled burden','Comparable scoped quote and confirmed slot'],['High burden, eligible service route nearby','Operator economics and routing acceptance'],['High burden, no documented option','Pickup/home-service feasibility and capacity'],['xEV capability unclear','Vehicle/concern triage and branch confirmation']],note='These are proposed tests informed by geography, not commercially validated recommendations.')
page('Select pilot cells, not a city-wide winner','Pilot design',[
 'A practical next step is to choose contrasting origin/catchment cells within the studied markets: low and high modelled Auto2000 burden, with strong and weak evidence about alternatives. That creates tests of the mechanism rather than a single city ranking.',
 'For a specified Toyota vehicle and paid job, obtain comparable prices, fitment, earliest slots and turnaround. Verify the owner\'s actual previous provider and applicable entitlements. Then compare the improved offer with current practice across channels.',
 'The outcome should be incremental completed work and realised contribution after displacement, discounts and capacity constraints, not app bookings alone. The public study does not supply those business effects.'
],table=[['Gate','Evidence needed before scaling'],['Equivalent job','Model/year, parts grade, labour, tax and scope'],['Real service option','Correct entrance, hours, competence and slot'],['Eligible owner','Payer, entitlement and prior provider'],['Incrementality','Completed all-channel jobs against comparison'],['Economics','Operator/payer margin and incremental costs']],note='A branch can look geographically attractive and still be unsuitable if it cannot fulfil the offer. [CX06-CX09; R1]')
page('What the study does not establish','Limits and unresolved questions',[
 'The four rectangular windows and equal-weight origins are analyst choices. Provider records are incomplete and may be wrong. Some official links conflict with addresses. Source confidence is not service competence. The boundary margin is finite and destination entrances were not field-verified.',
 'The routing profile does not observe traffic, queues, opening-hour alignment or appointment availability. Nearest-by-returned-duration is a model comparison. Published service information is not an actual accepted quote or completed job.',
 'No eligible Toyota-owner stock, competitor market share, customer preference, switching probability, utilisation, workshop capacity, incremental work order or realised profit is measured. The findings should be used to prioritise verification and experiments.',
 'The work was performed and reviewed by AI agents using public sources. Independent agent criticism is recorded, but it is neither human peer review nor field validation. No theoretical or causal finding is inferred merely from map density.'
],note='Uncertainty is attached to the claim it affects, rather than hidden in one generic disclaimer.')
page('Failures changed the workflow and remain in the evidence','Acquisition record',[
 'Direct Auto2000 and OtoXpert website requests returned access errors. Official pages were instead retrieved through public web access, with concise facts and source locators retained. Complete third-party page bodies were not redistributed.',
 'Global Overpass requests failed on tested endpoints. A regional Swiss endpoint was not an Indonesian data source. Overture\'s public catalogue was accessible; its cloud data required explicit proxy configuration in this runtime. This enabled the automotive-place extracts without paid services.',
 'Public OSRM routing succeeded. Requests were bounded, paced and cached. Reacquisition is not guaranteed to yield the same map snapshot or profile. Cached responses support inspection and offline recalculation of the recorded comparisons.'
],table=[['Attempt','Outcome','Consequence'],['Overpass global endpoints','Errors/timeouts','Use Overture; do not infer no garages'],['Official direct HTTP','403/access blocks','Public web fact extraction'],['Overture default cloud access','DNS/access issue','Explicit proxy; release frozen'],['OSRM tables','Returned model matrices','Retain requests, snaps and failures']],columns=[CW*.31,CW*.29,CW*.40])
page('What was achieved, and what remains unmeasured','Scope receipt',[
 'The run expanded provider discovery and added official oil-network evidence, while retaining clear limits on service comparability. The table distinguishes completed geographic work from research that public sources did not establish.',
 'The four market windows contain 27 routed Auto2000 destinations and 12 selected focal branches. The focal comparisons are computed access investigations, not field studies of branch operations.'
],table=[['Planned dimension','Achieved scope'],['Market breadth','15 administrative context selections and 15 different POI bbox windows; explicit crosswalk'],['Local depth','Four windows; 324 main grid origins; 27 Auto2000 destinations; 12 focal branches'],['Independent alternatives','Mapped candidate pool plus separately documented oil-network scenario'],['Two comparable paid jobs','Network/public service evidence; no matched model-specific current quote set'],['Origin robustness','Snapping and nested/central origin subsets; no population weighting or shifted-grid experiment'],['xEV access','Programme/corporate evidence; no branch-by-job high-voltage roster'],['Commercial result','Pilot hypotheses; no measured switching, utilisation or incremental profit']],columns=[CW*.28,CW*.72],note='These limits are conclusions about evidence obtained, not claims that the missing services or opportunities do not exist.')

page('The package separates observation from calculation','Reproducibility',[
 'The source pack includes relevant archive inputs, automotive source extracts, official-directory fact tables, provenance, routing responses, intermediate tables and figure/report scripts. Contact fields and unrelated all-category places are excluded from the automotive extracts.',
 'Offline summaries can be recalculated from included files. Reacquiring changing public sources is a separate process with network and access dependencies. The package does not claim a tested one-click replay of every browser or search action.',
 'The interactive explorer is a standalone analytical HTML file. Its grid and point layers work without a tile service or CDN. The absence of background street tiles is deliberate; illustrative polylines remain selected routes rather than a complete road map.'
],table=[['Folder','Contents'],['sources/','Frozen relevant inputs; attribution and hashes'],['workstreams/','Acquisition, classification, matrices and reviews'],['analysis/','Derived context and summarised outputs'],['figures/ and maps/','Static figures and offline explorer'],['scripts/ and report/','Report source and final PDF'],['qa/','Checks, page layout and review records']],columns=[CW*.32,CW*.68])
# Source reference pages split into manageable tables with live URLs in text.
sources=pd.read_csv(R/'workstreams/context/sources.csv').fillna('')
for start in range(0,len(sources),5):
 rows=sources.iloc[start:start+5]
 paras=[]
 for _,z in rows.iterrows():paras.append(f"<b>{z.source_id}. {z.title}</b><br/>{z.publisher}. Published: {z.published_date or 'not stated'}. Retrieved 14 November 2026.<br/><link href='{z.url}' color='#236a75'>{z.url}</link>")
 page('Sources and claim locators','References / official context',paras=paras,note='Source IDs resolve the bounded factual claims in the service and context evidence tables. Long page bodies and customer reviews are not redistributed.')
page('Technical sources and evidence files','References / spatial and data',[
 '<b>A1. Archived charging and statistical context.</b> Wiputra and Santiadi (2026), SPKLU dataset V2, snapshot 16 June 2026, DOI 10.17632/z2bvd5r574.2, CC BY-NC 3.0. Relevant archived reports and input hashes are in sources/archive_inputs/ and archive_input_manifest.json. BPS/Polri URLs accompany the vehicle-stock table.',
 '<b>B1. Official branch evidence.</b> workstreams/branches/directory_source_register.csv; original card facts, reconciled inventory, excluded coordinate cases and BRANCH_METHODS.md. Official source URLs and dates are recorded per observation.',
 '<b>P1. Provider discovery.</b> Overture Maps Places release 2026-10-21.0; raw selected automotive extracts, source dataset/license fields, GERS IDs, study windows and PROVIDERS_METHODS.md. Source/category confidence is not job competence.',
 '<b>R1. Road access.</b> workstreams/routing/inputs/, output/, cache/ and acquisition logs. API: https://router.project-osrm.org . Documentation: https://project-osrm.org/docs/v5.24.0/api/ . OpenStreetMap contributors, ODbL attribution: https://www.openstreetmap.org/copyright .',
 '<b>C1. Market screen.</b> workstreams/context/screening.csv and CONTEXT_FINDINGS.md. Descriptive counts are not an opportunity rank.',
 '<b>T1. Context mapping.</b> Natural Earth public-domain country outlines. https://www.naturalearthdata.com/about/terms-of-use/ . Coastlines are small-scale context, not validated local boundaries.'
],note='The source pack retains upstream attribution and restrictions. There is no blanket commercial licence over all third-party material.')
# Add late completed sensitivity and documented-service material here through appendix pages.
if (R/'workstreams/routing/sensitivity/sensitivity_summary.csv').exists():
 page('Sensitivity calculations are alternative views of the same evidence','Appendix / sensitivity',[
  'The supplementary outputs vary source confidence, explicit car-name wording, snap thresholds and destination boundary restrictions. They reuse the same observed provider records and road matrices, so they add no new customers or independent field evidence.',
  'Literal car-name filtering can remove capable workshops with generic names, while high confidence can retain a confidently classified motorcycle or specialist business. These scenarios reveal measurement dependence; none becomes ground truth by being stricter.',
  'Inspect the row-level sensitivity files alongside the main market summary. Compare both the reported duration and the retained origin count. A changed denominator can explain an apparent improvement.'
 ],fig='figures/gap_distributions.png',caption='Origin-level paired-gap distributions in the main model. Source and model limitations apply to every point. [R1]')

c.save();(R/'report/report_content.json').write_text(json.dumps(spec,indent=2));(R/'qa/pdf_layout_bounds.json').write_text(json.dumps(qa,indent=2));print(f'{PAGE} pages -> {OUT}')
