"""S32: Neste — 14 documents.
Read: page-1 text (text layer) for every document 2026-11-15; additional pages for DL2-12418, 12419.

Neste Corporation (Finland) produces NEXBASE™ Group III/III+ VHVI and PAO base oils.

Existing records: NEXBASE 3020, 3043, 3060, 3080.

New candidates:
  NEXBASE TM 2000 (DL2-14881): Fortum-era 8pp brochure titled 'NEXBASE TM 2000 Polyalphaolefins';
    'Fortum Base Oils is a part of the Finnish energy group Fortum' (Fortum was the predecessor of
    Neste's base oil business; renamed/acquired). Specific viscosity grade not stated on page 1; PAO
    base oil product — material class base_oil confirmed; grade TBD from full read.

Buyer CoAs (DL2-14402, DL2-14398): issued with buyer codes NT502 (= NEXBASE 3080) and NT503
  (= NEXBASE 3043) printed in the title; assigned to their respective existing records.

Two unidentified TDS (DL2-12418, DL2-12419): 2pp; page 1 is Neste contact/distributor info common
  to all Neste TDS; product name not extractable from text layer (table on page 2 likely image-based
  or the product title is in a graphic header); assigned as unresolved_identity pending OCR/manual read.

Writes decisions/s32_neste.json."""
from dec_common import rows, page_text, top, doc, prod, write

SUP = 'Neste Corporation'
MFG = SUP
B = 'base_oil'
OWN = 's32_neste.json'

EXISTING = {
    'NESTE:NEXBASE_3020': ('NESTE_NEXBASE_3020', 'NEXBASE 3020'),
    'NESTE:NEXBASE_3043': ('NESTE_NEXBASE_3043', 'NEXBASE 3043'),
    'NESTE:NEXBASE_3060': ('NESTE_NEXBASE_3060', 'NEXBASE 3060'),
    'NESTE:NEXBASE_3080': ('NESTE_NEXBASE_3080', 'NEXBASE 3080'),
}

D, PK = {}, {}

for key, (rec, name) in EXISTING.items():
    prod(PK, key, name, SUP, B, 'printed product name on the documents linked in this batch', existing=rec)

prod(PK, 'NESTE:NEXBASE_TM_2000', 'NEXBASE TM 2000', SUP, B,
     "printed: 'NEXBASE TM 2000 Polyalphaolefins'; Fortum-era brochure confirming PAO product from Fortum / Neste; "
     "'Fortum became the first European-owned producer of polyalphaolefins in 1991; PAO facility in Beringen, Belgium'; "
     "specific viscosity grade not stated on page 1; likely a 2 cSt or family range brochure; "
     "not in existing records",
     evidence='printed product name on DL2-14881 Fortum brochure')

for r in rows(lambda s: s == 'Neste', OWN):
    sha = r['sha256']
    p10 = sha[:10]

    # --- NEXBASE 3020 SDS (two editions) ---
    if p10 == 'bb9d7a7f42':  # DL2-14513 NEXBASE 3020 SDS (106pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NESTE:NEXBASE_3020'],
            'page-1 text (product identifier, REACH format, revision date)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'Revision date: 16/06/2020 Supersedes date: 25/03/2020'; 106pp (probable multi-language SDS compilation)")
    elif p10 == '8e4f510998':  # DL2-14514 NEXBASE 3020 SDS (9pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NESTE:NEXBASE_3020'],
            'page-1 text (product identifier, REACH format, revision date)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'Revision date: 16/06/2020 Supersedes date: 25/03/2020'; 9pp (single-language SDS)")

    # --- NEXBASE 3043 SDS and CoA ---
    elif p10 == 'b66289efbd':  # DL2-15010 NEXBASE 3043 SDS (153pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NESTE:NEXBASE_3043'],
            'page-1 text (product identifier, REACH format, revision date)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'Revision date: 28/10/2021 Supersedes date: 17/08/2021'; 153pp (multi-language SDS compilation)")
    elif p10 == 'ff57021470':  # DL2-14397 NEXBASE 3043 CoA (1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NESTE:NEXBASE_3043'],
            'page-1 text (product name, CoA header)',
            manufacturer=MFG, issuer=SUP,
            note="'Product Name: NEXBASE 3043 CERTIFICATE OF ANALYSIS'; 1pp")

    # --- NEXBASE 3060 SDS and CoAs ---
    elif p10 == '6e4ee41f8f':  # DL2-12735 NEXBASE 3060 SDS (9pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NESTE:NEXBASE_3060'],
            'page-1 text (product identifier, REACH format, revision date)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'Revision date: 17/10/2017 Supersedes date: 30/05/2016'; 9pp")
    elif p10 == '9f3a762a95':  # DL2-12853 NEXBASE 3060 CoA (1pp, x2 copies)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NESTE:NEXBASE_3060'],
            'page-1 text (Neste quality plan note, Neste Belgium contact)',
            manufacturer=MFG, issuer=SUP,
            note="x2 copies in archive; 'LAST MEASUREMENT ACCORDING TO NESTE'S QUALITY PLAN'; "
                 "Handled by: Jacquemyn Kirsten, Neste (Belgium); 1pp")
    elif p10 == 'e85a2cdbb7':  # DL2-14400 NEXBASE 3060 detailed CoA (2pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NESTE:NEXBASE_3060'],
            'page-1 text (product name, batch number, test results table)',
            manufacturer=MFG, issuer=SUP,
            note="'Product: NEXBASE 3060(Base Oil GIII, 6 cSt) Batch No: B201137 Date: 22 Feb 2020'; 2pp; "
                 "kV40 32.32 cSt, kV100 5.986 cSt (spec 5.7-6.3), VI (measured)")

    # --- NEXBASE 3080 SDS and CoA ---
    elif p10 == 'ab4aa0463c':  # DL2-14512 NEXBASE 3080 SDS (9pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NESTE:NEXBASE_3080'],
            'page-1 text (product identifier, REACH format, revision date)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'Revision date: 03/07/2020 Supersedes date: 17/10/2017'; 9pp")
    elif p10 == '89e29752a6':  # DL2-14401 NEXBASE 3080 CoA (1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NESTE:NEXBASE_3080'],
            'page-1 text (product name, CoA header)',
            manufacturer=MFG, issuer=SUP,
            note="'Product Name: NEXBASE 3080 CERTIFICATE OF ANALYSIS'; 1pp")

    # --- Buyer CoAs (NT502 = NEXBASE 3080, NT503 = NEXBASE 3043) ---
    elif p10 == 'd6a2a018c9':  # DL2-14402 NT502 CoA (2pp)
        doc(D, sha, 'certificate of analysis (buyer-issued)', SUP, ['NESTE:NEXBASE_3080'],
            'page-1 text (buyer code NT502 = NEXBASE 3080, batch, test results)',
            manufacturer=MFG, issuer=SUP,
            note="'Product: NT502 (NEXBASE 3080) Batch No: B201368 Date: 26 Jul 2020 PL NO: 253-10917/1222'; "
                 "buyer code NT502 printed with NEXBASE 3080 in parentheses; 2pp")
    elif p10 == 'f45b0fc5d7':  # DL2-14398 NT503 CoA (2pp)
        doc(D, sha, 'certificate of analysis (buyer-issued)', SUP, ['NESTE:NEXBASE_3043'],
            'page-1 text (buyer code NT503 = NEXBASE 3043, batch, test results)',
            manufacturer=MFG, issuer=SUP,
            note="'Product: NT 503(NEXBASE 3043) Batch No: B201369 Date: 30 Jun 2020 PL No: 253-10918/1287'; "
                 "buyer code NT503 printed with NEXBASE 3043 in parentheses; 2pp")

    # --- NEXBASE TM 2000 PAO brochure (Fortum era) ---
    elif p10 == '930032fd2a':  # DL2-14881
        doc(D, sha, 'product brochure (PAO range)', SUP, ['NESTE:NEXBASE_TM_2000'],
            'page-1 text (product family name, Fortum company overview)',
            manufacturer=MFG, issuer='Fortum Corporation / Neste Corporation (Fortum-era document)',
            note="'NEXBASE TM 2000 Polyalphaolefins'; Fortum-era brochure; "
                 "'Fortum Base Oils is a part of the Finnish energy group Fortum'; 8pp; "
                 "Fortum's base oil business subsequently became part of Neste; "
                 "PAO facility in Beringen, Belgium; product grade not stated on page 1")

    # --- Two unidentified Neste TDS ---
    elif p10 == 'ee74005aea':  # DL2-12418 (2pp, unidentified)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, [],
            'pages 1-2: Neste contact and distributor information; product properties not in extractable text',
            relation='unresolved_identity',
            manufacturer=MFG, issuer=SUP,
            note="2pp; page 1 is Neste contact/distributor info common to all Neste TDS (2017 format); "
                 "product name and properties table not in extractable text layer (likely in graphic header or image table on page 2)",
            next_action='OCR page 2 or manual read to identify product name')
    elif p10 == '36a7c68119':  # DL2-12419 (2pp, unidentified)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, [],
            'pages 1-2: Neste contact and distributor information; product properties not in extractable text',
            relation='unresolved_identity',
            manufacturer=MFG, issuer=SUP,
            note="2pp; page 1 is Neste contact/distributor info common to all Neste TDS (2017 format); "
                 "same format as DL2-12418 (ee74005aea); product name not extractable",
            next_action='OCR page 2 or manual read to identify product name')

write(OWN,
      'S32 Neste (identity)',
      '14 documents with provisional supplier Neste',
      PK, D)
