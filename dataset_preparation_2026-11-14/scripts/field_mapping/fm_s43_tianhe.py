"""Field-level mapping, S43 Tianhe Chemicals — 7 products, 7 sheets.

All sheets read in full (text layer) 2026-11-16.

Products:
  Additive components (4):
    TIANHE:C_TEC_104A   Low-base calcium sulfonate detergent    1 doc: TDS (DL2-12936)
    TIANHE:C_TEC_151A   PIB succinimide dispersant               1 doc: TDS (DL2-12937)
    TIANHE:C_TEC_206    ZDDP primary-secondary                   1 doc: TDS (DL2-12938)
    TIANHE:C_TEC_209    ZDDP secondary                           1 doc: TDS / web capture (DL2-13361)
  Additive packages (3):
    EXISTING:TIANHE_P_TEC_3232   General-purpose DI pack     1 doc: TDS (DL2-12939)
    TIANHE:P_TEC_3234            Diesel DI pack              1 doc: TDS (DL2-12940)
    TIANHE:P_TEC_9100            PCMO/motorcycle DI pack     1 doc: TDS (DL2-12941)

Manufacturer: Tianhe Chemicals Group Ltd (TIANHE brand)

Non-product docs in s43_tianhe.json (not mapped):
  c793935c48c1   TIANHE product range reference (xlsx)
  425b59d81f90   TIANHE product range reference (xlsx)

P_TEC_3232 density: TDS prints "Density, kg/m3, at 15℃: 1.0130"; likely g/mL printed
  with wrong unit label (1.0130 g/mL = 1013.0 kg/m3); recorded as printed with note.
P_TEC_9100 density: TDS prints "Density, kg/L, at 15°C: 0.9910" ASTM D4052; recorded
  as printed (kg/L = g/mL; 0.9910 g/mL = 991.0 kg/m3).
C_TEC_209: document is a web page capture (URL english.tianhechem.com, dated 7/18/2020);
  treated as TDS/PDS per document_register classification.

Writes field_evidence/s43_tianhe.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    # sha12: (canonical_file, revision_date)
    '9459a8a39e01': ('DL2-12936.pdf', ''),           # C_TEC_104A TDS, 2pp; no printed date
    '00b65021a682': ('DL2-12937.pdf', ''),           # C_TEC_151A TDS, 2pp; no printed date
    'fcaf972e3566': ('DL2-12938.pdf', ''),           # C_TEC_206 TDS, 2pp; no printed date
    '5b48698eaaea': ('DL2-13361.pdf', '2020-07-18'), # C_TEC_209 webpage capture; "7/18/2020"
    'de5df90125ec': ('DL2-12939.pdf', ''),           # P_TEC_3232 TDS, 2pp; no printed date
    'afcbf1a67b6c': ('DL2-12940.pdf', ''),           # P_TEC_3234 TDS, 2pp; no printed date
    '248ffefbcc1c': ('DL2-12941.pdf', ''),           # P_TEC_9100 TDS, 2pp; no printed date
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; parsed rows compared with the page text'
VC_TDS       = 'product data sheet, specifications / properties table'
VC_TDS_DESC  = 'product data sheet, description / introduction section'
VC_TDS_APP   = 'product data sheet, applications section'
VC_TDS_TREAT = 'product data sheet, treat rate table'
VC_WEB       = 'TDS page capture (web), specifications / properties table'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', vc=None, entry=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc or VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _m(pk, tmpl, field, notes_='', entry=''):
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': REVIEW,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text',
                            'unit', 'test_temperature_c', 'method', 'conditions']},
    })


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE C_TEC_104A   DL2-12936.pdf (TDS, 2pp)   sha 9459a8a39e01
# LOW BASE SYNTHETIC ALKYL BENZENE CALCIUM SULFONATE; engine oil detergent
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:C_TEC_104A'
S  = '9459a8a39e01'

_r(PK, 'component_general', 'function.primary',
   'LOW BASE SYNTHETIC ALKYL BENZENE CALCIUM SULFONATE; engine oil detergent, dispersant and antirust',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title and opening description in TDS; enterprise standard Q/YHT 003-2015')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (calcium sulfonate detergent)')
_r(PK, 'component_general', 'chemical_family',
   'Synthetic alkyl benzene calcium sulfonate',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='derived from product title; overbased calcium sulfonate detergent type')
_m(PK, 'component_general', 'active_content',
   'not found; no active matter or base oil content percentage stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; no carrier identity stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   '0.5-3.0%',
   unit='%', lo='0.5', hi='3.0', vk='range', vc=VC_TDS_APP, sha=S, pg=1,
   entry='applications',
   notes='from Applications section in TDS; percentage basis unspecified (not stated as mass or volume)')
_m(PK, 'component_general', 'compatibility_restrictions',
   'not found; no incompatibility or restriction listed in TDS')
_r(PK, 'component_general', 'function_specific_markers.tbn',
   'Total base number, mgKOH/g: 22.0',
   value='22.0', unit='mgKOH/g', vk='typical', meth='ASTM D2896', sha=S, pg=1)
_r(PK, 'component_general', 'function_specific_markers.ca',
   'Calcium, mass%: 2.400',
   value='2.400', unit='mass%', vk='typical', meth='ASTM D5185', sha=S, pg=1)
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.p',
   'not found; not stated in TDS (calcium sulfonate; no phosphorus expected)')
_m(PK, 'component_general', 'function_specific_markers.zn',
   'not found; not stated in TDS (calcium sulfonate; no zinc expected)')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; not stated in TDS')

_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Maroon clear liquid', vk='text', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:density_kgm3_20c',
   'Density, kg/m3: 933.2',
   value='933.2', unit='kg/m3', vk='typical', meth='ASTM D1298', sha=S, pg=1,
   notes='test temperature 20°C per TDS')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c',
   'Flash point(COC), ℃: 190',
   value='190', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:kv100_mm2s',
   'Kinematic viscosity, mm2/s, at 100℃: 20.00',
   value='20.00', unit='mm2/s', vk='typical', meth='ASTM D445', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:sulfur_mass_pct',
   'Sulfur, mass%: 2.450',
   value='2.450', unit='mass%', vk='typical', meth='ASTM D129', sha=S, pg=1)


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE C_TEC_151A   DL2-12937.pdf (TDS, 2pp)   sha 00b65021a682
# POLYISOBUTYLENE SUCCINIMIDE; ashless dispersant
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:C_TEC_151A'
S  = '00b65021a682'

_r(PK, 'component_general', 'function.primary',
   'POLYISOBUTYLENE SUCCINIMIDE; ashless dispersant',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title in TDS; enterprise standard Q/YHT007-2015')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (ashless dispersant)')
_r(PK, 'component_general', 'chemical_family',
   'Polyisobutylene succinimide; prepared from highly reactive polyisobutylene (f=1300) by thermal process; free of chlorine',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes="from product Features section; molecular weight f=1300 printed explicitly")
_m(PK, 'component_general', 'active_content',
   'not found; no active matter percentage stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; no carrier identity stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   '2.0-4.0%',
   unit='%', lo='2.0', hi='4.0', vk='range', vc=VC_TDS_APP, sha=S, pg=1,
   entry='applications',
   notes='from Applications section in TDS; percentage basis unspecified')
_m(PK, 'component_general', 'compatibility_restrictions',
   'not found; no incompatibility or restriction listed in TDS')
_r(PK, 'component_general', 'function_specific_markers.tbn',
   'Total base number, mgKOH/g: 50.0',
   value='50.0', unit='mgKOH/g', vk='typical', meth='ASTM D2896', sha=S, pg=1)
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; ashless dispersant (no metallic elements; Ca not stated)')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; ashless dispersant (no metallic elements)')
_m(PK, 'component_general', 'function_specific_markers.p',
   'not found; ashless dispersant (no phosphorus expected)')
_m(PK, 'component_general', 'function_specific_markers.zn',
   'not found; ashless dispersant (no zinc expected)')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; ashless dispersant (no molybdenum expected)')

_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Clear viscous liquid', vk='text', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:density_kgm3_20c',
   'Density, kg/m3: 910.0',
   value='910.0', unit='kg/m3', vk='typical', meth='ASTM D1298', sha=S, pg=1,
   notes='test temperature 20°C per TDS')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c',
   'Flash point(COC), ℃: 210',
   value='210', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:kv100_mm2s',
   'Kinematic viscosity, mm2/s, at 100℃: 205.0',
   value='205.0', unit='mm2/s', vk='typical', meth='ASTM D445', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:nitrogen_mass_pct',
   'Nitrogen, mass%: 2.10',
   value='2.10', unit='mass%', vk='typical', meth='ASTM D3228', sha=S, pg=1)


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE C_TEC_206   DL2-12938.pdf (TDS, 2pp)   sha fcaf972e3566
# ZINC PRIMARY-SECONDARY ALKYL DITHIOPHOSPHATE; antiwear, antioxidant, corrosion inhibitor
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:C_TEC_206'
S  = 'fcaf972e3566'

_r(PK, 'component_general', 'function.primary',
   'ZINC PRIMARY-SECONDARY ALKYL DITHIOPHOSPHATE; antioxidant, antiwear, corrosion inhibitor',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title in TDS; enterprise standard Q/YHT006-2015')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (ZDDP)')
_r(PK, 'component_general', 'chemical_family',
   'Zinc primary-secondary alkyl dithiophosphate (ZDDP); primary-secondary alkyl type',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='derived from product title; primary-secondary alkyl type per title')
_m(PK, 'component_general', 'active_content',
   'not found; no active matter percentage stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; no carrier identity stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   '0.5-3.0, mass%',
   unit='mass%', lo='0.5', hi='3.0', vk='range', vc=VC_TDS_APP, sha=S, pg=1,
   entry='applications',
   notes='"mass%" explicitly stated in TDS Applications section')
_r(PK, 'component_general', 'compatibility_restrictions',
   'not suitable for the lubricants which will contact with silver-containing metal parts',
   vk='text', vc=VC_TDS_APP, sha=S, pg=1,
   notes='from Applications section in TDS')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; not stated in TDS (TBN not typical for ZDDP type)')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; not stated in TDS (ZDDP; no calcium expected)')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; not stated in TDS (ZDDP; no magnesium expected)')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus, mass%: 8.180',
   value='8.180', unit='mass%', vk='typical', meth='ASTM D5185', sha=S, pg=1)
_r(PK, 'component_general', 'function_specific_markers.zn',
   'Zinc, mass%: 8.850',
   value='8.850', unit='mass%', vk='typical', meth='ASTM D5185', sha=S, pg=1)
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; not stated in TDS (ZDDP; no molybdenum expected)')

_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Light yellow clear liquid', vk='text', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:density_kgm3_20c',
   'Density, kg/m3: 1114.0',
   value='1114.0', unit='kg/m3', vk='typical', meth='ASTM D1298', sha=S, pg=1,
   notes='test temperature 20°C per TDS')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c',
   'Flash point(COC), ℃: 150',
   value='150', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:sulfur_mass_pct',
   'Sulfur, mass%: 16.100',
   value='16.100', unit='mass%', vk='typical', meth='ASTM D129', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:ph',
   'pH: ≥5.80',
   qual='>=', lo='5.80', vk='bound', sha=S, pg=1,
   notes='enterprise test method Q/YHT006 Affix A; test temperature not stated')


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE C_TEC_209   DL2-13361.pdf (TDS/web capture, 4pp, dated 7/18/2020)   sha 5b48698eaaea
# ZINC SECONDARY ALKYL DITHIOPHOSPHATE; antiwear, antioxidant, corrosion inhibitor
# Document is a web page capture from english.tianhechem.com dated 2020-07-18
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:C_TEC_209'
S  = '5b48698eaaea'

_r(PK, 'component_general', 'function.primary',
   'ZINC SECONDARY ALKYL DITHIOPHOSPHATE; antioxidant, antiwear, corrosion inhibitor',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=2,
   notes='product title from web capture; URL: english.tianhechem.com/Products/CorrosionInhibitors/10490753.shtml; date printed: 7/18/2020')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (ZDDP secondary)')
_r(PK, 'component_general', 'chemical_family',
   'Zinc secondary alkyl dithiophosphate (ZDDP); secondary alkyl type',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=2,
   notes='derived from product title; secondary alkyl type per title; web capture source')
_m(PK, 'component_general', 'active_content',
   'not found; no active matter percentage stated in document')
_m(PK, 'component_general', 'carrier.identity',
   'not found; no carrier identity stated in document')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   '0.5-3.0, mass%',
   unit='mass%', lo='0.5', hi='3.0', vk='range', vc=VC_WEB, sha=S, pg=2,
   entry='applications',
   notes='from Applications section of web capture; same range as C_TEC_206')
_m(PK, 'component_general', 'compatibility_restrictions',
   'not found; no restriction stated in document')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; not stated in document')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; ZDDP (no calcium expected)')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; ZDDP (no magnesium expected)')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus, mass%: 7.260',
   value='7.260', unit='mass%', vk='typical', meth='ASTM D5185', vc=VC_WEB, sha=S, pg=2)
_r(PK, 'component_general', 'function_specific_markers.zn',
   'Zinc, mass%: 7.760',
   value='7.760', unit='mass%', vk='typical', meth='ASTM D5185', vc=VC_WEB, sha=S, pg=2)
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; ZDDP (no molybdenum expected)')

_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Light yellow clear liquid', vk='text', vc=VC_WEB, sha=S, pg=2)
_r(PK, 'component_general', 'not_in_template:density_kgm3_20c',
   'Density, kg/m3: 1075.0',
   value='1075.0', unit='kg/m3', vk='typical', meth='ASTM D1298', vc=VC_WEB, sha=S, pg=2,
   notes='test temperature 20°C per document; web capture source')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c',
   'Flash point(COC), ℃: 150',
   value='150', unit='°C', vk='typical', meth='ASTM D92', vc=VC_WEB, sha=S, pg=2)
_r(PK, 'component_general', 'not_in_template:sulfur_mass_pct',
   'Sulfur, mass%: 14.400',
   value='14.400', unit='mass%', vk='typical', meth='ASTM D129', vc=VC_WEB, sha=S, pg=2)
_r(PK, 'component_general', 'not_in_template:ph',
   'pH: ≥5.80',
   qual='>=', lo='5.80', vk='bound', vc=VC_WEB, sha=S, pg=2,
   notes='enterprise test method Q/YHT006 Affix A; test temperature not stated')


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE P_TEC_3232   DL2-12939.pdf (TDS, 2pp)   sha de5df90125ec
# GENERAL PURPOSE ENGINE OIL PACKAGE
# EXISTING product record: product_key = EXISTING:TIANHE_P_TEC_3232
# ──────────────────────────────────────────────────────────────────────────────
PK = 'EXISTING:TIANHE_P_TEC_3232'
S  = 'de5df90125ec'

# package_tier1
_r(PK, 'package_tier1', 'package_type_application.package_type',
   'General Purpose Engine Oil Package',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title in TDS')
_r(PK, 'package_tier1', 'package_type_application.intended_service',
   'diesel and gasoline engine oils',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='from TDS description: "general-purpose engine oil additive package '
         'for diesel and gasoline engine oils"')
for _claim, _pg, _notes in [
    ('API CF4',  2, 'TDS: "surpasses the standard engine tests of API CF4"; listed in treat rate table'),
    ('MB 228.1', 2, 'TDS: "surpasses the OEM requirements of MB 228.1 (Mercedes-Benz)"; listed in treat rate table'),
    ('API SG',   2, 'listed in treat rate table (API CF4/SG and API CF/SF rows)'),
    ('API CF',   2, 'listed in treat rate table (API CF/SF row)'),
    ('API SF',   2, 'listed in treat rate table (API CF/SF row)'),
]:
    _r(PK, 'package_tier1', 'performance_claims', _claim,
       vk='text', vc=VC_TDS_TREAT, sha=S, pg=_pg,
       entry=_claim.replace('/', '_').replace(' ', '_').replace('.', '_'),
       notes=_notes)
_r(PK, 'package_tier1', 'sae_grades_documented',
   'Multi-grade',
   vk='text', vc=VC_TDS_TREAT, sha=S, pg=2,
   notes='treat rate table column header states "Multi" (multi-grade) for all three performance rows')
_m(PK, 'package_tier1', 'permitted_base_oils_restrictions',
   'not found; no base oil restriction or preferred type stated in TDS')
_m(PK, 'package_tier1', 'route_selector_restrictions',
   'not found; not stated in TDS')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API CF4/228.1 Multi-grade: 7.10 mass%',
   value='7.10', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='CF4_228_1_multigr',
   notes='from treat rate table; column: "Total add, mass%"; grade column: Multi')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API CF4/SG Multi-grade: 6.80 mass%',
   value='6.80', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='CF4_SG_multigr',
   notes='from treat rate table; column: "Total add, mass%"; grade column: Multi')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API CF/SF Multi-grade: 4.00 mass%',
   value='4.00', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='CF_SF_multigr',
   notes='from treat rate table; column: "Total add, mass%"; grade column: Multi')
_m(PK, 'package_tier1', 'required_co_components',
   'not found explicitly; TDS notes "a compatible booster can be recommended" for '
   'applications requiring higher TBN, but no specific product or dose is named')
_m(PK, 'package_tier1', 'published_formulations',
   'not found; not stated in TDS')

# package_tier2
_r(PK, 'package_tier2', 'tbn',
   'Total base number, mg KOH/g: 131',
   value='131', unit='mgKOH/g', vk='typical', meth='ASTM D2896', sha=S, pg=1)
_m(PK, 'package_tier2', 'sulfated_ash', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Ca',
   'Calcium, mass%: 4.420',
   value='4.420', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.Mg', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Zn',
   'Zinc, mass%: 1.410',
   value='1.410', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_r(PK, 'package_tier2', 'elements.P',
   'Phosphorous, mass%: 1.290',
   value='1.290', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1,
   notes='printed as "Phosphorous" (not "Phosphorus") in TDS; recorded as printed')
_m(PK, 'package_tier2', 'elements.B', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.Mo', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.N', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.S', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'kv40', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'kv100',
   'Kinematic viscosity, mm2/s, at 100℃: 185.0',
   value='185.0', unit='mm2/s', vk='typical', meth='ASTM D445', sha=S, pg=1)
_r(PK, 'package_tier2', 'density',
   'Density, kg/m3, at 15℃: 1.0130',
   value='1.0130', unit='kg/m3', vk='typical', meth='ASTM D4052', sha=S, pg=1,
   notes='apparent unit error in TDS: value 1.0130 printed with unit "kg/m3"; '
         'physically plausible as 1.0130 g/mL = 1013.0 kg/m3; recorded as printed; '
         'unit inconsistency to be resolved at JSON conversion')
_m(PK, 'package_tier2', 'specific_gravity', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'flash_point',
   'Flash point (COC), ℃: 200',
   value='200', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_m(PK, 'package_tier2', 'pour_point', 'not found; not stated in TDS')


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE P_TEC_3234   DL2-12940.pdf (TDS, 2pp)   sha afcbf1a67b6c
# DIESEL ENGINE OIL PACKAGE
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:P_TEC_3234'
S  = 'afcbf1a67b6c'

# package_tier1
_r(PK, 'package_tier1', 'package_type_application.package_type',
   'Diesel Engine Oil Package',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title in TDS')
_r(PK, 'package_tier1', 'package_type_application.intended_service',
   'diesel engine oil; API CF level',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='from TDS description; engine validation tests: Cat 1MPC and Seq VIII stated')
_r(PK, 'package_tier1', 'performance_claims',
   'API CF',
   vk='text', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='API_CF',
   notes='from treat rate table: "API CF 3.40%"; TDS also mentions Cat 1MPC and Seq VIII engine tests')
_m(PK, 'package_tier1', 'sae_grades_documented',
   'not found; no SAE viscosity grade stated in TDS')
_m(PK, 'package_tier1', 'permitted_base_oils_restrictions',
   'not found; not stated in TDS')
_m(PK, 'package_tier1', 'route_selector_restrictions',
   'not found; not stated in TDS')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API CF: 3.40 mass%',
   value='3.40', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='CF',
   notes='from treat rate table; TDS note: "above treat rate is calculated by internal added method"')
_m(PK, 'package_tier1', 'required_co_components',
   'not found; not stated in TDS')
_m(PK, 'package_tier1', 'published_formulations',
   'not found; not stated in TDS')

# package_tier2
_r(PK, 'package_tier2', 'tbn',
   'Total base number, mg KOH/g: 161',
   value='161', unit='mgKOH/g', vk='typical', meth='ASTM D2896', sha=S, pg=1)
_m(PK, 'package_tier2', 'sulfated_ash', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Ca',
   'Calcium, mass%: 5.550',
   value='5.550', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.Mg', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Zn',
   'Zinc, mass%: 1.490',
   value='1.490', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_r(PK, 'package_tier2', 'elements.P',
   'Phosphorus, mass%: 1.340',
   value='1.340', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.B', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.Mo', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.N',
   'Nitrogen, mass%: 0.55',
   value='0.55', unit='mass%', vk='typical', meth='ASTM D5921', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.S', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'kv40', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'kv100',
   'Kinematic viscosity, mm2/s, at 100℃: 125.0',
   value='125.0', unit='mm2/s', vk='typical', meth='ASTM D445', sha=S, pg=1)
_m(PK, 'package_tier2', 'density', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'specific_gravity', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'flash_point',
   'Flash point (COC), ℃: 210',
   value='210', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_m(PK, 'package_tier2', 'pour_point', 'not found; not stated in TDS')


# ──────────────────────────────────────────────────────────────────────────────
# TIANHE P_TEC_9100   DL2-12941.pdf (TDS, 2pp)   sha 248ffefbcc1c
# PASSENGER CAR AND MOTORCYCLE ENGINE OIL PACKAGE
# ──────────────────────────────────────────────────────────────────────────────
PK = 'TIANHE:P_TEC_9100'
S  = '248ffefbcc1c'

# package_tier1
_r(PK, 'package_tier1', 'package_type_application.package_type',
   'Passenger Car and Motorcycle Engine Oil Package',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='printed as product title in TDS')
_r(PK, 'package_tier1', 'package_type_application.intended_service',
   'passenger car gasoline engine oils; motorcycle engine oils (JASO MA/MA2)',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='from TDS description and application section; JASO MA/MA2 compatibility stated')
for _claim, _notes in [
    ('API SL',   'listed in treat rate table: "API SL/CF/JASO MA/MA2"'),
    ('API CF',   'listed in treat rate table: "API SL/CF/JASO MA/MA2"'),
    ('JASO MA',  'listed in treat rate table: "API SL/CF/JASO MA/MA2"; confirmed in description'),
    ('JASO MA2', 'listed in treat rate table: "API SL/CF/JASO MA/MA2"; confirmed in description'),
    ('API SJ',   'listed in treat rate table as separate row: "API SJ 5.4%"'),
    ('API SG',   'listed in treat rate table as separate row: "API SG 5.0%"'),
]:
    _r(PK, 'package_tier1', 'performance_claims', _claim,
       vk='text', vc=VC_TDS_TREAT, sha=S, pg=2,
       entry=_claim.replace('/', '_').replace(' ', '_'),
       notes=_notes)
_m(PK, 'package_tier1', 'sae_grades_documented',
   'not found; no SAE viscosity grade (e.g. 5W-30) stated explicitly; TDS notes '
   '"can blend with non-dispersant VII for wider viscosity grades" but no SAE grade listed')
_m(PK, 'package_tier1', 'permitted_base_oils_restrictions',
   'not found; not stated in TDS')
_m(PK, 'package_tier1', 'route_selector_restrictions',
   'not found; not stated in TDS')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API SL/CF/JASO MA/MA2: 6.5 mass%',
   value='6.5', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='SL_CF_JASO_MA_MA2',
   notes='from treat rate table; note: "above treat rate is calculated by internal added method"')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API SJ: 5.4 mass%',
   value='5.4', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='SJ',
   notes='from treat rate table; calculated by internal added method')
_r(PK, 'package_tier1', 'treat_rate_matrix',
   'API SG: 5.0 mass%',
   value='5.0', unit='mass%', vk='typical', vc=VC_TDS_TREAT, sha=S, pg=2,
   entry='SG',
   notes='from treat rate table; calculated by internal added method')
_r(PK, 'package_tier1', 'required_co_components',
   'non-dispersant viscosity index improver',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes='from TDS: "can blend with non-dispersant viscosity index improver for wider '
         'viscosity grades"; no specific product or dose named; treat rates above already '
         'reflect the package portion per TDS')
_m(PK, 'package_tier1', 'published_formulations',
   'not found; not stated in TDS')

# package_tier2
_r(PK, 'package_tier2', 'tbn',
   'Total base number, mg KOH/g: 98.0',
   value='98.0', unit='mgKOH/g', vk='typical', meth='ASTM D2896', sha=S, pg=1)
_m(PK, 'package_tier2', 'sulfated_ash', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Ca',
   'Calcium, mass%: 2.950',
   value='2.950', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.Mg', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.Zn',
   'Zinc, mass%: 1.550',
   value='1.550', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_r(PK, 'package_tier2', 'elements.P',
   'Phosphorus, mass%: 1.450',
   value='1.450', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'elements.B', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.Mo', 'not found; not stated in TDS')
_m(PK, 'package_tier2', 'elements.N', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'elements.S',
   'Sulfur, mass%: 2.900',
   value='2.900', unit='mass%', vk='typical', meth='ASTM D4951', sha=S, pg=1)
_m(PK, 'package_tier2', 'kv40', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'kv100',
   'Kinematic viscosity, mm2/s, at 100℃: 115.0',
   value='115.0', unit='mm2/s', vk='typical', meth='ASTM D445', sha=S, pg=1)
_r(PK, 'package_tier2', 'density',
   'Density, kg/L, at 15°C: 0.9910',
   value='0.9910', unit='kg/L', vk='typical', meth='ASTM D4052', sha=S, pg=1,
   notes='printed unit "kg/L" is equivalent to g/mL; value 0.9910 g/mL = 991.0 kg/m3; '
         'recorded as printed')
_m(PK, 'package_tier2', 'specific_gravity', 'not found; not stated in TDS')
_r(PK, 'package_tier2', 'flash_point',
   'Flash point (COC), ℃: 210',
   value='210', unit='°C', vk='typical', meth='ASTM D92', sha=S, pg=1)
_m(PK, 'package_tier2', 'pour_point', 'not found; not stated in TDS')


# ──────────────────────────────────────────────────────────────────────────────
write_rows('s43_tianhe.csv', ROWS)
if __name__ == '__main__':
    print(f's43_tianhe: {len(ROWS)} rows written to field_evidence/s43_tianhe.csv')
