"""Field-level mapping, S36 Elco (Italmatch Chemicals) — 4 additive component products.

All Elco TDS sheets are single-page (or two-page with p.1 characteristics, p.2 performance data).
All give typical values only. No revision dates except ELCO_87 and ELCO_88 (Rev. 8/18 = Aug 2018).

Products (all additive_component, component_general template):
  ELCO:ELCO_301   Antiwear and Rust Inhibitor          DL2-12590  sha12 511a2613091d
  ELCO:ELCO_313A  Slideway Lubricant Additive           DL2-11863  sha12 fc26ec81dc2a
  ELCO:ELCO_87    Extreme Pressure Grease Additive      DL2-12322  sha12 88450484ca43
  ELCO:ELCO_88    Partial Additive Package for Grease   DL2-12323  sha12 6380d36231d5

Notes:
- ELCO_301: Neutralization Number (ASTM D974) 160 mgKOH/g is TDS acid-base number for the
  concentrate, not TBN (ASTM D2896); mapped to not_in_template:neutralization_number.
- ELCO_301: N 3.5% — Nitrogen is not in function_specific_markers (which has tbn/ca/mg/p/zn/mo);
  mapped to not_in_template:nitrogen.
- ELCO_87/88: "Rev. 8/18" in footer → revision August 2018 (day unknown); recorded as '2018-08'.
- ELCO_88: Flash Point uses ASTM D93 (Pensky-Martens), not D92 (Cleveland); recorded as printed.

Writes field_evidence/s36_elco.csv."""
import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud = {r['sha256'][:12]: r for r in csv.DictReader(
    open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '511a2613091d': ('DL2-12590.pdf', ''),       # ELCO_301 TDS; no date
    'fc26ec81dc2a': ('DL2-11863.pdf', ''),        # ELCO_313A TDS; no date
    '88450484ca43': ('DL2-12322.pdf', '2018-08'), # ELCO_87 TDS; Rev. 8/18 (Aug 2018, day unknown)
    '6380d36231d5': ('DL2-12323.pdf', '2018-08'), # ELCO_88 TDS; Rev. 8/18 (Aug 2018, day unknown)
}

REVIEW = 'sheet read in full (text layer) 2026-11-16; both pages of each TDS parsed'
VC_TDS = 'product data sheet, characteristics table'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', sha=None, pg=1, notes=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': tmpl, 'field': field, 'entry': '',
        'value': str(value), 'qualifier': qual, 'min': str(lo), 'max': str(hi),
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': '',
        'status': 'Reported', 'value_class': VC_TDS, 'basis': '',
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


def _nit(pk, prop, printed, sha=None, pg=1, unit='', value='', lo='', hi='', qual='', vk='typical', meth='', notes=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop, 'entry': '',
        'value': str(value), 'qualifier': qual, 'min': str(lo), 'max': str(hi),
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': '',
        'status': 'Reported', 'value_class': VC_TDS, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': REVIEW,
    })


# ──────────────────────────────────────────────────────────────────────────────
# ELCO_301  DL2-12590.pdf  sha 511a2613091d
# Antiwear and Rust Inhibitor; N 3.5%, P 5.5%; treat rate 0.05-5.0 wt%
# ──────────────────────────────────────────────────────────────────────────────
PK = 'ELCO:ELCO_301'
S  = '511a2613091d'

_r(PK, 'component_general', 'function.primary',
   'Elco 301 is a multifunctional additive which imparts antiwear and rust inhibiting properties',
   vk='text', sha=S,
   notes='from Features section of TDS')
_r(PK, 'component_general', 'function.secondary',
   'can also improve demulsibility properties of the finished lubricant',
   vk='text', sha=S,
   notes='from Features section of TDS')
_m(PK, 'component_general', 'chemical_family',
   'not found; chemical family not stated in TDS (contains N 3.5% and P 5.5%)')
_m(PK, 'component_general', 'active_content',
   'not found; active content percentage not stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; carrier identity not stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct',
   'not found; carrier share not stated in TDS')
_r(PK, 'component_general', 'treat_rate',
   'The recommended treat level of Elco 301 ranges from 0.05 - 5.0 wt%',
   unit='wt%', lo='0.05', hi='5.0', vk='range', sha=S,
   notes='from Application section; range depends on the operation')
_r(PK, 'component_general', 'compatibility_restrictions',
   'Group I and Group II base oils; oil and grease formulations',
   vk='text', sha=S, pg=2,
   notes='from performance data table on p.2 (Group I ISO 32, Group II ISO 22 shown); '
         'no explicit incompatibility stated')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; TBN not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; Ca not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; Mg not stated in TDS')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus: 5.5%',
   unit='wt%', value='5.5', sha=S,
   notes='listed under Chemical section; Typical value; no method cited')
_m(PK, 'component_general', 'function_specific_markers.zn',
   'not found; Zn not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; Mo not stated in TDS')

_nit(PK, 'flash_point',
     'Flash Point, ASTM D92: 70°C min',
     sha=S, unit='°C', lo='70', qual='>=', vk='bound', meth='ASTM D92')
_nit(PK, 'neutralization_number',
     'Neutralization Number, ASTM D974: 160 mgKOH/g',
     sha=S, unit='mgKOH/g', value='160', meth='ASTM D974',
     notes='Neutralization Number (ASTM D974) for the additive concentrate; '
           'not TBN (ASTM D2896)')
_nit(PK, 'specific_gravity',
     'Specific Gravity @ 15.6°C, ASTM D1298: 0.94 (7.84 lb/gal)',
     sha=S, value='0.94', meth='ASTM D1298',
     notes='printed as 0.94 (7.84 lb/gal); dimensionless')
_nit(PK, 'kv40',
     'Viscosity @ 40°C, ASTM D7042: 430 cSt',
     sha=S, unit='cSt', value='430', meth='ASTM D7042')
_nit(PK, 'kv100',
     'Viscosity @ 100°C, ASTM D7042: 20 cSt',
     sha=S, unit='cSt', value='20', meth='ASTM D7042')
_nit(PK, 'nitrogen',
     'Nitrogen: 3.5%',
     sha=S, unit='wt%', value='3.5',
     notes='listed under Chemical section; not in function_specific_markers template fields')


# ──────────────────────────────────────────────────────────────────────────────
# ELCO_313A  DL2-11863.pdf  sha fc26ec81dc2a
# Slideway Lubricant Additive; P 0.4%, S 16.0%; treat rate 1.75 wt%
# ──────────────────────────────────────────────────────────────────────────────
PK = 'ELCO:ELCO_313A'
S  = 'fc26ec81dc2a'

_r(PK, 'component_general', 'function.primary',
   'Elco 313A is a slideway additive that provides a wide range of benefits in an appropriate base stock',
   vk='text', sha=S,
   notes='from Features section; benefits include stick-slip, antiwear/EP, filterability, demulsibility, oxidation stability')
_r(PK, 'component_general', 'function.secondary',
   'antiwear and EP performance; filterability and demulsibility',
   vk='text', sha=S,
   notes='from Features section of TDS')
_m(PK, 'component_general', 'chemical_family',
   'not found; chemical family not stated in TDS (contains P 0.4% and S 16.0%)')
_m(PK, 'component_general', 'active_content',
   'not found; active content percentage not stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; carrier identity not stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct',
   'not found; carrier share not stated in TDS')
_r(PK, 'component_general', 'treat_rate',
   'At a treatment level of 1.75 wt% (1.50% volume), Elco 313A meets requirements of Cincinnati Machine P-47/P-50/P-53 and GM LS-2',
   unit='wt%', value='1.75', sha=S,
   notes='from Application section; treat rate is a specific performance level, not a range; '
         'volume equivalent 1.50% also stated')
_r(PK, 'component_general', 'compatibility_restrictions',
   'Soluble / compatible in Group I, II, III base stocks',
   vk='text', sha=S,
   notes='from Features section; compatible with most industrial soluble oils and coolants')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; TBN not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; Ca not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; Mg not stated in TDS')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus, ASTM D6481: 0.4%',
   unit='wt%', value='0.4', meth='ASTM D6481', sha=S,
   notes='listed under Chemical section; Typical value')
_m(PK, 'component_general', 'function_specific_markers.zn',
   'not found; Zn not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; Mo not stated in TDS')

_nit(PK, 'flash_point',
     'Flash Point, ASTM D92: 110°C min',
     sha=S, unit='°C', lo='110', qual='>=', vk='bound', meth='ASTM D92')
_nit(PK, 'specific_gravity',
     'Specific Gravity @ 15.6°C, ASTM D1298: 0.96 (8.00 lb/gal)',
     sha=S, value='0.96', meth='ASTM D1298',
     notes='printed as 0.96 (8.00 lb/gal)')
_nit(PK, 'kv40',
     'Viscosity @ 40°C, ASTM D7042: 15 cSt',
     sha=S, unit='cSt', value='15', meth='ASTM D7042')
_nit(PK, 'kv100',
     'Viscosity @ 100°C, ASTM D7042: 4 cSt',
     sha=S, unit='cSt', value='4', meth='ASTM D7042')
_nit(PK, 'sulfur',
     'Sulfur, ASTM D6481: 16.0%',
     sha=S, unit='wt%', value='16.0', meth='ASTM D6481')


# ──────────────────────────────────────────────────────────────────────────────
# ELCO_87  DL2-12322.pdf  sha 88450484ca43  Rev. 8/18
# Extreme Pressure Grease Additive; S 14.0%, P 4.7%, Zn 4.7%; treat rate 4.0-6.0 wt%
# ──────────────────────────────────────────────────────────────────────────────
PK = 'ELCO:ELCO_87'
S  = '88450484ca43'

_r(PK, 'component_general', 'function.primary',
   'Elco 87 is a partial additive package for use in blending extreme pressure industrial grease',
   vk='text', sha=S,
   notes='from Features section of TDS')
_r(PK, 'component_general', 'function.secondary',
   'antiwear performance in grease',
   vk='text', sha=S,
   notes='from Application section: "impart extreme pressure and antiwear to the grease"')
_m(PK, 'component_general', 'chemical_family',
   'not found; chemical family not stated in TDS (contains S 14.0%, P 4.7%, Zn 4.7%)')
_m(PK, 'component_general', 'active_content',
   'not found; active content percentage not stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; carrier identity not stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct',
   'not found; carrier share not stated in TDS')
_r(PK, 'component_general', 'treat_rate',
   'At concentrations of 4.0 – 6.0 wt%',
   unit='wt%', lo='4.0', hi='6.0', vk='range', sha=S,
   notes='from Application section; range for extreme pressure and antiwear performance')
_r(PK, 'component_general', 'compatibility_restrictions',
   'for use in Lithium Complex Grease and Lithium Soap Grease',
   vk='text', sha=S, pg=1,
   notes='from performance characteristics table on p.1 (6% Elco 87 in Lithium Complex/Soap Grease)')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; TBN not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; Ca not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; Mg not stated in TDS')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus, ASTM D6481: 4.7%',
   unit='wt%', value='4.7', meth='ASTM D6481', sha=S,
   notes='listed under Chemical section; Typical value')
_r(PK, 'component_general', 'function_specific_markers.zn',
   'Zinc, ASTM D6481: 4.7%',
   unit='wt%', value='4.7', meth='ASTM D6481', sha=S,
   notes='listed under Chemical section; Typical value')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; Mo not stated in TDS')

_nit(PK, 'flash_point',
     'Flash Point, ASTM D92: 150°C min',
     sha=S, unit='°C', lo='150', qual='>=', vk='bound', meth='ASTM D92')
_nit(PK, 'specific_gravity',
     'Specific Gravity @ 15.6°C, ASTM D1298: 1.04 (8.7 lb/gal)',
     sha=S, value='1.04', meth='ASTM D1298')
_nit(PK, 'kv40',
     'Viscosity @ 40°C, ASTM D7042: 160 cSt',
     sha=S, unit='cSt', value='160', meth='ASTM D7042')
_nit(PK, 'kv100',
     'Viscosity @ 100°C, ASTM D7042: 15 cSt',
     sha=S, unit='cSt', value='15', meth='ASTM D7042')
_nit(PK, 'sulfur',
     'Sulfur, ASTM D6481: 14.0%',
     sha=S, unit='wt%', value='14.0', meth='ASTM D6481')


# ──────────────────────────────────────────────────────────────────────────────
# ELCO_88  DL2-12323.pdf  sha 6380d36231d5  Rev. 8/18
# Partial Additive Package for Grease; Zn 5.5%, S 32.0%, P 4.5%; treat rate 3.0-4.0 wt%
# ──────────────────────────────────────────────────────────────────────────────
PK = 'ELCO:ELCO_88'
S  = '6380d36231d5'

_r(PK, 'component_general', 'function.primary',
   'Elco 88 is a multipurpose additive for non-soap thickened greases to improve extreme pressure, antiwear performance, and oxidation stability',
   vk='text', sha=S,
   notes='from Features section of TDS')
_r(PK, 'component_general', 'function.secondary',
   'copper corrosion inhibition',
   vk='text', sha=S,
   notes='from Application section: "copper corrosion inhibition to oxidatively stable, non-soap thickened greases"')
_m(PK, 'component_general', 'chemical_family',
   'not found; chemical family not stated in TDS (contains Zn 5.5%, S 32.0%, P 4.5%)')
_m(PK, 'component_general', 'active_content',
   'not found; active content percentage not stated in TDS')
_m(PK, 'component_general', 'carrier.identity',
   'not found; carrier identity not stated in TDS')
_m(PK, 'component_general', 'carrier.share_wt_pct',
   'not found; carrier share not stated in TDS')
_r(PK, 'component_general', 'treat_rate',
   'At treat rates of 3.0 - 4.0 wt%',
   unit='wt%', lo='3.0', hi='4.0', vk='range', sha=S,
   notes='from Application section; for non-soap thickened greases in sealed-for-life applications')
_r(PK, 'component_general', 'compatibility_restrictions',
   'for non-soap thickened greases; tested in NLGI#1 Polyurea Base Grease',
   vk='text', sha=S,
   notes='from Application and performance data sections')
_m(PK, 'component_general', 'function_specific_markers.tbn',
   'not found; TBN not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.ca',
   'not found; Ca not stated in TDS')
_m(PK, 'component_general', 'function_specific_markers.mg',
   'not found; Mg not stated in TDS')
_r(PK, 'component_general', 'function_specific_markers.p',
   'Phosphorus, ASTM D6481: 4.5%',
   unit='wt%', value='4.5', meth='ASTM D6481', sha=S,
   notes='listed under Chemical section; Typical value')
_r(PK, 'component_general', 'function_specific_markers.zn',
   'Zinc, ASTM D6481: 5.5%',
   unit='wt%', value='5.5', meth='ASTM D6481', sha=S,
   notes='listed under Chemical section; Typical value')
_m(PK, 'component_general', 'function_specific_markers.mo',
   'not found; Mo not stated in TDS')

_nit(PK, 'flash_point',
     'Flash Point, ASTM D93: 90°C min',
     sha=S, unit='°C', lo='90', qual='>=', vk='bound', meth='ASTM D93',
     notes='ASTM D93 (Pensky-Martens closed cup), not D92 (Cleveland open cup); recorded as printed')
_nit(PK, 'specific_gravity',
     'Specific Gravity @ 15.6°C, ASTM D1298: 1.16 (9.7 lb/gal)',
     sha=S, value='1.16', meth='ASTM D1298')
_nit(PK, 'kv40',
     'Viscosity @ 40°C, ASTM D7042: 115 cSt',
     sha=S, unit='cSt', value='115', meth='ASTM D7042')
_nit(PK, 'kv100',
     'Viscosity @ 100°C, ASTM D7042: 15 cSt',
     sha=S, unit='cSt', value='15', meth='ASTM D7042')
_nit(PK, 'sulfur',
     'Sulfur, ASTM D6481: 32.0%',
     sha=S, unit='wt%', value='32.0', meth='ASTM D6481')


# ──────────────────────────────────────────────────────────────────────────────
write_rows('s36_elco.csv', ROWS)
if __name__ == '__main__':
    print(f's36_elco: {len(ROWS)} rows written to field_evidence/s36_elco.csv')
