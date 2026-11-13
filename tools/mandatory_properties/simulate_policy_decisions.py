"""READ-ONLY SIMULATION for the implementation plan of the four policy decisions approved on 2026-11-11.

This script changes nothing: it reads the product records and the generated reports and prints counts. It is NOT the
eligibility build, and its numbers are NOT eligibility results. tier1_complete and formulation_eligible keep their
current definition (requirements version mandatory-tier1-2026-11-10.3); the candidate fields below exist only here.

Usage: python tools/mandatory_properties/simulate_policy_decisions.py [--out FILE]   (FILE: a text copy of the output)
"""
import argparse, collections, csv, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [HERE, os.path.join(ROOT, 'tools', 'data_policy')]
import policy_lib as P  # noqa: E402
import requirements as R  # noqa: E402

NUMERIC_BASE = ('kv40', 'kv100', 'viscosity_index', 'density', 'ccs')
MASS = re.compile(r'wt|mass|weight|m/m|w/w', re.I)
VOL = re.compile(r'vol|v/v', re.I)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out')
    a = ap.parse_args(argv)
    buf = io.StringIO()

    def say(*x):
        print(*x, file=buf)

    out = [r for r in read('reports/mandatory_properties/requirement_outcomes.csv') if r['blocking'] == 'true']
    elig = {r['product_id']: r for r in read('reports/mandatory_properties/product_eligibility.csv')}
    by = collections.defaultdict(list)
    for r in out:
        by[r['product_id']].append(r)
    cls = {p: rs[0]['material_class'] for p, rs in by.items()}
    say('SIMULATION ONLY - not eligibility results. Requirements version in force:', R.REQUIREMENTS_VERSION)
    say('Data fingerprint of the reports read:', next(iter(elig.values()))['source_snapshot_sha256'])
    say()

    # ------------------------------------------------------------------ decision 1: ranges and bounds
    say('== Decision 1: ranges and bounds ==')
    say('Current (unchanged) result: tier1_complete = formulation_eligible =',
        dict(collections.Counter(cls[p] for p, r in elig.items() if r['tier1_complete'] == 'true')))
    bnd = [r for r in out if r['category'] == R.BOUND]
    say('Blocking outcomes in category bound_or_range_needs_assessment:', len(bnd), 'in', len({r['product_id'] for r in bnd}), 'products')
    say('  by requirement and representation:')
    for (req, rep), n in sorted(collections.Counter((r['requirement'], r['representation']) for r in bnd).items()):
        say(f'    {req:18s} {rep:12s} {n}')

    def count(ok_cats, label, extra=lambda rs: True):
        c = collections.Counter(cls[p] for p, rs in by.items() if all(r['category'] in ok_cats for r in rs) and extra(rs))
        say(f'  {label}: base_oil {c["base_oil"]}, additive_package {c["additive_package"]}, additive_component {c["additive_component"]}')
        return {p for p, rs in by.items() if all(r['category'] in ok_cats for r in rs) and extra(rs)}
    sat = {R.MET, R.NOT_APPLICABLE}
    say('Candidate fields (definitions in the plan):')
    a0 = count(sat, 'point_calculation_ready            (every requirement met with an accepted input; = current tier1_complete)')
    a1 = count(sat | {R.BOUND}, 'documentation_complete, variant A  (met or a valid sourced range/bound; pending selections NOT counted)')
    a2 = count(sat | {R.BOUND, R.SEL}, 'documentation_complete, variant B  (variant A plus pending source selections; = current all_blocking_documented)')

    def closed_only(rs):
        return all(r['representation'] == 'range' for r in rs if r['category'] == R.BOUND)
    a3 = count(sat | {R.BOUND}, 'range_aware_ready, illustration    (met or a CLOSED range only; one-sided bounds excluded)', closed_only)
    say('  products gained by variant A over point_calculation_ready:', sorted(a1 - a0))
    say('  products gained by variant B over variant A:', sorted(a2 - a1))
    say('  products in variant A that hold a one-sided bound or direction-less specification value:', sorted(a1 - a3))
    only_b = [p for p, rs in by.items() if cls[p] == 'base_oil' and any(r['category'] == R.BOUND for r in rs)]
    blockers = collections.Counter(c for p in only_b for c in {r['category'] for r in by[p]} - sat - {R.BOUND})
    say(f'  base oils with at least one range/bound requirement: {len(only_b)}; their OTHER unmet categories:', dict(blockers))
    say()

    # ------------------------------------------------------------------ decision 2: co-components
    say('== Decision 2: required co-components (78 packages) ==')
    co = {r['product_id']: r for r in out if r['requirement'] == 'required_co_components'}
    ev = {r['product']: r for r in read('reports/mandatory_properties/co_component_evidence.csv')}
    say('Current outcome categories:', dict(collections.Counter(r['category'] for r in co.values())))

    def state(pid):
        cat, e = co[pid]['category'], ev.get(pid, {})
        named, none = int(e.get('required_or_named_statements') or 0), int(e.get('none_required_statements') or 0)
        if cat == R.MET:
            return 'required, usable dose recorded'
        if cat == R.META:
            return 'required, dose recorded without a usable basis -> route incomplete'
        if named:
            return 'supplier names or requires a co-component, no usable dose recorded -> route incomplete'
        if none:
            return 'partial "none required" statement (one co-component type only) -> still unknown for the others'
        return 'silence -> unknown'
    for k, n in collections.Counter(state(p) for p in co).most_common():
        say(f'  {n:3d}  {k}')
    say('  (the statement counts come from a text-layer search of the cited pages: leads, not reviewed evidence)')
    say()

    # ------------------------------------------------------------------ decision 3: percentage basis
    say('== Decision 3: percentage basis (treat rates and co-component doses in the records) ==')
    prods = P.load_products()
    import json
    with open(os.path.join(HERE, 'treat_rate_basis_evidence.json'), encoding='utf-8') as fh:
        evidence = json.load(fh)['evidence']
    rows = []
    for pid, p in prods.items():
        ctx = R.Context(basis_evidence=evidence, product=pid)
        for d in p['files'].values():
            f = d.get('fields', {})
            items = [('treat_rate_matrix', (e or {}).get('treat_rate_wt_pct')) for e in f.get('treat_rate_matrix') or []]
            items += [('required_co_components', (e or {}).get('dose_wt_pct')) for e in f.get('required_co_components') or [] if isinstance(e, dict)]
            for k in ('treat_rate',):
                if isinstance(f.get(k), dict):
                    items.append((k, f[k]))
            for path, vo in items:
                if not isinstance(vo, dict) or vo.get('status') not in R.OK_STATUS:
                    continue
                u = str(vo.get('unit') or '')
                basis = ('mass (unit)' if MASS.search(u) else 'volume (unit)' if VOL.search(u) else
                         'mass (page evidence)' if ctx.mass_basis(path, vo) else 'unspecified')
                rows.append((pid, d.get('material_class'), path, u, basis))
    say('Reported dose values:', len(rows))
    for (path, basis), n in sorted(collections.Counter((r[2], r[4]) for r in rows).items()):
        say(f'  {path:24s} {basis:22s} {n}')
    say('  units recorded for the unspecified ones:', dict(collections.Counter(r[3] for r in rows if r[4] == 'unspecified')))
    say('  products with a volume-basis dose:', sorted({r[0] for r in rows if r[4].startswith('volume')}))
    tr = collections.Counter(r['category'] for r in out if r['requirement'] == 'treat_rate_matrix')
    say('Current treat_rate_matrix outcomes (78 packages):', dict(tr))
    say()

    # ------------------------------------------------------------------ decision 4: applicability
    say('== Decision 4: applicability ==')
    say('Approved applicability rules in force:', len(R.APPROVED_APPLICABILITY_RULES))
    na = collections.Counter()
    where = collections.defaultdict(set)
    for pid, p in prods.items():
        for d in p['files'].values():
            for path, n in P.value_objects(d.get('fields', {})):
                if n.get('status') in R.INAPPLICABLE_STATUS:
                    na[(d.get('material_class'), d.get('tier'), n.get('status'))] += 1
                    where[n.get('status')].add(pid)
    for k, n in sorted(na.items(), key=str):
        say(f'  value objects with status {k[2]!r}: class {k[0]}, tier {k[1]}: {n}')
    for k, v in where.items():
        say(f'  products using {k!r}:', sorted(v))
    ap_rows = [r for r in out if r['category'] == R.APPL]
    say('Blocking outcomes in category unresolved_applicability:', len(ap_rows))
    for (c, req), n in sorted(collections.Counter((r['material_class'], r['requirement']) for r in ap_rows).items()):
        say(f'    {c:20s} {req:40s} {n}')
    say('With no approved rule, every one of these stays unresolved: the simulated result equals the current one.')
    text = buf.getvalue()
    sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
    print(text, end='')
    if a.out:
        with open(a.out, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
