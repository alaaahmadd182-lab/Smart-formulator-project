"""Nineteenth pass, batch 31: duplicate (category A) coverage of five SDSs (HiTEC 8712, RF6089, Risella X 415 / 420, OLOA 59766).
Targeted reading; the sections / pages read are stated per link. Writes
decisions/zzzzzzzzzzzzzzzzzzz_b31_dup_sds_afton_richful_shell_oloa_nineteenth_pass.json."""
# Runs from any directory: it changes to the workspace root.
import os as _os
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))))
import json
B = 'existing_product_comparison_2026-11-12'
T = 'nineteenth pass, 2026-11-14'
links, F = [], []


def link(pid, f, read, ed, cov):
    links.append(dict(p=pid, f=f, cat='A', status='completed', fields_status=f'{read} ({T})',
                      coverage=f'assessed by reading (2026-11-14, nineteenth pass) for the sections stated ({ed}): {cov}',
                      identity='SHA-256 equal to the cited archive file; product name in section 1', note='Byte duplicate of the cited SDS (targeted reading; see scope).'))


def note(pid, f, read, page, old, text, reason):
    F.append(dict(p=pid, tier=1, path='open_questions', old=old, new_f=f, new_p=page, new_text=text, unit='as printed', form='SDS identification / composition statement as printed', qual='as printed', method='as printed', cond='', basis='',
                  outcome='in_old_source_not_captured', action='propose_note', reason=reason, old_rev=f're-read manually: {f} ({read}) ({T})', cmp_override='existing: not recorded'))


R139 = 'sections 1 (p.1), 3 (p.2) and 9 (p.6) read in full; sections 2 and 4-8, 10-16 not read'
link('AFTON_HITEC_8712', 'DL2-15020.pdf', R139, 'date of issue 2 February 2018',
     "section 9 values recorded from this SDS equal it (KV '1800 cSt at 40°C' / '95 cSt @ 100 °C', density 1.033 g/cm³ and relative density 1.036 without temperature, flash 'Closed cup: 135°C (275°F) [Pensky-Martens. Minimum]'); the section 3 shares of mineral oil, calcium alkylphenate sulfide and ZDDP are in the open question. Not recorded: the fourth listed ingredient -> note.")
note('AFTON_HITEC_8712', 'DL2-15020.pdf', R139, 2, "Record open question lists three section 3 shares (calcium alkylphenate sulfide 10 - 19.9 %, ZDDP 10 - 19.9 %, mineral oil 30 - 60 %).",
     "'Phenol, (tetrapropenyl) derivs 74499-35-7 0.5 - 0.99 SKIN CORROSION/IRRITATION - Category 1 SERIOUS EYE DAMAGE/EYE IRRITATION - Category 1 REPRODUCTIVE TOXICITY (Fertility) - Category 1B ...'",
     "Fourth section 3 ingredient never recorded. Preserve it as a component share (not an element content) with its ingredient classification as printed; the ingredient classification is not a classification of the mixture and nothing is derived from it.")
R1589 = 'sections 1 (p.1), 3 (p.2) and 9 (pp.5-6) read in full; sections 2 and 4-8, 10-16 not read'
link('RICHFUL_RF6089', 'DL2-15841.pdf', R1589, 'Version 1.0, Issue / Revision date 07/25/2025',
     "the record cites this SDS under the archive name 'DL2-15841 (1).pdf' (same bytes); its KV100 '92 mm2/s (100 ℃)', density '0.953 g/cm3(20 ℃)', flash '213 ℃(COC)' and the five section 3 component shares are recorded and equal the SDS (the deck differences are existing conflicts). No new row.")
for pid, f, g, code, ed in [('SHELL_RISELLA_X_415', 'DL2-13729.pdf', '415', '001E2773', 'Version 1.2, Revision Date 26.10.2018'), ('SHELL_RISELLA_X_420', 'DL2-13730.pdf', '420', '001E2774', 'Version 1.2, Revision Date 26.10.2018')]:
    R = 'sections 1 (p.1), 3 (p.2) and 9 (pp.7-9) read in full; sections 2 and 4-8, 10-16 not read'
    link(pid, f, R, ed, "section 9 relative density (recorded as specific_gravity) and density (in the existing density conflict with the TDS) equal the record; its pour (ISO 3016), flash (ISO 2592) and KV 20 / 40 / 100 °C (ISO 3104) repeat the TDS figures already recorded. Not recorded: the section 1 / 3 identity (CAS 848301-69-9, chemical nature) -> note.")
    note(pid, f, R, 2, "Record chemistry: TDS description 'GTL-derived hydrocarbon fluid; highly saturated, iso-paraffinic'; no CAS recorded.",
         f"Section 1 'Product name : Risella X {g} Product code : {code} CAS-No. : 848301-69-9'; section 3 'Chemical nature : Fischer-Tropsch derived base oil, consisting largely of branched, cyclic and linear hydrocarbons having carbon numbers in the range of C18 to C50.' and 'Distillates (Fischer - Tropsch), heavy, C18- 50 – branched, cyclic and linear 848301-69-9 Asp. Tox.1; H304 <= 100'.",
         "SDS identity and composition never recorded; they complement the TDS chemistry description, which is not replaced. Preserved as printed.")
R1731 = 'pp.1 and 7 read in full (section 1 and the second part of section 9); pp.2-6 and 8-11 not read in this pass (section 3 on pp.2-3 is already summarised in the record\'s open question)'
link('CHEVRON_OLOA_59766', 'DL2-11731.pdf', R1731, 'Revision Number 14, Revision Date January 24, 2017',
     "p.7 prints 'Flashpoint: (Cleveland Open Cup) 180 °C (356 °F) Minimum', 'Relative Density: 0.9918 @ 15.6°C (60°F)', 'Density: 0.9929 kg/l @ 15°C (59°F)' and 'Viscosity: 2486 mm2/s @ 40°C (104°F)', all recorded from this page; no KV100 and no pour point are printed on p.7 (KV100 and pour_point stay Missing). The first part of section 9 (p.6) was not read. No new row.")

d = dict(batch='duplicate coverage, batch 31: HiTEC 8712, RF6089, Risella X 415 / 420, OLOA 59766 SDSs (nineteenth pass)', reviewed_on='2026-11-14 (nineteenth pass)',
         note='Five byte-duplicate links; targeted reading (stated per link).', documents={}, links=links, fields=F)
json.dump(d, open(f'{B}/decisions/zzzzzzzzzzzzzzzzzzz_b31_dup_sds_afton_richful_shell_oloa_nineteenth_pass.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(links), len(F))
