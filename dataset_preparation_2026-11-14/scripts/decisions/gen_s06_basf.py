"""Supplier batch S06: BASF (204 documents whose provisional supplier is 'BASF').
Read: a compact listing of every document (automated identity, pages, page-1 top lines) checked row by row; for the 59 documents
without an automated identity, page 1 was searched for BASF brand names and the certificate product field.
Rule: subject = brand + grade printed on page 1 (Irganox, Irgalube, Irgafos, Irgamet, Irgaflo, Irgapac, Synative, Breox,
Plurasafe, Pluracol, Pluriol, Pluronic, Oppanol, Glysantin, Keropur / Keroflux / Kerojet / Keropon, Super Concentrate, Tinuvin);
descriptive words and file-name noise ('- TDS', 'v 2012') dropped; Irgalube variant suffixes (2030 A / 2030 C, ML 3010 A,
F 10 A) taken from the page-1 heading. Selection guides, product-range catalogues and brochures are multi-product: no subject.
Material class by brand: lubricant additives -> additive_component / additive_package; Synative ES esters and Breox / Pluracol /
Pluriol / Plurasafe WS-WI base polymers -> base_oil (Group V synthetic, template base_oil); fully formulated fluids (Plurasafe
GL / CL / H20K / HL-HFC, Breox FGL, Hydrolubes, NF 46) -> finished lubricants (no template); surfactants / fatty alcohols ->
component with a metalworking scope question; fuel / refinery additives, coolants, light stabiliser, monomers -> no template.
Identity only. Writes decisions/s06_basf.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'BASF']
SUP = 'BASF'
BR = r'(Irganox|Irgalube|Irgafos|Irgamet|Irgaflo|Irgapac|Synative|Breox|Plurasafe|Pluracol|Pluriol|Pluronic|Oppanol|Glysantin|Keropur|Keroflux|Kerojet|Keropon|Super Concentrate|Tinuvin|AMINE|XPDL|ProEco)'


def norm(s):
    s = re.sub(r'[®™]', ' ', s)
    s = re.sub(r'(?i)\s*-\s*TDS.*$|\s+v\s+20\d\d.*$|\(.*$', '', s).strip()
    m = re.match(r'(?i)^' + BR + r'\s*(.*)$', s)
    if not m:
        return s.upper()
    toks = []
    for t in re.split(r'\s+', m.group(2)):
        if re.fullmatch(r'[A-Z0-9][A-Z0-9/.\-]*', t) or (toks and re.fullmatch(r'\d+[A-Z]?', t)):
            toks.append(t)
        else:
            break
    return (m.group(1).upper() + ' ' + ' '.join(toks[:4])).strip()


def cls(k):
    b = k.split(' ')[0]
    if k.startswith(('IRGALUBE 2030', 'IRGALUBE 2040', 'IRGALUBE 2050', 'IRGALUBE ML', 'IRGALUBE 232')) or b == 'IRGAPAC':
        return 'additive_package', 'Irgalube / Irgapac industrial additive package'
    if b in ('IRGANOX', 'IRGAFOS', 'IRGAMET', 'IRGALUBE', 'AMINE', 'XPDL-590', 'XPDL'):
        return 'additive_component', {'IRGANOX': 'antioxidant', 'IRGAFOS': 'phosphite antiwear / antioxidant', 'IRGAMET': 'metal deactivator / corrosion inhibitor',
                                      'IRGALUBE': 'EP / antiwear / friction-modifier component', 'AMINE': 'amine corrosion inhibitor (Amine O)'}.get(b, 'lubricant additive component')
    if b == 'IRGAFLO': return 'additive_component', 'PMA pour point depressant (PPD subtype)'
    if b == 'OPPANOL': return 'additive_component', 'polyisobutene (PIB) polymer: thickener / VM-type component (scope to confirm)'
    if b == 'SYNATIVE' and k.startswith('SYNATIVE ES'): return 'base_oil', 'synthetic ester base stock (API Group V): base_oil template'
    if b == 'SYNATIVE' or b == 'PLURONIC' or b == 'PROECO': return 'additive_component', 'surfactant / fatty alcohol / ester additive for metalworking fluids: scope question'
    if b == 'BREOX' and re.search(r'NF|FGL|HYDROLUBE', k): return 'out_of_template: finished lubricant', 'fully formulated PAG fluid (fire-resistant / food-grade)'
    if b in ('BREOX', 'PLURACOL', 'PLURIOL') or k.startswith(('PLURASAFE WS', 'PLURASAFE WI')): return 'base_oil', 'polyalkylene glycol (PAG) base fluid (API Group V): base_oil template'
    if b == 'PLURASAFE': return 'out_of_template: finished lubricant', 'fully formulated PAG lubricant / hydraulic fluid / quenchant'
    if b in ('KEROPUR', 'KEROFLUX', 'KEROJET', 'KEROPON'): return 'out_of_template: fuel additive', 'fuel / refinery additive'
    if b in ('GLYSANTIN', 'SUPER'): return 'out_of_template: coolant', 'engine coolant / coolant concentrate'
    if b == 'TINUVIN': return 'out_of_template: other chemical', 'light stabiliser (not a lubricant raw material)'
    return 'unresolved', ''


def dtype(r):
    t = r['top_lines']
    if re.search(r'(?i)certificate of analysis', t): return 'certificate of analysis (batch)'
    if re.search(r'(?i)safety data sheet|Information Sheet Product Safety', t): return 'SDS'
    if re.search(r'(?i)selection guide|product range|Produktkatalog|Partner|Formula for|Soulmates|Teammates', t): return 'brochure / selection guide (multi-product)'
    return 'product data sheet (TDS/PDS)'


OV = {
    '302df72c29': ['SYNATIVE AC AMH 2'], 'ad4d5e414d': ['BREOX FGL'], '25c48b2711': ['BREOX HYDROLUBES NF46 2180', 'BREOX HYDROLUBES NF46 2181'],
    'c56fd9cbe7': ['PLURASAFE GL FG'], '02e00db6f3': ['SUPER CONCENTRATE G 103', 'GLYSANTIN G 48'], '45b1588ea2': ['GLYSANTIN G130K SC'],
    '4bccefbdd4': ['GLYSANTIN G140K SC'], 'a2a59a06c2': ['OPPANOL B'], 'bb895c5522': ['OPPANOL B'], 'd5ad902907': ['TINUVIN 765'],
    '31f41e89a3': ['PLURONIC PE'], '3ffb48b225': ['SYNATIVE ES TMP 05'], '9ff73d2303': ['SYNATIVE ES TMP 05 H'], 'ff5b31f979': ['PLURONIC PE 6100'],
    '75f6077446': ['SYNATIVE ES DPHA'], '816a2d829b': ['IRGAFLO 1100 V', 'IRGAFLO 6300 V', 'IRGAFLO 6305 V'], 'd43e0d7200': ['KEROPUR G'],
    '3a61c5ac7d': ['KEROPUR D'], 'd7f72c573f': ['SYNATIVE ES TMTC'], '40d22a11a8': ['PLURIOL V-10'], '7c3a4e2138': ['KEROPUR 3458 N'],
    '2fdf2689a5': ['PLURONIC PE 10100'], 'cc7ae6f698': ['BREOX NF 46 4005'], '3468f649f0': ['SUPER CONCENTRATE NFT'], '8040af3c9a': ['SUPER CONCENTRATE NFT'],
    '153c877a57': ['SUPER CONCENTRATE NFT'], '156c54a839': ['SUPER CONCENTRATE NFT'], 'c55eb723f8': ['PLURASAFE NF 46 4005'], '429575caea': ['BREOX 50 A 140'],
    '97e1f8deac': ['BREOX 60 D 460'], '3c63157319': ['XPDL-590'], '6ae7154568': ['IRGALUBE TPPT'], '005674433e': ['BREOX 50A 480'], '4275ced6f6': ['BREOX 50A 75'],
    '0756153460': ['IRGAPAC T 2030 C'], '871f8cc5e0': ['PLURASAFE CL GAS 9'], 'bbf2b94216': ['PLURASAFE GL PLUS'], 'e1a7923ec4': ['PLURASAFE PE CABLE'],
    '71ba97de57': ['PLURASAFE QUENCHANT'], 'edc55dd07e': ['PLURONIC PE 6100'], '4d8d5274a6': ['BREOX 50 A 140'], '8b1e130a74': ['GLYSANTIN'],
}
ALIAS = {'IRGAFLO 610': 'IRGAFLO 610 P', 'IRGAFLO 942': 'IRGAFLO 942 P', 'IRGAFLO 649': 'IRGAFLO 649 P', 'IRGAFLO 710': 'IRGAFLO 710 P', 'IRGAFLO 720': 'IRGAFLO 720 P',
         'IRGALUBE ML 605A': 'IRGALUBE ML 605 A', 'GLYSANTIN G48': 'GLYSANTIN G 48', 'SYNATIVE ES 2423 GTO': 'SYNATIVE ES 2423'}
OVN = {  # explicit no-subject or unresolved documents
    '4389ed7438': ('product list (spreadsheet, multi-product)', "'Polyalkylene Glycols (PAGs)' grade list (Breox 60 D 460, 60 D 1100, 50 A 20 ... ): multi-product", 'product'),
    '4eff32e788': ('brochure / selection guide (multi-product)', 'OPPANOL PIB brochure', 'product'),
    '49c20d98e5': ('brochure / selection guide (multi-product)', 'OPPANOL PIB brochure (same title as DL2-11888)', 'product'),
    '1c8fff488c': ('brochure / selection guide (multi-product)', "'BASF Polyisobutene Viscosity Grades' (EVO 1810) table", 'product'),
    'f0debc0d50': ('product data sheet (TDS/PDS)', "'Data Sheet D/EVO 069 e June 2017' (6 pp): product name not in the page-1 text", 'unresolved_identity'),
    '7a618f1dfe': ('product data sheet (TDS/PDS)', "'EVO 1617' sheet: product name not in the page-1 text", 'unresolved_identity'),
    'b6ef0c3192': ('product data sheet (TDS/PDS)', "'Data sheet D/EVO 070 e February 2008 ... Coolants': product name not in the page-1 text", 'unresolved_identity'),
    '91006dc3c3': ('product data sheet (TDS/PDS)', "'Petrochemicals Specialty Monomers TI/CP 0011 e': monomer, no lubricant template (name not in the card)", 'non_product'),
    'd2921b5288': ('product data sheet (TDS/PDS)', "'Specialty Monomers TI/CP 0033 e': monomer, no lubricant template", 'non_product'),
    '4f92595ee5': ('product data sheet (TDS/PDS)', "'Specialty Monomers TI/CP 1379 e': monomer, no lubricant template", 'non_product'),
    '183962d972': ('product data sheet (TDS/PDS)', "'Specialty Monomers TI/CP 0024 e': monomer, no lubricant template", 'non_product'),
    '23c33040dc': ('presentation', "'GEO Introduction June 2021' (GEO Specialty Chemicals company presentation; not a BASF product)", 'non_product'),
    '86759b7ac3': ('analysis report', "'Analysis results ... IEC 60296 Ed4' (transformer-oil test report): issuer and product not on the card", 'unresolved_identity'),
    'e7ff4e72fc': ('instrument / reference document', "'Electrol-U' by a diagnostic-instrument company: not a lubricant raw material", 'non_product'),
    '27c33a2309': ('product data sheet (TDS/PDS)', "'Equivalent replacement of foreign counterpart: IRGANOX L57' - another maker's product; maker not named on the card", 'unresolved_identity'),
}
D, PK = {}, {}
for r in A:
    sha = r['sha256']
    typ = dtype(r)
    pre = next((k for k in OVN if sha.startswith(k)), None)
    if pre:
        typ, note, rel = OVN[pre]
        keys = []
    else:
        ov = next((v for k, v in OV.items() if sha.startswith(k)), None)
        if ov is not None:
            keys, note = ov, ''
        elif typ.endswith('(multi-product)'):
            keys, note = [], 'multi-product selection guide / catalogue: no subject'
        else:
            m = re.search(r'IRGALUBE \| ((?:ML )?[\dA-Z]+ ?\d* ?[A-Z]?) \|', r['top_lines'])
            k = ('IRGALUBE ' + m.group(1).strip()) if m else norm(r['primary_identity'])
            keys, note = ([k] if k and k not in ('ORDER', 'PROPERTIES', 'BASE') else []), ''
        keys = [ALIAS.get(k, k) for k in keys]
        if keys and keys[0] in ('BREOX 50', 'BREOX 60'):
            note = "family data sheet titled '" + keys[0].title() + "' (several grades); kept as a family key"
        rel = 'product' if keys or typ.endswith('(multi-product)') else 'unresolved_identity'
    if r['byte_duplicate_of_existing']:
        note = (note + '; ' if note else '') + 'byte duplicate of an old-archive file'
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP, products=['BASF:' + k for k in keys], roles={'BASF:' + k: 'subject' for k in keys}, relation=rel,
                       read='page-1 listing / brand search read', note=note,
                       next_action='list the products inside (multi-product)' if typ.endswith('(multi-product)') else ('' if keys or rel == 'non_product' else 'identify the product (name not in the page-1 text: view the page image)'))
    for k in keys:
        if 'BASF:' + k in PK: continue
        mc, n = cls(k)
        PK['BASF:' + k] = dict(name=k.title().replace('Irg', 'Irg'), supplier=SUP, material_class=mc, existing_record='',
                               status='out_of_scope' if mc.startswith('out_of_template') else ('unresolved' if mc == 'unresolved' else 'new_candidate'), notes=n,
                               identity_evidence='printed brand and grade on the documents linked in this batch',
                               template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)',
                                         'base_oil': 'base_oil tier1-3 (Group V synthetic)'}.get(mc, 'none (see notes)'))
out = dict(batch='S06 BASF (identity)', reviewed_on='2026-11-14', scope='204 documents with provisional supplier BASF', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's06_basf.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['relation'] for v in D.values()), Counter(p['material_class'] for p in PK.values()))
print(sorted(k[5:] for k in PK))
