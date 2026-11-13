"""Seventeenth pass, batch 23: duplicate (category A) coverage of fifteen two-page ExxonMobil SpectraSyn / SpectraSyn Plus / Elite /
Ultra product datasheets, each read in full (text layer; DL2-13746.pdf has its table only as an image and was viewed). Each compared
with its own record. Writes decisions/zzzzzzzzzzzzzzzzz_b23_dup_spectrasyn_seventeenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'seventeenth pass, 2026-11-14'
links, F = [], []
FN2 = "'2 Single sample or two sample average determinations'"


def link(pid, f, ed, cov, read='pp.1-2 read in full (all 2 pages; text layer)'):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})', coverage=f'assessed by reading (2026-11-14, seventeenth pass) for the whole data sheet (2 pp., {ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name on both pages', note='Byte duplicate of the cited data sheet.'))


def row(pid, f, ed, old, reason, path='open_questions', action='propose_note', outcome='in_old_source_not_captured', form='values and statements as printed (no template field)', tier=1,
        new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', qual='as printed', cmp='existing: not recorded', page=1, how='pp.1-2 whole text'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=new_text, unit=unit, form=form, qual=qual, method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({ed}) {how} ({T})', cmp_override=cmp))


S = [  # pid, file, date, footnote-2 rows that are recorded, uncaptured items
    ('2', 'DL2-11328.pdf', '07/30/2015', 'none of the recorded values (the marked rows are not recorded)', "colour < 0.5; KV -40 °C 252 and -54 °C 1263 cSt (marked 2); water < 50 ppm; refractive index 1.4418; TAN < 0.05; Brookfield -40 °C 360 cP; density correction factor 6.73E-4; fire point 176 °C; evaporation loss 75.3 wt% (150 °C, 22 h); vapour pressure 18.0 mm Hg; dielectric constant 2.08 and strength 43.1 kV; aniline point 100.8 °C; 21 CFR 178.3620(b) and NSF H1"),
    ('2B', 'DL2-11330.pdf', 'no revision date printed', 'none', "colour < 0.5; water < 50 ppm; TAN < 0.05; vapour pressure 14.4 mm Hg (marked 2); aniline point 103.7 °C (marked 2); 21 CFR 178.3620(b) and NSF H1. The sheet prints the marker '2' but no footnote text and no revision date"),
    ('2C', 'DL2-11331.pdf', '07/30/2015', 'none', "colour < 0.5; water < 50 ppm; refractive index 1.4400; TAN < 0.05; density correction factor 6.47E-4; aniline point 104.5 °C; Kauri-Butanol 17.6; 21 CFR 178.3620(b) and NSF H1. The sheet prints the marker '2' but no footnote text"),
    ('4', 'DL2-11332.pdf', '07/30/2015', 'CCS -30 / -35 °C 910 / 1424 cP and MRV -40 °C < 5000 cP', "colour < 0.5; KV -40 °C 2900 and -54 °C 14500 cSt; water < 50 ppm; refractive index 1.4535; TAN < 0.05; Brookfield -40 °C 2500 cP; density correction factor 6.41E-4; fire point 256 °C; evaporation loss 1.6 wt%; vapour pressure 0.2 mm Hg; dielectric constant 2.10 / strength 43.6 kV; HTHS 1.46 cP (ASTM D5481); aniline point 119.2 °C; 21 CFR 178.3620(b) and NSF H1"),
    ('5', 'DL2-11333.pdf', '07/30/2015', 'none', "colour < 0.5; KV -40 °C 4920 cSt; water < 50 ppm; TAN < 0.05. The recorded CCS -35 °C 2420 cP and MRV -40 °C 4200 cP rows carry the marker '2', but this sheet prints no footnote text for it (the meaning is not taken from the other sheets)"),
    ('6', 'DL2-11334.pdf', '07/30/2015', 'CCS -30 °C 2260 cP and MRV -40 °C 6500 cP', "colour < 0.5; KV -40 °C 7800 and -54 °C 68500 cSt; water; refractive index 1.4565; TAN; Brookfield -40 °C 7310 cP; density correction factor 6.28E-4; fire point 266 °C; evaporation loss 1.4 wt% (150 °C) and 10.3 wt% (205 °C, 6.5 h); vapour pressure 0.1 mm Hg; dielectric 2.11 / 39.4 kV; HTHS 2.08 cP; aniline point 126.1 °C; Kauri-Butanol 10.9; 21 CFR 178.3620(b) and NSF H1"),
    ('8', 'DL2-11335.pdf', '07/30/2015', 'CCS -30 °C 4800 cP and MRV -40 °C 16200 cP', "colour; KV -40 °C 19000 cSt; water; refractive index 1.4605; TAN; Brookfield -40 °C 17590 cP; density correction factor 6.24E-4; fire point 286 °C; evaporation loss 0.8 / 5.5 wt%; vapour pressure 0.1 mm Hg; dielectric 2.12 / 37.7 kV; HTHS 2.58 cP; aniline point; 21 CFR 178.3620(b) and NSF H1"),
    ('10', 'DL2-11336.pdf', '07/30/2015', 'CCS -30 °C 8840 cP', "colour; KV -40 °C 39000 cSt; water; refractive index 1.4615; TAN; Brookfield -40 °C 36650 cP; density correction factor 6.32E-4; fire point 296 °C; evaporation loss 0.7 wt%; dielectric strength 35.6 kV; aniline point 134.6 °C; Kauri-Butanol 5.0; 21 CFR 178.3620(b) and NSF H1"),
    ('40', 'DL2-11375.pdf', '08/10/2009', 'none', "colour; KV 0 °C 4840 and -20 °C 40500 cSt; water; refractive index 1.4680; TAN < 0.10; Brookfield -26 °C 102000 cP; surface tension 31.5 dyne/cm; density correction factor 6.05E-4; fire point 318 °C; evaporation loss 0.4 / 2.5 wt%; vapour pressure (200 °C) 0.9 mm Hg; 21 CFR 178.3620(b) and NSF H1"),
    ('100', 'DL2-11376.pdf', '08/10/2009', 'none', "colour; KV 0 °C 25100 and -20 °C 250000 cSt; water; refractive index 1.4715; TAN < 0.10; Brookfield -26 °C 745000 cP; surface tension 32.5 dyne/cm; density correction factor 5.97E-4; fire point 330 °C; evaporation loss 0.3 / 2.3 wt%; vapour pressure (200 °C) 0.1 mm Hg; 21 CFR 178.3620(b) and NSF H1"),
    ('ELITE_300', 'DL2-11379.pdf', '05/01/2016', 'none', "appearance; colour < 0.5 (D1500 / D6045); water < 50 ppm; TAN < 0.10; 'Typical values, actual values will vary; Not to be construed as specifications. SpectraSyn Elite sales specification available at www.exxonmobilsynthetics.com'"),
    ('PLUS_3_6', 'DL2-11380.pdf', '06/13/2006', "specific gravity, KV100 / KV40 (row 'Kinematic Viscosity 2'), Noack, CCS -30 / -35 °C 660 / 1050 cP and MRV -40 °C 2060 cP", "colour; KV -40 °C 2000 cSt; water; refractive index 1.4530; TAN < 0.05; Brookfield -40 °C 2117 cP; density correction factor 6.48E-4 (marked 3 'Calculated'); fire point 248 °C; evaporation loss (205 °C) 22.6 wt%; vapour pressure 0.2 mm Hg (marked 3); aniline point 119.0 °C (marked 3)"),
    ('PLUS_4', 'DL2-11381.pdf', '07/17/2007', "specific gravity, KV100 / KV40, Noack, CCS -25 / -30 / -35 °C 733 / 804 / 1290 cP and MRV -40 °C 2023 cP", "colour; KV -40 °C 2430 cSt; water; refractive index 1.4530; TAN; Brookfield -40 °C 2538 cP; density correction factor 6.44E-4 (3); fire point 254 °C; evaporation loss 15.2 wt%; vapour pressure 0.2 mm Hg (3); aniline point 120.0 °C (3); Kauri-Butanol 13.0"),
    ('PLUS_6', 'DL2-11382.pdf', '04/26/2011', "specific gravity, KV100 / KV40, Noack, CCS -30 / -35 °C 2247 / 3600 cP and MRV -40 °C 6243 cP", "colour; KV -40 °C 7400 cSt; water; refractive index 1.4579; TAN; Brookfield -40 °C 6289 cP; density correction factor 6.32E-4 (3); fire point 278 °C; evaporation loss 5.7 wt%; vapour pressure 0.2 mm Hg (3); aniline point 125.0 °C (3)"),
]
for g, f, date, fn2rec, unc in S:
    pid = f'EXXONMOBIL_SPECTRASYN_{g}'
    ed = f'Product Datasheet, Revision Date {date}' if '/' in date else f'Product Datasheet, {date}'
    link(pid, f, ed, "every recorded value (specific gravity 15.6 °C, KV100 / KV40, VI where printed, pour, flash COC, Noack, CCS and MRV where printed, PAO / mPAO chemistry) equals the 'Typical Value (SI)' column; Group IV is recorded from the ExxonMobil web page. "
         + (f"Recorded values carrying the footnote {FN2}: {fn2rec} -> note." if fn2rec not in ('none', 'none of the recorded values (the marked rows are not recorded)') else 'No recorded value carries footnote 2.') + ' Not recorded: the other rows -> note.')
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): {unc}; note 'Typical properties: these are not to be construed as specifications.'"
        + (f" Recorded values marked with footnote {FN2}: {fn2rec}." if fn2rec not in ('none', 'none of the recorded values (the marked rows are not recorded)') else ''),
        'Old-source items without a template field, preserved as printed; nothing is mapped to a field.' + (' The footnote qualifies the marked recorded values (including mandatory CCS where marked): a single sample or a two-sample average. It should travel with them; no value changes.' if fn2rec not in ('none', 'none of the recorded values (the marked rows are not recorded)') else ''))

# SpectraSyn Plus 6: a CCS row printed at a positive temperature
row('EXXONMOBIL_SPECTRASYN_PLUS_6', 'DL2-11382.pdf', 'Product Datasheet, Revision Date 04/26/2011', "Record ccs: -30 °C 2247 cP and -35 °C 3600 cP; no other CCS entry.",
    "The 'Cold Cranking Simulator 2 ASTM D5293' block prints three rows: '77°F (25°C) 1400 cP', '-22°F (-30°C) 2247 cP', '-31°F (-35°C) 3600 cP'. The first row's temperature is printed as +25 °C (77 °F), which is not a usual CCS test temperature; it is recorded as printed and is not corrected to any other temperature, and no CCS entry is created from it. Propose an open question for ExxonMobil.",
    action='propose_open_question_update', outcome='additional', form='CCS row with an unusual printed temperature', new_text="'Cold Cranking Simulator 2 ASTM D5293 77°F (25°C) 1400 cP 1400 cP'", cmp='existing: CCS at -30 / -35 °C only')

# SpectraSyn Ultra 1000, dated 2011 edition (table only as an image)
ed13746 = 'Product datasheet printed Friday, December 23, 2011 (© 2011)'
link('EXXONMOBIL_SPECTRASYN_ULTRA_1000', 'DL2-13746.pdf', ed13746,
     "the record cites this sheet for specific gravity 0.855 only; its other values come from the undated scan DL2-11190.pdf. The image table prints the same typicals (KV100 1000, KV40 10000 mm²/s, VI 307, pour -18 °C, flash COC > 265 °C, Noack 0.3 wt%), so this dated edition can be added as a second source for the mandatory KV100, KV40 and VI -> source-addition rows. Its footnotes are numbered differently from the 2015 sheets ('2 Calculated', '3 Single sample or two sample average determinations') -> note.",
     read='pp.1-2 read in full (all 2 pages; the p.1 table has no text layer and was viewed as an image)')
for path, txt in [('kv100', "'212°F (100°C) 1000 cSt | 1000 mm²/s | ASTM D445'"), ('kv40', "'104°F (40°C) 10000 cSt | 10000 mm²/s'"), ('viscosity_index', "'Viscosity Index 307 | 307 | ASTM D2270'")]:
    row('EXXONMOBIL_SPECTRASYN_ULTRA_1000', 'DL2-13746.pdf', ed13746, f"Record {path} cites only the undated scan DL2-11190.pdf.",
        "Same value and method as the recorded entry, in a dated (2011) manufacturer datasheet. Propose adding it as a second source; the value is unchanged and nothing is selected or merged.",
        path=path, action='propose_source_addition', outcome='already_captured', form='typical value (Typical Value (SI) column; image)', new_text=txt, unit='cSt' if path != 'viscosity_index' else 'dimensionless', method='ASTM D445' if path != 'viscosity_index' else 'ASTM D2270', qual='typical', cmp='existing: same value, undated source only', how='pp.1-2, p.1 viewed as an image')
row('EXXONMOBIL_SPECTRASYN_ULTRA_1000', 'DL2-13746.pdf', ed13746,
    "DL2-13746.pdf prints (not recorded): KV '284°F (140°C) 2' 340 and '32°F (0°C) 2' 100000 mm²/s with footnote '2 Calculated'; Brookfield 0 / -20 °C 170000 / 1940000 cP ('2 Calculated'); refractive index (25 °C) 1.4710, density correction factor 0.000504, evaporation loss 0.5 wt% and Kauri-Butanol 3.2, each marked '3 Single sample or two sample average determinations'; colour 0.5; water < 50 ppm; TAN < 0.10; 21 CFR 178.3620(b) and NSF H1.",
    'Old-source items without a template field, preserved as printed. The calculated viscosities are calculated values, not measurements.', page=1, how='pp.1-2, p.1 viewed as an image')

d = dict(batch='duplicate coverage, batch 23: SpectraSyn product datasheets (seventeenth pass)', reviewed_on='2026-11-14 (seventeenth pass)',
         note='Fifteen byte-duplicate links; each two-page datasheet read in full with the record beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzz_b23_dup_spectrasyn_seventeenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
