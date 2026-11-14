"""Supplier batch S03: Infineum (241 documents whose provisional supplier is 'Infineum').
Read: a compact listing of every document (automated identity, page count, page-1 top lines) checked row by row; longer
page-1 cards (900 characters) for the 20 documents without a clean 'Infineum <code>' identity; page-1 images of DL2-15266,
15334, 15590, 15583-15587, 14989, 13002 (names printed as graphics); the DL2-11214 page-1 text for 'T442'.
Rule: subject = the 'Infineum <code>' identity printed on page 1 (labelled SDS field, data-sheet title or certificate header),
with OCR corrections (lnfineum -> Infineum, 03451 -> D3451, P509G -> P5096). Brochures / presentations: the code named on
page 1 is linked with role 'named on page 1' (the full subject list of a multi-product deck is NOT established).
Document type: 'SAFETY DATA SHEET' -> SDS; one- or two-page 'Version: <date>' sheets -> product data sheet; 'CERTIFICATE OF
ANALYSIS' -> certificate; 'CUSTOMER SPECIFICATION' -> customer specification; others -> presentation / brochure.
Identity only. Writes decisions/s03_infineum.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Infineum']
SUP = 'Infineum'
R = 'page-1 identity listing read (automated identity checked against page-1 top lines)'
EXIST = {c: 'INFINEUM_' + c for c in ('D3320', 'D3354', 'D3375', 'D3384', 'D3396', 'D3398', 'D3416', 'D3417', 'D3424', 'D3451', 'D3453', 'D3463', 'D3503', 'D3511')}
FIX = {'03451': 'D3451', 'P509G': 'P5096', 'SV200 SQR1810': 'SV200', 'SV260 SQR2815': 'SV260'}


def cls(code):
    if code.startswith('SV') or code == 'T4163':
        return 'additive_component', 'viscosity modifier: component general + VM subtype' + (" (named 'Viscosity Modifier' on a T4920 page)" if code == 'T4163' else '')
    if code.startswith(('V3', 'V5')):
        return 'additive_component', 'PPD / LOFI or VM component (Infineum V-series): component general (+ PPD or VM subtype after content review)'
    if code.startswith('C'):
        return 'additive_component', 'Infineum C-series component: function to be confirmed in the content review'
    if code in ('D2376', 'D2403'):
        return 'additive_package', 'booster (Infineum D23xx series): package booster used with a main package'
    if code.endswith('X') and code[:-1].isalnum() and not code[-2].isalpha():
        return 'additive_package', 'family name printed by Infineum (several grades); kept as a family key, not a single product'
    if code.startswith('F'):
        return 'out_of_template: fuel additive', 'fuel additive'
    return 'additive_package', ''


def dtype(r):
    t = r['top_lines']
    if re.search(r'(?i)safety data sheet', t): return 'SDS'
    if re.search(r'(?i)certificate of analysis', t): return 'certificate of analysis (batch)'
    if re.search(r'(?i)customer specification|SPECIFICATIONS - TEST ON PRODUCTS', t): return 'customer specification'
    if t.startswith('Version:') and int(r['pages'] or 0) <= 2: return 'product data sheet (TDS/PDS)'
    return 'presentation / brochure'


OV = {  # sha prefix -> (doc_type, [codes], note, relation)
    'c7114ad85a': ('customer specification', ['P5500'], "'CUSTOMER SPECIFICATION' (Global - Brenntag Group) 'Customer Designation Infineum P5500', printed 20-Dec-2022 (header viewed as an image)", None),
    'c111b1a35a': ('customer specification', ['D3417'], "'CUSTOMER SPECIFICATION' Brenntag, 'Infineum D3417', printed 12-Feb-2024 (image); byte duplicate of an old-archive file", None),
    'aacbd449a7': ('customer specification', ['P6080A'], "'CUSTOMER SPECIFICATION' Brenntag, 'Infineum P6080A' Mid SAPS PCMO package, printed 13-Sept-2022 (image)", None),
    '5f5dc0d58e': ('presentation / brochure', ['P5908'], "'INFINEUM P5908 is ready for ILSAC GF-7', presented to United Oil, Nov 2025 (image)", None),
    'fcb1eefb8c': ('presentation / brochure', ['P5000'], "'Infineum P5000' PCMO mainline reduced SAPS technology in ExxonMobil EHC (image)", None),
    '88a2134d83': ('presentation / brochure', [], "'TRENDS 60 YEARS' (Dubai, September 2024): market-trend presentation, no product subject on page 1", 'non_product'),
    'a60e8378c8': ('presentation / brochure', [], "'Hybrids: future perspectives and the role of lubricants' (Brenntag Customer Day UAE, 4 October 2024): general technology presentation", 'non_product'),
    '117e7345c2': ('presentation / brochure', [], "'TRENDS 60 YEARS' (Dubai, September 2024): market-trend presentation", 'non_product'),
    '631c50e128': ('presentation / brochure', [], "'E-DRIVELINE TRENDS' (4 October 2024): general technology presentation", 'non_product'),
    '0ac21a1943': ('presentation / brochure', [], "'Your Top Tier Product Portfolio' (2018): multi-product portfolio; subjects not on page 1", None),
    '470abc11c4': ('presentation / brochure', ['SV150', 'SV151', 'SV200', 'SV203', 'SV260', 'SV261', 'SV261L', 'SV603'], "'Infineum SV Viscosity Modifiers - Formulating to higher levels of performance' (2013); SV grades listed are those with their own documents in this batch, not a reading of the deck", None),
    'a08c8ae3fa': ('presentation / brochure', [], "'Infineum Specialties Additive Packages Overview' (January 2020, 44 pp); read for base-oil links in batch 34", None),
    '688d9186ea': ('presentation / brochure', [], "'Infineum Specialties Additive Packages Overview' (January 2020, 10 pp, 2 copies)", None),
    '1febe75b4c': ('presentation / brochure', [], "'Infineum Engine Oil Additive Packages Overview' (January 2020, 11 pp)", None),
    '340f563a6a': ('presentation / brochure', [], "'Infineum Engine Oil Additive Packages Overview' (January 2020, 22 pp, 2 copies)", None),
    '9d34f7e23b': ('presentation / brochure', [], "'Infineum Marine Additive Packages Overview - Technical Update for IMO2020' (December 2019)", None),
    '773bd0c7ea': ('presentation / brochure', ['D3494'], "'HDDO Full SAPS Offerings - ACEA E7/API CI-4 Cascade System' (01/01/2019, 5 pp); D3494 named in the existing-product comparison", None),
    '1844225616': ('presentation / brochure', [], "'Infineum DCTF Portfolio' (2021)", None),
    '773de54d9e': ('presentation / brochure', ['T4920'], "'T4920 Presentation' (2022)", None),
    'fa1019a693': ('certificate of analysis (batch)', ['UA 5113'], "certificate to United Oil Company (Singapore) for 'UA 5113' (customer code; average of batches in one tank, ITM 70-009)", None),
    '706ab82b38': ('certificate of analysis (batch)', ['UA 5161'], "Infineum certificate to PT Pacific Lubritama Indonesia 'Product: UA 5161' (customer code)", None),
    '1535f22787': ('SDS', ['UA 5800'], "Infineum SDS (SS586:2022) 'UA 5800' (customer code), Version 9.0", None),
    '6c11e127cb': ('SDS', ['UA 5803'], "Infineum SDS (SS586:2014) 'UA 5803' (customer code), Version 10.0", None),
    'd5ab9d0454': ('SDS', ['P5005'], 'SDS (SS586:2014) Infineum P5005', None), 'd719b96774': ('SDS', ['P5570'], 'SDS (SS586:2014) Infineum P5570', None),
    'bd6b46c753': ('SDS', ['SV603'], 'SDS (SS586:2014) Infineum SV603', None), '9ee4eae53e': ('SDS', ['M7290'], 'SDS (SS586:2014) Infineum M7290', None),
    'f3b35c09b4': ('SDS', ['T4318'], 'SDS (SS586:2022) INFINEUM T4318', None),
}
D, PK = {}, {}
for r in A:
    sha = r['sha256']
    ov = next((v for k, v in OV.items() if sha.startswith(k)), None)
    typ = dtype(r)
    if ov:
        typ, codes, note, rel = ov[0], ov[1], ov[2], ov[3] or 'product'
    else:
        m = re.match(r'(?i)^[il1]nfineum\s+([A-Z0-9]{1,2}\d{2,5}[A-Z]?(?:\s+SQR\d+)?)$', r['primary_identity'].strip())
        codes = [m.group(1).upper()] if m else []
        note, rel = ('' if codes else 'no identity on page 1'), ('product' if codes else 'unresolved_identity')
        if r['primary_identity'].upper().endswith(('SQR1810', 'SQR2815')):
            note = f"SDS printed '{r['primary_identity']}' (grade with an SQR code; kept under the SV grade with the code noted)"
    codes = [FIX.get(c, c) for c in codes]
    brochure = typ.startswith('presentation')
    roles = {('INFINEUM:' + c): ('named on page 1 (subject list of the deck not established)' if brochure and not ov else 'subject') for c in codes}
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['INFINEUM:' + c for c in codes], roles=roles, relation=rel, read=R, note=note,
                       next_action='' if codes or rel == 'non_product' else 'list the products presented inside (multi-product deck) in the package review')
    for c in codes:
        if 'INFINEUM:' + c in PK:
            continue
        mc, n = (('unresolved', 'Infineum customer product code (United Oil / Pacific Lubritama); nature not stated on page 1') if c.startswith('UA ') else cls(c))
        PK['INFINEUM:' + c] = dict(name=('Infineum ' + c) if not c.startswith('UA ') else c, supplier=SUP, material_class=mc, existing_record=EXIST.get(c, ''),
                                   status='existing' if c in EXIST else ('unresolved' if mc == 'unresolved' else 'new_candidate'), notes=n,
                                   identity_evidence='printed product code on the documents linked in this batch',
                                   template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}.get(mc, 'none (see notes)'))
out = dict(batch='S03 Infineum (identity)', reviewed_on='2026-11-14', scope='241 documents with provisional supplier Infineum', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's03_infineum.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['doc_type'] for v in D.values()), Counter(v['relation'] for v in D.values()))
