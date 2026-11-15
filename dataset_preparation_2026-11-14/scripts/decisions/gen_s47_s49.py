"""Supplier batches S47 ADNOC (7), S48 FRAGOL (7), S49 Kraton (7).

S47 ADNOC — ADNOC Refining, Abu Dhabi National Oil Company. All five ADbase grades
(2/3/4/6/8 cSt, Group III PAO-blend) are EXISTING production records. Batch contains:
a 10pp product brochure (DL2-12151) covering the ADbase range; a 1pp multi-grade range
TDS (DL2-12221) with all five grades; two Afton Chemical dexos1 Gen 2 formulation guides
using ADNOC 4 and ADNOC 6 (DL2-12248 1pp, DL2-13230 8pp) → non_product; a CoA for
ADbase GCST (6cSt) batch RE-2020 12290 (DL2-14106); two 1pp classified-only pages with
"ADNOC Classification: Internal" and no other legible text (DL2-14075, DL2-14107) →
unresolved_identity.

S48 FRAGOL — FRAGOL AG, Mülheim, Germany. Specialised heat-transfer fluids only. All four
products are out_of_template (heat transfer fluid — no lubricant component template exists).
Products: FRAGOLTHERM HT (Dibenzylbenzene ar-methyl derivative; operating range 0–350°C;
DL2-13178 2pp TDS, DL2-13467 2pp product info, DL2-13468 11pp SDS), FRAGOLTHERM 660
(Terphenyl hydrogenated; DL2-13179 14pp SDS REACH, e3f3c66a60 19pp MSDS older edition),
FRAGOLTHERM DPO (diphenyl oxide; DL2-13180 3pp TDS), FRAGOLTHERM 550 (DL2-15598 2pp TDS,
operating range -10 to 315°C).

S49 Kraton — Kraton Polymers LLC, Houston TX (Kraton Corporation). Star and diblock SEBS/
SEP polymers. G1750 V and G1765 (star-structured EP polymers, oil-extended variant) are
additive_component (VM) — G1750 CoA has standard lubricant VII test (kV100 at 1.70%w in
oil, 11.8–14.1 cSt), and both are covered by the G1750/G1765 SDS. G1701 E (S-E/P diblock
linear) mentions "oil gel applications" suggesting lubricant use — material class unresolved
(could be additive_component VM or out_of_template depending on evidence). G1701 M and
G1702 H: bitumen/adhesive/footwear/sealant applications with no lubricant use stated →
out_of_template.

Writes decisions/s47_adnoc.json, s48_fragol.json, s49_kraton.json."""
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S47 ADNOC
# ===========================================================================
SUP47 = 'ADNOC'
MFG47 = 'Abu Dhabi National Oil Company (ADNOC) Refining'
B47 = 'base_oil'
OWT47 = 'out_of_template (heat transfer fluid)'

EXISTING47 = {
    'EXISTING:ADNOC_ADBASE_2CST': 'ADbase 2CST',
    'EXISTING:ADNOC_ADBASE_3CST': 'ADbase 3CST',
    'EXISTING:ADNOC_ADBASE_4CST': 'ADbase 4CST',
    'EXISTING:ADNOC_ADBASE_6CST': 'ADbase 6CST',
    'EXISTING:ADNOC_ADBASE_8CST': 'ADbase 8CST',
}
ALL47 = list(EXISTING47.keys())

D47, PK47 = {}, {}
for key, name in EXISTING47.items():
    rec = key.replace('EXISTING:', '')
    prod(PK47, key, name, SUP47, B47,
         'printed product name on the documents linked in this batch', existing=rec)
prod(PK47, 'ADNOC:UNKNOWN_DOC_DL2_14075', 'DL2-14075 (unresolved)', SUP47,
     'unresolved',
     "document consists only of 'ADNOC Classification: Internal' header; "
     "no product name, no data visible; likely a cover page or classification banner; "
     "product identity unresolved; next_action: physical inspection or OCR scan",
     status='unresolved_identity')
prod(PK47, 'ADNOC:UNKNOWN_DOC_DL2_14107', 'DL2-14107 (unresolved)', SUP47,
     'unresolved',
     "document consists only of 'ADNOC Classification: Internal' header; "
     "no product name, no data visible; likely a cover page or classification banner; "
     "product identity unresolved; next_action: physical inspection or OCR scan",
     status='unresolved_identity')

for r in rows(lambda s: s == 'ADNOC', 's47_adnoc.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '308a48fabf':  # DL2-12151 ADbase brochure 10pp
        doc(D47, sha, 'product brochure', SUP47, ALL47,
            'table of contents and opening text: ADbase product range brochure',
            manufacturer=MFG47, issuer=MFG47,
            note="10pp; 'QUALITY CONSISTENCY RELIABILITY adnoc.ae'; TOC: About ADbase, process diagram, "
                 "Product specifications, Product consistency 4cSt 6cSt (highlighted), formulation approvals, "
                 "contact, exclusive sellers; covers full ADbase range 2/3/4/6/8 cSt; 4cSt and 6cSt get "
                 "dedicated consistency sections")
    elif p10 == '16b2a05864':  # DL2-12221 range TDS 1pp
        doc(D47, sha, 'product data sheet (range TDS)', SUP47, ALL47,
            'full page content: multi-grade typical properties table for all five ADbase grades',
            manufacturer=MFG47, issuer=MFG47,
            note="1pp range TDS; 'PROPERTIES Unit ADbase 2CST ADbase 3CST ADbase 4CST ADbase 6CST ADbase 8CST'; "
                 "covers: kV100, kV40, VI, Density @15°C, PP, FP, Noack evaporation, CCS @-30°C, "
                 "Sulfur (all <3 mg/kg), Aromatics (<0.2 mass%), Saturates (99.8 mass%); "
                 "all five grades covered")
    elif p10 == '868976f115':  # DL2-12248 dexos1 Gen 2 formulation guide 1pp
        doc(D47, sha, 'formulation guide (Afton Chemical / dexos1 Gen 2)', 'Afton Chemical',
            [], 'page content: dexos1 Gen 2 formulation using ADNOC 4 and ADNOC 6 base stocks',
            relation='non_product', issuer='Afton Chemical',
            note="1pp; 'dexos1TM Gen 2 ADNOC Final Formulations'; two formulations: 0W-20 and 5W-30; "
                 "components: ADNOC 4 (73.70/59.40 wt%), ADNOC 6 (10.00/21.20 wt%), HiTEC 11180 DI package, "
                 "HiTEC 5754A VI modifier; not an ADNOC product sheet; "
                 "mislabeled under ADNOC supplier — actual subject: Afton Chemical dexos1 formulation")
    elif p10 == '2d080036c0':  # DL2-13230 dexos1 Gen 2 formulation guide 8pp
        doc(D47, sha, 'formulation guide (Afton Chemical / dexos1 Gen 2)', 'Afton Chemical',
            [], 'page-1 content: multi-viscosity dexos1 Gen 2 formulations using ADNOC base stocks',
            relation='non_product', issuer='Afton Chemical',
            note="8pp; 'dexos1TM Gen 2 ADNOC Final Formulations'; extends the 1pp version (DL2-12248) with "
                 "three formulations (0W-16, 0W-20, 5W-30); same components: ADNOC 4, ADNOC 6, HiTEC 11180, HiTEC 5754A; "
                 "includes base oil property table and finished oil test data against dexos1 Gen 2 limits; "
                 "not an ADNOC product document")
    elif p10 == 'b0b334f256':  # DL2-14075 classified page 1pp
        doc(D47, sha, 'unresolved_identity', SUP47, ['ADNOC:UNKNOWN_DOC_DL2_14075'],
            "text layer contains only 'ADNOC Classification: Internal'; "
            "no product name or data visible",
            relation='unresolved_identity', issuer=MFG47,
            note="1pp; entire text layer: 'ADNOC Classification: Internal'; "
                 "likely a document cover page, classification banner, or header-only page; "
                 "next_action: physical inspection or OCR re-scan to identify product content",
            next_action='physical inspection / OCR re-scan needed')
    elif p10 == '56a48fd0a6':  # DL2-14106 ADbase GCST CoA 1pp
        doc(D47, sha, 'certificate of quality (CoA)', SUP47, ['EXISTING:ADNOC_ADBASE_6CST'],
            'page content: CoA header and test parameters for ADbase GCST (6cSt) batch',
            manufacturer=MFG47, issuer=MFG47,
            note="1pp; 'CERTIFICATE OF QUALITY SPEC.NO. R.RE/BO•060 CERT.NO. I 2020 08/07/2020'; "
                 "GRADE: BASE OIL AD BASE GCST; BATCH NO. 8360 202.0; "
                 "test parameters listed: kV100, kV40, VI, PP, FP (COC), Noack evaporation, CCS @-30°C, "
                 "Sulfur, Water, Color Saybolt, Density @15°C, Copper Corrosion 3h@100°C, Acid No., "
                 "Carbon Residue, Saturates, Aromatics; "
                 "GCST = ADbase 6cSt grade designation; issued by ADNOC Refining QC")
    elif p10 == '9c088f5618':  # DL2-14107 classified page 1pp
        doc(D47, sha, 'unresolved_identity', SUP47, ['ADNOC:UNKNOWN_DOC_DL2_14107'],
            "text layer contains only 'ADNOC Classification: Internal'; "
            "no product name or data visible",
            relation='unresolved_identity', issuer=MFG47,
            note="1pp; entire text layer: 'ADNOC Classification: Internal'; "
                 "see DL2-14075 (b0b334f256) — same situation; "
                 "next_action: physical inspection or OCR re-scan",
            next_action='physical inspection / OCR re-scan needed')

write('s47_adnoc.json', 'S47 ADNOC (identity)',
      '7 documents with provisional supplier ADNOC', PK47, D47)

# ===========================================================================
# S48 FRAGOL
# ===========================================================================
SUP48 = 'FRAGOL'
MFG48 = 'FRAGOL AG'
OWT48 = 'out_of_template (heat transfer fluid — no lubricant template)'

D48, PK48 = {}, {}
for key, name, note_text in [
    ('FRAGOL:FRAGOLTHERM_HT', 'FRAGOLTHERM HT',
     "printed: 'FRAGOLTHERM® HT Heat Transfer Fluid 0°C to 350°C'; CAS 53585-53-8, Dibenzylbenzene "
     "ar-methyl derivative; EC 258-649-2; heat transfer fluid, synthetic type; "
     "operating range 0 to 350°C; out_of_template (no lubricant component template)"),
    ('FRAGOL:FRAGOLTHERM_660', 'FRAGOLTHERM 660',
     "printed: 'FRAGOLTHERM® 660 Heat Transfer Fluid'; CAS 61788-32-7, Terphenyl hydrogenated; "
     "EC 262-967-7; REACH registration 01-2119488183-33-xxxx; heat transfer fluid; "
     "out_of_template (no lubricant component template)"),
    ('FRAGOL:FRAGOLTHERM_DPO', 'FRAGOLTHERM DPO',
     "printed: 'FRAGOLTHERM® DPO'; diphenyl oxide type heat transfer fluid; "
     "operating range 12 to 400°C; out_of_template (no lubricant component template)"),
    ('FRAGOL:FRAGOLTHERM_550', 'FRAGOLTHERM 550',
     "printed: 'FRAGOLTHERM® 550 Heat Transfer Fluid -10°C to 315°C'; "
     "heat transfer fluid; out_of_template (no lubricant component template)"),
]:
    prod(PK48, key, name, SUP48, OWT48, note_text)

for r in rows(lambda s: s == 'FRAGOL', 's48_fragol.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '771495801b':  # DL2-13178 FRAGOLTHERM HT 2pp TDS
        doc(D48, sha, 'product data sheet (TDS/PDS)', SUP48, ['FRAGOL:FRAGOLTHERM_HT'],
            'page-1 text: product name and operating range',
            manufacturer=MFG48, issuer=MFG48,
            note="2pp; 'FRAGOLTHERM® HT Heat Transfer Fluid'; synthetic heat transfer fluid; "
                 "operating range 0°C to 350°C; Dibenzylbenzene ar-methyl derivative; CAS 53585-53-8")
    elif p10 == '81518e2037':  # DL2-13179 FRAGOLTHERM 660 14pp SDS (REACH)
        doc(D48, sha, 'SDS', SUP48, ['FRAGOL:FRAGOLTHERM_660'],
            'section 1: product identifier and supplier for FRAGOLTHERM 660',
            manufacturer=MFG48, issuer=MFG48,
            note="14pp; REACH SDS; 'Trade name FRAGOLTHERM 660'; CAS 61788-32-7, Terphenyl hydrogenated; "
                 "REACH 01-2119488183-33-xxxx; issued by FRAGOL AG, Mülheim")
    elif p10 == 'f9f4fa39f0':  # DL2-13180 FRAGOLTHERM DPO 3pp TDS
        doc(D48, sha, 'product data sheet (TDS/PDS)', SUP48, ['FRAGOL:FRAGOLTHERM_DPO'],
            'page-1 and page-2 text: product name, description and properties',
            manufacturer=MFG48, issuer=MFG48,
            note="3pp; 'FRAGOLTHERM® DPO'; diphenyl oxide heat transfer fluid; "
                 "operating range 12°C to 400°C; thermal stability up to 400°C")
    elif p10 == 'c94ff2292c':  # DL2-13467 FRAGOLTHERM HT 2pp product info
        doc(D48, sha, 'product data sheet (TDS/PDS)', SUP48, ['FRAGOL:FRAGOLTHERM_HT'],
            'page-1 text: product name and brief description',
            manufacturer=MFG48, issuer=MFG48,
            note="2pp; 'FRAGOLTHERM® HT'; same product as DL2-13178 (771495801b); "
                 "possibly an older or alternate edition of the HT TDS")
    elif p10 == '7c16634657':  # DL2-13468 FRAGOLTHERM HT 11pp SDS
        doc(D48, sha, 'SDS', SUP48, ['FRAGOL:FRAGOLTHERM_HT'],
            'section 1: product identifier — FRAGOLTHERM HT; Dibenzylbenzene ar-methyl derivative',
            manufacturer=MFG48, issuer=MFG48,
            note="11pp; 'Trade name FRAGOLTHERM HT'; CAS 53585-53-8, Dibenzylbenzene ar-methyl derivative; "
                 "EC 258-649-2; REACH 01-2119488667-17-xxxx; issued by FRAGOL AG")
    elif p10 == '9c80fcbdd4':  # DL2-15598 FRAGOLTHERM 550 2pp TDS
        doc(D48, sha, 'product data sheet (TDS/PDS)', SUP48, ['FRAGOL:FRAGOLTHERM_550'],
            'page-1 text: product name, operating range',
            manufacturer=MFG48, issuer=MFG48,
            note="2pp; 'FRAGOLTHERM® 550 Heat Transfer Fluid'; operating range -10°C to 315°C")
    elif p10 == 'e3f3c66a60':  # MSDS FRAGOLTHERM 660 19pp (older edition)
        doc(D48, sha, 'SDS', SUP48, ['FRAGOL:FRAGOLTHERM_660'],
            'section 1: product identifier and supplier for FRAGOLTHERM 660',
            manufacturer=MFG48, issuer=MFG48,
            note="19pp; older MSDS edition (pre-2015 format, no REACH registration number); "
                 "'Trade name FRAGOLTHERM 660'; CAS 61788-32-7, Terphenyl hydrogenated; EC 262-967-7; "
                 "issued by FRAGOL AG; htf@fragol.de; "
                 "see also DL2-13179 (81518e2037) for the newer 14pp REACH SDS")

write('s48_fragol.json', 'S48 FRAGOL (identity)',
      '7 documents with provisional supplier FRAGOL', PK48, D48)

# ===========================================================================
# S49 Kraton
# ===========================================================================
SUP49 = 'Kraton'
MFG49 = 'Kraton Polymers LLC / Kraton Corporation'
AC49 = 'additive_component'
OWT49 = 'out_of_template (adhesive/bitumen/polymer modifier — no lubricant application stated)'
U49 = 'unresolved (additive_component or out_of_template — oil gel / lubricant use noted but unclear)'

D49, PK49 = {}, {}
prod(PK49, 'KRATON:G1701_E', 'Kraton G1701 E', SUP49, U49,
     "printed: 'Kraton G1701 E is a clear linear diblock copolymer based on styrene and ethylene/propylene, "
     "S-E/P, with bound styrene of 35% mass; used in formulating adhesives and coatings, as base material "
     "for compound formulations, as a modifier of thermoplastics and as base material for oil gel applications'; "
     "material class unresolved: 'oil gel applications' implies potential lubricant VII use, "
     "but primary stated market is adhesives/thermoplastics; needs template and evidence review")
prod(PK49, 'KRATON:G1701_M', 'Kraton G1701 M', SUP49, OWT49,
     "printed: 'Kraton G1701 M is a clear, linear diblock copolymer based on styrene and ethylene/propylene "
     "with a polystyrene content of 37%; used as a modifier of bitumen and polymers; also suitable as an "
     "ingredient in formulating compounds for footwear applications and may be used in formulating adhesives, "
     "sealants, and coatings'; no lubricant application stated → out_of_template")
prod(PK49, 'KRATON:G1702_H', 'Kraton G1702 H', SUP49, OWT49,
     "printed: 'Kraton G1702 H'; S-E/P diblock; used for adhesives, sealants, coatings, bitumen/asphalt modifier; "
     "no lubricant application stated → out_of_template (adhesive/bitumen/polymer modifier)")
prod(PK49, 'KRATON:G1750_V', 'Kraton G1750 V', SUP49, AC49,
     "printed: 'Kraton G1750 V is a clear, multi-arm polymer based on ethylene/propylene; "
     "supplied from Taiwan as a bale'; CoA (DL2-15680) tests kV100 at 1.70%w in oil = 11.8–14.1 cSt range, "
     "result 13.1 cSt — standard lubricant VII test method; star polymer SEBS structure; "
     "additive_component (VM, star polymer)")
prod(PK49, 'KRATON:G1765', 'Kraton G1765', SUP49, AC49,
     "printed: SDS (DL2-15681) covers 'G1750, G1765' together under 'Kraton G Polymers (EP and EP OE)'; "
     "EP OE designation = ethylene/propylene oil-extended star polymer; "
     "co-listed with G1750 V in SDS → same polymer class; "
     "additive_component (VM, star polymer oil-extended variant); no separate TDS in this batch")

for r in rows(lambda s: s == 'Kraton', 's49_kraton.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == 'a08813bc22':  # DL2-14629 G1701 E TDS 2pp
        doc(D49, sha, 'product data sheet (TDS/PDS)', SUP49, ['KRATON:G1701_E'],
            'page-1 text: product description, applications, physical form',
            manufacturer=MFG49, issuer=MFG49,
            note="'K0042 Europe 10/9/2019 KRATONTM G1701 E Polymer'; 2pp; "
                 "S-E/P diblock linear copolymer, bound styrene 35%; "
                 "applications: adhesives, coatings, thermoplastic compounds, oil gel; "
                 "'oil gel applications' is a potential lubricant use case")
    elif p10 == '91f3b59fa9':  # DL2-14630 G1701 M TDS 2pp
        doc(D49, sha, 'product data sheet (TDS/PDS)', SUP49, ['KRATON:G1701_M'],
            'page-1 text: product description, applications',
            manufacturer=MFG49, issuer=MFG49,
            note="'K0657 North America 11/11/2019 KRATONTM G1701 M Polymer'; 2pp; "
                 "S-E/P diblock linear, polystyrene content 37%; "
                 "applications: bitumen modifier, polymer modifier, footwear compounds, adhesives/sealants/coatings; "
                 "no lubricant application stated")
    elif p10 == 'ec63eedf52':  # DL2-14631 G1702 H TDS 2pp
        doc(D49, sha, 'product data sheet (TDS/PDS)', SUP49, ['KRATON:G1702_H'],
            'page-1 text: product description, applications',
            manufacturer=MFG49, issuer=MFG49,
            note="2pp; Kraton G1702 H; S-E/P diblock; adhesives, sealants, bitumen/asphalt modifier; "
                 "no lubricant application stated → out_of_template")
    elif p10 == '3e421e9567':  # DL2-14632 SDS for G1701/G1702/G1730 7pp
        doc(D49, sha, 'SDS', SUP49,
            ['KRATON:G1701_E', 'KRATON:G1701_M', 'KRATON:G1702_H'],
            'section 1: SDS covering Kraton G Polymers SEP(S) grades G1701 and G1702',
            manufacturer=MFG49, issuer=MFG49,
            note="7pp; 'Kraton G Polymers (SEP(S)) SDS number 14312'; "
                 "covers all alphanumeric suffixes of G1701, G1702, G1730; "
                 "G1730 not in this batch; issued by Kraton Polymers LLC, Houston TX")
    elif p10 == 'be598dbb11':  # DL2-15680 G1750 CoA 1pp
        doc(D49, sha, 'certificate of quality (CoA)', SUP49, ['KRATON:G1750_V'],
            'page content: CoA with batch test results for G1750',
            manufacturer=MFG49, issuer=MFG49,
            note="1pp; CoA for G1750 V batch; test results: Visc,Kin,1.70%w @100C = 13.1 cSt "
                 "(spec 11.8–14.1 cSt, method AGAM 1201); Volatile Matter 0.1% (spec max 0.7%, method KM 04); "
                 "Antioxidant 0.06% (spec 0.03–0.20%, method KM 08); "
                 "kV100 test at 1.70%w is the standard lubricant VII characterization protocol")
    elif p10 == 'cdd7a9a6a2':  # DL2-15681 SDS for G1750/G1765 7pp
        doc(D49, sha, 'SDS', SUP49,
            ['KRATON:G1750_V', 'KRATON:G1765'],
            'section 1: SDS covering Kraton G Polymers EP and EP OE grades G1750 and G1765',
            manufacturer=MFG49, issuer=MFG49,
            note="7pp; 'Kraton G Polymers (EP and EP OE) SDS number 14401'; "
                 "covers all alphanumeric suffixes of G1750 and G1765; "
                 "EP = ethylene/propylene star polymer; EP OE = oil-extended variant (G1765); "
                 "issued by Kraton Corporation")
    elif p10 == 'b5e171c2aa':  # DL2-15682 G1750 V TDS 3pp
        doc(D49, sha, 'product data sheet (TDS/PDS)', SUP49, ['KRATON:G1750_V'],
            'page-1 text: product description and sales specifications',
            manufacturer=MFG49, issuer=MFG49,
            note="'K0628 Asia 10/28/2018 KRATONTM G1750 V Polymer'; 3pp; "
                 "multi-arm star polymer based on ethylene/propylene; supplied from Taiwan as bale; "
                 "applications stated: modifier of polymers, footwear compounds, adhesives/sealants/coatings; "
                 "despite non-lubricant application list, CoA (DL2-15680) uses standard lubricant VII test; "
                 "this TDS covers antioxidant and volatile matter specs")

write('s49_kraton.json', 'S49 Kraton (identity)',
      '7 documents with provisional supplier Kraton', PK49, D49)
