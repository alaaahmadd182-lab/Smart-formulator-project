"""Automated source check of every archive value in the audit findings (read-only).

For each value of each finding that cites an archive document (or a saved evidence PDF) with a page number, the
script looks for the value as a separate number on the cited page's text layer. It records one of:

  on cited page        the number is printed on the cited page
  on other page(s)     not on the cited page, but on the listed page(s) of the same document (a page-reference issue)
  not found            not on any page of the document's text layer (needs reading; often a derived or quoted value)
  no text layer        image file or PDF page without text: the value can only be checked visually
  no page cited        the citation has no page number; the whole document is searched
  not an archive file  an external URL or a file outside the archive/evidence folder

The number check proves only that the number is printed on the page, not that it sits in the right column or row;
column-level checks are separate (check_columns.py) and visual checks are recorded in the source-reading log.

Usage:
    python tools/audit/review_2026-11-02/check_sources.py [--findings PATH] [--out CSV]
Exit codes: 0 every result is either confirmed or listed in EXPECTED with its reason; 1 an unexpected result.
"""
import argparse, collections, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import review_lib as R

# Results that are not "on cited page" and were explained by reading the source (see source_reading_log.csv).
# key: (finding id, value index) -> reason
EXPECTED = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--findings', default=R.SNAPSHOT_FINDINGS)
    ap.add_argument('--out')
    ap.add_argument('--expected', default=os.path.join(R.HERE, 'expected_source_results.json'))
    a = ap.parse_args()
    F = json.load(open(a.findings, encoding='utf-8'))
    exp = json.load(open(a.expected, encoding='utf-8')) if os.path.exists(a.expected) else {}
    ar = R.Archive()
    rows, C = [], collections.Counter()
    for f in F:
        for i, v in enumerate(f['values']):
            files = [x.strip() for x in str(v.get('file') or '').split(';') if x.strip()]
            if not files:
                continue
            page = v.get('page')
            pages_cited = [int(p) for p in re.findall(r'\d+', str(page))] if page not in (None, '') else []
            val = v.get('value')
            nums = [x for x in re.findall(r'[<>≥≤≮]?-?\d+(?:[.,]\d+)?', str(val))] if val is not None else []
            for fn in files:
                texts = ar.pages(fn)
                if texts is None:
                    res, where = 'not an archive file', ''
                elif not texts or not any(t.strip() for t in texts):
                    res, where = 'no text layer', ''
                elif not nums:
                    res, where = 'no numeric value', ''
                else:
                    found_cited = all(any(R.on_page(n, texts[p - 1]) for p in pages_cited if 1 <= p <= len(texts)) for n in nums) if pages_cited else False
                    other = sorted({p + 1 for p, t in enumerate(texts) for n in nums if R.on_page(n, t)})
                    if pages_cited and any(p > len(texts) for p in pages_cited):
                        res, where = 'cited page beyond document', f'{len(texts)} pages'
                    elif pages_cited and found_cited:
                        res, where = 'on cited page', ','.join(map(str, pages_cited))
                    elif pages_cited and any(not texts[p - 1].strip() for p in pages_cited):
                        res, where = 'no text layer', 'cited page has no text'
                    elif other:
                        res, where = ('no page cited' if not pages_cited else 'on other page(s)'), ','.join(map(str, other))
                    else:
                        res, where = 'not found', ''
                key = f"{f['id']}#{i}#{fn}"
                ok = res in ('on cited page', 'not an archive file', 'no numeric value') or key in exp
                C[res] += 1
                rows.append(dict(id=f['id'], value_index=i, file=fn, page=page, value=val, result=res, where=where,
                                 expected_reason=(exp[key].get('note', '') if isinstance(exp.get(key), dict) else exp.get(key, '')), status='ok' if ok else 'UNEXPECTED'))
    if a.out:
        with open(a.out, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    print('archive/evidence value citations:', len(rows), dict(C))
    bad = [r for r in rows if r['status'] != 'ok']
    for r in bad:
        print('UNEXPECTED', r['id'], r['value_index'], r['file'], 'p.', r['page'], repr(r['value'])[:60], '->', r['result'], r['where'])
    print('OVERALL:', 'PASS' if not bad else f'{len(bad)} unexpected results')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
