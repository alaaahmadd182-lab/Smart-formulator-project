"""Supplier batch S22: Vanderbilt Chemicals, LLC (29 documents).
Read: compact listing (automated identity = printed title); 4 pages viewed as images where the name is printed as graphics:
DL2-12184 'VANLUBE NA' (specification, RTV code 50506), DL2-13039 'VANLUBE AZ', DL2-13040 'MOLYVAN L', DL2-13046 'VANLUBE SB'
(specification, RTV code 50928).
Rules: subject = printed trade name; 'VANLUBE 289' vs '289HD', '0401', '887' / '887E' / '887 FG' (one sheet naming three grades:
all linked, role 'grade on a multi-grade sheet'). Other trade names printed in a sheet's text (e.g. 'VANLUBE 829', 'VANLUBE
972NT' recommended for combination on the Molyvan L sheet) are co-component mentions, NOT linked in this identity pass (they are
evidence for the field review of the sheet's product). All are lubricant additive components (antioxidant, antiwear / EP,
friction reducer, metal deactivator); VANLUBE 1305 'Engine Oil Performance Booster' -> class unresolved (booster);
MOLYVAN FEI Plus brochure -> subject MOLYVAN FEI PLUS. Identity only. Writes decisions/s22_vanderbilt.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Vanderbilt')]
SUP = 'Vanderbilt Chemicals, LLC'
OV = {'222cab7b16': (['VANLUBE NA'], 'specification', "RTV Product Code 50506; 'Mixture of alkylated diphenylamines' (page image viewed)"),
      'd990ebafad': (['VANLUBE AZ'], 'product data sheet (TDS/PDS)', "'zinc diamyldithiocarbamate'; multifunctional antioxidant / metal deactivator / corrosion inhibitor / antiwear (page image viewed)"),
      '1103318c0c': (['MOLYVAN L'], 'product data sheet (TDS/PDS)', "'Molybdenum di(2-ethylhexyl)phosphorodithioate' (page image viewed); VANLUBE 829 / 972NT named as combination partners (mentions, not linked)"),
      '7ba7fda6f7': (['VANLUBE SB'], 'specification', "RTV Product Code 50928; 'Sulfur-based additive' (page image viewed)"),
      '387520e4bd': (['MOLYVAN FEI PLUS'], 'brochure', "'MOLYVAN FEI Plus Lubricant Additive - Friction Reducer, Antiwear, Antioxidant' (8 pp)"),
      '0cd5bdebac': (['BUTYLATED HYDROXY TOLUENE TECH GRADE'], 'SDS', ''),
      '0745d4676a': (['VANLUBE 887', 'VANLUBE 887E', 'VANLUBE 887 FG'], 'product data sheet (TDS/PDS)', "one sheet for VANLUBE 887 / 887E / 887 FG ('Tolutriazole compound in mineral oil')")}
D, PK = {}, {}
for r in A:
    sha, p10, t = r['sha256'], r['sha256'][:10], r['top_lines']
    if p10 in OV:
        keys, typ, note = OV[p10]
    else:
        keys = [re.sub(r'\s+', ' ', r['primary_identity'].upper()).strip()]
        typ = 'SDS' if 'SAFETY DATA SHEET' in t.upper() else ('product data sheet (TDS/PDS)' if re.search(r'(?i)T\s?e\s?c\s?h\s?n\s?i\s?c\s?a\s?l', t) else 'specification / product bulletin')
        note = ''
    ks = ['VANDERBILT:' + k for k in keys]
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=ks, roles={k: ('subject' if len(ks) == 1 else 'grade on a multi-grade sheet') for k in ks}, relation='product',
                       read='page-1 listing' + ('; page image viewed' if p10 in ('222cab7b16', 'd990ebafad', '1103318c0c', '7ba7fda6f7') else ''), note=note, next_action='')
    parts = [x.strip() for x in re.split(r'\n|\s\|\s', t)]
    desc = ''
    if typ == 'product data sheet (TDS/PDS)':
        stop = next((i for i, x in enumerate(parts) if i > 0 and re.match(r'(?i)T\s?e\s?c\s?h|VANLUBE|MOLYVAN', x)), len(parts))
        desc = ' '.join(x for x in parts[0:stop] if x and not re.match(r'(?i)VANLUBE|MOLYVAN|T\s?e\s?c\s?h', x))[:90]
        if re.search(r'(?i)guarantee|warrant|before using', desc):
            desc = ''
    for k in ks:
        if k in PK and not (desc and PK[k]['notes'].startswith('lubricant additive (function')): continue
        if '1305' in k:
            mc, n = 'unresolved', "printed 'Engine Oil Performance Booster' (booster: package vs component to confirm)"
        else:
            mc, n = 'additive_component', note or ('printed: ' + desc if desc and 'Before using' not in desc and 'Liquid.' not in desc else 'lubricant additive (function as printed on its sheet)')
        PK[k] = dict(name=k.split(':', 1)[1], supplier=SUP, material_class=mc, existing_record='', status='new_candidate', notes=n,
                     identity_evidence='printed trade name on the documents linked in this batch', template='additive_component general' if mc == 'additive_component' else 'not determined')
out = dict(batch='S22 Vanderbilt (identity)', reviewed_on='2026-11-14', scope='29 documents with provisional supplier Vanderbilt Chemicals', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's22_vanderbilt.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(48), v['notes'][:70])
