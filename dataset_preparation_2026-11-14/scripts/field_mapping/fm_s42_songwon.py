"""Field-level mapping, S42 Songwon Industrial — 4 products, 8 sheets.

All sheets read in full (text layer) 2026-11-16.

Products (all additive_component, component_general template):
  SONGNOX L107  / Octadecyl-3-(3,5-di-tert-butyl-4-hydroxyphenyl)propionate   (1 doc: TDS)
  SONGNOX L135  / C7-9-branched alkyl 3,5-di-tBu-4-OH-phenylpropionate        (3 docs: TDS, SDS, TechGuide)
  SONGNOX L570  / Mixture of octylated & butylated diphenylamine               (3 docs: TDS, SDS, TechGuide)
  SONGNOX L670  / Bis(nonylphenyl)amine                                        (1 doc: TechGuide only; no TDS/SDS)

SONGNOX 5057 LQ is excluded: material_class unresolved (polymer stabiliser application, not lubricant).

All 4 products are neat antioxidants — no carrier oil, no metallic elements.
L107 is a solid (Crystalline Powder or Semi Bead); L135, L570, L670 are liquids.

Source notes:
  TDS (L107, L135, L570): 1pp; header 'Fuel and Lubricant Additives Technical Information'.
  SDS (L135, L570): 8pp EU/GHS SDS; Section 9 provides flash point, pour/freeze point,
    kinematic viscosity (single lot value), density — all from Section 9.
  TechGuide (L135, L570, L670): ~17-20pp performance guides ('Properties and Performance
    in Lubricants', February 2024); include a 'Typical Physical Properties' table with
    General Sales Specification bounds and typical lot values.
  L670 has no standalone TDS or SDS in this batch. The TechGuide 'General Sales
    Specification' column is the only source for property bounds.

TDS is the primary source where available; TechGuide values recorded as alternate evidence
(source selection deferred to JSON conversion). SDS Section 9 values are single lot or
test values; recorded separately.

Conflict noted for SONGNOX L570 kinematic viscosity:
  TDS: 'Max. 450 cSt' (one-sided bound);
  TechGuide: '200- 450 cSt' (range, adding a lower bound);
  SDS: '353 mm²/s' (single lot value within both specs).
  TDS is the primary source; TechGuide adds a lower bound not shown in TDS; both recorded.

Writes field_evidence/s42_songwon.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    # sha12: (file_name, revision_date)
    '39192984e171': ('DL2-15398.pdf', '2020-08-04'),   # L107 TDS, dated 04.08.2020
    '2beee424c0d8': ('DL2-15756.pdf', '2020-08-04'),   # L135 TDS, dated 04.08.2020
    'a267745cb9b2': ('DL2-15720.pdf', '2022-06-28'),   # L135 SDS v3.00, Revision 28.06.2022
    '177428ad0477': ('DL2-15772.pdf', '2024-02'),      # L135 TechGuide, February 2024
    'c9d6354e1ee2': ('DL2-15703.pdf', '2022-10-20'),   # L570 TDS, dated 20.10.2022
    '0b5e839c689b': ('DL2-15719.pdf', '2022-09-08'),   # L570 SDS v4.00, Revision 08.09.2022
    'dcded1d7e1e9': ('DL2-15773.pdf', '2024-02'),      # L570 TechGuide, February 2024
    '268f43c65d34': ('DL2-15774.pdf', '2024-02'),      # L670 TechGuide, February 2024
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; parsed rows compared with the page text'
VC_TDS   = 'product data sheet, table Properties'
VC_CHARS = 'product data sheet, Characteristics & Usages section'
VC_SDS9  = 'SDS Section 9, physical and chemical properties'
VC_GUIDE_SPEC    = 'product technical guide, General Sales Specification table'
VC_GUIDE_APPS    = 'product technical guide, Applications section'
VC_GUIDE_TYPICAL = 'product technical guide, Typical Physical Properties table'

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


# ──────────────────────────────────────────────────────────────────
# SONGNOX L107   DL2-15398.pdf (TDS, 1pp)   sha 39192984e171
# Octadecyl-3-(3,5-di-tert-butyl-4-hydroxyphenyl)propionate
# Solid antioxidant (CP/SB); no SDS in this batch.
# ──────────────────────────────────────────────────────────────────
PK = 'SONGWON:SONGNOX_L107'
S = '39192984e171'

# Template fields
_r(PK, 'component_general', 'function.primary',
   'High molecular weight phenolic antioxidant for lubricants',
   vk='text', vc=VC_CHARS, sha=S, pg=1)
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (antioxidant)')
_r(PK, 'component_general', 'chemical_family',
   'Octadecyl-3-(3,5-di-tert-butyl-4-hydroxyphenyl)propionate; CAS No: 2082-79-3; Mw: 531',
   vk='text', vc=VC_TDS, sha=S, pg=1,
   notes='printed in Components section; stearyl ester of a hindered phenol')
_r(PK, 'component_general', 'active_content',
   'Min. 99.0 %', unit='%', qual='>=', lo='99.0', vk='bound', sha=S, pg=1,
   notes="printed as 'Assay (%)' in Properties table; assay represents purity of the pure-compound product")
_m(PK, 'component_general', 'carrier.identity',
   'neat compound (solid); no carrier oil stated')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_m(PK, 'component_general', 'treat_rate',
   'not found; applications listed (industrial lubricants, engine oils) but no dose printed in the TDS')
_m(PK, 'component_general', 'compatibility_restrictions')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; ashless antioxidant (no metallic elements)')

# not_in_template from TDS
_r(PK, 'component_general', 'not_in_template:melting_point_c',
   'Melting Point (°C) 50–55',
   unit='°C', lo='50', hi='55', vk='range', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:volatile_loss_pct',
   'Volatile Loss (%) Max. 0.20',
   unit='%', qual='<=', hi='0.20', vk='bound', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:color_425nm_pct',
   'Color of solution 425nm (%) Min. 97.0',
   unit='%', qual='>=', lo='97.0', vk='bound', sha=S, pg=1,
   notes='light transmittance of a solution; condition (solvent/concentration) not printed')
_r(PK, 'component_general', 'not_in_template:color_500nm_pct',
   'Color of solution 500nm (%) Min. 98.0',
   unit='%', qual='>=', lo='98.0', vk='bound', sha=S, pg=1,
   notes='light transmittance of a solution; condition (solvent/concentration) not printed')
_r(PK, 'component_general', 'not_in_template:physical_form',
   'Physical Form: CP (Crystalline Powder), SB (Semi Bead)',
   vk='text', sha=S, pg=1,
   notes='two physical forms available; no numeric value')


# ──────────────────────────────────────────────────────────────────
# SONGNOX L135   DL2-15756.pdf (TDS, 1pp)   sha 2beee424c0d8
#                DL2-15720.pdf (SDS v3.00)  sha a267745cb9b2
#                DL2-15772.pdf (TechGuide)  sha 177428ad0477
# C7-9-branched alkyl 3-(3,5-di-tBu-4-hydroxyphenyl)propionate
# ──────────────────────────────────────────────────────────────────
PK = 'SONGWON:SONGNOX_L135'
S_TDS   = '2beee424c0d8'
S_SDS   = 'a267745cb9b2'
S_GUIDE = '177428ad0477'

# Template fields (primary source: TDS; TechGuide for treat_rate)
_r(PK, 'component_general', 'function.primary',
   'Liquid high molecular weight phenolic antioxidant for lubricants',
   vk='text', vc=VC_CHARS, sha=S_TDS, pg=1)
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (antioxidant)')
_r(PK, 'component_general', 'chemical_family',
   'Benzenepropanoic acid, 3,5-bis(1,1-dimethylethyl)-4-hydroxy-, C7-9-branched alkyl esters; CAS No: 125643-61-0',
   vk='text', vc=VC_TDS, sha=S_TDS, pg=1,
   notes='printed in Components section of TDS')
_r(PK, 'component_general', 'active_content',
   'Min. 98.0 %', unit='%', qual='>=', lo='98.0', vk='bound', sha=S_TDS, pg=1,
   notes="printed as 'Assay (%)' in TDS Properties table; assay represents purity of the pure-compound product")
_m(PK, 'component_general', 'carrier.identity',
   'neat liquid; no carrier oil stated in TDS or SDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
# treat_rate: not in TDS; TechGuide page 4 (Applications) gives two application-class ranges
_r(PK, 'component_general', 'treat_rate',
   'Industrial Lubricants: 0.1 – 0.5 wt.%',
   unit='wt.%', lo='0.1', hi='0.5', vk='range',
   vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=4,
   cond='Industrial Lubricants', entry='industrial_lubricants',
   notes='typical treat rate range printed in TechGuide Applications section')
_r(PK, 'component_general', 'treat_rate',
   'Engine Oils: 0.2 – 0.8 wt.%',
   unit='wt.%', lo='0.2', hi='0.8', vk='range',
   vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=4,
   cond='Engine Oils', entry='engine_oils',
   notes='typical treat rate range printed in TechGuide Applications section')
_m(PK, 'component_general', 'compatibility_restrictions')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; ashless antioxidant (no metallic elements)')

# not_in_template from TDS (1pp)
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Yellowish Liquid',
   vk='text', sha=S_TDS, pg=1)
_r(PK, 'component_general', 'not_in_template:viscosity_cst_40c',
   'Viscosity (cSt/40°C) 95–150',
   unit='cSt', lo='95', hi='150', vk='range', sha=S_TDS, pg=1,
   notes='test temperature from column header')
_r(PK, 'component_general', 'not_in_template:sg_20c',
   'Specific Gravity (20°C) 0.950–0.990',
   lo='0.950', hi='0.990', vk='range', sha=S_TDS, pg=1)
_r(PK, 'component_general', 'not_in_template:refractive_index_20c',
   'Refractive Index (20°C) 1.493–1.499',
   lo='1.493', hi='1.499', vk='range', sha=S_TDS, pg=1)

# not_in_template from TechGuide (page 5 General Sales Specification table)
# Same KV/SG/RI spec ranges as TDS; additional properties not in TDS:
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color (Gardner) Max. 3',
   unit='Gardner', qual='<=', hi='3', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)
_r(PK, 'component_general', 'not_in_template:water_content_wt_pct',
   'Water content (wt.%) Max. 0.10',
   unit='wt.%', qual='<=', hi='0.10', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)
_r(PK, 'component_general', 'not_in_template:acid_value_mgkohg',
   'Acid value, mgKOH/g Max. 1.0',
   unit='mgKOH/g', qual='<=', hi='1.0', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)

# not_in_template from SDS Section 9 (single lot / test values)
_r(PK, 'component_general', 'not_in_template:melting_freezing_point_c',
   'Melting point/freezing point: -23 °C (ASTM D97)',
   unit='°C', value='-23', vk='typical', meth='ASTM D97',
   vc=VC_SDS9, sha=S_SDS, pg=4,
   notes='SDS describes as melting/freezing point; equivalent to pour point for this liquid')
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash point: > 175 °C (ASTM D93)',
   unit='°C', qual='>', lo='175', vk='bound', meth='ASTM D93',
   vc=VC_SDS9, sha=S_SDS, pg=4)
_r(PK, 'component_general', 'not_in_template:viscosity_mm2s_40c',
   'Kinematic viscosity at 40 °C: 112 mm²/s',
   unit='mm²/s', value='112', vk='typical',
   vc=VC_SDS9, sha=S_SDS, pg=5,
   notes='SDS Section 9 single lot value; spec range 95-150 cSt in TDS and TechGuide')
_r(PK, 'component_general', 'not_in_template:density_20c_gcm3',
   'Density at 20 °C: 0.96 g/cm³ (OECD Guideline 109)',
   unit='g/cm³', value='0.96', vk='typical', meth='OECD Guideline 109',
   vc=VC_SDS9, sha=S_SDS, pg=5,
   notes='SDS Section 9 single test value')


# ──────────────────────────────────────────────────────────────────
# SONGNOX L570   DL2-15703.pdf (TDS, 1pp)   sha c9d6354e1ee2
#                DL2-15719.pdf (SDS v4.00)  sha 0b5e839c689b
#                DL2-15773.pdf (TechGuide)  sha dcded1d7e1e9
# Mixture of octylated & butylated diphenylamine; CAS 68411-46-1
# Same CAS as SONGNOX 5057 LQ; different document header (Fuel and Lubricant Additives).
# ──────────────────────────────────────────────────────────────────
PK = 'SONGWON:SONGNOX_L570'
S_TDS   = 'c9d6354e1ee2'
S_SDS   = '0b5e839c689b'
S_GUIDE = 'dcded1d7e1e9'

# Template fields
_r(PK, 'component_general', 'function.primary',
   'Liquid octylated/butylated diphenylamine antioxidant for lubricants',
   vk='text', vc=VC_CHARS, sha=S_TDS, pg=1)
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (antioxidant)')
_r(PK, 'component_general', 'chemical_family',
   'Mixture of octylated & butylated diphenylamine; CAS No: 68411-46-1',
   vk='text', vc=VC_TDS, sha=S_TDS, pg=1,
   notes='printed in Components section of TDS; diphenylamine (DPA) type aminic antioxidant')
_m(PK, 'component_general', 'active_content',
   'not found; no assay or active-ingredient percentage stated in TDS; '
   'nitrogen content and DPA residual printed separately as not_in_template')
_m(PK, 'component_general', 'carrier.identity',
   'neat liquid; no carrier oil stated in TDS or SDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Typical treatment rate: 0.1 – 1.0 wt.%',
   unit='wt.%', lo='0.1', hi='1.0', vk='range',
   vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=4,
   notes='treat rate not stated in TDS; TechGuide Applications section gives typical range')
_m(PK, 'component_general', 'compatibility_restrictions')
# TBN: TechGuide page 5 'Typical Physical Properties' table shows Base Number.
# General Sales Specification column: 'NA'; SONGNOX L570 lot column: 182 mgKOH/g.
# Recorded as typical lot value; spec says not applicable.
_r(PK, 'component_general', 'function_specific_markers.tbn',
   'Base Number: 182 mgKOH/g (typical lot)',
   unit='mg KOH/g', value='182', vk='typical',
   vc=VC_GUIDE_TYPICAL, sha=S_GUIDE, pg=5,
   notes="TechGuide 'Typical Physical Properties' table: General Sales Specification column "
         "shows 'NA' for Base Number; SONGNOX L570 lot column shows 182; "
         "value is a typical lot measurement, not a sales specification requirement")
for _mk in ['ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; aminic antioxidant (no metallic elements)')

# not_in_template from TDS (1pp)
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Yellow to reddish brown Liquid',
   vk='text', sha=S_TDS, pg=1)
_r(PK, 'component_general', 'not_in_template:viscosity_cst_40c',
   'Viscosity (cSt/40°C) Max. 450',
   unit='cSt', qual='<=', hi='450', vk='bound', sha=S_TDS, pg=1,
   notes='one-sided upper bound; TechGuide spec shows range 200-450 cSt (see alternate row)')
_r(PK, 'component_general', 'not_in_template:nitrogen_content_pct',
   'Nitrogen content (%) 4.2 – 4.9',
   unit='%', lo='4.2', hi='4.9', vk='range', sha=S_TDS, pg=1)
_r(PK, 'component_general', 'not_in_template:sg_20c',
   'Specific Gravity (20°C) 0.960 –1.000',
   lo='0.960', hi='1.000', vk='range', sha=S_TDS, pg=1,
   notes='printed with extra space before 1.000')
_r(PK, 'component_general', 'not_in_template:refractive_index_20c',
   'Refractive Index (20°C) 1.560 –1.580',
   lo='1.560', hi='1.580', vk='range', sha=S_TDS, pg=1,
   notes='printed with extra space before 1.580')

# not_in_template from TechGuide page 5 (General Sales Specification column)
# Kinematic viscosity shows a range 200-450, conflicting with TDS upper bound Max. 450.
_r(PK, 'component_general', 'not_in_template:viscosity_cst_40c',
   'Kinematic viscosity (40C): 200- 450 cSt (General Sales Specification)',
   unit='cSt', lo='200', hi='450', vk='range',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5,
   notes='TechGuide spec adds a lower bound 200 not present in TDS Max. 450; '
         'both recorded; source selection deferred to JSON conversion; '
         'typical lot value 390 cSt also shown in TechGuide table')
_r(PK, 'component_general', 'not_in_template:dpa_residual_wt_pct',
   'DPA, wt.%: 1.0 max',
   unit='wt.%', qual='<=', hi='1.0', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5,
   notes='DPA (diphenylamine) residual; purity indicator')

# not_in_template from SDS Section 9
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash point: 154 °C (DIN 51758)',
   unit='°C', value='154', vk='typical', meth='DIN 51758',
   vc=VC_SDS9, sha=S_SDS, pg=4)
_r(PK, 'component_general', 'not_in_template:boiling_point_c',
   'Boiling point or initial boiling point: > 300 °C (OECD Guideline 103)',
   unit='°C', qual='>', lo='300', vk='bound', meth='OECD Guideline 103',
   vc=VC_SDS9, sha=S_SDS, pg=4)
_r(PK, 'component_general', 'not_in_template:viscosity_mm2s_40c',
   'Kinematic viscosity at 40 °C: 353 mm²/s',
   unit='mm²/s', value='353', vk='typical',
   vc=VC_SDS9, sha=S_SDS, pg=5,
   notes='SDS Section 9 single lot value; within TDS bound Max. 450 and TechGuide range 200-450')
_r(PK, 'component_general', 'not_in_template:density_20c_gcm3',
   'Density at 20 °C: 0.97 g/cm³ (OECD Guideline 109)',
   unit='g/cm³', value='0.97', vk='typical', meth='OECD Guideline 109',
   vc=VC_SDS9, sha=S_SDS, pg=5)
_r(PK, 'component_general', 'not_in_template:ph',
   'pH: 5.1',
   value='5.1', vk='typical',
   vc=VC_SDS9, sha=S_SDS, pg=5,
   notes='SDS Section 9; test temperature not stated')


# ──────────────────────────────────────────────────────────────────
# SONGNOX L670   DL2-15774.pdf (TechGuide, ~20pp)   sha 268f43c65d34
# Bis(nonylphenyl)amine; CAS 36878-20-3
# No TDS or SDS in this batch. All property data from TechGuide only.
# ──────────────────────────────────────────────────────────────────
PK = 'SONGWON:SONGNOX_L670'
S_GUIDE = '268f43c65d34'

# Template fields
_r(PK, 'component_general', 'function.primary',
   'Versatile antioxidant for automotive and industrial lubricants',
   vk='text', vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=3,
   notes='printed in About SONGNOX L670 section of TechGuide; no standalone TDS available in this batch')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (antioxidant)')
_r(PK, 'component_general', 'chemical_family',
   'Bis(nonylphenyl)amine (CAS No: 36878-20-3)',
   vk='text', vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=3,
   notes='printed in About section of TechGuide; DPA-subtype aminic antioxidant (dinonylated diphenylamine)')
_m(PK, 'component_general', 'active_content',
   'not found; no assay or active-ingredient percentage stated in the TechGuide; '
   'nitrogen content and DPA residual printed separately as not_in_template')
_m(PK, 'component_general', 'carrier.identity',
   'neat liquid; no carrier oil stated in TechGuide')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Typical treatment rate: 0.1 – 1.0 wt.%',
   unit='wt.%', lo='0.1', hi='1.0', vk='range',
   vc=VC_GUIDE_APPS, sha=S_GUIDE, pg=4,
   notes='only source; no TDS available; value from TechGuide Applications section')
_m(PK, 'component_general', 'compatibility_restrictions')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; no base number stated in TechGuide; aminic antioxidant')
for _mk in ['ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; aminic antioxidant (no metallic elements)')

# not_in_template from TechGuide page 5 (General Sales Specification table)
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Yellow to reddish liquid (General Sales Specification)',
   vk='text', vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5,
   notes='TechGuide spec; no standalone TDS for this product')
_r(PK, 'component_general', 'not_in_template:viscosity_cst_40c',
   'Kinematic viscosity (40C): 450- 900 cSt (General Sales Specification)',
   unit='cSt', lo='450', hi='900', vk='range',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5,
   notes='TechGuide spec; no TDS available; typical lot value 600 cSt also shown in table')
_r(PK, 'component_general', 'not_in_template:dpa_residual_wt_pct',
   'DPA, wt.%: 1.0 max',
   unit='wt.%', qual='<=', hi='1.0', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5,
   notes='DPA (diphenylamine) residual; purity indicator')
_r(PK, 'component_general', 'not_in_template:nitrogen_content_pct',
   'Total N, wt.%: 3.2 – 3.8',
   unit='wt.%', lo='3.2', hi='3.8', vk='range',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)
_r(PK, 'component_general', 'not_in_template:sg_20c',
   'Specific Gravity (20C): 0.930 – 0.980',
   lo='0.930', hi='0.980', vk='range',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)
_r(PK, 'component_general', 'not_in_template:water_content_pct',
   'Water Content, %: Max. 0.50',
   unit='%', qual='<=', hi='0.50', vk='bound',
   vc=VC_GUIDE_SPEC, sha=S_GUIDE, pg=5)


# ──────────────────────────────────────────────────────────────────
write_rows('s42_songwon.csv', ROWS)
if __name__ == '__main__':
    print(f's42_songwon: {len(ROWS)} rows written to field_evidence/s42_songwon.csv')
