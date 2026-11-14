"""Supplier batch S11: Clariant (73 documents with provisional supplier 'Clariant').
Read: compact page-1 listing of all 73 documents; 6 longer cards (600 characters).
Rules
- Subject = trade name printed on page 1 (TDS / SDS title, or the product name in a clariant.com web-page printout / URL).
- Grade spelling normalised only for spacing ('Polyglykol B01/240' = 'POLYGLYKOL B 01/240'); printed suffixes kept as separate
  products ('B 11/150 K'; 'P 41/12000 M 80 N' (80 % aqueous dilution) is NOT merged with the web page 'Polyglykol P 41/12000').
- Several Chinese-site TDSs (CLARIANT CHEMICALS (CHINA)) have a font-shifted text layer ('9HUVLRQ-DQ' = 'Version Jan'); the product
  names are legible and were used; dates on them must be read from the page image.
- Class from the printed composition / descriptor and brand family: Polyglykol PAGs -> base_oil candidates (template fit to confirm:
  no API group); Hostagliss / Hordaphos / Hostacor / Emulsogen / Emulchem / Arkomon / Nipacide / Lubricant Additive 1655 N /
  Inhibitor Concentrate HFC -> additive components with an application-scope question (many are for water-based metalworking or
  HFC fluids); Hostagel HT 300 (grease thickener) and Genamin 8 R 100 D (raw material for de-watering fluids) -> other chemicals;
  Antifrogen brines -> heat-transfer / coolant (out of template).
Identity only. Writes decisions/s11_clariant.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Clariant')]
SUP = 'Clariant'
BR = r'(POLYGLYKOL|HOSTAGLISS|HOSTACOR|HOSTAGEL|HORDAPHOS|EMULSOGEN|EMULCHEM|GENAMIN|LUBRICANT ADDITIVE|INHIBITOR CONCENTRATE|ANTIFROGEN|NIPACIDE|ARKOMON)'
NAME = re.compile(r'(?i)' + BR + r'[®\s-]*([A-Z0-9][A-Z0-9 /.-]{0,24}?)(?=\s*(?:\||$|January|February|April|May|June|November|Version|Page|\?p=|\(low| https|\s{2})|[ -]\d{1,2}/\d{1,2}/\d{4})')
MULTI = {'74a8671e03': "'Synthetic Base Fluid Selection Guide - industrial lubricants'", '59736a6e60': "'Base fluids and additives for Fire-resistant Hydraulic Fluids'",
         '092358ddfd': "'Base fluids and additives for Fire-resistant Hydraulic Fluids' (different bytes)", 'b14547613e': "'INDUSTRIAL LUBRICANTS Corrosion Inhibitor Selection Guide'",
         'b3a5bc084b': "'Components for HFC HYDRAULIC FLUIDS'"}
OV = {'38433b3ba3': 'ARKOMON SO', 'b8c30a8830': 'ANTIFROGEN KF VP 1974', 'ec126af9cd': 'ANTIFROGEN N', '273eec9a8f': 'ANTIFROGEN L', 'ab73a4b747': 'POLYGLYKOL P 41/12000',
      '23ec7a64cf': 'EMULSOGEN MS 12', '756de3d77c': 'EMULSOGEN LP', 'df65cb77d1': 'HORDAPHOS MDHX', 'fdf56dc9de': 'HORDAPHOS MDAH', '40d74d2427': 'NIPACIDE BIT 20',
      'a09f690019': 'HOSTACOR DT', '94e03cb9e1': 'HOSTACOR MT', 'e5f1b65151': 'EMULSOGEN M', '52770ea1da': 'LUBRICANT ADDITIVE 1655 N', '4be9a94db3': 'LUBRICANT ADDITIVE 1655 N',
      '3b8ad6b194': 'LUBRICANT ADDITIVE 1655 N', '48fbdc7325': 'LUBRICANT ADDITIVE 1655 N', '2fc82241fb': 'INHIBITOR CONCENTRATE HFC', 'b7ba4de7ce': 'POLYGLYKOL P 41/12000 M 80 N',
      '8669fb9d17': 'EMULSOGEN MTP 070', 'f0ad2e3041': 'POLYGLYKOL B 11/150 K'}
CLS = {'POLYGLYKOL': ('base_oil', 'polyalkylene glycol base fluid (base_oil template fit to confirm: no API group)'),
       'HOSTAGEL': ('out_of_template: other chemical', "printed 'Thickening agent for lubricating greases'"),
       'GENAMIN': ('out_of_template: other chemical', "printed 'Raw material for de-watering fluids with corrosion inhibiting properties' (octylamine)"),
       'ANTIFROGEN': ('out_of_template: heat transfer fluid / coolant', 'heat-transfer medium / brine'),
       'ARKOMON': ('additive_component', "printed 'Oil-soluble corrosion inhibitor' (oleoyl sarcoside)"),
       'LUBRICANT ADDITIVE': ('additive_component', "printed 'Corrosion inhibitor, ageing protecting agent and extreme pressure/anti wear additive ... for non-aqueous lubricants based on polyalkylene glycols'")}


def canon(k):
    k = re.sub(r'\s+', ' ', k.upper().replace('-', ' ')).strip()
    k = re.sub(r'POLYGLYKOL ([A-Z])(\d)', r'POLYGLYKOL \1 \2', k)
    k = re.sub(r'(\d) (\d)', r'\1\2', k) if not k.startswith('POLYGLYKOL') else k
    return k


D, PK = {}, {}
for r in A:
    sha, t = r['sha256'], r['top_lines'].replace('\n', ' | ')
    p10 = sha[:10]
    if p10 in MULTI:
        D[sha[:12]] = dict(doc_type='brochure / selection guide (multi-product)', supplier=SUP, products=[], roles={}, relation='product', read='page-1 listing',
                           note=MULTI[p10], next_action='list the products inside (multi-product)')
        continue
    if p10 in OV:
        key = OV[p10]
    else:
        m = NAME.search(t)
        key = canon(m.group(1) + ' ' + m.group(2)) if m else ''
    web = 'clariant.com/en/Solutions' in t
    typ = 'SDS' if re.search(r'(?i)safety data sheet', t) else ('manufacturer web-page printout' if web else ('product information brochure' if 'Product description' in t else 'product data sheet (TDS/PDS)'))
    note = 'font-shifted text layer (dates unreadable in text)' if '9HUVLRQ' in t else ''
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['CLARIANT:' + key] if key else [], roles={'CLARIANT:' + key: 'subject'} if key else {},
                       relation='product' if key else 'unresolved_identity', read='page-1 listing' + ('; longer card' if p10 in ('38433b3ba3', 'b8c30a8830', '3b8ad6b194', 'b7ba4de7ce', 'e4b92b2fc2', '8190667c6a') else ''),
                       note=note, next_action='' if key else 'identify the product')
    if key and 'CLARIANT:' + key not in PK:
        br = next((b for b in CLS if key.startswith(b)), None)
        mc, n = CLS[br] if br else ('additive_component', 'component by brand family / printed composition; application scope (metalworking / water-based HFC) to confirm')
        PK['CLARIANT:' + key] = dict(name=key, supplier=SUP, material_class=mc, existing_record='', status='out_of_scope' if mc.startswith('out_of') else 'new_candidate', notes=n,
                                     identity_evidence='printed product name on the documents linked in this batch',
                                     template={'additive_component': 'additive_component general', 'base_oil': 'base_oil tier1-3 (template fit to confirm)'}.get(mc, 'none'))
PK['CLARIANT:POLYGLYKOL P 41/12000']['notes'] += "; web-page name; NOT merged with 'P 41/12000 M 80 N' (80 % aqueous dilution, printed 'Base oil component')"
out = dict(batch='S11 Clariant (identity)', reviewed_on='2026-11-14', scope='73 documents with provisional supplier Clariant', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's11_clariant.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['material_class'] for p in PK.values()))
print(sorted(k[9:] for k in PK))
print([s for s, v in D.items() if v['relation'] != 'product'])
