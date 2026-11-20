"""Field-level mapping, S37 Chemtura / SI Group — 3 products, 4 documents.

Products:
  SIGROUP:ETHAFLOW_6705    — SI Group ETHAFLOW 6705 phosphite antiwear/antioxidant
    additive_component (component_general); 2 docs: DL2-15396 (SDS R1.4 2022-12-08),
    DL2-15397 (TDS R2 7/22)
  SIGROUP:ETHANOX_4703     — SI Group ETHANOX 4703 hindered-phenol/amine antioxidant
    additive_component (component_general); 1 doc: DL2-15381 (TDS UT05582 08/14)
  CHEMTURA:NAUGALUBE_16    — Chemtura Naugalube 16 sulfur-phenolic antioxidant
    additive_component (component_general); 1 doc: DL2-13771 (TDS issued 7/2006)

Document notes:
  DL2-15396 (ETHAFLOW SDS, REACH/EU, Revision 1.4): Section 3 lists "No hazardous ingredients"
    (single substance, all components below hazard threshold); Section 9 gives flash point (CC)
    228°C and dynamic viscosity 1970 mPa.s @40°C; no density listed (Density: "Not available").
  DL2-15397 (ETHAFLOW TDS, R2 July 2022): "proprietary liquid phosphite ashless-antiwear
    additive"; P content 5.2%, density @25°C 1.02 g/cm³, flash point (CC) 228°C, viscosity
    @40°C 1715 cP (dynamic); treat rate 0.5-1.5 wt% lubricants, 0.7-3.0 wt% greases.
    TDS and SDS viscosity @40°C slightly differ (1715 vs 1970): both recorded; TDS selected per
    Rule 2 (technical document preferred where both exist).
  DL2-15381 (ETHANOX 4703 TDS, UT05582 08/14): crystalline powder; TBN 214 mgKOH/g;
    flash point (COC) >93°C (stated as min); hindered phenol + aliphatic amine structure.
  DL2-13771 (NAUGALUBE 16 TDS, issued 7/2006): crystalline white powder, CAS 96-69-5;
    specific gravity 1.10 (20/20°C), flash point 215°C (CC), sulfur 8.9 wt%;
    treat rate 0.1-1.0 wt%.

Writes field_evidence/s37_chemtura.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '056ae1411750': ('DL2-15396.pdf', '2022-12-08'),  # ETHAFLOW SDS rev 1.4
    '358fecf67a8f': ('DL2-15397.pdf', '2022-07-01'),  # ETHAFLOW TDS R2 7/22
    '1919f6444880': ('DL2-15381.pdf', '2014-08-01'),  # ETHANOX_4703 TDS UT05582 08/14
    'b6b41d837bf7': ('DL2-13771.pdf', '2006-07-01'),  # NAUGALUBE_16 TDS issued 7/2006
}

REVIEW_ETH  = ('sheets read in full (text layer) 2026-11-16; '
               '2 docs: TDS DL2-15397 (R2 7/22), SDS DL2-15396 (rev 1.4 2022-12-08)')
REVIEW_4703 = ('sheet read in full (text layer) 2026-11-16; '
               '1 doc: TDS DL2-15381 (UT05582 08/14)')
REVIEW_NL16 = ('sheet read in full (text layer) 2026-11-16; '
               '1 doc: TDS DL2-13771 (issued 7/2006)')

VC_TDS = 'product data sheet (TDS/PDS), typical properties table'
VC_SDS = 'safety data sheet (SDS), Section 9 physical properties'

ETH  = 'SIGROUP:ETHAFLOW_6705'
E703 = 'SIGROUP:ETHANOX_4703'
NL16 = 'CHEMTURA:NAUGALUBE_16'

ROWS = []


def _r(pk, tmpl, field, printed, unit='', value='', qual='', lo='', hi='', vk='typical',
       meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_TDS, review=''):
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
         meth='', cond='', sha='', pg=1, notes='', vc=VC_TDS, review=''):
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


# ===========================================================================
# SIGROUP:ETHAFLOW_6705
# ===========================================================================

_r(ETH, 'component_general', 'function.primary',
   'ETHAFLOW 6705 is a proprietary liquid phosphite ashless-antiwear additive.',
   vk='text', sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
   notes='from TDS product description; TDS also states the product is '
         '"multifunctional, supplying antioxidant and friction modification properties"')

_r(ETH, 'component_general', 'function.secondary',
   'ETHAFLOW 6705 is also multifunctional, supplying antioxidant and friction '
   'modification properties to formulated lubricants and greases.',
   vk='text', sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
   notes='secondary functions stated in TDS product description alongside primary antiwear function')

_r(ETH, 'component_general', 'chemical_family',
   'proprietary liquid phosphite (ashless)',
   vk='text', sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
   notes='chemical family from TDS description; "proprietary" means exact phosphite '
         'structure is not disclosed; SDS Section 3 lists "No hazardous ingredients" '
         '(single substance, components below hazard threshold per REACH)')

_m(ETH, 'component_general', 'active_content',
   'not found; product is described as a neat liquid with no diluent; active '
   'content % not stated; SDS Section 3 gives no component percentage',
   review=REVIEW_ETH)
_m(ETH, 'component_general', 'carrier.identity',
   'not found; described as a neat liquid additive; no carrier stated',
   review=REVIEW_ETH)
_m(ETH, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_ETH)

_r(ETH, 'component_general', 'treat_rate',
   'For lubricants, the dosage of ETHAFLOW 6705 ... typical dosage range is 0.5 – 1.5 wt%.',
   unit='wt%', lo='0.5', hi='1.5', vk='range',
   sha='358fecf67a8f', pg=2, vc=VC_TDS, review=REVIEW_ETH,
   entry='lubricants')
_r(ETH, 'component_general', 'treat_rate',
   'For greases, the dosage of ETHAFLOW 6705 is 0.7 – 3.0 wt%.',
   unit='wt%', lo='0.7', hi='3.0', vk='range',
   sha='358fecf67a8f', pg=2, vc=VC_TDS, review=REVIEW_ETH,
   entry='greases')

_r(ETH, 'component_general', 'compatibility_restrictions',
   'ETHAFLOW 6705 is nonylphenol-free and has excellent solubility in all types of '
   'base stocks (Group I – V).',
   vk='text', sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
   notes='no compatibility restrictions stated; Group I-V solubility stated positively')

_m(ETH, 'component_general', 'function_specific_markers.tbn',
   'not found; ashless antiwear/antioxidant phosphite — TBN not stated',
   review=REVIEW_ETH)
_m(ETH, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_ETH)
_m(ETH, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_ETH)
_r(ETH, 'component_general', 'function_specific_markers.p',
   'Phosphorus Content, %: 5.2',
   unit='%', value='5.2', vk='typical',
   sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
   notes='from Typical Physical Properties table in TDS; unit printed as "%" (interpreted '
         'as wt%); no test method printed')
_m(ETH, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_ETH)
_m(ETH, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_ETH)

# not_in_template for ETHAFLOW_6705
_nit(ETH, 'density',
     'Density at 25°C, g/cm3: 1.02',
     unit='g/cm3', value='1.02', vk='typical',
     cond='25°C',
     sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
     notes='from TDS Typical Physical Properties; temperature 25°C (non-standard; '
           'SDS Section 9 states density "Not available")')
_nit(ETH, 'flash_point',
     'Flash Point (CC), °C: 228',
     unit='°C', value='228', vk='typical',
     meth='closed cup',
     sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
     notes='TDS and SDS agree: both give 228°C closed cup; selected from TDS per Rule 2')
_nit(ETH, 'dynamic_viscosity',
     'Viscosity at 40°C, cP: 1,715',
     unit='cP', value='1715', vk='typical',
     cond='40°C',
     sha='358fecf67a8f', pg=1, vc=VC_TDS, review=REVIEW_ETH,
     notes='from TDS; SDS Section 9 gives 1970 mPa.s @40°C (same unit, different value); '
           'TDS value selected per Rule 2; SDS value in alternate (see SDS row)')
_nit(ETH, 'dynamic_viscosity',
     'Viscosity, dynamic: 1,970 mPa.s (40°C)',
     unit='mPa.s', value='1970', vk='typical',
     cond='40°C',
     sha='056ae1411750', pg=5, vc=VC_SDS, review=REVIEW_ETH,
     notes='from SDS Section 9; TDS gives 1715 cP @40°C (same unit, cP=mPa.s for '
           'dynamic viscosity) — values differ; TDS selected per Rule 2; this is alternate')


# ===========================================================================
# SIGROUP:ETHANOX_4703
# ===========================================================================

_r(E703, 'component_general', 'function.primary',
   'ETHANOX 4703 lubricant antioxidant is a unique polar molecule containing a '
   'hindered phenol structure and an aliphatic amine group. It is effective at high '
   'temperatures, which makes it particularly suitable for industrial lubricants.',
   vk='text', sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703)

_r(E703, 'component_general', 'function.secondary',
   'Ashless TBN source for the neutralization of harmful acidic oxidation byproducts.',
   vk='text', sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703,
   notes='from Features and Benefits; stated as an additional function alongside AO activity')

_r(E703, 'component_general', 'chemical_family',
   'hindered phenol with aliphatic amine (dual-functionality antioxidant); CAS 88-27-7',
   vk='text', sha='1919f6444880', pg=2, vc=VC_TDS, review=REVIEW_4703,
   notes='chemical class from TDS description: "hindered phenol structure and an aliphatic '
         'amine group"; CAS 88-27-7 printed on page 2; MW 263.4; solid crystalline powder')

_m(E703, 'component_general', 'active_content',
   'not found; pure solid compound (single substance, CAS 88-27-7, MW 263.4); '
   'no active content % stated in TDS',
   review=REVIEW_4703)
_m(E703, 'component_general', 'carrier.identity',
   'not found; product is a solid crystalline powder; no carrier stated',
   review=REVIEW_4703)
_m(E703, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_4703)
_m(E703, 'component_general', 'treat_rate',
   'not found in the inspected text; no recommended dosage or treat rate stated',
   review=REVIEW_4703)

_r(E703, 'component_general', 'compatibility_restrictions',
   'Applications include steam turbine oils, R&O oils, hydraulic fluids, transformer '
   'oils, industrial gear oils and grease.',
   vk='text', sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703,
   notes='application list from TDS description; no base oil compatibility restrictions stated; '
         'solubility in petroleum oils: 2.0 wt% @20°C (limited — noted in solubility table)')

_r(E703, 'component_general', 'function_specific_markers.tbn',
   'Total Base Number, mg KOH/g: 214',
   unit='mgKOH/g', value='214', vk='typical',
   sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703,
   notes='from Typical Physical Properties table; high TBN reflects aliphatic amine '
         'functionality; product described as "ashless TBN source"')
_m(E703, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_4703)
_m(E703, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_4703)
_m(E703, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_4703)
_m(E703, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_4703)
_m(E703, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_4703)

# not_in_template for ETHANOX_4703
_nit(E703, 'flash_point',
     'Flash Point (COC), °F (°C), min: >200 (>93)',
     unit='°C', value='93', qual='>', vk='bound',
     meth='COC (ASTM D92)',
     sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703,
     notes='stated as minimum value "min"; solid compound')
_nit(E703, 'melting_point',
     'Melting Point, °F (°C): 201 (94)',
     unit='°C', value='94', vk='typical',
     sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703)
_nit(E703, 'molecular_weight',
     'Molecular Weight: 263.4',
     value='263.4', vk='typical',
     sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703)
_nit(E703, 'solubility_in_petroleum_oils',
     'Solubility (Wt% at 20°C) Petroleum Oils: 2.0',
     unit='wt%', value='2.0', vk='typical',
     cond='20°C, in petroleum oils',
     sha='1919f6444880', pg=1, vc=VC_TDS, review=REVIEW_4703,
     notes='limited oil solubility (2 wt%); may limit treat rate ceiling in mineral oil formulations')


# ===========================================================================
# CHEMTURA:NAUGALUBE_16
# ===========================================================================

_r(NL16, 'component_general', 'function.primary',
   'Naugalube 16 is a versatile sulfur-containing phenol that can be used as a primary '
   'or secondary antioxidant for lubricants, especially for those formulated with natural '
   'and synthetic esters.',
   vk='text', sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16)

_r(NL16, 'component_general', 'function.secondary',
   'can be used as a primary or secondary antioxidant ... in combination with suitable '
   'Naugalube aminic antioxidants',
   vk='text', sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16,
   notes='TDS explicitly states it can serve as either primary OR secondary AO; '
         'also noted for synergy with aminic (secondary amine) antioxidants')

_r(NL16, 'component_general', 'chemical_family',
   '4,4\'-Thiobis(2-tert-butyl-5-methylphenol); CAS No. [96-69-5]',
   vk='text', sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16,
   notes='IUPAC-style name and CAS printed on page 1 of TDS alongside structural formula')

_m(NL16, 'component_general', 'active_content',
   'not found; pure substance (single compound, CAS 96-69-5); no active content % stated',
   review=REVIEW_NL16)
_m(NL16, 'component_general', 'carrier.identity',
   'not found; product is a crystalline solid; no carrier stated',
   review=REVIEW_NL16)
_m(NL16, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_NL16)

_r(NL16, 'component_general', 'treat_rate',
   'Typical Treatment Rate: 0.1 – 1.0 wt%.',
   unit='wt%', lo='0.1', hi='1.0', vk='range',
   sha='b6b41d837bf7', pg=2, vc=VC_TDS, review=REVIEW_NL16)

_r(NL16, 'component_general', 'compatibility_restrictions',
   'Naugalube 16 can be used in a broad range of lubricants, in both automotive and '
   'industrial applications and is particularly effective in hydraulic fluids and '
   'circulating oils.',
   vk='text', sha='b6b41d837bf7', pg=2, vc=VC_TDS, review=REVIEW_NL16,
   notes='no base oil restrictions stated; limited solubility in mineral oil '
         '(<0.4 wt%) noted in Typical Property Data; more soluble in esters (>5 wt%)')

_m(NL16, 'component_general', 'function_specific_markers.tbn',
   'not found; sulfur-phenolic AO — no TBN stated',
   review=REVIEW_NL16)
_m(NL16, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_NL16)
_m(NL16, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_NL16)
_m(NL16, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_NL16)
_m(NL16, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_NL16)
_m(NL16, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_NL16)

# not_in_template for NAUGALUBE_16
_nit(NL16, 'specific_gravity',
     'Specific Gravity 20/20°C: 1.10',
     value='1.10', vk='typical',
     meth='ASTM D1298 / ISO 3675',
     cond='20/20°C',
     sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16,
     notes='from Typical Property Data table; measured as solid; SG 20/20°C standard')
_nit(NL16, 'melting_range',
     'Melting Range: 160-164°C',
     unit='°C', lo='160', hi='164', vk='range',
     sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16)
_nit(NL16, 'flash_point',
     'Flash Point: 215°C (Closed cup)',
     unit='°C', value='215', vk='typical',
     meth='ASTM D93 / ISO 2719', cond='closed cup',
     sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16)
_nit(NL16, 'ash_content',
     'Ash Content: < 0.05 wt.%',
     unit='wt%', hi='0.05', qual='<', vk='bound',
     meth='ASTM D482',
     sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16)
_nit(NL16, 'sulfur_content',
     'Sulfur: 8.9 wt.%',
     unit='wt%', value='8.9', vk='typical',
     sha='b6b41d837bf7', pg=1, vc=VC_TDS, review=REVIEW_NL16,
     notes='high sulfur content is intrinsic to the thio-bisphenol structure (C-S-C linkage); '
           'not a carrier-oil sulfur contribution')


# ===========================================================================
write_rows('s37_chemtura.csv', ROWS)
if __name__ == '__main__':
    print(f's37_chemtura: {len(ROWS)} rows written to field_evidence/s37_chemtura.csv')
