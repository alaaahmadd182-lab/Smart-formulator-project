"""Progress measures with fixed definitions, kept separate for DOCUMENTS, LINKS and PROPOSALS (read-only; writes two tables).

Definitions (stable; applied to tables/progress_ledger.csv and tables/proposed_json_changes_NOT_APPLIED.csv):

LINKS (one ledger row = one product x document link)
  duplicate link        reviewed_categories starts with 'A' (byte duplicate of an archive file)
  coverage assessed     source_to_json_coverage starts with 'assessed by reading'
  coverage n/a          source_to_json_coverage starts with 'not applicable' (e.g. another product)
  coverage not assessed everything else
  content review open   field_verification_status starts with 'content review LIMITED', 'NOT ASSESSED', 'hit lines only',
                        'additive lines only', 'page 1 only' or 'no content comparison needed'

DOCUMENTS (unique SHA-256 over all ledger links) - reading scope only, independent of any product's coverage
  read in full          at least one link's field_verification_status states a page range 'pp.1-N' (N = the document's page count)
                        or '(only page)', or 'all N pages', or the document has 1 page and the status says 'in full' or 'whole'
  read in part          some documented reading exists but the rule above is not met
  no documented reading every link of the document is 'content review open' (see above)
  NOTE: a document read in full does NOT make every link to it 'coverage assessed'; each product link is judged separately.

PROPOSALS (rows of proposed_json_changes_NOT_APPLIED.csv)
  ready                 action_readiness starts with 'ready'   (ready for reviewer decision; NOT approved)
  provisional           everything else
"""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
OPEN = ('content review LIMITED', 'NOT ASSESSED', 'hit lines only', 'additive lines only', 'page 1 only', 'no content comparison needed')


def doc_scope(statuses, pages):
    import re
    if all(s.startswith(OPEN) for s in statuses):
        return 'no documented reading'
    try:
        n = int(pages)
    except ValueError:
        n = None
    for s in statuses:
        if '(only page)' in s:
            return 'read in full'
        if n and any(int(k) == n for k in re.findall(r'all (\d+) pages', s)):
            return 'read in full'
        if n == 1 and ('in full' in s or 'whole' in s):
            return 'read in full'
        if n and any(int(a) == 1 and int(b) == n for a, b in re.findall(r'pp\.(\d+)\s*-\s*(\d+)', s)):
            return 'read in full'
    return 'read in part'


def main():
    L = list(csv.DictReader(open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8')))
    P = list(csv.DictReader(open(os.path.join(BASE, 'tables', 'proposed_json_changes_NOT_APPLIED.csv'), encoding='utf-8')))
    cov = lambda r: ('assessed' if r['source_to_json_coverage'].startswith('assessed by reading') else
                     'n/a' if r['source_to_json_coverage'].startswith('not applicable') else 'not assessed')
    links = {}
    for kind, rows in (('duplicate', [r for r in L if r['reviewed_categories'].startswith('A')]),
                       ('non-duplicate', [r for r in L if not r['reviewed_categories'].startswith('A')])):
        links[kind] = dict(total=len(rows), coverage=dict(Counter(cov(r) for r in rows)),
                           content_review_open=sum(r['field_verification_status'].startswith(OPEN) for r in rows),
                           relationship_status=dict(Counter(r['relationship_status'] for r in rows)))
    bysha = {}
    for r in L:
        bysha.setdefault(r['sha256'], []).append(r)
    drows = []
    for sha, rs in bysha.items():
        drows.append(dict(sha256=sha, file=rs[0]['file'], pages=rs[0]['pages'], links=len(rs), read_scope=doc_scope([r['field_verification_status'] for r in rs], rs[0]['pages']),
                          links_coverage_assessed=sum(cov(r) == 'assessed' for r in rs), links_coverage_not_assessed=sum(cov(r) == 'not assessed' for r in rs),
                          products='; '.join(sorted({r['product_id'] for r in rs}))[:400]))
    with open(os.path.join(BASE, 'tables', 'document_read_scope.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(drows[0])); w.writeheader(); w.writerows(sorted(drows, key=lambda d: (d['read_scope'], d['file'])))
    docs = dict(total=len(drows), read_scope=dict(Counter(d['read_scope'] for d in drows)),
                read_in_full_but_some_links_not_assessed=sum(d['read_scope'] == 'read in full' and d['links_coverage_not_assessed'] > 0 for d in drows))
    props = dict(total=len(P), ready=sum(r['action_readiness'].startswith('ready') for r in P),
                 provisional=sum(not r['action_readiness'].startswith('ready') for r in P), approved=0,
                 by_action=dict(Counter(r['recommended_action'] for r in P)))
    out = dict(definitions=__doc__.strip(), documents=docs, links=links, proposals=props)
    json.dump(out, open(os.path.join(BASE, 'tables', 'progress_measures.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps(dict(documents=docs, links=links, proposals={k: v for k, v in props.items() if k != 'by_action'}), indent=1))


if __name__ == '__main__':
    main()
