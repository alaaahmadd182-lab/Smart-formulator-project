"""Build the mandatory Tier 1 eligibility outputs (Rule 3) from Products_json (read-only on the data).

Outputs (the only files written):
  reports/mandatory_properties/product_eligibility.csv        one row per product (interface for Workstream B)
  reports/mandatory_properties/missing_mandatory_properties.csv  one row per unmet requirement
  reports/mandatory_properties/missing_mandatory_properties.md   summary with counts

Usage:
  python tools/mandatory_properties/build_eligibility.py            write the three outputs
  python tools/mandatory_properties/build_eligibility.py --check    regenerate in memory, compare with the files, write nothing
Exit codes: 0 ok; 1 --check found a difference; 2 a product could not be classified.
Interface: docs/data_policy_mandatory_review/eligibility_interface.md
"""
import argparse, collections, csv, hashlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import requirements as R

ROOT = os.path.dirname(os.path.dirname(HERE))
PRODUCTS = os.path.join(ROOT, 'Products_json')
OUT = os.path.join(ROOT, 'reports', 'mandatory_properties')
COLUMNS = ['product_id', 'material_class', 'product_name', 'supplier', 'tier1_complete', 'formulation_eligible',
           'missing_mandatory_properties', 'eligibility_reasons', 'calculated_mandatory_properties',
           'requirements_version', 'source_snapshot_sha256']
CLASSES = ('base_oil', 'additive_package', 'additive_component')
COMPONENT_ROLE = {1: 'general', 2: 'vm', 3: 'ppd'}


def lp(p):
    p = os.path.abspath(p)
    return '\\\\?\\' + p if os.name == 'nt' and not p.startswith('\\\\?\\') else p


def product_paths(root=PRODUCTS):
    """All Products_json/**/*.json as project-relative POSIX paths, sorted (byte order of the UTF-8 path)."""
    out = []
    for d, _, fs in os.walk(lp(root)):
        for f in fs:
            if f.lower().endswith('.json'):
                full = os.path.join(d, f)
                rel = os.path.relpath(full.replace('\\\\?\\', ''), os.path.dirname(os.path.abspath(root)))
                out.append(rel.replace(os.sep, '/'))
    return sorted(out, key=lambda s: s.encode('utf-8'))


def snapshot_sha256(root=PRODUCTS):
    """SHA-256 of the UTF-8 manifest '<file sha256>  <relative path>\\n' over all product JSON files."""
    base = os.path.dirname(os.path.abspath(root))
    lines = []
    for rel in product_paths(root):
        with open(lp(os.path.join(base, rel)), 'rb') as fh:
            lines.append(f'{hashlib.sha256(fh.read()).hexdigest()}  {rel}\n')
    return hashlib.sha256(''.join(lines).encode('utf-8')).hexdigest()


def load_products(root=PRODUCTS):
    """{product_id: {'class', 'files': {tier-or-role: doc}, 'paths': [...]}}; product_id is the product folder name."""
    base = os.path.dirname(os.path.abspath(root))
    prods, problems = {}, []
    for rel in product_paths(root):
        with open(lp(os.path.join(base, rel)), encoding='utf-8') as fh:
            d = json.load(fh)
        cls = d.get('material_class')
        pid = rel.split('/')[-2]
        if cls not in CLASSES:
            problems.append(f'{rel}: material_class {cls!r}')
            continue
        p = prods.setdefault(pid, {'class': cls, 'files': {}, 'paths': []})
        if p['class'] != cls:
            problems.append(f'{rel}: material_class {cls} differs from {p["class"]} in the same product folder')
        key = COMPONENT_ROLE.get(d.get('tier')) if cls == 'additive_component' else d.get('tier')
        if key in p['files']:
            problems.append(f'{rel}: second file for tier/role {key}')
        p['files'][key] = d
        p['paths'].append(rel)
    return prods, problems


def evaluate(pid, p, snapshot):
    checks = R.CHECKERS[p['class']](p['files'])
    head = p['files'].get(1) or p['files'].get('general') or next(iter(p['files'].values()))
    prod = head.get('product') or {}
    missing = [rid for rid, ok, why, calc in checks if not ok]
    reasons = [why for rid, ok, why, calc in checks if not ok and why]
    notes = [f'{rid}: {why}' for rid, ok, why, calc in checks if ok and why]
    calculated = [rid for rid, ok, why, calc in checks if ok and calc]
    # an unresolved conflict on a satisfied requirement does not block, but is reported (the value is the selected one)
    open_props = set()
    for d in p['files'].values():
        for c in d.get('conflicts') or []:
            if isinstance(c, dict) and c.get('resolved') is not True:
                name = str(c.get('field') or c.get('property') or '')
                open_props.add(name.replace('[', '.').split('.')[-1].strip())
    for rid, ok, why, calc in checks:
        if ok and rid.split('.')[-1] in open_props:
            notes.append(f'{rid}: warning - an unresolved conflict is recorded for this property; the selected value is used '
                         'and the conflict stays open (see conflicts[])')
    complete = not missing
    if complete:
        reasons = [f'all mandatory Tier 1 requirements met under {R.REQUIREMENTS_VERSION} '
                   '(eligible under mandatory-data rules only; not a statement of chemical suitability or performance)']
    return dict(product_id=pid, material_class=p['class'], product_name=prod.get('product_name') or '',
                supplier=prod.get('supplier') or '', tier1_complete=complete, formulation_eligible=complete,
                missing_mandatory_properties=missing, eligibility_reasons=reasons + notes,
                calculated_mandatory_properties=calculated, requirements_version=R.REQUIREMENTS_VERSION,
                source_snapshot_sha256=snapshot), checks


def build(root=PRODUCTS):
    snapshot = snapshot_sha256(root)
    prods, problems = load_products(root)
    rows, detail = [], []
    for pid in sorted(prods):
        row, checks = evaluate(pid, prods[pid], snapshot)
        rows.append(row)
        for rid, ok, why, calc in checks:
            if not ok:
                detail.append(dict(product_id=pid, material_class=row['material_class'], product_name=row['product_name'],
                                   requirement=rid, reason=why, calculated_value_rejected=str(bool(calc)).lower()))
    return rows, detail, problems, snapshot


def _csv(rows, cols, encode):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({c: encode(r[c]) for c in cols})
    return buf.getvalue()


def _cell(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    return v


def render(rows, detail, snapshot):
    elig = _csv(rows, COLUMNS, _cell)
    miss = _csv(detail, ['product_id', 'material_class', 'product_name', 'requirement', 'reason', 'calculated_value_rejected'], lambda v: v)
    by_cls = collections.Counter(r['material_class'] for r in rows)
    ok_cls = collections.Counter(r['material_class'] for r in rows if r['formulation_eligible'])
    req = collections.Counter((d['material_class'], d['requirement']) for d in detail)
    nmiss = collections.Counter((r['material_class'], len(r['missing_mandatory_properties'])) for r in rows)
    md = ['# Missing mandatory (Tier 1) properties', '',
          f'Generated by `python tools/mandatory_properties/build_eligibility.py`. Requirements version '
          f'`{R.REQUIREMENTS_VERSION}`; source snapshot SHA-256 `{snapshot}`.', '',
          '"Eligible" means eligible under the mandatory-data rules only. It is not a statement of chemical suitability, '
          'compatibility or performance. Ineligible products stay in the database.', '',
          '## Eligibility by material class', '', '| Material class | Products | Eligible | Not eligible |', '|---|---:|---:|---:|']
    for c in R.CHECKERS:
        md.append(f'| {c} | {by_cls[c]} | {ok_cls[c]} | {by_cls[c] - ok_cls[c]} |')
    md.append(f'| **Total** | **{sum(by_cls.values())}** | **{sum(ok_cls.values())}** | **{sum(by_cls.values()) - sum(ok_cls.values())}** |')
    md += ['', '## Unmet requirements (products missing each)', '', '| Material class | Requirement | Products |', '|---|---|---:|']
    for (c, rid), n in sorted(req.items(), key=lambda x: (list(R.CHECKERS).index(x[0][0]), -x[1], x[0][1])):
        md.append(f'| {c} | `{rid}` | {n} |')
    md += ['', '## Number of unmet requirements per product', '', '| Material class | Unmet requirements | Products |', '|---|---:|---:|']
    for (c, n), k in sorted(nmiss.items(), key=lambda x: (list(R.CHECKERS).index(x[0][0]), x[0][1])):
        md.append(f'| {c} | {n} | {k} |')
    calc = [r for r in rows if r['calculated_mandatory_properties']]
    md += ['', '## Calculated values', '',
           f'{len(calc)} product(s) satisfy a requirement with a calculated value. '
           f'{sum(1 for d in detail if d["calculated_value_rejected"] == "true")} requirement(s) have a calculated value that was not accepted '
           '(see `calculated_value_rejected` in the CSV).', '',
           '## Interpretations used (need reviewer confirmation)', '']
    md += [f'- **{k}.** {t}' for k, t in R.INTERPRETATIONS]
    md += ['', 'Per-product detail: `missing_mandatory_properties.csv`; interface: `product_eligibility.csv`.', '']
    return {'product_eligibility.csv': elig, 'missing_mandatory_properties.csv': miss, 'missing_mandatory_properties.md': '\n'.join(md)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default=PRODUCTS)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--check', action='store_true', help='compare with existing outputs; write nothing')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    rows, detail, problems, snapshot = build(a.input)
    if problems:
        print('\n'.join(problems))
        return 2
    files = render(rows, detail, snapshot)
    if a.check:
        bad = []
        for name, text in files.items():
            p = os.path.join(a.out, name)
            if not os.path.exists(p) or open(p, encoding='utf-8', newline='').read() != text:
                bad.append(name)
        print('up to date' if not bad else 'differs: ' + ', '.join(bad))
        return 1 if bad else 0
    os.makedirs(a.out, exist_ok=True)
    for name, text in files.items():
        with open(os.path.join(a.out, name), 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    c = collections.Counter((r['material_class'], r['formulation_eligible']) for r in rows)
    print(f'products: {len(rows)}; snapshot {snapshot}')
    for cls in R.CHECKERS:
        print(f'  {cls}: eligible {c[(cls, True)]}, not eligible {c[(cls, False)]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
