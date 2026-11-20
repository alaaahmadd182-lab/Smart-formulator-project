"""Field-level mapping, S50 Ocean Chem P8401 — 1 product, 1 document.

Supplier: Ocean Chemical Technology Co., Ltd. (Yiwu, Zhejiang, China).
Product is a PMA pour point depressant (additive_component, component_general).
Decisions file: s50_formosa.json (included alongside Formosa products in that batch).

Product:
  OCEAN_CHEM:P8401_PPD — polyalkyl methacrylate (PMA) pour point depressant

Documents:
  0532ef083f9e  DL2-15432.pdf  2024-05-18  P8401 TDS (2pp)

Document notes:
  TDS page 1: Product introduction, Typical Physical Properties table, Performance bullets,
    Treat rate. Properties: Visual appearance (Clear, free of sediment), kv@100°C = 260 mm²/s,
    Color = 0.5 (ASTM D1500), Density @20°C = 900 kg/m³ (ASTM 4052), Flash Point = 160°C
    (ASTM D92). Treat rate: 0.1%-1% wt. Stated "especially suitable for API Group II and III
    base oils." Performance data: pour point reduction table for Group I and II base oils.
  TDS page 2: Extended performance data — pour point reduction in CH-4 10W-30 and 15W-40
    engine oils at 0.3 wt%; compatibility with OCP VIIs; hydraulic oil performance
    (L-HV 46 with V6245+P8401).
  Note: Performance table header reads "0.2%P8201" (apparent typo for P8401); recorded as printed
    with note. Density unit "ASTM 4052" in TDS is a method reference, not a unit — standard unit
    for this method is kg/m³.

Writes field_evidence/s50_ocean_p8401.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '0532ef083f9e': ('DL2-15432.pdf', '2024-05-18'),  # P8401 TDS
}

REVIEW = ('sheets read in full (text layer) 2026-11-16; '
          'TDS DL2-15432 (2pp); all property rows read')
VC_TDS = 'product data sheet (TDS), typical properties table'

PK = 'OCEAN_CHEM:P8401_PPD'
SHA = '0532ef083f9e'

ROWS = []


def _r(tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', pg=1, notes='', entry=''):
    fname, rev = FILE[SHA]
    ROWS.append({
        'product_key': PK, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[SHA]['sha256'],
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
         meth='', cond='', pg=1, notes=''):
    fname, rev = FILE[SHA]
    ROWS.append({
        'product_key': PK, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[SHA]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


# ===========================================================================
# OCEAN_CHEM:P8401_PPD — PMA pour point depressant
# ===========================================================================

_r('component_general', 'function.primary',
   'P8401 is an effective polyalkyl methacrylate pour point depressant, which can be used '
   'in most lubricants, such as engine oils, gear oils, and hydraulic oils, especially '
   'suitable for API Group II and III base oils.',
   vk='text',
   notes='from TDS product introduction')

_r('component_general', 'function.secondary',
   'High shear stability; Lower viscosity, easy to treat; Wide application',
   vk='text', pg=1,
   notes='from TDS Performance section; secondary benefits listed as bullets')

_r('component_general', 'chemical_family',
   'polyalkyl methacrylate (PMA)',
   vk='text',
   notes='chemical family from TDS product name and introduction')

_m('component_general', 'active_content',
   'not found; active polymer content % not stated in TDS')

_m('component_general', 'carrier.identity',
   'not found; product is described as a clear liquid; no carrier stated explicitly; '
   'low flash point (160°C) and density (900 kg/m³) are consistent with a diluted PMA solution')

_m('component_general', 'carrier.share_wt_pct',
   'not found; no carrier percentage stated')

_r('component_general', 'treat_rate',
   'P8401: 0.1%-1%wt, depends on the actual situation.',
   unit='wt%', lo='0.1', hi='1.0', vk='range',
   notes='from TDS "Typical treat rate" section')

_r('component_general', 'compatibility_restrictions',
   'especially suitable for API Group II and III base oils',
   vk='text',
   notes='from TDS product introduction; also demonstrated in performance table with '
         'Group I (DL 150SN/400SN) and Group II (Ssangyong, Formosa, CNOOC, Yubase) base oils')

_m('component_general', 'function_specific_markers.tbn',
   'not found; PMA PPD — ashless, no TBN')
_m('component_general', 'function_specific_markers.ca',  'not found')
_m('component_general', 'function_specific_markers.mg',  'not found')
_m('component_general', 'function_specific_markers.p',   'not found')
_m('component_general', 'function_specific_markers.zn',  'not found')
_m('component_general', 'function_specific_markers.mo',  'not found')

# not_in_template
_nit('kv100',
     'Viscosity at 100°C, mm2/s: 260',
     unit='mm2/s', value='260', vk='typical',
     meth='ASTM D445', cond='100°C',
     notes='kv100 of neat PMA concentrate (not a formulated oil); '
           'high viscosity typical of undiluted PMA solutions')

_nit('density',
     'Density at 20°C, kg/m3: 900',
     unit='kg/m3', value='900', vk='typical',
     meth='ASTM 4052', cond='20°C',
     notes='temperature is 20°C (non-standard; template density fields assume 15°C or 15.6°C); '
           '"ASTM 4052" in TDS is the method reference, standard for this method is kg/m³')

_nit('flash_point',
     'Flash point, °C: 160',
     unit='°C', value='160', vk='typical',
     meth='ASTM D92',
     notes='COC method (open cup, as ASTM D92)')

_nit('color',
     'Color: 0.5',
     unit='ASTM D1500', value='0.5', vk='typical',
     meth='ASTM D1500',
     notes='color 0.5 on ASTM D1500 scale; consistent with a pale yellow/amber PPD product')


# ===========================================================================
write_rows('s50_ocean_p8401.csv', ROWS)
if __name__ == '__main__':
    print(f's50_ocean_p8401: {len(ROWS)} rows written to field_evidence/s50_ocean_p8401.csv')
