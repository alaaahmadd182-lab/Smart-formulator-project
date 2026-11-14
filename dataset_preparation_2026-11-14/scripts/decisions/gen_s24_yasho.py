"""Supplier batch S24: Yasho Industries Limited (YALUB / YAPOX; 27 documents).
Read: compact listing; SDS 'Product Name' fields; DL2-13410 / 13414 / 13419 page 1 viewed (names printed as graphics:
'YALUB LA', 'YALUB NA-A', 'YALUB ZDD').
Rules: subject = printed trade name ('YALUB(R)LA' = 'YALUB LA'). Each TDS has an SDS of the same name.
Recorded printed inconsistency (blocker for using the SDS): the YALUB ZDD TDS prints composition 'Zinc Diamyldithiocarbamate in 50%
oil', while the YALUB ZDD SDS (sha 2051c7f920) prints 'Chemical Name: 2,5-Dimercapto-1,3,4-thiadiazol...' - not resolved.
YAPOX 50% TTZ (name from the text 'YAPOX(R)50%TTZ'; product type not printed in the inspected text) -> class unresolved.
YALUB grades are lubricant additive components (friction modifier, antioxidant, metal deactivator ...).
Identity only. Writes decisions/s24_yasho.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Yasho')]
SUP = 'Yasho Industries Limited'
OV = {'20ba71d4af': 'YALUB LA', '2ef1341107': 'YALUB LA', 'fecc8bd8bd': 'YALUB NA-A', '93725f6c81': 'YALUB NA-A', 'd3381d66b0': 'YALUB ZDD', '2051c7f920': 'YALUB ZDD',
      'dfca323680': 'YAPOX 50% TTZ'}
NOTES = {'2051c7f920': "SDS prints 'Chemical Name: 2,5-Dimercapto-1,3,4-thiadiazol...' while the YALUB ZDD TDS prints 'Zinc Diamyldithiocarbamate in 50% oil': printed inconsistency, blocker for using this SDS",
         'd3381d66b0': "TDS composition 'Zinc Diamyldithiocarbamate in 50% oil' (page image viewed); see the SDS conflict"}
D, PK = {}, {}
for r in A:
    sha, p10, t = r['sha256'], r['sha256'][:10], r['top_lines']
    key = OV.get(p10) or re.sub(r'\s+', ' ', r['primary_identity'].upper()).strip()
    k = 'YASHO:' + key
    typ = 'SDS' if 'SAFETY DATA SHEET' in t else 'product data sheet (TDS/PDS)'
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=[k], roles={k: 'subject'}, relation='product',
                       read='page-1 listing / SDS product-name field' + ('; page image viewed' if p10 in ('20ba71d4af', 'fecc8bd8bd', 'd3381d66b0') else ''),
                       note=NOTES.get(p10, ''), next_action='blocker: resolve the SDS / TDS composition disagreement before using the SDS' if p10 == '2051c7f920' else '')
    if k not in PK:
        mc = 'unresolved' if key.startswith('YAPOX') else 'additive_component'
        PK[k] = dict(name=key, supplier=SUP, material_class=mc, existing_record='', status='new_candidate',
                     notes='product type not printed in the inspected text' if mc == 'unresolved' else 'lubricant additive component (function as printed on its TDS)',
                     identity_evidence='printed trade name on the documents linked in this batch', template='additive_component general' if mc != 'unresolved' else 'not determined')
PK['YASHO:YALUB ZDD']['notes'] += '; TDS / SDS composition disagree (see document notes)'
out = dict(batch='S24 Yasho (identity)', reviewed_on='2026-11-14', scope='27 documents with provisional supplier Yasho Industries', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's24_yasho.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', sorted(PK))
