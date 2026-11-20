"""Field-level mapping, S46 Cristol — 4 products, 8 sheets.

All sheets read in full (text layer) 2026-11-16.

Products (all additive_component):
  CRISTOL EPR-3400     (antioxidant)         1 doc: TDS
  CRISTOL VII-400      (VM, PMA-based)       2 docs: TDS, SDS
  CRISTOL PMA D-70     (VM, dispersant-type) 2 docs: TDS, SDS
  CRISTOL PPD LX 250   (PPD)                3 docs: SDS, brochure (Series), brochure (LX 250)

Manufacturer: Krishna Antioxidants Pvt. Ltd. (CRISTOL brand)

EPR_3400: ashless antioxidant for greases and lubricating oils; Clear liquid; no chemical
  family printed in TDS; treat rate 0.20-0.30% w/w for grease/industrial, 100-250 ppm for
  formulations; no TDS revision date visible.

VII_400: PMA-based hydraulic-oil VI improver; KV100 1200-1800 cSt product spec;
  TDS and SDS agree on KV, SG, flash point; SDS adds boiling point (>250°C).
  Shear stability: SSI=13.79, 30-cycle Bosch ASTM D6278, at 3.5% wt in ISO 32.

PMA_D_70: dispersant-type PMA VM; SDS Section 3 identifies carrier as "Solvent" (20-40%);
  Three conflicts between TDS and SDS:
    (1) Flash point: TDS >150°C vs SDS >193°C
    (2) KV100: TDS 2500-2700 cSt vs SDS 2500-2900 cSt
    (3) Density @15°C: TDS 0.91 g/ml (single) vs SDS 0.900-0.950 g/ml (range)
  TDS note: "Properties are typical for guidance only, this should not considered as specification."
  SDS note: "physical and chemical properties are typical for guidance only."
  Source selection deferred to JSON conversion.

PPD_LX_250: pour point depressant; carrier identified from SDS Section 3 as
  Distillates, petroleum, hydrotreated heavy paraffinic CAS 64742-54-7, 45.0-65.0%;
  "PMA" not stated in any document text — reviewer classification only;
  Brochure2 gives complete ASTM D97 pour point depression table (4 base stocks, 5 doses).

Writes field_evidence/s46_cristol.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    # sha12: (canonical_file, revision_date)
    '8699857a6489': ('DL2-13778.pdf', ''),           # EPR_3400 TDS, 1pp; no printed date
    '79cd58b019ef': ('DL2-13722.pdf', '2018-05-04'), # VII_400 TDS, 2pp; Date 04 May 2018
    '2b4c7987e66f': ('DL2-13723.pdf', '2018-05-08'), # VII_400 SDS v1.2; Revision 08/05/2018
    'a6630a943c7f': ('DL2-13724.pdf', '2018-11-12'), # PMA_D70 TDS, 2pp; Revision 12 Nov 2018
    '7167c81a277e': ('DL2-13725.pdf', '2019-03-26'), # PMA_D70 SDS v1.2; Revision 26/03/2019
    'c9071fa271a2': ('DL2-13666.pdf', '2020-09-07'), # PPD_LX_250 SDS v1.0; Date 07/09/2020
    'f5e80db8dd08': ('DL2-13667.pdf', ''),           # PPD_LX_250 brochure (LX Series); no date
    'e60e59342832': ('DL2-15288.pdf', ''),           # PPD_LX_250 brochure (LX 250); no date
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; parsed rows compared with the page text'
VC_TDS      = 'product data sheet, typical parameters / specifications table'
VC_TDS_DESC = 'product data sheet, product description section'
VC_TDS_PERF = 'product data sheet, performance test data table'
VC_SDS3     = 'SDS Section 3, composition / information on ingredients'
VC_SDS9     = 'SDS Section 9, physical and chemical properties'
VC_BROCHURE = 'product brochure, typical physical properties table'
VC_BROCHURE_DOSE = 'product brochure, typical dosages in finish lubricants'
VC_BROCHURE_PERF = 'product brochure, pour point depression performance table'

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
# CRISTOL EPR-3400   DL2-13778.pdf (TDS, 1pp)   sha 8699857a6489
# Antioxidant for greases and lubricating oils; ashless; clear liquid
# ──────────────────────────────────────────────────────────────────
PK = 'CRISTOL:EPR_3400'
S = '8699857a6489'

_r(PK, 'component_general', 'function.primary',
   'Antioxidant for Greases and Lubricating Oil formulations',
   vk='text', vc=VC_TDS_DESC, sha=S, pg=1,
   notes="printed under 'Fields of application' in TDS")
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (antioxidant)')
_m(PK, 'component_general', 'chemical_family',
   'not found; TDS describes product as ash-less, less volatile, non-corrosive '
   'but no chemical name or CAS number is printed')
_m(PK, 'component_general', 'active_content',
   'not found; no assay or purity stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'neat liquid; no carrier oil stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct')
# Treat rate: three application classes from TDS dosage table
_r(PK, 'component_general', 'treat_rate',
   'Grease (Lithium based) 0.20-0.30 % w/w',
   unit='% w/w', lo='0.20', hi='0.30', vk='range',
   sha=S, pg=1, entry='grease_lithium',
   notes='from dosage table in TDS; test method ASTM-D 942 (oxidative stability, 0.15 kg/cm²)')
_r(PK, 'component_general', 'treat_rate',
   'Transformer Oils / Insulating Oils / Industrial Lubricants 0.20-0.30 % w/w',
   unit='% w/w', lo='0.20', hi='0.30', vk='range',
   sha=S, pg=1, entry='transformer_insulating_industrial',
   notes='from dosage table in TDS; test method ASTM-D 2272 (100 minutes min)')
_r(PK, 'component_general', 'treat_rate',
   '100 - 250 ppm',
   unit='ppm', lo='100', hi='250', vk='range',
   sha=S, pg=1, entry='formulations_ppm',
   notes="from dosage table in TDS; row labelled 'Formulations'; IS-335 test (<0.4 mg KOH/g); "
         'IS-335 is the Indian Standard for transformer/insulating oil performance')
_m(PK, 'component_general', 'compatibility_restrictions')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; ashless antioxidant (no metallic elements)')

# not_in_template from TDS
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Clear Liquid', vk='text', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:colour_apha',
   'Colour (APHA): 100 max.',
   qual='<=', hi='100', vk='bound', unit='APHA', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:acid_no_mgkohg',
   'Acid No. (mg KOH / gm): 0.50 max.',
   qual='<=', hi='0.50', vk='bound', unit='mg KOH/g', sha=S, pg=1)
_r(PK, 'component_general', 'not_in_template:sg_25c_15_5c',
   'Specific Gravity: 0.980 - 0.992 (25°C/15.5°C)',
   lo='0.980', hi='0.992', vk='range', sha=S, pg=1,
   notes='test temperature printed as 25°C/15.5°C (reference temperature pair)')
_r(PK, 'component_general', 'not_in_template:density_gmml',
   'Density (gm / ml): 0.98',
   value='0.98', vk='typical', unit='g/ml', sha=S, pg=1,
   notes='single value; test temperature not stated explicitly; '
         'consistent with SG range 0.980-0.992 @25°C/15.5°C on same sheet')
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point: 196°C (385°F) (Pensky-Martens Closed Cup)',
   value='196', vk='typical', unit='°C', meth='Pensky-Martens Closed Cup', sha=S, pg=1)


# ──────────────────────────────────────────────────────────────────
# CRISTOL VII-400   DL2-13722.pdf (TDS, 2pp)   sha 79cd58b019ef
#                   DL2-13723.pdf (SDS v1.2)   sha 2b4c7987e66f
# PMA-based Viscosity Index Improver; hydraulic oil application
# TDS and SDS agree on KV100, SG, flash point.
# ──────────────────────────────────────────────────────────────────
PK  = 'CRISTOL:VII_400'
S_T = '79cd58b019ef'
S_S = '2b4c7987e66f'

# component_general
_r(PK, 'component_general', 'function.primary',
   'PMA Based Viscosity Index Improver',
   vk='text', vc=VC_TDS_DESC, sha=S_T, pg=1,
   notes="printed as product title in TDS")
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (VI improver)')
_r(PK, 'component_general', 'chemical_family',
   'PMA Based Viscosity Index Improver',
   vk='text', vc=VC_TDS_DESC, sha=S_T, pg=1,
   notes="'PMA Based' printed in product title and description; "
         "PMA = polymethacrylate; no explicit chemical family field in TDS")
_m(PK, 'component_general', 'active_content',
   'not found; SDS Section 3 lists "Proprietary mixture 100%" with no component breakdown')
_m(PK, 'component_general', 'carrier.identity',
   'not found; SDS Section 3 gives "Proprietary mixture 100%": no carrier component listed')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'CRISTOL VII-400 3.5% wt in ISO 32 formulation example',
   unit='wt.%', value='3.5', vk='typical', sha=S_T, pg=2,
   entry='formulation_example',
   notes='formulation example in TDS performance section: 3.5% VII-400 + 44.58% 100SN GI + '
         '51.92% 150SN GI = ISO 32 hydraulic oil; not a recommended dose range')
_m(PK, 'component_general', 'compatibility_restrictions')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; PMA VI improver (no metallic elements)')

# not_in_template from TDS
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Pale to yellow viscous liquid', vk='text', sha=S_T, pg=1)
_r(PK, 'component_general', 'not_in_template:kv100_cst',
   'Viscosity at 100°C, cSt: 1200-1800',
   lo='1200', hi='1800', vk='range', unit='cSt', sha=S_T, pg=1,
   notes='product spec range; SDS Section 9 confirms same value')
_r(PK, 'component_general', 'not_in_template:sg_25c',
   'Specific Gravity at 25°C: 0.90-0.950',
   lo='0.90', hi='0.950', vk='range', sha=S_T, pg=1,
   notes='SDS Section 9 confirms same range (0.90-0.950 @25°C)')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c',
   'Flash Point, COC: >140°C',
   qual='>', lo='140', vk='bound', unit='°C', meth='COC', sha=S_T, pg=1,
   notes='SDS Section 9 confirms same value (>140°C COC)')

# not_in_template from SDS Section 9 (adds boiling point; KV/SG/flash same as TDS)
_r(PK, 'component_general', 'not_in_template:boiling_point_c',
   'Boiling point: > 250 °C',
   qual='>', lo='250', vk='bound', unit='°C', vc=VC_SDS9, sha=S_S, pg=3,
   notes='SDS Section 9 only; not stated in TDS')

# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'PMA Based', vk='text', vc=VC_TDS_DESC, sha=S_T, pg=1,
   notes="'PMA Based Viscosity Index Improver' in TDS product title")
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'Pale to yellow viscous liquid', vk='text', sha=S_T, pg=1)
_m(PK, 'component_vm', 'active_polymer.wt_pct',
   'not found; no active polymer content stated')
_m(PK, 'component_vm', 'active_polymer.carrier_identity',
   'not found; SDS Section 3 gives "Proprietary mixture 100%": no carrier listed')
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_m(PK, 'component_vm', 'treat_range_by_sae_grade',
   'not found; hydraulic-oil VI improver — no SAE grade treat ranges stated')

# thickening_response: performance table from TDS p2 (5% dose entries)
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 6.274 cSt (5 wt.% dose in SN100 Group-I; base oil 0%: 4.193 cSt)',
   unit='cSt', value='2.081', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='SN100_GI_5pct',
   notes='delta KV100 = 6.274 - 4.193 = 2.081 cSt; both values from same performance table row; '
         'base oil SN100 Group-I; test method from table header (D445)')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 8.718 cSt (5 wt.% dose in SN150 Group-I; base oil 0%: 5.705 cSt)',
   unit='cSt', value='3.013', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='SN150_GI_5pct',
   notes='delta KV100 = 8.718 - 5.705 = 3.013 cSt; both values from same performance table row; '
         'base oil SN150 Group-I')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 8.393 cSt (10 wt.% dose in SN100 Group-I; base oil 0%: 4.193 cSt)',
   unit='cSt', value='4.200', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='SN100_GI_10pct',
   notes='delta KV100 = 8.393 - 4.193 = 4.200 cSt; base oil SN100 Group-I')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 12.00 cSt (10 wt.% dose in SN150 Group-I; base oil 0%: 5.705 cSt)',
   unit='cSt', value='6.295', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='SN150_GI_10pct',
   notes='delta KV100 = 12.00 - 5.705 = 6.295 cSt; base oil SN150 Group-I')

# shear_stability: formulation example in TDS p2
_r(PK, 'component_vm', 'shear_stability',
   'Shear Stability Index (SSI) 30-cycle Bosch: 13.79',
   value='13.79', unit='%', vk='typical', meth='ASTM D6278', sha=S_T, pg=2,
   entry='SSI_30cycle',
   notes='from formulation example (3.5% VII-400 in ISO 32); '
         'shear tests conducted by independent laboratory per TDS note')

# post_shear_blend_behaviour: after-shear KV100 from formulation example
_r(PK, 'component_vm', 'post_shear_blend_behaviour',
   'K. viscosity @ 100°C after 30-cycle Bosch shear: 6.28 cSt',
   value='6.28', unit='cSt', vk='typical', meth='ASTM D6278', sha=S_T, pg=2,
   notes='from formulation example (ISO 32, 3.5% dose); pre-shear KV100 = 6.52 cSt; '
         'viscosity loss = 3.68%; SSI = 13.79')

_m(PK, 'component_vm', 'dissolution_blend_temperature',
   'not found; handling and blending temperature not stated')


# ──────────────────────────────────────────────────────────────────
# CRISTOL PMA D-70   DL2-13724.pdf (TDS, 2pp)   sha a6630a943c7f
#                    DL2-13725.pdf (SDS v1.2)   sha 7167c81a277e
# Dispersant-type PMA VM; SDS carrier "Solvent" 20-40%;
# Three TDS vs SDS conflicts: flash, KV100, density.
# ──────────────────────────────────────────────────────────────────
PK  = 'CRISTOL:PMA_D_70'
S_T = 'a6630a943c7f'
S_S = '7167c81a277e'

# component_general
_r(PK, 'component_general', 'function.primary',
   'Dispersant type viscosity index improver; PMA based',
   vk='text', vc=VC_TDS_DESC, sha=S_T, pg=1,
   notes="product description in TDS: 'PMA based dispersant type VII which is used in the "
         "formulation of high quality lubricating oils'")
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (dispersant-type VM)')
_m(PK, 'component_general', 'chemical_family',
   "not found; TDS describes product as 'PMA based' in prose but no explicit chemical "
   "family field or CAS number is printed")
_m(PK, 'component_general', 'active_content',
   'not found; no active polymer percentage stated in TDS; SDS Section 3 identifies '
   '"Solvent (Component) 20.0-40.0%" as the only listed ingredient; active polymer share '
   'can be inferred as 60-80% but is not printed as such')

# carrier: SDS Section 3 identifies carrier as unnamed "Solvent (Component)"
_r(PK, 'component_general', 'carrier.identity',
   'Solvent (Component)',
   vk='text', vc=VC_SDS3, sha=S_S, pg=1,
   notes='SDS Section 3: "Mixture of below component with non-hazardous addition"; '
         'one component listed as "Solvent (Component)" at 20.0-40.0%; '
         'chemical identity not disclosed; Asp. Tox. 1 (H304) hazard classification')
_r(PK, 'component_general', 'carrier.share_wt_pct',
   'Solvent (Component): 20.0-40.0 %',
   unit='wt.%', lo='20.0', hi='40.0', vk='range', vc=VC_SDS3, sha=S_S, pg=1,
   notes='SDS Section 3; percentage basis: wt.% stated in SDS column heading; '
         'active polymer share implied as 60-80% but not printed as such')

_m(PK, 'component_general', 'treat_rate',
   'not found; TDS shows performance test doses (5%, 10%) and one shear test dose (7.5%) '
   'but no recommended dose range is stated')
_m(PK, 'component_general', 'compatibility_restrictions')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; PMA-type VM (no metallic elements)')

# not_in_template from TDS (primary source)
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Viscous fluid', vk='text', sha=S_T, pg=1)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D 1500): 1 Max.',
   qual='<=', hi='1', vk='bound', unit='ASTM D1500', meth='ASTM D1500', sha=S_T, pg=1)
_r(PK, 'component_general', 'not_in_template:kv100_cst_tds',
   'Viscosity at 100°C, cSt: 2500-2700',
   lo='2500', hi='2700', vk='range', unit='cSt', sha=S_T, pg=1,
   notes='TDS "typical parameters"; TDS note: "Properties are typical for guidance only, '
         'this should not considered as specification"; CONFLICT with SDS 2500-2900 cSt')
_r(PK, 'component_general', 'not_in_template:density_15c_gml_tds',
   'Density at 15°C, g/ml: 0.91',
   value='0.91', vk='typical', unit='g/ml', sha=S_T, pg=1,
   notes='TDS single value @15°C; CONFLICT with SDS range 0.900-0.950 g/ml @15°C')
_r(PK, 'component_general', 'not_in_template:flash_point_coc_c_tds',
   'Flash Point, COC: >150°C',
   qual='>', lo='150', vk='bound', unit='°C', meth='COC', sha=S_T, pg=1,
   notes='TDS value; CONFLICT with SDS >193°C')

# SDS Section 9 values (conflict source)
_r(PK, 'component_general', 'not_in_template:kv100_cst_sds',
   'Viscosity, kinematic: 2500 - 2900 cSt (@100°C)',
   lo='2500', hi='2900', vk='range', unit='cSt', vc=VC_SDS9, sha=S_S, pg=3,
   notes='SDS Section 9; CONFLICT with TDS 2500-2700 cSt; SDS note: '
         '"physical and chemical properties are typical for guidance only"')
_r(PK, 'component_general', 'not_in_template:density_15c_gml_sds',
   'Density: 0.900 - 0.950 g/ml (@15°C)',
   lo='0.900', hi='0.950', vk='range', unit='g/ml', vc=VC_SDS9, sha=S_S, pg=3,
   notes='SDS Section 9; CONFLICT with TDS 0.91 g/ml @15°C '
         '(single value vs range; SDS upper bound 0.950 vs TDS 0.91)')
_r(PK, 'component_general', 'not_in_template:flash_point_c_sds',
   'Flash point: > 193 °C',
   qual='>', lo='193', vk='bound', unit='°C', vc=VC_SDS9, sha=S_S, pg=3,
   notes='SDS Section 9; CONFLICT with TDS Flash Point COC >150°C '
         '(different test method and significantly different value; source selection deferred)')

# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'PMA Based, dispersant type',
   vk='text', vc=VC_TDS_DESC, sha=S_T, pg=1,
   notes="TDS: 'PMA based dispersant type viscosity index improver'")
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'Viscous fluid', vk='text', sha=S_T, pg=1,
   notes="printed under 'Appearance' in TDS typical parameters table")
_m(PK, 'component_vm', 'active_polymer.wt_pct',
   'not found; active polymer percentage not stated; SDS Section 3 gives carrier as '
   '20.0-40.0% implying active polymer ~60-80% but not printed as such')

# active_polymer carrier from SDS Section 3 (same carrier as component_general)
_r(PK, 'component_vm', 'active_polymer.carrier_identity',
   'Solvent (Component)',
   vk='text', vc=VC_SDS3, sha=S_S, pg=1,
   notes='SDS Section 3: carrier listed as "Solvent (Component)"; chemical identity not disclosed')
_r(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct',
   'Solvent (Component): 20.0-40.0 %',
   unit='wt.%', lo='20.0', hi='40.0', vk='range', vc=VC_SDS3, sha=S_S, pg=1,
   notes='SDS Section 3 component percentage; wt.% basis from SDS column heading')

_m(PK, 'component_vm', 'treat_range_by_sae_grade',
   'not found; no SAE grade treat ranges stated')

# thickening_response: performance data from TDS p2 (5% dose, Group-II base oils)
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 9.8 cSt (5 wt.% dose in 100N Group-II; base oil 0%: 4.95 cSt)',
   unit='cSt', value='4.85', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='100N_GII_5pct',
   notes='delta KV100 = 9.8 - 4.95 = 4.85 cSt; base oil 100N Group-II')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 11.92 cSt (5 wt.% dose in 150N Group-II; base oil 0%: 6.2 cSt)',
   unit='cSt', value='5.72', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='150N_GII_5pct',
   notes='delta KV100 = 11.92 - 6.2 = 5.72 cSt; base oil 150N Group-II')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 18.92 cSt (10 wt.% dose in 100N Group-II; base oil 0%: 4.95 cSt)',
   unit='cSt', value='13.97', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='100N_GII_10pct',
   notes='delta KV100 = 18.92 - 4.95 = 13.97 cSt; base oil 100N Group-II')
_r(PK, 'component_vm', 'thickening_response',
   'K. Viscosity @ 100°C: 21.9 cSt (10 wt.% dose in 150N Group-II; base oil 0%: 6.2 cSt)',
   unit='cSt', value='15.70', vk='typical', meth='D445', sha=S_T, pg=2,
   entry='150N_GII_10pct',
   notes='delta KV100 = 21.9 - 6.2 = 15.70 cSt; base oil 150N Group-II')

# shear_stability: TDS shear stability test at 7.5% in 150N GII
_r(PK, 'component_vm', 'shear_stability',
   'Shear Stability Index (SSI) 30-cycle Bosch: 28.93',
   value='28.93', unit='%', vk='typical', meth='ASTM D6278', sha=S_T, pg=2,
   entry='SSI_30cycle',
   notes='from TDS shear stability test: 7.5% PMA D-70 in 150N GII; '
         'initial KV100 = 14.67 cSt; shear tests by independent laboratory per TDS note')
_r(PK, 'component_vm', 'shear_stability',
   'Shear Stability Index (SSI) 250-cycle Bosch: 48.06',
   value='48.06', unit='%', vk='typical', meth='ASTM D6278', sha=S_T, pg=2,
   entry='SSI_250cycle',
   notes='from TDS shear stability test: 7.5% PMA D-70 in 150N GII; 250-cycle Bosch ASTM D6278')

_m(PK, 'component_vm', 'post_shear_blend_behaviour',
   'not found; after-shear KV100 not given explicitly; SSI values given (28.93% at 30-cycle, '
   '48.06% at 250-cycle ASTM D6278) but after-shear viscosity not printed')
_m(PK, 'component_vm', 'dissolution_blend_temperature',
   'not found; handling and blending temperature not stated')


# ──────────────────────────────────────────────────────────────────
# CRISTOL PPD LX 250   DL2-13666.pdf (SDS v1.0)       sha c9071fa271a2
#                      DL2-13667.pdf (brochure, Series) sha f5e80db8dd08
#                      DL2-15288.pdf (brochure, LX 250) sha e60e59342832
# Pour point depressant; carrier identified from SDS Section 3
# "PMA" not stated in documents; pour point response table from brochure2
# ──────────────────────────────────────────────────────────────────
PK   = 'CRISTOL:PPD_LX_250'
S_SD = 'c9071fa271a2'
S_B1 = 'f5e80db8dd08'
S_B2 = 'e60e59342832'

# component_general
_r(PK, 'component_general', 'function.primary',
   'Flow Improver for Automotive Lubricants; Pour Point Depressant',
   vk='text', vc=VC_BROCHURE, sha=S_B2, pg=1,
   notes='product title from brochure; SDS type-of-product: "Pour point depressant"')
_m(PK, 'component_general', 'function.secondary',
   'not found; product described by a single primary function (PPD / flow improver)')
_m(PK, 'component_general', 'chemical_family',
   "not found; mechanism description in brochures is consistent with PMA-type PPD "
   "but 'PMA' or 'polymethacrylate' is not explicitly printed in any document; "
   "reviewer classification only (s46_cristol.json note)")
_m(PK, 'component_general', 'active_content',
   'not found; active polymer content not stated; carrier share 45-65% from SDS Section 3 '
   'implies active polymer ~35-55% but not printed as such')

# carrier: SDS Section 3 identifies carrier explicitly
_r(PK, 'component_general', 'carrier.identity',
   'Distillates, petroleum, hydrotreated heavy paraffinic; CAS No. 64742-54-7',
   vk='text', vc=VC_SDS3, sha=S_SD, pg=1,
   notes='SDS Section 3 component: "Distillates, petroleum, hydrotreated heavy paraffinic '
         '(Component); CAS No. 64742-54-7"; Group I/II base stock diluent; Asp. Tox. 1 (H304)')
_r(PK, 'component_general', 'carrier.share_wt_pct',
   'Distillates, petroleum, hydrotreated heavy paraffinic: 45.0-65.0 %',
   unit='wt.%', lo='45.0', hi='65.0', vk='range', vc=VC_SDS3, sha=S_SD, pg=1,
   notes='SDS Section 3; wt.% basis from SDS column heading')

# treat_rate: two application classes from both brochures (same values)
_r(PK, 'component_general', 'treat_rate',
   'Engine Oils: 0.1 - 0.5 % w/w',
   unit='% w/w', lo='0.1', hi='0.5', vk='range',
   vc=VC_BROCHURE_DOSE, sha=S_B2, pg=1, entry='engine_oils',
   notes='from brochure2; same values in brochure1 (Series)')
_r(PK, 'component_general', 'treat_rate',
   'Gear Oils: 0.2 - 1.5 % w/w',
   unit='% w/w', lo='0.2', hi='1.5', vk='range',
   vc=VC_BROCHURE_DOSE, sha=S_B2, pg=1, entry='gear_oils',
   notes='from brochure2; same values in brochure1 (Series)')

_m(PK, 'component_general', 'compatibility_restrictions',
   'not found; brochure states "completely soluble in all new generation base stocks" '
   'but no incompatibility or restriction listed')
for _mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{_mk}',
       'not found; PPD additive (no metallic elements)')

# not_in_template from SDS Section 9
_r(PK, 'component_general', 'not_in_template:appearance',
   'Appearance: Organic viscous liquid; Colour: Yellow to amber',
   vk='text', vc=VC_SDS9, sha=S_SD, pg=3)
_r(PK, 'component_general', 'not_in_template:sg_25c',
   '0.86 - 0.90 (@25°C)',
   lo='0.86', hi='0.90', vk='range', vc=VC_SDS9, sha=S_SD, pg=3,
   notes='SDS field header "Specific gravity"; same range in both brochures')
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash point: > 120 °C',
   qual='>', lo='120', vk='bound', unit='°C', vc=VC_SDS9, sha=S_SD, pg=3,
   notes='same value in SDS and both brochures')
_r(PK, 'component_general', 'not_in_template:kv40_cst',
   'Viscosity, kinematic: 955 cSt (@40°C)',
   value='955', vk='typical', unit='cSt', vc=VC_SDS9, sha=S_SD, pg=3,
   notes='SDS Section 9; "typical for guidance only"; brochure gives KV100 >100 cSt only')
_r(PK, 'component_general', 'not_in_template:kv100_cst',
   'Viscosity, kinematic (calculated value) (100°C): > 100 cSt',
   qual='>', lo='100', vk='bound', unit='cSt', vc=VC_SDS9, sha=S_SD, pg=3,
   notes='SDS calculated entry; same bound in brochures ("Viscosity @ 100°C: >100 cst")')

# component_ppd
_m(PK, 'component_ppd', 'chemistry',
   "not found; 'PMA' or 'polymethacrylate' not printed in any document; "
   "reviewer classification only")
_m(PK, 'component_ppd', 'active_content',
   'not found; active polymer content not stated explicitly')

# carrier in component_ppd (same as component_general)
_r(PK, 'component_ppd', 'carrier.identity',
   'Distillates, petroleum, hydrotreated heavy paraffinic; CAS No. 64742-54-7',
   vk='text', vc=VC_SDS3, sha=S_SD, pg=1,
   notes='SDS Section 3; same as component_general carrier.identity')
_r(PK, 'component_ppd', 'carrier.share_wt_pct',
   'Distillates, petroleum, hydrotreated heavy paraffinic: 45.0-65.0 %',
   unit='wt.%', lo='45.0', hi='65.0', vk='range', vc=VC_SDS3, sha=S_SD, pg=1,
   notes='SDS Section 3; wt.% basis')

# tested_dose_range_wt_pct: from brochure2 performance table (doses 0.00-1.00%)
_r(PK, 'component_ppd', 'tested_dose_range_wt_pct',
   'Doses in ASTM D97 pour point table: 0.00, 0.10, 0.25, 0.50, 1.00 %',
   unit='wt.%', lo='0.00', hi='1.00', vk='range', meth='ASTM D97',
   vc=VC_BROCHURE_PERF, sha=S_B2, pg=2,
   notes='five dose levels in pour point depression table; '
         'ASTM D97 test method stated in brochure')

# pour_point_response: 4 base oils × 4 non-zero doses = 16 entries
# Base oils from brochure2 table (ASTM D97): Core 100 GI, Core 600 GI,
#   Chevron 100R GII, Flint Hill-230 HC GII
# Base oil pour points (0% dose): Core100=-21, Core600=-6, Chev100R=-12, FH230=-15
# Change = PP_at_dose - PP_at_zero_dose (both values on same page; calculation noted)

for _dose, _c100, _c600, _ch100r, _fh230 in [
        ('0.10', -21-(-21), -12-(-6), -27-(-12), -30-(-15)),   # 0, -6, -15, -15
        ('0.25', -27-(-21), -18-(-6), -30-(-12), -30-(-15)),   # -6, -12, -18, -15
        ('0.50', -30-(-21), -21-(-6), -33-(-12), -33-(-15)),   # -9, -15, -21, -18
        ('1.00', -30-(-21), -24-(-6), -36-(-12), -36-(-15)),   # -9, -18, -24, -21
]:
    for _oil, _delta, _pp_base, _pp_dose in [
        ('Core 100 Group-I',         _c100,   -21, -21 + _c100),
        ('Core 600 Group-I',         _c600,    -6,  -6 + _c600),
        ('Chevron 100R Group-II',    _ch100r, -12, -12 + _ch100r),
        ('Flint Hill-230 HC Group-II', _fh230, -15, -15 + _fh230),
    ]:
        _safe_oil = _oil.replace(' ', '_').replace('-', '_')
        _r(PK, 'component_ppd', 'pour_point_response',
           f'{_oil}; dose={_dose}%: PP={_pp_dose}°C (base={_pp_base}°C)',
           value=str(_delta), unit='°C', vk='typical', meth='ASTM D97',
           vc=VC_BROCHURE_PERF, sha=S_B2, pg=2,
           entry=f'{_safe_oil}_{_dose.replace(".", "_")}pct',
           notes=f'delta PP = {_pp_dose} - {_pp_base} = {_delta}°C; '
                 'both values from same pour point depression table in brochure2; '
                 'ASTM D97 test method stated')

_m(PK, 'component_ppd', 'low_temp_response',
   'not found; no MRV, CCS or yield stress data in any document')
_m(PK, 'component_ppd', 'compatibility_envelope',
   'brochure states "completely soluble in all new generation base stocks" but no '
   'specific wax system or base oil compatibility envelope is detailed; '
   'four base stocks used in ASTM D97 test (Core 100 GI, Core 600 GI, Chevron 100R GII, '
   'Flint Hill-230 HC GII) indicate broad compatibility but not an enumerated envelope')
_m(PK, 'component_ppd', 'addition_procedure',
   'not found; handling instructions refer to SDS only; no blend procedure or temperature stated')


# ──────────────────────────────────────────────────────────────────
write_rows('s46_cristol.csv', ROWS)
if __name__ == '__main__':
    print(f's46_cristol: {len(ROWS)} rows written to field_evidence/s46_cristol.csv')
