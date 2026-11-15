"""S29: Nynas — 17 documents.
Read: page-1 text (text layer) for every document 2026-11-15.

Nynas AB (Stockholm, Sweden) produces naphthenic base oils under multiple brands:
  Nyfrost (refrigeration fluids), Nynas T grades / NS grades / S grades (process / specialty oils),
  NYBASE (high-quality lube base stocks), Nytro (electrical insulating / transformer oils).

Existing records: NYFROST 32, 68, 100; NS 3; S 3B; T 3, 4, 9, 600; NYBASE 70.
New candidates:
  Nytro Libra — 'uninhibited transformer oil conforming to IEC 60296 Edition 4.0'; naphthenic base
    stock marketed as electrical insulating oil, not a lubricating base oil — material class and
    template to be confirmed.
  Nytro Lyra X — 'inhibited high-grade insulating oil conforming to IEC 60296 Edition 4.0';
    same classification question.

Two batch certificates of analysis (DL2-14773, DL2-14775) for NYFROST 32: batch-specific production
records, included as product documents.
Four documents cover the same NYNAS format families (T grades, NS grades, S grades): each file covers
a single grade on page 1; assigned to the grade named on page 1 only.
Two TDS documents for NS 3 (DL2-12382, DL2-15474): different revision or format editions; both dupOLD.

Writes decisions/s29_nynas.json."""
from dec_common import rows, page_text, top, doc, prod, write

SUP = 'Nynas AB'
MFG = SUP
B = 'base_oil'
U = 'unresolved'
OWN = 's29_nynas.json'

# Existing products
EXISTING = {
    'NYNAS_NYFROST_32': ('NYNAS:NYFROST_32', 'NYFROST 32'),
    'NYNAS_NYFROST_68': ('NYNAS:NYFROST_68', 'Nyfrost 68'),
    'NYNAS_NYFROST_100': ('NYNAS:NYFROST_100', 'NYFROST 100'),
    'NYNAS_NS_3':        ('NYNAS:NS_3',        'NS 3'),
    'NYNAS_S_3B':        ('NYNAS:S_3B',        'Nynas S 3B'),
    'NYNAS_T_3':         ('NYNAS:T_3',         'Nynas T 3'),
    'NYNAS_T_4':         ('NYNAS:T_4',         'Nynas T 4'),
    'NYNAS_T_9':         ('NYNAS:T_9',         'Nynas T 9'),
    'NYNAS_T_600':       ('NYNAS:T_600',       'Nynas T 600'),
    'NYNAS_NYBASE_70':   ('NYNAS:NYBASE_70',   'NYBASE 70'),
}

D, PK = {}, {}

for rec, (key, name) in EXISTING.items():
    prod(PK, key, name, SUP, B, 'printed product name on the documents linked in this batch', existing=rec)

prod(PK, 'NYNAS:NYTRO_LIBRA', 'Nytro Libra', SUP, U,
     "printed: 'Nytro Libra is an uninhibited transformer oil that conforms to IEC 60296 Edition 4.0'; "
     "'STANDARD GRADE Electrical insulating oil'; naphthenic base stock sold as transformer oil; "
     "not a lubricating base oil — material class and template to be confirmed")
prod(PK, 'NYNAS:NYTRO_LYRA_X', 'Nytro Lyra X', SUP, U,
     "printed: 'Nytro Lyra X is an inhibited high-grade insulating oil conforming to IEC 60296 Edition 4.0 "
     "— including the fulfilment of specific requirements for special applications'; 'HIGH GRADE "
     "High performance insulating oil'; naphthenic base stock sold as transformer oil; "
     "not a lubricating base oil — material class and template to be confirmed")

for r in rows(lambda s: s == 'Nynas', OWN):
    sha = r['sha256']
    p10 = sha[:10]

    # --- NYFROST 32: TDS, SDS, two CoAs ---
    if p10 == 'a5d090bc37':  # DL2-11510 NYFROST 32 TDS (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYFROST_32'],
            'page-1 text (product name, description, applications)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'wax-free, hydrotreated naphthenic ISO VG 32 base oil intended for use as a refrigeration fluid'")
    elif p10 == 'd489c09f49':  # DL2-13444 NYFROST 32 SDS (12pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NYNAS:NYFROST_32'],
            'page-1 text (product name, REACH/SDS format, CAS No.)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; REACH Annex II format; 'CAS number 64742-52-5'; 12pp")
    elif p10 == '65af812d82':  # DL2-14773 Nyfrost 32 CoA (1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NYNAS:NYFROST_32'],
            'page-1 text (product name, batch number, analysis results)',
            manufacturer=MFG, issuer=SUP,
            note="batch TRAF4-201208 / N2020-17163; dated Dec 2020; 1pp; "
                 "properties: density 15°C, kV40, flash point PM, colour, TAN, refractive index")
    elif p10 == '2fc903132a':  # DL2-14775 Nyfrost 32 CoA (1pp)
        doc(D, sha, 'certificate of analysis (batch)', SUP, ['NYNAS:NYFROST_32'],
            'page-1 text (product name, batch number, analysis results)',
            manufacturer=MFG, issuer=SUP,
            note="batch TRAFl-210219 / N2021-02889; dated Feb 2021; 1pp; "
                 "properties: density 15°C, kV40, flash point PM, colour, TAN")

    # --- NYFROST 68 and 100 TDS ---
    elif p10 == '85a23a2ab7':  # DL2-11747 Nyfrost 68 TDS (1pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYFROST_68'],
            'page-1 text (product name, specification limits table with typical data)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'PRODUCT DATA SHEET Nyfrost 68 CHARACTERISTICS'; specification limits and typical data columns; 1pp")
    elif p10 == '4dd1792d2a':  # DL2-12383 NYFROST 100 TDS (2pp, dupOLD, x2 copies in archive)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYFROST_100'],
            'page-1 text (product name, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; x2 copies in archive (filename DL2-12383 (1).pdf); "
                 "'high viscosity, wax-free, hydrotreated naphthenic ISO VG 100 base oil for heavy duty refrigeration fluid applications'")

    # --- Nynas T grades (four products, each from their own TDS) ---
    elif p10 == 'c51d26a6dd':  # DL2-12381 T 4 (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:T_4'],
            'page-1 text (product name within T grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'T grades' format banner; page 1 names T 4: 'very low viscosity hydrotreated naphthenic oil with excellent solvent power'; assigned to T 4 from page-1 content only")
    elif p10 == '0e59ae6950':  # DL2-15475 T 3 (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:T_3'],
            'page-1 text (product name within T grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'T grades' format; 'NYNAS® T 3 A naphthenic base oil'; outstanding emulsion stability in water-based metalworking fluids")
    elif p10 == 'b4c3d3c505':  # DL2-13356 T 9 (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:T_9'],
            'page-1 text (product name within T grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'T grades' format; 'NYNAS® T 9 A naphthenic base oil'; low viscosity hydrotreated naphthenic oil with excellent solvent power")
    elif p10 == 'e981acd7c9':  # DL2-13009 T 600 (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:T_600'],
            'page-1 text (product name within T grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'T grades' format; 'NYNAS T 600 high viscosity hydrotreated naphthenic oil with high solvent power and very good low temperature properties'; suitable for grease production")

    # --- Nynas NS grades: NS 3 (two TDS editions) ---
    elif p10 == '6d6dd73da8':  # DL2-12382 NS 3 TDS (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NS_3'],
            'page-1 text (product name within NS grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'NS grades' banner; 'NS 3 highly refined, very low viscosity hydrotreated naphthenic oil with excellent low temperature properties'; used in aviation hydraulic fluids")
    elif p10 == '2d21cf27bc':  # DL2-15474 NS 3 TDS (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NS_3'],
            'page-1 text (product name within NS grades banner, newer format with trademark listing)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; newer Nynas format with trademark list; 'NYNAS® NS 3 A naphthenic base oil'; same product as DL2-12382, different edition")

    # --- Nynas S 3B (SDS and TDS) ---
    elif p10 == 'cfb7485790':  # DL2-12819 S 3B TDS (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:S_3B'],
            'page-1 text (product name within S grades banner, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; 'S grades' banner; 'NYNAS® S 3B low viscosity hydrotreated naphthenic oil with a very high refining degree; narrow boiling range and very low aromatic content'")
    elif p10 == 'ad281d3d91':  # DL2-13379 S 3B SDS (36pp, dupOLD)
        doc(D, sha, 'SDS', SUP, ['NYNAS:S_3B'],
            'page-1 text (product name, REACH/SDS format, CAS No.)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; REACH Annex II format; 'CAS number 64742-46-7'; 36pp")

    # --- NYBASE 70 ---
    elif p10 == 'b852035a74':  # DL2-13344 NYBASE 70 TDS (2pp, dupOLD)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYBASE_70'],
            'page-1 text (product name, trademark list, description)',
            manufacturer=MFG, issuer=SUP,
            note="dupOLD; newer Nynas format with trademark list; 'NYBASE® 70 Base oil'; suitable for blending high quality lubricants")

    # --- New products: Nytro transformer oils ---
    elif p10 == '905e9e74bb':  # DL2-12260 Nytro Libra TDS (2pp)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYTRO_LIBRA'],
            'page-1 text (product name, grade category, description)',
            manufacturer=MFG, issuer=SUP,
            note="'STANDARD GRADE Nytro Libra Electrical insulating oil'; 'conforms to IEC 60296 Edition 4.0'; "
                 "uninhibited transformer oil; not dupOLD; not in existing records")
    elif p10 == 'bd8c3a68db':  # DL2-12627 Nytro Lyra X TDS (2pp)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['NYNAS:NYTRO_LYRA_X'],
            'page-1 text (product name, grade category, description)',
            manufacturer=MFG, issuer=SUP,
            note="'HIGH GRADE Nytro Lyra X High performance insulating oil'; 'conforms to IEC 60296 Edition 4.0 "
                 "including specific requirements for special applications'; inhibited transformer oil; not dupOLD; not in existing records")

write(OWN,
      'S29 Nynas (identity)',
      '17 documents with provisional supplier Nynas',
      PK, D)
