"""Context-level recheck of every archive value in the findings (excluding the Petro-Canada and S-OIL edition groups,
which are verified column by column in verify_pc.py / verify_soil.py). Writes audit/recheck.json and a review listing."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A
from audit_docmap import aliases, pattern  # noqa: E402

ar = A.Archive(); P = A.load_products()
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
LABEL = {'kv40': r'(?i)visc|40', 'kv100': r'(?i)visc|100', 'viscosity_index': r'(?i)viscosity index|\bVI\b', 'density': r'(?i)densit|gravity',
         'flash_point': r'(?i)flash', 'pour_point': r'(?i)pour', 'noack_volatility': r'(?i)noack|volatil', 'tbn': r'(?i)base number|TBN',
         'sulfated_ash': r'(?i)ash', 'sulfur': r'(?i)sul(f|ph)ur', 'treat_rate': r'(?i)treat|%', 'elements.Zn': r'(?i)zn|zinc', 'elements.Ca': r'(?i)ca\b|calcium'}


def fnums(s):
    t = str(s or '').replace('−', '-').replace('–', '-')
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+(?:[.,]\d+)?', t):
        for c in {m.group(0).replace(',', '.'), m.group(0).replace(',', '')}:
            try: out.add(round(float(c), 6))
            except ValueError: pass
    return out


def prop_key(prop):
    p = re.sub(r'^tier\d\.', '', prop).split(' ')[0].split(';')[0].split(',')[0]
    return next((k for k in LABEL if p.startswith(k)), None)


rows = []
for f in F:
    if f['source_kind'] == 'documented' and (f['record_id'].startswith('PETRO_CANADA_PURITY_') or f['supplier'] == 'S-OIL'): continue
    folder = next(k for k, p in P.items() if p['record_id'] == f['record_id'])
    name_rx = [pattern(a) for a in aliases(P[folder]) if pattern(a)]
    pk = prop_key(f['property'])
    for i, v in enumerate(f['values']):
        fn = str(v.get('file') or '').split(';')[0].split(' (')[0].strip()
        e = ar.get(fn) if fn and not fn.startswith('http') else None
        r = dict(id=f['id'], record_id=f['record_id'], property=f['property'], vi=i, file=fn, page=v.get('page'), value=v.get('value'),
                 unit=v.get('unit'), rev=v.get('revision_date'), printed=v.get('printed_text'), check=v.get('source_check'))
        if not e:
            r['state'] = 'external or no file'; rows.append(r); continue
        if not e.get('chars'):
            r['state'] = 'image-only'; rows.append(r); continue
        doc = '\n'.join(e['pages']); pages = [int(x) for x in re.findall(r'\d+', str(v.get('page') or ''))] or list(range(1, len(e['pages']) + 1))
        txt = '\n'.join(e['pages'][p - 1] for p in pages if 1 <= p <= len(e['pages']))
        L = [l.strip() for l in txt.splitlines() if l.strip()]
        want = fnums(v.get('value')) or fnums(v.get('printed_text'))
        hits = [j for j, l in enumerate(L) if fnums(l) & want] if want else []
        ctx = [' | '.join(L[max(0, j - 2):j + 2]) for j in hits[:3]]
        r.update(state='text', product_in_doc=any(rx.search(doc) for rx in name_rx), product_on_page=any(rx.search(txt) for rx in name_rx),
                 value_on_page=bool(hits), label_near=bool(pk and any(re.search(LABEL[pk], ' '.join(L[max(0, j - 3):j + 2])) for j in hits)),
                 unit_near=bool(v.get('unit') and any(str(v['unit']).split(' ')[0].lower().replace('³', '3') in ' '.join(L[max(0, j - 3):j + 2]).lower().replace('³', '3') for j in hits)),
                 rev_in_doc=(None if not v.get('revision_date') else bool(set(re.findall(r'\d{2,4}', str(v['revision_date']))) <= set(re.findall(r'\d{2,4}', doc)))),
                 context=ctx)
        rows.append(r)
json.dump(rows, open(os.path.join(A.SCR, 'audit', 'recheck.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
import collections
print('values checked', len(rows), collections.Counter(r['state'] for r in rows))
t = [r for r in rows if r['state'] == 'text']
for k in ('product_in_doc', 'product_on_page', 'value_on_page', 'label_near', 'unit_near'):
    print(f'{k}: {sum(1 for r in t if r.get(k))}/{len(t)}')
print('rev_in_doc false:', [(r['id'], r['file'], r['rev']) for r in t if r.get('rev_in_doc') is False])
