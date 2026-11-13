"""Sixteenth pass, batch 17: duplicate (category A) coverage of three family tables, each read in full and viewed as an image:
ExxonMobil 'EHC Series' PDS DL2-11785.pdf (3 pp., 5 grades), Petro-Canada 'PURITY VHVI Specialty Base Fluids' brochure
DL2-11261.pdf (2 pp., LUB3212E (2015.07), 5 grades) and S-OIL 'PREMIUM SERIES' DL2-11173.pdf (1 page, no text layer, 5 grades).
Each grade column compared with its own record. Writes decisions/zzzzzzzzzzzzzzzz_b17_family_ehc_purity_premium_sixteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'sixteenth pass, 2026-11-13'
links, F = [], []


def link(pid, f, read, scope, cov, col):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read}; {scope} ({T})', coverage=f'assessed by reading (2026-11-13, sixteenth pass) for {scope}: {cov}',
                      identity=f"exact column header {col!r}", note='Byte duplicate of the cited family table; this product column compared with this record.'))


def row(pid, f, page, old, reason, o, path='open_questions', outcome='in_old_source_not_captured', action='propose_note', form='values as printed in the supplier table (no template field)', tier=1,
        new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', cond='', cmp='existing: not recorded'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=new_text, unit=unit, form=form, qual='as printed', method=method, cond=cond, basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=o, cmp_override=cmp))


# ---------------- ExxonMobil EHC Series DL2-11785 ----------------
oE = f're-read manually: DL2-11785.pdf (ExxonMobil "EHC Series" PDS, printed 4/29/2019, footer 03-2019) pp.1-3 whole text, pp.1-2 also viewed as images ({T})'
E = {'45': 'L0.5', '50': '0.5', '65': 'L0.5', '110': '0.5', '120': '0.5'}
for g, colour in E.items():
    pid = f'EXXONMOBIL_EHC_{g}'
    link(pid, 'DL2-11785.pdf', 'pp.1-3 read in full (text layer; pp.1-2 also viewed as images)', 'the whole document (3 pp.)',
         f"column 'EHC {g}' of the 'Specifications' table (columns Property / Standard Method(a) / Limits): every recorded limit equals the table (KV100 and VI 'Min- Max', pour 'Max', flash COC 'Min', Noack D5800-PROB 'Max' and CCS D5293 'Max' at the printed temperature where printed; blank cells not recorded). The representation of the ranges / limits is already proposed (eleventh / twelfth pass); no new row for it. Not recorded: ASTM Color, Appearance, Notes 1-2, footnote (a) and the p.3 disclaimer -> note.", f'EHC {g}')
    row(pid, 'DL2-11785.pdf', 1, f"DL2-11785.pdf, column 'EHC {g}', prints (not recorded): p.1 'ASTM Color | ASTM D1500 | Max | {colour}'; 'Appearance | Visual | Min- Max | Clear and Bright'. p.2 'Note 1: Products are certified on release to meet the values specified. Actual values may deviate within the established reproducibility of the test method specified.'; 'Note 2: For purpose of determining conformance with specification, observed or calculated values shall be rounded off to the nearest unit in the last significant digit used in expressing the limiting value in accordance to the ASTM E 29 method'; '(a) In lieu of standard test method, alternate test methods may be used for the certification of a product property.' p.3 'Typical values may vary within modest ranges and specifications may be subject to change.'",
        "Old-source items without a template field, and the notes that qualify every recorded limit (certification on release, reproducibility, E 29 rounding, alternate methods). Quoted as printed; 'L0.5' is not interpreted.", oE)

# ---------------- Petro-Canada PURITY VHVI DL2-11261 ----------------
oP = f're-read manually: DL2-11261.pdf (Petro-Canada "PURITY VHVI Specialty Base Fluids", LUB3212E (2015.07)) pp.1-2 whole text and both pages viewed as images ({T})'
P = {'2': ('<0.5', '60', '-42 (-44)', '184 (363)', '185 (365)', "'@ -35°C, cP' 641 only"),
     '3': ('<0.5', '86', '-24 (-11)', '195 (383)', '204 (399)', "'@ -35°C, cP' 1683 only"),
     '4': ('<0.5', '109', '-24 (-11)', '210 (410)', '215 (419)', "'@ -25°C' 990, '@ -30°C' 1621, '@ -35°C' 3250"),
     '6': ('<1.0', '175', '-15 (5)', '225 (437)', '230 (446)', "'@ -20°C' 1550, '@ -25°C' 1998, '@ -30°C' 3560"),
     '8': ('<1.5', '261', '-15 (5)', '242 (468)', '258 (496)', "'@ -20°C' 3291, '@ -25°C' 5894")}
for g, (col, sus, pour, pm, coc, ccs) in P.items():
    pid = f'PETRO_CANADA_PURITY_VHVI_{g}'
    rec = ('the -35 °C entry only is recorded (3250); -25 °C 990 and -30 °C 1621 are NOT recorded -> capture rows' if g == '4' else 'every printed CCS cell is recorded')
    link(pid, 'DL2-11261.pdf', 'pp.1-2 read in full (all 2 pages; both viewed as images)', 'the whole brochure (2 pp.)',
         f"column 'VHVI {g}' of 'TYPICAL PROPERTIES OF PURITY VHVI' (p.2): density @15 °C kg/L, KV40 / KV100, VI, pour D5950, flash COC D92, Noack D5800, saturates / aromatics PCM435 and sulfur D5453 equal the record; CCS D5293 cells as placed on the image: {ccs} ({rec}). Group III from the p.1 text is recorded as a family-level statement. Not recorded: Colour ASTM, SUS @ 100°F, flash PM D93, the °F figures; the JSON printed_text strings are composed (unit appended, °F part omitted) -> note." + (" The p.1 'Benchmarking Results' charts print VHVI 4 figures that differ from the table -> open-question row." if g == '4' else ''), f'VHVI {g}')
    row(pid, 'DL2-11261.pdf', 2, f"DL2-11261.pdf p.2, column 'VHVI {g}' (TYPICAL PROPERTIES), prints (not recorded): 'Colour, ASTM | D1500 | {col}'; 'SUS @ 100°F | D2161 | {sus}'; 'Flash Point, PM, °C (°F) | D93 | {pm}'. The recorded pour point and flash COC are printed '{pour}' and '{coc}' (°C with °F in parentheses); the JSON printed_text gives the °C figure with a unit and omits the °F part.",
        "Old-source items without a template field (colour, SUS, Pensky-Martens flash) preserved as printed. The printed_text strings are not verbatim: propose recording the cells exactly as printed (e.g. the pour cell 'Pour Point, °C (°F) ... " + pour + "'); the recorded values are unchanged. The column heading is 'TYPICAL PROPERTIES'; no limits are printed.", oP)
for t, v in [(-25, '990'), (-30, '1621')]:
    row('PETRO_CANADA_PURITY_VHVI_4', 'DL2-11261.pdf', 2, f"DL2-11261.pdf p.2 (TYPICAL PROPERTIES, COLD CRANK SIMULATOR, '@ {t}°C, cP', D5293), column 'VHVI 4' prints {v}; the record's ccs holds the -35 °C entry (3250) only.",
        f"Old-source typical never captured. Propose an additional ccs entry: {v} cP at {t} °C, ASTM D5293, typical, from the same table as the recorded -35 °C entry (cell position verified on the page image, where the text layer order is ambiguous). Kept as a separate temperature entry; nothing is interpolated.",
        oP, path='ccs', action='capture_from_old_source', form='typical value (brochure Typical Properties table)', new_text=f"'@ {t}°C, cP | D5293 | {v}'", unit='cP', method='D5293', cond=f'{t} °C', cmp='existing: -35 °C entry only')
row('PETRO_CANADA_PURITY_VHVI_4', 'DL2-11261.pdf', 1, "DL2-11261.pdf p.1 'Benchmarking Results' charts print for VHVI 4: 'NOACK, % wt Loss (ASTM D5800)' 12.65; 'Group III – Cold Crank Simulator (ASTM D5293) / Cold Crank Simulation @ -30°C' 1608 (cP) with 'Viscosity @100ºC (cSt)' 4.50; and 'Note: VHVI 4 has a higher Vis100, but a comparable CCS'. The p.2 table (TYPICAL PROPERTIES) prints Noack 12.2, CCS @ -30°C 1621, KV100 4.5; the record holds the table values (Noack 12.2).",
    "Within one document the chart figures for VHVI 4 differ from the table typicals (Noack 12.65 vs 12.2; CCS @ -30 °C 1608 vs 1621); the charts do not state sample, date or basis. Recorded side by side as an open question; not resolved, not averaged, neither preferred. The competitor columns (Comp A-D) are not attributed to any product.",
    oP, action='propose_open_question_update', outcome='additional', form='benchmark chart figure beside the typical-properties table (same document)', new_text="'12.65' (Noack chart); '1608' (CCS @ -30°C chart)", cmp='existing: table values only')

# ---------------- S-OIL PREMIUM SERIES DL2-11173 ----------------
oS = f're-read manually: DL2-11173.pdf (S-OIL "PREMIUM SERIES", 1 page, undated, no text layer) whole page viewed as an image, table at 220 dpi ({T})'
S = {'8': ('P-8 (Premium 60N)', 'L 0.5', '<0.01', '8.4 / 42.5 / 49.1', '77.8', 'limit'), '20': ('P-20 (Premium 100N)', 'L 0.5', '0.01', '2.2 / 29.4 / 68.4', '107.0', 'upper bound'),
     '31': ('P-31 (Premium 150N)', 'L 1.0', '0.01', '1.8 / 32.1 / 66.1', '107.1', 'limit'), '96': ('P-96 (Premium 500N)', 'L 2.0', '0.01', '7.2 / 26.0 / 66.8', '116.3', 'limit'),
     '480': ('P-480 (150BS)', 'L 2.0', '0.20', '7.3 / 21.7 / 71.0', '129.7', 'limit')}
for g, (col, colour, ccr, ring, anil, svk) in S.items():
    pid = f'S_OIL_PREMIUM_P_{g}'
    link(pid, 'DL2-11173.pdf', 'p.1 (only page) read in full (image; no text layer)', 'the whole page (image, table viewed at 220 dpi)',
         f"column {col!r}: Sp.Gravity 15/4 °C D 1298 (recorded as specific_gravity, density Missing), KV40 / KV100 D 445, VI D 2270, flash COC D 92, pour D 5950 and sulfur D 5453 equal the record. The table heading is 'Test Items' / 'ASTM' only: no Typical, Specification, Min or Max label is printed, while the record labels the values 'typical' (sulfur '<' as value_kind '{svk}') -> open-question note. Not recorded: Color ASTM, CCR, copper corrosion, TAN, ring analysis, aniline point -> same note.", col)
    row(pid, 'DL2-11173.pdf', 1, f"DL2-11173.pdf p.1, column {col!r}, prints (not recorded): 'Color, ASTM | D 1500 | {colour}'; 'Carbon Residue (CCR), wt% | D 4530 | {ccr}'; 'Copper Corrosion, 100 °C/3hr | D 130 | 1a'; 'TAN, mgKOH/g | D 974 | <0.01'; 'Ring Analysis, wt% CA / CN / CP | D 3238 | {ring}'; 'Aniline point, °C | D 611 | {anil}'. The table has no value-type label (columns 'Test Items', 'ASTM' and the grade names only); the record's value_kind is 'typical' (sulfur '{svk}').",
        "Old-source items without a template field, preserved as printed ('L 0.5' not interpreted; ring-analysis CA is a carbon-type percentage and is not mapped to aromatics). The page does not say whether the figures are typicals or specifications: propose an open question quoting the headings; no value or value_kind is changed and no limit direction is inferred. The sulfur value_kind differs between grades for the same printed form ('<10' / '<100': 'limit' or 'upper bound'); recorded for the reviewer, not changed.", oS)

d = dict(batch='family tables, batch 17: EHC, PURITY VHVI and S-OIL Premium (sixteenth pass)', reviewed_on='2026-11-13 (sixteenth pass)',
         note='Fifteen duplicate links over three family tables; each read in full and viewed as an image; each grade column compared with its own record.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzz_b17_family_ehc_purity_premium_sixteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
