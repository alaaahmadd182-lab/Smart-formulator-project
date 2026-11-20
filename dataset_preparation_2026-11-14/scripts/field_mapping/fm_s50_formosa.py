"""Field-level mapping, S50 Formosa + TOHO_CHEM LUBRAN VI-870 — 4 products, 5 documents.

Products:
  FORMOSA:BASE_OIL_GII_150N — Formosa Petrochemical Group II base oil 150N
    base_oil (tiers 1–3); 1 doc: DL2-14076 (CoQ, B/L 17 Jan 2020)
  FORMOSA:BASE_OIL_GII_500N — Formosa Petrochemical Group II base oil 500N
    base_oil (tiers 1–3); 1 doc: DL2-14080 (CoQ, B/L 18 Jan 2020)
  FORMOSA:M_25_SSI — Formosa Petrochemical M 25 SSI OCP viscosity index improver
    additive_component (component_general); 2 docs: DL2-11416 (TDS), DL2-11417 (MSDS/Kemipex)
  TOHO_CHEM:LUBRAN_VI_870 — Toho Chemical LUBRAN VI-870 PMA viscosity index improver
    additive_component (component_general); 1 doc: DL2-11661 (TDS)

Document notes:
  DL2-14076 (150N CoQ): 3-tank sample (T-9391, T-9392, T-9391(2)); typical results given;
    spec lists "SATURATES WT% 99 MIN" and "AROMATICS WT% 1 MAX" in footnote area
    (not in main spec column due to OCR layout); NOACK 15 MAX. Sulfur in ppm (10 MAX).
  DL2-14080 (500N CoQ): single-tank sample (T-9395); NOACK and WATER spec = REPORT.
    "Note: 5.0" printed above results — likely a footnote mark. OCR layout makes water
    content (ppmw) and color Saybolt ambiguous (both appear as "30" in results column);
    recorded with note.
  DL2-11416 (M25SSI TDS): "data are typical values … not to be considered as delivery spec";
    no flash point (solid polymer); CCS/RV measured at 1.0 wt% in Formosa 150N base oil.
  DL2-11417 (M25SSI MSDS, supplier Kemipex FZE): SDS document; confirms chemical composition
    Ethylene Propylene Copolymer CAS 61789-00-2, 90-100 wt%.
  DL2-11661 (LUBRAN VI-870 TDS): date 2016-06-10; density at 60°C (non-standard);
    kv100 1500 mm²/s is for neat PMA concentrate; performance data at 5 wt% in Group II oils.

Writes field_evidence/s50_formosa.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    'f992acdbaf72': ('DL2-14076.pdf', '2020-01-17'),  # 150N CoQ, B/L 17 Jan 2020
    '7c0c04f8834d': ('DL2-14080.pdf', '2020-01-18'),  # 500N CoQ, B/L 18 Jan 2020
    'dc3ea00a3343': ('DL2-11416.pdf', ''),             # M 25 SSI TDS
    '356a13758421': ('DL2-11417.pdf', ''),             # M 25 SSI MSDS (Kemipex FZE)
    'b1a14b1f1289': ('DL2-11661.pdf', '2016-06-10'),  # LUBRAN VI-870 TDS
}

REVIEW_150 = ('sheet read in full (text layer) 2026-11-16; '
              'CoQ DL2-14076, 3-tank sample; all spec and result rows read')
REVIEW_500 = ('sheet read in full (text layer) 2026-11-16; '
              'CoQ DL2-14080, 1-tank sample; all spec and result rows read')
REVIEW_SSI = ('sheets read in full (text layer) 2026-11-16; '
              '2 docs: TDS DL2-11416, MSDS DL2-11417')
REVIEW_VII = ('sheet read in full (text layer) 2026-11-16; '
              '1 doc: TDS DL2-11661')

VC_COQ_SPEC   = 'certificate of quality (CoQ), product specification'
VC_COQ_RESULT = 'certificate of quality (CoQ), batch test result'
VC_TDS        = 'product data sheet (TDS), typical properties table'
VC_MSDS       = 'material safety data sheet (MSDS), composition section'

BO150 = 'FORMOSA:BASE_OIL_GII_150N'
BO500 = 'FORMOSA:BASE_OIL_GII_500N'
SSI   = 'FORMOSA:M_25_SSI'
VII   = 'TOHO_CHEM:LUBRAN_VI_870'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_COQ_RESULT, review=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': review,
    })


def _m(pk, tmpl, field, notes_='', review=''):
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': review,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind',
                            'printed_text', 'unit', 'test_temperature_c',
                            'method', 'conditions']},
    })


def _nit(pk, prop, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
         meth='', cond='', sha='', pg=1, notes='', vc=VC_COQ_RESULT, review=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': review,
    })


def _map_base_oil(pk, sha_coq, kv100_lo, kv100_hi, vi_min, pour_max, flash_min,
                  sulfur_max_ppm,
                  density_result, kv100_result, kv40_result, vi_result,
                  pour_result, flash_result, sulfur_result_ppm,
                  saturates_result, aromatics_result,
                  noack_max, noack_result,
                  color_result, review):
    """Write base_oil tier1/2/3 and not_in_template rows for one Formosa CoQ product."""

    # ── Tier 1: Blocking ────────────────────────────────────────────────────
    _r(pk, 'base_oil_tier1', 'api_group_chemistry',
       f'FORMOSA PETROCHEMICAL CORPORATION BASE OIL {"150" if "150" in pk else "500"} N GII',
       vk='text', sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes='cargo name on CoQ explicitly states "GII"; also corroborated by spec limits '
             f'(VI {vi_min} MIN, sulfur {sulfur_max_ppm} ppm MAX, saturates 99 MIN wt%, '
             'aromatics 1 MAX wt%) consistent with API Group II classification '
             '(saturates ≥90%, aromatics <10%, sulfur <0.03%=300 ppm, VI 80-119)')

    _r(pk, 'base_oil_tier1', 'kv40',
       f'VISCOSITY @ 40°C, CST: {kv40_result} (REPORT spec — no limit stated)',
       unit='mm2/s', value=str(kv40_result), vk='report-only',
       meth='ASTM D445', cond='40°C',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes='CoQ spec column says "REPORT" (no specification limit for kv40); '
             'value is batch result')

    _r(pk, 'base_oil_tier1', 'kv100',
       f'VISCOSITY @ 100°C, CST: {kv100_lo}-{kv100_hi} (spec)',
       unit='mm2/s', lo=str(kv100_lo), hi=str(kv100_hi), vk='range',
       meth='ASTM D445',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review)
    _r(pk, 'base_oil_tier1', 'kv100',
       f'VISCOSITY @ 100°C, CST: {kv100_result}',
       unit='mm2/s', value=str(kv100_result), vk='report-only',
       meth='ASTM D445', cond='100°C',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes='batch result; CoQ spec ' + str(kv100_lo) + '-' + str(kv100_hi))

    _r(pk, 'base_oil_tier1', 'viscosity_index',
       f'VISCOSITY INDEX: {vi_min} MIN (spec)',
       lo=str(vi_min), qual='>=', vk='bound',
       meth='ASTM D2270',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review)
    _r(pk, 'base_oil_tier1', 'viscosity_index',
       f'VISCOSITY INDEX: {vi_result}',
       value=str(vi_result), vk='report-only',
       meth='ASTM D2270',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes='batch result; spec ' + str(vi_min) + ' MIN')

    _r(pk, 'base_oil_tier1', 'density',
       f'DENSITY @ 15°C, KG/L: {density_result} (REPORT spec)',
       unit='kg/L', value=str(density_result), vk='report-only',
       meth='ASTM D4052', cond='15°C',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes='CoQ spec column says "REPORT" (no limit); value is batch result at 15°C')

    _m(pk, 'base_oil_tier1', 'specific_gravity',
       'not found; CoQ reports density (kg/L) not specific gravity', review=review)
    _m(pk, 'base_oil_tier1', 'ccs',
       'not found in CoQ; CCS not a specified item in this document', review=review)

    # ── Tier 2: Verification ─────────────────────────────────────────────────
    _m(pk, 'base_oil_tier2', 'mrv',
       'not found in CoQ; MRV not a specified item in this document', review=review)

    if noack_max is not None:
        _r(pk, 'base_oil_tier2', 'noack_volatility',
           f'NOACK, WT%: {noack_max} MAX (spec)',
           unit='wt%', hi=str(noack_max), qual='<=', vk='bound',
           meth='ASTM D5800B',
           sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review)
    _r(pk, 'base_oil_tier2', 'noack_volatility',
       f'NOACK, WT%: {noack_result}' + ('' if noack_max is None else f' (spec {noack_max} MAX)'),
       unit='wt%', value=str(noack_result), vk='report-only',
       meth='ASTM D5800B',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=('CoQ spec column says "REPORT" (no limit); value is batch result'
              if noack_max is None else f'batch result; spec {noack_max} MAX'))

    _r(pk, 'base_oil_tier2', 'pour_point',
       f'POUR POINT, °C: {pour_max} MAX (spec)',
       unit='°C', hi=str(pour_max), qual='<=', vk='bound',
       meth='ASTM D5950',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review)
    _r(pk, 'base_oil_tier2', 'pour_point',
       f'POUR POINT, °C: {pour_result}',
       unit='°C', value=str(pour_result), vk='report-only',
       meth='ASTM D5950',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=f'batch result; spec {pour_max} MAX')

    _r(pk, 'base_oil_tier2', 'flash_point',
       f'FLASH POINT, °C: {flash_min} MIN (spec)',
       unit='°C', lo=str(flash_min), qual='>=', vk='bound',
       meth='ASTM D92',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review)
    _r(pk, 'base_oil_tier2', 'flash_point',
       f'FLASH POINT, °C: {flash_result}',
       unit='°C', value=str(flash_result), vk='report-only',
       meth='ASTM D92',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=f'batch result; spec {flash_min} MIN')

    # ── Tier 3: Substitution ──────────────────────────────────────────────────
    _r(pk, 'base_oil_tier3', 'sulfur',
       f'SULFUR, PPM: {sulfur_max_ppm} MAX (spec)',
       unit='ppm', hi=str(sulfur_max_ppm), qual='<=', vk='bound',
       meth='ASTM D2622',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review,
       notes='unit is ppm (not wt%); 10 ppm max = 0.001 wt% max; Group II/III threshold')
    _r(pk, 'base_oil_tier3', 'sulfur',
       f'SULFUR, PPM: {sulfur_result_ppm}',
       unit='ppm', value=str(sulfur_result_ppm), vk='report-only',
       meth='ASTM D2622',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=f'batch result; spec {sulfur_max_ppm} MAX; unit is ppm (1 ppm = 0.0001 wt%)')

    _r(pk, 'base_oil_tier3', 'saturates',
       'SATURATES, WT%: 99 MIN (spec)',
       unit='wt%', lo='99', qual='>=', vk='bound',
       meth='ASTM D7419',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review,
       notes='spec appears in footnote area of CoQ due to OCR layout; not in main spec column')
    _r(pk, 'base_oil_tier3', 'saturates',
       f'SATURATES, WT%: {saturates_result}',
       unit='wt%', value=str(saturates_result).replace('>', ''), qual='>',
       vk='report-only',
       meth='ASTM D7419',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=f'batch result printed as "{saturates_result}"; spec 99 MIN')

    _r(pk, 'base_oil_tier3', 'aromatics',
       'AROMATICS, WT%: 1 MAX (spec)',
       unit='wt%', hi='1', qual='<=', vk='bound',
       meth='ASTM D7419',
       sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review,
       notes='spec appears in footnote area of CoQ due to OCR layout; not in main spec column')
    _r(pk, 'base_oil_tier3', 'aromatics',
       f'AROMATICS, WT%: {aromatics_result}',
       unit='wt%', value=str(aromatics_result).replace('<', ''), qual='<',
       vk='report-only',
       meth='ASTM D7419',
       sha=sha_coq, pg=1, vc=VC_COQ_RESULT, review=review,
       notes=f'batch result printed as "{aromatics_result}"; spec 1 MAX')

    _m(pk, 'base_oil_tier3', 'cloud_point',
       'not found; cloud point not in CoQ specification', review=review)
    _m(pk, 'base_oil_tier3', 'wax_content',
       'not found; wax content not in CoQ specification', review=review)

    # ── not_in_template ────────────────────────────────────────────────────
    _nit(pk, 'color',
         f'COLOR: {color_result} MAX (spec), result {color_result}',
         unit='ASTM D1500', value=str(color_result).replace('L', ''), qual='<=',
         hi='0.5', vk='bound',
         meth='ASTM D1500',
         sha=sha_coq, pg=1, vc=VC_COQ_SPEC, review=review,
         notes=f'spec 0.5 MAX; result {color_result} (L prefix may denote < 0.5 on D1500 scale)')


# ===========================================================================
# FORMOSA:BASE_OIL_GII_150N
# ===========================================================================

_map_base_oil(
    pk=BO150, sha_coq='f992acdbaf72',
    kv100_lo=5.0, kv100_hi=5.6, vi_min=105, pour_max=-15, flash_min=210,
    sulfur_max_ppm=10,
    density_result=0.8550, kv100_result=5.278, kv40_result=29.79,
    vi_result=109,
    pour_result=-25, flash_result=224, sulfur_result_ppm=1.40,
    saturates_result='>99.80', aromatics_result='<0.20',
    noack_max=15, noack_result=14.3,
    color_result='L0.5',
    review=REVIEW_150,
)

_nit(BO150, 'water_content',
     'WATER CONTENT, PPMW: 100 MAX (spec), result 22.22',
     unit='ppmw', hi='100', lo='', value='22.22', qual='<=', vk='bound',
     meth='ASTM D6304',
     sha='f992acdbaf72', pg=1, vc=VC_COQ_SPEC, review=REVIEW_150,
     notes='spec 100 MAX ppmw; batch result 22.22 ppmw (T-9391); '
           'other tanks: 21.04 (T-9392), 24.71 (T-9391(2)) — all well below spec')
_nit(BO150, 'color_saybolt',
     'COLOR, SAYBOLT: REPORT spec, result 30',
     unit='Saybolt', value='30', vk='report-only',
     meth='ASTM D156',
     sha='f992acdbaf72', pg=1, vc=VC_COQ_RESULT, review=REVIEW_150,
     notes='spec says REPORT (no limit); result 30 on Saybolt color scale (all 3 tanks)')
_nit(BO150, 'appearance',
     'APPEARANCE: BRIGHT & CLEAR',
     vk='text', meth='ASTM D4176',
     sha='f992acdbaf72', pg=1, vc=VC_COQ_RESULT, review=REVIEW_150)


# ===========================================================================
# FORMOSA:BASE_OIL_GII_500N
# ===========================================================================

_map_base_oil(
    pk=BO500, sha_coq='7c0c04f8834d',
    kv100_lo=10, kv100_hi=12, vi_min=95, pour_max=-12, flash_min=230,
    sulfur_max_ppm=10,
    density_result=0.8723, kv100_result=10.34, kv40_result=89.04,
    vi_result=97,
    pour_result=-29, flash_result=248, sulfur_result_ppm=2.90,
    saturates_result='>99.80', aromatics_result='<0.20',
    noack_max=None, noack_result=17.86,
    color_result='L0.5',
    review=REVIEW_500,
)

_nit(BO500, 'color_saybolt',
     'COLOR, SAYBOLT: REPORT spec, result 30',
     unit='Saybolt', value='30', vk='report-only',
     meth='ASTM D156',
     sha='7c0c04f8834d', pg=1, vc=VC_COQ_RESULT, review=REVIEW_500,
     notes='spec REPORT (no limit); result 30 Saybolt units; OCR layout makes water '
           'content ambiguous — both water content and saybolt may appear as "30" in '
           'the results column; recorded as saybolt color based on item order in spec table')
_nit(BO500, 'appearance',
     'APPEARANCE: BRIGHT & CLEAR',
     vk='text', meth='ASTM D4176',
     sha='7c0c04f8834d', pg=1, vc=VC_COQ_RESULT, review=REVIEW_500)


# ===========================================================================
# FORMOSA:M_25_SSI — additive_component (component_general)
# ===========================================================================

_r(SSI, 'component_general', 'function.primary',
   'M 25 SSI is a shear stable amorphous olefin copolymer intended for use as a '
   'Viscosity Index Improver when formulating multi grade crankcase and industrial oils.',
   vk='text', sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI)

_m(SSI, 'component_general', 'function.secondary',
   'not found; no secondary function stated in TDS', review=REVIEW_SSI)

_r(SSI, 'component_general', 'chemical_family',
   'shear stable amorphous olefin copolymer',
   vk='text', sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
   notes='TDS description; MSDS confirms chemical identity: Ethylene Propylene Copolymer, '
         'CAS 61789-00-2 (90-100 wt%) per DL2-11417')

_r(SSI, 'component_general', 'active_content',
   'Ethylene Propylene Copolymer CAS 61789-00-2: 90-100%wt/wt',
   unit='wt%', lo='90', hi='100', vk='range',
   sha='356a13758421', pg=1, vc=VC_MSDS, review=REVIEW_SSI,
   notes='from MSDS DL2-11417, Composition section; solid polymer in bale form '
         '(no diluent carrier stated in TDS); MSDS is from Kemipex FZE (distributor), '
         'not Formosa — admitted as evidence for chemical composition')

_m(SSI, 'component_general', 'carrier.identity',
   'not found; product is a solid polymer in bale form; no carrier stated',
   review=REVIEW_SSI)
_m(SSI, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_SSI)

_m(SSI, 'component_general', 'treat_rate',
   'not found; no recommended treat rate stated in TDS; '
   'CCS and MRV measurements at 1.0 wt% in Formosa 150N are test concentrations, '
   'not recommended treat levels',
   review=REVIEW_SSI)

_r(SSI, 'component_general', 'compatibility_restrictions',
   'M 25 SSI … suitable for use as shear stable VII. '
   'Key Benefits: High shear stability, Excellent low temperature properties, '
   'Good Oil Solubility, Excellent thickening capacity, Economical.',
   vk='text', sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
   notes='no restrictions stated; product description implies broad base oil compatibility')

_m(SSI, 'component_general', 'function_specific_markers.tbn',
   'not found; OCP VM — TBN not stated', review=REVIEW_SSI)
_m(SSI, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_SSI)
_m(SSI, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_SSI)
_m(SSI, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_SSI)
_m(SSI, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_SSI)
_m(SSI, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_SSI)

# not_in_template for M_25_SSI
_nit(SSI, 'shear_stability_index',
     'DIN SSI: 23%',
     unit='%', value='23', vk='typical',
     meth='ASTM D6278',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
     notes='from Typical Properties table; "data are typical values … not to be '
           'considered as delivery specification"')
_nit(SSI, 'ethylene_content',
     'Ethylene content: 51%',
     unit='%', value='51', vk='typical',
     meth='ASTM D3900',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
     notes='from Typical Properties table')
_nit(SSI, 'molecular_weight_distribution',
     'MWD: Narrow',
     vk='text',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI)
_nit(SSI, 'ash_content',
     'Ash Content: Max 0.1%',
     unit='%', hi='0.1', qual='<=', vk='bound',
     meth='ASTM D482',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
     notes='from Typical Properties table; stated as "Max 0.1" — a spec bound')
_nit(SSI, 'ccs',
     'CCS @ -25°C: 3,400 mPa.s (1.0 wt% in Formosa 150N)',
     unit='mPa.s', value='3400', vk='typical',
     meth='ASTM D5293', cond='-25°C, 1.0 wt% in Formosa 150N',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
     notes='solution measurement at 1.0 wt% in Formosa 150N base oil, not a pure-product property')
_nit(SSI, 'mrv',
     'RV @ -30°C: 13,200 mPa.s (1.0 wt% in Formosa 150N)',
     unit='mPa.s', value='13200', vk='typical',
     meth='ASTM D4684', cond='-30°C, 1.0 wt% in Formosa 150N',
     sha='dc3ea00a3343', pg=1, vc=VC_TDS, review=REVIEW_SSI,
     notes='"RV" in document likely refers to Mini-Rotary Viscometer (MRV) measurement; '
           'solution measurement at 1.0 wt% in Formosa 150N base oil')


# ===========================================================================
# TOHO_CHEM:LUBRAN_VI_870 — additive_component (component_general)
# ===========================================================================

_r(VII, 'component_general', 'function.primary',
   'LUBRAN VI-870 is a polymethacrylate (PMA) type viscosity index improver (VII).',
   vk='text', sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII)

_r(VII, 'component_general', 'function.secondary',
   'excellent viscosity properties at low temperature with excellent shear stability '
   'for gear oil and hydraulic fluids',
   vk='text', sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
   notes='from product description; combined with primary function in one statement')

_r(VII, 'component_general', 'chemical_family',
   'polymethacrylate (PMA) type',
   vk='text', sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
   notes='chemical family stated in product description')

_m(VII, 'component_general', 'active_content',
   'not found; active polymer content % not stated; product is a neat liquid (no diluent)',
   review=REVIEW_VII)
_m(VII, 'component_general', 'carrier.identity',
   'not found; product is described as a liquid; no carrier stated',
   review=REVIEW_VII)
_m(VII, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_VII)

_r(VII, 'component_general', 'treat_rate',
   'Performance data shown at VII: 5 wt% in Group II base oils (Formosa 150N/500N, '
   'Hyundai Shell 150N/500N)',
   unit='wt%', value='5', vk='typical',
   sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
   notes='treat level from performance table; not an explicit recommended dose')

_r(VII, 'component_general', 'compatibility_restrictions',
   'Group II base oils (150N and 500N grades): Formosa, Hyundai Shell; '
   'designed for gear oil and hydraulic fluids',
   vk='text', sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
   notes='compatibility derived from performance data base oils; no restrictions explicitly stated')

_m(VII, 'component_general', 'function_specific_markers.tbn',
   'not found; PMA VII — TBN not stated', review=REVIEW_VII)
_m(VII, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_VII)
_m(VII, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_VII)
_m(VII, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_VII)
_m(VII, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_VII)
_m(VII, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_VII)

# not_in_template for LUBRAN VI-870
_nit(VII, 'kv100',
     'Kinematic Viscosity (mm2/s, 100°C): 1,500',
     unit='mm2/s', value='1500', vk='typical',
     cond='100°C',
     sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
     notes='kv100 of neat PMA concentrate; very high viscosity typical of undiluted PMA polymers')
_nit(VII, 'density',
     'Density (g/cm³, 60°C): 0.904',
     unit='g/cm3', value='0.904', vk='typical',
     cond='60°C',
     sha='b1a14b1f1289', pg=1, vc=VC_TDS, review=REVIEW_VII,
     notes='temperature is 60°C (non-standard; template density fields assume 15°C or 15.6°C)')
_nit(VII, 'shear_stability_index',
     'SSI (Sonic, JASO M347 60min): 30.2% at 5 wt% in Formosa 150N',
     unit='%', value='30.2', vk='typical',
     meth='JASO M347 (Sonic, 60min)',
     sha='b1a14b1f1289', pg=2, vc=VC_TDS, review=REVIEW_VII,
     notes='from performance table at 5 wt% in Formosa 150N (Grade A); '
           'also SSI Bosch 250pass ASTM D3945: 4.0%; SSI KRL CEC L-45-T99: 50.9%')


# ===========================================================================
write_rows('s50_formosa.csv', ROWS)
if __name__ == '__main__':
    print(f's50_formosa: {len(ROWS)} rows written to field_evidence/s50_formosa.csv')
