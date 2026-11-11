"""Review of the outstanding source leads (read-only on the product data).

Cases come from the source coverage ledger (reports/data_policy/source_coverage_ledger.csv), deduplicated by
product x property:
  mand_lead   mandatory property Missing; an associated document mentions it          (missing_label_found, mandatory)
  mand_img    mandatory property Missing; an associated document has no text layer     (missing_not_searchable, mandatory)
  lead        non-mandatory property Missing; an associated document mentions it
  img         non-mandatory property Missing; an associated document has no text layer
  cmp_gap     a technical page and an SDS page both mention the property; no TDS-SDS comparison recorded
A case can belong to several lists; it is reviewed once.

For every case and associated page the tool extracts the property line and the lines that follow it (the text layer
of a single-product sheet usually prints the value there). A keyword mention is only a lead. The reviewer's decisions
are recorded in lead_review_decisions.json: each rule names the documents read (and how: text layer or render), the
identity finding, what is printed, the outcome and the resulting change. Outcomes:
  usable_evidence        a product-specific printed value that satisfies the field's conditions (change applied
                         through source_selection.CHANGES, or a reviewed TDS-SDS comparison added to the inventory)
  already_recorded       the printed value is the one already in the record (comparison gap: the SDS value is recorded
                         as a reviewed comparison)
  unrelated_mention      the label belongs to another grade, table, quantity or boilerplate
  insufficient_evidence  the cell is "Report", "-", "N/A", or the value lacks a condition the property requires
  unavailable_source     the document cannot be read for this property (no text layer and no render read)
  unresolved_identity    the document's applicability to this product is not established
A case without a matching decision is reported as 'not_reviewed'.

Usage: python tools/data_policy/lead_review.py [--out reports/data_policy/lead_review.csv]
Writes --out and prints the counts. Exit 0.
"""
import argparse, collections, csv, io, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402
import source_coverage_ledger as L  # noqa: E402

DECISIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lead_review_decisions.json')
OUTCOMES = ['usable_evidence', 'already_recorded', 'unrelated_mention', 'insufficient_evidence', 'unavailable_source',
            'unresolved_identity', 'not_reviewed']
DOC_RX = re.compile(r'([^;|]+?\.(?:pdf|PDF|jpg|jpeg|jfif))(?: p\.(\d+))?')


def cases(ledger):
    out = collections.OrderedDict()
    for r in ledger:
        lists = []
        m = r['mandatory'] == 'true'
        if r['selection_status'] == 'missing_label_found':
            lists.append('mand_lead' if m else 'lead')
        if r['selection_status'] == 'missing_not_searchable':
            lists.append('mand_img' if m else 'img')
        if r['comparison_status'].startswith('gap'):
            lists.append('cmp_gap')
        if lists:
            out[(r['product'], r['property'])] = dict(r, lists=lists)
    return out


def docs_of(c):
    found = []
    for col in ('technical_pages_with_label', 'sds_pages_with_label', 'unsearchable_documents'):
        for f, pg in DOC_RX.findall(c[col]):
            f = f.strip()
            if (f, pg) not in found:
                found.append((f, pg))
    return found


def snippet(ar, f, pg, prop, n=6):
    pages = ar.pages(f)
    if not pages or not pg:
        return ''
    t = pages[int(pg) - 1]
    lines = [x.strip() for x in t.splitlines() if x.strip()]
    out = []
    for i, ln in enumerate(lines):
        if re.search(L.LABELS[prop], ln, re.I):
            out.append(' / '.join(lines[i:i + n]))
    return ' || '.join(out[:3])[:600]


def matches(rule, c, docs, comps=frozenset()):
    m = rule['match']
    if rule.get('requires_comparison') and (c['product'], c['property']) not in comps:
        return False
    if rule.get('exclude_if_comparison') and (c['product'], c['property']) in comps:
        return False
    if 'product' in m and not any(re.fullmatch(p, c['product']) for p in m['product']):
        return False
    if 'property' in m and c['property'] not in m['property']:
        return False
    if 'lists' in m and not set(m['lists']) & set(c['lists']):
        return False
    if 'documents' in m and not {f for f, _ in docs} & set(m['documents']):
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'lead_review.csv'))
    ap.add_argument('--baseline-ref', default='4e83652', help='commit whose ledger defines the reviewed case universe')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'), encoding='utf-8') as fh:
        ledger = list(csv.DictReader(fh))
    # the case universe is frozen at the revision-2 ledger, so that a case resolved by a later correction is reported
    # with its outcome instead of disappearing; cases that appear only in the current ledger are added
    base = subprocess.run(['git', 'show', f'{a.baseline_ref}:reports/data_policy/source_coverage_ledger.csv'], cwd=P.ROOT,
                          capture_output=True, text=True, encoding='utf-8')
    if base.returncode != 0:
        raise SystemExit(f'cannot read the revision-2 ledger at {a.baseline_ref}')
    base_cases = cases(list(csv.DictReader(io.StringIO(base.stdout))))
    cur_cases = cases(ledger)
    cur_by_key = {(r['product'], r['property']): r for r in ledger}
    with open(DECISIONS, encoding='utf-8') as fh:
        dec = json.load(fh)
    rules = dec['rules']
    comps = frozenset((x['product'], x['property']) for x in dec.get('comparisons', []))
    for i, r in enumerate(rules):
        assert r['outcome'] in OUTCOMES[:-1], (i, r['outcome'])
    ar = P.Archive()
    rows, used = [], collections.Counter()
    universe = collections.OrderedDict(base_cases)
    for k, v in cur_cases.items():
        universe.setdefault(k, v)
    # cases found during the review and resolved before this run (recorded so they are not lost when resolved)
    for x in dec.get('added_cases', []):
        k = (x['product'], x['property'])
        if k not in universe and k in cur_by_key:
            universe[k] = dict(cur_by_key[k], lists=list(x['lists']))
    for (pid, prop), c0 in universe.items():
        cur = cur_by_key.get((pid, prop), c0)
        c = dict(cur, lists=c0['lists'] + [x for x in cur_cases.get((pid, prop), {}).get('lists', []) if x not in c0['lists']])
        c['still_open'] = (pid, prop) in cur_cases
        docs = docs_of(dict(c0, **{k: c0[k] + ';' + cur.get(k, '') for k in ('technical_pages_with_label', 'sds_pages_with_label', 'unsearchable_documents')}))
        rule = next((r for r in rules if matches(r, c, docs, comps)), None)
        if rule:
            used[rules.index(rule)] += 1
        rows.append(dict(
            product=pid, property=prop, mandatory=c['mandatory'], lists=';'.join(c['lists']),
            in_current_ledger=str(c['still_open']).lower(), record_status=c['status'],
            selected_source=f"{c['selected_file']} p.{c['selected_page']}" if c['selected_file'] else '',
            documents='; '.join(f'{f} p.{p}' if p else f'{f} (no text layer)' for f, p in docs),
            extract=' || '.join(filter(None, (f'{f} p.{p}: ' + snippet(ar, f, p, prop) for f, p in docs if p)))[:1500],
            outcome=rule['outcome'] if rule else 'not_reviewed',
            identity=rule.get('identity', '') if rule else '',
            printed=((rule.get('printed', {}).get(pid) or rule.get('printed', {}).get('*', '')) if not rule.get('requires_comparison') else
                     '; '.join(f"{x['sds']['file']} p.{x['sds']['page']}: {x['sds']['printed_text']}" for x in dec['comparisons']
                               if (x['product'], x['property']) == (pid, prop))) if rule else '',
            change=rule.get('change', '') if rule else '',
            reason=rule['reason'] if rule else 'no recorded decision',
            read_how=rule.get('read', '') if rule else '',
            rule=rules.index(rule) if rule else ''))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'cases (deduplicated product x property): {len(rows)}')
    for lst in ('mand_lead', 'mand_img', 'lead', 'img', 'cmp_gap'):
        sub = [r for r in rows if lst in r['lists'].split(';')]
        print(f'  {lst}: {len(sub)}  ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['outcome'] for r in sub).most_common()))
    print('outcomes: ' + ', '.join(f'{k} {v}' for k, v in collections.Counter(r['outcome'] for r in rows).most_common()))
    unused = [i for i in range(len(rules)) if not used[i]]
    if unused:
        print(f'decision rules matching no case: {unused}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
