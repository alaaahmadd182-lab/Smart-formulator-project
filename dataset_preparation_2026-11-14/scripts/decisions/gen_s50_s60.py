"""Supplier batches S50–S60: remaining small labelled suppliers.

S50 Formosa Petrochemical (5 docs, 5 products):
  M 25 SSI OCP solid VII (DL2-11416 TDS) → new_candidate additive_component (VM, OCP);
  LUBRAN VI-870 TDS from Toho Chemical Industry (DL2-11661) — mislabeled under Formosa
    because page 2 uses Formosa base oils in performance testing → new_candidate
    additive_component (VM, PMA) under Toho Chemical;
  Formosa Petrochemical 150N GII CoA (DL2-14076) → new_candidate base_oil (Group II);
  Formosa Petrochemical 500N GII CoA (DL2-14080) → new_candidate base_oil (Group II);
  P8401 PMA PPD from Ocean Chemical Technology (DL2-15432) — mislabeled under Formosa
    → new_candidate additive_component (PPD) under Ocean Chemical Technology.
  Kemipex DL2-11417 (S57 below) is the MSDS for the same M 25 SSI product.

S51 Hyrax Oil (5 docs, 2 products):
  Hypertrans: transformer oil (naphthenic, IEC 60296) → out_of_template for all 4 docs
  (DL2-12262 3pp TDS, DL2-13942 11pp SDS, DL2-14995 2pp TDS, DL2-15803 10pp SDS).
  Naprex L-40 (DL2-13142 1pp): "naphthenic process oil"; kV40 4.28 cSt, PP -60°C,
  FP 120°C, density 0.8778 at 15°C; "meets US EPA Final Rule"; material class: unresolved
  (naphthenic process oil — possibly Group V; template applicability to be confirmed).

S52 PETRONAS (5 docs, 5 products): all EXISTING production records.
  ETRO 6+ SDS (DL2-14610), EQUINAS 4 SDS (DL2-15184), EQUINAS 6 SDS (DL2-15185),
  EQUINAS 8 TDS (DL2-15279); CoA for 'Base Oil GIII-6Cst (Etro 6)' (DL2-15356) —
  'Etro 6' without '+' suffix → linked to PETRONAS_ETRO_6 not PETRONAS_ETRO_6_PLUS;
  ETRO 6 and ETRO 6+ are separately registered production records.

S53 Petro-Canada (4 docs, 3 products):
  VHVI 4 benchmarking brochure (DL2-11261) → EXISTING:PETRO_CANADA_PURITY_VHVI_4;
  PURITY L50 TDS (DL2-13351, kV40 5.5 cSt, PP -12°C, FP 152°C)
    → EXISTING:PETRO_CANADA_PURITY_L50;
  SUNISO 5GS SDS 12pp (DL2-15709) and Suniso GS brochure 2pp (DL2-15710)
    → out_of_template (refrigeration compressor lubricant);
    Petro-Canada/HF Sinclair brand.

S54 Ergon (3 docs):
  HY 40 naphthenic base oil 1pp spec sheet (DL2-13168) → EXISTING:ERGON_HY_40 (product
    name 'HY 40' printed in footer 'HY 40 is a product of Ergon Refining, Inc. May 10, 2018');
  DL2-13279 (1pp): Ergon naphthenic/mineral base oil spec; product name not in text layer;
    Saybolt 34-44 SUS at 100°F, kV40 2.4-5.2 cSt, density 0.8124 at 15.6°C, PP -14°C,
    FP 124°C (COC) → unresolved_identity (product name needed);
  DL2-13346 (1pp): Ergon naphthenic base oil spec; product name not in text layer;
    Saybolt 60-75 SUS at 100°F, kV40 9.6-13.3 cSt, density 0.8552, VI 60-81, VGC 0.817,
    MW 312 → unresolved_identity.

S55 Bapco (2 docs, 2 unresolved_identity):
  Both DL2-14114 and DL2-14119 are Bapco Laboratory Report / Test Certificate
  (Form BP0209 04/16). Property list consistent with a base oil CoA (kV100, kV40, VI,
  Noack, CCS, Saturates, Sulfur, UV wavelengths 280-350nm — food-grade screening).
  Product names and batch data not legible from text layer → unresolved_identity.

S56 Huntsman (2 docs, 1 product):
  TEPA (tetraethylenepentamine) technical bulletin (DL2-15232 2pp) and SDS
  (DL2-15247 133pp). Applications: 'Asphalt additives, Mineral processing aids,
  Corrosion inhibitors, Polyamide resins, Epoxy curing agents, Surfactants' — NO
  lubricant application stated → out_of_template (industrial chemical/polyamide precursor).

S57 Kemipex (1 doc):
  DL2-11417: M 25 SSI Viscosity Index Improver MSDS (5pp). Supplier section: Kemipex FZE
  (Dubai) → Kemipex is the distributor. Same product as Formosa TDS (DL2-11416) → linked
  to FORMOSA:M_25_SSI; issuer = Kemipex FZE; manufacturer = Formosa Petrochemical.

S58 Turkmenbashy refinery (1 doc):
  DL2-11239: 1pp multi-grade spec for Turkmenbashy base oils SN-80/180/350/600/1200.
  Standard TŞ 05766698-60-2006. kV100: 2.5-3.5, 4.5-6.0, 8.0-9.5, 11.5-13.5, 18.0-23.0
  cSt; VI ≥95 all grades; density @20°C 870-905 kg/m³; Sulfur max 0.03%. Five new_candidate
  base_oil products.

S59 TotalEnergies (1 doc):
  DL2-15095: JARYTHERM DBT 1pp TDS. 'Synthetic heat transfer fluid, made from a blend of
  dibenzyltoluene isomers. Operating from 0°C to +350°C.' → out_of_template (heat transfer
  fluid — same chemical class as FRAGOLTHERM HT from FRAGOL).

S60 Tanee Chemical / Minglan Chemical / Shenyang Great Wall (3 docs, 3 products):
  DL2-15242 (Tanee Chem 1pp): TE-598 Dialkyl Diphenylamine → new_candidate
    additive_component (antioxidant, DPA/alkylated diphenylamine).
  DL2-15278 (Minglan Chemical 1pp): '151 T106D Super High TBN Synthetic Calcium Sulfonate'
    → new_candidate additive_component (detergent, super-high-TBN calcium sulfonate).
  DL2-15800 (Shenyang Great Wall 35pp): Shenyang Great Wall finished lubricant product
    manual covering engine oils, gear oils, industrial oils, additive products — this is a
    finished lubricant manufacturer's catalog, not a raw-material source document → out_of_scope.

Writes decisions/s50_formosa.json, s51_hyrax.json, s52_petronas.json, s53_petro_canada.json,
s54_ergon.json, s55_bapco.json, s56_huntsman.json, s57_kemipex.json, s58_turkmenbashy.json,
s59_total.json, s60_micro.json."""
from dec_common import rows, page_text, top, doc, prod, write

# ===========================================================================
# S50 Formosa Petrochemical
# ===========================================================================
SUP50 = 'Formosa Petrochemical'
MFG50 = 'Formosa Petrochemical Corporation'
AC = 'additive_component'
B = 'base_oil'

D50, PK50 = {}, {}
prod(PK50, 'FORMOSA:M_25_SSI', 'M 25 SSI', SUP50, AC,
     "printed: 'M 25 SSI is a shear stable amorphous olefin copolymer intended for use as a "
     "Viscosity Index Improver when formulating multi grade crankcase and industrial oils; "
     "High shear stability, Excellent low temperature properties'; solid in bale form 25 kg; "
     "additive_component (VM, OCP, shear-stable); manufacturer Formosa Petrochemical; "
     "MSDS in DL2-11417 (s57_kemipex) with Kemipex FZE as distributor issuer")
prod(PK50, 'TOHO_CHEM:LUBRAN_VI_870', 'LUBRAN VI-870', 'Toho Chemical Industry', AC,
     "printed: 'LUBRAN VI-870 is a polymethacrylate (PMA) type viscosity index improver; "
     "excellent viscosity properties at low temperature with excellent shear stability for "
     "gear oil and hydraulic fluids; Kinematic Viscosity 1500 mm2/s at 100°C'; "
     "mislabeled under Formosa Petrochemical — document is a Toho Chemical Industry "
     "(Tokyo, Japan) product TDS; page 2 uses Formosa, Hyundai, Shell base oils in "
     "performance testing (not a Formosa document); "
     "additive_component (VM, PMA, dispersant-type or non-dispersant TBD)")
prod(PK50, 'FORMOSA:BASE_OIL_GII_150N', 'Formosa Petrochemical Group II 150N', SUP50, B,
     "CoA text: 'FORMOSA PETROCHEMCIAL CORPORATION BASE OIL 150 N GII' from Mailiao, Taiwan; "
     "kV100 5.0-5.6 cSt, VI ≥105, PP ≤-15°C, FP ≥210°C, Sulfur ≤10 ppm; "
     "Group II base oil, medium grade (~SN 150); new_candidate base_oil")
prod(PK50, 'FORMOSA:BASE_OIL_GII_500N', 'Formosa Petrochemical Group II 500N', SUP50, B,
     "CoA text: 'FORMOSA PETROCHEMICAL CORPORATION BASE OIL 500 N G II' from Mailiao, Taiwan; "
     "kV100 10-12 cSt, VI ≥95, PP ≤-12°C, FP ≥230°C, Sulfur ≤10 ppm; "
     "Group II base oil, heavy grade (~SN 500); new_candidate base_oil")
prod(PK50, 'OCEAN_CHEM:P8401_PPD', 'P8401 PMA PPD', 'Ocean Chemical Technology', AC,
     "printed: 'P8401 Polyalkyl methacrylate PPD... effective polyalkyl methacrylate pour "
     "point depressant... API Group II and III base oils; "
     "Viscosity at 100°C 260 mm2/s, Density 900 kg/m3, FP 160°C'; "
     "mislabeled under Formosa Petrochemical — document is Ocean Chemical Technology Co., Ltd "
     "(Yiwu, Zhejiang, China); additive_component (PPD, PMA)")

for r in rows(lambda s: s == 'Formosa Petrochemical', 's50_formosa.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'dc3ea00a33':  # DL2-11416 M 25 SSI TDS 1pp
        doc(D50, sha, 'product data sheet (TDS/PDS)', SUP50, ['FORMOSA:M_25_SSI'],
            'page-1 text: product description, key benefits, typical properties',
            manufacturer=MFG50, issuer=MFG50,
            note="1pp TDS; 'M 25 SSI Viscosity Index Improver for Lubricant Application'; "
                 "OCP (amorphous olefin copolymer), shear stable, solid bale 25 kg; "
                 "MSDS for same product in s57_kemipex (Kemipex FZE as distributor issuer)")
    elif p10 == 'b1a14b1f12':  # DL2-11661 Toho LUBRAN VI-870 TDS 2pp
        doc(D50, sha, 'product data sheet (TDS/PDS)', 'Toho Chemical Industry', ['TOHO_CHEM:LUBRAN_VI_870'],
            'page-1 text: product description, typical properties; page 2: performance data with Formosa base oils',
            manufacturer='Toho Chemical Industry Co., Ltd.', issuer='Toho Chemical Industry Co., Ltd.',
            note="2pp; mislabeled under Formosa Petrochemical in auto-classifier; "
                 "'TOHO CHEMICAL INDUSTRY CO., LTD., Tokyo, Japan (03)5550-3728'; "
                 "document date: 2016-6-10; 'LUBRAN VI-870 PMA type viscosity index improver'; "
                 "page 2 performance table uses Formosa (150N/500N GrII), Hyundai, Shell base oils — "
                 "this is likely why the classifier attributed to Formosa")
    elif p10 == 'f992acdbaf':  # DL2-14076 150N GII CoA 1pp
        doc(D50, sha, 'certificate of quality (CoA)', SUP50, ['FORMOSA:BASE_OIL_GII_150N'],
            'full page content: CoA issued by independent surveyors for vessel MT Southern Dragon',
            manufacturer=MFG50, issuer='Independent Surveyors (Mailiao)',
            note="1pp; W.O.NO. OGC-2080092; 'FORMOSA PETROCHEMCIAL CORPORATION BASE OIL 150 N GII'; "
                 "vessel MT SOUTHERN DRAGON V.2001; port Mailiao, Taiwan; B/L date 17 Jan 2020; "
                 "spec: kV100 5.0-5.6 cSt, VI 105 min, PP -15°C max, FP 210°C min, S 10 ppm max, Color 0.5 max")
    elif p10 == '7c0c04f883':  # DL2-14080 500N GII CoA 1pp
        doc(D50, sha, 'certificate of quality (CoA)', SUP50, ['FORMOSA:BASE_OIL_GII_500N'],
            'full page content: CoA issued by independent surveyors for vessel MT Southern Dragon',
            manufacturer=MFG50, issuer='Independent Surveyors (Mailiao)',
            note="1pp; W.O.NO. OGC-2080093; 'FORMOSA PETROCHEMICAL CORPORATION BASE OIL 500 N G II'; "
                 "vessel MT SOUTHERN DRAGON V.2001; port Mailiao, Taiwan; B/L date 18 Jan 2020; "
                 "spec: kV100 10-12 cSt, VI 95 min, PP -12°C max, FP 230°C min, S 10 ppm max, Color 0.5 max")
    elif p10 == '0532ef083f':  # DL2-15432 P8401 PPD TDS 2pp
        doc(D50, sha, 'product data sheet (TDS/PDS)', 'Ocean Chemical Technology', ['OCEAN_CHEM:P8401_PPD'],
            'page-1 text: product name, description, typical properties',
            manufacturer='Ocean Chemical Technology Co., Ltd.', issuer='Ocean Chemical Technology Co., Ltd.',
            note="2pp; mislabeled under Formosa Petrochemical; "
                 "'OCEAN CHEMICAL TECHNOLOGY CO.,LTD, No.844 Guomao, North Chouzhou Road, Yiwu, Zhejiang, China'; "
                 "'P8401 Polyalkyl methacrylate PPD... API Group II and III base oils'; "
                 "Viscosity@100°C 260 cSt, Density 900 kg/m³ at 20°C, FP 160°C (ASTM D92), Color 0.5 (ASTM D1500)")

write('s50_formosa.json', 'S50 Formosa Petrochemical (identity)',
      '5 documents with provisional supplier Formosa Petrochemical', PK50, D50)

# ===========================================================================
# S51 Hyrax Oil
# ===========================================================================
SUP51 = 'Hyrax Oil'
MFG51 = 'Hyrax Oil Sdn Bhd'
OWT51 = 'out_of_template (transformer / electrical insulating oil)'

D51, PK51 = {}, {}
prod(PK51, 'HYRAX:HYPERTRANS', 'Hyrax Hypertrans', SUP51, OWT51,
     "printed: 'Hyrax Hypertrans transformer oil is a premium uninhibited mineral electrical "
     "insulating oil made from severely hydrotreated wax-free naphthenic oil; "
     "good as a dielectric and coolant; IEC 60296 conformant'; "
     "out_of_template (transformer/electrical insulating oil — not a lubricant base oil or component)")
prod(PK51, 'HYRAX:NAPREX_L40', 'Hyrax Naprex L-40', SUP51,
     'unresolved (naphthenic process oil — base_oil Group V or out_of_template)',
     "printed: 'Hyrax Naprex L-40 - Process Oils; density 0.8778 at 15°C; FP >120°C; "
     "PP -60°C; kV40 4.28 cSt; kV100 1.53 cSt; meets US EPA Final Rule'; "
     "naphthenic process oil / rubber process oil; API Group V (naphthenic); "
     "material class: unresolved (process oil — template applicability to be confirmed)")

for r in rows(lambda s: s == 'Hyrax Oil', 's51_hyrax.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'bd50ad82d6':  # DL2-12262 Hypertrans TDS 3pp
        doc(D51, sha, 'product data sheet (TDS/PDS)', SUP51, ['HYRAX:HYPERTRANS'],
            'page-1 text: product description, features and benefits',
            manufacturer=MFG51, issuer=MFG51,
            note="3pp; Rev: 23/08/17; 'Hyrax Hypertrans transformer oil; premium uninhibited "
                 "mineral electrical insulating oil from severely hydrotreated wax-free naphthenic oil; "
                 "IEC 60296 conformant'; Kuala Lumpur, Malaysia")
    elif p10 == '464899c796':  # DL2-13142 Naprex L-40 TDS 1pp
        doc(D51, sha, 'product data sheet (TDS/PDS)', SUP51, ['HYRAX:NAPREX_L40'],
            'full page content: typical properties for Naprex L-40',
            manufacturer=MFG51, issuer=MFG51,
            note="1pp; Rev:18/04/12; 'Hyrax Naprex L-40 - Process Oils'; "
                 "kV40 4.28 cSt, kV100 1.53 cSt, density 0.8778 at 15°C, PP -60°C, FP >120°C; "
                 "described as process oil meeting US EPA Final Rule (rubber-compounding process oil)")
    elif p10 == '3c4e9de6c0':  # DL2-13942 Hypertrans SDS 11pp
        doc(D51, sha, 'SDS', SUP51, ['HYRAX:HYPERTRANS'],
            'page-1: SDS header for Hyrax Hypertrans, IEC 60296',
            manufacturer=MFG51, issuer=MFG51,
            note="11pp SDS; 'PRODUCT NAME: Hyrax Hypertrans; IEC 60296 conformant'; "
                 "transformer oil / electrical insulating oil")
    elif p10 == '302fe0f134':  # DL2-14995 Hypertrans TDS 2pp
        doc(D51, sha, 'product data sheet (TDS/PDS)', SUP51, ['HYRAX:HYPERTRANS'],
            'page-1 text: product description',
            manufacturer=MFG51, issuer=MFG51,
            note="2pp; Rev: 15/09/21; newer edition of Hypertrans TDS; "
                 "same description as DL2-12262 (bd50ad82d6) with updated revision date")
    elif p10 == '0f544584e2':  # DL2-15803 Hypertrans SDS 10pp
        doc(D51, sha, 'SDS', SUP51, ['HYRAX:HYPERTRANS'],
            'page-1: SDS header for Hyrax Hypertrans, IEC 60296',
            manufacturer=MFG51, issuer=MFG51,
            note="10pp SDS; 'PRODUCT NAME: Hyrax Hypertrans; IEC 60296'; "
                 "see also DL2-13942 (3c4e9de6c0); possibly different revision")

write('s51_hyrax.json', 'S51 Hyrax Oil (identity)',
      '5 documents with provisional supplier Hyrax Oil', PK51, D51)

# ===========================================================================
# S52 PETRONAS
# ===========================================================================
SUP52 = 'PETRONAS'
MFG52 = 'PETRONAS Lubricants International / Malaysian Refining Company Sdn Bhd'
B52 = 'base_oil'

EXISTING52 = {
    'EXISTING:PETRONAS_ETRO_6_PLUS': ('PETRONAS_ETRO_6_PLUS', 'ETRO 6+'),
    'EXISTING:PETRONAS_ETRO_6':      ('PETRONAS_ETRO_6',      'ETRO 6'),
    'EXISTING:PETRONAS_EQUINAS_4':   ('PETRONAS_EQUINAS_4',   'EQUINAS 4'),
    'EXISTING:PETRONAS_EQUINAS_6':   ('PETRONAS_EQUINAS_6',   'EQUINAS 6'),
    'EXISTING:PETRONAS_EQUINAS_8':   ('PETRONAS_EQUINAS_8',   'EQUINAS 8'),
}

D52, PK52 = {}, {}
for key, (rec, name) in EXISTING52.items():
    prod(PK52, key, name, SUP52, B52,
         'printed product name on the documents linked in this batch', existing=rec)

for r in rows(lambda s: s == 'PETRONAS', 's52_petronas.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == '1d4994a6c7':  # DL2-14610 ETRO 6+ SDS 9pp
        doc(D52, sha, 'SDS', SUP52, ['EXISTING:PETRONAS_ETRO_6_PLUS'],
            'section 1: product name ETRO 6+, manufacturer Malaysian Refining Company, CAS 64742-54-7',
            manufacturer='Malaysian Refining Company Sdn Bhd', issuer='Malaysian Refining Company Sdn Bhd',
            note="9pp; 'ETRO 6+ Version 1.2 Release Date: 24.03.2020'; "
                 "manufactured by Malaysian Refining Company Sdn Bhd (MRCSB), Sungai Udang, Melaka; "
                 "'Recommended use: Base oil for Automotive Engine Oil'; "
                 "CAS 64742-54-7, REACH 01-2119484627-25-XXXX; Group III+ 6cSt designation")
    elif p10 == 'bf1276e393':  # DL2-15184 EQUINAS 4 SDS 10pp
        doc(D52, sha, 'SDS', SUP52, ['EXISTING:PETRONAS_EQUINAS_4'],
            'section 1: product name EQUINAS 4, PETRONAS Lubricants International',
            manufacturer=MFG52, issuer='PETRONAS Lubricants International',
            note="10pp; 'EQUINAS 4 Version 1.0 Release Date: 21.10.2021'; "
                 "CAS 64742-54-7; 'Lubricant base oil'; PETRONAS LUBRICANTS INTERNATIONAL, "
                 "Level 26 Integra Tower, Kuala Lumpur")
    elif p10 == 'c4612ea4e5':  # DL2-15185 EQUINAS 6 SDS 9pp
        doc(D52, sha, 'SDS', SUP52, ['EXISTING:PETRONAS_EQUINAS_6'],
            'section 1: product name EQUINAS 6, PETRONAS Lubricants International',
            manufacturer=MFG52, issuer='PETRONAS Lubricants International',
            note="9pp; 'EQUINAS 6 Version 1.0 Release Date: 21.10.2021'; same issuer as DL2-15184")
    elif p10 == 'b1fc67e8be':  # DL2-15279 EQUINAS 8 TDS 1pp
        doc(D52, sha, 'product data sheet (TDS/PDS)', SUP52, ['EXISTING:PETRONAS_EQUINAS_8'],
            'full page content: EQUINAS 8 product data with typical properties',
            manufacturer=MFG52, issuer='PETRONAS Lubricants International',
            note="1pp; 'EQUINAS 8 | High Quality Group III Base Oil'; "
                 "typical properties table for Group III 8cSt")
    elif p10 == 'a57e42fd17':  # DL2-15356 Etro 6 CoA 1pp
        doc(D52, sha, 'certificate of analysis (CoA)', SUP52, ['EXISTING:PETRONAS_ETRO_6'],
            'full page content: CoA for GIII-6Cst base oil named Etro 6',
            manufacturer='Malaysian Refining Company Sdn Bhd', issuer='Malaysian Refining Company Sdn Bhd',
            note="1pp; 'Base Oil GIII-6Cst (Etro 6) Date: Oct-2023'; "
                 "kV40 34.35 cSt, kV100 6.158 cSt, VI 128, PP -21°C, FP 246°C, Noack 6.8 wt%, "
                 "S 3 ppm, Saturates 99.7 wt%; "
                 "product name 'Etro 6' (without '+') → linked to PETRONAS_ETRO_6; "
                 "ETRO 6 and ETRO 6+ are separately registered production records")

write('s52_petronas.json', 'S52 PETRONAS (identity)',
      '5 documents with provisional supplier PETRONAS', PK52, D52)

# ===========================================================================
# S53 Petro-Canada
# ===========================================================================
SUP53 = 'Petro-Canada'
MFG53 = 'Petro-Canada Lubricants Inc. (HF Sinclair brand)'
OWT53 = 'out_of_template (refrigeration compressor lubricant)'

D53, PK53 = {}, {}
for key, rec, name, notes_text in [
    ('EXISTING:PETRO_CANADA_PURITY_VHVI_4', 'PETRO_CANADA_PURITY_VHVI_4', 'PURITY VHVI 4',
     "product name from benchmarking document title 'Benchmarking Results VHVI 4'; "
     "VHVI = Very High Viscosity Index; Group III+ 4 cSt base oil; "
     "'Alternative to more expensive PAOs/GP III+ in many high performance lubricant applications'"),
    ('EXISTING:PETRO_CANADA_PURITY_L50', 'PETRO_CANADA_PURITY_L50', 'PURITY L50',
     "product name from TDS footer 'Product Data Sheet - PURITY L50 BASE OIL'; "
     "kV40 5.5 cSt, kV100 1.78 cSt, PP -12°C, FP 152°C (COC)"),
]:
    prod(PK53, key, name, SUP53, 'base_oil',
         notes_text, existing=rec)
prod(PK53, 'PETRO_CANADA:SUNISO_GS', 'Suniso GS (5GS)', SUP53, OWT53,
     "printed: 'SUNISO 5GS Refrigeration Compressor Lubricant'; "
     "'Petro-Canada Lubricants is a HF Sinclair brand'; "
     "Internet: www.petrocanadalubricants.com/sds; "
     "refrigeration compressor lubricant → out_of_template")

for r in rows(lambda s: s == 'Petro-Canada', 's53_petro_canada.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == '10fde6778e':  # DL2-11261 VHVI 4 benchmarking brochure 2pp
        doc(D53, sha, 'product brochure (benchmarking)', SUP53, ['EXISTING:PETRO_CANADA_PURITY_VHVI_4'],
            'page-1 and page-2 content: Noack benchmarking results and product features',
            manufacturer=MFG53, issuer=MFG53,
            note="2pp; 'Benchmarking Results VHVI 4 Comp A B C D'; "
                 "Noack values: VHVI 4 = 12.65%, vs Comp A/B/C/D = 14-16%; "
                 "features: 0W-16 positioning, premium HTHS motor oils, PAO alternative")
    elif p10 == '04b526e8d4':  # DL2-13351 PURITY L50 TDS 1pp
        doc(D53, sha, 'product data sheet (TDS/PDS)', SUP53, ['EXISTING:PETRO_CANADA_PURITY_L50'],
            'full page content: PURITY L50 typical properties',
            manufacturer=MFG53, issuer=MFG53,
            note="1pp; 'Product Data Sheet - PURITY L50 BASE OIL'; kV40 4.5-6.5 cSt, typical 5.5; "
                 "kV100 Report (1.78 cSt typical); PP -12°C (max -3°C); FP COC 152°C (min 140°C); "
                 "Density 0.853 kg/L at 15°C; Color <0.5 ASTM")
    elif p10 == '975453076b':  # DL2-15709 SUNISO 5GS SDS 12pp
        doc(D53, sha, 'SDS', SUP53, ['PETRO_CANADA:SUNISO_GS'],
            'section 1: product name SUNISO 5GS, refrigeration compressor lubricant',
            manufacturer=MFG53, issuer=MFG53,
            note="12pp REACH SDS; 'SUNISO TM/MC 5GS Version 3.1 Revision Date 2025/04/17'; "
                 "product codes: SNGS5C16, SNGS5P20, SNGS5DRM; "
                 "'Refrigeration Compressor Lubricant'; Petro-Canada Lubricants (HF Sinclair brand)")
    elif p10 == 'ef7b2cd25a':  # DL2-15710 Suniso GS brochure 2pp
        doc(D53, sha, 'product brochure', SUP53, ['PETRO_CANADA:SUNISO_GS'],
            'page-1 and page-2 content: Suniso GS features and application description',
            manufacturer=MFG53, issuer=MFG53,
            note="2pp; 'Suniso GS WORLD-LEADING REFRIGERATION LUBRICANTS'; "
                 "features: low wax/PP, high dielectric strength, chemical stability with refrigerant; "
                 "covers entire Suniso GS series; premium refrigeration compressor lubricant")

write('s53_petro_canada.json', 'S53 Petro-Canada (identity)',
      '4 documents with provisional supplier Petro-Canada', PK53, D53)

# ===========================================================================
# S54 Ergon
# ===========================================================================
SUP54 = 'Ergon'
MFG54 = 'Ergon Refining, Inc.'
B54 = 'base_oil'

D54, PK54 = {}, {}
prod(PK54, 'EXISTING:ERGON_HY_40', 'HY 40', SUP54, B54,
     "product name confirmed in document footer: 'HY 40 is a product of Ergon Refining, Inc. May 10, 2018'",
     existing='ERGON_HY_40')
prod(PK54, 'ERGON:UNKNOWN_SPEC_DL2_13279', 'Ergon naphthenic/mineral oil (DL2-13279, name unknown)', SUP54,
     'unresolved',
     "document is an Ergon Refining base oil spec sheet; product name not legible from text layer; "
     "properties: Saybolt 34-44 SUS at 100°F, kV40 2.4-5.2 cSt (typical 3.2), kV100 1.3 cSt, "
     "API Gravity 42.5, density 0.8124 at 15.6°C, PP -14°C, FP 124°C (COC) / 115°C (PMCC), "
     "Water PASS, Appearance PASS, Acid Number max 0.05, Aniline Point (D611) listed; "
     "density 0.8124 is notably lower than HY 40 (0.8618) despite similar Saybolt range → "
     "likely a different grade or product line; "
     "next_action: identify product name from physical document or Ergon catalog",
     status='unresolved_identity')
prod(PK54, 'ERGON:UNKNOWN_SPEC_DL2_13346', 'Ergon naphthenic oil (DL2-13346, name unknown)', SUP54,
     'unresolved',
     "document is an Ergon Refining naphthenic base oil spec sheet; product name not legible; "
     "properties: Saybolt 60-75 SUS at 100°F, kV40 9.6-13.3 cSt (typical 11.8), kV100 2.9 cSt, "
     "density 0.8552 at 15.6°C (Specific Gravity 0.8559), VI 60-81, VGC 0.817, MW 312, "
     "PP -17°C, FP 187°C (COC); "
     "VGC 0.817 and VI 60-81 confirm naphthenic character; Saybolt 60-75 SUS → medium naphthenic; "
     "possibly ERGON_HYGOLD_60 or similar — not confirmable without product name in text layer; "
     "next_action: identify product name from physical document or Ergon catalog",
     status='unresolved_identity')

for r in rows(lambda s: s == 'Ergon', 's54_ergon.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'b36bfbe9ef':  # DL2-13168 HY 40 1pp
        doc(D54, sha, 'product data sheet (TDS/PDS)', SUP54, ['EXISTING:ERGON_HY_40'],
            'full page content: HY 40 spec sheet with typical values',
            manufacturer=MFG54, issuer=MFG54,
            note="1pp; product name confirmed in footer: 'HY 40 is a product of Ergon Refining, Inc. May 10, 2018 "
                 "HY 40 Naphthenic In...'; Saybolt 30-40 SUS at 100°F, kV40 3.0 cSt, kV100 1.2 cSt, "
                 "density 0.8618, PP -88°C, FP 109°C (COC)")
    elif p10 == '09571a3ded':  # DL2-13279 unknown naphthenic 1pp
        doc(D54, sha, 'product data sheet (TDS/PDS)', SUP54, ['ERGON:UNKNOWN_SPEC_DL2_13279'],
            'full page content: spec table; product name not in text layer',
            manufacturer=MFG54, issuer=MFG54,
            relation='unresolved_identity',
            note="1pp; Ergon Refining spec sheet format; product name not in text layer; "
                 "Saybolt 34-44 SUS at 100°F, kV40 2.4-5.2 cSt, density 0.8124 at 15.6°C, "
                 "PP -14°C, FP 124°C, Aniline Point test listed (D611); "
                 "density notably lower than HY 40 → different product",
            next_action='identify product name from physical document or Ergon catalog')
    elif p10 == 'c8ce093918':  # DL2-13346 unknown naphthenic 1pp
        doc(D54, sha, 'product data sheet (TDS/PDS)', SUP54, ['ERGON:UNKNOWN_SPEC_DL2_13346'],
            'full page content: spec table; product name not in text layer',
            manufacturer=MFG54, issuer=MFG54,
            relation='unresolved_identity',
            note="1pp; Ergon Refining naphthenic base oil spec; product name not in text layer; "
                 "Saybolt 60-75 SUS at 100°F, kV40 9.6-13.3 cSt, density 0.8552, VI 60-81, "
                 "VGC 0.817, MW 312, PP -17°C, FP 187°C; "
                 "viscosity/density profile matches medium naphthenic oil grade",
            next_action='identify product name; possibly ERGON_HYGOLD_60 or similar')

write('s54_ergon.json', 'S54 Ergon (identity)',
      '3 documents with provisional supplier Ergon', PK54, D54)

# ===========================================================================
# S55 Bapco
# ===========================================================================
SUP55 = 'Bapco'
MFG55 = 'Bahrain Petroleum Company (Bapco)'
D55, PK55 = {}, {}
for key, dl2 in [
    ('BAPCO:UNKNOWN_COA_DL2_14114', 'DL2-14114'),
    ('BAPCO:UNKNOWN_COA_DL2_14119', 'DL2-14119'),
]:
    prod(PK55, key, f'Bapco base oil CoA ({dl2}, grade unknown)', SUP55,
         'unresolved',
         f"document is a Bapco Laboratory Report/Test Certificate Form BP0209 (04/16); "
         "property list consistent with base oil CoA: kV100, kV40, VI, Noack evaporation, "
         "CCS @-30°C, Saturates, Sulfur, UV wavelength bands (280-350nm — food-grade screening); "
         "product name, tank number, batch dates and test results not legible from text layer "
         "(likely printed in fields that weren't captured by OCR); "
         "next_action: identify product name and batch data from physical document",
         status='unresolved_identity')

for r in rows(lambda s: s == 'Bapco', 's55_bapco.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'cf682f89b0':  # DL2-14114 Bapco CoA 1pp
        doc(D55, sha, 'certificate of quality (CoA)', SUP55, ['BAPCO:UNKNOWN_COA_DL2_14114'],
            'page content: Bapco CoA form with property list; product name and values not in text layer',
            manufacturer=MFG55, issuer=MFG55,
            relation='unresolved_identity',
            note="1pp; Form BP0209 (04/16); property list includes kV100, kV40, VI, Noack, CCS @-30°C, "
                 "Saturates, Sulfur, UV wavelength bands; "
                 "values and product name fields not captured in text layer; "
                 "next_action: manual read of physical document",
            next_action='read product name and test values from physical document')
    elif p10 == '98105b37a2':  # DL2-14119 Bapco CoA 1pp
        doc(D55, sha, 'certificate of quality (CoA)', SUP55, ['BAPCO:UNKNOWN_COA_DL2_14119'],
            'page content: Bapco CoA form; product name and values not in text layer',
            manufacturer=MFG55, issuer=MFG55,
            relation='unresolved_identity',
            note="1pp; Form BP0209 (04/16); same form type as DL2-14114 (cf682f89b0); "
                 "FDA 21 CFR 172 reference (food-grade base oil screening); "
                 "next_action: manual read of physical document",
            next_action='read product name and test values from physical document')

write('s55_bapco.json', 'S55 Bapco (identity)',
      '2 documents with provisional supplier Bapco', PK55, D55)

# ===========================================================================
# S56 Huntsman
# ===========================================================================
SUP56 = 'Huntsman'
MFG56 = 'Huntsman Corporation'
OWT56 = 'out_of_template (industrial chemical / polyamide precursor — no lubricant application stated)'

D56, PK56 = {}, {}
prod(PK56, 'HUNTSMAN:TEPA', 'TEPA (Tetraethylenepentamine)', SUP56, OWT56,
     "printed: 'TETRAETHYLENEPENTAMINE (TEPA) is principally a mixture of four TEPA ethyleneamines; "
     "Applications: Asphalt additives, Mineral processing aids, Corrosion inhibitors, "
     "Polyamide resins, Epoxy curing agents, Surfactants'; "
     "CAS 112-57-2 (linear TEPA); no lubricant application stated → out_of_template")

for r in rows(lambda s: s == 'Huntsman', 's56_huntsman.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == '4c5654be8e':  # DL2-15232 TEPA technical bulletin 2pp
        doc(D56, sha, 'product technical bulletin', SUP56, ['HUNTSMAN:TEPA'],
            'full page content: TEPA composition, applications',
            manufacturer=MFG56, issuer=MFG56,
            note="2pp; 'Technical Bulletin TETRAETHYLENEPENTAMINE (TEPA)'; "
                 "CAS: linear TEPA 112-57-2, AETETA 31295-46-2, APEEDA 31295-54-2, PEDETA 31295-49-5; "
                 "applications: asphalt additives, mineral processing, corrosion inhibitors, "
                 "polyamide resins, epoxy curing, surfactants; no lubricant additive application")
    elif p10 == '9aeeece1b5':  # DL2-15247 TEPA SDS 133pp
        doc(D56, sha, 'SDS', SUP56, ['HUNTSMAN:TEPA'],
            'section 1: SDS for TEPA, 133pp EU REACH format',
            manufacturer=MFG56, issuer=MFG56,
            note="133pp; REACH SDS; very comprehensive safety data sheet for TEPA; "
                 "same product as DL2-15232 (4c5654be8e) technical bulletin")

write('s56_huntsman.json', 'S56 Huntsman (identity)',
      '2 documents with provisional supplier Huntsman', PK56, D56)

# ===========================================================================
# S57 Kemipex (1 doc) — M 25 SSI MSDS distributed by Kemipex FZE Dubai
# ===========================================================================
D57, PK57 = {}, {}
prod(PK57, 'FORMOSA:M_25_SSI', 'M 25 SSI', 'Kemipex / Formosa Petrochemical', AC,
     "same product as s50_formosa FORMOSA:M_25_SSI; "
     "MSDS issued by Kemipex FZE (Dubai) as the distributor; "
     "product name and description identical to DL2-11416 (Formosa TDS); "
     "manufacturer: Formosa Petrochemical Corporation",
     existing='')  # not 'EXISTING' — this is the same new_candidate; share key

for r in rows(lambda s: s == 'Kemipex', 's57_kemipex.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == '356a137584':  # DL2-11417 Kemipex M 25 SSI MSDS 5pp
        doc(D57, sha, 'SDS', 'Kemipex', ['FORMOSA:M_25_SSI'],
            'section 1: product name M 25 SSI, supplier Kemipex FZE Dubai',
            manufacturer='Formosa Petrochemical Corporation', issuer='Kemipex FZE',
            note="5pp; 'M 25 SSI Viscosity Index Improver for Lubricant Application'; "
                 "'Supplier: Kemipex FZE, Maze Tower, Sheikh Zayed Road, PO Box 24200, Dubai UAE'; "
                 "Kemipex = distributor; same product as DL2-11416 (s50_formosa, Formosa TDS); "
                 "classification: not classified (CLP)")

write('s57_kemipex.json', 'S57 Kemipex (identity)',
      '1 document with provisional supplier Kemipex', PK57, D57)

# ===========================================================================
# S58 Turkmenbashy refinery (1 doc) — 5 base oil grades
# ===========================================================================
SUP58 = 'Turkmenbashy refinery'
MFG58 = 'Turkmenbashy Oil Refinery Complex'
D58, PK58 = {}, {}
for grade in ['SN80', 'SN180', 'SN350', 'SN600', 'SN1200']:
    prod(PK58, f'TURKMENBASHY:{grade}', f'Turkmenbashy {grade}', SUP58, 'base_oil',
         f"printed: multi-grade spec table TŞ 05766698-60-2006, grade {grade[2:]}; "
         f"VI ≥95; Sulfur ≤0.03%; density @20°C: SN80=870, SN180=880, SN350=890, SN600=900, "
         f"SN1200=905 g/L; kV100 ranges: SN80=2.5-3.5, SN180=4.5-6.0, SN350=8.0-9.5, "
         f"SN600=11.5-13.5, SN1200=18.0-23.0 cSt; new_candidate base_oil (Group I or Group II; "
         f"class unresolved — Saturates content not given in this document)")

for r in rows(lambda s: s == 'Turkmenbashy refinery', 's58_turkmenbashy.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'e8f4ae204d':  # DL2-11239 Turkmenbashy range spec 1pp
        doc(D58, sha, 'product data sheet (range TDS)', SUP58,
            ['TURKMENBASHY:SN80', 'TURKMENBASHY:SN180', 'TURKMENBASHY:SN350',
             'TURKMENBASHY:SN600', 'TURKMENBASHY:SN1200'],
            'full page content: 5-grade range specification table',
            manufacturer=MFG58, issuer=MFG58,
            note="1pp; 'TURKMENISTAN Turkmenbashy oil refinery complex Base oil TŞ 05766698-60-2006'; "
                 "range TDS covering SN-80/180/350/600/1200; "
                 "properties: density @20°C, kV100, PP, FP, VI, Color (ASTM and ЦНТ), Sulfur (mass%), "
                 "Acid Number; "
                 "all grades VI ≥95 and Sulfur ≤0.03%; API group unresolved (Saturates not stated)")

write('s58_turkmenbashy.json', 'S58 Turkmenbashy refinery (identity)',
      '1 document with provisional supplier Turkmenbashy refinery', PK58, D58)

# ===========================================================================
# S59 TotalEnergies (1 doc) — JARYTHERM DBT heat transfer fluid
# ===========================================================================
D59, PK59 = {}, {}
prod(PK59, 'TOTAL:JARYTHERM_DBT', 'JARYTHERM DBT', 'TotalEnergies',
     'out_of_template (heat transfer fluid — synthetic dibenzyltoluene type)',
     "printed: 'JARYTHERM DBT Heat transfer circuit Synthetic heat transfer fluid, made from a "
     "blend of dibenzyltoluene isomers. Applications: Heat transfer installations by fluid "
     "circulation Operating from 0°C to +350°C in the mass (370°C in the film) without air "
     "contact'; same chemical class as FRAGOLTHERM HT (Fragol AG) which is also dibenzyltoluene; "
     "out_of_template (heat transfer fluid — no lubricant component template)")

for r in rows(lambda s: s == 'TotalEnergies', 's59_total.json'):
    sha = r['sha256']
    p10 = sha[:10]
    if p10 == 'a7138fcf74':  # DL2-15095 JARYTHERM DBT 1pp
        doc(D59, sha, 'product data sheet (TDS/PDS)', 'TotalEnergies / Total Lubrifiants',
            ['TOTAL:JARYTHERM_DBT'],
            'full page content: product description and applications',
            manufacturer='Total Lubrifiants', issuer='Total Lubrifiants',
            note="1pp; 'TOTAL LUBRIFIANTS Industrie & Spécialités 14-09-2010'; "
                 "'JARYTHERM DBT; Synthetic heat transfer fluid, made from a blend of "
                 "dibenzyltoluene isomers; Operating from 0°C to +350°C (+370°C in the film)'; "
                 "heat transfer fluid, same chemical type as FRAGOLTHERM HT from FRAGOL AG")

write('s59_total.json', 'S59 TotalEnergies (identity)',
      '1 document with provisional supplier TotalEnergies', PK59, D59)

# ===========================================================================
# S60 Tanee Chemical / Minglan Chemical / Shenyang Great Wall (3 docs)
# ===========================================================================
D60, PK60 = {}, {}
prod(PK60, 'TANEE:TE_598', 'TE-598 Dialkyl Diphenylamine', 'Tanee Chemical', AC,
     "printed: 'TE-598 Dialkyl Di Phenylamine TANEE CHEMICAL LTD, Beijing; "
     "light yellow liquid, prepared from diphenylamine and olefin; "
     "excellent high-temperature anti-oxidation; ashless antioxidant; "
     "Applications: internal combustion engine oils, turbine oils, heat conducting oils, "
     "hydraulic oils and greases, fuel oils'; "
     "additive_component (antioxidant, DPA/alkylated diphenylamine)")
prod(PK60, 'MINGLAN:T106D_SUP_HIGH_TBN_CA_SUL', 'T106D Super High TBN Calcium Sulfonate',
     'Shanghai Minglan Chemical', AC,
     "printed: '151 T106D Super High TBN Synthetic Calcium Sulfonate; "
     "SHANGHAI MINGLAN CHEMICAL CO.,LTD. Mobiel:+86 15840446549; "
     "super high-based synthetic calcium sulfonate; heavy alkyl benzene sulfonic acid raw material; "
     "excellent alkaline reserve, acid neutralization, high-temperature detergency and thermal stability'; "
     "additive_component (detergent, super-high-TBN synthetic calcium sulfonate); "
     "'151' and 'T106D' are Minglan internal code designations")
prod(PK60, 'SHENYANG_GW:CATALOG', 'Shenyang Great Wall finished lubricant catalog', 'Shenyang Great Wall',
     'out_of_scope',
     "printed: 'SHENYANG GREAT WALL LUBRICATING OIL MANUFACTURING CO., LTD; "
     "established 1987; lubricating oil, special oil and additive series products; "
     "brand 润驰 (Runchike); products include engine oils, gear oils, industrial oils'; "
     "35pp product manual for a finished lubricant manufacturer → out_of_scope "
     "(catalog of finished lubricant blends, not a raw-material source document); "
     "product mix of finished lubricants and possibly additive components, but no "
     "individual raw material TDS identified")

for r in rows(lambda s: s in ('Tanee Chemical', 'Minglan Chemical', 'Shenyang Great Wall'), 's60_micro.json'):
    sha = r['sha256']
    p10 = sha[:10]
    sup = r['supplier_provisional']
    if p10 == '613671bd2b':  # DL2-15242 Tanee TE-598 1pp
        doc(D60, sha, 'product data sheet (TDS/PDS)', 'Tanee Chemical', ['TANEE:TE_598'],
            'full page content: product name, description, applications, typical properties',
            manufacturer='Tanee Chemical Ltd.', issuer='Tanee Chemical Ltd.',
            note="1pp; 'TE-598 Dialkyl Di Phenylamine TANEE CHEMICAL LTD, Room 2703, "
                 "Building 26, Link Park, No.8 Culture Park, West Road, BDA, Beijing, China'; "
                 "ashless DPA antioxidant prepared from diphenylamine and olefin")
    elif p10 == '0722625048':  # DL2-15278 Minglan T106D 1pp
        doc(D60, sha, 'product data sheet (TDS/PDS)', 'Shanghai Minglan Chemical',
            ['MINGLAN:T106D_SUP_HIGH_TBN_CA_SUL'],
            'full page content: product name and description',
            manufacturer='Shanghai Minglan Chemical Co., Ltd.', issuer='Shanghai Minglan Chemical Co., Ltd.',
            note="1pp; '151 T106D Super High TBN Synthetic Calcium Sulfonate'; "
                 "Shanghai Minglan Chemical Co., Ltd.; "
                 "lubeadditive.com domain; super high TBN calcium sulfonate detergent")
    elif p10 == 'dfd31b0807':  # DL2-15800 Shenyang Great Wall catalog 35pp
        doc(D60, sha, 'finished lubricant product catalog', 'Shenyang Great Wall',
            ['SHENYANG_GW:CATALOG'], '',
            relation='out_of_scope', issuer='Shenyang Great Wall Lubricating Oil Manufacturing Co., Ltd.',
            note="35pp; product manual for Shenyang Great Wall Lubricating Oil Manufacturing Co., Ltd.; "
                 "covers engine oils, gear oils, industrial gear oils, hydraulic oils, compressor oils "
                 "as finished lubricant products (brand 润驰/Runchike); "
                 "includes ISO 9001:2015 quality certification info; "
                 "this is a finished lubricant manufacturer catalog, not a raw-material source; "
                 "some additive product data may be embedded but not separated in this document")

write('s60_micro.json', 'S60 Tanee/Minglan/Shenyang (identity)',
      '3 documents: Tanee Chemical, Minglan Chemical, Shenyang Great Wall', PK60, D60)
