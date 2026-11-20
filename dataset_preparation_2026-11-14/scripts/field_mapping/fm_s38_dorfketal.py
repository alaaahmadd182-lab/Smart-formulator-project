"""Field-level mapping, S38 Dorf Ketal — 2 products, 2 documents.

Supplier: Dorf Ketal Chemicals (I) Pvt. Ltd. / Dorf Ketal Chemicals, LLC.
Both products are lubricant additive components (additive_component, component_general).
Decisions file: s38_dorfketal.json (7 products total; only 2 have all docs cached).

Products:
  DORFKETAL:PX_3841 — oligomeric non-silicone defoamant; Gear Oil use
  DORFKETAL:PX_3871 — mixed alkyl borate ester; dispersancy/friction-wear/EP; Gear Oil + Grease

Documents:
  c627e08f6c64  DL2-12257.pdf  2009-10-14  PX-3841 TDS (single page)
  0c6cfd4d5f77  DL2-14626.pdf  2014-12-05  PX-3871 TDS (single page)

Document notes:
  PX-3841 TDS: "LUBRICANT ADDITIVE" header; Typical Properties table with Specific Gravity
    @15.6/15.6°C=0.92, Density lb/gal=7.7, Viscosity cSt @40°C=60, Flash Point °C (PMCC)=38.
    CAS: 9003-49-0 (polyisobutylene) / 95-63-6 (1,2,4-trimethylbenzene solvent).
    Treat rate: Gear Oil 0.05-0.30 wt%. Shelf life: 96 months.
  PX-3871 TDS: "LUBRICANT ADDITIVE" header; Typical Properties table with Specific Gravity
    @15.6/15.6°C=0.94, Density lb/gal=7.8, Viscosity cSt @40°C=16.0, @100°C=3.5,
    Flash Point °C=130, Boron Content wt%=5.5, Pour Point °C=-64. CAS not listed.
    Functions stated: Dispersancy, Friction and wear reduction, Dropping point increase in
    lithium-based greases. Treat: Automotive Gear 0.3-1.5%, Grease 0.5-1.5%.
    Shelf life: 24 months.

Writes field_evidence/s38_dorfketal.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    'c627e08f6c64': ('DL2-12257.pdf', '2009-10-14'),  # PX-3841 TDS
    '0c6cfd4d5f77': ('DL2-14626.pdf', '2014-12-05'),  # PX-3871 TDS
}

REVIEW = 'sheets read in full (text layer) 2026-11-16; single-page TDS, all rows read'
VC_TDS = 'product data sheet (TDS), typical properties table'

PX3841 = 'DORFKETAL:PX_3841'
PX3871 = 'DORFKETAL:PX_3871'

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
# DORFKETAL:PX_3841 — oligomeric non-silicone defoamant
# ===========================================================================

_r(PX3841, 'component_general', 'function.primary',
   'PX 3841 is an oligomeric, non-silicone defoamant.',
   vk='text', sha='c627e08f6c64',
   notes='from product description in TDS; CAS 9003-49-0 (polyisobutylene/polybutene) '
         'and 95-63-6 (1,2,4-trimethylbenzene, aromatic solvent) — defoamant in solvent carrier')

_m(PX3841, 'component_general', 'function.secondary',
   'not found; no secondary function stated in TDS')

_r(PX3841, 'component_general', 'chemical_family',
   'oligomeric non-silicone (polyisobutylene/polybutene-based) defoamant',
   vk='text', sha='c627e08f6c64',
   notes='chemical family inferred from TDS description ("oligomeric, non-silicone") '
         'and CAS 9003-49-0 (polyisobutylene/polybutene polymer); basis: general_knowledge '
         'for the connection between CAS and chemical class',
   entry='CAS 9003-49-0 / 95-63-6')

_m(PX3841, 'component_general', 'active_content',
   'not found; active polymer content % not stated in TDS; '
   'CAS listing (9003-49-0 / 95-63-6) suggests defoamant polymer in aromatic solvent '
   'but no concentration given')

_m(PX3841, 'component_general', 'carrier.identity',
   'not found; CAS 95-63-6 (1,2,4-trimethylbenzene) may be the carrier/solvent but '
   'is listed alongside polymer CAS without percentage; no explicit carrier statement')

_m(PX3841, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier percentage stated')

_r(PX3841, 'component_general', 'treat_rate',
   'Gear Oil: 0.05 – 0.30 wt%',
   unit='wt%', lo='0.05', hi='0.30', vk='range',
   sha='c627e08f6c64',
   notes='from Recommended Treat Levels table; only Gear Oil application given in TDS')

_m(PX3841, 'component_general', 'compatibility_restrictions',
   'not found; TDS states "All PX lubricant additives are components designed to be used '
   'with other components for a fully formulated lubricant" — no explicit restriction stated')

_m(PX3841, 'component_general', 'function_specific_markers.tbn',
   'not found; defoamant — TBN not applicable and not stated')
_m(PX3841, 'component_general', 'function_specific_markers.ca', 'not found')
_m(PX3841, 'component_general', 'function_specific_markers.mg', 'not found')
_m(PX3841, 'component_general', 'function_specific_markers.p',  'not found')
_m(PX3841, 'component_general', 'function_specific_markers.zn', 'not found')
_m(PX3841, 'component_general', 'function_specific_markers.mo', 'not found')

# not_in_template for PX_3841
_nit(PX3841, 'specific_gravity',
     'Specific Gravity @ 15.6/15.6°C: 0.92',
     unit='', value='0.92', vk='typical',
     meth='ASTM D-4052', cond='15.6/15.6°C',
     sha='c627e08f6c64',
     notes='unitless specific gravity; equivalent to density 0.92 g/cm³ at 15.6°C')

_nit(PX3841, 'density_lb_gal',
     'Density, lb/gal: 7.7',
     unit='lb/gal', value='7.7', vk='typical',
     meth='ASTM D-4052',
     sha='c627e08f6c64',
     notes='non-SI unit; 7.7 lb/gal ≈ 0.923 g/cm³ — consistent with specific gravity 0.92')

_nit(PX3841, 'kv40',
     'Viscosity, cSt @ 40°C: 60',
     unit='mm2/s', value='60', vk='typical',
     meth='ASTM D-445', cond='40°C',
     sha='c627e08f6c64')

_nit(PX3841, 'flash_point',
     'Flash Point, °C (PMCC): 38',
     unit='°C', value='38', vk='typical',
     meth='ASTM D-93',
     sha='c627e08f6c64',
     notes='PMCC (Pensky-Martens Closed Cup) method; low flash point consistent with '
           'aromatic solvent carrier (1,2,4-trimethylbenzene bp 169°C, fp ~44°C)')


# ===========================================================================
# DORFKETAL:PX_3871 — mixed alkyl borate ester (dispersant/AW/EP + grease EP)
# ===========================================================================

_r(PX3871, 'component_general', 'function.primary',
   'PX-3871 is a mixed alkyl borate ester additive. It is used in lubricating oils '
   'and greases to provide: Dispersancy; Friction and wear reduction; '
   'Dropping point increase in lithium based greases.',
   vk='text', sha='0c6cfd4d5f77',
   notes='multiple functions stated in TDS description; primary is dispersancy + AW/EP')

_m(PX3871, 'component_general', 'function.secondary',
   'not found; multiple functions already listed under function.primary from TDS description')

_r(PX3871, 'component_general', 'chemical_family',
   'mixed alkyl borate ester',
   vk='text', sha='0c6cfd4d5f77',
   notes='chemical family stated in TDS product description; CAS number field is blank in TDS')

_m(PX3871, 'component_general', 'active_content',
   'not found; active content % not stated in TDS')

_m(PX3871, 'component_general', 'carrier.identity',
   'not found; product described as "Clear & Bright Liquid"; no carrier stated')

_m(PX3871, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated')

_r(PX3871, 'component_general', 'treat_rate',
   'Automotive Gear: 0.3 - 1.5 wt%; Grease: 0.5 - 1.5 wt%',
   unit='wt%', lo='0.3', hi='1.5', vk='range',
   sha='0c6cfd4d5f77',
   notes='two application ranges in Recommended Treat Levels table; '
         'lo=0.3 from Automotive Gear min; hi=1.5 is shared max for both applications; '
         'Grease range 0.5-1.5 also noted')

_m(PX3871, 'component_general', 'compatibility_restrictions',
   'not found; TDS states only "All PX lubricant additives are components designed to be '
   'used with other components for a fully formulated lubricant" — no explicit restrictions')

_m(PX3871, 'component_general', 'function_specific_markers.tbn',
   'not found; borate ester — no TBN stated')
_m(PX3871, 'component_general', 'function_specific_markers.ca', 'not found')
_m(PX3871, 'component_general', 'function_specific_markers.mg', 'not found')
_m(PX3871, 'component_general', 'function_specific_markers.p',
   'not found; borate ester (not phosphorus-based); no phosphorus content stated')
_m(PX3871, 'component_general', 'function_specific_markers.zn', 'not found')
_m(PX3871, 'component_general', 'function_specific_markers.mo', 'not found')

# not_in_template for PX_3871
_nit(PX3871, 'specific_gravity',
     'Specific Gravity @ 15.6/15.6°C: 0.94',
     unit='', value='0.94', vk='typical',
     meth='ASTM D-4052', cond='15.6/15.6°C',
     sha='0c6cfd4d5f77',
     notes='unitless; equivalent to density 0.94 g/cm³ at 15.6°C')

_nit(PX3871, 'density_lb_gal',
     'Density, lb/gal: 7.8',
     unit='lb/gal', value='7.8', vk='typical',
     meth='ASTM D-4052',
     sha='0c6cfd4d5f77')

_nit(PX3871, 'kv40',
     'Viscosity, cSt @ 40°C: 16.0',
     unit='mm2/s', value='16.0', vk='typical',
     meth='ASTMD-445', cond='40°C',
     sha='0c6cfd4d5f77')

_nit(PX3871, 'kv100',
     'Viscosity, cSt @ 100°C: 3.5',
     unit='mm2/s', value='3.5', vk='typical',
     meth='ASTMD-445', cond='100°C',
     sha='0c6cfd4d5f77')

_nit(PX3871, 'flash_point',
     'Flash Point, °C: 130',
     unit='°C', value='130', vk='typical',
     meth='ASTM D-93',
     sha='0c6cfd4d5f77')

_nit(PX3871, 'boron_content',
     'Boron Content, wt %: 5.5',
     unit='wt%', value='5.5', vk='typical',
     meth='ASTM D-4051',
     sha='0c6cfd4d5f77',
     notes='boron is the functional element for this borate ester additive')

_nit(PX3871, 'pour_point',
     'Pour Point, °C: -64',
     unit='°C', value='-64', vk='typical',
     meth='ASTM D-97',
     sha='0c6cfd4d5f77')


# ===========================================================================
write_rows('s38_dorfketal.csv', ROWS)
if __name__ == '__main__':
    print(f's38_dorfketal: {len(ROWS)} rows written to field_evidence/s38_dorfketal.csv')
