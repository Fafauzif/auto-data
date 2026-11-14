import csv,hashlib,json,re,subprocess,zipfile
from pathlib import Path

ROOT=Path('/workspace/scratch/13acdac15ef5')
OUT=ROOT/'Auto2000_Pilot_Analysis_Followup'
D=json.loads((ROOT/'upload/dataset_x-tweet-scraper_2026-11-14_09-21-02-237.json').read_text())
MET=json.loads((OUT/'pilot_metrics.json').read_text())
COMMIT=subprocess.check_output(['git','-C',str(ROOT/'auto-data'),'rev-parse','HEAD'],text=True).strip()
PILOT_IDS={r['id'] for r in D}
def save(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

EXCLUDE='-from:AUTO2000ID_ -from:ToyotaID -filter:nativeretweets'
def q(base,start='2026-01-01',end='2026-11-14',exclude=True):
 return f'{base} '+(EXCLUDE+' ' if exclude else '-filter:nativeretweets ')+f'since:{start} until:{end}'
def single(query,cap):
 return dict(mode='search',twitterContent=query,queryType='Latest',maxItems=cap,maxItemsPerTarget=cap,outputVariant='rich')
def batch(queries,cap,target):
 return dict(mode='search',searchTerms=queries,queryType='Latest',maxItems=cap,maxItemsPerTarget=target,outputVariant='rich')

SMOKES=[('01_digiroom_external','"Digiroom"'),('02_completed_buying','"mobil listrik" "akhirnya"'),('03_workshop_choice','"Toyota" "bengkel resmi"'),('04_upgrade','"mobil" "tukar tambah"'),('05_chery_support','"Chery" "garansi"'),('06_specific_hybrid_service','"Yaris Cross" "service"')]
for name,base in SMOKES:save(f'01_preflight/{name}.json',single(q(base),50))
save('01_preflight/07_batch_control.json',batch([q('"Digiroom"'),q('"Toyota" "bengkel resmi"')],100,50))

CONTEXT_INDICES=[0,67,71,87,118,119,186,199,417,420,429,430]
lookup_ids=sorted({str(r[k]) for i in CONTEXT_INDICES for r in [D[i]] for k in ['conversationId','inReplyToId'] if r.get(k) and str(r[k]) not in PILOT_IDS})
save('02_context/01_missing_roots_and_parents.json',dict(mode='tweet',tweetIds=lookup_ids,maxItems=len(lookup_ids),outputVariant='rich'))
REPLY_INDICES=[0,67,71,118,186,199,429,133,139,97,92,296,421,415,401]
roots=list(dict.fromkeys(D[i]['conversationId'] for i in REPLY_INDICES))
save('02_context/02_selected_conversation_replies.json',dict(mode='replies',tweetIds=roots,maxItems=len(roots)*100,maxItemsPerTarget=100,outputVariant='rich'))
with (OUT/'context_selection.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['pilot_row_1_based','seed_post_id','root_id','seed_url_private','reason']);
 for i in REPLY_INDICES:w.writerow([i+1,D[i]['id'],D[i]['conversationId'],D[i]['url'],'Recover outcome/context; review root before treating replies as relevant'])

P1=[('actual_bev_purchase','"mobil listrik" "akhirnya beli"'),('actual_hybrid_choice','"mobil hybrid" "akhirnya"'),('abandoned_bev','"mobil listrik" "batal"'),('home_fit','"mobil listrik" "rumah"'),('apartment_fit','"mobil listrik" "apartemen"'),('family_fit','"hybrid" "keluarga"'),('zenix_tax','"Zenix" "pajak"'),('tax_and_purchase','"hybrid" "pajak" "beli"'),('finance','"mobil listrik" "cicilan"'),('test_drive','"hybrid" "test drive"'),('inventory','"Toyota" "inden"'),('needs_based_shortlist','"hybrid" "pilih" "kebutuhan"')]
P2=[('official_channel','"Toyota" "bengkel resmi"'),('independent_channel','"Toyota" "bengkel umum"'),('trusted_garage','"Toyota" "bengkel langganan"'),('post_warranty','"Toyota" "garansi habis"'),('oil_job','"Avanza" "ganti oli"'),('innova_service','"Innova" "servis"'),('clutch_job','"Calya" "kopling"'),('auto2000_cost','"Auto2000" "biaya"'),('auto2000_booking','"Auto2000" "booking"'),('auto2000_resolution','"Auto2000" "selesai"'),('hybrid_cost','"hybrid" "service" "mahal"'),('hybrid_service','"hybrid" "servis"'),('battery_claim','"Toyota" "baterai" "garansi"'),('economy_channel','"OtoXpert"'),('chery_service','"Chery" "servis"'),('chery_warranty','"Chery" "garansi"'),('toyota_bev','"bZ4X" "bengkel"'),('phev_support','"PHEV" "garansi"')]
P3=[('trade_in','"mobil" "tukar tambah"'),('trade_in_english','"mobil" "trade in"'),('avanza_veloz_upgrade','"Avanza" "Veloz" "jual"'),('repeat_toyota','"Toyota" "beli lagi"'),('appraisal','"Auto2000" "appraisal"'),('appraiser_price','"OLXmobbi" "harga"'),('bev_resale','"mobil listrik" "jual kembali"'),('hybrid_replacement','"hybrid" "ganti mobil"'),('condition_record','"hybrid" "service record"'),('loan_equity','"mobil" "tukar tambah" "cicilan"')]
SHARED=[('digiroom_external','"Digiroom"'),('app_external','"Auto2000" "aplikasi"'),('whatsapp','"Auto2000" "WhatsApp"'),('confirmation','"Auto2000" "konfirmasi"')]
WINDOWS=[('2026-01-01','2026-04-01'),('2026-04-01','2026-07-01'),('2026-07-01','2026-10-01'),('2026-10-01','2026-11-14')]
manifest=[];budgets=[]
for stem,bases,target in [('01_P1_buyer_decisions',P1,200),('02_P2_paid_jobs_and_xev',P2,200),('03_P3_upgrade_and_appraisal',P3,200),('04_shared_handoff',SHARED,50)]:
 queries=[]
 for topic,base in bases:
  for n,(start,end) in enumerate(WINDOWS,1):
   query=q(base,start,end); queries.append(query)
   name=f'04_atomic_searches/{stem}/{topic}_Q{n}.json'
   save(name,single(query,target))
   manifest.append(dict(input_file=name,prong=stem,theme=topic,since_inclusive=start,until_exclusive=end,cap=target,query=query))
 cap=len(queries)*target
 save(f'03_bulk_after_checks/{stem}.json',batch(queries,cap,target))
 budgets.append(dict(run=stem,target_queries=len(queries),max_rows=cap,event_fee_usd=round(cap*.00015,4)))

# Targeted supply-side novelty check: this deliberately includes operator accounts.
save('02_context/03_smartdrive_programme_claims.json',single(q('"Toyota" "SmartDrive"',exclude=False),100))
assert sum(x['max_rows'] for x in budgets)==32800
assert len(manifest)==176
with (OUT/'search_job_manifest.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)

# The optional supplement uses the SAME queries, with a distinct ranking regime.
top_terms=[q('"mobil listrik" "akhirnya beli"'),q('"Toyota" "bengkel umum"'),q('"Auto2000" "biaya"'),q('"hybrid" "ganti mobil"')]
top=batch(top_terms,2000,500);top['queryType']='Top'
save('05_optional/01_top_discovery_only.json',top)

# Cross-reference the new cases to the pre-existing evidence, without claiming independent verification.
crosswalk=[
 dict(pilot_cases=['C01','C02'],repository_refs=['reports/INSIGHT_BOOK.md: IB04, IB09','workstreams/journeys/FRIEND_CONTEXT_CHALLENGE.md: R1'],relation='New illustrative accounts of information/household decisions; existing finance/comparison capability remains baseline.'),
 dict(pilot_cases=['C04','C05','C06','C18','C19','C20','C22'],repository_refs=['reports/INSIGHT_BOOK.md: IB03, IB16','workstreams/extension_stakeholders/MECE_STAKEHOLDER_REPORT.md: sections 1 and 2'],relation='Supports investigating job, trust and payer distinctions; does not measure switchable paid volume or branch GP.'),
 dict(pilot_cases=['C03','C07','C08','C14'],repository_refs=['reports/INSIGHT_BOOK.md: IB04, IB09','reports/SOLUTION_MENU.md: SOL-14 and SOL-15'],relation='New replacement illustrations; prior retailer, actual settlement and incremental delivery remain unknown.'),
 dict(pilot_cases=['C09','C10'],repository_refs=['reports/INSIGHT_BOOK.md: IB06','workstreams/journeys/FRIEND_CONTEXT_CHALLENGE.md: JX02/JX07'],relation='An existing certificate/retrieval route and BEV trade-in already exist; seller claims are not appraiser acceptance or a premium.'),
 dict(pilot_cases=['C11','C12'],repository_refs=['workstreams/friend_insurance/claim_matrix.csv','workstreams/extension_economics/EXTENSION_ECONOMICS_REPORT.md'],relation='SmartDrive is an additional programme-claim lead; no SmartDrive literal found in bounded repository text search. Existing guarantee/risk distinctions still apply.'),
 dict(pilot_cases=['C27'],repository_refs=['workstreams/extension_reviews/EXTENSION_REVIEW_REPORT.md: tests 1 and 3','reports/HYPOTHESIS_ASSESSMENT_NOTES.md'],relation='No independent Digiroom account in X pilot does not erase 50 existing selected Digiroom app-store records, 25 coded interactions, including 6 specific interactions on/after date boundary.'),
 dict(pilot_cases=['C15','C16','C17'],repository_refs=['DATA_GUIDE.md','reports/INSIGHT_BOOK.md: IB12, IB14'],relation='Reinforces source-role and label-quality caution; requires explicit narrative, fiction and commercial-content checks.')
]
repo_files=['DATA_GUIDE.md','reports/RESEARCH_REPORT.md','reports/EXTENSION_SYNTHESIS.md','reports/INSIGHT_BOOK.md','reports/HYPOTHESIS_ASSESSMENT_NOTES.md','workstreams/extension_reviews/EXTENSION_REVIEW_REPORT.md','workstreams/journeys/FRIEND_CONTEXT_CHALLENGE.md','workstreams/extension_stakeholders/MECE_STAKEHOLDER_REPORT.md']
save('repository_integration.json',dict(repository='https://github.com/Fafauzif/auto-data',local_clone=str(ROOT/'auto-data'),commit=COMMIT,repository_research_cutoff='2026-11-11',current_strategy_document='User-supplied Auto2000_Master_AI_Context_Updated (2).md, strategy updated 2026-11-14',precedence='Current user request and 14 November strategy guide proposal work; 11 November repository supplies historical evidence and methods. Earlier no-strategy release boundaries do not reverse the later user-approved strategy.',reviewed_files=[dict(path=p,sha256=hashlib.sha256((ROOT/'auto-data'/p).read_bytes()).hexdigest()) for p in repo_files],crosswalk=crosswalk,cautions=['358 app review IDs are not 358 verified customers.','95 narrative annotation units span 38 source URLs; not independent people.','434 X posts are not 434 new customers and cannot be added to app reviews as unique people.','No relevant earlier raw X-post URLs were identified in the bounded overlap scan; this does not establish person-level independence.','Public repository omits some private source text. Do not imply source-level revalidation of omitted bodies.']))

followup_rows=400+len(lookup_ids)+len(roots)*100+100+32800+2000
save('followup_budget.json',dict(assumed_event_price_usd=.00015,actual_pilot_cost_unknown=True,pilot_export_rows=434,pilot_conditional_result_fee_usd=.0651,preflight_rows=400,parent_lookup_rows=len(lookup_ids),replies_rows=len(roots)*100,programme_claims_rows=100,main_searches=budgets,optional_top_rows=2000,max_new_delivered_rows=followup_rows,new_event_fee_ceiling_usd=round(followup_rows*.00015,4),conditional_pilot_plus_new_event_fees_usd=round((followup_rows+434)*.00015,4),nominal_remainder_of_10_usd_before_actual_platform_costs=round(10-(followup_rows+434)*.00015,4),important=['Bulk inputs and their atomic counterparts are ALTERNATIVES. Running both repeats work and spends extra.','Preflight plus main intentional query overlap is budgeted as delivered rows, not unique-post promises.','Actual remaining balance cannot be computed without pilot and account usage.','Treat previous broad input pack as superseded for this next wave.']))

def write_text(name,t):
 (OUT/name).write_text(t)

write_text('READ_ME_FIRST.txt',f'''AUTO2000 PILOT ANALYSIS AND REVISED FOLLOW-UP
Prepared 14 November 2026. Repository commit {COMMIT}.

START HERE
The pilot is useful for decision discovery, but it is not a clean customer-only corpus. Do not launch the earlier broad bulk inputs unchanged. Use these narrower staged inputs instead. No paid run has been executed by this analysis.

1. Read FINDINGS.txt. Its source is the 434-post uploaded export plus the existing repository, with both kept separate.
2. Run 01_preflight/01_digiroom_external.json first; its exact JSON is ready to paste into xquik/x-tweet-scraper. The other five single-query preflights test different topics. Run 07_batch_control last to compare batching with the single-query path. The six singles are capped at 50 each; batch control is capped at 100. Maximum 400 delivered rows / $0.06 result fees at the assumed rate.
3. In Console set a small charge ceiling for each preflight (e.g. $0.02) and a short timeout (e.g. 180 seconds); these are RUN options, not Actor input JSON keys. Check the displayed result rate for your account and actual cost after each run. A row cap is not an all-in dollar guarantee.
4. Review every returned preflight row. Use verify_followup.py to flag missing literal anchors, date violations and excluded-author matches. It checks query compliance, not whether the post reports a genuine customer experience. Manually inspect up to 50 posts per preflight for buying/service relevance and source role. Proposed gate: investigate any obvious keyword leakage or excluded-author returns; revise a topical query if fewer than about half the inspected compliant posts address its intended decision. This is an operating threshold, not a validated statistical rule. Empty output is not evidence of zero real-world demand.
5. Recover context with 02_context/01_missing_roots_and_parents.json. It contains real missing IDs selected from the pilot. Read the returned roots before running 02_selected_conversation_replies.json. Drop unrelated roots; do not assume every comment under an automotive root is a customer account. Replies mode collects direct replies; missing nested replies are not guaranteed recovered. Use tweetIds or a documented conversation search only for necessary missing context, within remaining spend.
6. 02_context/03_smartdrive_programme_claims.json deliberately includes corporate posts. It is for identifying a published programme and its terms, not measuring customer uptake. Verify an actual written contract/manual on an official source before making any current programme claim.
7. Only after preflight passes, run either FOUR files in 03_bulk_after_checks OR the selected single-query jobs in 04_atomic_searches. NEVER run both versions of the same search. Atomic files give exact requested-query provenance and are the fallback if multi-query batching misbehaves. They also let you skip already-exhausted themes. Do not run all 176 atomic jobs merely because they are supplied.
8. All main searches use simple mandatory quoted terms, no OR expansion, four nonoverlapping 2026 date windows, and explicit exclusions for the two dominant Toyota/Auto2000-branded accounts. Exclusions apply to authors, not customers mentioning those brands. We do not blanket-exclude links, promotions or all seller accounts. Sell-side evidence and genuine user accounts with unrelated business promotion must still be separated after collection. No language filter is used: the pilot labels every record in but includes visibly non-Indonesian content. This change probes language omission and does not establish Indonesian residence. Screen language/market after export.
9. Date-only bounds use UTC. Since is inclusive and until exclusive. The final bound is 14 November 2026 00:00 UTC / 07:00 WIB. Window lengths differ; per-window caps cannot measure posting rates. Exact terms can miss spelling variants and synonyms. Add variants only after a useful theme is demonstrated, and record a new input revision.
10. At the listed $0.00015 rate, main ceilings are P1 9,600 / $1.44; P2 14,400 / $2.16; P3 8,000 / $1.20; shared 800 / $0.12. Suggested Console event-charge ceilings match those amounts. Actual remaining balance must be checked because pilot usage and previous runs are unknown.
11. Optional Top discovery is capped at 2,000 / $0.30. It overlaps Latest intentionally and is a distinct ranked discovery supplement. Do not use it to estimate prevalence. All new stages together cap at {followup_rows:,} delivered rows / ${followup_rows*.00015:.4f} result fees at the assumed rate. Including the 434-row pilot would imply ${(followup_rows+434)*.00015:.4f} result fees before platform usage. This is not your actual invoice or confirmed remaining balance. Stop if actual cumulative costs would exceed the $10 total.
12. Export JSON, submitted input, run ID, run status, actual usage and any diagnostics/run-report together. The pilot export alone did not include those run-level records, so query attribution, underdelivery cause and cost are unknown. Preserve result IDs as strings.

FILES
FINDINGS.txt: interpreted findings and decision implications.
pilot_metrics.json: exact mechanical counts and limitations.
PRIVATE_all_434_screening.csv: full export screened for source/context flags, with pseudonymous author keys; not a validated qualitative classification of every record.
PRIVATE_curated_evidence.csv/.json: 27 purposively selected analytical examples, including exclusions and counterexamples; not 27 independently verified customers or an exhaustive relevance count.
repository_integration.json: repository version, files read and evidence crosswalk.
repository_overlap_audit.json: exact X-status URL scan; not a person-level overlap test.
search_job_manifest.csv: one row per requested atomic search; the request log is not a count of returned matches.
verify_followup.py: local export audit, with no network calls or paid actor execution.
followup_budget.json: conditional event-fee ceilings.

PRIVACY AND INTERPRETATION
PRIVATE files retain source URLs for your internal checks; do not publish the row-level files. Contact emails and common Indonesian phone-number patterns are removed from text copies, and author biographies/media are omitted. This pattern screen is not an anonymity guarantee. Raw export remains unchanged outside this pack. Anonymize public examples and minimize identifying detail.
All qualitative interpretations were produced by one AI analyst, with local arithmetic checks. No human coding reliability, recruitment, dealer fieldwork or offline transaction verification is claimed. Existing repo AI coding is not independent validation of this pilot. Keep unknowns explicit.
The latest 14 November strategy guides the three prongs. The repository is the 11 November evidence baseline. No repository files were changed or pushed.
''')

write_text('FINDINGS.txt',f'''THE PILOT ADDS USEFUL DECISION ACCOUNTS, BUT DOES NOT JUSTIFY SCALING THE ORIGINAL QUERIES UNCHANGED
14 November 2026. Source: dataset_x-tweet-scraper_2026-11-14_09-21-02-237.json.
Repository: https://github.com/Fafauzif/auto-data at {COMMIT}.

WHAT WE ACTUALLY HAVE
434 unique post IDs, 214 distinct author IDs and 409 conversation IDs. No exact full-text duplicates and no native reposts were found. Post timestamps run from 3 January through 13 November 2026 UTC. November contributes 184/434 posts, or 42.4%; that concentration includes noise and cannot establish a demand trend. All supplied language metadata is in, but visibly non-Indonesian text occurs. The post-ID timestamp check agrees within one second for every row; this is an internal consistency check, not proof that the source content or reported offline events are true.

There are 177 replies. The immediate parent is missing for 168 of them (94.9%), comprising 161 distinct missing parent IDs. Across the corpus, 152 distinct conversation roots are missing. Some missing roots have multiple supplied replies, so these counts are not additive people or separate incidents. The 34 quote posts may carry extra context; they do not automatically become independent owner accounts.

The Auto2000-branded account contributes 41 posts and the Toyota-branded account 24: 65/434, or 15.0%. All 29 literal Digiroom mentions are from the Auto2000-branded account. There are 38 literal Auto2000 mentions: 36 by that account, one used-car listing and one community inspection-price recollection. The pilot supplies no independent account of an actual Digiroom task, and no verified Auto2000 work order, delivery, qualified first-time buyer or repeat Auto2000 buyer.

This is not a claim that Digiroom has no users or that no such accounts exist on X. The submitted input, job status, pagination diagnostics and run cost were not included. We cannot distinguish scarce search matches from a cap, interruption, parser issue or changed submitted input. A proposed 1,000-row pilot yielding 434 records is not evidence of complete coverage or budget exhaustion.

QUALITY FINDINGS
The export contains political arguments, military engineering/zeni references, entertainment, foreign vehicle listings and unrelated personal replies. A disclosed mechanical lexicon flags 116 rows with no selected automotive/electrification anchor after removing mentions and URLs. That is not an irrelevant-post count: the lexicon omits valid phrases such as Brio listrik, while some irrelevant political posts still mention Toyota/Innova. The CSV retains this distinction.

Source-role errors would materially distort a naive sentiment run. C16 first sounds like a detailed Ford Everest purchase but explicitly ends as April Fools fiction. C27 sounds like a workshop waiting complaint but is promotional copy from the Auto2000-branded account. C17 mixes a non-hybrid descriptive framing with a hybrid sale specification. Many long persuasive car reviews end with a vehicle-for-sale offer, while C03 appends an unrelated business promotion to a potentially useful self-reported purchase. Neither first-person wording nor a commercial account is a sufficient classification rule by itself.

THE REPOSITORY CHANGES THE SCOPE OF THE GAP
The cloned repository is the research frozen on 11 November, older than the user's 14 November strategy update. Its existing datasets include 358 selected app-review IDs across apps, 95 narrative annotation units across 38 source URLs, and evaluator journeys. These are distinct evidence units, not additive customer samples. In particular, 50 selected Digiroom app reviews already exist; 25 are coded as specific self-reported app interactions. Thirteen records are on/after the 6 December 2025 date boundary and six of those describe specific interactions. Dates do not establish exposure to a particular installed build, and no resulting offline transaction was independently verified. The X gap is therefore incremental-source-specific, not absence of all customer feedback.

An exact status-ID scan of 397 bounded text files in reports/workstreams found no X/Twitter status URL IDs to match against the pilot. That does not establish author/person independence or that every source body is present. The public mirror omits private app-review text and some other source bodies. We have read its reports and derived registers, not independently revalidated all omitted original text. Existing app coding cannot be treated as a second independent confirmation of new X experiences.

PRONG 1: TEST DECISION-RELEVANT ACCURACY, NOT A GENERIC INFORMATION DEFICIT
C01 (pilot row 200) is the strongest specific information-path lead. An owner says they selected a Reborn diesel after reading/asking about a higher annual tax on the Zenix hybrid, then regretted the decision after seeing another figure. The issue to investigate is the source, locality, model/variant, year and correctness of the comparison. It does not verify either tax amount. Recover the missing parent and root before interpreting what triggered the regret.

C02 (row 187) presents a shortlist across Fronx, XL7 and Veloz Hybrid. Two versus three rows, styling, family needs and budget matter together, with Batam-specific figures explicitly mentioned. This illustrates a possible household-fit task, but the poster says they must first accumulate cash. A useful shortlist feature would not necessarily overcome affordability. C24 and C25 further warn that public interest and jokes about insufficient money are not qualified leads or actual abandoned purchases.

Repository IB04 and the live journey challenge already establish a functioning contact-free finance preview, comparisons and dated model-specific service guidance. These posts do not justify claiming that calculators are absent. Test whether a current, locality/variant-specific comparison corrects a consequential misunderstanding and improves a credible next step. The rival is that price, available cash, credit eligibility or stock is binding even when understanding is good. No P1 account establishes no prior Auto2000 vehicle purchase; keep retailer history unknown.

PRONG 2: PRICE, TRUST, JOB SCOPE AND CAPABILITY REQUIRE SEPARATE TESTS
C04 (row 68) is a Yaris Cross Hybrid owner's complaint that fuel savings coexist with perceived tax, insurance, service and resale costs. This is more useful than a general negative label because it specifies categories to separate. It does not contain a service invoice, entitlement, paid job or realized resale loss. Do not feed its statements into a GP model as observed margins or a current service-price benchmark.

C06 (row 431) recounts a friend's Calya clutch/AC repair and subsequent dissatisfaction. It is hearsay without verified workshop identity, invoice or diagnosis. C18 contains a broader workshop-trust complaint. These support interview questions about quote scope, extra-work authorization, parts and handover records; they do not verify misconduct, identify Auto2000 failures or measure how many paid jobs can be won back.

The contrary accounts are important. C05 (row 430) describes choosing official workshops for Toyota and community workshops for other brands. C19 (row 88) reports regular official servicing, C20 (row 418) reports frequent official Toyota care, and C22 (row 416) advises considering a trusted general or specialist garage as an acceptable option. The relevant competitive set is the owner's credible local alternative, not an assumed low-trust generic garage.

C13 discusses post-warranty channels, while the repository already documents advertised OtoXpert and T-OPT economy offerings. A new budget-service tier needs a gap beyond those existing channels. Verify exact parts fitment, job competence, branch capacity, contribution owner and customer trade-off between price and protection. The pilot has not identified a confirmed paid work order switching from an independent garage to Auto2000.

All seven own-text Chery mentions in this export are listings, recommendations, market/resale commentary or promotion. None is a clearly identified personal Chery aftersales episode. C26's instruction to skip Chery is a recommendation, not a service complaint. The repository's eight selected Chery app reviews and published programme sources remain useful but do not fill the missing matched job/branch/fulfillment comparison. Search narrowly for service or warranty episodes, then match powertrain, covered work, payer and outcome. Public xEV support can matter for trust without generating immediate paid GP.

PRONG 3: THE BEST ACCOUNT IS AN UPGRADE STORY WITH UNKNOWN RETAILER HISTORY
C03 (row 134) reports selling an Avanza for Rp190m and purchasing a Veloz Hybrid at Rp354m. Subtracting those reported prices gives Rp164m before loan settlement, fees, taxes and other adjustments. It illustrates a possible upgrade-cost screen, not an observed all-in cash requirement, net equity, verified trade-in settlement or Auto2000 repeat delivery. Fuel-saving calculations in the post are the author's unverified estimates.

C07 (row 1) describes repeated used-Toyota purchases tied to family changes and comfort. It is a direct challenge to a simplistic loyalty-to-new-xEV-conversion story: continuing with Toyota can mean buying used again or retaining the current Innova. C08 (row 119) describes saving operating-cost differences toward a future resale buffer; its missing earlier thread is a high-priority recovery target. Resale uncertainty may be managed by an owner in several ways, not only through a guarantee.

C09 and C10 show inspection advice and a seller's use of Auto2000 service records and a battery-condition claim. Repository JX02/JX07 already establishes a digital Hybrid Health Check retrieval route and BEV trade-in selection. The unresolved bridge is whether an authorized appraiser accepts existing evidence and changes a valid offer. A seller claiming a healthy certified battery is not proof of that bridge or a realized price premium.

C11/C12 are an additional novelty-check lead: two Toyota-branded posts advertise a SmartDrive 70% future-value/upgrade proposition, with conditions in one post. A bounded repository text search found no SmartDrive literal. This deserves a new programme-term check, not immediate acceptance as a current unconditional floor. Verify model/cohort/location, repayment conditions, condition rules, responsible counterparty and settlement mechanics. Both posts share an issuer and claim family; they are not independent confirmations. Do not present a new residual-value guarantee as novel before checking this lead.

WHAT CHANGES IN THE NEXT RUN
The earlier bulk design is superseded for this wave. Six single-query preflights use mandatory quoted terms and one batch-control run tests whether combining searches preserves expected behavior. Two dominant brand authors are excluded from customer-discovery searches; programme checks deliberately retain them. This is a proposed refinement, not a claim that the Actor's parsing has been fixed. There is no basis to identify the cause of the pilot's unrelated results without submitted input and run diagnostics.

The main stage has 176 small dated search targets: 48 buyer targets, 72 workshop/support targets, 40 replacement targets and 16 shared digital targets. Each can be run separately for provenance, or via the four bulk inputs after batching is checked. Choose one route. Four date windows reduce newest-first saturation, but capped queries remain incomplete selections and their lengths differ. Search spelling and exact phrase selection will shape what is found; preserve queries and revisions.

Spend attention first on missing context, the tax/total-cost information path, concrete paid jobs and the actual upgrade story. Limit Digiroom-only X collection to 800 main-stage rows because its pilot yield is entirely corporate. Do not spend thousands of rows repeatedly harvesting brand promotion. Keep a lower-yield finding as a finding and triangulate with the repository's dated app evidence and future task interviews.

HOW TO REPORT IT
Report 434 retrieved posts, 214 author IDs and 27 purposively curated analytical examples, including exclusions and counterexamples. Do not call them 434 customers or 27 confirmed experiences. Source role, model/powertrain, locality, dates, task stage, payer, resolution and retailer history must stay explicit. Unknown is a useful result.

For every proposed mechanism report supporting accounts, the strongest competing explanation, a contrary case and the field test needed. The three business mechanisms remain unmeasured: first-time Auto2000 delivery lift, paid work recovered from independent garages and repeat Auto2000 xEV deliveries. Work orders, current matched quotes, recruitment and a credible all-channel comparison are still needed for incremental GP.

Reproduction and external documentation
The included Python scripts regenerate counts, curated-case exports and proposed inputs. They do not establish human coding reliability. Actor fields checked against https://apify.com/xquik/x-tweet-scraper/input-schema on 14 November 2026. Public listing price of $0.00015 per delivered post is conditional on the account's displayed rate; platform usage is separate. Actual pilot invoice was not provided. Original source stays unchanged; no repository modification or push occurred.
''')

for p in OUT.rglob('*.json'):json.loads(p.read_text())
assert len(roots)==15
assert len(lookup_ids)==len(set(lookup_ids)) and not set(lookup_ids)&PILOT_IDS
assert sum(b['max_rows'] for b in budgets)==32800
print(json.dumps(dict(output=str(OUT),commit=COMMIT,lookup_ids=len(lookup_ids),reply_roots=len(roots),main_jobs=len(manifest),main_rows=32800,total_new_rows=followup_rows,new_fee=round(followup_rows*.00015,4))))
