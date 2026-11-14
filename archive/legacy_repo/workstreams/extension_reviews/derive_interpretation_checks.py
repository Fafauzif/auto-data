"""Offline ER-T05 source-inspection outputs and explicitly exploratory checks.

Semantic labels are frozen AI inputs. Counts describe the displayed records only.
No p-values, customer populations, causal effects or completed jobs are estimated.
"""
import collections
import csv
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
old = list(csv.DictReader((ROOT / 'workstreams/reviews/reviews_derived.csv').open()))
new = list(csv.DictReader((OUT / 'new_reviews_derived.csv').open()))
def export(name, rows):
    with (OUT / name).open('w', newline='', encoding='utf8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

groups = collections.defaultdict(list)
for row in new:
    groups[(row['app'], row['locale'])].append(row)
summary = []
for (app, locale), group in sorted(groups.items()):
    for label, selected in [('all_stars', group), ('stars4_5', [r for r in group if int(r['rating']) >= 4])]:
        counts = collections.Counter(r['report_type'] for r in selected)
        summary.append({'wave':'extension_new', 'app':app, 'locale':locale, 'subset':label,
            'subset_n':len(selected), **{k+'_n':counts[k] for k in [
                'success_report','constraint_or_failure_report','recovery_report',
                'feature_request_or_concern','generic_nonjob','mixed_or_unclear']},
            'selected_listing_records_not_population':True})
export('ER_T05_new_report_types.csv', summary)

# A purposeful set fixed before calculation. Preserve old frozen primary labels.
specified = json.loads((OUT / 'PRESPECIFIED_COUNTEREXAMPLES.json').read_text())['record_ids']
old_types = {
    'REV-0001':('generic_nonjob','rating_before_reported_service'),
    'REV-0003':('mixed_or_unclear','booking_help_and_multivehicle_constraint'),
    'REV-0020':('generic_nonjob','positive_rating_without_vehicle'),
    'REV-0030':('constraint_or_failure_report','booking_cancelled_offline_alternative'),
    'REV-0035':('constraint_or_failure_report','repeated_booking_unanswered'),
    'REV-0122':('constraint_or_failure_report','high_rating_missing_images_historical'),
    'REV-0130':('recovery_report','access_restored_after_update_historical'),
    'REV-0141':('feature_request_or_concern','charging_control_wish_not_absence_proof'),
    'REV-0165':('mixed_or_unclear','booking_possible_other_access_scope_constraints'),
    'REV-0205':('mixed_or_unclear','charging_controls_reportedly_added_remaining_friction'),
}
cards = []
for row in old:
    if row['evidence_id'] not in specified:
        continue
    report_type, interpretation = old_types[row['evidence_id']]
    cards.append({k:row[k] for k in ['evidence_id','record_key','app','platform','locale',
        'review_date','rating','review_version','experience_status','source_url']})
    cards[-1].update(wave='original210', report_type=report_type,
        interpretation_code=interpretation, source_inspected_by_ai=True,
        human_validation=False, independent_outcome_verification=False,
        selection='purposeful_precalculation_known_counterexample_not_blind_holdout')
export('ER_T05_original_counterexamples.csv', cards)

# The Suzuki release spans car and motorcycle parts. This new-wave-only check
# deliberately retains unspecified context rather than guessing vehicle type.
suzuki = [r for r in new if r['app']=='my_suzuki']
context = []
for kind in ['motorcycle_explicit','car_explicit','vehicle_unspecified']:
    selected = [r for r in suzuki if r['vehicle_context_reported']==kind]
    context.append({'app':'my_suzuki','wave':'extension_new',
        'vehicle_context_reported':kind,'selected_source_n':len(selected),
        'specific_reported_app_job_n':sum(r['experience_status']=='self_reported_app_job' for r in selected),
        'year2026_n':sum(r['review_date'][:4]=='2026' for r in selected),
        'stars4_5_n':sum(int(r['rating'])>=4 for r in selected),
        'exploratory_post_acquisition':True,
        'vehicle_type_not_inferred_for_unspecified':True})
export('EX_Suzuki_vehicle_context_sensitivity.csv', context)

# Does a different public language selection change apparent recency? This
# implements the source-selection question without pooling brand scores.
recency = []
for app in sorted({r['app'] for r in old+new}):
    for wave, data in [('original210',old),('extension_new',new)]:
        selected = [r for r in data if r['app']==app]
        if not selected:
            continue
        recency.append({'app':app,'wave':wave,'selected_source_n':len(selected),
            'year2026_n':sum(r['review_date'][:4]=='2026' for r in selected),
            'year2026_and_source_version_present_n':sum(r['review_date'][:4]=='2026' and r['review_version'] not in ('','None','null') for r in selected),
            'earliest_source_date':min(r['review_date'][:10] for r in selected),
            'latest_source_date':max(r['review_date'][:10] for r in selected),
            'source_selection_not_temporal_trend':True})
export('ER_T06_wave_recency_sensitivity.csv', recency)

receipt = {'calculated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'original_counterexample_n':len(cards),'new_ai_report_type_n':len(new),
    'new_favorable_rating_n':sum(int(r['rating'])>=4 for r in new),
    'new_favorable_constraint_n':sum(int(r['rating'])>=4 and r['report_type']=='constraint_or_failure_report' for r in new),
    'new_favorable_mixed_n':sum(int(r['rating'])>=4 and r['report_type']=='mixed_or_unclear' for r in new),
    'old_primary_annotations_modified':False,
    'suzuki_vehicle_context_check_post_acquisition':True,
    'human_validation':False,'population_or_task_completion_measurement':False,
    'plan_sha256':json.loads((OUT/'prespecification_receipt.json').read_text())['plan_sha256']}
(OUT/'interpretation_summary.json').write_text(json.dumps(receipt,indent=2))
print(json.dumps(receipt,indent=2))
