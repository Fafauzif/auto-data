#!/usr/bin/env python3
"""Verify the private interview overlay and its source and decision references offline."""
import csv
import hashlib
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
INTERVIEWS = 'analysis/interviews/'


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def read_csv(path):
    with (ROOT / path).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))


def require(condition, message):
    if not condition:
        raise SystemExit(f'Interview verification failed: {message}')


def verify_file(entry):
    path = PurePosixPath(entry['path'])
    require(not path.is_absolute() and '..' not in path.parts and '.git' not in path.parts, f'invalid path {path}')
    file = ROOT.joinpath(*path.parts)
    require(file.is_file(), f'missing file {path}')
    require(file.stat().st_size == entry['size_bytes'], f'wrong byte size {path}')
    with file.open('rb') as stream:
        digest = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    require(digest.hexdigest() == entry['sha256'], f'wrong hash {path}')


def references(value):
    return {part.strip() for part in re.split(r'[,;]', value) if part.strip()}


def main():
    manifest = read_json('manifests/interview_overlay.json')
    require(manifest['distribution'] == 'private' and not manifest['deleted_paths'], 'private replacement-only manifest')
    files = manifest['files']
    require(len({entry['path'] for entry in files}) == len(files), 'duplicate overlay paths')
    for entry in files:
        verify_file(entry)

    register = read_json(INTERVIEWS + 'source_register.json')
    ledger = read_json(INTERVIEWS + 'evidence_records.json')
    catalogue = {row['evidence_ref']: row for row in read_json('data/evidence_catalogue.json')}
    insights = {row['insight_id'] for row in read_json('data/insights.json')}
    sources = {row['source_id']: row for row in register['sources']}
    require(register['interview_cases'] == 3 and set(sources) == {'WA', 'YH', 'BA', 'IG'}, 'source count and IDs')
    require(sources['IG']['kind'] == 'interview_protocol', 'unfilled guide is method evidence')
    require(sources['BA']['verbatim_status'].startswith('uncertain'), 'Atto notes must retain verbatim uncertainty')
    inventory = {
        row['logical_path']: row
        for line in (ROOT / 'manifests/source_inventory.jsonl').read_text(encoding='utf-8').splitlines()
        if line and (row := json.loads(line))
    }
    for source in sources.values():
        verify_file(source)
        row = inventory[source['path']]
        require(row['sha256'] == source['sha256'] and row['size_bytes'] == source['size_bytes'], 'source inventory mismatch')

    require(ledger == read_csv(INTERVIEWS + 'evidence_records.csv'), 'CSV and JSON ledger mismatch')
    ledger_ids = {row['evidence_id'] for row in ledger}
    require(len(ledger_ids) == len(ledger) and ledger_ids <= catalogue.keys(), 'missing or duplicate interview evidence IDs')
    for row in ledger:
        ref = row['evidence_id']
        code = row['source_id']
        require(code != 'IG' and row['source_path'] == sources[code]['path'], f'wrong respondent source for {ref}')
        require(row['locator'] == catalogue[ref]['locator'] and row['source_path'] in catalogue[ref]['paths'], f'wrong locator for {ref}')
        if code in {'WA', 'YH'}:
            page_numbers = [int(number) for number in re.findall(r'\d+', row['locator'].split(',')[0])]
            require(page_numbers and all(1 <= n <= sources[code]['pages'] for n in page_numbers), f'invalid PDF page for {ref}')
        else:
            require(row['evidence_type'] in {'summarized_firsthand_account', 'elicited_concept_reaction'}, f'Atto summary boundary for {ref}')
    for code in ('WA', 'YH'):
        require({f'{code}-Q{n:02}' for n in range(1, 13)} <= ledger_ids, f'incomplete question coverage for {code}')
    require({item for item in ledger_ids if item.startswith('BA-')} == {f'BA-A{n:02}' for n in range(1, 7)}, 'wrong Atto answer coverage')
    require(catalogue['BA-A06']['type'] == 'elicited_concept_reaction', 'floor preference must stay elicited')

    matrix = read_csv(INTERVIEWS + 'cross_source_matrix.csv')
    legacy = read_csv(INTERVIEWS + 'legacy_hypothesis_bridge.csv')
    guides = read_csv(INTERVIEWS + 'guide_hypothesis_bridge.csv')
    options = read_csv(INTERVIEWS + 'solution_priority_update.csv')
    for row in matrix + legacy + guides + options:
        require(references(row['interview_refs']) <= ledger_ids, f'unresolved interview reference in {row}')
    for row in matrix:
        require(references(row['prior_refs']) <= catalogue.keys(), f'unresolved comparison source in {row}')
    require({f'I{n:02}' for n in range(1, 11)} <= {row['prior_finding'] for row in matrix}, 'missing baseline finding')
    require([row['hypothesis_id'] for row in legacy] == [f'H{n:02}' for n in range(1, 26)], 'missing legacy hypothesis')
    require({(row['guide_id'], row['local_hypothesis_id']) for row in guides} ==
            {(code, f'H{n}') for code in ('WA', 'YH') for n in range(1, 7)}, 'missing guide hypothesis')
    require([row['solution_id'] for row in options] == [f'SOL-{n:02}' for n in range(1, 28)], 'missing prior option')
    pilot = read_json(INTERVIEWS + 'pilot_decision.json')
    all_refs = catalogue.keys() | insights
    require(set(pilot['evidence_refs']) <= all_refs, 'unresolved pilot reference')
    require(all(references(row['refs']) <= all_refs for row in pilot['workbook_rows']), 'unresolved workbook reference')
    require(pilot['branch_readiness'] == 'unverified', 'pilot must retain the site readiness condition')
    print(json.dumps({
        'passed': True, 'verified_overlay_files': len(files), 'interviews': register['interview_cases'],
        'private_sources': len(sources), 'coded_ledger_entries': len(ledger),
        'cross_source_comparisons': len(matrix), 'prior_hypotheses': len(legacy),
        'guide_hypotheses': len(guides), 'prior_options': len(options)
    }, indent=2))


if __name__ == '__main__':
    main()
