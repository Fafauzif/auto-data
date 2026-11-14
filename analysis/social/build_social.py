#!/usr/bin/env python3
"""Offline, standard-library social corpus normalisation. No paid/network calls.

Usage: python build_social.py --input-dir ../../upload --output-dir .
Heuristic tags are retrieval flags, never validated sentiment/ownership labels.
"""
import argparse, collections, csv, datetime as dt, hashlib, html, json, pathlib, re
from email.utils import parsedate_to_datetime

def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False).replace('\u2028', '\\u2028').replace('\u2029', '\\u2029').replace('\x85', '\\u0085') + '\n')

def table(path, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else [])
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

def clean(text):
    return re.sub('[ \\t]+', ' ', re.sub('<br\\s*/?>', '\n', html.unescape(text or ''), flags=re.I)).strip()
PATTERNS = {'first_person': '\\b(?:saya|aku|gue|gua|gw|sy|ane|kami|my|i)\\b', 'toyota': 'toyota|innova|inova|avanza|fortuner|calya|agya|yaris|zenix|veloz|corolla|kijang|alphard|rush|sienta|raize|bz4x', 'retailer': 'auto\\s?2000|digiroom|otoxpert|otoexpert|t-opt', 'electrification': '\\bhybrid\\b|\\bhe[vb]\\b|\\bbev\\b|\\bphev\\b|mobil listrik|molis|\\bev\\b|\\bbyd\\b|wuling|neta|ioniq', 'workshop': 'bengkel|\\bberes\\b|servis|service|ganti oli|spare\\s?part|suku cadang|kampas|kaki.kaki|perawatan', 'booking_wait_handoff': 'booking|antri|antre|nunggu|menunggu|jadwal|konfirmasi|serah.terima|test.?drive|tes.?drive', 'resale_upgrade': 'jual lagi|jual mobil|tukar tambah|trade.?in|appraisal|resale|harga bekas|harga jual|upgrade|ganti mobil', 'home_charging': 'wall.?charg|home.?charg|ngecas.*rumah|cas.*rumah|meteran|daya listrik', 'selling_or_marketing_marker': '#titipjual|for sale|ready stock|hubungi|wa.me|cash.*nego|dp mulai|cicilan mulai|booking fee|promo.*(?:beli|servis|service)|jual.*(?:cash|nego)', 'motorcycle_marker': 'sepeda motor|bengkel motor|servis motor|service motor|\\bmotor\\b|yamaha|honda beat|vario|nmax|aerox|scoopy', 'news_or_commentary_marker': 'berita|menurut laporan|dilansir|gaikindo|penjualan nasional|market share|pangsa pasar'}
RX = {k: re.compile(v, re.I | re.S) for k, v in PATTERNS.items()}

def flags(text):
    return [k for k, rx in RX.items() if rx.search(text)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input-dir', type=pathlib.Path, required=True)
    ap.add_argument('--output-dir', type=pathlib.Path, default=pathlib.Path('.'))
    a = ap.parse_args()
    out = a.output_dir
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(a.input_dir.glob('dataset*json'))
    sources = []
    raw = collections.defaultdict(list)
    for p in files:
        platform = 'x' if 'x-tweet' in p.name else 'maps' if 'Google-Maps' in p.name else 'youtube' if 'youtube' in p.name else None
        if not platform:
            continue
        rows = json.loads(p.read_text(encoding='utf-8'))
        b = p.read_bytes()
        cohort = 'lowest_rating_diagnostic' if '12-13-55' in p.name else 'four_city_auto2000_latest' if '12-04-38' in p.name else 'four_city_shopdrive_latest' if '12-13-10' in p.name else 'jabodetabek_selected' if platform == 'maps' else 'selected_query_run' if platform == 'x' else 'selected_videos_comments'
        sources.append({'source_id': p.stem, 'filename': p.name, 'platform': platform, 'rows': len(rows), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'cohort': cohort})
        raw[platform].extend(((r, p.name, cohort, i + 1) for i, r in enumerate(rows)))
    table(out / 'source_runs.csv', sources)
    memberships = []
    conflicts = []
    norm = {}
    summary = {}
    for platform, entries in raw.items():
        grouped = collections.defaultdict(list)
        for r, filename, cohort, rownum in entries:
            ident = str(r.get('id') if platform == 'x' else r.get('reviewId') if platform == 'maps' else r.get('cid'))
            if ident in ('None', ''):
                raise ValueError(f'missing source ID {filename}:{rownum}')
            grouped[ident].append((r, filename, cohort, rownum))
            memberships.append({'platform': platform, 'record_id': ident, 'source_filename': filename, 'source_row_1_based': rownum, 'cohort': cohort})
        rows = []
        for ident, variants in sorted(grouped.items()):
            textfield = 'comment' if platform == 'youtube' else 'text'
            chosen = max(variants, key=lambda z: (len(z[0].get(textfield) or ''), z[1]))
            r = chosen[0]
            bodies = {r0.get(textfield) or '' for r0, *_ in variants}
            if len(bodies) > 1:
                conflicts.append({'platform': platform, 'record_id': ident, 'body_variants': len(bodies), 'source_files': ';'.join(sorted({v[1] for v in variants})), 'resolution': 'richest_body_then_latest_export_filename'})
            text = clean(r.get(textfield))
            base = {'record_id': ident, 'platform': platform, 'text_original': r.get(textfield) or '', 'text_normalized': text, 'retrieval_flags': flags(text), 'source_files': sorted({v[1] for v in variants}), 'cohorts': sorted({v[2] for v in variants}), 'source_row_count': len(variants), 'selected_source_file': chosen[1], 'selected_source_row_1_based': chosen[3]}
            if platform == 'x':
                author = r.get('author') or {}
                username = author.get('username') or ''
                aid = str(author.get('id') or username)
                try:
                    created = parsedate_to_datetime(r['createdAt']).isoformat()
                except (ValueError, TypeError, KeyError):
                    created = r.get('createdAt')
                parent = str(r.get('inReplyToId') or '')
                base.update({'created_at_utc': created, 'language_metadata': r.get('lang'), 'author_key': hashlib.sha256(aid.encode()).hexdigest()[:20], 'author_username_private': username, 'source_url': r.get('url'), 'conversation_id': str(r.get('conversationId') or ''), 'parent_id': parent, 'is_reply': bool(r.get('isReply')), 'is_quote': bool(r.get('isQuoteStatus')), 'is_repost': bool(r.get('isRetweet')), 'parent_in_corpus': parent in grouped if parent else None, 'root_in_corpus': str(r.get('conversationId') or '') in grouped, 'named_brand_account': username.lower() in {'auto2000id_', 'toyotaid'}, 'like_count': r.get('likeCount'), 'reply_count': r.get('replyCount'), 'view_count': r.get('viewCount'), 'ownership_or_transaction_verified': False})
            elif platform == 'maps':
                base.update({'place_id': r.get('placeId'), 'cid': r.get('cid'), 'branch_title_as_source': r.get('title'), 'city_as_source': r.get('city'), 'location_as_source': r.get('location'), 'review_published_at': r.get('publishedAtDate'), 'visit_time_as_source': r.get('visitedIn'), 'stars': r.get('stars'), 'owner_response': clean(r.get('responseFromOwnerText')), 'permanently_closed': r.get('permanentlyClosed'), 'temporarily_closed': r.get('temporarilyClosed'), 'original_language_metadata': r.get('originalLanguage'), 'place_source_url': r.get('url'), 'review_source_url': r.get('reviewUrl'), 'has_text': bool(text), 'lowest_rating_diagnostic_member': any((v[2] == 'lowest_rating_diagnostic' for v in variants)), 'has_non_diagnostic_membership': any((v[2] != 'lowest_rating_diagnostic' for v in variants)), 'ownership_or_transaction_verified': False})
            else:
                base.update({'video_id': r.get('videoId'), 'video_title_as_source': r.get('title'), 'video_url': r.get('pageUrl'), 'comment_type': r.get('type'), 'parent_id': r.get('replyToCid'), 'published_relative_as_source': r.get('publishedTimeText'), 'author_is_channel_owner': r.get('authorIsChannelOwner'), 'author_key': hashlib.sha256(str(r.get('author')).encode()).hexdigest()[:20], 'like_count': r.get('voteCount'), 'ownership_or_transaction_verified': False})
            rows.append(base)
        norm[platform] = rows
        jsonl(out / f'cleaned/{platform}.jsonl', rows)
        summary[platform] = {'source_rows': len(entries), 'unique_ids': len(rows), 'duplicate_excess_rows': len(entries) - len(rows), 'body_variant_conflicts': sum((c['platform'] == platform for c in conflicts)), 'retrieval_flag_counts': dict(collections.Counter((t for r in rows for t in r['retrieval_flags'])))}
    table(out / 'record_run_membership.csv', memberships)
    run_ids = collections.defaultdict(set)
    for m in memberships:
        if m['platform'] == 'x':
            run_ids[m['source_filename']].add(m['record_id'])
    overlaps = []
    for i, run_a in enumerate(sorted(run_ids)):
        for run_b in sorted(run_ids)[i + 1:]:
            aa, bb = (run_ids[run_a], run_ids[run_b])
            overlaps.append({'run_a': run_a, 'run_b': run_b, 'a_ids': len(aa), 'b_ids': len(bb), 'shared_post_ids': len(aa & bb), 'a_only_ids': len(aa - bb), 'b_only_ids': len(bb - aa)})
    table(out / 'x_run_overlap.csv', overlaps)
    table(out / 'body_variant_audit.csv', conflicts, ['platform', 'record_id', 'body_variants', 'source_files', 'resolution'])
    xs = norm.get('x', [])
    summary['x'].update({'unique_author_keys': len({r['author_key'] for r in xs}), 'replies': sum((r['is_reply'] for r in xs)), 'replies_missing_parent': sum((r['is_reply'] and (not r['parent_in_corpus']) for r in xs)), 'roots_missing': sum((not r['root_in_corpus'] for r in xs)), 'quotes': sum((r['is_quote'] for r in xs)), 'native_reposts': sum((r['is_repost'] for r in xs)), 'named_brand_account_posts': sum((r['named_brand_account'] for r in xs)), 'date_min': min((r['created_at_utc'] for r in xs)), 'date_max': max((r['created_at_utc'] for r in xs)), 'language_metadata_counts': dict(collections.Counter((r['language_metadata'] for r in xs)))})
    digiroom_posts = [r for r in xs if 'digiroom' in r['text_normalized'].lower()]
    summary['x'].update({'digiroom_matching_unique_posts': len(digiroom_posts), 'digiroom_case_insensitive_substring_occurrences': sum(r['text_normalized'].lower().count('digiroom') for r in digiroom_posts), 'digiroom_matching_author_accounts': dict(collections.Counter(r['author_username_private'] for r in digiroom_posts)), 'digiroom_check_definition': 'Unique post bodies containing case-insensitive substring digiroom; literal occurrence count is separate, includes repeated strings in a single post.'})
    branches = collections.defaultdict(list)
    for r in norm.get('maps', []):
        for cohort in r['cohorts']:
            branches[r['place_id'], cohort].append(r)
    bs = []
    for (pid, cohort), rs in sorted(branches.items()):
        stars = collections.Counter((str(r['stars']) for r in rs))
        bs.append({'place_id': pid, 'branch_title': rs[0]['branch_title_as_source'], 'city': rs[0]['city_as_source'], 'cohort': cohort, 'unique_reviews': len(rs), 'with_text': sum((r['has_text'] for r in rs)), 'stars_1': stars['1'], 'stars_2': stars['2'], 'stars_3': stars['3'], 'stars_4': stars['4'], 'stars_5': stars['5'], 'date_min': min((r['review_published_at'] for r in rs)), 'date_max': max((r['review_published_at'] for r in rs)), 'closed': any((r['permanently_closed'] for r in rs))})
    table(out / 'maps_branch_cohort_summary.csv', bs)
    summary['maps'].update({'places': len({r['place_id'] for r in norm['maps']}), 'with_text': sum((r['has_text'] for r in norm['maps'])), 'diagnostic_and_non_diagnostic_overlap_ids': sum((r['lowest_rating_diagnostic_member'] and r['has_non_diagnostic_membership'] for r in norm['maps'])), 'date_min': min((r['review_published_at'] for r in norm['maps'])), 'date_max': max((r['review_published_at'] for r in norm['maps']))})
    yt = collections.defaultdict(list)
    for r in norm.get('youtube', []):
        yt[r['video_id']].append(r)
    vs = [{'video_id': vid, 'title': rs[0]['video_title_as_source'], 'rows': len(rs), 'top_level': sum((r['comment_type'] == 'comment' for r in rs)), 'replies': sum((r['comment_type'] == 'reply' for r in rs)), 'channel_owner_rows': sum((bool(r['author_is_channel_owner']) for r in rs)), 'video_url': rs[0]['video_url']} for vid, rs in sorted(yt.items())]
    table(out / 'youtube_video_summary.csv', vs)
    summary['youtube']['videos'] = vs
    dump(out / 'corpus_metrics.json', summary)
    dump(out / 'codebook.json', {'normalization': 'HTML br converted to line breaks; HTML entities unescaped; horizontal whitespace normalized. Original text retained separately.', 'dedup_key': {'x': 'post ID', 'maps': 'reviewId', 'youtube': 'cid'}, 'variant_resolution': 'Longest text, then latest export filename; all variants retained in immutable originals and membership ledger.', 'patterns': PATTERNS, 'interpretation': 'All regex flags are candidate retrieval aids. They can overlap and have false positives. Counts are corpus composition, not validated incidents, sentiment, demand or population prevalence. First-person flag is not ownership verification. A named-brand flag is not a comprehensive business-account classifier.', 'maps_selection': 'Lowest-ranking diagnostic and newest selected cohorts are separate memberships, not mutually exclusive people. Publication date is not visit date. No inferred transaction date.', 'youtube_time': 'Relative publication strings remain relative; no invented exact dates.', 'engagement': 'Export-time counts are retained, not weighting or population exposure.', 'originals': 'Unmodified raw exports are preserved by the enclosing repository archival pipeline.'})
    print(json.dumps(summary, ensure_ascii=False, indent=2))
if __name__ == '__main__':
    main()
