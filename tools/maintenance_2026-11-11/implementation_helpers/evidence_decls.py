
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

# Disagreements found in the evidence review, recorded as conflicts (both values, both sources; not resolved).
CONFLICT_ADDS = [
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
                        change='filled from the record\'s own technical document (was Missing)', evidence=c['evidence']))
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
