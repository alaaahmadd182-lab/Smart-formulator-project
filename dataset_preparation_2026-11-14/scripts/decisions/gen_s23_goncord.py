"""Supplier batch S23: Goncord Chemical (Singapore) Pte Ltd (29 documents).
Read: compact listing; page-1 text after the letterhead (title line with the grade list) for every document.
Rules: most Goncord sheets are SERIES sheets printing several grades in the title (e.g. 'G1820, G1830, (POE) G2824, G2825'):
every printed grade is linked with role 'series sheet (grade listed in the title)'; grades are not split further. SynCold sheets
are refrigeration compressor lubricants (finished fluids: out of template), linked to the grade printed as the automated identity.
'POE 22# ... 320#' (refrigeration-compressor ester base series) grades are keyed 'POE 22#' etc. as printed.
Classes from the printed title: 'Ester Base Oil' / 'Ester based PAO' / 'PMA Base Oil' -> class unresolved (synthetic base fluid,
base_oil template fit to confirm); 'Polyalphaolefin (PAO) Base Oil' -> base_oil; brake-fluid ester bases -> out of template
(brake fluid); PMA PPD / PMA VII -> component (PPD / VM); GH400 'Engine Oil Additive Package' -> package.
Identity only. Writes decisions/s23_goncord.json."""
import csv, json, os, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
A = [r for r in csv.DictReader(open(os.path.join(PKG, 'tables', 'document_identity_auto.csv'), encoding='utf-8')) if r['supplier_provisional'].startswith('Goncord')]
SUP = 'Goncord Chemical (Singapore) Pte Ltd'
U, B, C, P = 'unresolved', 'base_oil', 'additive_component', 'additive_package'
SERIES = {
    '795886f1d7': (['GH400'], P, "'High Performance Multi-Purpose Engine Oil Additive Package'"),
    '6dd13a5d18': (['GTM68', 'GTM150', 'GTM320', 'G28150', 'G28220', 'G28320', 'G28800'], U, "'Ester Base Oil for High Temperature Chain Oil' (Aromatic GTM / POE G28 series)"),
    '07acd5a9f3': (['GHB295', 'GHB300', 'GHB310'], 'out_of_template: other chemical (brake-fluid base)', "'Ester Base Oil (Boric Acid) for Brake Fluid'"),
    '243e34d780': (['G1820', 'G1830', 'G2824', 'G2825'], U, "'Ester Base Oil for Aviation Engine Oil' (Diester G18xx, POE G282x)"),
    '02c5011ab4': (['G-HFDU-32', 'G-HFDU-46', 'G-HFDU-68'], U, "'Ester Base Oil for Biodegradable Fire Resistant Hydraulic Oil' (Trimethylolpropane Oleate)"),
    'fa865a899a': (['GP15', 'GP25', 'GP35', 'GP45', 'GP50'], U, "'Ester based PAO for High Viscosity Performance'"),
    '51a3047b0f': (['G2820', 'G2823', 'G2835'], U, "'Ester Base Oil (POE) for High Performance Engine Oil'"),
    '6afff8ed11': (['POE 22#', 'POE 32#', 'POE 46#', 'POE 68#', 'POE 100#', 'POE 120#', 'POE 150#', 'POE 170#', 'POE 220#', 'POE 320#'], U, "'Ester Base Oil (POE) for Refrigeration Compressor Oil'"),
    '66ac6439e4': (['G2828'], U, "'Ester Base Oil (POE) for Transformer Oil'"),
    '701e6ecfc0': (['GD2000'], U, "'Ester Base Oil (Polyol Compound) for Gear Oil'"),
    '30be9f7b4c': (['PAO 4', 'PAO 6', 'PAO 8'], B, "'Polyalphaolefin (PAO) Base Oil for High Performance Lubricant'"),
    '5cc35b47b5': (['G6600B'], U, "'PMA Base Oil for Heavy Duty Gear Oil' (polymethacrylate synthetic base oil)"),
    '40002aba71': (['G826P'], C, "'PMA Pour Point Depressant' (PPD subtype)"), 'ea9eeb52ab': (['G886P'], C, "'PMA Pour Point Depressant' (PPD subtype)"),
    '7f872765fa': (['G6100V'], C, "'PMA Viscosity Index Improver' (VM subtype)"), '9957be9a2b': (['G6300V'], C, "'PMA Viscosity Index Improver' (VM subtype)"),
    'dc3d0ab0bd': (['G6500V'], C, "'PMA Viscosity Index Improver' (VM subtype)"), '170f8a79bd': (['G6800V'], C, "'PMA Viscosity Index Improver' (VM subtype)")}
D, PK = {}, {}
for r in A:
    sha, p10 = r['sha256'], r['sha256'][:10]
    if p10 == '52281686e6':
        D[sha[:12]] = dict(doc_type='product structure overview (multi-product)', supplier=SUP, products=[], roles={}, relation='product', read='page-1 listing',
                           note="'Goncord Products Structure' overview", next_action='list the products inside (multi-product)')
        continue
    if p10 in SERIES:
        grades, mc, n = SERIES[p10]
    else:
        grades, mc = ['SYNCOLD ' + r['primary_identity'].strip().upper()], 'out_of_template: finished lubricant (refrigeration compressor oil)'
        m = re.search(r'Introduction \| ([^|]{0,90})|Product Description \| ([^|]{0,90})', r['top_lines'].replace('\n', ' | '))
        n = 'SynCold refrigeration lubricant: ' + ((m.group(1) or m.group(2)) if m else '')
    ks = ['GONCORD:' + g for g in grades]
    D[sha[:12]] = dict(doc_type='product data sheet (TDS/PDS)', supplier=SUP, products=ks, roles={k: ('subject' if len(ks) == 1 else 'series sheet (grade listed in the title)') for k in ks},
                       relation='product', read='page-1 text (title / grade list)', note=n if len(ks) > 1 else '', next_action='')
    for k in ks:
        PK.setdefault(k, dict(name=k.split(':', 1)[1], supplier=SUP, material_class=mc, existing_record='', status='out_of_scope' if mc.startswith('out_of') else 'new_candidate',
                              notes='printed: ' + n + ('' if mc != U else ' (synthetic base fluid: base_oil template fit to confirm)'), identity_evidence='printed grade on the documents linked in this batch',
                              template={B: 'base_oil tier1-3', C: 'additive_component general (+ subtype)', P: 'additive_package tier1 + tier2'}.get(mc, 'not determined')))
out = dict(batch='S23 Goncord (identity)', reviewed_on='2026-11-14', scope='29 documents with provisional supplier Goncord', products=PK, documents=D)
json.dump(out, open(os.path.join(PKG, 'decisions', 's23_goncord.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(D), 'documents', len(PK), 'products', Counter(p['material_class'] for p in PK.values()))
