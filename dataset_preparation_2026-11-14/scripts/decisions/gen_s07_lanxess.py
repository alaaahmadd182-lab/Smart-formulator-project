"""Supplier batch S07: LANXESS / Rhein Chemie (125 documents with this provisional supplier).
Read: compact page-1 listing of every document checked row by row; 6 longer cards (700 characters).
Rule: subject = brand + grade printed on page 1 (Additin RC xxxx [suffix], Synton PAO, Stabaxol, Diphyl, phosphate esters);
'RC 9200 N' and 'RC 9321 D' kept as printed variants of RC 9200 / RC 9321 (LANXESS letter DL2-15263: RC 9321 and RC 9321 'D'
performance 'equal' - recorded, not merged). Brochures / catalogues are multi-product (no subject).
Classes: Additin RC 9xxx = additive packages; other Additin RC grades = components (AW / EP, corrosion inhibitor, antioxidant,
friction modifier, speciality); Synton PAO = base_oil (Group IV PAO); Diphyl = heat-transfer fluid (no template); Stabaxol =
hydrolysis stabiliser (component, scope question); TiBP / TBP / dibutyl phenyl phosphate = phosphate esters (class unresolved).
Identity only. Writes decisions/s07_lanxess.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'LANXESS / Rhein Chemie']
SUP = 'LANXESS (Rhein Chemie)'


def norm(r):
    t = r['top_lines']
    m = re.search(r'(?i)ADDITIN\s*®?\s*RC\s*(\d{4})(?:\s*(N|D|LD|NA)\b)?', t) or re.search(r'(?i)\bRC\s*(\d{4})(?:\s*(N|D|LD)\b)?', t)
    if m:
        return 'ADDITIN RC ' + m.group(1) + (' ' + m.group(2).upper() if m.group(2) else '')
    for pat, key in ((r'(?i)SYNTON PAO\s*(\d+)', 'SYNTON PAO {}'), (r'(?i)STABAXOL\s+([A-Z]\s?\d*\s?[A-Z]*)', 'STABAXOL {}'), (r'(?i)DIPHYL\s*([A-Z]{2,3})?', 'DIPHYL {}')):
        m = re.search(pat, t)
        if m:
            return key.format((m.group(1) or '').strip().upper()).strip()
    return ''


def cls(k):
    if k.startswith('ADDITIN RC 9'): return 'additive_package', 'Additin RC 9xxx package'
    if k == 'ADDITIN RC 8103': return 'additive_component', "printed type 'Synthetic ester for metal working': metalworking scope question"
    if k.startswith('ADDITIN RC'):
        n = int(k.split()[2])
        f = {2: 'EP / AW', 3: 'antiwear / friction modifier', 4: 'corrosion inhibitor', 5: 'water-miscible / speciality', 6: 'antiwear', 7: 'antioxidant', 8: 'speciality product'}.get(n // 1000, '')
        return 'additive_component', f'Additin RC component ({f})'
    if k.startswith('SYNTON PAO'): return 'base_oil', 'polyalphaolefin base stock (API Group IV): base_oil template'
    if k.startswith('DIPHYL'): return 'out_of_template: heat transfer fluid', 'heat-transfer fluid'
    if k.startswith('STABAXOL'): return 'additive_component', 'carbodiimide hydrolysis stabiliser (polymer / ester additive): scope question'
    if 'PHOSPHATE' in k: return 'unresolved', 'phosphate ester chemical (possible antiwear / fire-resistant fluid base): class not established'
    return 'unresolved', ''


def dtype(t):
    if re.search(r'(?i)safety data sheet|Product Safety Assessment', t): return 'SDS'
    if re.search(r'(?i)certificate of analysis', t): return 'certificate of analysis (batch)'
    if re.search(r'(?i)technical report|test results may vary', t): return 'technical report (performance data)'
    if re.search(r'(?i)product data sheet|technical data sheet', t): return 'product data sheet (TDS/PDS)'
    return 'brochure (multi-product)'


OV = {'6440238bde': (['ADDITIN RC 3661'], ''), 'f30bbf7eb2': (['ADDITIN RC 9321', 'ADDITIN RC 9321 D'], "LANXESS letter (02 Nov 2021): performance of RC 9321 and RC 9321 'D' 'is equal' (supplier statement recorded; variants kept apart)"),
      '9b2562cef3': (['TRI-ISO-BUTYL PHOSPHATE (TIBP)'], ''), '5971e07790': (['TRIBUTYL PHOSPHATE (TBP)'], ''), '5b026785da': (['DIBUTYL PHENYL PHOSPHATE'], 'product safety assessment'),
      '74baf00f1f': (['STABAXOL I LF'], ''), 'ecf5095558': (['STABAXOL L'], ''), 'e584692aba': (['STABAXOL L', 'STABAXOL P 211'], 'confidential presentation of new hydrolysis stabilisers'),
      'ac84fce66c': (['ADDITIN RC 3502'], "'ORGANIC FRICTION MODIFIER' brochure (Additin RC 3502 per the companion data sheets; the name on this brochure is in its pages, read for identity only)"),
      'fa178486c5': (['ADDITIN RC 7130'], ''), '8d74243620': (['ADDITIN RC 9502'], ''), '1afc1bcc97': (['DIPHYL DT'], ''), 'fdb81d2ade': (['DIPHYL KT'], ''), '65af04c850': (['DIPHYL'], ''),
      '4966c833d9': (['DIPHYL THT'], ''), '5e13d1824a': (['ADDITIN RC 3038'], "batch certificate (LANXESS India, 23.12.2022): 'Material Description ADDITIN RC 3038' read in the longer card"), 'd971f92178': (['ADDITIN RC 9200'], ''), 'd3a4481bec': (['ADDITIN RC 9330'], '')}
MULTI = {'0558d6a902': "'QUALITY BOOSTS. Additives for the lubricant oil industry' product catalogue (20 pp)", '9917719105': 'same title as DL2-13075 (different bytes)',
         '1f7ae3df8f': "'QUALITY BOOSTS. Synthetic base fluids & lubricant additives' catalogue (16 pp, 2 copies)", 'cba38d03a7': "'QUALITY BOOSTS. Lubricant Additives Formulated lubricants' brochure",
         'b56454b204': "'Heat Transfer Fluids KT / DT / THT' brochure", '19dad0c6ad': "'LANXESS Heat Transfer Fluids' brochure (2017)"}
D, PK = {}, {}
for r in A:
    sha = r['sha256']
    t = r['top_lines']
    typ = dtype(t)
    if any(sha.startswith(k) for k in MULTI):
        keys, note, typ = [], next(v for k, v in MULTI.items() if sha.startswith(k)), 'brochure / catalogue (multi-product)'
    elif any(sha.startswith(k) for k in OV):
        keys, note = next(v for k, v in OV.items() if sha.startswith(k))
        if sha.startswith('ac84fce66c'):
            typ = 'brochure'
    else:
        k = norm(r)
        keys, note = ([k] if k else []), ''
    if sha.startswith('ac84fce66c'):
        note = "'QUALITY ENDURES. ORGANIC FRICTION MODIFIER' brochure; linked to Additin RC 3502 by its printed title 'Organic Friction Modifier' only - role 'probable subject (name not on page 1)'"
    roles = {'LANXESS:' + k: ('probable subject (name not on page 1)' if sha.startswith('ac84fce66c') else 'subject') for k in keys}
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['LANXESS:' + k for k in keys], roles=roles, relation='product' if keys or 'multi' in typ else 'unresolved_identity',
                       read='page-1 listing read; longer cards for 6', note=note, next_action='list the products inside (multi-product)' if 'multi' in typ else ('' if keys else 'identify the product'))
    for k in keys:
        if 'LANXESS:' + k in PK: continue
        mc, n = cls(k)
        PK['LANXESS:' + k] = dict(name=k.title().replace('Rc', 'RC').replace('Pao', 'PAO'), supplier=SUP, material_class=mc, existing_record='',
                                  status='out_of_scope' if mc.startswith('out_of') else 'new_candidate', notes=n, identity_evidence='printed name on the documents linked in this batch',
                                  template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general', 'base_oil': 'base_oil tier1-3 (Group IV PAO)'}.get(mc, 'none / not determined'))
out = dict(batch='S07 LANXESS / Rhein Chemie (identity)', reviewed_on='2026-11-14', scope='125 documents with provisional supplier LANXESS / Rhein Chemie', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's07_lanxess.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['material_class'] for p in PK.values()))
print(sorted(k[8:] for k in PK))
