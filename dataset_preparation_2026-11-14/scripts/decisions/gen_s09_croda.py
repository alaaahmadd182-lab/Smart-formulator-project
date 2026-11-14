"""Supplier batch S09: Croda (102 documents with provisional supplier 'Croda').
Read: compact page-1 listing of all 102 documents; 6 longer cards (600 characters); DL2-15219 page 1 viewed as an image
(title printed as graphics: 'Cargill Priolube(TM) 1939', Cargill logo).
Rules
- Subject = brand + grade printed on page 1 (Priolube, Emkarox, Crodacid, Cithrol, Perfad, Crodasinic, Xenitron).
- Croda SDS / specification / CoA names carry a form + site suffix ('-LQ-(GD)', '-(CQ)', '-(SI)', '-(SG)', '-(MV)', '-FL-'): the
  document is linked to the base grade with role 'subject (site-coded name <suffix>)'; the suffix is kept as printed in 'region'.
  Site-coded supplies are NOT asserted to be identical in composition; any value difference between sites stays a conflict.
- 'SP PRIOLUBE 3970 MBAL' is kept as a separate product (printed variant of Priolube 3970; not merged).
- 'Emkarox HV20 SOL 60%' / 'HV45 SOL 56%': grade = HV20 / HV45, the printed solution strength kept in the note.
- 'PRODUCT DATA | ENERGY TECHNOLOGIES' sheets: DL2-15219 viewed and is Cargill-branded; the others share the layout (brand not
  individually viewed). The brand printed is recorded per document; no ownership statement is made.
- Classes from the printed descriptor: 'synthetic (ester) lubricant base fluid and additive' -> class unresolved (base fluid vs
  component; base_oil template has no API group for esters): schema / scope question. '...lubricant additive' -> component.
  Water-insoluble / soluble PAG base fluids -> base_oil candidates (template fit to confirm). Dielectric ester -> out of template.
- The product-list spreadsheets DL2-12147 / 12148 (Croda + Clariant names) and the brochures are multi-product. DL2-12143 is not a
  Croda document (SinoSyn / SynNaph / NacoFlow names): supplier left unestablished, multi-product.
Identity only. Writes decisions/s09_croda.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Croda')]
SUP = 'Croda'
BR = r'(PRIOLUBE|EMKAROX|CRODACID|CITHROL|PERFAD|CRODASINIC|XENITRON)'
NAME = re.compile(r'(?i)(SP\s+)?' + BR + r'[\s™-]*((?:DB\s)?(?:VG\s?|HV|DC\s?)?\d{2,4}[A-Z]{0,2}|O\b|PG32IS)(\s+MBAL)?((?:-[A-Z]{2})?-\([A-Z]{2}\)|-LQ\b|-FL\b)?')
CL = {'PRIOLUBE 3986': ('additive_component', "printed 'High performance synthetic ester lubricant additive'"),
      'CITHROL PG32IS': ('additive_component', "printed 'High performance ashless friction modifier'"),
      'PERFAD DB 3343': ('additive_component', "printed 'soot dispersant booster for engine oils'"),
      'CRODASINIC O': ('additive_component', "printed 'Oleyol sarcosine' corrosion inhibitor"),
      'CRODACID DC 1195': ('out_of_template: other chemical', "printed 'renewable, saturated dicarboxylic acid'"),
      'XENITRON 3221': ('out_of_template: finished fluid (dielectric ester)', "printed 'fully synthetic dielectric ester'")}
MULTI = {'b89851c517': "'Fire Resistant Hydraulic Fluids' brochure (Croda Lubricants)", '532c733bf0': "'Priolube 2720 / Priolube 3970' comparison presentation (22 pp, 2 copies)",
         '6f6f2b11bf': 'product-list spreadsheet naming Croda and Clariant products (Perfad 8100, Crodamol GTCC, Priolube 1415 ... 3986)', '6ceb17ca14': 'same title list as DL2-12147 (different bytes)'}
NOTCRODA = {'74c1681ad2': "spreadsheet of SinoSyn PAO / SynNaph alkylated naphthalene / NacoFlow mPAO grades: not a Croda document; supplier not established"}
OV = {'8cb456d085': ('PRIOLUBE 1939', '', "Cargill-branded 'Cargill Priolube 1939' product data sheet (title printed as graphics; page image viewed)"),
      'd75efef25d': ('EMKAROX HV20', '', "printed 'Emkarox HV20 SOL 60%'"), '6e9bc58b8b': ('EMKAROX HV45', '', "printed 'Emkarox HV45 SOL 56%'")}


def canon(m):
    br = m.group(2).upper()
    g = re.sub(r'\s', '', m.group(3).upper())
    g = re.sub(r'^(VG|DC|DB)(\d)', r'\1 \2', g)
    if br == 'PERFAD' and g.startswith('DB'): g = 'DB ' + g[3:].strip() if g[2] == ' ' else g
    key = ('SP ' if m.group(1) else '') + br + ' ' + g + (' MBAL' if m.group(4) else '')
    return key, (m.group(5) or '').strip('-')


def dtype(t, pages):
    if re.search(r'(?i)safety data sheet|fiche de donn', t): return 'SDS'
    if re.search(r'(?i)Period of validity of Certificate|Quality Control Results', t): return 'specification / certificate of analysis'
    if re.search(r'(?i)^.{0,40}Specification', t[:120]) or 'Specification prepared' in t: return 'specification'
    return 'product data sheet (TDS/PDS)'


D, PK = {}, {}
for r in A:
    sha, t = r['sha256'], r['top_lines'].replace('\n', ' | ')
    p10 = sha[:10]
    region, brand = '', ''
    if p10 in MULTI or p10 in NOTCRODA:
        D[sha[:12]] = dict(doc_type='brochure / product list (multi-product)', supplier=SUP if p10 in MULTI else 'not established (not Croda)', products=[], roles={},
                           relation='product', read='page-1 listing / longer card', note=MULTI.get(p10) or NOTCRODA[p10], next_action='list the products inside (multi-product)')
        continue
    if p10 in OV:
        key, region, note = OV[p10]
    else:
        m = NAME.search(r['primary_identity']) or NAME.search(t)
        key, region = canon(m) if m else ('', '')
        note = ''
    if 'PRODUCT DATA | ENERGY TECHNOLOGIES' in t:
        note = (note + '; ' if note else '') + "'PRODUCT DATA / ENERGY TECHNOLOGIES' layout (as DL2-15219, which is Cargill-branded); brand not individually viewed"
    role = 'subject' + (f" (site-coded name '{region}')" if region else '')
    D[sha[:12]] = dict(doc_type=dtype(t, r['pages']), supplier=SUP, products=['CRODA:' + key] if key else [], roles={'CRODA:' + key: role} if key else {},
                       relation='product' if key else 'unresolved_identity', region=region, read='page-1 listing' + ('; page image viewed' if p10 == '8cb456d085' else ''),
                       note=note, next_action='' if key else 'identify the product')
    if key and 'CRODA:' + key not in PK:
        base = key.replace('SP ', '').replace(' MBAL', '')
        desc = re.search(re.escape(m.group(0) if p10 not in OV else '') + r'.{0,4}\|\s*([^|]{10,90})', t) if p10 not in OV else None
        if base in CL:
            mc, n = CL[base]
        elif key.startswith('EMKAROX'):
            mc, n = 'base_oil', 'polyalkylene glycol lubricant base fluid (base_oil template fit to confirm: no API group)'
        elif key.startswith(('PRIOLUBE', 'SP PRIOLUBE')):
            mc, n = 'unresolved', 'synthetic ester lubricant base fluid (and additive): base fluid vs component to confirm; base_oil template has no API group for esters'
        else:
            mc, n = 'unresolved', ''
        PK['CRODA:' + key] = dict(name=key.title().replace('Sp ', 'SP ').replace('Mbal', 'MBAL').replace('Vg', 'VG').replace('Hv', 'HV').replace('Db ', 'DB ').replace('Dc ', 'DC ').replace('Pg32Is', 'PG32IS'),
                                  supplier=SUP, material_class=mc, existing_record='', status='out_of_scope' if mc.startswith('out_of') else 'new_candidate', notes=n,
                                  identity_evidence='printed product name on the documents linked in this batch',
                                  template={'additive_component': 'additive_component general', 'base_oil': 'base_oil tier1-3 (template fit to confirm)'}.get(mc, 'none / not determined'))
out = dict(batch='S09 Croda (identity)', reviewed_on='2026-11-14', scope='102 documents with provisional supplier Croda', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's09_croda.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['material_class'] for p in PK.values()))
print(sorted(PK))
print(Counter(v['region'] for v in D.values() if v.get('region')))
