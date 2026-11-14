from pathlib import Path
import json,csv
out=Path(__file__).resolve().parent;root=out.parents[1]
journey=json.loads((root/'workstreams/journeys/journey_observations.json').read_text());ux={r['observation_id']:r for r in journey['observations']};cards=json.loads((out/'option_cards.json').read_text())
M={
1:(['UX12'],'Website already has app-store destinations; destination/app/deep-link behavior unverified.','Role confusion or integration gap not established.'),
2:(['UX05','UX06','UX07','UX12'],'Test-drive, workshop, trade-in and app routes exist with task-specific prerequisites.','Actual context transfer to staff/app untested; do not label failed continuity.'),
3:(['UX05','UX08'],'Test-drive page says team will contact customer; tentative date windows exist. B&P calendar was inspected only partially.','Some status qualification is already present; do not propose confirmation wording as wholly absent.'),
4:(['UX05','UX06','UX07'],'Existing task forms specify purchase/vehicle/plate/mileage requirements before later stages.','Need for additional preparation guidance is untested; field necessity not judged.'),
5:([],'No current full entitlement comprehension or vehicle-linked programme walkthrough in these12cells.','Untested gap; competitor programme complexity alone is not demand.'),
6:([],'No ownership-transfer entitlement walkthrough or participant evidence.','Untested gap; first-owner restrictions cannot imply actual resale confusion.'),
7:([],'No fleet-specific journey was tested.','Untested audience need, terms and route; no fleet product recommendation.'),
8:([],'No current Digiroom/website battery-certificate interpretation task was tested.','Existing OEM certificate must remain baseline; current Auto2000 gap unknown.'),
9:(['UX07'],'Auto2000 already describes professional inspection and subsequent trade-in offer.','No estimate or evidence exchange generated; appraiser acceptance and value untested.'),
10:(['UX07'],'Professional inspection and subsequent offer are already explained on the trade-in page.','Distinction may already be adequate; partial boundary prevents assessment of estimate presentation.'),
11:(['UX07'],'Trade-in prerequisites were observed but no completed transaction/payment timing.','No timing mismatch established; OLX operator terms are not Auto2000 achieved performance.'),
12:(['UX03','UX04'],'A functioning no-contact simulator returns multiple tenor options; insurance/first-installment timing is disclosed.','Do not propose a missing simulator or hidden-fee diagnosis; prequalification/approval/expiry remain different untested states.'),
13:(['UX11'],'Toyota OEM form explicitly allows delivery by someone else; not a household finance task.','Roles can differ, but household financial coordination pain remains unmeasured.'),
14:([],'No fitment/parts purchase task in the available12cells.','Untested gap; warranty terms do not establish compatibility friction.'),
15:(['UX02','UX03','UX04'],'Model comparison and repeatable credit scenarios already exist; insurance timing changes cash/cicilan outputs.','New value must address a specific unresolved ownership comparison; affordability and comprehension remain unmeasured.'),
16:([],'No paid-protection decision task tested.','Untested gap; rival package price is not Auto2000 cost or willingness to pay.'),
17:(['UX08'],'B&P branch lookup works for Bekasi and opens named specialist branch/calendar before plate entry.','Reject blanket absence of specialist locator; current ambiguous date state cannot establish capacity or harmful misrouting.'),
18:([],'No location-qualified emergency support fulfillment was tested.','Untested gap; competitor scope does not prove local Auto2000 failure.'),
19:([],'No current breakdown/onward-mobility decision task tested.','Untested gap and demand; no actual partner/control/cost basis.'),
20:(['UX06','UX09'],'Workshop and home-service forms already impose vehicle-to-service-to-location sequencing.','Do not propose home service as absent; early context suitability and scope utility remain untested.'),
21:(['UX12'],'Website app destinations observed; no vehicle-connected account setup or transfer tested.','No observed dealer setup gap; OEM security/control limits remain.'),
22:([],'No subscription renewal or linked vehicle contract task tested.','Untested gap; independent dealer revenue role unknown.'),
23:(['UX11'],'Toyota OEM service form already recognizes a person other than owner can deliver the vehicle.','Avoid claiming all flows assume owner=driver; multi-account and fleet needs untested.'),
24:([],'No current programme-eligibility decision/comprehension task tested.','Conditional-service facts support a research question, not evidence of retention loss.'),
25:(['UX01','UX02'],'Catalogue and comparison expose apparent numeric anomalies and different bZ4X price representations.','Reconcile model/year/variant/location/date before calling stale or misleading; not a proven campaign problem.')
}
rows=[]
for i,c in enumerate(cards,1):
 ids,cap,limit=M[i]
 assert all(u in ux for u in ids)
 c.update(root_journey_evidence_ids=ids,existing_auto2000_capability_observed=cap,auto2000_gap_status=limit,integration_status='Reconciled against desktop-only logged-out12cell AI evaluator record; no participant/app/mobile claims')
 rows.append(dict(option_id=c['option_id'],journey_ids=' | '.join(ids),observed_existing_capability=cap,remaining_gap_status=limit,user_decision_status='Candidate only; no winner/implementation'))
(out/'option_cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2))
with (out/'option_journey_reconciliation.csv').open('w',newline='',encoding='utf8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'option_journey_reconciliation.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (out/'option_cards.csv').open('w',newline='',encoding='utf8') as f:
 rs=[{**c,'affected_stakeholders':' | '.join(c['affected_stakeholders']),'evidence_ids':' | '.join(c['evidence_ids']),'root_journey_evidence_ids':' | '.join(c['root_journey_evidence_ids'])} for c in cards];w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
md=(out/'option_cards.md').read_text();md+='\n\n## Reconciliation with observed Auto2000 journeys\n\nThe companion option_journey_reconciliation table is authoritative for current baseline caveats. The available12cells are desktop-only logged-out AI walkthroughs, not app/mobile/participant tests. Existing simulation, comparison, specialist lookup, home/workshop and inspection routes were observed. Candidates must not claim those capabilities are absent.\n'
for r in rows:md+=f"\n- {r['option_id']} ({r['journey_ids'] or 'not tested in available journeys'}): {r['observed_existing_capability']} {r['remaining_gap_status']}\n"
(out/'option_cards.md').write_text(md)
print('Reconciled25options against',len(ux),'journeycells')
