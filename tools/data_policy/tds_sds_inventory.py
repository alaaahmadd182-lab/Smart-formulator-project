"""Rule 2, steps A and B: inventory every TDS-SDS comparison and establish comparability (read-only on data).

Sources of comparisons (deduplicated by product, property and the two printed values):
  1. the v5 audit findings (tools/audit/review_2026-11-02/output/findings_v5.json): every pair of a technical-document
     value and an SDS value inside one finding;
  2. conflicts[] entries of the product JSON that list a technical-document value and an SDS value;
  3. value objects whose selected value and an alternate entry come from different document classes.
Document class per (file, page) comes from reports/data_policy/document_classes.csv.

For each pair the value is parsed (number, qualifier / value kind, unit, temperature, method) and comparability is
decided BEFORE any difference is computed:
  comparable                  same product and property, convertible units, same condition (temperature), both point
                              values (typical or single), methods equal or not printed on one side (flagged)
  bound check only            one side is a bound (min / max / >= / <) or a range: no difference is computed; the
                              point value is checked against the bound
  not comparable: condition   different temperature or other stated condition (e.g. density at 15 vs 20 °C)
  not comparable: method      both methods printed and different (e.g. COC vs PMCC flash point)
  not comparable: quantity    different quantity (e.g. density vs relative density, kinematic vs dynamic viscosity)
  comparability unknown       unit, temperature or value missing on one side
For comparable pairs: absolute difference (canonical unit) and relative difference = |TDS - SDS| / |TDS| x 100
(undefined when the TDS value is 0; the absolute difference is then used), and the print-rounding tolerance
(half a unit of the last printed digit of the less precise value).

The PROPOSED screening outcome (tools/data_policy/thresholds.py) is shown per row for review only; no finding is
reclassified (review checkpoint, docs/data_policy_mandatory_review/threshold_proposal.md).

Usage: python tools/data_policy/tds_sds_inventory.py [--out reports/data_policy/tds_sds_comparisons.csv]
Writes only the --out file (and a summary to stdout). Exit 0.
"""
import argparse, collections, csv, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P
import thresholds as TH

FINDINGS = os.path.join(P.ROOT, 'tools', 'audit', 'review_2026-11-02', 'output', 'findings_v5.json')
PROPERTY_GROUP = {'kv40': 'viscosity', 'kv100': 'viscosity', 'density': 'density', 'specific_gravity': 'density',
                  'flash_point': 'flash point', 'pour_point': 'pour point', 'noack_volatility': 'volatility', 'tbn': 'TBN',
                  'viscosity_index': 'viscosity index', 'sulfur': 'composition', 'Zn': 'elements', 'Ca': 'elements',
                  'P': 'elements', 'Mg': 'elements', 'N': 'elements', 'S': 'elements', 'sulfated_ash': 'ash'}
GROUP_ORDER = ['viscosity', 'density', 'flash point', 'pour point', 'volatility', 'viscosity index', 'TBN', 'elements', 'ash', 'composition', 'other']
UNIT_FAMILY = {
    'visc': {'cst': 1, 'mm2/s': 1, 'mm²/s': 1, 'mm2/sec': 1},
    'dens': {'kg/m3': 0.001, 'kg/m³': 0.001, 'g/cm3': 1, 'g/cm³': 1, 'g/ml': 1, 'kg/l': 1, 'kg/dm3': 1, 'kg/dm³': 1},
    'temp': {'°c': 1, 'c': 1, '℃': 1},
}


def prop_of(path):
    keys = [k for k in re.split(r'[.\[\]]', str(path)) if k and not k.isdigit() and not re.fullmatch(r'tier\d', k)]
    return keys[-1] if keys else str(path)


def parse(v):
    """Parse one printed value dict into number / kind / unit / temperature / method / quantity."""
    text = ' '.join(str(v.get(k) or '') for k in ('value', 'printed_text', 'unit', 'conditions'))
    t = text.replace('−', '-').replace('，', ',').replace('㎡', 'm2')
    val = v.get('value')
    kind, num, lo, hi = 'point', None, None, None
    m = re.search(r'(-?\d+(?:[.,]\d+)?)\s*(?:-|–|~|to)\s*(-?\d+(?:[.,]\d+)?)\s*(cst|mm|kg|g/|°|℃|ppm|%|$)', str(val) + ' ', re.I)
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        num = float(val)
    elif m:
        kind, lo, hi = 'range', float(m.group(1).replace(',', '.')), float(m.group(2).replace(',', '.'))
    else:
        mm = re.search(r'(-?\d+(?:[.,]\d+)?)', str(val or ''))
        num = float(mm.group(1).replace(',', '.')) if mm else None
    sv = str(val or '') + ' ' + str(v.get('printed_text') or '')
    if re.search(r'≥|>=|≮|\bmin(imum)?\b|lower bound|>\s*\d', str(val or '')) or (num is not None and re.search(r'(≥|>=|≮|>)\s*' + re.escape(str(int(num)) if num == int(num) else str(num)), sv)):
        kind = 'lower bound'
    elif re.search(r'≤|<=|≯|\bmax(imum)?\b|upper limit|<\s*\d', str(val or '')):
        kind = 'upper bound'
    # the recorded qualifier / value_kind / min-max of a value object take precedence over the text
    q = str(v.get('qualifier') or '').strip()
    vk = str(v.get('value_kind') or '').lower()
    if q in ('>', '>=', '≥', 'min', 'minimum') or 'lower bound' in vk or 'minimum' in vk:
        kind = 'lower bound'
    elif q in ('<', '<=', '≤', 'max', 'maximum') or 'upper' in vk or 'maximum' in vk:
        kind = 'upper bound'
    elif num is None and isinstance(v.get('min'), (int, float)) and isinstance(v.get('max'), (int, float)):
        kind, lo, hi = 'range', float(v['min']), float(v['max'])
    unit = None
    for u in ('mm2/s', 'mm²/s', 'mm2/sec', 'cst', 'kg/m3', 'kg/m³', 'g/cm3', 'g/cm³', 'g/ml', 'kg/l', 'kg/dm3', 'kg/dm³', '°c', '℃', 'mgkoh/g', 'mg koh/g', 'ppm', 'wt%', 'wt.%', 'mass%', 'mass %', '%'):
        if u in t.lower().replace(' (', ' '):
            unit = u
            break
    temp = None
    if isinstance(v.get('test_temperature_c'), (int, float)):
        temp = float(v['test_temperature_c'])
    deg = r'(?:°\s*℃|°\s*C|℃)'
    mt = re.search(r'\(\s*(\d+(?:\.\d+)?)\s*' + deg + r'|(?:@|at)\s*(\d+(?:\.\d+)?)\s*' + deg + r'|(\d+(?:\.\d+)?)\s*' + deg + r'\s*\)', t, re.I)
    if mt and temp is None:
        temp = float(next(x for x in mt.groups() if x))
    mth = sorted(set(x.upper().replace(' ', '').replace('-', '') for x in re.findall(r'ASTM\s*-?\s*D\s*-?\s*\d{2,5}|ISO\s*\d{3,5}', t + ' ' + str(v.get('method') or ''), re.I)))
    if 'ASTMD92' in mth:
        cup = 'COC'
    elif 'ASTMD93' in mth:
        cup = 'PMCC'
    else:
        cup = 'COC' if re.search(r'\bCOC\b|cleveland|open\s+cup', t, re.I) else 'PMCC' if re.search(r'\bPM\b|PMCC|pensky|closed\s+cup', t, re.I) else None
    # quantity as labelled; a label that contradicts the printed unit is recorded, not silently corrected
    quantity, label_issue, ref = None, None, None
    if re.search(r'relative\s+density|specific\s+gravity|sp\.\s*gravity', t, re.I):
        quantity = 'relative density'
        if re.search(r'g/cm|kg/m|kg/l', t, re.I):
            label_issue = "labelled 'relative density' but printed with a density unit"
        mref = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)\s*(?:°\s*[CF]|℃)', t)
        ref = f'{mref.group(1)}/{mref.group(2)}' if mref else None
    if re.search(r'viscosity,\s*dynamic', t, re.I):
        quantity = 'dynamic viscosity'
        if re.search(r'mm2/s|mm²/s|cst', t, re.I):
            label_issue = "labelled 'dynamic' but printed with a kinematic unit (mm²/s)"
    decimals = None
    raw = None
    if num is not None:
        for mnum in re.finditer(r'(-?\d+(?:[.,](\d+))?)', str(v.get('printed_text') or '').replace('−', '-')):
            try:
                if abs(float(mnum.group(0).replace(',', '.')) - num) < 1e-9:
                    raw = mnum
                    break
            except ValueError:
                pass
    if raw is None:
        raw = re.search(r'(-?\d+(?:[.,](\d+))?)', str(val if not isinstance(val, float) or val != int(val) else int(val)))
    if raw:
        decimals = len(raw.group(2) or '')
    return dict(num=num, lo=lo, hi=hi, kind=kind, unit=unit, temp=temp, methods=mth, cup=cup, quantity=quantity, label_issue=label_issue,
                sg_ref=ref, decimals=decimals, text=text.strip())


def canon(p, num):
    if num is None or not p['unit']:
        return None, None
    u = p['unit'].lower()
    for fam, table in UNIT_FAMILY.items():
        if u in table:
            return fam, num * table[u]
    return u, num


def compare(prop, tds, sds):
    a, b = parse(tds), parse(sds)
    row = dict(tds_kind=a['kind'], sds_kind=b['kind'], tds_unit=a['unit'], sds_unit=b['unit'], tds_temp=a['temp'], sds_temp=b['temp'],
               tds_method='/'.join(a['methods']) or a['cup'] or '', sds_method='/'.join(b['methods']) or b['cup'] or '')
    caveat = None
    if a['label_issue'] or b['label_issue']:
        # the label and the printed unit disagree on one side: numbers are shown, the pair stays pending review
        caveat = 'label/unit inconsistent: ' + '; '.join(f'{s} {x["label_issue"]}' for s, x in (('TDS', a), ('SDS', b)) if x['label_issue'])
    elif prop == 'specific_gravity' or a['quantity'] == b['quantity'] == 'relative density':
        if a['sg_ref'] and b['sg_ref'] and a['sg_ref'] != b['sg_ref']:
            return dict(row, comparability='not comparable: condition', reason=f"reference temperatures {a['sg_ref']} vs {b['sg_ref']}")
        if not (a['sg_ref'] and b['sg_ref']):
            caveat = 'relative-density reference temperatures not printed on both sides (' + ', '.join(
                f'{s}: {x["sg_ref"] or "not printed"}' for s, x in (('TDS', a), ('SDS', b))) + ')'
    elif a['quantity'] != b['quantity']:
        return dict(row, comparability='not comparable: quantity', reason=f"{a['quantity'] or 'stated quantity'} vs {b['quantity'] or 'stated quantity'}")
    r = _numeric(prop, a, b, row)
    if caveat and r['comparability'] == 'comparable':
        r.update(comparability='comparability unknown', reason=caveat + '; difference shown for information only')
    elif caveat:
        r['reason'] = (r['reason'] + '; ' if r['reason'] else '') + caveat
    return r


def _numeric(prop, a, b, row):
    if a['kind'] != 'point' or b['kind'] != 'point':
        pt, bd = (a, b) if a['kind'] == 'point' else (b, a)
        if pt['kind'] != 'point':
            return dict(row, comparability='bound check only', reason='both sides are bounds or ranges')
        x = pt['num']; ok = None
        if bd['kind'] == 'lower bound' and bd['num'] is not None and x is not None:
            ok = x >= bd['num']
        elif bd['kind'] == 'upper bound' and bd['num'] is not None and x is not None:
            ok = x <= bd['num']
        elif bd['kind'] == 'range' and x is not None:
            ok = bd['lo'] <= x <= bd['hi']
        return dict(row, comparability='bound check only',
                    reason=('point value satisfies the bound' if ok else 'point value outside the bound' if ok is False else 'bound not parsed'),
                    bound_satisfied='' if ok is None else str(ok).lower())
    if a['num'] is None or b['num'] is None:
        return dict(row, comparability='comparability unknown', reason='a value is not numeric')
    fa, ca = canon(a, a['num']); fb, cb = canon(b, b['num'])
    implied = {'kv40': 40.0, 'kv100': 100.0}
    ta = a['temp'] if prop not in implied else (a['temp'] or implied[prop])
    tb = b['temp'] if prop not in implied else (b['temp'] or implied[prop])
    if prop == 'specific_gravity':
        ta = tb = None  # the condition is the reference-temperature pair, checked in compare()
    elif prop == 'density' and (ta is None or tb is None):
        return dict(row, comparability='comparability unknown', reason='temperature not printed on one side')
    if ta is not None and tb is not None and abs(ta - tb) > 0.6:
        return dict(row, comparability='not comparable: condition', reason=f'temperature {ta} vs {tb} °C')
    if prop in ('flash_point',) and a['cup'] and b['cup'] and a['cup'] != b['cup']:
        return dict(row, comparability='not comparable: method', reason=f"{a['cup']} vs {b['cup']}")
    if a['methods'] and b['methods'] and not set(a['methods']) & set(b['methods']):
        return dict(row, comparability='not comparable: method', reason=f"{'/'.join(a['methods'])} vs {'/'.join(b['methods'])}")
    if ca is None or cb is None:
        if (a['unit'] is None) != (b['unit'] is None) and prop not in ('viscosity_index',):
            return dict(row, comparability='comparability unknown', reason='unit not printed on one side')
        ca, cb = a['num'], b['num']
    elif fa != fb:
        return dict(row, comparability='comparability unknown', reason=f'units not convertible: {a["unit"]} vs {b["unit"]}')
    diff = abs(ca - cb)
    rel = (diff / abs(ca) * 100) if ca else None
    dec = min(x for x in (a['decimals'], b['decimals']) if x is not None) if a['decimals'] is not None or b['decimals'] is not None else 0
    scale = 0.001 if fa == 'dens' and ((a['unit'] or '').lower().startswith('kg/m') or (b['unit'] or '').lower().startswith('kg/m')) else 1
    tol = 0.5 * 10 ** (-dec) * scale
    method_note = '' if (a['methods'] and b['methods']) or (a['cup'] and b['cup']) else 'method not printed on one or both sides'
    return dict(row, comparability='comparable', reason=method_note, tds_canonical=round(ca, 6), sds_canonical=round(cb, 6),
                abs_diff=round(diff, 6), rel_diff_pct=None if rel is None else round(rel, 3), rounding_tolerance=round(tol, 6),
                within_rounding=str(diff <= tol + 1e-12).lower())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'tds_sds_comparisons.csv'))
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    cls = {(r['file'], r['page']): r['class'] for r in csv.DictReader(open(os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'), encoding='utf-8'))}
    def c_of(f, pg):
        pgs = re.findall(r'\d+', str(pg)) if pg not in (None, '') else []
        return cls.get((str(f), pgs[0] if pgs else ''))
    pairs = collections.OrderedDict()
    def vkey(v):
        p = parse(v)
        return str(p['num'] if p['num'] is not None else (p['lo'], p['hi']) if p['lo'] is not None else v.get('value'))

    def add(pid, prop, tds, sds, origin):
        prop = prop.strip().replace(' ', '_')
        key = (pid, prop, str(tds.get('file')), vkey(tds), str(sds.get('file')), vkey(sds))
        if key in pairs:
            pairs[key]['origin'] += '; ' + origin
        else:
            pairs[key] = dict(product=pid, property=prop, tds=tds, sds=sds, origin=origin)
    for f in json.load(open(FINDINGS, encoding='utf-8')):
        files = [v for v in f['values'] if v.get('file') and ';' not in str(v.get('file'))]
        tech = [v for v in files if c_of(v['file'], v.get('page')) == 'TECHNICAL']
        sds = [v for v in files if c_of(v['file'], v.get('page')) == 'SDS']
        for t in tech:
            for s in sds:
                for prop in [x.strip() for x in re.split(r'[;,]', f['property'])] if ';' in f['property'] else [f['property']]:
                    add(f['record_id'], prop_of(prop), t, s, f"audit {f['id']}")
    prods = P.load_products()
    for pid, p in prods.items():
        for rel, d in p['files'].items():
            for c in d.get('conflicts') or []:
                if not isinstance(c, dict) or not isinstance(c.get('values'), list):
                    continue
                vals = [v for v in c['values'] if isinstance(v, dict) and v.get('file')]
                tech = [v for v in vals if c_of(v['file'], v.get('page')) == 'TECHNICAL']
                sds = [v for v in vals if c_of(v['file'], v.get('page')) == 'SDS']
                for t in tech:
                    for s in sds:
                        add(pid, prop_of(c.get('field') or c.get('property')), t, s, f"conflicts[] {rel.rsplit('/', 1)[1]}")
            for path, n in P.value_objects(d.get('fields', {})):
                sel = dict(n, file=P.src(n)[0], page=P.src(n)[1])
                for alt in n.get('alternate_entries') or []:
                    s2 = alt.get('source') or {}
                    av = dict(alt, file=s2.get('file'), page=s2.get('page'))
                    cs, ca = c_of(sel['file'], sel['page']), c_of(av['file'], av['page'])
                    if {cs, ca} == {'TECHNICAL', 'SDS'}:
                        t, s = (sel, av) if cs == 'TECHNICAL' else (av, sel)
                        add(pid, prop_of(path), t, s, f"alternate entry {rel.rsplit('/', 1)[1]}#{path}")
    rows = []
    for k, x in pairs.items():
        r = compare(x['property'], x['tds'], x['sds'])
        grp = PROPERTY_GROUP.get(x['property'], 'other')
        rows.append(dict(group=grp, property=x['property'], product=x['product'],
                         tds_value=str(x['tds'].get('value')), tds_printed=str(x['tds'].get('printed_text') or ''), tds_file=x['tds'].get('file'), tds_page=x['tds'].get('page'),
                         sds_value=str(x['sds'].get('value')), sds_printed=str(x['sds'].get('printed_text') or ''), sds_file=x['sds'].get('file'), sds_page=x['sds'].get('page'),
                         origin=x['origin'], **r))
        rows[-1]['proposed_screen'] = TH.screen(x['property'], r['comparability'], r.get('rel_diff_pct'), r.get('abs_diff'),
                                                r.get('bound_satisfied', ''), r.get('within_rounding', ''))
        rows[-1]['thresholds_version'] = TH.VERSION
    rows.sort(key=lambda r: (GROUP_ORDER.index(r['group']) if r['group'] in GROUP_ORDER else 99, r['property'], r['product']))
    cols = ['group', 'property', 'product', 'tds_value', 'tds_printed', 'tds_file', 'tds_page', 'sds_value', 'sds_printed', 'sds_file', 'sds_page',
            'tds_kind', 'sds_kind', 'tds_unit', 'sds_unit', 'tds_temp', 'sds_temp', 'tds_method', 'sds_method', 'comparability', 'reason',
            'bound_satisfied', 'tds_canonical', 'sds_canonical', 'abs_diff', 'rel_diff_pct', 'rounding_tolerance', 'within_rounding', 'proposed_screen', 'thresholds_version', 'origin']
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols, lineterminator='\n', extrasaction='ignore'); w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, '') for c in cols})
    print(f'TDS-SDS comparisons: {len(rows)}')
    by = collections.Counter((r['group'], r['comparability']) for r in rows)
    for g in GROUP_ORDER:
        sub = {k[1]: v for k, v in by.items() if k[0] == g}
        if sub:
            print(f'  {g}: {sum(sub.values())}  {dict(sub)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
