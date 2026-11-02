"""Update open_questions_and_conflicts.md for the 2026-10-31 source-backed corrections (exact, single-occurrence edits)."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\Users\windo\OneDrive\Desktop\Smart formulator project')
P = 'open_questions_and_conflicts.md'
raw = open(P, encoding='utf-8', newline='').read()
assert '\r\n' in raw
t = raw.replace('\r\n', '\n')
RF66 = json.load(open('Products_json/Additive_packages_json/Richful/RICHFUL_RF6066/tier2_numeric_contribution.json', encoding='utf-8'))
NOTE66 = RF66['conflicts'][1]['note']
OLD66 = 'At least one document is undated, so the most recent cannot be determined; field left null. Not resolved.'
assert NOTE66.startswith(OLD66)


def rep(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:90])
    t = t.replace(old, new)


# §59 RF6066: the kv100 conflict line mirrors the JSON note, which now carries the appended review note.
kv = ("Viscosity, dynamic : 185 mm²/s (100 °C) — " + OLD66 + "\n")
rep(kv, "Viscosity, dynamic : 185 mm²/s (100 °C) — " + NOTE66 + "\n")

# §63 RF6078: the conflict note is unchanged; the review of the kept proposal is recorded in final_resolution.
rf78 = ("'RF6078 - TDS.pdf' lists API CI-4 Plus at 11.85%. Not resolved.\n")
rep(rf78, rf78 + "- (tier1) [Review 2026-10-31, audit CF-180; recorded in this conflict's final_resolution] The kept origin/main "
    "proposal says \"the note text has the two files swapped\". Checked against both PDFs: the statement is incorrect. "
    "DL2-15832.pdf p.1 prints 'ACEA E7/API CI-4 10W-30, 10W-40, 15W-40, 20W-50 11.85%' and 'API CI-4 10W-30, 10W-40, "
    "15W-40, 20W-50 10.85%'; 'RF6078 - TDS.pdf' p.1 prints 'ACEA E7/API CI-4 … 10.85%' and 'API CI-4 Plus … 11.85%'. "
    "The note and the values are both correct. The conflict remains unresolved.\n")

# §50 / §54 Lubrizol: corrections recorded in field notes.
for prod, f, rev, ash, old, zn, s in (('LUBRIZOL_CV1100', 'DL2-11503.pdf', 'Effective 11/8/2017', 7, 5.8, '0.778 (min 0.700, max 0.856)', '2.35'),
                                      ('LUBRIZOL_CV3515', 'DL2-15722.pdf', 'Effective 10/9/2017', 10, 9.2, '0.772 (min 0.695, max 0.850)', '2.4')):
    anchor = (f"## {'50' if prod.endswith('1100') else '54'}. {prod}\n")
    i = t.index(anchor); j = t.index('\n## ', i + 1)
    sec = t[i:j]
    last = sec.rstrip('\n').split('\n')[-1]
    assert last.startswith('- (tier2) [History] User decision 2026-10-17: the density field'), last[:80]
    add = (f"\n- (tier2) [Correction 2026-10-31, audit CF-{'142' if prod.endswith('1100') else '143'}] Sulfated ash now holds the "
           f"printed typical value 'SULFATED ASH {ash}' ({f} p.2, {rev}; Chemical Characteristics table, 'Typical' column "
           "under the p.1 header 'Minimum % Weight | Typical | Maximum % Weight'; no method printed), status Reported. "
           f"The previous calculated estimate {old} wt.% (ASTM D874-type factors, Zn taken as 0) is kept in alternate_entries "
           "as a historical calculation, not a measurement. [fields: sulfated_ash]"
           f"\n- (tier2) [Correction 2026-10-31] Zn and S were recorded as Missing although printed on {f} p.2: now Zn "
           f"{zn} wt.% and S {s} wt.% (typical column; no method printed), status Reported. [fields: elements.Zn, elements.S]")
    t = t[:i] + sec.rstrip('\n') + add + t[i + len(sec.rstrip('\n')):]

# §110 Dimer C12
dim = "## 110. CHEVRON_SYNFLUID_DIMER_C12\n- (tier1) PAO suggests API Group IV by standard classification, but no explicit supplier API group statement verified; kept Missing. [fields: api_group_chemistry.api_group]\n"
rep(dim, dim + "- (tier2) [Correction 2026-10-31, audit CF-136] Pour point corrected from -63 °C to -53 °C. DL2-13202.pdf p.1 "
    "(Revision Date April 2011) prints 'Pour Point, °F, °C -53 (-63)': in label order -53 °F would be about -47 °C, not -63 °C, "
    "so the pair is consistent only as -53 °C (-63 °F). The sheet's other °F, °C rows follow the label order (flash 362 (183), "
    "fire 396 (202)). DL2-13200.pdf p.1 (C12 Dimer column) and the Chevron Phillips data sheet of June 2012 (copy in "
    "reconciliation/audit_evidence) print 'Pour Point, °C (°F) -53 (-63)'. The previous reading (-63 °C, printed_text '-63') "
    "is recorded in the field note; method left null (none printed in DL2-13202.pdf). [fields: pour_point]\n")

# Documentation uncertainties and corrections: dated summary bullet.
arch = "- Archive file names: seven archive PDFs are stored in the zip with U+FFFD"
rep(arch, "- Source-backed corrections (2026-10-31, from the comprehensive conflicts audit; see "
    "reconciliation/comprehensive_conflicts_audit_corrections_2026-10-31.md): CF-136 CHEVRON_SYNFLUID_DIMER_C12 pour point "
    "-63 -> -53 °C; CF-142/CF-143 LUBRIZOL_CV1100/CV3515 sulfated ash now the printed typical values 7 and 10 (previous "
    "calculated estimates 5.8 and 9.2 kept as historical alternates), with the omitted printed Zn and S added; CF-159 "
    "RICHFUL_RF6066 KV100 conflict note clarified; CF-180 RICHFUL_RF6078 incorrect 'swapped' statement in the kept proposal "
    "annotated. Both Richful conflicts remain unresolved.\n" + arch)

# Human review: RF6078 item, keep original text and record the check.
hr = "and RICHFUL_RF6078 (the proposal states that the conflict note has the two files swapped; check against both PDFs)."
rep(hr, hr + " Checked 2026-10-31 (audit CF-180): the statement is incorrect, the note matches both PDFs; the conflict itself "
    "is still to be decided. For RICHFUL_RF6066 KV100, the 2021 SDS value 185 is printed on a 'Viscosity, dynamic' line with "
    "a kinematic unit (audit CF-159).")

out = t.replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print('written', P, len(raw), '->', len(out))
