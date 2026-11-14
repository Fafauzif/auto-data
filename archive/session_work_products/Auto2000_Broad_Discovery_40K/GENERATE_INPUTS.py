import csv,json,hashlib,zipfile
from pathlib import Path

R=Path('/workspace/scratch/13acdac15ef5')
O=R/'Auto2000_Broad_Discovery_40K'
O.mkdir(exist_ok=True)

P1=[
('discovery','showroom_car','"showroom" "mobil"'),
('discovery','car_dealer','"dealer mobil"'),
('discovery','car_salesperson','"sales mobil"'),
('discovery','test_drive','"test drive"'),
('discovery','testdrive_variant','"testdrive"'),
('discovery','buying_car','"beli mobil"'),
('discovery','looking_for_car','"cari mobil"'),
('discovery','casual_looking_for_car','"nyari mobil"'),
('discovery','choosing_car','"pilih mobil"'),
('discovery','abandoned_purchase','"batal beli mobil"'),
('treatment','showroom_ignored','"showroom" "dicuekin"'),
('treatment','showroom_served','"showroom" "dilayani"'),
('treatment','showroom_friendly','"showroom" "ramah"'),
('treatment','showroom_comfort','"showroom" "nyaman"'),
('treatment','showroom_alone','"showroom" "sendirian"'),
('treatment','dealer_ignored','"dealer" "dicuekin"'),
('treatment','dealer_served','"dealer" "dilayani"'),
('treatment','sales_pressure','"sales mobil" "maksa"'),
('treatment','friendly_sales','"sales mobil" "ramah"'),
('treatment','honest_sales','"sales mobil" "jujur"'),
('fit','uncertain_choice','"mobil" "bingung"'),
('fit','casual_comparison','"mobil" "bandingin"'),
('fit','formal_comparison','"mobil" "bandingkan"'),
('fit','household_agreement','"mobil" "istri"'),
('fit','family_use','"mobil" "keluarga"'),
('fit','child_seats','"mobil" "car seat"'),
('fit','stroller','"mobil" "stroller"'),
('fit','luggage','"mobil" "bagasi"'),
('fit','third_row','"mobil" "baris ketiga"'),
('fit','garage','"mobil" "garasi"'),
('demo','testdrive_queue','"test drive" "antri"'),
('demo','testdrive_comfort','"test drive" "nyaman"'),
('demo','demo_vehicle','"test drive" "unit"'),
('demo','demo_booking','"test drive" "booking"'),
('demo','demo_duration','"test drive" "lama"'),
('demo','walk_in_demo','"test drive" "langsung"'),
('commercial','downpayment','"mobil" "DP"'),
('commercial','instalments','"mobil" "cicilan"'),
('commercial','extra_costs','"mobil" "biaya tambahan"'),
('commercial','cash_due','"mobil" "uang muka"'),
('commercial','insurance','"mobil" "asuransi"'),
('commercial','cash_vs_credit','"mobil" "cash" "kredit"'),
('commercial','price_difference','"mobil" "harga beda"'),
('commercial','discount','"mobil" "diskon"'),
('commercial','offer','"mobil" "penawaran"'),
('commitment','refund','"mobil" "refund"'),
('commitment','order','"mobil" "SPK"'),
('commitment','waiting_for_stock','"mobil" "inden"'),
('commitment','delivery','"mobil" "delivery"'),
('commitment','handover','"mobil" "serah terima"'),
('handoff','sales_followup','"sales mobil" "follow up"'),
('handoff','sales_reply','"sales mobil" "balas"'),
('handoff','sales_promises','"sales mobil" "janji"'),
('handoff','dealer_complaint','"dealer mobil" "komplain"'),
('handoff','dealer_satisfaction','"dealer mobil" "puas"'),
('handoff','dealer_recommendation','"dealer mobil" "rekomendasi"'),
('buyer_status','first_car','"beli mobil pertama"'),
('buyer_status','recent_purchase','"baru beli mobil"'),
('digital','online_showroom','"showroom" "online"'),
('digital','virtual_vehicle','"mobil" "virtual"')
]
P2=[
('discovery','car_workshop','"bengkel mobil"'),
('discovery','car_servis','"servis mobil"'),
('discovery','car_service','"service mobil"'),
('provider','official_workshop','"bengkel resmi"'),
('provider','independent_workshop','"bengkel umum"'),
('provider','regular_workshop','"bengkel langganan"'),
('provider','specialist_workshop','"bengkel spesialis"'),
('job','scheduled_service','"servis berkala"'),
('job','oil_change','"ganti oli mobil"'),
('price','service_cost','"biaya servis mobil"'),
('price','expensive_workshop','"bengkel" "mahal"'),
('price','economical_workshop','"bengkel" "murah"'),
('trust','honesty','"bengkel" "jujur"'),
('trust','satisfaction','"bengkel" "puas"'),
('trust','disappointment','"bengkel" "kecewa"'),
('fulfillment','queue','"bengkel" "antri"'),
('fulfillment','booking','"bengkel" "booking"'),
('fulfillment','parts','"bengkel" "sparepart"'),
('coverage','warranty','"bengkel" "garansi"'),
('trust','deception_account','"bengkel" "dibohongi"'),
('fulfillment','completion','"bengkel" "selesai"'),
('coverage','car_warranty_claim','"mobil" "klaim garansi"'),
('quality','repeat_fault','"mobil" "rusak lagi"'),
('job','auxiliary_battery','"mobil" "ganti aki"'),
('xev_support','battery_coverage','"mobil" "baterai" "garansi"')
]
P3=[
('discovery','replacement','"ganti mobil"'),
('discovery','selling','"jual mobil"'),
('alternative','sell_independently','"jual mobil sendiri"'),
('tradein','trade_in_id','"tukar tambah mobil"'),
('tradein','trade_in_en','"trade in" "mobil"'),
('appraisal','appraisal','"mobil" "appraisal"'),
('appraisal','offer_received','"mobil" "ditawar"'),
('resale','resale_value','"mobil" "harga jual"'),
('resale','depreciation','"mobil" "depresiasi"'),
('equity','remaining_instalments','"mobil" "sisa cicilan"'),
('equity','loan_settlement','"mobil" "pelunasan"'),
('resale','selling_at_loss','"mobil" "jual rugi"'),
('resale','selling_urgently','"mobil" "jual cepat"'),
('discovery','upgrade','"mobil" "upgrade"'),
('condition','service_record','"mobil" "service record"')
]
assert len(P1)==60 and len(P2)==25 and len(P3)==15
WINDOWS=[('2025-01-01','2025-04-01'),('2025-04-01','2025-07-01'),('2025-07-01','2025-10-01'),('2025-10-01','2026-01-01'),('2026-01-01','2026-04-01'),('2026-04-01','2026-07-01'),('2026-07-01','2026-10-01'),('2026-10-01','2026-11-14')]
manifest=[];allocations=[]
for filename,label,themes in [('01_SHOWROOM_AND_BUYING_BIG.json','P1_buyer_and_showroom',P1),('02_WORKSHOP_AND_OWNERSHIP_BIG.json','P2_service_and_ownership',P2),('03_REPLACEMENT_AND_TRADEIN_BIG.json','P3_replacement_and_tradein',P3)]:
 terms=[]
 # Spread families through all date windows, rather than spending an entire cap on one recent broad theme.
 for start,end in WINDOWS:
  for domain,slug,base in themes:
   term=f'{base} lang:id -filter:nativeretweets since:{start} until:{end}'
   terms.append(term)
   manifest.append(dict(file=filename,prong=label,domain=domain,theme=slug,base_query=base,since_inclusive=start,until_exclusive=end,cap_per_search=50,search_query=term))
 cap=len(terms)*50
 d=dict(mode='search',searchTerms=terms,queryType='Latest',maxItems=cap,maxItemsPerTarget=50,outputVariant='rich')
 (O/filename).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 allocations.append(dict(file=filename,themes=len(themes),dated_searches=len(terms),maximum_delivered_rows=cap,conditional_result_fee_usd=round(cap*.00015,2)))
assert len(manifest)==800 and sum(x['maximum_delivered_rows'] for x in allocations)==40000

with (O/'QUERY_REGISTER.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)
(O/'BUDGET_AND_SCOPE.json').write_text(json.dumps(dict(actor='xquik/x-tweet-scraper',prepared_date='2026-11-14',date_range_utc={'since_inclusive':'2025-01-01','until_exclusive':'2026-11-14'},assumed_result_price_usd=.00015,collections=allocations,total_maximum_delivered_rows=40000,total_conditional_result_fees_usd=6.00,platform_usage='additional; not estimated',previous_actual_usage='unknown; check Console balance',evidence_scope='Cross-brand, all powertrains, Indonesian-language public discourse; not a verified Indonesia-customer sample',code_status='JSON syntax, fields/enums, date windows, unique query strings and cap arithmetic checked locally; no paid run executed',repository_context='https://github.com/Fafauzif/auto-data commit 34498fe033ae4dcd1a52c8d2e039f870b00d08fe, interpreted under the later user-supplied 14 November strategy'),indent=2)+'\n')

(O/'RUN_THESE_THREE.txt').write_text('''BROAD AUTOMOTIVE SOCIAL LISTENING: THREE LARGE INPUTS
Prepared 14 November 2026 for xquik/x-tweet-scraper.

RUN ORDER
1. 01_SHOWROOM_AND_BUYING_BIG.json: 60 themes x 8 windows = 480 searches, at most 24,000 delivered posts. Result-fee allocation $3.60 at $0.00015 per delivered row.
2. 02_WORKSHOP_AND_OWNERSHIP_BIG.json: 25 themes x 8 windows = 200 searches, at most 10,000 posts. Allocation $1.50.
3. 03_REPLACEMENT_AND_TRADEIN_BIG.json: 15 themes x 8 windows = 120 searches, at most 6,000 posts. Allocation $0.90.
TOTAL: 100 thematic seed searches, 800 dated search targets, at most 40,000 delivered posts, $6.00 in conditional result fees. Dates: 1 January 2025 through 13 November 2026 UTC. The final until boundary is 14 November 00:00 UTC / 07:00 WIB.

Open the exact Actor. Paste the full contents of one numbered JSON into its Input JSON tab, replacing previous input. Run the files sequentially in order 1, 2, 3. No additional preflight round or interim response is required. Do not also run the earlier narrower main inputs for this discovery wave. These are three separate complete inputs, not an array to paste together.

Before the first run, check the rate shown in your own Console and the actual remaining account balance. The public listing checked today says $0.00015 per delivered result, with platform usage billed separately. The $6 event allocation leaves nominal room within the original $10 envelope for earlier consumption, platform usage and contingencies; it does NOT establish your actual remaining balance. If available funds are insufficient for all three plus usage, lower the Console charge caps rather than incur extra spending. This may reduce topic coverage, so retain that fact in the run record.

Set the run's maximum charge setting to the corresponding allocation: $3.60, $1.50, $0.90. These are RUN settings, not extra Actor input JSON fields. Keep a finite timeout; 15 minutes per run is a reasonable initial operating limit for these large inputs, not a tested runtime estimate. Do not automatically restart a timed-out or failed run. Preserve partial results and logs; a restart can repeat already collected results and incur additional cost. Stop further runs if actual usage would exceed your total budget.

At completion, export each dataset as JSON and retain exact submitted input, log, run ID and actual usage. Send all three exports and logs together for combined analysis. There is no need to return between successful runs. If a file fails visibly, do not spend on repeated retries to force its cap.

WHAT IS BROADER
No Toyota, Auto2000, model or xEV requirement. All brands and powertrains qualify for discovery. We no longer insist on an exact phrase describing a completed purchase before listening. Most searches use one everyday phrase or two simple anchors. The buyer file covers showroom treatment, feeling ignored, sales pressure, independent browsing, household agreement, physical fit, luggage, child seats, demo access, finance, offers, refunds, waiting, handover, positive recommendations and digital exploration.

Service remains a distinct stream because showroom accounts cannot establish paid workshop demand. Its searches cover providers, costs, quality, trust, bookings, queues, parts, protection and repairs. The replacement stream covers retaining/replacing, selling independently, trade-in, appraisal, resale, loan settlement and condition records.

Both favorable and unfavorable experiences remain eligible. There is no minimum likes, followers or verification filter. Links, receipts, screenshots, mentions, replies and quote posts remain eligible. Native reposts are excluded to reduce repeated amplification. No account is excluded in this broader cross-brand wave; corporate publications and promotions remain source-role categories to separate later. Do not produce brand satisfaction rankings from this corpus.

LANGUAGE AND SOURCE SCOPE
Every query keeps lang:id to reduce the Turkish/Czech spillover observed in Run 1. It does not prove Indonesian residence, exclude every Malay record or guarantee proper classification of code-switching. Some broad anchors such as test drive, showroom, dealer and bengkel can describe motorcycles, furniture or other contexts. That is an intentional recall/precision trade-off in discovery, not permission to treat them as car evidence. Code vehicle and country explicitly; otherwise unknown. No generic hybrid-family search is used, limiting the earlier non-automotive hybrid contamination.

Why eight windows and only 50 results each? Broad anchors such as beli mobil can be dominated by one recent period. Smaller date targets distribute the ceiling across 2025 and 2026. Windows have different lengths and fixed quotas; raw counts do not measure monthly demand or population prevalence. Recent and historical information must be reported separately. Product offers, eligibility and features can change between years.

These searches intentionally overlap. The sum of target quotas is the row ceiling, not a prediction of yield or number of unique posts. Cross-run and cross-pilot duplicates must be removed globally by string post ID, retaining source-run memberships. One incident can produce several posts and one author can write several times. A source_exhausted result does not establish complete coverage of X. Larger row caps do not guarantee more results.

HOW WE WILL ANALYZE THE OUTPUT
First partition vehicle/market relevance and source role: firsthand experience, shopping consideration, question, advice, seller account, media, operator statement, campaign-like promotion, satire/fiction or unclear. Campaign-like language is a review flag, not proof of sponsorship or falsehood.
Reconstruct useful decision episodes: need -> options -> uncertainty or obstacle -> interaction -> reported action -> outcome or unresolved status. Code favorable examples and contrary cases alongside complaints. Public claims remain self-reported; missing parents and quotes must be checked for decision-critical examples.
Keep current vehicle/powertrain, locality, date, job, payer, quote status and retailer purchase history explicit. First car, first EV and first Auto2000 purchase are different. Retaining the current car is a meaningful decision, not an automatic lost conversion. An asking price is not a valid offer or realized sale. Zero customer cash is not zero dealer reimbursement. Recall and safety actions are not discretionary paid upsell.
Use discovered needs to specify tests for Digiroom. Existing finance/comparison, Hybrid Health Check, trade-in, economical care channels and app-to-branch capabilities in the repository remain the baseline. Competitor accounts generate hypotheses; they do not prove Auto2000 has the same failure or establish incremental sales/GP. Customer interviews, matched real offers and work orders are still needed to establish the commercial effect.

REPRODUCIBILITY
QUERY_REGISTER.csv contains the 800 requested targets and their families. It is a request register, not recovered output-query provenance or 800 independent findings. BUDGET_AND_SCOPE.json records allocations. GENERATE_INPUTS.py preserves this pack's generation logic in its original workspace; adjust its output-root path elsewhere. JSON parsing, documented field names/enums, date-window continuity, unique strings and total cap arithmetic were checked locally. No paid Actor run has been performed by this pack.
Reference schema: https://apify.com/xquik/x-tweet-scraper/input-schema
Pricing: https://apify.com/xquik/x-tweet-scraper/pricing
Context: user-supplied 14 November strategy and auto-data commit 34498fe033ae4dcd1a52c8d2e039f870b00d08fe. No repository files were changed.
''')

for name in ['01_SHOWROOM_AND_BUYING_BIG.json','02_WORKSHOP_AND_OWNERSHIP_BIG.json','03_REPLACEMENT_AND_TRADEIN_BIG.json']:
 d=json.loads((O/name).read_text())
 assert set(d)=={'mode','searchTerms','queryType','maxItems','maxItemsPerTarget','outputVariant'}
 assert d['mode']=='search' and d['queryType']=='Latest' and d['outputVariant']=='rich'
 assert len(d['searchTerms'])==len(set(d['searchTerms']))
 assert all('lang:id' in t and '-filter:nativeretweets' in t for t in d['searchTerms'])
 assert d['maxItems']==len(d['searchTerms'])*d['maxItemsPerTarget']
for i in range(1,len(WINDOWS)):assert WINDOWS[i-1][1]==WINDOWS[i][0]
print(json.dumps(dict(folder=str(O),themes=100,dated_searches=len(manifest),allocations=allocations,total_rows=40000,result_fees=6.0),indent=2))
