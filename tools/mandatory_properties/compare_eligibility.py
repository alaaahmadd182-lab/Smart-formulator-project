"""Before/after comparison of the eligibility outputs (read-only on the data and on the production reports).

Compares a saved copy of product_eligibility.csv and requirement_outcomes.csv with the current files and reports every
difference: eligibility counts per class, each product whose tier1_complete / formulation_eligible / missing list
changed (with its reasons before and after), and each requirement outcome whose category changed. A change is never
suppressed and never required to be zero: the comparison explains it.

Usage:
  python tools/mandatory_properties/compare_eligibility.py \
      --before-eligibility docs/data_policy_mandatory_review/baselines/product_eligibility__before_policy_implementation_2026-11-11.csv \
      --before-outcomes    docs/data_policy_mandatory_review/baselines/requirement_outcomes__before_policy_implementation_2026-11-11.csv \
      [--out docs/data_policy_mandatory_review/baselines/eligibility_changes__policy_implementation_2026-11-11.csv]
Exit 0 always (it is a report, not a gate); exit 2 if a file is missing or the product sets differ.
"""
import argparse, collections, csv, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CUR = os.path.join(ROOT, 'reports', 'mandatory_properties')
BASE = os.path.join(ROOT, 'docs', 'data_policy_mandatory_review', 'baselines')
BOOLS = ('tier1_complete', 'formulation_eligible')


def read(p):
    with open(p, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def compare(be, bo, ae, ao):
    """(count rows, product changes, category changes) from before/after eligibility rows and outcome rows."""
    b, a = {r['product_id']: r for r in be}, {r['product_id']: r for r in ae}
    if set(a) != set(b):
        raise ValueError(f'product sets differ: only before {sorted(set(b) - set(a))[:5]}, only after {sorted(set(a) - set(b))[:5]}')
    counts = []
    for cls in sorted({r['material_class'] for r in ae}):
        for col in BOOLS:
            counts.append(dict(material_class=cls, field=col, products=sum(r['material_class'] == cls for r in ae),
                               before=sum(r['material_class'] == cls and r[col] == 'true' for r in be),
                               after=sum(r['material_class'] == cls and r[col] == 'true' for r in ae)))
    products = []
    for pid in sorted(a):
        x, y = b[pid], a[pid]
        ch = [c for c in BOOLS + ('missing_mandatory_properties',) if x[c] != y[c]]
        if ch:
            products.append(dict(product_id=pid, material_class=y['material_class'], changed='; '.join(ch),
                                 before=' | '.join(f'{c}={x[c]}' for c in ch), after=' | '.join(f'{c}={y[c]}' for c in ch),
                                 reasons_before=x['eligibility_reasons'], reasons_after=y['eligibility_reasons']))
    kb = {(r['product_id'], r['requirement']): r for r in bo}
    ka = {(r['product_id'], r['requirement']): r for r in ao}
    cats = []
    for k in sorted(set(kb) | set(ka)):
        x, y = kb.get(k), ka.get(k)
        cb, ca = (x or {}).get('category', '(no outcome)'), (y or {}).get('category', '(no outcome)')
        if cb != ca:
            cats.append(dict(product_id=k[0], requirement=k[1], blocking=(y or x)['blocking'], category_before=cb, category_after=ca,
                             reason_after=(y or {}).get('reason', '')))
    return counts, products, cats


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--before-eligibility', default=os.path.join(BASE, 'product_eligibility__before_policy_implementation_2026-11-11.csv'))
    ap.add_argument('--before-outcomes', default=os.path.join(BASE, 'requirement_outcomes__before_policy_implementation_2026-11-11.csv'))
    ap.add_argument('--out', default=os.path.join(BASE, 'eligibility_changes__policy_implementation_2026-11-11.csv'))
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        be, bo = read(a.before_eligibility), read(a.before_outcomes)
        ae, ao = read(os.path.join(CUR, 'product_eligibility.csv')), read(os.path.join(CUR, 'requirement_outcomes.csv'))
        counts, products, cats = compare(be, bo, ae, ao)
    except (OSError, ValueError) as e:
        print('STOP:', e)
        return 2
    print(f'requirements version: before {be[0]["requirements_version"]}, after {ae[0]["requirements_version"]}')
    print(f'data fingerprint: before {be[0]["source_snapshot_sha256"]}, after {ae[0]["source_snapshot_sha256"]}')
    print(f'interface columns identical: {list(be[0]) == list(ae[0])}')
    for c in counts:
        print(f'  {c["material_class"]:20s} {c["field"]:22s} before {c["before"]:3d}  after {c["after"]:3d}  of {c["products"]}')
    print(f'products whose eligibility fields or missing list changed: {len(products)}')
    for p in products:
        print(f'  {p["product_id"]}: {p["before"]}  ->  {p["after"]}')
    tr = collections.Counter((c['category_before'], c['category_after'], c['requirement'].split('[')[0]) for c in cats)
    print(f'requirement outcomes whose category changed: {len(cats)}')
    for (x, y, req), n in sorted(tr.items()):
        print(f'  {n:3d}  {req}: {x} -> {y}')
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['section', 'product_id', 'requirement_or_field', 'material_class_or_blocking', 'before', 'after', 'detail'])
        for c in counts:
            w.writerow(['count', '', c['field'], c['material_class'], c['before'], c['after'], f'of {c["products"]} products'])
        for p in products:
            w.writerow(['product', p['product_id'], p['changed'], p['material_class'], p['before'], p['after'], p['reasons_after']])
        for c in cats:
            w.writerow(['outcome_category', c['product_id'], c['requirement'], c['blocking'], c['category_before'], c['category_after'], c['reason_after']])
    return 0


if __name__ == '__main__':
    sys.exit(main())
