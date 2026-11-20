"""Field-level mapping, S60 Micro — 2 products, 2 documents.

Products:
  MINGLAN:T106D_SUP_HIGH_TBN_CA_SUL — super high TBN synthetic calcium sulfonate detergent
    Supplier: Shanghai Minglan Chemical Co., Ltd.
  TANEE:TE_598 — dialkyl diphenylamine (DDPA) ashless antioxidant
    Supplier: Tanee Chemical Ltd, Beijing, China

Documents:
  0722625048bb  DL2-15278.pdf  2022-02-21  T106D Super High TBN Ca Sulfonate TDS (1pp)
  613671bd2b28  DL2-15242.pdf  2023-08-16  TE-598 Dialkyl Di Phenylamine TDS (1pp)

Document notes:
  T106D TDS: Specification table — Appearance (Visual), Density @20°C 1150-1250 kg/m³,
    Kinematic Viscosity @100°C "Report" (no value), Flash Point COC ≥180°C, TBN ≥395 mgKOH/g,
    Calcium ≥14.5 m%, Sulfur ≥1.2 m%, Water ≤0.2 m%, Machinery Impurities ≤0.1 m%.
    kv100 is a "Report" item — no spec limit and no batch value printed; recorded as Missing.
    Product described as "preferred additive for blending over-based marine cylinder oil".
    Packing: 200L metal drum. Storage ≤45°C.
  TE-598 TDS: Specification table — Density @20°C 900-1000 kg/cm³ (sic: unit misprint, should
    be kg/m³; 900-1000 kg/m³ = 0.90-1.00 g/cm³ consistent with DDPA), Flash Point (open cup)
    180°C, Kinematic Viscosity @40°C 100-350 mm²/s, TBN 152-172 mgKOH/g, Diphenylamine ≤1.0 m%,
    Nitrogen 3.8-5.5 m%, Water ≤0.15 m%, Impurities ≤0.01 m%.
    Treat rate: "The dosage is from 0.25% to 0.5%."

Writes field_evidence/s60_micro.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '0722625048bb': ('DL2-15278.pdf', '2022-02-21'),  # T106D TDS
    '613671bd2b28': ('DL2-15242.pdf', '2023-08-16'),  # TE-598 TDS
}

REVIEW = 'sheets read in full (text layer) 2026-11-16; single-page TDS, all rows read'
VC_TDS = 'product data sheet (TDS), typical properties table'

T106D = 'MINGLAN:T106D_SUP_HIGH_TBN_CA_SUL'
TE598 = 'TANEE:TE_598'

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


# ===========================================================================
# MINGLAN:T106D_SUP_HIGH_TBN_CA_SUL — super high TBN synthetic calcium sulfonate
# ===========================================================================

_r(T106D, 'component_general', 'function.primary',
   'super high-based synthetic calcium sulfonate prepared by neutralization and super high '
   'alkalization reaction; preferred additive for blending over-based marine cylinder oil',
   vk='text', sha='0722625048bb',
   notes='from product introduction in TDS; overbased detergent with strong acid neutralisation '
         'capability; stated for marine cylinder oil use')

_m(T106D, 'component_general', 'function.secondary',
   'not found; product introduction mentions high-temperature detergency and thermal stability '
   'but these are described as properties, not separate functions')

_r(T106D, 'component_general', 'chemical_family',
   'overbased synthetic calcium sulfonate (heavy alkyl benzene sulfonate base)',
   vk='text', sha='0722625048bb',
   notes='from TDS product introduction: "With heavy alkyl benzene sulfonic acid as a main '
         'raw material, super high-based synthetic calcium sulfonate is prepared by '
         'neutralization and super high alkalization reaction"')

_m(T106D, 'component_general', 'active_content',
   'not found; active sulfonate content not stated in TDS')

_m(T106D, 'component_general', 'carrier.identity',
   'not found; no carrier or diluent mentioned in TDS')

_m(T106D, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated')

_m(T106D, 'component_general', 'treat_rate',
   'not found; no recommended treat rate stated in TDS; '
   'product described as an overbased detergent used in additive packages for marine cylinder oil')

_r(T106D, 'component_general', 'compatibility_restrictions',
   'preferred additive for blending over-based marine cylinder oil',
   vk='text', sha='0722625048bb',
   notes='from TDS product introduction; stated application is marine cylinder oil; '
         'no explicit restrictions on other oil types')

_r(T106D, 'component_general', 'function_specific_markers.tbn',
   'TBN, mgKOH/g: >=395',
   unit='mgKOH/g', lo='395', qual='>=', vk='bound',
   meth='SH/T0251,ASTM D2896',
   sha='0722625048bb',
   notes='minimum spec bound; super high TBN overbased calcium sulfonate detergent')

_r(T106D, 'component_general', 'function_specific_markers.ca',
   'Calcium, m%: >=14.5',
   unit='m%', lo='14.5', qual='>=', vk='bound',
   meth='GB/T17476,SH/T0270,SH/T0297,ASTM D4951',
   sha='0722625048bb',
   notes='minimum spec bound; wt% by context (m% = mass percent in Chinese standards)')

_m(T106D, 'component_general', 'function_specific_markers.mg',
   'not found; calcium sulfonate — no magnesium stated')
_m(T106D, 'component_general', 'function_specific_markers.p',
   'not found; overbased calcium sulfonate — no phosphorus stated')
_m(T106D, 'component_general', 'function_specific_markers.zn',
   'not found')
_m(T106D, 'component_general', 'function_specific_markers.mo',
   'not found')

# not_in_template for T106D
_nit(T106D, 'density',
     'Density(20°C), kg/m3: 1150-1250',
     unit='kg/m3', lo='1150', hi='1250', vk='range',
     meth='GB/T13377,ASTM D4052', cond='20°C',
     sha='0722625048bb',
     notes='specification range at 20°C (non-standard temperature for most base oil templates); '
           'high density consistent with heavily overbased calcium sulfonate (CaCO3 dispersion)')

_nit(T106D, 'flash_point',
     'Flash Point(COC), °C: >=180',
     unit='°C', lo='180', qual='>=', vk='bound',
     meth='GB/T3536,ASTM D92',
     sha='0722625048bb')

_nit(T106D, 'sulfur_content',
     'Sulfur, m%: >=1.2',
     unit='m%', lo='1.2', qual='>=', vk='bound',
     meth='GB/T17476,SH/T0303,ASTM D1552',
     sha='0722625048bb',
     notes='minimum spec bound; sulfur from sulfonate anion moiety; m% = wt%')

_nit(T106D, 'water_content',
     'Water Content, m%: <=0.2',
     unit='m%', hi='0.2', qual='<=', vk='bound',
     meth='GB/T260,ASTM D95',
     sha='0722625048bb')


# ===========================================================================
# TANEE:TE_598 — dialkyl diphenylamine (DDPA) ashless antioxidant
# ===========================================================================

_r(TE598, 'component_general', 'function.primary',
   'TE-598: Dialkyl Di Phenylamine; ashless antioxidant providing excellent '
   'high-temperature anti-oxidation and oil solubility',
   vk='text', sha='613671bd2b28',
   notes='from TDS product description: "It is an ashless antioxidant. '
         'The product is a light yellow liquid, prepared from diphenylamine and olefin."')

_r(TE598, 'component_general', 'function.secondary',
   'can also be used as rubber antioxidant',
   vk='text', sha='613671bd2b28',
   notes='from TDS applications section: secondary application outside lubricants')

_r(TE598, 'component_general', 'chemical_family',
   'dialkyl diphenylamine (DDPA)',
   vk='text', sha='613671bd2b28',
   notes='from TDS product name and description: "Dialkyl Di Phenylamine"; '
         'prepared from diphenylamine and olefin — standard DDPA synthesis route')

_m(TE598, 'component_general', 'active_content',
   'not found; active content (DDPA %) not stated; '
   'Diphenylamine residual ≤1.0 m% is a purity spec, not an active content statement')

_m(TE598, 'component_general', 'carrier.identity',
   'not found; product is described as a "light yellow liquid"; no carrier stated')

_m(TE598, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated')

_r(TE598, 'component_general', 'treat_rate',
   'The dosage is from 0.25% to 0.5%.',
   unit='%', lo='0.25', hi='0.5', vk='range',
   sha='613671bd2b28',
   notes='from TDS applications section; applies to stated end uses: internal combustion '
         'engine oils, turbine oils, heat conducting oils, hydraulic oils, greases, fuel oils')

_r(TE598, 'component_general', 'compatibility_restrictions',
   'can be used in internal combustion engine oils, turbine oils, heat conducting oils, '
   'hydraulic oils and greases, and fuel oils as well',
   vk='text', sha='613671bd2b28',
   notes='from TDS applications section; no restrictions stated; broad application stated')

_r(TE598, 'component_general', 'function_specific_markers.tbn',
   'TBN, mg KOH/g: 152-172',
   unit='mgKOH/g', lo='152', hi='172', vk='range',
   meth='SH/T 0251',
   sha='613671bd2b28',
   notes='TBN is from ashless amine nitrogen (diphenylamine-based), not from metal-based '
         'alkalinity; range reflects spec; method SH/T 0251 (equivalent to ASTM D2896)')

_m(TE598, 'component_general', 'function_specific_markers.ca',
   'not found; ashless antioxidant — no calcium stated')
_m(TE598, 'component_general', 'function_specific_markers.mg',
   'not found')
_m(TE598, 'component_general', 'function_specific_markers.p',
   'not found; DDPA is nitrogen-based, not phosphorus-based')
_m(TE598, 'component_general', 'function_specific_markers.zn',
   'not found')
_m(TE598, 'component_general', 'function_specific_markers.mo',
   'not found')

# not_in_template for TE_598
_nit(TE598, 'density',
     'Density (20°C), kg/cm3: 900-1000',
     unit='kg/m3', lo='900', hi='1000', vk='range',
     meth='GB/T 1884', cond='20°C',
     sha='613671bd2b28',
     notes='TDS prints unit as "kg/cm3" which is physically impossible for a liquid; '
           'correct unit is kg/m3 (900-1000 kg/m3 = 0.90-1.00 g/cm3 consistent with DDPA density); '
           'recorded as kg/m3 with note of TDS misprint')

_nit(TE598, 'flash_point',
     'Flash Point (open cup), °C: 180',
     unit='°C', value='180', vk='typical',
     meth='GB/T 267',
     sha='613671bd2b28',
     notes='open cup method; single spec value printed as typical')

_nit(TE598, 'kv40',
     'Kinematics Viscosity (40°C), mm2/s: 100~350',
     unit='mm2/s', lo='100', hi='350', vk='range',
     meth='GB/T 265', cond='40°C',
     sha='613671bd2b28',
     notes='wide range reflects variability in DDPA alkyl chain length distribution')

_nit(TE598, 'nitrogen_content',
     'Nitrogen, m%: 3.8-5.5',
     unit='m%', lo='3.8', hi='5.5', vk='range',
     meth='SH/T 0224',
     sha='613671bd2b28',
     notes='nitrogen is the functional marker for amine-based antioxidants (DDPA); m% = wt%')

_nit(TE598, 'diphenylamine_residual',
     'Diphenylamine, m%: 1.0',
     unit='m%', hi='1.0', qual='<=', vk='bound',
     meth='Chromatography',
     sha='613671bd2b28',
     notes='purity spec: unreacted diphenylamine monomer residual ≤1.0 m%')

_nit(TE598, 'water_content',
     'Water, m%: 0.15',
     unit='m%', hi='0.15', qual='<=', vk='bound',
     meth='GB/T 260',
     sha='613671bd2b28')


# ===========================================================================
write_rows('s60_micro.csv', ROWS)
if __name__ == '__main__':
    print(f's60_micro: {len(ROWS)} rows written to field_evidence/s60_micro.csv')
