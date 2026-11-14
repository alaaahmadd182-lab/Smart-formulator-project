"""Supplier batch S12: INEOS (INEOS Oligomers; 55 documents with provisional supplier 'INEOS').
Read: compact page-1 listing; longer cards for DL2-11373 / 11374 (grade below the disclaimer: Panalane H-300E / L-14E) and the
product-list spreadsheet DL2-12145.
Rules
- Subject = 'Durasyn <grade>' / 'Indopol <grade>' / 'Panalane <grade>' as printed; 'Durasyn 174 I' = '174i', '180 I' = '180I'
  (spacing / case only); '164' vs '164X', '166' vs '166X', '162' vs '162S', '180I' vs '180R' are separate products.
- Multi-grade SDSs (INDOPOL H-1500 ... H-18000; INDOPOL H-50 ... H1200 CP) are linked to each printed grade with role
  'covered by multi-grade SDS'; grades printed only there (H-100 CP, H-300 C, H-300 CP, H-1200 CP) become products of their own.
- Two LANXESS 'Additin RC 9330' technical reports filed here are linked to LANXESS:ADDITIN RC 9330 (S07 key), supplier LANXESS.
- Classes: Durasyn polyalphaolefins -> base_oil (Group IV PAO; 'Polyalphaolefin' printed). Indopol polybutene / Panalane
  hydrogenated polybutene -> class unresolved (role as base fluid / VM / tackifier not stated on page 1). Cereclor 42
  (chlorinated paraffin wax) -> additive component, application to confirm (not printed on page 1).
Identity only. Writes decisions/s12_ineos.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('INEOS')]
SUP = 'INEOS (INEOS Oligomers)'
MULTI = {'24d12782dc': 'product-list spreadsheet (Panalane, Indopol, Durasyn grades)', '9ee551d202': "presentation 'Exploring opportunities for high-vis PAO synthetics in the growing wind energy sector'",
         '6c3e296f8a': "'Durasyn Polyalphaolefins - The base oil of choice for your synthetic lubricants' brochure (33 pp)"}
OV = {'be8bfd62bf': ['PANALANE H-300E'], '2de22f9aa9': ['PANALANE L-14E'], '5c21f68cba': ['CERECLOR 42'],
      '37fad1b20f': ['INDOPOL H-1500', 'INDOPOL H-1900', 'INDOPOL H-2100', 'INDOPOL H-6000', 'INDOPOL H-18000'],
      'cc38abafa8': ['INDOPOL H-50', 'INDOPOL H-100', 'INDOPOL H-100 CP', 'INDOPOL H-300', 'INDOPOL H-300 C', 'INDOPOL H-300 CP', 'INDOPOL H-1200', 'INDOPOL H-1200 CP']}
LANX = ('a295c62fae', '3d3ba2f5bb')


def key_of(t):
    m = re.search(r'(?i)DURASYN[\W_]*(\d{3})\s?([A-Z])?\b', t)
    if m: return 'DURASYN ' + m.group(1) + (m.group(2) or '').upper()
    m = re.search(r'Grade:\s*([HL]-\d+)', t)
    if m: return 'INDOPOL ' + m.group(1)
    return ''


D, PK = {}, {}
for r in A:
    sha, t = r['sha256'], r['top_lines'].replace('\n', ' | ')
    p10 = sha[:10]
    if p10 in MULTI:
        D[sha[:12]] = dict(doc_type='brochure / presentation / product list (multi-product)', supplier=SUP, products=[], roles={}, relation='product', read='page-1 listing / longer card',
                           note=MULTI[p10], next_action='list the products inside (multi-product)')
        continue
    if p10 in LANX:
        D[sha[:12]] = dict(doc_type='technical report (performance data)', supplier='LANXESS (Rhein Chemie)', products=['LANXESS:ADDITIN RC 9330'], roles={'LANXESS:ADDITIN RC 9330': 'subject'},
                           relation='product', read='page-1 listing', note="LANXESS 'Additin RC 9330' technical report (Edition March 2018" + (", gear" if p10 == 'a295c62fae' else '') + ") filed under INEOS by the automated supplier label", next_action='')
        continue
    keys = OV.get(p10) or [key_of(t)]
    keys = [k for k in keys if k]
    multi_sds = p10 in ('37fad1b20f', 'cc38abafa8')
    typ = 'SDS' if (multi_sds or re.search(r'(?i)safety data sheet|Identification of the material|GHS product identifier|REACH', t)) else ('product information bulletin / TDS')
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['INEOS:' + k for k in keys], roles={'INEOS:' + k: ('covered by multi-grade SDS' if multi_sds else 'subject') for k in keys},
                       relation='product' if keys else 'unresolved_identity', read='page-1 listing' + ('; longer card' if p10 in ('be8bfd62bf', '2de22f9aa9') else ''),
                       note='multi-grade SDS (grades as printed in the title)' if multi_sds else '', next_action='' if keys else 'identify the product')
    for k in keys:
        if 'INEOS:' + k in PK: continue
        if k.startswith('DURASYN'):
            mc, n = 'base_oil', 'polyalphaolefin (API Group IV) base fluid'
        elif k.startswith(('INDOPOL', 'PANALANE')):
            mc, n = 'unresolved', ('hydrogenated ' if k.startswith('PANALANE') else '') + 'polybutene: role (base fluid / VM / tackifier) not stated on page 1'
        else:
            mc, n = 'additive_component', "printed 'chlorinated wax paraffin' (application not printed on page 1)"
        PK['INEOS:' + k] = dict(name=k.title().replace('Cp', 'CP'), supplier=SUP, material_class=mc, existing_record='', status='new_candidate', notes=n,
                                identity_evidence='printed product name / grade on the documents linked in this batch',
                                template={'base_oil': 'base_oil tier1-3 (Group IV PAO)', 'additive_component': 'additive_component general'}.get(mc, 'not determined'))
for k in ('INDOPOL H-100 CP', 'INDOPOL H-300 C', 'INDOPOL H-300 CP', 'INDOPOL H-1200 CP'):
    PK['INEOS:' + k]['notes'] += '; grade printed only in a multi-grade SDS title'
out = dict(batch='S12 INEOS (identity)', reviewed_on='2026-11-14', scope='55 documents with provisional supplier INEOS', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's12_ineos.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['material_class'] for p in PK.values()))
print(sorted(k[6:] for k in PK))
