"""Build the mandatory Tier 1 eligibility outputs (Rule 3) from Products_json (read-only on the data).

Inputs besides the product data:
  - reports/data_policy/source_coverage_ledger.csv (+ .meta.json): Rule 1 pending / unreviewed source selections. Its
    recorded product snapshot must equal the current one, otherwise the build stops (exit 3): rerun the ledger first.
  - tools/mandatory_properties/treat_rate_basis_evidence.json: reviewed page evidence of a mass basis for bare '%'.
  - the source archive (text of cited pages), to verify that calculation inputs are printed where the record says.

Outputs (the only files written):
  reports/mandatory_properties/product_eligibility.csv          one row per product (interface for Workstream B)
  reports/mandatory_properties/requirement_outcomes.csv         one row per product x requirement (all categories)
  reports/mandatory_properties/missing_mandatory_properties.csv one row per unmet requirement, with its category
  reports/mandatory_properties/missing_mandatory_properties.md  summary, categories and sensitivity

Usage:
  python tools/mandatory_properties/build_eligibility.py            write the outputs
  python tools/mandatory_properties/build_eligibility.py --check    regenerate in memory, compare with the files, write nothing
Exit codes: 0 ok; 1 --check found a difference; 2 a product could not be classified; 3 stale or missing ledger.
Interface: docs/data_policy_mandatory_review/eligibility_interface.md
"""
import argparse, collections, csv, hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import requirements as R

ROOT = os.path.dirname(os.path.dirname(HERE))
PRODUCTS = os.path.join(ROOT, 'Products_json')
OUT = os.path.join(ROOT, 'reports', 'mandatory_properties')
LEDGER = os.path.join(ROOT, 'reports', 'data_policy', 'source_coverage_ledger.csv')
BASIS = os.path.join(HERE, 'treat_rate_basis_evidence.json')
COLUMNS = ['product_id', 'material_class', 'product_name', 'supplier', 'tier1_complete', 'formulation_eligible',
           'missing_mandatory_properties', 'eligibility_reasons', 'calculated_mandatory_properties',
           'requirements_version', 'source_snapshot_sha256']
DETAIL_COLUMNS = ['product_id', 'material_class', 'product_name', 'requirement', 'category', 'blocking', 'representation',
                  'calculated', 'reason']
CLASSES = ('base_oil', 'additive_package', 'additive_component')
COMPONENT_ROLE = {1: 'general', 2: 'vm', 3: 'ppd'}
SELECTION_PENDING = ('pending', 'gap_tech_label_unreviewed')


class StaleInput(Exception):
    pass


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
    """SHA-256 of the UTF-8 manifest '<file sha256>  <relative path>\\n' over the exact bytes of all product JSON files."""
    base = os.path.dirname(os.path.abspath(root))
    lines = []
    for rel in product_paths(root):
        with open(lp(os.path.join(base, rel)), 'rb') as fh:
            lines.append(f'{hashlib.sha256(fh.read()).hexdigest()}  {rel}\n')
    return hashlib.sha256(''.join(lines).encode('utf-8')).hexdigest()


def snapshot_sha256_lf(root=PRODUCTS):
    """INFORMATIONAL ONLY (never the interface value): the same manifest over the bytes with CRLF written as LF, which is
    how the files are committed. Lets checkouts with different line-ending conversion compare their data."""
    base = os.path.dirname(os.path.abspath(root))
    lines = []
    for rel in product_paths(root):
        with open(lp(os.path.join(base, rel)), 'rb') as fh:
            lines.append(f'{hashlib.sha256(fh.read().replace(bytes([13, 10]), bytes([10]))).hexdigest()}  {rel}\n')
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


def load_pending(snapshot, ledger=LEDGER):
    """{(product, property): reason} for mandatory properties whose Rule 1 selection is pending or unreviewed."""
    meta = ledger.replace('.csv', '.meta.json')
    if not (os.path.exists(ledger) and os.path.exists(meta)):
        raise StaleInput(f'{ledger} or its .meta.json is missing: run python tools/data_policy/source_coverage_ledger.py')
    with open(meta, encoding='utf-8') as fh:
        m = json.load(fh)
    if m.get('source_snapshot_sha256') != snapshot:
        raise StaleInput(f'the coverage ledger was built from snapshot {m.get("source_snapshot_sha256")}, the data is {snapshot}: '
                         'rerun python tools/data_policy/source_coverage_ledger.py')
    out = {}
    with open(ledger, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if r['mandatory'] == 'true' and r['selection_status'] in SELECTION_PENDING:
                out[(r['product'], r['property'])] = f'{r["selection_status"]}: {r["selection_reason"]}'
    return out


class PageText:
    """Cited page text from the source archive (opened lazily; None when unavailable)."""

    def __init__(self):
        self._ar = None

    def __call__(self, f, page):
        if not f or str(f).lower().startswith(('http://', 'https://')):
            return None
        if self._ar is None:
            sys.path.insert(0, os.path.join(ROOT, 'tools', 'data_policy'))
            import policy_lib
            self._ar = policy_lib.Archive()
        pages = self._ar.pages(f)
        n = re.findall(r'\d+', str(page))
        if not pages or not n or not 1 <= int(n[0]) <= len(pages):
            return None
        return pages[int(n[0]) - 1] or None


def evaluate(pid, p, snapshot, pending, basis, page_text):
    ctx = R.Context(page_text=page_text, pending=pending, basis_evidence=basis, product=pid)
    outs = R.CHECKERS[p['class']](p['files'], ctx)
    head = p['files'].get(1) or p['files'].get('general') or next(iter(p['files'].values()))
    prod = head.get('product') or {}
    complete, eligible = R.summarize(outs)
    blocking_unmet = [o for o in outs if o.blocking and o.category not in R.SATISFIED]
    reasons = [f'{o.requirement} [{o.category}]: {o.reason}' for o in blocking_unmet]
    notes = [f'{o.requirement} [{o.category}]: {o.reason}' for o in outs if o.blocking and o.category in R.SATISFIED and o.reason]
    notes += [f'{o.requirement} [{o.category}, non-blocking subtype block]: {o.reason}' for o in outs
              if not o.blocking and o.category not in R.SATISFIED]
    open_props = set()
    for d in p['files'].values():
        for c in d.get('conflicts') or []:
            if isinstance(c, dict) and c.get('resolved') is not True:
                open_props.add(str(c.get('field') or c.get('property') or '').replace('[', '.').split('.')[-1].strip())
    notes += [f'{o.requirement}: warning - an unresolved conflict is recorded for this property; the selected value is used '
              'and the conflict stays open (see conflicts[])' for o in outs
              if o.category in R.SATISFIED and o.requirement.split('.')[-1] in open_props]
    if eligible:
        reasons = [f'all blocking mandatory Tier 1 requirements met under {R.REQUIREMENTS_VERSION} '
                   '(eligible under mandatory-data rules only; not a statement of chemical suitability or performance)']
    row = dict(product_id=pid, material_class=p['class'], product_name=prod.get('product_name') or '',
               supplier=prod.get('supplier') or '', tier1_complete=complete, formulation_eligible=eligible,
               missing_mandatory_properties=[o.requirement for o in blocking_unmet], eligibility_reasons=reasons + notes,
               calculated_mandatory_properties=[o.requirement for o in outs if o.blocking and o.category in R.SATISFIED and o.calculated],
               requirements_version=R.REQUIREMENTS_VERSION, source_snapshot_sha256=snapshot)
    return row, outs


def build(root=PRODUCTS, ledger=LEDGER, page_text=None):
    snapshot = snapshot_sha256(root)
    prods, problems = load_products(root)
    pending = load_pending(snapshot, ledger)
    with open(BASIS, encoding='utf-8') as fh:
        basis = json.load(fh)['evidence']
    page_text = page_text or PageText()
    rows, outcomes = [], []
    for pid in sorted(prods):
        row, outs = evaluate(pid, prods[pid], snapshot, pending, basis, page_text)
        rows.append(row)
        for o in outs:
            outcomes.append(dict(product_id=pid, material_class=row['material_class'], product_name=row['product_name'],
                                 requirement=o.requirement, category=o.category, blocking=o.blocking,
                                 representation=o.representation or '', calculated=o.calculated, reason=o.reason))
    return rows, outcomes, problems, snapshot


def _csv(rows, cols):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({c: _cell(r[c]) for c in cols})
    return buf.getvalue()


def _cell(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, list):
        return json.dumps(v, ensure_ascii=False)
    return v


def _eligible_if(rows, outcomes, also):
    """Products that would be eligible if blocking outcomes in the categories `also` were satisfied (sensitivity only)."""
    by = collections.defaultdict(list)
    for o in outcomes:
        if o['blocking']:
            by[o['product_id']].append(o['category'])
    return sum(1 for r in rows if all(c in R.SATISFIED or c in also for c in by[r['product_id']]))


def render(rows, outcomes, snapshot):
    unmet = [o for o in outcomes if o['category'] not in R.SATISFIED]
    files = {'product_eligibility.csv': _csv(rows, COLUMNS),
             'requirement_outcomes.csv': _csv(outcomes, DETAIL_COLUMNS),
             'missing_mandatory_properties.csv': _csv(unmet, DETAIL_COLUMNS)}
    cls_order = list(R.CHECKERS)
    n = collections.Counter(r['material_class'] for r in rows)
    comp = collections.Counter(r['material_class'] for r in rows if r['tier1_complete'])
    elig = collections.Counter(r['material_class'] for r in rows if r['formulation_eligible'])
    md = ['# Mandatory (Tier 1) requirements: outcomes by product', '',
          f'Generated by `python tools/mandatory_properties/build_eligibility.py`. Requirements version `{R.REQUIREMENTS_VERSION}`; '
          f'source snapshot SHA-256 `{snapshot}` (exact bytes of this checkout; the interface value). Informational '
          f'LF-normalised fingerprint, for comparing checkouts with different line-ending conversion: `{snapshot_sha256_lf()}`.', '',
          '"Formulation-eligible" means every blocking mandatory requirement is met under the mandatory-data rules. It is not a '
          'statement of chemical suitability, compatibility or performance. "Tier 1 complete" means every blocking requirement '
          'has documented information, including ranges or bounds still awaiting a use-specific decision and values whose '
          'source selection is pending. Products that are not eligible stay in the database.', '',
          'An unmet requirement is not necessarily an absent property: see the category of each row.', '',
          '## Products by material class', '',
          '| Material class | Products | Tier 1 complete | Formulation-eligible |', '|---|---:|---:|---:|']
    for c in cls_order:
        md.append(f'| {c} | {n[c]} | {comp[c]} | {elig[c]} |')
    md.append(f'| **Total** | **{sum(n.values())}** | **{sum(comp.values())}** | **{sum(elig.values())}** |')
    md += ['', '## Blocking requirement outcomes by category', '', '| Material class | Requirement | ' +
           ' | '.join(c for c in R.CATEGORIES) + ' |', '|---|---|' + '---:|' * len(R.CATEGORIES)]
    tab = collections.defaultdict(collections.Counter)
    for o in outcomes:
        if o['blocking']:
            tab[(o['material_class'], o['requirement'])][o['category']] += 1
    for (c, rid), cnt in sorted(tab.items(), key=lambda x: (cls_order.index(x[0][0]), x[0][1])):
        md.append(f'| {c} | `{rid}` | ' + ' | '.join(str(cnt[k] or '') for k in R.CATEGORIES) + ' |')
    nb = [o for o in outcomes if not o['blocking']]
    md += ['', '## Non-blocking subtype blocks (VM / PPD, stored in tier 2 / tier 3 files)', '',
           f'{len(nb)} subtype requirement outcomes for {len({o["product_id"] for o in nb})} product(s); '
           f'{sum(1 for o in nb if o["category"] in R.SATISFIED)} met. They do not affect eligibility (decision C, '
           'requirements_review.md).', '',
           '## Sensitivity (information only; no rule changed)', '',
           '| If these blocking categories were also accepted | Eligible products |', '|---|---:|',
           f'| none (current rules) | {sum(elig.values())} |',
           f'| bound_or_range_needs_assessment | {_eligible_if(rows, outcomes, {R.BOUND})} |',
           f'| unresolved_source_selection | {_eligible_if(rows, outcomes, {R.SEL})} |',
           f'| both | {_eligible_if(rows, outcomes, {R.BOUND, R.SEL})} |', '',
           '## Calculated values', '',
           f'{sum(1 for o in outcomes if o["calculated"] and o["category"] in R.SATISFIED)} requirement outcome(s) are met by a '
           f'calculated value; {sum(1 for o in outcomes if o["calculated"] and o["category"] not in R.SATISFIED)} calculated value(s) '
           'were not accepted (category invalid_or_unreproducible_calculation, or a missing condition).', '',
           '## Interpretations used (provisional; need reviewer confirmation)', '']
    md += [f'- **{k}.** {t}' for k, t in R.INTERPRETATIONS]
    md += ['', 'Detail: `requirement_outcomes.csv` (every requirement), `missing_mandatory_properties.csv` (unmet only); '
           'interface: `product_eligibility.csv`; authority of each requirement: '
           '`docs/data_policy_mandatory_review/requirements_review.md`.', '']
    files['missing_mandatory_properties.md'] = '\n'.join(md)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default=PRODUCTS)
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--check', action='store_true', help='compare with existing outputs; write nothing')
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        rows, outcomes, problems, snapshot = build(a.input)
    except StaleInput as e:
        print(f'STOP: {e}')
        return 3
    if problems:
        print('\n'.join(problems))
        return 2
    files = render(rows, outcomes, snapshot)
    if a.check:
        bad = []
        for name, text in files.items():
            p = os.path.join(a.out, name)
            if not os.path.exists(p):
                bad.append(name)
                continue
            with open(p, encoding='utf-8', newline='') as fh:
                if fh.read() != text:
                    bad.append(name)
        print('up to date' if not bad else 'differs: ' + ', '.join(bad))
        return 1 if bad else 0
    os.makedirs(a.out, exist_ok=True)
    for name, text in files.items():
        with open(os.path.join(a.out, name), 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    c = collections.Counter((r['material_class'], r['tier1_complete'], r['formulation_eligible']) for r in rows)
    print(f'products: {len(rows)}; snapshot {snapshot}')
    for cls in R.CHECKERS:
        print(f'  {cls}: tier1_complete {sum(v for k, v in c.items() if k[0] == cls and k[1])}, '
              f'eligible {sum(v for k, v in c.items() if k[0] == cls and k[2])}, of {sum(v for k, v in c.items() if k[0] == cls)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
