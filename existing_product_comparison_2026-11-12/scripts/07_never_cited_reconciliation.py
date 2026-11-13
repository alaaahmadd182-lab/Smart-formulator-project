"""Reconcile the 33 never-cited duplicate links outstanding after the twelfth pass (frozen in
scripts/never_cited_baseline_twelfth_pass.json, key = product_id + sha256) against the current ledger.

Writes tables/never_cited_reconciliation.csv. Status per link:
  reviewed                                - category A kept; source-to-JSON coverage 'assessed by reading'
  reclassified, coverage assessed        - category changed; coverage assessed by reading
  reclassified, coverage NOT assessed    - category changed only (reclassification is not coverage)
  outstanding                            - coverage not assessed
  missing from ledger                    - key no longer present (must be explained)
Read-only on everything except its own output table.
"""
import csv, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)


def main():
    base = json.load(open(os.path.join(HERE, 'never_cited_baseline_twelfth_pass.json'), encoding='utf-8'))
    ledger = list(csv.DictReader(open(os.path.join(BASE, 'tables', 'progress_ledger.csv'), encoding='utf-8')))
    now = {(r['product_id'], r['sha256']): r for r in ledger}
    rows = []
    for b in base['links']:
        r = now.get((b['product_id'], b['sha256']))
        if r is None:
            st, cat, cov, batch = 'missing from ledger', '', '', ''
        else:
            cat, cov, batch = r['reviewed_categories'], r['source_to_json_coverage'], r['batch']
            assessed = cov.startswith('assessed by reading')
            if cat == b['category_at_twelfth']:
                st = 'reviewed' if assessed else 'outstanding'
            else:
                st = 'reclassified, coverage assessed' if assessed else 'reclassified, coverage NOT assessed'
        rows.append(dict(product_id=b['product_id'], file=b['file'], sha256=b['sha256'], category_at_twelfth=b['category_at_twelfth'], category_now=cat,
                         inventory_label_present=b['inventory_label_present'], status=st, batch_now=batch, coverage_now=cov[:300]))
    out = os.path.join(BASE, 'tables', 'never_cited_reconciliation.csv')
    with open(out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    from collections import Counter
    c = Counter(r['status'] for r in rows)
    print(f"baseline {len(rows)} (of {base['counts']['never_cited_total']} never-cited; {base['counts']['assessed_at_twelfth']} assessed by the twelfth pass):", dict(c))
    for r in rows:
        if r['status'] != 'reviewed':
            print('  ', r['status'], '|', r['product_id'], '|', r['file'])


if __name__ == '__main__':
    main()
