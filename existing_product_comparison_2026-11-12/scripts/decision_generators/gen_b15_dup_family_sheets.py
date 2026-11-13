"""Fifteenth pass, batch 15: coverage of ten duplicate (category A) links to two one-page family sheets read in full (and viewed as
an image where the heading matters): ADNOC ADbase DL2-12221.pdf (5 grades) and S-OIL Ultra-S DL2-11177.pdf (5 grades). Each grade's
column is compared with that grade's JSON separately. Writes decisions/zzzzzzzzzzzzzzz_b15_dup_family_sheets_fifteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'fifteenth pass, 2026-11-13'
links, F = [], []
oA = f're-read manually: DL2-12221.pdf (ADNOC ADbase family table, 1 page) whole page, text layer and image ({T})'
oS = f're-read manually: DL2-11177.pdf (S-OIL Ultra-S series, 1 page) whole page ({T})'
ADN = {'2CST': '2.3 / 7.5 / 115 / 0.823 / -27 / 170; Noack and CCS printed "-"', '3CST': '3.05 / 12 / 120 / 0.825 / -24 / 190; Noack and CCS "-"',
       '4CST': '4.35 / 20 / 130 / 0.832 / -18 / 220; Noack 12.5; CCS @-30 1400', '6CST': '6.18 / 34 / 137 / 0.844 / -15 / 235; Noack 6.8; CCS @-30 3700',
       '8CST': '8.05 / 49 / 137 / 0.845 / -12 / 255; Noack 3.5; CCS @-30 8000'}
for g, vals in ADN.items():
    pid = f'ADNOC_ADBASE_{g}'
    links.append(dict(p=pid, f='DL2-12221.pdf', cat='A', status='completed', fields_status=f'whole page read (text layer) and viewed as an image ({T})',
                      coverage=f"assessed by reading (2026-11-13, fifteenth pass) for the whole page: column 'ADbase {g}' (KV100 / KV40 / VI / density 15 °C / pour / flash: {vals}; sulfur <3 mg/kg, aromatics <0.2 mass%, saturates 99.8 mass%) equals the JSON, incl. the CCS temperature -30 °C. The page heads the table 'PRODUCT SPECIFICATIONS' with the footnote '*The product specifications listed within the table are all accurate on the date of publishing', while the JSON open questions call these values 'brochure typical' (value_kind 'single') -> open-question row; not resolved.",
                      identity="exact column header 'ADbase " + g + "'", note='Byte duplicate of the cited family table.'))
    F.append(dict(p=pid, tier=1, path='open_questions', old="JSON: value_kind 'single' for every DL2-12221.pdf value; several open questions describe them as 'brochure typical'.", new_f='DL2-12221.pdf', new_p=1,
                  new_text="Page heading 'PRODUCT SPECIFICATIONS' above the table, and footnote '*The product specifications listed within the table are all accurate on the date of publishing.' The table prints one value per grade (no min / max column).",
                  unit='as printed', form='label of the source table as printed (single values under a "product specifications" heading)', qual='as printed', method='', cond='', basis='',
                  outcome='additional', action='propose_open_question_update',
                  reason="The page labels the table 'product specifications' but prints single values without limits; the JSON's neutral value_kind 'single' fits the print, while the open-question wording 'brochure typical' does not. Inspected in full (whole page, text layer and image): the only heading is 'PRODUCT SPECIFICATIONS', the only footnote/disclaimer is the asterisked sentence, and no column prints Min, Max, Typical or a direction (no '<' or '>' except the printed '<3' and '<0.2' values). Propose only rewording the open questions to quote the heading and footnote and to ask ADNOC whether these single values are typicals or specification targets. No value-type correction is proposed: value_kind stays 'single', and no minimum or maximum is inferred where no direction is printed. Not resolved.",
                  old_rev=oA, cmp_override="existing: 'brochure typical' wording in open questions"))
S = {'2': ('0.820', '0.1 / 21.9 / 78.0', '101.8'), '3': ('0.827', '0.2 / 17.3 / 82.5', '111.3'), '4': ('0.834', '0.2 / 17.7 / 82.1', '115.8'),
     '6': ('0.843', '0.2 / 17.3 / 82.5', '119.8'), '8': ('0.847', '0.2 / 20.9 / 78.9', '124.0')}
for g, (sg, ring, anil) in S.items():
    pid = f'S_OIL_ULTRA_S_{g}'
    links.append(dict(p=pid, f='DL2-11177.pdf', cat='A', status='completed', fields_status=f'whole page read (text layer) ({T})',
                      coverage=f"assessed by reading (2026-11-13, fifteenth pass) for the whole page ('Typical Properties' table): column 'Ultra-S {g}' values for SG {sg}, KV40 / KV100, VI, flash (COC), pour, sulfur, saturates (and Noack where printed) equal the JSON" + (" (the pour point printed '-20' is recorded with printed_text '-20.0 °C' -> correction row)" if g == '6' else '') + "; not recorded: appearance, colour Saybolt, CCR, copper corrosion, TAN, ring analysis (D 3238), aniline point, UV absorbance -> note.",
                      identity=f"exact column header 'Ultra-S {g}'", note='Byte duplicate of the cited family table.'))
    F.append(dict(p=pid, tier=1, path='open_questions', old=f"DL2-11177.pdf p.1 'Typical Properties', column 'Ultra-S {g}', prints (not recorded): Appearance (Visual) B & C; Color, Saybolt (D 156) +30; Carbon Residue (CCR) wt% (D 4530) <0.01; Copper Corrosion 100 °C/3hr (D 130) 1a; TAN mgKOH/g (D 974) <0.01; Ring Analysis wt% CA / CN / CP (D 3238) {ring}; Aniline Point °C (D 611) {anil}; UV Absorbance 260-350nm (D 2269) <0.1.",
                  new_f='DL2-11177.pdf', new_p=1, new_text='(same file; byte duplicate in the new archive)', unit='as printed', form='typical values as printed (supplier Typical Properties table)', qual='as printed', method='as printed',
                  cond='', basis='', outcome='in_old_source_not_captured', action='propose_note',
                  reason='Old-source information without a template field. Ring-analysis CA (D 3238) is a carbon-type percentage, not aromatic content by mass, and is not mapped to the aromatics field.', old_rev=oS, cmp_override='existing: not recorded'))
F.append(dict(p='S_OIL_ULTRA_S_6', tier=2, path='pour_point', old="JSON pour_point value -20 with printed_text '-20.0 °C' (DL2-11177.pdf p.1).", new_f='DL2-11177.pdf', new_p=1,
              new_text="Pour Point, °C (D 5950), column 'Ultra-S 6': '-20' (the other columns print one decimal: -37.5, -25.0, -20.0, -15.0)", unit='°C', form='typical value as printed (printed_text fidelity)', qual='as printed', method='ASTM D5950', cond='', basis='',
              outcome='changed_or_conflicting', action='propose_printed_text_correction',
              reason="printed_text must be verbatim: propose '-20' instead of '-20.0 °C'. The value -20 is unchanged; nothing else changes.", old_rev=oS, cmp_override="existing: printed_text '-20.0 °C'"))
d = dict(batch='duplicate coverage, batch 15: ADNOC and S-OIL family sheets (fifteenth pass)', reviewed_on='2026-11-13 (fifteenth pass)',
         note='Ten byte-duplicate links over two one-page family tables; each grade column compared with its own record.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzz_b15_dup_family_sheets_fifteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
