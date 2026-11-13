"""Confirm the S_OIL_ARAMCO_ULTRA_8 values taken from the saved S-OIL manufacturer table (read-only).

The S-OIL "Lube Base Oil" page is saved twice in reconciliation/audit_evidence/ (an Internet Archive capture of
2026-06-10 and the live page of 2026-10-30; SHA-256 in evidence_manifest.md). A capture or retrieval date is not a
publication or revision date: the page prints none, so its edition date is unknown.

For each checked property the tool reads, in BOTH saved copies:
  table      the table whose caption starts 'Typical Properties of aramcoULTRA Base Oil' (the typical qualifier)
  column     the header cell 'aramcoULTRA 8' (the product)
  row        the row label as printed (property, unit, temperature, and the cup type for flash point)
  ASTM       the method cell of the row
and compares the printed cell, unit, temperature and method with the product record. Exit 1 on any mismatch.

Usage: python tools/data_policy/verify_soil_table.py
"""
import hashlib, html, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P  # noqa: E402

URL = 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx'
COPIES = {  # saved copy -> SHA-256 recorded in reconciliation/audit_evidence/evidence_manifest.md
    'reconciliation/audit_evidence/SOIL_LubeBaseOil__wayback_20260610070302.html': 'cff0d3bbb7964c7450a1b9fa813617bf76e4b09de39187d026f674c7604fda60',
    'reconciliation/audit_evidence/SOIL_LubeBaseOil_live_2026-10-30.html': '94b263ad23cfd8b9631b5b637635c0cbdb341aad25cb7553a2a44513f10f011c',
}
CAPTION = 'Typical Properties of aramcoULTRA Base Oil'
PRODUCT, COLUMN = 'S_OIL_ARAMCO_ULTRA_8', 'aramcoULTRA 8'
# field -> (row label exactly as printed, ASTM cell, printed cell, value, unit, test temperature, record method)
EXPECTED = {
    'kv40': ('Kinematic Viscosity @ 40℃, cSt', 'D445', '41.10', 41.1, 'cSt', 40, 'ASTM D445'),
    'kv100': ('Kinematic Viscosity @ 100℃, cSt', 'D445', '7.1', 7.1, 'cSt', 100, 'ASTM D445'),
    'flash_point': ('Flash Point,COC ,℃', 'D92', '250', 250, '°C', None, 'ASTM D92'),
}


def cell_text(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', x))).strip()


def read_table(path):
    """(sha256, caption, header, {row label: cells}) of the aramcoULTRA typical-properties table in one saved copy."""
    with open(os.path.join(P.ROOT, path), 'rb') as fh:
        raw = fh.read()
    text = raw.decode('utf-8', errors='replace')
    for tb in re.findall(r'<table.*?</table>', text, re.S):
        cap = [cell_text(c) for c in re.findall(r'<caption[^>]*>(.*?)</caption>', tb, re.S)]
        rows = [[cell_text(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', tr, re.S)] for tr in re.findall(r'<tr.*?</tr>', tb, re.S)]
        if cap and cap[0].startswith(CAPTION) and rows and COLUMN in rows[0]:
            return hashlib.sha256(raw).hexdigest(), cap[0], rows[0], {r[0]: r for r in rows[1:] if r}
    return hashlib.sha256(raw).hexdigest(), None, None, {}


def record_field(prods, prop):
    for d in prods[PRODUCT]['files'].values():
        if prop in (d.get('fields') or {}):
            return d['fields'][prop]
    return None


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    prods = P.load_products()
    errors = []
    for path, want in COPIES.items():
        sha, cap, header, rows = read_table(path)
        print(f'{path}\n  SHA-256 {sha} ({"matches the manifest" if sha == want else "DIFFERS from the manifest"})')
        if sha != want:
            errors.append(f'{path}: hash differs')
        if not header:
            errors.append(f'{path}: table not found'); continue
        j = header.index(COLUMN)
        print(f'  caption: {cap}\n  header: {header}')
        for prop, (label, astm, printed, value, unit, temp, method) in EXPECTED.items():
            r = rows.get(label)
            if not r:
                errors.append(f'{path}: row {label!r} not found'); continue
            print(f'  {prop}: row {r[0]!r} | ASTM {r[1]!r} | column {COLUMN!r}: {r[j]!r}')
            if (r[1], r[j]) != (astm, printed):
                errors.append(f'{path} {prop}: printed {r[1]!r} / {r[j]!r}, expected {astm!r} / {printed!r}')
    print('record (selected values):')
    for prop, (label, astm, printed, value, unit, temp, method) in EXPECTED.items():
        n = record_field(prods, prop) or {}
        got = (n.get('value'), n.get('unit'), n.get('test_temperature_c'), n.get('method'), n.get('value_kind'), (n.get('source') or {}).get('file'))
        ok = got == (value, unit, temp, method, 'typical', URL) and printed in (n.get('printed_text') or '')
        print(f'  {prop}: value {got[0]!r} {got[1]!r} at {got[2]!r} °C, {got[3]!r}, {got[4]!r}, source {got[5]!r}: {"agrees with the table" if ok else "DOES NOT hold the table value"}')
        if not ok:
            errors.append(f'record {prop}: does not hold the table value')
    print('edition date of the page: not printed (unknown); capture and retrieval dates are not publication dates')
    for e in errors:
        print('ERROR', e)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
