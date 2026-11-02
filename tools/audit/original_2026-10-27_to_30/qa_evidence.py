"""QA: re-check every value of every finding against its cited archive page (read-only)."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

ar = A.Archive()
F = json.load(open(os.path.join(A.SCR, 'audit', 'findings.json'), encoding='utf-8'))
COMMON = re.compile(r'(?i)\b(the|and|of|for|with|product|data|value|density|viscosity|point|test|method|typical)\b')


def forms(text):
    t = str(text or '').replace('−', '-').replace('–', '-').replace('≥', ' ').replace('＞', ' ')
    out = set()
    for m in re.finditer(r'(?<![\w.])-?\d+(?:[.,]\d+)?', t):
        s = m.group(0)
        for c in {s.replace(',', '.'), s.replace(',', '')}:
            try: out.add(round(float(c), 6))
            except ValueError: pass
    for m in re.finditer(r'(?<!\d)\d{1,3}(?: \d{3})+(?:[.,]\d+)?(?!\d)', t):
        out.add(round(float(m.group(0).replace(' ', '').replace(',', '.')), 6))
    return out


def pages_of(pg):
    if isinstance(pg, int): return [pg]
    return [int(x) for x in re.findall(r'\d+', str(pg or ''))]


res = []
for f in F:
    for i, v in enumerate(f['values']):
        files = [x.strip() for x in re.split(r';|\(=', str(v.get('file') or '')) if x.strip() and not x.strip().startswith(('http', 'byte'))]
        files = [re.sub(r'\s*\(.*$', '', x) for x in files]
        if not files:
            res.append((f['id'], i, 'no archive file', v.get('source_check'))); continue
        want = forms(v.get('value')) if v.get('value') is not None else set()
        if not want and v.get('printed_text'): want = forms(v['printed_text'])
        for fn in files:
            e = ar.get(fn)
            if e is None: res.append((f['id'], i, f'{fn}: not in archive', v.get('source_check'))); continue
            pgs = pages_of(v.get('page'))
            texts = [(p, ar.page_text(fn, p) or '') for p in pgs] if pgs else list(enumerate(e.get('pages') or [], 1))
            if not e.get('chars'):
                res.append((f['id'], i, f'{fn}: image-only document', v.get('source_check'))); continue
            readable = [(p, t) for p, t in texts if len(t.strip()) > 40 and (len(COMMON.findall(t)) >= 2 or len(t) < 200)]
            if not readable:
                res.append((f['id'], i, f'{fn} p.{v.get("page")}: page has no usable text layer', v.get('source_check'))); continue
            found = set().union(*(forms(t) for _, t in readable))
            if not want:
                res.append((f['id'], i, f'{fn}: no numeric value to check', v.get('source_check'))); continue
            hit = want & found
            # every numeric token of the value should appear (values like "kv40 1649.0; kv100 156.0" carry several)
            core = {x for x in want if abs(x) not in (40.0, 100.0, 15.0, 20.0)} or want
            status = 'ALL found' if core <= found else ('SOME found' if hit else 'NOT found')
            res.append((f['id'], i, f'{fn} p.{v.get("page")}: {status}' + ('' if status == 'ALL found' else f' missing {sorted(core - found)[:6]}'), v.get('source_check')))
json.dump(res, open(os.path.join(A.SCR, 'audit', 'qa_evidence.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
c = collections.Counter(r[2].split(': ')[-1].split(' missing')[0] if ': ' in r[2] else r[2] for r in res)
print(c.most_common())
byid = {f['id']: f for f in F}
for r in res:
    if re.search(r'NOT found|SOME found|no usable|image-only|not in archive', r[2]):
        f = byid[r[0]]
        print(r[0], f['record_id'], f['property'][:40], '|', r[2], '| claimed:', f['verification'][:70], '| value check was:', r[3])
