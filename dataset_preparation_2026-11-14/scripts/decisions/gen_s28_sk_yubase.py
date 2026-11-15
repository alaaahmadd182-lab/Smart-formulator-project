"""S28: SK (YUBASE) — 17 documents.
Read: page-1 text (text layer) for every document 2026-11-15.

SK Lubricants Co., Ltd. (South Korea) makes YUBASE Group III base oils (grades 3, 4, 4 Plus, 5, 6).
YUBASE 3, 4, 5, 6 have existing production records. YUBASE 4 Plus (YUBASE 4P) is a distinct grade
not in the existing records: confirmed by its own SDS (YUBASE_SDS_GLOBAL_UN_4_PLUS) and by its
separate listing alongside YUBASE 4 in the Afton DL2-13231 formulation (kV100 4.164 vs 4.224 cSt).

Mislabeled documents (3): DL2-15502 and DL2-15503 (Ocean Chemical Technology Co., Ltd. HC6247
Hydro-Diene Polymer VM) and DL2-15627 (Dowpol Chemical International Corp. NeoFlex 680 PPD) were
classified under the SK (YUBASE) provisional label; the actual manufacturers are different. Identity
corrected here; neither product is in any existing decision file.

Non-product documents (4): DL2-11732 (Yubase formulation qualification table), DL2-11733 (Ford
WSS-M2C913-D supplement listing Yubase 4 and 6 as approved blend stocks), DL2-12438 (Infineum P6003
engine test programme in Yubase base stocks), DL2-13231 (Afton HiTEC 11180 final formulations using
Yubase 4, 6 and 4 Plus).

Writes decisions/s28_sk_yubase.json."""
from dec_common import rows, page_text, top, doc, prod, write

SUP = 'SK Lubricants Co., Ltd.'
MFG = SUP
B = 'base_oil'
C = 'additive_component'
OWN = 's28_sk_yubase.json'

# YUBASE existing-record shorthand
YUBASE = {
    'YUBASE 3': ('SK:YUBASE_3', 'YUBASE_3'),
    'YUBASE 4': ('SK:YUBASE_4', 'YUBASE_4'),
    'YUBASE 5': ('SK:YUBASE_5', 'YUBASE_5'),
    'YUBASE 6': ('SK:YUBASE_6', 'YUBASE_6'),
}

D, PK = {}, {}

# Register products up front so non-product docs can reference them
for name, (key, rec) in YUBASE.items():
    prod(PK, key, name, SUP, B, 'printed product name on the documents linked in this batch', existing=rec)
prod(PK, 'SK:YUBASE_4P', 'YUBASE 4 Plus (YUBASE 4P)', SUP, B,
     "YUBASE 4 Plus (also called YUBASE 4P); SK SDS product identifier 'YUBASE 4 Plus (YUBASE 4P)'; "
     "listed separately from YUBASE 4 in Afton formulation DL2-13231 with kV100 4.164 cSt (vs 4.224 for YUBASE 4); "
     "Group III base oil; not merged with YUBASE_4")
prod(PK, 'OCEANCHEMICAL:HC6247', 'HC6247', 'Ocean Chemical Technology Co., Ltd.', C,
     "printed: 'HC6247 is a star type hydro-diene polymer with the appearance of a semi-transparent adhesive block; "
     "with excellent shear stability (SSI<5)'; VM (viscosity modifier) subtype; "
     "document was mislabeled under SK (YUBASE) in automated classification")
prod(PK, 'DOWPOL:NEOFLEX_680', 'NeoFlex 680', 'Dowpol Chemical International Corp.', C,
     "printed: 'NeoFlex 680 Pour Point Depressant is based on the Neo Synthetic Hydrocarbon chemistry; "
     "it delivers good low-temperature performance that adapts to a variety of base oils'; PPD subtype; "
     "document was mislabeled under SK (YUBASE) in automated classification")

for r in rows(lambda s: s == 'SK (YUBASE)', OWN):
    sha = r['sha256']
    p10 = sha[:10]

    # --- four NARMAK TRADE distributor sheets (dupOLD, 1pp each) ---
    if p10 == '37238f1ddb':  # DL2-11303 YUBASE 3
        doc(D, sha, 'product data sheet (distributor)', 'Narmak Trade s.r.o.', ['SK:YUBASE_3'],
            'page-1 text (grade name and property table)',
            manufacturer=MFG, distributor='Narmak Trade s.r.o.', issuer='Narmak Trade s.r.o.',
            note='dupOLD; Narmak Trade s.r.o. (Czech Republic) distributor data sheet; manufacturer SK Lubricants printed implicitly via brand YUBASE')
    elif p10 == '0d8b8c389b':  # DL2-11304 YUBASE 4
        doc(D, sha, 'product data sheet (distributor)', 'Narmak Trade s.r.o.', ['SK:YUBASE_4'],
            'page-1 text (grade name and property table)',
            manufacturer=MFG, distributor='Narmak Trade s.r.o.', issuer='Narmak Trade s.r.o.',
            note='dupOLD; Narmak Trade s.r.o. (Czech Republic) distributor data sheet')
    elif p10 == '13f642c38d':  # DL2-11305 YUBASE 5
        doc(D, sha, 'product data sheet (distributor)', 'Narmak Trade s.r.o.', ['SK:YUBASE_5'],
            'page-1 text (grade name and property table)',
            manufacturer=MFG, distributor='Narmak Trade s.r.o.', issuer='Narmak Trade s.r.o.',
            note='dupOLD; Narmak Trade s.r.o. (Czech Republic) distributor data sheet')
    elif p10 == 'c3bac1888f':  # DL2-11306 YUBASE 6
        doc(D, sha, 'product data sheet (distributor)', 'Narmak Trade s.r.o.', ['SK:YUBASE_6'],
            'page-1 text (grade name and property table)',
            manufacturer=MFG, distributor='Narmak Trade s.r.o.', issuer='Narmak Trade s.r.o.',
            note='dupOLD; Narmak Trade s.r.o. (Czech Republic) distributor data sheet')

    # --- SK manufacturer SDS documents ---
    elif p10 == '8eadd31670':  # Yubase%203%20MSDS.pdf — YUBASE 3 SDS
        doc(D, sha, 'SDS', SUP, ['SK:YUBASE_3'],
            'page-1 text (product identifier, SDS revision date)',
            manufacturer=MFG, issuer=SUP,
            note="'SDS No.: YUB300(ENG) Version number: 2 Revision: 19 September 2014'")
    elif p10 == '683522d84d':  # YUBASE_SDS_GLOBAL_UN_4.pdf — YUBASE 4 SDS
        doc(D, sha, 'SDS', SUP, ['SK:YUBASE_4'],
            'page-1 text (product identifier, GHS UN revision date)',
            manufacturer=MFG, issuer=SUP,
            note="'Issue date: 2020-01-01 Revision date: 2026-06-30 Supersedes: 2025-11-01 Version: 4.0'; GHS UN Rev.10 2023 format")
    elif p10 == '8d54d874b4':  # YUBASE_SDS_GLOBAL_UN_4_PLUS.pdf — YUBASE 4 Plus SDS
        doc(D, sha, 'SDS', SUP, ['SK:YUBASE_4P'],
            'page-1 text (product identifier, GHS UN revision date)',
            manufacturer=MFG, issuer=SUP,
            note="'Trade name: YUBASE 4 Plus (YUBASE 4P)'; 'Issue date: 2020-01-01 Revision date: 2026-06-30'; "
                 "GHS UN Rev.10 2023 format; confirms YUBASE 4 Plus is a distinct product from YUBASE 4")
    elif p10 == '287a7490e2':  # YUBASE_SDS_GLOBAL_UN_6.pdf — YUBASE 6 SDS
        doc(D, sha, 'SDS', SUP, ['SK:YUBASE_6'],
            'page-1 text (product identifier, GHS UN revision date)',
            manufacturer=MFG, issuer=SUP,
            note="'Issue date: 2020-01-01 Revision date: 2026-06-30 Supersedes: 2025-11-01 Version: 4.0'; GHS UN Rev.10 2023 format")

    # --- Shell cargo handling sheet for Yubase 4 ---
    elif p10 == '769987aa79':  # chs-yubase-4-rev-3.pdf
        doc(D, sha, 'cargo handling sheet', 'Shell', ['SK:YUBASE_4'],
            'page-1 text (title, subject, date, issuer)',
            manufacturer=MFG, distributor='', issuer='Shell',
            note="'Cargo Handling Sheets are for the use of vessels chartered on behalf of Shell'; "
                 "Document Date: 12 May 2023, Revision 3; Shell issues CHS for marine cargo logistics; "
                 "product subject is Yubase 4 (SK Lubricants)")

    # --- Hilditch Pty Ltd distributor SDS for Yubase 6 ---
    elif p10 == '55e993c575':  # Yubase_6-SDS.pdf
        doc(D, sha, 'SDS', 'Hilditch Pty Ltd', ['SK:YUBASE_6'],
            'page-1 text (product name, reference, issuer)',
            manufacturer=MFG, distributor='Hilditch Pty Ltd', issuer='Hilditch Pty Ltd',
            note="'Reference No: HIL0045 Issued: 2021-09-28 Version: 5.0'; "
                 "Supplier: Hilditch Pty Ltd (Australian distributor); manufacturer SK Lubricants not explicitly named on page 1")

    # --- Non-product documents ---
    elif p10 == '5988c3eaad':  # DL2-11732 — formulation qualification summary
        doc(D, sha, 'formulation qualification summary', '', [],
            'page-1 text (grade table, engine test results)',
            relation='non_product',
            note="page-1 table: Yubase (Group III) used as base oil in 5W-40 and 5W-30 formulations with API SN qualification; "
                 "engine tests listed (Sequence IIIG/IVA/VG/VIII); Yubase grade not stated on page 1; issuer not stated on page 1",
            next_action='read full text to identify issuer and specific Yubase grades')
    elif p10 == 'fee095b35a':  # DL2-11733 — Ford WSS-M2C913-D supplement
        doc(D, sha, 'OEM specification supplement', 'Ford Motor Company', [],
            'page-1 text (specification number, table of approved blend stocks)',
            relation='non_product',
            note="Ford WSS-M2C913-D Supplement A: table of approved base oil products, blend plants and cloud points; "
                 "lists Yubase 4 (Group III, kV100 ~4.2 cSt) and Yubase 6 (Group III, kV100 ~6.4 cSt) as approved blend stocks; "
                 "OEM specification — not a product document for SK/YUBASE",
            issuer='Ford Motor Company')
    elif p10 == '1ffc84cf8e':  # DL2-12438 — Infineum P6003 test report
        doc(D, sha, 'technical report (engine test programme)', 'Infineum UK Limited', [],
            'page-1 text (title: test programme in Yubase Group III base stocks)',
            relation='non_product',
            note="'Infineum P6003 Core Engine Test Programme In Yubase Group III Base Stocks with Infineum SV:261 / SV201 VMs'; "
                 "IBL No: 1109 February 2005; subject is Infineum P6003 / SV:261 / SV201; Yubase is the test base stock, not the subject",
            issuer='Infineum UK Limited')
    elif p10 == '1493fb9c84':  # DL2-13231 — Afton HiTEC 11180 final formulations
        doc(D, sha, 'application technical note (final formulation)', 'Afton Chemical Corporation', [],
            'page-1 text (formulation table: Yubase 4, 6 and 4 Plus as blend stocks)',
            relation='non_product',
            note="'Final Formulations 05/05/2019 AC dexos1 / ILSAC GF-5 / API SN PLUS / API SN'; "
                 "Yubase 4, Yubase 6 and Yubase 4 Plus listed as blend stocks by kV100 and % wt.; "
                 "subject is Afton HiTEC 11180 DI package; confirms YUBASE 4 Plus is a distinct product from YUBASE 4",
            issuer='Afton Chemical Corporation')

    # --- Mislabeled documents ---
    elif p10 == 'b9233a17f3':  # DL2-15502 — Ocean Chemical HC6247 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', 'Ocean Chemical Technology Co., Ltd.',
            ['OCEANCHEMICAL:HC6247'],
            'page-1 text (product name, description, properties)',
            manufacturer='Ocean Chemical Technology Co., Ltd.',
            issuer='Ocean Chemical Technology Co., Ltd.',
            note="mislabeled under SK (YUBASE) in automated classification; "
                 "actual manufacturer: Ocean Chemical Technology Co., Ltd., No.844 Guomao, North Chouzhou Road, Yiwu, Zhejiang, China; "
                 "'HC6247 is a star type hydro-diene polymer with excellent shear stability (SSI<5)'; 4pp TDS")
    elif p10 == '55be2fa8cb':  # DL2-15503 — Ocean Chemical HC6247 1pp sheet
        doc(D, sha, 'product data sheet (TDS/PDS, 1pp)', 'Ocean Chemical Technology Co., Ltd.',
            ['OCEANCHEMICAL:HC6247'],
            'page-1 text (product name, description; auto-classified SDS but page-1 text is product description)',
            manufacturer='Ocean Chemical Technology Co., Ltd.',
            issuer='Ocean Chemical Technology Co., Ltd.',
            note="mislabeled under SK (YUBASE) in automated classification; "
                 "auto-classifier called this SDS but page-1 text matches product description format, not SDS sections; "
                 "1pp; subject same as DL2-15502 (HC6247); may be a 1-page product sheet or combined spec")
    elif p10 == 'f4170e3899':  # DL2-15627 — Dowpol NeoFlex 680 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', 'Dowpol Chemical International Corp.',
            ['DOWPOL:NEOFLEX_680'],
            'page-1 text (product name, description)',
            manufacturer='Dowpol Chemical International Corp.',
            issuer='Dowpol Chemical International Corp.',
            note="mislabeled under SK (YUBASE) in automated classification; "
                 "actual manufacturer: Dowpol Chemical International Corp. (http://www.dowpol.com); "
                 "'NeoFlex 680 Pour Point Depressant is based on the Neo Synthetic Hydrocarbon chemistry'; "
                 "Revision Date April 2018; 2pp TDS; "
                 "S19 Dowpol batch does not include this document (it was labeled SK in the automated classifier)")

write(OWN,
      'S28 SK (YUBASE) (identity)',
      '17 documents with provisional supplier SK (YUBASE)',
      PK, D)
