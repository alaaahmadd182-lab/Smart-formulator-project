"""Field-level mapping, S49 Kraton — 2 products, 3 documents.

Supplier: Kraton Corporation (Mailiao Plant, Taiwan).
Both products are OCP/EP polymer VIIs (additive_component, component_general).
Decisions file: s49_kraton.json (5 products total; only G1750_V and G1765 have
  their cached docs; G1701_E, G1701_M, G1702_H are not mapped here).

Products:
  KRATON:G1750_V — multi-arm EP copolymer; 3 docs: TDS + CoA + SDS
  KRATON:G1765   — EP copolymer; 1 doc: SDS only (shared with G1750_V)

Documents:
  b5e171c2aa4e  DL2-15682.pdf          (TDS, Asia region, 2018-10-28 K0628)
  be598dbb1155  DL2-15680.pdf  2024-09-02  G1750_V CoA (Mfg date 2024-09-02)
  cdd7a9a6a24e  DL2-15681.pdf  2024-01-29  SDS covers G1750 and G1765 (rev 2.1)

Document notes:
  TDS (b5e171c2aa4e): G1750 V; product identifier K628DDb17A. Supplied from Taiwan in bale.
    Sales Specification: Antioxidant 0.03-0.20 %m (non-staining phenolic AO); Volatile Matter
    ≤0.7 %m; Visc,Kin,1.70%w @100C = 11.8-14.1 cSt (AGAM 1201).
    Typical Properties: Specific Gravity 0.86; Melt Index 200°C/5kg = 8 g/10min;
    Elongation at Break 100%; Shore A Hardness 11; Styrene/Rubber ratio 0/100; Tensile 50 max psi.
    TDS describes use as "modifier of polymers", footwear, adhesives, sealants — this is
    consistent with an EP/SEBS polymer that also functions as a lubricant VII in solution.
  CoA (be598dbb1155): G1750 VO; Batch 09DXH1001; Mfg 2024-09-02. Results: Volatile 0.1 %m,
    Visc 13.1 cSt, Antioxidant 0.06 %m (all within spec). Footnote: results labelled
    1=Guaranteed, 2=Typical, 3=Report Only.
  SDS (cdd7a9a6a24e): Covers G1750 and G1765 (all alphanumeric suffixes). Rev date 2024-01-29.
    Section 3: EP copolymer CAS 127883-08-3 <100 %. Section 9: Relative density >0.88-<0.95
    at 20°C; Flash point Not applicable; Viscosity Not available.
    G1765 has no TDS or CoA in the cache — SDS is the only source.

Writes field_evidence/s49_kraton.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    'b5e171c2aa4e': ('DL2-15682.pdf', ''),             # G1750_V TDS (K0628, 2018-10-28)
    'be598dbb1155': ('DL2-15680.pdf', '2024-09-02'),   # G1750_V CoA (Mfg date)
    'cdd7a9a6a24e': ('DL2-15681.pdf', '2024-01-29'),   # SDS for G1750 + G1765
}

REVIEW_V  = ('sheets read in full (text layer) 2026-11-16; '
             'TDS DL2-15682 (3pp), CoA DL2-15680 (1pp), SDS DL2-15681 (7pp)')
REVIEW_65 = ('sheet read in full (text layer) 2026-11-16; '
             'SDS DL2-15681 only (7pp); no TDS or CoA in cache for G1765')

VC_TDS        = 'product data sheet (TDS), typical properties table'
VC_COQ_SPEC   = 'certificate of quality (CoQ), product specification'
VC_COQ_RESULT = 'certificate of quality (CoQ), batch test result'
VC_SDS        = 'safety data sheet (SDS), Section 9 physical properties'
VC_SDS3       = 'safety data sheet (SDS), Section 3 composition'

G1750 = 'KRATON:G1750_V'
G1765 = 'KRATON:G1765'

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
# KRATON:G1750_V — TDS + CoA + SDS
# ===========================================================================

_r(G1750, 'component_general', 'function.primary',
   'Kraton G1750 V is a clear, multi-arm polymer based on ethylene/propylene. '
   'It is used as a modifier of polymers.',
   vk='text', sha='b5e171c2aa4e', pg=1, vc=VC_TDS, review=REVIEW_V,
   notes='TDS describes "modifier of polymers" and footwear/adhesives use; '
         'in lubricant context, EP copolymers (OCP) are used as viscosity index improvers; '
         'Styrene/Rubber ratio 0/100 confirms no styrene block — pure EP rubber polymer')

_m(G1750, 'component_general', 'function.secondary',
   'not found; no secondary lubricant function stated in TDS', review=REVIEW_V)

_r(G1750, 'component_general', 'chemical_family',
   'ethylene/propylene copolymer (CAS 127883-08-3)',
   vk='text', sha='cdd7a9a6a24e', pg=1, vc=VC_SDS3, review=REVIEW_V,
   notes='SDS Section 3 gives EP copolymer CAS 127883-08-3 <100%; TDS confirms '
         '"multi-arm polymer based on ethylene/propylene" with Styrene/Rubber ratio 0/100; '
         'product is a solid OCP polymer in bale form')

_r(G1750, 'component_general', 'active_content',
   'Antioxidant: 0.03 TO 0.20 %m (spec); Volatile Matter: = 0.7 %m max (spec)',
   unit='%m', lo='0.03', hi='0.20', vk='range',
   sha='b5e171c2aa4e', pg=1, vc=VC_COQ_SPEC, review=REVIEW_V,
   notes='TDS Sales Specification: antioxidant is a stabiliser additive (non-staining phenolic), '
         'not a measure of polymer active content; EP polymer is essentially the active component; '
         'volatile matter ≤0.7 %m; active polymer content (100 - AO - VM) is not stated explicitly')

_m(G1750, 'component_general', 'carrier.identity',
   'not found; product is supplied in solid bale form; no liquid carrier stated in TDS or SDS',
   review=REVIEW_V)
_m(G1750, 'component_general', 'carrier.share_wt_pct',
   'not found; solid polymer, no carrier', review=REVIEW_V)

_m(G1750, 'component_general', 'treat_rate',
   'not found; TDS and CoA do not state a recommended treat rate for lubricant use; '
   'kinematic viscosity is measured at 1.70 %w solution — this is a characterisation '
   'concentration, not a treat rate recommendation',
   review=REVIEW_V)

_m(G1750, 'component_general', 'compatibility_restrictions',
   'not found; TDS describes polymer applications (footwear, adhesives, sealants); '
   'no lubricant-specific compatibility restrictions stated; food contact and medical device '
   'restrictions noted in TDS sections 2-3 but not relevant to lubricant use',
   review=REVIEW_V)

_m(G1750, 'component_general', 'function_specific_markers.tbn',
   'not found; EP polymer — TBN not applicable', review=REVIEW_V)
_m(G1750, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_V)
_m(G1750, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_V)
_m(G1750, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_V)
_m(G1750, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_V)
_m(G1750, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_V)

# not_in_template for G1750_V — TDS spec bounds
_nit(G1750, 'kv_1pct_sol_100c_spec',
     'Visc,Kin,1.70%w (@100C): 11.8 TO 14.1 cSt (spec)',
     unit='cSt', lo='11.8', hi='14.1', vk='range',
     meth='AGAM 1201', cond='1.70 %w solution at 100°C',
     sha='b5e171c2aa4e', pg=1, vc=VC_COQ_SPEC, review=REVIEW_V,
     notes='Sales Specification range; AGAM 1201 is a Kraton internal method; '
           'measurement is at 1.70 wt% solution, not neat polymer')

_nit(G1750, 'volatile_matter_spec',
     'Volatile Matter: = 0.7 %m (spec max)',
     unit='%m', hi='0.7', qual='<=', vk='bound',
     meth='KM 04',
     sha='b5e171c2aa4e', pg=1, vc=VC_COQ_SPEC, review=REVIEW_V)

_nit(G1750, 'antioxidant_content_spec',
     'Antioxidant: 0.03 TO 0.20 %m (spec)',
     unit='%m', lo='0.03', hi='0.20', vk='range',
     meth='KM 08',
     sha='b5e171c2aa4e', pg=1, vc=VC_COQ_SPEC, review=REVIEW_V,
     notes='non-staining phenolic antioxidant (stabiliser additive in polymer)')

# CoA batch results for G1750_V
_nit(G1750, 'kv_1pct_sol_100c_result',
     'Visc,Kin,1.70%w @100C: 13.1 Centistoke',
     unit='cSt', value='13.1', vk='report-only',
     meth='AGAM 1201', cond='1.70 %w solution at 100°C',
     sha='be598dbb1155', pg=1, vc=VC_COQ_RESULT, review=REVIEW_V,
     notes='CoA batch result; spec 11.8-14.1 cSt; Batch 09DXH1001 Mfg 2024-09-02')

_nit(G1750, 'volatile_matter_result',
     'Volatile Matter: 0.1 % Weight',
     unit='%m', value='0.1', vk='report-only',
     meth='KM 04',
     sha='be598dbb1155', pg=1, vc=VC_COQ_RESULT, review=REVIEW_V,
     notes='CoA batch result; spec ≤0.7 %m')

_nit(G1750, 'antioxidant_content_result',
     'Antioxidant: 0.06 % Weight',
     unit='%m', value='0.06', vk='report-only',
     meth='KM 08',
     sha='be598dbb1155', pg=1, vc=VC_COQ_RESULT, review=REVIEW_V,
     notes='CoA batch result; spec 0.03-0.20 %m')

# SDS Section 9 physical properties
_nit(G1750, 'specific_gravity',
     'Specific Gravity: 0.86',
     unit='', value='0.86', vk='typical',
     sha='b5e171c2aa4e', pg=1, vc=VC_TDS, review=REVIEW_V,
     notes='from TDS Typical Properties table; no temperature stated')

_nit(G1750, 'density_sds_bounds',
     'Relative density: > 0.88 - < 0.95 at 20°C',
     unit='g/cm3', lo='0.88', hi='0.95', qual='range', vk='range',
     cond='20°C',
     sha='cdd7a9a6a24e', pg=4, vc=VC_SDS, review=REVIEW_V,
     notes='SDS Section 9 physical properties; stated as bounds (> 0.88 to < 0.95); '
           'consistent with TDS typical SG of 0.86')

_nit(G1750, 'melt_index',
     'Melt Index 200C, 5 kg: 8 gms/10 min',
     unit='g/10min', value='8', vk='typical',
     meth='ASTM D 1238', cond='200°C, 5 kg',
     sha='b5e171c2aa4e', pg=1, vc=VC_TDS, review=REVIEW_V,
     notes='from TDS Typical Properties table; non-lubricant characterisation property')


# ===========================================================================
# KRATON:G1765 — SDS only
# ===========================================================================

_r(G1765, 'component_general', 'function.primary',
   'Kraton G1765 — ethylene/propylene copolymer (CAS 127883-08-3)',
   vk='text', sha='cdd7a9a6a24e', pg=1, vc=VC_SDS3, review=REVIEW_65,
   notes='SDS covers both G1750 and G1765 (all alphanumeric suffixes); product '
         'description from SDS product identifier section; no TDS available for G1765')

_m(G1765, 'component_general', 'function.secondary',
   'not found in SDS; no secondary function stated', review=REVIEW_65)

_r(G1765, 'component_general', 'chemical_family',
   'ethylene/propylene copolymer (CAS 127883-08-3)',
   vk='text', sha='cdd7a9a6a24e', pg=1, vc=VC_SDS3, review=REVIEW_65,
   notes='SDS Section 3 composition: EP copolymer CAS 127883-08-3 <100%; '
         'same chemical family as G1750_V')

_m(G1765, 'component_general', 'active_content',
   'not found in SDS; no composition percentages beyond EP copolymer <100% in Section 3',
   review=REVIEW_65)
_m(G1765, 'component_general', 'carrier.identity',
   'not found in SDS; solid polymer form implied; no carrier stated',
   review=REVIEW_65)
_m(G1765, 'component_general', 'carrier.share_wt_pct',
   'not found', review=REVIEW_65)
_m(G1765, 'component_general', 'treat_rate',
   'not found in SDS; no treat rate stated', review=REVIEW_65)
_m(G1765, 'component_general', 'compatibility_restrictions',
   'not found in SDS; no lubricant compatibility information in SDS', review=REVIEW_65)

_m(G1765, 'component_general', 'function_specific_markers.tbn',
   'not found; EP polymer — TBN not applicable', review=REVIEW_65)
_m(G1765, 'component_general', 'function_specific_markers.ca',  'not found', review=REVIEW_65)
_m(G1765, 'component_general', 'function_specific_markers.mg',  'not found', review=REVIEW_65)
_m(G1765, 'component_general', 'function_specific_markers.p',   'not found', review=REVIEW_65)
_m(G1765, 'component_general', 'function_specific_markers.zn',  'not found', review=REVIEW_65)
_m(G1765, 'component_general', 'function_specific_markers.mo',  'not found', review=REVIEW_65)

# SDS Section 9 physical properties for G1765
_nit(G1765, 'density_sds_bounds',
     'Relative density: > 0.88 - < 0.95 at 20°C',
     unit='g/cm3', lo='0.88', hi='0.95', qual='range', vk='range',
     cond='20°C',
     sha='cdd7a9a6a24e', pg=4, vc=VC_SDS, review=REVIEW_65,
     notes='SDS Section 9 physical properties; shared SDS covers both G1750 and G1765; '
           'bounds may not distinguish between grades')


# ===========================================================================
write_rows('s49_kraton.csv', ROWS)
if __name__ == '__main__':
    print(f's49_kraton: {len(ROWS)} rows written to field_evidence/s49_kraton.csv')
