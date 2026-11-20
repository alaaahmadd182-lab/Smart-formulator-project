"""Field-level mapping, S41 Arkema TPS/VPS (6 products, 10 sheets; every sheet read in full 2026-11-15).

Sources: 1pp product data sheets (TDS) + SDS where available.
  TDS: DL2-14640..14645 (1pp each, no printed revision date); SDS: DL2-14646..14649 (6-12pp).
  Primary source for all Reported rows is the TDS ('TYPICAL PROPERTIES' table).
  SDS docs cited in source_file/sha256 only where SDS is the sole source for a property.

Products (all additive_component, component_general template only):
  TPS 20 / Ditertiododecyl Polysulfide     (TDS + SDS; Sulfur 20-23 %wt)
  TPS 32 / Dialkyl Penta-sulfide           (TDS + SDS; Sulphur 29-32 (23) %wt; active notation explained in notes)
  TPS 44 / Dialkyl Tri-sulfide             (TDS only; Sulfur 42-46 %wt)
  VPS 11 / Vegetable PS, Fatty Ester Trig  (TDS + SDS; Sulfur (Active) >10 (<1) %wt)
  VPS 15 / Vegetable PS, Fatty Ester Trig  (TDS + SDS; Sulfur (Active) 14.5-16.0 (8) %wt)
  VPS 17 / Vegetable PS, Fatty Ester Trig  (TDS only; Sulfur (Active) 16.0-18.0 (8) %wt)

TPS/VPS sheets contain no explicit function paragraph — function.primary is Missing for all.
No carrier oil is stated; these are neat sulfur-carrier compounds — carrier.* is Missing.
Treat rate '5% in Paraffinic Base Oil' is a 4-Ball EP test condition, not a recommended application dose.
Sulfur content (active): parenthetical value printed next to range (e.g. '29-32 (23)') — recorded as printed
  with a note; parenthetical may indicate active / freely available sulfur fraction.
EP-test footnotes (PB, PD, Load Wear Index) cite 'ASTM D2783, 5% in Paraffinic Base Oil'; recorded as conditions.

Writes field_evidence/s41_arkema.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    # sha12: (file, revision_date)
    'bfbe2bc10a5d': ('DL2-14640.pdf', ''),          # TPS 20 TDS
    '765d3a343b9d': ('DL2-14649.pdf', '2021-03-19'),  # TPS 20 SDS v2.5
    'f64497f6d4f1': ('DL2-14641.pdf', ''),          # TPS 32 TDS
    'b18b5cdacf06': ('DL2-14646.pdf', '2021-05-10'),  # TPS 32 SDS v2.4
    '96b2b1975a0c': ('DL2-14642.pdf', ''),          # TPS 44 TDS
    '946493e52804': ('DL2-14643.pdf', ''),          # VPS 11 TDS
    'b923519a3345': ('DL2-14648.pdf', '2020-10-09'),  # VPS 11 SDS v2.0
    '6d43103e60e7': ('DL2-14644.pdf', ''),          # VPS 15 TDS
    'ade4932914f2': ('DL2-14647.pdf', '2019-09-20'),  # VPS 15 SDS v1.1
    '00ad91ffe9b9': ('DL2-14645.pdf', ''),          # VPS 17 TDS
}

REVIEW = 'sheet read in full (text layer) 2026-11-15; parsed rows compared with the page text'
VC_TDS = 'product data sheet, table TYPICAL PROPERTIES'
VC_SDS = 'SDS Section 1 / product identification'

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
# Component_general fields shared across all 6 products (helper)
# ──────────────────────────────────────────────────────────────────
def _gen_missing_core(pk, chem_family_text, chem_sha):
    """Write component_general fields; function.primary and carrier.* are Missing for all."""
    _m(pk, 'component_general', 'function.primary',
       'no function paragraph printed in the TDS; product is a sulfurized EP additive by name and test data')
    _m(pk, 'component_general', 'function.secondary')
    _r(pk, 'component_general', 'chemical_family', chem_family_text, sha=chem_sha)
    _m(pk, 'component_general', 'active_content',
       'neat product; no active-ingredient percentage stated (sulfur content printed separately as not_in_template)')
    _m(pk, 'component_general', 'carrier.identity',
       'no carrier stated; product is a neat sulfur compound')
    _m(pk, 'component_general', 'carrier.share_wt_pct')
    _m(pk, 'component_general', 'treat_rate',
       "footnote prints '5% in Paraffinic Base Oil' as a 4-Ball EP test condition, not a recommended application dose")
    _m(pk, 'component_general', 'compatibility_restrictions')
    for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
        _m(pk, 'component_general', f'function_specific_markers.{mk}')


# ──────────────────────────────────────────────────────────────────
# TPS 20   DL2-14640.pdf (TDS)   sha bfbe2bc10a5d   1pp
# TPS 20 SDS   DL2-14649.pdf   sha 765d3a343b9d   12pp
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:TPS_20'
S = 'bfbe2bc10a5d'
_gen_missing_core(PK, 'tertiaryalkyl polysulfide / ditertiododecyl polysulfide', S)
# not_in_template from TDS
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear Light Yellow Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:sulfur_content_wt_pct',
   'Sulfur Content (ASTM D4794), %wt 20 - 23',
   unit='wt%', lo='20', hi='23', vk='range', meth='ASTM D4794', sha=S)
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color (ASTM D1544), Gardner 2',
   unit='Gardner', value='2', meth='ASTM D1544', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion_astm_d130',
   'Copper Corrosion (ASTM D130) ≤ 1b',
   qual='<=', value='1b', meth='ASTM D130', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point (ASTM D93, Closed Cup), ℃ ≥ 121',
   unit='℃', qual='>=', value='121', vk='bound', meth='ASTM D93 (Closed Cup)', sha=S)
_r(PK, 'component_general', 'not_in_template:specific_gravity_20c',
   'Specific Gravity@20℃ 0.950',
   value='0.950', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_20c_mPas',
   'Viscosity@20℃, mPa.s 208',
   unit='mPa.s', value='208', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_40c_mPas',
   'Viscosity@40℃, mPa.s 53',
   unit='mPa.s', value='53', sha=S)
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ -20',
   unit='℃', qual='<=', value='-20', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:refraction_index',
   'Refraction Index 1.514', value='1.514', sha=S)
_r(PK, 'component_general', 'not_in_template:vapor_pressure_20c_hPa',
   'Vapor Pressure@20℃, hPa ＜0.03',
   unit='hPa', qual='<', value='0.03', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB+ 76',
   value='76', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil',
   notes='footnote: + = 4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD+ 250',
   value='250', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index+ 50',
   value='50', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 0.78',
   unit='mm', value='0.78', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 4',
   unit='mm2', value='4', cond='300N Load', sha=S)


# ──────────────────────────────────────────────────────────────────
# TPS 32   DL2-14641.pdf (TDS)   sha f64497f6d4f1   1pp
# TPS 32 SDS   DL2-14646.pdf   sha b18b5cdacf06   12pp
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:TPS_32'
S = 'f64497f6d4f1'
_gen_missing_core(PK, 'tertiaryalkyl polysulfide / dialkyl penta-sulfide', S)
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear Yellow Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:sulfur_content_wt_pct',
   'Sulphur Content (Active), %wt 29 - 32 (23)',
   unit='wt%', lo='29', hi='32', vk='range', sha=S,
   notes='printed as "29 - 32 (23)"; parenthetical (23) may denote active/freely available sulfur fraction; recorded as printed')
_r(PK, 'component_general', 'not_in_template:color_astm_d1544',
   'Color (ASTM D1544) ≤ 10',
   qual='<=', value='10', vk='bound', meth='ASTM D1544', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point (ASTM D93, Closed Cup), ℃ > 121',
   unit='℃', qual='>', value='121', vk='bound', meth='ASTM D93 (Closed Cup)', sha=S)
_r(PK, 'component_general', 'not_in_template:density_20c',
   'Density@20℃ 1.010',
   value='1.010', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_20c_mPas',
   'Viscosity@20℃, mPa.s 603',
   unit='mPa.s', value='603', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_50c_mPas',
   'Viscosity@50℃, mpa.S 64',
   unit='mPa.s', value='64', sha=S,
   notes='printed unit "mpa.S" (mixed case); recorded as printed')
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ -20',
   unit='℃', qual='<=', value='-20', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:refraction_index',
   'Refraction Index 1.547', value='1.547', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB+ 82', value='82', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD+ 315', value='315', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index 72', value='72', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 1.07',
   unit='mm', value='1.07', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 9.7',
   unit='mm2', value='9.7', cond='300N Load', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion_pure',
   'Copper Corrosion (Pure Product)++ 4c',
   value='4c', sha=S, notes='pure product test (no dilution)')
_r(PK, 'component_general', 'not_in_template:copper_corrosion_diluted',
   'Copper Corrosion 1a - 1b (0.3)',
   lo='1a', hi='1b', vk='range', sha=S,
   notes='printed "(0.3)"; likely tested with 0.3% Dimercaptothiadiazole added (incomplete footnote in extracted text)')


# ──────────────────────────────────────────────────────────────────
# TPS 44   DL2-14642.pdf (TDS only)   sha 96b2b1975a0c   1pp
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:TPS_44'
S = '96b2b1975a0c'
_gen_missing_core(PK, 'tertiaryalkyl polysulfide / dialkyl tri-sulfide', S)
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear Light Yellow Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:sulfur_content_wt_pct',
   'Sulfur Content (ASTM D4794), %wt 42 - 46',
   unit='wt%', lo='42', hi='46', vk='range', meth='ASTM D4794', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point (ASTM D93 Closed Cup), ℃ ≥ 70',
   unit='℃', qual='>=', value='70', vk='bound', meth='ASTM D93 (Closed Cup)', sha=S)
_r(PK, 'component_general', 'not_in_template:density_20c',
   'Density@20℃ 1.010', value='1.010', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_20c_mPas',
   'Viscosity@20℃, mPa.s 4',
   unit='mPa.s', value='4', sha=S)
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ 10',
   unit='℃', qual='<=', value='10', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:melting_point_c',
   'Melting Point, ℃ ≤ 3',
   unit='℃', qual='<=', value='3', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:boiling_point_c',
   'Boiling Point, ℃ 178',
   unit='℃', value='178', sha=S)
_r(PK, 'component_general', 'not_in_template:vapor_pressure_20c_hPa',
   'Vapor Pressure@20℃, hPa < 0.1',
   unit='hPa', qual='<', value='0.1', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color (ASTM D1544), Gardner 4',
   unit='Gardner', value='4', meth='ASTM D1544', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB+ 63', value='63', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil',
   notes='footnote: + = 4 Ball EP, ASTM D2783, 5% in Paraffinic base, 5 kg 1800 rpm')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD+ 400', value='400', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index 64', value='64', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 0.85',
   unit='mm', value='0.85', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 2.6',
   unit='mm2', value='2.6', cond='300N Load', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion',
   'Copper Corrosion++ ≤ 1b',
   qual='<=', value='1b', vk='bound', sha=S,
   notes='footnote ++ not visible in extracted text; test conditions unknown')


# ──────────────────────────────────────────────────────────────────
# VPS 11   DL2-14643.pdf (TDS)   sha 946493e52804   1pp
# VPS 11 SDS   DL2-14648.pdf   sha b923519a3345   6pp
# CAS 68153-37-7 Rape oil, sulfurized
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:VPS_11'
S = 'bfbe2bc10a5d'  # will override
S = '946493e52804'
_gen_missing_core(PK, 'vegetable polysulfide / fatty ester triglyceride (rape oil sulfurized)', S)
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Light Brown Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color, Gardner < 7',
   qual='<', value='7', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_40c_cSt',
   'Viscosity@40℃, cSt 200 - 300',
   unit='cSt', lo='200', hi='300', vk='range', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_100c_cSt',
   'Viscosity@100℃, cSt 35',
   unit='cSt', value='35', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion',
   'Copper Corrosion++ ≤ 1B',
   qual='<=', value='1B', vk='bound', sha=S,
   notes='footnote ++ = 10%, 3h, 100℃ (from VPS 15 sheet; VPS 11 footnote text incomplete in this doc)')
_r(PK, 'component_general', 'not_in_template:sulfur_content_active_wt_pct',
   'Sulfur Content (Active), %wt > 10 (< 1)',
   unit='wt%', qual='>', value='10', vk='bound', sha=S,
   notes='printed "> 10 (< 1)"; parenthetical (< 1) may indicate free/active sulfur fraction; recorded as printed')
_r(PK, 'component_general', 'not_in_template:h2s_test_acetate_paper',
   'H2S Test, Acetate Paper Color < 3',
   qual='<', value='3', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:specific_gravity',
   'Specific Gravity 0.950', value='0.950', sha=S)
_r(PK, 'component_general', 'not_in_template:average_weight_lbs_gal',
   'Average Weight, lbs/gal 7.93',
   unit='lbs/gal', value='7.93', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, ℃ > 150',
   unit='℃', qual='>', value='150', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ -10',
   unit='℃', qual='<=', value='-10', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD+ 250', value='250', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB+ 80', value='80', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index 42', value='42', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 0.5',
   unit='mm', value='0.5', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 1.2',
   unit='mm2', value='1.2', cond='300N Load', sha=S)


# ──────────────────────────────────────────────────────────────────
# VPS 15   DL2-14644.pdf (TDS)   sha 6d43103e60e7   1pp
# VPS 15 SDS   DL2-14647.pdf   sha ade4932914f2   6pp
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:VPS_15'
S = '6d43103e60e7'
_gen_missing_core(PK, 'vegetable polysulfide / fatty ester triglyceride', S)
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear Brown Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color, Gardner < 6.5',
   qual='<', value='6.5', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_40c_cSt',
   'Viscosity@40℃, cSt 550 - 750',
   unit='cSt', lo='550', hi='750', vk='range', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion',
   'Copper Corrosion+ ≤ 1B',
   qual='<=', value='1B', vk='bound', sha=S,
   notes='footnote + = 10%, 3h, 100℃')
_r(PK, 'component_general', 'not_in_template:sulfur_content_active_wt_pct',
   'Sulfur Content (Active), %wt 14.5 - 16.0 (8)',
   unit='wt%', lo='14.5', hi='16.0', vk='range', sha=S,
   notes='printed "14.5 - 16.0 (8)"; parenthetical (8) may indicate free/active sulfur fraction')
_r(PK, 'component_general', 'not_in_template:h2s_test_acetate_paper',
   'H2S Test, Acetate Paper Color < 3',
   qual='<', value='3', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:specific_gravity',
   'Specific Gravity 0.980', value='0.980', sha=S)
_r(PK, 'component_general', 'not_in_template:average_weight_lbs_gal',
   'Average Weight, lbs/gal 7.9',
   unit='lbs/gal', value='7.9', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, ℃ > 100',
   unit='℃', qual='>', value='100', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ -10',
   unit='℃', qual='<=', value='-10', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD++ 400', value='400', sha=S,
   cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil',
   notes='footnote ++ = 4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB++ 80', value='80', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index++ 62', value='62', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 0.76',
   unit='mm', value='0.76', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 0.8',
   unit='mm2', value='0.8', cond='300N Load', sha=S)


# ──────────────────────────────────────────────────────────────────
# VPS 17   DL2-14645.pdf (TDS only)   sha 00ad91ffe9b9   1pp
# ──────────────────────────────────────────────────────────────────
PK = 'ARKEMA:VPS_17'
S = '00ad91ffe9b9'
_gen_missing_core(PK, 'vegetable polysulfide / fatty ester triglyceride', S)
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear Brown Fluid', sha=S)
_r(PK, 'component_general', 'not_in_template:color_gardner',
   'Color, Gardner < 5',
   qual='<', value='5', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_40c_cSt',
   'Viscosity@40℃, cSt 10 - 30',
   unit='cSt', lo='10', hi='30', vk='range', sha=S)
_r(PK, 'component_general', 'not_in_template:viscosity_100c_cSt',
   'Viscosity@100℃, cSt 5',
   unit='cSt', value='5', sha=S)
_r(PK, 'component_general', 'not_in_template:sulfur_content_active_wt_pct',
   'Sulfur Content (Active), %wt 16.0 - 18.0 (8)',
   unit='wt%', lo='16.0', hi='18.0', vk='range', sha=S,
   notes='printed "16.0 - 18.0 (8)"; parenthetical (8) likely free/active sulfur fraction')
_r(PK, 'component_general', 'not_in_template:h2s_test_acetate_paper',
   'H2S Test, Acetate Paper Color < 3',
   qual='<', value='3', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:specific_gravity',
   'Specific Gravity 0.970', value='0.970', sha=S)
_r(PK, 'component_general', 'not_in_template:average_weight_lbs_gal',
   'Average Weight, lbs/gal 7.9',
   unit='lbs/gal', value='7.9', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, ℃ > 150',
   unit='℃', qual='>', value='150', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:copper_corrosion',
   'Copper Corrosion (ASTM D130) 4a - 4c',
   lo='4a', hi='4c', vk='range', meth='ASTM D130', sha=S)
_r(PK, 'component_general', 'not_in_template:pour_point_c',
   'Pour Point, ℃ ≤ -10',
   unit='℃', qual='<=', value='-10', vk='bound', sha=S)
_r(PK, 'component_general', 'not_in_template:4ball_ep_pd',
   'PD+ 315', value='315', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_pb',
   'PB+ 63', value='63', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_ep_load_wear_index',
   'Load Wear Index 62', value='62', sha=S, cond='4 Ball EP, ASTM D2783, 5% in Paraffinic Base Oil')
_r(PK, 'component_general', 'not_in_template:4ball_wear_mm',
   '4 Ball Wear (IP239, 40kg, 1h), mm 0.72',
   unit='mm', value='0.72', meth='IP239, 40kg, 1h', sha=S)
_r(PK, 'component_general', 'not_in_template:reichert_test_mm2',
   'Reichert Test (300N Load), mm2 1.0',
   unit='mm2', value='1.0', cond='300N Load', sha=S)


write_rows('s41_arkema.csv', ROWS)
print(f'Written {len(ROWS)} rows to field_evidence/s41_arkema.csv')
