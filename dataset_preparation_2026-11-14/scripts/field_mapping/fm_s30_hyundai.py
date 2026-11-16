"""Field-level mapping, S30 Hyundai Oil Bank — 1 product, 2 documents.

Supplier: Hyundai and Shell Base Oil Co., Ltd. (Daesan, South Korea — Hyundai Oil Bank/Shell JV).
Product is a base oil with spec parameters consistent with API Group II.
Decisions file: s30_shell.json (8 products total; HSB_500N is the only base oil here).

Product:
  HYUNDAIOILBANK:HSB_500N — HSB 500N (Daesan) base oil

Documents:
  22dd31aaf8f6  DL2-12275.pdf          Product Data Sheet (TDS), no revision date printed
  eead3091dcc6  DL2-14931.pdf  2021-06-15  Certificate of Analysis (CoA/CoQ), Intertek witness

Document notes:
  TDS (22dd31aaf8f6): "Product Data Sheet, Product Name: HSB 500N (DAESAN)_EN". Specification
    table with ASTM methods and limits. Density @15°C = Report (no limit). kv@40°C = Report.
    kv@100°C = 10.0-12.0 mm²/s. VI = 95-119. Color = Max 0.5. Pour Point = Max -15°C.
    Sulfur = Max 0.001 %wt. Flash Point COC = Min 230°C. Aromatics = Max 1 %wt.
    Saturates = Min 99 %wt. Air release @50°C = Report. Apparent Viscosity @-20°C = Report.
    No explicit API Group stated; VI range 95-119 is consistent only with Group II (Group III
    requires VI ≥120); sulfur ≤0.001%=10 ppm and saturates ≥99% meet Group II/III criteria.
  CoA (eead3091dcc6): Shipment date June 15, 2021; vessel GOLDEN DENISE; load port DAESAN;
    destination HAMRIYAH FREE ZONE, UAE; tested by Intertek Kimsco Co. Ltd, Korea.
    Results: kv@40°C = 94.36 mm²/s, kv@100°C = 11.07, VI = 102, Color = L0.5, Pour = -20°C,
    Flash = 278°C, Sulfur = 0.00021 wt%, Saturates = 99.5 wt%, Aromatics = 0.5 wt%,
    CCS @-20°C = 11381 mPas, Air release = 0.8 min, Density @15°C = 868.5 kg/m³,
    Cloud test = NO CLOUD (SMS 2556), Visual = B&C.

Writes field_evidence/s30_hyundai.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '22dd31aaf8f6': ('DL2-12275.pdf', ''),             # HSB_500N TDS (no date printed)
    'eead3091dcc6': ('DL2-14931.pdf', '2021-06-15'),   # HSB_500N CoA, Jun 15 2021
}

REVIEW = ('sheets read in full (text layer) 2026-11-16; '
          'TDS DL2-12275 (1pp), CoA DL2-14931 (1pp); all spec and result rows read')

VC_TDS        = 'product data sheet (TDS), typical properties table'
VC_COQ_SPEC   = 'certificate of quality (CoQ), product specification'
VC_COQ_RESULT = 'certificate of quality (CoQ), batch test result'

PK = 'HYUNDAIOILBANK:HSB_500N'

ROWS = []


def _r(tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_TDS):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': PK, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _m(tmpl, field, notes_=''):
    ROWS.append({
        'product_key': PK, 'template': tmpl, 'field': field, 'entry': '',
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': REVIEW,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind',
                            'printed_text', 'unit', 'test_temperature_c',
                            'method', 'conditions']},
    })


def _nit(prop, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
         meth='', cond='', sha='', pg=1, notes='', vc=VC_TDS):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': PK, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


# ── Tier 1: Blocking ────────────────────────────────────────────────────────

_m('base_oil_tier1', 'api_group_chemistry',
   'not found; API group not explicitly stated in TDS or CoA; '
   'VI range 95-119 (TDS spec) is consistent only with API Group II (Group III requires VI ≥120); '
   'sulfur ≤0.001%wt and saturates ≥99% meet Group II/III criteria; '
   'Hyundai Oil Bank (Daesan) is a known Group II producer; '
   'API group cannot be recorded without an explicit statement in a source document')

# kv40: TDS says "Report" (no spec limit); CoA gives batch result
_r('base_oil_tier1', 'kv40',
   'Vis@40°C (mm²/s): Report (spec) — CoA result: 94.36',
   unit='mm2/s', value='94.36', vk='report-only',
   meth='ASTM D 445', cond='40°C',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='TDS spec column says "Report" (no specification limit); value is CoA batch result; '
         'typical kv40 for a 500N grade base oil')

# kv100: TDS spec + CoA result
_r('base_oil_tier1', 'kv100',
   'Vis@100°C (mm²/s): 10.0-12.0 (spec)',
   unit='mm2/s', lo='10.0', hi='12.0', vk='range',
   meth='ASTM D 445',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS,
   notes='TDS product specification range')

_r('base_oil_tier1', 'kv100',
   'VISCOSITY @ 100 DEG C: 11.07 mm2s (result)',
   unit='mm2/s', value='11.07', vk='report-only',
   meth='ASTM D445', cond='100°C',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA batch result; spec MIN 10 MAX 12')

# VI: TDS spec + CoA result
_r('base_oil_tier1', 'viscosity_index',
   'VI (-): 95-119 (spec)',
   lo='95', hi='119', vk='range',
   meth='ASTM D 2270',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS,
   notes='TDS specification range; upper bound 119 rules out Group III (VI ≥120)')

_r('base_oil_tier1', 'viscosity_index',
   'VISCOSITY INDEX: 102 (result)',
   value='102', vk='report-only',
   meth='ASTM D2270',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA batch result; spec MIN 95 MAX 119')

# density: TDS "Report"; CoA result
_r('base_oil_tier1', 'density',
   'DENSITY @ 15 DEG C: 868.5 kg/m3 (result)',
   unit='kg/m3', value='868.5', vk='report-only',
   meth='ASTM D4052', cond='15°C',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='TDS spec column says "Report" (no limit); CoA result in kg/m3 (= 0.8685 g/cm3)')

# CCS / Apparent Viscosity @-20°C: TDS "Report"; CoA result
_r('base_oil_tier1', 'ccs',
   'VD CCS @ -20 DEG C: 11381 mPas (result)',
   unit='mPas', value='11381', vk='report-only',
   meth='ASTM D5293', cond='-20°C',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='TDS item "Apparent Viscosity @-20°C" (ASTM D5293) spec says "Report"; '
         'CoA item "VD CCS @ -20 DEG C" result = 11381 mPas; same test method')

_m('base_oil_tier1', 'specific_gravity',
   'not found; CoA reports density in kg/m3 not specific gravity')


# ── Tier 2: Verification ────────────────────────────────────────────────────

_m('base_oil_tier2', 'mrv',
   'not found; MRV not in TDS specification or CoA')

_r('base_oil_tier2', 'noack_volatility',
   'not found in TDS or CoA',
   vk='text', sha='22dd31aaf8f6', pg=1, vc=VC_TDS,
   notes='NOACK not a specified item in this TDS or CoA')

# Pour point: TDS spec + CoA result
_r('base_oil_tier2', 'pour_point',
   'Pour Point (°C): Max -15 (spec)',
   unit='°C', hi='-15', qual='<=', vk='bound',
   meth='ASTM D 97',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS)

_r('base_oil_tier2', 'pour_point',
   'POUR POINT: -20 deg C (result)',
   unit='°C', value='-20', vk='report-only',
   meth='ASTM D5950',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA method ASTM D5950; spec Max -15°C; result -20°C')

# Flash point: TDS spec + CoA result
_r('base_oil_tier2', 'flash_point',
   'Flash Point (COC) (°C): Min 230 (spec)',
   unit='°C', lo='230', qual='>=', vk='bound',
   meth='ASTM D 92',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS)

_r('base_oil_tier2', 'flash_point',
   'FLASH POINT: 278 deg C (result)',
   unit='°C', value='278', vk='report-only',
   meth='ASTM D92',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA batch result; spec Min 230°C')


# ── Tier 3: Substitution ────────────────────────────────────────────────────

# Sulfur: TDS spec + CoA result
_r('base_oil_tier3', 'sulfur',
   'Sulfur Content(%wt): Max 0.001 (spec)',
   unit='wt%', hi='0.001', qual='<=', vk='bound',
   meth='ASTM D5453',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS,
   notes='Max 0.001 wt% = 10 ppm; Group II/III sulfur threshold')

_r('base_oil_tier3', 'sulfur',
   'SULFUR: 0.00021 wt % (result)',
   unit='wt%', value='0.00021', vk='report-only',
   meth='ASTM D5453',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA batch result; spec Max 0.001 wt%')

# Saturates: TDS spec + CoA result
_r('base_oil_tier3', 'saturates',
   'Saturates (%wt): Min 99 (spec)',
   unit='wt%', lo='99', qual='>=', vk='bound',
   meth='ASTM D 2007',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS)

_r('base_oil_tier3', 'saturates',
   'SATURATES: 99.5 wt % (result)',
   unit='wt%', value='99.5', vk='report-only',
   meth='ASTM D7419',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA method ASTM D7419 (vs TDS D2007 — different standard for same property)')

# Aromatics: TDS spec + CoA result
_r('base_oil_tier3', 'aromatics',
   'Aromatic (%wt): Max 1 (spec)',
   unit='wt%', hi='1', qual='<=', vk='bound',
   meth='ASTM D 2007',
   sha='22dd31aaf8f6', pg=1, vc=VC_TDS)

_r('base_oil_tier3', 'aromatics',
   'AROMATICS: 0.5 wt % (result)',
   unit='wt%', value='0.5', vk='report-only',
   meth='ASTM D7419',
   sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
   notes='CoA method ASTM D7419; spec Max 1 wt%')

_m('base_oil_tier3', 'cloud_point',
   'not found; cloud point not in TDS or CoA specification')
_m('base_oil_tier3', 'wax_content',
   'not found; wax content not in TDS or CoA specification')


# ── not_in_template ──────────────────────────────────────────────────────────

# Color: TDS spec + CoA result
_nit('color',
     'Color (ASTM): Max 0.5 (spec)',
     unit='ASTM D1500', hi='0.5', qual='<=', vk='bound',
     meth='ASTM D 1500',
     sha='22dd31aaf8f6', pg=1, vc=VC_TDS)

_nit('color',
     'COLOR: L0.5 (result)',
     unit='ASTM D1500', value='0.5', qual='<=', vk='report-only',
     meth='ASTM D1500',
     sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
     notes='"L0.5" printed in CoA result — L prefix likely denotes less than 0.5 on ASTM D1500 scale')

# Air release @50°C
_nit('air_release',
     'Air release(@50°C): 0.8 Minutes (result)',
     unit='min', value='0.8', vk='report-only',
     meth='ASTM D 3427', cond='50°C',
     sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
     notes='TDS spec says "Report" (no limit); CoA result 0.8 min')

# Cloud test
_nit('cloud_test',
     'CLOUD TEST (7H/0): NO CLOUD',
     vk='text',
     meth='SMS 2556',
     sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
     notes='CoA result; SMS 2556 is a Shell internal method (7h at 0°C); '
           'confirms no wax precipitation under test conditions')

# Visual appearance
_nit('appearance',
     'VISUAL APPEARANCE: B&C',
     vk='text', meth='Visual',
     sha='eead3091dcc6', pg=1, vc=VC_COQ_RESULT,
     notes='"B&C" = Bright and Clear')


# ===========================================================================
write_rows('s30_hyundai.csv', ROWS)
if __name__ == '__main__':
    print(f's30_hyundai: {len(ROWS)} rows written to field_evidence/s30_hyundai.csv')
