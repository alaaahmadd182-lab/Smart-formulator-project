#!/usr/bin/env python3
"""Task 5 report: open_questions_and_conflicts.md generated from every product JSON (read-only).

Usage: python build_conflicts_report.py [--input Products_json] [--output open_questions_and_conflicts.md]

Sections: 1 unresolved conflicts, 2 resolved values (value_final) and resolved conflict records,
3 reported numeric values with no test method, no unit or no reference temperature,
4 open questions per product. Final (integrated) keys are used where present, else the originals.
"""
import argparse, collections, datetime, glob, json, os, re, sys

CLASSES = (('base_oil', 'Base oils'), ('additive_package', 'Additive packages'), ('additive_component', 'Additive components'))
NEEDS_TEMPERATURE = {'kv40', 'kv100', 'delta_kv100_cst', 'density', 'ccs', 'ccs_viscosity', 'mrv', 'mrv_viscosity',
                     'yield_stress', 'hths', 'noack_volatility'}
UNITLESS = {'viscosity_index', 'shear_stability'}
# Doses and composition shares are recommendations, not test results: no test method is expected.
NO_METHOD_EXPECTED = {'treat_rate', 'treat_rate_wt_pct', 'treat_range_wt_pct', 'dose_wt_pct', 'tested_dose_range_wt_pct',
                      'share_wt_pct', 'carrier_share_wt_pct', 'wt_pct', 'active_content'}


def long_path(p):
    """Windows extended-length path so files beyond the 260-character limit are never skipped."""
    s = os.path.abspath(str(p))
    return '\\\\?\\' + s if os.name == 'nt' and not s.startswith('\\\\?\\') else s


def final(node, key):
    return node[f'{key}_final'] if f'{key}_final' in node else node.get(key)


def md(v):
    """One table cell: no line breaks, pipes escaped, empty shown as a dash."""
    if v is None or v == '' or v == []:
        return '–'
    if isinstance(v, dict):
        v = f"{v.get('file') or v.get('url')} p.{v.get('page')}" if ('file' in v or 'url' in v) else json.dumps(v, ensure_ascii=False)
    elif isinstance(v, list):
        v = '; '.join(md(x) for x in v)
    return re.sub(r'\s+', ' ', str(v)).replace('|', '\\|')


def last_key(path):
    keys = [k for k in re.split(r'[.\[\]]', path) if k and not k.isdigit()]
    return keys[-1] if keys else path


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def walk(node, path, parent, out):
    """Yield (path, value object, parent container) for every value object in fields{}."""
    if isinstance(node, dict):
        if 'status' in node and 'value' in node and not isinstance(node['status'], dict):
            out.append((path, node, parent))
        for k, v in node.items():
            if k not in ('source', 'source_final', 'alternate_entries'):
                walk(v, f'{path}.{k}' if path else k, node, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f'{path}[{i}]', parent, out)


def load(root):
    products = collections.OrderedDict()
    for f in sorted(glob.glob(os.path.join(os.path.abspath(root), '**', '*.json'), recursive=True)):
        with open(long_path(f), encoding='utf-8') as fh:
            d = json.load(fh)
        key = (d.get('material_class'), os.path.relpath(os.path.dirname(f), os.path.abspath(root)))
        products.setdefault(key, []).append(d)
    for docs in products.values():
        docs.sort(key=lambda d: (d.get('tier') or 0, str(d.get('component_subtype'))))
    return products


def tier_label(d):
    return f"tier{d.get('tier')}" + (f" {d['component_subtype']}" if d.get('component_subtype') else '')


def build(products, generated):
    unresolved, resolved_values, resolved_records, gaps, questions = [], [], [], [], collections.OrderedDict()
    seen_conflicts, corrections, unresolved_values = set(), [], []
    for (cl, folder), docs in products.items():
        pid = os.path.basename(folder)
        for d in docs:
            tl = tier_label(d)
            for c in d.get('conflicts', []):
                body = {k: v for k, v in c.items() if k not in ('resolved', 'final_resolution')} if isinstance(c, dict) else c
                sig = (pid, json.dumps(body, ensure_ascii=False, sort_keys=True))
                if sig in seen_conflicts:  # the same conflict is often repeated in every tier file
                    continue
                seen_conflicts.add(sig)
                row = (cl, pid, tl, body, c.get('final_resolution') if isinstance(c, dict) else None)
                (resolved_records if isinstance(c, dict) and c.get('resolved') else unresolved).append(row)
            nodes = []
            walk(d.get('fields', {}), '', None, nodes)
            for path, n, parent in nodes:
                if n.get('resolution') and 'value_final' in n:
                    target = unresolved_values if n['resolution'].startswith('UNRESOLVED') else resolved_values
                    target.append((cl, pid, tl, path, n))
                conv = str(n.get('unit_conversion') or '')
                if 'does not match printed text' in conv or any('left null' in fl for fl in n.get('integration_flags', [])):
                    corrections.append((cl, pid, tl, path, n))
                status = str(final(n, 'status') or '').lower()
                v = final(n, 'value')
                if status != 'reported' or not any(is_num(x) for x in (v, final(n, 'min'), final(n, 'max'))):
                    continue
                key, missing = last_key(path), []
                if key not in NO_METHOD_EXPECTED and not final(n, 'method'):
                    missing.append('method')
                if key not in UNITLESS and not final(n, 'unit'):
                    missing.append('unit')
                if key in NEEDS_TEMPERATURE:
                    t = final(n, 'test_temperature_c')
                    if t is None and isinstance(parent, dict):
                        t = parent.get('test_temperature_c')
                    if t is None:
                        missing.append('temperature')
                if missing:
                    rng = '–'.join(md(final(n, k)) for k in ('min', 'max')) if v is None else md(v)
                    gaps.append((cl, pid, tl, path, rng, final(n, 'unit'), missing))
            for q in d.get('open_questions', []):
                questions.setdefault((cl, pid), []).append((tl, q))

    L = ['# Open questions and conflicts (all products)', '',
         f'Generated {generated} by `build_conflicts_report.py` from the `open_questions`, `conflicts` and '
         '`fields` of every JSON file in `Products_json` (base oils, additive packages, additive components). '
         'Final values (`value_final`, `unit_final`, `status_final`, `source_final`, written by '
         '`integrate_products.py`) are used where present, otherwise the original keys.', '',
         '| Section | Count |', '|---|---|',
         f'| 1. Unresolved conflicts | {len(unresolved)} |',
         f'| 2a. Properties whose value_final was resolved | {len(resolved_values)} |',
         f'| 2b. Conflict records marked resolved | {len(resolved_records)} '
         f'({sum(1 for r in resolved_records if not r[4] or "see " not in r[4].lower())} needed no value change) |',
         f'| 2c. value_final corrected or left null during unit integration | {len(corrections)} |',
         f'| 3. Reported numeric values with no method, unit or reference temperature | {len(gaps)} |',
         f'| 4. Open questions | {sum(len(v) for v in questions.values())} (in {len(questions)} products) |', '']

    L += ['## 1. Unresolved conflicts', '',
          'The resolution rules could not choose a value for these. The value_final shown is the field as it stands, '
          'pending supplier confirmation.', '']
    by_pid = {(r[1], last_key(r[3])): r for r in unresolved_values}
    for cl, pid, tl, body, note in unresolved:
        L.append(f'### {pid} ({dict(CLASSES)[cl]}, {tl})')
        L.append(f'- **Recorded conflict:** {md(body)}')
        prop = (body.get('field') or body.get('property') or '') if isinstance(body, dict) else ''
        match = next((r for (p, k), r in by_pid.items() if p == pid and k in prop), None)
        if match:
            n = match[4]
            L.append(f"- **Property:** `{match[2]} fields.{match[3]}`; value_final **{md(n.get('value_final'))} "
                     f"{md(n.get('unit_final'))}** (printed: {md(n.get('printed_text'))}; source {md(n.get('source'))})")
            L.append(f"- **Why unresolved:** {md(n['resolution'][len('UNRESOLVED: '):])}")
        L.append('')

    L += ['## 2. Resolved values', '',
          'Rules (user decision 2026-10-24): TDS (or PDS / bulletin / specification sheet) preferred over SDS; '
          'same document type -> newest dated edition, or the average (status Calculated) when the dates cannot be '
          'compared; text values take the newest; a measured or typical number beats a bound; the user decisions '
          'of 2026-10-18 on RF6077 and RF6088F are kept.', '',
          '### 2a. Properties whose value_final was resolved', '',
          '| Class | Product | Tier | Property | Original value | value_final | Final status | Final source | How it was resolved |',
          '|---|---|---|---|---|---|---|---|---|']
    for cl, pid, tl, path, n in resolved_values:
        orig = f"{md(n.get('value'))} {md(n.get('unit'))}" if n.get('value') is not None else f"– (printed: {md(n.get('printed_text'))})"
        L.append(f"| {dict(CLASSES)[cl]} | {pid} | {tl} | `{path}` | {orig} | **{md(n.get('value_final'))} "
                 f"{md(n.get('unit_final'))}** | {md(final(n, 'status'))} | {md(final(n, 'source'))} | {md(n['resolution'])} |")
    L += ['', '### 2b. Conflict records marked resolved', '',
          'Every resolved entry of the `conflicts` arrays (duplicates across tier files listed once). Entries pointing '
          'to a property are detailed in 2a; the others needed no value change, e.g. claim conflicts where the fields '
          'already held the newest edition.', '',
          '| Class | Product | Tier | Recorded conflict | Final resolution |', '|---|---|---|---|---|']
    for cl, pid, tl, body, note in resolved_records:
        L.append(f'| {dict(CLASSES)[cl]} | {pid} | {tl} | {md(body)} | {md(note)} |')
    L += ['', '### 2c. value_final corrected or left null during unit integration', '',
          '| Class | Product | Tier | Property | Printed | value | value_final | Note |', '|---|---|---|---|---|---|---|---|']
    for cl, pid, tl, path, n in corrections:
        note = n.get('unit_conversion') if 'does not match' in str(n.get('unit_conversion')) else '; '.join(n.get('integration_flags', []))
        L.append(f"| {dict(CLASSES)[cl]} | {pid} | {tl} | `{path}` | {md(n.get('printed_text'))} | {md(n.get('value'))} "
                 f"{md(n.get('unit'))} | {md(n.get('value_final'))} {md(n.get('unit_final'))} | {md(note)} |")

    counts = collections.Counter(m for g in gaps for m in g[6])
    L += ['', '## 3. Reported numeric values with no test method, no unit or no reference temperature', '',
          f"{len(gaps)} reported numeric values: {counts['method']} with no method, {counts['unit']} with no unit, "
          f"{counts['temperature']} with no reference temperature. A reference temperature is checked only where the "
          f"property needs one ({', '.join(sorted(NEEDS_TEMPERATURE))}); viscosity index and shear stability index are "
          'unitless. Treat rates, doses and composition shares are recommendations, not test results, so they are '
          'checked for a unit but not for a method. For Noack the method itself fixes 250 °C / 1 h, but the '
          'temperature is still listed when it is not recorded.', '']
    for cl, label in CLASSES:
        rows = [g for g in gaps if g[0] == cl]
        L += [f'### {label} ({len(rows)})', '', '| Product | Tier | Property | Value | Unit | Missing |', '|---|---|---|---|---|---|']
        L += [f'| {pid} | {tl} | `{path}` | {val} | {md(unit)} | {", ".join(miss)} |' for _, pid, tl, path, val, unit, miss in rows]
        L.append('')

    L += ['## 4. Open questions', '']
    for cl, label in CLASSES:
        L += [f'### {label}', '']
        for (qcl, pid), qs in questions.items():
            if qcl != cl:
                continue
            L.append(f'#### {pid}')
            for tl, q in qs:
                if isinstance(q, dict):
                    head = q.get('fields') or q.get('field')
                    text = q.get('question') or q.get('note')
                    q = (f'`{md(head)}`: ' if head else '') + md(text) + (f" (sources: {md(q['source_files'])})" if q.get('source_files') else '')
                L.append(f'- ({tl}) {md(q)}')
            L.append('')
    return '\n'.join(L).rstrip() + '\n', len(unresolved), len(resolved_values), len(gaps)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--input', default='Products_json', help='product JSON folder (default: Products_json)')
    ap.add_argument('--output', default='open_questions_and_conflicts.md', help='report to write')
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    if not os.path.isdir(args.input):
        sys.exit(f'input folder not found: {args.input}')
    text, n_unres, n_res, n_gaps = build(load(args.input), datetime.date.today().isoformat())
    with open(args.output, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(text)
    print(f'OUTPUT {args.output}: unresolved conflicts {n_unres}, resolved values {n_res}, '
          f'method/unit/temperature gaps {n_gaps}')


if __name__ == '__main__':
    main()
