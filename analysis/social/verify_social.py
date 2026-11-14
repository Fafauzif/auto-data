#!/usr/bin/env python3
"""Release checks for source integrity, preserved bodies and analytical boundaries."""
import argparse, csv, hashlib, json, pathlib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', type=pathlib.Path, required=True)
    ap.add_argument('--social-dir', type=pathlib.Path, default=pathlib.Path('.'))
    a = ap.parse_args()
    p = a.social_dir
    sources = list(csv.DictReader(open(p / 'source_runs.csv', encoding='utf-8')))
    raw = {}
    checks = []
    for source in sources:
        f = a.input_dir / source['filename']
        b = f.read_bytes()
        rows = json.loads(b)
        assert hashlib.sha256(b).hexdigest() == source['sha256'], f'changed source {f}'
        assert len(rows) == int(source['rows'])
        raw[f.name] = rows
    checks.append('all 16 original-export SHA256 values and row counts match')
    clean = {platform: {r['record_id']: r for r in map(json.loads, open(p / 'cleaned' / f'{platform}.jsonl', encoding='utf-8'))} for platform in ['x', 'maps', 'youtube']}
    assert {k: len(v) for k, v in clean.items()} == {'x': 14291, 'maps': 8119, 'youtube': 74}
    for platform, rs in clean.items():
        field = 'comment' if platform == 'youtube' else 'text'
        for r in rs.values():
            source = raw[r['selected_source_file']][r['selected_source_row_1_based'] - 1]
            assert r['text_original'] == (source.get(field) or ''), f"text loss {platform}:{r['record_id']}"
    checks.append('all 22,484 selected original bodies survive losslessly and resolve to exact source rows')
    memberships = list(csv.DictReader(open(p / 'record_run_membership.csv', encoding='utf-8')))
    assert len(memberships) == 23351
    for m in memberships:
        assert m['record_id'] in clean[m['platform']]
        assert m['source_filename'] in clean[m['platform']][m['record_id']]['source_files']
    checks.append('all 23,351 source-row memberships retained')
    overlap = [r for r in clean['maps'].values() if r['lowest_rating_diagnostic_member'] and r['has_non_diagnostic_membership']]
    assert len(overlap) == 266
    assert len({r['place_id'] for r in clean['maps'].values()}) == 37
    checks.append('266 cross-cohort overlaps retained as memberships; 37 distinct place IDs')
    assert clean['x']['2068881419091542064']['root_in_corpus'] is True
    assert clean['x']['2068881419091542064']['parent_in_corpus'] is False
    assert '2068876979131355331' in clean['x']
    checks.append('partial EV-saving thread correctly has a supplied root but missing immediate parent')
    digi = [r for r in clean['x'].values() if 'digiroom' in r['text_normalized'].lower()]
    assert len(digi) == 37 and all((r['named_brand_account'] for r in digi))
    checks.append('all 37 literal Digiroom posts are named-brand communication, not independent task accounts')
    annotations = [json.loads(line) for line in open(p / 'youtube_analyst_annotations.jsonl', encoding='utf-8')]
    assert len(annotations) == 74 and {r['record_id'] for r in annotations} == set(clean['youtube'])
    assert not any((r['verified_owner_or_transaction'] for r in annotations))
    checks.append('every returned YouTube comment has an annotation and none is treated as authenticated ownership')
    curated = [json.loads(line) for line in open(p / 'curated_social_evidence.jsonl', encoding='utf-8')]
    assert len(curated) == 45 and len({(r['platform'], r['record_id']) for r in curated}) == 44
    fiction = next((r for r in curated if r['evidence_id'] == 'PILOT_C16'))
    assert 'fiction' in fiction['analyst_role'] and fiction['verified_transaction'] is False
    checks.append('45 analytical entries resolve to 44 source records; explicit fiction remains excluded from actual purchase evidence')
    map_cases = list(csv.DictReader(open(p / 'maps_deep/curated_maps_evidence.csv', encoding='utf-8')))
    assert len(map_cases) == 34 and len({r['review_id'] for r in map_cases}) == 34
    for r in map_cases:
        source_record = clean['maps'][r['review_id']]
        assert r['branch'] == source_record['branch_title_as_source'] and r['place_id'] == source_record['place_id']
    corrected_trade = next(r for r in map_cases if r['evidence_id'] == 'M21')
    assert corrected_trade['review_id'] == 'ChZDSUhNMG9nS0VJQ0FnSURqbDhDVU1REAE' and 'trade in' in corrected_trade['original_review_text_html_cleaned'].lower()
    corrected_readiness = next(r for r in map_cases if r['evidence_id'] == 'M11')
    assert 'ban' in corrected_readiness['original_review_text_html_cleaned'].lower() and 'booking' in corrected_readiness['original_review_text_html_cleaned'].lower()
    checks.append('all 34 Maps cases resolve to matching branch/place sources; M11 readiness and M21 trade-in source corrections remain intact')
    assert sum(r['text_normalized'].lower().count('digiroom') for r in digi) == 45
    checks.append('37 Digiroom-matching posts are distinguished from 45 literal substring occurrences')
    result = {'passed': True, 'checks': checks, 'scope': 'Integrity and interpretation-boundary checks; no authentication of source allegations, identities or offline outcomes.'}
    (p / 'QA_SOCIAL.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
