"""Supplier batch S04: Lubrizol (196 documents whose provisional supplier is 'Lubrizol').
Read: a compact listing of every document (automated identity, page count, page-1 top lines) checked row by row; longer cards
(700 characters) for 11 documents; page-1 images of DL2-12748 (Schercozoline O) and DL2-12512 (AT9231).
Rule: subject = the grade printed at the top of page 1 (data sheet 'Product | Type | <grade>', SDS 'SDS_xx - <grade>', certificate
'Material: <grade>'), normalised (prefix 'LUBRIZOL', packaging suffixes such as ', STD DRUM' dropped, 'LZ' = 'LUBRIZOL').
Scope classes: SLF 'Fluid Supply Services' finished fluids and ULTRAZOL gasoline additives have no raw-material template;
metalworking / metal-processing products are kept as candidates with a scope question. Identity only.
Writes decisions/s04_lubrizol.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'] == 'Lubrizol']
SUP = 'Lubrizol'
R = 'page-1 identity listing read (automated identity checked against page-1 top lines)'
EXIST = {g: 'LUBRIZOL_' + g for g in ('16008', '3589C', '3700', '3700D', '4986', '4986D', '4986E', '4986F', '4986G', '4987', 'CV1100', 'CV1103', 'CV2301', 'CV2601', 'CV3515', 'CV6320', 'CV7540')}
COMP = {'888': 'silicone foam inhibitor', '889D': 'industrial component', '7067C': 'OCP viscosity modifier (VM subtype)', '7077': 'viscosity modifier (VM subtype)',
        '8676': 'antioxidant supplement', '5370C': 'borated ester friction modifier for grease', 'SCHERCOZOLINE O': 'oleyl hydroxyethyl imidazoline (CAS 95-38-5), single chemical'}
METAL = {'5333', '5340MG', '5340MW', '5346', '5347', 'MC9500', '5408B', 'ADDCO ADDTAC', 'CONTRAM ST-1', 'CONTRAM ST-2', 'SODIUM SULFONATE 425HJ', 'SKOSAN RE', 'SKOSAN S',
         'SOLUBLE BASE GT-1100LAS', 'SOLUBLE BASE GT-1580VS', 'SOLUBLE BASE GT-1900S'}


def key(s):
    s = re.sub(r'(?i),\s*(STD|DRUM|STD BLACK).*$', '', s.strip())
    s = re.sub(r'\(TM\)', '', s)
    s = re.sub(r'(?i)^(?:LUBRIZOL|LZ)\s*', '', s).strip().upper()
    return re.sub(r'\s+', ' ', s)


def dtype(r):
    t = r['top_lines']
    if re.search(r'(?i)SAFETY DATA SHEET', t): return 'SDS'
    if re.search(r'(?i)CERTIFICATE OF ANALYSIS', t): return 'certificate of analysis (batch)'
    if re.search(r'(?i)Bench Test Performance|Engine Test Summary|Oil Code|Conducted by|approval|report contains engine testing', t): return 'formulation / approval data'
    if re.search(r'(?i)^IP-\d|IP Report|Technical report|Technical Data', t): return 'technical report (performance data)'
    if re.search(r'(?i)Product \| Type|APPLICATIONS AND CREDENTIALS|Metalworking \| Packages', t) or int(r['pages'] or 0) <= 4: return 'product data sheet (TDS/PDS)'
    return 'presentation / brochure'


OV = {
    'fabd69720b': ('formulation / approval data', ['16008?'], "MAN approval data form (Juni 2009), internal oil code OS268035: finished-oil approval document; additive named inside not read", None),
    '78574b8bc8': ('product data sheet (TDS/PDS)', ['SCHERCOZOLINE O'], "Lubrizol Advanced Materials 'TECHNICAL DATA SHEET TDS-446 Schercozoline™ O Imidazoline' (Edition February 28, 2007; header viewed as an image)", None),
    '8881a93dc5': ('presentation / brochure', [], "'Enhancing performance under constraint - The evolving additives market' (Kapil Telang, 2026): market presentation", 'non_product'),
    'cdcf52afe4': ('product data sheet (TDS/PDS)', ['EVOGEN 5191SA', 'EVOGEN 5193'], "file 'Evogen 5193.pdf'; page 1 prints 'Evogen 5191SA ELECTRIC VEHICLES' (both names recorded as printed)", None),
    '4bcdc5003b': ('product data sheet (TDS/PDS)', ['JILIN J0010', '7067'], "sheet of 'Jilin J0010' solid OCP VI improver (PetroChina Jilin); Lubrizol 7067 only mentioned", None),
    'c8b5c15871': ('competitor cross-reference table', [], "'Starrychem products alternative to competitive products' (Ver. 20250625): Starrychem's own table naming Lubrizol / Afton / BASF / Evonik products and Starrychem 'equivalents'; equivalence claims are the issuer's, not verified", 'non_product'),
    '206f66eae5': ('formulation / approval data', ['CV1100'], 'Lubrizol CV1100 MB 228.31 read-across matrix (reviewed in the existing-product comparison)', None),
    '7b389e96fe': ('presentation / brochure', [], "'Viscosity Modifiers - Right VM, Right Application' (March 2016): VM portfolio presentation", None),
    '4420e195b2': ('presentation / brochure', [], "'The Value of a High Quality, Proven Viscosity Modifier' (March 2017)", None),
    'af143b0cc0': ('presentation / brochure', [], "'The Value of High Quality, Proven Performance Polymer' (February 2019)", None),
    'cd4086972f': ('presentation / brochure', [], "'Capitalising on the Needs of the Aging Vehicle Parc' (January 2018): market presentation", 'non_product'),
    '673b3d5d92': ('technical report (performance data)', ['5408B'], "IP-1198 'Lubrizol 5408B Multi-functional Industrial Lubricant Package for Slideway, Industrial Gear, and Hydraulic' (17 January 2018)", None),
    '5d2a138f5d': ('technical report (performance data)', ['MC9500'], "IP-1186 'Lubrizol MC9500 Industrial Lubricant Package for Slideway' (August 2017)", None),
    '265b85732a': (None, ['SKOSAN RE'], 'metalworking emulsifier package', None), '18afb3357d': (None, ['SKOSAN S'], 'metalworking emulsifying package', None),
    '703d49dc09': (None, ['SODIUM SULFONATE 425HJ'], 'synthetic sodium sulfonate emulsifier (metal processing)', None),
    'ed82e589b0': (None, ['SOLUBLE BASE GT-1100LAS'], 'metalworking package', None), '8ba2ae5db6': (None, ['SOLUBLE BASE GT-1580VS'], 'metalworking package', None),
    '408402d3b6': (None, ['SOLUBLE BASE GT-1900S'], 'metalworking package', None), '8b62579caf': (None, ['ADDCO ADDTAC'], 'tackifier / anti-mist polymer (metal processing)', None),
    '53990e628b': (None, ['CONTRAM ST-1'], 'metalworking biocide', None), '353fd9aabf': (None, ['CONTRAM ST-2'], 'metalworking biocide', None),
    '5a541a26d1': (None, ['SG9L01'], 'stationary natural gas engine oil additive', None), '4ed84c0be0': (None, ['SG9L20'], 'stationary natural gas engine oil additive', None),
    '1a681b8727': ('product data sheet (TDS/PDS)', ['7067C'], "'Lubrizol 7067C is a 25 SSI non-dispersant olefin copolymer viscosity modifier'", None),
    'f2861b13b0': ('product data sheet (TDS/PDS)', ['CVT10'], 'CVT10 leaflet (market need / features)', None),
    '568a593139': ('product data sheet (TDS/PDS)', ['AT9231'], "'Lubrizol® AT9231 Multi-Vehicle DCT Fluid Additive' (header viewed as an image)", None),
}
D, PK = {}, {}
for r in A:
    sha = r['sha256']
    ov = next((v for k, v in OV.items() if sha.startswith(k)), None)
    typ = dtype(r)
    if ov:
        typ, grades, note, rel = (ov[0] or typ), ov[1], ov[2], ov[3] or 'product'
    else:
        g = key(r['primary_identity']) if r['primary_identity'] else ''
        grades, note, rel = ([g] if g else []), '', ('product' if g else 'unresolved_identity')
    if grades == ['16008?']:
        grades, rel = [], 'product'
        note += '; the additive grade is not on page 1 (not assumed)'
    if r['byte_duplicate_of_existing']:
        note = (note + '; ' if note else '') + 'byte duplicate of an old-archive file'
    roles = {'LUBRIZOL:' + g: ('mentioned' if g == '7067' or (g == 'EVOGEN 5193' and len(grades) > 1) else 'subject') for g in grades}
    D[sha[:12]] = dict(doc_type=typ, supplier=SUP if not any(g.startswith('JILIN') for g in grades) else 'PetroChina Jilin (named on the sheet)',
                       products=['LUBRIZOL:' + g for g in grades], roles=roles, relation=rel, read=R, note=note,
                       next_action='' if grades or rel == 'non_product' else 'identify the subject products inside (multi-product deck or approval form)')
    for g in grades:
        k = 'LUBRIZOL:' + g
        if k in PK: continue
        if g.startswith('SLF'):
            mc, n = 'out_of_template: finished lubricant', "Lubrizol 'Fluid Supply Services' finished fluid: no finished-lubricant template (schema gap)"
        elif g.startswith('ULTRAZOL'):
            mc, n = 'out_of_template: fuel additive', 'gasoline / refinery additive: no template'
        elif g in METAL:
            mc, n = 'additive_component', 'metalworking / metal-processing product: fits the component general block, but the application is outside lubricating-oil formulation (scope question)'
        elif g in COMP:
            mc, n = 'additive_component', COMP[g]
        elif g.startswith('JILIN'):
            mc, n = 'additive_component', 'PetroChina Jilin solid OCP VI improver (VM subtype)'
        else:
            mc, n = 'additive_package', ''
        st = 'existing' if g in EXIST else ('out_of_scope' if mc.startswith('out_of_template') else 'new_candidate')
        PK[k] = dict(name=('Lubrizol ' + g) if re.match(r'^[A-Z]{0,3}\d', g) else g.title() if g.isupper() and ' ' in g else g,
                     supplier=SUP if not g.startswith('JILIN') else 'PetroChina Jilin', material_class=mc, existing_record=EXIST.get(g, ''), status=st, notes=n,
                     identity_evidence='printed grade on the documents linked in this batch',
                     template={'additive_package': 'additive_package tier1 + tier2', 'additive_component': 'additive_component general (+ subtype as noted)'}.get(mc, 'none (see notes)'))
out = dict(batch='S04 Lubrizol (identity)', reviewed_on='2026-11-14', scope='196 documents with provisional supplier Lubrizol', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's04_lubrizol.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(v['doc_type'] for v in D.values()), Counter(v['relation'] for v in D.values()), Counter(p['status'] for p in PK.values()))
print(sorted(PK))
