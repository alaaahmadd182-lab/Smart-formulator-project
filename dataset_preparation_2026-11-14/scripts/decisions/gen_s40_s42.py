"""Supplier batches S40 S-OIL (10), S41 Arkema (10), S42 Songwon (10).

S40 S-OIL Corporation (Seoul, Korea). Maker of Ultra-S® VHVI (Group III) base oils and S-OIL Premium /
S-OIL Super (Group II) base oils. All 5 Ultra-S grades (2/3/4/6/8) are existing records. Documents in
this batch: 5 SDS (one per grade, all dupOLD), two range TDS sheets covering multiple grades (also
dupOLD), one S-OIL transformer oil TDS (out of template: electrical insulating oil), one company
brochure (non_product, OCR-impaired text), and one SDS for a heavy paraffinic product (dupOLD; product
name not in extractable text layer — unresolved_identity).

S41 Arkema Inc. (King of Prussia, PA). Maker of TPS® (tertiaryalkyl polysulfides) and VPS® (vegetable
polysulfides) EP additives for lubricants:
  TPS 20 (ditertiododecyl polysulfide, 20-23% S), TPS 32 (dialkyl pentasulfide, 29-32% S),
  TPS 44 (dialkyl trisulfide, 42-46% S) — polysulfide EP additives, synthetic origin.
  VPS 11 (fatty ester triglyceride, >10% S), VPS 15 (fatty ester triglyceride, 14.5-16% S),
  VPS 17 (fatty ester triglyceride, 16-18% S) — polysulfide EP additives, vegetable/renewable origin.
  10 docs: TDS + SDS pairs for TPS 20, TPS 32, VPS 11, VPS 15; TDS only for TPS 44 and VPS 17.

S42 Songwon Industrial Co., Ltd. (Seoul, Korea). Maker of SONGNOX® antioxidants for lubricants and
polymers. Products in the lubricant-additive scope: L107 (hindered phenol, stearyl ester type),
L135 (hindered phenol ester), L570 (DPA, octylated/butylated diphenylamine), L670 (DPA).
SONGNOX 5057 LQ has the same DPA chemistry (CAS 68411-46-1) as L570 but is primarily sold for
polymer stabilisation — material class left unresolved pending scope confirmation.
10 docs: TDS + SDS for L135 and L570, performance guides for L135/L570/L670, TDS only for L107 and
5057 LQ, plus a 4pp marketing brochure for 5057 LQ.

Writes decisions/s40_soil.json, s41_arkema.json, s42_songwon.json."""
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S40 S-OIL
# ===========================================================================
SUP40 = 'S-OIL Corporation'
MFG40 = SUP40
B = 'base_oil'
OWN40 = 's40_soil.json'

ULTRA_S = {
    'EXISTING:S_OIL_ULTRA_S_2': ('S_OIL_ULTRA_S_2', 'Ultra-S 2 (60 Neutral)'),
    'EXISTING:S_OIL_ULTRA_S_3': ('S_OIL_ULTRA_S_3', 'Ultra-S 3 (70 Neutral)'),
    'EXISTING:S_OIL_ULTRA_S_4': ('S_OIL_ULTRA_S_4', 'Ultra-S 4 (100 Neutral)'),
    'EXISTING:S_OIL_ULTRA_S_6': ('S_OIL_ULTRA_S_6', 'Ultra-S 6 (150 Neutral)'),
    'EXISTING:S_OIL_ULTRA_S_8': ('S_OIL_ULTRA_S_8', 'Ultra-S 8 (250 Neutral)'),
}
SDS40 = {
    # sha10: (key, grade_name, rev_note)
    '2f41b47d9b': ('EXISTING:S_OIL_ULTRA_S_2', 'Ultra-S 2 (60 Neutral)',
                   "dupOLD; 'Base Oil Ultra-S 2 (60 Neutral)'; SDS Rev. 5, Revision Date June 10, 2015; 4pp"),
    '0d23219a4c': ('EXISTING:S_OIL_ULTRA_S_3', 'Ultra-S 3 (70 Neutral)',
                   "dupOLD; 'Base Oil Ultra-S 3 (70 Neutral)'; SDS Rev. 5, Revision Date June 10, 2015; 4pp"),
    '33983c4d3d': ('EXISTING:S_OIL_ULTRA_S_4', 'Ultra-S 4 (100 Neutral)',
                   "dupOLD; 'Base Oil Ultra-S 4 (100 Neutral)'; SDS Rev. 5, Revision Date June 10, 2015; 4pp"),
    '205ff9f5d6': ('EXISTING:S_OIL_ULTRA_S_6', 'Ultra-S 6 (150 Neutral)',
                   "dupOLD; 'Base Oil Ultra-S 6 (150 Neutral)'; SDS Rev. 5, Revision Date June 10, 2015; 4pp"),
    'a05a608b92': ('EXISTING:S_OIL_ULTRA_S_8', 'Ultra-S 8 (250 Neutral)',
                   "dupOLD; 'Base Oil Ultra-S 8 (250 Neutral)'; SDS Rev. 5, Revision Date June 10, 2015; 4pp"),
}

D40, PK40 = {}, {}
for key, (rec, name) in ULTRA_S.items():
    prod(PK40, key, name, SUP40, B,
         'printed product name on the documents linked in this batch', existing=rec)
prod(PK40, 'SOIL:TRANSFORMER_OIL_TI', 'S-OIL Transformer Oil T/I', SUP40,
     'out_of_template (electrical insulating oil)',
     "printed: 'S-OIL TRANSFORMER OIL T/I HIGHLY REFINED HYDROTREATED ELECTRICAL INSULATING OIL "
     "(Trace-inhibited / Inhibited)'; electrical insulating oil — out of template for lubricant base oil / additive database")

for r in rows(lambda s: s == 'S-OIL', OWN40):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in SDS40:
        key, name, note = SDS40[p10]
        doc(D40, sha, 'SDS', SUP40, [key],
            'page-1 text (product name, CAS class, SDS revision date)',
            manufacturer=MFG40, issuer=MFG40, note=note)
    elif p10 == 'a2cf10bf67':  # DL2-11177 Ultra-S range TDS 1pp x5
        doc(D40, sha, 'product data sheet (range TDS)', SUP40,
            list(ULTRA_S.keys()),
            'page-1 text: Ultra-S® 5-grade range properties table (kV100, VI, density, PP, FP)',
            manufacturer=MFG40, issuer=MFG40,
            note="dupOLD; 1pp x5 copies; 'Ultra-S® series consists of five viscosity grades, Ultra-S® 2, 3, 4, 6 and 8'; "
                 "range TDS covering all five grades with typical properties table")
    elif p10 == '705b8a2860':  # DL2-11240 Ultra-S 4/6/8 range TDS 1pp x3
        doc(D40, sha, 'product data sheet (range TDS)', SUP40,
            ['EXISTING:S_OIL_ULTRA_S_4', 'EXISTING:S_OIL_ULTRA_S_6', 'EXISTING:S_OIL_ULTRA_S_8'],
            'page-1 text: Ultra-S Series 4/6/8 typical properties table',
            manufacturer=MFG40, issuer=MFG40,
            note="dupOLD; 1pp x3 copies; 'Typical Properties Ultra-S Series... Ultra-S 4, Ultra-S 6, Ultra-S 8'; "
                 "partial range TDS covering only grades 4, 6, 8")
    elif p10 == '0617afb876':  # DL2-12265 Transformer Oil T/I 1pp
        doc(D40, sha, 'product data sheet (TDS/PDS)', SUP40, ['SOIL:TRANSFORMER_OIL_TI'],
            'page-1 text: product name and type description',
            manufacturer=MFG40, issuer=MFG40,
            note="'S-OIL TRANSFORMER OIL T/I HIGHLY REFINED HYDROTREATED ELECTRICAL INSULATING OIL "
                 "(Trace-inhibited / Inhibited)'; 1pp TDS; out_of_template")
    elif p10 == '9aea001c7c':  # DL2-12545 S-OIL lube base oil brochure 6pp
        doc(D40, sha, 'company/product brochure (lube base oil range)', SUP40, [],
            'page text (OCR-impaired): S-OIL company profile, lube base oil range overview',
            relation='non_product', issuer=MFG40,
            note="6pp; OCR-impaired text (scanned document); 'Lube Base Oil S·OIL Company Profile'; "
                 "covers Ultra-S, Premium and Super ranges; not a product-specific TDS; "
                 "company overview brochure for the base oil product range")
    elif p10 == 'b1699931d2':  # DL2-14611 SDS 4pp dupOLD
        doc(D40, sha, 'SDS', SUP40, [],
            'page text (partial): SDS for a hydrotreated heavy paraffinic distillate; product name not in text layer',
            relation='unresolved_identity',
            manufacturer=MFG40, issuer=MFG40,
            note="dupOLD; 4pp SDS; 'Distillates (petroleum), hydrotreated heavy paraffinic / 4'; "
                 "product name not in extractable text layer (product identifier likely in a graphic header); "
                 "probable Ultra-S 6 or Ultra-S 8 SDS given heavy paraffinic classification",
            next_action='read header or OCR to identify S-OIL product name (Ultra-S 6 or 8)')

write(OWN40, 'S40 S-OIL (identity)', '10 documents with provisional supplier S-OIL', PK40, D40)

# ===========================================================================
# S41 Arkema
# ===========================================================================
SUP41 = 'Arkema Inc.'
MFG41 = SUP41
AC = 'additive_component'
OWN41 = 's41_arkema.json'

TPS = {
    'ARKEMA:TPS_20': ('TPS 20', 'bfbe2bc10a', '765d3a343b',
                      "printed: 'TPS 20 Tertiaryalkyl Poly-sulfedes Ditertiododecyl Polysulfide; "
                      "Sulfur Content (ASTM D4794) %wt 20-23; CAS/Appearance Clear Light Yellow Fluid'; "
                      "EP/sulfur additive (synthetic origin); additive_component (EP additive)"),
    'ARKEMA:TPS_32': ('TPS 32', 'f64497f6d4', 'b18b5cdacf',
                      "printed: 'TPS 32 Tertiaryalkyl Poly-sulfedes Dialkyl Penta-sulfide; "
                      "Sulphur Content (Active) %wt 29-32 (23)'; EP/sulfur additive; additive_component"),
    'ARKEMA:TPS_44': ('TPS 44', '96b2b1975a', None,
                      "printed: 'TPS 44 Tertiaryalkyl Poly-sulfedes Dialkyl Tri-sulfide; "
                      "Sulfur Content (ASTM D4794) %wt 42-46'; EP/sulfur additive; additive_component"),
    'ARKEMA:VPS_11': ('VPS 11', '946493e528', 'b923519a33',
                      "printed: 'VPS 11 Vegetable Poly-sulfides Fatty Ester Triglyceride; "
                      "Sulfur Content (Active) %wt >10 (<1)'; EP additive, renewable/vegetable-oil origin; additive_component"),
    'ARKEMA:VPS_15': ('VPS 15', '6d43103e60', 'ade4932914',
                      "printed: 'VPS 15 Vegetable Poly-sulfides Fatty Ester Triglyceride; "
                      "Sulfur Content (Active) %wt 14.5-16.0 (8)'; EP additive, renewable origin; additive_component"),
    'ARKEMA:VPS_17': ('VPS 17', '00ad91ffe9', None,
                      "printed: 'VPS 17 Vegetable Poly-sulfides Fatty Ester Triglyceride; "
                      "Sulfur Content (Active) %wt 16.0-18.0 (8)'; EP additive, renewable origin; additive_component"),
}
SDS_SHA10 = {
    '765d3a343b': 'ARKEMA:TPS_20',
    'b18b5cdacf': 'ARKEMA:TPS_32',
    'b923519a33': 'ARKEMA:VPS_11',
    'ade4932914': 'ARKEMA:VPS_15',
}

D41, PK41 = {}, {}
for key, (name, tds_p10, sds_p10, notes) in TPS.items():
    prod(PK41, key, name, SUP41, AC, notes)

for r in rows(lambda s: s == 'Arkema', OWN41):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in SDS_SHA10:
        key = SDS_SHA10[p10]
        name = TPS[key][0]
        doc(D41, sha, 'SDS', SUP41, [key],
            'page-1 text: SDS header with product name and product code',
            manufacturer=MFG41, issuer=MFG41,
            note=f"'{name}'; Arkema Inc., King of Prussia PA; 6–12pp GHS SDS")
    else:
        # TDS docs — match by p10 to TPS tds_p10 field
        for key, (name, tds_p10, sds_p10, _) in TPS.items():
            if p10 == tds_p10:
                doc(D41, sha, 'product data sheet (TDS/PDS)', SUP41, [key],
                    'page-1 text: product name, chemical type, typical properties table',
                    manufacturer=MFG41, issuer=MFG41,
                    note=f"'{name}'; 1pp TDS; Arkema EP sulfur additive")
                break

write(OWN41, 'S41 Arkema (identity)', '10 documents with provisional supplier Arkema', PK41, D41)

# ===========================================================================
# S42 Songwon
# ===========================================================================
SUP42 = 'Songwon Industrial Co., Ltd.'
MFG42 = SUP42
OWN42 = 's42_songwon.json'

D42, PK42 = {}, {}
prod(PK42, 'SONGWON:SONGNOX_5057_LQ', 'SONGNOX 5057 LQ', SUP42, 'unresolved',
     "printed: 'SONGNOX® 5057 LQ Antioxidant; Mixture of octylated & butylated diphenylamine; CAS No: 68411-46-1'; "
     "'Polymer Stabilizers Technical Information'; SONGWON describes 5057 as primarily for polyurethane foam production "
     "in the brochure — material class unresolved (DPA antioxidant used in polymer stabilisation; lubricant applicability to confirm); "
     "same CAS as SONGNOX L570")
prod(PK42, 'SONGWON:SONGNOX_L107', 'SONGNOX L107', SUP42, AC,
     "printed: 'Fuel and Lubricant Additives... L107; Octadecyl-3-(3,5-di-tert-butyl-4-hydroxyphenyl)propionate; "
     "CAS No: 2082-79-3'; stearyl ester of hindered phenol; additive_component (antioxidant, hindered phenol)")
prod(PK42, 'SONGWON:SONGNOX_L135', 'SONGNOX L135', SUP42, AC,
     "printed: 'Fuel and Lubricant Additives Technical Information... SONGNOX® L135; "
     "Benzenepropanoic acid, 3,5-bis(1,1-dimethylethyl)-4-hydroxy-, C7-9-branched alkyl esters; CAS No: 125643-61-0'; "
     "hindered phenol ester antioxidant for lubricants; additive_component (antioxidant)")
prod(PK42, 'SONGWON:SONGNOX_L570', 'SONGNOX L570', SUP42, AC,
     "printed: 'Fuel and Lubricant Additives Technical Information... SONGNOX® L570; "
     "Mixture of octylated & butylated diphenylamine; CAS No: 68411-46-1'; "
     "DPA antioxidant for lubricants; additive_component (antioxidant, DPA type)")
prod(PK42, 'SONGWON:SONGNOX_L670', 'SONGNOX L670', SUP42, AC,
     "printed: 'SONGNOX® L670 Properties and Performance in Lubricants February 2024'; "
     "DPA antioxidant for lubricants (Songwon L-series); additive_component (antioxidant, DPA type); "
     "only performance guide in this batch — no TDS or SDS")

for r in rows(lambda s: s == 'Songwon', OWN42):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == 'b8898c220d':  # DL2-15147 SONGNOX 5057 LQ TDS 1pp
        doc(D42, sha, 'product data sheet (TDS/PDS)', SUP42, ['SONGWON:SONGNOX_5057_LQ'],
            'page-1 text: product name, CAS No., typical properties',
            manufacturer=MFG42, issuer=MFG42,
            note="'SONGNOX® 5057 LQ; Polymer Stabilizers Technical Information 19.05.2022'; 1pp TDS; "
                 "DPA antioxidant; header says Polymer Stabilizers (not Fuel and Lubricant Additives)")
    elif p10 == '54cb73a74f':  # DL2-15148 SONGNOX 5057 LQ brochure 4pp
        doc(D42, sha, 'product brochure (marketing)', SUP42, ['SONGWON:SONGNOX_5057_LQ'],
            'page-1 text: product description and primary application (polyurethane foam)',
            relation='non_product', issuer=MFG42,
            note="'New SONGNOX® 5057 extends SONGWON's range of high-performance antioxidants; "
                 "SONGNOX® 5057 is used in combination with hindered phenols... to protect polyols against "
                 "oxidation during polyurethane foam production'; 4pp marketing brochure; "
                 "primary application is polymer (PU foam), not lubricant")
    elif p10 == '39192984e1':  # DL2-15398 SONGNOX L107 TDS 1pp
        doc(D42, sha, 'product data sheet (TDS/PDS)', SUP42, ['SONGWON:SONGNOX_L107'],
            'page-1 text: product code L107, CAS No., typical properties',
            manufacturer=MFG42, issuer=MFG42,
            note="'Fuel and Lubricant Additives Technical Information 04.08.2020... L107; CAS No: 2082-79-3'; 1pp TDS")
    elif p10 == '2beee424c0':  # DL2-15756 SONGNOX L135 TDS 1pp
        doc(D42, sha, 'product data sheet (TDS/PDS)', SUP42, ['SONGWON:SONGNOX_L135'],
            'page-1 text: product name, CAS No., properties',
            manufacturer=MFG42, issuer=MFG42,
            note="'Fuel and Lubricant Additives Technical Information 04.08.2020 Page 1 of 1 SONGNOX® L135; CAS No: 125643-61-0'; 1pp TDS")
    elif p10 == 'a267745cb9':  # DL2-15720 SONGNOX L135 SDS 8pp
        doc(D42, sha, 'SDS', SUP42, ['SONGWON:SONGNOX_L135'],
            'page-1 text: SDS product identifier',
            manufacturer=MFG42, issuer=MFG42,
            note="'Version No: 3.00 (replaces version 2.05)'; Printing date 01.07.2022; 8pp GHS SDS for SONGNOX® L135")
    elif p10 == '177428ad04':  # DL2-15772 SONGNOX L135 performance guide 17pp
        doc(D42, sha, 'product technical guide (performance data)', SUP42, ['SONGWON:SONGNOX_L135'],
            'page-1 text: product name, guide title',
            manufacturer=MFG42, issuer=MFG42,
            note="'SONGNOX® L135 Properties and Performance in Lubricants February 2024'; 17pp; "
                 "detailed performance data for lubricant formulations (engine oil, gear oil, compressor oil, grease, etc.)")
    elif p10 == 'c9d6354e1e':  # DL2-15703 SONGNOX L570 TDS 1pp
        doc(D42, sha, 'product data sheet (TDS/PDS)', SUP42, ['SONGWON:SONGNOX_L570'],
            'page-1 text: product name, CAS No., properties',
            manufacturer=MFG42, issuer=MFG42,
            note="'Fuel and Lubricant Additives Technical Information 20.10.2022... SONGNOX® L570; CAS No: 68411-46-1'; 1pp TDS; "
                 "same CAS as SONGNOX 5057 LQ; note difference in header (Fuel and Lubricant Additives vs Polymer Stabilizers for 5057)")
    elif p10 == '0b5e839c68':  # DL2-15719 SONGNOX L570 SDS 8pp
        doc(D42, sha, 'SDS', SUP42, ['SONGWON:SONGNOX_L570'],
            'page-1 text: SDS product identifier',
            manufacturer=MFG42, issuer=MFG42,
            note="'Version No: 4.00 (replaces version 3.04)'; Printing date 08.09.2022; 8pp GHS SDS for SONGNOX® L570")
    elif p10 == 'dcded1d7e1':  # DL2-15773 SONGNOX L570 performance guide 20pp
        doc(D42, sha, 'product technical guide (performance data)', SUP42, ['SONGWON:SONGNOX_L570'],
            'page-1 text: product name, guide title',
            manufacturer=MFG42, issuer=MFG42,
            note="'SONGNOX® L570 Properties and Performance in Lubricants February 2024'; 20pp performance guide")
    elif p10 == '268f43c65d':  # DL2-15774 SONGNOX L670 performance guide 20pp
        doc(D42, sha, 'product technical guide (performance data)', SUP42, ['SONGWON:SONGNOX_L670'],
            'page-1 text: product name, guide title',
            manufacturer=MFG42, issuer=MFG42,
            note="'SONGNOX® L670 Properties and Performance in Lubricants February 2024'; 20pp performance guide; "
                 "only document for L670 in this batch; no TDS or SDS")

write(OWN42, 'S42 Songwon (identity)', '10 documents with provisional supplier Songwon', PK42, D42)
