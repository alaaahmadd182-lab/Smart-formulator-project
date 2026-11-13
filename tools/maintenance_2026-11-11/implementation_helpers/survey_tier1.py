import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\windo\sf-wsA'
recs = collections.defaultdict(dict)
for dp, _, fs in os.walk(os.path.join(ROOT, 'Products_json')):
    for f in fs:
        if f.endswith('.json'):
            d = json.load(open(os.path.join(dp, f), encoding='utf-8'))
            recs[(d['material_class'], os.path.basename(dp))][(d['tier'], d.get('component_subtype'), f)] = d
print(collections.Counter(k[0] for k in recs))
print(collections.Counter((k[0], tuple(sorted((t, str(s)) for t, s, _ in v))) for k, v in recs.items()))


def st(n):
    if isinstance(n, dict):
        if 'status' in n and not isinstance(n['status'], dict):
            return n['status']
        return {k: st(v) for k, v in n.items() if k not in ('source', 'notes', 'basis')}
    if isinstance(n, list):
        return ['list', len(n)] + [st(x) for x in n[:1]]
    return None


agg = collections.defaultdict(collections.Counter)
for (cls, pid), tiers in recs.items():
    for (t, sub, f), d in tiers.items():
        if cls == 'additive_component':
            key = f'{cls}:{sub or "general"}'
        elif t != 1:
            continue
        else:
            key = cls
        for k, v in d['fields'].items():
            agg[(key, k)][json.dumps(st(v), ensure_ascii=False)[:170]] += 1
for k in sorted(agg):
    print('==', k)
    for s, n in agg[k].most_common(5):
        print('   ', n, s)
