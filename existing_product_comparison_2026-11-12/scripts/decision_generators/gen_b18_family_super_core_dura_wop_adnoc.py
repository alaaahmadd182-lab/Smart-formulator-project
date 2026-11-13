"""Sixteenth pass, batch 18: duplicate (category A) coverage of family tables and single-grade specification images, each read in
full and viewed as an image: S-OIL 'SUPER SERIES' DL2-12392.pdf (3 grades), ExxonMobil 'AP/E CORE' DL2-13265.pdf (2 pp., 4 grades),
Luberef 'SPECIFICATIONS OF BASE OIL' DL2-12173.pdf (3 grades), Chevron 'White Oil Pharmaceutical' DL2-13008.pdf (3 pp., 3 grades) and
the ADNOC 'Product Specification' images DL2-12420.jpg / DL2-12421.jpg / DL2-12468.jpg (one grade each).
Each grade column compared with its own record. Writes decisions/zzzzzzzzzzzzzzzz_b18_family_super_core_dura_wop_adnoc_sixteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'sixteenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, read, scope, cov, col):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read}; {scope} ({T})', coverage=f'assessed by reading (2026-11-14, sixteenth pass) for {scope}: {cov}',
                      identity=f"exact column / grade header {col!r}", note='Byte duplicate of the cited source; this product column compared with this record.'))


def row(pid, f, page, old, reason, o, path='open_questions', outcome='in_old_source_not_captured', action='propose_note', form='values as printed in the supplier table (no template field)', tier=1,
        new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', qual='as printed', cond='', cmp='existing: not recorded'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=new_text, unit=unit, form=form, qual=qual, method=method, cond=cond, basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=o, cmp_override=cmp))


# ---------------- S-OIL SUPER SERIES DL2-12392 ----------------
oS = f're-read manually: DL2-12392.pdf (S-OIL "SUPER SERIES", 1 page, undated) whole page, text layer and image ({T})'
S = {'8': ('S-8 (Super 60N)', '1.6 / 39.4 / 59.0', '84.5', " The pour cell 'L-40.0' is kept Missing with its existing open question and the ninth-pass row; no new row."),
     '31': ('S-31 (Super 150N)', '0.6 / 34.0 / 65.4', '110.8', ''), '96': ('S-96 (Super 500N)', '0.1 / 32.6 / 67.3', "'-'", '')}
for g, (col, ring, anil, extra) in S.items():
    pid = f'S_OIL_SUPER_S_{g}'
    link(pid, 'DL2-12392.pdf', 'p.1 (only page) read in full (text layer and image)', 'the whole page (text layer and image)',
         f"column {col!r}: Sp.Gravity '15/4 °C D 1298' (recorded as specific_gravity; density Missing), KV40 / KV100 D 445, VI D 2270, flash COC D 92, pour D 5950 and sulfur D 5453 '<10' equal the record.{extra} The table heading is 'Test Items' / 'ASTM' only (no Typical / Specification / Min / Max label) while the record labels the values 'typical' -> note. Not recorded: Saybolt colour, CCR, copper corrosion, TAN, ring analysis, aniline point, the series description -> same note.", col)
    row(pid, 'DL2-12392.pdf', 1, f"DL2-12392.pdf p.1, column {col!r}, prints (not recorded): 'Color, Saybolt | D 156 | +30'; 'Carbon Residue (CCR), wt% | D 4530 | <0.01'; 'Copper Corrosion, 100 °C/3hr | D 130 | 1a'; 'TAN, mgKOH/g | D 974 | <0.01'; 'Ring Analysis, wt% CA / CN / CP | D 3238 | {ring}'; 'Aniline point, °C | D 611 | {anil}'; and the description 'Super series base oils are highly purified water-white color products which have low aromatic and high naphthenic content with high viscosity index.' The table has no value-type label; the record's value_kind is 'typical'.",
        "Old-source items without a template field, preserved as printed (ring-analysis CA is a carbon-type percentage, not mapped to aromatics; the description is not a property value). The page does not say whether the figures are typicals or specifications: propose an open question quoting the headings; no value or value_kind is changed and no limit direction is inferred.", oS)

# ---------------- ExxonMobil AP/E CORE DL2-13265 ----------------
oC = f're-read manually: DL2-13265.pdf (ExxonMobil "AP/E CORE", ExxonMobil Basestocks, Italy, 05-2020, printed 17.06.2020) pp.1-2 whole text, p.1 also viewed as an image ({T})'
C = {'100': ('CORE 100', '1', "KV40 'Min-Max 18.5-21.0'; CCS '@ -25 C' 'Max 1,650'; Noack 'Max 29.3'", "ccs printed_text '1650' for the printed '1,650'"),
     '150': ('CORE 150', '1.5', "KV40 'Min-Max 29.0-32.0'; CCS '@ -15 C' 'Max 1,250'; Noack 'Max 15.8'", "kv40 printed_text '29-32' for the printed '29.0-32.0'; ccs printed_text '1250' for '1,250'"),
     '600': ('CORE 600', '4', "KV40 'Min-Max 109.0-116.0'", "kv40 printed_text '109-116' for the printed '109.0-116.0'"),
     '2500': ('CORE 2500', '6', "KV100 'Min-Max 30.6-32.7'", '')}
for g, (col, colour, ranges, pt) in C.items():
    pid = f'EXXONMOBIL_APE_CORE_{g}'
    link(pid, 'DL2-13265.pdf', 'pp.1-2 read in full (all 2 pages; text layer, p.1 also viewed as an image)', 'the whole document (2 pp.)',
         f"column {col!r} of 'Specifications' (Property / Standard Method(a) / Limits): every recorded limit equals the table ({ranges}; flash COC 'Min', pour 'Max', VI 'Min'); blank cells are not recorded. The limits are recorded as value + qualifier 'Min' / 'Max' with value_kind 'single' (not in min / max), kinematic viscosities in 'cSt' for the printed 'mm2/s'" + (f", and {pt}" if pt else '') + " -> representation row. Group I is recorded from the ExxonMobil web page (not this sheet). Not recorded: ASTM Color, Appearance, Notes 1-2, footnote (a), the p.2 disclaimer -> note.", col)
    row(pid, 'DL2-13265.pdf', 1, f"DL2-13265.pdf, column {col!r}, prints (not recorded): p.1 'ASTM Color | ASTM D1500 | Max | {colour}'; 'Appearance | Visual | Min-Max | Clear and Bright'; 'Note 1: Products are certified on release to meet the values specified. Actual values may deviate within the established reproducibility of the test method specified.'; 'Note 2: For purpose of determining conformance with specification, observed or calculated values shall be rounded off to the nearest unit in the last significant digit used in expressing the limiting value in accordance to the ASTM E 29 method'; '(a) In lieu of standard test method, alternate test methods may be used for the certification of a product property.'; edition '05-2020'. p.2 'Typical values may vary within modest ranges and specifications may be subject to change.'",
        "Old-source items without a template field, and the notes that qualify every recorded limit. Quoted as printed.", oC)
    row(pid, 'DL2-13265.pdf', 1, f"Record: the DL2-13265.pdf limits for {col!r} are stored as value + qualifier ('Min' / 'Max'), value_kind 'single', min / max empty; kinematic-viscosity unit 'cSt'" + (f"; {pt}" if pt else '') + '.',
        "The values are captured but not in the agreed form (as for EHC, eleventh / twelfth pass): a printed limit belongs in min or max with its printed direction ('Min', 'Max', 'Min-Max'), ranges stay ranges, the unit is kept as printed ('mm2/s', 'mPa.s') and printed_text holds the cell as printed. Propose a representation correction note; no value changes and nothing is converted.", oC,
        form='specification limits as printed (representation of the recorded entries)', cmp='existing: limits as value + qualifier, value_kind single')

# ---------------- Luberef SPECIFICATIONS OF BASE OIL DL2-12173 ----------------
oD = f're-read manually: DL2-12173.pdf (Luberef "SPECIFICATIONS OF BASE OIL - LUBEREF GI BASE OIL PRODUCTION GUARANTEED SPECIFICATION", 1 page, undated) whole page, text layer and image ({T})'
SHARED = "'Neutralization No | Max. | MG KOH/GM | ASTM-D 664 | 0.05'; 'Copper Strip Corrosion | Max. | 100°C/3 HRS | ASTM-D 130 | 1A'; 'Ash | Max. | WT% | ASTM-D 482 | 0.01'; 'Appearance | - | VISUAL | CLEAR & BRIGHT'; 'Density @ 15°c | ASTM- D 4052 | REPORT'"
for g, col, colour, pm, ccr in [('150_JEDDAH', 'aramcoDURA® 150', '1.5', '200+', '-'), ('500_JEDDAH', 'aramcoDURA® 500', '2.5', '210+', '0.10')]:
    pid = f'ARAMCO_LUBEREF_DURA_{g}'
    link(pid, 'DL2-12173.pdf', 'p.1 (only page) read in full (text layer and image)', 'the whole page (text layer and image)',
         f"'Luberef I – Jeddah Refinery' table, column {col!r}: KV40 'Range 28/31' or '91/101' (as a range), VI 'Min.', pour 'Max.', flash COC 'Min.' (PMCC '{pm}' as an alternate), sulfur 'Max.' WT% D 4294 equal the record; KV100 printed '-' (Missing with an open question). The density, TAN, copper, ash and appearance cells span both Jeddah columns (merged cells on the image). Not recorded: colour, furfural, CCR and the merged rows -> note.", col)
    row(pid, 'DL2-12173.pdf', 1, f"DL2-12173.pdf p.1 ('LUBEREF GI BASE OIL PRODUCTION GUARANTEED SPECIFICATION', 'Luberef I – Jeddah Refinery'), column {col!r}, prints (not recorded): 'Colour | Max. | ASTM-D 1500 | {colour}'; 'Furfural Content | Max. | PPM | M - 1414 | 5'; 'Conradson Carbon Residue | Max. | WT% | ASTM-D 189 | {ccr}'; and, in cells spanning both Jeddah columns, {SHARED}. The viscosity unit is printed 'Cst'.",
        "Old-source items without a template field, preserved as printed. 'REPORT' for density is not a value, consistent with the record's open question. A merged cell is recorded for each of the two grades it spans; nothing is inferred beyond the print.", oD)
pid = 'ARAMCO_LUBEREF_DURA_BS150_YANBU'
link(pid, 'DL2-12173.pdf', 'p.1 (only page) read in full (text layer and image)', 'the whole page (text layer and image)',
     "'Luberef II – Yanbu Refinery' table, column 'aramcoDURA® BS150': only the sulfur 'Max. 1.3 WT%' is recorded from this sheet (with the existing unit conflict against DL2-13944.pdf). The record's KV100 31.32, VI 95, pour -6, flash COC 282 and PMCC 232 come from DL2-13944.pdf; this sheet's guaranteed limits are NOT recorded: KV100 'Range 30/33' Cst, VI 'Min. 95', pour 'Max. -6', flash COC 'Min. 282', PMCC 'Min. 232+' -> alternate-entry rows; colour, furfural, CCR, TAN, copper, ash, appearance, density 'REPORT' -> note.", 'aramcoDURA® BS150')
for path, tier, txt, unit, meth, form in [('kv100', 1, "Viscosity @ 100° c | Range | Cst | ASTM-D 445 | 30/33", 'Cst', 'ASTM-D 445', 'specification range (guaranteed specification; printed 30/33, kept as a range)'),
                                          ('viscosity_index', 1, "Viscosity Index | Min. | - | ASTM-D 2270 | 95", 'dimensionless', 'ASTM-D 2270', 'specification minimum (guaranteed specification)'),
                                          ('pour_point', 2, "Pour Point | Max. | °C | ASTM -D 97 | -6", '°C', 'ASTM -D 97', 'specification maximum (guaranteed specification)'),
                                          ('flash_point', 2, "Flash Point COC | Min. | °C | ASTM-D 92 | 282", '°C', 'ASTM-D 92', 'specification minimum (guaranteed specification, COC)'),
                                          ('flash_point (PMCC)', 2, "Flash Point PMCC | Min. | °C | ASTM-D 93 | 232+", '°C', 'ASTM-D 93', "specification minimum (guaranteed specification, PMCC; printed '232+')")]:
    row(pid, 'DL2-12173.pdf', 1, f"DL2-12173.pdf p.1 ('Luberef II – Yanbu Refinery', column 'aramcoDURA® BS150') prints '{txt}'; the record's {path.split(' ')[0]} holds a DL2-13944.pdf entry only.",
        "Old-source guaranteed-specification limit never captured. Propose an alternate entry with its printed direction and unit, kept separate from the DL2-13944.pdf entry; the two are different value classes (specification limit vs the other document's value), are not compared as a conflict, and neither is preferred or merged. Where the numbers coincide (VI 95, pour -6, flash 282 / 232) that is recorded as printed, not as confirmation." + (" The range is kept as a range; 31.32 lying inside it is only logically compatible." if path == 'kv100' else ''),
        oD, path=path, action='propose_alternate_entry', form=form, tier=tier, new_text=f"'{txt}'", unit=unit, method=meth, qual='as printed (Min. / Max. / Range)', cmp='existing: DL2-13944.pdf entry')
row(pid, 'DL2-12173.pdf', 1, "DL2-12173.pdf p.1 ('Luberef II – Yanbu Refinery', column 'aramcoDURA® BS150') prints (not recorded): 'Colour | Max. | ASTM-D 1500 | 4.0'; 'Furfural Content | Max. | PPM | M - 1414 | 5'; 'Conradson Carbon Residue | Max. | WT% | ASTM-D 189 | 0.70'; " + SHARED + '.',
    "Old-source items without a template field, preserved as printed; 'REPORT' is not a value.", oD)

# ---------------- Chevron White Oil Pharmaceutical DL2-13008 ----------------
oW = f're-read manually: DL2-13008.pdf (Chevron "White Oil Pharmaceutical", EU v6 10 September 2015) pp.1-3 whole text, p.3 table also viewed as an image ({T})'
W = {'40': ('WOP 40', 'VG15', '146184', '32', '0 / 32 / 68'), '70': ('WOP 70', 'VG24', '146679', '60', '0 / 38 / 62'), '240': ('WOP 240', 'VG68', '(146183)', '240', '0 / 32 / 68')}
for g, (col, vg, nsf, kv20, cd) in W.items():
    pid = f'CHEVRON_WOP_{g}'
    link(pid, 'DL2-13008.pdf', 'pp.1-3 read in full (all 3 pages; text layer, the p.3 table also viewed as an image)', 'the whole document (3 pp.)',
         f"column {col!r} of 'Typical test data' (p.3): KV40 / KV100 D445, flash COC D92, pour D5950 and density 15 °C D1298 equal the record; chemistry from the p.1 description is recorded; VI is not printed (Missing). Units printed 'mm²/s' and 'kg/l' are recorded as 'cSt' and 'kg/L'. Not recorded: viscosity grade, NSF registration number, Saybolt colour, odour / acidity / taste / appearance, KV at 20 °C, carbon distribution D2140, shelf life, the table footnote, approvals and handling statements -> note.", col)
    row(pid, 'DL2-13008.pdf', 3, f"DL2-13008.pdf p.3 'Typical test data', column {col!r}, prints (not recorded): 'Viscosity Grade | {vg}'; 'NSF registration nr | {nsf}'; 'Color, Saybolt | ASTM D156 | +30'; 'Odour | Odourless', 'Acidity | Neutral', 'Taste | Tasteless', 'Appearance | Clear and Bright' (cells spanning the three grades); 'Kinematic viscosity at 20°C, mm²/s | ASTM D445 | {kv20}'; 'Carbon distribution,% | ASTM D2140 | CA / CN / Cp {cd}'; 'Shelf Life: 36 months from date of filling indicated on the product label.'; footnote 'The information given in the typical data does not constitute a specification but is an indication based on current production and can be affected by allowable production tolerances.' p.2: approvals 'NSF H1 and NSF HX1', 'Kosher (Parve) & Halal', 'U.S. FDA 21 CFR 178.3620(a), 21 CFR 172.878', USP, NF, BP; 'Not recommended for use in breathing air compressors'; storage 'at room temperature or lower, and not kept in clear glass containers located in direct sunlight'.",
        "Old-source items without a template field, preserved as printed (carbon distribution D2140 is a carbon-type percentage, not mapped to aromatics or saturates; the parenthesised NSF number for WOP 240 is kept with its parentheses and not interpreted). The units differ from the print only in notation; propose keeping the printed unit in printed_text. No value changes.", oW)

# ---------------- ADNOC Product Specification images ----------------
AD = {'4CST': ('DL2-12420.jpg', 'AD Base 4cSt (Group III)', '4.2 / 4.4', '121', '-18', '14.1', "'Max 1800' mPas", "'Replaces | February, 2016', 'Reissued | September, 2016'; handwritten date '27-9-2016'", "'ASTM D6304 or ISO 12937'", True),
      '6CST': ('DL2-12421.jpg', 'AD Base 6cSt (Group III)', '5.8 / 6.2', '125', '-15', '8.0', "'Max 4500' mPas", "'Replaces | February, 2016', 'Reissued | Septemebr, 2016' (spelling as printed); handwritten date '27-9-2016'", "'ASTM D6304 or ISO 12937'", True),
      '8CST': ('DL2-12468.jpg', 'AD Base 8cSt (Group III)', '7.6 / 8.2', '125', '-12', '5.0', "'Report' (no limit; not recorded, correctly)", "'Replaces | None', 'Issued | November, 2016'; stamp 'CONTROLLED COPY'; handwritten date '27-11-2016'", "'ASTM D6304'", False)}
for g, (f, col, kv, vi, pour, noack, ccs, ed, water, cu) in AD.items():
    pid = f'ADNOC_ADBASE_{g}'
    oA = f're-read manually: {f} (ADNOC "Product Specification", Grade "{col}", 1 image) whole image viewed' + (' and enlarged' if g == '8CST' else '') + f' ({T})'
    link(pid, f, 'p.1 (only page) read in full (image; no text layer)', 'the whole image',
         f"grade {col!r}, columns 'Limit' 'Min' / 'Max': the alternate entries equal the image (KV100 {kv} mm²/s, VI Min {vi}, pour Max {pour}, flash COC Min 220, Noack Max {noack} '% M/M' 'ASTM 5800 Method B', sulfur Max 10 mg/kg, CCS at -30 °C {ccs}); Group III from the grade line. Unlike the brochure table DL2-12221.pdf (batch 15), this sheet prints Min / Max columns; that does not settle the batch-15 open question about the brochure values, which stays open. Not recorded: appearance, KV40 'Report', water, Saybolt colour, density / acid no. / carbon residue / saturates / aromatics 'Report'" + (', copper corrosion' if cu else '') + ', edition lines -> note.', col)
    row(pid, f, 1, f"{f} ('Product Specification', Grade '{col}') prints (not recorded): 'Appearance | - | Clear and bright | ASTM D4176-1'; 'Viscosity, Kinematic @40°C | mm²/s | Report | ASTM D445'; 'Water | mg/kg | - | 50 | {water[1:-1]}'; 'Color, Saybolt | - | +20 | - | ASTM D156'; 'Density | g/mL | Report | ASTM D4052'; " + ("'Copper Corrosion, 3hrs at 100°C | - | Report | ASTM D130'; " if cu else '') + f"'Acid No. | mgKOH/g | Report | ASTM D664'; 'Carbon Residue | Report'; 'Saturates | mass % | Report'; 'Aromatics | mass % | Report' (methods 'ASTM D2007, ASTM D7419 or IP 368'); {ed}; signatures 'Sales & Marketing (RPUM)' and the refinery.",
        "Old-source items without a template field, preserved as printed. 'Report' rows carry no value or limit and fill nothing; the Saybolt '+20' sits in the Min column and the water '50' in the Max column, as printed. Edition lines quoted, not interpreted (no edition order is inferred between this sheet and the undated brochure).", oA)

d = dict(batch='family tables, batch 18: S-OIL Super, AP/E CORE, Luberef DURA, Chevron WOP, ADNOC spec images (sixteenth pass)', reviewed_on='2026-11-14 (sixteenth pass)',
         note='Sixteen duplicate links over seven documents; each read in full and viewed as an image; each grade column compared with its own record.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzz_b18_family_super_core_dura_wop_adnoc_sixteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
