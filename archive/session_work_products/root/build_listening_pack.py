import csv
import json
import zipfile
from pathlib import Path

ROOT = Path('/workspace/scratch/13acdac15ef5')
OUT = ROOT / 'Auto2000_X_Listening_10USD'
(OUT / 'inputs').mkdir(parents=True, exist_ok=True)
(OUT / 'templates').mkdir(exist_ok=True)

P1 = [
('buy_decision', '("mobil listrik" OR "mobil hybrid") ("akhirnya pilih" OR "akhirnya beli" OR "jadi beli" OR "batal beli" OR "gak jadi beli" OR "nggak jadi beli")'),
('choice_tradeoff', '("mobil listrik" OR "mobil hybrid") ("pilih mana" OR "mending" OR "galau" OR "bandingin" OR "dibanding")'),
('toyota_shortlist', '(Toyota OR Zenix OR Yaris OR "Corolla Cross" OR bZ4X) (hybrid OR listrik OR BEV OR PHEV) (beli OR pilih OR pertimbangan OR pengalaman)'),
('household_fit', '("mobil listrik" OR "mobil hybrid") (keluarga OR stroller OR "car seat" OR bagasi OR garasi OR "mobil pertama" OR "mobil satu-satunya")'),
('charging_fit', '("mobil listrik" OR bZ4X OR "BYD M6" OR "BYD Atto" OR "Omoda E5") (rumah OR apartemen OR kos OR SPKLU OR "luar kota" OR mudik)'),
('finance_cash', '("mobil hybrid" OR "mobil listrik" OR "Zenix hybrid" OR "Yaris Cross hybrid") (DP OR cicilan OR kredit OR leasing OR "uang muka" OR "bunga kredit")'),
('ownership_cost', '("mobil listrik" OR "mobil hybrid") ("biaya servis" OR "biaya perawatan" OR "biaya listrik" OR "biaya bensin" OR "biaya asuransi" OR "total biaya")'),
('demo_fulfillment', '(Toyota OR Auto2000 OR "Auto 2000" OR bZ4X OR "Yaris Cross" OR Zenix) ("test drive" OR testdrive OR "tes drive" OR inden OR "stok kosong" OR SPK)'),
('switching_alternatives', '(Toyota OR Zenix OR "Yaris Cross" OR bZ4X) (BYD OR Chery OR Wuling OR Hyundai OR Honda OR Suzuki) (pilih OR beli OR batal OR banding)'),
('outcome_counterexamples', '("mobil listrik" OR "mobil hybrid") ("puas" OR "cocok" OR "nyesel" OR "menyesal" OR "belum butuh" OR "tetap bensin")'),
('handoff', '(Toyota OR Auto2000 OR "Auto 2000") (hybrid OR listrik OR bZ4X) (sales OR dealer OR WhatsApp OR WA OR penawaran OR respons)'),
('timing_and_access', '("mobil listrik" OR "mobil hybrid") ("nunggu" OR "menunda" OR "ditolak" OR "disetujui" OR "unit ready" OR "ready stock" OR "belum mampu")')
]
P2 = [
('provider_choice', '(Toyota OR Avanza OR Calya OR Agya OR Rush OR Innova OR Fortuner) ("bengkel resmi" OR "bengkel umum" OR "bengkel langganan")'),
('provider_switch', '(Toyota OR Avanza OR Innova OR Fortuner OR Auto2000 OR "Auto 2000") ("pindah bengkel" OR "balik ke bengkel" OR "servis di luar" OR "service di luar" OR "bengkel non resmi")'),
('oil_service', '(Toyota OR Avanza OR Innova OR Fortuner) ("ganti oli" OR "servis berkala" OR "service berkala") (harga OR biaya OR murah OR mahal OR bengkel)'),
('brake_and_wear', '(Toyota OR Avanza OR Innova OR Fortuner) ("kampas rem" OR "kaki kaki" OR "kaki-kaki" OR "ganti aki") (bengkel OR servis OR service OR biaya)'),
('scope_and_bill', '(Toyota OR Auto2000 OR "Auto 2000") ("biaya servis" OR "biaya service" OR "tagihan" OR "estimasi biaya" OR "tambahan biaya" OR "tanpa persetujuan")'),
('slot_and_time', '(Toyota OR Auto2000 OR "Auto 2000") (booking OR antre OR antri OR menunggu OR "tepat waktu") (servis OR service OR bengkel)'),
('quality_and_trust', '(Toyota OR Auto2000 OR "Auto 2000") (bengkel OR servis OR service) (beres OR puas OR percaya OR transparan OR jujur OR kecewa OR "rusak lagi")'),
('parts_choices', '(Toyota OR Auto2000 OR "Auto 2000" OR OtoXpert OR "T-OPT") ("suku cadang" OR sparepart OR "spare part" OR onderdil) (harga OR asli OR palsu OR stok OR inden)'),
('warranty_expiry', '(Toyota OR Avanza OR Innova OR Fortuner) ("garansi habis" OR "habis garansi" OR "di luar garansi" OR "diluar garansi" OR "servis gratis habis")'),
('hybrid_service', '(Toyota OR Zenix OR "Yaris Cross" OR "Corolla Cross") (hybrid OR HEV) (servis OR service OR bengkel OR "health check" OR "cek baterai")'),
('hybrid_diagnosis', '(Toyota OR Zenix OR "Yaris Cross" OR "Corolla Cross") (hybrid OR HEV) (baterai OR garansi OR klaim OR diagnosis OR "lampu indikator")'),
('bev_phev_support', '(bZ4X OR "Toyota BEV" OR "Toyota PHEV" OR "Prius PHEV" OR "RAV4 PHEV") (bengkel OR servis OR service OR baterai OR garansi OR klaim OR diagnosis)'),
('competitor_support', '(Chery OR BYD OR Wuling OR Hyundai) (listrik OR hybrid OR BEV OR PHEV OR "Omoda E5" OR "Ioniq 5") (servis OR service OR bengkel OR garansi OR klaim)'),
('chery_ice_comparator', '(Chery OR "Chery C5" OR "Omoda 5" OR "Tiggo 7") (bensin OR ICE OR turbo) (servis OR service OR bengkel OR sparepart OR garansi)'),
('chery_xev_comparator', '("Chery E5" OR "Omoda E5" OR "Chery J6" OR "Tiggo Cross CSH" OR "Tiggo 8 CSH") (servis OR service OR bengkel OR baterai OR garansi OR klaim)'),
('economy_channels', '(OtoXpert OR "Oto Xpert" OR "T-OPT" OR "T OPT" OR "Toyota Home Service") (servis OR service OR biaya OR harga OR pengalaman OR booking)'),
('entitlement_payer', '(Toyota OR Auto2000 OR "Auto 2000" OR "T-CARE" OR "T CARE") ("servis gratis" OR "gratis jasa" OR "gratis sparepart" OR "biaya ditanggung" OR "klaim garansi")'),
('resolution_recommendation', '(Toyota OR Auto2000 OR "Auto 2000" OR Chery) (bengkel OR servis OR service OR garansi) (selesai OR ditangani OR dibantu OR rekomendasi OR "belum selesai" OR mangkrak)')
]
P3 = [
('toyota_upgrade', '(Toyota OR Auto2000 OR "Auto 2000" OR Avanza OR Innova OR Fortuner OR Zenix) ("tukar tambah" OR "trade in" OR "trade-in")'),
('xev_replacement', '(hybrid OR "mobil listrik" OR bZ4X OR "BYD M6") ("ganti mobil" OR "upgrade mobil" OR "tukar tambah" OR "trade in")'),
('valuation', '(Toyota OR Auto2000 OR "Auto 2000" OR OLXmobbi OR "Toyota Trust") (appraisal OR apraisal OR taksiran OR inspeksi OR valuasi OR "harga penawaran")'),
('resale_economics', '("mobil hybrid" OR "mobil listrik" OR "Zenix hybrid" OR "Yaris Cross hybrid" OR bZ4X) ("harga jual" OR "harga bekas" OR depresiasi OR "jual lagi" OR "nilai jual")'),
('loan_and_equity', '(mobil OR Toyota OR Innova OR Avanza OR Zenix) ("tukar tambah" OR "trade in" OR "ganti mobil") (cicilan OR kredit OR pelunasan OR leasing OR selisih OR nombok)'),
('replacement_outcomes', '(Toyota OR Auto2000 OR "Auto 2000" OR Innova OR Avanza OR Zenix) ("akhirnya ganti" OR "batal ganti" OR "belum ganti" OR "beli lagi" OR "tetap pakai" OR "jadi tukar")'),
('trade_or_sell', '(mobil OR Toyota OR Innova OR Avanza) ("tukar tambah" OR "trade in" OR OLXmobbi) ("jual sendiri" OR murah OR rendah OR cepat OR praktis OR ribet OR puas)'),
('condition_evidence', '(mobil OR Toyota OR hybrid OR "mobil listrik") ("riwayat servis" OR "record service" OR "service record" OR "sertifikat baterai" OR "health check" OR "battery health") (jual OR bekas OR appraisal OR harga OR "tukar tambah")'),
('retailer_loyalty', '(Auto2000 OR "Auto 2000" OR "dealer Toyota") ("beli lagi" OR "langganan" OR "pindah dealer" OR "dealer lain" OR "sales yang sama" OR "beda dealer")'),
('retain_or_switch', '(Toyota OR Innova OR Avanza OR Fortuner OR Zenix) (BYD OR Chery OR Wuling OR Hyundai OR hybrid OR listrik) ("ganti" OR "beralih" OR "pindah" OR "tetap" OR "balik")')
]
CROSS = [
('digiroom', '(Digiroom OR "Digi Room" OR "Auto2000 app" OR "aplikasi Auto2000" OR "aplikasi Auto 2000")'),
('toyota_apps', '(mToyota OR "m Toyota" OR "T-Intouch" OR "T Intouch") (aplikasi OR app OR booking OR servis OR service OR dealer)'),
('app_service_handoff', '(Auto2000 OR "Auto 2000" OR Toyota) (aplikasi OR online OR website OR WhatsApp OR WA) (booking OR konfirmasi OR jadwal OR servis OR service)'),
('sales_handoff', '(Auto2000 OR "Auto 2000" OR "dealer Toyota") (sales OR admin OR WhatsApp OR WA) (respons OR respon OR balas OR followup OR "follow up" OR penawaran)'),
('support_recovery', '(Auto2000 OR "Auto 2000" OR Toyota) (komplain OR keluhan OR dibantu OR ditangani OR "customer service")'),
('competitor_apps', '(MyChery OR "My Chery" OR "myHyundai" OR "aplikasi BYD" OR "aplikasi Wuling")'),
('success_paths', '(Auto2000 OR "Auto 2000") ("booking online" OR aplikasi OR Digiroom OR WhatsApp) (mudah OR cepat OR praktis OR berhasil OR lancar OR puas)'),
('channel_choice', '(Toyota OR Auto2000 OR "Auto 2000") ("langsung ke dealer" OR "langsung ke bengkel" OR "lewat sales" OR "via WA" OR "pakai aplikasi" OR "pake aplikasi")')
]

WINDOWS = [('2025-01-01','2025-07-01'),('2025-07-01','2026-01-01'),('2026-01-01','2026-07-01'),('2026-07-01','2026-11-14')]

def query(base, start, end, language=True):
    return f'{base}' + (' lang:id' if language else '') + f' -filter:nativeretweets since:{start} until:{end}'

def actor(terms, cap, per_target):
    return dict(mode='search', searchTerms=terms, queryType='Latest', maxItems=cap, maxItemsPerTarget=per_target, outputVariant='rich')

def save(path, data):
    (OUT/path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

pilot_bases = [P1[0],P1[2],P1[5],P2[0],P2[4],P2[9],P2[14],P3[0],P3[3],CROSS[0]]
save('inputs/00_pilot.json', actor([query(b,'2026-01-01','2026-11-14') for _,b in pilot_bases],1000,100))
catalogue=[]
budgets=[('00_pilot',1000,0.15)]
for stem, bases, cap, per_target in [('01_first_time_buyers',P1,12000,250),('02_workshop_and_xev_support',P2,18000,250),('03_repeat_purchase',P3,10000,250),('04_digital_handoff',CROSS,4000,125)]:
    terms=[]
    for topic,base in bases:
        for start,end in WINDOWS:
            term=query(base,start,end)
            terms.append(term)
            catalogue.append([stem,topic,start,end,per_target,term])
    assert len(terms)*per_target==cap
    save(f'inputs/{stem}.json',actor(terms,cap,per_target))
    budgets.append((stem,cap,cap*0.00015))

# Later-stage templates are deliberately not executable until real result IDs/queries are selected.
save('templates/05a_context_replies_TEMPLATE.json',dict(mode='replies',tweetIds=['REPLACE_WITH_REAL_ROOT_POST_ID_FROM_EXPORT'],maxItems=2000,maxItemsPerTarget=100,outputVariant='rich'))
save('templates/05b_no_language_recovery_TEMPLATE.json',actor(['REPLACE_WITH_A_VALIDATED_QUERY_WITHOUT_lang_id_AND_WITH_DATE_BOUNDS'],1000,250))
top=actor(['REPLACE_WITH_A_VALIDATED_UNDERSAMPLED_QUERY_WITH_DATE_BOUNDS'],2000,250)
top['queryType']='Top'
save('templates/05c_top_discovery_TEMPLATE.json',top)

with (OUT/'query_manifest.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['run','topic','since_inclusive','until_exclusive','max_items_per_target','search_term']);w.writerows(catalogue)

codebook=[
('record_id','Post ID preserved as a string; one unique post can have several prong labels.'),
('author_id_private','Pseudonymous author key for counts; keep raw identifiers private.'),
('conversation_id','Thread ID where available; retain context before interpreting replies.'),
('experience_type','self_reported_experience / consideration / advice / hearsay / media / official / dealer_promotion / unclear'),
('prong_tags','P1 / P2_petrol_paid / P2_xEV_support / P3 / shared_handoff; allow multiple tags.'),
('auto2000_purchase_history','explicit_no_prior_purchase / explicit_prior_purchase / unknown; first EV is a different variable.'),
('powertrain','ICE / HEV / PHEV / BEV / ambiguous; retain exact model and variant evidence.'),
('brand_model_variant','Record exactly what is stated; do not classify every Zenix or Yaris Cross as hybrid.'),
('location_evidence','Explicit city/branch / indirect / absent; Indonesian language alone is not proof of residence.'),
('journey_stage','consideration / quote / confirmed_test_drive / attended_test_drive / SPK / delivery / requested_booking / confirmed_slot / attendance / work_completed / claim_resolved / appraisal / valid_trade_offer / trade_completed / unknown'),
('reported_outcome','Separate observed post text from claimed offline events; offline completion remains self-reported.'),
('previous_provider','Auto2000 / other_Toyota_dealer / independent / other_brand / unknown'),
('alternative_considered','Competing car/dealer/garage/channel or postpone/retain; unknown if unstated.'),
('friction_or_enabler','price / finance / household_fit / charging / stock / demo / advisor_response / quote_scope / extra_work_approval / time / capability / parts / warranty / appraisal / trust / convenience / other'),
('service_job','Record job, powertrain, mileage/age and whether paid, covered or unknown.'),
('payer_and_economics','customer / OEM_programme / warranty / insurer / unknown; no GP inference from customer bill alone.'),
('sentiment_target','Identify target and mixed/positive/negative/neutral/unclear; sentiment alone is not the mechanism.'),
('resolution','resolved / unresolved / pending / unknown; distinguish reassurance from an actual completed job.'),
('counterevidence','Evidence that weakens a proposed solution, plus competing explanation.'),
('interpretation','What the account suggests and what evidence is still needed.'),
('evidence_excerpt_private','Short contextual excerpt for internal review; anonymize public case illustrations.'),
('source_url','Original post link and collection date for internal traceability.'),
('review_status','AI_suggested / checked_against_post / context_missing / ambiguous; AI agreement is not human validation.')
]
with (OUT/'coding_codebook.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['field','rule']);w.writerows(codebook)

budget=dict(actor='xquik/x-tweet-scraper',budget_usd=10,assumed_event_price_usd=0.00015,event_price_must_be_checked_in_console=True,collection_plan=[dict(run=s,maximum_rows=n,event_fee_upper_bound_usd=round(c,2)) for s,n,c in budgets],adaptive_followup_maximum_rows=5000,adaptive_followup_event_fee_usd=0.75,total_event_row_ceiling=50000,total_event_fees_usd=7.50,platform_and_contingency_reserve_usd=2.50,warning='These are conditional event-fee ceilings, not guaranteed yields or a guaranteed all-in cost. Check actual cumulative usage after every run. No scraping has been executed.')
save('budget_plan.json',budget)

sources=[
('Actor README','https://apify.com/xquik/x-tweet-scraper'),
('Input schema','https://apify.com/xquik/x-tweet-scraper/input-schema'),
('Pricing','https://apify.com/xquik/x-tweet-scraper/pricing'),
('Historic rate discrepancy issue','https://apify.com/xquik/x-tweet-scraper/issues/unexpected-credit-co-dHNgWx4numHDqVBTJ'),
('Apify run charging','https://docs.apify.com/actors/running/actors-in-store'),
('Peer reviewed sampling caution, Scientific Reports (2024)','https://www.nature.com/articles/s41598-024-51555-0')
]
save('sources.json',dict(checked_date='2026-11-14',sources=[dict(label=a,url=b) for a,b in sources]))

readme='''AUTO2000 X SOCIAL LISTENING: $10 INPUT PACK
Prepared 14 November 2026. Actor assumed: xquik/x-tweet-scraper.
This is a proposed collection design. No paid actor run or customer validation has occurred.

PURPOSE
Find decision mechanisms and counterexamples for the three current strategy prongs:
P1: first-time Auto2000 xEV purchases; P2: recover paid workshop jobs and resolve xEV ownership needs; P3: repeat Auto2000 xEV purchases.
Use both Toyota/Auto2000-specific evidence and the wider Indonesian-language market, with separate labels. Evidence from other brands can generate hypotheses, not establish Auto2000 performance.

START
1. Open the exact Actor and check the rate displayed for YOUR account. The current public listing says $0.00015 per delivered result plus platform usage. A historical issue describes a much higher free-tier rate; the current listing says all plans use the same rate. This pack is conditional on the displayed $0.00015 rate, not a promise of account billing.
2. Paste inputs/00_pilot.json into the Actor JSON input tab. For the first pilot set the Console Maximum total charge to $0.20; this is a RUN setting, not a key in actor input JSON. Keep a timeout (for example 180 seconds for this pilot) and inspect the actual total usage afterward. Separate platform consumption may need additional monitoring.
3. Inspect at least 20 posts per returned query where available, including low-engagement posts. Across the pilot inspect about 200 posts. Check irrelevant homonyms, seller spam, media articles, mixed-language omissions, dates, replies missing their parents, and whether a post reports a real decision. Keep complaints and successful outcomes. Label promotions/media separately rather than deleting all links or all positive comments.
4. Proposed practical go/no-go: refine a query if fewer than roughly half the inspected posts are about its intended decision. This is a working screening threshold, not a statistical validity test. Low personal-experience yield may justify narrower action terms even when topic relevance is high.
5. Run core files sequentially in order 02, 01, 03, 04 after the pilot. Aftersales has the largest quota because it covers paid petrol work, hybrid/BEV/PHEV support, and matched competitive support. Each JSON is a separate run. Do not paste budget_plan.json or query_manifest.csv into the Actor.
6. Suggested event-charge caps in Console: 02=$2.70, 01=$1.80, 03=$1.50, 04=$0.60. Pilot actual event fees are at most $0.15 at the assumed price; the $0.20 Console pilot ceiling allows a small discrepancy. Track actual spend, not the sum of nominal caps alone.
7. Stop or reduce a later run if actual total account consumption plus its conservative expected cost would exceed $10. The $2.50 reserve is not a guaranteed platform-price quote. If the displayed result price differs, recompute row ceilings before proceeding: floor(available event budget / displayed price).

BUDGET
Pilot: 1,000 rows / $0.15 event fees.
P1: 12,000 rows / $1.80.
P2: 18,000 rows / $2.70.
P3: 10,000 rows / $1.50.
Shared digital handoff: 4,000 rows / $0.60.
Adaptive follow-up: up to 5,000 rows / $0.75 combined.
Maximum planned total: 50,000 delivered rows / $7.50 event fees.
Reserve: $2.50 for platform usage, overlap, retries or unanticipated consumption. Any retries must fit the same cumulative budget; do not add 50,000 new rows after a pilot or follow-up.
These are delivered-row ceilings, not forecasts. Cross-run overlap will reduce the number of unique posts. Sparse queries can return far less than their quotas. Do not manufacture volume by loosening relevance without recording the design change.

SAMPLING AND COVERAGE
The four core files contain 192 dated searches: 48 P1, 72 P2, 40 P3 and 32 shared. Each theme is split into four nonoverlapping windows, avoiding a single newest-first search that spends the whole quota on recent posts.
Windows: 2025-01-01 to 2025-07-01; 2025-07-01 to 2026-01-01; 2026-01-01 to 2026-07-01; 2026-07-01 to 2026-11-14. Since is inclusive and until exclusive; date-only searches use UTC. The collection stops before 14 November 2026 00:00 UTC, equivalent to 07:00 WIB on 14 November. Report 2025 and 2026 separately when product offers or app versions changed. Window lengths are unequal; quotas cannot be used to compare posting rates.
Latest is used for the main collection. Each search is bounded at 250 rows (125 for shared). A capped search is still a censored slice, not the full population of matches. If a query hits its cap, split that query into smaller nonoverlapping date ranges using an unspent portion of its original quota or the follow-up budget. Date splitting does not establish complete X coverage.
No minimum engagement, follower or verified-account filter. Replies and quote posts remain eligible. Native reposts are excluded to limit repeated amplification. Do not infer nationality from lang:id or profile language. Avoid geo restrictions during initial discovery; code explicitly stated branch/city afterward.
Do not exclude broad words such as promo, diskon, jual, link or kredit at collection: they can also occur in genuine customer narratives. Classify commercial accounts and near-duplicate scripts after export.
The searches intentionally contain some overlapping concepts. Retain multiple analytical tags for one post; never add prong counts as if they were independent people or revenue pools.

ADAPTIVE FOLLOW-UP, TOTAL LIMIT 5,000 ROWS
Templates require replacements and are NOT ready to execute as-is.
05a: select up to 20 genuine decision/service thread roots across all prongs, not only viral complaints. Insert real root post IDs, collect up to 100 direct replies per root, max 2,000. This mode does not guarantee nested conversation recovery. If nested context is essential, use the documented conversationIds/search route within the same budget. Keep all languages in reply collection and screen relevance afterward.
05b: choose up to four validated topical queries, remove lang:id, retain dates and non-repost filter, and retrieve up to 250 each / 1,000 total. This probes Indonesian/English code-switching and language classification omissions; manually screen geography and relevance.
05c: use Top only for selected thin or contrasting themes, up to eight queries x 250 / 2,000 total. Label this a separate discovery supplement. Do not merge it into a denominator as if it had the same selection process as Latest. If not useful, reallocate within the 5,000-row total and document the change.
Missing parents can be looked up with tweetIds, also within the same adaptive allowance. Do not scrape an owner's entire history merely to guess purchase history.

ANALYSIS
Export JSON with nested structure preserved, plus optional CSV for reading. Save each submitted input and run ID, collection time, actual total cost, delivered rows, status, diagnostics and run-report if present. Keep query_manifest.csv as the requested-search record; do not assume every output row includes its exact matching query. Record any available query provenance and retain multiple matches where possible.
Exclude diagnostic/non-post records. Deduplicate globally by post ID, keeping source-run membership. Keep repeated author posts for context, but report unique authors and conversations alongside post counts. Separate near-duplicate dealer templates from individual experiences. Native amplification counts are not counts of independent experiences.
Use coding_codebook.csv. Prior purchase at Auto2000 is explicit_prior_purchase, explicit_no_prior_purchase or unknown. A first-time EV buyer is not necessarily a first-time Auto2000 buyer. A Toyota owner is not necessarily an Auto2000 customer. Most public accounts may remain unknown on retailer history.
Distinguish an actual self-reported choice, hypothetical intent, advice, hearsay, official statements and promotions. For every useful account reconstruct: trigger, options, constraint/enabler, channel handoff, reported action, resolution and remaining uncertainty.
Code model/powertrain/variant, job and payer. Do not compare Chery ICE routine service with Toyota BEV battery diagnosis as if their work were equivalent. A covered service with zero customer cash is not evidence of zero dealer reimbursement, and customer bills do not establish gross profit.
Use AI labels only as a first pass. Check all quotations and decision-critical examples against full text plus thread context; inspect both supporting and conflicting cases. If a human second coder is available, independently review a stratified subset and document disagreements. AI-to-AI agreement is not human reliability evidence.

DECISION OUTPUTS
P1: compare price/credit/stock/demo constraints with fit/comprehension constraints. A showroom feature is useful only if the latter actually explains stalled next steps; collect positive and negative cases.
P2: distinguish owners who prefer independent workshops for price/trust from those who need certainty of scope, authorization, timing, parts or competence. Identify the actual paid job and conditions for switching, plus high-stakes xEV cases that mainly create trust rather than immediate GP.
P3: distinguish low trade-in value or affordability from confusing upgrade economics or missing credible condition evidence. Track self-reported retain/sell/trade/upgrade decisions and unknown prior retailer history.
Shared: identify request versus confirmation versus attendance versus completion, and the actor controlling each handoff. App mentions alone do not establish app-to-branch success or failure.
Produce a mechanism matrix with supporting accounts, counterexamples, evidence strength, testable solution implication and the field evidence still needed. Report frequencies only within a clearly defined retrieved-and-coded corpus. Equal topic quotas and overlapping queries prevent interpreting raw theme counts as market prevalence or brand market share.
Use this as qualitative discovery and fieldwork design. X accounts and posts are selective public expressions, not a representative sample of Indonesian buyers or verified offline transaction records. The 2024 Scientific Reports paper in sources.json discusses Twitter sampling bias in a different substantive domain; it supports this methodological caution, not any Indonesian automotive conclusion.
No causal conversion lift, switching rate, app retention, willingness-to-pay estimate or incremental GP can be established from these posts alone. Validate candidate mechanisms with matched quotes, recruited buyer/owner journeys and a credible branch pilot.

PRIVACY
Keep raw handles, vehicle details and contact information private. Do not contact posters without separate authorization. Pseudonymize excerpts for external reporting, minimize identifying details, and keep private source links only for the review trail.

VALIDATION STATUS
JSON syntax, expected fields/enums, date ranges, target quotas and arithmetic checked locally against the retrieved public schema. No actor execution, live query parsing, result completeness or account-specific charge has been tested.
'''
(OUT/'READ_ME_FIRST.txt').write_text(readme)
for p in OUT.rglob('*.json'):
    json.loads(p.read_text())
assert len(catalogue)==192
assert sum(x[1] for x in budgets)+5000==50000
assert round(sum(x[2] for x in budgets)+.75,2)==7.5
archive=ROOT/'Auto2000_X_Listening_10USD.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(ROOT))
print(json.dumps(dict(archive=str(archive),query_count=len(catalogue),files=sum(p.is_file() for p in OUT.rglob('*')),bytes=archive.stat().st_size)))
