"""Supplier batch S14: ExxonMobil (48 documents with provisional supplier 'ExxonMobil').
Read: compact page-1 listing; 6 longer cards; DL2-13129 and DL2-15014 page 1 viewed (names only in graphics / beyond the card).
Most documents are byte duplicates of old-archive sources of existing EXXONMOBIL_* records; their product links come from the
existing-comparison ledger (existing_product_comparison_2026-11-12) and are re-stated here as identity decisions:
- one linked record -> role 'subject'; several (EHC Series, AP/E Core, blending study, product list) -> 'series / multi-grade sheet'.
Additional decisions: DL2-13129 = 'SpectraSyn Polyalphaolefins (PAO), 40 and 100 cSt' (2003 PDS, two grades); DL2-15467 = AP/E Core
sheet for 'ExxonMobil Basestocks, Egypt' listing CORE 100 / 150 / 600 / 2500 (regional sheet: applicability to the existing records
to be reviewed, not assumed); DL2-15014 = Exxsol D60 hydrocarbon fluid sales specification and DL2-12988 = Exxsol D80 dearomatized
fluid (solvents: out of template); Vistamaxx 6202 (propylene elastomer) out of template; Exxon IT0316 ethylene propylene copolymer
rubber -> component (VM use not printed on page 1); DL2-13502-like LANXESS report 'RC 9200 N' -> LANXESS:ADDITIN RC 9200 N.
Identity only. Writes decisions/s14_exxonmobil.json."""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = {r['sha256']: r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('ExxonMobil')}
REG = {d['sha256']: d for d in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_register.csv'), encoding='utf-8')) if d['sha256'] in A}
SUP = 'ExxonMobil'
APE = ['EXXONMOBIL_APE_CORE_100', 'EXXONMOBIL_APE_CORE_150', 'EXXONMOBIL_APE_CORE_600', 'EXXONMOBIL_APE_CORE_2500']
OV = {'f4fd219df7': (['EXXONMOBIL_SPECTRASYN_40', 'EXXONMOBIL_SPECTRASYN_100'], 'product data sheet (TDS/PDS)', "2003 PDS 'SpectraSyn Polyalphaolefins (PAO), 40 and 100 cSt' (page image viewed)"),
      '4f4b206be5': (APE, 'product data sheet (TDS/PDS)', "AP/E Core sheet, 'ExxonMobil Basestocks, Egypt' (grades CORE 100 / 150 / 600 / 2500 printed): regional applicability to the existing records to be reviewed"),
      '6c668ceb31': (['EXXONMOBIL:EXXSOL D60'], 'sales specification', "'Exxsol D60 Hydrocarbon Fluid' sales specification effective 01 Oct 2014 (page image viewed)"),
      'a441ee2dd4': (['EXXONMOBIL:EXXSOL D80'], 'product data sheet (TDS/PDS)', "'Exxsol D80 Dearomatized Fluid'"),
      '086ffe1830': (['EXXONMOBIL:VISTAMAXX 6202'], 'product data sheet (TDS/PDS)', "'Vistamaxx Performance Polymer 6202 - Propylene Elastomer'"),
      'c9c76741a1': (['EXXONMOBIL:EXXON IT0316'], 'product data sheet (TDS/PDS)', "'Exxon IT0316 Ethylene Propylene Copolymer Rubber'"),
      'd550734093': (['LANXESS:ADDITIN RC 9200 N'], 'technical report (performance data)', "LANXESS 'RC 9200 N (HVLP, group I + II)' technical report, Edition September 2018, filed under ExxonMobil by the automated label")}
NEW = {'EXXONMOBIL:EXXSOL D60': ('out_of_template: other chemical', 'hydrocarbon solvent'), 'EXXONMOBIL:EXXSOL D80': ('out_of_template: other chemical', 'dearomatized hydrocarbon solvent'),
       'EXXONMOBIL:VISTAMAXX 6202': ('out_of_template: other chemical', 'propylene elastomer (polymer)'),
       'EXXONMOBIL:EXXON IT0316': ('additive_component', "'Ethylene Propylene Copolymer Rubber' (VM use not printed on page 1)")}
D, PK = {}, {}
for sha, a in A.items():
    p10 = sha[:10]
    if p10 in OV:
        prods, typ, note = OV[p10]
    else:
        prods = [p.strip() for p in REG[sha]['existing_comparison_products'].split('|') if p.strip()]
        typ = 'SDS' if 'Product Name:' in a['top_lines'] else ('blending study' if 'Blending Study' in a['top_lines'] else ('product list (spreadsheet)' if a['kind'] in ('xlsx', 'xls') or not a['pages'] else 'product data sheet (TDS/PDS)'))
        note = 'links as in the existing-comparison ledger'
    keys = [p if ':' in p else 'EXISTING:' + p for p in prods]
    role = 'subject' if len(keys) == 1 else 'series / multi-grade sheet (grade listed)'
    sup = 'LANXESS (Rhein Chemie)' if p10 == 'd550734093' else SUP
    D[sha[:12]] = dict(doc_type=typ, supplier=sup, products=keys, roles={k: role for k in keys}, relation='product' if keys else 'unresolved_identity',
                       read='page-1 listing' + ('; page image viewed' if p10 in ('f4fd219df7', '6c668ceb31') else ''), note=note, next_action='' if keys else 'identify the product')
for k, (mc, n) in NEW.items():
    PK[k] = dict(name=k.split(':')[1].title().replace('Exxon It0316', 'Exxon IT0316'), supplier=SUP, material_class=mc, existing_record='', status='out_of_scope' if mc.startswith('out_of') else 'new_candidate',
                 notes=n, identity_evidence='printed product name', template='additive_component general' if mc == 'additive_component' else 'none')
out = dict(batch='S14 ExxonMobil (identity)', reviewed_on='2026-11-14', scope='48 documents with provisional supplier ExxonMobil', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's14_exxonmobil.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'new products', Counter(v['relation'] for v in D.values()), len({k for v in D.values() for k in v['products'] if k.startswith('EXISTING:')}), 'existing records linked')
