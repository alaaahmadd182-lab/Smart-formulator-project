"""Field-level mapping, S30 TOHOLCHEM — 3 products, 3 documents.

Supplier: TOHO CHEMICAL INDUSTRY CO., LTD., Tokyo, Japan.
All three products are PMA-type pour point depressants (additive_component, component_general).
Decisions file: s30_shell.json (supplier grouped with Shell documents; TOHOLCHEM products
  are listed separately — LUBRAN products are distinct from Shell products in that file).

Products:
  TOHOLCHEM:LUBRAN_141  — PMA PPD for wide range of base oils; Group II performance data
  TOHOLCHEM:LUBRAN_165  — PMA PPD especially for Group III base oils; also Group I/II effective
  TOHOLCHEM:LUBRAN_171  — PMA PPD for wide range of base oils; Group II performance data

Documents (one per product):
  5f3703fa2fe2  DL2-11664.pdf  2015-10-22  LUBRAN_141 TDS (single page)
  abdb494fb861  DL2-11665.pdf  2015-10-22  LUBRAN_165 TDS (single page)
  e51460de2cb1  DL2-11666.pdf  2015-10-22  LUBRAN_171 TDS (single page)

Document notes:
  All three TDS are single-page, same layout. Date "2015.10.22" (ISO format → 2015-10-22).
  "Typical properties" table: Appearance, Color (ASTM), Density (g/cm³ at 50°C),
    Kinematic Viscosity (mm²/s at 100°C), Flash Point (°C, COC). Test methods are JIS.
  Performance table: Group II base oils (150N and 500N grades), pour point (°C) vs dosage (%).
    Dosages shown: 0.0%, 0.1%, 0.3%, 0.5% for LUBRAN_141 and _171; 0.0, 0.05, 0.1, 0.3, 0.5% for _165.
  LUBRAN_165 color printed as "L0.5" — "L" appears to be a less-than notation in the JIS scale.
  Density at 50°C (non-standard; most templates use 15°C or 15.6°C).
  Kinematic viscosity at 100°C: concentrates have high viscosity (400-420 mm²/s);
    this reflects the neat PMA product, not a formulated oil.
  No carrier mentioned; product appears to be neat PMA polymer (no dilution stated).
  Test methods are JIS: JIS K2580 (color), JIS K2249 (density), JIS K2283 (viscosity),
    JIS K2265 (flash point), JIS K2269 (pour point for performance table).

Writes field_evidence/s30_toholchem.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '5f3703fa2fe2': ('DL2-11664.pdf', '2015-10-22'),
    'abdb494fb861': ('DL2-11665.pdf', '2015-10-22'),
    'e51460de2cb1': ('DL2-11666.pdf', '2015-10-22'),
}

REVIEW = 'sheets read in full (text layer) 2026-11-16; single-page TDS, all rows read'
VC_TDS = 'product data sheet (TDS), typical properties table'

L141 = 'TOHOLCHEM:LUBRAN_141'
L165 = 'TOHOLCHEM:LUBRAN_165'
L171 = 'TOHOLCHEM:LUBRAN_171'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_TDS):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
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
        **{k: '' for k in ['value', 'qualifier', 'min', 'max', 'value_kind',
                            'printed_text', 'unit', 'test_temperature_c',
                            'method', 'conditions']},
    })


def _nit(pk, prop, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
         meth='', cond='', sha='', pg=1, notes='', vc=VC_TDS):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _map_product(pk, sha, density_50, kv100, flash,
                 color_printed, color_val,
                 treat_lo, treat_hi,
                 compat_note, function_note=''):
    """Write all component_general and not_in_template rows for one LUBRAN product.

    pk          : product_key
    sha         : sha12 of the single TDS document
    density_50  : density at 50°C (g/cm³)
    kv100       : kinematic viscosity at 100°C (mm²/s) of neat concentrate
    flash       : flash point COC (°C)
    color_printed: printed color value (may include L prefix)
    color_val   : numeric string for color value
    treat_lo    : minimum dose shown in performance table (wt%)
    treat_hi    : maximum dose shown in performance table (wt%)
    compat_note : compatibility/base oil range note
    function_note: additional note for function.primary
    """
    # function.primary
    _r(pk, 'component_general', 'function.primary',
       f'LUBRAN {pk.split("_",1)[1]} is a Polymethacrylate (PMA) type of pour point '
       'depressant for lubricating oils.',
       vk='text', sha=sha, notes=function_note)
    # function.secondary
    _m(pk, 'component_general', 'function.secondary',
       'not found; no secondary function stated in TDS')
    # chemical_family
    _r(pk, 'component_general', 'chemical_family',
       'Polymethacrylate (PMA) type',
       vk='text', sha=sha,
       notes='chemical family stated in product description; full INCI/IUPAC name not given')
    # active_content
    _m(pk, 'component_general', 'active_content',
       'not found; active polymer content % not stated in TDS')
    # carrier.identity
    _m(pk, 'component_general', 'carrier.identity',
       'not found; no carrier or diluent mentioned in TDS — product appears to be neat PMA')
    # carrier.share_wt_pct
    _m(pk, 'component_general', 'carrier.share_wt_pct',
       'not found; no carrier stated')
    # treat_rate — from performance table
    _r(pk, 'component_general', 'treat_rate',
       f'Pour point depressant performance shown at {treat_lo}%–{treat_hi}% in '
       'Group II base oils (150N and 500N)',
       unit='wt%', lo=str(treat_lo), hi=str(treat_hi), vk='range',
       sha=sha,
       notes='range from dosage levels in performance table; not an explicit recommended '
             'treat rate; individual results for Hyundai/Shell 150N and CNOOC/Exxon Mobil/Formosa '
             '500N base oils; test method JIS K2269')
    # compatibility_restrictions
    _r(pk, 'component_general', 'compatibility_restrictions',
       compat_note,
       vk='text', sha=sha,
       notes='from product description in TDS')
    # function_specific_markers — all Missing (PPD has no TBN/Ca/Mg/P/Zn/Mo)
    _m(pk, 'component_general', 'function_specific_markers.tbn',
       'not found; PPD — TBN not applicable and not stated')
    _m(pk, 'component_general', 'function_specific_markers.ca',
       'not found')
    _m(pk, 'component_general', 'function_specific_markers.mg',
       'not found')
    _m(pk, 'component_general', 'function_specific_markers.p',
       'not found')
    _m(pk, 'component_general', 'function_specific_markers.zn',
       'not found')
    _m(pk, 'component_general', 'function_specific_markers.mo',
       'not found')
    # not_in_template: density @50°C
    _nit(pk, 'density',
         f'Density (g/cm³, at 50°C): {density_50}',
         unit='g/cm3', value=str(density_50), vk='typical',
         meth='JIS K2249', cond='50°C',
         sha=sha,
         notes='temperature is 50°C (non-standard; template density fields assume 15°C or 15.6°C)')
    # not_in_template: kv100 of neat concentrate
    _nit(pk, 'kv100',
         f'Kinematic Viscosity (mm²/s, at 100°C): {kv100}',
         unit='mm2/s', value=str(kv100), vk='typical',
         meth='JIS K2283', cond='100°C',
         sha=sha,
         notes='viscosity of neat PMA concentrate (not a formulated oil); '
               'very high viscosity typical of concentrate PMA polymers')
    # not_in_template: flash point
    _nit(pk, 'flash_point',
         f'Flash Point (°C, COC): {flash}',
         unit='°C', value=str(flash), vk='typical',
         meth='JIS K2265',
         sha=sha)
    # not_in_template: color
    _nit(pk, 'color',
         f'Color (ASTM): {color_printed}',
         unit='ASTM', value=color_val, vk='typical',
         meth='JIS K2580',
         sha=sha,
         notes='JIS K2580 is the Japanese standard equivalent of ASTM D1500 color scale; '
               + ('"L0.5" may denote less than 0.5 on the ASTM D1500 scale' if 'L' in color_printed else ''))


# LUBRAN_141
_map_product(
    pk=L141, sha='5f3703fa2fe2',
    density_50=0.874, kv100=400, flash=196,
    color_printed='0.5', color_val='0.5',
    treat_lo=0.1, treat_hi=0.5,
    compat_note=(
        'LUBRAN 141 can be used as an excellent pour point depressant in order to improve '
        'oil flows of low viscosity to high viscosity lubricating oils. LUBRAN 141 is effective '
        'pour point depressant for a wide range of baseoils, especially oils, such as engine '
        'oils and gear oils.'
    ),
)

# LUBRAN_165
_map_product(
    pk=L165, sha='abdb494fb861',
    density_50=0.896, kv100=420, flash=196,
    color_printed='L0.5', color_val='0.5',
    treat_lo=0.05, treat_hi=0.5,
    compat_note=(
        'LUBRAN 165 is a Polymethacrylate (PMA) type of pour point depressant for high '
        'viscosity index baseoil especially for group 3 baseoils. LUBRAN 165 is also effective '
        'with small added to group 1 and group 2 base oils.'
    ),
    function_note='especially suited to Group III (high VI) base oils; also effective in Group I and II',
)

# LUBRAN_171
_map_product(
    pk=L171, sha='e51460de2cb1',
    density_50=0.915, kv100=400, flash=198,
    color_printed='0.5', color_val='0.5',
    treat_lo=0.1, treat_hi=0.5,
    compat_note=(
        'LUBRAN 171 can be used as an excellent pour point depressant in order to improve '
        'oil flows of low viscosity to high viscosity lubricating oils. LUBRAN 171 is effective '
        'pour point depressant for a wide range of baseoils, especially oils, such as engine '
        'oils and gear oils.'
    ),
)


# ===========================================================================
write_rows('s30_toholchem.csv', ROWS)
if __name__ == '__main__':
    print(f's30_toholchem: {len(ROWS)} rows written to field_evidence/s30_toholchem.csv')
