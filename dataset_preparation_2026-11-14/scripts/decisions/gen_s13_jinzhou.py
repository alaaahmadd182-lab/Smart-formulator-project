"""Supplier batch S13: provisional label 'Jinzhou Donggong' (50 documents). The label groups FOUR companies in Jinzhou (Liaoning):
Jinzhou Donggong Petrochemical Products (T3xxx, T106), Jinzhou Xinxing Petroleum Additive (T-1xx / T-2xx / XT- / L557 / EPM 0010),
Jinzhou Bett Chemical (Bettchem: BT3xxxx), Jinzhou KangTai Lubricant Additives (KT...). Supplier is set per document from its
printed company name; product keys use DONGGONG: / XINXING: / BETTCHEM: / KANGTAI: so that later batches consolidate.
Read: compact listing; page-1 text after the letterhead for every document; Xinxing MSDS 'Product code & name' field; DL2-15761 /
15762 (KangTai bulletins, name printed as graphics) viewed as images.
Rules: subject = printed code; same code from two companies are different products (Donggong 'T106' vs Xinxing 'T-106').
Recorded printed inconsistency: Xinxing T-106A TDSs print 'TBN400', its MSDS prints 'T-106A Alkyl Benzene Calcium Sulfonate/TBN300'
(note only; no identity change, no value used). Classes from the printed descriptor; KTC-150 / KTSA-250 (SDS title only) unresolved.
Existing records: JINZHOU_DONGGONG_T3160. Identity only. Writes decisions/s13_jinzhou.json."""
import csv, json, os, re, importlib.util
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('ident', os.path.join(os.path.dirname(HERE), '02_identify.py'))
ident = importlib.util.module_from_spec(spec); spec.loader.exec_module(ident)
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Jinzhou')]
CO = {'DONGGONG': 'Jinzhou Donggong Petrochemical Products Co., Ltd.', 'XINXING': 'Jinzhou Xinxing Petroleum Additive Co., Ltd.',
      'BETTCHEM': 'Jinzhou Bett Chemical Co., Ltd. (Bettchem)', 'KANGTAI': 'Jinzhou KangTai Lubricant Additives Co., Ltd.'}
EXIST = {'DONGGONG:T3160': 'JINZHOU_DONGGONG_T3160'}
P, C = 'additive_package', 'additive_component'
DESC = {}
# page-1 code and printed descriptor, as read in the page-1 text (listing / 'Product code & name' field)
MAP = {'06574486e7': ('T30501', 'High Performance Gasoline Engine Oil Additive Package'), '36dd61d3ab': ('T30501', 'Gasoline Engine Oil Additive Package'),
       '7ec63a0bda': ('T3212', 'Multifunction Engine Oil Additive Package'), '005889a31e': ('T3212', 'Multifunction Engine Oil Additive Package'),
       'e43c8eaa90': ('T3209', 'Multifunction Engine Oil Additive Package'), '5ab6c2d960': ('T3209', 'Multifunction Engine Oil Additive Package'),
       '2dbc619571': ('T106', 'High based Synthetic Calcium Sulfonate'), '7b0821d1a4': ('T106', 'High Based Number Synthetic Calcium Sulfonate'),
       'c1c0b3fc6e': ('T3160', 'Multifunction Engine Oil Additive Package'),
       'f783131a91': ('L557', 'Octyl/Butyl Diphenylamine'), '57d9f6d848': ('T-106', 'High Base Synthetic Calcium Sulfonate/TBN300'),
       '07f8ae17f9': ('T-106', 'High-based Synthetic Calcium Sulfonate/TBN300'), '34eb5ae4f3': ('T-106A', 'Over-based Synthetic Calcium Sulfonate/TBN400'),
       '4285274954': ('T-106A', 'Over-based Synthetic Calcium Sulfonate/TBN400'), '2b5ee275d3': ('T-106A', 'Alkyl Benzene Calcium Sulfonate/TBN300'),
       '2a31f3efb8': ('T-106D', 'Alkyl Benzene Calcium Sulfonate/TBN400'), '1f1e5b4ab9': ('T-115B', 'Sulfurized Calcium Alkyl Phenolate'),
       'c31aaaba03': ('T-115B', 'Sulfurized Calcium Alkyl Phenolate'), '11f0b30f0b': ('T-154A', 'PIB Succinimide/Explosive Emulsifier'),
       '51446e9474': ('T-154A', 'PIB Succinimide'), '07ed2984bc': ('T-154B', 'Ashless Dispersant (Boride Polyisobutylene Bis-succinimide)'),
       '7fdde15deb': ('T-154', 'PIB Bis-succinimide (High Nitrogen, Ashless)'), 'c89b2f7a97': ('T-155', 'Polyisobutylene Poly-succinimide'),
       '89d20a74f6': ('T-161', 'High Molecular Weight Polyisobutylene Succinimide'), 'c253457b8e': ('T-161A', 'High Molecular Weight PIB Succinimide'),
       '28f2ac8fd8': ('T-161B', 'Boride High Molecular Weight Polyisobutylene Succinimide'), '3e49cb25c3': ('T-202', 'Zinc Butyl-octyl Dithiophosphate'),
       'c0179bc0c2': ('T-203', 'Zinc Dioctyl Dithiophosphate (Alkali-Type)'), 'a4b215b598': ('T-204', 'Zinc Primary-Secondary Dialkyl Dithiophosphate'),
       '780a57d4a1': ('T-204', 'Alkali Type Zinc Dioctyl Primary Dialkyl Dithiophosphate'), '1b86ca7c34': ('T-205', 'Zinc Propyl Octyl Primary-Secondary Dialkyl Dithiophosphate'),
       'f7d5915504': ('T-205', 'Zinc Propyl Octyl Primary-Secondary Dialkyl Dithiophosphate'), '094d28ed8c': ('EPM 0010', 'white & slab rubber solid'),
       '72003da48c': ('XT-3205', 'Diesel Engine Oil Additive Package'), 'a32a5aa657': ('XT-63297', 'Diesel Engine Oil Additive Package (High-end, Heavy-load, Economical)'),
       '61d777abfa': ('XT-64223', 'Universal Gear Oil Additive Package'),
       'ae15f00d2c': ('BT33040', 'formulated with detergent, dispersant, antioxidant (engine oil)'), '314091172e': ('BT33069', 'formulated with detergent, dispersant, antioxidant (engine oil)'),
       '4fa25b357c': ('BT33138', 'engine oil additive (detergency, acid neutralization, antioxidant, anti-wear); package type not printed in the first lines'),
       '95f67d654e': ('BT33159A', 'formulated with detergent, dispersant, antioxidant and corrosion inhibitor'), 'da8a7a3d92': ('BT33265', 'formulated with detergent, dispersant, antioxidant and corrosion inhibitor'),
       '53a2c3fb80': ('BT33780', 'developed to formulate natural gas engine oils; compounded with selected detergent, dispersant ...'),
       '67b4aa97ff': ('BT44208', 'gear oil additive (high-temp antioxidant, anti-corrosion, antifoaming, demulsibility); package type not printed in the first lines'),
       '522f70d659': ('BT55008', 'formulated with zinc-containing antioxidant, anti-corrosion and anti-wear agent (hydraulic oil)'),
       '25a87e6e7f': ('KTS-250', 'CALCIUM ALKYLSALICYLATE')}
OV = {'fb016636e7': ('KANGTAI', 'KTD1354', "'1300 Mw HR PIB Bis-Succinimide' (DISPERSANT; page image viewed)"),
      'b33820c828': ('KANGTAI', 'KTD1961', "'1900 Mw HR PIB Bis-Succinimide' (DISPERSANT; page image viewed)"),
      '784d13c5dc': ('KANGTAI', 'KTC-150', 'SDS title only'), 'c26de69e7c': ('KANGTAI', 'KTSA-250', 'SDS title only')}


def company(t):
    if 'Bett Chemical' in t: return 'BETTCHEM'
    if 'KANGTAI' in t.upper(): return 'KANGTAI'
    if 'XINXING' in t.upper() or 'jzxxpa' in t or 'XIAN LI' in t: return 'XINXING'
    return 'DONGGONG'


def cls(code, d):
    if 'package type not printed' in d: return 'unresolved', d + ' (package vs component to confirm)'
    if re.search(r'(?i)package|formulated with|compounded with|developed to formulate', d): return P, d
    if re.search(r'(?i)explosive emulsifier', d): return C, d + ' (explosive-emulsifier use: scope question)'
    if re.search(r'(?i)rubber', d): return C, d + ' (solid ethylene-propylene rubber; VM use not stated on page 1)'
    if re.search(r'(?i)sulfonate|phenolate|succinimide|dithiophosphate|diphenylamine|salicylate|dispersant', d): return C, d
    return 'unresolved', d or 'class not printed on the documents read'


D, PK = {}, {}
for r in A:
    sha, p10 = r['sha256'], r['sha256'][:10]
    pg, _ = ident.pages_for(sha)
    t = re.sub(r'\s+', ' ', pg[0] if pg else '')
    co = company(t)
    if p10 == 'a67970c219':
        D[sha[:12]] = dict(doc_type='technical note', supplier=CO['BETTCHEM'], products=[], roles={}, relation='non_product', read='page-1 text',
                           note="Bettchem note 'The N-heptane Insoluble Test of Engine Oil Additive Package' (test-method explanation; no product named on page 1)", next_action='')
        continue
    if p10 in OV:
        co, code, d = OV[p10]
    else:
        code, d = MAP[p10]
    typ = 'SDS' if re.search(r'(?i)safety data sheet|M S D S', t[:600]) else 'product data sheet (TDS/PDS)'
    key = co + ':' + code
    note = ''
    if key == 'XINXING:T-106A' and 'TBN300' in t:
        note = "MSDS prints 'T-106A Alkyl Benzene Calcium Sulfonate/TBN300' while the T-106A TDSs print 'TBN400': printed inconsistency recorded (no value used)"
    D[sha[:12]] = dict(doc_type=typ, supplier=CO[co], products=[key], roles={key: 'subject'}, relation='product',
                       read='page-1 text after the letterhead' + ('; page image viewed' if p10 in ('fb016636e7', 'b33820c828') else ''), note=note, next_action='')
    if d and (key not in DESC or typ != 'SDS'):
        DESC[key] = d
for key, d in DESC.items():
    pass
for key in dict.fromkeys(p for v in D.values() for p in v['products']):
    mc, n = cls(key.split(':')[1], DESC.get(key, ''))
    co = key.split(':')[0]
    PK[key] = dict(name=key.split(':')[1], supplier=CO[co], material_class=mc, existing_record=EXIST.get(key, ''), status='existing' if key in EXIST else 'new_candidate',
                   notes=('printed: ' + n) if n else '', identity_evidence='printed product code on the documents linked in this batch',
                   template={P: 'additive_package tier1 + tier2', C: 'additive_component general'}.get(mc, 'not determined'))
PK['XINXING:T-106A']['notes'] += "; T-106A TDS prints 'TBN400', its MSDS 'TBN300' (see document note)"
out = dict(batch='S13 Jinzhou companies (identity)', reviewed_on='2026-11-14', scope="50 documents with provisional supplier 'Jinzhou Donggong' (4 companies)", products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's13_jinzhou.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['status'] for p in PK.values()))
for k, v in sorted(PK.items()): print(k.ljust(22), v['material_class'].ljust(20), v['notes'][:85])
