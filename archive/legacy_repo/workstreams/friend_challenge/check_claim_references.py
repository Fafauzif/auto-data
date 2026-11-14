from pathlib import Path
import json,csv
BASE=Path(__file__).parent;ROOT=BASE.parents[1]
J=lambda p:json.loads((ROOT/p).read_text())
L=lambda p:[json.loads(x) for x in (ROOT/p).read_text().splitlines() if x]
refs={
 'market':{r['evidence_id'] for r in J('workstreams/market/evidence.json')},
 'competition':{r['record_id'] for r in J('workstreams/competition/evidence_matrix.json')},
 'journeys':{r['observation_id'] for r in J('workstreams/journeys/journey_observations.json')['observations']} | {r['observation_id'] for r in J('workstreams/journeys/friendcontext_JX_observations.json')['observations']},
 'reviews':{r['evidence_id'] for r in csv.DictReader((ROOT/'workstreams/reviews/reviews_derived.csv').open())},
 'narratives':{r['record_id'] for r in L('workstreams/narratives/narrative_units.jsonl')},
 'validation':{r['record_id'] for r in L('workstreams/narratives/validation_units.jsonl')},
 'logic':{r['test_id'] for r in json.loads((BASE/'logic_tests.json').read_text())},
 'insurance':{r['claim_id'] for r in J('workstreams/friend_insurance/claim_matrix.json')},
 'capabilities':{r['claim_id'] for r in J('workstreams/friend_capabilities/claim_matrix.json')},
 'surveys':{r['claim_id'] for r in J('workstreams/friend_surveys/survey_claims.json')},
 'cadence':{r['evidence_id'] for r in json.loads((BASE/'cadence_checks.json').read_text())}
}
rows=json.loads((BASE/'claims.json').read_text());missing=[]
for row in rows:
 for ref in row['current_evidence_refs']:
  prefix,rid=ref.split(':',1)
  if rid not in refs.get(prefix,set()):missing.append({'claim_id':row['claim_id'],'ref':ref})
result={'claim_groups':len(rows),'referenced_evidence_records':len({ref for row in rows for ref in row['current_evidence_refs']}),'missing_refs':missing,'checks_do_not_validate_claim_truth':True,'JX02_structured_locator_pending':False}
(BASE/'reference_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
assert not missing
