"""Supplier batches S33 NYCO (13 docs), S34 King Industries (12), S35 Evonik (11).

S33 NYCO. NYCO S.A. (Paris, France) makes NYCOBASE® synthetic polyol ester base stocks: TMP esters
(trimethylolpropane), pentaerythritol esters, complex esters and high-temperature neopolyol esters.
Used in compressor, aviation and industrial lubricants. 6 specific-product TDS + 2 CoAs → 6 products.
4 non-product: two range property tables (DL2-13023 8pp×2 and DL2-13133 2pp) and two application
guides for compressor oil product selection (DL2-13825 and DL2-13134 5pp each).
Material class: unresolved (ester: base fluid vs additive_component; no API group in the template).

S34 King Industries. King Industries, Inc. (Norwalk CT, USA) makes NA-LUBE® and NA-SUL® specialty
additives. Products in this batch: NA-LUBE AO-142-I (DPA antioxidant), NA-LUBE BL-1208 (ashless
R&O additive package for turbine/industrial oils), NA-LUBE KR-008 and KR-019 (specialty synthetic
fluids / base oil modifiers), NA-SUL BSN (barium sulfonate rust inhibitor).
Mislabeled: DL2-15643 — a Dover Chemical Corporation trademark notice page (DOVERNOX®, DOVERPHOS®,
CHLOROWAX® etc. registered trademarks); product name not on the page; unresolved identity.
DL2-14948 (AO-142-I comparative study) → non_product.

S35 Evonik. Evonik Industries AG (formerly RohMax Additives) makes VISCOPLEX® PMA viscosity modifiers.
Eight specific grades: 0-223 (gear oil VII), 1-254 (shear-stable VII/PPD), 4-677 (engine oil VII/PPD
multifunction), 7-310 (hydraulic arctic VII), 8-200 (hydraulic VII/PPD), 8-251 (hydraulic VII, two TDS
editions), 8-400 (hydraulic VII), 14-520 (defoamer for lubricating oils — different from VM grades).
Unresolved: DL2-14627 (9pp 2013 MSDS for a hydraulic VII, product name not in extractable text layer)
and DL2-11204 (1pp RohMax contact/disclaimer page, no product data).

Writes decisions/s33_nyco.json, s34_king.json, s35_evonik.json."""
import re
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S33 NYCO
# ===========================================================================
SUP33 = 'NYCO S.A.'
MFG33 = SUP33
U = 'unresolved'
AP = 'additive_package'
AC = 'additive_component'

NYCOBASE = {
    'ac79e22282': ('NYCO:NYCOBASE_20798', 'NYCOBASE 20798',
                   "printed: 'NYCOBASE 20798 TRIMETHYLOLPROPANE ESTER'; TDS ref TDS_NB20798-1E2"),
    '87ba51b075': ('NYCO:NYCOBASE_5750', 'NYCOBASE 5750',
                   "printed: 'NYCOBASE 5750 PENTAERYTHRITOL ESTER'"),
    '0dd72d01c2': ('NYCO:NYCOBASE_7300', 'NYCOBASE 7300',
                   "printed: 'NYCOBASE 7300 TRIMETHYLOLPROPANE ESTER'; TDS ref TDS_NB7300-1E10; x2 copies in archive"),
    'a883d8265b': ('NYCO:NYCOBASE_8103', 'NYCOBASE 8103',
                   "printed: 'NYCOBASE 8103 TRIMETHYLOLPROPANE ESTER'; TDS ref TDS_NB8103-1E12"),
    'a60aecac8a': ('NYCO:NYCOBASE_8851', 'NYCOBASE 8851',
                   "printed: 'NYCOBASE 8851 TRIMETHYLOLPROPANE COMPLEX ESTER'; TDS ref TDS_NB8851-1E6"),
    '1f3bdc6c72': ('NYCO:NYCOBASE_9680X', 'NYCOBASE 9680X',
                   "printed: 'NYCOBASE 9680X HIGH TEMPERATURE NEOPOLYOL ESTER'; TDS ref TDS_NB9680X-1E2; 2pp"),
}

D33, PK33 = {}, {}
for p10, (key, name, notes) in NYCOBASE.items():
    prod(PK33, key, name, SUP33, U,
         notes + '; synthetic polyol ester base stock for compressor / aviation lubricants; '
         'ester: base fluid vs additive_component to confirm; no API group in the template')

for r in rows(lambda s: s == 'NYCO', 's33_nyco.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in NYCOBASE:
        key, name, _ = NYCOBASE[p10]
        is2pp = p10 == '1f3bdc6c72'
        doc(D33, sha, 'product data sheet (TDS/PDS)', SUP33, [key],
            'page-1 text (product name, ester type, typical data)',
            manufacturer=MFG33, issuer=SUP33,
            note=('2pp' if is2pp else '1pp') + '; NYCO Technical Data Sheet')
    elif p10 in ('df6c985cbb', '41393b1f7d', 'b5a09e2935'):
        # SDS and CoAs
        if p10 == 'df6c985cbb':
            k, n = 'NYCO:NYCOBASE_5750', 'NYCOBASE 5750 SDS'
            note = "'No legal obligation to provide SDS for this substance'; " \
                   "'Date of issue: 04/10/2012 Revision date: 10/04/2018 Version: 4.1'; 5pp"
            dt = 'SDS'
        elif p10 == '41393b1f7d':
            k, n = 'NYCO:NYCOBASE_5750', 'NYCOBASE 5750 CoA'
            note = "'CERTIFICATE OF ANALYSIS CUSTOMER: RENEWABLE ENERGY FZE BATCH N°5012101160 " \
                   "ORDER EMAIL 12/03/2021'; 1pp"
            dt = 'certificate of analysis (batch)'
        else:  # b5a09e2935 7300 CoA
            k, n = 'NYCO:NYCOBASE_7300', 'NYCOBASE 7300 CoA'
            note = "'CERTIFICATE OF ANALYSIS'; kV100 3.42 cSt (spec 3.10-3.70), Density 0.959 kg/dm³; 1pp"
            dt = 'certificate of analysis (batch)'
        doc(D33, sha, dt, SUP33, [k], 'page-1 text (product name, test results)',
            manufacturer=MFG33, issuer=SUP33, note=note)
    elif p10 in ('6b44cc3c61', '83f04c4009'):
        doc(D33, sha, 'product range reference (properties table)', SUP33, [],
            'page text: multi-product NYCOBASE properties table',
            relation='non_product', issuer=SUP33,
            note="'NYCOBASE® PROPERTIES PRODUCT REFERENCE Chemical description...'; "
                 "table listing all NYCOBASE grades with kV40, kV100, VI, density, PP, FP, Noack, iodine, saponification numbers; "
                 + ('x2 copies; 8pp (longer edition)' if p10 == '6b44cc3c61' else '2pp (shorter edition)'))
    elif p10 in ('1f0faeb842', 'ff7e7b959a'):
        title = 'COMPRESSOR OILS' if p10 == '1f0faeb842' else 'AIR COMPRESSOR OILS'
        doc(D33, sha, 'application technical guide', SUP33, [],
            'page-1 text (product selection guide for compressor oils using NYCOBASE esters)',
            relation='non_product', issuer=SUP33,
            note=f"'PRODUCT SELECTION FOR {title}'; 5pp; discusses neopolyol ester advantages for compressor oil formulation; "
                 "mentions NYCOBASE products as examples; no specific product as subject")

write('s33_nyco.json', 'S33 NYCO (identity)', '13 documents with provisional supplier NYCO', PK33, D33)

# ===========================================================================
# S34 King Industries
# ===========================================================================
SUP34 = 'King Industries, Inc.'
MFG34 = SUP34

D34, PK34 = {}, {}
prod(PK34, 'KINGINDUSTRIES:NA_LUBE_AO_142_I', 'NA-LUBE AO-142-I', SUP34, AC,
     "printed: 'NA-LUBE AO-142-I is a liquid diphenylamine based antioxidant for synthetic and "
     "mineral oil based lubricants and greases'; DPA antioxidant type; additive_component (antioxidant)")
prod(PK34, 'KINGINDUSTRIES:NA_LUBE_BL_1208', 'NA-LUBE BL-1208', SUP34, AP,
     "printed: 'NA-LUBE BL-1208 Multifunctional Ashless R&O Package for Industrial Oils; "
     "ashless, multifunctional additive package for turbine oils, R&O oils, and compressor oils'; "
     "additive_package for industrial (turbine / R&O / hydraulic) oils, not engine oil")
prod(PK34, 'KINGINDUSTRIES:NA_LUBE_KR_008', 'NA-LUBE KR-008', SUP34, U,
     "printed: 'NA-LUBE KR-008 is a specialty synthetic fluid for high performance lubricants "
     "offering outstanding solubility plus excellent hydrolytic and thermo-oxidative stability; "
     "CHEMICAL COMPOSITION: Proprietary alkylated aromatic'; base stock modifier or specialty solvent; "
     "material class and template to be confirmed")
prod(PK34, 'KINGINDUSTRIES:NA_LUBE_KR_019', 'NA-LUBE KR-019', SUP34, U,
     "printed: 'NA-LUBE KR-019 is a unique additive & base oil modifier offering excellent "
     "hydrolytic and thermo-oxidative stability; recommended for use in gear oils'; "
     "base oil modifier: could be additive_component or unresolved class")
prod(PK34, 'KINGINDUSTRIES:NA_SUL_BSN', 'NA-SUL BSN', SUP34, AC,
     "printed: 'NA-SUL BSN is a premium non-staining rust inhibitor for petroleum and synthetic "
     "lubricants, greases, rust preventive fluids and metalworking specialties'; "
     "barium sulfonate rust inhibitor; additive_component (corrosion inhibitor)")
prod(PK34, 'DOVER:UNKNOWN_DOC_DL2_15643', 'Unknown Dover Chemical product', 'Dover Chemical Corporation',
     U, 'product name not on page (only Dover Chemical trademark notice: DOVERNOX®, DOVERPHOS®, CHLOROWAX® etc.); '
     'mislabeled under King Industries in automated classification; identity unresolved',
     evidence='Dover Chemical trademark notice page; no product name in extractable text')

for r in rows(lambda s: s == 'King Industries', 's34_king.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '39a7f5fadd':  # DL2-14947 AO-142-I PDS (2pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_LUBE_AO_142_I'],
            'page-1 text (product name, type, description)', manufacturer=MFG34, issuer=SUP34,
            note="2pp; 'NA-LUBE AO-142-I is a liquid diphenylamine based antioxidant for synthetic and mineral oil based lubricants and greases'")
    elif p10 == 'c65c5066f5':  # DL2-14948 AO-142-I comparative study (5pp)
        doc(D34, sha, 'comparative study (marketing)', SUP34, ['KINGINDUSTRIES:NA_LUBE_AO_142_I'],
            'page-1 text (comparative claim)',
            relation='non_product', issuer=SUP34,
            note="'NA-LUBE AO-142-I vs. Competitive Product'; 5pp comparative/marketing document; subject AO-142-I is mentioned but document is not a TDS or SDS")
    elif p10 == '5ff875cfbd':  # DL2-11419 BL-1208 TDS (12pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_LUBE_BL_1208'],
            'page-1 text (product name and type)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE BL-1208 Multifunctional Ashless R&O Package for Industrial Oils'; 12pp TDS")
    elif p10 == '1550ea1a8f':  # DL2-11696 BL-1208 PDS (2pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_LUBE_BL_1208'],
            'page-1 text (product name, composition note, properties)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE BL-1208 is a multifunctional premium ashless R&O additive package for industrial oils'; "
                 "'CHEMICAL COMPOSITION: Proprietary preparation'; 2pp")
    elif p10 == 'fc88711a8e':  # DL2-11697 BL-1208 performance evaluation (17pp)
        doc(D34, sha, 'performance evaluation report', SUP34, ['KINGINDUSTRIES:NA_LUBE_BL_1208'],
            'page-1 text (product and report title)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE BL-1208 Performance Evaluation Program'; 17pp; "
                 "'ashless, multifunctional additive package for turbine oils, R&O oils, and compressors oils'; "
                 "evaluation data for 0.45% BL-1208 in various base oils")
    elif p10 == 'eeea8dbc0c':  # DL2-12838 BL-1208 application notes (3pp)
        doc(D34, sha, 'application technical note', SUP34, ['KINGINDUSTRIES:NA_LUBE_BL_1208'],
            'page-1 text (product and application description)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE BL-1208 Ashless Multifunctional R&O Package'; 3pp; "
                 "formulation guidance for turbine oils, R&O oils, hydraulic fluids HL, gear oils CL; "
                 "Cincinnati Lamb and ISO test references")
    elif p10 == '9c0ebc98e4':  # DL2-14391 BL-1208 CoA (1pp)
        doc(D34, sha, 'certificate of analysis (batch)', SUP34, ['KINGINDUSTRIES:NA_LUBE_BL_1208'],
            'page-1 text (product name, lot number, CoA results)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE BL-1208 LOT# 08641 MFG.DATE 08/11/2020'; kV40 139 cSt (spec 115-165), %S 6.96 (spec 6.40-7.20); 1pp")
    elif p10 == 'adc1259dc5':  # DL2-11892 KR-008 PDS (2pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_LUBE_KR_008'],
            'page-1 text (product name and description)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE KR-008... specialty synthetic fluid... CHEMICAL COMPOSITION: Proprietary alkylated aromatic'; 2pp")
    elif p10 == 'beddfa6fd5':  # DL2-12836 KR-019 PDS (2pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_LUBE_KR_019'],
            'page-1 text (product name and description)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-LUBE KR-019 unique additive & base oil modifier... recommended for use in gear oils'; 2pp")
    elif p10 == 'a796dc2229':  # DL2-14395 NA-SUL BSN TDS (1pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_SUL_BSN'],
            'page-1 text (product name and test results table)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-SUL BSN'; tests listed: Appearance, %Sulfonate, kV100, Moisture, Barium content, Color, Flash point, Neutralization No., SG; 1pp")
    elif p10 == '5ef35a1346':  # DL2-12347 NA-SUL BSN PDS (2pp)
        doc(D34, sha, 'product data sheet (TDS/PDS)', SUP34, ['KINGINDUSTRIES:NA_SUL_BSN'],
            'page-1 text (product name and description)', manufacturer=MFG34, issuer=SUP34,
            note="'NA-SUL BSN is a premium non-staining rust inhibitor for petroleum and synthetic lubricants, greases, rust preventive fluids and metalworking specialties'; 2pp")
    elif p10 == '4ea8a9f557':  # DL2-15643 Dover Chemical trademark notice page
        doc(D34, sha, 'product data sheet (last page, trademark notice)', 'Dover Chemical Corporation', ['DOVER:UNKNOWN_DOC_DL2_15643'],
            'page text (Dover Chemical trademark list; no product name)', relation='unresolved_identity',
            manufacturer='Dover Chemical Corporation', issuer='Dover Chemical Corporation',
            note="mislabeled under King Industries; page contains Dover Chemical trademark notice: "
                 "DOVERNOX®, DOVERPHOS®, CHLOROWAX® 40/50, DOVERPHOS S-9228® etc.; "
                 "product name not on this page; likely the last page of a Dover PDS",
            next_action='read other pages to identify Dover product (DOVERPHOS/DOVERNOX/CHLOROWAX range)')

write('s34_king.json', 'S34 King Industries (identity)', '12 documents with provisional supplier King Industries', PK34, D34)

# ===========================================================================
# S35 Evonik
# ===========================================================================
SUP35 = 'Evonik Industries AG'
MFG35 = SUP35

VISCOPLEX = {
    '738c84bd57': ('EVONIK:VISCOPLEX_4_677',  'VISCOPLEX 4-677',
                   "printed: 'VISCOPLEX® 4-677 is a multifunctional engine oil additive combining the functions of "
                   "viscosity index improver (VII) and pour point depressant (PPD); designed for multigrade gasoline and diesel engine oil'",
                   "2pp; engine oil VII/PPD multifunction"),
    'f3789d833a': ('EVONIK:VISCOPLEX_8_400',  'VISCOPLEX 8-400',
                   "printed: 'Viscosity index improver and pour point depressant for hydraulic fluids; "
                   "VISCOPLEX® 8-400 offers high VI improvement in combination with a high level of shear stability'",
                   "2pp; hydraulic VII with PPD"),
    '0c92fd0f82': ('EVONIK:VISCOPLEX_8_251',  'VISCOPLEX 8-251',
                   "printed: 'Viscosity index improver for hydraulic fluids; VISCOPLEX® 8-251 offers high VI improvement "
                   "in combination with very high shear stability'; Technical Information Evonik Industries AG August 2013",
                   "2pp TDS edition 2013"),
    'e9e8d1cd6c': ('EVONIK:VISCOPLEX_7_310',  'VISCOPLEX 7-310',
                   "printed: 'Shear-stable viscosity index improver for special hydraulic fluids; VISCOPLEX® 7-310 is designed "
                   "for use in high-VI arctic and automotive fluids'; Evonik Resource Efficiency GmbH July 2017",
                   "2pp"),
    'fabdd3f8f8': ('EVONIK:VISCOPLEX_8_200',  'VISCOPLEX 8-200',
                   "printed: 'Viscosity index improver with pour point depressant properties for hydraulic fluids; "
                   "VISCOPLEX® 8-200 offers high VI improvement in combination with very high shear stability'",
                   "2pp"),
    'ab32453908': ('EVONIK:VISCOPLEX_1_254',  'VISCOPLEX 1-254',
                   "printed: 'A RohMax Product; Typical Physical Properties: kV100 90 mm2/s, Density 0.90 g/ml, FP 160°C; "
                   "Shear...' (function truncated); RohMax era PMA",
                   "2pp; PMA shear-stable VII/PPD"),
    'c4df3a5053': ('EVONIK:VISCOPLEX_0_223',  'VISCOPLEX 0-223',
                   "printed: 'VISCOPLEX® 0-223 VISCOPLEX® Series 0 Gear Oil Viscosity Index Improvers; "
                   "Viscosity index and low-temperature fluidity improver for multigrade gear oils such as SAE 75W-90'",
                   "2pp"),
    '2201cf07a8': ('EVONIK:VISCOPLEX_8_251',  'VISCOPLEX 8-251',
                   "printed: 'Viscosity index improver for hydraulic fluids'; Evonik Resource Efficiency GmbH July 2015",
                   "2pp TDS edition 2015 (second edition for the same product)"),
}

D35, PK35 = {}, {}

prod(PK35, 'EVONIK:VISCOPLEX_14_520', 'VISCOPLEX 14-520', SUP35, AC,
     "printed: 'VISCOPLEX® 14-520 defoamer for lubricating oils'; 8pp; x2 copies in archive; "
     "VISCOPLEX series 14 = defoamers (polysiloxane-based); additive_component (defoamer)")
for p10, (key, name, notes, _) in VISCOPLEX.items():
    prod(PK35, key, name, SUP35, AC,
         notes + '; additive_component (viscosity modifier / VM subtype)')

for r in rows(lambda s: s == 'Evonik', 's35_evonik.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == 'f650c36c24':  # DL2-13549 VISCOPLEX 14-520 (8pp, x2)
        doc(D35, sha, 'product data sheet (TDS/PDS)', SUP35, ['EVONIK:VISCOPLEX_14_520'],
            'page-1 text (product name: defoamer for lubricating oils)',
            manufacturer=MFG35, issuer=SUP35,
            note="'VISCOPLEX® 14-520 defoamer for lubricating oils'; 8pp; x2 copies in archive; "
                 "VISCOPLEX series 14 = defoamers; not a VM despite being in VISCOPLEX family")
    elif p10 in VISCOPLEX:
        key, name, _, note = VISCOPLEX[p10]
        doc(D35, sha, 'product data sheet (TDS/PDS)', SUP35, [key],
            'page-1 text (product name, function, performance description)',
            manufacturer=MFG35, issuer=SUP35, note=note)
    elif p10 == '191e53a21a':  # DL2-11204 RohMax contact/disclaimer 1pp
        doc(D35, sha, 'contact page (disclaimer and contact addresses)', SUP35, [],
            'page-1 text: RohMax contact addresses (Germany, USA, Asia) + liability disclaimer only',
            relation='unresolved_identity',
            manufacturer='RohMax Additives GmbH / Evonik Industries AG', issuer='RohMax Additives GmbH',
            note="1pp; entire page is RohMax/Degussa contact information and standard liability disclaimer; "
                 "no product name or data; likely a standalone contact sheet or the back/cover of a TDS; "
                 "cannot identify any specific VISCOPLEX product from this page",
            next_action='manual review: may be a standalone page, not associated with a specific product')
    elif p10 == '77b14d733f':  # DL2-14627 Evonik MSDS 9pp
        doc(D35, sha, 'SDS', SUP35, [],
            'pages 1-2: SDS header with product use (viscosity index improver for hydraulic fluids); product name not in extracted text',
            relation='unresolved_identity',
            manufacturer=MFG35, issuer='Evonik Oil Additives USA, Inc.',
            note="'Update 03/20/2013 Version 7'; 'Product Use: Viscosity index improver for hydraulic fluids'; "
                 "'Ingredients... acrylate polymer (PMA)'; product name not in extractable text layer "
                 "(likely in a graphic header or in a form field); "
                 "probable VISCOPLEX 8-series hydraulic VII MSDS; not VISCOPLEX 8-251 (two TDS already present)",
            next_action='OCR or manual read to identify VISCOPLEX grade from section 1 product name')

write('s35_evonik.json', 'S35 Evonik (identity)', '11 documents with provisional supplier Evonik', PK35, D35)
