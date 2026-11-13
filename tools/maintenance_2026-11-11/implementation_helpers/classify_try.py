import json, os, re, sys, collections, zipfile
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf
ROOT = r'C:\Users\windo\sf-wsA'
z = zipfile.ZipFile(os.path.join(ROOT, 'Manual + Data to share.zip'))
key = lambda n: re.sub(r'\s+', ' ', str(n).replace('\ufffd', '%').replace('%20', ' ').replace('%', '').lower().strip())
members = {key(os.path.basename(n)): n for n in z.namelist() if not n.endswith('/')}
cited = collections.Counter()
for dp, _, fs in os.walk(os.path.join(ROOT, 'Products_json')):
    for f in fs:
        if f.endswith('.json'):
            t = open(os.path.join(dp, f), encoding='utf-8').read()
            for m in re.findall(r'"file":\s*"([^"]+)"', t):
                cited[m] += 1
            for m in re.findall(r'(DL2-\d{5}\.(?:pdf|PDF|jpe?g))', t):
                cited[m] += 0
arch = {f for f in cited if key(f) in members}
other = {f for f in cited if key(f) not in members}
print('cited files', len(cited), 'in archive', len(arch), 'other', len(other))
print('other:', sorted(other)[:20])
SDS = re.compile(r'safety data sheet|material safety data|hazards? identification|section\s*1\b|according to regulation \(ec\)|ghs', re.I)
TYP = re.compile(r'typical (properties|characteristics|data|value|inspections)|product data sheet|technical data sheet|product information', re.I)
SPEC = re.compile(r'specification|guaranteed|\bmin\b|\bmax\b', re.I)
BUL = re.compile(r'bulletin|performance (benefits|comparison)|key performance', re.I)
COA = re.compile(r'certificate of analysis|\bC\.?O\.?A\b|batch no', re.I)
res = {}
for f in sorted(arch):
    m = members[key(f)]
    if not m.lower().endswith('.pdf'):
        res[f] = ('image', ''); continue
    d = pymupdf.open(stream=z.read(m), filetype='pdf')
    t = ' '.join(p.get_text() for p in d)[:20000]
    if len(t.strip()) < 50:
        res[f] = ('no text', f'{len(d)} pages'); continue
    sig = [n for n, r in (('SDS', SDS), ('TYP', TYP), ('SPEC', SPEC), ('BUL', BUL), ('COA', COA)) if r.search(t)]
    res[f] = ('/'.join(sig) or 'none', f'{len(d)}p')
c = collections.Counter(v[0] for v in res.values())
print(c)
for f, v in sorted(res.items(), key=lambda x: x[1]):
    if v[0] in ('none', 'image', 'no text') or ('SDS' in v[0] and 'TYP' in v[0]):
        print(v, f)
