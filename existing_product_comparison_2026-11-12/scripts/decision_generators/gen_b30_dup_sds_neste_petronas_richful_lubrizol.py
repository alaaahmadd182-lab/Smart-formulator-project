"""Nineteenth pass, batch 30: duplicate (category A) coverage of seven 9-10 page SDSs (NEXBASE 3060 / 3080, EQUINAS 4 / 6, ETRO 6+,
RF6602, LUBRIZOL CV6320). Targeted reading of sections 1 (identification), 3 (composition) and 9 (physical and chemical properties)
located by their headings; the page span read is stated per link and the other sections are listed as not read.
Writes decisions/zzzzzzzzzzzzzzzzzzz_b30_dup_sds_neste_petronas_richful_lubrizol_nineteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, read, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})',
                      coverage=f'assessed by reading (2026-11-14, nineteenth pass) for SDS sections 1, 3 and 9 ({ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name in section 1', note='Byte duplicate of the cited SDS (targeted reading; see scope).'))


def row(pid, f, read, path, tier, old, text, reason, action, outcome, form, unit, method, qual, cmp, page):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=text, unit=unit, form=form, qual=qual, method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({read}) ({T})', cmp_override=cmp))


NOTE = 'SDS items without a template field (or already recorded figures), preserved as printed; nothing is mapped to a field.'

# NEXBASE 3060 / 3080 (Neste)
RN = 'sections 1 (p.1), 3 (p.2) and 9 (pp.4-5) read in full; sections 2 and 4-8, 10-16 not read'
link('NESTE_NEXBASE_3060', 'DL2-12735.pdf', RN, 'Revision date 17/10/2017, supersedes 30/05/2016',
     "section 9 prints 'Kinematic viscosity 32 mm2/s @ 40°C typical value (ASTM D-445)' (equal to the record's TDS typical 32), pour '≤ -12°C (ASTM D-97)' and flash '> 220°C (ASTM D-92)' (the existing open question says they are compatible with the TDS limits), relative density '0,83-0,85 @ 15°C' (recorded as specific_gravity). Not recorded: section 1/3 identity 'Lubricating oils (petroleum), C20-C50, hydrotreated neutral oil-based', CAS 72623-87-1, boiling range 370...600°C, dynamic viscosity -> note.")
row('NESTE_NEXBASE_3060', 'DL2-12735.pdf', RN, 'open_questions', 1, 'Record chemistry: TDS supplier description (DL2-10039.pdf); no CAS recorded.',
    "Section 1 'Chemical name Lubricating oils (petroleum), C20-C50, hydrotreated neutral oilbased'; section 3 '... 100 % CAS number: 72623-87-1 EC number: 276-738-4', 'DMSO < 3% (IP 346)'; section 9 'Initial boiling point and range 370...600°C', 'Dynamic viscosity 69,6 mPa s @ +20°C'.",
    NOTE + ' The SDS chemical name and CAS complement the TDS description; the recorded chemistry is not replaced.', 'propose_note', 'in_old_source_not_captured', 'SDS identification and composition as printed', 'as printed', 'as printed', 'as printed', 'existing: not recorded', 2)
link('NESTE_NEXBASE_3080', 'DL2-14512.pdf', RN, 'Revision date 03/07/2020, supersedes 17/10/2017',
     "a grade-specific SDS ('Product name NEXBASE™ 3080'), contrary to the record's open question 'SDS specific to NEXBASE 3080 not independently verified' -> open-question row. Section 9 prints 'Kinematic viscosity 48 mm2/s @ 40°C typical value (ASTM D-445)' against the TDS typical 49 (edition 2.2, no calendar date) -> conflict row after the comparability check; pour '≤ -12°C', flash '> 220°C', relative density 0,84 (recorded). Not recorded: CAS 72623-87-1, boiling range 430...620°C -> in the open-question row.")
row('NESTE_NEXBASE_3080', 'DL2-14512.pdf', RN, 'kv40', 1, 'Record kv40 49 mm²/s typical (TDS DL2-10040.pdf, edition 2.2, no calendar date).',
    "'Kinematic viscosity 48 mm2/s @ 40°C typical value (ASTM D-445).' (section 9, p.4)",
    "Comparability checked: same property, unit, temperature, method (ASTM D445) and grade, and the SAME value class (both labelled typical); the editions differ (TDS edition 2.2 undated; SDS revised 03/07/2020) and their order is not established. Two typicals of the same grade differ (48 vs 49). Propose a conflict entry with both values, sources and editions; not resolved, not averaged, the TDS value stays selected and no edition preference is applied.",
    'propose_record_conflict', 'changed_or_conflicting', 'typical value (SDS section 9, labelled typical by the supplier)', 'mm²/s', 'ASTM D-445', 'typical', 'existing: kv40 49', 4)
row('NESTE_NEXBASE_3080', 'DL2-14512.pdf', RN, 'open_questions', 1, "Record open question 'SDS specific to NEXBASE 3080 not independently verified.'",
    "Section 1 'Product name NEXBASE™ 3080', 'Product number ID 13447'; section 3 'Lubricating oils (petroleum), C20-50, hydrotreated neutral oil- based 100 % CAS number: 72623-87-1'; section 9 boiling range '430...620°C'; 'Revision date: 03/07/2020'.",
    'The archived SDS names the grade in section 1 and on every page header, so the open question can be updated: a grade-specific SDS exists in the archive (sections 1, 3 and 9 read). Its CAS and chemical name are recorded here as printed; nothing else changes.',
    'propose_open_question_update', 'additional', 'SDS identification and composition as printed', 'as printed', 'as printed', 'as printed', "existing: 'not independently verified'", 1)

# EQUINAS 4 / 6, ETRO 6+ (PETRONAS)
for pid, f, ed, cov, unc, page in [
    ('PETRONAS_EQUINAS_6', 'DL2-15185.pdf', 'Version 1.0, Release Date 21.10.2021', "every recorded value comes from this SDS and equals it (KV 6.08 / 32.56 mm2/s, density 0.8385 g/cm3 at 15 °C, Noack 5.9 % mass D5800 B, pour -15 °C D97, flash 248 °C D92; CAS 64742-54-7 'Paraffinic Distillate, Heavy, Hydrotreated').", "'Colour : L 0.5 Method: ASTM D 1500'; appearance 'Clear and bright liquid'; flammability limits 7 % / 0.6 % (V)", 4),
    ('PETRONAS_EQUINAS_4', 'DL2-15184.pdf', 'Version 1.0, Release Date 21.10.2021', "every recorded value comes from this SDS and equals it (KV 4.21 / 18.14 mm2/s, density 0.8291, Noack 13.9 % mass, flash 216 °C D92; CAS 64742-54-7). Section 9 prints no pour point ('Melting point/freezing point : Remarks :No data available'), so pour_point stays Missing correctly.", "'Colour : L 0.5 Method: ASTM D 1500'; appearance; flammability limits 7 % / 0.6 % (V)", 4),
    ('PETRONAS_ETRO_6_PLUS', 'DL2-14610.pdf', 'Version 1.2, Release Date 24.03.2020', "the record already holds this SDS's density (0.8486 g/cm3 at 15 °C) and existing conflict entries for KV40 (34.79 vs 32.55), flash (SDS '228 °C Method: ASTM D 93', closed cup, vs TDS 240 °C ASTM D92 open cup: the methods differ, as printed; the existing entry is not reopened), Noack (5.3 vs 5.7) and density. Section 3 lists 'No hazardous ingredients' (no CAS share).", "'pH : 8.4'; 'Melting point/freezing point : -9 °C' (a different property from the recorded pour point); 'Boiling point/boiling range : 220 °C'; 'Auto-ignition temperature : 450 °C'; 'Viscosity, dynamic : 76.02 mPa.s (20 °C)'; 'Partition coefficient ... Log Kow: 2 to >6'", 3)]:
    rd = 'sections 1 (p.1), 3 (pp.1-2) and 9 (pp.3-4) read in full; sections 2 and 4-8, 10-16 not read' if 'EQUINAS' in pid else 'sections 1 (p.1), 3 (pp.1-2) and 9 (pp.3-4) read in full; sections 2 and 4-8, 10-16 not read'
    link(pid, f, rd, ed, cov + ' Not recorded: ' + unc.split(';')[0] + ' and the other items -> note.')
    row(pid, f, rd, 'open_questions', 1, f"{f} ({ed}) section 9 prints (not recorded): {unc}.", '(same file; byte duplicate in the new archive)',
        NOTE + (" The freezing point is not a pour point and is not compared with it." if 'ETRO' in pid else ''), 'propose_note', 'in_old_source_not_captured',
        'SDS reported value; statistical basis unspecified (PETRONAS SDS section 9)', 'as printed', 'as printed', 'SDS reported value', 'existing: not recorded', page)

# RF6602 (Richful)
RR = 'sections 1 (p.1), 3 (pp.1-2) and 9 (pp.4-5) read in full; sections 2 and 4-8, 10-16 not read'
link('RF6602', 'RF6602.pdf', RR, 'Issue / Revision date 18/2/2022',
     "section 3 ('Acrylic copolymer ... 65 - 85'; 'Distillates (petroleum), hydrotreated heavy paraffinic ... 64742-54-7 ... 15 – 35') is the record's active-content and carrier source and equals it. Section 9 prints 'Flash point : 160 °C' (no method), 'Viscosity, kinematic : 53691mm²/s (40℃)' and 'Density : 0.9 g/cm³' (no temperature); the component templates have no field for them, and the TDS figures are in an open question -> note with the comparability stated.")
row('RF6602', 'RF6602.pdf', RR, 'open_questions', 1, "Record open question lists the TDS DL2-14874.pdf physical properties (KV100 1100-1850 / 1360 mm2/s, Flash Point (COC) '≮180 / 210', ...); no field exists for them.",
    "Section 9: 'Flash point : 160 °C'; 'Viscosity, kinematic : 53691mm²/s (40℃)'; 'Density : 0.9 g/cm³'; 'Trade name : RF6602 Viscocity Index Improver' (section 1, spelling as printed).",
    "Preserve the SDS values beside the TDS figures in the open question. Comparability: the SDS flash prints no method (the TDS is COC) and its 160 °C lies below the TDS index '≮180'; with the method unknown and the value classes different (SDS basis unspecified vs TDS index / typical) this is recorded as a difference to ask Richful about, not as a conflict. The density has no temperature and the KV40 has no TDS counterpart. Nothing is mapped to a field.",
    'propose_open_question_update', 'additional', 'SDS reported value; statistical basis unspecified (Richful SDS section 9)', 'as printed', 'not printed', 'SDS reported value', 'existing: TDS figures only', 4)

# LUBRIZOL CV6320
RL = 'sections 1 (p.1), 3 (p.2) and 9 (p.4) read in full; sections 2 and 4-8, 10-16 not read'
link('LUBRIZOL_CV6320', 'DL2-12016.pdf', RL, 'Version 1.1, Revision Date 21.12.2017',
     "section 3 (mineral oil 40 - 50 %, olefin sulfide 1 - 5 %, ethoxylated alcohol 0.5 - 1 %, aryl thiophosphate 0.1 - 0.5 %) is the record's carrier source and its existing chemical-family open question; section 9 repeats the data-sheet figures already held (flash '181 °C (Pensky-Martens Closed Cup)', relative density '0,849 - 0,889 (15,6 °C)', viscosity '787 mm2/s (40 °C); 69 mm2/s (100 °C )'). Not recorded: the CAS list for the mineral oil -> note.")
row('LUBRIZOL_CV6320', 'DL2-12016.pdf', RL, 'open_questions', 1, "Record carrier.identity 'Mineral oil' (share 40 - 50 %).",
    "'The mineral oil contained in this material may be described by one or more of the following CAS Nos.: 64742-54-7, 64742-65-0, 64742- 55-8, and 64742-56-9.' (section 3, p.2)",
    NOTE + " The CAS list is a set of possible descriptions ('one or more'), not an identification of the carrier; the carrier identity stays 'Mineral oil'.",
    'propose_note', 'in_old_source_not_captured', 'SDS composition statement as printed', 'as printed', 'as printed', 'as printed', 'existing: not recorded', 2)

d = dict(batch='duplicate coverage, batch 30: Neste, PETRONAS, Richful and Lubrizol SDSs (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='Seven byte-duplicate links; targeted reading of sections 1, 3 and 9 (stated per link).', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b30_dup_sds_neste_petronas_richful_lubrizol_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
