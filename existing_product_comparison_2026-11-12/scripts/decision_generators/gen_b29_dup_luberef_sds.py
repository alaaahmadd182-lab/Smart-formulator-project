"""Nineteenth pass, batch 29: duplicate (category A) coverage of three nine-page Saudi Aramco Luberef SDSs (aramcoDURA 150, aramcoDURA
150BS, AramcoPRIMA 70). Targeted reading for identity, composition and physical properties; the pages / sections read are stated per
link and the others are listed as not read. Writes decisions/zzzzzzzzzzzzzzzzzzz_b29_dup_luberef_sds_nineteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'
SDSU = 'SDS reported value; statistical basis unspecified (Luberef SDS section 9)'
links, F = [], []


def link(pid, f, read, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})',
                      coverage=f'assessed by reading (2026-11-14, nineteenth pass) for SDS sections 1, 3 and 9 (9 pp., {ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; trade name in section 1 and every page header', note='Byte duplicate of the cited SDS (targeted reading; see scope).'))


def row(pid, f, read, path, tier, old, text, reason, action, outcome, form, unit, method, cmp, page):
    F.append(dict(p=pid, tier=tier, path=path, old=old, new_f=f, new_p=page, new_text=text, unit=unit, form=form, qual='SDS reported value', method=method, cond='', basis='',
                  outcome=outcome, action=action, reason=reason, old_rev=f're-read manually: {f} ({read}) ({T})', cmp_override=cmp))


# aramcoDURA 150 (Jeddah)
R1 = 'pp.1, 2, 4 and 5 read in full (sections 1-3, 8-9 and the start of 10-11); pp.3 and 6-9 (sections 5-7, 11-16) not read'
link('ARAMCO_LUBEREF_DURA_150_JEDDAH', 'DL2-15783.pdf', R1, 'Revision nr 2.0, Issue date 05/08/2019, supersedes 26/07/2017, Location: Jeddah',
     "section 3 ('Distillates, petroleum, solvent-dewaxed light paraffinic (DMSO<3%)', CAS 64742-56-9, 100 %) is the record's chemistry source. Section 9 repeats the guaranteed-specification limits already recorded from DL2-12173.pdf (KV '28 - 31 mm²/s (40 °C)', 'Viscosity index (min) :101', 'Pour point :-12 °C (max)', 'Sulfur :1.0 (Wt%) (max)') and adds 'Flash point : >= 200 °C' (no method), 'ASTM Color :L1.5' and 'Furfural Content (ppm) :<5' -> note. No value differs.")
row('ARAMCO_LUBEREF_DURA_150_JEDDAH', 'DL2-15783.pdf', R1, 'open_questions', 1, 'Record: flash_point 210 °C min COC with a PMCC alternate 200 (DL2-12173.pdf); the SDS is cited only for chemistry.',
    "p.4 'Flash point : >= 200 °C' (no method); p.5 'Kinematic viscosity : 28 - 31 mm²/s (40 °C)'; '9.2. Other information Other properties : Viscosity index (min) :101. Pour point :-12 °C (max) . ASTM Color :L1.5. Sulfur :1.0 (Wt%) (max). Furfural Content (ppm) :<5.'",
    "The SDS section 9 restates the specification limits already recorded (same figures, no new value). The flash bound '>= 200 °C' prints no method, so it is not matched to either the COC minimum 210 or the PMCC '200+'. Preserve as an SDS note; nothing changes.",
    'propose_note', 'in_old_source_not_captured', SDSU, 'as printed', 'as printed', 'existing: specification limits from DL2-12173.pdf', 4)

# aramcoDURA 150BS (Yanbu)
R2 = 'sections 1, 3 and 9 read in full (pp.1-2 and 4-5, located by their SECTION headings); sections 2 and 4-8, 10-16 not read'
link('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-12648.pdf', R2, 'Revision nr 2.0, Issue date 05/08/2019, supersedes 31/07/2017, Location: Yanbu',
     "section 3 ('Paraffin oils (petroleum), catalytic dewaxed heavy, Baseoil (DMSO<3%)', CAS 64742-70-7) is the record's chemistry source. Section 9 prints 'Kinematic viscosity : 476,2 mm²/s (40 °C)' while the record's mandatory kv40 is Missing and its open question says KV40 is 'not reported' in DL2-13944.pdf, DL2-12648.pdf and DL2-12173.pdf -> open-question correction row for the source-selection decision (the earlier review missed this line). Also 'Flash point : >= 232 °C' (no method), 'Viscosity index (min) :95', 'Pour point : -6°C', 'Sulfur : <1.3 Wt%', 'Furfural Content (ppm) <5' -> note.")
row('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-12648.pdf', R2, 'open_questions', 1,
    "Record kv40 Missing; open question 'KV40 and CCS are not reported in the reviewed source specifications' (source files DL2-13944.pdf, DL2-12648.pdf, DL2-12173.pdf). DL2-13944.pdf prints 'Kinematic Viscosity @ 400C | ASTM D445 | cSt | Report' and DL2-12173.pdf prints '-' for 'Viscosity @ 40° c'.",
    "'Kinematic viscosity : 476,2 mm²/s (40 °C)' (section 9.1, p.5)",
    "The SDS prints a single KV40 value with its temperature and unit, so the record's statement that KV40 is 'not reported' in DL2-12648.pdf is wrong (the earlier review missed the line). No technical document gives a KV40 value (one prints 'Report', the other '-'). Under CLAUDE.md data rule 2 the applicable SDS value is then the candidate for selection, but selection belongs to tools/data_policy/source_selection.py and is not made in this review, and the review's own rule forbids proposing an SDS value of unspecified basis as an added value. Propose correcting the open question: quote '476,2 mm²/s (40 °C)' (decimal comma as printed; method not printed; SDS class, statistical basis unspecified) as the only printed KV40 for this grade and flag it for the source-selection decision. CCS remains not reported. kv40 stays Missing here.",
    'propose_open_question_update', 'in_old_source_not_captured', SDSU + '; single value with temperature', 'mm²/s', 'not printed', 'existing: kv40 Missing; open question says not reported', 5)
row('ARAMCO_LUBEREF_DURA_BS150_YANBU', 'DL2-12648.pdf', R2, 'open_questions', 1, 'Record: flash_point 282 COC (DL2-13944.pdf) with a PMCC alternate 232; VI 95, pour -6, sulfur 1.3 recorded from the technical sheets.',
    "p.4 'Flash point : >= 232 °C' (no method); p.5 '9.2. Other information Other properties : Viscosity index (min) :95. Pour point : -6°C. Sulfur : <1.3 Wt%. Furfural Content (ppm) <5.'",
    "The SDS repeats the figures of the technical sheets (VI 95 min, pour -6, sulfur '<1.3 Wt%' where the specification prints 'Max. 1.3') and a flash bound '>= 232 °C' without a method. Preserve as an SDS note; the existing sulfur unit conflict is not changed.",
    'propose_note', 'in_old_source_not_captured', SDSU, 'as printed', 'as printed', 'existing: values from DL2-13944.pdf / DL2-12173.pdf', 4)

# AramcoPRIMA 70
R3 = 'pp.1, 2 and 4 read in full and the section 9 part of p.5; pp.3, 6-9 and the rest of p.5 not read'
link('ARAMCO_LUBEREF_PRIMA_70', 'DL2-15448.pdf', R3, 'Revision nr 2.0, Issue date 5/05/2021, supersedes 14/03/2018',
     "section 1 'Trade name/designation : AramcoPRIMA® 70', CAS 64742-55-8; section 3 'Base oil : distillates hydrotreated light paraffinic (DMSO% < 3%)' is the record's chemistry source. Section 9 prints 'Kinematic viscosity : > 13 mm²/s' WITHOUT a temperature (not usable for the Missing kv40) and 'Flash point : 168 °C' without a method, below the specification minimum 175 (COC) recorded from DL2-12172.pdf -> alternate-entry and open-question rows.")
row('ARAMCO_LUBEREF_PRIMA_70', 'DL2-15448.pdf', R3, 'flash_point', 2, 'Record flash_point min 175 °C, ASTM D92 (COC), specification (DL2-12172.pdf).',
    "'Flash point : 168 °C' (section 9.1, p.5; no method)",
    "Comparability checked: same property and unit; the SDS prints no method (the specification is COC), a single value of unstated basis against a specification minimum, and the editions differ (SDS 2021; specification sheet undated). 168 lies below the minimum 175, but with the method unknown and the value classes different this is not called a direct conflict. Propose an SDS alternate entry with the missing method stated, and an open question to Luberef; the specification minimum stays selected.",
    'propose_alternate_entry', 'additional', SDSU + '; single value, no method', '°C', 'not printed', 'existing: specification minimum 175 COC', 5)
row('ARAMCO_LUBEREF_PRIMA_70', 'DL2-15448.pdf', R3, 'open_questions', 1, "Record kv40 Missing; open question 'KV40, density and CCS are not reported in the reviewed source specifications' (DL2-12172.pdf, DL2-15448.pdf).",
    "'Kinematic viscosity : > 13 mm²/s' (section 9.1, p.5; no temperature printed); 'Flash point : 168 °C'",
    "The SDS kinematic viscosity has no test temperature, so it cannot fill kv40 (or kv100) and is not assigned to either; the open question should quote it. The flash value is handled in the alternate-entry row. Nothing is inferred.",
    'propose_open_question_update', 'additional', SDSU + '; lower bound without temperature', 'mm²/s', 'not printed', 'existing: KV40 not reported', 5)

d = dict(batch='duplicate coverage, batch 29: Luberef SDSs (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='Three byte-duplicate links; targeted reading (pages / sections stated per link).', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b29_dup_luberef_sds_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
