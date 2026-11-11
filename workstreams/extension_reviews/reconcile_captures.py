"""Offline review-ID deduplication, preserving one relation per capture appearance.

Requires private captured records. Public output contains locators, not review text.
The semantic annotations are frozen inputs and are not changed by this operation.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private_cache/extension_reviews'
with (ROOT / 'workstreams/reviews/reviews_derived.csv').open(newline='') as stream:
    old = {r['record_key'] for r in csv.DictReader(stream)}
captures = json.loads((PRIVATE / 'new_captured_review_records.json').read_text())
seen = set()
unique = []
relations = []
for row in captures:
    key = row['platform'] + ':' + row['reviewId']
    row['record_key'] = key
    if key in old:
        relation = 'overlap_original210'
    elif key in seen:
        relation = 'repeat_new_capture_not_new_review'
    else:
        relation = 'new_unique_review'
        seen.add(key)
        unique.append(row)
    relations.append({'record_key':key, 'review_id':row['reviewId'],
        'app':row['app'], 'locale':row['locale'],
        'source_url':row['source_url'], 'source_request_id':row['source_request_id'],
        'source_capture_sha256':row['source_capture_sha256'], 'relation':relation})
annotation_path = OUT / 'new_ai_annotations.json'
if annotation_path.exists():
    annotations = json.loads(annotation_path.read_text())
    assert {r['record_key'] for r in annotations} == {r['record_key'] for r in unique}, \
        'Capture differs from frozen annotations: do not overwrite this research snapshot'
(PRIVATE / 'new_unique_records.json').write_text(json.dumps(unique,indent=2,ensure_ascii=False))
with (OUT / 'capture_relations.csv').open('w',newline='',encoding='utf8') as stream:
    writer = csv.DictWriter(stream,fieldnames=list(relations[0]))
    writer.writeheader()
    writer.writerows(relations)
print({'capture_appearances':len(captures),'new_unique_records':len(unique),
    'original_overlap':sum(r['relation']=='overlap_original210' for r in relations),
    'new_repeat_appearances':sum(r['relation']=='repeat_new_capture_not_new_review' for r in relations)})
