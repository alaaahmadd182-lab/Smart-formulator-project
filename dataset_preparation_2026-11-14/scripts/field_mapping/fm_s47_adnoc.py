"""Field-level mapping, S47 ADNOC ADbase — 5 base oil products, 3 documents.

Documents:
  DL2-12151.pdf  sha12 308a48fabf14  ADbase product brochure; covers all 5 grades;
                                     no printed date; source for all 5 products
  DL2-12221.pdf  sha12 16b2a05864c4  ADbase spec extract (properties table only);
                                     covers all 5 grades; no printed date;
                                     identical values to DL2-12151 — shorter alternate
  DL2-14106.pdf  sha12 56a48fd0a61c  ADBASE 6CST Certificate of Quality;
                                     Cert No. R.RE/BO•060/2020; Batch No. 12290;
                                     Date 08/07/2020 (D/M/YYYY → 2020-07-08); 6CST only

Products (all base_oil):
  EXISTING:ADNOC_ADBASE_2CST   ADbase 2cSt  Group III
  EXISTING:ADNOC_ADBASE_3CST   ADbase 3cSt  Group III
  EXISTING:ADNOC_ADBASE_4CST   ADbase 4cSt  Group III
  EXISTING:ADNOC_ADBASE_6CST   ADbase 6cSt  Group III
  EXISTING:ADNOC_ADBASE_8CST   ADbase 8cSt  Group III

Document notes:
- DL2-12151 brochure explicitly identifies ADbase as Group III: "Group III base oil" (p. 2).
- DL2-12221 is a one-page properties extract of the same spec data as DL2-12151; values
  are identical; recorded from DL2-12151 (fuller document); DL2-12221 noted as alternate.
- Both documents give single-point values in the Properties table with footnote "all accurate
  on the date of publishing" — recorded as 'typical' (no min/max stated).
- CCS and Noack are printed as "-" for 2CST and 3CST → Missing.
- Sulfur: <3 mg/kg for all grades (not wt%).
- DL2-14106 batch cert, 6CST: OCR artefact in kv100 spec min reads "Minfi.800"; interpreted
  as "Min 5.800" (Max 6.200 and result 6.002 are consistent with that bound; "Min 6.800" would
  exceed the stated max). Noted on the row.
- DL2-14106 batch cert date: "08/07/2020" (day 8 > implied max day=12 not violated, but the
  cert is ADNOC UAE so D/M/YYYY is assumed) → 2020-07-08.

Writes field_evidence/s47_adnoc.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '308a48fabf14': ('DL2-12151.pdf', ''),       # ADbase brochure, all 5 grades, no date
    '16b2a05864c4': ('DL2-12221.pdf', ''),        # properties extract, identical values, no date
    '56a48fd0a61c': ('DL2-14106.pdf', '2020-07-08'), # 6CST batch cert
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; brochure and batch cert parsed in full'
VC_TDS   = 'product data sheet (brochure), properties table'
VC_COQ_SPEC   = 'certificate of quality, specification limits'
VC_COQ_RESULT = 'certificate of quality, batch test result'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='308a48fabf14', pg=1, notes='', vc=None):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'value': str(value), 'qualifier': qual, 'min': str(lo), 'max': str(hi),
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc or VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _m(pk, tmpl, field, notes_=''):
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'status': 'Missing', 'value_class': '', 'basis': '',
        'source_file': '', 'sha256': '', 'page': '', 'revision_date': '',
        'notes': notes_ or 'not found in the inspected text',
        'review': REVIEW,
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text',
                            'unit', 'test_temperature_c', 'method', 'conditions']},
    })


def _nit(pk, prop, printed, sha='308a48fabf14', pg=1, unit='', value='', lo='', hi='',
         qual='', vk='typical', meth='', notes='', vc=None):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': str(value), 'qualifier': qual, 'min': str(lo), 'max': str(hi),
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': '',
        'status': 'Reported', 'value_class': vc or VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Brochure data: DL2-12151.pdf — properties table, all 5 grades, page 6-7
# DL2-12221.pdf has identical values; noted as alternate in `notes` field
# ──────────────────────────────────────────────────────────────────────────────
# (kv100, kv40, VI, density @15°C, pour, flash, noack, ccs)
_BROCHURE_DATA = {
    'EXISTING:ADNOC_ADBASE_2CST':  (2.3,  7.5,  115, 0.823, -27, 170, None,  None),
    'EXISTING:ADNOC_ADBASE_3CST':  (3.05, 12,   120, 0.825, -24, 190, None,  None),
    'EXISTING:ADNOC_ADBASE_4CST':  (4.35, 20,   130, 0.832, -18, 220, 12.5,  1400),
    'EXISTING:ADNOC_ADBASE_6CST':  (6.18, 34,   137, 0.844, -15, 235, 6.8,   3700),
    'EXISTING:ADNOC_ADBASE_8CST':  (8.05, 49,   137, 0.845, -12, 255, 3.5,   8000),
}

BROCHURE_ALT_NOTE = ('DL2-12221.pdf (sha12 16b2a05864c4) is a shorter properties extract '
                     'with identical values; recorded from DL2-12151 (fuller brochure)')

for pk, (kv100, kv40, vi, dens, pour, flash, noack, ccs) in _BROCHURE_DATA.items():
    # tier1: Blocking
    _r(pk, 'base_oil_tier1', 'api_group_chemistry',
       'ADbase: Group III base oil', vk='text',
       notes='stated in brochure text: "Group III base oil" (p.2 and throughout)')
    _r(pk, 'base_oil_tier1', 'kv40',
       f'Kinematic Viscosity @40°C, mm2/s: {kv40}',
       unit='mm2/s', value=kv40, meth='ASTM D445', cond='40°C',
       notes=BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier1', 'kv100',
       f'Kinematic Viscosity @100°C, mm2/s: {kv100}',
       unit='mm2/s', value=kv100, meth='ASTM D445', cond='100°C',
       notes=BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier1', 'viscosity_index',
       f'Viscosity Index: {vi}',
       value=vi, notes=BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier1', 'density',
       f'Density @15°C, g/ml: {dens}',
       unit='g/ml', value=dens, cond='15°C', meth='ASTM D4052',
       notes=BROCHURE_ALT_NOTE)
    _m(pk, 'base_oil_tier1', 'specific_gravity',
       'not found; not stated separately from density in brochure')
    if ccs is not None:
        _r(pk, 'base_oil_tier1', 'ccs',
           f'Apparent Viscosity by CCS @-30°C, mPas: {ccs}',
           unit='mPas', value=ccs, meth='ASTM D5293', cond='-30°C',
           notes=BROCHURE_ALT_NOTE)
    else:
        _m(pk, 'base_oil_tier1', 'ccs',
           'printed as "-" in brochure properties table; not measured for this grade')

    # tier2: Verification
    _m(pk, 'base_oil_tier2', 'mrv',
       'not found; MRV not stated in ADbase brochure')
    if noack is not None:
        _r(pk, 'base_oil_tier2', 'noack_volatility',
           f'Evaporation Loss Noack method, %M/M: {noack}',
           unit='%M/M', value=noack, meth='ASTM D5800',
           notes=BROCHURE_ALT_NOTE)
    else:
        _m(pk, 'base_oil_tier2', 'noack_volatility',
           'printed as "-" in brochure properties table; not measured for this grade')
    _r(pk, 'base_oil_tier2', 'pour_point',
       f'Pour Point, °C: {pour}',
       unit='°C', value=pour, meth='ASTM D5949',
       notes=BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier2', 'flash_point',
       f'Flash Point, °C: {flash}',
       unit='°C', value=flash, meth='ASTM D92',
       notes=BROCHURE_ALT_NOTE)

    # tier3: Substitution
    _r(pk, 'base_oil_tier3', 'sulfur',
       'Sulfur, mg/kg: <3',
       unit='mg/kg', hi='3', qual='<', vk='bound', meth='ASTM D2622',
       notes='<3 mg/kg applies to all 5 grades; ' + BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier3', 'saturates',
       'Saturates, mass%: 99.8',
       unit='mass%', value=99.8, meth='ASTM D7419',
       notes=BROCHURE_ALT_NOTE)
    _r(pk, 'base_oil_tier3', 'aromatics',
       'Aromatic content, mass%: <0.2',
       unit='mass%', hi='0.2', qual='<', vk='bound', meth='ASTM D7419',
       notes='<0.2 mass% applies to all 5 grades; ' + BROCHURE_ALT_NOTE)
    _m(pk, 'base_oil_tier3', 'cloud_point',
       'not found; cloud point not stated in ADbase brochure')
    _m(pk, 'base_oil_tier3', 'wax_content',
       'not found; wax content not stated in ADbase brochure')


# ──────────────────────────────────────────────────────────────────────────────
# DL2-14106.pdf — ADBASE 6CST Certificate of Quality, 2020-07-08
# Records spec limits (from spec column) and batch results (from result column)
# for ADBASE 6CST only
# ──────────────────────────────────────────────────────────────────────────────
PK6 = 'EXISTING:ADNOC_ADBASE_6CST'
COQ = '56a48fd0a61c'
COQ_NOTE = 'batch certificate (Cert No. R.RE/BO•060/2020, Batch No. 12290, 2020-07-08)'

# kv100: spec bounds (OCR "Minfi.800" interpreted as "Min 5.800") + batch result
_r(PK6, 'base_oil_tier1', 'kv100',
   'kv100 spec: Min [5].800, Max 6.200 mm2/s',
   unit='mm2/s', lo='5.800', hi='6.200', vk='range', meth='ASTM D445', cond='100°C',
   sha=COQ, pg=1, vc=VC_COQ_SPEC,
   notes='spec bounds from batch cert; OCR reads "Minfi.800" — interpreted as "Min 5.800" '
         '(result=6.002 is within 5.800–6.200; "Min 6.800" would exceed Max 6.200); ' + COQ_NOTE)
_r(PK6, 'base_oil_tier1', 'kv100',
   'kv100 batch result: 6,002 mm2/s (European decimal = 6.002)',
   unit='mm2/s', value='6.002', meth='ASTM D445', cond='100°C',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# kv40: spec Report (no bound), batch result 32.14
_r(PK6, 'base_oil_tier1', 'kv40',
   'kv40 batch result: 32.14 mm2/s (spec: Report)',
   unit='mm2/s', value='32.14', meth='ASTM D445', cond='40°C',
   sha=COQ, pg=1, vc=VC_COQ_RESULT,
   notes='spec column says Report (no bound); batch result 32.14; ' + COQ_NOTE)

# viscosity_index: spec Min 125, batch result 135
_r(PK6, 'base_oil_tier1', 'viscosity_index',
   'VI spec: Min 125',
   lo='125', qual='>=', vk='bound', meth='ASTM D2270',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier1', 'viscosity_index',
   'VI batch result: 135',
   value='135', meth='ASTM D2270',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# density: spec Report, batch result 0.8372 g/mL @15°C
_r(PK6, 'base_oil_tier1', 'density',
   'Density @15°C batch result: 0.8372 g/mL (spec: Report)',
   unit='g/mL', value='0.8372', cond='15°C', meth='ASTM D4052',
   sha=COQ, pg=1, vc=VC_COQ_RESULT,
   notes='spec column says Report; batch result 0.8372 g/mL; ' + COQ_NOTE)

# ccs @-30°C: spec Max 4500, batch result 3335
_r(PK6, 'base_oil_tier1', 'ccs',
   'CCS @-30°C spec: Max 4500 mPas',
   unit='mPas', hi='4500', qual='<=', vk='bound', meth='ASTM D5293', cond='-30°C',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier1', 'ccs',
   'CCS @-30°C batch result: 3335 mPas',
   unit='mPas', value='3335', meth='ASTM D5293', cond='-30°C',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# noack: spec Max 8.0, batch result 5.4
_r(PK6, 'base_oil_tier2', 'noack_volatility',
   'Noack spec: Max 8.0 %M/M',
   unit='%M/M', hi='8.0', qual='<=', vk='bound', meth='ASTM D5800',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier2', 'noack_volatility',
   'Noack batch result: 5.4 %M/M',
   unit='%M/M', value='5.4', meth='ASTM D5800',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# pour_point: spec Max -15, batch result -18
_r(PK6, 'base_oil_tier2', 'pour_point',
   'Pour Point spec: Max -15 °C',
   unit='°C', hi='-15', qual='<=', vk='bound', meth='ASTM D5949',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier2', 'pour_point',
   'Pour Point batch result: -18 °C',
   unit='°C', value='-18', meth='ASTM D5949',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# flash_point (COC): spec Min 220, batch result 242
_r(PK6, 'base_oil_tier2', 'flash_point',
   'Flash Point (COC) spec: Min 220 °C',
   unit='°C', lo='220', qual='>=', vk='bound', meth='ASTM D92',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier2', 'flash_point',
   'Flash Point (COC) batch result: 242 °C',
   unit='°C', value='242', meth='ASTM D92',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# sulfur: spec Max 10 mg/kg, batch result <3.0
_r(PK6, 'base_oil_tier3', 'sulfur',
   'Sulfur spec: Max 10 mg/kg',
   unit='mg/kg', hi='10', qual='<=', vk='bound', meth='ASTM D2622',
   sha=COQ, pg=1, vc=VC_COQ_SPEC, notes=COQ_NOTE)
_r(PK6, 'base_oil_tier3', 'sulfur',
   'Sulfur batch result: <3.0 mg/kg',
   unit='mg/kg', hi='3.0', qual='<', vk='bound', meth='ASTM D2622',
   sha=COQ, pg=1, vc=VC_COQ_RESULT, notes=COQ_NOTE)

# saturates: spec Report, batch result 99.8
_r(PK6, 'base_oil_tier3', 'saturates',
   'Saturates batch result: 99.8 mass% (spec: Report)',
   unit='mass%', value='99.8', meth='ASTM D7419',
   sha=COQ, pg=1, vc=VC_COQ_RESULT,
   notes='spec column says Report; ' + COQ_NOTE)

# aromatics: spec Report, batch result <0.2
_r(PK6, 'base_oil_tier3', 'aromatics',
   'Aromatics batch result: <0.2 mass% (spec: Report)',
   unit='mass%', hi='0.2', qual='<', vk='bound', meth='ASTM D7419',
   sha=COQ, pg=1, vc=VC_COQ_RESULT,
   notes='spec column says Report; ' + COQ_NOTE)

# not_in_template: batch cert properties not in template
_nit(PK6, 'appearance',
     'Appearance: Clear & Bright', sha=COQ, pg=1, vk='text', meth='ASTM D4176-1',
     vc=VC_COQ_RESULT, notes=COQ_NOTE)
_nit(PK6, 'water_content',
     'Water batch result: 23 mg/kg (spec Max 50 mg/kg)',
     sha=COQ, pg=1, unit='mg/kg', value='23', meth='ASTM D6304',
     vc=VC_COQ_RESULT, notes='spec Max 50 mg/kg; batch result 23; ' + COQ_NOTE)
_nit(PK6, 'color_saybolt',
     'Color, Saybolt batch result: +30 (spec Min +20)',
     sha=COQ, pg=1, value='+30', meth='ASTM D156',
     vc=VC_COQ_RESULT, notes='spec Min +20; batch result +30; ' + COQ_NOTE)
_nit(PK6, 'copper_corrosion',
     'Copper Corrosion 3hrs @100°C batch result: 1b (spec: Report)',
     sha=COQ, pg=1, vk='text', meth='ASTM D130',
     vc=VC_COQ_RESULT, notes='spec Report; ' + COQ_NOTE)
_nit(PK6, 'acid_number',
     'Acid Number batch result: <0.1 mgKOH/g (spec: Report)',
     sha=COQ, pg=1, unit='mgKOH/g', hi='0.1', qual='<', vk='bound', meth='ASTM D664',
     vc=VC_COQ_RESULT, notes='spec Report; ' + COQ_NOTE)
_nit(PK6, 'carbon_residue',
     'Carbon Residue batch result: <0.1 %(m/m) (spec: Report)',
     sha=COQ, pg=1, unit='%(m/m)', hi='0.1', qual='<', vk='bound', meth='ASTM D4530',
     vc=VC_COQ_RESULT, notes='spec Report; ' + COQ_NOTE)


# ──────────────────────────────────────────────────────────────────────────────
write_rows('s47_adnoc.csv', ROWS)
if __name__ == '__main__':
    print(f's47_adnoc: {len(ROWS)} rows written to field_evidence/s47_adnoc.csv')
