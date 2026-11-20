"""Field-level mapping, S34 King Industries — 3 products, 8 documents.

Products:
  KINGINDUSTRIES:NA_LUBE_BL_1208 — Ashless multifunctional R&O additive package
    additive_package (tier 1 + tier 2); 5 docs: DL2-11419 (TDS), DL2-11696 (PDS),
    DL2-11697 (performance evaluation), DL2-12838 (application bulletin),
    DL2-14391 (CoA lot 08641, MFG 2020-08-11, Last Spec Rev 2015-11-04)
  KINGINDUSTRIES:NA_SUL_BSN — Neutral barium dinonylnaphthalenesulfonate rust inhibitor
    additive_component (component_general); 2 docs: DL2-12347 (PDS),
    DL2-14395 (CoA lot 9A625, MFG 2019-10-03, Last Spec Rev 2019-05-08)
  KINGINDUSTRIES:NA_LUBE_AO_142_I — Butylated/octylated diphenylamine antioxidant
    additive_component (component_general); 1 doc: DL2-14947 (PDS)

Document notes:
  DL2-11419 (TDS) and DL2-11696 (PDS) carry identical typical properties; both note
    "The above analytical data are not specifications." DL2-11419 is the more detailed
    bulletin (10 pages of performance data); DL2-11696 is a 2-sided PDS.
  DL2-11697: performance evaluation at 0.45% in ISO VG 46 Group II (ExxonMobil EHC 60);
    confirms Siemens TVL 9013 04 and Alstom HTGD 90117 (exception: foam seq. III).
  DL2-12838: application bulletin; same spec list as DL2-11419; Group I/II/III/IV
    performance table at 0.7%.
  DL2-14391 (CoA): US date format M/D/Y: MFG 08/11/2020 -> 2020-08-11.
  DL2-14947 (AO-142-I PDS): PDF text extraction produced doubled content — every line
    appears twice; values are internally consistent; noted in review.
  DL2-14395 (BSN CoA): US date format: MFG 10/03/2019 -> 2019-10-03.
  Density temperatures: BL-1208 @25°C (non-standard); BSN @15.6°C; AO-142-I @15.6°C.

Writes field_evidence/s34_king.csv."""

import csv, os
from fm_common import PKG, write_rows

ROOT = os.path.dirname(PKG)
INV  = os.path.join(ROOT, 'incoming_dataset_review_2026-11-12')
_ud  = {r['sha256'][:12]: r for r in csv.DictReader(
         open(os.path.join(INV, 'tables', 'unique_documents.csv'), encoding='utf-8'))}

FILE = {
    '5ff875cfbd75': ('DL2-11419.pdf', ''),
    '1550ea1a8f64': ('DL2-11696.pdf', ''),
    'fc88711a8eb5': ('DL2-11697.pdf', ''),
    'eeea8dbc0c27': ('DL2-12838.pdf', ''),
    '9c0ebc98e4f4': ('DL2-14391.pdf', '2020-08-11'),
    '5ef35a134626': ('DL2-12347.pdf', ''),
    'a796dc222984': ('DL2-14395.pdf', '2019-10-03'),
    '39a7f5fadd1d': ('DL2-14947.pdf', ''),
}

REVIEW_BL  = ('sheets read in full (text layer) 2026-11-16; 5 docs: '
              'TDS DL2-11419, PDS DL2-11696, perf eval DL2-11697, '
              'app bulletin DL2-12838, CoA DL2-14391')
REVIEW_BSN = ('sheets read in full (text layer) 2026-11-16; '
              '2 docs: PDS DL2-12347, CoA DL2-14395')
REVIEW_AO  = ('sheet read in full (text layer) 2026-11-16; 1 doc: PDS DL2-14947 '
              '(PDF text extraction produced doubled content; values confirmed consistent)')

VC_TDS      = 'product data sheet (TDS/PDS), typical properties table'
VC_APPL     = 'application bulletin / performance evaluation'
VC_COA_ACT  = 'certificate of analysis (CoA), batch result'
VC_COA_SPEC = 'certificate of analysis (CoA), product specification'

BL  = 'KINGINDUSTRIES:NA_LUBE_BL_1208'
BSN = 'KINGINDUSTRIES:NA_SUL_BSN'
AO  = 'KINGINDUSTRIES:NA_LUBE_AO_142_I'

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
         meth='', cond='', sha='', pg=1, notes='', entry='', vc=VC_TDS, review=''):
    fname, rev = FILE[sha]
    ROWS.append({
        'product_key': pk, 'template': 'not_in_template:' + prop, 'field': prop,
        'entry': entry,
        'value': value, 'qualifier': qual, 'min': lo, 'max': hi,
        'value_kind': vk, 'printed_text': printed, 'unit': unit,
        'test_temperature_c': '', 'method': meth, 'conditions': cond,
        'status': 'Reported', 'value_class': vc, 'basis': '',
        'source_file': fname, 'sha256': _ud[sha]['sha256'],
        'page': str(pg), 'revision_date': rev, 'notes': notes, 'review': review,
    })


# ===========================================================================
# NA_LUBE_BL_1208 — additive_package, Tier 1
# ===========================================================================

_r(BL, 'package_tier1', 'package_type_application.package_type',
   'Multifunctional Ashless R&O Package for Industrial Oils',
   vk='text', sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='document title / product heading; identical heading on DL2-11696 and DL2-12838')

_r(BL, 'package_tier1', 'package_type_application.intended_service',
   'R&O oils, hydraulic fluids HL, and gear oils CL; turbine oils; compressor oils; '
   'environmentally friendly fluids (HETG based on rapeseed oils, HEES based on '
   'synthetic esters); industrial gear oils',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   notes='derived from applications list on DL2-11419 p.2; same list on DL2-12838 p.1')

# performance_claims — R&O, hydraulic, gear
_r(BL, 'package_tier1', 'performance_claims',
   'Cincinnati Lamb P-38 (HL-32), P-55 (HL-46), P-54 (HL-68), P-57 (HL-150), P-62 (FC-10)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='Cincinnati Lamb P-38/P-55/P-54/P-57/P-62 (HL/FC)',
   notes='R&O oils, hydraulic fluids HL, gear oils CL; listed under Applications on p.2')
_r(BL, 'package_tier1', 'performance_claims',
   'DIN 51524 part 1 (HL)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='DIN 51524 part 1 (HL)')
_r(BL, 'package_tier1', 'performance_claims',
   'DIN 51517 part 2 (CL)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='DIN 51517 part 2 (CL)')
_r(BL, 'package_tier1', 'performance_claims',
   'AFNOR NF E 48-603 (HL)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='AFNOR NF E 48-603 (HL)')
_r(BL, 'package_tier1', 'performance_claims',
   'Siemens TLV 9013 04/01',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='Siemens TLV 9013 04/01',
   notes='turbine oil spec; also confirmed by test at 0.45% in DL2-11697')
_r(BL, 'package_tier1', 'performance_claims',
   'British Standard BS 489',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='British Standard BS 489')
_r(BL, 'package_tier1', 'performance_claims',
   'General Electric GEK 32568 A/C',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='General Electric GEK 32568 A/C')
_r(BL, 'package_tier1', 'performance_claims',
   'MIL-L-17672 D',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='MIL-L-17672 D')
_r(BL, 'package_tier1', 'performance_claims',
   'CEGB Standard 207001',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='CEGB Standard 207001')
_r(BL, 'package_tier1', 'performance_claims',
   'Brown Boveri HTGD 90117 / Alstom HTGD 90 117 V0001 S',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='Brown Boveri / Alstom HTGD 90117',
   notes='two name variants for same spec; confirmed by test at 0.45% in DL2-11697 '
         '(exception: foam seq. III — BL-1208 contains no foam inhibitor)')
_r(BL, 'package_tier1', 'performance_claims',
   'U.S. Steel 120',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='U.S. Steel 120')
_r(BL, 'package_tier1', 'performance_claims',
   'Westinghouse Electric Corp. Turbine Oil Spec.',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='Westinghouse Electric Corp. Turbine Oil Spec.')
_r(BL, 'package_tier1', 'performance_claims',
   'DIN 51515 part 1 (L-TD) & part 2 (L-TG)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='DIN 51515 part 1 (L-TD) & part 2 (L-TG)')
_r(BL, 'package_tier1', 'performance_claims',
   'ISO / DP 6521 (DAA, DAB, DAH, DAG)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='ISO/DP 6521 (DAA, DAB, DAH, DAG)',
   notes='compressor oils')
_r(BL, 'package_tier1', 'performance_claims',
   'DIN 51506 (VBL, VCL, VDL)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='DIN 51506 (VBL, VCL, VDL)',
   notes='compressor oils')
_r(BL, 'package_tier1', 'performance_claims',
   'VDMA 24568 HETG (based on rapeseed oils) & HEES (based on synthetic esters)',
   vk='text', sha='5ff875cfbd75', pg=2, vc=VC_APPL, review=REVIEW_BL,
   entry='VDMA 24568 HETG & HEES',
   notes='environmentally friendly fluids')

_m(BL, 'package_tier1', 'sae_grades_documented',
   'not found; industrial oil package — SAE viscosity grades not stated or applicable',
   review=REVIEW_BL)

_r(BL, 'package_tier1', 'permitted_base_oils_restrictions',
   'Performance demonstrated in typical Group I, II, III and IV base oils at 0.7%. '
   'Also tested in canola oil and soybean oil. '
   '"Solubility in a wide range of mineral oils, vegetable oils and synthetic basestocks."',
   vk='text', sha='eeea8dbc0c27', pg=1, vc=VC_APPL, review=REVIEW_BL,
   notes='from DL2-12838 performance table header and DL2-11419 product description; '
         'no restrictions stated, only broad compatibility')

_m(BL, 'package_tier1', 'route_selector_restrictions',
   'not found in the inspected text', review=REVIEW_BL)

# treat_rate_matrix — TDS recommended levels
_r(BL, 'package_tier1', 'treat_rate_matrix',
   'Industrial R&O Oils: 0.70% to 1.0%',
   unit='wt%', lo='0.70', hi='1.0', vk='range',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   entry='Industrial R&O Oils',
   notes='from "TYPICAL TREAT LEVELS" table on TDS; identical on DL2-11696')
_r(BL, 'package_tier1', 'treat_rate_matrix',
   'Circulating Oils: 0.70% to 1.0%',
   unit='wt%', lo='0.70', hi='1.0', vk='range',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   entry='Circulating Oils',
   notes='from "TYPICAL TREAT LEVELS" table on TDS; identical on DL2-11696')
# treat dose used in performance evaluation
_r(BL, 'package_tier1', 'treat_rate_matrix',
   '0.45% NA-LUBE BL-1208 incorporated into an ISO VG 46 Group II oil',
   unit='wt%', value='0.45', vk='typical',
   sha='fc88711a8eb5', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='ISO VG 46 Group II (perf eval dose)',
   notes='test dose in DL2-11697 performance evaluation; not a recommended treat level')
_r(BL, 'package_tier1', 'treat_rate_matrix',
   'Treat Level of NA-LUBE BL-1208, %: 0.70 (Group I, II, III, IV)',
   unit='wt%', value='0.70', vk='typical',
   sha='eeea8dbc0c27', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='Group I/II/III/IV (app bulletin dose)',
   notes='dose used in comparative performance table in DL2-12838')

_m(BL, 'package_tier1', 'required_co_components',
   'not found; no co-components stated as required in any of the 5 inspected documents',
   review=REVIEW_BL)

# published_formulations
_r(BL, 'package_tier1', 'published_formulations',
   'Performance in Group I, II, III & IV Oils at 0.70% (ISO VG 46)',
   vk='text', sha='eeea8dbc0c27', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='Group I-IV ISO VG 46 at 0.70%',
   notes='table of test results in DL2-12838; also referenced in DL2-11419 table of contents p.3')
_r(BL, 'package_tier1', 'published_formulations',
   'Performance evaluation: 0.45% in ISO VG 46 Group II (ExxonMobil EHC 60) '
   'vs Siemens TVL 9013 04 and Alstom HTGD 90117',
   vk='text', sha='fc88711a8eb5', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='ISO VG 46 Group II (EHC 60) at 0.45%')
_r(BL, 'package_tier1', 'published_formulations',
   'Performance in Canola Oil and Soybean Oil (pp.5-6)',
   vk='text', sha='5ff875cfbd75', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='Canola oil and Soybean oil',
   notes='referenced in table of contents on DL2-11419 p.1; full data on pp.5-6')
_r(BL, 'package_tier1', 'published_formulations',
   'Formulating Industrial Gear Oils (p.7)',
   vk='text', sha='5ff875cfbd75', pg=1, vc=VC_APPL, review=REVIEW_BL,
   entry='Industrial Gear Oil formulations',
   notes='referenced in table of contents on DL2-11419 p.1; full data on p.7')


# ===========================================================================
# NA_LUBE_BL_1208 — additive_package, Tier 2
# ===========================================================================

_m(BL, 'package_tier2', 'tbn',
   'not found; ashless package — TBN not stated in any of the 5 inspected documents',
   review=REVIEW_BL)
_m(BL, 'package_tier2', 'sulfated_ash',
   'not found; product is described as "ashless" but no measured sulfated ash value is '
   'stated in any of the 5 inspected documents',
   review=REVIEW_BL)
_m(BL, 'package_tier2', 'elements.Ca',
   'not found; ashless package — no metallic detergents; Ca not stated', review=REVIEW_BL)
_m(BL, 'package_tier2', 'elements.Mg',
   'not found; ashless package — Mg not stated', review=REVIEW_BL)
_m(BL, 'package_tier2', 'elements.Zn',
   'not found; ashless package — Zn not stated', review=REVIEW_BL)
# S — TDS typical + CoA actual + CoA spec
_r(BL, 'package_tier2', 'elements.S',
   'Sulfur Content: 7.0%',
   unit='wt%', value='7.0', vk='typical',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696')
_r(BL, 'package_tier2', 'elements.S',
   '% SULFUR: ACTUAL 6.96',
   unit='wt%', value='6.96', vk='report-only',
   meth='KI-220 (X-RAY FLUOR)',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result; MFG 2020-08-11')
_r(BL, 'package_tier2', 'elements.S',
   '% SULFUR: MIN 6.40  MAX 7.20',
   unit='wt%', lo='6.40', hi='7.20', vk='range',
   meth='KI-220 (X-RAY FLUOR)',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product specification bounds; Last Spec Rev 2015-11-04')
_m(BL, 'package_tier2', 'elements.B',
   'not found; not stated in any of the 5 inspected documents', review=REVIEW_BL)
_m(BL, 'package_tier2', 'elements.Mo',
   'not found; not stated in any of the 5 inspected documents', review=REVIEW_BL)
# P — TDS typical + CoA actual + CoA spec
_r(BL, 'package_tier2', 'elements.P',
   'Phosphorus Content: 0.2%',
   unit='wt%', value='0.2', vk='typical',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696')
_r(BL, 'package_tier2', 'elements.P',
   '% PHOSPHORUS: ACTUAL 0.21',
   unit='wt%', value='0.21', vk='report-only',
   meth='KI-220 (X-RAY FLUOR)',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result')
_r(BL, 'package_tier2', 'elements.P',
   '% PHOSPHORUS: MIN 0.17  MAX 0.22',
   unit='wt%', lo='0.17', hi='0.22', vk='range',
   meth='KI-220 (X-RAY FLUOR)',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product specification bounds')
# N — TDS typical only (not on CoA)
_r(BL, 'package_tier2', 'elements.N',
   'Nitrogen Content: 3.5%',
   unit='wt%', value='3.5', vk='typical',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696; '
         'not measured in CoA DL2-14391')
# kv40 — TDS + CoA actual + CoA spec
_r(BL, 'package_tier2', 'kv40',
   'Viscosity @ 40°C: 132 mm2/s (cSt)',
   unit='mm2/s', value='132', vk='typical',
   meth='ASTM D 445, DIN 51 550', cond='40°C',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696')
_r(BL, 'package_tier2', 'kv40',
   'VISCOSITY, 40°C, CST: ACTUAL 139',
   unit='mm2/s', value='139', vk='report-only',
   meth='ASTM D445  ISO 3104', cond='40°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result')
_r(BL, 'package_tier2', 'kv40',
   'VISCOSITY, 40°C, CST: MIN 115  MAX 165',
   unit='mm2/s', lo='115', hi='165', vk='range',
   meth='ASTM D445  ISO 3104', cond='40°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product specification bounds')
# kv100 — TDS + CoA actual + CoA spec
_r(BL, 'package_tier2', 'kv100',
   'Viscosity @ 100°C: 9 mm2/s (cSt)',
   unit='mm2/s', value='9', vk='typical',
   meth='ASTM D 445, DIN 51 550', cond='100°C',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696')
_r(BL, 'package_tier2', 'kv100',
   'VISCOSITY, 100°C, CST: ACTUAL 9.1',
   unit='mm2/s', value='9.1', vk='report-only',
   meth='ASTM D445  ISO 3104', cond='100°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result')
_r(BL, 'package_tier2', 'kv100',
   'VISCOSITY, 100°C, CST: MIN 7.5  MAX 11.0',
   unit='mm2/s', lo='7.5', hi='11.0', vk='range',
   meth='ASTM D445  ISO 3104', cond='100°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product specification bounds')
# density — TDS @25°C (non-standard temperature)
_r(BL, 'package_tier2', 'density',
   'Density @ 25°C: 0.976 g/ml',
   unit='g/ml', value='0.976', vk='typical',
   meth='ASTM D 4052', cond='25°C',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='temperature is 25°C (not the standard 15°C); identical on DL2-11696')
# specific_gravity — CoA @25°C actual + spec
_r(BL, 'package_tier2', 'specific_gravity',
   'SPECIFIC GRAVITY, 25°C: ACTUAL 0.977',
   unit='', value='0.977', vk='report-only',
   meth='ASTM D4052', cond='25°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result; temperature is 25°C')
_r(BL, 'package_tier2', 'specific_gravity',
   'SPECIFIC GRAVITY, 25°C: MIN 0.960  MAX 0.990',
   unit='', lo='0.960', hi='0.990', vk='range',
   meth='ASTM D4052', cond='25°C',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product specification bounds; temperature is 25°C')
# flash_point — TDS + CoA actual + CoA spec
_r(BL, 'package_tier2', 'flash_point',
   'Flash Point, COC: 140°C',
   unit='°C', value='140', vk='typical',
   meth='ASTM D 92, DIN 51376',
   sha='5ff875cfbd75', pg=1, vc=VC_TDS, review=REVIEW_BL,
   notes='from "TYPICAL PROPERTIES" table; noted "not specifications"; identical on DL2-11696')
_r(BL, 'package_tier2', 'flash_point',
   'FLASH POINT, COC, °C: ACTUAL >150',
   unit='°C', value='150', qual='>', vk='report-only',
   meth='ASTM D92  ISO 2592',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_ACT, review=REVIEW_BL,
   notes='CoA lot 08641 batch result; printed as ">150"')
_r(BL, 'package_tier2', 'flash_point',
   'FLASH POINT, COC, °C: MIN 120',
   unit='°C', lo='120', qual='>=', vk='bound',
   meth='ASTM D92  ISO 2592',
   sha='9c0ebc98e4f4', pg=1, vc=VC_COA_SPEC, review=REVIEW_BL,
   notes='CoA product spec lower bound; no upper bound stated')
_m(BL, 'package_tier2', 'pour_point',
   'not found in the inspected text', review=REVIEW_BL)


# ===========================================================================
# NA_SUL_BSN — additive_component (component_general)
# ===========================================================================

_r(BSN, 'component_general', 'function.primary',
   'NA-SUL BSN is a premium non-staining rust inhibitor for petroleum and synthetic '
   'lubricants, greases, rust preventive fluids and metalworking specialties.',
   vk='text', sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN)

_r(BSN, 'component_general', 'function.secondary',
   'It provides excellent demulsibility and resistance to the negative effects of water.',
   vk='text', sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   notes='demulsibility and water resistance stated as key features alongside rust inhibition')

_r(BSN, 'component_general', 'chemical_family',
   'Neutral barium dinonylnaphthalenesulfonate in light mineral oil.',
   vk='text', sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   notes='from "CHEMICAL COMPOSITION" section; active component is Ba-DNNSA; '
         'carrier stated as light mineral oil')

_m(BSN, 'component_general', 'active_content',
   'not found; % active (Ba-DNNSA concentrate) not stated in PDS; '
   'CoA reports % Sulfonate (51.4% actual, spec 50.0-52.0%) but this is sulfonate '
   'mass fraction, not "active content" in the template sense',
   review=REVIEW_BSN)

_r(BSN, 'component_general', 'carrier.identity',
   'Neutral barium dinonylnaphthalenesulfonate in light mineral oil.',
   vk='text', sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   notes='carrier identified as "light mineral oil" in chemical composition')

_m(BSN, 'component_general', 'carrier.share_wt_pct',
   'not found; wt% of light mineral oil diluent not stated in PDS or CoA',
   review=REVIEW_BSN)

# treat_rate — 8 application-specific ranges from TDS
_r(BSN, 'component_general', 'treat_rate',
   'Oil & Solvent Based Rust Preventive Fluids: 1.00% - 15.0%',
   unit='wt%', lo='1.00', hi='15.0', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Oil & Solvent Based Rust Preventive Fluids')
_r(BSN, 'component_general', 'treat_rate',
   'Hydraulic Fluids: 0.05% - 0.5%',
   unit='wt%', lo='0.05', hi='0.5', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Hydraulic Fluids')
_r(BSN, 'component_general', 'treat_rate',
   'Circulating Oils: 0.05% - 1.0%',
   unit='wt%', lo='0.05', hi='1.0', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Circulating Oils')
_r(BSN, 'component_general', 'treat_rate',
   'Compressor Oils: 0.10% - 0.5%',
   unit='wt%', lo='0.10', hi='0.5', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Compressor Oils')
_r(BSN, 'component_general', 'treat_rate',
   'Paper Machine Oils: 0.25% - 1.0%',
   unit='wt%', lo='0.25', hi='1.0', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Paper Machine Oils')
_r(BSN, 'component_general', 'treat_rate',
   'Way Lubricants: 0.10% - 0.5%',
   unit='wt%', lo='0.10', hi='0.5', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Way Lubricants')
_r(BSN, 'component_general', 'treat_rate',
   'Greases: 0.50% - 3.0%',
   unit='wt%', lo='0.50', hi='3.0', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Greases')
_r(BSN, 'component_general', 'treat_rate',
   'Industrial and Automotive Gear Oils: 0.10% - 1.0%',
   unit='wt%', lo='0.10', hi='1.0', vk='range',
   sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   entry='Industrial and Automotive Gear Oils')

_r(BSN, 'component_general', 'compatibility_restrictions',
   'compatible with a wide range of additives and base oils',
   vk='text', sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
   notes='from product description in PDS; no restrictions stated; '
         'barium DNNSA also available in PAO, ester, and mineral spirits diluents (stated in body text)')

_m(BSN, 'component_general', 'function_specific_markers.tbn',
   'not found; TBN not stated in PDS or CoA '
   '(Ba-DNNSA is neutral — TBN near zero is expected but not printed)',
   review=REVIEW_BSN)
_m(BSN, 'component_general', 'function_specific_markers.ca',
   'not found', review=REVIEW_BSN)
_m(BSN, 'component_general', 'function_specific_markers.mg',
   'not found', review=REVIEW_BSN)
_m(BSN, 'component_general', 'function_specific_markers.p',
   'not found', review=REVIEW_BSN)
_m(BSN, 'component_general', 'function_specific_markers.zn',
   'not found', review=REVIEW_BSN)
_m(BSN, 'component_general', 'function_specific_markers.mo',
   'not found', review=REVIEW_BSN)

# not_in_template for BSN
# barium — TDS typical + CoA actual + CoA spec
_nit(BSN, 'barium',
     'Barium Content: 6.6%',
     unit='wt%', value='6.6', vk='typical',
     sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"; Ba not in function_specific_markers')
_nit(BSN, 'barium',
     'BARIUM CONTENT, %: ACTUAL 6.65',
     unit='wt%', value='6.65', vk='report-only',
     meth='KI-205 (GRAV.)',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; MFG 2019-10-03')
_nit(BSN, 'barium',
     'BARIUM CONTENT, %: MIN 6.50  MAX 6.80',
     unit='wt%', lo='6.50', hi='6.80', vk='range',
     meth='KI-205 (GRAV.)',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# kv40 — TDS typical only
_nit(BSN, 'kv40',
     'Viscosity @ 40°C: 2100 mm2/s (cSt)',
     unit='mm2/s', value='2100', vk='typical',
     meth='ASTM D 445, DIN 51 550', cond='40°C',
     sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
# kv100 — TDS typical + CoA actual + CoA spec
_nit(BSN, 'kv100',
     'Viscosity @ 100°C: 53 mm2/s (cSt)',
     unit='mm2/s', value='53', vk='typical',
     meth='ASTM D 445, DIN 51 550', cond='100°C',
     sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
_nit(BSN, 'kv100',
     'VISCOSITY, CST @ 100°C: ACTUAL 59.8',
     unit='mm2/s', value='59.8', vk='report-only',
     meth='ISO 3104  ASTM D445', cond='100°C',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; higher than TDS typical (53 vs 59.8) — both within spec 47-61')
_nit(BSN, 'kv100',
     'VISCOSITY, CST @ 100°C: MIN 47.0  MAX 61.0',
     unit='mm2/s', lo='47.0', hi='61.0', vk='range',
     meth='ISO 3104  ASTM D445', cond='100°C',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# density — TDS @15.6°C
_nit(BSN, 'density',
     'Density @ 15.6°C: 1.02 g/ml',
     unit='g/ml', value='1.02', vk='typical',
     meth='ASTM D 4052', cond='15.6°C',
     sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"; temperature 15.6°C')
# specific_gravity — CoA @15.6°C actual + spec
_nit(BSN, 'specific_gravity',
     'SPECIFIC GRAVITY, 15.6°C: ACTUAL 1.015',
     unit='', value='1.015', vk='report-only',
     meth='ASTM D4052', cond='15.6°C',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; slightly lower than TDS density 1.02 (different batches, '
           'both "> 1" consistent with Ba-DNNSA in mineral oil)')
_nit(BSN, 'specific_gravity',
     'SPECIFIC GRAVITY, 15.6°C: MIN 1.010  MAX 1.030',
     unit='', lo='1.010', hi='1.030', vk='range',
     meth='ASTM D4052', cond='15.6°C',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# flash_point — TDS + CoA actual + CoA spec
_nit(BSN, 'flash_point',
     'Flash Point, COC: 165°C (329°F)',
     unit='°C', value='165', vk='typical',
     meth='ASTM D 92, DIN 51 376',
     sha='5ef35a134626', pg=1, vc=VC_TDS, review=REVIEW_BSN,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
_nit(BSN, 'flash_point',
     'FLASH POINT, COC, °C: ACTUAL 180',
     unit='°C', value='180', vk='report-only',
     meth='ASTM D92  ISO 2592',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; higher than TDS typical 165°C '
           '(batch result vs typical; both > spec min 160°C)')
_nit(BSN, 'flash_point',
     'FLASH POINT, COC, °C: MIN 160',
     unit='°C', lo='160', qual='>=', vk='bound',
     meth='ASTM D92  ISO 2592',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product spec lower bound; no upper bound stated')
# sulfonate — CoA actual + CoA spec
_nit(BSN, 'sulfonate_content',
     '% SULFONATE: ACTUAL 51.4',
     unit='wt%', value='51.4', vk='report-only',
     meth='ASTM D3049',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; sulfonate mass fraction of product')
_nit(BSN, 'sulfonate_content',
     '% SULFONATE: MIN 50.0  MAX 52.0',
     unit='wt%', lo='50.0', hi='52.0', vk='range',
     meth='ASTM D3049',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# moisture — CoA actual + CoA spec
_nit(BSN, 'moisture_content',
     'MOISTURE CONTENT, %: ACTUAL 0.2',
     unit='wt%', value='0.2', vk='report-only',
     meth='ASTM E1064',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result')
_nit(BSN, 'moisture_content',
     'MOISTURE CONTENT, %: MIN 0  MAX 0.4',
     unit='wt%', lo='0', hi='0.4', vk='range',
     meth='ASTM E1064',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# neutralization number — CoA actual + CoA spec
_nit(BSN, 'neutralization_number',
     'NEUTRALIZATION NO.: ACTUAL 0.2',
     unit='mg KOH/g', value='0.2', vk='report-only',
     meth='KI-203',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; KI-203 is a King Industries internal method; '
           'not equivalent to TBN (ASTM D2896)')
_nit(BSN, 'neutralization_number',
     'NEUTRALIZATION NO.: MIN 0.0  MAX 1.0',
     unit='mg KOH/g', lo='0.0', hi='1.0', vk='range',
     meth='KI-203',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product specification bounds')
# color — CoA actual + CoA spec
_nit(BSN, 'color',
     'COLOR, DILUTE: ACTUAL 4.0',
     unit='ASTM D1500', value='4.0', vk='report-only',
     meth='ISO 2049  ASTM D1500',
     sha='a796dc222984', pg=1, vc=VC_COA_ACT, review=REVIEW_BSN,
     notes='CoA lot 9A625 batch result; dilute solution color')
_nit(BSN, 'color',
     'COLOR, DILUTE: MAX 6.0',
     unit='ASTM D1500', hi='6.0', qual='<=', vk='bound',
     meth='ISO 2049  ASTM D1500',
     sha='a796dc222984', pg=1, vc=VC_COA_SPEC, review=REVIEW_BSN,
     notes='CoA product spec upper bound')


# ===========================================================================
# NA_LUBE_AO_142_I — additive_component (component_general)
# ===========================================================================

_r(AO, 'component_general', 'function.primary',
   'NA-LUBE AO-142-I is a liquid diphenylamine based antioxidant for synthetic '
   'and mineral oil based lubricants and greases.',
   vk='text', sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO)

_m(AO, 'component_general', 'function.secondary',
   'not found; no secondary function stated in PDS', review=REVIEW_AO)

_r(AO, 'component_general', 'chemical_family',
   'Butylated, octylated diphenylamine.',
   vk='text', sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   notes='from "CHEMICAL COMPOSITION" section; liquid DPA-type antioxidant')

_m(AO, 'component_general', 'active_content',
   'not found; no active content % stated in PDS', review=REVIEW_AO)

_m(AO, 'component_general', 'carrier.identity',
   'not found; no carrier stated — product appears to be a neat liquid (no diluent mentioned)',
   review=REVIEW_AO)

_m(AO, 'component_general', 'carrier.share_wt_pct',
   'not found; no carrier stated', review=REVIEW_AO)

# treat_rate — 4 application-specific ranges from TDS
_r(AO, 'component_general', 'treat_rate',
   'Hydraulic and Circulating Oils: 0.2% - 0.5%',
   unit='wt%', lo='0.2', hi='0.5', vk='range',
   sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   entry='Hydraulic and Circulating Oils')
_r(AO, 'component_general', 'treat_rate',
   'Compressor and Paper Machine Oils: 0.2% - 0.5%',
   unit='wt%', lo='0.2', hi='0.5', vk='range',
   sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   entry='Compressor and Paper Machine Oils')
_r(AO, 'component_general', 'treat_rate',
   'Greases and Engine Oils: 0.2% - 0.6%',
   unit='wt%', lo='0.2', hi='0.6', vk='range',
   sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   entry='Greases and Engine Oils')
_r(AO, 'component_general', 'treat_rate',
   'Industrial and Automotive Gear Oils: 0.1% - 0.6%',
   unit='wt%', lo='0.1', hi='0.6', vk='range',
   sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   entry='Industrial and Automotive Gear Oils')

_m(AO, 'component_general', 'compatibility_restrictions',
   'not found; no compatibility restrictions stated in PDS; '
   '"suitable for synthetic and mineral oil based lubricants and greases; '
   'can also be used in synthetic base fluids such as silicone oils and diesters" '
   '(broad application scope, no restrictions)',
   review=REVIEW_AO)

_r(AO, 'component_general', 'function_specific_markers.tbn',
   'Total Base Number (ASTM D 2896): 135 mg KOH/g',
   unit='mg KOH/g', value='135', vk='typical',
   meth='ASTM D 2896',
   sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
   notes='from "TYPICAL PROPERTIES"; noted "not specifications"; DPA antioxidant TBN')

_m(AO, 'component_general', 'function_specific_markers.ca',
   'not found', review=REVIEW_AO)
_m(AO, 'component_general', 'function_specific_markers.mg',
   'not found', review=REVIEW_AO)
_m(AO, 'component_general', 'function_specific_markers.p',
   'not found', review=REVIEW_AO)
_m(AO, 'component_general', 'function_specific_markers.zn',
   'not found', review=REVIEW_AO)
_m(AO, 'component_general', 'function_specific_markers.mo',
   'not found', review=REVIEW_AO)

# not_in_template for AO-142-I
_nit(AO, 'nitrogen',
     'Nitrogen Content: 4.5%',
     unit='wt%', value='4.5', vk='typical',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"; '
           'N not in function_specific_markers template field')
_nit(AO, 'kv40',
     'Viscosity @ 40°C: 280 mm2/s (cSt)',
     unit='mm2/s', value='280', vk='typical',
     meth='ASTM D 445, DIN 51 550', cond='40°C',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
_nit(AO, 'kv100',
     'Viscosity @ 100°C: 9.0 mm2/s (cSt)',
     unit='mm2/s', value='9.0', vk='typical',
     meth='ASTM D 445, DIN 51 550', cond='100°C',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
_nit(AO, 'density',
     'Density @ 15.6°C: 0.98 g/ml',
     unit='g/ml', value='0.98', vk='typical',
     meth='ASTM D 4052', cond='15.6°C',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"; temperature 15.6°C')
_nit(AO, 'flash_point',
     'Flash Point, COC: 185°C (366°F)',
     unit='°C', value='185', vk='typical',
     meth='ASTM D 92, DIN 51 376',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"')
_nit(AO, 'color',
     'Color (ASTM D 1500 neat): 3.0',
     unit='ASTM D1500', value='3.0', vk='typical',
     meth='ASTM D 1500',
     sha='39a7f5fadd1d', pg=1, vc=VC_TDS, review=REVIEW_AO,
     notes='from "TYPICAL PROPERTIES"; noted "not specifications"; neat product color')


# ===========================================================================
write_rows('s34_king.csv', ROWS)
if __name__ == '__main__':
    print(f's34_king: {len(ROWS)} rows written to field_evidence/s34_king.csv')
