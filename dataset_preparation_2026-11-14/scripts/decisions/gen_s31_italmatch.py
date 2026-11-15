"""S31: Italmatch — 15 documents.
Read: page-1 text (text layer) for every document 2026-11-15; additional page text for 1pp TDS
where page-1 starts with copyright boilerplate (product name appears later on page 1).

Italmatch Chemicals S.p.A. (Milan, Italy) produces specialty chemicals. The 15 documents in this
batch are all metalworking fluid (MWF) additives under the Polartech® and Dapralube® brands, plus
one Ketjenlube® ester range overview document.

All Polartech products are MWF additives (corrosion inhibitor packages, emulsifiers, lubricity
additives, passivators, antifoams) explicitly described as 'for use in metalworking fluids' or
'water-mix metalworking fluids'. They are out of template for the lubricant base oil / additive
database whose scope is engine oil / lubricant formulation.

Dapralube 77 and 9501 are Italmatch MWF specialty chemicals (SDS available; application in
metalworking coolant systems). Also out of template.

Ketjenlube 09 (1pp ester overview, ×2 copies): 'conventional esters... synthetic and natural esters
under the Ketjenlube trade name'; auto-classified Ketjenlube 09 (medium confidence). Synthetic
esters can be used as Group V base fluids or lubricant additives (polyol esters, TMP esters); the
specific Ketjenlube 09 type and application need confirmation from full text — material class left
unresolved pending full read.

DL2-13610: 24pp confidential Italmatch MWF package range internal catalog — non_product.

Writes decisions/s31_italmatch.json."""
from dec_common import rows, page_text, top, doc, prod, write

SUP = 'Italmatch Chemicals S.p.A.'
MFG = SUP
OT = 'out_of_template (metalworking fluid additive)'
OWN = 's31_italmatch.json'

D, PK = {}, {}

PRODUCTS = {
    # sha10: (key, name, description, doc_type)
    '87a731f90b': ('ITALMATCH:POLARTECH_8142',    'Polartech 8142',
                   "printed: 'Polartech® 8142 Combined Emulsifier and Corrosion Inhibitor Package; "
                   "superior quality package capable of producing a range of high performance, long service life fluids'",
                   'product data sheet (TDS/PDS)', OT),
    'ac2b163103': ('ITALMATCH:POLARTECH_LA_8610', 'Polartech LA 8610',
                   "printed: 'Polartech® LA 8610 Synthetic Lubricity Additive; "
                   "high quality synthetic ester suitable for use in all types of metal cutting, forming and drawing fluids'",
                   'product data sheet (TDS/PDS)', OT),
    'd8277dd624': ('ITALMATCH:POLARTECH_MP_900_CU', 'Polartech MP 900 CU',
                   "printed: 'Polartech® MP 900 CU Water Miscible Multimetal Passivator; "
                   "synthetic corrosion inhibitor particularly soluble for protection of copper and yellow metal alloys'",
                   'product data sheet (TDS/PDS)', OT),
    'fccccbe686': ('ITALMATCH:POLARTECH_8430',    'Polartech 8430',
                   "printed: 'Polartech® 8430 Versatile Synthetic Corrosion Inhibitor Package Boron Technology Synthetic Fluid Package; "
                   "secondary amine free'",
                   'product data sheet (TDS/PDS)', OT),
    '4907a2f2ab': ('ITALMATCH:POLARTECH_EA_150',  'Polartech EA 150',
                   "printed: 'Polartech® EA 150 Co-emulsifier Lauryl Ether Carboxylate; "
                   "amine free co-emulsifier for use at low concentrations to provide improved emulsion and concentrate stability'",
                   'product data sheet (TDS/PDS)', OT),
}

PAIRED = {
    # sha10: (key, doc_type, note)
    '0ffdce1466': ('ITALMATCH:POLARTECH_8310', 'SDS',
                   "26pp; 'Industrial applications: Metalworking Fluid Package'"),
    '9f64298792': ('ITALMATCH:POLARTECH_8430', 'SDS',
                   "9pp; MWF package SDS (paired with TDS fccccbe686)"),
    '849b79f169': ('ITALMATCH:POLARTECH_EA_150', 'SDS',
                   "10pp; co-emulsifier SDS (paired with TDS 4907a2f2ab)"),
    '63f695af9b': ('ITALMATCH:DAPRALUBE_77', 'SDS',
                   "14pp; UK REACH format; 'Version 1.2 Date 08.04.2022'"),
    '99848ddf0f': ('ITALMATCH:DAPRALUBE_9501', 'SDS',
                   "12pp; 'Version 1.0 Date 24.05.2023'; Product code 1008016/1000675"),
}

# pre-register all products
for p10, (key, name, notes, _, mc) in PRODUCTS.items():
    prod(PK, key, name, SUP, mc, notes)

prod(PK, 'ITALMATCH:POLARTECH_8221', 'Polartech 8221', SUP, OT,
     "printed: 'Polartech® 8221 Boron technology combined emulsifier and corrosion inhibitor package'; "
     "MWF application; from DL2-13170 2pp product sheet")
prod(PK, 'ITALMATCH:POLARTECH_AF_2000', 'Polartech AF 2000', SUP, OT,
     "printed: 'Polartech® AF 2000 Antifoaming and Defoaming Additive Organo Polysiloxane Defoaming Additive; "
     "high performance Polysiloxane based antifoam for use in watermix metalworking fluids'")
prod(PK, 'ITALMATCH:POLARTECH_8310', 'Polartech 8310', SUP, OT,
     "printed: 'Polartech® 8310 Synthetic Corrosion Inhibitor Package; to form the basis of a series of "
     "high performance metalworking fluids; Boron Technology'")
prod(PK, 'ITALMATCH:DAPRALUBE_77',    'Dapralube 77',    SUP, OT,
     "'Dapralube® 77'; Italmatch MWF specialty chemical; application in metalworking coolant systems; "
     "identity confirmed by SDS DL2-15233")
prod(PK, 'ITALMATCH:DAPRALUBE_9501',  'Dapralube 9501',  SUP, OT,
     "'Dapralube® 9501 Product code 1008016/1000675'; Italmatch MWF specialty chemical")
prod(PK, 'ITALMATCH:KETJENLUBE_09', 'Ketjenlube 09', SUP, 'unresolved',
     "'Ketjenlube© Polymer Esters... conventional esters... synthetic and natural esters under the Ketjenlube trade name'; "
     "Ketjenlube 09 specific type and application not stated on page 1 (ester range overview document); "
     "synthetic esters can be Group V base fluids or lubricant additives (polyol ester, TMP ester); "
     "material class and template to be confirmed from full read",
     evidence='auto-classified Ketjenlube 09 (medium confidence); page-1 text: ester range overview')

for r in rows(lambda s: s == 'Italmatch', OWN):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 in PRODUCTS:
        key, name, _, dtype, _ = PRODUCTS[p10]
        doc(D, sha, dtype, SUP, [key],
            'page-1 text (product name in second paragraph after copyright boilerplate)',
            manufacturer=MFG, issuer=SUP,
            note='1pp TDS; product name follows copyright boilerplate at top of page')

    elif p10 in PAIRED:
        key, dtype, note = PAIRED[p10]
        doc(D, sha, dtype, SUP, [key],
            'page-1 text (product name, SDS header)',
            manufacturer=MFG, issuer=SUP, note=note)

    elif p10 == '2ee6e2828b':  # DL2-13170 Polartech 8221 2pp product sheet
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['ITALMATCH:POLARTECH_8221'],
            'page-1 text (product properties table)',
            manufacturer=MFG, issuer=SUP,
            note="2pp; 'Polartech® 8221 Boron technology combined emulsifier and corrosion inhibitor package'; "
                 "properties: Specific Gravity 1.00, Total Alkalinity 12% wt KOH, Stability tests")
    elif p10 == '31d806bd73':  # DL2-13264 Polartech AF 2000 TDS
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['ITALMATCH:POLARTECH_AF_2000'],
            'page-1 text (product name and description)',
            manufacturer=MFG, issuer=SUP,
            note="1pp; 'Polartech® AF 2000 Antifoaming and Defoaming Additive Organo Polysiloxane Defoaming Additive; "
                 "high performance Polysiloxane based antifoam for use in watermix metalworking fluids'")
    elif p10 == '34d2ee7e67':  # DL2-13608 Polartech 8310 TDS (2pp)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['ITALMATCH:POLARTECH_8310'],
            'page-1 text (product name and typical characteristics)',
            manufacturer=MFG, issuer=SUP,
            note="2pp; 'Polartech 8310 Appearance Amber/green fluid SG 1.17 Total Alkalinity 34% KOH; "
                 "Combined Emulsifier and Corrosion Inhibitor Package; Boron Technology; "
                 "MWF application'")
    elif p10 == '37cea831d5':  # DL2-13610 MWF package range catalog (24pp, confidential)
        doc(D, sha, 'product range catalog (internal)', SUP, [],
            'page-1 text (catalog header; Conventional Packages table excerpt)',
            relation='non_product',
            issuer=SUP,
            note="'Confidential and Proprietary — not to be copied or shared'; 24pp internal Italmatch MWF package range; "
                 "covers Polartech and other packages in table form with chemistry, compatibility, treat rates; "
                 "not a TDS or SDS; multiple products mentioned")
    elif p10 == '7200033086':  # DL2-13857 Ketjenlube 09 ester range overview (1pp, x2)
        doc(D, sha, 'product data sheet (TDS/PDS)', SUP, ['ITALMATCH:KETJENLUBE_09'],
            'page-1 text (ester range overview; Ketjenlube 09 named in full text per auto-classifier)',
            manufacturer=MFG, issuer=SUP,
            note="x2 copies in archive; 'Conventional Esters... wide range of synthetic and natural esters under the Ketjenlube trade name'; "
                 "auto-classified Ketjenlube 09 (medium confidence); specific product details not on page 1; "
                 "1pp overview may be a summary sheet for the Ketjenlube ester range")

write(OWN,
      'S31 Italmatch (identity)',
      '15 documents with provisional supplier Italmatch',
      PK, D)
