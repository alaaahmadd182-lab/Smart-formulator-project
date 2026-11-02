"""Map every archive document to the JSON products it names (read-only). Writes audit/docmap.json."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

P = A.load_products(); ar = A.Archive()


def name_of(p):
    for t in p['tiers'].values():
        n = (t['doc'].get('product') or {}).get('product_name')
        if n: return n
    return p['record_id']


def pattern(name):
    """Regex for a product name: case-insensitive, flexible spaces/hyphens, not followed by + or another digit/letter."""
    n = re.sub(r'[®™]', '', str(name)).strip()
    n = re.sub(r'\s*\(.*?\)\s*', ' ', n).strip()
    toks = [re.escape(t) for t in re.split(r'[\s\-_]+', n) if t]
    if not toks: return None
    return re.compile(r'(?<![\w+])' + r'[\s\-_®™]*'.join(toks) + r'(?![\w+]|\s*\+|\s*plus\b)', re.I)


cited = collections.defaultdict(set)   # archive key -> products citing it
for folder, p in P.items():
    for t in p['tiers'].values():
        d = t['doc']
        for path, n, _ in A.value_objects(d.get('fields', {})):
            f = A.src_of(n)[0]
            if f and not str(f).startswith('http'): cited[ar.key(f)].add(folder)
        sf = (d.get('product') or {}).get('source_file')
        for x in (sf if isinstance(sf, list) else [sf]):
            if x and not str(x).startswith('http'): cited[ar.key(x)].add(folder)
        for sd in d.get('source_documents') or []:
            if isinstance(sd, dict) and sd.get('file') and not str(sd['file']).startswith('http'): cited[ar.key(sd['file'])].add(folder)

pats = {folder: pattern(name_of(p)) for folder, p in P.items()}
GENERIC = r'\b(base\s*oils?|base\s*stocks?|basestocks?|base\s*fluid|lubricant\s*additive|additive)\b'
SUPPLIER_WORDS = r'^(chevron|petro[- ]?canada|exxonmobil|exxon\s*mobil|mobil|shell|nynas|neste|petronas|s-oil|sk|adnoc|aramco|bapco|ergon|formosa|fpcc)\b'


def aliases(p):
    n = re.sub(r'[®™]', '', str(name_of(p))).strip()
    core = re.sub(GENERIC, '', n, flags=re.I).strip()
    return {a for a in (n, core, re.sub(SUPPLIER_WORDS, '', core, flags=re.I).strip()) if a}


def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())


apats = {folder: [(a, pattern(a)) for a in aliases(p)] for folder, p in P.items()}
docmap = {}
for key, e in ar.by_key.items():
    if not key.endswith('.pdf'):
        docmap[key] = dict(path=e['path'], text=False, cited_by=sorted(cited.get(key, ())), names=[])
        continue
    text = '\n'.join(e.get('pages') or [])
    arch_sup = norm(e['path'].split('/')[-2])
    hits = []
    for f, lst in apats.items():
        same_sup = norm(P[f]['supplier_folder'])[:6] == arch_sup[:6]
        for a, rx in lst:
            short = len(norm(a)) < 6 or not re.search(r'[a-z]{3}', a.lower())
            if rx and text and (same_sup or not short) and rx.search(text):
                hits.append(f); break
    low = text.lower()
    typ = ('SDS' if re.search(r'safety data sheet|material safety data|hazards? identification', low[:8000]) else
           'COA' if 'certificate of analysis' in low else
           'TDS/PDS' if re.search(r'typical|product data|technical data|product information', low) else
           'Specification' if 'specification' in low else ('image-only' if not text.strip() else 'other'))
    docmap[key] = dict(path=e['path'], text=bool(e.get('chars')), type=typ, cited_by=sorted(cited.get(key, ())), names=hits)
json.dump(docmap, open(os.path.join(A.SCR, 'audit', 'docmap.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
unc = {k: v for k, v in docmap.items() if not v['cited_by']}
print('documents', len(docmap), '| uncited', len(unc))
print('uncited by type', collections.Counter(v.get('type') for v in unc.values()))
print('uncited text docs naming exactly one product', sum(1 for v in unc.values() if len(v['names']) == 1),
      '| several', sum(1 for v in unc.values() if len(v['names']) > 1), '| none', sum(1 for v in unc.values() if v['text'] and not v['names']))
print('cited docs whose text does not name any citing product:',
      sum(1 for v in docmap.values() if v['cited_by'] and v['text'] and not set(v['names']) & set(v['cited_by'])))
for k, v in list(unc.items()):
    if v['text'] and not v['names']: print('   unmapped uncited:', k, v.get('type'), v['path'][-70:])
