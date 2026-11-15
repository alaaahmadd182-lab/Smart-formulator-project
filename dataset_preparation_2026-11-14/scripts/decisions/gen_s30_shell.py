"""S30: Shell — 17 unreviewed documents (18 total, 1 already decided in S28).
Read: page-1 text (text layer) for every document 2026-11-15; additional pages for
DL2-12275 and DL2-14931.

Shell products: Risella X 415, 420, 430 (GTL-derived technical white oils / base oils, all existing
records; CAS 848301-69-9; Shell Pearl GTL Qatar; brand 'GtL Technical White Oil').

Mislabeled documents (8 of 17):
  DL2-11664, 11665, 11666: Toho Chemical Industry Co., Ltd. LUBRAN 141/165/171 PMA pour point
    depressants — not Shell products; mislabeled under Shell in automated classification.
  DL2-11726, DL2-12269: 7pp GHS SDS documents dated 2016-04-15, same format as the LUBRAN TDS above;
    product name not extractable from text layer (pages 1-5 show only GHS boilerplate); probable Toho
    Chemical LUBRAN SDS for two of the three grades; unresolved identity.
  DL2-12275: Product data sheet for 'HSB 500N (DAESAN)_EN'; address 7F Yonsei Bldg, Seoul; page text
    ends '...HYUNDAI and SHELL Base Oi' (truncated) confirming HSB = Hyundai Shell Base oil; product
    of Hyundai Oilbank / Shell base oil JV; manufactured at Daesan industrial complex (Korea); Group III
    10 cSt (kV100 10-12 cSt, VI 95-119).
  DL2-14931: 1pp buyer-issued CoA, buyer material code MFH5306; spec limits identical to HSB 500N
    (kV100 10-12, VI 95-119); tested by Intertek Kimsco, Gunpo, Korea; assigned tentatively to HSB 500N.
  DL2-15441: 'ILCO PHOS 366 as Fire Resistant Hydraulic Fluid'; ISO HFDR class phosphate ester
    hydraulic fluid; mislabeled under Shell; manufacturer name not printed on page 1.

Non-product (1): DL2-14668 — Shell Turbo range marketing brochure.
Trade document (1): DL2-13736 — Certificate of Origin for Risella X 420 cargo from Qatar.

Writes decisions/s30_shell.json."""
from dec_common import rows, page_text, top, doc, prod, write

SUP = 'Shell'
MFG_SHELL = 'Shell (Pearl GTL, Qatar)'
B = 'base_oil'
C = 'additive_component'
OWN = 's30_shell.json'

RISELLA = {
    'SHELL:RISELLA_X_415': ('SHELL_RISELLA_X_415', 'Shell Risella X 415'),
    'SHELL:RISELLA_X_420': ('SHELL_RISELLA_X_420', 'Shell Risella X 420'),
    'SHELL:RISELLA_X_430': ('SHELL_RISELLA_X_430', 'Shell Risella X 430'),
}
LUBRAN = {
    '5f3703fa2f': ('TOHOLCHEM:LUBRAN_141', 'LUBRAN 141'),
    'abdb494fb8': ('TOHOLCHEM:LUBRAN_165', 'LUBRAN 165'),
    'e51460de2c': ('TOHOLCHEM:LUBRAN_171', 'LUBRAN 171'),
}
LUBRAN_SUP = 'Toho Chemical Industry Co., Ltd.'

D, PK = {}, {}

for key, (rec, name) in RISELLA.items():
    prod(PK, key, name, SUP, B, 'printed product name on the documents linked in this batch', existing=rec)

for p10, (key, name) in LUBRAN.items():
    prod(PK, key, name, LUBRAN_SUP, C,
         "printed: '" + name + " is a Polymethacrylate (PMA) type of pour point depressant for lubricating oil'; "
         "(Data for Group II); PPD subtype; mislabeled under Shell in automated classification",
         evidence='printed product name and description on 1pp TDS in this batch')

prod(PK, 'HYUNDAIOILBANK:HSB_500N', 'HSB 500N (DAESAN)',
     'Hyundai Oilbank Co., Ltd. / Shell (joint venture base oil)',
     B,
     "printed: 'HSB 500N (DAESAN)_EN'; address: 7F Yonsei Bldg, 10 Tongil-ro, Jung-gu, Seoul (Hyundai Oilbank HQ); "
     "page text truncated as '...HYUNDAI and SHELL Base Oi' confirming HSB = Hyundai Shell Base oil JV; "
     "Group III, kV100 10.0-12.0 cSt, VI 95-119, kV40 (Report), PP ≤-15, FP ≥230, S ≤0.001wt%, Sat ≥99wt%, Ar ≤1wt%; "
     "manufactured at Daesan industrial complex, South Korea; brand: HSB",
     evidence='printed product name on DL2-12275 TDS; spec match on DL2-14931 CoA')

prod(PK, 'ILCO:ILCO_PHOS_366', 'ILCO PHOS 366', 'ILCO (manufacturer not printed on page 1)',
     'out_of_template (fire-resistant hydraulic fluid)',
     "printed: 'ILCO PHOS 366 as Fire Resistant Hydraulic Fluid'; ISO HFDR class phosphate ester; "
     "not a lubricant base oil or lubricant additive — out of template; "
     "mislabeled under Shell in automated classification")

for r in rows(lambda s: s == 'Shell', OWN):
    sha = r['sha256']
    p10 = sha[:10]

    # --- Shell Risella X TDS (1pp each, dupOLD) ---
    if p10 == '61f3443933':  # DL2-13728 Risella X 415 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['SHELL:RISELLA_X_415'],
            'page-1 text (product name, GtL classification, typical properties)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="dupOLD; 'Technical Data Sheet Shell Risella X 415 GtL Technical White Oil'; 1pp typical properties table")
    elif p10 == '334d56401d':  # DL2-13726 Risella X 420 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['SHELL:RISELLA_X_420'],
            'page-1 text (product name, GtL classification, typical properties)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="dupOLD; 'Technical Data Sheet Shell Risella X 420 GtL Technical White Oil'; 1pp typical properties table")
    elif p10 == 'e4790b838f':  # DL2-13727 Risella X 430 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['SHELL:RISELLA_X_430'],
            'page-1 text (product name, GtL classification, typical properties)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="dupOLD; 'Technical Data Sheet Shell Risella X 430 GtL Technical White Oil'; 1pp typical properties table")

    # --- Shell Risella X SDS (15pp each, dupOLD) ---
    elif p10 == 'efae4694d1':  # DL2-13729 Risella X 415 SDS
        doc(D, sha, 'SDS', SUP, ['SHELL:RISELLA_X_415'],
            'page-1 text (product name, CAS No., SDS revision date)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="dupOLD; 'Version 1.2 Revision Date 26.10.2018'; CAS-No. 848301-69-9; Product code 001E2773; 15pp")
    elif p10 == 'ab23007491':  # DL2-13730 Risella X 420 SDS
        doc(D, sha, 'SDS', SUP, ['SHELL:RISELLA_X_420'],
            'page-1 text (product name, CAS No., SDS revision date)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="dupOLD; 'Version 1.2 Revision Date 26.10.2018'; CAS-No. 848301-69-9; Product code 001E2774; 15pp")

    # --- Risella X batch CoAs ---
    elif p10 == '014d2db56e':  # DL2-13732 Risella X 415 batch CoA (Hong Kong, 1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['SHELL:RISELLA_X_415'],
            'page-1 text (material number, description, batch number, test results)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="'Material 500006734 Risella X 415_BULK_A03Q Batch 11720728 Date 27-Feb-21'; location: H122 Sai Tso Wan Road, Tsing Yi Island, Hong Kong")
    elif p10 == '526856fa41':  # DL2-13733 Risella X 420 batch CoA (Hong Kong, 1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['SHELL:RISELLA_X_420'],
            'page-1 text (material number, description, batch number, test results)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="'Material 500006740 Risella X 420_BULK Batch 11729367 Date 10-Mar-21'; location: H122 Sai Tso Wan Road, Tsing Yi Island, Hong Kong")

    # --- Risella X 420 Certificate of Origin ---
    elif p10 == 'f1c9d82949':  # DL2-13736 Risella X 420 CoO (trade doc, 1pp)
        doc(D, sha, 'certificate of origin (trade document)', SUP, ['SHELL:RISELLA_X_420'],
            'page-1 text (product name, quantity, origin)',
            manufacturer=MFG_SHELL, issuer=SUP,
            note="'Risella X 420_BULK_A03Q 17510 KGS + 17490 KGS Manufactured in QATAR Date 7-Nov-20 P.O. NO. 4533328415'; "
                 "trade document, no product properties; confirms Qatar (Pearl GTL) as origin")

    # --- Mislabeled: HSB 500N (Hyundai Oilbank / Shell JV) ---
    elif p10 == '22dd31aaf8':  # DL2-12275 HSB 500N TDS (1pp)
        doc(D, sha, 'product data sheet (TDS/PDS)', 'Hyundai Oilbank Co., Ltd.', ['HYUNDAIOILBANK:HSB_500N'],
            'page-1 text (product name, specification table; full text truncated confirming HYUNDAI and SHELL Base Oil JV)',
            manufacturer='Hyundai Oilbank Co., Ltd.', issuer='Hyundai Oilbank Co., Ltd.',
            note="mislabeled under Shell in automated classification; actual issuer: Hyundai Oilbank Co., Ltd. (Seoul HQ); "
                 "page text ends '...HYUNDAI and SHELL Base Oi' confirming HSB brand is Hyundai Shell Base oil JV; "
                 "product: HSB 500N, Group III, kV100 10-12 cSt, VI 95-119, manufactured at Daesan industrial complex, Korea")
    elif p10 == 'eead3091dc':  # DL2-14931 MFH5306 CoA (1pp, issuer unclear)
        doc(D, sha, 'certificate of analysis (batch)', '', ['HYUNDAIOILBANK:HSB_500N'],
            'page-1 text (buyer code, spec limits, test results, testing lab)',
            manufacturer='Hyundai Oilbank Co., Ltd.',
            note="buyer material code MFH5306; spec limits (kV100 10-12 cSt, VI 95-119, PP ≤-15 °C, FP ≥230 °C, S ≤0.001wt%, Sat ≥99wt%, Ar ≤1wt%) match HSB 500N exactly; "
                 "tested by Intertek Kimsco Co., Ltd., Gunpo-si, Korea; SHIPMENT DATE JUN. 15, 2021; "
                 "issuer not identified on page 1; assigned to HSB 500N tentatively based on spec match; "
                 "labeled under Shell in automated classifier",
            next_action='read other pages to confirm issuer and product name')

    # --- Mislabeled: Toho Chemical LUBRAN TDS ---
    elif p10 in LUBRAN:
        key, name = LUBRAN[p10]
        t = page_text(sha)
        doc(D, sha, 'product data sheet (TDS/PDS)', LUBRAN_SUP, [key],
            'page-1 text (product name, type description, properties for Group II base oil)',
            manufacturer=LUBRAN_SUP, issuer=LUBRAN_SUP,
            note="mislabeled under Shell in automated classification; actual manufacturer: "
                 "Toho Chemical Industry Co., Ltd., 6-4 Akashi-cho, Chuo-ku, Tokyo 104-0044 Japan; "
                 "PMA pour point depressant; 1pp TDS; (Data for Group II) in heading")

    # --- Toho SDS (unresolved which LUBRAN grade) ---
    elif p10 == '5dd6c4e82c':  # DL2-11726 Toho SDS 7pp
        doc(D, sha, 'SDS', LUBRAN_SUP, [],
            'pages 1-5: GHS boilerplate only; product name not in extractable text layer',
            relation='unresolved_identity',
            manufacturer=LUBRAN_SUP, issuer=LUBRAN_SUP,
            note="mislabeled under Shell; Toho Chemical Industry format, same date (2016-04-15) as DL2-11726 (08a4939222); "
                 "7pp GHS SDS; product name not extractable from text layer (all pages show GHS classification boilerplate); "
                 "probable SDS for one of LUBRAN 141/165/171 (PMA PPD); cannot be assigned without OCR or manual read",
            next_action='read OCR or full text to identify LUBRAN grade (141, 165 or 171)')
    elif p10 == '08a4939222':  # DL2-12269 Toho SDS 7pp
        doc(D, sha, 'SDS', LUBRAN_SUP, [],
            'pages 1-5: GHS boilerplate only; product name not in extractable text layer',
            relation='unresolved_identity',
            manufacturer=LUBRAN_SUP, issuer=LUBRAN_SUP,
            note="mislabeled under Shell; Toho Chemical Industry format, same date (2016-04-15) as DL2-11726 (5dd6c4e82c); "
                 "7pp GHS SDS; product name not extractable from text layer; "
                 "probable SDS for one of LUBRAN 141/165/171; cannot be assigned without OCR or manual read",
            next_action='read OCR or full text to identify LUBRAN grade (141, 165 or 171)')

    # --- Mislabeled: ILCO PHOS 366 ---
    elif p10 == 'a0d599a7b8':  # DL2-15441 ILCO PHOS 366 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', 'ILCO (manufacturer not printed on page 1)',
            ['ILCO:ILCO_PHOS_366'],
            'page-1 text (product name, type description: fire-resistant hydraulic fluid)',
            manufacturer='ILCO (manufacturer not printed on page 1)', issuer='',
            note="mislabeled under Shell; actual product: ILCO PHOS 366 phosphate ester fire-resistant hydraulic fluid (ISO HFDR); "
                 "out of template for lubricant base oil / additive database; manufacturer name not on page 1",
            next_action='read full text to identify manufacturer')

    # --- Non-product: Shell Turbo brochure ---
    elif p10 == '09b86a8a5b':  # DL2-14668 Shell Turbo marketing brochure (6pp)
        doc(D, sha, 'marketing brochure', SUP, [],
            'page-1 text (brand name and claim)',
            relation='non_product',
            issuer=SUP,
            note="'SHELL TURBO MAKES IT POSSIBLE... The Shell Turbo range of oils helps to protect your equipment'; "
                 "6pp marketing brochure for the Shell Turbo turbine oil range; no product properties; not a TDS or SDS")

write(OWN,
      'S30 Shell (identity)',
      '17 documents with provisional supplier Shell (1 doc already decided in S28)',
      PK, D)
