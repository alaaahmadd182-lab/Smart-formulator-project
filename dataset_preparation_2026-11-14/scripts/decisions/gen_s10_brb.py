"""Supplier batch S10: BRB International BV (90 documents with provisional supplier 'BRB').
Read: compact page-1 listing; for every document the page-1 text after the letterhead (product name + printed descriptor line up
to 'Issue date'); 6 longer cards (500 characters); SDS section 1.2 of Petrolad 8100 ('Recommended Use No information available').
Rules
- Subject = the printed name INCLUDING its printed variant: Viscotech 'L' / 'LP' liquid forms and the printed solution viscosity
  (e.g. 'Viscotech 6540 L 850 cSt' and '... 1300 cSt' are separate products; 'Viscotech 494L' (2016, no viscosity printed) is
  NOT merged with 'Viscotech 494L 3500 cSt'). 'Petrolad 6779' / '6779A', '743EU' / '743N', '42336' / '42336G' etc. kept apart.
- Two editions of one name (Petrolad 336 2016-10-31 'Gear oil additive package' and 2016-11-09 'EP Gear oil additive package';
  Petrolad 19002 2015 / 2016) are linked to the same product as editions; differences stay for the field review.
- Class from the printed descriptor only: fuel additives (gasoline / diesel / cetane / octane / VSR protector) and the coolant
  package are out of template; 'STOP SMOKE' oil supplement is an aftermarket finished product; Thixocal gelled calcium sulfonates
  (oil / solvent / water based) are a scope question; the metalworking package keeps a scope question.
- Viscotech 595L prints no descriptor (typical data only): class component (VM) taken from the brand family, marked provisional.
- Existing production record: BRB_PETROLAD_8099.
Identity only. Writes decisions/s10_brb.json."""
import csv, json, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('BRB')]
SUP = 'BRB International BV'
EXIST = {'PETROLAD 8099': 'BRB_PETROLAD_8099'}
NAME = re.compile(r'(?i)(PETROLAD|VISCOTECH|THIXOCAL)\s*®?\s*(\d{3,5}[A-Z]{0,2})(?:\s?(LP|L)\b)?(?:\s(FGD))?(?:-(FAST DRY))?(?:\s(\d{3,5})\s?cSt)?')
OV = {'4ba3ebd9a1': ('STOP SMOKE', 'Oil additive'), '719ab2a8c8': ('BRB SILICONE OIL', 'silicone oil: release agent, anti-foam agent and other printed uses'),
      'c6ee1a6d8f': ('BRB SILICONE OIL 12500 CST', "SDS 'BRB Silicone Oil 12500 cSt' (Dimethicone)"), '40f4485feb': ('BRB SILICONE OIL 12500 CST', 'certificate of analysis, batch B118682'),
      'd9f68004e0': ('PETROLAD 8100', 'SDS only; recommended use printed as \'No information available\''),
      '21f5f5a6f7': ('PETROLAD 9200', 'Engine Oil Additive Package (2-page leaflet with treat-rate chart)'), '6b365d28fd': ('PETROLAD 743N', 'multi-purpose low ash additive package (Automatic Transmission Fluid additive)'),
      'dd379b7c6e': ('PETROLAD 3550', 'Coolant Corrosion-Inhibitor Additive Package (BRB Lube oil Additives & Chemicals, 2022-11)')}
FUEL = re.compile(r'(?i)fuel|cetane|octane|VSR protector')


def cls(key, d):
    if key == 'STOP SMOKE': return 'out_of_template: finished product (aftermarket oil supplement)', 'printed: ' + d
    if key.startswith('BRB SILICONE'): return 'additive_component', 'silicone fluid; anti-foam is one of several printed uses: scope question'
    if FUEL.search(d): return 'out_of_template: fuel additive', 'printed: ' + d
    if re.search(r'(?i)coolant', d): return 'out_of_template: coolant additive', 'printed: ' + d
    if key.startswith('THIXOCAL'): return 'unresolved', 'printed: ' + d + ' (gelled calcium sulfonate; scope question: not a lubricant-oil additive class in the templates)'
    if key.startswith('VISCOTECH'):
        return 'additive_component', ('printed: ' + d + ' (VM subtype)') if d else 'no descriptor printed; viscosity modifier by brand family (provisional, VM subtype)'
    if re.search(r'(?i)metalworking', d): return 'additive_package', 'printed: ' + d + ' (metalworking: scope question)'
    if re.search(r'(?i)foam inhibitor|anti-wear additive|sulfonate|pour point|friction modifier|tacky', d): return 'additive_component', 'printed: ' + d
    if re.search(r'(?i)performance booster', d): return 'unresolved', 'printed: ' + d + ' (booster: package vs component to confirm)'
    if re.search(r'(?i)package|engine oil additive|oil additive|transmission|gasoline additive|UTTO|hydraulic', d):
        return 'additive_package', 'printed: ' + d + (" (description: 'designed to meet API CB/SB to CC/CF levels in the automotive lubricant industry')" if 'gasoline additive' in d else '')
    return 'unresolved', 'printed: ' + d


D, PK, desc = {}, {}, {}
for r in A:
    sha = r['sha256']
    pg, _ = ident.pages_for(sha)
    t = re.sub(r'\s+', ' ', pg[0] if pg else '')
    body = re.sub(r'^.*?(?:brb-international\.com|info@brbbv\.com|page 1)\s*', '', t, count=1, flags=re.I)
    if 'BRB USA Inc' in body:
        body = re.sub(r'^.*?info@brbbv\.com\s*', '', body)
    if sha[:10] in OV:
        key, d = OV[sha[:10]]
        variant = ''
    else:
        m = NAME.search(body) or NAME.search(t)
        if not m: print("NO NAME", sha[:10], body[:200]); continue
        br, code, form, fgd, fast, visc = m.groups()
        key = f'{br.upper()} {code.upper()}' + (f' {fgd}' if fgd else '') + (f' {form.upper()}' if form else '') + (f'-{fast.upper()}' if fast else '') + (f' {visc} CST' if visc else '')
        key = re.sub(r'(\d)L\b', r'\1 L', key)
        d = re.split(r'(?i)\s*issue date', body[m.end():], 1)[0].strip(' ®:-')[:90]
    rev = re.search(r'(?i)issue date:?\s*([0-9A-Za-z ,.\-]{6,22}?\d{4})', t)
    D[sha[:12]] = dict(doc_type='SDS' if re.search(r'(?i)safety data sheet', t[:400]) else ('certificate of analysis (batch)' if 'Certificate of analysis' in t else 'product data sheet (TDS/PDS)'),
                       supplier=SUP, products=['BRB:' + key], roles={'BRB:' + key: 'subject'}, relation='product', date=rev.group(1) if rev else '',
                       read='page-1 text after the letterhead (name + printed descriptor)', note='', next_action='')
    desc.setdefault(key, d or desc.get(key, ''))
    if d and not desc[key]:
        desc[key] = d
for k, d in desc.items():
    mc, n = cls(k, d)
    PK['BRB:' + k] = dict(name=k.title().replace('Cst', 'cSt').replace('Brb', 'BRB').replace(' Lp', ' LP').replace('Fgd', 'FGD'), supplier=SUP, material_class=mc,
                          existing_record=EXIST.get(k, ''), status='existing' if k in EXIST else ('out_of_scope' if mc.startswith('out_of') else 'new_candidate'), notes=n,
                          identity_evidence='printed product name on the documents linked in this batch',
                          template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}.get(mc, 'none / not determined'))
for k in ('PETROLAD 336', 'PETROLAD 19002'):
    PK['BRB:' + k]['notes'] += '; two dated editions linked (differences to be compared in the field review)'
PK['BRB:VISCOTECH 494 L']['notes'] += "; possibly the same grade as 'Viscotech 494L 3500 cSt' (viscosity not printed): NOT merged"
out = dict(batch='S10 BRB International (identity)', reviewed_on='2026-11-14', scope='90 documents with provisional supplier BRB', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's10_brb.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['status'] for p in PK.values()), Counter(p['material_class'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(34), v['material_class'][:30].ljust(31), v['notes'][:80])
