"""Audit literal query compliance in a local Actor export. No network or paid runs.

Usage: python3 verify_followup.py INPUT.json EXPORT.json [--out audit.csv]
Designed for the simple mandatory-phrase follow-up inputs, not arbitrary X syntax.
Semantic relevance and offline event truth still require contextual review.
"""
import argparse,csv,json,re,unicodedata
from collections import Counter
from datetime import datetime,timezone
from email.utils import parsedate_to_datetime

def norm(t):
    return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',str(t)).casefold()).strip()

def compile_query(q):
    if re.search(r'\bOR\b|[()]',q):
        raise ValueError('Boolean/grouped queries are not supported by this local literal checker.')
    phrases=re.findall(r'"([^"]+)"',q)
    if not phrases:raise ValueError('Expected mandatory quoted search phrases.')
    since=re.search(r'\bsince:(\d{4}-\d{2}-\d{2})',q)
    until=re.search(r'\buntil:(\d{4}-\d{2}-\d{2})',q)
    return dict(phrases=[norm(p) for p in phrases],exclude={x.casefold() for x in re.findall(r'-from:(\w+)',q)},since=datetime.fromisoformat(since[1]).replace(tzinfo=timezone.utc) if since else None,until=datetime.fromisoformat(until[1]).replace(tzinfo=timezone.utc) if until else None,no_reposts='-filter:nativeretweets' in q)

def date_of(r):
    value=r.get('createdAt','')
    try:return parsedate_to_datetime(value)
    except (ValueError,TypeError):
        try:return datetime.fromisoformat(value.replace('Z','+00:00'))
        except (ValueError,TypeError):return None

def body(r):
    return norm(re.sub(r'https?://\S+|@\w+',' ',r.get('text','')))

def literal_match(text,phrase):
    return re.search(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',text) is not None

def check(r,c):
    own=body(r); quoted=body(r.get('quoted_tweet') or {})
    own_match=all(literal_match(own,p) for p in c['phrases'])
    combined_match=all(literal_match(own+' '+quoted,p) for p in c['phrases'])
    author=str((r.get('author') or {}).get('username','')).casefold()
    if author in c['exclude']:return 'excluded_author'
    if c['no_reposts'] and r.get('isRetweet'):return 'native_repost'
    t=date_of(r)
    if (c['since'] or c['until']) and t is None:return 'date_missing'
    if t and ((c['since'] and t<c['since']) or (c['until'] and t>=c['until'])):return 'outside_date_window'
    return 'own_text_matches' if own_match else 'quoted_context_only' if combined_match else 'mandatory_phrase_missing'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input');p.add_argument('export');p.add_argument('--out',default='followup_compliance_audit.csv')
    a=p.parse_args()
    inp=json.load(open(a.input));data=json.load(open(a.export))
    if not isinstance(data,list):raise ValueError('Expected a JSON array of output rows.')
    queries=inp.get('searchTerms') or ([inp['twitterContent']] if inp.get('twitterContent') else [])
    if not queries:raise ValueError('This checker audits search inputs; direct tweet/reply lookup is a different collection mode.')
    configs=[compile_query(q) for q in queries]
    rows=[]
    for r in data:
        if not isinstance(r,dict) or not r.get('id') or not isinstance(r.get('text'),str):
            rows.append(dict(post_id='',status='non_post_record',compatible_requested_queries=''))
            continue
        statuses=[check(r,c) for c in configs]
        indices=[str(i+1) for i,s in enumerate(statuses) if s=='own_text_matches']
        status='own_text_matches' if indices else 'quoted_context_only' if 'quoted_context_only' in statuses else 'mandatory_phrase_missing' if 'mandatory_phrase_missing' in statuses else statuses[0]
        rows.append(dict(post_id=str(r['id']),status=status,compatible_requested_queries=';'.join(indices)))
    with open(a.out,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['post_id','status','compatible_requested_queries']);w.writeheader();w.writerows(rows)
    print(json.dumps(dict(rows=len(rows),status_counts=dict(Counter(r['status'] for r in rows)),output=a.out,caution='Compatible queries are inferred from text/date/author checks, not recovered source-query provenance. This is not semantic relevance, author verification, population coverage or offline outcome validation.'),indent=2))

if __name__=='__main__':main()
