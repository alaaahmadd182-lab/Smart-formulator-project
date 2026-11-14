"""Supplier batch S02: Afton Chemical (305 documents whose provisional supplier is 'Afton Chemical').
Read: the page-1 identity card of every document (cards.py, 170 characters), longer cards (700 characters) for 38 documents,
and the page-1 header images of DL2-14233, DL2-14266, DL2-12471.
Rule applied (checked card by card): the subject product is the first HiTEC / OTR / Axcel code printed in the page-1 title
(first 600 characters, or the 'Product' field of a certificate); further codes in the same title are recorded as 'mentioned'.
Document type from page-1 markers (SDS heading, certificate heading, 'Sales Specification Sheet', 'Report No' technical report,
two-page bulletins with the Afton section banner). Explicit overrides below where the rule does not hold.
Identity only: no property values are taken. Writes decisions/s02_afton.json."""
import json, os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)
import csv
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Afton Chemical']
SUP = 'Afton Chemical'
R = 'page-1 identity card (text layer) read'
EXIST = {'12010': 'AFTON_HITEC_12010', '12200': 'AFTON_HITEC_12200', '12204L': 'AFTON_HITEC_12204L', '12208': 'AFTON_HITEC_12208', '12210': 'AFTON_HITEC_12210',
         '12210M': 'AFTON_HITEC_12210M', '12250': 'AFTON_HITEC_12250', '12360': 'AFTON_HITEC_12360', '12400': 'AFTON_HITEC_12400', '5748': 'AFTON_HITEC_5748',
         '8712': 'AFTON_HITEC_8712', '8767B': 'AFTON_HITEC_8767B', '8788B': 'AFTON_HITEC_8788B', '8799B': 'AFTON_HITEC_8799B', '8766B': 'HiTEC_8766B'}
COMPONENT = {'5724': 'PMA VI improver (VM subtype)', '5710': 'dispersant PMA VI improver (VM subtype)', '5748': 'OCP VM (existing record)', '5751': 'OCP VI improver (VM)',
             '5754A': 'OCP VI improver (VM)', '5777': 'dispersant OCP VI improver (VM)', '5825H': 'solid OCP VI improver (VM; solid polymer)', '5825K': 'solid OCP VM',
             '5835A': 'OCP (mentioned only)', '2030': 'non-silicone antifoam', '4716': 'organomolybdenum friction modifier', '511T': 'ashless AW / EP agent',
             '686': 'calcium phosphate-phenate detergent', '12250': 'HDEO booster (existing record filed as additive_component)',
             '12255': 'HDEO booster (filed like the existing HiTEC 12250 record)', '12260': 'HDDEO booster (filed like HiTEC 12250)', '9310': 'PCMO booster for HiTEC 9300',
             '7133': 'friction-modifier booster', '5748A': 'OCP VM (distinct from HiTEC 5748)'}
FUEL = ('4133G', '4139G', '6431')
CODE = re.compile(r'(?i)\b(HiTEC|OTR)\s*[®@]?\s*(\d{3,5}(?:/\d{2})?[A-Z]{0,3}\d?)\b')

FIX = {'87888': '8788B', '932SC': '9325C', '930': None}  # OCR / text-layer artefacts seen on the cards (8788B, 9325C; '930' is a fragment)


def norm(brand, code):
    code = code.upper()
    if code in FIX:
        if FIX[code] is None:
            return None
        code = FIX[code]
    return f"{'HiTEC' if brand.lower() == 'hitec' else 'OTR'} {code}"

def cls_of(key):
    b, code = key.split(' ', 1)
    if b == 'OTR' or code in FUEL:
        return 'out_of_template: fuel additive', 'fuel additive: no lubricant raw-material template (schema gap; excluded from conversion unless the scope is widened)'
    if code in COMPONENT:
        return 'additive_component', COMPONENT[code]
    return 'additive_package', ''

def dtype(p1, pages, f):
    h = p1[:400]
    if re.search(r'(?i)safety data sheet|material safety', h): return 'SDS'
    if re.search(r'(?i)certificate of analysis', h): return 'certificate of analysis (batch)'
    if 'Sales Specification Sheet' in h or 'Global Sales Specification' in h: return 'sales specification sheet'
    if re.search(r'(?i)packing list|delivery note', h): return 'shipping document'
    if re.search(r'Report N(?:o|umber)', h + (pages[1][:400] if len(pages) > 1 else '')): return 'technical report (performance data)'
    if re.search(r'E N G I N E|D R I V E L I N E|C O M P O N E N T S|I N D U S T R I A L|F U E L S|V I S C O S I T Y|M e t a l|\b(?:TURBINE|GEAR|HYDRAULIC|GREASE|SLIDEWAY)\b', h) and int(pages and len(pages) or 0) <= 2:
        return 'product bulletin (TDS/PDS)'
    if len(pages) <= 2 and re.search(r'(?i)(?<![A-Za-z])Application(?![A-Za-z])', h):
        return 'product bulletin (TDS/PDS)'
    return 'presentation / formulation data'

D, PK = {}, {}
OV = {  # sha prefix -> (doc_type or None, products [subject first], note, relation)
 '0157a3055b': (None, ['HiTEC 12200'], "certificate printed 'Product: GE220 (HiTEC 12200)'; GE220 is a customer code printed as HiTEC 12200; issuer not printed on the card", None),
 'e8714d199d': (None, ['HiTEC 12200'], "certificate 'Product: GE220' (material 030231); GE220 is printed as 'GE220 (HiTEC 12200)' on the companion certificates", None),
 '7dbaeece35': (None, ['P3010'], "certificate 'Product: P3010'; issuer / manufacturer not printed on the card (supplier unresolved)", None),
 'caf90b46d1': (None, ['P3010'], "certificate 'Product: P3010'; issuer not printed on the card", None),
 'ddfdf0c88e': (None, [], "Afton certificate (material 011581, lot 0220SA006): the 'Product' field is blurred / redacted on the page image", 'unresolved_identity'),
 'f3fe139685': (None, [], 'Afton certificate (material 026067, lot 0120SN015): no product name printed in the header (page image viewed)', 'unresolved_identity'),
 'cc2f6ded30': (None, ['Axcel S'], "bulletin 'Axcel® S Automotive Gear Oil Additive Package' (name printed as graphics; page image viewed)", None),
 '884563cea3': (None, ['UA4158'], "Afton certificate to United Oil Company (Singapore) 'Product: UA4158' (customer product code)", None),
 'f19b6447f7': (None, ['UA4159'], "Afton certificate to United Oil Company 'Product: UA4159'", None),
 '81f417ef68': (None, ['UA4159'], "Afton certificate 'Product: UA4159'", None), 'c5788c483c': (None, ['UA4159'], "Afton certificate 'Product: UA4159'", None),
 '18d8601031': ('SDS', ['UA4159'], "Afton SDS 'UA4159' (SDS no. UA4159)", None),
 '570dfe73a5': ('product bulletin (TDS/PDS)', ['Jilin J0030', 'HiTEC 5835A'], "sheet of 'Jilin J0030' solid OCP VI improver (PetroChina Jilin; not an Afton product); HiTEC 5835A only mentioned", None),
 'cf360d1e30': ('journal article', [], "'International Journal of Energy Engineering 2018' literature review on metal-based octane boosters: not a product document", 'non_product'),
 '37245348b3': ('letter (formulation data)', ['HiTEC 579'], "'To whom it may concern' letter with HiTEC 579 quench-oil formulation data", None),
 '41887a61c9': ('shipping document', ['HiTEC 9387X'], 'packing list / delivery note (HiTEC 9387X Bulk, batch 0419FB640)', None),
 '95a83e8b76': ('presentation / formulation data', [], "'Afton HDEO Technology for PC-11' presentation: no single subject product on page 1", None),
 '342651a88d': ('presentation / formulation data', [], "'Afton Chemical ILSAC GF-5 Technology August 2012' presentation", None),
 '0a6d75c250': ('presentation / formulation data', [], "'Next generation PCMO solutions ILSAC GF-7 / API SQ & JASO GLV-1, GLV-2' (same title as DL2-15688)", None),
 '3f22898875': ('presentation / formulation data', [], "same title as DL2-15678 (different bytes)", None),
 '63249a25cc': ('formulation data', ['HiTEC 11455'], "'API SQ/GF-7A formulations aramcoULTRA/Ultra-S' with HiTEC 11455 (2025)", None),
 '673c5b0d74': ('presentation (Chevron base oils)', [], "'Afton Automotive Product Qualification Summary' by Chevron base oils (December 2018): Afton products qualified in Chevron Group II", None),
 'd3a191a915': ('presentation / formulation data', ['HiTEC 9490', 'HiTEC 12200', 'HiTEC 8788B'], "'German Mirror OEM Request Product information and Formulations' (read for base-oil links in batch 35)", None),
 '7e0eb4b743': ('formulation data', ['HiTEC 9325G'], 'formulation table (Luberef / BPCL / Chevron base oils)', None),
 'b97324eff1': (None, ['HiTEC 349'], "bulletin 'HiTEC® 349 Manual Transmission Fluid Additive Package'", None),
 'd8c1db6360': ('formulation data', ['HiTEC 11456'], "'Final Formulations' with ETRO plus base oils (20211224); reviewed in the existing-product comparison", None),
 '322ef6165e': ('claims summary', ['HiTEC 34321'], 'claim / performance supporting-data table', None),
 '0192a82054': ('formulation data', ['HiTEC 12204L', 'HiTEC 5748'], 'candidate data package API CI-4 PLUS / SL (May-19)', None),
 'cebc17117d': (None, ['HiTEC 8705'], "bulletin 'HiTEC® 8705 Off Road Additive Package'", None),
 'c9d74e812d': (None, ['HiTEC 3491K'], "bulletin 'HiTEC® 3491K ATF Additive Package'", None),
 '818c980a3a': (None, ['HiTEC 8703'], "bulletin 'HiTEC® 8703 Off-road Additive Package'", None),
 '3b9c333576': ('product bulletin (TDS/PDS)', ['HiTEC 344'], "bulletin 'HiTEC® 344 Automotive only Gear Oil Additive' (text also prints 'GA 2419 additive'; recorded as printed)", None),
 '637139fca0': ('product bulletin (TDS/PDS)', ['APL'], "bulletin 'APL™ Synthetic Lubricity Improver Additive' (metalworking fluids)", None),
 **{k: ('certificate of analysis (batch)', ['HiTEC 343'], "Afton certificate 'HiTEC ® 343 Drum' (the certificate heading is not in the text layer)", None) for k in ('66401b5be2', 'c15892bee1', 'd9129b7f9a', 'd213829e46', '8cb07d1093')},
 'b8bc9294db': ('product bulletin (TDS/PDS)', ['HiTEC 382'], 'one-page bulletin (OCR-damaged text: HiTEC 382 Gear Oil Additive Top Treat)', None),
 '00e78e5f7c': ('product bulletin (TDS/PDS)', ['HiTEC 382'], 'same content as DL2-11635 (different bytes)', None),
}
for r in A:
    sha = r['sha256']
    pages, _ = ident.pages_for(sha)
    p1 = re.sub(r'\s+', ' ', pages[0] if pages else '')
    ov = next((v for k, v in OV.items() if sha.startswith(k)), None)
    typ = dtype(p1, pages, r['first_path'])
    if ov:
        prods, note, rel = ov[1], ov[2], ov[3] or ('product' if ov[1] else 'product')
        typ = ov[0] or typ
    else:
        src = p1[:600]
        if typ.startswith('certificate'):
            m = re.search(r'Product\s*:?\s*(?:[^A-Za-z]{0,40})?(HiTEC\s*®?\s*\d{3,5}[A-Z]{0,3})', p1)
            src = m.group(1) if m else p1
        if typ == 'SDS' and len(pages) > 1:
            src = p1[:300]
        prods = [x for x in dict.fromkeys(norm(m.group(1), m.group(2)) for m in CODE.finditer(src)) if x]
        note, rel = '', 'product' if prods else 'unresolved_identity'
    roles = {p: 'mentioned' for p in prods[1:]}
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP if not prods or not prods[0].startswith('Jilin') else 'PetroChina Jilin (named on the sheet)', products=prods,
                       relation=rel, read=R, note=note, roles=roles, date='',
                       next_action='' if prods or rel == 'non_product' else 'identify the subject products (multi-product presentation) in the package review')
    for p in prods:
        if p in PK: continue
        code = p.split(' ', 1)[1] if ' ' in p else p
        if p.startswith(('HiTEC', 'OTR')):
            c, n = cls_of(p)
            PK[p] = dict(name=p, supplier=SUP, material_class=c, existing_record=EXIST.get(code, '') if p.startswith('HiTEC') else '', notes=n)
        elif p == 'Axcel S':
            PK[p] = dict(name='Axcel S', supplier=SUP, material_class='additive_package', existing_record='', notes='Afton Axcel® brand gear oil package')
        elif p in ('UA4158', 'UA4159'):
            PK[p] = dict(name=p, supplier=SUP, material_class='unresolved', existing_record='', notes='Afton customer product code (United Oil Company, Singapore); nature not stated on page 1')
        elif p == 'P3010':
            PK[p] = dict(name=p, supplier='unresolved (issuer not printed)', material_class='unresolved', existing_record='', notes='certificate product code; composition data (P, S, N) suggest an additive but nothing is inferred')
        elif p == 'Jilin J0030':
            PK[p] = dict(name=p, supplier='PetroChina Jilin (named on the sheet)', material_class='additive_component', existing_record='', notes='solid OCP VI improver (VM subtype); solid polymer')
        elif p == 'APL':
            PK[p] = dict(name='APL', supplier=SUP, material_class='additive_component', existing_record='', notes='synthetic lubricity improver for metalworking fluids: component general block; application outside engine / driveline scope')
unres = [k for k, v in D.items() if not v['products'] and v['relation'] == 'product']
products = {}
for k, v in PK.items():
    st = 'existing' if v['existing_record'] else ('unresolved' if v['material_class'] == 'unresolved' else 'out_of_scope' if v['material_class'].startswith('out_of_template') else 'new_candidate')
    products['AFTON:' + k] = dict(v, status=st, identity_evidence='printed product name / code on the documents linked in this batch',
                                  template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ VM subtype where noted)'}.get(v['material_class'], 'none (see notes)'))
out = dict(batch='S02 Afton Chemical (identity)', reviewed_on='2026-11-14', scope='305 documents with provisional supplier Afton Chemical', products=products,
           documents={k: dict(v, products=['AFTON:' + p for p in v['products']], roles={'AFTON:' + p: r for p, r in v['roles'].items()}) for k, v in D.items()})
json.dump(out, open(os.path.join(PKG, 'decisions', 's02_afton.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(D), 'documents', len(PK), 'products', Counter(v['doc_type'] for v in D.values()), 'no-product docs', len([v for v in D.values() if not v['products']]))
print(sorted(PK)[:400])
