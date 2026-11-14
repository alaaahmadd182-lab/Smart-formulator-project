"""Supplier batch S08: Sama Lubricants Co. (Tehran; 118 documents with provisional supplier 'Sama').
Read: compact page-1 listing of all 118 documents; 25 longer cards (450 characters) where the product type was not in the
listing; DL2-14662 page 1 viewed as an image (text layer holds only the letterhead).
Sama is a TRADING company: many sheets carry Sama's letterhead but name another refiner's grade (Pertamina, CEPSA, IRPC,
Thai Lube, Aramco, Luberef, ADNOC, Bapco, Kusa). Such documents are distributor-issued: the printed manufacturer is recorded in
the product notes, the document is NOT a manufacturer source, and grades are never matched to manufacturer records here.
Rules: subject = the code / name printed as 'Product' (or the title line); spaces and hyphens in NT codes normalised
(NT 538 -> NT538, NT-422 -> NT422); class from the printed product type only. Where no product type is printed (C8090, P5050,
SE543) the class stays unresolved: it is NEVER inferred from the values. Two transformer oils with identical typical values
(NT561, P46) are kept as separate products (identity is never inferred from values). Identity only. Writes decisions/s08_sama.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Sama')]
SUP = 'Sama Lubricants Co. (trading company)'
C, P, B = 'additive_component', 'additive_package', 'base_oil'
OT = 'out_of_template: '
# key: (material_class, printed type / note, manufacturer printed on the document ('' = Sama label only))
PR = {
    'V7013': (C, "'alkyl methacrylate co-polymer' (VM or PPD role not stated on page 1)", ''), 'V9005': (C, "'premium viscosity modifier' (VM subtype)", ''),
    'V9022': (C, "'Viscosity Index Improver' (VM subtype)", ''), 'V9025A': (C, "'Viscosity Modifier additive' (VM subtype)", ''),
    'C7081': (C, "'Over-based Calcium Sulfonate TBN Booster 400'", ''), 'C7082': (C, "'Super High TBN Synthetic Calcium Sulfonate'", ''),
    'C7083': (C, "'Polyisobutylene Succinimide'", ''), 'C7084': (C, "'Super Overbased Synthetic Calcium Sulfonate'", ''), 'C7085': (C, "'Super Overbased Synthetic Calcium Sulfonate'", ''),
    'C8090': ('unresolved', 'batch certificate only; product type not printed (class not inferred from the values)', ''),
    'P1010': (P, "'Engines Oil Additive Package' (SDS: 'Diesel Engine Oil Additive')", ''), 'P1011': (P, "'Passenger Car Motor Oil Additive Package'", ''),
    'P5050': ('unresolved', "batch certificate only; product type not printed (rows labelled 'blended oil'); class not inferred from the values", ''),
    'A1010': (OT + 'coolant additive', "'Solid Dye for MEG based antifreeze-coolants'", ''), 'A1011': (OT + 'coolant additive', "'Solid Dye for MEG based antifreeze-coolants'", ''),
    'A1060': (OT + 'coolant additive', "'Antifreeze Hybrid Organic Base Corrosion Inhibitor'", ''), 'TTAS 50%': (OT + 'other chemical', "'Sodium Tolyltrazole 50%'", ''),
    'OIL SOLUBLE LIQUID RED DYE': (C, "dye for lubricating oils, greases and fuels (name read on the page image; no code printed)", ''),
    'M7002': ('unresolved', "'Polybutene' (SDS: 'Polyisobutene'): role (base fluid / tackifier / VM) not stated", ''),
    '12-HSA': (OT + 'other chemical', "'12-Hydroxy Stearic acid' (grease raw material)", ''), 'HCO': (OT + 'other chemical', "'Hydrogenated Castor oil flakes' (grease raw material)", ''),
    'PELARGONIC ACID': (OT + 'other chemical', 'fatty acid', ''), 'AN (ACRYLONITRILE)': (OT + 'other chemical', 'monomer', ''),
    'NT546': (OT + 'other chemical', "'Lithium Hydroxide Monohydrate' (grease raw material)", ''), 'ACTIVATED CLAY': (OT + 'other chemical', 'activated clay', ''),
    'NT425': (OT + 'other chemical', "'Hindered amine light stabilizer (HALS) for plastics and coatings'", ''),
    'NB048': (OT + 'finished lubricant (transformer oil)', 'transformer oil', ''), 'NB049': (OT + 'finished lubricant (transformer oil)', "'Uninhibited Naphthenic Grade Transformer Oil- IEC 60296-2012'", ''),
    'NB050': (OT + 'finished lubricant (transformer oil)', "'Uninhibited Paraffinic Grade Transformer Oil- IEC 60296-2012'", ''),
    'SE511': (OT + 'finished lubricant (transformer oil)', "'Uninhibited Naphthenic Grade Transformer Oil- IEC 60296-2012'", ''),
    'NT561': (OT + 'finished lubricant (transformer oil)', "'Uninhibited Transformer Oil' (typical values print the same as P46; kept separate)", ''),
    'P46': (OT + 'finished lubricant (transformer oil)', "'Transformer Oil' (typical values print the same as NT561; kept separate)", ''),
    'NT592': (OT + 'finished lubricant (transformer oil)', "'Uninhibited Naphthenic Grade Transformer Oil- IEC 60296'", ''),
    'NT533': (OT + 'heat transfer fluid', "'Heat Transfer Fluid'", ''), 'NT632': (OT + 'fuel additive', "'Octane Improver' (MMT)", ''),
    'B3065': (B, "'Polyalphaolefin'", ''), 'NT535': (B, "'Polyalphaolefin'", ''), 'NT538': (B, "'PAO1000'", ''), 'NT581': (B, "'Polyalphaolefin (PAO 2)'", ''),
    'NT583': (B, "'Polyalphaolefin (PAO 6)'", ''), 'PAO10': (B, "'Polyalphaolefin'", ''), 'PAO100': (B, "'Polyalphaolefin'", ''), 'NT640': (B, "'PAO6B'", ''),
    'BN042': (B, "'Naphthenic Base Oil' (no API group)", ''), 'BN043': (B, "'Naphthenic Base Oil' (no API group)", ''), 'BN045': (B, "'Naphthenic Base Oil' (no API group)", ''),
    'PAG SE VG180': (B, "'water insoluble polyalkylene glycol lubricant base fluid' (base_oil template fit to confirm: no API group)", ''),
    'BN046': ('unresolved', "'Ester for Synthetic Lubricants', 'used as additive for ISO VG 46 and 68 fluids': base fluid vs component to confirm", ''),
    'BN047': ('unresolved', "'Ester for Synthetic Lubricants', 'used as additive': base fluid vs component to confirm", ''),
    'SE513': ('unresolved', "'Synthetic Polyol Ester': base fluid vs component to confirm", ''),
    'SE543': ('unresolved', 'product type not printed in the inspected card; class not inferred from the values', ''),
    'NT557 (SN500)': (B, "'Mineral Base Oil' (type on the card)", ''), 'NT558 (SN500)': (B, "'Mineral Base Oil'", ''), 'NT559 (SN500)': (B, "'Mineral Base Oil'", ''),
    'NT560 (SN500)': (B, "'Mineral Base Oil, Group I'", ''), 'NT562': (B, "'Mineral Base Oil, Group III (3 cSt)'", ''),
    'SE531': (B, "'Mineral Base Oil, Group III' (4 cSt; two-product sheet with SE526)", ''), 'SE526': (B, "'Mineral Base Oil, Group III' (6 cSt; two-product sheet with SE531)", ''),
    'PERTAMINA BS 150': (B, 'bright stock', 'Pertamina (printed in the product name)'), 'BRIGHT STOCK 150': (B, 'bright stock; manufacturer not printed', ''),
    'CEPSA BS 150': (B, 'bright stock', 'CEPSA (printed in the product name)'), 'IRPC BRIGHT STOCK': (B, "bright stock; title 'Thailand - IRPC'", 'IRPC (printed)'),
    'THAI LUBE BS 150': (B, 'bright stock', 'Thai Lube (printed)'), 'ARAMCO DURA BS 150': (B, 'bright stock', 'Aramco (printed)'),
    'LUBEREF 220N': (B, "base oil ('Specification of Analysis')", 'Luberef (printed)'), 'ADNOC 2CST': (B, 'base oil', 'ADNOC (printed)'),
    'BAPCO BAP BASE 6 CST': (B, 'base oil', 'Bapco (printed)'), 'EHC-50': (B, 'base oil certificate; manufacturer not printed', ''), 'EHC-120': (B, 'base oil certificate; manufacturer not printed', ''),
    'NT422': (C, "'Viscosity Index Improver' (VM subtype); certificates issued to Sama by 'GROUP INTERNATIONAL'", 'GROUP INTERNATIONAL (certificate issuer)'),
    'NT430': (C, "'Ashless TBN Booster'", ''), 'NT435': (C, "'Aminic Antioxidant'", ''), 'NT438': (C, "'Overbased Sulfurized Calcium Alkyl Phenate'", ''),
    'NT439': (C, "'Overbased Synthetic Calcium Sulfonate'", ''), 'NT440': (C, "'Butyl Octyl Diphenylamine'", ''), 'NT441': (C, "'Super Overbased Synthetic Calcium Sulfonate'", ''),
    'NT442': (C, "'Polyisobutylene Succinimide'", ''), 'NT443': (C, "'High MW Polyisobutylene Succinimide Ashless Dispersant'", ''),
    'NT444': (C, "'Alkali-type Zinc Dioctyl Primary Alkyl Dithiophosphate'", ''), 'NT445': (C, "'Zinc Propyl Octyl Secondary-Primary Alkyl Dithiophosphate'", ''),
    'NT446': (C, "'Over based Sulfurized Calcium Alkyl Phenate'", ''), 'NT447': (C, "'Antioxidant and Corrosion Inhibitor'", ''), 'NT450': (C, "'ZDDP'", ''),
    'NT542': (C, "'High-Nitrogen Ashless Dispersant'", ''), 'NT564': (C, "'Viscosity Index Improver, Poly Methacrylate (PMA)' (VM subtype)", ''),
    'NT567': (C, "'Corrosion Inhibitor'", ''), 'NT617': (C, "'Polyisobutylene Succinimide'", ''), 'NT618': (C, "'Polyisobutylene Succinimide'", ''),
    'NT629': (C, "'Over based Synthetic Calcium Sulfonate'", ''), 'NT649': (C, "'over based synthetic calcium sulfonate (TBN Booster)'", ''),
    'NT645': (C, "'Aminic antioxidant'", ''), 'NT646': (C, "'PPD' alkyl methacrylate (PPD subtype)", ''), 'NT648': (C, "'PPD' alkyl methacrylate (PPD subtype)", ''),
    'NT653': (C, "'PPD' (PPD subtype)", ''), 'NT651A': (C, "'TRI CRESYL PHOSPHATE (T.C.P)'", ''),
    'NT637': (C, "'Polyisobutylene Succinic Anhydride (Thermal Adduction PIBSA)', 'lubricant additive intermediate' (schema gap: process intermediate)", ''),
    'NT638': (C, "'Thermal Adduction PIBSA' intermediate (schema gap: process intermediate)", ''), 'NT639': (C, "'Thermal Adduction PIBSA' intermediate (schema gap: process intermediate)", ''),
}
# documents whose product cannot be taken from the listing pattern
OV = {'662d4599c8': ['PERTAMINA BS 150'], 'f0e3cde93b': ['PERTAMINA BS 150'], '7b051dd987': ['BRIGHT STOCK 150'], 'c814018da7': ['CEPSA BS 150'],
      '3b833f9846': ['IRPC BRIGHT STOCK'], '88ada26b5c': ['THAI LUBE BS 150'], 'b514cbf502': ['ARAMCO DURA BS 150'], '1361355ae7': ['LUBEREF 220N'],
      '0a2d2ac312': ['ADNOC 2CST'], '67eef59bab': ['BAPCO BAP BASE 6 CST'], '7939263dc9': ['NT422'], 'e852fef516': ['NT422'], 'e7243a04fa': ['NT422'],
      '67b70078a3': ['OIL SOLUBLE LIQUID RED DYE'], '76e9fd6ba2': ['SE531', 'SE526'], 'f17127b843': ['AN (ACRYLONITRILE)'], '760062fdd6': ['TTAS 50%'],
      '79c89b2ea1': ['ACTIVATED CLAY'], 'a608cc96d5': ['PELARGONIC ACID'], '5eb5d4fab3': ['PAG SE VG180'], 'e398a57c15': ['12-HSA'], '536334d832': ['12-HSA'],
      '10b0536b5b': ['HCO'], '3cc2bde06b': ['NT653'], '7e8556fe6e': ['NT546'], '7aa3d23bef': ['NT632'], '1df31d8d6b': ['NT533'], '8e121598f9': ['P46'], '2e10f8b87a': ['PAO10']}
SPECIAL = {'2ed6830ac7': dict(products=['KUSA:KUSACRYL 2231'], note="Sama technical report on KUSACRYL 2231 (Kusa product; keyed under KUSA for consolidation with the Kusa batch)"),
           '092d504eaf': dict(products=[], relation='unresolved_identity', doc_type='third-party laboratory report', note="LABORELEC final report 2020-0418 for 'FEEDO TRADING Co' (7 pp); oil sample identity not on page 1",
                              next_action='read the sample identification inside the report'),
           'cb74fdc418': dict(products=['A1011', 'A1010'], roles={'SAMA:A1011': 'subject (title)', 'SAMA:A1010': 'named in Section 1 (printed inconsistency)'},
                              note="SDS title prints 'A1011' but Section 1 'Identification of the mixture' prints 'A1010 - Solid Dye for MEG based antifreeze-coolants': identity conflict recorded, not resolved",
                              next_action='blocker: establish which grade this SDS covers before using it for either product'),
           '543640321d': dict(products=[], relation='non_product', doc_type='equipment catalogue (Persian)', note="Sama catalogue of an explosion-proof varnish-removal filter package (model EF-VRS4-Ex): equipment, not a material", next_action='')}
CODES = sorted((k for k in PR if re.fullmatch(r'[A-Z]{1,3}\d{3,4}[A-Z]?(?: \(SN500\))?', k)), key=len, reverse=True)


def dtype(t):
    if re.search(r'(?i)safety data sheet', t): return 'SDS'
    if re.search(r'(?i)certificate of analysis|specification of analysis', t): return 'certificate of analysis (batch)'
    if re.search(r'(?i)technical report', t): return 'technical report'
    return 'product data sheet (TDS/PDS)'


D, PK, used = {}, {}, Counter()
for r in A:
    sha, t = r['sha256'], r['top_lines']
    s = SPECIAL.get(sha[:10], {})
    if s:
        keys = s['products']
    elif sha[:10] in OV:
        keys = OV[sha[:10]]
    else:
        tt = re.sub(r'(?<=\b(?:NT|NB))[\s-]+(?=\d)', '', t.replace('\n', ' | ')[:260])
        tt = re.sub(r'NT\s?(\d{3})\(\s?SN\s?500\)', r'NT\1 (SN500)', tt)
        keys = [next((c for c in CODES if re.search(r'(?<![A-Z0-9])' + re.escape(c) + r'(?![0-9A-Z])', tt)), None)]
        keys = [k for k in keys if k]
        for k in ('EHC-50', 'EHC-120'):
            if 'Product: ' + k in t:
                keys = [k]
    for k in keys:
        used[k] += 1
    D[sha[:12]] = dict(doc_type=s.get('doc_type', dtype(t)), supplier=SUP, products=[k if ':' in k else 'SAMA:' + k for k in keys],
                       roles=s.get('roles') or {(k if ':' in k else 'SAMA:' + k): 'subject' for k in keys},relation=s.get('relation', 'product' if keys else 'unresolved_identity'),
                       read='page-1 listing; longer card for 25; page image for DL2-14662', note=s.get('note', 'distributor-issued document (Sama letterhead)'),
                       next_action=s.get('next_action', '' if keys else 'identify the product'))
for k, (mc, n, man) in PR.items():
    if not used[k]:
        raise SystemExit('product defined but not linked: ' + k)
    PK['SAMA:' + k] = dict(name=k, supplier=SUP, material_class=mc, existing_record='', status='out_of_scope' if mc.startswith(OT) else 'new_candidate',
                           notes=n + ('; manufacturer printed: ' + man if man else '; Sama label (manufacturer not stated)'), identity_evidence='printed product name / code on the documents linked in this batch',
                           template={C: 'additive_component general (+ subtype as noted)', P: 'additive_package tier1 + tier2', B: 'base_oil tier1-3'}.get(mc, 'none / not determined'))
PK['KUSA:KUSACRYL 2231'] = dict(name='KUSACRYL 2231', supplier='Kusa (named on a Sama technical report)', material_class='unresolved', existing_record='', status='new_candidate',
                                notes='class to be taken from the Kusa batch (not inferred here)', identity_evidence='printed product name on DL2 Sama technical report', template='not determined')
miss = [s for s, v in D.items() if v['relation'] == 'unresolved_identity' and not s.startswith('092d504eaf')]
out = dict(batch='S08 Sama Lubricants (identity)', reviewed_on='2026-11-14', scope='118 documents with provisional supplier Sama', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's08_sama.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['status'] for p in PK.values()), 'unmatched:', miss)
