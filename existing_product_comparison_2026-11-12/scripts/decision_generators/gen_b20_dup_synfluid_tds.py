"""Seventeenth pass, batch 20: duplicate (category A) coverage of ten one-page Chevron Phillips Synfluid data sheets, each read in
full (text layer) with its product's record beside it (reading aid scripts/reading_aids/dupcmp.py).
Writes decisions/zzzzzzzzzzzzzzzzz_b20_dup_synfluid_tds_seventeenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'seventeenth pass, 2026-11-14'
links, F = [], []
HAND = "'Maximum temperatures of 65 ºC (149 ºF) for handling and ambient for long-term storage are recommended.'"


def link(pid, f, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'p.1 (only page) read in full (text layer) ({T})',
                      coverage=f'assessed by reading (2026-11-14, seventeenth pass) for the whole page ({ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name on the page', note='Byte duplicate of the cited data sheet.'))


def o(f, ed):
    return f're-read manually: {f} ({ed}) p.1 whole text ({T})'


def note(pid, f, ed, text, reason='Old-source items without a template field, preserved as printed; nothing is mapped to a field.', path='open_questions', action='propose_note', outcome='in_old_source_not_captured',
         form='typical values and statements as printed (data sheet; no template field)', tier=1, new_text='(same file; byte duplicate in the new archive)', cmp='existing: not recorded', unit='as printed', method='as printed'):
    F.append(dict(p=pid, tier=tier, path=path, old=text, new_f=f, new_p=1, new_text=new_text, unit=unit, form=form, qual='as printed', method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=o(f, ed), cmp_override=cmp))


S = [  # pid, file, edition, uncaptured items
    ('CHEVRON_SYNFLUID_DIMER_C10', 'DL2-13201.pdf', 'MSDS #3341, Revision Date April 2011',
     "'Kinematic Viscosity, cSt @ -40°F, -40°C 220'; 'Fire Point (COC), °F, °C 338 (170)'; 'Density, lb/gal 6.683'; 'Total Acid Number <0.03'; Odor 'No Foreign Odor'; Appearance 'Clear and Bright'; 'Color, Pt-Co 0'; VI, Noack and Bromine Index printed '----'; application 'reactive olefinic intermediate typically containing about 20 carbon atoms'"),
    ('CHEVRON_SYNFLUID_DIMER_C12', 'DL2-13202.pdf', 'MSDS #5836, Revision Date April 2011',
     "'Kinematic Viscosity, cSt @ -40°F, -40°C 858'; 'Fire Point (COC), °F, °C 396 (202)'; 'Density, lb/gal 6.745'; 'Total Acid Number <0.03'; Odor / Appearance / 'Color, Pt-Co 0'; VI, Noack and Bromine Index '----'; 'reactive olefinic intermediate typically containing about 24 carbon atoms'"),
    ('CHEVRON_SYNFLUID_MPAO_50', 'DL2-13190.pdf', 'MSDS #100000101860, Revision Date April 2013',
     "'Density, lb/gal 7.046'; 'Bromine Index <400'; Odor / Appearance / 'Color, Pt-Co 0'; applications 'engine oils, gear oils, greases, and other functional fluids'"),
    ('CHEVRON_SYNFLUID_PAO_40', 'DL2-13127.pdf', 'MSDS # 4814, Revision Date March, 2004',
     "'Fire Point (COC), °F, °C 599 (315)'; 'Density, lb/gal 7.087'; 'Bromine Index <200'; 'Color, Pt-Co 20'; 'Color, Saybolt 26'; Odor / Appearance; KV -40 °C, Noack and TAN printed '----'"),
    ('CHEVRON_SYNFLUID_PAO_5', 'DL2-13193.pdf', 'MSDS #5940, Revision Date December, 2008',
     "'Kinematic Viscosity, cSt @ -40°F, -40°C 4716'; 'Fire Point (COC), °F, °C 529 (276)'; 'Density, lb/gal 6.862'; 'Total Acid Number <0.03'; 'Bromine Index <200'; Odor / Appearance / 'Color, Pt-Co 0'"),
    ('CHEVRON_SYNFLUID_PAO_6_HVI', 'DL2-13197.pdf', 'MSDS # 100000101638, Revision Date June 2012',
     "'Kinematic Viscosity, cSt @ -40°F, -40°C 7,457'; 'Fire Point (COC), °F, °C 556 (291)'; 'Density, lb/gal 6.893'; 'Total Acid Number <0.03'; 'Bromine Index <200'; Odor / Appearance / 'Color, Pt-Co 0'"),
    ('CHEVRON_SYNFLUID_PAO_7', 'DL2-13194.pdf', 'MSDS #5941, Revision Date December, 2008',
     "'Kinematic Viscosity, cSt @ -40°F, -40°C 10,561'; 'Fire Point (COC), °F, °C 558 (292)'; 'Density, lb/gal 6.917'; 'Total Acid Number <0.03'; 'Bromine Index <200'; Odor / Appearance / 'Color, Pt-Co 0'"),
    ('CHEVRON_SYNFLUID_PAO_8_BLEND', 'DL2-13195.pdf', 'MSDS #8014, Revision Date March, 2004',
     "'Fire Point (COC), °F, °C 555 (290)'; 'Density, lb/gal 6.933'; 'Bromine Index <200'; 'Color, Pt-Co <1'; 'Color, Saybolt +30'; Odor / Appearance; KV -40 °C and TAN '----'"),
    ('CHEVRON_SYNFLUID_PAO_9', 'DL2-13196.pdf', 'MSDS #5653, Revision Date December, 2008',
     "'Fire Point (COC), °F, °C 581 (305)'; 'Density, lb/gal 6.947'; 'Total Acid Number <0.03'; 'Bromine Index <200'; Odor / Appearance / 'Color, Pt-Co 0'; KV -40 °C '----'"),
]
for pid, f, ed, unc in S:
    extra = ''
    if pid == 'CHEVRON_SYNFLUID_DIMER_C12':
        extra = (" The pour point is printed 'Pour Point, °F, °C -53 (-63)'; the record already documents the unit-order problem in full"
                 " (pour_point calculation_note and notes, audit CF-136, citing DL2-13200.pdf '°C (°F) -53 (-63)'), so no row is proposed."
                 " (An open-question row proposed in the first version of this batch was withdrawn in the eighteenth pass as redundant.)")
    link(pid, f, ed, "every recorded value (KV100 / KV40 / VI where printed, specific gravity 60/60 °F, pour, flash COC, Noack where printed, chemistry from the product sub-title) equals the 'Typical Properties' table; each °F (°C) pair was checked on the page." + extra + " Not recorded: " + unc.split(';')[0] + ' and the other items -> note.')
    note(pid, f, ed, f"{f} ('Typical Properties', {ed}) prints (not recorded): {unc}; handling {HAND}.")


# PAO 2.5 on the combined C10 / C12 sheet
ed13200 = 'combined C10 / C12 PAO typical-properties sheet, undated'
link('CHEVRON_SYNFLUID_PAO_2_5', 'DL2-13200.pdf', ed13200,
     "column '2.5 cSt' of the 'C12 Based PAOs' table: KV100 2.4 / KV40 8.2 (ASTM D 7042), pour -52 (-62) ASTM D 5950, flash COC 188 (370) ASTM D 92 and specific gravity 0.8086 (ASTM D 4052) equal the record; VI and Noack are printed '—' (Missing, correctly). The record's chemistry is Missing although the column sits under the heading 'C12 Based PAOs' -> capture row; not recorded: KV -40 °C 1,811 (ASTM D 445), fire point 208 (406), density 6.733 lb/gal and the shared footnote -> note. The page does not print the trade name 'Synfluid' (the existing citation establishes the link). The sheet's other columns are reviewed product by product in batch 26 (eighteenth pass).")
note('CHEVRON_SYNFLUID_PAO_2_5', 'DL2-13200.pdf', ed13200,
     "DL2-13200.pdf, column '2.5 cSt' (C12 Based PAOs), prints (not recorded): '-40°C (-40°F) 1,811 ASTM D 445'; 'Fire Point (COC), °C (°F) 208 (406) ASTM D 92'; 'Density, lb/gal. 6.733'; and for all products 'Total Acid Numbers of <0.03 (ASTM D 974), Appearance is Clear and Bright (ASTM D 4176), No Foreign Odor (ASTM D 1296) and Pt Co Color of 0 (ASTM D 5306)'.")
note('CHEVRON_SYNFLUID_PAO_2_5', 'DL2-13200.pdf', ed13200, "Record: api_group_chemistry.chemistry Missing; the other fields of this record cite DL2-13200.pdf p.1 column '2.5 cSt'.",
     reason="The only chemistry the sheet prints for this column is its table heading 'C12 Based PAOs' (beside 'C10 Based PAOs'). Propose capturing it as printed ('C12 Based PAOs'), cited to the heading, for the mandatory chemistry field. It is a supplier family heading, not an assay; no API group is inferred from it (api_group stays Missing). The reviewer should confirm that the '2.5 cSt' column is the product of this record, as the existing citations assume, since the page does not print 'Synfluid'.",
     path='api_group_chemistry.chemistry', action='capture_from_old_source', form='supplier table heading naming the chemical family (data sheet)', new_text="'C12 Based PAOs' (table heading above the '2.5 cSt' column)",
     cmp='existing: Missing', unit='n/a', method='n/a')
# Eighteenth pass: the capture is conditional on identity verification (the page does not print 'Synfluid').
F[-1]['cond'] = "CONDITIONAL: apply only after the reviewer confirms that the '2.5 cSt' column of DL2-13200.pdf is Synfluid PAO 2.5 cSt"
F[-1]['reason'] += " Conditional: this capture must not be applied before that identity is confirmed; until then chemistry stays Missing."

d = dict(batch='duplicate coverage, batch 20: Chevron Phillips Synfluid one-page sheets (seventeenth pass)', reviewed_on='2026-11-14 (seventeenth pass)',
         note='Ten byte-duplicate links; each page read in full with the record beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzz_b20_dup_synfluid_tds_seventeenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
