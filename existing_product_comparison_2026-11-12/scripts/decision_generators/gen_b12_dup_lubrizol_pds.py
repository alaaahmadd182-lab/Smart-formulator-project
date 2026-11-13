"""Fifteenth pass, batch 12: coverage of six duplicate (category A) links to cited Lubrizol product data sheets, each read in
full (all 3 pages) against the JSON. Writes decisions/zzzzzzzzzzzzzzz_b12_dup_lubrizol_pds_fifteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'fifteenth pass, 2026-11-13'
links, F = [], []


def link(pid, f, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'pp.1-3 read in full in the original ({T})',
                      coverage=f'assessed by reading (2026-11-13, fifteenth pass) for the whole data sheet (3 pp., {ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file', note='Byte duplicate of the cited data sheet.'))


def handling(pid, f, ed, text):
    F.append(dict(p=pid, tier=1, path='open_questions', old=f"{f} (cited, {ed}) p.3 prints (not recorded in the JSON): {text}", new_f=f, new_p=3,
                  new_text='(same file; byte duplicate in the new archive)', unit='as printed', form='data-sheet handling instructions and viscosity data (not property values of a template field)',
                  qual='as printed', method='as printed', cond='unloading / storage / blending', basis='', outcome='in_old_source_not_captured', action='propose_note',
                  reason='Old-source information never captured; no template field. Preserve as printed; the 25 °C viscosity and SUS values are not mapped to any field.',
                  old_rev=f're-read manually: {f} ({ed}) pp.1-3 whole text ({T})', cmp_override='existing: not recorded'))


link('LUBRIZOL_CV1100', 'DL2-11503.pdf', 'Effective: 11/8/2017',
     "every JSON value equals the sheet (claims: 16 in the 14.2 % SAE 15W-40 / 10W-30 block and 3 in the FA-4 block with 2.0 wt% CV6320; the 'API CK-4 / SN claim limited to SAE 15W-40 ... select Group II base oils' line is in the open questions; physical 'Target' and chemical 'Typical' columns with min/max as recorded; IMP gal alternate present). Not recorded: the p.3 handling block and viscosity data -> note.")
handling('LUBRIZOL_CV1100', 'DL2-11503.pdf', 'Effective: 11/8/2017', "'Unloading Pumping Temperature 50oC 122oF Maximum temperature 70oC 158oF Storage Maximum temperature for long-term storage 45oC 113oF Blending Maximum base oil temperature for mechanical or in-line mixing 70oC 158oF'; steam 107 °C max; transfer line 2-3 inch; 'Viscosity data cSt SUS at 25°C,77°F 3714 17183 at 40°C, 104°F 1305 6047 at 100°C, 211°F 80 373'; '* Holding the material in excess of this temperature may cause chemical degradation'; cold storage: heat to 21 °C if stored below the pour point; 'Effective: 11/8/2017'.")
link('LUBRIZOL_CV1103', 'DL2-14978.pdf', 'Published on 11 Jan, 2021',
     "every JSON value equals the sheet (25 claim entries over the two '14.30% by weight' columns with codes A / L / M; typicals with LZ / ASTM methods and footnote '²Not a manufacturing specification'; the FA-4 sentence with 2.0 wt% CV6320 and 'Lubrizol 7077 series' is recorded; its routes were reviewed in Part A). Not recorded: the p.3 handling block -> note.")
handling('LUBRIZOL_CV1103', 'DL2-14978.pdf', 'Published on 11 Jan, 2021', "'Unloading Pumping Temperature 50°C 122°F Maximum Temperature * 70°C 158°F Storage Maximum Temperature for Long-term Storage 45°C 113°F Blending Maximum Base Oil Temperature for Mechanical or in-line Mixing 70°C 158°F'; steam 107 °C max; '* Holding the material in excess of this temperature may cause chemical degradation'; cold storage: heat to 21 °C if stored below the pour point.")
link('LUBRIZOL_CV2601', 'DL2-11702.pdf', 'Effective: 6/16/2016',
     "every JSON value equals the sheet (11 claims of the 15.5 % SAE 10W-40 block; target / typical columns with min/max; B, Ca, Mg, Zn, P, N, sulfated ash; IMP gal alternate). Not recorded: the p.3 handling block and viscosity data -> note.")
handling('LUBRIZOL_CV2601', 'DL2-11702.pdf', 'Effective: 6/16/2016', "'Unloading Pumping Temperature 65oC 149oF Maximum temperature 75oC 167oF Storage Maximum temperature for long-term storage 45oC 113oF Blending Maximum base oil temperature for mechanical or in-line mixing 75oC 167oF'; transfer line 3 inch/8 cm min; 'Viscosity data cSt SUS at 25°C,77°F 11830 54727 at 40°C, 104°F 3800 17607 at 100°C, 211°F 175 816'; degradation and cold-storage statements; 'Effective: 6/16/2016'.")
link('LUBRIZOL_CV3515', 'DL2-15722.pdf', 'Effective: 10/9/2017',
     "every JSON value equals the sheet (10 claims of the 15.45 % SAE 10W-40 block, 'Cummins CES 20078' printed twice and recorded twice; target / typical columns; IMP gal alternate). Not recorded: the p.3 handling block and viscosity data -> note.")
handling('LUBRIZOL_CV3515', 'DL2-15722.pdf', 'Effective: 10/9/2017', "'Unloading Pumping Temperature 50oC 122oF Maximum temperature 70oC 158oF Storage Maximum temperature for long-term storage 45oC 113oF Blending Maximum base oil temperature for mechanical or in-line mixing 70oC 158oF'; 'Viscosity data cSt SUS at 25°C,77°F 3997 18489 at 40°C, 104°F 1347 6241 at 100°C, 211°F 76 355'; degradation and cold-storage statements; 'Effective: 10/9/2017'.")
link('LUBRIZOL_CV7540', 'DL2-15581.pdf', 'Published on 13 May, 2022',
     "every JSON value equals the sheet (18 claims with codes A / L / M; typicals with methods and '²Not a manufacturing specification'; SAE 20W-50 / 15W-40 from the text). The p.3 handling block is covered by the thirteenth-pass note row (its reading statement corrected to this full read). No new row.")
link('LUBRIZOL_CV2301', 'DL2-13065.pdf', 'Effective: 10/24/2017',
     "pp.1-2 claims and characteristics and p.3 compared with the JSON: the 11.7 % (23 claims), 10.7 % (18), 9.1 % (8) and the p.1 8.2 % booster block (7) are recorded; physical / chemical values, ranges and the IMP gal alternate equal the sheet; the p.3 handling block is in the thirteenth-pass note. NOT recorded: the p.2 second 8.2 % block WITHOUT a booster and the sentence 'Not all approvals are possible on a single formulation...' -> capture row.")
F.append(dict(p='LUBRIZOL_CV2301', tier=1, path='treat_rate_matrix', old="DL2-13065.pdf p.2 prints a second block: 'Recommended for use at: 8.2 % by weight When blended with appropriate base oils and viscosity modifier, the formulated lubricant meets the following performance specifications as SAE 15W-40 viscosity grades: ACEA E2-96 Issue 5 (2007) API CG-4 API CF-4 API CF MB-Approval 228.1 MAN 271', followed by 'Not all approvals are possible on a single formulation and some approvals only apply to specific viscosity grades and oil formulations.' The JSON records only the p.1 8.2 % block ('base oils, booster and viscosity modifier'; 7 claims incl. MTU Type 1).",
              new_f='DL2-13065.pdf', new_p=2, new_text='(same file; byte duplicate in the new archive)', unit='% by weight', form='supplier treat-rate block with its claim list (data sheet)', qual='as printed', method='',
              cond='8.2 % by weight, SAE 15W-40, base oils and viscosity modifier only (no booster)', basis='mass % (% by weight)', outcome='in_old_source_not_captured', action='capture_from_old_source',
              reason="Old-source block never captured. Propose a separate route-bound treat-rate entry for the 8.2 % block without a booster (6 claims; MTU Type 1 is NOT in this block), kept apart from the p.1 booster block, plus the printed caveat that not all approvals are possible on a single formulation. Nothing is merged or inferred between the two 8.2 % blocks.",
              old_rev=f're-read manually: DL2-13065.pdf (Effective: 10/24/2017) pp.1-3 whole text ({T})', cmp_override='existing: one 8.2 % block (booster) only'))
d = dict(batch='duplicate coverage, batch 12: cited Lubrizol data sheets (fifteenth pass)', reviewed_on='2026-11-13 (fifteenth pass)',
         note='Six byte-duplicate links; each 3-page data sheet read in full with the JSON beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzz_b12_dup_lubrizol_pds_fifteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
