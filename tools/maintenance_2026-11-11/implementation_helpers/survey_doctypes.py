import json, os, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\windo\sf-wsA'
dt = collections.Counter(); files_by_type = collections.defaultdict(set); sel_src = collections.Counter()
alt = collections.Counter(); per_file_types = collections.defaultdict(set)
n_vo = 0
for dp, _, fs in os.walk(os.path.join(ROOT, 'Products_json')):
    for f in fs:
        if not f.endswith('.json'):
            continue
        d = json.load(open(os.path.join(dp, f), encoding='utf-8'))
        sd = {}
        for s in d.get('source_documents') or []:
            t = str(s.get('doc_type')); dt[t] += 1
            files_by_type[t].add(s.get('file'))
            per_file_types[s.get('file')].add(t)
            sd[s.get('file')] = t

        def rec(n):
            global n_vo
            if isinstance(n, dict):
                if 'status' in n and 'value' in n and not isinstance(n['status'], dict):
                    n_vo += 1
                    src = n.get('source') or {}
                    fl = src.get('file') if isinstance(src, dict) else None
                    if n.get('status') in ('Reported',):
                        sel_src[sd.get(fl, 'NOT IN source_documents' if fl else 'no file')] += 1
                    for a in n.get('alternate_entries') or []:
                        s2 = a.get('source') or {}
                        alt[sd.get(s2.get('file') if isinstance(s2, dict) else None, '?')] += 1
                for k, v in n.items():
                    if k != 'source':
                        rec(v)
            elif isinstance(n, list):
                for v in n:
                    rec(v)
        rec(d.get('fields'))
print('value objects', n_vo)
print('doc_type vocabulary:')
for t, n in dt.most_common():
    print(f'  {n:4d}  {t}')
print('selected Reported values by source doc_type:')
for t, n in sel_src.most_common(30):
    print(f'  {n:5d}  {t}')
print('alternate entries by doc_type:', alt.most_common(15))
multi = {f: t for f, t in per_file_types.items() if len(t) > 1}
print('files with more than one doc_type label:', len(multi), list(multi.items())[:8])
