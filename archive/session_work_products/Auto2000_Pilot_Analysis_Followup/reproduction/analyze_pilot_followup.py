import csv, hashlib, json, re
from pathlib import Path
from collections import Counter
from email.utils import parsedate_to_datetime

ROOT=Path('/workspace/scratch/13acdac15ef5')
SRC=ROOT/'upload/dataset_x-tweet-scraper_2026-11-14_09-21-02-237.json'
OUT=ROOT/'Auto2000_Pilot_Analysis_Followup'
OUT.mkdir(exist_ok=True)
D=json.loads(SRC.read_text())
IDS={r['id'] for r in D}

def dump(name,obj):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def redact(t):
    t=re.sub(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b','[email removed]',t)
    t=re.sub(r'(?<!\d)(?:\+?62|0)\d[\d -]{7,}\d(?!\d)','[contact number removed]',t)
    return t

COUNTS=Counter(r['author']['username'] for r in D)
metrics=dict(rows=len(D),unique_post_ids=len(IDS),unique_authors=len({r['author']['id'] for r in D}),unique_conversation_ids=len({r['conversationId'] for r in D}),replies=sum(r['isReply'] for r in D),replies_missing_immediate_parent=sum(r['isReply'] and r.get('inReplyToId') not in IDS for r in D),unique_missing_parent_ids=len({r['inReplyToId'] for r in D if r.get('inReplyToId') and r['inReplyToId'] not in IDS}),unique_missing_root_ids=len({r['conversationId'] for r in D if r['conversationId'] not in IDS}),quote_posts=sum(r['isQuoteStatus'] for r in D),native_reposts=sum(r['isRetweet'] for r in D),date_min=min(parsedate_to_datetime(r['createdAt']) for r in D).isoformat(),date_max=max(parsedate_to_datetime(r['createdAt']) for r in D).isoformat(),monthly_counts=dict(sorted(Counter(parsedate_to_datetime(r['createdAt']).strftime('%Y-%m') for r in D).items())),language_metadata=dict(Counter(r['lang'] for r in D)),zero_like_posts=sum(r['likeCount']==0 for r in D),top_author_counts=COUNTS.most_common(15),digiroom_mentions=sum('digiroom' in r['text'].lower() for r in D),digiroom_mention_authors=dict(Counter(r['author']['username'] for r in D if 'digiroom' in r['text'].lower())),auto2000_literal_mentions=sum('auto2000' in r['text'].lower() for r in D),conditional_event_fee_usd=round(len(D)*.00015,4),actual_run_cost='not provided',actual_submitted_input='not provided',run_status_and_diagnostics='not provided',raw_source_sha256=hashlib.sha256(SRC.read_bytes()).hexdigest())
dump('pilot_metrics.json',metrics)

CASES=[
('C01',199,'P1','self-reported ownership/past choice','Tax information may have shaped the powertrain choice','Owner says they bought a 2025 Reborn diesel after browsing/asking about a higher annual tax on a Zenix hybrid. They express regret after seeing a lower figure.','The post establishes the owner\'s reported information process, not the correct tax or a causal counterfactual. Parent/root are missing.','Test verified city/year/variant-specific tax information alongside financing and household fit.','high'),
('C02',186,'P1/P3','consideration, not purchase','Household capacity competes with design, features and available cash','Poster lists Fronx, XL7 and Veloz Hybrid, distinguishes two versus three rows, states Batam prices and says cash must first be accumulated.','No completed transaction, current vehicle, Auto2000 history or verified quote.','Compare shortlist usefulness on a real household task; financing capacity may remain binding.','high'),
('C03',133,'P3','self-reported purchase with unrelated business promotion appended','Upgrade economics can be expressed as a net cash gap','Poster says an Avanza sold for Rp190m and a Veloz Hybrid was purchased at Rp354m, with fuel savings and comfort motivating the change.','Rp164m is arithmetic on reported prices before loan settlement, fees and other adjustments. Retailer and actual settlement route are unknown. Fuel savings are unverified.','Use a net-upgrade-cost prototype with an explicit loan payoff, fees, quote status and next step.','high'),
('C04',67,'P2_xEV/P3','self-reported ownership, unresolved context','Fuel savings do not automatically mean perceived total ownership value','Yaris Cross Hybrid owner praises fuel economy but complains about tax, insurance, service cost and falling resale value.','No invoice, job, dates of charges or realized resale transaction; immediate parent missing.','Distinguish scheduled covered service, paid jobs, tax and insurance before comparing total costs.','high'),
('C05',429,'P2','self-reported brand-specific provider preference','Owners may choose different workshop channels for different brands','Poster says Toyota and Chinese-brand cars go to official workshops, whereas Honda/Mazda go to community workshops.','No job-level switching episode, price or Auto2000 identification.','Investigate perceived capability, trust and parts access; do not assume owners uniformly avoid official workshops.','high'),
('C06',430,'P2','hearsay allegation','Bill and repair-trust complaints merit verification','Poster recounts a friend\'s Calya clutch and AC bill and a subsequent clutch problem.','Third-party allegation; workshop identity, invoice, work scope and diagnosis are not established. No Auto2000 attribution.','Use as an interview prompt about scope approval and parts traceability, not verified misconduct.','high'),
('C07',0,'P1/P3/P2','self-reported ownership history','Family transitions can support continued used-Toyota ownership','Poster describes Camry to Innova to Fortuner and back to Innova, always used, prioritizing family comfort and repair access.','No Auto2000 purchase history or xEV purchase; continuity with Toyota is not a qualified new-car lead.','Include used-versus-new and retain-current-car alternatives in the replacement journey.','high'),
('C08',118,'P1/P3','self-reported saving behavior, thread fragment','An owner may manage resale risk using operating savings','Poster describes six months of savings and setting money aside against future resale loss.','Vehicle, baseline, amounts and earlier thread sections are missing. No verified net total-cost saving.','Recover the earlier thread and seek contrasting ownership strategies before proposing a guarantee.','high'),
('C09',401,'P2/P3','community advice with explicit uncertainty','Inspection is already discussed as a purchasable service','Community account suggests inspecting a used Toyota hybrid at an official workshop, recalling an Auto2000 inspection fee.','The remembered price is uncertain and not a branch quote, certificate acceptance or completed inspection.','Check the existing service and appraiser acceptance before creating another certificate.','medium'),
('C10',72,'P3','commercial listing','Service records and battery-condition claims already appear in seller positioning','Seller advertises an Altis Hybrid with Auto2000 records and a healthy certified battery.','Not proof of certificate validity, appraisal acceptance, realized premium or completed sale.','Test whether the named appraiser accepts the existing evidence and changes an offer.','medium'),
('C11',135,'P3','Toyota-branded programme communication','A published future-value/upgrade promise is a novelty-check lead','Post advertises a SmartDrive 70% resale-value proposition and a third-year upgrade route with stated conditions.','Uploaded text is not the full contract, current eligibility confirmation, funding commitment or evidence of customer use.','Verify programme terms and responsible counterparties before proposing a new value guarantee.','medium'),
('C12',308,'P3','Toyota-branded programme communication','Repeated SmartDrive messaging is not independent confirmation','A second post from the same account advertises the SmartDrive upgrade proposition.','Same publisher and claim family as C11; no independent uptake evidence.','Group both posts into one programme-claim family.','medium'),
('C13',421,'P2','community generalization','Post-warranty economy channels are already part of discussion','Community post links warranty expiry, independent workshops, CARfix and an economy workshop network.','It does not measure the share leaving dealers, validate commercial relationships or prove price advantage.','Verify OtoXpert/T-OPT capability, participating outlets and contribution ownership.','high'),
('C14',139,'P3_adjacent','shopping question','An upgrade comparison can combine cash difference and use value','Poster asks whether adding Rp100m to move from an older Avanza to an XL7 is worth the comfort, maintenance and efficiency change.','Other-brand and non-confirmed purchase; no xEV or Auto2000-history proof.','Use as an adjacent design case for understandable upgrade economics.','medium'),
('C15',114,'P1/P2','unverified dramatic narrative','Specific incidents cannot be recovered from a generic ownership story','Long narrative describes a friend\'s EV trip, charging failure, a mechanic discussion and claimed subsequent research.','No named model, branch, receipts or source records. Claimed interviews inside the post are not this project\'s interviews.','Treat as a narrative to challenge, not verified EV failure or causal education evidence.','low'),
('C16',382,'exclude_actual_purchase','explicit April Fools fiction','First-person grammar can misclassify fiction as a purchase','The post initially describes a Ford Everest purchase and ends by saying it is an April Fools creative-writing example.','Exclude from actual buyer accounts regardless of persuasive detail or engagement.','Add satire/fiction checks before purchase-outcome classification.','exclude'),
('C17',76,'commercial_quality_check','sales listing with inconsistent vehicle framing','Powertrain cannot safely be inferred from one keyword','The descriptive review contrasts Zenix with a hybrid sibling while the listing specifies a Zenix Q Hybrid.','Commercial and internally ambiguous; no independent product assessment or confident powertrain label.','Use ambiguous powertrain until exact vehicle evidence resolves the inconsistency.','exclude_primary'),
('C18',97,'P2','self-reported brand use plus broad complaint','Service trust concerns may coexist with longstanding Toyota use','Poster identifies longstanding Toyota use and complains about fuel loss at official workshops. A separate reply in the export echoes the experience.','No named workshop, completed-job details or verified explanation. The second account is conversational corroboration, not causal verification.','Ask about handover records, job communication and explanations, retaining positive accounts as contrasts.','high'),
('C19',87,'P2','self-reported maintenance','Official workshop retention is a necessary counterexample','Poster describes Freed/Fortuner ownership and consistently using official workshops while discussing replacement batteries.','Not a measured retention rate or evidence about Auto2000 specifically.','Recruit loyal official-workshop users alongside switchers.','medium'),
('C20',417,'P2','self-reported use/maintenance','Heavy use may sustain official-service demand','Poster describes a heavily used Veloz and monthly official Toyota workshop care.','Job mix, commercial use, paid-versus-covered status and dates are not established.','Test job and usage intensity rather than assuming a uniform maintenance cadence.','medium'),
('C21',419,'P2','community advice plus self-reported other-brand service','Capability can depend on vehicle age and technician familiarity','Poster mentions servicing an older Taft at an official Daihatsu workshop and suggests older technicians may understand older cars better.','Other-brand experience and general advice; not a measured Toyota capacity problem.','Validate branch/job/technician capability for the chosen older-Toyota job.','medium'),
('C22',415,'P2/P1','advice','A credible specialist may substitute for an official workshop','Account recommends considering nearby official, specialist or trusted general workshops before buying a used car.','Advice does not establish where the author paid for their last job.','Benchmark local trusted specialists, not just the cheapest generic garage.','high'),
('C23',127,'shared_adjacent','third-party allegation about another brand','Retailer responsibility and payment provenance can matter in handoff failures','Poster recounts alleged problems with another brand\'s dealer, trade-in, payments and complaint handling.','Unverified third-party allegation; not evidence against Auto2000 or a verified regulatory finding.','Use only as an adjacent scenario for official quote/payment channels and accountable ownership.','low'),
('C24',115,'P1','aspiration with humorous budget admission','Stated interest need not indicate a qualified near-term buyer','Poster expresses interest in EV running-cost savings and concern about resale, then says available money is only Rp2m.','No quote, credit eligibility or completed purchase; humor complicates seriousness.','Separate curiosity, serious shopping and financially qualified next steps.','medium'),
('C25',375,'P1','humorous affordability statement','Jokes are discourse evidence, not demand estimates','Post lists technical barriers as crossed out and says lack of money is the reason for not buying.','Not a verified abandoned transaction or willingness-to-pay observation.','Use only to motivate an affordability probe, not estimate lost sales.','low'),
('C26',184,'P1_competitor','recommendation only','A brand rejection is not an aftersales experience','Poster ranks hybrid alternatives and says to skip Chery.','No Chery ownership, service interaction, job or reason supplied.','Do not count this as a Chery aftersales complaint.','exclude_aftersales'),
('C27',50,'shared','Auto2000-branded promotional scenario','An apparent waiting-time complaint is actually brand copy','Auto2000-branded post imagines a cancelled date after waiting at a workshop and promotes Digiroom booking.','Not an independent customer\'s failed booking or appointment outcome.','Classify source role before sentiment; keep brand promises separate from fulfillment evidence.','exclude_customer')
]

case_records=[]
for cid,i,prong,typ,finding,evidence,limit,implication,priority in CASES:
    r=D[i]
    case_records.append(dict(case_id=cid,pilot_row_1_based=i+1,post_id=r['id'],conversation_id=r['conversationId'],parent_id=r.get('inReplyToId'),prong=prong,evidence_type=typ,finding=finding,evidence_paraphrase=evidence,limitation=limit,test_implication=implication,followup_priority=priority,source_url_private=r['url'],text_private_redacted=redact(r['text'])))
dump('PRIVATE_curated_evidence.json',case_records)
fields=[k for k in case_records[0] if k!='text_private_redacted']
with (OUT/'PRIVATE_curated_evidence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows({k:r[k] for k in fields} for r in case_records)

ANCHOR=re.compile(r'\b(?:toyota|innova|inova|avanza|fortuner|calya|agya|yaris|zenix|veloz|bz4x|corolla|hybrid|hev|bev|phev|mobil|bengkel|servis|sparepart|chery|byd|wuling|hyundai|digiroom|auto2000|olxmobbi|carsome|otoexpert)\b',re.I)
case_map={c['post_id']:c['case_id'] for c in case_records}
screen=[]
for i,r in enumerate(D):
    body=re.sub(r'https?://\S+|@\w+',' ',r['text'])
    flags=[]
    if not ANCHOR.search(body): flags.append('no_lexical_anchor_not_an_irrelevance_verdict')
    if r['author']['username'] in {'AUTO2000ID_','ToyotaID'}:flags.append('brand_named_account_separate_from_customer_evidence')
    if r['isReply'] and r.get('inReplyToId') not in IDS:flags.append('parent_missing')
    if r['conversationId'] not in IDS:flags.append('root_missing')
    if i==382:flags.append('explicit_fiction_exclude_purchase')
    if i==76:flags.append('internally_ambiguous_powertrain')
    screen.append(dict(pilot_row_1_based=i+1,post_id=r['id'],author_key=hashlib.sha256(r['author']['id'].encode()).hexdigest()[:12],created_at_utc=parsedate_to_datetime(r['createdAt']).isoformat(),is_reply=r['isReply'],is_quote=r['isQuoteStatus'],parent_id=r.get('inReplyToId'),conversation_id=r['conversationId'],case_id=case_map.get(r['id'],''),screen_flags=';'.join(flags),text_private_redacted=redact(r['text']),source_url_private=r['url']))
with (OUT/'PRIVATE_all_434_screening.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(screen[0]));w.writeheader();w.writerows(screen)
metrics['no_lexical_anchor_count']=sum('no_lexical_anchor' in r['screen_flags'] for r in screen)
metrics['no_lexical_anchor_caution']='A mechanical audit flag, not a count of irrelevant posts; lexicon omits some valid terms such as Brio.'
dump('pilot_metrics.json',metrics)

print(json.dumps(dict(rows=len(D),curated_cases=len(CASES),out=str(OUT))))
