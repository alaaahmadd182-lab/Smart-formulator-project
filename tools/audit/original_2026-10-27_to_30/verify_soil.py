"""Column-level verification of the S-OIL Ultra-S / aramcoULTRA edition-difference findings."""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

EV = os.path.join(A.REPO, 'reconciliation', 'audit_evidence')
GR = ['2', '3', '4', '6', '8']


def cells(t):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    t = html.unescape(re.sub(r'<[^>]+>', '|', t)); return [c.strip() for c in re.sub(r'\s*\|[\s|]*', '|', t).split('|') if c.strip()]


def web_table(path, brand):
    c = cells(open(path, encoding='utf-8', errors='replace').read())
    hdr = [i for i in range(len(c) - 6) if c[i] == 'ASTM' and c[i + 1] == f'{brand} 2']
    if not hdr: return None
    i = hdr[0] + 6; grid = {g: {} for g in GR}
    rows = {'Density @ 15.6℃, kg/L': 'density', 'Kinematic Viscosity @ 40℃, cSt': 'kv40', 'Kinematic Viscosity @ 100℃, cSt': 'kv100',
            'Viscosity Index': 'viscosity_index', 'Pour Point, ℃': 'pour_point', 'Noack Volatility, wt% (Procedure B)': 'noack_volatility'}
    while i < len(c) - 7 and not c[i].startswith(('aramcoULTRA base oil is', 'Ultra-S base oil is', 'S-OIL')):
        lab = c[i]; key = rows.get(lab) or ('flash_point' if lab.replace(' ', '').startswith('FlashPoint,COC') else None)
        if key:
            for g, v in zip(GR, c[i + 2:i + 7]): grid[g][key] = (v, c[i + 1], lab)
            i += 7
        else: i += 1
        if i - hdr[0] > 200: break
    return grid


def catalog():
    t = A.Archive().page_text('DL2-11177.pdf', 1); L = [l.strip() for l in t.splitlines() if l.strip()]
    s = L.index('Ultra-S 8'); grid = {g: {} for g in GR}
    def row(label, n=5):
        i = next(j for j in range(s, len(L)) if L[j].startswith(label)); return L[i:i + 2 + n]
    sg = row('Sp.Gravity'); [grid[g].__setitem__('specific_gravity', (v, sg[1], sg[0])) for g, v in zip(GR, sg[2:7])]
    i = next(j for j in range(s, len(L)) if L[j].startswith('Kin.Vis @40')); vals = L[i + 3:i + 13]
    for k, g in enumerate(GR):
        grid[g]['kv40'] = (vals[2 * k], 'D 445', 'Kin.Vis @40 °C, cSt'); grid[g]['kv100'] = (vals[2 * k + 1], 'D 445', '@100 °C, cSt')
    for label, key in (('Viscosity Index', 'viscosity_index'), ('Flash Point', 'flash_point'), ('Pour Point', 'pour_point')):
        r = row(label); [grid[g].__setitem__(key, (v, r[1], r[0])) for g, v in zip(GR, r[2:7])]
    return grid


cat = catalog()
live = web_table(os.path.join(EV, 'SOIL_LubeBaseOil_live_2026-10-30.html'), 'Ultra-S')
live_au = web_table(os.path.join(EV, 'SOIL_LubeBaseOil_live_2026-10-30.html'), 'aramcoULTRA')
wb = web_table(os.path.join(EV, 'SOIL_LubeBaseOil__wayback_20260610070302.html'), 'Ultra-S') or web_table(os.path.join(EV, 'SOIL_LubeBaseOil__wayback_20260610070302.html'), 'aramcoULTRA')
print('catalog', cat['6']); print('live Ultra-S', live['6']); print('live aramcoULTRA == live Ultra-S:', live_au == live); print('wayback 2026-06-10 == live:', wb == live)
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
num = lambda s: (re.findall(r'-?\d+(?:\.\d+)?', str(s).replace(',', '')) or [None])[0]
out = []
for f in F:
    if f['supplier'] != 'S-OIL' or f['source_kind'] != 'documented': continue
    g = re.search(r'(\d)$', f['record_id']).group(1); prop = re.sub(r'^tier\d\.', '', f['property'])
    a = next((v for v in f['values'] if not str(v.get('file', '')).startswith('http')), None)
    b = next((v for v in f['values'] if str(v.get('file', '')).startswith('http')), None)
    ca, cw = cat[g].get(prop), live[g].get(prop)
    ok_a = ca is not None and a is not None and float(num(ca[0])) == float(num(a['value'] if a.get('value') is not None else a.get('printed_text')))
    ok_b = cw is not None and b is not None and float(num(cw[0])) == float(num(b['value'] if b.get('value') is not None else b.get('printed_text')))
    out.append(dict(id=f['id'], record_id=f['record_id'], property=f['property'], grade=g, archive=(a.get('file') if a else None, a and a.get('value')), archive_cell=ca,
                    web=(b and b.get('value')), web_cell=cw, match_archive=ok_a, match_web=ok_b))
json.dump(dict(catalog=cat, live=live, findings=out, live_equals_wayback=wb == live, aramcoultra_equals_ultras=live_au == live),
          open(os.path.join(A.SCR, 'audit', 'verify_soil.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('S-OIL documented findings', len(out), '| archive column match', sum(o['match_archive'] for o in out), '| web column match', sum(o['match_web'] for o in out))
for o in out:
    if not (o['match_archive'] and o['match_web']): print('  CHECK', json.dumps(o, ensure_ascii=False)[:420])
