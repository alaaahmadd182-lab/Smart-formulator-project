"""Seventeenth pass, batch 21: duplicate (category A) coverage of sixteen one-page base-oil sheets (Ergon, SpectraSyn Elite / Ultra,
YUBASE distributor sheets, PETRONAS EQUINAS 8 / ETRO 4 & 6, Shell Risella X, Luberef DURA BS150), each read in full; image-only pages
viewed. Plus one reviewer-recorded link: the ETRO 4 column of DL2-12475.pdf compared with PETRONAS_ETRO_4.
Writes decisions/zzzzzzzzzzzzzzzzz_b21_dup_onepage_baseoils_seventeenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'seventeenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, ed, cov, read='p.1 (only page) read in full (text layer)', cat='A', ident='SHA-256 equal to the cited archive file; product name on the page', note='Byte duplicate of the cited source.'):
    links.append(dict(p=pid, f=f, cat=cat, status='completed', fields_status=f'{read} ({T})', coverage=f'assessed by reading (2026-11-14, seventeenth pass) for the whole page ({ed}): {cov}',
                      identity=ident, note=note))


def row(pid, f, ed, old, reason, path='open_questions', action='propose_note', outcome='in_old_source_not_captured', form='values and statements as printed (no template field)', tier=1,
        new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', qual='as printed', cond='', cmp='existing: not recorded', read='p.1 whole text'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=1, new_text=new_text, unit=unit, form=form, qual=qual, method=method, cond=cond, basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({ed}) {read} ({T})', cmp_override=cmp))


NOTE = 'Old-source items without a template field, preserved as printed; nothing is mapped to a field.'

# ---------------- Ergon (Marketing Specifications with MIN / MAX / TYPICAL columns) ----------------
E = [('ERGON_HYGOLD_P40', 'DL2-13279.pdf', 'HyGold P40 Marketing Specification, May 9, 2017',
      "SUS 100 °F min 34.0 / max 44.0 / typ 36.9; SUS 210 °F typ 30.3; API gravity 42.5; density 6.777 lbs/gal; 'Flash Point, PMCC, °F (°C) ASTM D93' min 200 (93) / typ 239 (115); 'Color, Saybolt ASTM D6045' 30; water content and appearance PASS / PASS; 'Acid Number, mg KOH/g ASTM D664' max 0.05 / typ 0.01; 'Aniline Point, °F (°C) ASTM D611' 188 (87)"),
     ('ERGON_HYGOLD_P70N', 'DL2-13346.pdf', 'HyGold P70N Marketing Specification, May 9, 2017',
      "SUS 100 °F min 60.0 / max 75.0 / typ 68.8; SUS 210 °F typ 35.9; API gravity 33.8; VGC 0.817 (ASTM D2501); 7.132 lbs/gal; molecular weight 312 (ASTM D2502); 'Flash Point, PMCC' typ 347 (175); 'Color, ASTM ASTM D6045' max 1.5 / typ L0.5; acid number typ 0.01; aniline point min 190 (88) / max 210 (99) / typ 206 (97); 'Polycyclic Aromatic Compounds, wt% IP 346' max 3 / typ <3; 'Modified Ames Assay, MI ASTM E1687' max 1 / typ <1; 'FDA Regulation 21 CFR 178.3620 (C)' PASS"),
     ('ERGON_HY_40', 'DL2-13168.pdf', 'HY 40 Naphthenic Ink Oil Marketing Specification, May 10, 2018',
      "SUS 100 °F min 30.0 / max 40.0 / typ 36.0; SUS 210 °F typ 30.0; API gravity 32.7; 'Flash Point, PMCC' min 200 (93) / typ 208 (98); 'Color, Saybolt' min 20 / typ 29; 'Water Content, ppm ASTM D7546M 120 PASS'; appearance PASS")]
for pid, f, ed, unc in E:
    link(pid, f, ed, "every recorded value equals the MIN / MAX / TYPICAL VALUES columns (KV40 / KV100, density 15.6 °C and specific gravity, VI where printed, pour, flash COC, sulfur, chemistry from the title / description)" + ("; 'Cloud Point, °F (°C) ASTM D5773 10 (-12)' sits in the TYPICAL VALUES column on the image while cloud_point is Missing -> capture row" if pid == 'ERGON_HYGOLD_P70N' else '') + '. Not recorded: SUS, PMCC flash and the other items -> note.',
         read='p.1 (only page) read in full (text layer' + ('; viewed as an image for the column positions)' if pid == 'ERGON_HYGOLD_P70N' else ')'))
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): {unc}.", NOTE)
row('ERGON_HYGOLD_P70N', 'DL2-13346.pdf', 'HyGold P70N Marketing Specification, May 9, 2017', 'Record: cloud_point Missing.',
    "Old-source typical never captured; the figure is in the TYPICAL VALUES column (MIN and MAX cells blank), checked on the page image. Propose capturing it as printed: -12 °C (printed '10 (-12)', °F with °C in brackets), ASTM D5773, typical.",
    path='cloud_point', action='capture_from_old_source', form='typical value (marketing specification, TYPICAL VALUES column)', tier=3, new_text="'Cloud Point, °F (°C) | ASTM D5773 | | | 10 (-12)'", unit='°C (printed °F (°C))', method='ASTM D5773', qual='typical', cmp='existing: Missing')

# ---------------- SpectraSyn Elite / Ultra ----------------
for pid, f, extra in [('EXXONMOBIL_SPECTRASYN_ELITE_150', 'DL2-11378.pdf', ''),
                      ('EXXONMOBIL_SPECTRASYN_ELITE_65', 'DL2-11377.pdf', " Every row of this sheet carries footnote '2 Single sample or two sample average determinations'.")]:
    ed = 'Product Datasheet, Revision / Effective Date 01/07/2015'
    link(pid, f, ed, 'every recorded value (specific gravity 15.6 °C, KV100 / KV40, VI, pour, flash COC, mPAO chemistry) equals the sheet; Group IV is recorded from the ExxonMobil web page.' + extra + " Not recorded: appearance, colour, water, TAN and the notes -> note.")
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): Appearance 'Bright & Clear'; 'Color < 0.5 ASTM D1500/ D6045'; 'Water < 50 ppm ASTM D6304'; 'Total Acid Number < 0.10 mg KOH/g ASTM D974'; note 'Typical properties: these are not to be construed as specifications.'" + (" and footnote '2 Single sample or two sample average determinations' on every property row." if extra else '.'),
        NOTE + (" The footnote qualifies every recorded typical of this product (single sample or a two-sample average) and should travel with them; no value changes." if extra else ''))
for pid, f, g, unc in [('EXXONMOBIL_SPECTRASYN_ULTRA_1000', 'DL2-11190.pdf', '1000', "'Color 0.5 ASTM D1500'; KV '140°C, Calculated 340 mm²/s' and '0°C, Calculated 100000 mm²/s'; 'Water < 50 ppm'; 'Refractive Index (25°C) 1.4710 ASTM D1218'; 'Total Acid Number < 0.10 mg KOH/g ASTM D974 (mod)'; Brookfield 'ASTM D2983' '0°C, Calculated 170000 cP', '-20°C, Calculated 1940000 cP'; 'Density Correction Factor 0.000504 (g/cm³)/°C ASTM D1250'; 'Evaporation Loss (150°C, 22.0 hr) 0.5 wt% ASTM D972'; 'Kauri-Butanol Value 3.2 ASTM D1133'"),
                       ('EXXONMOBIL_SPECTRASYN_ULTRA_300', 'DL2-11197.pdf', '300', "'Color 0.5'; KV '140°C, Calculated 110 mm²/s' and '0°C, Calculated 36000 mm²/s'; 'Water < 50 ppm'; 'Refractive Index (25°C) 1.4707'; TAN '< 0.10 mg KOH/g ASTM D974 (mod)'; Brookfield '0°C, Calculated 37800 cP', '-20°C, Calculated 311000 cP'; 'Density Correction Factor 0.000506 (g/cm³)/°C'; 'Evaporation Loss (150°C, 22.0 hr) 0.3 wt%'")]:
    ed = f'SpectraSyn Ultra {g} sheet, scanned, undated'
    link(pid, f, ed, "every recorded value (KV100 / KV40, VI, pour, flash COC '> 265' as a lower bound, Noack, PAO chemistry) equals the 'Typical Value' column. Not recorded: the calculated viscosities, Brookfield, refractive index and the other items -> note.",
         read='p.1 (only page) read in full (no text layer; viewed as an image)')
    row(pid, f, ed, f"{f} ({ed}; 'Typical Value' column) prints (not recorded): {unc}.", NOTE + " The 'Calculated' viscosities are printed as calculated values and are not measured data.")

# ---------------- YUBASE distributor sheets (NARMAK TRADE s.r.o.) ----------------
Y = {'3': ('DL2-11303.pdf', '0,8299'), '4': ('DL2-11304.pdf', '0,8338'), '5': ('DL2-11305.pdf', '0,8363'), '6': ('DL2-11306.pdf', '0,8423')}
for g, (f, sg) in Y.items():
    pid = f'YUBASE_{g}'
    ed = 'distributor property sheet, NARMAK TRADE s.r.o., undated'
    link(pid, f, ed, f"'BASE OIL YUBASE {g}' (distributor sheet; one 'VALUE' column, no typical / specification label): KV40, KV100, VI, Noack (DIN 51581), flash (D92), pour (D97) and sulfur '< 10' equal the record. The sheet prints 'Specific gravity at 15 °C | g/m3 | {sg} | ASTM D1298' while the record's density is Missing -> open-question row. Not recorded: colour, CCR, copper corrosion, TAN, appearance -> note.",
         ident='SHA-256 equal to the cited archive file; grade name on the page (distributor document)')
    row(pid, f, ed, f"{f} prints (not recorded): Appearance 'Bright & Clear'; 'Color --- L0,5 ASTM D1500'; 'Conradson carbon residue wt % < 0,01 ASTM D189'; 'Copper corrosion --- 1-a ASTM D130'; 'Total acid number mgKOH/g 0,01 ASTM D664'; 'PACKAGE: BULK'.", NOTE)
    row(pid, f, ed, f"Record: density Missing (mandatory Tier 1). {f} prints 'Specific gravity at 15 °C | g/m3 | {sg} | ASTM D1298'.",
        f"The row is labelled 'specific gravity' (dimensionless) but carries the unit 'g/m3', which cannot hold a value of {sg}; the label and the unit cannot both be right, and the issuer is a distributor (NARMAK TRADE s.r.o.), not SK. Propose an open question quoting the row; it is not used to fill density (no unit or basis is established) and nothing is converted.",
        action='propose_open_question_update', outcome='additional', form='distributor value with an inconsistent label and unit', new_text=f"'Specific gravity at 15 °C g/m3 {sg} ASTM D1298'", cmp='existing: density Missing')

# ---------------- PETRONAS ----------------
link('PETRONAS_EQUINAS_8', 'DL2-15279.pdf', 'Product Data Sheet, Version 03-2023',
     "every recorded value equals the 'Specification Value' / 'Typical Value' columns (density 15 °C, KV40 / KV100, VI, pour, flash, Noack, saturates, sulfur, CCS -30 °C, Group III and the process description). Not recorded: appearance and colour ('L 0.5 Max' / 'L 0.5') -> note.")
row('PETRONAS_EQUINAS_8', 'DL2-15279.pdf', 'Version 03-2023', "DL2-15279.pdf prints (not recorded): Appearance 'Bright & Clear' (specification and typical); 'Colour ASTM D 1500 | L 0.5 Max | L 0.5'.", NOTE)
ed6 = "Technical Data Sheet 'ETRO 4 & ETRO 6 GROUP III BASE OIL', undated, scanned"
link('PETRONAS_ETRO_6', 'DL2-12475.pdf', ed6,
     "column 'ETRO 6' (Specification / Typical value): KV100 6.00 – 6.50 / 6.10, VI ≥ 125 / 133, pour ≤ -15 / -18, flash > 220 / 230, Noack ≤ 8 / 7.1, saturates > 95 / 99, sulfur < 30 / 5, CCS 2,088 / 3,977 / 7,422 at -25 / -30 / -35 °C equal the record. Not recorded: appearance, colour, 'Formulation Support' -> note.",
     read='p.1 (only page) read in full (no text layer; viewed as an image)', ident="exact column header 'ETRO 6'")
row('PETRONAS_ETRO_6', 'DL2-12475.pdf', ed6, "DL2-12475.pdf column 'ETRO 6' prints (not recorded): Appearance 'Bright & Clear'; 'Colour ASTM D1500 | L 0.5 max | L 0.5'; and for both grades 'ETRO 4 & ETRO 6 are supported with top-tier engine oil formulations that meet: API SM, ILSAC GF-4, ACEA 2008'.",
    NOTE + " The formulation-support line names no package, dose or route and is not a co-component statement.", read='p.1 viewed as an image')
# reviewer-recorded link: ETRO 4 column
link('PETRONAS_ETRO_4', 'DL2-12475.pdf', ed6,
     "column 'ETRO 4', compared with the record (whose values come from DL2-10230.pdf): the existing unresolved conflict EVR-2026-11-10-ETRO4 already records KV100 4.26, VI 130 and CCS 886 / 1,442 / 2,419, and these equal the image. Not in that conflict: Noack '< 15' / 14.9 (record 13.8), sulfur '< 30' / 5 (record 4), and the flash specification printed '≤ 200' (record ≥ 200 from DL2-10230.pdf) -> conflict / open-question rows. The record's open question 'Supplementary DL2-12475.pdf is image-only and has not been independently reconciled' -> update row.",
     read='p.1 (only page) read in full (no text layer; viewed as an image)', cat='D', ident="exact column header 'ETRO 4' (image-only sheet; the automated search could not pair it)",
     note='Reviewer-recorded link: the sheet names ETRO 4 beside ETRO 6.')
for path, tier, txt, rec, unit, meth in [('noack_volatility', 2, "'Noack Volatility | ASTM D5800(b) | wt% | < 15 | 14.9'", '13.8 mass% (DL2-10230.pdf)', 'wt%', 'ASTM D5800(b)'),
                                         ('sulfur', 3, "'Sulphur Content | ASTM D2622 | ppm | < 30 | 5'", '4 mg/kg (DL2-10230.pdf)', 'ppm', 'ASTM D2622')]:
    row('PETRONAS_ETRO_4', 'DL2-12475.pdf', ed6, f"Record {path}: typical {rec}; the image sheet's ETRO 4 column prints a different typical.",
        "Two undated PETRONAS technical sheets print different typicals for ETRO 4. Propose adding this property to the existing unresolved conflict EVR-2026-11-10-ETRO4 with both values and sources; not averaged, no edition order assumed, the record keeps its value.",
        path=path, action='propose_record_conflict', outcome='changed_or_conflicting', form='typical value (technical data sheet, Typical value column; image)', tier=tier, new_text=txt, unit=unit, method=meth, qual='typical', cmp=f'existing: {rec}', read='p.1 viewed as an image')
row('PETRONAS_ETRO_4', 'DL2-12475.pdf', ed6, "Record flash_point: specification ≥ 200 °C (DL2-10230.pdf); the open question says DL2-12475.pdf 'is image-only and has not been independently reconciled'.",
    "The image sheet (read in full on this pass) prints the ETRO 4 flash specification as '≤ 200' (typical 220), while the ETRO 6 column prints '> 220' and DL2-10230.pdf prints a minimum. The direction is recorded as printed; no corrected direction is inferred. Propose updating the open question: DL2-12475.pdf has now been read (all values listed in EVR-2026-11-10-ETRO4 and the two new conflict rows), and the '≤ 200' printing is an open question for PETRONAS.",
    action='propose_open_question_update', outcome='additional', form='specification limit with its printed direction (image)', new_text="'Flash Point | ASTM D92 | °C | ≤ 200 | 220' (column ETRO 4)", cmp="existing: 'not independently reconciled'", read='p.1 viewed as an image')

# ---------------- Shell Risella X ----------------
for pid, f, g, unc in [('SHELL_RISELLA_X_420', 'DL2-13726.pdf', '420', "'Colour (Saybolt) ASTM D156 +30'; 'Refractive Index @ 20 0C ASTM D1218 1.454'; 'Kinematic Viscosity @ 20 0C mm 2/s ISO 3104 40'; 'Aniline Point 0C ISO 2977 120'; 'Evaporation Loss 22h/107 0C %m ASTM D972 0.12'; 'Purity Requirements for Technical White Oil FDA 178.3620 (b) Pass'"),
                       ('SHELL_RISELLA_X_430', 'DL2-13727.pdf', '430', "'Colour (Saybolt) +30'; 'Refractive Index @ 20 0C 1.460'; 'Kinematic Viscosity @ 20 0C 111'; 'Aniline Point 0C >130'; 'Evaporation Loss 22h/107 0C %m 0.1'; 'FDA 178.3620 (b) Pass'")]:
    ed = f'Technical Data Sheet Shell Risella X {g}, v 2.1 02.06.2014'
    link(pid, f, ed, "every recorded value (density 15 °C, VI, flash COC, pour, KV40 / KV100, sulfur '<5', Noack, GtL chemistry) equals the 'Typical Physical Characteristics' table; the density difference with the SDS is an existing unresolved conflict. Not recorded: Saybolt colour, refractive index, KV20, aniline point, evaporation loss, FDA statement -> note.")
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): {unc}; and 'These characteristics are typical of current production. Whilst future production will conform to Shell's specification, variations in these characteristics may occur.'", NOTE)

# ---------------- Luberef DURA BS150 Yanbu ----------------
ed13944 = "Luberef 'Typical' Group I Yanbu sheet, undated"
link('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-13944.pdf', ed13944,
     "column 'BS150' ('Typical', 'Group I', 'Yanbu'): KV100 31.32, VI 95, density 15.6 °C 0.894, flash COC 282 (PMCC 232 as an alternate), Group I equal the record; sulfur '1.3‡' is in the existing unit conflict. The pour point is printed '-6*' with the note '* - D 97' while the record carries the column method 'ASTM D5950' -> correction row. Not recorded: KV40 'Report', colour, furfural, copper, CCR, TAN, appearance -> note.")
row('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-13944.pdf', ed13944,
    "DL2-13944.pdf prints (not recorded): Appearance 'C & B'; 'Kinematic Viscosity @ 400C | ASTM D445 | Report'; 'Color, ASTM | ASTM D1500 | 4.0'; 'Furfural Content | M - 1414 | ppm | 5'; 'Copper Strip Corrosion, 1000C, 3 hrs | ASTM D130 | 1a'; 'Conradson Carbon Residue | ASTM D4530 | wt% | 0.7'; 'Total Acid Number | ASTM D974 | mgKOH/g | 0.05'.", NOTE)
row('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-13944.pdf', ed13944, "Record pour_point -6 °C, method 'ASTM D5950', printed_text '-6' (DL2-13944.pdf p.1).",
    "The method column prints ASTM D5950 for the pour row, but the value is printed '-6*' and the sheet's note reads '* - D 97'. Propose keeping the printed text with its asterisk ('-6*') and recording the method as printed, i.e. the column method together with the footnote ('ASTM D5950; footnote * - D 97'), so that the D 97 qualification is not lost. The value -6 is unchanged; which method was used is not decided here.",
    path='pour_point', action='propose_printed_text_correction', outcome='changed_or_conflicting', form='typical value as printed (printed_text and method fidelity)', tier=2,
    new_text="'Pour Point | °C | ASTM D5950 | -6*'; 'Notes: * - D 97 | ‡ - D 2622'", unit='°C', method='ASTM D5950 with footnote * - D 97', qual='typical', cmp="existing: printed_text '-6', method 'ASTM D5950'")

d = dict(batch='duplicate coverage, batch 21: one-page base-oil sheets (seventeenth pass)', reviewed_on='2026-11-14 (seventeenth pass)',
         note='Sixteen byte-duplicate links and one reviewer-recorded link; each page read in full (image-only pages viewed) with the record beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzz_b21_dup_onepage_baseoils_seventeenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
