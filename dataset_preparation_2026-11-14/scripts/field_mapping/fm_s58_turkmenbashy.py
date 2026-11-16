"""Field-level mapping, S58 Turkmenbashy — 5 base oil products, 1 document.

Document: DL2-11239.pdf (also archived as DL2-13630.pdf, DL2-13758.pdf — 3 identical copies)
  sha256 e8f4ae204dd0…  |  1 page  |  no printed date
  Standard: TŞ 05766698-60-2006 (Turkmenistan industrial standard, Turkmenbashy oil refinery complex)
  Single-page tabular specification covering all five grades.

Products (all base_oil, all tiers 1–3):
  TURKMENBASHY:SN80    solvent-refined base oil SN-80
  TURKMENBASHY:SN180   solvent-refined base oil SN-180
  TURKMENBASHY:SN350   solvent-refined base oil SN-350
  TURKMENBASHY:SN600   solvent-refined base oil SN-600
  TURKMENBASHY:SN1200  solvent-refined base oil SN-1200

Document notes:
- Document type says 'unresolved' in register; content is a product specification table
  with spec bounds (not more than / not less than / within) — no typical values given.
- kv100 column header says "Kinematic viscosity at 100°C, cSt, within" → spec range, not typical.
- Density at 20°C (g/cm3); temperature is 20°C, not the more common 15°C.
- kv40 is not measured/stated in this standard.
- api_group_chemistry is not stated; VI range 90-95 is consistent with Group I but
  cannot be confirmed from this document alone.
- Test methods are not cited (only the TŞ standard number applies).
- Sulfur (row 8): single upper bound applies to all five grades.
- Ash (row 10) and mechanical impurities (row 11): single value for all grades.
- Refraction coefficient (row 2): "Have no standard, is necessary" — no numerical value.

Writes field_evidence/s58_turkmenbashy.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    'e8f4ae204dd0': ('DL2-11239.pdf', ''),  # TŞ 05766698-60-2006 spec; no printed date
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; single-page spec table, all rows read'
VC_SPEC = 'technical specification (TŞ 05766698-60-2006), properties table'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='bound',
       meth='', cond='', sha='e8f4ae204dd0', pg=1, notes=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': VC_SPEC, 'basis': '',
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


def _nit(pk, prop, printed, unit='', value='', lo='', hi='', qual='', vk='bound', notes=''):
    """not_in_template row."""
    fname, rev = FILE['e8f4ae204dd0']
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': '', 'conditions': '',
        'status': 'Reported', 'value_class': VC_SPEC, 'basis': '',
        'source_file': fname, 'sha256': _ud['e8f4ae204dd0']['sha256'],
        'page': '1', 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


def _map_product(pk, kv100_lo, kv100_hi, vi_min, density_max,
                 pour_max, flash_min,
                 color_cnt_max, color_astm_max, acid_max):
    """Write all tier1/2/3 and not_in_template rows for one product."""
    # ── tier1: Blocking ──────────────────────────────────────────────────────
    _m(pk, 'base_oil_tier1', 'api_group_chemistry',
       'not found; API group not stated in TŞ 05766698-60-2006 specification table')
    _m(pk, 'base_oil_tier1', 'kv40',
       'not found; specification table does not include kinematic viscosity at 40°C')
    _r(pk, 'base_oil_tier1', 'kv100',
       f'Kinematic viscosity at 100°C, cSt, within: {kv100_lo}–{kv100_hi}',
       unit='cSt', lo=str(kv100_lo), hi=str(kv100_hi), vk='range',
       notes='column header says "within" (Turkmenistan spec range; not a typical value)')
    _r(pk, 'base_oil_tier1', 'viscosity_index',
       f'Viscosity index, not less than: {vi_min}',
       lo=str(vi_min), qual='>=', vk='bound',
       notes='dimensionless; spec lower bound only; no typical stated')
    _r(pk, 'base_oil_tier1', 'density',
       f'Density, at 20°C, g/cm3, not more than: {density_max}',
       unit='g/cm3', hi=str(density_max), qual='<=', vk='bound',
       cond='20°C',
       notes='temperature is 20°C (not the more common 15°C); spec upper bound only')
    _m(pk, 'base_oil_tier1', 'specific_gravity',
       'not found; not stated in specification table (density at 20°C given instead)')
    _m(pk, 'base_oil_tier1', 'ccs',
       'not found; CCS not stated in TŞ 05766698-60-2006 specification table')

    # ── tier2: Verification ──────────────────────────────────────────────────
    _m(pk, 'base_oil_tier2', 'mrv',
       'not found; MRV not stated in TŞ 05766698-60-2006 specification table')
    _m(pk, 'base_oil_tier2', 'noack_volatility',
       'not found; Noack volatility not stated in TŞ 05766698-60-2006 specification table')
    _r(pk, 'base_oil_tier2', 'pour_point',
       f'Pour point, °C, not higher than: {pour_max}',
       unit='°C', hi=str(pour_max), qual='<=', vk='bound')
    _r(pk, 'base_oil_tier2', 'flash_point',
       f'Flash point, °C, not less than: {flash_min}',
       unit='°C', lo=str(flash_min), qual='>=', vk='bound')

    # ── tier3: Substitution ──────────────────────────────────────────────────
    _r(pk, 'base_oil_tier3', 'sulfur',
       'Mass portion of sulfur, %, not more than: 0.03',
       unit='%', hi='0.03', qual='<=', vk='bound',
       notes='single upper bound applies to all five SN grades in the table')
    _m(pk, 'base_oil_tier3', 'saturates',
       'not found; saturates not stated in TŞ 05766698-60-2006 specification table')
    _m(pk, 'base_oil_tier3', 'aromatics',
       'not found; aromatics not stated in TŞ 05766698-60-2006 specification table')
    _m(pk, 'base_oil_tier3', 'cloud_point',
       'not found; cloud point not stated in TŞ 05766698-60-2006 specification table')
    _m(pk, 'base_oil_tier3', 'wax_content',
       'not found; wax content not stated in TŞ 05766698-60-2006 specification table')

    # ── not_in_template ───────────────────────────────────────────────────────
    if color_astm_max:
        _nit(pk, 'color',
             f'Color by ASTM, max: {color_astm_max}',
             hi=str(color_astm_max), qual='<=', vk='bound',
             notes='ASTM color scale; printed in separate column from ЦНТ (Russian) color')
    else:
        _nit(pk, 'color',
             f'Color by ЦНТ, max: {color_cnt_max}',
             hi=str(color_cnt_max), qual='<=', vk='bound',
             notes='ЦНТ color; no ASTM color column given for this grade')
    _nit(pk, 'acid_number',
         f'Acidity number, mg KOH by 1g oil, not more than: {acid_max}',
         unit='mg KOH/g', hi=str(acid_max), qual='<=', vk='bound',
         notes='total acid number (TAN); spec upper bound')
    _nit(pk, 'ash',
         'Ash, %, not more than: 0.005',
         unit='%', hi='0.005', qual='<=', vk='bound',
         notes='ash content (not sulfated ash); single upper bound for all five grades')
    _nit(pk, 'mechanical_impurities',
         'Mass portion of mechanical impurities, %, not more than: 0.005',
         unit='%', hi='0.005', qual='<=', vk='bound',
         notes='mechanical impurities (filterable solids); single upper bound for all grades')
    _nit(pk, 'refraction_coefficient',
         'Refraction coefficient at 20°C: Have no standard, is necessary',
         vk='text',
         notes='document states "Have no standart, is nessesary" — no numerical value given; '
               'measurement required but no spec limit defined in this standard')


# ──────────────────────────────────────────────────────────────────────────────
# Map all five products
# args: pk, kv100_lo, kv100_hi, vi_min, density_max, pour_max, flash_min,
#       color_cnt_max, color_astm_max (None if not given), acid_max
# ──────────────────────────────────────────────────────────────────────────────

_map_product('TURKMENBASHY:SN80',
             kv100_lo=2.5,  kv100_hi=3.5,  vi_min=95, density_max=870,
             pour_max=-12,  flash_min=170,
             color_cnt_max=0.5, color_astm_max=None, acid_max=0.02)

_map_product('TURKMENBASHY:SN180',
             kv100_lo=4.5,  kv100_hi=6.0,  vi_min=95, density_max=880,
             pour_max=-12,  flash_min=205,
             color_cnt_max=0.5, color_astm_max=None, acid_max=0.03)

_map_product('TURKMENBASHY:SN350',
             kv100_lo=8.0,  kv100_hi=9.5,  vi_min=95, density_max=890,
             pour_max=-12,  flash_min=220,
             color_cnt_max=1.0, color_astm_max=1.0, acid_max=0.05)

_map_product('TURKMENBASHY:SN600',
             kv100_lo=11.5, kv100_hi=13.5, vi_min=95, density_max=900,
             pour_max=-9,   flash_min=225,
             color_cnt_max=2.0, color_astm_max=2.0, acid_max=0.05)

_map_product('TURKMENBASHY:SN1200',
             kv100_lo=18.0, kv100_hi=23.0, vi_min=90, density_max=905,
             pour_max=-9,   flash_min=250,
             color_cnt_max=3.0, color_astm_max=3.0, acid_max=0.06)

# ──────────────────────────────────────────────────────────────────────────────
write_rows('s58_turkmenbashy.csv', ROWS)
if __name__ == '__main__':
    print(f's58_turkmenbashy: {len(ROWS)} rows written to field_evidence/s58_turkmenbashy.csv')
