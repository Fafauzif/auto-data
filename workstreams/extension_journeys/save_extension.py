import csv
import datetime as dt
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).parent
stamp = dt.datetime.now(dt.timezone.utc).isoformat()
registered = json.loads((BASE / 'preregistered_tests.json').read_text())
common = {
    'observed_date': '2026-11-11',
    'browser': 'cloud Chrome cdp',
    'viewport': '1363x936 CSS pixels; DPR1',
    'account_state': 'logged_out',
    'session_context': 'Public Jakarta Pusat preference retained from prior evaluator work; no cleared-cookie or new-user claim.',
    'method': 'Live evaluator interaction; accessibility/DOM and selective visual checks; no form submission.',
    'customer_identifiers_entered': False,
    'performance_seconds': None,
    'not_measured': 'Mobile/native app; recruited users; customer completion time; causal uplift; branch fulfilment; private owner records.',
}
records = [
    dict(observation_id='XT01', topic='Mobile feasibility', status='not_tested_unsupported',
         source_ids=[], start_url='', final_url='', settings='Browser capabilities list returned []; read-only DOM measured window.innerWidth=1363, innerHeight=936, devicePixelRatio=1.',
         actions='Checked advertised browser capabilities. Did not alter browser/device settings or claim emulation.',
         observation='The available browser advertises no viewport/device-control capability. All remaining observations are desktop.',
         counterexample_result='Mobile comparison could not be performed.',
         limit='No inference about mobile usability or responsive behavior.'),
    dict(observation_id='XT02', topic='BEV pre-contact finance', status='completed_safe_endpoint',
         source_ids=['XTS01'], start_url='https://auto2000.co.id/', final_url='https://auto2000.co.id/mobil-baru-toyota/p/bz4x',
         settings='Jakarta Pusat; bZ4X A/T; Platinum White Pearl Mica; Rp799000000; parameter DP20%=Rp159800000; insurance upfront; ADDM; optional income left empty.',
         actions='Homepage actual bZ4X banner; Simulasi Kredit; dismissed an automatic offer popup; Hitung Simulasi; inspected five tenors; stopped before Minta Penawaran.',
         observation='Five finance illustrations appear without contact details. 60-month total upfront247187147 and monthly15581947 for59 remaining months. Separate CSV preserves all five outputs.',
         counterexample_result='Falsifies universal pre-contact finance blockage for this BEV, alongside earlier hybrid evidence.',
         limit='A calculator illustration is not a binding lender/insurer quote. No lead form was requested or submitted; an automatic popup was closed without input.'),
    dict(observation_id='XT03', topic='BEV and hybrid workshop qualification', status='partial_identifier_boundary',
         source_ids=['XTS03'], start_url='https://auto2000.co.id/layanan-bengkel', final_url='https://auto2000.co.id/layanan-bengkel',
         settings='Guest; BZ4X -> 2024 -> Bz4X A/T; then INNOVA ZENIX HYBRID -> 2024 -> NEW ZENIX 2.0 V HV Mod CVT (PC). Plate and contact fields empty.',
         actions='Tambah Mobil; inspect/select model, year and variant for BEV; switch to hybrid and repeat selection; stop without saving.',
         observation='Both model/year/variant combinations are supported before the required plate field. Vehicle Save remains disabled with plate empty; service selection and branch/time remain disabled pending qualification.',
         counterexample_result='BEV is not universally absent from the workshop selector. Both tested contexts reach the same identifier boundary.',
         limit='No job catalogue, entitlement, branch competence, capacity or order was tested downstream. Required fields may serve legitimate qualification. No excessive-field or abandonment inference.'),
    dict(observation_id='XT04', topic='Programme-specific service estimates', status='completed_safe_endpoint',
         source_ids=['XTS04'], start_url='https://aftersales.toyota.astra.co.id/t-care', final_url='https://aftersales.toyota.astra.co.id/t-care',
         settings='All New BZ4X Battery EV -> All New BZ4X Panoramic View; then Agya -> Agya 1.2 A/T. No owner identifier.',
         actions='Choose model; Lihat Servis; choose variant; inspect visit rows; open bZ4Xvisit8 and Agyavisit2.',
         observation='bZ4X rows1-7 display FREE labor/parts; rows8-11 display model-specific amounts. Agya1.2A/T displays FREE labor but paid parts on visits2-7 and a T-CARE Lite condition. Both opened cost notes date estimates to March2024, tax included, with dealer/additional-work caveats.',
         counterexample_result='General free-service language is not universal free labor and parts across all models. Pre-contact BEV estimates already exist.',
         limit='These are dated programme examples, not personal entitlement or current invoices. Selected BEV output also retains generic gasoline/diesel oil wording in the estimate note; do not infer an oil requirement for the BEV.'),
    dict(observation_id='XT05', topic='BEV technical data and warranty handoff', status='observed_with_detail_network_boundary',
         source_ids=['XTS01','XTS02','XTS05','XTS06'], start_url='https://auto2000.co.id/mobil-baru-toyota/p/bz4x', final_url='https://toyota.astra.co.id/ownership',
         settings='bZ4X A/T; Jakarta Pusat. Separately followed Toyota After Sales Warranty ->Lihat Detail.',
         actions='Expand product battery FAQ; open actual specification route and expand MESIN; visually verify fields; visit public OEM Warranty page and follow detail endpoint.',
         observation='Current product heading says2026 while overview includes a2025 subsection and battery FAQ71.4kWh. Expanded BEV specification renders tank capacity7311 under a litre label, power165 under Ps/Rpm and torque268.6 under Kgm/Rpm. OEM warranty publicly distinguishes 12V1year/20000km and traction xEV8years/160000km, whichever first. Model-detail ownership endpoint returned upstream remote-connection failure.',
         counterexample_result='Public battery/warranty information exists. A concrete label/content-scope mismatch is observable, while model-specific warranty details were not verified.',
         limit='Literal rendered values are not validated vehicle specifications. No actual tank size, battery-health state, warranty acceptance or customer effect is inferred. Connection failure is not classified as bot detection or feature absence; no alternate-route bypass attempted.'),
    dict(observation_id='XT06', topic='BEV test-drive request versus confirmation', status='completed_safe_preview',
         source_ids=['XTS07'], start_url='https://auto2000.co.id/testdrive/new-car/BZ4X', final_url='https://auto2000.co.id/testdrive/new-car/BZ4X',
         settings='bZ4X; Jakarta Pusat; Juanda; 13November2026 preview; no time chosen, contact or purchase period entered.',
         actions='Open actual product test-drive route; choose branch; choose13November; inspect two windows; close preview; expand booking FAQ.',
         observation='Settled branch list contains ten Jakarta Pusat choices; Juanda exposes08:00-12:00 and13:00-17:00 windows. FAQ explicitly says staff later contacts the customer to confirm schedule and unit availability.',
         counterexample_result='BEV pre-contact branch/calendar preview exists, but preview is not a confirmed unit or appointment.',
         limit='An initial no-slot/default-location message disappeared after loading and was not treated as actual unavailability. No request was submitted, and no inventory or fulfilment was verified.'),
    dict(observation_id='XT07', topic='Indonesian HHC discovery query', status='null_local_result',
         source_ids=['XTS08'], start_url='https://auto2000.co.id/testdrive/new-car/BZ4X', final_url='https://auto2000.co.id/search/global?text=cek%20kesehatan%20baterai',
         settings='Exact search phrase: cek kesehatan baterai; navbar search; current default Jakarta Pusat.',
         actions='Enter exact Indonesian phrase in navbar search; pressReturn; inspect settled result and screenshot.',
         observation='Search route displays0results and a vehicle-price catalogue heading. No programme result appears in this inspected query state.',
         counterexample_result='This phrase did not resolve the prior English-query discovery lead. The interface may search a product catalogue rather than the whole knowledge base.',
         limit='Two targeted queries across rounds are not an exhaustive findability study; the OEM HHC programme and retrieval route are already confirmed. No global absence, prevalence or causal claim.'),
    dict(observation_id='XT08', topic='Branch metadata and handoff preservation', status='completed_safe_handoff',
         source_ids=['XTS09','XTS10','XTS11','XTS12'], start_url='https://auto2000.co.id/dealer-toyota', final_url='https://auto2000.co.id/testdrive/new-car/hiace?branchCode=T155',
         settings='Juanda bZ4X branchCodeT151; then Cempaka Putih Hiace branchCodeT155, a different branch from the preceding selection.',
         actions='Open Juanda from branch list; inspect department metadata and actual bZ4X test-drive link; follow link and verify loaded branch. Open Cempaka Putih; follow its actual Hiace link and verify changed branch/model.',
         observation='Juanda page shows showroom hours and no workshop-hours row in the inspected panel; Cempaka Putih explicitly lists showroom and workshop/spares hours plus Booking Service. Loaded test-drive destinations preserve Juanda/bZ4X and then Cempaka Putih/Hiace respectively.',
         counterexample_result='A blanket claim that branch/model context is lost is contradicted on these two routes. Branch-category information differs by branch; model-by-job capability remains unresolved.',
         limit='Juanda generic dealer/bengkel prose is not proof of an EV workshop, and absent hours are not proof of inability. The second handoff changes both vehicle and branch; it does not isolate a powertrain effect. No booking submitted.'),
]
records[0].update(settings='Cloud API has no advertised viewport capability; desktop1363x936/DPR1. Separate intended Pixel7 preset412x839/DPR2.625 was never applied to a page.',actions='Check cloud capability list; inspect installed Playwright/Chromium; try a new sandboxed headless profile; inspect native Chromium and DevTools availability via Sky.',observation='Local Chromium launch fails before navigation because socket() is not permitted. Native Chrome explicitly blocks DevTools by organization policy. No available native-app setup identified.',counterexample_result='No mobile-emulated or native-app journey could be executed. See mobile_feasibility.json and mobile_capability_receipt.json.',limit='No security, SSL or proxy changes. No policy bypass, new emulator/app/account installation or mobile usability inference.')
records[4].update(status='observed_with_unverified_model_terms',source_ids=['XTS01','XTS02','XTS05','XTS06','XTS13'],final_url='https://www.toyota.astra.co.id/ownership',observation='Product2026heading coexists with2025section and71.4kWh FAQ. Selected BEV technical table renders tank-capacity7311 under litre label, power165/Ps-Rpm and torque268.6/Kgm-Rpm. OEM public warranty distinguishes12V1year/20000km and tractionxEV8years/160000km, whichever first. A direct non-www ownership navigation failed, but the actual earlier click opened a separate www ownership tab successfully; native view shows owner-manual type/variant controls. No model-specific warranty document was opened.',limit='Rendered technical values are not validated vehicle specifications or evidence of customer harm. The non-www connection failure does not mean the clicked handoff failed or details are absent. The actual clicked www landing exists; detailed model terms remain untested.')
rows=[{**common,**r} for r in records]
(BASE/'observations.json').write_text(json.dumps({'registered_at_utc':registered['registered_at_utc'],'saved_at_utc':stamp,'registered_tests':8,'live_ui_test_groups':7,'unsupported_capability_checks':1,'observations':rows},indent=2,ensure_ascii=False))
def csvout(name,data):
    with (BASE/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader()
        for row in data:w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in row.items()})
csvout('observations.csv',rows)
finance=[]
for tenor,upfront,monthly in [(60,247187147,15581947),(48,237736504,18056504),(36,229736214,22061314),(24,224790296,30718496),(12,238257968,57869168)]:
    finance.append(dict(observation_id='XT02',source_id='XTS01',model='New bZ4X Battery EV',variant='bZ4X A/T',color='Platinum White Pearl Mica',city='Jakarta Pusat',listed_price_idr=799000000,dp_percent=20,base_dp_idr=159800000,insurance_timing='upfront',first_instalment='ADDM',income_entered=False,tenor_months=tenor,total_upfront_idr=upfront,monthly_idr=monthly,remaining_payments=tenor-1,scope='Rendered illustration; not binding finance/insurance quote',observed_date='2026-11-11'))
csvout('bev_finance_illustrations.csv',finance)
costs=[]
models=[('All New BZ4X Battery EV','All New BZ4X Panoramic View',[(0,0)]*7+[(847000,0),(1582000,2112000),(847000,0),(1073000,2640000)]),('Agya','Agya 1.2 A/T',[(0,0),(0,564000),(0,637000),(0,564000),(0,842000),(0,564000),(0,637000),(416000,564000),(633000,1072000),(416000,564000),(452000,2076000)])]
for model,variant,values in models:
    for visit,(labor,parts) in enumerate(values,1):
        costs.append(dict(observation_id='XT04',source_id='XTS04',model=model,variant=variant,service_visit=visit,labor_rendered='FREE' if labor==0 else str(labor),parts_rendered='FREE' if parts==0 else str(parts),labor_estimate_idr=labor,parts_estimate_idr=parts,listed_total_idr=labor+parts,estimate_basis='March 2024',tax_note='Included in opened estimate note',scope='Published model programme estimate; FREE is a displayed benefit, not evidence that work is costless or of personal entitlement',observed_date='2026-11-11'))
csvout('service_estimates_extension.csv',costs)
sources=[
('XTS01','https://auto2000.co.id/mobil-baru-toyota/p/bz4x','Live product and calculator','observed'),
('XTS02','https://auto2000.co.id/mobil-baru-toyota/p/bz4x/spesifikasi','Live selected specification accordion','observed'),
('XTS03','https://auto2000.co.id/layanan-bengkel','Workshop qualification selector','observed to identifier boundary'),
('XTS04','https://aftersales.toyota.astra.co.id/t-care','Live model/variant programme cost tool','observed; March2024 estimate basis'),
('XTS05','https://aftersales.toyota.astra.co.id/warranty','Public category warranty page','observed'),
('XTS06','https://toyota.astra.co.id/ownership','Direct non-www navigation, separate from clicked target','remote connection failure; clicked target XTS13 loaded'),
('XTS07','https://auto2000.co.id/testdrive/new-car/BZ4X','BEV branch/calendar/FAQ','observed preview; no request'),
('XTS08','https://auto2000.co.id/search/global?text=cek%20kesehatan%20baterai','Indonesian exact-query state','observed0results'),
('XTS09','https://auto2000.co.id/dealer-toyota/jakarta-pusat/auto2000juanda','Named branch metadata and product links','observed'),
('XTS10','https://auto2000.co.id/testdrive/new-car/bz4x?branchCode=T151','Actual Juanda product link destination','loaded Juanda andbZ4X'),
('XTS11','https://auto2000.co.id/dealer-toyota/jakarta-pusat/auto2000cempakaputih','Named workshop branch metadata and product links','observed'),
('XTS12','https://auto2000.co.id/testdrive/new-car/hiace?branchCode=T155','Actual Cempaka Putih product link destination','loaded Cempaka Putih andHiace'),
('XTS13','https://www.toyota.astra.co.id/ownership','Separate tab opened by actual Warranty detail click','accessible owner-manual landing; model warranty document not opened'),
]
csvout('sources.csv',[dict(source_id=a,url=b,role=c,access_state=e,observed_date='2026-11-11',ownership_cluster='Astra/Toyota affiliated official sites; not independent corroborators') for a,b,c,e in sources])
report=(BASE/'report_source.md').read_text()
(BASE/'REPORT.md').write_text(report)
(BASE/'EXTENSION_JOURNEY_REPORT.md').write_text(report)
summary={'registered_tests':8,'live_ui_test_groups':7,'unsupported_mobile_checks':1,'finance_illustrations':len(finance),'service_estimate_rows':len(costs),'source_urls':len(sources),'observed_customer_outcomes':0,'bookings_or_leads_submitted':0,'mobile_journeys':0,'first_wave_files_overwritten':False,'local_mobile_browser_launch':'failed_before_navigation_socket_permission','native_app_setup':'not_available','bev_visits8_11_listed_total_idr':sum(x['listed_total_idr'] for x in costs if x['model']=='All New BZ4X Battery EV' and x['service_visit']>=8)}
(BASE/'summary.json').write_text(json.dumps(summary,indent=2))
files=['observations.csv','observations.json','bev_finance_illustrations.csv','service_estimates_extension.csv','sources.csv','REPORT.md','summary.json','preregistered_tests.json','PREREGISTRATION.md','EXTENSION_JOURNEY_REPORT.md','report_source.md','mobile_capability_receipt.json','mobile_feasibility.json']
(BASE/'sha256.json').write_text(json.dumps({n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in files},indent=2))
print(json.dumps(summary,indent=2))
