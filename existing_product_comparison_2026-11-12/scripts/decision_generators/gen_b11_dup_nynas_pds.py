"""Fourteenth pass, batch 11: coverage of 14 duplicate (category A) links to cited Nynas product data sheets. Each sheet read in
full in the original (text layer; DL2-12370 / DL2-12371 have no text layer and were viewed as images). Every value in the JSON
equals the sheet; items without a template field are proposed as notes where the JSON does not already list them.
Writes decisions/zzzzzzzzzzzzzz_b11_dup_nynas_pds_fourteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'fourteenth pass, 2026-11-13'
links, F = [], []
CT = 'carbon-type percentages (IR method / ASTM D2140) are not aromatic content by mass and are not mapped to the aromatics field'
# pid, file, pages, edition, JSON-equal summary, uncaptured (None = already listed in the JSON / earlier rows), extra note
D = [
 ('NYNAS_BASE_STOCK_20', 'DL2-13010.pdf', 1, 'Issuing date: 2017-05-10', 'density 0.899, KV40 12-19 / 16, KV100 3.1, PM flash min 136 / 147, pour max -39 / -54, sulphur <0.01 %',
  "Viscosity, 100°F SUS D 2161 '807' (printed as such; no corrected figure inferred); Copper Strip 3 hrs D 130 max 1 / 1; Aniline Point D 611 73-83 / 78; Refractive Index 20 °C D 1747 1.487; Colour D 1500 max 0.5 / <0.5; TAN D 974 max 0.03 / <0.01; IR-method CA 8 %; D 2140 CA 8 / CN 50 / CP 42 %; Appearance D 4176 clear and bright; DMSO extractible IP 346 max 3.0 / <3.0 wt %; 'Severely Hydrotreated Base Oil'; issuing date 2017-05-10"),
 ('NYNAS_BNS_5', 'DL2-13442.pdf', 1, 'Issuing date: 2017-10-04', 'density 0.871, KV40 5-5.5 / 5.0, PM flash 114, pour -66, sulphur <0.01 %',
  "Aniline point D 611 73; Refractive Index 20 °C D 1747 1.474; Viscosity-Gravity-Constant D 2501 0; Colour Saybolt D 156 30; Colour D 1500 <0.5; TAN D 974 <0.01; IR-method CA 6 %; D 2140 CA / CN / CP 'N/A'; Appearance clear and bright; DMSO extractable IP 346 <3.0 %; issuing date 2017-10-04; footer 'BC: 11:10:0'"),
 ('NYNAS_NYBASE_70', 'DL2-13344.pdf', 2, 'Issuing Date: 04-15-2020', 'density 0.853-0.873 / 0.862, KV40 12.5-15.5 / 14, KV100 3.2, VI 85, COC 145 min / 184 (PM 170 in printed_text), Noack 60, pour max -18 / -27, sulphur max 2000 / <100 ppm',
  "Viscosity, 100°F SUS ASTM D2161 74; Copper Strip 100 °C 3 hrs max 1; Aniline Point ASTM D611 97; Colour D1500 max 0.5 / <0.5; TAN D974 <0.01; IR-method Ca 2 %; ASTM D2140 Ca <1 / Cn 40 / Cp 59 %; Appearance clear and bright; DMSO extractible IP 346 <3.0 / <3.0 wt %; issuing date 04-15-2020; p.1 'suitable for the replacement of Group I base oils' and the aniline point 'matches well the values found in other Solvent Neutral 70 Group I base oils'"),
 ('NYNAS_NYFROST_68', 'DL2-11747.pdf', 1, 'Issuing date: 30/09/2014', 'density 0.904-0.924 / 0.912, KV40 61.2-74.8 / 69, KV100 6.6, PM flash min 174 / 192, pour max -24 / -36, sulphur 0.06 %',
  "Flash Point COC D 92 200; Colour D 1500 max 1.5 / <1.0; Floc point R12 DIN 51351 -29 °C; Copper Strip 100 °C 3 hrs max 1 / 1; Neutralization value D 974 max 0.03 / <0.01; IR-method CA 15 %; D 2140 CA 11 / CN 40 / CP 49 %; Breakdown voltage IEC 156 min 40 / >45 kV; 'Nyfrost 68 is a naphthenic based refrigerating oil meeting specification BS 2626: 1992'; issuing date 30/09/2014"),
 ('NYNAS_NYFROST_100', 'DL2-12383 (1).pdf', 2, 'Issuing date: 2016-11-01', 'density 0.896-0.916 / 0.905, KV40 90.0-110 / 98, KV100 8.8, PM flash min 204 / 216, pour max -15 / -30, sulphur 0.03 %, Group V / hydrotreated naphthenic',
  "Flash Point COC D 92 220; Colour D 1500 max 1.0 / <1.0; Floc point R12 DIN 51351 -24 °C; Floc point R600A DIN 51351 -50 °C (R22 and U-tube rows blank); Copper Strip 100 °C 3 hrs max 1 / 1; Neutralization value D 974 max 0.03 / <0.01; IR-method CA 10 %; Carbon-type CA 7 / CN 40 / CP 53 %; Breakdown voltage IEC 156 >45 kV; 'meeting specification BS 2626: 1992'; issuing date 2016-11-01; p.1 refrigerants named (R600a, R717, R12, R22)"),
 ('NYNAS_T_3', 'DL2-15475.pdf', 2, 'Issuing date: 30-05-2024', 'density 0.857-0.877 / 0.868, KV40 3.2-4.2 / 3.75, KV100 1.3, PM flash min 101 / 104, pour max -60 / < -70, sulphur < 10 ppm, Group V',
  "Viscosity, 100°F SUS ASTM D2161 38.6; Copper Strip 100 °C 3 hrs max 1 / 1; Aniline Point ASTM D611 64-72 / 69; Colour Saybolt ASTM D156 min +15 / +30; Colour D1500 <0.5; TAN D974 max 0.03 / <0.01; IR-method Ca 6 %; ASTM D2140 N/A; Appearance clear and bright; DMSO extractible IP 346 <3.0 / <3.0 wt %; issuing date 30-05-2024"),
 ('NYNAS_T_4', 'DL2-12381.pdf', 2, 'Issuing date: 2012-08-21', 'density 0.880-0.900 / 0.892, KV40 4.0-5.0 / 4.5, KV100 1.6, PM flash min 110 / 118, pour max -60 / <-70, sulphur <0.01 %, Group V',
  "Viscosity, 100°F SUS D 2161 42; Copper Strip 3 hrs max 1 / 1; Aniline Point D 611 57-63 / 60; Refractive Index 20 °C D 1747 1.484; Colour Saybolt D 156 min +15 / +23; Colour D 1500 <0.5; TAN D 974 max 0.03 / <0.01; IR-method CA 9 %; D 2140 CA 7 / CN 59 / CP 34 %; Appearance clear and bright; DMSO IP 346 'NA'; issuing date 2012-08-21; p.1 'The T 4 vapour pressure at 20°C (ASTM E 1194-01) is 1 Pa which is 10 times lower than threshold level for VOC (volatile organic compound) as set by EU 1999/13/EC directive'"),
 ('NYNAS_T_600', 'DL2-13009.pdf', 2, 'Issuing date: 2018-03-19', 'density 0.920-0.940 / 0.932, KV40 540-640 / 580, KV100 21, PM flash min 240 / 250, pour max 0 / -12, sulphur 0.30 %, Group V',
  "Viscosity, 100°F SUS D 2161 3245; Flash Point COC D 92 >250; Copper Strip 3 hrs max 1 / 1; Aniline Point D 611 85-93 / 89; Refractive Index 20 °C D 1747 1.512; Colour D 1500 max 4.0 / <2.5; TAN D 974 max 0.03 / <0.01; IR-method CA 20 %; D 2140 CA 15 / CN 33 / CP 52 %; Appearance clear and bright; DMSO IP 346 max 3.0 / <3.0 wt %; issuing date 2018-03-19"),
 ('NYNAS_T_9', 'DL2-13356.pdf', 2, 'Issuing Date: 01-30-2020', 'density 0.880-0.899 / 0.889, KV40 8.0-10.0 / 8.9, KV100 2.2, PM flash min 140 / 146, pour max -45 / -57, sulphur 200 ppm, Group V',
  "Viscosity, 100°F SUS ASTM D2161 57; Copper Strip 100 °C 3 hrs max 1 / 1; Aniline Point ASTM D611 62-74 / 70; Colour D1500 max 0.5 / <0.5; TAN D974 max 0.03 / <0.01; IR-method Ca 14 %; ASTM D2140 Ca 9 / Cn 44 / Cp 47 %; Appearance clear and bright; DMSO IP 346 <3.0 / <3.0 wt %; footer 'Severly Hydrotreated Base Oil' (spelling as printed); issuing date 01-30-2020"),
 ('NYNAS_NS_3', 'DL2-15474.pdf', 2, 'Issuing date: 30-05-2024', 'density 0.850-0.875 / 0.863, KV40 2.7-3.1 / 2.92, PM flash min 90 / 95, pour max -60 / < -70, sulfur < 10 ppm, Group V (read in full in the thirteenth pass, batch 3)',
  "Viscosity, 100°F SUS ASTM D2161 36; Copper Strip 100 °C 3 hrs max 1 / 1; Aniline Point ASTM D611 61-69 / 65; Colour Saybolt ASTM D156 min +15 / +30; Colour D1500 <0.5; TAN D974 max 0.03 / <0.01; IR-method Ca 6 %; ASTM D2140 N/A; Appearance clear and bright; DMSO IP 346 N/A; KV100 printed 'N/A'; issuing date 30-05-2024 (the 2016 edition's extra items are in the batch-3 note)"),
 ('NYNAS_T_110', 'DL2-12370.pdf', 1, 'no date printed', 'density 0,910-0,925 / 0,920, KV40 100-120 / 114, KV100 8,5, PM flash min 206 / 212, pour max -15 / -30, sulphur 0.06 % (viewed as an image; no text layer)', None),
 ('NYNAS_T_22', 'DL2-12371.pdf', 1, 'Issuing date: 2012-08-10', 'density 0.895-0.910 / 0.902, KV40 20.5-25 / 22.3, KV100 3.7, PM flash min 164 / 174, pour max -33 / -45, sulphur 0.06 % (viewed as an image; no text layer)', None),
 ('NYNAS_NYFROST_32', 'DL2-11510.pdf', 2, 'Issuing date: 2016-11-01', 'all JSON values equal the sheet (read in full in the thirteenth pass, batch 3)', 'BATCH3'),
 ('NYNAS_S_3B', 'DL2-12819.pdf', 2, 'Issuing date: 2019-05-29', 'all JSON values equal the sheet (read in full in the thirteenth pass, batch 3)', 'BATCH3'),
]
for pid, f, n, ed, eq, unc in D:
    if unc is None:
        tail = "the JSON open question 'Printed properties with no template field' already lists every remaining printed item (checked against the page image: SUS, copper strip, aniline point, refractive index, colour, TAN, appearance, DMSO IP 346; the IR / D 2140 carbon types are in the tier-3 open question). No new row."
    elif unc == 'BATCH3':
        tail = "uncaptured items were listed in the thirteenth-pass batch-3 rows (decisions/zzzzzzzzzzzzz_b3_nynas_purity_nexbase_thirteenth_pass.json). No new row."
    else:
        tail = "the items without a template field are not listed in the JSON -> note row."
        F.append(dict(p=pid, tier=1, path='open_questions', old=f"{f} (cited, {ed}) prints items the JSON does not record: {unc}.", new_f=f, new_p=n, new_text='(same file; byte duplicate in the new archive)',
                      unit='as printed', form='typical data and specification limits as printed (data sheet)', qual='as printed', method='as printed', cond='', basis='',
                      outcome='in_old_source_not_captured', action='propose_note',
                      reason=f'Old-source information without a template field. Propose preserving it with methods, limits and edition; {CT}; nothing is corrected or converted.',
                      old_rev=f're-read manually: {f} ({ed}) pp.1-{n} whole text ({T})', cmp_override='existing: not recorded'))
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f"pp.1-{n} read in full in the original ({T}{'; page image' if 'image' in eq else ''})",
                      coverage=f"assessed by reading (2026-11-13, fourteenth pass) for the whole data sheet ({n} p., {ed}): JSON values equal the sheet ({eq}); {tail}",
                      identity='SHA-256 equal to the cited archive file', note='Byte duplicate of the cited data sheet.'))
d = dict(batch='duplicate coverage, batch 11: cited Nynas data sheets (fourteenth pass)', reviewed_on='2026-11-13 (fourteenth pass)',
         note='Coverage of 14 byte-duplicate links; each data sheet read in full in the original with the JSON summary beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzz_b11_dup_nynas_pds_fourteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
