"""Sixteenth pass, batch 16: duplicate (category A) coverage of three family tables, each read in full and viewed as an image:
GS Caltex 'Product specification' DL2-13094.pdf (7 grades), aramcoPRIMA brochure 'Group II' table DL2-11773.pdf (6 linked grades;
no text layer) and 'LUBEREF GII Product Specifications*' DL2-12172.pdf (4 grades). Each grade column compared with its own record.
Writes decisions/zzzzzzzzzzzzzzzz_b16_family_gscaltex_aramco_sixteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'sixteenth pass, 2026-11-13'
links, F = [], []


def link(pid, f, scope, cov, col):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'p.1 (only page) read in full; {scope} ({T})', coverage=f'assessed by reading (2026-11-13, sixteenth pass) for {scope}: {cov}',
                      identity=f"exact column header {col!r}", note='Byte duplicate of the cited family table; this product column compared with this record.'))


def note(pid, f, old, reason, o, path='open_questions', outcome='in_old_source_not_captured', action='propose_note', form='values as printed in the supplier table (no template field)', tier=1, new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', cmp='existing: not recorded'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=1, new_text=new_text, unit=unit, form=form, qual='as printed', method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=o, cmp_override=cmp))


# ---------------- GS Caltex DL2-13094 ----------------
oG = f're-read manually: DL2-13094.pdf (GS Caltex "Product specification", 1 page, undated) whole page, text layer and image ({T})'
G = {'60N': ('Gr.I 60N', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.05 / 0.004'), '150N': ('150N', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.01 / 0.004'),
     '220N': ('220N', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.01 / 0.003'), '600N': ('600N', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.01 / 0.004'),
     '2CST_L': ('2cSt_L', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.01 / 0.005'), '2CST_H': ('2cst_H', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', 'Max 0.01 / 0.003'),
     '150BS': ('150BS', 'Max 0.5 / L0.5', 'Max 0.01 / L0.01', None)}
for g, (col, colour, ccr, tan) in G.items():
    pid = f'GS_CALTEX_{g}'
    link(pid, 'DL2-13094.pdf', 'the whole page (text layer and image)',
         f"column {col!r} (Spec. / Typical): every recorded value and limit equals the table (KV40, KV100, VI, pour D6749, flash COC D92, Noack and aromatics D3238 where printed; blank Spec. cells and the 600N KV40 Spec. '-' are recorded as printed; group heading {'Gr.I' if g == '60N' else 'Gr.II'}). Not recorded: ASTM Color, CCR" + (', TAN' if tan else '') + ' -> note.', col)
    note(pid, 'DL2-13094.pdf', f"DL2-13094.pdf p.1, column {col!r}, prints (not recorded): ASTM Color (ASTM D1500) Spec. / Typical {colour}; CCR (ASTM D189, wt%) {ccr}" + (f"; TAN (ASTM D974, mgKOH/g) {tan}" if tan else '; the TAN cells are blank for this column') + '.',
         "Old-source items without a template field. 'L0.5' and 'L0.01' are quoted exactly as printed; their meaning is not interpreted.", oG)

# ---------------- aramcoPRIMA brochure DL2-11773 ----------------
oA = f're-read manually: DL2-11773.pdf (aramcoPRIMA brochure "Group II" table, printed pages 8-9, no text layer) whole page viewed as an image ({T})'
FOOT = "footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.' (applies to the starred columns 110*, 230*, 500L* only)"
A = {'100': ('aramcoPRIMA 100', "Brookfield @ -40°C (D 2983) 12,500; Color ASTM (D 1500) L 0.5; Copper Corrosion 100°C 3hrs (D 130) 1a; Tan mgKOH/gm (D 974) 0.01; Appearance C&B"),
     '150': ('aramcoPRIMA 150', "Saybolt Color (D 156) +30; Color ASTM L 0.5; Copper Corrosion 1b; Tan < 0.01; Appearance C&B"),
     '220': ('aramcoPRIMA 220', "Color ASTM L 0.5; Appearance C&B (copper corrosion, TAN and saturates cells blank)"),
     '500L': ('aramcoPRIMA 500L*', "Color ASTM L 0.5; Copper Corrosion 1b; Tan 0.02; Appearance C&B (under the '*' footnote)"),
     '600': ('aramcoPRIMA 600', "Color ASTM L 0.5; Copper Corrosion 1b; Tan 0.02; Appearance C&B (Noack cell blank)")}
for g, (col, unc) in A.items():
    pid = f'ARAMCO_LUBEREF_PRIMA_{g}'
    link(pid, 'DL2-11773.pdf', 'the whole page (image; no text layer)',
         f"column {col!r} ('Typical'): every recorded value equals the table (KV40, KV100, VI, density 15 °C Kg/L, CCS at the printed temperatures, Noack D 5800 (B), pour, flash COC, sulfur, saturates and aromatics where printed); {FOOT}. Not recorded: {unc} -> note.", col)
    note(pid, 'DL2-11773.pdf', f"DL2-11773.pdf p.1, column {col!r} (Typical), prints (not recorded): {unc}.", "Old-source items without a template field; quoted as printed ('L 0.5' not interpreted).", oA)
link('ARAMCO_LUBEREF_PRIMA_500', 'DL2-11773.pdf', 'the whole page (image; no text layer)',
     "column 'aramcoPRIMA 500' (Typical; no '*'): KV40 96.4 and CCS 14,550 (-20 °C) / 26,000 (-25 °C) are recorded from it; the density 0.8720 is in the existing unresolved discrepancy with DL2-12172.pdf 0.867. NOT recorded: KV100 11.3, VI 104, Saturates 99, Sulfur 2, Noack 6.9, Pour -18, Flash COC 240, Aromatic < 1, Saybolt +30, Color L0.5, Copper 1b, Tan < 0.01 (the record's other fields hold the DL2-12172.pdf specification limits) -> alternate-entry, capture and open-question rows.", 'aramcoPRIMA 500')
for path, tier, txt, unit, meth in [('kv100', 1, 'Kinematic Viscosity @ 100°C, cSt (D 445): 11.3', 'cSt', 'D 445'), ('viscosity_index', 1, 'Viscosity Index (D 2270): 104', 'dimensionless', 'D 2270'),
                                    ('noack_volatility', 2, 'Noack Volatility, wt% (D 5800 (B)): 6.9', 'wt%', 'D 5800 (B)'), ('pour_point', 2, 'Pour Point, °C (D 97): -18', '°C', 'D 97'),
                                    ('flash_point', 2, 'Flash Point COC, °C (D 92): 240', '°C', 'D 92'), ('sulfur', 3, 'Sulfur, wt ppm (D2622): 2', 'wt ppm', 'D2622'), ('saturates', 3, 'Saturates, wt% (D 2007): 99', 'wt%', 'D 2007')]:
    note('ARAMCO_LUBEREF_PRIMA_500', 'DL2-11773.pdf', f"DL2-11773.pdf p.1 column 'aramcoPRIMA 500' (Typical) prints {txt!r}; the record's {path} holds the DL2-12172.pdf specification entry only.",
         "Old-source typical never captured. Propose an alternate entry labelled 'typical (brochure, undated)', kept separate from the specification limit already selected; the two value classes are not compared as a conflict and neither is preferred.",
         oA, path=path, action='propose_alternate_entry', form='typical value (brochure Typical column)', tier=tier, new_text=f"'{txt}'", unit=unit, method=meth, cmp='existing: specification limit from DL2-12172.pdf')
note('ARAMCO_LUBEREF_PRIMA_500', 'DL2-11773.pdf', "DL2-11773.pdf p.1 column 'aramcoPRIMA 500' prints 'Aromatic, wt% (D 2007): < 1'; the aromatics field is Missing ('Not reported in reviewed source specifications').",
     "Old-source value never captured: propose aromatics '< 1' wt% (D 2007) as a typical with qualifier '<', from the brochure column, as printed.", oA, path='aromatics', action='capture_from_old_source',
     form='typical value (brochure Typical column; upper bound as printed)', tier=3, new_text="'< 1'", unit='wt%', method='D 2007', cmp='existing: Missing')
note('ARAMCO_LUBEREF_PRIMA_500', 'DL2-11773.pdf', "DL2-12172.pdf ('LUBEREF GII Product Specifications*', column 'aramcoPRIMA 500 Spec.') prints VI 'Min 105' and Noack 'Max 5'.",
     "Two brochure typicals lie outside the specification limits of the other document: VI typical 104 vs specification min 105; Noack typical 6.9 vs specification max 5. Recorded side by side as an open question for Aramco / Luberef; not resolved, not averaged, and it does not settle whether both documents describe the same product (the record's existing identity question stays open).",
     oA, action='propose_open_question_update', outcome='additional', form='typical (brochure) beside specification limit (Luberef sheet)', new_text="'Viscosity Index ... 104'; 'Noack Volatility, wt% ... 6.9' (column 'aramcoPRIMA 500', Typical)", cmp='existing: density discrepancy only')

# ---------------- LUBEREF spec sheet DL2-12172 ----------------
oL = f're-read manually: DL2-12172.pdf ("LUBEREF GII Product Specifications*", 1 page, undated) whole page, text layer and image ({T})'
for g, col in [('70', 'aramcoPRIMA 70 Spec.'), ('110', 'aramcoPRIMA 110 Spec.'), ('230', 'aramcoPRIMA 230 Spec.'), ('500', 'aramcoPRIMA 500 Spec.')]:
    pid = f'ARAMCO_LUBEREF_PRIMA_{g}'
    link(pid, 'DL2-12172.pdf', 'the whole page (text layer and image)',
         f"column {col!r}: every recorded limit and typical equals the table (density Typical / 'Report', KV40 / KV100 Min-Max or 'Report', pour Max, flash COC Min, VI Min, saturates Typical, Noack Max where printed, sulfur Max). The title carries an asterisk ('Product Specifications*') but no footnote text is printed on the page. Not recorded: Appearance 'C & B', ASTM Color '<0.5' -> note.", col)
    note(pid, 'DL2-12172.pdf', f"DL2-12172.pdf p.1, column {col!r}, prints (not recorded): Appearance 'Clear & Bright' / 'C & B'; ASTM Color (ASTM D-1500) '<0.5'. The title 'LUBEREF GII Product Specifications*' has an asterisk with no footnote text on the page.",
         'Old-source items without a template field; the unexplained asterisk is recorded, not interpreted.', oL)
d = dict(batch='family tables, batch 16: GS Caltex and aramcoPRIMA (sixteenth pass)', reviewed_on='2026-11-13 (sixteenth pass)',
         note='Seventeen duplicate links over three family tables; each read in full and viewed as an image; each grade column compared with its own record.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzz_b16_family_gscaltex_aramco_sixteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
