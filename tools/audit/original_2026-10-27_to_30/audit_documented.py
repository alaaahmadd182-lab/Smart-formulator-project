"""Normalise every documented JSON conflict entry and check each value against its cited source page."""
import json, re, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

DOC_PATTERNS = [('SDS', r'safety data sheet|material safety|\bsds\b|section\s*1\b.*identification|hazards identification'),
                ('COA', r'certificate of analysis|\bcoa\b'),
                ('TDS/PDS', r'typical|product data|technical data|product information|typical properties|typical characteristics'),
                ('Specification', r'\bspecification\b|guaranteed|sales specification')]


def doc_type(ar, name, page=None):
    """Type of the cited page (a TDS that mentions 'safety data sheet' in its footer is not an SDS)."""
    if not name: return 'unknown'
    if str(name).startswith('http'): return 'external web/PDF'
    e = ar.get(name)
    if e is None: return 'not in archive'
    pages = e.get('pages') or []
    if not e.get('chars'): return 'image-only (type not machine-readable)'
    # An SDS states it in its title block and is organised in numbered sections; a TDS may only mention an SDS in a footer.
    first = (pages[0] if pages else '').lower()
    whole = '\n'.join(pages).lower()
    sections = len(set(re.findall(r'section\s*(\d{1,2})\b', whole)))
    if 'safety data sheet' in first[:400] or 'material safety data sheet' in first[:400] or sections >= 5 or 'hazards identification' in whole:
        return 'SDS'
    t = ar.page_text(name, page) if isinstance(page, int) else None
    low = (t if t and t.strip() else '\n'.join(pages)).lower()
    if 'certificate of analysis' in low: return 'COA'
    if re.search(r'typical|product data|technical data|product information|characteristics', low): return 'TDS/PDS'
    if re.search(r'\bspecification\b|guaranteed', low): return 'Specification'
    return 'other'


def norm_entry(c):
    """-> (property, [values], note, conflict_type, resolved, final_resolution)"""
    if isinstance(c, str):
        return ('viscosity_index' if 'Viscosity index' in c else '(text)'), [], c, None, None, None
    prop = c.get('field') or c.get('property') or '(unnamed)'
    vals = []
    def add(value=None, printed=None, file=None, page=None, rev=None, unit=None, temp=None, label=None):
        vals.append(dict(value=value, printed_text=printed, file=file, page=page, revision_date=rev, unit=unit,
                         temperature_c=temp, label=label))
    if isinstance(c.get('values'), list):
        for v in c['values']:
            add(v.get('value'), v.get('printed_text'), v.get('file') or v.get('source_file'), v.get('page'), v.get('revision_date'))
    for a, b in (('primary', 'alternate'), ('tds', 'sds')):
        for k in (a, b):
            v = c.get(k)
            if isinstance(v, dict):
                add(v.get('value'), v.get('printed_text'), v.get('source_file') or v.get('file'), v.get('page'), v.get('revision_date'),
                    v.get('unit'), v.get('temperature_c'), k)
    if 'primary_value' in c:
        add(c.get('primary_value'), None, c.get('primary_source'), None, None, label='primary')
        cv = str(c.get('comparison_value') or ''); m = re.search(r'page\s*(\d+)', cv)
        add(c.get('comparison_value'), None, c.get('comparison_source'), int(m.group(1)) if m else None, label='comparison')
    for k in ('a', 'b'):
        sv, vv = c.get(f'source_{k}'), c.get(f'value_{k}')
        if isinstance(sv, dict):
            add(sv.get('value'), None, sv.get('file'), sv.get('page'), label=f'source_{k}')
        elif sv or vv:
            m = re.match(r'(\S+)\s*(?:p\.?\s*(\d+))?\s*(?:\(([^)]*)\))?', str(sv or ''))
            add(vv, None, m.group(1) if m else sv, int(m.group(2)) if m and m.group(2) else None, m.group(3) if m else None, label=f'source_{k}')
    if isinstance(c.get('sources'), list) and not vals:
        for s in c['sources']:
            add(None, s.get('printed_text'), s.get('file'), s.get('page'))
    note = c.get('note') or c.get('description') or c.get('assessment') or c.get('resolution')
    return prop, vals, note, c.get('conflict_type'), c.get('resolved'), c.get('final_resolution')


def check_value_on_page(ar, v):
    f, pg = v.get('file'), v.get('page')
    if not f: return 'no source recorded'
    if str(f).startswith('http'): return 'external source (not in archive)'
    e = ar.get(f)
    if e is None: return 'file not in archive'
    if not e.get('chars'): return 'image-only document (visual check needed)'
    texts = [ar.page_text(f, pg)] if isinstance(pg, int) else e['pages']
    texts = [t for t in texts if t]
    if not texts: return 'cited page not in document'
    if isinstance(pg, int) and not texts[0].strip(): return 'cited page has no text layer (visual check needed)'
    cand = []
    pt = v.get('printed_text')
    nums = A.numbers(pt) if pt else []
    if isinstance(v.get('value'), (int, float)) and not isinstance(v.get('value'), bool): nums = [v['value']] + nums
    elif v.get('value') is not None and not nums: nums = A.numbers(v['value'])
    blob = ' '.join(texts)
    found_nums = set(A.numbers(blob))
    if pt:
        key = re.sub(r'\s+', '', str(pt).lower())[:40]
        if key and key in re.sub(r'\s+', '', blob.lower()): return 'verified: printed text found on cited page' if isinstance(pg, int) else 'verified: printed text found in document'
    if nums:
        hit = [n for n in nums[:1] if any(abs(n - x) < 1e-9 for x in found_nums)]
        if hit: return ('verified: value found on cited page' if isinstance(pg, int) else 'verified: value found in document (page not recorded)')
        return 'value NOT found on cited page' if isinstance(pg, int) else 'value not found in document'
    return 'text value (manual check)'


def run():
    P = A.load_products(); ar = A.Archive()
    groups = collections.OrderedDict()
    for folder, p in P.items():
        for tk, t in p['tiers'].items():
            for i, c in enumerate(t['doc'].get('conflicts', [])):
                body = {k: v for k, v in c.items() if k not in ('resolved', 'final_resolution')} if isinstance(c, dict) else c
                sig = (folder, json.dumps(body, ensure_ascii=False, sort_keys=True))
                g = groups.setdefault(sig, {'folder': folder, 'entry': c, 'locations': []})
                g['locations'].append(f"{t['file']}#conflicts[{i}]")
    out = []
    for (folder, _), g in groups.items():
        p = P[folder]; prop, vals, note, ctype, resolved, finalres = norm_entry(g['entry'])
        for v in vals:
            v['doc_type'] = doc_type(ar, v.get('file'), v.get('page'))
            v['source_check'] = check_value_on_page(ar, v)
        out.append(dict(folder=folder, record_id=p['record_id'], material_class=p['class'], property=prop, values=vals, note=note,
                        conflict_type=ctype, resolved=resolved, final_resolution=finalres, locations=g['locations'], raw=g['entry']))
    json.dump(out, open(os.path.join(A.SCR, 'audit', 'documented.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('unique documented conflicts', len(out), 'from entries', sum(len(g['locations']) for g in groups.values()))
    print(collections.Counter(o['conflict_type'] for o in out))
    print('resolved', collections.Counter(str(o['resolved']) for o in out))
    print('source checks', collections.Counter(v['source_check'].split(':')[0] for o in out for v in o['values']))
    print('values per entry', collections.Counter(len(o['values']) for o in out))
    print('doc type pairs', collections.Counter(' vs '.join(sorted({v['doc_type'] for v in o['values']})) for o in out).most_common(12))


if __name__ == '__main__':
    run()
