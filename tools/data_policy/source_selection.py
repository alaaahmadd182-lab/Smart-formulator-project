"""Rule 1 (source-selection policy, 2026-11-10): select the TDS value, with SDS fallback.

  1. For a property, the selected value comes from the applicable technical document (TDS, PDS, technical bulletin,
     specification sheet, product catalog; see document_classes.py) when one provides that property.
  2. If no technical document provides the property, the applicable SDS value is selected (SDS fallback).
  3. The selected value keeps its exact source, page, revision, qualifier, unit, method and conditions; every other
     printed value stays in alternate_entries or conflicts[] with its provenance.
  4. The SDS is always inspected when both document types provide the property (the comparison inventory,
     tds_sds_inventory.py, lists every such pair). Selecting the TDS value is a selection rule; it does not mean the SDS
     value is wrong, and a TDS-SDS disagreement stays recorded and unresolved.
  5. A TDS value is not selected (documented exception) when it is unreadable, internally inconsistent, demonstrably
     erroneous, or lacks a condition the property definition requires (e.g. a density without a reference temperature).
  6. "Applicable" means the same product, grade, region and formulation and the same property under the property's
     defining conditions. A technical specification range or bound can be the selected information: it is selected as
     printed, never converted to a single value, and the SDS typical value is kept as an alternate (clarified
     2026-11-10). Whether a range or bound is usable for a calculation is assessed separately (mandatory-property
     rules). A different value kind alone is not a reason to keep the SDS; identity, applicability, conflicting
     editions or source reliability are (PENDING, with the reason).
  7. Several TDS editions: the newest dated edition supplies the value. Undated editions that print the same value may
     be cited interchangeably; undated editions that disagree are a TDS-TDS conflict and stay PENDING (no edition rule
     applies). A supplier's current public product page (retrieval date recorded) is treated as the current edition
     only where the record already uses it; such cases are listed, not changed.

SDS wording is kept as printed: an SDS bound such as ">= 180 °C" is a lower bound and is not relabelled as a
"specification", "safety limit" or "safety margin".

Usage:
    python tools/data_policy/source_selection.py            # dry run: checks every declared change, writes nothing
    python tools/data_policy/source_selection.py --write    # applies the changes (only if every check passes)
    python tools/data_policy/source_selection.py --report   # writes reports/data_policy/source_selection_changes.csv
Exit codes: 0 all declared changes match the data (or were applied); 1 a declared "before" does not match.
Importing this module writes nothing.
"""
import argparse, copy, csv, importlib.util, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import policy_lib as P

POLICY_DATE = '2026-11-10'
SEL_NOTE = (f'Selected under the source-selection policy of {POLICY_DATE} (TDS value first, SDS fallback); '
            'see docs/data_policy_mandatory_review/source_selection_policy.md.')
ALT_NOTE = (f'Previously selected value, kept as an alternate under the source-selection policy of {POLICY_DATE}. '
            'Not judged erroneous: the policy selects the technical-document value first.')
RICHFUL_UNDATED = 'TDS prints no revision date'

# ---------------------------------------------------------------- the reviewed selection changes
# Each change: product, file name, field path, the field as it is now (expect: value + source file), the new selected
# value (new), what the previous value was (old_kind: value_kind correction for the alternate, if its label was not
# supported by the printed wording), and the evidence (TDS row as printed, read from the text layer or a render).


def richful_flash(pid, sds_file, tds_file, typical, printed, method='GB/T 3536, ASTM D92', bound='≥180'):
    return dict(product=pid, file='tier2_numeric_contribution.json', path='flash_point',
                expect=dict(value=180, source=sds_file),
                new=dict(value=typical, qualifier=None, min=None, max=None, value_kind='typical', printed_text=printed,
                         unit='°C', test_temperature_c=None, method=method, flash_method='COC',
                         source=dict(file=tds_file, page=1, revision_date=None),
                         calculation_note=(f'TDS "Typical Value" column (Item | Index | Typical Value | Test Method); the same row prints '
                                           f'the index (specification) {bound} °C, which this typical value meets. {RICHFUL_UNDATED}.')),
                old_kind=('lower bound', 'The SDS prints the flash point as a lower bound (">= 180 °C" / "≥180"); the earlier '
                                         'label value_kind "specification" is not supported by the SDS wording.'),
                evidence=f'{tds_file} p.1 (text layer): "{printed}"')


def richful_row(pid, path, expect_value, sds_file, tds_file, value, printed, unit, temp, method, rng=None):
    lo, hi = (rng or (None, None))
    return dict(product=pid, file='tier2_numeric_contribution.json', path=path,
                expect=dict(value=expect_value, source=sds_file),
                new=dict(value=value, qualifier=None, min=lo, max=hi, value_kind='typical', printed_text=printed, unit=unit,
                         test_temperature_c=temp, method=method, source=dict(file=tds_file, page=1, revision_date=None),
                         calculation_note=(f'TDS "Typical Value" column' + (f'; index (specification range) {lo}-{hi} {unit} printed in the same row' if rng else '')
                                           + f'. {RICHFUL_UNDATED}.')),
                old_kind=None, evidence=f'{tds_file} p.1 (text layer): "{printed}"')


CHANGES = [
    # --- flash point: SDS lower bound -> TDS typical (audit CF-148 to CF-156; CF-003)
    richful_flash('RICHFUL_RF6066', 'DL2-15831.pdf', 'DL2-15451.pdf', 220, 'Flash Point (COC), ℃ ≥180 220 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6069', 'DL2-15619.pdf', 'DL2-15618.pdf', 216, 'Flash Point (COC), ℃ ≥180 216 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6077', 'DL2-15542.pdf', 'DL2-15536.pdf', 210, 'Flash Point (COC), ℃ ≥180 210 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6078', 'DL2-15833.pdf', 'DL2-15832.pdf', 220, 'Flash Point (COC), ℃ ≥180 220 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6079', 'DL2-15541.pdf', 'DL2-15535.pdf', 214, 'Flash Point (COC), ℃ ≥180 214 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6088', 'DL2-15838.pdf', 'DL2-15452.pdf', 203, 'Flash Point (COC), ℃ ≥180 203 GB/T 3536, ASTM D92'),
    richful_flash('RICHFUL_RF6088F', 'DL2-15840.pdf', 'DL2-15839.pdf', 218, 'Flash Point (COC), ℃ ≮180 218 GB/T 3536，ASTM D92',
                  method='GB/T 3536, ASTM D92', bound='≮180'),
    richful_flash('RICHFUL_RF6400', 'DL2-15850.pdf', 'DL2-15849.pdf', 226, 'Flash Point (COC), ℃ ≥180 226 GB/T3536, ASTM D92',
                  method='GB/T3536, ASTM D92'),
    richful_flash('RICHFUL_RF6406', 'RF6406.pdf', 'DL2-15456.pdf', 223, 'Flash Point (COC), ℃ ≮180 223 GB/T3536, ASTM D92',
                  method='GB/T3536, ASTM D92', bound='≮180'),
    dict(product='INFINEUM_D3424', file='tier2_numeric_contribution.json', path='flash_point',
         expect=dict(value=110, source='DL2-10204.pdf'),
         new=dict(value=190, qualifier=None, min=None, max=None, value_kind='typical', printed_text='Flash Point (PM) 190 °C ASTM D 93',
                  unit='°C', test_temperature_c=None, method='ASTM D 93', flash_method='PMCC',
                  source=dict(file='DL2-10204.pdf', page=1, revision_date='2004-11-09'),
                  calculation_note=('"Typical Inspections" table of the TDS (p.1, version 9th November 2004 (3.1)), footnote "(a) Not a '
                                    'specification". The SDS in the same file (p.6, revision 02Dec2008) prints ">110C (230F)", a lower bound '
                                    'that the typical value meets. A newer SDS revision is not a newer edition of the TDS.')),
         old_kind=('lower bound', 'The SDS prints ">110C" (a lower bound); the earlier label value_kind "specification" is not supported by '
                                  'the SDS wording.'),
         evidence='DL2-10204.pdf p.1 (text layer): "Flash Point (PM) 190 °C ASTM D 93"'),
    # --- density: SDS -> TDS (same number, or the TDS value where they differ)
    richful_row('RICHFUL_RF6069', 'density', 981, 'DL2-15619.pdf', 'DL2-15618.pdf', 981, 'Density (20℃), kg/m3 961-1001 981 SH/T 0604, ASTM D4052',
                'kg/m3', 20, 'SH/T 0604, ASTM D4052', (961, 1001)),
    richful_row('RICHFUL_RF6077', 'density', 0.991, 'DL2-15542.pdf', 'DL2-15536.pdf', 998, 'Density (20℃), kg/m3 978-1018 998 GB/T 13377, ASTM D4052',
                'kg/m3', 20, 'GB/T 13377, ASTM D4052', (978, 1018)),
    richful_row('RICHFUL_RF6079', 'density', 1.0, 'DL2-15541.pdf', 'DL2-15535.pdf', 1000, 'Density (20℃), kg/m3 980-1020 1000 GB/T 13377, ASTM D4052',
                'kg/m3', 20, 'GB/T 13377, ASTM D4052', (980, 1020)),
    richful_row('RICHFUL_RF6088', 'density', 0.955, 'DL2-15838.pdf', 'DL2-15452.pdf', 955, 'Density (20℃), kg/m3 935-975 955 GB/T 13377, ASTM D4052',
                'kg/m3', 20, 'GB/T 13377, ASTM D4052', (935, 975)),
    richful_row('RICHFUL_RF6400', 'density', 1039, 'DL2-15850.pdf', 'DL2-15849.pdf', 1039, 'Density (20℃), kg/m3 1019-1059 1039 SH/T 0604, ASTM D4052',
                'kg/m3', 20, 'SH/T 0604, ASTM D4052', (1019, 1059)),
    richful_row('RICHFUL_RF6406', 'density', 1.06, 'RF6406.pdf', 'DL2-15456.pdf', 1060, 'Density (20℃), kg/m3 1037-1077 1060 SH/T 0604, ASTM D4052',
                'kg/m3', 20, 'SH/T 0604, ASTM D4052', (1037, 1077)),
    # --- KV100: SDS -> TDS
    richful_row('RICHFUL_RF6077', 'kv100', 150, 'DL2-15542.pdf', 'DL2-15536.pdf', 160, 'Kinematic Viscosity (100℃), mm2/s Report 160 GB/T 265, ASTM D445',
                'mm2/s', 100, 'GB/T 265, ASTM D445'),
    richful_row('RICHFUL_RF6078', 'kv100', 146, 'DL2-15833.pdf', 'DL2-15832.pdf', 146, 'Kinematic Viscosity (100℃), mm2/s Report 146 GB/T 265, ASTM D445',
                'mm2/s', 100, 'GB/T 265, ASTM D445'),
    richful_row('RICHFUL_RF6079', 'kv100', 140, 'DL2-15541.pdf', 'DL2-15535.pdf', 140, 'Kinematic Viscosity (100℃), mm2/s Report 140 GB/T 265, ASTM D445',
                'mm2/s', 100, 'GB/T 265, ASTM D445'),
    richful_row('RICHFUL_RF6088', 'kv100', 100, 'DL2-15838.pdf', 'DL2-15452.pdf', 100, 'Kinematic Viscosity (100℃), mm2/s Report 100 GB/T 265, ASTM D445',
                'mm2/s', 100, 'GB/T 265, ASTM D445'),
    richful_row('RICHFUL_RF6088F', 'kv100', 178.2, 'DL2-15840.pdf', 'DL2-15839.pdf', 177, 'Kinematic Viscosity (100℃), mm2/s Report 177 GB/T 265，ASTM D445',
                'mm2/s', 100, 'GB/T 265, ASTM D445'),
    richful_row('RICHFUL_RF6400', 'kv100', 109, 'DL2-15850.pdf', 'DL2-15849.pdf', 109, 'Kinematic Viscosity (100℃), mm2/s Report 109 GB/T265, ASTM D445',
                'mm2/s', 100, 'GB/T265, ASTM D445'),
    richful_row('RICHFUL_RF6406', 'kv100', 72, 'RF6406.pdf', 'DL2-15456.pdf', 72, 'Kinematic Viscosity (100℃), mm2/s Report 72 GB/T265, ASTM D445',
                'mm2/s', 100, 'GB/T265, ASTM D445'),
]

NEX = 'DL2-10962.pdf'
NEX_NOTE = ('NEXBASE family "Technical Data Sheet BASE OILS" (Neste Oil, Edition 8; no calendar date printed), image-only page read on a '
            'render (2026-11-10), column "Nexbase 3020", sub-column "Typ".')
for path, file, expect_v, expect_src, new in [
    ('kv40', 'NESTE_NEXBASE_3020_tier1.json', 7.5, 'DL2-14513.pdf',
     dict(value=7.5, value_kind='typical', printed_text='Viscosity at 40 °C, mm²/s: Spec ≥ 7.1, Typ 7.5', unit='mm2/s', test_temperature_c=40,
          method=None, min=None, max=None, qualifier=None)),
    ('kv100', 'NESTE_NEXBASE_3020_tier1.json', None, None,
     dict(value=2.2, value_kind='typical', printed_text='Viscosity at 100 °C, mm²/s: Spec 2.1-2.3, Typ 2.2', unit='mm2/s', test_temperature_c=100,
          method=None, min=None, max=None, qualifier=None)),
    ('density', 'NESTE_NEXBASE_3020_tier1.json', None, None,
     dict(value=834, value_kind='typical', printed_text='Density@15 °C, Kg/m³: Spec –, Typ 834', unit='kg/m3', test_temperature_c=15,
          method=None, min=None, max=None, qualifier=None)),
    ('pour_point', 'NESTE_NEXBASE_3020_tier2.json', -42, 'DL2-14513.pdf',
     dict(value=-45, value_kind='typical', printed_text='Pour Point, °C: Spec ≤ -42, Typ -45', unit='°C', test_temperature_c=None,
          method=None, min=None, max=None, qualifier=None)),
    ('flash_point', 'NESTE_NEXBASE_3020_tier2.json', 150, 'DL2-14513.pdf',
     dict(value=160, value_kind='typical', printed_text='Flash Point, °C: Spec ≥155, Typ 160', unit='°C', test_temperature_c=None,
          method=None, min=None, max=None, qualifier=None)),
]:
    new['source'] = dict(file=NEX, page=1, revision_date=None)
    new['calculation_note'] = NEX_NOTE + (' The sheet prints no test method.' if path in ('kv40', 'kv100', 'pour_point', 'flash_point', 'density') else '')
    if path == 'flash_point':
        new['flash_method'] = None
    CHANGES.append(dict(product='NESTE_NEXBASE_3020', file=file, path=path, expect=dict(value=expect_v, source=expect_src), new=new,
                        old_kind=(('upper limit', 'The SDS prints "Pour point ≤ -42°C" (an upper limit); kept as printed.') if path == 'pour_point' else
                                  ('lower bound', 'The SDS prints "Flash point > 150°C" (a lower bound); kept as printed.') if path == 'flash_point' else None),
                        evidence=f'{NEX} p.1 (render): 3020 column, Typ value; the record previously stated "No product TDS supplied for NEXBASE 3020", '
                                 'but this family TDS has a 3020 column'))

FORMOSA_NOTE = ('Product specification (Formosa Petrochemical, issue date 2009-10-21, version 1.0), "Limitation" columns Min. / Max.; '
                'a specification range, not a typical value. Selected as printed (no single value derived); the SDS typical value is '
                'kept as an alternate. Clarified rule of 2026-11-10: a different value kind alone does not override the technical document.')
for pid, fname, spec_file, lo, hi, sds_file, sds_val, sds_line in [
        ('FORMOSA_150N_GII_PLUS', 'FORMOSA_150N_GII_PLUS_tier1.json', 'DL2-10001.pdf', 5.0, 5.4, 'DL2-10011.pdf', 5.2,
         'Viscosity:   29.3 cSt at 40℃  |  5.2 cSt at 100℃'),
        ('FORMOSA_500N_GII', 'FORMOSA_500N_GII_tier1.json', 'DL2-10003.pdf', 10, 12, 'DL2-10017.pdf', 11,
         'Viscosity:   85 cSt at 40℃  | 11 cSt at 100℃')]:
    CHANGES.append(dict(
        product=pid, file=fname, path='kv100', expect=dict(value=sds_val, source=sds_file),
        new=dict(value=None, qualifier='Specification', min=lo, max=hi, value_kind='range',
                 printed_text=f'3. Kinematic viscosity，100℃ mm2/s （cSt） {lo} {hi} D445', unit='mm2/s', test_temperature_c=100,
                 method='ASTM D445', source=dict(file=spec_file, page=1, revision_date='2009-10-21'), calculation_note=FORMOSA_NOTE),
        old_kind=None,
        old_override=dict(min=None, max=None, printed_text=sds_line,
                          notes=(f'SDS {sds_file} p.3 line as printed. The specification range that this entry previously carried in min/max '
                                 f'(and in its printed_text) is printed in {spec_file}, not in the SDS; it is now the selected value.')),
        evidence=f'{spec_file} p.1 (text layer): "3. Kinematic viscosity，100℃ mm2/s （cSt） {lo} {hi} D445" (Min., Max. columns)'))

# ---------------------------------------------------------------- evidence review of 2026-11-10 (revision 3)
# Fills of Missing fields from exact product-specific printed evidence found in the lead review
# (reports/data_policy/lead_review.csv). Technical document first; SDS only where no technical document prints the
# property. Each entry was read on the cited page (text layer, or a render where stated).
REVIEW_NOTE = 'Filled in the evidence review of 2026-11-10 (lead review, reports/data_policy/lead_review.csv); '


def _src(f, p, rev=None):
    return dict(file=f, page=p, revision_date=rev)


CHANGES += [
    dict(product='CHEVRON_GROUP_II_600R', file='CHEVRON_GROUP_II_600R__base_oil_tier1_blocking.json', path='kv40',
         expect=dict(value=None, source=None), change_label='filled from the technical specification (was Missing)',
         new=dict(value=None, qualifier='minimum', min=100, max=None, value_kind='minimum', printed_text='100 (MIN)', unit='cSt',
                  test_temperature_c=40, method='ASTM D445', source=_src('DL2-10004.pdf', 1),
                  calculation_note=REVIEW_NOTE + 'Chevron "Group II/II+ Specifications" table, row "Viscosity @ 40°C, cSt" (ASTM D445), '
                                                 'column 600R prints "100 (MIN)" (render read 2026-11-10). A specification minimum, not a typical '
                                                 'value; recorded as a lower bound. DL2-10008/10010/10013/10014/10019 are byte-identical copies.'),
         old_kind=None, evidence='DL2-10004.pdf p.1 (render): Viscosity @ 40°C, cSt | ASTM D445 | ... | 600R: 100 (MIN)'),
    dict(product='CHEVRON_SYNFLUID_MPAO_65', file='CHEVRON_SYNFLUID_MPAO_65__base_oil_tier2_verification.json', path='flash_point',
         expect=dict(value=None, source=None), change_label='filled from the technical sheet (was Missing); SDS value kept as alternate',
         new=dict(value=266, qualifier='>', min=None, max=None, value_kind='lower bound', printed_text='Flash Point (COC), °F, °C >511 (266)',
                  unit='°C', test_temperature_c=None, method='COC', flash_method='COC', source=_src('DL2-11910.pdf', 1),
                  calculation_note=REVIEW_NOTE + 'Synfluid mPAO 65 cSt technical sheet prints the flash point as ">511 (266)" (°F, °C), '
                                                 'a lower bound. DL2-15009.pdf prints the same line. The SDS DL2-11908.PDF p.3 prints 270 °C '
                                                 '(ASTM D-92), kept as an alternate.'),
         add_alternates=[dict(value=270, qualifier=None, min=None, max=None, value_kind='SDS reported', printed_text='Flash point : 270 °C (518 °F) Method: ASTM D-92',
                              unit='°C', test_temperature_c=None, method='ASTM D-92', status='Reported', calculation_note=None,
                              source=_src('DL2-11908.PDF', 3, '2017-07-10'),
                              selection_note='SDS value, kept as an alternate: the technical sheet prints the property (Rule 1).')],
         old_kind=None, evidence='DL2-11910.pdf p.1 (text layer): "Flash Point (COC), °F, °C >511 (266)"'),
    dict(product='ERGON_HYGOLD_P150BS', file='ERGON_HYGOLD_P150BS_tier2.json', path='noack_volatility',
         expect=dict(value=None, source=None), change_label='filled from the technical specification (was Missing)',
         new=dict(value=1.1, qualifier=None, min=None, max=None, value_kind='typical', printed_text='Noack Volatility, wt% ASTM D5800 1.1',
                  unit='wt%', test_temperature_c=None, method='ASTM D5800', source=_src('DL2-10961.pdf', 1),
                  calculation_note=REVIEW_NOTE + 'HyGold P150BS Marketing Specification, "TYPICAL VALUES" column (no specification limit printed; '
                                                 'render read 2026-11-10). Procedure and test temperature are not printed.'),
         old_kind=None, evidence='DL2-10961.pdf p.1 (render): Noack Volatility, wt% | ASTM D5800 | | | 1.1 (typical)'),
    dict(product='EXXONMOBIL_SPECTRASYN_ULTRA_1000', file='EXXONMOBIL_SPECTRASYN_ULTRA_1000__base_oil_tier1_blocking.json', path='specific_gravity',
         expect=dict(value=None, source=None), create_field=True, change_label='filled from a technical sheet of the same product (field absent)',
         new=dict(value=0.855, qualifier=None, min=None, max=None, value_kind='typical', printed_text='Specific Gravity (60.1°F (15.6°C)) 0.855',
                  unit='dimensionless', test_temperature_c=15.6, method='ASTM D4052', source=_src('DL2-13746.pdf', 1, '2011'),
                  calculation_note=REVIEW_NOTE + 'SpectraSyn Ultra 1000 product sheet (© 2011), typical value. The record\'s other values cite '
                                                 'DL2-11190.pdf (image, undated), which prints no specific gravity; no conflict.'),
         old_kind=None, evidence='DL2-13746.pdf p.1 (text layer): "Specific Gravity (60.1°F (15.6°C)) 0.855 0.855 ASTM D4052"'),
]
CHANGES.append(dict(
    product='ARAMCO_LUBEREF_PRIMA_500', file='ARAMCO_LUBEREF_PRIMA_500__base_oil_tier1_blocking.json', path='kv40',
    expect=dict(value=None, source=None), change_label='filled from the supplier brochure (technical; was Missing)',
    new=dict(value=96.4, qualifier=None, min=None, max=None, value_kind='typical', printed_text='Kinematic Viscosity @ 40°C, cSt (D 445): 96.4',
             unit='cSt', test_temperature_c=40, method='ASTM D445', source=_src('DL2-11773.pdf', 1),
             calculation_note=REVIEW_NOTE + 'aramcoPRIMA brochure, Group II "Typical" table, column "aramcoPRIMA 500" (image, render read '
                                            '2026-11-10; no "subject to confirmation" mark on this column). The specification DL2-12172.pdf cited '
                                            'by the record prints KV40 "Report".'),
    old_kind=None, evidence='DL2-11773.pdf p.1 (render): Kinematic Viscosity @ 40°C, cSt | D 445 | aramcoPRIMA 500 Typical 96.4'))

# aramcoULTRA 8 (decision of 2026-11-11): the applicable technical-source value is selected; the archived SDS range is
# kept as an alternate, and the disagreement with the SDS is recorded and assessed separately (it is not a veto).
# Values confirmed on both saved copies of the manufacturer table by verify_soil_table.py.
SOIL_URL = 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx'
SOIL_NOTE = ("Selected 2026-11-11 under the source-selection policy (technical source first). S-OIL 'Lube Base Oil' web page, table "
             "'Typical Properties of aramcoULTRA Base Oil', column 'aramcoULTRA 8', row '{row}', ASTM cell '{astm}'. Read on the two "
             "saved copies in reconciliation/audit_evidence/: SOIL_LubeBaseOil__wayback_20260610070302.html (Internet Archive capture "
             "2026-06-10, SHA-256 cff0d3bbb7964c7450a1b9fa813617bf76e4b09de39187d026f674c7604fda60) and SOIL_LubeBaseOil_live_2026-10-30.html (live page retrieved 2026-10-30, SHA-256 "
             "94b263ad23cfd8b9631b5b637635c0cbdb341aad25cb7553a2a44513f10f011c); both print the same cell. The page prints no publication or revision date: its edition date is unknown, "
             "and a capture or retrieval date is not an edition date. The archived SDS DL2-14611.pdf (2018-09-07) prints {sds}; it is "
             "kept as an alternate entry. {rel}")
for _path, _file, _row, _astm, _printed, _val, _unit, _temp, _method, _sds, _rel, _extra in [
        ('kv40', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'Kinematic Viscosity @ 40℃, cSt', 'D445', '41.10', 41.1, 'cSt', 40, 'ASTM D445',
         'the range 42.0 - 55.0 cSt @ 40 °C (ASTM D 445)',
         'The typical value lies below that range: the disagreement is the unresolved conflict already in conflicts[] (2026-10 audit); '
         'selecting the technical value does not resolve it and does not judge the SDS wrong.', {}),
        ('kv100', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'Kinematic Viscosity @ 100℃, cSt', 'D445', '7.1', 7.1, 'cSt', 100, 'ASTM D445',
         'the range 7.0 - 7.5 cSt @ 100 °C (ASTM D 445)',
         'The typical value lies inside that range: logically compatible, which is not evidence of agreement (the kind of the SDS range '
         'is not stated).', {}),
        ('flash_point', 'S_OIL_ARAMCO_ULTRA_8_tier2.json', 'Flash Point,COC ,℃', 'D92', '250', 250, '°C', None, 'ASTM D92',
         'the range 240 ~ 260 °C (ASTM D 92)',
         'The typical value lies inside that range: logically compatible, which is not evidence of agreement (the kind of the SDS range '
         'is not stated; the SDS prints the method number only, the page also prints COC).', dict(flash_method='COC'))]:
    CHANGES.append(dict(
        product='S_OIL_ARAMCO_ULTRA_8', file=_file, path=_path, expect=dict(value=None, source='DL2-14611.pdf'),
        change_label='external technical source selected (manufacturer table, typical; edition date unknown); SDS range kept as alternate',
        new=dict(value=_val, qualifier=None, min=None, max=None, value_kind='typical', printed_text=f'{_row}: {_printed}', unit=_unit,
                 test_temperature_c=_temp, method=_method, source=dict(file=SOIL_URL, page=None, revision_date=None),
                 calculation_note=SOIL_NOTE.format(row=_row, astm=_astm, sds=_sds, rel=_rel), **_extra),
        old_kind=None,
        evidence=f"S-OIL page (saved copies, hashes verified): 'Typical Properties of aramcoULTRA Base Oil' | {_row} | {_astm} | aramcoULTRA 8: {_printed}"))

for _pid, _file, _src_file, _pg, _rev, _printed, _val, _rng in [
        ('NESTE_NEXBASE_3020', 'NESTE_NEXBASE_3020_tier1.json', 'DL2-14513.pdf', 5, '2020-06-16', 'Relative density 0,82 @ 15°C (ASTM D-4052).', 0.82, None),
        ('NESTE_NEXBASE_3043', 'NESTE_NEXBASE_3043_tier1.json', 'DL2-15010.pdf', 5, None, 'Relative density 0,82-0,84 @ 15°C (ASTM D-4052).', None, (0.82, 0.84)),
        ('NESTE_NEXBASE_3060', 'NESTE_NEXBASE_3060_tier1.json', 'DL2-12735.pdf', 4, '2017-10-17', 'Relative density 0,83-0,85 @ 15°C (ASTM D-4052)', None, (0.83, 0.85)),
        ('NESTE_NEXBASE_3080', 'NESTE_NEXBASE_3080_tier1.json', 'DL2-14512.pdf', 4, '2020-07-03', 'Relative density 0,84 @ 15°C (ASTM D-4052)', 0.84, None)]:
    CHANGES.append(dict(
        product=_pid, file=_file, path='specific_gravity', expect=dict(value=None, source=None), create_field=True,
        change_label='filled from the SDS (SDS fallback: no technical document prints it; field absent)',
        new=dict(value=_val, qualifier=None, min=_rng[0] if _rng else None, max=_rng[1] if _rng else None,
                 value_kind='range' if _rng else 'SDS reported', printed_text=_printed, unit='dimensionless', test_temperature_c=15,
                 method='ASTM D-4052', source=_src(_src_file, _pg, _rev),
                 calculation_note=REVIEW_NOTE + 'SDS section 9 "Relative density" (product name on p.1 is this NEXBASE grade). SDS fallback: '
                                                'the family TDS DL2-10962.pdf and the individual sheet print density, not specific gravity. '
                                                'The reference temperature of water is not printed.'),
        old_kind=None, evidence=f'{_src_file} p.{_pg} (text layer): "{_printed}"'))

# PETRONAS_ETRO_6 CCS is a list field: filled from the record's own TDS (DL2-12475.pdf, image, read on its render).
LIST_FILLS = [
    dict(product='PETRONAS_ETRO_6', file='PETRONAS_ETRO_6_tier1.json', path='ccs',
         new=[dict(value=v, qualifier=None, min=None, max=None, value_kind='typical', printed_text=f'CCS Viscosity (ASTM D5293, cP) at {t}°C: {p}',
                   unit='cP', test_temperature_c=t, method='ASTM D5293', status='Reported',
                   calculation_note=REVIEW_NOTE + 'ETRO 4 & ETRO 6 Technical Data Sheet, column "ETRO 6 / Typical value" (image, render read '
                                                  '2026-11-10). No specification is printed for CCS. 1 cP = 1 mPa·s.',
                   source=_src('DL2-12475.pdf', 1)) for v, t, p in ((2088, -25, '2,088'), (3977, -30, '3,977'), (7422, -35, '7,422'))],
         evidence='DL2-12475.pdf p.1 (render): CCS Viscosity, ASTM D5293, cP: at -25°C 2,088; at -30°C 3,977; at -35°C 7,422 (ETRO 6 typical)'),
    dict(product='ARAMCO_LUBEREF_PRIMA_500', file='ARAMCO_LUBEREF_PRIMA_500__base_oil_tier1_blocking.json', path='ccs',
         change_label='filled from the supplier brochure (technical; was Missing)',
         new=[dict(value=v, qualifier=None, min=None, max=None, value_kind='typical', printed_text=f'Cranking Viscosity @ {t}°C, mPa-s (D 5293): {p}',
                   unit='mPa.s', test_temperature_c=t, method='ASTM D5293', status='Reported',
                   calculation_note=REVIEW_NOTE + 'aramcoPRIMA brochure, Group II "Typical" table, column "aramcoPRIMA 500" (image, render read '
                                                  '2026-11-10; this column carries no "subject to confirmation" mark). The specification '
                                                  'DL2-12172.pdf cited by the record prints no CCS row.',
                   source=_src('DL2-11773.pdf', 1)) for v, t, p in ((14550, -20, '14,550'), (26000, -25, '26,000'))],
         evidence='DL2-11773.pdf p.1 (render): Cranking Viscosity @ -20°C, mPa-s 14,550; @ -25°C 26,000 (aramcoPRIMA 500, Typical)'),
]

# Qualifier corrections confirmed on the source page (not only on the record's notes).
QUALIFIER_FIXES = [
    dict(product='ERGON_HYGOLD_5000BS', file='ERGON_HYGOLD_5000BS_tier1.json', path='viscosity_index', expect=dict(value=81, qualifier='minimum', min=80),
         new_qualifier=None,
         note='Corrected 2026-11-10: DL2-10409.pdf p.1 (render) prints Viscosity Index with specification MIN 80 and TYPICAL VALUES 81; the '
              'qualifier "minimum" belonged to the specification (kept in min), not to the typical value 81.'),
    dict(product='ERGON_HYGOLD_P70N', file='ERGON_HYGOLD_P70N_tier1.json', path='viscosity_index', expect=dict(value=81, qualifier='minimum', min=60),
         new_qualifier=None,
         note='Corrected 2026-11-10: DL2-13346.pdf p.1 (render) prints Viscosity Index with specification MIN 60 and TYPICAL VALUES 81; the '
              'qualifier "minimum" belonged to the specification (kept in min), not to the typical value 81.'),
]

PRIMA230_SHEET = ('https://www.aramco.com/-/media/downloads/creating-value/base-oils/aramcoprima/aramcoprima_2021_december/'
                  'aramcoprima-230_yanbu_ar.pdf?hash=35009BCB03F8661F4C2220E5BC82ED39EAFE713F&la=ar')
# Disagreements found in the evidence review, recorded as conflicts (both values, both sources; not resolved).
PRIMA_NOTE = ('Found in the evidence review of 2026-11-10. The record cites the Luberef GII specification DL2-12172.pdf (typical density at '
              '15 °C printed without a unit); the aramcoPRIMA brochure DL2-11773.pdf (image, render read) prints a different typical density '
              'in Kg/L at 15 °C and marks the 110 and 230 typicals "subject to confirmation upon startup of the new Group II plant". Both '
              'technical documents are undated; not resolved; the field is pending.')
CONFLICT_ADDS = [
    *[(pid, f'{pid}__base_oil_tier1_blocking.json', dict(
        id=f'EVR-2026-11-10-{pid.rsplit("_", 1)[1]}-density', field='density', conflict_type='technical document vs technical document (undated)',
        values=[dict(file='DL2-12172.pdf', page=1, value=f'Density @ 15 °C, Typical: {spec} (no unit printed)'),
                dict(file='DL2-11773.pdf', page=1, value=f'Density @ 15°C, Kg/L, Typical: {bro}{star}')],
        resolved=False, note=PRIMA_NOTE))
      for pid, spec, bro, star in (('ARAMCO_LUBEREF_PRIMA_110', '0.8500', '0.8510', ' (column marked * "subject to confirmation")'),
                                   ('ARAMCO_LUBEREF_PRIMA_230', '0.8630', '0.8625', ' (column marked * "subject to confirmation")'),
                                   ('ARAMCO_LUBEREF_PRIMA_500', '0.867', '0.8720', ''))],
    ('PETRONAS_ETRO_4', 'PETRONAS_ETRO_4_tier1.json', dict(
        id='EVR-2026-11-10-ETRO4', field='kv100, viscosity_index, ccs', conflict_type='technical document vs technical document (undated editions)',
        values=[dict(file='DL2-10230.pdf', page=1, value='KV100 4.22 mm²/s; VI 129; CCS 810 / 1,390 / 2,500 mPa·s at -25 / -30 / -35 °C (typical)'),
                dict(file='DL2-12475.pdf', page=1, value='KV100 4.26 mm²/s; VI 130; CCS 886 / 1,442 / 2,419 cP at -25 / -30 / -35 °C (ETRO 4 typical; image, render read)')],
        resolved=False, note='Found in the evidence review of 2026-11-10. Both technical documents are undated; no edition rule applies. The record keeps '
                             'the DL2-10230.pdf values; the fields are pending (source_selection.PENDING_FIELDS).')),
    ('LUBRIZOL_CV2301', 'tier2_numeric_contribution.json', dict(
        id='EVR-2026-11-10-CV2301', field='flash_point', conflict_type='internal inconsistency of the technical document',
        values=[dict(file='DL2-13065.pdf', page=2, value='FLASH POINT, C, PMCC 158 (Physical Characteristics, Target)'),
                dict(file='DL2-13065.pdf', page=3, value='Flash Point (method) 165oC PMCC (handling instructions page)'),
                dict(file='DL2-13713.pdf', page=5, value='Flash Point 316 °F (158 °C) (Pensky-Martens Closed Cup) (SDS)')],
        resolved=False, note='Found in the evidence review of 2026-11-10. The same technical document prints 158 and 165 °C PMCC; the SDS prints '
                             '158 °C. Not resolved; the field is pending (internally inconsistent technical document).')),
    # found in the external-source review of 2026-11-11 (external_review_decisions.json)
    ('ARAMCO_LUBEREF_PRIMA_230', 'ARAMCO_LUBEREF_PRIMA_230__base_oil_tier1_blocking.json', dict(
        id='EVR-2026-11-11-230-density-external', field='density', conflict_type='technical document vs technical document',
        values=[dict(file='DL2-12172.pdf', page=1, value='Density @ 15 °C, Typical: 0.8630 (no unit printed)'),
                dict(file=PRIMA230_SHEET, page=1, value='Density @ 15 °C | kg/L | D 4052 | 0.8635')],
        resolved=False, note='Found in the external-source review of 2026-11-11 (Aramco sheet, bytes equal to the source_registry.json SHA-256). '
                             'A third value beside conflict EVR-2026-11-10-230-density (brochure DL2-11773.pdf 0.8625, provisional). '
                             'Not resolved; the field stays pending.')),
    ('ARAMCO_LUBEREF_PRIMA_230', 'ARAMCO_LUBEREF_PRIMA_230__base_oil_tier2_verification.json', dict(
        id='EVR-2026-11-11-230-noack', field='noack_volatility', conflict_type='technical document vs technical document (typical outside the specification limit)',
        values=[dict(file='DL2-12172.pdf', page=1, value='Noack, ASTM D5800-B: 7 (maximum)'),
                dict(file=PRIMA230_SHEET, page=1, value='Noack Volatility (Procedure B) | wt% | D 5800 | 7.5')],
        resolved=False, note='Found in the external-source review of 2026-11-11. The typical 7.5 printed by the Aramco sheet lies above the maximum 7 '
                             'printed by the specification DL2-12172.pdf: logically incompatible. Not resolved; the selected value is unchanged.')),
]


def apply_evidence_corrections(prods, integ):
    """Apply LIST_FILLS, QUALIFIER_FIXES and CONFLICT_ADDS (idempotent; each checks the expected current state)."""
    errors, log, changed = [], [], set()
    for c in LIST_FILLS:
        f, d = find_file(prods, c['product'], c['file'])
        cur = d['fields'].get(c['path'])
        if isinstance(cur, list) and [x.get('value') for x in cur] == [x['value'] for x in c['new']]:
            continue
        if not (isinstance(cur, list) and all(x.get('status') == 'Missing' and x.get('value') is None for x in cur)):
            errors.append(f"{c['product']} {c['path']}: expected an all-Missing list"); continue
        new = []
        for x in c['new']:
            x = copy.deepcopy(x)
            flags = integ.normalise(x, c['path'])
            if flags:
                x['integration_flags'] = flags
            new.append(x)
        d['fields'][c['path']] = new
        changed.add(f)
        log.append(dict(product=c['product'], file=c['file'], field=c['path'], before_value='Missing', before_source='',
                        after_value='; '.join(f"{x['value']} at {x['test_temperature_c']} °C" for x in c['new']), after_unit='cP',
                        after_source=c['new'][0]['source']['file'], after_page=c['new'][0]['source']['page'],
                        change=c.get('change_label', "filled from the record's own technical document (was Missing)"), evidence=c['evidence']))
    for c in QUALIFIER_FIXES:
        f, d = find_file(prods, c['product'], c['file'])
        n = d['fields'].get(c['path']) or {}
        if n.get('qualifier') == c['new_qualifier'] and n.get('qualifier_previous') == c['expect']['qualifier']:
            continue
        if {k: n.get(k) for k in c['expect']} != c['expect']:
            errors.append(f"{c['product']} {c['path']}: expected {c['expect']}"); continue
        n['qualifier_previous'] = n.get('qualifier')
        n['qualifier'] = c['new_qualifier']
        n['notes'] = ((n.get('notes') or '') + ' ' + c['note']).strip()
        changed.add(f)
        log.append(dict(product=c['product'], file=c['file'], field=c['path'] + '.qualifier', before_value=c['expect']['qualifier'],
                        before_source=(n.get('source') or {}).get('file'), after_value='null', after_unit='', after_source=(n.get('source') or {}).get('file'),
                        after_page=(n.get('source') or {}).get('page'), change='qualifier corrected against the source page', evidence=c['note']))
    for pid, name, conflict in CONFLICT_ADDS:
        f, d = find_file(prods, pid, name)
        if any(isinstance(x, dict) and x.get('id') == conflict['id'] for x in d.get('conflicts') or []):
            continue
        d.setdefault('conflicts', []).append(copy.deepcopy(conflict))
        changed.add(f)
        log.append(dict(product=pid, file=name, field=conflict['field'], before_value='', before_source='', after_value='conflict recorded',
                        after_unit='', after_source='; '.join(v['file'] for v in conflict['values']), after_page='',
                        change='disagreement recorded in conflicts[] (not resolved)', evidence=conflict['note']))
    return changed, errors, log


# conflict entries whose recorded resolution changes with the policy: (product, file, conflict field, new final_resolution)
CONFLICT_UPDATES = [
    ('RICHFUL_RF6077', 'tier2_numeric_contribution.json', 'tier2.density',
     'Superseded 2026-11-10: the source-selection policy (TDS value first, SDS fallback) selects the TDS value 998 kg/m³ at 20 °C; '
     'the documents still disagree (SDS 0.991 g/cm³ at 15 °C), so the conflict is not resolved. Earlier annotation: User decision of '
     '2026-10-18 kept (SDS value).'),
    ('RICHFUL_RF6077', 'tier2_numeric_contribution.json', 'tier2.kv100',
     'Superseded 2026-11-10: the source-selection policy (TDS value first, SDS fallback) selects the TDS value 160 mm²/s; the documents '
     'still disagree (SDS 150 mm²/s), so the conflict is not resolved. Earlier annotation: User decision of 2026-10-18 kept (SDS value).'),
    ('RICHFUL_RF6088F', 'tier2_numeric_contribution.json', 'tier2.kv100',
     'Superseded 2026-11-10: the source-selection policy (TDS value first, SDS fallback) selects the TDS value 177 mm²/s; the documents '
     'still disagree (SDS 178.2 mm²/s), so the conflict is not resolved. Earlier annotation: User decision of 2026-10-18 kept (SDS value).'),
]
NOTE_APPENDS = [  # (product, file, conflict field, text appended to the conflict note)
    ('S_OIL_ARAMCO_ULTRA_8', 'S_OIL_ARAMCO_ULTRA_8_tier1.json', 'tier1.kv40',
     ' [2026-11-11 source-selection policy: the field now holds the S-OIL table typical 41.10 cSt (technical source first; edition date '
     'of the page unknown); the SDS range 42.0 - 55.0 cSt is kept as an alternate entry. The typical lies below the SDS range, so the '
     'documents still disagree. Not resolved.]'),
    ('INFINEUM_D3424', 'tier2_numeric_contribution.json', 'tier2.flash_point',
     ' [2026-11-10 source-selection policy: the field now holds the TDS typical 190 °C (p.1); the SDS ">110C" lower bound is kept as an '
     'alternate entry. The two values are compatible (190 > 110) and remain recorded.]'),
    ('RICHFUL_RF6077', 'tier2_numeric_contribution.json', 'tier2.density',
     ' [2026-11-10: the user decision of 2026-10-18 is superseded by the source-selection policy; the field holds the TDS value. Not resolved.]'),
    ('RICHFUL_RF6077', 'tier2_numeric_contribution.json', 'tier2.kv100',
     ' [2026-11-10: the user decision of 2026-10-18 is superseded by the source-selection policy; the field holds the TDS value. Not resolved.]'),
    ('RICHFUL_RF6088F', 'tier2_numeric_contribution.json', 'tier2.kv100',
     ' [2026-11-10: the user decision of 2026-10-18 is superseded by the source-selection policy; the field holds the TDS value. Not resolved.]'),
]
OPEN_QUESTION_UPDATES = [  # (product, file, text of the open question to annotate, appended text)
    ('NESTE_NEXBASE_3020', 'NESTE_NEXBASE_3020_tier1.json', 'No product TDS supplied for NEXBASE 3020; only two matching SDS files.',
     ' [Corrected 2026-11-10: the NEXBASE family TDS DL2-10962.pdf (Edition 8, image) has a "Nexbase 3020" column; KV40, KV100 and density '
     'are now taken from it. VI is printed as "–" for 3020 and stays Missing.]'),
    ('NESTE_NEXBASE_3020', 'NESTE_NEXBASE_3020_tier1.json', 'API group, KV100, VI, mass density, sulfur and other absent properties remain missing.',
     ' [2026-11-10: KV100 (2.2 mm²/s) and density (834 kg/m³ at 15 °C) are now Reported from DL2-10962.pdf; API group, VI and sulfur remain '
     'Missing.]'),
]


def apply_open_questions(prods):
    """Append the dated corrections to the listed open questions (idempotent); return the changed files."""
    changed = set()
    for pid, name, q, text in OPEN_QUESTION_UPDATES:
        for fname in [x for x in prods[pid]['files'] if x.rsplit('/', 1)[1].startswith(pid)]:
            d = prods[pid]['files'][fname]
            for i, item in enumerate(d.get('open_questions') or []):
                if item == q:
                    d['open_questions'][i] = q + text
                    changed.add(fname)
    return changed

PRODUCT_UPDATES = [  # (product, file prefix, key, expected current value, new value): product-block provenance of new sources
    ('NESTE_NEXBASE_3020', 'NESTE_NEXBASE_3020_tier', 'source_file', ['DL2-14513.pdf', 'DL2-14514.pdf'],
     ['DL2-14513.pdf', 'DL2-14514.pdf', 'DL2-10962.pdf']),
    ('NESTE_NEXBASE_3020', 'NESTE_NEXBASE_3020_tier', 'document_type', 'Safety Data Sheet', 'Safety Data Sheet; Technical Data Sheet'),
]


def apply_product_updates(prods):
    """Record a newly cited document in the product block (idempotent; revision_date is left as the SDS date)."""
    changed = set()
    for pid, prefix, key, old, new in PRODUCT_UPDATES:
        for fname in [x for x in prods[pid]['files'] if x.rsplit('/', 1)[1].startswith(prefix)]:
            prod = prods[pid]['files'][fname]['product']
            if prod.get(key) == old:
                prod[key] = new
                changed.add(fname)
            elif prod.get(key) != new:
                raise SystemExit(f'{fname}: product.{key} is {prod.get(key)!r}, expected {old!r} or {new!r}')
    return changed

# ---------------------------------------------------------------- reviewed non-changes (documented for the report)
EXCEPTIONS = [  # TDS value exists but is not selected; reason recorded
    ('PETRONAS_ETRO_6_PLUS', 'density', 'TDS DL2-10234.pdf p.1 prints "Density ASTM D 1298/D 4052 kg/L 0.8429" with no reference temperature; '
     'the property definition requires one (Tier 1: density + reference temperature). The SDS value 0.8486 g/cm³ at 15 °C stays selected; '
     'the TDS value stays in conflicts[] (audit CF-036). Exception type: TDS value lacks a required condition.'),
    ('AFTON_HITEC_12210M', 'density', 'The bulletin DL2-15568.pdf p.2 prints "Density, lbs/gal. 7.90" with no temperature; the SDS value '
     '0.95 g/cm³ at 15 °C stays selected. Exception type: TDS value lacks a required condition.'),
]
PENDING = [  # needs a decision outside this rule
    ('RICHFUL_RF6066', 'density, kv100, tbn, elements.Zn, elements.Ca', 'Two undated TDS (DL2-13819.pdf, DL2-15451.pdf) print different values; no edition rule applies (TDS-TDS conflict). Fields keep their current values.'),
    ('RICHFUL_RF6069', 'kv100', 'Field holds 142 mm²/s from the supplier web page (2026-10-17); the archived undated TDS DL2-15618.pdf prints 118. Web page vs archived TDS edition; kept as is, for review.'),
    ('AFTON_HITEC_8788B', 'kv40, kv100, density, flash_point', 'The record cites an archived external Afton PDS (Internet Archive) for a base-oil claim; whether it prints these values is unknown: no copy could be obtained on 2026-11-11 (external_review.csv). If it prints them, Rule 1 would prefer them to the SDS values selected now.'),
    ('NESTE_NEXBASE_3043 to 3080', 'several', 'The NEXBASE family TDS DL2-10962.pdf (Edition 8) and the individual sheets (e.g. DL2-10037.pdf, edition 5.2) print different typical values for the same grades (TDS-TDS editions; not dated); not changed.'),
]
# Field-level form of the pending cases (used by the coverage ledger and the eligibility build). The NEXBASE fields
# are those where the family TDS DL2-10962.pdf (Edition 8, read on its render 2026-11-10) and the individual sheet the
# record cites print different values; fields where the two agree are not pending.
NEX_WHY = ('Family TDS DL2-10962.pdf (Edition 8, undated) and the individual sheet cited by the record (undated) print different '
           'values for this field: conflicting technical editions; no edition rule applies.')
PENDING_FIELDS = [
    ('NESTE_NEXBASE_3043', 'density', NEX_WHY + ' (831 vs 837 kg/m³ at 15 °C)'),
    ('NESTE_NEXBASE_3043', 'flash_point', NEX_WHY + ' (224 vs 228 °C)'),
    ('NESTE_NEXBASE_3043', 'noack_volatility', NEX_WHY + ' (14.4 vs 14.2 w-%)'),
    ('NESTE_NEXBASE_3050', 'density', NEX_WHY + ' (835 vs 839 kg/m³ at 15 °C)'),
    ('NESTE_NEXBASE_3050', 'pour_point', NEX_WHY + ' (-15 vs -18 °C)'),
    ('NESTE_NEXBASE_3060', 'kv40', NEX_WHY + ' (33 vs 32 mm²/s)'),
    ('NESTE_NEXBASE_3060', 'kv100', NEX_WHY + ' (6.0 vs 5.9 mm²/s)'),
    ('NESTE_NEXBASE_3060', 'density', NEX_WHY + ' (838 vs 843 kg/m³ at 15 °C)'),
    ('NESTE_NEXBASE_3060', 'noack_volatility', NEX_WHY + ' (5.7 vs 7.2 w-%)'),
    ('NESTE_NEXBASE_3080', 'kv40', NEX_WHY + ' (50 vs 49 mm²/s)'),
    ('NESTE_NEXBASE_3080', 'kv100', NEX_WHY + ' (8 vs 7.9 mm²/s)'),
    ('NESTE_NEXBASE_3080', 'viscosity_index', NEX_WHY + ' (128 vs 130)'),
    ('NESTE_NEXBASE_3080', 'density', NEX_WHY + ' (843 vs 847 kg/m³ at 15 °C)'),
    ('NESTE_NEXBASE_3080', 'flash_point', NEX_WHY + ' (260 vs 261 °C)'),
    ('NESTE_NEXBASE_3080', 'pour_point', NEX_WHY + ' (-15 vs -12 °C)'),
]

# Field-level SDS fallbacks reviewed against the technical document (used by the coverage ledger).
PENDING_FIELDS += [
    *[(pid, 'density', 'Spec DL2-12172.pdf (no unit printed) and brochure DL2-11773.pdf (Kg/L at 15 °C) print different typical densities; both '
                       'undated; the brochure marks 110/230 typicals as provisional (conflict EVR-2026-11-10-...-density).')
      for pid in ('ARAMCO_LUBEREF_PRIMA_110', 'ARAMCO_LUBEREF_PRIMA_230', 'ARAMCO_LUBEREF_PRIMA_500')],
    ('PETRONAS_ETRO_4', 'kv100', 'Technical documents DL2-10230.pdf (4.22) and DL2-12475.pdf (4.26) disagree; both undated (conflict EVR-2026-11-10-ETRO4).'),
    ('PETRONAS_ETRO_4', 'viscosity_index', 'Technical documents DL2-10230.pdf (129) and DL2-12475.pdf (130) disagree; both undated (conflict EVR-2026-11-10-ETRO4).'),
    ('PETRONAS_ETRO_4', 'ccs', 'Technical documents DL2-10230.pdf (810/1,390/2,500) and DL2-12475.pdf (886/1,442/2,419) disagree; both undated (conflict EVR-2026-11-10-ETRO4).'),
    ('LUBRIZOL_CV2301', 'flash_point', 'The technical document DL2-13065.pdf prints 158 °C (p.2) and 165 °C (p.3) PMCC (conflict EVR-2026-11-10-CV2301).'),
    ('FORMOSA_150N_GII_PLUS', 'kv40', 'SDS fallback source DL2-10011.pdf names "150N Base oil" without the grade "GII+"; Formosa supplies 150N as GII (FPCC table '
                                      'DL2-12108.jpeg) and GII+ (DL2-10001.pdf); the SDS cannot be tied to this exact product (identity).'),
    ('FORMOSA_150N_GII_PLUS', 'specific_gravity', 'Same identity question as kv40: SDS DL2-10011.pdf names "150N Base oil" without "GII+".'),
    ('FORMOSA_500N_GII', 'kv40', 'SDS fallback source DL2-10017.pdf names "500N Base oil" without the grade "GII"; its applicability to this exact '
                                 'product is not stated (identity).'),
    ('FORMOSA_500N_GII', 'specific_gravity', 'Same identity question as kv40: SDS DL2-10017.pdf names "500N Base oil" without "GII".'),
]

SDS_FALLBACK_FIELDS = [
    ('NESTE_NEXBASE_3020', 'specific_gravity', 'Family TDS DL2-10962.pdf (image, read on its render 2026-11-10) prints density at 15 °C but no '
                                               'specific gravity; SDS DL2-14513.pdf value used.'),
    ('INFINEUM_D3384', 'specific_gravity', 'Technical sheet DL2-10218.pdf p.1 (image, read on its render 2026-11-10) prints density at 15 °C and in '
                                           'lb/USG but no specific gravity; SDS value kept.'),
]

SDS_FALLBACK_CONFIRMED = ('No technical document in the archive provides the property for these SDS-selected values (checked with '
                          'tds_candidates.py and a text search of the archive): AFTON_HITEC_12010, AFTON_HITEC_8712, AFTON_HITEC_8799B, '
                          'CHEVRON_N204, CHEVRON_N216, CHEVRON_OLOA_59766 and RICHFUL_RF6089 (SDS-only packages); PETRONAS_EQUINAS_4 and _6 '
                          '(SDS only; DL2-15279.pdf is EQUINAS 8); specific gravity where the TDS prints a density but no specific gravity '
                          '(INFINEUM_D3384, INFINEUM_D3451, AFTON_HITEC_12200, SHELL_RISELLA_X_415/420, PETRONAS_ETRO_6_PLUS; FORMOSA moved to PENDING_FIELDS '
                          'on 2026-11-10: SDS identity); '
                          'CAS chemical names from SDS section 3 where the technical document prints no chemistry; component carrier '
                          'and active-content shares (LUBRIZOL_CV6320, RF6602).')


def integrate_module():
    spec = importlib.util.spec_from_file_location('integrate_products', os.path.join(P.ROOT, 'integrate_products.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def find_file(prods, pid, name):
    for f, d in prods[pid]['files'].items():
        if f.rsplit('/', 1)[1] == name:
            return f, d
    raise KeyError(f'{pid}/{name}')


def is_applied(node, c):
    """The declared new selection is already in the field (value, min, max and source file)."""
    return (node.get('value') == c['new']['value'] and node.get('min') == c['new'].get('min', node.get('min'))
            and node.get('max') == c['new'].get('max', node.get('max'))
            and (node.get('source') or {}).get('file') == c['new']['source']['file'])


def change_log():
    """One row per declared change, from the declarations (before = the declared expectation, after = the new value)."""
    return [dict(product=c['product'], file=c['file'], field=c['path'], before_value=c['expect']['value'], before_source=c['expect']['source'],
                 after_value=c['new']['value'] if c['new']['value'] is not None else f"{c['new'].get('min')}-{c['new'].get('max')} (range)",
                 after_unit=c['new'].get('unit'), after_source=c['new']['source']['file'], after_page=c['new']['source']['page'],
                 change=(c['change_label'] if c.get('change_label') else 'filled from TDS (was Missing)' if c['expect']['value'] is None else
                         'technical specification range selected; SDS typical kept as alternate' if c['new']['value'] is None else
                         'source switched to TDS, same value' if c['expect']['value'] == c['new']['value'] else
                         'TDS value selected (differs from previous)'),
                 evidence=c['evidence']) for c in CHANGES] + [
        dict(product=c['product'], file=c['file'], field=c['path'], before_value='Missing', before_source='',
             after_value='; '.join(f"{x['value']} at {x['test_temperature_c']} °C" for x in c['new']), after_unit=c['new'][0]['unit'],
             after_source=c['new'][0]['source']['file'], after_page=c['new'][0]['source']['page'],
             change=c.get('change_label', "filled from the record's own technical document (was Missing)"), evidence=c['evidence']) for c in LIST_FILLS] + [
        dict(product=c['product'], file=c['file'], field=c['path'] + '.qualifier', before_value=c['expect']['qualifier'], before_source='',
             after_value='null', after_unit='', after_source='', after_page='', change='qualifier corrected against the source page',
             evidence=c['note']) for c in QUALIFIER_FIXES] + [
        dict(product=pid, file=name, field=cf['field'], before_value='', before_source='', after_value='conflict recorded', after_unit='',
             after_source='; '.join(v['file'] for v in cf['values']), after_page='', change='disagreement recorded in conflicts[] (not resolved)',
             evidence=cf['note']) for pid, name, cf in CONFLICT_ADDS]


def apply(prods, integ):
    """Apply every declared change to the in-memory documents; return (changed relpaths, errors, log rows)."""
    errors, log, changed = [], [], set()
    for c in CHANGES:
        f, d = find_file(prods, c['product'], c['file'])
        node = d['fields'].get(c['path'])
        if node is None and c.get('create_field'):
            # the record lacks this optional template field; it is created in the template's value-object shape
            node = dict(value=None, qualifier=None, min=None, max=None, value_kind=None, printed_text=None, unit=None,
                        test_temperature_c=None, method=None, status='Missing', calculation_note=None,
                        source=dict(file=None, page=None, revision_date=None))
        if node is None:
            errors.append(f"{c['product']} {c['path']}: field not found"); continue
        now = dict(value=node.get('value'), source=(node.get('source') or {}).get('file'))
        if is_applied(node, c):
            continue
        if now != c['expect']:
            errors.append(f"{c['product']} {c['path']}: expected {c['expect']}, found {now}"); continue
        old = {k: copy.deepcopy(v) for k, v in node.items() if k not in P.OWN_KEYS and k != 'alternate_entries'}
        alts = copy.deepcopy(node.get('alternate_entries') or [])
        if old.get('status') not in (None, 'Missing'):
            if c.get('old_kind'):
                old['value_kind_previous_label'] = old.get('value_kind')
                old['value_kind'], kind_note = c['old_kind']
                old['notes'] = ((old.get('notes') or '') + ' ' + kind_note).strip()
            old.update(copy.deepcopy(c.get('old_override') or {}))
            old['selection_note'] = ALT_NOTE
            alts.append(old)
        for extra in c.get('add_alternates') or []:  # reviewed values of the other document class, kept with provenance
            if not any(a.get('source') == extra['source'] and a.get('value') == extra.get('value') for a in alts):
                alts.append(copy.deepcopy(extra))
        keep_extra = {k: v for k, v in node.items() if k not in P.OWN_KEYS and k not in c['new'] and k not in
                      ('alternate_entries', 'notes', 'calculation_note', 'status', 'source', 'flash_method', 'value_kind_previous_label')}
        new = dict(keep_extra)
        new.update(copy.deepcopy(c['new']))
        new['status'] = 'Reported'
        new['notes'] = SEL_NOTE
        if alts:
            new['alternate_entries'] = alts
        order = ['value', 'qualifier', 'min', 'max', 'value_kind', 'printed_text', 'unit', 'test_temperature_c', 'method', 'status',
                 'calculation_note', 'source', 'flash_method', 'notes', 'alternate_entries']
        rebuilt = {k: new[k] for k in order if k in new}
        rebuilt.update({k: v for k, v in new.items() if k not in rebuilt})
        flags = integ.normalise(rebuilt, c['path'])
        if flags:
            rebuilt['integration_flags'] = flags
        ann = integ.ANNOTATIONS.get((c['product'], d.get('tier'), c['path']))
        if ann:
            rebuilt['resolution'] = ann['resolution']
        d['fields'][c['path']] = rebuilt
        changed.add(f)
        log.append(dict(product=c['product'], file=f, field=c['path'], before_value=c['expect']['value'], before_source=c['expect']['source'],
                        after_value=c['new']['value'], after_unit=c['new'].get('unit'), after_source=c['new']['source']['file'],
                        after_page=c['new']['source']['page'], change=('filled from TDS (was Missing)' if c['expect']['value'] is None else
                                                                      'source switched to TDS, same value' if c['expect']['value'] == c['new']['value'] else
                                                                      'TDS value selected (differs from previous)'),
                        evidence=c['evidence']))
    for pid, name, fld, text in CONFLICT_UPDATES:
        f, d = find_file(prods, pid, name)
        hit = [x for x in d.get('conflicts', []) if isinstance(x, dict) and x.get('field') == fld]
        if len(hit) != 1:
            errors.append(f'{pid} conflict {fld}: {len(hit)} entries'); continue
        if hit[0].get('resolved') is not False or hit[0].get('final_resolution') != text:
            hit[0]['resolved'] = False
            hit[0]['final_resolution'] = text
            changed.add(f)
    for pid, name, fld, text in NOTE_APPENDS:
        f, d = find_file(prods, pid, name)
        hit = [x for x in d.get('conflicts', []) if isinstance(x, dict) and (x.get('field') == fld or x.get('property') == fld)]
        if len(hit) != 1:
            errors.append(f'{pid} conflict note {fld}: {len(hit)} entries'); continue
        if text.strip() not in hit[0].get('note', ''):
            hit[0]['note'] = hit[0].get('note', '') + text
            changed.add(f)
    changed |= apply_open_questions(prods) | apply_product_updates(prods)
    c2, e2, l2 = apply_evidence_corrections(prods, integ)
    changed |= c2
    errors += e2
    log += l2
    return sorted(changed), errors, log


def write_json(relpath, d):
    p = P.lp(os.path.join(P.ROOT, relpath))
    raw = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    tail = '\n' if raw.endswith(('\n', '\r\n')) else ''
    new = (json.dumps(d, indent=2, ensure_ascii='\\u' in raw) + tail).replace('\n', nl)
    with open(p, 'w', encoding='utf-8', newline='') as fh:
        fh.write(new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    prods = P.load_products()
    todo = [c for c in CHANGES if not is_applied(find_file(prods, c['product'], c['file'])[1]['fields'].get(c['path']) or {}, c)]
    integ = integrate_module()
    changed, errors, log = apply(prods, integ)   # skips declared changes that are already applied
    # keep the reviewed resolution notes of integrate_products.ANNOTATIONS on the selected fields (idempotent)
    for c in CHANGES:
        f, d = find_file(prods, c['product'], c['file'])
        ann = integ.ANNOTATIONS.get((c['product'], d.get('tier'), c['path']))
        if ann and d['fields'][c['path']].get('resolution') != ann['resolution']:
            d['fields'][c['path']]['resolution'] = ann['resolution']
            changed = sorted(set(changed) | {f})
    print(f'{len(CHANGES)} declared selections; {len(CHANGES) - len(todo)} already in the data; {len(todo)} to apply; '
          f'files to write (selections, notes, open questions, product blocks): {len(changed)}')
    for e in errors:
        print('ERROR', e)
    if errors:
        print('nothing written'); return 1
    if a.report or a.write:
        out = os.path.join(P.REPORTS, 'data_policy', 'source_selection_changes.csv')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        rows = change_log()
        with open(out, 'w', encoding='utf-8', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
    if a.write and changed:
        for f in changed:
            write_json(f, find_doc(prods, f))
        print(f'WRITTEN: {len(changed)} files')
    elif changed:
        print('DRY RUN: nothing written (use --write)')
    return 0


def find_doc(prods, relpath):
    pid = relpath.rsplit('/', 2)[1]
    return prods[pid]['files'][relpath]


if __name__ == '__main__':
    sys.exit(main())
