"""Column-level verification of the Petro-Canada PURITY edition-difference findings (2015.07 archive vs 2023.03 brochure)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
import audit_lib as A

EVID = os.path.join(A.REPO, 'reconciliation', 'audit_evidence', 'PetroCanada_PURITY_LUB3213E_2023-03__wayback_20251215051152.pdf')
ROWS = [('density', r'^Density @ 15°C, kg/L$'), ('colour', r'^Colou?r, ASTM$'), ('kv40', r'^@ 40°C, cSt$'), ('kv100', r'^@ 100°C, cSt$'),
        ('sus', r'^SUS @ 100°F$'), ('viscosity_index', r'^Viscosity Index$'), ('pour_point', r'^Pour Point, °C \(°F\)$'),
        ('flash_point_PM', r'^Flash Point, PM, °C \(°F\)$'), ('flash_point_COC', r'^Flash Point, COC, [ºo°]C \(°F\)$'),
        ('ccs[-20 C]', r'^@ -20°C, cP$'), ('ccs[-25 C]', r'^@ -25°C, cP$'), ('ccs[-30 C]', r'^@ -30°C, cP$'), ('ccs[-35 C]', r'^@ -35°C, cP$'),
        ('noack_volatility', r'^NOACK Volatility, % wt$'), ('saturates', r'^% Saturates$'), ('aromatics', r'^% Aromatics$'), ('sulfur', r'^Sulfur, ppm$')]


def parse(text):
    L = [l.strip() for l in text.splitlines() if l.strip()]
    grid = {}
    starts = [i for i, l in enumerate(L) if l == 'PRODUCT NAME']
    for si, s in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(L)
        n = 6 if L[s + 1] == 'L35' else 5
        grades = L[s + 1:s + 1 + n]
        for i in range(s + 1 + n, end):
            for prop, rx in ROWS:
                if re.match(rx, L[i]):
                    method, vals = L[i + 1], L[i + 2:i + 2 + n]
                    for g, v in zip(grades, vals):
                        grid.setdefault(g, {})[prop] = (v, method)
    return grid


ar = A.Archive()
g2015 = parse(ar.page_text('DL2-10020.pdf', 2))
g2023 = parse(pymupdf.open(EVID)[1].get_text())
assert set(g2015) == set(g2023) == {'L35', 'L40', 'L45', 'L50', 'L60', 'L65', '1003', '1017', '1020', '2204', '2305'}, (set(g2015), set(g2023))
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
out = []
for f in F:
    if not f['record_id'].startswith('PETRO_CANADA_PURITY_') or f['source_kind'] != 'documented': continue
    grade = f['record_id'].replace('PETRO_CANADA_PURITY_', '')
    prop = re.sub(r'^tier\d\.', '', f['property'])
    a = next((v for v in f['values'] if v.get('file') == 'DL2-10020.pdf'), None)
    b = next((v for v in f['values'] if str(v.get('file', '')).startswith('http')), None)
    if prop == 'viscosity_index' and not a:  # text-only L65 record
        a = {'value': 92, 'printed_text': None}; b = {'value': 104, 'printed_text': None}
    keys = [prop]
    if prop == 'flash_point':
        pt = ' '.join(str(x.get('printed_text') or '') + ' ' + str(x.get('value')) for x in (a, b) if x)
        keys = ['flash_point_COC'] if 'COC' in pt else ['flash_point_PM'] if re.search(r'PM|Pensky', pt) else ['flash_point_COC', 'flash_point_PM']
    res = []
    for k in keys:
        c15, c23 = g2015[grade].get(k), g2023[grade].get(k)
        num = lambda s: [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', str(s))[:1]]
        ok15 = c15 and a and num(c15[0]) == num(a.get('value') if a.get('value') is not None else a.get('printed_text'))
        ok23 = c23 and b and num(c23[0]) == num(b.get('value') if b.get('value') is not None else b.get('printed_text'))
        res.append(dict(row=k, col=grade, printed_2015=c15, printed_2023=c23, recorded_2015=a and (a.get('value'), a.get('printed_text')),
                        recorded_2023=b and (b.get('value'), b.get('printed_text')), match_2015=bool(ok15), match_2023=bool(ok23)))
    out.append(dict(id=f['id'], record_id=f['record_id'], property=f['property'], checks=res))
json.dump(dict(g2015=g2015, g2023=g2023, findings=out), open(os.path.join(A.SCR, 'audit', 'verify_pc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
bad = [o for o in out if not any(c['match_2015'] and c['match_2023'] for c in o['checks'])]
print('Petro-Canada documented findings', len(out), '| both editions match in the correct column and row', len(out) - len(bad))
for o in bad: print('  MISMATCH', o['id'], o['record_id'], o['property'], json.dumps(o['checks'], ensure_ascii=False)[:400])
amb = [o for o in out if len(o['checks']) > 1 or 'flash' in o['property']]
for o in amb: print('  flash method', o['id'], o['record_id'], [(c['row'], c['printed_2015'], c['printed_2023'], c['recorded_2015'][1] if c['recorded_2015'] else None) for c in o['checks']])
