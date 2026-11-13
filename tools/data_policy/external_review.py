"""Review of values from external (URL) sources (review of 2026-11-11; read-only on the data).

The coverage ledger marks a value 'external_selected' when its source is a URL registered in source_registry.json, and
some pending fields have an external technical document as their open question. Every such case has a reviewed
outcome in external_review_decisions.json:

  confirmed                         the value was re-read as printed on a copy that was obtained; property, unit,
                                    qualifier, conditions and page agree with the record
  inconclusive_source_unavailable   no copy could be obtained in the review: the value was not re-read

External evidence is admissible; there is no blanket rule for or against it. Each source is assessed separately:
  per evidence item   authority (who issued it), authenticity (how the copy is tied to the source), provenance
  per case            identity_status (exact product identity) and applicability
'confirmed' is not an approval to select a source: a distributor-issued document is never treated as
manufacturer-issued. identity_status concerns only the link between the source and the record: a source that names
the record's exact grade is 'exact_grade_named_merge_question_separate' when a separate question about merging two
records (ID-01) is open; that question is not resolved here and does not restrict the use of the source.

The tool checks that (1) every external_selected ledger row has a decision, (2) every decision still matches the record
(its 'expect' values), and (3) every stored evidence file still has its recorded SHA-256. It writes
reports/data_policy/external_review.csv and exits 1 if any check fails. It never changes product data.

Usage: python tools/data_policy/external_review.py [--out reports/data_policy/external_review.csv]
"""
import argparse, collections, csv, hashlib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402

DECISIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'external_review_decisions.json')
OUTCOMES = ('confirmed', 'inconclusive_source_unavailable')
KINDS = ('external_selected', 'pending_external_alternative')
AUTHORITY = ('manufacturer_issued', 'distributor_issued', 'third_party')
AUTHENTICITY = ('registry_hash_match', 'saved_copy_hash_verified', 'live_feed_unhashed_in_registry', 'not_obtained')
IDENTITY = ('exact_grade_named', 'exact_grade_named_merge_question_separate', 'not_assessed_source_not_obtained')


def field(prods, pid, prop):
    for d in prods[pid]['files'].values():
        if prop in (d.get('fields') or {}):
            return d['fields'][prop]
    return None


def matches(node, expect):
    if 'list_values' in expect:
        if not isinstance(node, list):
            return False
        return ([x.get('value') for x in node] == expect['list_values']
                and [x.get('test_temperature_c') for x in node] == expect['list_temperatures'])
    return isinstance(node, dict) and all(node.get(k) == v for k, v in expect.items())


def sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'external_review.csv'))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    with open(DECISIONS, encoding='utf-8') as fh:
        dec = json.load(fh)
    with open(os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'), encoding='utf-8') as fh:
        ledger = {(r['product'], r['property']): r for r in csv.DictReader(fh)}
    prods = P.load_products()
    errors = []

    ev_check = {}
    for key, e in dec['evidence'].items():
        if e.get('path'):
            p = os.path.join(P.ROOT, e['path'])
            if not os.path.exists(p):
                errors.append(f'evidence {key}: {e["path"]} missing'); ev_check[key] = 'missing'
            elif sha256(p) != e['sha256']:
                errors.append(f'evidence {key}: SHA-256 differs from the recorded value'); ev_check[key] = 'hash differs'
            else:
                ev_check[key] = 'stored copy, hash verified'
        elif e.get('registry_sha256_match'):
            ev_check[key] = 'not stored; bytes matched the registry SHA-256 at retrieval'
        else:
            ev_check[key] = 'no copy obtained'

    for key, e in dec['evidence'].items():
        if e.get('authority') not in AUTHORITY or e.get('authenticity') not in AUTHENTICITY or not e.get('provenance'):
            errors.append(f'evidence {key}: authority, authenticity and provenance must be assessed')
        if (e.get('authenticity') == 'not_obtained') != (ev_check[key] == 'no copy obtained'):
            errors.append(f'evidence {key}: authenticity {e.get("authenticity")!r} contradicts the copy state')
    cases = {(c['product'], c['property']): c for c in dec['cases']}
    if len(cases) != len(dec['cases']):
        errors.append('duplicate product x property in the decisions')
    external = {k for k, r in ledger.items() if r['selection_status'] == 'external_selected'}
    for k in sorted(external - {k for k, c in cases.items() if c['kind'] == 'external_selected'}):
        errors.append(f'{k[0]} {k[1]}: external_selected in the ledger but no external_selected decision')
    rows = []
    for (pid, prop), c in cases.items():
        r = ledger.get((pid, prop))
        if c['outcome'] not in OUTCOMES or c['kind'] not in KINDS:
            errors.append(f'{pid} {prop}: unknown outcome or kind')
        if r is None:
            errors.append(f'{pid} {prop}: not in the ledger'); continue
        want = 'external_selected' if c['kind'] == 'external_selected' else 'pending'
        if r['selection_status'] != want:
            errors.append(f'{pid} {prop}: ledger selection_status {r["selection_status"]!r}, decision expects {want!r}')
        unread = all(dec['evidence'][e]['authenticity'] == 'not_obtained' for e in c['evidence'])
        if c.get('identity_status') not in IDENTITY or not c.get('applicability'):
            errors.append(f'{pid} {prop}: identity_status and applicability must be assessed')
        elif unread != (c['identity_status'] == 'not_assessed_source_not_obtained'):
            errors.append(f'{pid} {prop}: identity_status {c["identity_status"]!r} contradicts whether the source was read')
        if unread != (c['outcome'] == 'inconclusive_source_unavailable'):
            errors.append(f'{pid} {prop}: outcome {c["outcome"]!r} contradicts whether the source was read')
        if not matches(field(prods, pid, prop), c['expect']):
            errors.append(f'{pid} {prop}: the record no longer matches the reviewed values {c["expect"]}')
        rows.append(dict(product=pid, property=prop, mandatory=r['mandatory'], kind=c['kind'], selection_status=r['selection_status'],
                         selected_file=r['selected_file'], outcome=c['outcome'],
                         evidence='; '.join(f'{e} ({ev_check.get(e, "unknown")})' for e in c['evidence']),
                         authority='; '.join(dict.fromkeys(dec['evidence'][e]['authority'] for e in c['evidence'])),
                         authenticity='; '.join(dict.fromkeys(dec['evidence'][e]['authenticity'] for e in c['evidence'])),
                         identity_status=c.get('identity_status', ''), identity=c['identity'], applicability=c.get('applicability', ''),
                         provenance=' | '.join(dec['evidence'][e]['provenance'] for e in c['evidence']),
                         printed=c['printed'], sds_comparison=c['sds'], change=c['change'], reason=c['reason']))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader(); w.writerows(rows)
    print(f'external-source cases: {len(rows)} (external_selected {sum(r["kind"] == "external_selected" for r in rows)}, '
          f'pending with an external alternative {sum(r["kind"] == "pending_external_alternative" for r in rows)})')
    for kind in KINDS:
        cnt = collections.Counter(r['outcome'] for r in rows if r['kind'] == kind)
        print(f'  {kind}: ' + ', '.join(f'{k} {v}' for k, v in sorted(cnt.items())))
    for col in ('authority', 'authenticity', 'identity_status'):
        print(f'  {col}: ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(r[col] for r in rows).items())))
    print('evidence: ' + ', '.join(f'{k} {v}' for k, v in ev_check.items()))
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
