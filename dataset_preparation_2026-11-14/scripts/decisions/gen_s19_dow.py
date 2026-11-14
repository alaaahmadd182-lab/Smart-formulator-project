"""Supplier batch S19: provisional label 'Dow' (35 documents). Two different companies:
- Dowpol Chemical International Corp. (Shanghai; brand 'DowSyn'): 32 documents. Dowpol is NOT asserted to be related to Dow.
- The Dow Chemical Company: DOWTHERM A heat-transfer fluid TDS, 'UCON OSP Fluids' brochure, 'Fluids and Lubricants' catalogue.
Read: compact listing; page-1 text after the Dowpol letterhead for the 7 documents without an automated identity.
Rules: subject = 'DowSyn <grade>' as printed ('VM 9777' = 'VM9777' spacing only; 'PAO2' and 'PAO2B' separate). The two
'DowSyn Alkylated Naphthalene' family sheets are multi-product (grades not listed on page 1).
Classes: DowSyn PAO -> base_oil (Group IV); 'V600' / 'V1000' (certificate + SDS only) -> class unresolved; DowSyn AN (alkylated naphthalene) -> base_oil candidate
(Group V synthetic, template fit to confirm); DowSyn VM200 / VM260 (hydrogenated styrene-diene star polymer) and VM 9777 (PMA VII)
-> component, VM; DowSyn PB2400 (polybutene) -> class unresolved; DOWTHERM A -> out of template (heat transfer fluid).
DowSyn VM200 TDS carries existing-comparison links to YUBASE_4 / YUBASE_6 from the earlier workstream (kept as recorded there).
Identity only. Writes decisions/s19_dow.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Dow']
DOWPOL, DOW = 'Dowpol Chemical International Corp. (DowSyn)', 'The Dow Chemical Company'
OV = {'857163c479': 'PAO2', '1d0cf30a8c': 'PAO2', '3831c4cc4a': 'PAO2B', '82b809812d': 'PAO6', 'b38b1aaeed': 'PAO4'}
MULTI = {'455eadbb73': (DOWPOL, "'DowSyn Alkylated Naphthalene' family sheet (April 2018)"), '3e0da48df1': (DOWPOL, "'DowSyn Alkylated Naphthalene' family sheet (April 2018; different bytes)"),
         '652fdec215': (DOW, "'UCON OSP Fluids - Oil-soluble polyalkylene glycol lubricant technology' brochure"), '9ab95de537': (DOW, "'Fluids and Lubricants' catalogue (47 pp)")}


def cls(g):
    if g.startswith('PAO'): return 'base_oil', 'polyalphaolefin (API Group IV)'
    if g.startswith(('V6', 'V1')): return 'unresolved', 'product type not printed on the documents read (certificate of analysis and SDS header only); not inferred from the name'
    if g.startswith('AN'): return 'base_oil', 'alkylated naphthalene synthetic base fluid (template fit to confirm: Group V)'
    if g.startswith('VM'): return 'additive_component', 'viscosity modifier (VM subtype)'
    if g.startswith('PB'): return 'unresolved', 'polybutene: role not stated'
    return 'unresolved', ''


D, PK = {}, {}
for r in A:
    sha, p10, t = r['sha256'], r['sha256'][:10], r['top_lines']
    if p10 in MULTI:
        sup, note = MULTI[p10]
        D[sha[:12]] = dict(doc_type='brochure / family sheet (multi-product)', supplier=sup, products=[], roles={}, relation='product', read='page-1 listing / text',
                           note=note, next_action='list the products inside (multi-product)')
        continue
    if p10 == '1826d9008b':
        k = 'DOW:DOWTHERM A'
        D[sha[:12]] = dict(doc_type='product data sheet (TDS/PDS)', supplier=DOW, products=[k], roles={k: 'subject'}, relation='product', read='page-1 listing', note='', next_action='')
        PK[k] = dict(name='DOWTHERM A', supplier=DOW, material_class='out_of_template: heat transfer fluid', existing_record='', status='out_of_scope',
                     notes="printed 'Synthetic organic heat transfer fluid - Liquid and Vapor Phase'", identity_evidence='printed name', template='none')
        continue
    g = OV.get(p10) or re.sub(r'(?i)^DowSyn\s*', '', r['primary_identity'].replace('02 TDS ', '').replace(' EN V2', '')).replace(' ', '').upper()
    k = 'DOWPOL:DOWSYN ' + g
    D[sha[:12]] = dict(doc_type='SDS' if 'SAFETY DATA SHEET' in t.upper()[:200] or p10 == '1d0cf30a8c' else ('certificate of analysis (batch)' if p10 in ('65c1444bbb', '0b6cf4886d') else 'product data sheet (TDS/PDS)'), supplier=DOWPOL, products=[k], roles={k: 'subject'},
                       relation='product', read='page-1 listing / text', note='', next_action='')
    if k not in PK:
        mc, n = cls(g)
        PK[k] = dict(name='DowSyn ' + g, supplier=DOWPOL, material_class=mc, existing_record='', status='new_candidate', notes=n,
                     identity_evidence='printed product name on the documents linked in this batch',
                     template={'base_oil': 'base_oil tier1-3', 'additive_component': 'additive_component general (+ VM subtype)'}.get(mc, 'not determined'))
out = dict(batch='S19 Dowpol (DowSyn) / Dow (identity)', reviewed_on='2026-11-14', scope="35 documents with provisional supplier 'Dow'", products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's19_dow.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()), sorted(PK))
