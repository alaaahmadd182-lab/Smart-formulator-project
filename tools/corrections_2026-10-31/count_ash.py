"""CF-144 count: selected Calculated sulfated-ash estimates vs historical Calculated alternates, at e6617ca and now."""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
LONG = '\\\\?\\'


def files_at(rev):
    names = subprocess.run(['git', 'ls-tree', '-r', '--name-only', rev, 'Products_json'], capture_output=True, text=True, encoding='utf-8').stdout.splitlines()
    for n in names:
        if n.endswith('.json'):
            yield n, json.loads(subprocess.run(['git', 'show', f'{rev}:{n}'], capture_output=True, text=True, encoding='utf-8').stdout)


def files_now():
    root = LONG + os.path.abspath('.')
    for dp, _, fs in os.walk(LONG + os.path.abspath('Products_json')):
        for f in fs:
            if f.endswith('.json'):
                p = os.path.join(dp, f)
                yield os.path.relpath(p, root).replace(os.sep, '/'), json.load(open(p, encoding='utf-8'))


for label, it in (('e6617ca', files_at('e6617ca')), ('working tree', files_now())):
    sel, alt, rep, factor = [], [], [], {}
    for n, d in it:
        sa = d.get('fields', {}).get('sulfated_ash')
        if not isinstance(sa, dict):
            continue
        prod = n.split('/')[-2]
        note = sa.get('calculation_note') or ''
        if sa.get('status') == 'Calculated':
            sel.append(prod)
            factor[prod] = '1.5 (+Mo, B)' if 'Mo' in note and '1.5' in note else '1.24'
        elif sa.get('status') == 'Reported':
            rep.append(prod)
        for a in sa.get('alternate_entries') or []:
            if a.get('status') == 'Calculated':
                alt.append(prod)
    print(f'{label}: selected Calculated sulfated_ash = {len(sel)} '
          f'(Zn 1.24: {sum(v == "1.24" for v in factor.values())}; Zn 1.5: {sorted(k for k, v in factor.items() if v != "1.24")}); '
          f'historical Calculated alternates = {len(alt)} {sorted(alt)}; Reported sulfated_ash = {len(rep)}')
