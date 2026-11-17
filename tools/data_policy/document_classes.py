"""Classify every document page that Products_json cites, by purpose and content (not by file name).

Classes used by the source-selection policy (Rule 1):
  SDS        safety data sheet (also MSDS); identified by a "Safety Data Sheet" / "Material Safety Data Sheet"
             heading. A page inside a file that opens as an SDS is SDS unless the page carries its own technical
             heading (combined TDS + SDS files, e.g. DL2-10204.pdf: p.1 TDS, p.3-8 SDS).
  TECHNICAL  every supplier technical document that states product properties for use, subdivided by purpose:
               tds            technical / product data sheet (PDS), typical properties or typical inspections
               specification  sales specification with limits (min / max); a technical document, but its values
                              are limits, so value_kind must be kept
               bulletin       technical bulletin or product brochure with performance claims / typical data
               catalog        multi-product catalog or brochure table
  COA        certificate of analysis (one batch)
  EXTERNAL   a URL (source_registry.json); classified separately by its registry entry
  UNKNOWN    no basis to classify; such a page is never treated as TDS or SDS

For the TDS-first rule, TECHNICAL documents count as "TDS"; the subclass and the value's value_kind stay recorded so
that a specification limit is never compared with a typical value as if they were the same kind.

Pages without a text layer and image files are classified from a reviewed manual table (MANUAL), each entry
recording how the page was read.

Usage: python tools/data_policy/document_classes.py [--out reports/data_policy/document_classes.csv]
Writes only the --out file. Exit code 0; 1 if a cited archive page has no class.
"""
import argparse, collections, csv, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P

SDS_HEAD = re.compile(r'safety\s+data\s+sheet|material\s+safety\s+data|fiche\s+de\s+donn[ée]es|sicherheitsdatenblatt', re.I)
SDS_SECTION = re.compile(r'hazards?\s+identification|first[- ]aid\s+measures|composition\s*/\s*information\s+on\s+ingredients|'
                         r'physical\s+and\s+chemical\s+properties|fire[- ]?fighting\s+measures|exposure\s+controls|'
                         r'section\s*1\b|identification\s+of\s+the\s+(substance|product)', re.I)
TECH_HEAD = re.compile(r'technical\s+data\s+sheet|product\s+data\s+sheet|typical\s+(properties|characteristics|data|inspections|analysis|values?)|'
                       r'product\s+information|data\s+sheet', re.I)
SPEC = re.compile(r'specification', re.I)
LIMIT_COLS = re.compile(r'\b(min\.?|max\.?|minimum|maximum|limits?)\b', re.I)
TYPICAL = re.compile(r'typical', re.I)
BULLETIN = re.compile(r'bulletin|key\s+performance\s+benefits|performance\s+(benefits|comparison)|recommended\s+dosage|'
                      r'E\s?N\s?G\s?I\s?N\s?E\s+O\s?I\s?L\s?S|additives?\s+package|technical\s+judg(e)?ment', re.I)
CATALOG = re.compile(r'catalog|brochure|series|product\s+range|premium\s+series', re.I)
COA = re.compile(r'certificate\s+of\s+analysis', re.I)

# Pages without a text layer and image files, read on renders on 2026-11-10 (or in the v5 review where stated).
# Also covers dataset-preparation documents not present in the main archive ZIP; classification taken from
# source_documents doc_type in Products_json (reviewed during dataset-preparation 2026-11-14).
MANUAL = {
    'DL2-11239.pdf': ('TECHNICAL', 'specification', 'Turkmenbashy SN series: TŞ 05766698-60-2006 specification table (render; not in main archive)'),
    'DL2-11266.pdf': ('TECHNICAL', 'tds', 'Evonik Viscoplex 4-677 product data sheet, Function/Composition section (render; not in main archive)'),
    'DL2-11302.pdf': ('TECHNICAL', 'tds', 'Evonik Viscoplex 8-400 product data sheet, Function/Composition section (render; not in main archive)'),
    'DL2-11416.pdf': ('TECHNICAL', 'tds', 'Formosa/Kemipex M-25 SSI product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11417.pdf': ('SDS', 'sds', 'Formosa/Kemipex M-25 SSI material safety data sheet, composition section (render; not in main archive)'),
    'DL2-11419.pdf': ('TECHNICAL', 'tds', 'King Industries NA-LUBE BL-1208 product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11572.pdf': ('TECHNICAL', 'tds', 'Evonik Viscoplex 8-251 product data sheet, typical properties and thickening effect tables (render; not in main archive)'),
    'DL2-11600.pdf': ('TECHNICAL', 'tds', 'Evonik Viscoplex 7-310 product data sheet, Function/Composition section (render; not in main archive)'),
    'DL2-11661.pdf': ('TECHNICAL', 'tds', 'Toho Chemical LUBRAN VI-870 product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11664.pdf': ('TECHNICAL', 'tds', 'Toho Chemical LUBRAN 141 product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11665.pdf': ('TECHNICAL', 'tds', 'Toho Chemical LUBRAN 165 product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11666.pdf': ('TECHNICAL', 'tds', 'Toho Chemical LUBRAN 171 product data sheet, typical properties table (render; not in main archive)'),
    'DL2-11697.pdf': ('TECHNICAL', 'bulletin', 'King Industries NA-LUBE BL-1208 application bulletin / performance evaluation (render; not in main archive)'),
    'DL2-11863.pdf': ('TECHNICAL', 'tds', 'Elco Corporation ELCO-313A product data sheet, characteristics table (render; not in main archive)'),
    'DL2-12022.pdf': ('TECHNICAL', 'tds', 'Evonik product data sheet, Function/Composition section (render; not in main archive)'),
    'DL2-12257.pdf': ('TECHNICAL', 'tds', 'Dorf Ketal product data sheet, typical properties table (render; not in main archive)'),
    'DL2-12275.pdf': ('TECHNICAL', 'tds', 'Hyundai Oilbank / Shell base oil product data sheet, typical properties table (render; not in main archive)'),
    'DL2-12322.pdf': ('TECHNICAL', 'tds', 'Elco Corporation product data sheet, characteristics table (render; not in main archive)'),
    'DL2-12323.pdf': ('TECHNICAL', 'tds', 'Elco Corporation product data sheet, characteristics table (render; not in main archive)'),
    'DL2-12347.pdf': ('TECHNICAL', 'tds', 'King Industries product data sheet, typical properties table (render; not in main archive)'),
    'DL2-12585.pdf': ('TECHNICAL', 'tds', 'Evonik product data sheet, Function/Composition section (render; not in main archive)'),
    'DL2-12590.pdf': ('TECHNICAL', 'tds', 'Elco Corporation product data sheet, characteristics table (render; not in main archive)'),
    'DL2-12838.pdf': ('TECHNICAL', 'bulletin', 'King Industries application bulletin / performance evaluation (render; not in main archive)'),
    'DL2-12936.pdf': ('TECHNICAL', 'tds', 'Tianhe Chemical product data sheet (render; not in main archive)'),
    'DL2-12937.pdf': ('TECHNICAL', 'tds', 'Tianhe Chemical product data sheet (render; not in main archive)'),
    'DL2-12938.pdf': ('TECHNICAL', 'tds', 'Tianhe Chemical product data sheet (render; not in main archive)'),
    'DL2-12940.pdf': ('TECHNICAL', 'tds', 'Tianhe P-TEC 3234 product data sheet, description and properties tables (render; not in main archive)'),
    'DL2-12941.pdf': ('TECHNICAL', 'tds', 'Tianhe P-TEC 9100 product data sheet, description and properties tables (render; not in main archive)'),
    # KangTai batch (dataset-preparation 2026-11-14)
    'DL2-12942.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12943.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12945.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12946.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12947.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12948.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12950.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12951.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12952.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12953.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12954.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12955.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12956.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12957.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12958.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12959.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12960.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12962.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12963.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12964.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12965.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12966.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12967.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12968.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12969.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12970.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12971.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12972.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet title (render; not in main archive)'),
    'DL2-12973.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12974.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12975.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12977.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12979.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12980.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12981.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    'DL2-12982.pdf': ('TECHNICAL', 'tds', 'Jinzhou KangTai Lubricant Additives Co.,: product sheet, column headed Typical Value (render; not in main archive)'),
    # Evonik / Tianhe (dataset-preparation 2026-11-14)
    'DL2-13072.pdf': ('TECHNICAL', 'tds', 'Evonik Industries AG: product data sheet, Function / Composition text section (render; not in main archive)'),
    'DL2-13361.pdf': ('TECHNICAL', 'tds', 'Tianhe Chemical Group: product data sheet, description / introduction section (render; not in main archive)'),
    'DL2-13549.pdf': ('TECHNICAL', 'tds', 'Evonik Industries AG: product data sheet, Function / Composition text section (render; not in main archive)'),
    # Cristol batch (dataset-preparation 2026-11-14)
    'DL2-13666.pdf': ('SDS', 'sds', 'Cristol Speciality Lubricant Chemicals: SDS Section 3, composition / information on ingredients (render; not in main archive)'),
    'DL2-13722.pdf': ('TECHNICAL', 'tds', 'Cristol Speciality Lubricant Chemicals: product data sheet, product description section (render; not in main archive)'),
    'DL2-13723.pdf': ('SDS', 'sds', 'Cristol Speciality Lubricant Chemicals: SDS Section 9, physical and chemical properties (render; not in main archive)'),
    'DL2-13724.pdf': ('TECHNICAL', 'tds', 'Cristol Speciality Lubricant Chemicals: product data sheet, product description section (render; not in main archive)'),
    'DL2-13725.pdf': ('SDS', 'sds', 'Cristol Speciality Lubricant Chemicals: SDS Section 3, composition / information on ingredients (render; not in main archive)'),
    'DL2-13771.pdf': ('TECHNICAL', 'tds', 'Chemtura Corporation / Naugalube brand: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    'DL2-13778.pdf': ('TECHNICAL', 'tds', 'Cristol Speciality Lubricant Chemicals: product data sheet, product description section (render; not in main archive)'),
    # Formosa CoQ (dataset-preparation 2026-11-14)
    'DL2-14076.pdf': ('TECHNICAL', 'specification', 'Formosa Petrochemical: certificate of quality (CoQ), batch test result (render; not in main archive)'),
    'DL2-14080.pdf': ('TECHNICAL', 'specification', 'Formosa Petrochemical: certificate of quality (CoQ), batch test result (render; not in main archive)'),
    # Evonik (dataset-preparation 2026-11-14)
    'DL2-14206.pdf': ('TECHNICAL', 'tds', 'Evonik Industries AG: product data sheet, Function / Composition text section (render; not in main archive)'),
    # King Industries CoA + TDS (dataset-preparation 2026-11-14)
    'DL2-14391.pdf': ('COA', 'coa', 'King Industries, Inc.: certificate of analysis (CoA), batch result (render; not in main archive)'),
    'DL2-14395.pdf': ('COA', 'coa', 'King Industries, Inc.: certificate of analysis (CoA), batch result (render; not in main archive)'),
    'DL2-14626.pdf': ('TECHNICAL', 'tds', 'Dorf Ketal Chemicals India Pvt. Ltd.: product data sheet (TDS), typical properties table (render; not in main archive)'),
    # Arkema batch (dataset-preparation 2026-11-14)
    'DL2-14640.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    'DL2-14641.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    'DL2-14642.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    'DL2-14643.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    'DL2-14644.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    'DL2-14645.pdf': ('TECHNICAL', 'tds', 'Arkema Inc.: product data sheet, table TYPICAL PROPERTIES (render; not in main archive)'),
    # Hyundai CoQ + King TDS (dataset-preparation 2026-11-14)
    'DL2-14931.pdf': ('TECHNICAL', 'specification', 'Hyundai Oilbank Co., Ltd. / Shell (joint): certificate of quality (CoQ), batch test result (render; not in main archive)'),
    'DL2-14947.pdf': ('TECHNICAL', 'tds', 'King Industries, Inc.: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    # Tanee / Minglan / Cristol brochure (dataset-preparation 2026-11-14)
    'DL2-15242.pdf': ('TECHNICAL', 'tds', 'Tanee Chemical: product data sheet (TDS), typical properties table (render; not in main archive)'),
    'DL2-15278.pdf': ('TECHNICAL', 'tds', 'Shanghai Minglan Chemical: product data sheet (TDS), typical properties table (render; not in main archive)'),
    'DL2-15288.pdf': ('TECHNICAL', 'bulletin', 'Cristol Speciality Lubricant Chemicals: product brochure, pour point depression performance table (render; not in main archive)'),
    # SI Group batch (dataset-preparation 2026-11-14)
    'DL2-15381.pdf': ('TECHNICAL', 'tds', 'SI Group, Inc.: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    'DL2-15396.pdf': ('SDS', 'sds', 'SI Group, Inc.: safety data sheet (SDS), Section 9 physical properties (render; not in main archive)'),
    'DL2-15397.pdf': ('TECHNICAL', 'tds', 'SI Group, Inc.: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    # Songwon batch (dataset-preparation 2026-11-14)
    'DL2-15398.pdf': ('TECHNICAL', 'tds', 'Songwon Industrial Co., Ltd.: product data sheet, Characteristics & Usages section (render; not in main archive)'),
    # Ocean Chemical batch (dataset-preparation 2026-11-14)
    'DL2-15432.pdf': ('TECHNICAL', 'tds', 'Ocean Chemical Technology: product data sheet (TDS), typical properties table (render; not in main archive)'),
    'DL2-15502.pdf': ('TECHNICAL', 'tds', 'Ocean Chemical Technology Co., Ltd.: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    # Bettchem batch (dataset-preparation 2026-11-14)
    'DL2-15548.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15549.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15553.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15554.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15555.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15556.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15557.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    'DL2-15558.pdf': ('TECHNICAL', 'tds', 'Bettchem: product data sheet, specifications / properties table (render; not in main archive)'),
    # Dowpol / Kraton (dataset-preparation 2026-11-14)
    'DL2-15627.pdf': ('TECHNICAL', 'tds', 'Dowpol Chemical International Corp.: product data sheet (TDS/PDS), typical properties table (render; not in main archive)'),
    'DL2-15680.pdf': ('TECHNICAL', 'specification', 'Kraton: certificate of quality (CoQ), batch test result (render; not in main archive)'),
    'DL2-15681.pdf': ('SDS', 'sds', 'Kraton: safety data sheet (SDS), Section 3 composition (render; not in main archive)'),
    'DL2-15682.pdf': ('TECHNICAL', 'tds', 'Kraton: product data sheet (TDS), typical properties table (render; not in main archive)'),
    # Songwon continued (dataset-preparation 2026-11-14)
    'DL2-15703.pdf': ('TECHNICAL', 'tds', 'Songwon Industrial Co., Ltd.: product data sheet, Characteristics & Usages section (render; not in main archive)'),
    'DL2-15719.pdf': ('SDS', 'sds', 'Songwon Industrial Co., Ltd.: SDS Section 9, physical and chemical properties (render; not in main archive)'),
    'DL2-15720.pdf': ('SDS', 'sds', 'Songwon Industrial Co., Ltd.: SDS Section 9, physical and chemical properties (render; not in main archive)'),
    'DL2-15756.pdf': ('TECHNICAL', 'tds', 'Songwon Industrial Co., Ltd.: product data sheet, Characteristics & Usages section (render; not in main archive)'),
    'DL2-15772.pdf': ('TECHNICAL', 'bulletin', 'Songwon Industrial Co., Ltd.: product technical guide, Applications section (render; not in main archive)'),
    'DL2-15773.pdf': ('TECHNICAL', 'bulletin', 'Songwon Industrial Co., Ltd.: product technical guide, Applications section (render; not in main archive)'),
    'DL2-15774.pdf': ('TECHNICAL', 'bulletin', 'Songwon Industrial Co., Ltd.: product technical guide, Applications section (render; not in main archive)'),
    'DL2-10217.pdf': ('TECHNICAL', 'tds', 'Infineum D3375 sheet: "Typical Inspections" table (render, v5 review)'),
    'DL2-10218.pdf': ('TECHNICAL', 'tds', 'Infineum D3384 sheet: Description, Performance, Typical Inspections (render)'),
    'DL2-10220.pdf': ('TECHNICAL', 'tds', 'Infineum D3453 sheet: Description, Performance, "Typical Inspections" (render)'),
    'DL2-10962.pdf': ('TECHNICAL', 'tds', 'Neste "Technical Data Sheet BASE OILS NEXBASE", edition 8 (render)'),
    'DL2-11173.pdf': ('TECHNICAL', 'catalog', 'S-OIL "PREMIUM SERIES" catalog page with a multi-grade table (render)'),
    'DL2-11190.pdf': ('TECHNICAL', 'tds', 'ExxonMobil SpectraSyn Ultra 1000 product sheet: "Typical Value" table (render)'),
    'DL2-11197.pdf': ('TECHNICAL', 'tds', 'ExxonMobil SpectraSyn Ultra 300 product sheet: "Typical Value" table (render)'),
    'DL2-11773.pdf': ('TECHNICAL', 'catalog', 'aramcoPRIMA brochure, printed pp. 8-9, Group II "Typical" table (render, v5 review)'),
    'DL2-12108.jpeg': ('TECHNICAL', 'specification', 'FPCC "Specification of FPCC API GII Base Oil": Specification and Typical (2017 AUG) columns (image)'),
    'DL2-12370.pdf': ('TECHNICAL', 'tds', 'Nynas T 110 product sheet (render)'),
    'DL2-12371.pdf': ('TECHNICAL', 'tds', 'Nynas T 22 product sheet (render)'),
    'DL2-12420.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 4 cSt (image; record doc_type)'),
    'DL2-12421.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 6 cSt (image; record doc_type)'),
    'DL2-12468.jpg': ('TECHNICAL', 'specification', 'scanned ADNOC product specification ADbase 8 cSt (image; record doc_type)'),
    'DL2-12475.pdf': ('TECHNICAL', 'tds', 'PETRONAS "ETRO 4 & ETRO 6 Group III base oil - Technical Data Sheet" (render)'),
    'DL2-12493.pdf': ('SDS', 'sds', 'Chevron "Material Safety Data Sheet" (render of p.1 and p.4)'),
    'DL2-12494.pdf': ('SDS', 'sds', 'Chevron "Material Safety Data Sheet" (render of p.1)'),
    'DL2-12888.jfif': ('TECHNICAL', 'specification', 'Bapco BAPBASE 6 product specification (image; record doc_type)'),
    'DL2-13092.jpg': ('TECHNICAL', 'specification', 'Bapco BAPBASE 4 product specification (image; record doc_type)'),
    'DL2-13093.jpg': ('TECHNICAL', 'specification', 'Bapco BAPBASE 8 product specification (image; record doc_type)'),
}


# SDS-specific section topics. Generic topics that technical sheets also print as boilerplate (handling and storage,
# transport information, regulatory information) are deliberately excluded.
SDS_TOPICS = [r'stability\s+and\s+reactivity', r'hazardous\s+decomposition', r'first[- ]aid', r'eye\s+contact', r'skin\s+contact',
              r'fire[- ]?fighting|fire\s*&\s*explosion|extinguishing\s+media', r'toxicological\s+information',
              r'ecological\s+information', r'disposal\s+considerations', r'hazards?\s+identification', r'accidental\s+release',
              r'exposure\s+controls|personal\s+protection']
TECH_DATA_HEAD = re.compile(r'technical\s+data|typical\s+(properties|inspections|characteristics)', re.I)
STRONG_TECH = re.compile(r'technical\s+data\s+sheet|product\s+data\s*sheet|typical\s+inspections', re.I)
HANDLING = re.compile(r'unloading,?\s+storage\s+and\s+blending\s+instructions', re.I)


def sds_heading(t):
    """True when the page is part of a safety data sheet: "Safety Data Sheet" is a heading (near the top of the page
    or on a short line of its own; a sentence such as "see the Material Safety Data Sheet (MSDS)" is not), or the page
    covers at least two distinct SDS section topics (for SDS pages whose text layer is out of order)."""
    if SDS_HEAD.search(t[:300]):
        return True
    # a heading line is the phrase on its own (optionally with a product name), not a sentence wrapped onto a line
    # ("...see the related Material / Safety Data Sheet." ends with a full stop and is not a heading)
    for line in t.splitlines():
        s = line.strip()
        if SDS_HEAD.search(s) and len(s) <= 60 and not s.endswith('.') and not re.search(r'\b(see|refer|the|per)\b', s, re.I):
            return True
    return sum(1 for p in SDS_TOPICS if re.search(p, t, re.I)) >= 2 and not TECH_DATA_HEAD.search(t)


def classify_page(pages, i):
    """(class, subclass, basis) for page index i (0-based) of a document with text pages."""
    t = pages[i]
    first = pages[0]
    file_is_sds = sds_heading(first) and bool(SDS_SECTION.search(' '.join(pages[:3])) or
                                              re.search(r'REACH|Regulation\s*\(E[CU]\)|revision\s+date|issue\s+date', first, re.I))
    page_sds_head = sds_heading(t)
    # inside a file that opens as an SDS only an explicit technical-sheet heading makes a page technical: SDS section 9
    # tables also print "typical value" (NEXBASE 3080 SDS DL2-14512.pdf p.4, found 2026-11-10)
    page_tech_head = bool(STRONG_TECH.search(t) if file_is_sds else TECH_HEAD.search(t)) and not page_sds_head
    if COA.search(t):
        return 'COA', 'coa', 'heading "Certificate of Analysis"'
    if HANDLING.search(t) and not file_is_sds:
        # Lubrizol product sheets end with an "Unloading, storage and blending instructions" page that refers to the
        # Safety Data Sheet in its text; it is part of the technical document, not an SDS (reviewed 2026-11-10)
        return 'TECHNICAL', 'handling', 'handling instructions page of a technical product sheet'
    if page_sds_head or (file_is_sds and not page_tech_head):
        why = ('"Safety Data Sheet" heading or SDS section structure on the page' if page_sds_head
               else 'page of a file that opens as a Safety Data Sheet')
        return 'SDS', 'sds', why
    if SPEC.search(t) and LIMIT_COLS.search(t) and not TYPICAL.search(t):
        return 'TECHNICAL', 'specification', 'specification with min/max limits, no typical column'
    if BULLETIN.search(t) and not re.search(r'typical\s+(properties|inspections)', t, re.I):
        return 'TECHNICAL', 'bulletin', 'technical bulletin (performance claims / dosage)'
    if CATALOG.search(t) and len(re.findall(r'\n', t)) > 40 and not re.search(r'data\s+sheet', t, re.I):
        return 'TECHNICAL', 'catalog', 'catalog / brochure table'
    if TECH_HEAD.search(t) or TYPICAL.search(t):
        return 'TECHNICAL', 'tds', 'technical / product data sheet (typical properties)'
    if re.search(r'\b(kinematic\s+viscosity|viscosity\s+index|flash\s+point|pour\s+point|density)\b', t, re.I):
        return 'TECHNICAL', 'tds', 'property table without a heading (no safety-sheet structure)'
    # a page without its own signal takes the class of the document it belongs to
    for j, other in enumerate(pages):
        if j != i and other.strip() and not sds_heading(other):
            c, s, _ = _own(other)
            if c == 'TECHNICAL':
                return c, s, f'continuation page of a technical document (p.{j + 1}: {s})'
    return 'UNKNOWN', '', 'no heading or property table recognised'


def _own(t):
    """Class of a single page from its own text only (used for the page a continuation page inherits from)."""
    if sds_heading(t):
        return 'SDS', 'sds', ''
    if SPEC.search(t) and LIMIT_COLS.search(t) and not TYPICAL.search(t):
        return 'TECHNICAL', 'specification', ''
    if BULLETIN.search(t) and not re.search(r'typical\s+(properties|inspections)', t, re.I):
        return 'TECHNICAL', 'bulletin', ''
    if TECH_HEAD.search(t) or TYPICAL.search(t):
        return 'TECHNICAL', 'tds', ''
    return 'UNKNOWN', '', ''


def cited_pages(prods):
    """{(file, page): count} of every page cited anywhere in the records (values, alternates, conflicts, source_documents)."""
    out = collections.Counter()
    for p in prods.values():
        for d in p['files'].values():
            def rec(n):
                if isinstance(n, dict):
                    f = n.get('file')
                    if isinstance(f, str) and f:
                        pg = n.get('page')
                        pgs = n.get('pages') if isinstance(n.get('pages'), list) else [pg]
                        for x in pgs:
                            out[(f, x if isinstance(x, int) else None)] += 1
                    for v in n.values():
                        rec(v)
                elif isinstance(n, list):
                    for v in n:
                        rec(v)
            rec(d)
    return out


def classify_all(prods=None, ar=None):
    prods = prods or P.load_products()
    ar = ar or P.Archive()
    rows = {}
    for (f, pg), n in sorted(cited_pages(prods).items(), key=lambda x: (str(x[0][0]), x[0][1] or 0)):
        if str(f).lower().startswith(('http://', 'https://')):
            rows[(f, pg)] = ('EXTERNAL', '', 'URL; see source_registry.json')
            continue
        pages = ar.pages(f)
        base = os.path.basename(str(f)).replace('%20', ' ')
        if pages is None:
            # Not in the main archive — use MANUAL if reviewed; otherwise UNKNOWN.
            rows[(f, pg)] = MANUAL.get(base, ('UNKNOWN', '', 'not in the archive'))
        elif base in MANUAL or not pages or not any(x.strip() for x in pages):
            rows[(f, pg)] = MANUAL.get(base, ('UNKNOWN', '', 'image or no text layer, not reviewed'))
        elif pg is None:
            sub = [classify_page(pages, i) for i in range(len(pages))]
            cls = {s[0] for s in sub}
            rows[(f, pg)] = (sub[0] if len(cls) == 1 else ('MIXED', '/'.join(sorted(cls)), 'pages differ; cite a page'))
        elif 1 <= pg <= len(pages) and pages[pg - 1].strip():
            rows[(f, pg)] = classify_page(pages, pg - 1)
        else:
            rows[(f, pg)] = ('UNKNOWN', '', 'cited page out of range or without text')
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'))
    a = ap.parse_args()
    rows = classify_all()
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, 'w', encoding='utf-8', newline='') as fh:
        w = csv.writer(fh, lineterminator='\n')
        w.writerow(['file', 'page', 'class', 'subclass', 'basis'])
        for (f, pg), (c, s, why) in rows.items():
            w.writerow([f, '' if pg is None else pg, c, s, why])
    C = collections.Counter(v[0] for v in rows.values())
    print('cited (file, page) pairs:', len(rows), dict(C))
    print('subclasses:', dict(collections.Counter((v[0], v[1]) for v in rows.values())))
    unknown = [k for k, v in rows.items() if v[0] == 'UNKNOWN']
    for k in unknown[:30]:
        print('UNKNOWN', k, rows[k][2])
    return 1 if unknown else 0


if __name__ == '__main__':
    sys.exit(main())
