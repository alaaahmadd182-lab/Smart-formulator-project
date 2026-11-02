"""Column-level check of the multi-grade-table findings (read-only).

Petro-Canada PURITY (LUB3213E): the 2015.07 archive brochure DL2-10020.pdf p.2 and the 2023.03 brochure saved in
reconciliation/audit_evidence are parsed into grade x property grids; every Petro-Canada finding's two values must
sit in the finding's own grade column and property row.
S-OIL: the catalog DL2-11177.pdf p.1 and the saved S-OIL web page (live 2026-10-30 and Internet Archive 2026-06-10
captures) are parsed the same way for every S-OIL finding that compares the catalog with the web table.

Re-implements the logic of the 2026-10-30 scripts verify_pc.py / verify_soil.py (preserved in
tools/audit/original_2026-10-27_to_30/) with repository-relative paths.

Usage: python tools/audit/review_2026-11-02/check_columns.py [--findings PATH]
Exit codes: 0 every value found in its column and row; 1 otherwise.
"""
import argparse, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
import review_lib as R

PC_EVID = os.path.join(R.EVIDENCE, 'PetroCanada_PURITY_LUB3213E_2023-03__wayback_20251215051152.pdf')
PC_ROWS = [('density', r'^Density @ 15°C, kg/L$'), ('colour', r'^Colou?r, ASTM$'), ('kv40', r'^@ 40°C, cSt$'), ('kv100', r'^@ 100°C, cSt$'),
           ('sus', r'^SUS @ 100°F$'), ('viscosity_index', r'^Viscosity Index$'), ('pour_point', r'^Pour Point, °C \(°F\)$'),
           ('flash_point_PM', r'^Flash Point, PM, °C \(°F\)$'), ('flash_point_COC', r'^Flash Point, COC, [ºo°]C \(°F\)$'),
           ('ccs[-20 C]', r'^@ -20°C, cP$'), ('ccs[-25 C]', r'^@ -25°C, cP$'), ('ccs[-30 C]', r'^@ -30°C, cP$'), ('ccs[-35 C]', r'^@ -35°C, cP$'),
           ('noack_volatility', r'^NOACK Volatility, % wt$'), ('saturates', r'^% Saturates$'), ('aromatics', r'^% Aromatics$'), ('sulfur', r'^Sulfur, ppm$')]
GR = ['2', '3', '4', '6', '8']


def first_num(s):
    m = re.findall(r'-?\d+(?:\.\d+)?', str(s).replace('−', '-').replace(',', ''))
    return float(m[0]) if m else None


def pc_grid(text):
    L = [l.strip() for l in text.splitlines() if l.strip()]
    grid = {}
    starts = [i for i, l in enumerate(L) if l == 'PRODUCT NAME']
    for si, s in enumerate(starts):
        end = starts[si + 1] if si + 1 < len(starts) else len(L)
        n = 6 if L[s + 1] == 'L35' else 5
        grades = L[s + 1:s + 1 + n]
        for i in range(s + 1 + n, end):
            for prop, rx in PC_ROWS:
                if re.match(rx, L[i]):
                    for g, v in zip(grades, L[i + 2:i + 2 + n]):
                        grid.setdefault(g, {})[prop] = v
    return grid


def web_cells(t):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '|', t))
    return [c.strip() for c in re.sub(r'\s*\|[\s|]*', '|', t).split('|') if c.strip()]


def web_grid(path, brand):
    c = web_cells(open(path, encoding='utf-8', errors='replace').read())
    hdr = [i for i in range(len(c) - 6) if c[i] == 'ASTM' and c[i + 1] == f'{brand} 2']
    if not hdr:
        return None
    rows = {'Density @ 15.6℃, kg/L': 'density', 'Kinematic Viscosity @ 40℃, cSt': 'kv40', 'Kinematic Viscosity @ 100℃, cSt': 'kv100',
            'Viscosity Index': 'viscosity_index', 'Pour Point, ℃': 'pour_point', 'Noack Volatility, wt% (Procedure B)': 'noack_volatility'}
    i, grid = hdr[0] + 6, {g: {} for g in GR}
    while i < len(c) - 7 and i - hdr[0] <= 200 and not c[i].startswith(('aramcoULTRA base oil is', 'Ultra-S base oil is', 'S-OIL')):
        key = rows.get(c[i]) or ('flash_point' if c[i].replace(' ', '').startswith('FlashPoint,COC') else None)
        if key:
            for g, v in zip(GR, c[i + 2:i + 7]):
                grid[g][key] = v
            i += 7
        else:
            i += 1
    return grid


def soil_catalog(text):
    L = [l.strip() for l in text.splitlines() if l.strip()]
    s = L.index('Ultra-S 8'); grid = {g: {} for g in GR}
    def row(label, n=5):
        i = next(j for j in range(s, len(L)) if L[j].startswith(label)); return L[i:i + 2 + n]
    for g, v in zip(GR, row('Sp.Gravity')[2:7]):
        grid[g]['specific_gravity'] = v
    i = next(j for j in range(s, len(L)) if L[j].startswith('Kin.Vis @40')); vals = L[i + 3:i + 13]
    for k, g in enumerate(GR):
        grid[g]['kv40'], grid[g]['kv100'] = vals[2 * k], vals[2 * k + 1]
    for label, key in (('Viscosity Index', 'viscosity_index'), ('Flash Point', 'flash_point'), ('Pour Point', 'pour_point')):
        for g, v in zip(GR, row(label)[2:7]):
            grid[g][key] = v
    return grid


def cosan_grid(text):
    """Cosan 'Typical Properties Ultra-S Series' sheet DL2-11240.pdf p.1: columns Ultra-S 4, 6, 8."""
    L = [l.strip() for l in text.splitlines() if l.strip()]
    cols = ['Ultra-S 4', 'Ultra-S 6', 'Ultra-S 8']; grid = {c: {} for c in cols}
    def after(label, skip):
        i = next(j for j, l in enumerate(L) if l.startswith(label)); return L[i + 1 + skip:i + 4 + skip]
    for label, key, skip in (('Sp.Gravity', 'specific_gravity', 1), ('Kin.Vis@40', 'kv40', 0), ('@100', 'kv100', 0),
                             ('Viscosity Index', 'viscosity_index', 1), ('Flash Point', 'flash_point', 1), ('Pour Point', 'pour_point', 1),
                             ('Noack', 'noack_volatility', 1)):
        for c, v in zip(cols, after(label, skip)):
            grid[c][key] = v
    return grid


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--findings', default=R.SNAPSHOT_FINDINGS)
    ap.add_argument('--out', help='write the citation keys verified here (JSON list)'); a = ap.parse_args()
    F = json.load(open(a.findings, encoding='utf-8'))
    ar = R.Archive(); fails = []
    verified = set()  # 'CF-xxx#value_index#file' of every citation that passed its column/row check

    def key(f, v):
        return f"{f['id']}#{f['values'].index(v)}#{v['file']}"
    g15 = pc_grid(ar.pages('DL2-10020.pdf')[1]); g23 = pc_grid(pymupdf.open(PC_EVID)[1].get_text())
    grades = {'L35', 'L40', 'L45', 'L50', 'L60', 'L65', '1003', '1017', '1020', '2204', '2305'}
    if not (set(g15) == set(g23) == grades):
        print('FAIL Petro-Canada grids not parsed', set(g15), set(g23)); return 1
    n_pc = 0
    for f in F:
        if not f['record_id'].startswith('PETRO_CANADA_PURITY_') or f['id'] == 'CF-147':
            continue
        n_pc += 1
        grade = f['record_id'].replace('PETRO_CANADA_PURITY_', '')
        prop = re.sub(r'^tier\d\.', '', f['property'])
        a15 = next((v for v in f['values'] if str(v.get('file')) == 'DL2-10020.pdf'), None)
        b23 = next((v for v in f['values'] if v is not a15), None)
        v15 = a15.get('value') if a15 else None; v23 = b23.get('value') if b23 else None
        if prop == 'viscosity_index' and f['id'] == 'CF-093':  # stored as text in the JSON ("brochure reports 104")
            v15, v23 = 92, 104
        keys = [prop] if prop != 'flash_point' else ['flash_point_COC', 'flash_point_PM']
        ok = any(first_num(g15[grade].get(k)) == first_num(v15) and first_num(g23[grade].get(k)) == first_num(v23) for k in keys)
        if ok:
            verified.update({key(f, a15), key(f, b23)})
        if not ok:
            fails.append(f"{f['id']} {grade} {prop}: recorded {v15} / {v23}; printed {[g15[grade].get(k) for k in keys]} / {[g23[grade].get(k) for k in keys]}")
    print(f'Petro-Canada: {n_pc} findings checked in grade column and property row of both editions; mismatches {len(fails)}')
    cat = soil_catalog(ar.pages('DL2-11177.pdf')[0])
    live = web_grid(os.path.join(R.EVIDENCE, 'SOIL_LubeBaseOil_live_2026-10-30.html'), 'Ultra-S')
    live_au = web_grid(os.path.join(R.EVIDENCE, 'SOIL_LubeBaseOil_live_2026-10-30.html'), 'aramcoULTRA')
    wb = os.path.join(R.EVIDENCE, 'SOIL_LubeBaseOil__wayback_20260610070302.html')
    wbg = web_grid(wb, 'Ultra-S') or web_grid(wb, 'aramcoULTRA')
    print('S-OIL web: aramcoULTRA table == Ultra-S table:', live_au == live, '| Internet Archive 2026-06-10 == live 2026-10-30:', wbg == live)
    n_so = 0; so_fail = []
    # CF-141: three multi-property value sets for Ultra-S 6 (catalog, Cosan distributor sheet, web table)
    KEYS = {'kv40': 'kv40', 'kv100': 'kv100', 'VI': 'viscosity_index', 'flash': 'flash_point', 'pour': 'pour_point'}
    cosan = cosan_grid(ar.pages('DL2-11240.pdf')[0])
    f141 = next(f for f in F if f['id'] == 'CF-141')
    for v, grid in zip(f141['values'], (cat['6'], cosan['Ultra-S 6'], live['6'])):
        okv = True
        for k, val in re.findall(r'(kv40|kv100|VI|flash|pour) (-?[\d.]+)', v['value']):
            if first_num(grid.get(KEYS[k])) != float(val):
                okv = False
                so_fail.append(f'CF-141 {v["file"][:13]} {k}: recorded {val}, printed {grid.get(KEYS[k])}')
        if okv and v is not f141['values'][1]:
            verified.add(key(f141, v))
    extra = dict(re.findall(r'(Noack|Sp\.Gravity 15/4 °C) ([\d.]+)', f141['values'][1]['value']))
    if first_num(cosan['Ultra-S 6'].get('noack_volatility')) != float(extra['Noack']) or \
            first_num(cosan['Ultra-S 6'].get('specific_gravity')) != float(extra['Sp.Gravity 15/4 °C']):
        so_fail.append('CF-141 Cosan Noack / specific gravity')
    elif not any(x.startswith('CF-141 DL2-11240') for x in so_fail):
        verified.add(key(f141, f141['values'][1]))
    same48 = all(first_num(cosan[f'Ultra-S {g}'].get(k)) == first_num(cat[g].get(k)) for g in ('4', '8')
                 for k in ('specific_gravity', 'kv40', 'kv100', 'viscosity_index', 'flash_point', 'pour_point'))
    print('CF-141: three value sets checked in the Ultra-S 6 columns; Cosan sheet equals the catalog for Ultra-S 4 and 8:', same48)
    if not same48:
        so_fail.append('CF-141 claim "matches DL2-11177 exactly for Ultra-S 4 and 8" not confirmed')
    # CF-102: the web typical KV40 of aramcoULTRA 8 (the SDS range is read on DL2-14611.pdf p.2 by check_sources.py)
    f102 = next(f for f in F if f['id'] == 'CF-102')
    w102 = next(v for v in f102['values'] if str(v.get('file', '')).startswith('http'))
    ok102 = first_num(live_au['8'].get('kv40')) == first_num(w102['value'])
    print(f'CF-102: web aramcoULTRA 8 column, KV40 row prints {live_au["8"].get("kv40")}; recorded {w102["value"]}:', ok102)
    if ok102:
        verified.add(key(f102, w102))
    else:
        so_fail.append('CF-102 web value')
    for f in F:
        if f['supplier'] != 'S-OIL' or f['id'] == 'CF-141':
            continue
        arch = next((v for v in f['values'] if str(v.get('file')) == 'DL2-11177.pdf'), None)
        web = next((v for v in f['values'] if str(v.get('file', '')).startswith('http')), None)
        if not (arch and web):
            continue
        n_so += 1
        g = re.search(r'(\d)$', f['record_id']).group(1); prop = re.sub(r'^tier\d\.', '', f['property'])
        if not (first_num(cat[g].get(prop)) == first_num(arch['value']) and first_num(live[g].get(prop)) == first_num(web['value'])):
            so_fail.append(f"{f['id']} grade {g} {prop}: recorded {arch['value']} / {web['value']}; printed {cat[g].get(prop)} / {live[g].get(prop)}")
        else:
            verified.update({key(f, arch), key(f, web)})
    print(f'S-OIL: {n_so} catalog-vs-web findings checked in grade column and property row; mismatches {len(so_fail)}')
    fails += so_fail
    if live_au != live or wbg != live:
        fails.append('S-OIL web tables differ between brands or captures')
        verified = {k for k in verified if 's-oil.com' not in k}
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            json.dump(sorted(verified), fh, ensure_ascii=False, indent=1)
    print(f'citations verified by this check: {len(verified)}')
    for x in fails:
        print('FAIL', x)
    print('OVERALL:', 'PASS' if not fails else f'{len(fails)} failed')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
