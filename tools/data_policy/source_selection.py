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
    ('S_OIL_ARAMCO_ULTRA_8', 'kv40, kv100, flash_point', 'Only the SDS DL2-14611.pdf is in the archive (ranges); the S-OIL web table (external, typical) prints typical values. External technical page vs archived SDS; kept as is, for review.'),
    ('AFTON_HITEC_8788B', 'kv40, kv100, density, flash_point', 'The record cites an archived external Afton PDS (Internet Archive) for a base-oil claim; its numeric values have not been reviewed against the SDS values selected now.'),
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
SDS_FALLBACK_FIELDS = [
    ('FORMOSA_150N_GII_PLUS', 'kv40', 'Specification DL2-10001.pdf p.1 prints "Report" for KV40 (no value); SDS value kept.'),
    ('FORMOSA_150N_GII_PLUS', 'specific_gravity', 'Specification DL2-10001.pdf p.1 prints "Report" for specific gravity (no value); SDS value kept.'),
    ('FORMOSA_500N_GII', 'kv40', 'Specification DL2-10003.pdf p.1 prints "Report" for KV40 (no value); SDS value kept.'),
    ('FORMOSA_500N_GII', 'specific_gravity', 'Specification DL2-10003.pdf p.1 prints "Report" for specific gravity (no value); SDS value kept.'),
    ('INFINEUM_D3384', 'specific_gravity', 'Technical sheet DL2-10218.pdf p.1 (image, read on its render 2026-11-10) prints density at 15 °C and in '
                                           'lb/USG but no specific gravity; SDS value kept.'),
]

SDS_FALLBACK_CONFIRMED = ('No technical document in the archive provides the property for these SDS-selected values (checked with '
                          'tds_candidates.py and a text search of the archive): AFTON_HITEC_12010, AFTON_HITEC_8712, AFTON_HITEC_8799B, '
                          'CHEVRON_N204, CHEVRON_N216, CHEVRON_OLOA_59766 and RICHFUL_RF6089 (SDS-only packages); PETRONAS_EQUINAS_4 and _6 '
                          '(SDS only; DL2-15279.pdf is EQUINAS 8); specific gravity where the TDS prints a density but no specific gravity '
                          '(INFINEUM_D3384, INFINEUM_D3451, AFTON_HITEC_12200, SHELL_RISELLA_X_415/420, PETRONAS_ETRO_6_PLUS, FORMOSA); '
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
                 change=('filled from TDS (was Missing)' if c['expect']['value'] is None else
                         'technical specification range selected; SDS typical kept as alternate' if c['new']['value'] is None else
                         'source switched to TDS, same value' if c['expect']['value'] == c['new']['value'] else
                         'TDS value selected (differs from previous)'),
                 evidence=c['evidence']) for c in CHANGES]


def apply(prods, integ):
    """Apply every declared change to the in-memory documents; return (changed relpaths, errors, log rows)."""
    errors, log, changed = [], [], set()
    for c in CHANGES:
        f, d = find_file(prods, c['product'], c['file'])
        node = d['fields'].get(c['path'])
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
    todo = [c for c in CHANGES if not is_applied(find_file(prods, c['product'], c['file'])[1]['fields'][c['path']], c)]
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
