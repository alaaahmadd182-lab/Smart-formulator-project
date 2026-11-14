"""Supplier batch S16: Kusa Chemicals Pvt. Ltd. (Mumbai / Godhra; 46 documents).
Read: compact listing; page-1 text after the letterhead for every non-certificate document (name + printed descriptor); SDS
'Product name' field for 2 SDSs; 'PRODUCT NAME' / 'CUSTOMER NAME' fields of all 20 NT-415 test reports (OCR / text layer).
Rules: subject = printed name. 'NT-415' / 'NT 415' / 'NT415' (20 batch test reports, 2019) are one printed code; the customer
name field is blank in every report and the product type is not printed, so NT-415 stays class-unresolved (a 'VII' string in
three reports is not used for the class without review). NT-415 is NOT linked to Sama's NT-series codes (no printed evidence).
KUSACRYL 2231 uses key KUSA:KUSACRYL 2231 (also linked from a Sama technical report in S08).
Classes: Kusapour (alkyl methacrylate polymer solution 'recommended for use as a Pour Point Depressant') -> component, PPD;
Kusacryl ('VI Improver', alkyl methacrylate polymer) -> component, VM; Kunox (aminic antioxidant) -> component; Vicol 5005 / 6006 /
VCH (metalworking emulsifiers) -> component with metalworking scope question; Vicol S50 'Package for Neat Cutting Oils' ->
package with metalworking scope question. Identity only. Writes decisions/s16_kusa.json."""
import csv, json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Kusa')]
SUP = 'Kusa Chemicals Pvt. Ltd.'
OV = {'4a92bee7d4': 'VICOL 6006', '79170183da': 'VICOL 5005', '3c97802430': 'KUSACRYL V20', '6106832e30': 'KUSACRYL 835',
      '3c01e36eca': 'NT-415', 'd016e4cd96': 'NT-415', 'd396b65776': 'NT-415'}
CL = {'KUSAPOUR': ('additive_component', "alkyl methacrylate polymer solution 'recommended for use as a Pour Point Depressant' (PPD subtype)"),
      'KUSACRYL': ('additive_component', "alkyl methacrylate polymer 'VI Improver' (VM subtype)"),
      'KUNOX A8000': ('additive_component', "'octylated/butylated Aminic Antioxidant'"), 'KUNOX A9000': ('additive_component', "'nonylated Aminic Antioxidant'"),
      'VICOL S50': ('additive_package', "'Package for Neat Cutting Oils' (metalworking: scope question)"),
      'VICOL': ('additive_component', 'metalworking emulsifier (scope question)'),
      'NT-415': ('unresolved', 'batch test reports only; product type and customer not printed')}
D, PK = {}, {}
for r in A:
    sha, t, p10 = r['sha256'], r['top_lines'], r['sha256'][:10]
    key = OV.get(p10) or r['primary_identity'].upper().replace('NT 415', 'NT-415').replace('NT415', 'NT-415').strip()
    sds = 'SAFETY DATA SHEET' in t.upper()
    typ = 'SDS' if sds else ('batch test report (certificate)' if key == 'NT-415' else 'product data sheet (TDS/PDS)')
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['KUSA:' + key], roles={'KUSA:' + key: 'subject'}, relation='product', read='page-1 text / name field',
                       note='', next_action='')
    if 'KUSA:' + key not in PK:
        mc, n = next(v for k, v in CL.items() if key.startswith(k))
        PK['KUSA:' + key] = dict(name=key, supplier=SUP, material_class=mc, existing_record='', status='new_candidate', notes=n,
                                 identity_evidence='printed product name on the documents linked in this batch',
                                 template={'additive_component': 'additive_component general (+ subtype as noted)', 'additive_package': 'additive_package tier1 + tier2'}.get(mc, 'not determined'))
out = dict(batch='S16 Kusa Chemicals (identity)', reviewed_on='2026-11-14', scope='46 documents with provisional supplier Kusa Chemicals', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's16_kusa.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()), sorted(k[5:] for k in PK))
