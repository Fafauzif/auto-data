from pathlib import Path
import json,hashlib,collections

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
MENU=ROOT/'reports/SOLUTION_MENU.json'
AUDIT=ROOT/'workstreams/extension_stakeholders/all_27_option_audit.json'
menu=json.loads(MENU.read_text())
audit={x['solution_id']:x for x in json.loads(AUDIT.read_text())}

# Editorially rewritten against the full concepts and extension counterevidence.
# These are three display fields, not clipped extracts of the technical descriptions.
copy={
1:(
'Auto2000 already compares vehicles and finance costs; Toyota publishes service estimates with an older date.',
'Help a household compare the actual vehicle, budget, journeys and charging arrangement using clearly dated assumptions.',
'Price or stock decides the purchase, or existing advice already settles the choice.'),
2:(
'PLN and qualified installers already support home charging; a nearby charger does not establish permission to use it.',
'Clarify parking rights, building permission, electrical capacity and vehicle compatibility for the customer’s actual charging arrangement.',
'Existing providers resolve readiness, public charging already fits, or the required permission is impossible.'),
3:(
'The finance simulator works before contact entry; SEVA already offers routes toward a lender’s approval decision.',
'Explain which amounts are estimates, what remains unapproved and the customer’s full obligations under an actual offer.',
'The customer already understands the offer, or affordability and underwriting determine the outcome.'),
4:(
'Subscription and commercial rental programmes exist, with different included costs, usage rules and ownership obligations.',
'Compare eligible purchase and subscription contracts for the same use, including end-of-term costs and restrictions.',
'No comparable eligible contract exists, or existing quotes already make the choice clear.'),
5:(
'Work quotations and service records may already exist; this research did not inspect private repair orders.',
'Make necessary work, provisional estimates, approved changes and the final bill understandable within the same service case.',
'Current explanations are sufficient, or the dispute concerns actual repair quality rather than unclear information.'),
6:(
'Booking and guest routes exist; a requested date can still require branch review and confirmation.',
'Make clear whether the customer has requested a visit, received acceptance or secured a specific service commitment.',
'Current confirmations already work, or missing technicians, parts and physical capacity remain the binding problem.'),
7:(
'Current forms and partner instructions already request vehicle details, documents and other task-specific prerequisites.',
'Explain what must happen before a visit, inspection or advertised completion time becomes a realistic commitment.',
'Preparation failures are uncommon, existing advisers resolve them, or extra instructions only increase effort.'),
8:(
'Branch filters, guest booking, home service and body repair routes exist; economical workshops add another existing choice.',
'Clarify which available provider can handle this model and job, including specialist or lower-cost care when relevant.',
'Current routing already works, or reliable capability and availability information cannot be obtained.'),
9:(
'Official parts channels and economical T-OPT parts exist; model lists do not establish every variant’s fit or stock.',
'Explain the actual part’s compatibility, availability, price and any protection consequences before the customer approves work.',
'Existing parts advice suffices, or price and unavailable supply matter more than information.'),
10:(
'Toyota already offers several care and warranty programmes, each with its own eligibility and payment rules.',
'Show which benefits apply to this vehicle now, what expires next and what any paid continuation actually covers.',
'The customer already understands the benefits, is ineligible, or receives better value from existing alternatives.'),
11:(
'Toyota allows remaining warranty to continue for eligible later owners; other programmes have different transfer and use conditions.',
'Explain what a sale, shared use or commercial use changes under the actual contract and ownership record.',
'Existing ownership updates resolve the change, or the relevant contract imposes no consequential restriction.'),
12:(
'Toyota offers eligible battery checks and digital certificates; a certificate does not automatically guarantee resale value.',
'Explain what a specific test measures, its date and limits, and how warranty or appraisal decisions remain separate.',
'The measure is unreliable, existing explanations suffice, or the result changes no meaningful decision.'),
13:(
'mToyota advertises service history; Astra describes customer systems, but private record completeness was not tested.',
'Keep permitted vehicle information useful when the customer moves between service, protection and replacement decisions.',
'Existing records are adequate, information cannot be shared appropriately, or continuity changes no outcome.'),
14:(
'Digital certificates, used-car inspections and BEV trade-in selection exist; appraiser acceptance of each report remains unknown.',
'Determine whether a buyer would use trustworthy condition evidence when making a real inspection and purchase offer.',
'The buyer does not accept the evidence, or market price dominates any useful condition information.'),
15:(
'Trade-in routes already separate an initial estimate from inspection and a later offer; competing bids remain available.',
'Explain why an estimate can change, which conditions matter and what obligations remain at the actual sale.',
'The process is already understood, or dissatisfaction concerns the market price rather than uncertainty.'),
16:(
'Appraisals and trade-in allowances exist; no Auto2000 contract for this proposed extra credit was verified.',
'Offer a clearly limited replacement credit, with its cap understood as different from a guaranteed future value.',
'The subsidy mainly rewards customers who would return anyway, or its cost exceeds additional contribution.'),
17:(
'Some manufacturers offer conditional resale guarantees; this does not establish an equivalent Auto2000 promise or funding.',
'Assess a genuine minimum-value commitment, including who owes the full shortfall and which conditions apply.',
'The guarantor cannot afford or reliably honor the obligation when vehicle prices fall together.'),
18:(
'Digiroom, Toyota apps, advisers and partner services already provide overlapping routes for different ownership jobs.',
'Help customers reach the correct existing service and decision owner without assuming that every route needs consolidation.',
'Customers already find the right route, or clearer navigation cannot resolve the underlying constraint.'),
19:(
'Dealer customer systems and insurer claim channels already exist; shared ownership does not prove useful information transfer.',
'Carry permitted case details into assisted help, while lenders and insurers retain their own decisions.',
'Existing case owners already have the context, or consent and partner authority prevent a useful handoff.'),
20:(
'Toyota already allows another person to deliver a vehicle; G-Fleet provides an existing fleet-monitoring service.',
'Clarify who can view, approve and carry out a task without assuming the driver owns the vehicle.',
'Existing representative processes suffice, or customer and employer permissions cannot support the proposed access.'),
21:(
'Service reminders and loyalty programmes already exist; low-use PHEVs can still have engine and fuel-care needs.',
'Link support to meaningful ownership jobs, including low-use care, without treating frequent app visits as value.',
'Current reminders already work, extra contact adds no value, or fewer messages would miss necessary care.'),
22:(
'OEM and insurer emergency services already exist, with different locations, hours, incident types and entitlement conditions.',
'Clarify who can actually dispatch suitable local help, what it covers and any customer charges.',
'Existing helplines resolve the task, or reliable recovery supply remains unavailable despite clearer information.'),
23:(
'Some programmes already offer conditional transport or replacement vehicles; household backup cars and existing rentals are alternatives.',
'Address a specific essential-mobility shortfall during repair, with clear eligibility, available supply and responsibility for costs.',
'Existing alternatives already suffice, or the required replacement vehicle cannot be supplied economically.'),
24:(
'OEM vehicle-linked services and dealer-assisted setup exist; this research did not authenticate accounts or install native apps.',
'Explain the correct vehicle link, ownership checks and permitted support route when setup does not work.',
'Current setup support succeeds, or the dealer lacks a useful authorized role in resolving the issue.'),
25:(
'Connected services and renewal routes already exist; fleet and private-vehicle contracts can have different terms.',
'Make the actual renewal price, included functions and contract owner clear for this vehicle and customer.',
'The current renewal route already answers the question, or Auto2000 has no useful authorized role.'),
26:(
'EV-specific insurance and claims channels exist; battery wear, manufacturing defects and resale losses are different risks.',
'Help customers compare voluntary cover using the actual vehicle, insured events, exclusions, deductibles and repair-network conditions.',
'Existing policy explanations suffice, the relevant risk is excluded, or no valid distribution arrangement exists.'),
27:(
'Some international insurers cover agreed future-value risks for businesses; an Indonesian syariah contract was not confirmed.',
'Assess whether an actual insurer would accept a defined part of the dealer’s promised future-value exposure.',
'No suitable local contract exists, premiums overwhelm the benefit, or uncovered obligations remain unaffordable.'),
}

cards=[];trace={}
for option in menu['options']:
 ident=option['solution_id'];n=int(ident[-2:]);baseline,addition,kill=copy[n]
 cards.append({'solution_id':ident,'title':option['title'],'family':option['family'],'existing_baseline':baseline,'possible_addition':addition,'what_could_kill_it':kill})
 trace[ident]={'full_solution_path':'reports/SOLUTION_MENU.json','selector':{'solution_id':ident},'consolidated_draft_ids':option['consolidated_draft_ids'],'support_evidence_ids':option['support_evidence_ids'],'counter_or_boundary_evidence_ids':option['counter_or_boundary_evidence_ids'],'full_evidence_locators_field':'evidence_locators','extension_audit_path':'workstreams/extension_stakeholders/all_27_option_audit.json','extension_new_evidence_ids':audit[ident]['new_evidence_ids']}

recall={'candidate_id':'EXT-OPT01','title':'VIN-specific safety-campaign completion across custody changes','family':'Separate extension research candidate','existing_baseline':'Toyota already provides a VIN recall lookup, campaign guidance and dealer booking; missing Auto2000 capability was not established.','possible_addition':'Clarify authorized campaign completion for a current owner or buyer when existing records do not resolve the question.','what_could_kill_it':'Existing processes already provide usable completion evidence, or no consequential unresolved job exists.','status':'Separate from the 27 concepts; conditional research candidate, no winner or implementation selected.','full_candidate_path':'workstreams/extension_stakeholders/new_option_candidates.json','support_evidence_ids':['EXT-E12','EXT-E13','EXT-E20','EXT-E14']}
family_counts=collections.Counter(x['family'] for x in cards)
payload={'as_of':'2026-11-11','purpose':'Concise plain-English display copy for the visual findings PDF; all underlying research remains in the full package.','scope_note':'These are alternatives and coordination or contract layers, not 27 independent needs or additive profit pools. Possible additions are unmeasured hypotheses. The user chooses; no winner or implementation is selected.','reference_document_policy':'The supplied four-page audit PDF is a visual reference only. No unrelated case content, figures or numbers were imported.','family_order':menu['families'],'family_counts':dict(family_counts),'cards':cards,'separate_candidate':recall,'traceability':trace}
(OUT/'solution_cards.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False))
lines=['# Twenty-seven concepts, in plain English','',payload['scope_note'],'']
for fam in menu['families']:
 lines+=['## '+fam,'']
 for c in cards:
  if c['family']!=fam:continue
  lines+=['### '+c['solution_id']+' | '+c['title'],'','**Already exists.** '+c['existing_baseline'],'','**Possible addition.** '+c['possible_addition'],'','**What could kill it.** '+c['what_could_kill_it'],'']
lines+=['## Separate research candidate','',recall['candidate_id']+' | '+recall['title'],'','**Already exists.** '+recall['existing_baseline'],'','**Possible addition.** '+recall['possible_addition'],'','**What could kill it.** '+recall['what_could_kill_it'],'',recall['status'],'']
(OUT/'solution_cards.md').write_text('\n'.join(lines))

counts=[]
for c in cards:
 counts.append({'solution_id':c['solution_id'],'field_word_counts':{f:len(c[f].split()) for f in ('existing_baseline','possible_addition','what_could_kill_it')},'display_words_excluding_title':sum(len(c[f].split()) for f in ('existing_baseline','possible_addition','what_could_kill_it'))})
qa={'method':'Curated editorial rewrite from full menu and extension audit; automatic checks verify identity, family counts and length, not causal truth.','original_menu_sha256':hashlib.sha256(MENU.read_bytes()).hexdigest(),'solution_cards_json_sha256':hashlib.sha256((OUT/'solution_cards.json').read_bytes()).hexdigest(),'solution_cards_md_sha256':hashlib.sha256((OUT/'solution_cards.md').read_bytes()).hexdigest(),'card_count':len(cards),'all_27_ids_exact_order':[c['solution_id'] for c in cards]==[c['solution_id'] for c in menu['options']],'titles_and_families_exact':all(c['title']==o['title'] and c['family']==o['family'] for c,o in zip(cards,menu['options'])),'family_counts_expected_4_5_4_4_4_4_2':[family_counts[x] for x in menu['families']]==[4,5,4,4,4,4,2],'all_under_60_display_words':all(x['display_words_excluding_title']<=60 for x in counts),'card_word_counts':counts,'max_display_words':max(x['display_words_excluding_title'] for x in counts),'min_display_words':min(x['display_words_excluding_title'] for x in counts),'recall_candidate_separate':True,'unrelated_visual_reference_content_imported':False,'original_menu_modified':False,'human_review_claimed':False}
assert qa['card_count']==27 and qa['all_27_ids_exact_order'] and qa['titles_and_families_exact'] and qa['family_counts_expected_4_5_4_4_4_4_2'] and qa['all_under_60_display_words']
(OUT/'solution_cards_QA.json').write_text(json.dumps(qa,indent=2))
print(json.dumps({k:v for k,v in qa.items() if k!='card_word_counts'},indent=2))
