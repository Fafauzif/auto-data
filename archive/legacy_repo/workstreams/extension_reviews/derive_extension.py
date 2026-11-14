"""Offline metadata derivation. Full review text is a private input, never an output.

The AI source annotations are a frozen research input, not a classifier trained or
validated on an independent human gold standard. This script checks provenance,
joins nontext fields, and does not regenerate semantic judgments.
"""
from pathlib import Path
import csv
import collections
import datetime
import hashlib
import json
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
raw_path = ROOT / 'private_cache/extension_reviews/new_unique_records.json'
raw = json.loads(raw_path.read_text())
annotations = json.loads((OUT / 'new_ai_annotations.json').read_text())
annotated = {r['record_key']: r for r in annotations}
with (ROOT / 'workstreams/reviews/reviews_derived.csv').open(newline='') as stream:
    old = list(csv.DictReader(stream))
old_keys = {r['record_key'] for r in old}
assert len(annotated) == len(raw) == 148
assert len({r['record_key'] for r in raw}) == len(raw)
assert not old_keys.intersection(annotated)
connection = sqlite3.connect(f'file:{ROOT / "private_cache/transport.sqlite"}?mode=ro', uri=True)
rows = []
for source in raw:
    annotation = annotated[source['record_key']]
    content_sha = hashlib.sha256((source.get('content') or '').encode()).hexdigest()
    assert annotation['source_text_sha256'] == content_sha
    request = connection.execute('SELECT started FROM requests WHERE id=?', (source['source_request_id'],)).fetchone()
    assert request
    capture_utc = datetime.datetime.fromtimestamp(request[0], datetime.timezone.utc).isoformat()
    record = {
        'evidence_id': annotation['evidence_id'], 'record_key': source['record_key'],
        'app': source['app'], 'app_id': source['app_id'], 'platform': source['platform'],
        'locale': source['locale'], 'review_id': source['reviewId'],
        'review_date': source['at'], 'rating': source['score'],
        'review_version': source.get('reviewCreatedVersion') or '',
        'developer_reply_present': bool(source.get('developer_reply_present')),
        'published_source_epoch': source['published_source_epoch'],
        'source_url': source['source_url'], 'source_request_id': source['source_request_id'],
        'source_capture_sha256': source['source_capture_sha256'],
        'source_capture_utc': capture_utc, 'source_text_sha256': content_sha,
        'wave': 'extension_new', 'selection': source['selection'],
        'experience_status': annotation['experience_status'],
        'report_type': annotation['report_type'], 'paraphrase_code': annotation['paraphrase_code'],
        'vehicle_context_reported': annotation['vehicle_context_reported'],
        'source_inspected_by_ai': True, 'human_validation': False,
        'independently_verified': False, 'reviewer_residence_verified': False,
        'second_ai_checked': annotation['second_ai_checked'],
        'eligible_for_app_task_analysis': annotation['experience_status'] == 'self_reported_app_job',
        'coding_method': 'source_grounded_AI_reading_frozen_annotation_join',
    }
    rows.append(record)
connection.close()
with (OUT / 'new_reviews_derived.csv').open('w', newline='', encoding='utf8') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
validation = {
    'calculated_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'raw_input_unique_n': len(raw), 'new_public_rows': len(rows),
    'old_new_overlap_n': len(old_keys.intersection(annotated)),
    'combined_unique_review_ids': len(old) + len(rows),
    'new_evidence_ids_unique': len({r['evidence_id'] for r in rows}) == len(rows),
    'new_source_urls_n': len({r['source_url'] for r in rows}),
    'new_source_request_ids_n': len({r['source_request_id'] for r in rows}),
    'source_text_hash_matches_n': len(rows),
    'captured_source_timestamp_joined_n': len(rows),
    'ratings_in_1_5': all(1 <= int(r['rating']) <= 5 for r in rows),
    'complete_source_locators': all(r['review_id'] and r['source_url'] for r in rows),
    'no_author_contact_or_review_text_columns': not {'userName','userImage','content','title','replyContent','email','phone','handle'}.intersection(rows[0]),
    'source_inspected_by_one_ai_n': len(rows),
    'source_inspected_by_second_ai_n': sum(r['second_ai_checked'] for r in rows),
    'human_validation': False, 'independent_service_outcomes_measured': False,
    'status_counts': dict(collections.Counter(r['experience_status'] for r in rows)),
    'report_type_counts': dict(collections.Counter(r['report_type'] for r in rows)),
    'vehicle_context_counts': dict(collections.Counter(r['vehicle_context_reported'] for r in rows)),
}
(OUT / 'validation.json').write_text(json.dumps(validation, indent=2))
print(json.dumps(validation, indent=2))
