"""Build source-scoped checks of supplied friend research. No deployment claims."""
import csv, json, hashlib
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[2]
AR25 = 'https://r2.astra.co.id/annual-reports/documents/Astra-Annual-Report-2025.pdf'
AR24 = 'https://r2.astra.co.id/annual-reports/documents/Astra-Annual-Report-2024.pdf'
VENDOR = 'https://suitmedia.com/work/astra-sam'

sources = [
 dict(source_id='FC-S01', title='Astra Annual Report 2025', url=AR25, ownership_cluster='Astra corporate reporting', year_covered=2025, source_type='Issuer primary annual report', sha256='713cc7b9ab22df7c8c80af27c66aa323838e5027f8804b61ba3a3754fddc5628', independence_note='Independently retrieved from official public host; same issuer and underlying document as friend citation, not a new independent corroborating study.', limits='Operating capability statements are issuer descriptions. Do not extend financial-statement audit assurance to every operational claim; no branch usage logs, APIs, uptime or causal effects.'),
 dict(source_id='FC-S02', title='Astra Annual Report 2024', url=AR24, ownership_cluster='Astra corporate reporting', year_covered=2024, source_type='Issuer primary annual report', sha256='84f812b5011ada65188737598fd2ae411b9086f43d734024eb9b8a995baae170', independence_note='Same issuer as FC-S01; longitudinal disclosure, not independent corroboration.', limits='Historical disclosure, not a current availability or adoption audit.'),
 dict(source_id='FC-S03', title='Astra: Making Sales Activity Management Work Across Devices', url=VENDOR, ownership_cluster='Suitmedia vendor case study', year_covered='Page labels project 2016–2016; publication date not established', source_type='Primary supplier description', sha256='5d43f5ec47a5def9e304a724a0adca5fdf45cb37a20420c8bfd4722f66203464', independence_note='Separate supplier ownership but commercial interest; implementation description, not an independent outcome evaluation.', limits='Do not assume described SAM Advance version, interfaces or access rights remain current. No measured adoption denominator or causal design.'),
]

claims=[]
def c(n, subject, claim, status, finding, scope, pages='', limitation='', implication='', source='FC-S01'):
    claims.append(dict(claim_id=f'FC{n:02d}', subject=subject, supplied_claim_or_inference=claim, status=status, verified_finding=finding, entity_and_time_scope=scope, source_ids=source, printed_pages=pages, pdf_pages_1based=','.join(str(int(x)+2) for x in pages.split(',') if x.isdigit()), limitation=limitation, research_implication=implication, causal_effect_established=False))

c(1,'SAP S/4HANA','All Auto2000 branches targeted for end-2026','confirm','The 2025 report gives end-2026 as the target for completion across all Auto2000 branches.','Auto2000; target disclosed in FY2025 report','124','Target is not completion evidence as of 11 November 2026.','Treat rollout state as a possible source of branch heterogeneity, not a completed common foundation.')
c(2,'SAP S/4HANA','All Auto2000 branches already fully migrated','unverified','No official completion notice was located in the retrieved current-search results; the report only supplies a target.','Auto2000; current completion date','124','Search coverage cannot establish absence. Individual staff profiles were excluded as proof of nationwide completion.','Do not predicate analysis on universal migration or universal failure.')
c(3,'SAP S/4HANA','The completed rollout statement applies to Auto2000','qualify','The completed integration statement names ASMO3; the Auto2000 statement is a subsequent target.','ASMO3 versus Auto2000; FY2025','124','These are different sales operations.','Keep named business units separate.')
c(4,'Sales Activity Management','SAM already supports dealer sales','confirm','Astra reports SAM supporting activity from leads to vehicle unit sales.','Astra dealer/frontline ecosystem; FY2025','125','No active-user count, lead completeness or Auto2000 branch usage rate.','A proposal for a basic new sales activity tool overlaps a disclosed baseline.')
c(5,'After-sales frontline systems','Reminder Service and MSA already exist','confirm','The report identifies Reminder Service and Mobile Service Advisor as after-sales support applications.','Astra dealer/frontline ecosystem; FY2025','125','Existence does not establish an EV job-specific workflow, reminder receipt, usable slot inventory or advisor adoption.','Separate existing workflow from the unresolved quality of handoffs.')
c(6,'Management analytics','Auto Intelligence already supports monitoring','confirm','The report names Auto Intelligence for branch and head-office monitoring.','Astra dealer/frontline ecosystem; FY2025','125','No public event schema, customer-outcome attribution or exported dataset.','A new generic dashboard requires a distinct decision gap to justify novelty.')
c(7,'Identity and CRM','Single ID / Customer 360 already exists','confirm','The 2025 report describes Single ID, consolidated customer interactions, consumer/frontline platforms, analytics and marketing automation.','Astra dealer ecosystem; FY2025','126','An architectural claim is not proof of universally correct linkage or accessible records for every advisor.','The relevant hypothesis concerns usable identity at the decision moment rather than the total absence of identity technology.')
c(8,'Identity and CRM','Existing Single ID means customer context is usable in every branch','unverified','The annual report does not disclose branch usability, match/error rates, permissions, or how missing/duplicate identities are handled.','Auto2000 branches and advisors','126','No linked customer-to-work-order microdata or field adoption study.','Keep case testimony on difficult usage compatible with reported system existence.')
c(9,'AI','Astra has deployed multiple AI applications','qualify','The report describes corporate audit/tax/HR/knowledge tools and separate motorcycle inventory AI; mobile frontline discussion also mentions GenAI.','Multiple Astra functions; FY2025','125,126','These examples do not establish an Auto2000 EV-diagnostic model, consumer recommendation system, model accuracy or economic uplift.','Do not transfer group-level AI examples into an Auto2000 EV capability claim.')
c(10,'Motorcycle systems','DMS/NMS/GIS/Smartstock are Auto2000 vehicle systems','qualify','The relevant DMS/NMS/GIS and Smartstock passages explicitly concern motorcycle dealers.','Two-wheel operations, not automatically Auto2000','124,126','The source provides no basis to assign those exact systems to Auto2000.','Exclude cross-business capability leakage.')
c(11,'Single ID history','Single ID would be an entirely new initiative','qualify','The 2024 report explicitly describes implementation for Auto2000 and Daihatsu Sales Operation customers.','Auto2000 and Daihatsu; FY2024','125','Historical existence does not establish 2026 adoption, accuracy or outcomes.','The novelty bar for a basic unified customer profile is already high.',source='FC-S02')
c(12,'EV outlet footprint','31 Auto2000 outlets provide integrated EV ecosystem service','confirm','The FY2025 Toyota section reports 31 Auto2000 outlets with integrated EV ecosystem service.','Auto2000 outlet footprint in FY2025','137','No named branch list, service/job matrix, technician roster, battery-test coverage or live appointment capacity.','Use 31 as a reported footprint, not 31 interchangeable job-capable service locations.')
c(13,'Charging footprint','Toyota has 118 charging locations','qualify','The sidebar totals 118: 113 Toyota dealer locations, two rest-area locations and three mall locations.','Toyota network footprint in FY2025','138','Not 118 Auto2000 sites, not connector count, and not live availability/uptime.','Distinguish location coverage from access, compatibility, capacity and operational reliability.')
c(14,'Existing Digiroom scope','Digiroom already has sales and after-sales functions','confirm','The report lists new-car purchase, service booking, tracking, test drive and trade-in.','Auto2000; FY2025','138','Feature lists do not verify completion or incremental customer outcomes.','Booking, test-drive and trade-in labels alone are not new solution directions.')
c(15,'Loyalty','A new loyalty program would fill a blank baseline','qualify','Auto2000 already reports Bronze–Platinum tiers based on transactions and Astrapoints/voucher benefits.','Auto2000; FY2025','139','No eligible base, redemption rate, lift or program-cost evidence here.','Any loyalty direction needs a distinct unmet incentive or coverage gap.')
c(16,'TASIA','Auto2000 lacks an existing chatbot','qualify','TASIA is reported on website, Digiroom and WhatsApp, including product/service/order/finance information.','Auto2000; FY2025','139','Accuracy, response coverage, human escalation and resolution rates are not established.','Generic chatbot novelty is weak; unresolved customer jobs matter more.')
c(17,'OEM digital ecosystem','mTOYOTA and T-Intouch are already present','confirm','TAM lists T-Intouch via mTOYOTA, mTOYOTA, TARRA, Halobeng and Toyota Mobile Service.','TAM/Toyota ecosystem; FY2025','138','Not all are owned by Auto2000; no public permission to reuse data or integrate statuses.','Separate ecosystem overlap from legal/technical access.')
c(18,'Trade cycle','Trade Cycle Management and trade-in collaboration are new concepts','qualify','TAM reports Trade Cycle Management and used-car trade-in collaboration with OLX.','TAM; FY2025','141','No measured retention effect or guaranteed future residual price.','The unsolved gap may be valuation evidence or execution rather than absence of trade-in.')
c(19,'OLXmobbi','A Toyota dealer trade-in partner path already exists','confirm','OLXmobbi reports expanded trade-in cooperation with Toyota and Daihatsu dealer networks.','OLXmobbi and Toyota/Daihatsu networks; FY2025','181','Does not establish each Auto2000 branch agreement, battery-certificate acceptance, shared customer permissions or funded price guarantee.','A partner footprint does not automatically confer contracts or residual-risk transfer.')
c(20,'After-free-service economics','Affordable alternative parts and alternative workshops are absent','qualify','TAM reports T-OPT for customers after free routine service and OtoXpert as a second workshop channel.','Toyota ecosystem; FY2025','137,141','No public measured cross-channel retention or Auto2000 margin allocation.','A lower-price retention option can overlap another existing ecosystem channel.')
c(21,'National market','National car market was about 804k and down 7%','confirm','The report states approximately 804 thousand national cars and a 7% decline, citing GAIKINDO.','National cars; FY2025','134','Rounded aggregate; retain wholesales/retail and vehicle coverage caveats when combining other series.','This is market context, not Auto2000 demand or dealer performance.')
c(22,'Group market share','Astra had 51% national share','qualify','The reported 51% is Astra Group car market share.','Astra Group; FY2025','134','Not Toyota-only, not Toyota HEV share, and not Auto2000 share.','Keep group, distributor, brand and dealer denominators distinct.')
c(23,'National xEV','National xEV was about172k,+72%,22% of cars','confirm','The report defines xEV as BEV+HEV+PHEV and reports rounded 172k,+72%,22%; BEV13% and HEV8%.','National new-car xEV; FY2025','135','Rounded shares do not add exactly to total. Do not overwrite case175,144/+69.7% using this number.','Preserve conflicting source versions and definitions rather than silently harmonizing.')
c(24,'Toyota and Lexus sales','Toyota and Lexus xEV sold37,693 in2024 and31,668 in2025','confirm','The chart confirms37,693 and31,668 xEV, alongside total domestic sales291,566 and251,954.','Toyota AND Lexus; FY2024/FY2025','140','Dealer volume, installed base and separate HEV/PHEV/BEV counts are not supplied by this chart.','Use a brand-portfolio acquisition signal, not an Auto2000 retention measure.')
c(25,'Auto2000 xEV volume','The Toyota/Lexus xEV chart measures Auto2000 xEV sales','unverified','The chart is explicitly Toyota and Lexus, not Auto2000.','Auto2000 dealer; FY2024/FY2025','140','No valid dealer conversion factor in this source; case coverage estimate is not a substitute.','Do not allocate sales to Auto2000 by an unsupported multiplier.')
c(26,'Electrification penetration','Toyota/Lexus adoption was lower than national adoption','qualify','The chart implies xEV sales mix12.57% in Toyota/Lexus2025 versus about22% reported nationally.','New-car sales mix, brand portfolio versus market','135,140','This is not owner adoption, not installed-base mix, not matched model/customer demand, and category/channel definitions require alignment.','Portfolio availability and national segment mix are plausible rival explanations for sales differences.')
c(27,'Case/source discrepancies','External AR numbers can replace casebook estimates','qualify','AR172k/+72% national and31,668 Toyota+Lexus differ from friend-reported case175,144/+69.7% and approximately33,950 Toyota.','Different document versions/brand coverage/bases','135,140','The cause of discrepancies is not confirmed; rounding alone is not established. Friend transcription is not a new check of casebook.','Preserve casebook as its own competition baseline and flag unresolved external differences.')
c(28,'SAM vendor history','There is a public supplier description of SAM Advance','confirm','Suitmedia describes rebuilding Auto2000 SAM as a cross-device web application using core-system interfaces; page labels project2016–2016.','Historical supplier case, retrieved2026','','Publication date and exact deployment date not established; current code/version/API access and quantified effects unverified.','Supports that the basic advisor-tool concept predates this proposal.',source='FC-S03')
c(29,'Integration feasibility','Existing internal systems are publicly accessible for new work','unverified','The sources describe applications and architecture but provide no public APIs, scopes, partner agreements or credentials.','Researcher/team access and prospective integrations','','A referenced interface in a historical vendor story is not present access authorization.','Keep solution feasibility conditional on actual permissions and data availability.',source='FC-S01;FC-S03')
c(30,'Entity roles','TAM and Auto2000 are interchangeable operating units','qualify','TAM is the50/50 Astra–Toyota brand-holder/importer/distributor; Auto2000 is one of its dealers.','Corporate/entity structure; FY2025','136','OEM data, dealer systems, finance, insurer and used-car partners have different rights and economics.','Shared group affiliation does not consolidate customer promises, budgets or margin ownership.')
c(31,'Battery certificates','The first digital retrieval of a Toyota battery certificate would be new','qualify','A current public Toyota HHC route exposes chassis validation, personal details and download stages.','Current Toyota OEM route; 11 November 2026','','No VIN entered or certificate obtained; completeness and appraisal acceptance remain unknown.','The candidate distinction is consented use in appraisal and useful context, not the first digital certificate.',source='JX02;M015')
c(32,'Service cost guidance','Model-specific service cost guidance does not exist','qualify','The current Toyota T-CARE tool shows variant-specific service rows, but its stated estimate basis is March 2024.','Current public tool with historically dated cost assumptions','','Not a current 2026 invoice or personalized entitlement.','Powertrain fit and lifecycle cost guidance may remain distinct from existing tools, with date and scope reconciliation required.',source='JX03')
c(33,'Branch discovery','There is no branch/service-type filtering','qualify','The inspected branch panel has a working coarse workshop filter; later model/job filtering was beyond the public walkthrough boundary.','Auto2000 desktop route; 11 November 2026','','No whole-site absence claim; no live branch capability certification was measured.','A granular model/job match remains a candidate distinction, not a demonstrated missing feature.',source='JX05')
c(34,'BEV trade-in','Auto2000 does not support BEV trade-in','qualify','The current public selector allows BZ4X model/year/type before plate entry.','Auto2000 trade-in selector; 11 November 2026','','No price estimate, inspection or battery record acceptance was completed.','A candidate needs additional condition evidence or appraisal coordination beyond BEV selection.',source='JX07')
c(35,'Private owner records','Login boundary proves battery/service history is absent','unverified','The public account route redirects to login, leaving private records uninspected.','Logged-out observation; 11 November 2026','','No account or owner records accessed.','Keep record existence, completeness and interoperability unknown.',source='JX04')

numbers=[]
def num(id, metric, value, unit, year, entity, printed, definition, rounded=False):
 numbers.append(dict(observation_id=id,metric=metric,value=value,unit=unit,year=year,entity=entity,source_id='FC-S01',printed_page=printed,pdf_page_1based=printed+2,definition=definition,rounded_in_source=rounded))
num('FC-N01','National car sales',804000,'vehicles',2025,'Indonesia',134,'National new-car market; rounded report total',True)
num('FC-N02','National car sales YoY',-7,'percent',2025,'Indonesia',134,'Reported national market growth',True)
num('FC-N03','Astra car market share',51,'percent',2025,'Astra Group',134,'Group share of national car market; not Auto2000',True)
num('FC-N04','National xEV sales',172000,'vehicles',2025,'Indonesia',135,'BEV+HEV+PHEV; rounded report total',True)
num('FC-N05','National xEV growth YoY',72,'percent',2025,'Indonesia',135,'Reported xEV growth',True)
num('FC-N06','National xEV sales mix',22,'percent',2025,'Indonesia',135,'Reported share of new-car sales',True)
num('FC-N07','National BEV sales mix',13,'percent',2025,'Indonesia',135,'Reported share of new-car sales',True)
num('FC-N08','National HEV sales mix',8,'percent',2025,'Indonesia',135,'Reported share of new-car sales',True)
num('FC-N09','Integrated EV-service outlets',31,'outlets',2025,'Auto2000',137,'Reported integrated EV ecosystem service footprint; not a service-capability matrix')
num('FC-N10','Toyota charging locations',118,'locations',2025,'Toyota ecosystem',138,'113dealer+2restarea+3mall locations; not connectors')
num('FC-N11','Toyota dealer charging locations',113,'locations',2025,'Toyota dealers',138,'Includes three stated dealer UFC locations')
num('FC-N12','Toyota/Lexus total domestic sales',291566,'vehicles',2024,'Toyota and Lexus',140,'Chart total domestic sales; not Auto2000')
num('FC-N13','Toyota/Lexus total domestic sales',251954,'vehicles',2025,'Toyota and Lexus',140,'Chart total domestic sales; not Auto2000')
num('FC-N14','Toyota/Lexus xEV sales',37693,'vehicles',2024,'Toyota and Lexus',140,'Chart xEV sales; not Auto2000')
num('FC-N15','Toyota/Lexus xEV sales',31668,'vehicles',2025,'Toyota and Lexus',140,'Chart xEV sales; not Auto2000')
num('FC-N16','OLX/OLXmobbi used-car sales',27313,'vehicles',2024,'OLX and OLXmobbi report section',180,'Used-car volume chart; not EV-only or Auto2000-only')
num('FC-N17','OLX/OLXmobbi used-car sales',33139,'vehicles',2025,'OLX and OLXmobbi report section',180,'Used-car volume chart; not EV-only or Auto2000-only')

t0,t1,x0,x1=291566,251954,37693,31668
m0,m1=x0/t0,x1/t1
calc={
 'calculation_type':'Descriptive arithmetic and accounting identity; no causal identification or forecast',
 'inputs':dict(total_2024=t0,total_2025=t1,xev_2024=x0,xev_2025=x1,source_ids=['FC-N12','FC-N13','FC-N14','FC-N15']),
 'xev_change_units':x1-x0,'xev_change_pct':(x1/x0-1)*100,'total_change_pct':(t1/t0-1)*100,
 'xev_mix_2024_pct':m0*100,'xev_mix_2025_pct':m1*100,'mix_change_percentage_points':(m1-m0)*100,
 'accounting_decomposition':dict(identity='x1-x0 = (t1-t0)*m0 + t1*(m1-m0)',total_sales_scale_component_units=(t1-t0)*m0,within_portfolio_mix_component_units=t1*(m1-m0),expected_xev_at_2024_mix=t1*m0,interpretation='The terms allocate the observed change algebraically. They do not identify market conditions, product availability, pricing or Digiroom as causes; order of decomposition matters.'),
 'national_comparison':dict(toyota_lexus_mix_pct=m1*100,national_reported_rounded_mix_pct=22,gap_percentage_points=m1*100-22,interpretation='Cross-scope new-sales comparison only. Not Auto2000 adoption, owner installed base or customer intent. Rounded national figure and channel consistency limit precision.'),
 'non_identification':['xEV sales decline does not identify Digiroom causality.','New sales are flows, not the service-eligible installed base.','Dealer profit cannot be inferred from group/brand sales counts.','Reported digital infrastructure does not establish customer or advisor adoption.']
}

overlap=[
 ('R1','Powertrain fit and ownership-cost comparison','Existing catalogue/comparison, finance simulation, SAM product/pricing context and dated OEM service-cost tool.','FC04;FC14;FC32;UX02;UX03;UX04;JX03','Personal route/charging fit and transparent lifecycle assumptions are distinct from finance and are not refuted by its existence. Absence and customer value remain unverified.','Accurate information or advisor help may resolve the same job without another interface.'),
 ('R2','Model/job/capability-aware booking','Existing Digiroom booking, coarse branch/service filter, MSA, Reminder Service;31reportedEVoutlets.','FC05;FC12;FC14;FC33;UX06;UX08;JX05','Job-specific capability and credible capacity visibility are not established by a31outlet total; public walkthrough stopped before vehicle qualification.','Vehicle-first questions may be necessary for fit; no observed abandonment or incremental completed work.'),
 ('R3','Warranty and inspection next step','Toyota Hybrid Health Check, digital certificate retrieval and existing service booking/reminders.','FC05;FC14;FC31;M015;JX02','Eligibility explanation and accessible official results are candidate gaps; certificate issuance/retrieval already exists for eligible vehicles.','A paid visit or GP uplift cannot be assumed from a free inspection or repeated reminder.'),
 ('M1','Home-charger coordination','Toyota charging network and existing PLN/home-charging services.','FC13;M018;M019','Installer/status access and unresolved lead stage are not publicly established.','Referral can merely move an already-planned purchase; any commission requires an actual agreement.'),
 ('M2','Battery-history-to-trade-in evidence','Existing Toyota certificate retrieval, BEV trade-in selector, Trade Cycle Management, OLXmobbi network.','FC18;FC19;FC31;FC34;M015;JX02;JX04;JX07','Appraiser acceptance, permissible data linkage and incremental valuation information remain open.','A certificate is not a residual-value guarantee and need not raise executable bids.'),
 ('M3','EV protection and repair navigation','Existing ecosystem insurance and after-sales; friend cites available EV-insurance products.','FC14;FC30','Policy wording, model/job coverage and customer fit need distinct verification; this task does not confirm a new product.','Insurance, warranty, wear, capacity degradation and resale price are different risks.'),
 ('O1','Extended real-life test drive','Existing test-drive request with branch/calendar preview and explicit subsequent staff confirmation.','FC14;UX05;JX06','A longer trial changes duration/cost rather than creating the first test-drive path.','Demo capacity, selection and insurance costs may consume the margin of induced purchases.'),
 ('O2','Future trade-in price protection','Existing appraisal/trade-in, not evidence of a funded future-price floor.','FC18;FC19;UX07','Public sources checked do not confirm this exact contract or a sharia residual-value insurer.','General market-price falls can raise both unit loss and exercise probability; group affiliation does not transfer that liability.'),
 ('O3','Replacement mobility during repair','Toyota ecosystem mobility services and existing service journeys.','FC17;FC30','No confirmation of universal eligible EV-repair replacement-car entitlement in the checked sources.','Retained job contribution must exceed vehicle/rental and displacement costs; service footprint is not spare fleet capacity.'),
]
options=[dict(option_id=a,friend_direction=b,existing_baseline=c,evidence_refs=d,unresolved_distinction=e,strongest_economic_rival=f,status='Research candidate; not selected; no implementation design') for a,b,c,d,e,f in overlap]

# Preserve model/system names while making prose and number/unit boundaries readable.
fixes={
 'about172k,+72%,22%':'about 172k, +72%, 22%', 'sales37,693':'sales 37,693',
 'sold37,693 in2024 and31,668 in2025':'sold 37,693 in 2024 and 31,668 in 2025',
 'confirms37,693 and31,668':'confirms 37,693 and 31,668',
 'sales291,566 and251,954':'sales 291,566 and 251,954',
 'mix12.57% in Toyota/Lexus2025':'mix 12.57% in Toyota/Lexus in 2025',
 'about22%':'about 22%', 'AR172k/+72%':'AR 172k / +72%',
 'and31,668':'and 31,668', 'case175,144/+69.7%':'case 175,144 / +69.7%',
 'approximately33,950':'approximately 33,950', 'project2016–2016':'project 2016–2016',
 'retrieved2026':'retrieved in 2026', 'the50/50':'the 50/50',
 ';31reportedEVoutlets.':'; 31 reported EV outlets.',
 'a31outlet':'a 31-outlet', 'by a31outlet':'by a 31-outlet',
 '113dealer+2restarea+3mall':'113 dealer + 2 rest-area + 3 mall',
 'model2016':'model 2016', '172k,+72%,22%':'172k, +72%, 22%',
 'BEV13% and HEV8%':'BEV 13% and HEV 8%',
}
for rows in [claims,sources,numbers,options]:
 for row in rows:
  for key,value in row.items():
   if isinstance(value,str):
    for old,new in fixes.items():value=value.replace(old,new)
    row[key]=value

def save(name, rows):
 (B/f'{name}.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 with (B/f'{name}.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
save('sources',sources);save('claim_matrix',claims);save('numeric_observations',numbers);save('option_overlap',options)
(B/'economic_diagnostics.json').write_text(json.dumps(calc,indent=2)+'\n')
assert len({x['claim_id'] for x in claims})==len(claims)
assert set(x['status'] for x in claims)<= {'confirm','qualify','unverified'}
assert abs(calc['accounting_decomposition']['total_sales_scale_component_units']+calc['accounting_decomposition']['within_portfolio_mix_component_units']-(x1-x0))<1e-8
inputs=[ROOT/'upload'/'IBSC_2026_Auto2000_Digiroom_Master_AI_Context (2).md',ROOT/'auto2000_run'/'workstreams'/'journeys'/'journey_observations.json',ROOT/'auto2000_run'/'workstreams'/'journeys'/'friendcontext_JX_observations.json',ROOT/'auto2000_run'/'workstreams'/'market'/'evidence.json']
manifest=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in inputs]
index={r['source_id']:dict(kind='source',title=r['title'],url=r['url']) for r in sources}
index.update({r['claim_id']:dict(kind='claim',subject=r['subject'],source_ids=r['source_ids']) for r in claims})
market=json.loads(inputs[-1].read_text())
index.update({r['evidence_id']:dict(kind='market_evidence',url=r['source_url'],locator=r['locator']) for r in market})
for ip in inputs[1:3]:
 for row in json.loads(ip.read_text())['observations']:
  index[row['observation_id']]=dict(kind='journey',url=row['final_url'],observed_date=row['observed_date'],limit=row['limit'])
refs={s for row in claims for s in row['source_ids'].split(';')}
refs|={s for row in options for s in row['evidence_refs'].split(';')}
missing=sorted(refs-set(index));assert not missing,missing
(B/'reference_index.json').write_text(json.dumps(index,indent=2)+'\n')
(B/'checks.json').write_text(json.dumps(dict(generated_utc=datetime.now(timezone.utc).isoformat(),claims=len(claims),numeric_cells=len(numbers),option_overlap_rows=len(options),source_documents=len(sources),ownership_clusters=2,ar2025_visual_qa_pdf_pages=[126,127,128,142],reference_ids_resolved=len(refs),unresolved_reference_ids=missing,checks_passed=['Unique claim IDs','Allowed verification states','Accounting identity','Printed/PDF page map checked on rendered pages','All cross-workstream evidence references resolve'],input_manifest=manifest,exclusions=['No publisher PDF or page images in public deliverables','No individual employee profile evidence','No implementation or final selection']),indent=2)+'\n')
print(json.dumps(calc,indent=2));print('Wrote',len(claims),'claims,',len(numbers),'numeric cells,',len(options),'option checks')
