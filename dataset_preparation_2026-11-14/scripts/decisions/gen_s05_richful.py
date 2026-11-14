"""Supplier batch S05: Richful (Xinxiang Richful Lube Additive Co., Ltd.; 343 documents with provisional supplier 'Richful').
Read: the automated identity of every document checked against its page-1 top lines; for the 98 documents without a clean
'RFxxxx' identity, pages 1-2 were searched for RF codes and the printed product-name field (SDS 'Product name' / 'Trade name',
certificate '产品名称 (Product Name)'), and 7 cards were read at 500 characters.
Rule: single-product documents (SDS, product data sheet, certificate, data package) -> subject = the RF code printed with the
product name (first RF code on pages 1-2); glued-title artefacts corrected (RF6079AP -> RF6079, RF6078AC -> RF6078,
RF6125AC -> RF6125; RF42021 dropped). Company profiles and product-line presentations are multi-product: no subject assigned.
A chemistry name without an RF code is NOT mapped to a code. Identity only. Writes decisions/s05_richful.json."""
import csv, json, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Richful']
SUP = 'Richful (Xinxiang Richful Lube Additive Co., Ltd.)'
EXIST = {'RF6602': 'RF6602', 'RF6066': 'RICHFUL_RF6066', 'RF6069': 'RICHFUL_RF6069', 'RF6071L': 'RICHFUL_RF6071L', 'RF6077': 'RICHFUL_RF6077', 'RF6078': 'RICHFUL_RF6078',
         'RF6079': 'RICHFUL_RF6079', 'RF6080': 'RICHFUL_RF6080', 'RF6081': 'RICHFUL_RF6081', 'RF6088': 'RICHFUL_RF6088', 'RF6088F': 'RICHFUL_RF6088F', 'RF6089': 'RICHFUL_RF6089',
         'RF6400': 'RICHFUL_RF6400', 'RF6406': 'RICHFUL_RF6406', 'RF6408': 'RICHFUL_RF6408'}
FIX = {'RF6077CI': 'RF6077', 'RF6079AP': 'RF6079', 'RF6078AC': 'RF6078', 'RF6125AC': 'RF6125', 'RF42021': None}
CODE = re.compile(r'(?<![A-Za-z0-9])RF\s?\d{4}[A-Z]{0,2}\d?(?:-\d)?')


COMPKW = re.compile(r'(?i)viscosity index improver|VII?|pour point|dispersant|sulfonate|sulphonate|phenate|phenolate|salicylate|antioxidant|anti-oxidant|dithiophosphate|friction modifier|rust (?:inhibitor|preventive)|corrosion inhibitor|anti-?wear agent|extreme pressure agent|defoam|anti-?foam|demulsif|tackifier|ester|succinimide|diphenylamine|metal deactivator|olefin copolymer|polymethacrylate')
COMPKW = re.compile(r'(?i)viscosity index improver|\bVII?\b|pour point|dispersant|sulfonate|sulphonate|phenate|phenolate|salicylate|antioxidant|anti-oxidant|'
                    r'dithiophosphate|friction modifier|rust (?:inhibitor|preventive)|corrosion inhibitor|anti-?wear agent|extreme pressure agent|defoam|anti-?foam|'
                    r'demulsif|tackifier|\bester\b|succinimide|diphenylamine|metal deactivator|olefin copolymer|polymethacrylate')  # clean definition (replaces the line above)
PKGKW = re.compile(r'(?i)package|additive for|oil additive')
TITLE = {}


def cls(c):
    t = TITLE.get(c, '')
    if re.search(r'(?i)gasoline detergent|fuel additive', t):
        return 'out_of_template: fuel additive', 'printed title: ' + t[:80]
    if c not in ('RF6602',) and t:
        if PKGKW.search(t) and not re.search(r'(?i)^\W*RF\d+\w*\s+(?:[A-Za-z-]+\s){0,4}(?:dispersant|sulfonate|phenate|salicylate|antioxidant|dithiophosphate|improver|depressant)', t):
            return 'additive_package', 'printed title names a package: ' + t[:90]
        if COMPKW.search(t):
            return 'additive_component', 'printed title names a component function: ' + t[:90]
    n = int(re.sub(r'\D', '', c[2:6]) or 0)
    if c == 'RF6602': return 'additive_component', 'viscosity index improver (existing record)'
    if c == 'RF8248' or c.startswith('RF8'): return 'additive_component', 'pour point depressant (PPD subtype)'
    if 1100 <= n < 1200: return 'additive_component', 'detergent / dispersant / antioxidant component (RF11xx series)'
    if 2200 <= n < 2300: return 'additive_component', 'ZDDP antioxidant / anti-corrosion component (RF22xx series)'
    if c == 'RF5057': return 'additive_component', 'octylated / butylated diphenylamine antioxidant'
    if 6600 <= n < 6700: return 'additive_component', 'viscosity index improver (RF66xx; VM subtype)'
    if 6000 <= n < 6600 or 4000 <= n < 4500 or 5000 <= n < 5100: return 'additive_package', 'package series (RF4xxx gear / RF50xx hydraulic / RF60xx-65xx engine): class by series, title not decisive'
    return 'unresolved', 'class not established from the printed title (series function unknown): ' + t[:80]


def dtype(r, t):
    h = r['top_lines'] + ' ' + t[:300]
    if re.search(r'(?i)safety data sheet', h): return 'SDS'
    if re.search(r'Company Profile', h): return 'company catalogue (multi-product)'
    if re.search(r'(?i)confidential and proprietary to Richful|Product Line|Solutions? of Richful|Additive Product', h): return 'presentation / brochure (multi-product)'
    if re.search(r'Catalogue', h): return 'product data package (specification, COA, evaluation data)'
    if re.search(r'执行标准|规格及测试结果|Specification and Result|Batch No', h): return 'certificate of analysis (batch)'
    if re.search(r'(?i)Product Introduction|Typical|Technical', h) or int(r['pages'] or 0) <= 2: return 'product data sheet (TDS/PDS)'
    return 'presentation / brochure (multi-product)'


D, PK = {}, {}
for r in A:
    sha = r['sha256']
    pg, _ = ident.pages_for(sha)
    t = re.sub(r'\s+', ' ', '\n'.join(pg[:2]))
    typ = dtype(r, t)
    note, rel = '', 'product'
    if typ.endswith('(multi-product)'):
        codes = []
        note = 'multi-product document: products presented inside are not listed in this identity pass'
    elif sha.startswith('f0b3b8abdd'):
        codes, note = ['T900 SILICON FLUID'], "'T900 Silicon Fluid' product sheet (Richful)"
    else:
        auto = re.sub(r'\s', '', r['primary_identity']).upper()
        cand = [auto] if re.fullmatch(r'RF\d{3,4}[A-Z]{0,2}', auto) else [re.sub(r'\s', '', m.group(0)).upper() for m in CODE.finditer(t)]
        codes = []
        for c in cand:
            c = FIX.get(c, c)
            if c and c not in codes:
                codes.append(c)
        codes = codes[:1]
        for c in codes:
            m = re.search(re.escape(c) + r'.{0,110}', t)
            TITLE.setdefault(c, re.sub(r'\s+', ' ', m.group(0)) if m else '')
        if not codes:
            rel, note = 'unresolved_identity', 'no RF code printed on pages 1-2 (chemistry name only); not mapped to a code'
    if r['byte_duplicate_of_existing']:
        note = (note + '; ' if note else '') + 'byte duplicate of an old-archive file'
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['RICHFUL:' + c for c in codes], roles={'RICHFUL:' + c: 'subject' for c in codes}, relation=rel,
                       read='automated identity checked against page-1 top lines; RF codes / product-name field searched on pages 1-2', note=note,
                       next_action='list the products presented inside in the package review' if typ.endswith('(multi-product)') else ('' if codes else 'identify the RF grade (not printed on pages 1-2)'))
for k in dict.fromkeys(p for v in D.values() for p in v['products']):
    c = k.split(':', 1)[1]
    mc, n = (('additive_component', 'silicone fluid (antifoam / special fluid); component general') if c.startswith('T900') else cls(c))
    PK[k] = dict(name=c if not c.startswith('T900') else 'T900 Silicon Fluid', supplier=SUP, material_class=mc, existing_record=EXIST.get(c, ''),
                 status='existing' if c in EXIST else ('out_of_scope' if mc.startswith('out_of_template') else 'new_candidate'), notes=n, identity_evidence='printed RF code on the documents linked in this batch',
                 template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}.get(mc, 'not determined (class unresolved)'))
out = dict(batch='S05 Richful (identity)', reviewed_on='2026-11-14', scope='343 documents with provisional supplier Richful', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's05_richful.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['doc_type'] for v in D.values()), Counter(v['relation'] for v in D.values()), Counter(p['status'] for p in PK.values()))
