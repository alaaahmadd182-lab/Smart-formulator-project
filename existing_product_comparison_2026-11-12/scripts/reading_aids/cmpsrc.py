"""Reading aid (read-only): for each (product_id, file) print every JSON entry that cites the file (path, value,
printed_text, page) and the FULL text of the cited pages plus every page that contains section-9 / typical-property
headings. Usage: python cmpsrc.py PID|FILE [PID|FILE ...]"""
# Saved from the session scratchpad on 2026-11-13 (thirteenth pass). Runs from any directory: it changes to the
# workspace root (the folder that holds Products_json and existing_product_comparison_2026-11-12).
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import gzip, glob, json, os, re, sys
INV = 'incoming_dataset_review_2026-11-12'
ref = json.load(open(f'{INV}/_cache/reference.json', encoding='utf-8'))
mem = {m['name'].split('/')[-1]: m for m in ref['archive']['members']}
HEAD = re.compile(r'(?i)SECTION\s*9|PHYSICAL AND CHEMICAL|Typical (Properties|Characteristics|Inspections|Value)|Technical (Data|Specification)|Specifications')


def entries(pid, f):
    out = []
    for jf in sorted(glob.glob(f'Products_json/**/{pid}/*.json', recursive=True)):
        d = json.load(open(jf, encoding='utf-8'))

        def walk(k, v):
            if isinstance(v, dict):
                src = v.get('source') if isinstance(v.get('source'), dict) else {}
                if src.get('file') in (f, f.replace('%20', ' ')):
                    out.append((os.path.basename(jf)[:28], k, v.get('value'), v.get('qualifier'), v.get('min'), v.get('max'), v.get('unit'), v.get('test_temperature_c'), v.get('method'), src.get('page'), str(v.get('printed_text'))[:110]))
                for a, b in v.items():
                    if a != 'source':
                        walk(k + '.' + a if k else a, b)
            elif isinstance(v, list):
                for i, b in enumerate(v):
                    walk(f'{k}[{i}]', b)
        walk('', d['fields'])
        for q in d.get('open_questions', []) + d.get('conflicts', []):
            s = json.dumps(q, ensure_ascii=False)
            if f in s or f.replace('%20', ' ') in s:
                out.append((os.path.basename(jf)[:28], 'OQ/CONFLICT', s[:260]))
    return out


for arg in sys.argv[1:]:
    pid, f = arg.split('|')
    print('=' * 100, '\n', pid, f)
    seen = set()
    E = entries(pid, f)
    for e in E:
        if e not in seen:
            seen.add(e); print('  JSON', e)
    m = mem.get(f) or mem.get(f.replace('%20', ' '))
    p = f'{INV}/_cache/ref_text/{m["sha256"]}.txt.gz' if m else None
    if not p or not os.path.exists(p):
        print('  NO TEXT LAYER (visual review needed)'); continue
    pages = gzip.open(p, 'rt', encoding='utf-8').read().split('\f')
    want = {e[9] for e in E if len(e) > 9 and isinstance(e[9], int)} | {i + 1 for i, t in enumerate(pages) if HEAD.search(t)}
    want |= {i + 2 for i, t in enumerate(pages) if re.search(r'(?i)SECTION\s*9', t)}
    allv = []
    for jf in sorted(glob.glob(f'Products_json/**/{pid}/*.json', recursive=True)):
        d = json.load(open(jf, encoding='utf-8'))
        for k, v in d['fields'].items():
            vs = v if isinstance(v, list) else [v]
            for x in vs:
                if isinstance(x, dict) and x.get('status') not in (None, 'Missing') and 'value' in x:
                    allv.append(f"{k}={x.get('value')}[{x.get('min')}-{x.get('max')}]{x.get('qualifier') or ''} T{x.get('test_temperature_c')} {x.get('method') or ''} <{(x.get('source') or {}).get('file')}>")
    print('  ALL JSON:', ' ; '.join(allv))
    print(f'  pages={len(pages)}; printing pages {sorted(want)} in full')
    for i in sorted(want):
        if 1 <= i <= len(pages):
            print(f'  --- p.{i} ---', re.sub(r'\s+', ' ', pages[i - 1]))
