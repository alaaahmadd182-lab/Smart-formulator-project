import json, os, re, sys, collections, zipfile
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
ROOT = r'C:\Users\windo\sf-wsA'
z = zipfile.ZipFile(os.path.join(ROOT, 'Manual + Data to share.zip'))
key = lambda n: re.sub(r'\s+', ' ', str(n).replace('\ufffd', '%').replace('%20', ' ').replace('%', '').lower().strip())
members = {key(os.path.basename(n)): n for n in z.namelist() if not n.endswith('/')}
# (file, page) pairs that select values
pairs = collections.Counter()
for dp, _, fs in os.walk(os.path.join(ROOT, 'Products_json')):
    for f in fs:
        if not f.endswith('.json'):
            continue
        d = json.load(open(os.path.join(dp, f), encoding='utf-8'))
        def rec(n):
            if isinstance(n, dict):
                if 'status' in n and 'value' in n and n.get('status') == 'Reported':
                    s = n.get('source')
                    if isinstance(s, dict) and s.get('file'):
                        pairs[(s['file'], s.get('page'))] += 1
                for k, v in n.items():
                    if k != 'source':
                        rec(v)
            elif isinstance(n, list):
                for v in n:
                    rec(v)
        rec(d.get('fields'))
SDS_HDR = re.compile(r'safety\s+data\s+sheet|material\s+safety|\bM?SDS\b|fiche de donn|sicherheitsdatenblatt', re.I)
SDS_SEC = re.compile(r'hazards?\s+identification|first[- ]aid measures|composition\s*/\s*information on ingredients|'
                     r'physical and chemical properties|fire[- ]?fighting measures|exposure controls', re.I)
TDS_SIG = re.compile(r'typical\s+(properties|characteristics|data|value|inspections|analysis)|product data sheet|technical data sheet|'
                     r'product information|test\s+method|typical', re.I)
cache = {}
def pages(f):
    m = members.get(key(f))
    if m is None:
        return None
    if m not in cache:
        cache[m] = [p.get_text() for p in pymupdf.open(stream=z.read(m), filetype='pdf')] if m.lower().endswith('.pdf') else []
    return cache[m]
out = collections.Counter(); detail = []
for (f, p), n in pairs.items():
    ps = pages(f)
    if ps is None:
        out['external'] += n; continue
    if not ps or not isinstance(p, int) or p < 1 or p > len(ps) or not ps[p - 1].strip():
        out['no text/image/page?'] += n; detail.append(('NOTEXT', f, p, n)); continue
    t = ps[p - 1]; first = ps[0]
    sds_page = bool(SDS_HDR.search(t)) and bool(SDS_SEC.search(t) or re.search(r'section\s*\d|revision|version', t, re.I))
    sds_file = bool(SDS_HDR.search(first)) and bool(SDS_SEC.search(' '.join(ps[:3])))
    tds_page = bool(TDS_SIG.search(t))
    if sds_page and not tds_page:
        c = 'SDS'
    elif sds_page and tds_page:
        c = 'SDS?TDS'
    elif sds_file:
        c = 'SDS-file page'
    else:
        c = 'TDS-class'
    out[c] += n; detail.append((c, f, p, n))
print(out)
for c, f, p, n in sorted(detail):
    if c in ('SDS?TDS', 'SDS-file page', 'NOTEXT'):
        print(c, f, p, n)
