"""Field-level mapping, S35 Evonik Viscoplex (8 products, 9 TDS sheets; every sheet read in full 2026-11-15).

Sources: Evonik Viscoplex TDS / product data sheets (Evonik Industries AG / Evonik Resource Efficiency GmbH / RohMax).
Sheet format: Table 1 'Typical Physical Properties' (all 9 sheets); Table 2 'Thickening Effect at 100°C' (7-310, 8-200,
  8-251, 8-400) or 'Characteristics of typical formulations' (4-677 p.2); Table 3 'Treat Rate' (4-677 p.2).
Sheet disclaimer: "These do not constitute specifications" / "representative physical properties" (Table 1 on all sheets).
  All Table 1 numeric values are recorded as 'typical' per value_kind.

VISCOPLEX® 8-251: two editions present (DL2-11572 August 2013; DL2-14206 July 2015). Jul 2015 adds kV40 (43,100 mm²/s)
  and reports 100N baseline kV100 as 4.1 instead of 4.0 mm²/s. All other values are identical. Both rows written
  for the differing 100N baseline; Jul 2015 used as source for kV40.

VISCOPLEX® 14-520 treat rate: printed column heading says '%', value printed is '200-400 ppm'. Recorded as printed;
  flagged in notes (unit inconsistency between heading and value).

Templates per product:
  0-223, 7-310, 8-200, 8-251, 8-400: component_general + component_vm
  4-677: component_general + component_vm (formulation table and treat-rate table on p.2)
  1-254: component_general + component_ppd (stated function: pour point depressant)
  14-520: component_general only (stated function: defoamer)

Properties printed but not in any template: kV100 / kV40 of concentrate, density at 15°C, flash point, color,
  visual appearance, pumping temperature (4-677), silicon content (14-520). Written as not_in_template:<item>.

Writes field_evidence/s35_evonik.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    'c4df3a5053a2': ('DL2-13072.pdf', ''),
    'ab32453908c6': ('DL2-12585.pdf', ''),
    '738c84bd57bd': ('DL2-11266.pdf', ''),
    'e9e8d1cd6ce5': ('DL2-11600.pdf', 'July 2017'),
    'fabdd3f8f850': ('DL2-12022.pdf', ''),
    '0c92fd0f8279': ('DL2-11572.pdf', 'August 2013'),
    '2201cf07a8e8': ('DL2-14206.pdf', 'July 2015'),
    'f3789d833a0e': ('DL2-11302.pdf', ''),
    'f650c36c243f': ('DL2-13549.pdf', ''),
}

REVIEW = 'sheet read in full (text layer) 2026-11-15; parsed rows compared with the page text'
VC_T1 = 'product data sheet, Table 1 Typical Physical Properties (representative; not specifications)'
VC_FN = 'product data sheet, Function / Composition text section'
VC_T2 = 'product data sheet, Table 2 Thickening Effect at 100°C (representative)'
VC_T2F = 'product data sheet, Table 2 Characteristics of typical formulations (representative)'
VC_T3 = 'product data sheet, Table 3 Typical treat rates and % of KV100°C loss'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, rev_key=None, notes='', vc=None, entry=''):
    fname, rev = FILE[sha]
    if rev_key:
        rev = rev_key
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc or VC_T1, 'basis': '',
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
# VISCOPLEX® 0-223   DL2-13072.pdf   sha c4df3a5053a2   2pp
# VII for multigrade gear oils; PAMA in solvent-refined carrier oil
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_0_223'
S = 'c4df3a5053a2'
# component_general
_r(PK, 'component_general', 'function.primary',
   'Viscosity index and low-temperature fluidity improver for multigrade gear oils',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity',
   'solvent-refined carrier oil', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_m(PK, 'component_general', 'treat_rate',
   'treat rate not printed; product is designed for SAE 75W-90 (stated in Performance section)')
_m(PK, 'component_general', 'compatibility_restrictions')
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 0-223 is a viscous concentrate of polyalkyl methacrylate (PAMA) in a solvent-refined carrier oil',
   vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity',
   'solvent-refined carrier oil', vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_m(PK, 'component_vm', 'treat_range_by_sae_grade',
   'SAE 75W-90 stated as designed application, no treat rate printed')
_m(PK, 'component_vm', 'thickening_response',
   'Table 2 (Thickening Effect) not present in this sheet')
_r(PK, 'component_vm', 'shear_stability',
   'Shear Stability Index (P-SSI) KRL, 20 hour (CEC L-45-T-93) 40',
   value='40', vk='typical', meth='CEC L-45-T-93 KRL 20h', sha=S,
   notes='P-SSI value only; wt% of polymer in test blend not printed')
for f in ['post_shear_blend_behaviour.post_shear_kv100', 'post_shear_blend_behaviour.hths_150c',
          'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact',
          'post_shear_blend_behaviour.low_temp_gelation',
          'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure']:
    _m(PK, 'component_vm', f)
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear', sha=S)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D 1500) 2', value='2', meth='ASTM D1500', sha=S)
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity at 100°C, mm2/s (ASTM D 445) 775',
   unit='mm2/s', value='775', meth='ASTM D445', sha=S)
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15°C, g/cm3 (ASTM D 4052) 0.93',
   unit='g/cm3', value='0.93', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C PM (ASTM D 93) 135',
   unit='°C', value='135', meth='ASTM D93 (PM)', sha=S)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 1-254   DL2-12585.pdf   sha ab32453908c6   2pp
# Shear-stable PPD for engine oils, hydraulic fluids, gear oils; PAMA in highly refined neutral oil
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_1_254'
S = 'ab32453908c6'
# component_general
_r(PK, 'component_general', 'function.primary',
   'Shear-stable pour point depressant for use in engine oils, hydraulic fluids, and gear oils',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family', 'polyalkyl methacrylate', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity', 'highly refined neutral oil', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Typical addition rates are 0.1 % to 0. 3 % by weight. Higher treat rates – for example, 0.5 % to 1.0 % by weight– may be required for some gear oil formulations.',
   unit='wt%', lo='0.1', hi='0.3', vk='range', vc=VC_FN, sha=S,
   notes='second range (0.5–1.0 wt%) printed for some gear oil formulations; recorded in component_ppd.tested_dose_range_wt_pct')
_m(PK, 'component_general', 'compatibility_restrictions',
   "printed: 'Conventional pour point depressant particularly effective in lubricants formulated with solvent-refined base stocks' — effectiveness note, not an explicit restriction")
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_ppd
_r(PK, 'component_ppd', 'chemistry', 'polyalkyl methacrylate', vc=VC_FN, sha=S)
_m(PK, 'component_ppd', 'active_content')
_r(PK, 'component_ppd', 'carrier.identity', 'highly refined neutral oil', vc=VC_FN, sha=S)
_m(PK, 'component_ppd', 'carrier.share_wt_pct')
_r(PK, 'component_ppd', 'tested_dose_range_wt_pct',
   'Typical addition rates are 0.1 % to 0. 3 % by weight. Higher treat rates – for example, 0.5 % to 1.0 % by weight– may be required for some gear oil formulations.',
   unit='wt%', lo='0.1', hi='1.0', vk='range', vc=VC_FN, sha=S,
   notes='typical range 0.1–0.3%; extended range 0.5–1.0% for some gear oil formulations; both printed in Performance section')
_m(PK, 'component_ppd', 'pour_point_response')
_m(PK, 'component_ppd', 'low_temp_response')
_m(PK, 'component_ppd', 'compatibility_envelope')
_m(PK, 'component_ppd', 'addition_procedure.procedure')
_m(PK, 'component_ppd', 'addition_procedure.blend_temperature_c')
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Viscous, clear', sha=S)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D1500) 1.0', value='1.0', meth='ASTM D1500', sha=S)
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity at 100 °C, mm2/s (ASTM D445) 90',
   unit='mm2/s', value='90', meth='ASTM D445', sha=S)
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15 ° C, g/ml (ASTM D4052) 0.90',
   unit='g/ml', value='0.90', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, ° C (ASTM D3278) 160',
   unit='°C', value='160', meth='ASTM D3278', sha=S)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 4-677   DL2-11266.pdf   sha 738c84bd57bd   2pp
# Multifunctional VII+PPD for engine oils; OCP emulsion in carrier fluid
# pp.2: formulation characteristics table, treat-rate table per SAE grade
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_4_677'
S = '738c84bd57bd'
_r(PK, 'component_general', 'function.primary',
   'VISCOPLEX® 4-677 is a multifunctional engine oil additive combining the functions of viscosity index improver (VII) and pour point depressant (PPD)',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'ethylene and propylene copolymer (OCP)', vc=VC_FN, sha=S,
   notes='printed as "ethylene and propylene copolymer"; OCP identity derived from composition and product series description')
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity',
   'carrier fluid', vc=VC_FN, sha=S,
   notes='carrier identity is printed as "carrier fluid" only; no further specification in this document')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_m(PK, 'component_general', 'treat_rate',
   'treat rate stated per SAE grade in Table 3 (component_vm.treat_range_by_sae_grade); no single-dose value printed')
_m(PK, 'component_general', 'compatibility_restrictions')
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'ethylene-propylene copolymer (OCP)', vc=VC_FN, sha=S)
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 4-677 is a unique low-viscosity emulsion based on ethylene and propylene copolymer in a carrier fluid',
   vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity', 'carrier fluid', vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
# treat_range_by_sae_grade — Table 3 (p.2), one row per SAE grade
for grade, lo, hi, loss in [
    ('SAE 10W-30', '1.6', '2.0', '12'),
    ('SAE 10W-40', '3.0', '3.6', '16'),
    ('SAE 15W-40', '2.3', '2.8', '14'),
    ('SAE 15W-50', '3.7', '4.6', '18'),
    ('SAE 20W-40', '0.8', '1.1', '8'),
    ('SAE 20W-50', '1.8', '2.2', '12'),
]:
    _r(PK, 'component_vm', 'treat_range_by_sae_grade',
       f'{grade}: {lo} – {hi} % wt; KV100°C loss after 30 passes (ASTM D6278) {loss} %',
       unit='wt%', lo=lo, hi=hi, vk='range', sha=S, pg=2, vc=VC_T3, entry=grade,
       notes=f'% of KV100°C loss (ASTM D6278) also printed: {loss}%')
# thickening_response — Table 2 formulation characteristics (p.2)
for grade, dose, kv100, kv40, vi_, ccs, kv_shear, loss, mrv, hths, pp in [
    ('20W-50', '2.2', '19.2', '171.7', '127', '9200', '16.7', '12.9', '38000', '4.9', '-30'),
    ('15W-40', '2.6', '14.65', '109.9', '158', '6600', '12.6', '14.3', '25000', '4.0', '-39'),
    ('10W-40', '3.4', '14.8', '97.9', '141', '6600', '12.6', '15.4', '35000', '4.0', '-39'),
]:
    _r(PK, 'component_vm', 'thickening_response',
       f'{grade} formulation: VISCOPLEX 4-677 {dose} %wt; KV@100°C {kv100} mm2/s, KV@40°C {kv40} mm2/s, VI {vi_}; CCS {ccs} mPa·s; KV100 after shear {kv_shear} mm2/s ({loss}% loss); ASTM D4684 MRV {mrv} mPa·s; HTHS@150°C {hths} mPa·s; Pour Point {pp} °C',
       sha=S, pg=2, vc=VC_T2F, entry=grade)
# shear stability (Table 1 p.1)
_r(PK, 'component_vm', 'shear_stability',
   'Shear Stability Index (ASTM D6278) 28',
   value='28', vk='typical', meth='ASTM D6278', sha=S,
   notes='single SSI value printed; number of passes not stated in this row')
# post_shear from Table 2
_r(PK, 'component_vm', 'post_shear_blend_behaviour.post_shear_kv100',
   'KV100°C after shear (ASTM D6278): 20W-50=16.7, 15W-40=12.6, 10W-40=12.6 mm2/s',
   sha=S, pg=2, vc=VC_T2F,
   notes='from Table 2 formulation characteristics; values per SAE grade (see thickening_response rows)')
_r(PK, 'component_vm', 'post_shear_blend_behaviour.hths_150c',
   'HTHS@150°C: 20W-50=4.9, 15W-40=4.0, 10W-40=4.0 mPa·s',
   sha=S, pg=2, vc=VC_T2F)
_r(PK, 'component_vm', 'post_shear_blend_behaviour.ccs_impact',
   'CCS SAE J300 May 04: 20W-50=9200, 15W-40=6600, 10W-40=6600 mPa·s',
   sha=S, pg=2, vc=VC_T2F)
_r(PK, 'component_vm', 'post_shear_blend_behaviour.mrv_impact',
   'ASTM D4684 MRV TP-1 SAE J300 May 04: 20W-50=38000, 15W-40=25000, 10W-40=35000 mPa·s',
   sha=S, pg=2, vc=VC_T2F)
_m(PK, 'component_vm', 'post_shear_blend_behaviour.low_temp_gelation')
_m(PK, 'component_vm', 'dissolution_blend_temperature.temperature_c')
_m(PK, 'component_vm', 'dissolution_blend_temperature.procedure')
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Turbid', sha=S)
_r(PK, 'component_general', 'not_in_template:color_visual',
   'Color (visual) Brown', sha=S,
   notes='color by visual inspection, not ASTM D1500')
_r(PK, 'component_general', 'not_in_template:kv40_concentrate_cSt',
   'Viscosity at 40°C, mm2/s (ASTM D445) 7,500',
   unit='mm2/s', value='7500', meth='ASTM D445', sha=S,
   notes='printed as 7,500')
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15°C, g/cm3 (ASTM D4052) 0.90',
   unit='g/cm3', value='0.90', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C (ASTM D3278) 150',
   unit='°C', value='150', meth='ASTM D3278', sha=S)
_r(PK, 'component_general', 'not_in_template:pumping_temperature_astm_d4684',
   'Pumping Temperature (ASTM D4684)',
   sha=S, meth='ASTM D4684',
   notes='item printed in Table 1 but no value follows in the extracted text; value may be on page 2 or was not printed (OCR artefacts at top of sheet)')


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 7-310   DL2-11600.pdf   sha e9e8d1cd6ce5   2pp   July 2017
# Shear-stable VII for special hydraulic fluids; polymer in severely refined mineral oil
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_7_310'
S = 'e9e8d1cd6ce5'
_r(PK, 'component_general', 'function.primary',
   'Shear-stable viscosity index improver for special hydraulic fluids',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'polymer (type not stated in document)', vc=VC_FN, sha=S,
   notes='Composition states "VISCOPLEX® 7-310 is a polymer dissolved in severely refined mineral oil"; polymer type not named')
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity', 'severely refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_m(PK, 'component_general', 'treat_rate',
   'no single treat rate printed; thickening effect data at 5% and 10% wt in Table 2')
_m(PK, 'component_general', 'compatibility_restrictions',
   "compatibility note printed: 'designed for use in naphthenic, paraffinic, and synthetic base fluids' — not an exclusion restriction")
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'polymer (type not stated)', vc=VC_FN, sha=S,
   notes='document does not name the polymer type; product number series 7 (hydraulic shear-stable)')
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 7-310 is a polymer dissolved in severely refined mineral oil',
   vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity', 'severely refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_m(PK, 'component_vm', 'treat_range_by_sae_grade',
   'product targets hydraulic fluids (ISO VG), not SAE engine/gear grades; no ISO VG treat rate printed')
# thickening_response — Table 2 (p.1), data at 100N/150N/200N/350N base oils, 0/5/10 %wt
for bo, v0, v5, v10 in [
    ('100N',  '4.0', '5.7', '7.8'),
    ('150N',  '5.1', '7.2', '9.7'),
    ('200N',  '6.2', '8.6', '11.6'),
    ('350N',  '8.9', '12.0', '15.9'),
]:
    _r(PK, 'component_vm', 'thickening_response',
       f'Table 2 Thickening Effect at 100°C: {bo} base oil — 0% wt: {v0} mm²/s; 5% wt: {v5} mm²/s; 10% wt: {v10} mm²/s',
       sha=S, vc=VC_T2, entry=bo)
# shear stability — Table 1 (p.1)
for meth_str, val_str, entry_lbl in [
    ('ASTM D6278 30 Passes',  '4',    'D6278 30 Passes'),
    ('ASTM D6278 250 Passes', '10',   'D6278 250 Passes'),
    ('ASTM D5621 Sonic Test', '36/5.6', 'D5621 Sonic'),
    ('CEC L-45-A-99 KRL 20h', '50/5.6', 'CEC KRL 20h'),
]:
    _r(PK, 'component_vm', 'shear_stability',
       f'Shear Stability Index (P-SSI) ({meth_str}) {val_str}',
       value=val_str, vk='typical', meth=meth_str, sha=S, entry=entry_lbl,
       notes='P-SSI/wt% printed as one cell for Sonic and KRL methods (e.g. 36/5.6 means P-SSI=36, wt%=5.6)')
for f in ['post_shear_blend_behaviour.post_shear_kv100', 'post_shear_blend_behaviour.hths_150c',
          'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact',
          'post_shear_blend_behaviour.low_temp_gelation',
          'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure']:
    _m(PK, 'component_vm', f)
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance',
   'Clear, free of sediment', sha=S)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D1500) 0.5', value='0.5', meth='ASTM D1500', sha=S)
_r(PK, 'component_general', 'not_in_template:kv40_concentrate_cSt',
   'Viscosity, mm2/s (ASTM D445) at 40°C 18,800',
   unit='mm2/s', value='18800', meth='ASTM D445', sha=S, notes='printed as 18,800')
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity, mm2/s (ASTM D445) at 100°C 825',
   unit='mm2/s', value='825', meth='ASTM D445', sha=S)
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15°C, g/cm3 (ASTM D4052) 0.92',
   unit='g/cm3', value='0.92', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C (ASTM D92) >100',
   unit='°C', qual='>', value='100', vk='bound', meth='ASTM D92', sha=S)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 8-200   DL2-12022.pdf   sha fabdd3f8f850   2pp
# VII+PPD for hydraulic fluids; PAMA in highly refined mineral oil; treat rate 11.4 %wt for ISO VG 46
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_8_200'
S = 'fabdd3f8f850'
_r(PK, 'component_general', 'function.primary',
   'Viscosity index improver with pour point depressant properties for hydraulic fluids',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity', 'highly refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Typical addition rate: 11.4 % wt for ISO VG 46, VI 175',
   unit='wt%', value='11.4', vk='typical', vc=VC_FN, sha=S,
   notes='treat rate is for a specific finished oil grade (ISO VG 46, VI 175); not a general range')
_m(PK, 'component_general', 'compatibility_restrictions',
   "compatibility note: 'designed for use in formulations containing paraffinic or blends of paraffinic and naphthenic base oils'")
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 8-200 is a solution of polyalkyl methacrylate (PAMA) in highly refined mineral oil',
   vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity', 'highly refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_r(PK, 'component_vm', 'treat_range_by_sae_grade',
   'Typical addition rate: 11.4 % wt for ISO VG 46, VI 175',
   unit='wt%', value='11.4', vk='typical', vc=VC_FN, sha=S,
   notes='ISO VG 46 hydraulic grade, not SAE; treat rate is for a specific finished oil condition')
for bo, v0, v5, v10 in [
    ('100N', '4.0', '5.5', '7.4'),
    ('150N', '5.1', '7.0', '9.3'),
    ('200N', '6.2', '8.4', '11.0'),
    ('350N', '8.9', '11.9', '15.6'),
]:
    _r(PK, 'component_vm', 'thickening_response',
       f'Table 2 Thickening Effect at 100°C: {bo} base oil — 0% wt: {v0} mm²/s; 5% wt: {v5} mm²/s; 10% wt: {v10} mm²/s',
       sha=S, vc=VC_T2, entry=bo)
for meth_str, val_str, entry_lbl in [
    ('DIN 51382 30 Passes',   '0',    'DIN 51382 30 Passes'),
    ('DIN 51382 250 Passes',  '4',    'DIN 51382 250 Passes'),
    ('ASTM D5621 Sonic Test', '19/7.4', 'D5621 Sonic'),
    ('CEC L-45-A-99 KRL 20h', '39/7.4', 'CEC KRL 20h'),
]:
    _r(PK, 'component_vm', 'shear_stability',
       f'Shear Stability Index (P-SSI) ({meth_str}) {val_str}',
       value=val_str, vk='typical', meth=meth_str, sha=S, entry=entry_lbl,
       notes='P-SSI/wt% for Sonic and KRL methods; 0 for DIN 30 passes indicates negligible shear loss')
for f in ['post_shear_blend_behaviour.post_shear_kv100', 'post_shear_blend_behaviour.hths_150c',
          'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact',
          'post_shear_blend_behaviour.low_temp_gelation',
          'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure']:
    _m(PK, 'component_vm', f)
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear, free of sediment', sha=S)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D1500) 0.5', value='0.5', meth='ASTM D1500', sha=S)
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity at 100 °C, mm2/s (ASTM D445) 674',
   unit='mm2/s', value='674', meth='ASTM D445', sha=S)
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15 °C, g/cm3 (ASTM D4052) 0.94',
   unit='g/cm3', value='0.94', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C (ASTM D3278) 150',
   unit='°C', value='150', meth='ASTM D3278', sha=S)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 8-251   DL2-11572 (Aug 2013) + DL2-14206 (Jul 2015)   2pp each
# VII for hydraulic fluids; polymer in highly refined mineral oil
# Two editions; Jul 2015 adds kV40; 100N kV100 at 0% differs: 4.0 (Aug 2013) vs 4.1 (Jul 2015)
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_8_251'
S1, S2 = '0c92fd0f8279', '2201cf07a8e8'  # Aug 2013, Jul 2015
_r(PK, 'component_general', 'function.primary',
   'Viscosity index improver for hydraulic fluids',
   vc=VC_FN, sha=S2)  # use newer edition as source
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'polymer (type not stated in document)', vc=VC_FN, sha=S2,
   notes='Composition: "VISCOPLEX® 8-251 is a polymer dissolved in highly refined mineral oil"; type not named')
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity', 'highly refined mineral oil', vc=VC_FN, sha=S2)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_m(PK, 'component_general', 'treat_rate',
   'no single treat rate printed; thickening data at 5% and 10% wt in Table 2')
_m(PK, 'component_general', 'compatibility_restrictions',
   "compatibility note: 'designed for use in formulations containing paraffinic or blends of paraffinic and naphthenic base oils'")
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type',
   'polymer (type not stated)', vc=VC_FN, sha=S2)
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 8-251 is a polymer dissolved in highly refined mineral oil',
   vc=VC_FN, sha=S2)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity', 'highly refined mineral oil', vc=VC_FN, sha=S2)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_m(PK, 'component_vm', 'treat_range_by_sae_grade',
   'product targets hydraulic fluids (ISO VG); no treat rate printed')
# thickening_response — Table 2, two editions (note 100N at 0%: 4.0 Aug 2013 vs 4.1 Jul 2015)
for bo, v0_s1, v5, v10 in [
    ('150N', '5.1', '7.5', '10.7'),
    ('200N', '6.2', '9.1', '12.7'),
    ('350N', '8.9', '12.6', '17.3'),
]:
    _r(PK, 'component_vm', 'thickening_response',
       f'Table 2 Thickening Effect at 100°C: {bo} base oil — 0% wt: {v0_s1} mm²/s; 5% wt: {v5} mm²/s; 10% wt: {v10} mm²/s',
       sha=S2, vc=VC_T2, entry=bo,
       notes='values identical in both editions')
# 100N row differs between editions
_r(PK, 'component_vm', 'thickening_response',
   'Table 2 Thickening Effect at 100°C: 100N base oil — 0% wt: 4.1 mm²/s; 5% wt: 6.0 mm²/s; 10% wt: 8.6 mm²/s',
   sha=S2, vc=VC_T2, entry='100N (Jul 2015)',
   notes='100N at 0% prints 4.1 mm²/s in Jul 2015 edition; Aug 2013 edition prints 4.0 mm²/s (see alternate entry below)')
_r(PK, 'component_vm', 'thickening_response',
   'Table 2 Thickening Effect at 100°C: 100N base oil — 0% wt: 4.0 mm²/s; 5% wt: 6.0 mm²/s; 10% wt: 8.6 mm²/s',
   sha=S1, vc=VC_T2, entry='100N (Aug 2013)',
   notes='100N at 0% prints 4.0 mm²/s in Aug 2013 edition; Jul 2015 prints 4.1 mm²/s — minor discrepancy between editions')
# shear stability — same in both editions
for meth_str, val_str, entry_lbl in [
    ('DIN 51382 30 Passes',   '4',    'DIN 51382 30 Passes'),
    ('DIN 51382 250 Passes',  '10',   'DIN 51382 250 Passes'),
    ('ASTM D5621 Sonic Test', '36/6', 'D5621 Sonic'),
    ('CEC L-45-A-99 KRL 20h', '47/6', 'CEC KRL 20h'),
]:
    _r(PK, 'component_vm', 'shear_stability',
       f'Shear Stability Index (P-SSI/PSSI) ({meth_str}) {val_str}',
       value=val_str, vk='typical', meth=meth_str, sha=S2, entry=entry_lbl,
       notes='values identical in Aug 2013 and Jul 2015 editions; Jul 2015 used as source')
for f in ['post_shear_blend_behaviour.post_shear_kv100', 'post_shear_blend_behaviour.hths_150c',
          'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact',
          'post_shear_blend_behaviour.low_temp_gelation',
          'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure']:
    _m(PK, 'component_vm', f)
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance',
   'Viscous, clear', sha=S1, notes='Aug 2013 and Jul 2015 both print Viscous, clear')
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D1500) 1', value='1', meth='ASTM D1500', sha=S2)
_r(PK, 'component_general', 'not_in_template:kv40_concentrate_cSt',
   'Viscosity, mm2/s (ASTM D445) at 40°C 43,100',
   unit='mm2/s', value='43100', meth='ASTM D445', sha=S2,
   notes='kV40 printed only in Jul 2015 edition (DL2-14206); not in Aug 2013 edition (DL2-11572)')
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity at 100°C, mm2/s (ASTM D445) 1,100',
   unit='mm2/s', value='1100', meth='ASTM D445', sha=S1,
   notes='printed as 1,100; Aug 2013 and Jul 2015 both print 1,100')
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15°C, g/cm3 (ASTM D4052) 0.94',
   unit='g/cm3', value='0.94', meth='ASTM D4052', sha=S2)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C (ASTM D3278) 140',
   unit='°C', value='140', meth='ASTM D3278', sha=S2)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 8-400   DL2-11302.pdf   sha f3789d833a0e   2pp
# VII+PPD for hydraulic fluids; PAMA in highly refined mineral oil; treat rate 7.1 %wt for ISO VG 46
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_8_400'
S = 'f3789d833a0e'
_r(PK, 'component_general', 'function.primary',
   'Viscosity index improver and pour point depressant for hydraulic fluids',
   vc=VC_FN, sha=S)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family', 'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'active_content')
_r(PK, 'component_general', 'carrier.identity', 'highly refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Typical addition rate: 7.1% wt for ISO VG 46, VI 175',
   unit='wt%', value='7.1', vk='typical', vc=VC_FN, sha=S,
   notes='treat rate for a specific finished oil grade (ISO VG 46, VI 175)')
_m(PK, 'component_general', 'compatibility_restrictions',
   "compatibility note: 'designed for use in formulations containing paraffinic or blends of paraffinic and naphthenic base oils'")
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# component_vm
_r(PK, 'component_vm', 'polymer_chemistry.type', 'polyalkyl methacrylate (PAMA)', vc=VC_FN, sha=S)
_r(PK, 'component_vm', 'polymer_chemistry.form',
   'VISCOPLEX® 8-400 is a solution of polyalkyl methacrylate (PAMA) in highly refined mineral oil',
   vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.wt_pct')
_r(PK, 'component_vm', 'active_polymer.carrier_identity', 'highly refined mineral oil', vc=VC_FN, sha=S)
_m(PK, 'component_vm', 'active_polymer.carrier_share_wt_pct')
_r(PK, 'component_vm', 'treat_range_by_sae_grade',
   'Typical addition rate: 7.1% wt for ISO VG 46, VI 175',
   unit='wt%', value='7.1', vk='typical', vc=VC_FN, sha=S,
   notes='ISO VG 46 hydraulic grade; not SAE engine/gear grade')
for bo, v0, v5, v10 in [
    ('100N', '4.0', '6.2', '9.8'),
    ('150N', '5.1', '7.8', '11.4'),
    ('200N', '6.2', '9.4', '13.6'),
    ('350N', '8.9', '13.0', '18.4'),
]:
    _r(PK, 'component_vm', 'thickening_response',
       f'Table 2 Thickening Effect at 100°C: {bo} base oil — 0% wt: {v0} mm²/s; 5% wt: {v5} mm²/s; 10% wt: {v10} mm²/s',
       sha=S, vc=VC_T2, entry=bo)
for meth_str, val_str, entry_lbl in [
    ('DIN 51382 30 Passes',   '8',    'DIN 51382 30 Passes'),
    ('DIN 51382 250 Passes',  '15',   'DIN 51382 250 Passes'),
    ('ASTM D5621 Sonic Test', '43/5.7', 'D5621 Sonic'),
    ('CEC L-45-A-99 KRL 20h', '63/5.7', 'CEC KRL 20h'),
]:
    _r(PK, 'component_vm', 'shear_stability',
       f'Shear Stability Index (P-SSI) ({meth_str}) {val_str}',
       value=val_str, vk='typical', meth=meth_str, sha=S, entry=entry_lbl,
       notes='P-SSI/wt% for Sonic and KRL methods')
for f in ['post_shear_blend_behaviour.post_shear_kv100', 'post_shear_blend_behaviour.hths_150c',
          'post_shear_blend_behaviour.ccs_impact', 'post_shear_blend_behaviour.mrv_impact',
          'post_shear_blend_behaviour.low_temp_gelation',
          'dissolution_blend_temperature.temperature_c', 'dissolution_blend_temperature.procedure']:
    _m(PK, 'component_vm', f)
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear, free of sediment', sha=S)
_r(PK, 'component_general', 'not_in_template:color_astm_d1500',
   'Color (ASTM D1500) 0.5', value='0.5', meth='ASTM D1500', sha=S)
_r(PK, 'component_general', 'not_in_template:kv100_concentrate_cSt',
   'Viscosity at 100 °C, mm2/s (ASTM D445) 1,100',
   unit='mm2/s', value='1100', meth='ASTM D445', sha=S, notes='printed as 1,100')
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density at 15 °C, g/cm3 (ASTM D4052) 0.93',
   unit='g/cm3', value='0.93', meth='ASTM D4052', sha=S)
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point, °C (ASTM D3278) 140',
   unit='°C', value='140', meth='ASTM D3278', sha=S)


# ──────────────────────────────────────────────────────────────────
# VISCOPLEX® 14-520   DL2-13549.pdf   sha f650c36c243f   8pp brochure
# Defoamer (Organo-Modified Siloxane / OMS); component_general only
# ──────────────────────────────────────────────────────────────────
PK = 'EVONIK:VISCOPLEX_14_520'
S = 'f650c36c243f'
_r(PK, 'component_general', 'function.primary',
   'defoamer for lubricating oils',
   vc=VC_FN, sha=S, pg=2)
_m(PK, 'component_general', 'function.secondary')
_r(PK, 'component_general', 'chemical_family',
   'Organo-Modified Siloxane (OMS)', vc=VC_FN, sha=S, pg=2,
   notes='printed: "Based on patented Organo-Modified Siloxane (OMS) technology"')
_r(PK, 'component_general', 'active_content',
   'Active ingredient (a.i.) Approx. 8%',
   unit='%', value='8', vk='typical', sha=S, pg=3,
   notes='"Approx." prefix on the printed value; value_kind = typical')
_r(PK, 'component_general', 'carrier.identity',
   'Solvent Ester',
   sha=S, pg=3,
   notes='printed column "Solvent" with value "Ester"; likely ester-based solvent / carrier')
_m(PK, 'component_general', 'carrier.share_wt_pct')
_r(PK, 'component_general', 'treat_rate',
   'Recommended treat rate, % 200-400 ppm',
   unit='ppm', lo='200', hi='400', vk='range', vc=VC_FN, sha=S, pg=3,
   notes='column heading printed as "%", but value printed as "200-400 ppm"; recorded as printed; unit inconsistency between heading and value')
_m(PK, 'component_general', 'compatibility_restrictions')
for mk in ['tbn', 'ca', 'mg', 'p', 'zn', 'mo']:
    _m(PK, 'component_general', f'function_specific_markers.{mk}')
# not_in_template
_r(PK, 'component_general', 'not_in_template:visual_appearance', 'Clear', sha=S, pg=3)
_r(PK, 'component_general', 'not_in_template:silicon_content_ww_pct',
   'Silicon content Approx. 0.9 (w/w)%',
   unit='w/w%', value='0.9', sha=S, pg=3,
   notes='"Approx." prefix; w/w basis')
_r(PK, 'component_general', 'not_in_template:density_15c',
   'Density, 15°C Approx. 0.93 g/cm3',
   unit='g/cm3', value='0.93', sha=S, pg=3, notes='"Approx." prefix')
_r(PK, 'component_general', 'not_in_template:kv_25c_cSt',
   'Viscosity, 25°C Approx. 27 mm2/s',
   unit='mm2/s', value='27', sha=S, pg=3,
   notes='"Approx." prefix; test temperature is 25°C, not 40°C or 100°C')
_r(PK, 'component_general', 'not_in_template:flash_point_c',
   'Flash Point (ASTM D 3278) >120°C',
   unit='°C', qual='>', value='120', vk='bound', meth='ASTM D3278', sha=S, pg=3)


write_rows('s35_evonik.csv', ROWS)
print(f'Written {len(ROWS)} rows to field_evidence/s35_evonik.csv')
