"""Cross-document screen: does every other archive document that names a product and prints a property
also print the JSON value (in any equivalent form)? Candidates go to manual triage. Read-only."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

P = A.load_products(); ar = A.Archive()
DM = json.load(open(os.path.join(A.SCR, 'audit', 'docmap.json'), encoding='utf-8'))
DOC = json.load(open(os.path.join(A.SCR, 'audit', 'documented.json'), encoding='utf-8'))
LABEL = {
    'kv40': r'(?i)(visc[^\n]{0,60}40|40\s*°?\s*[C℃][^\n]{0,40}visc|kv\s*40|@\s*40)',
    'kv100': r'(?i)(visc[^\n]{0,60}100|100\s*°?\s*[C℃][^\n]{0,40}visc|kv\s*100|@\s*100)',
    'viscosity_index': r'(?i)viscosity\s*index|\bVI\b',
    'density': r'(?i)density|specific\s*gravity|relative\s*density',
    'flash_point': r'(?i)flash',
    'pour_point': r'(?i)pour',
    'noack_volatility': r'(?i)noack|evaporation\s*loss|volatility',
    'tbn': r'(?i)\bTBN\b|base\s*number',
    'sulfated_ash': r'(?i)sul(ph|f)ated\s*ash',
}


def forms(text):
    """All numbers in text, with decimal-comma and thousands-space readings both included."""
    t = str(text or '').replace('−', '-').replace('–', '-')
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+(?:[.,]\d+)?', t):
        s = m.group(0)
        for c in {s.replace(',', '.'), s.replace(',', '')}:
            try: out.add(round(float(c), 6))
            except ValueError: pass
    for m in re.finditer(r'(?<!\d)\d{1,3}(?: \d{3})+(?:[.,]\d+)?(?!\d)', t):
        try: out.add(round(float(m.group(0).replace(' ', '').replace(',', '.')), 6))
        except ValueError: pass
    return out


def equivalents(prop, v, unit):
    vs = {round(v, 6)}
    if prop == 'density': vs |= {round(v * 1000, 6), round(v / 1000, 6), round(v * 1000, 1), round(v / 1000, 4)}
    if prop in ('sulfur',): vs |= {round(v * 10000, 6), round(v / 10000, 6)}
    return vs


documented_values = collections.defaultdict(set)   # (folder, prop) -> numbers recorded in conflicts
for o in DOC:
    key = re.sub(r'^tier\d\.', '', str(o['property'])).split('[')[0].split(' ')[0]
    for v in o['values']:
        for x in forms(v.get('value')) | forms(v.get('printed_text')):
            documented_values[(o['folder'], key)].add(x)

docs_for = collections.defaultdict(set)
for k, v in DM.items():
    for f in set(v.get('names', [])) | set(v.get('cited_by', [])):
        if v.get('text'): docs_for[f].add(k)

cands = []; compared = collections.Counter()
for folder, p in P.items():
    for tk, t in p['tiers'].items():
        for path, n, _ in A.value_objects(t['doc'].get('fields', {})):
            prop = path.split('.')[-1].split('[')[0]
            if prop not in LABEL or path.count('.') or '[' in path: continue
            v = n.get('value') if isinstance(n.get('value'), (int, float)) and not isinstance(n.get('value'), bool) else None
            if v is None: v = n.get('min') if isinstance(n.get('min'), (int, float)) else n.get('max') if isinstance(n.get('max'), (int, float)) else None
            if v is None or n.get('status') not in ('Reported', 'Calculated'): continue
            cited = ar.key(A.src_of(n)[0] or '')
            eq = equivalents(prop, float(v), n.get('unit'))
            for ae in n.get('alternate_entries') or []:
                if isinstance(ae, dict) and isinstance(ae.get('value'), (int, float)): eq |= equivalents(prop, float(ae['value']), ae.get('unit'))
            for dk in sorted(docs_for[folder]):
                if dk == cited: continue
                e = ar.by_key.get(dk)
                if not e or not e.get('pages'): continue
                hits = [(i, l) for i, pg in enumerate(e['pages'], 1) for l in pg.splitlines() if re.search(LABEL[prop], l)]
                if not hits: continue
                compared[prop] += 1
                allnums = forms('\n'.join(e['pages']))
                if eq & allnums: continue
                if documented_values[(folder, prop)] & allnums and documented_values[(folder, prop)]:
                    continue  # the other value is already recorded in a documented conflict
                ctx = []
                for i, l in hits[:4]:
                    lines = e['pages'][i - 1].splitlines(); j = lines.index(l)
                    ctx.append(f"p.{i}: " + ' | '.join(x.strip() for x in lines[j:j + 4] if x.strip())[:220])
                cands.append(dict(folder=folder, record_id=p['record_id'], material_class=p['class'], tier=tk, file=t['file'], path=path,
                                  property=prop, json_value=v, unit=n.get('unit'), cited=A.src_of(n)[0], cited_page=A.src_of(n)[1],
                                  other_doc=e['path'].rsplit('/', 1)[-1], other_type=DM[dk].get('type'),
                                  other_names=len(DM[dk].get('names', [])), other_cited_by_product=folder in DM[dk].get('cited_by', []),
                                  context=ctx))
json.dump(cands, open(os.path.join(A.SCR, 'audit', 'crossdoc.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('property/document comparisons', sum(compared.values()), dict(compared))
print('candidates', len(cands), collections.Counter(c['property'] for c in cands))
print('by other-doc type', collections.Counter(c['other_type'] for c in cands), '| single-product docs', sum(1 for c in cands if c['other_names'] <= 1))
