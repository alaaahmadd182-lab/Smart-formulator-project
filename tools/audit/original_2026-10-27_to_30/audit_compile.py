"""Compile the audit findings (documented + new) into one list. Read-only on the repository.
Writes audit/findings.json. Every value below was read from the JSON or the archive in this audit."""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.stdout.reconfigure(encoding='utf-8')
import audit_lib as A

P = A.load_products(); ar = A.Archive()
DOC = json.load(open(os.path.join(A.SCR, 'audit', 'documented.json'), encoding='utf-8'))
CAT = {
    'C01': 'Conflicting values for the same product',
    'C02': 'Contradiction between document types (TDS/PDS/SDS/COA/specification)',
    'C03': 'Edition or revision difference',
    'C04': 'Test method, temperature, unit or condition difference',
    'C05': 'Typical value vs specification, limit or range',
    'C06': 'Classification contradiction (API group, chemistry, function)',
    'C07': 'Inconsistency across JSON tiers',
    'C08': 'Reported without adequate source evidence',
    'C09': 'Status inconsistent with available evidence',
    'C10': 'Unsupported assumption, conversion or derived value',
    'C11': 'Original value vs normalised *_final value',
    'C13': 'Product identity, supplier or reference mismatch',
    'C14': 'Documentation omitted, incorrectly resolved or duplicated',
}
TEAMMATE = 'Rawan-Mohammad, PR #2 (53ed010, a38d5ca)'


def product(folder):
    p = P[folder]; pr = {}
    for t in p['tiers'].values():
        for k, v in (t['doc'].get('product') or {}).items():
            pr.setdefault(k, v) if v is not None else None
    return p, pr.get('product_name') or p['record_id'], pr.get('supplier') or p['supplier_folder']


def folder_of(rid):
    return next(f for f, p in P.items() if p['record_id'] == rid)


def oq(rid, pattern):
    """Verbatim open-question text (first match) for a product."""
    p = P[folder_of(rid)]
    for tk, t in p['tiers'].items():
        for q in t['doc'].get('open_questions', []):
            text = q if isinstance(q, str) else ' '.join(str(x) for x in q.values())
            if re.search(pattern, text, re.I): return tk, text
    return None, None


def field(rid, tier, path):
    p = P[folder_of(rid)]
    for tk, t in p['tiers'].items():
        if t['tier'] == tier:
            for pth, n, _ in A.value_objects(t['doc'].get('fields', {})):
                if pth == path: return t['file'], n
    return None, None


F = []


def add(**kw):
    kw.setdefault('teammate', 'No'); F.append(kw)


# ---------------------------------------------------------------- previously documented conflicts (125 unique)
VISUAL = {('RICHFUL_RF6066', 'DL2-15831.pdf'): 'p.5 checked visually: density 0.988 g/cm³ (20 °C), flash point ≥ 180 °C (open cup); the 185 mm²/s value is printed on the line "Viscosity, dynamic" although the unit is kinematic',
          ('RICHFUL_RF6069', 'DL2-15619.pdf'): 'p.5 checked visually: "Viscosity, kinematic 142 mm²/s (100 °C, ASTM D445)", density 981 kg/m³ (20 °C, ASTM D4052)',
          ('RICHFUL_RF6078', 'DL2-15833.pdf'): 'p.5 checked visually: density 975 kg/m³ (20 °C, ASTM D4052), kinematic viscosity 146 mm²/s (100 °C)',
          ('SHELL_RISELLA_X_430', 'DL2-13731.pdf'): 'p.7 checked visually (the text layer uses an encoded font): density 824.8 kg/m3 (15.0 °C), ISO 12185; relative density 0.8248 (15 °C)'}
RECONSIDER = {
    ('RICHFUL_RF6077', 'tier2.density'): 'Marked resolved by the user decision of 2026-10-18 (SDS 0.991 g/cm³ at 15 °C used). The TDS prints 998 kg/m³ at 20 °C. A lower value at the lower temperature cannot be explained by the temperature difference (density decreases as temperature rises), so the two documents genuinely disagree; the field choice can stand as a recorded decision, but the conflict itself should not read as explained.',
    ('RICHFUL_RF6088F', 'tier2.density'): 'Marked resolved by the user decision of 2026-10-18 (TDS 963 kg/m³ at 20 °C used). The SDS value is printed as "Relative density : 0.958 g/cm3@20℃": a relative density label with a density unit, so the two values may not be the same quantity. The comparison basis should be confirmed before the record is treated as resolved.',
}
SPECIAL = {
    ('NYNAS_NYFROST_32', 'kv40'): 'The SDS values are printed on p.7 of DL2-13444.pdf ("Kinematic (40°C): 0,31 cm2/s (31 cSt)", "Closed cup: >180°C [Pensky-Martens.]"); the conflict entry cites p.6. Page reference to be corrected.',
    ('NYNAS_NYFROST_32', 'flash_point'): 'The SDS values are printed on p.7 of DL2-13444.pdf ("Kinematic (40°C): 0,31 cm2/s (31 cSt)", "Closed cup: >180°C [Pensky-Martens.]"); the conflict entry cites p.6. Page reference to be corrected.',
    ('ERGON_HYGOLD_L750', 'density_at_15_6_c'): 'Additional evidence found in this audit: the uncited Ergon SDS DL2-10025.pdf p.6 prints "Relative density 0,92 (15,56 °C (60 °F) ASTM D 4052/ ISO 12185)", consistent with the TDS specific gravity 0.9183 and not with the TDS density 0.854 g/cm³.',
    ('RICHFUL_RF6078', 'tier1.treat_rate_matrix (ACEA E7/API CI-4)'): 'Checked against both PDFs in this audit: the recorded values and the note are correct (DL2-15832.pdf p.1 rows "ACEA E7/API CI-4 11.85%" and "API CI-4 10.85%"; RF6078 - TDS.pdf p.1 rows "ACEA E7/API CI-4 10.85%" and "API CI-4 Plus 11.85%"). The proposal text from PR #2 kept in final_resolution states that "the note text has the two files swapped"; that statement is incorrect.',
}


def doc_types(vals):
    return sorted({v['doc_type'] for v in vals if v.get('doc_type')})


for o in DOC:
    folder = o['folder']; p, name, sup = product(folder)
    prop = o['property']; ctype = o['conflict_type']; vals = o['values']
    types = doc_types(vals)
    assess = ' '.join(str(x) for x in (o.get('note'),) if x)
    if ctype == 'edition difference':
        cat, nature = 'C03', 'Edition difference (values changed between editions of supplier documents)'
    elif ctype == 'unit or test-condition discrepancy':
        cat, nature = 'C04', 'Difference in units or test conditions'
    elif ctype == 'inconsistency within one document':
        cat, nature = 'C01', 'Genuine contradiction within one supplier document'
    elif ctype is None:
        cat, nature = 'C02', 'Genuine contradiction between documents (untyped text record)'
    elif re.search(r'(?i)different methods|not directly comparable|threshold', assess):
        cat, nature = 'C04', 'Difference explainable by test method or bound type; both values kept'
    elif 'SDS' in types and len(types) > 1:
        cat, nature = 'C02', 'Genuine contradiction between document types'
    else:
        cat, nature = 'C01', 'Genuine contradiction between documents'
    checks = [v['source_check'] for v in vals]
    extra = []
    for v in vals:
        key = (o['record_id'], A.Archive.key(v.get('file') or '').replace(' ', '').upper().replace('PDF', 'pdf'))
        for (rid, fname), txt in VISUAL.items():
            if rid == o['record_id'] and v.get('file') and A.Archive.key(v['file']) == A.Archive.key(fname):
                v['source_check'] = 'verified visually'; extra.append(txt)
    checks = [v['source_check'] for v in vals]
    sp = SPECIAL.get((o['record_id'], prop))
    if sp and 'p.7' in sp:
        checks = ['verified on p.7 (cited p.6)' if 'NOT' in c else c for c in checks]
    if not vals:
        ver = 'Recorded as text; source page not machine-checked'
    elif all(c.startswith('verified') for c in checks):
        ver = 'Verified in source documents'
    elif any(c.startswith('external') for c in checks) and all(c.startswith(('verified', 'external')) for c in checks):
        ver = 'Archive value verified; external web value relies on source_registry.json verification (not re-fetched)'
    else:
        ver = 'Partially verified: ' + '; '.join(sorted(set(checks)))
    if o['resolved'] is True:
        res = 'Requires Review' if (o['record_id'], prop) in RECONSIDER else 'Resolved'
    else:
        res = 'Unresolved'
    expl = (o.get('note') or '') + ((' ' + ' '.join(extra)) if extra else '')
    if sp: expl += ' ' + sp
    if (o['record_id'], prop) in RECONSIDER: expl += ' RECONSIDER: ' + RECONSIDER[(o['record_id'], prop)]
    if o.get('final_resolution'): expl += ' final_resolution: ' + o['final_resolution']
    step = {'C03': 'Confirm with the supplier which edition is current; keep both editions documented.',
            'C04': 'Compare methods/conditions on both documents; keep both values with their conditions.',
            'C02': 'Ask the supplier which document is authoritative for this property; keep both values.',
            'C01': 'Confirm the correct value with the supplier; keep both values until then.'}[cat]
    if res == 'Resolved': step = 'None required; confirm the recorded basis (newer dated edition / recorded user decision) is still accepted.'
    if res == 'Requires Review': step = 'Re-examine the 2026-10-18 decision against the evidence noted; keep both values documented.'
    if sp and 'p.7' in sp: step = 'Correct the page reference (p.6 -> p.7) in the conflict entry; ' + step
    add(id=None, material_class=p['class'], supplier=sup, product=name, record_id=o['record_id'], property=prop, category=cat,
        nature=nature, values=[{k: v.get(k) for k in ('value', 'printed_text', 'unit', 'temperature_c', 'file', 'page', 'revision_date', 'doc_type', 'source_check', 'label')} for v in vals],
        json_paths=o['locations'], explanation=expl.strip(), verification=ver, resolution=res, next_step=step,
        provenance='Previously documented (JSON conflicts[] and open_questions_and_conflicts.md)',
        teammate=('Yes: PR #2 annotated this entry (resolved/final_resolution); decision reviewed in the 2026-10-24 reconciliation' if o['resolved'] is not None else 'No'),
        source_kind='documented')


def V(value, file=None, page=None, rev=None, printed=None, unit=None, cond=None, doc_type=None, check='verified in source text'):
    return dict(value=value, file=file, page=page, revision_date=rev, printed_text=printed, unit=unit, conditions=cond, doc_type=doc_type, source_check=check)


def new(rid, prop, cat, nature, values, expl, ver, res, step, prov='New (this audit)', teammate='No', paths=None):
    folder = folder_of(rid); p, name, sup = product(folder)
    add(id=None, material_class=p['class'], supplier=sup, product=name, record_id=rid, property=prop, category=cat, nature=nature,
        values=values, json_paths=paths or [t['file'] for t in p['tiers'].values()][:1], explanation=expl, verification=ver,
        resolution=res, next_step=step, provenance=prov, teammate=teammate, source_kind='new')


def jp(rid, tier, path):
    f, _ = field(rid, tier, path); return [f'{f}#fields.{path}'] if f else None


# ---------------------------------------------------------------- new: Chevron Phillips Synfluid TDS vs SDS flash points
for rid, tds, tdsrev, tval, sds, sdsrev, sval, meth in [
        ('CHEVRON_SYNFLUID_MPAO_100', 'DL2-11912.pdf', 'April 2013', 265, 'DL2-11906.PDF; DL2-14992.pdf', '2017-07-10 (version 2.0, both)', 255, 'TDS "Flash Point (COC)"; SDS p.3/p.4 "Flash point : 255 °C (491 °F)" (no method on that line)'),
        ('CHEVRON_SYNFLUID_MPAO_150', 'DL2-11913.pdf', 'November 2013', 278, 'DL2-11909.PDF', '2017-07-10 (version 2.0)', 250, 'TDS "Flash Point (COC)"; SDS p.3/p.4 "Method: ASTM D-92"'),
        ('CHEVRON_SYNFLUID_PAO_4', 'DL2-11914.pdf', 'April 2011', 226, 'DL2-11904.PDF', '2018-08-03 (version 3.4)', 219, 'both Cleveland Open Cup'),
        ('CHEVRON_SYNFLUID_PAO_6', 'DL2-11915.pdf', 'April 2011', 245, 'DL2-11907.pdf', '2016-03-07 (version 1.8)', 238, 'both Cleveland Open Cup'),
        ('CHEVRON_SYNFLUID_PAO_8', 'DL2-11916.pdf', 'April 2011', 262, 'DL2-11905.PDF', '2016-05-31 (version 2.5)', 257, 'both Cleveland Open Cup')]:
    new(rid, 'tier2.flash_point', 'C02', 'Genuine contradiction between document types (same open-cup method)',
        [V(tval, tds, 1, tdsrev, unit='°C', cond='COC', doc_type='TDS'), V(sval, sds, '3 and 4' if 'MPAO' in rid or rid.endswith('8') else '3 and 5' if rid.endswith('4') else '2 and 4', sdsrev, unit='°C', cond=meth, doc_type='SDS')],
        f'The TDS cited in the field prints {tval} °C; the product SDS (cited in source_documents, not compared in the JSON) prints {sval} °C. Both are open-cup values ({meth}). The difference ({tval - sval} °C) is not recorded in conflicts[].',
        'Verified in source text (both documents)', 'Unresolved', 'Ask Chevron Phillips which value is current; record as a conflict with both values.', paths=jp(rid, 2, 'flash_point'))
new('CHEVRON_SYNFLUID_PAO_2', 'tier2.flash_point', 'C03', 'Difference between editions and document types',
    [V(159, 'DL2-14990.pdf', 1, 'April 2011', unit='°C', cond='COC', doc_type='TDS (cited)'), V(164, 'DL2-13192.pdf', 1, 'December 2008', printed='Flash Point (COC), °F, °C 327 (164)', unit='°C', doc_type='TDS (older)'),
     V(160, 'DL2-14991.pdf', '4 and 6', '2016-05-31 (version 1.9)', printed='Flash point : 160 °C (320 °F) Method: Cleveland Open Cup', unit='°C', doc_type='SDS')],
    'Three documents for the same product print 159, 164 and 160 °C (all open cup); only the 2011 TDS value is in the field and no conflict is recorded.',
    'Verified in source text (all three documents)', 'Unresolved', 'Confirm the current value with Chevron Phillips; record the older TDS and the SDS values as a conflict.', paths=jp('CHEVRON_SYNFLUID_PAO_2', 2, 'flash_point'))
new('CHEVRON_SYNFLUID_PAO_2', 'tier1.kv40', 'C03', 'Difference between editions',
    [V(5.1, 'DL2-14990.pdf', 1, 'April 2011', unit='cSt', cond='40 °C', doc_type='TDS (cited)'), V(5.0, 'DL2-13192.pdf', 1, 'December 2008', printed='Kinematic Viscosity, cSt @ 104°F, 40°C 5.0', unit='cSt', cond='40 °C', doc_type='TDS (older)')],
    'The 2008 and 2011 TDS editions print 5.0 and 5.1 cSt at 40 °C; not recorded as a conflict.', 'Verified in source text', 'Unresolved',
    'Record as an edition difference (minor).', paths=jp('CHEVRON_SYNFLUID_PAO_2', 1, 'kv40'))
for rid, tds, diffs in [
        ('CHEVRON_SYNFLUID_PAO_5', 'DL2-13193.pdf', [('viscosity_index', 144, 145), ('pour_point', -45, -46), ('noack_volatility', 5.5, 5.6)]),
        ('CHEVRON_SYNFLUID_PAO_7', 'DL2-13194.pdf', [('kv40', 37.3, 37.7), ('viscosity_index', 148, 146), ('pour_point', -42, -43), ('flash_point', 262, 264), ('noack_volatility', 3.3, 3.7)]),
        ('CHEVRON_SYNFLUID_PAO_9', 'DL2-13196.pdf', [('kv40', 53.9, 53.4), ('kv100', 9.0, 8.9), ('pour_point', -36, -34), ('flash_point', 276, 280), ('noack_volatility', 2.2, 2.4)])]:
    props = ', '.join(d[0] for d in diffs)
    new(rid, props, 'C01', 'Genuine differences between two cited supplier documents (small magnitude)',
        [V('; '.join(f'{k} {a}' for k, a, b in diffs), tds, 1, 'December 2008', doc_type='individual TDS (cited in fields)'),
         V('; '.join(f'{k} {b}' for k, a, b in diffs), 'DL2-13200.pdf', 1, 'not printed', doc_type='Synfluid C10/C12 PAO family typical-properties table (cited in source_documents)')],
        f'The individual TDS and the family table (both cited by this product) print different typical values for {props}. The field uses the individual TDS; the family table values are not recorded and neither document is dated relative to the other (the family table has no date).',
        'Verified in source text (both documents, column read for this grade)', 'Unresolved', 'Ask Chevron Phillips which table is current; record the differences as conflicts.')
new('CHEVRON_SYNFLUID_DIMER_C12', 'tier2.pour_point', 'C10', 'Likely transcription error caused by a mislabelled header in the source',
    [V(-63, 'DL2-13202.pdf', 1, 'April 2011', printed='Pour Point, °F, °C | -53 (-63)', unit='°C (as stored)', doc_type='TDS (cited)'),
     V(-53, 'DL2-13200.pdf', 1, 'not printed', printed='Pour Point, °C (°F) | -53 (-63)', unit='°C', doc_type='family typical-properties table')],
    'DL2-13202 heads the row "°F, °C" but prints "-53 (-63)". Read in header order this would be -53 °F = -63 °C, which is impossible (-53 °F is about -47 °C); the pair is only consistent as -53 °C (-63 °F), which is how the family table DL2-13200 prints it. The JSON stores -63 °C. Every other °F/°C pair in the archive was checked and is internally consistent.',
    'Verified in source text (both documents; arithmetic check of the °F/°C pair)', 'Requires Review', 'Confirm with Chevron Phillips; if confirmed, the field value -63 °C should be reviewed by the data owner (not changed by this audit).',
    paths=jp('CHEVRON_SYNFLUID_DIMER_C12', 2, 'pour_point'))
# ---------------------------------------------------------------- new: ExxonMobil TDS vs SDS
new('EXXONMOBIL_SPECTRASYN_ELITE_150', 'tier2.flash_point', 'C02', 'Genuine contradiction between document types (same method)',
    [V(277.0, 'DL2-11378.pdf', 1, '01/07/2015', unit='°C', cond='ASTM D92', doc_type='TDS (cited)'), V(246, 'DL2-11849.pdf', '2 and 5', '26 Sep 2012', printed='Flash Point [Method]: 246°C (475°F) [ASTM D-92]', unit='°C', doc_type='SDS (uncited)')],
    'TDS 277 °C and SDS 246 °C, both ASTM D92: a 31 °C difference not recorded in conflicts[].', 'Verified in source text', 'Unresolved',
    'Ask ExxonMobil which value applies; record both.', paths=jp('EXXONMOBIL_SPECTRASYN_ELITE_150', 2, 'flash_point'))
new('EXXONMOBIL_SPECTRASYN_ELITE_150', 'tier1.kv40; tier1.kv100', 'C04', 'Difference between document types; SDS uses an in-house method',
    [V('kv40 1649.0; kv100 156.0', 'DL2-11378.pdf', 1, '01/07/2015', unit='cSt', cond='ASTM D445', doc_type='TDS (cited)'),
     V('kv40 1731; kv100 157', 'DL2-11849.pdf', 5, '26 Sep 2012', printed='Viscosity: 1731 cSt (1731 mm2/sec) at 40 °C | 157 cSt (157 mm2/sec) at 100°C [In-house method]', unit='cSt', doc_type='SDS (uncited)')],
    'KV40 differs by about 5 % (1649 vs 1731 cSt); the SDS states an in-house method, so the difference may be method-related.', 'Verified in source text', 'Requires Review',
    'Record as a conflict with methods noted; confirm with ExxonMobil if needed.', paths=jp('EXXONMOBIL_SPECTRASYN_ELITE_150', 1, 'kv40'))
new('EXXONMOBIL_ESTEREX_P81', 'tier1.kv40; tier1.kv100', 'C04', 'Difference between document types; SDS uses an in-house method',
    [V('kv40 84.0; kv100 8.3', 'DL2-12120.pdf', 1, '05/27/2008', unit='cSt', cond='ASTM D445', doc_type='TDS (cited)'),
     V('kv40 86.7; kv100 8.5', 'DL2-12989.pdf', 5, '30 Mar 2018', printed='Viscosity: 86.7 cSt (86.7 mm2/sec) at 40 °C | 8.5 cSt (8.5 mm2/sec) at 100°C [In-house method]', unit='cSt', doc_type='SDS (uncited)')],
    'The 2018 SDS prints higher viscosities than the 2008 TDS (different method and edition); not recorded.', 'Verified in source text', 'Requires Review',
    'Record as a conflict with methods and dates noted.', paths=jp('EXXONMOBIL_ESTEREX_P81', 1, 'kv40'))
# ---------------------------------------------------------------- new: aramcoPRIMA 70 SDS below specification minimum
new('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash_point', 'C05', 'Genuine contradiction: value in one document below the specification minimum in another',
    [V('minimum 175', 'DL2-12172.pdf', 1, 'not printed', printed='Flash Point, COC | ASTM D-92 | Min | 175', unit='°C', doc_type='LUBEREF GII product specifications (cited)'),
     V(168, 'DL2-15448.pdf', 5, 'Issue date 5/05/2021 (revision 2.0, supersedes 14/03/2018)', printed='Flash point : 168 °C', unit='°C', cond='no method printed', doc_type='SDS (cited in source_documents)')],
    'The SDS flash point (168 °C) is below the specification minimum (175 °C, COC). The SDS prints no method; if it is a closed-cup value the difference could be method-related.', 'Verified in source text', 'Unresolved',
    'Ask Aramco for the SDS test method; record as a conflict.', paths=jp('ARAMCO_LUBEREF_PRIMA_70', 2, 'flash_point'))
# ---------------------------------------------------------------- new: S-OIL Ultra-S 6 third value set
new('S_OIL_ULTRA_S_6', 'kv40, kv100, viscosity_index, flash_point, pour_point, noack_volatility, specific gravity', 'C03', 'Additional undocumented edition (third value set)',
    [V('kv40 33.32; kv100 6.0; VI 127; flash 235; pour -20', 'DL2-11177.pdf', 1, 'not printed', doc_type='S-OIL catalog (values in the JSON fields)'),
     V('kv40 32.69; kv100 6.017; VI 132; flash 234; pour -17.5; Noack 7.9; Sp.Gravity 15/4 °C 0.840', 'DL2-11240.pdf (= DL2-11241.pdf, DL2-11242.pdf, byte-identical)', 1, 'not printed', doc_type='Cosan (authorised S-OIL distributor) typical properties, uncited'),
     V('kv40 32.54; kv100 6.04; VI 134; flash 240; pour -16', 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx', None, None, doc_type='S-OIL web table (documented)', check='external (documented conflict)')],
    'The documented Ultra-S 6 conflicts compare DL2-11177 with the S-OIL web table. A third archive source, the Cosan distributor sheet, prints a different set of values for Ultra-S 6 (for Ultra-S 4 and 8 it matches DL2-11177 exactly). It is not cited and not recorded.',
    'Verified in source text (column for Ultra-S 6 read)', 'Unresolved', 'Add the Cosan values to the existing Ultra-S 6 conflicts as a third source; confirm the current edition with S-OIL.')
# ---------------------------------------------------------------- new: calculated values contradicting printed values
for rid, calc, printed, f in [('LUBRIZOL_CV1100', 5.8, 7, 'DL2-11503.pdf'), ('LUBRIZOL_CV3515', 9.2, 10, 'DL2-15722.pdf')]:
    new(rid, 'tier2.sulfated_ash', 'C09', 'Calculated value used although the cited product document prints a typical value; the two disagree',
        [V(calc, None, None, None, unit='wt.%', cond='Calculated from Ca/Mg/Zn with factors 3.40/4.95/1.24', doc_type='JSON calculation (status Calculated, no source)', check='JSON only'),
         V(printed, f, 2, None, printed=f'SULFATED ASH | {printed}', unit='% weight (column heading "Minimum % Weight | Typical | Maximum % Weight")', doc_type='Lubrizol product data sheet (cited by this product)')],
        f'The product data sheet prints a typical sulfated ash of {printed} (% weight); the JSON field is Calculated ({calc} wt.%) from element contents. A printed value exists, and the calculation does not reproduce it.',
        'Verified in source text and visually (table on p.2; headings on p.1)', 'Requires Review',
        'Data owner to decide whether the printed value should be recorded; keep the calculation documented. Not changed by this audit.', paths=jp(rid, 2, 'sulfated_ash'))
ash = []
for folder, p in P.items():
    for tk, t in p['tiers'].items():
        n = t['doc'].get('fields', {}).get('sulfated_ash')
        if isinstance(n, dict) and n.get('status') == 'Calculated':
            note = n.get('calculation_note') or ''
            zf = '1.5' if '1.5×' in note and 'Zn' in note else ('1.24' if '1.24' in note else '?')
            ash.append((p['record_id'], n.get('value'), zf))
z124 = [a for a in ash if a[2] == '1.24']; z15 = [a for a in ash if a[2] == '1.5']
new('MINGLAN_T3161A', f'tier2.sulfated_ash (all {len(ash)} Calculated values)', 'C10', 'Inconsistent derivation rule across products',
    [V(f'Zn factor 1.24, Ca/Mg/Zn only ({len(z124)} products: ' + ', '.join(a[0] for a in z124) + ')', None, None, None, doc_type='JSON calculation_note', check='JSON only'),
     V('Zn factor 1.5, plus Mo 1.5 and B 3.22 terms (MINGLAN_T3161A)', None, None, None, doc_type='JSON calculation_note', check='JSON only')],
    'All Calculated sulfated-ash values cite "ASTM D874" conversion factors, but two different zinc factors are used (1.24 in most products, 1.5 in MINGLAN_T3161A), and only MINGLAN_T3161A adds molybdenum and boron. The same rule cannot both be the D874 factor set; at least one set of derived values rests on an unverified factor.',
    'JSON-only inconsistency; factor not checked against the ASTM D874 text (standard not in the archive)', 'Requires Review',
    'Check the factors against ASTM D874 (Appendix) and apply one documented rule; values not changed by this audit.',
    paths=[f'{P[folder_of(a[0])]["tiers"]["tier2"]["file"]}#fields.sulfated_ash' for a in ash])
# ---------------------------------------------------------------- new: API group vs properties
for rid, issue, extra in [
        ('ADNOC_ADBASE_3CST', 'Group II with VI 120', 'API 1509 places VI 80 to < 120 in Group II and VI >= 120 in Group III; a VI of exactly 120 falls in Group III by that definition.'),
        ('ARAMCO_LUBEREF_PRIMA_70', 'Group II with a specification VI minimum of 76', 'The specification allows a VI below 80, the API 1509 lower limit for Group II; the printed value is a minimum, not a measurement.'),
        ('PETRO_CANADA_PURITY_VHVI_2', 'Group III with VI 100', 'The Group III label comes from a family/refinery statement ("the only Group III refinery in North America", value_kind "supplier family classification"), while the grade VI is 100 (< 120).')]:
    fg, ng = field(rid, 1, 'api_group_chemistry.api_group'); fv, nv = field(rid, 1, 'viscosity_index')
    new(rid, 'tier1.api_group_chemistry.api_group vs tier1.viscosity_index', 'C06', 'Classification contradicts reported properties (API 1509 definition)',
        [V(ng.get('value'), *A.src_of(ng), printed=ng.get('printed_text'), doc_type='API group as recorded'),
         V(nv.get('value'), *A.src_of(nv), printed=nv.get('printed_text'), cond=f"qualifier {nv.get('qualifier')}" if nv.get('qualifier') else None, doc_type='viscosity index as recorded')],
        issue + '. ' + extra, 'Recorded values verified in source text on their cited pages; the classification rule (API 1509 group definitions) is not in the archive', 'Requires Review',
        'Ask the supplier for the grade-specific API group; keep the recorded label and VI as printed.',
        paths=[f'{fg}#fields.api_group_chemistry.api_group', f'{fv}#fields.viscosity_index'])
# ---------------------------------------------------------------- new: Richful flash-point field selection (explainable, not a contradiction)
for rid, sds, tds, typ in [('RICHFUL_RF6066', 'DL2-15831.pdf', 'DL2-15451.pdf', 220), ('RICHFUL_RF6069', 'DL2-15619.pdf', 'DL2-15618.pdf', 216), ('RICHFUL_RF6077', 'DL2-15542.pdf', 'DL2-15536.pdf', 210),
                           ('RICHFUL_RF6078', 'DL2-15833.pdf', 'DL2-15832.pdf; RF6078 - TDS.pdf', 220), ('RICHFUL_RF6079', 'DL2-15541.pdf', 'DL2-15535.pdf; RF6079 Diesel Engine Oil Additive Package.pdf', 214),
                           ('RICHFUL_RF6088', 'DL2-15838.pdf', 'DL2-15452.pdf', 203), ('RICHFUL_RF6088F', 'DL2-15840.pdf', 'DL2-15839.pdf', 218), ('RICHFUL_RF6400', 'DL2-15850.pdf', 'DL2-15849.pdf; RF6400 TDS.pdf', 226),
                           ('RICHFUL_RF6406', 'RF6406.pdf', 'DL2-15456.pdf', 223)]:
    new(rid, 'tier2.flash_point', 'C05', 'Explainable difference (bound vs typical); inconsistent field selection, not a contradiction',
        [V('≥ 180 (lower bound)', sds, 5 if sds != 'RF6406.pdf' else None, None, unit='°C', doc_type='SDS (value in field)'),
         V(f'{typ} (typical; specification ≥ 180 / ≮ 180)', tds, 1, None, unit='°C', cond='COC, ASTM D92 / GB/T 3536', doc_type='TDS')],
        f'The field holds the SDS lower bound although the TDS prints a typical value of {typ} °C (compatible: {typ} ≥ 180). Other Richful records (RF6071L, RF6408) store the TDS typical. Not recorded in conflicts[].',
        'Verified in source text (TDS); SDS value as recorded', 'Requires Review', 'Data owner to choose a consistent rule for Richful flash points; record the TDS typical as an alternate value.',
        paths=jp(rid, 2, 'flash_point'))
# ---------------------------------------------------------------- new: data-quality items in the JSON
for rid in ('INFINEUM_D3354', 'INFINEUM_D3375'):
    f, n = field(rid, 2, 'flash_point')
    new(rid, 'tier2.flash_point', 'C05', 'Data-quality inconsistency (specification minimum labelled typical)',
        [V(n.get('value'), *A.src_of(n), printed=n.get('printed_text'), cond=f"qualifier {n.get('qualifier')}; value_kind {n.get('value_kind')}")],
        'The printed text is a minimum ("min."/"Minimum") and the qualifier is "≥", but value_kind is "typical".', 'Verified against printed_text', 'Requires Review',
        'Correct value_kind to the specification/minimum label (data owner).', paths=[f'{f}#fields.flash_point'])
f, n = field('RICHFUL_RF6066', 2, 'kv100')
new('RICHFUL_RF6066', 'tier2.kv100 (SDS value)', 'C04', 'Label/unit inconsistency within one supplier document',
    [V(185, 'DL2-15831.pdf', 5, '2021-09-02', printed='Viscosity, dynamic : 185 mm²/s (100 °C)', unit='mm²/s', doc_type='SDS')],
    'The SDS prints the value on its "Viscosity, dynamic" line with a kinematic unit (mm²/s), while its "Viscosity, kinematic" line reads "Not available". The value is recorded as kinematic viscosity in the existing RF6066 KV100 conflict.',
    'Verified visually (p.5)', 'Requires Review', 'Note the label/unit inconsistency in the RF6066 KV100 conflict; confirm with Richful.', prov='New (this audit); related to a documented conflict')
f, n = field('TIANHE_P_TEC_3232', 2, 'density')
new('TIANHE_P_TEC_3232', 'tier2.density', 'C04', 'Unit inconsistency within one supplier document',
    [V(1.013, 'DL2-12939.pdf', 1, None, printed='Density, kg/m3, at 15℃ | 1.0130 | ASTM D4052', unit='kg/m3 (as printed)')],
    'The unit kg/m3 is inconsistent with the magnitude 1.0130 (a density in kg/m3 would be about 1000). integrate_products.py flags it and leaves value_final null.',
    'Verified in source text', 'Unresolved', 'Confirm the unit with Tianhe; keep the value as printed.',
    prov='Previously flagged (integration flag; human-review list in open_questions_and_conflicts.md, integration section)', teammate='Yes: detected by the integration flags of PR #2 (value_final left null)', paths=[f'{f}#fields.density'])
# ---------------------------------------------------------------- previously documented only as open questions
OQS = [
    ('RF6602', r'Flash point differs', 'flash_point (no template field)', 'C02', 'Genuine contradiction between document types', 'TDS DL2-14874.pdf p.1: Flash Point (COC) ≮180 (index), typical 210 °C; SDS RF6602.pdf p.4 (2022-02-18): "Flash point : 160 °C" (no method). The SDS value is below the TDS minimum.', 'Verified in source text', 'Unresolved'),
    ('RF6602', r'Storage temperature differs', 'storage temperature (no template field)', 'C01', 'Difference between documents (handling data)', None, 'As recorded in the open question (not re-checked in this audit)', 'Unresolved'),
    ('RICHFUL_RF6066', r'Storage/blending limits differ', 'storage / blending temperature (no template field)', 'C01', 'Difference between two undated TDS (handling data)', None, 'As recorded in the open question (not re-checked in this audit)', 'Unresolved'),
    ('AFTON_HITEC_5748', r'SSI discrepancy', 'shear_stability (SSI)', 'C01', 'Difference between documents/editions', None, 'As recorded in the open question; DL2-13692.pdf p.2 in the archive, PDS editions external', 'Unresolved'),
    ('AFTON_HITEC_12250', r'14\.5%', 'treat_rate', 'C01', 'Internal arithmetic inconsistency in supplier documents', None, 'As recorded in the open question (external PDS)', 'Unresolved'),
    ('AFTON_HITEC_12210M', r'Claims table changed', 'performance_claims', 'C03', 'Edition difference (claims)', None, 'As recorded in the open question', 'Unresolved'),
    ('AFTON_HITEC_12200', r'Rows and columns only in the 08/18', 'performance_claims / treat_rate_matrix', 'C03', 'Edition difference (claims; partly covered by the MTU 2.0 and DDC 93K215 conflicts)', None, 'As recorded in the open question', 'Unresolved'),
    ('ARAMCO_LUBEREF_PRIMA_110', r'Document discrepancy', 'density', 'C01', 'Difference between documents (unit not printed in one)', None, 'As recorded in the open question', 'Requires Review'),
    ('ARAMCO_LUBEREF_PRIMA_230', r'Document discrepancy', 'density', 'C01', 'Difference between documents (unit not printed in one)', None, 'As recorded in the open question', 'Requires Review'),
    ('ARAMCO_LUBEREF_PRIMA_500', r'Document discrepancy', 'density', 'C01', 'Difference between documents (unit not printed in one)', None, 'As recorded in the open question', 'Requires Review'),
    ('S_OIL_ULTRA_S_4', r'CAS 64742-54-7', 'chemistry / CAS', 'C06', 'Contradiction within one supplier document (description vs CAS number)', None, 'As recorded in the open question', 'Unresolved'),
    ('S_OIL_ULTRA_S_6', r'specific gravity of Ultra-S 6', 'specific gravity', 'C01', 'Difference between documents (0.843 vs 0.841; the Cosan sheet prints 0.840)', None, 'As recorded in the open question; Cosan value verified in this audit', 'Requires Review'),
    ('YUBASE_3', r'g/m3', 'specific gravity', 'C04', 'Unit inconsistency within one supplier document', None, 'As recorded in the open question', 'Unresolved'),
    ('YUBASE_4', r'g/m3', 'specific gravity', 'C04', 'Unit inconsistency within one supplier document', None, 'As recorded in the open question', 'Unresolved'),
    ('YUBASE_5', r'g/m3', 'specific gravity', 'C04', 'Unit inconsistency within one supplier document', None, 'As recorded in the open question', 'Unresolved'),
    ('YUBASE_6', r'g/m3', 'specific gravity', 'C04', 'Unit inconsistency within one supplier document', None, 'As recorded in the open question', 'Unresolved'),
]
for rid, pat, prop, cat, nature, verified_note, ver, res in OQS:
    tk, text = oq(rid, pat)
    if not text: print('OQ not found', rid, pat); continue
    folder = folder_of(rid)
    new(rid, prop, cat, nature, [V(verified_note or 'see open question', None, None, None, check='as recorded')],
        'Open question (verbatim): ' + text + (f' AUDIT CHECK: {verified_note}' if verified_note else ''), ver, res,
        'Promote to a conflicts[] entry with both values and sources, or close the question with evidence.',
        prov='Previously documented as an open question only (not in conflicts[])', paths=[P[folder]['tiers'][tk]['file'] + '#open_questions'])
# ---------------------------------------------------------------- identity (previously documented in reconciliation/identity_review.md / README)
new('S_OIL_ULTRA_S_8', 'product identity', 'C13', 'Possible duplicate identity', [V('S_OIL_ULTRA_S_8 and S_OIL_ARAMCO_ULTRA_8 are separate folders', check='as recorded')],
    'README / identity_review.md ID-01: Ultra-S 8 and aramcoULTRA 8 are named in separate archive SDSs and have two folders; whether they are one product is unresolved. Both SDSs print relative density 0.847 @ 15 ℃ (DL2-15238.pdf, DL2-14611.pdf).',
    'Documented; SDS values verified in source text', 'Unresolved', 'Confirm with S-OIL whether the two names designate one product.', prov='Previously documented (README, reconciliation/identity_review.md ID-01)')
new('FORMOSA_150N_GII_PLUS', 'product identity', 'C13', 'Unresolved product identity', [V('FPCC GII table columns 150N / 500N vs FORMOSA_150N_GII_PLUS and FORMOSA_500N_GII', 'DL2-12108.jpeg', 1, check='image (not machine-readable)')],
    'README / identity_review.md ID-15: the FPCC GII table prints 150N and 500N columns whose identity with the existing records is unresolved.', 'Documented; image source not machine-checked',
    'Unresolved', 'Confirm with Formosa.', prov='Previously documented (README, reconciliation/identity_review.md ID-15)')
new('RICHFUL_RF6406', 'product.supplier', 'C13', 'Missing / inconsistent supplier names', [V('supplier null in RICHFUL_RF6071L, RICHFUL_RF6406, RICHFUL_RF6408; other Richful records use "Xinxiang Richful Lube Additive Co., Ltd" with and without a final period', check='JSON only')],
    'identity_review.md records that product.supplier is null for these records because neither TDS prints a company name. The Richful supplier name is also spelled two ways across records.', 'JSON-only', 'Unresolved',
    'Keep null where the source prints no name; align the spelling of the documented name.', prov='Partly previously documented (reconciliation/identity_review.md); spelling variant new')
# ---------------------------------------------------------------- documentation issue introduced by teammate proposal text
new('RICHFUL_RF6078', 'tier1.treat_rate_matrix (conflict final_resolution text)', 'C14', 'Documentation issue: an incorrect statement kept in a proposal text',
    [V('final_resolution states "The \'values\' in this entry are correct; the note text has the two files swapped."', check='JSON only'),
     V('DL2-15832.pdf p.1: "ACEA E7/API CI-4 11.85%", "API CI-4 10.85%"; RF6078 - TDS.pdf p.1: "ACEA E7/API CI-4 10.85%", "API CI-4 Plus 11.85%"', 'DL2-15832.pdf; RF6078%20-%20TDS.pdf', 1)],
    'The note in the conflict entry is correct; the claim from PR #2, preserved in the not-adopted proposal, is not. The underlying conflict remains unresolved.', 'Verified in source text (both PDFs)', 'Requires Review',
    'Add a note to the entry that the proposal\'s "swapped" claim was checked and is incorrect (data owner).', prov='New (this audit)', teammate='Yes: proposal text from PR #2')

VERIFY_FIX = {
    ('ERGON_HYGOLD_L750', 'density_at_15_6_c'): 'Verified in source text (DL2-10414.pdf p.1 prints 0.854 and 0.9183; SDS DL2-10025.pdf p.6 prints relative density 0,92)',
    ('PETRO_CANADA_PURITY_L65', 'viscosity_index'): 'Archive value verified (DL2-10020.pdf p.2, L-series Viscosity Index row "87 | 92", L65 column = 92); brochure value 104 is not in the archive',
}
for f in F:
    if (f['record_id'], f['property']) in VERIFY_FIX: f['verification'] = VERIFY_FIX[(f['record_id'], f['property'])]
    if (f['record_id'], f['property']) == ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'sulfur'):
        f['nature'] = 'Genuine contradiction: same number printed in units 10,000 times apart (ppm vs wt.%)'
        f['values'] = [dict(value=1.3, unit='ppm', printed_text='Sulfur Content ppm 1.3‡ (‡ D2622)', file='DL2-13944.pdf', page=1, doc_type='typical-properties sheet', source_check='verified in source text'),
                       dict(value=1.3, unit='wt.% (maximum)', printed_text='Sulfur Content Max. WT% ASTM-D 4294 1.3', file='DL2-12173.pdf', page=1, doc_type='specification', source_check='verified in source text')]
        f['verification'] = 'Verified in source text (both documents)'
    if (f['record_id'], f['property']) == ('ERGON_HYGOLD_L750', 'density_at_15_6_c'):
        f['values'] = [dict(value=0.854, unit='g/cm3', conditions='15.6 °C, ASTM D1250', file='DL2-10414.pdf', page=1, revision_date='2017-01-05', doc_type='TDS', source_check='verified in source text'),
                       dict(value=0.9183, unit='dimensionless (specific gravity)', conditions='60 °F (15.6 °C), ASTM D4052', file='DL2-10414.pdf', page=1, revision_date='2017-01-05', doc_type='TDS (same page)', source_check='verified in source text'),
                       dict(value='0,92', unit='relative density', conditions='15,56 °C (60 °F), ASTM D 4052 / ISO 12185', file='DL2-10025.pdf', page=6, doc_type='SDS (uncited)', source_check='verified in source text')]
# ---------------------------------------------------------------- QA corrections (2026-10-27 review)
DOC_TYPE_FIX = {('DL2-10204.pdf', 1): 'TDS/PDS (p.1 of a combined TDS + SDS file)', ('DL2-10204.pdf', 6): 'SDS (p.6 of a combined TDS + SDS file)',
                ('DL2-13731.pdf', 7): 'SDS (confirmed visually)'}
for f in F:
    for v in f['values']:
        if (v.get('file'), v.get('page')) in DOC_TYPE_FIX: v['doc_type'] = DOC_TYPE_FIX[(v.get('file'), v.get('page'))]
key = lambda f: (f['record_id'], f['property'])
for f in F:
    k = key(f)
    # verification labels that must say how the value was checked
    if f['source_kind'] == 'documented' and any(v.get('source_check') == 'verified visually' for v in f['values']):
        f['verification'] = 'Verified in source documents (values on image/vector pages confirmed visually; others in source text)'
    if k[0] == 'NYNAS_NYFROST_32' and k[1] in ('kv40', 'flash_point'):
        f['verification'] = 'Verified in source text; the SDS values are on p.7 of DL2-13444.pdf, not on the cited p.6'
    if k == ('INFINEUM_D3375', 'tier2.flash_point'):
        f['verification'] = 'JSON printed_text only; the source DL2-10217.pdf is an image-only PDF and was not checked'
    if k == ('INFINEUM_D3354', 'tier2.flash_point'):
        f['verification'] = 'Verified against printed_text and the cited page'
    if k == ('LUBRIZOL_CV3515', 'tier2.sulfated_ash'):
        f['verification'] = 'Verified in source text (value on p.2; column headings on p.1)'
    if k == ('LUBRIZOL_CV1100', 'tier2.sulfated_ash'):
        f['verification'] = 'Verified in source text and visually (value on p.2; column headings on p.1)'
    if k[0] in ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'ERGON_HYGOLD_L750') and f['source_kind'] == 'documented' and k[1] in ('sulfur', 'density_at_15_6_c'):
        f['explanation'] += ' NOTE: the JSON conflict entry lists sources only; the values shown here were read from those sources in this audit.'
    if k == ('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'density'):
        f['values'] = [dict(value=0.894, unit='kg/L', conditions='Density @ 15.6 °C (printed "15.6 0C")', file='DL2-13944.pdf', page=1, doc_type='TDS/PDS', source_check='verified in source text')]
        f['verification'] = 'Verified in source text (DL2-13944.pdf p.1 prints "Density @ 15.6 0C" with 0.894 kg/L)'
    if k == ('PETRO_CANADA_PURITY_L65', 'viscosity_index'):
        f['values'] = [dict(value=92, file='DL2-10020.pdf', page=2, revision_date='2015-07', printed_text='Viscosity Index | D2270 | … | 87 | 92 (L65 column)', doc_type='TDS/PDS', source_check='verified in source text'),
                       dict(value=104, file="Petro-Canada 'World-Class Base Oils' brochure (as named in the record)", doc_type='brochure, not in the archive', source_check='not in archive')]
        f['verification'] = 'Archive value verified (DL2-10020.pdf p.2, L65 column = 92); the brochure value 104 is not in the archive and has no registered URL'
    # external sources: two different situations
    if 'relies on source_registry' in f['verification']:
        if f['supplier'].startswith('Petro-Canada'):
            f['verification'] = ('Archive value verified (DL2-10020.pdf, 2015-07). The 2023.03 value comes from Petro-Canada LUB3213E/IM-1809E, read '
                                 '(per the record) from a distributor-hosted mirror at mascherpa.it because the Petro-Canada server blocks automated '
                                 'retrieval; neither URL is in source_registry.json and no copy or checksum is kept. Not verifiable from the repository.')
        else:
            f['verification'] = ('Archive value verified (DL2-11177.pdf and SDSs). The S-OIL web value comes from https://www.s-oil.com/en/energy/LubeBaseOil.aspx, '
                                 'registered in source_registry.json as verified on 2026-10-22 (HTML, undated, no stored copy); not re-fetched in this audit.')
    # new findings: provenance and evidence corrections
    if f['source_kind'] == 'new' and f['category'] == 'C05' and k[0].startswith('RICHFUL_RF6') and k[1] == 'tier2.flash_point':
        f['provenance'] = 'Previously recorded in field notes (calculation_note quotes the TDS line incl. the typical value); not recorded as a conflict'
        fp, n = field(k[0], 2, 'flash_point'); src, pg, rev = A.src_of(n)
        f['values'][0].update(file=src, page=pg, revision_date=rev, printed_text=n.get('printed_text'))
        f['values'][1]['value'] = f['values'][1]['value'].split(' (')[0] + ' (typical)'
        rid = k[0]
        f['verification'] = ('Verified in source text (TDS typical); SDS value confirmed visually' if rid in ('RICHFUL_RF6066', 'RICHFUL_RF6069', 'RICHFUL_RF6078')
                             else 'Finding verified: the TDS typical was found in source text; the SDS bound is quoted from the JSON record (image/vector SDS page, not re-read in this audit)')
        f['explanation'] += ' The field calculation_note quotes the TDS line as "Same value in: …", although the TDS also prints a typical value.'
    if k[0] == 'CHEVRON_SYNFLUID_PAO_8' and k[1] == 'tier2.flash_point':
        f['values'][1]['page'] = '3 and 5'
    if k[0] == 'S_OIL_ULTRA_S_6' and k[1].startswith('kv40, kv100'):
        f['provenance'] = 'New (this audit); DL2-11240.pdf is listed in reconciliation/inventory_reconciliation.csv as a register document, but its values were never compared'
    if k == ('RF6602', 'flash_point (no template field)'):
        f['values'] = [dict(value='≮180 (index); 210 (typical)', unit='°C', conditions='COC', file='DL2-14874.pdf', page=1, printed_text='Flash Point (COC), ℃ | ≮180 | 210', doc_type='TDS', source_check='verified in source text'),
                       dict(value=160, unit='°C', conditions='no method printed', file='RF6602.pdf', page=4, revision_date='2022-02-18', printed_text='Flash point : 160 °C', doc_type='SDS', source_check='verified in source text')]
OQ_CHECK = {
    ('YUBASE_3', 'DL2-11303.pdf', '0,8299'), ('YUBASE_4', 'DL2-11304.pdf', '0,8338'), ('YUBASE_5', 'DL2-11305.pdf', '0,8363'), ('YUBASE_6', 'DL2-11306.pdf', '0,8423')}
for f in F:
    k = key(f)
    for rid, fn, val in OQ_CHECK:
        if k == (rid, 'specific gravity'):
            f['values'] = [dict(value=val, unit='g/m3 (as printed)', conditions='15 °C, ASTM D1298', file=fn, page=1, printed_text=f'Specific gravity at 15 °C | g/m3 | {val}', doc_type='TDS', source_check='verified in source text')]
            f['verification'] = 'Verified in source text'
    if k == ('AFTON_HITEC_12250', 'treat_rate'):
        f['values'] = [dict(value='14.2 % = 10.3 % + 4.2 % (sum is 14.5 %)', file='DL2-14639.pdf', page=2, revision_date='08/18', printed_text='14.2% HiTEC® 12204L = 10.3% HiTEC® 12200 + 4.2% HiTEC® 12250', doc_type='TDS/PDS (HiTEC 12200 bulletin)', source_check='verified in source text')]
        f['verification'] = 'Verified in source text (the footnote of DL2-14639.pdf p.2 itself states 14.2 % = 10.3 % + 4.2 %)'
    if k == ('AFTON_HITEC_5748', 'shear_stability (SSI)'):
        f['values'] = [dict(value='"5748 25SSI"', file='DL2-13692.pdf', page=2, revision_date='07/20', doc_type='HiTEC 12360 bulletin', source_check='verified in source text'),
                       dict(value='SSI 22 (05/23, 04/21, 03/18 PDS); "23 SSI polymer" (07/11 PDS)', file='Afton HiTEC 5748 PDS editions (external, Internet Archive)', doc_type='PDS', source_check='as recorded')]
        f['verification'] = 'Partially verified: DL2-13692.pdf p.2 prints "5748 25SSI"; the PDS editions are external (05/23 edition registered; older editions as recorded)'
    if k == ('AFTON_HITEC_12210M', 'performance_claims'):
        f['verification'] = 'Verified in source text (05/18 DL2-11796.pdf p.2 has API CJ-4 and MTU 2.1 columns; 04/22 DL2-15568.pdf p.2 has ACEA E11-22 and MAN 3775)'
    if k == ('RICHFUL_RF6066', 'storage / blending temperature (no template field)'):
        f['values'] = [dict(value='storage ≤ 50 ℃; loading/unloading and blending ≤ 60 ℃', file='DL2-13819.pdf', page=1, doc_type='TDS (undated)', source_check='verified in source text'),
                       dict(value='long-term storage ≤ 45 ℃; loading/unloading or blending ≤ 65 ℃', file='DL2-15451.pdf', page=1, doc_type='TDS (undated)', source_check='verified in source text')]
        f['verification'] = 'Verified in source text (both TDS)'
    if k == ('RF6602', 'storage temperature (no template field)'):
        f['verification'] = 'Partially verified: TDS DL2-14874.pdf p.1 (short-term ≤ 75 ℃, long-term ≤ 45 ℃) verified; the Richful product-page value is external and not re-checked'
    for rid, a, b in (('ARAMCO_LUBEREF_PRIMA_110', '0.8500', '0.8510'), ('ARAMCO_LUBEREF_PRIMA_230', '0.8630', '0.8625'), ('ARAMCO_LUBEREF_PRIMA_500', '0.867', '0.8720')):
        if k == (rid, 'density'):
            f['values'] = [dict(value=a, unit='no unit printed', conditions='@ 15 °C, ASTM D-4052, Typical', file='DL2-12172.pdf', page=1, doc_type='LUBEREF GII product specifications', source_check='verified in source text'),
                           dict(value=b, unit='kg/L', conditions='@ 15 °C, D 4052, Typical', file='DL2-11773.pdf', page=1, doc_type='aramcoPRIMA brochure (Group II table, printed pp. 8-9; image-only PDF)', source_check='verified visually')]
            f['verification'] = 'Verified (DL2-12172.pdf in source text; DL2-11773.pdf visually)'
            if rid != 'ARAMCO_LUBEREF_PRIMA_500':
                f['explanation'] += ' The brochure marks the aramcoPRIMA 110 and 230 columns "*Typicals are subject to confirmation upon startup of the new Group II plant".'
    if k == ('S_OIL_ULTRA_S_4', 'chemistry / CAS'):
        f['values'] = [dict(value='"Distillates (petroleum), hydrotreated light paraffinic" with CAS 64742-54-7', file='DL2-15139.pdf', page=1, revision_date='2015-06-10', doc_type='SDS', source_check='verified in source text')]
        f['verification'] = 'Printed text verified; the mismatch claim rests on the name registered for CAS 64742-54-7, which is not in the archive'
    if k == ('S_OIL_ULTRA_S_6', 'specific gravity'):
        f['values'] = [dict(value='0.843 (as recorded)', file='DL2-11177.pdf', page=1, doc_type='S-OIL catalog', source_check='not resolved in the text layer (multi-column)'),
                       dict(value='0.841', file='DL2-15237.pdf', page=2, revision_date='June 10, 2015', printed_text='RELATIVE DENSITY 0.841 @ 15℃', doc_type='SDS', source_check='verified in source text'),
                       dict(value='0.840', file='DL2-11240.pdf', page=1, printed_text='Sp.Gravity,15/4℃ D 1298 0.840 (Ultra-S 6 column)', doc_type='Cosan distributor sheet', source_check='verified in source text')]
        f['verification'] = 'Partially verified: 0.841 (SDS) and 0.840 (Cosan) verified; the 0.843 catalog value could not be isolated in the multi-column text layer'


def group_of(f):
    n = f['nature']; k = key(f)
    if k in (('INFINEUM_D3424', 'tier2.flash_point'), ('RICHFUL_RF6406', 'tier2.tbn')): return 'Explainable difference'
    if re.search(r'(?i)explainable|bound vs typical|in-house method|units or test conditions|test method', n): return 'Explainable difference'
    if re.search(r'(?i)edition', n): return 'Edition difference'
    if re.search(r'(?i)data-quality|documentation|derivation|calculated value used|label/unit|unit inconsistency|identity|supplier names|likely transcription', n): return 'Data-quality issue'
    return 'Genuine contradiction'


BASIS = {'Genuine contradiction': 'Incompatible values for the same product and property; no documented method, condition or edition explains them.',
         'Edition difference': 'Values differ between dated editions (or editions of one document series) of the supplier\'s documents.',
         'Explainable difference': 'Values differ, but the documents themselves state a different method, condition, unit or bound type; the values are not incompatible.',
         'Data-quality issue': 'A problem in how the JSON or a supplier document records a value, unit, label, derivation rule or identity.'}
for f in F:
    f['group'] = group_of(f); f['group_basis'] = BASIS[f['group']]
    if key(f) == ('INFINEUM_D3424', 'tier2.flash_point'):
        f['nature'] = 'Explainable difference: TDS typical (190 °C) vs SDS lower bound (>110 °C); compatible, as the record states'
    if key(f) == ('RICHFUL_RF6406', 'tier2.tbn'):
        f['nature'] = 'Explainable difference: typical 185 vs minimum ≥ 180 (compatible); the two undated TDS also print different specification ranges'
# verification priority for findings that still need a source check
# (record_id, exact property) -> priority and reason
PRIORITY = {
    ('CHEVRON_SYNFLUID_DIMER_C12', 'tier2.pour_point'): 'High: the stored value was probably misread from a mislabelled header.',
    ('MINGLAN_T3161A', 'tier2.sulfated_ash (all 26 Calculated values)'): 'High: the zinc-factor rule affects all 26 Calculated sulfated-ash values; needs the ASTM D874 text.',
    ('ADNOC_ADBASE_3CST', 'tier1.api_group_chemistry.api_group vs tier1.viscosity_index'): "High: API group classification; needs the API 1509 definition and the supplier's grade-level group.",
    ('PETRO_CANADA_PURITY_VHVI_2', 'tier1.api_group_chemistry.api_group vs tier1.viscosity_index'): 'High: API group taken from a family statement; needs a grade-level source.',
    ('ARAMCO_LUBEREF_PRIMA_70', 'tier1.api_group_chemistry.api_group vs tier1.viscosity_index'): 'High: API group vs specification VI minimum 76; needs the supplier\'s grade-level group.',
    ('ARAMCO_LUBEREF_PRIMA_70', 'tier2.flash_point'): 'High: SDS flash point below the specification minimum; the SDS test method is needed.',
    ('INFINEUM_D3375', 'tier2.flash_point'): 'High: the source is an image-only PDF; the JSON value has not been checked against the page.',
    ('S_OIL_ULTRA_S_4', 'chemistry / CAS'): 'High: chemical identity (description vs CAS number) in the SDS.',
    ('S_OIL_ULTRA_S_6', 'specific gravity'): 'Medium: the catalog value could not be isolated; three value sets for one grade.',
    ('AFTON_HITEC_5748', 'shear_stability (SSI)'): 'Medium: SSI 22 / 23 / 25 across editions; older PDS editions external.',
    ('AFTON_HITEC_12200', 'performance_claims / treat_rate_matrix'): 'Medium: claims rows between editions recorded only as an open question.',
    ('RF6602', 'storage temperature (no template field)'): 'Low: handling data; the product-page value is external.',
    ('FORMOSA_150N_GII_PLUS', 'product identity'): 'Medium: identity question rests on an image source.',
    ('S_OIL_ULTRA_S_8', 'product identity'): 'Medium: identity question (Ultra-S 8 vs aramcoULTRA 8) needs the supplier.',
    ('RICHFUL_RF6406', 'product.supplier'): 'Low: supplier name not printed; spelling variants only.',
    ('PETRO_CANADA_PURITY_L65', 'viscosity_index'): 'Medium: the brochure value 104 has no archived copy or registered URL.',
}
for f in F:
    f['verification_priority'] = ''
    if 'mascherpa' in f['verification']:
        f['verification_priority'] = 'High (one action for all 61): register and archive the Petro-Canada 2023.03 LUB3213E document, then re-check its values.'
    elif 'registered in source_registry.json' in f['verification']:
        f['verification_priority'] = 'Low: registered manufacturer web page (S-OIL); a dated spot check before submission is sufficient.'
    elif (f['record_id'], f['property']) in PRIORITY:
        f['verification_priority'] = PRIORITY[(f['record_id'], f['property'])]
    elif re.search(r'(?i)as recorded|not checked|not verifiable|partially|JSON-only|JSON printed_text only|rests on|not in the archive|image source|not machine', f['verification']):
        f['verification_priority'] = 'Low: minor or handling-data difference; check when the supplier is contacted.'
for i, f in enumerate(F, 1):
    f['id'] = f'CF-{i:03d}'
json.dump(F, open(os.path.join(A.SCR, 'audit', 'findings.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
c = collections.Counter
print('findings', len(F), '| by kind', c(f['source_kind'] for f in F), '| by provenance', c(f['provenance'].split(' (')[0] for f in F))
print('by category', sorted(c(f['category'] for f in F).items()))
print('by class', c(f['material_class'] for f in F)); print('by resolution', c(f['resolution'] for f in F))
print('verification', c(f['verification'].split(':')[0].split(' (')[0] for f in F).most_common())
print('teammate', c(f['teammate'].split(':')[0] for f in F))
