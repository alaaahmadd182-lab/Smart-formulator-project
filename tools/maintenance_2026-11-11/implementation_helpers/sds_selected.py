import csv, json, os, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:\Users\windo\sf-wsA\tools\data_policy')
import policy_lib as P
cls = {(r['file'], r['page']): (r['class'], r['subclass']) for r in csv.DictReader(open(r'C:\Users\windo\sf-wsA\reports\data_policy\document_classes.csv', encoding='utf-8'))}
def c_of(f, pg):
    return cls.get((f, '' if pg is None else str(pg)), ('?', ''))
prods = P.load_products()
rows = []
for pid, p in prods.items():
    techfiles = set()
    for f, d in p['files'].items():
        for vp, n in P.value_objects(d.get('fields', {})):
            fl, pg, _ = P.src(n)
            if fl and c_of(fl, pg)[0] == 'TECHNICAL':
                techfiles.add(fl)
    for f, d in p['files'].items():
        conf = json.dumps(d.get('conflicts', []), ensure_ascii=False)
        for vp, n in P.value_objects(d.get('fields', {})):
            if n.get('status') not in ('Reported', 'Calculated'):
                continue
            fl, pg, _ = P.src(n)
            if not fl:
                continue
            c = c_of(fl, pg)
            if c[0] != 'SDS':
                continue
            alts = [(a.get('source') or {}).get('file') for a in n.get('alternate_entries') or []]
            alt_tech = [a for a in alts if a and any(c_of(a, x)[0] == 'TECHNICAL' for x in ([''] + [str(i) for i in range(1, 12)]))]
            top = vp.split('.')[0].split('[')[0]
            in_conf = top in conf
            rows.append((pid, f.split('/')[-1], vp, n.get('value'), n.get('unit'), fl, pg, bool(alt_tech), in_conf, sorted(techfiles)[:4]))
print('selected values from SDS pages:', len(rows))
print(collections.Counter(r[2].split('.')[0].split('[')[0] for r in rows))
for r in rows:
    print(r)
