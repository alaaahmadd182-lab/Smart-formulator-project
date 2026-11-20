"""Supplier batches S43 Tianhe Chemicals (9), S44 Saudi Aramco/Luberef (9),
S45 Plasmoil (9), S46 Cristol (8).

S43 Tianhe Chemical Group (english.tianhechem.com). C-TEC series (additive components):
104A (calcium sulfonate detergent, TBN25), 151A (PIBSI dispersant), 206 (ZDDP primary-
secondary), 209 (ZDDP secondary). P-TEC series (additive packages): 3232 existing,
3234 (API CF diesel), 9100 (PCMO/motorcycle). Two xlsx range-table files for a Tianhe
Sunshine T-series (T-202 through T-154A) — multi-product reference table, non_product.

S44 Saudi Aramco / Luberef. All products are existing records. aramcoDURA 150 (Jeddah GI,
SDS dupOLD), aramcoDURA 150BS (Yanbu GI BS, SDS dupOLD), aramcoPRIMA 70 (SDS dupOLD),
multi-product range TDS for aramcoPRIMA 70/110/230/500 (DL2-12172 dupOLD), Luberef GII
range TDS for aramcoDURA 150/500 (DL2-12173 dupOLD), DL2-12180 (Yanbu Refinery aramcoDURA
BS150 spec sheet), DL2-12296 (NB051 Technical Data Sheet for Saudi Aramco Group II N70,
issued by Sama Lubricants — buyer/distributor issuer; assigned to aramcoPRIMA 70 on spec
match kV40 14.20, kV100 3.208, VI 83, PP -30°C, FP 176°C). DL2-15293 (OLOA 59211 Afton
formulation using Aramco Prima base) → non_product.

S45 Plasmoil / MicRos Lubrication Technology Ltd (Suzhou, Jiangsu, China; parent in Belgium).
Plasmoil products are "API Group V" bio-based lubricant additives/bases made by electro-
polarization of vegetable oils. Products: Plasmoil Bio, MR-A, MR-B, MR-H (described together
in a combined TDS). Material class: unresolved (bio-based Group V; additive_component or base
stock component; template to be confirmed). DL2-15593 is an Agilent Technologies marketing
letter to MicRos LT, not a Plasmoil product document → non_product.

S46 Cristol™ (manufacturer India, brand identity confirmed by website / letterhead).
Four products: EPR-3400 (ashless antioxidant for greases/lubricating oils), PMA D-70
(dispersant-type PMA viscosity modifier), PPD LX 250 (PMA pour point depressant for
automotive lubricants), VII-400 (PMA-based VII for hydraulic oils). All additive_component.

Writes decisions/s43_tianhe.json, s44_saudi_aramco.json, s45_plasmoil.json, s46_cristol.json."""
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S43 Tianhe Chemicals
# ===========================================================================
SUP43 = 'Tianhe Chemical Group'
MFG43 = SUP43
AC = 'additive_component'
AP = 'additive_package'

D43, PK43 = {}, {}
prod(PK43, 'TIANHE:C_TEC_104A', 'C-TEC 104A', SUP43, AC,
     "printed: 'C-TEC 104A (TBN25) LOW BASE SYNTHETIC ALKYL BENZENE CALCIUM SULFONATE; "
     "provides engine oils with fine detergency, dispersion and antirust effects'; "
     "additive_component (detergent, calcium sulfonate)")
prod(PK43, 'TIANHE:C_TEC_151A', 'C-TEC 151A', SUP43, AC,
     "printed: 'C-TEC 151A POLYISOBUTYLENE SUCCINIMIDE; ashless dispersant prepared from highly "
     "reactive isobutylene (f=1300) by thermal process; good detergency and low temperature dispersancy'; "
     "additive_component (dispersant, PIBSI)")
prod(PK43, 'TIANHE:C_TEC_206', 'C-TEC 206', SUP43, AC,
     "printed: 'C-TEC 206 ZINC PRIMARY-SECONDARY ALKYL DITHIOPHOSPHATE; zinc thiophosphate prepared "
     "from thiophosphoric acid made from mixed primary-secondary alcohols; inhibit oils oxidation'; "
     "additive_component (antioxidant/antiwear ZDDP, mixed primary-secondary)")
prod(PK43, 'TIANHE:C_TEC_209', 'C-TEC 209', SUP43, AC,
     "printed: 'C-TEC 209 ZINC SECONDARY ALKYL DITHIOPHOSPHATE; zinc thiophosphate prepared from "
     "thiophosphoric acid made from secondary alcohols'; "
     "additive_component (antioxidant/antiwear ZDDP, secondary)")
prod(PK43, 'EXISTING:TIANHE_P_TEC_3232', 'P-TEC 3232', SUP43, AP,
     'printed product name on the documents linked in this batch', existing='TIANHE_P_TEC_3232')
prod(PK43, 'TIANHE:P_TEC_3234', 'P-TEC 3234', SUP43, AP,
     "printed: 'P-TEC 3234 DIESEL ENGINE OIL PACKAGE; developed to meet API CF performance'; "
     "additive_package (diesel engine oil, API CF)")
prod(PK43, 'TIANHE:P_TEC_9100', 'P-TEC 9100', SUP43, AP,
     "printed: 'P-TEC 9100 PASSENGER CAR AND MOTOCYCLE ENGINE OIL PACKAGE; "
     "API SL performance levels at different treat rates'; additive_package (PCMO/JASO MA)")

for r in rows(lambda s: s == 'Tianhe Chemicals', 's43_tianhe.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '9459a8a39e':  # DL2-12936 C-TEC 104A TDS 2pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:C_TEC_104A'],
            'page-1 text: product name, CAS class, typical properties',
            manufacturer=MFG43, issuer=MFG43, note="2pp; ENGLISH.TIANHECHEM.COM format")
    elif p10 == '00b65021a6':  # DL2-12937 C-TEC 151A TDS 2pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:C_TEC_151A'],
            'page-1 text: product name, chemistry, typical properties',
            manufacturer=MFG43, issuer=MFG43, note="2pp; PIBSI dispersant")
    elif p10 == 'fcaf972e35':  # DL2-12938 C-TEC 206 TDS 2pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:C_TEC_206'],
            'page-1 text: product name, chemistry',
            manufacturer=MFG43, issuer=MFG43, note="2pp; ZDDP primary-secondary")
    elif p10 == '5b48698eaa':  # DL2-13361 C-TEC 209 TDS 3pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:C_TEC_209'],
            'page-1 text: product name, URL, chemistry',
            manufacturer=MFG43, issuer=MFG43,
            note="3pp; captured from tianhechem.com/Products/CorrosionInhibitors/10490753; "
                 "ZDDP secondary; date captured 7/18/2020")
    elif p10 in ('c793935c48', '425b59d81f'):  # DL2-12141/12142 Tianhe Sunshine xlsx range tables
        doc(D43, sha, 'product range reference table (xlsx)', 'Tianhe Sunshine', [],
            'spreadsheet content: multi-product properties table covering T-202 through T-154A',
            relation='non_product', issuer='Tianhe Sunshine',
            note="xlsx file; 'Tianhe Sunshine' brand; covers T-202 (ZDDP), T-203 (ZDDP), T-204 (ZDDP), "
                 "T-161/T-161B (PIBSI/boronated PIBSI), L557 (DPA antioxidant), T-106/T-106A (high-base sulfonate), "
                 "T-115B (high-base sulfurized phenate), T-154A (PIBSI); multi-product reference; "
                 "Tianhe Sunshine is a related entity to Tianhe Chemical Group")
    elif p10 == 'de5df90125':  # DL2-12939 P-TEC 3232 TDS 2pp (dupOLD)
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['EXISTING:TIANHE_P_TEC_3232'],
            'page-1 text: product name and type', manufacturer=MFG43, issuer=MFG43,
            note="dupOLD; 'P-TEC 3232 GENERAL PURPOSE ENGINE OIL PACKAGE'; 2pp")
    elif p10 == 'afcbf1a67b':  # DL2-12940 P-TEC 3234 TDS 2pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:P_TEC_3234'],
            'page-1 text: product name, performance claims',
            manufacturer=MFG43, issuer=MFG43,
            note="'P-TEC 3234 DIESEL ENGINE OIL PACKAGE; developed to meet API CF performance'; 2pp")
    elif p10 == '248ffefbcc':  # DL2-12941 P-TEC 9100 TDS 2pp
        doc(D43, sha, 'product data sheet (TDS/PDS)', SUP43, ['TIANHE:P_TEC_9100'],
            'page-1 text: product name, performance claims',
            manufacturer=MFG43, issuer=MFG43,
            note="'P-TEC 9100 PASSENGER CAR AND MOTOCYCLE ENGINE OIL PACKAGE; API SL'; 2pp")

write('s43_tianhe.json', 'S43 Tianhe Chemicals (identity)',
      '9 documents with provisional supplier Tianhe Chemicals', PK43, D43)

# ===========================================================================
# S44 Saudi Aramco / Luberef
# ===========================================================================
SUP44 = 'Saudi Aramco / Luberef'
MFG44 = 'Saudi Aramco Oil Company / Luberef'
B = 'base_oil'

EXISTING44 = {
    'EXISTING:ARAMCO_LUBEREF_DURA_150_JEDDAH': ('ARAMCO_LUBEREF_DURA_150_JEDDAH', 'aramcoDURA 150 (Jeddah)'),
    'EXISTING:ARAMCO_LUBEREF_DURA_500_JEDDAH': ('ARAMCO_LUBEREF_DURA_500_JEDDAH', 'aramcoDURA 500 (Jeddah)'),
    'EXISTING:ARAMCO_LUBEREF_DURA_BS150_YANBU': ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'aramcoDURA BS150 (Yanbu)'),
    'EXISTING:ARAMCO_LUBEREF_PRIMA_70': ('ARAMCO_LUBEREF_PRIMA_70', 'aramcoPRIMA 70'),
    'EXISTING:ARAMCO_LUBEREF_PRIMA_110': ('ARAMCO_LUBEREF_PRIMA_110', 'aramcoPRIMA 110'),
    'EXISTING:ARAMCO_LUBEREF_PRIMA_230': ('ARAMCO_LUBEREF_PRIMA_230', 'aramcoPRIMA 230'),
    'EXISTING:ARAMCO_LUBEREF_PRIMA_500': ('ARAMCO_LUBEREF_PRIMA_500', 'aramcoPRIMA 500'),
}

D44, PK44 = {}, {}
for key, (rec, name) in EXISTING44.items():
    prod(PK44, key, name, SUP44, B,
         'printed product name on the documents linked in this batch', existing=rec)

for r in rows(lambda s: s == 'Saudi Aramco / Luberef', 's44_saudi_aramco.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == 'c93939869f':  # DL2-15783 aramcoDURA 150 SDS 9pp (dupOLD)
        doc(D44, sha, 'SDS', SUP44, ['EXISTING:ARAMCO_LUBEREF_DURA_150_JEDDAH'],
            'page-1 text: product name, SDS revision', manufacturer=MFG44, issuer=MFG44,
            note="dupOLD; 'aramcoDURA® 150 Revision nr: 2.0 Issue date: 05/08/2019 Location: Jeddah'; 9pp EU-REACH SDS")
    elif p10 == 'e599b547c4':  # DL2-12648 aramcoDURA 150BS SDS 9pp (dupOLD)
        doc(D44, sha, 'SDS', SUP44, ['EXISTING:ARAMCO_LUBEREF_DURA_BS150_YANBU'],
            'page-1 text: product name, location', manufacturer=MFG44, issuer=MFG44,
            note="dupOLD; 'aramcoDURA® 150BS Revision nr: 2.0 Issue date: 05/08/2019 Location: Yanbu'; 9pp")
    elif p10 == 'd6d22407d7':  # DL2-15448 AramcoPRIMA 70 SDS 9pp (dupOLD)
        doc(D44, sha, 'SDS', SUP44, ['EXISTING:ARAMCO_LUBEREF_PRIMA_70'],
            'page-1 text: product name, SDS header', manufacturer=MFG44, issuer=MFG44,
            note="dupOLD; 'AramcoPRIMA® 70 Revision nr: 2.0 Issue date: 5/05/2021'; 9pp")
    elif p10 == '8ee1d6db59':  # DL2-12172 Luberef range TDS 1pp (dupOLD)
        doc(D44, sha, 'product data sheet (range TDS)', SUP44,
            ['EXISTING:ARAMCO_LUBEREF_PRIMA_70', 'EXISTING:ARAMCO_LUBEREF_PRIMA_110',
             'EXISTING:ARAMCO_LUBEREF_PRIMA_230', 'EXISTING:ARAMCO_LUBEREF_PRIMA_500'],
            'page text: multi-product range specifications table for Luberef GII base oils',
            manufacturer=MFG44, issuer=MFG44,
            note="dupOLD; 1pp; 'LUBEREF GII Product Specifications*'; range TDS covering aramcoPRIMA 70, 110, 230, 500 "
                 "with density, kV40, kV100 ranges, VI, PP, FP, Saturates, S content, Noack specifications; "
                 "top of table also shows Group I products (density 0.8500-0.867)")
    elif p10 == '35b596c91a':  # DL2-12173 Luberef GI specs 1pp (dupOLD)
        doc(D44, sha, 'product data sheet (range TDS)', SUP44,
            ['EXISTING:ARAMCO_LUBEREF_DURA_150_JEDDAH', 'EXISTING:ARAMCO_LUBEREF_DURA_500_JEDDAH'],
            'page text: Luberef I Jeddah Refinery guaranteed specifications for aramcoDURA 150® and 500®',
            manufacturer=MFG44, issuer=MFG44,
            note="dupOLD; 1pp; 'SPECIFICATIONS OF BASE OIL LUBEREF GI BASE OIL PRODUCTION GUARANTEED SPECIFICATION "
                 "Luberef I – Jeddah Refinery'; covers aramcoDURA 150® and aramcoDURA 500®")
    elif p10 == 'be2ed22afd':  # DL2-12180 Luberef Yanbu BS150 1pp
        doc(D44, sha, 'product data sheet (TDS/PDS)', SUP44, ['EXISTING:ARAMCO_LUBEREF_DURA_BS150_YANBU'],
            'page text: Luberef II Yanbu Refinery specifications for aramcoDURA® BS150',
            manufacturer=MFG44, issuer=MFG44,
            note="1pp; 'SPECIFICATIONS OF BASE OIL Luberef II – Yanbu Refinery... aramcoDURA® BS150'; "
                 "kV100 30/33 cSt, VI min 95, Sulfur max 1.3 wt%")
    elif p10 == 'd5c07d0388':  # DL2-15131 aramcoPRIMA multi-grade range TDS 1pp
        doc(D44, sha, 'product data sheet (range TDS)', SUP44,
            ['EXISTING:ARAMCO_LUBEREF_PRIMA_70', 'EXISTING:ARAMCO_LUBEREF_PRIMA_110',
             'EXISTING:ARAMCO_LUBEREF_PRIMA_230', 'EXISTING:ARAMCO_LUBEREF_PRIMA_500'],
            'page-1 text: Motiva Base Oils aramcoPRIMA range (60/100/150/500) typical properties',
            manufacturer=MFG44, issuer='Motiva Enterprises (Aramco/Shell JV)',
            note="'SPECIFICATIONS & TYPICAL PROPERTIES FOR MOTIVA BASE OILS'; "
                 "issued by Motiva Enterprises (Saudi Aramco / Shell JV); covers aramcoPRIMA 60, 100, 150, 500; "
                 "auto-classified as aramcoPRIMA 60 (title includes that grade); 1pp")
    elif p10 == '54f8e3d1f7':  # DL2-12296 NB051 Group II N70 1pp (Sama Lubricants issuer)
        doc(D44, sha, 'product data sheet (TDS/PDS)', 'Sama Lubricants', ['EXISTING:ARAMCO_LUBEREF_PRIMA_70'],
            'page-1 text: product name NB051, origin Saudi Aramco, Group II N70 typical properties',
            manufacturer=MFG44, issuer='Sama Lubricants',
            note="'Technical Data Sheet NB051 Base Oil Group II N70 Origin: Saudi Aramco Date: 13 Oct 2019'; "
                 "buyer code NB051 = aramcoPRIMA 70 (spec match: kV40 14.20 cSt, kV100 3.208 cSt, VI 83, PP -30°C, FP 176°C); "
                 "issued by Sama Lubricants (Technicalsales@samalubricants.com) as distributor of Saudi Aramco base oils; "
                 "1pp; mislabeled under Saudi Aramco/Luberef (issuer is Sama, not Saudi Aramco direct)")
    elif p10 == '9462acf566':  # DL2-15293 OLOA 59211 Afton formulation guide 6pp
        doc(D44, sha, 'formulation guide (Afton Chemical / Aramco co-branded)', 'Afton Chemical',
            [], 'page-1 text: formulation guide using OLOA 59211 (Afton package) + Aramco PRIMA base stock',
            relation='non_product', issuer='Afton Chemical',
            note="'Cover HDEO product line... OLOA® 59211 at 11.95 wt% ... Base Stock: Aramco PRIMA (Group II)'; "
                 "6pp; this is an Afton Chemical product data package / formulation guide for OLOA 59211 (Afton DI package), "
                 "not a Luberef base oil product sheet; "
                 "mislabeled under Saudi Aramco/Luberef; actual subject: Afton OLOA 59211")

write('s44_saudi_aramco.json', 'S44 Saudi Aramco / Luberef (identity)',
      '9 documents with provisional supplier Saudi Aramco / Luberef', PK44, D44)

# ===========================================================================
# S45 Plasmoil
# ===========================================================================
SUP45 = 'MicRos Lubrication Technology Ltd / Plasmoil'
MFG45 = 'MicRos Lubrication Technology Ltd'
U = 'unresolved'

D45, PK45 = {}, {}
prod(PK45, 'MICROS:PLASMOIL_BIO', 'Plasmoil Bio', SUP45, U,
     "printed: 'PLASMOIL BIO is a line of bio-additives with plasma induced thickness and polarity; "
     "PLASMOIL BIO combine the two antagonist properties of high polarity and high viscosity; honey-like products'; "
     "API Group V bio-based lubricant additive/base; material class: unresolved (Group V; additive_component or base stock component)")
prod(PK45, 'MICROS:PLASMOIL_MR_A', 'Plasmoil MR-A', SUP45, U,
     "printed: 'Plasmoil MR-A MSDS'; described together with MR-H and MR-B as "
     "'honey-like bio-compounded bases which combine antagonist properties like high dipolar moment, "
     "high viscosity, dispersion, physical adhesiveness and anti-oxidation effect'; "
     "API Group V bio-based lubricant additive/base; material class: unresolved")
prod(PK45, 'MICROS:PLASMOIL_MR_B', 'Plasmoil MR-B', SUP45, U,
     "printed: 'Plasmoil MR-B'; MSDS 1pp; described as bio-compounded base; material class: unresolved")
prod(PK45, 'MICROS:PLASMOIL_MR_H', 'Plasmoil MR-H', SUP45, U,
     "described together with MR-A and MR-B in DL2-15386; material class: unresolved; "
     "no separate product sheet in this batch — only the combined MR-H & A & B TDS")

for r in rows(lambda s: s == 'Plasmoil', 's45_plasmoil.json'):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '51cd661840':  # DL2-15188 Plasmoil Bio MSDS 5pp
        doc(D45, sha, 'SDS', SUP45, ['MICROS:PLASMOIL_BIO'],
            'page-1 text: product name, REACH format SDS', manufacturer=MFG45, issuer=MFG45,
            note="'Plasmoil Bio 1.2 Relevant identified uses... Plasmoil Bio: lubricating properties'; 5pp MSDS")
    elif p10 == '9f08f4cb18':  # DL2-15189 Plasmoil MR-B MSDS 1pp
        doc(D45, sha, 'SDS', SUP45, ['MICROS:PLASMOIL_MR_B'],
            'page-1 text: product name, relevant uses', manufacturer=MFG45, issuer=MFG45,
            note="'Plasmoil MR-B... Provides adhesive & protective lubricating film, dispersant'; 1pp MSDS")
    elif p10 == '97dc526e9e':  # DL2-15187 Plasmoil MR-A MSDS 6pp
        doc(D45, sha, 'SDS', SUP45, ['MICROS:PLASMOIL_MR_A'],
            'page-1 text: product name, REACH format SDS', manufacturer=MFG45, issuer=MFG45,
            note="'Plasmoil MR-A MSDS PLASMOIL MR-A According to Regulation (EC) No. 1907/2006'; 6pp")
    elif p10 == 'afd11ced3a':  # DL2-15190 PLASMOIL product overview brochure 4pp (x2)
        doc(D45, sha, 'product brochure (API Group V bio-additive range)', SUP45,
            ['MICROS:PLASMOIL_BIO', 'MICROS:PLASMOIL_MR_A', 'MICROS:PLASMOIL_MR_B', 'MICROS:PLASMOIL_MR_H'],
            'page-1 and page-2 text: company overview and Plasmoil product range description',
            manufacturer=MFG45, issuer=MFG45,
            note="x2 copies in archive; 4pp; 'PLASMOIL™... Belonging to API Group V category, PLASMOIL can serve as a "
                 "bases or an additive for a variety of lubricants, greases and fuel additives; "
                 "outstanding tribological properties by being powerful and multifunctional'; "
                 "covers all Plasmoil variants including MR-H, MR-A, MR-B, Bio")
    elif p10 == 'cdf13b0e5e':  # DL2-15385 Plasmoil Bio TDS 1pp
        doc(D45, sha, 'product data sheet (TDS/PDS)', SUP45, ['MICROS:PLASMOIL_BIO'],
            'page-1 text: product description and properties',
            manufacturer=MFG45, issuer=MFG45,
            note="'PLASMOIL BIO is a line of bio-additives with plasma induced thickness and polarity; "
                 "PLASMOIL BIO combine the two antagonist properties of high polarity and high viscosity'; 1pp TDS")
    elif p10 == 'b4574af00c':  # DL2-15386 Plasmoil MR-H & A & B combined TDS 1pp
        doc(D45, sha, 'product data sheet (TDS/PDS)', SUP45,
            ['MICROS:PLASMOIL_MR_H', 'MICROS:PLASMOIL_MR_A', 'MICROS:PLASMOIL_MR_B'],
            'page-1 text: MR-H & A & B combined description',
            manufacturer=MFG45, issuer=MFG45,
            note="'Plasmoil MR-H & A & B are honey-like bio-compounded bases which combine antagonist properties "
                 "like high dipolar moment, high viscosity, dispersion, physical adhesiveness and anti-oxidation effect'; "
                 "1pp TDS; covers three products together: MR-H, MR-A, MR-B")
    elif p10 == 'd8c4737304':  # DL2-15500 Plasmoil product range 1pp
        doc(D45, sha, 'product range reference', SUP45,
            ['MICROS:PLASMOIL_BIO', 'MICROS:PLASMOIL_MR_A', 'MICROS:PLASMOIL_MR_B', 'MICROS:PLASMOIL_MR_H'],
            'page-1 text: Plasmoil product range and technology description',
            manufacturer=MFG45, issuer=MFG45,
            note="'PLASMOIL® MicRos Lubrication Technology 2022-04-24; "
                 "Micros LT treats vegetable oils by electro-polarization; "
                 "bio-components become outstanding lubricity additives at 2.5-10% in a formulation'; 1pp; "
                 "describes all Plasmoil variants and their applications in lubricants, greases and fuels")
    elif p10 == '1ff4015fff':  # DL2-15593 Agilent Technologies letter 1pp
        doc(D45, sha, 'third-party letter (marketing)', 'Agilent Technologies', [],
            'page-1 text: Agilent marketing letter to MicRos Lubrication Technology about FTIR',
            relation='non_product', issuer='Agilent Technologies (China) Co., Ltd.',
            note="'Agilent Technologies (China) Co., Ltd. ... Mar. 27, 2025 Dear Micros Lubrication Technology, "
                 "FTIR is widely used in chemistry to identify unknown compounds...'; "
                 "Agilent marketing/sales letter about FTIR analytical instruments; "
                 "not a Plasmoil product document; mislabeled under Plasmoil supplier")
    elif p10 == '6dfe957b8d':  # DL2-15798 Plasmoil tech comments on concentration 2pp
        doc(D45, sha, 'product technical note', SUP45,
            ['MICROS:PLASMOIL_BIO', 'MICROS:PLASMOIL_MR_A', 'MICROS:PLASMOIL_MR_B', 'MICROS:PLASMOIL_MR_H'],
            'page-1 and page-2 text: technical comments on Plasmoil concentration effects in formulations',
            manufacturer=MFG45, issuer=MFG45,
            note="'Michel ROEGIERS, Ir. MicRos Lubrication Technology ltd Nov.2, 2021; "
                 "Technical comments on PLASMOIL concentrations; "
                 "NO MINIMUM concentrations; higher concentration = higher VI, dispersion, temperature stability, lubricity, thixotropy'; "
                 "2pp; authored by chief technical officer; covers all Plasmoil variants")

write('s45_plasmoil.json', 'S45 Plasmoil (identity)',
      '9 documents with provisional supplier Plasmoil', PK45, D45)

# ===========================================================================
# S46 Cristol
# ===========================================================================
SUP46 = 'Cristol Speciality Lubricant Chemicals'
MFG46 = SUP46
OWN46 = 's46_cristol.json'

D46, PK46 = {}, {}
prod(PK46, 'CRISTOL:EPR_3400', 'CRISTOL EPR-3400', SUP46, AC,
     "printed: 'CRISTOL EPR-3400 Antioxidant for Greases and Lubricating Oil formulations; "
     "ash-less, less volatile and non-corrosive'; additive_component (antioxidant)")
prod(PK46, 'CRISTOL:PMA_D_70', 'CRISTOL PMA D-70', SUP46, AC,
     "printed: 'CRISTOL PMA D-70 Dispersant type viscosity index improver; "
     "PMA based dispersant type VII which is used in the formulation of high quality lubricating oils; "
     "moderate shear stability and high VI improvement'; additive_component (VM, dispersant-type PMA)")
prod(PK46, 'CRISTOL:PPD_LX_250', 'CRISTOL PPD LX 250', SUP46, AC,
     "printed: 'CRISTOL PPD LX 250; Flow Improver for Automotive Lubricants; "
     "Cristol-PPD LX Series... CRISTOL-PPD LX 250 is recommended for use in multi grade engine oils and transmission fluids'; "
     "additive_component (PPD, pour point depressant)")
prod(PK46, 'CRISTOL:VII_400', 'CRISTOL VII-400', SUP46, AC,
     "printed: 'CRISTOL VII-400 is a PMA based Viscosity Index Improver; "
     "used to blend Hydraulic oils to provide moderate shear stability and retention of oil viscosity'; "
     "additive_component (VM, PMA-based, hydraulic oil application)")

for r in rows(lambda s: s == 'Cristol', OWN46):
    sha = r['sha256']
    p10 = sha[:10]

    if p10 == '8699857a64':  # DL2-13778 EPR-3400 TDS 1pp
        doc(D46, sha, 'product data sheet (TDS/PDS)', SUP46, ['CRISTOL:EPR_3400'],
            'page-1 text: product description and typical properties',
            manufacturer=MFG46, issuer=MFG46,
            note="1pp TDS; 'Fields of application: Antioxidant for Greases and Lubricating Oil formulations; "
                 "Product is ash-less, less volatile and non-corrosive'; Specific Gravity 0.980")
    elif p10 == '7167c81a27':  # DL2-13725 PMA D-70 SDS 6pp
        doc(D46, sha, 'SDS', SUP46, ['CRISTOL:PMA_D_70'],
            'page-1 text: SDS with product name and version', manufacturer=MFG46, issuer=MFG46,
            note="'CRISTOL PMA D-70 Version: 1.2 Date: 26/03/2019'; 6pp GHS SDS")
    elif p10 == 'a6630a943c':  # DL2-13724 PMA D-70 TDS 2pp
        doc(D46, sha, 'product data sheet (TDS/PDS)', SUP46, ['CRISTOL:PMA_D_70'],
            'page-1 text: product description and typical properties',
            manufacturer=MFG46, issuer=MFG46,
            note="'CRISTOL TM PMA D-70 Dispersant type viscosity index improver'; 2pp TDS with typical properties table")
    elif p10 == 'c9071fa271':  # DL2-13666 PPD LX 250 SDS 6pp
        doc(D46, sha, 'SDS', SUP46, ['CRISTOL:PPD_LX_250'],
            'page-1 text: SDS with product name and version', manufacturer=MFG46, issuer=MFG46,
            note="'CRISTOL PPD LX 250 Version: 1.0 Date: 07/09/2020'; 6pp GHS SDS")
    elif p10 == 'f5e80db8dd':  # DL2-13667 PPD LX series brochure 4pp
        doc(D46, sha, 'product brochure', SUP46, ['CRISTOL:PPD_LX_250'],
            'page-1 text: PPD LX series description',
            manufacturer=MFG46, issuer=MFG46,
            note="'Flow Improver for Automotive Lubricants CRISTOL-PPD LX SERIES™'; 4pp; "
                 "covers PPD LX series in general; PPD LX 250 specifically named; "
                 "PMA pour point depressant for engine oils and transmission fluids")
    elif p10 == 'e60e593428':  # DL2-15288 PPD LX 250 brochure 4pp (x2)
        doc(D46, sha, 'product brochure', SUP46, ['CRISTOL:PPD_LX_250'],
            'page-1 text: PPD LX 250 product details',
            manufacturer=MFG46, issuer=MFG46,
            note="x2 copies in archive; 'Flow Improver for Automotive Lubricants CRISTOL-PPD LX 250™'; 4pp brochure")
    elif p10 == '79cd58b019':  # DL2-13722 VII-400 TDS 2pp
        doc(D46, sha, 'product data sheet (TDS/PDS)', SUP46, ['CRISTOL:VII_400'],
            'page-1 text: product description and typical properties',
            manufacturer=MFG46, issuer=MFG46,
            note="'CRISTOL TM VII-400 PMA Based Viscosity Index Improver'; 2pp TDS")
    elif p10 == '2b4c7987e6':  # DL2-13723 VII-400 SDS 5pp
        doc(D46, sha, 'SDS', SUP46, ['CRISTOL:VII_400'],
            'page-1 text: SDS with product name', manufacturer=MFG46, issuer=MFG46,
            note="'CRISTOL VII-400 Version: 1.2 Date: 08/05/2018'; 5pp GHS SDS")

write(OWN46, 'S46 Cristol (identity)', '8 documents with provisional supplier Cristol', PK46, D46)
