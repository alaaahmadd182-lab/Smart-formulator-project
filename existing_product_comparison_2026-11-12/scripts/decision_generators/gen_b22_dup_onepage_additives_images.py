"""Seventeenth pass, batch 22: duplicate (category A) coverage of twelve one-page sources: Bettchem BT3088 / 3089 / 3093, OLOA 59230,
Jinzhou Donggong T3160, KangTai KT31140, Wuxi WX3118 / WX3326 (additive packages, text layer; Bettchem tables also viewed), and the
image-only BAPCO BAPbase 4 / 6 / 8 specifications and the FPCC Group II table (viewed). Each compared with its own record.
Writes decisions/zzzzzzzzzzzzzzzzz_b22_dup_onepage_additives_images_seventeenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'seventeenth pass, 2026-11-14'
links, F = [], []
NOTE = 'Old-source items without a template field, preserved as printed; nothing is mapped to a field.'


def link(pid, f, ed, cov, read='p.1 (only page) read in full (text layer)', ident='SHA-256 equal to the cited archive file; product name on the page'):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})', coverage=f'assessed by reading (2026-11-14, seventeenth pass) for the whole page ({ed}): {cov}',
                      identity=ident, note='Byte duplicate of the cited source.'))


def row(pid, f, ed, old, reason=NOTE, path='open_questions', action='propose_note', outcome='in_old_source_not_captured', form='values and statements as printed (no template field)', tier=1,
        new_text='(same file; byte duplicate in the new archive)', unit='as printed', method='as printed', qual='as printed', cmp='existing: not recorded', how='p.1 whole text'):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=1, new_text=new_text, unit=unit, form=form, qual=qual, method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({ed}) {how} ({T})', cmp_override=cmp))


HB = "'Storage and handling temperature 45 ℃; Maximum storage temperature 50℃ Maximum handling temperature 70 ℃; Maximum blending temperature 70℃'"
for pid, f, ed, cov, unc in [
    ('BETTCHEM_BT_3088', 'DL2-15551.pdf', 'Version 2.0/ME, Date 12/12/2024', "treat rates (CI-4 8.0, CH-4/SJ 7.0, CF-4/SG 6.0), every Minimum / Maximum / TYPICAL value (TBN 112 / 125 / 118, Ca, N, P, S, sulphated ash, Zn, B, KV100 / KV40, SG 15.6 °C, flash '180 / ＞190', pour) equal the record; the element rows print no unit (existing open question).", f"handling: 'Drum net weight 190Kg'; {HB}"),
    ('BETTCHEM_BT_3089', 'DL2-15552.pdf', 'Version 1.0/ME, Date 9/25/2024', "treat rates (CF-4/SJ 4.8 ... CC/SC 2.2) and every value equal the record; on the image the base number prints 198 under 'Minimum' and 233 under 'TYPICAL' with the 'Maximum' cell empty, as the record states.", f"handling: 'Drum net weight 200Kg'; {HB}"),
    ('BETTCHEM_BT_3093', 'DL2-15550.pdf', 'Version 2.0/ME, Date 12/6/2023', "the dosage table (API CI-4 8.0, CH-4 7.0, CF-4/SL 6.0; row order checked on the image, the text layer prints the specification names after the table) and every value equal the record; base number 100 'Minimum' / 115 'TYPICAL' (no maximum) as recorded.", f"'COLOR (DILUTION), Scale | Report | ＜2.0 | ASTM D1500'; handling: 'Drum net weight 190kg'; {HB}"),
]:
    link(pid, f, ed, cov + ' Not recorded: handling' + (' and colour' if 'COLOR' in unc else '') + ' -> note.', read='p.1 (only page) read in full (text layer; the property table also viewed as an image)')
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): {unc}; 'Please refer to corresponding material safety data sheet for further details'.")

link('CHEVRON_OLOA_59230', 'DL2-13876.pdf', 'Version 1, 25 June, 2020', "dosage 5.94 wt%, the CF-4 claim wording (existing open question), Ca / N / Zn / P / sulfated ash / base number, density 15 °C (no method printed), KV40 / KV100 equal the record. Not recorded: the composition sentence -> note.")
row('CHEVRON_OLOA_59230', 'DL2-13876.pdf', 'Version 1, 25 June, 2020', "DL2-13876.pdf prints (not recorded): 'OLOA® 59230 contains ashless dispersant, zinc dithiophosphate, metallic detergents and anti-oxidant.'; handling 'Please refer to the corresponding material safety data sheet for handling and blending precautions and maximum recommended temperatures.'",
    NOTE + ' The composition sentence names component classes only: no shares, no element contents and no co-component requirement are derived from it.')
link('JINZHOU_DONGGONG_T3160', 'DL2-11882.pdf', 'undated', "dosage table (CI-4/SL 13.0 ... CF-4/SJ 6.0 m%, grades 15W40 / 10W40 / 10W30), the 'Quality Index' minima (flash ≥170, TBN ≥90, N ≥0.50, Zn ≥1.1, Ca ≥3.3) and the Group II / III base-oil sentence equal the record; density and KV100 'Report' (Missing). Not recorded: storage, packing -> note.")
row('JINZHOU_DONGGONG_T3160', 'DL2-11882.pdf', 'undated', "DL2-11882.pdf prints (not recorded): 'According to the requirements of SH/T0164, the maximum temperature should not exceed 75°C for the storage, handling and blending of the product, and it should not exceed 45°C for long-term storage.'; 'Net Weight: 190 Kg/Iron Drum'.")
link('JINZHOU_KANGTAI_KT31140', 'DL2-12961.pdf', 'undated', "dosages (CF-4/SG 5.8, CD/SF 4.0, CC/SE 2.8 wt%) and the characteristics equal the record, which stores them as specification minima. The column is headed 'Typical Value' while each entry is printed 'NNN min' -> open-question row. Not recorded: packing -> note.")
row('JINZHOU_KANGTAI_KT31140', 'DL2-12961.pdf', 'undated', "DL2-12961.pdf prints (not recorded): 'Packed in 200 liter steel drum, 190 kg net weight per drum.'")
row('JINZHOU_KANGTAI_KT31140', 'DL2-12961.pdf', 'undated', "Record: TBN, Ca, Zn, P, N and flash stored as specification minima (q '≥', value_kind 'specification').",
    "The 'PRODUCT CHARACTERISTICS' table is headed 'Item | Typical Value | Test Method' but every entry is printed with 'min' (e.g. 'TBN, mg KOH/g 135 min'). The heading and the entries disagree on the value type. Propose an open question quoting both; the record's minima are not changed and no typical is inferred.",
    action='propose_open_question_update', outcome='additional', form='table heading vs printed entries (value type)', new_text="'Item Typical Value Test Method' ... 'TBN, mg KOH/g 135 min SH/T 0251'", cmp="existing: specification minima")
for pid, f, extra in [('WUXI_WX3118', 'DL2-13534.pdf', "Mg ≥0.33, B ≥0.12"), ('WUXI_WX3326', 'DL2-13538.pdf', '')]:
    link(pid, f, 'undated, no company name', f"treat rates by performance level and SAE grade, and the 'Limit' minima (flash, TBN, P, Zn, Ca, N{', ' + extra if extra else ''}) equal the record; KV100 and density 'Report' (Missing); methods printed 'ASTM D - 4628' for the elements and 'ASTM D - 3228' for N, as recorded. Not recorded: storage, packing, warranty -> note.")
    row(pid, f, 'undated', f"{f} prints (not recorded): 'In the storage, loading/unloading and blending. The maximum temperature is 65ºC; if in long time storage we suggest the Max. Temperature is 50ºC. Avoid contact with water and moist air.'; 'Packing in 200L drum, net weight is 185Kg/drum.'; 'The warranty period is 24 months.'")

# ---------------- image-only specifications ----------------
BAP = {'4': ('DL2-13092.jpg', 'B-743B', 'REFIN/TS/PRODSPEC/GENE/83', "4.200 – 4.400", "To be reported", '14.8 max', "Cloud Point 'To be reported'; 'Color, Saybolt' '+20 min' (note b)"),
       '6': ('DL2-12888.jfif', 'B-760B', 'REFIN/TS/PRODSPEC/GENE/84', "5.800 – 6.200", "31.00 -35.00", '8.0 max', "'Color, Saybolt' 'To be reported' (note b); no cloud-point row"),
       '8': ('DL2-13093.jpg', 'B-780B', 'REFIN/TS/PRODSPEC/GENE/85', "7.800 – 8.200", "45.00 – 55.00", '5.0 max', "'Color, Saybolt' 'To be reported' (note b); no cloud-point row")}
for g, (f, code, ref, kv100, kv40, noack, extra) in BAP.items():
    pid = f'BAPCO_BAPBASE_{g}'
    ed = f"Bahrain Refinery Product Specification, Code No. {code}, {ref}, Issue Status 1.0, 17 August 2017, 'Controlled Bapco Document', 'New Product Specification'"
    link(pid, f, ed, f"'SPECIFIED VALUE' column: KV100 '{kv100}', KV40 '{kv40}', VI min, CCS -30 °C max, Noack (CEC L-40-93 Proc. B) '{noack}', pour max, flash COC min, saturates min, sulphur max equal the record as limits; density 'To be reported' (Missing, correctly). The record's printed_text strings are shortened ('4.2 - 4.4' for '4.200 – 4.400', '8 max' for '8.0 max') -> correction row. Not recorded: appearance, colour, PMCC, odour, UV absorbance, water and the notes -> note.",
         read='p.1 (only page) read in full (image; no text layer)', ident=f"exact grade line 'BAPbase®{g}', code {code}")
    row(pid, f, ed, f"{f} ({ed}) prints (not recorded): 'Appearance @25 °C | ASTM D 4176-1 | Pass' (note a 'Clear and bright liquid without solid particles.'); 'Color | ASTM D 1500 | 0.5 max'; {extra}; 'Flash Point, PMCC, °C | ASTM D 93 | To be reported'; 'Odor | NM 105-1998 EN | Marketable'; UV-absorbance 280-289 / 290-299 / 300-329 / 330-350 nm 'FDA:21CFR178.3620 (b) | To be reported' (note c 'Absorbance per centimeter optical pathlength'); 'Water Content, mg/kg | ASTM D 6304 | 50 max'; note b 'Color determination \"referee\" method will be ASTM D 156'; '* Denotes addition or change.'", how='p.1 viewed as an image')
    row(pid, f, ed, f"Record printed_text: kv100 '{ {'4': '4.2 - 4.4', '6': '5.8 - 6.2', '8': '7.8 - 8.2'}[g] }'" + ("" if g == '4' else f", kv40 '{ {'6': '31 - 35', '8': '45 - 55'}[g] }'") + f", noack '{ {'4': '14.8 max', '6': '8 max', '8': '5 max'}[g] }'.",
        "printed_text must be verbatim: propose the cells as printed (" + f"KV100 '{kv100}'" + ("" if g == '4' else f", KV40 '{kv40}'") + f", Noack '{noack}'). Values, limits and directions are unchanged.",
        path='kv100', action='propose_printed_text_correction', outcome='changed_or_conflicting', form='specification range as printed (printed_text fidelity)', new_text=f"'{kv100}'" + ("" if g == '4' else f"; '{kv40}'") + f"; '{noack}'",
        unit='cSt / mass %', method='ASTM D 445; CEC L-40-93 Proc. B', qual='specification', cmp='existing: shortened printed_text', how='p.1 viewed as an image')
link('FORMOSA_FPCC_70N_GII', 'DL2-12108.jpeg', "'Specification of FPCC API GII Base Oil', Typical (2017 AUG)",
     "column '70N' (Specification / Typical): density 15 °C, KV100 / KV40, VI, pour (spec -24, typical '<-30'), flash, sulfur, saturates, aromatics and the Group II title equal the record; colour, water and appearance are already in its open question. No new row.",
     read='p.1 (only page) read in full (image; no text layer)', ident="exact column header '70N'")

d = dict(batch='duplicate coverage, batch 22: one-page additive sheets and image-only specifications (seventeenth pass)', reviewed_on='2026-11-14 (seventeenth pass)',
         note='Twelve byte-duplicate links; each page read in full (images viewed) with the record beside it.', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzz_b22_dup_onepage_additives_images_seventeenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
