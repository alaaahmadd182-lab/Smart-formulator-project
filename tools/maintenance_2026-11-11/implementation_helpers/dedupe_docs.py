R = 'C:\\Users\\windo\\sf-wsA\\'
EXIST = 'already recorded as an unresolved edition-difference conflict by the 2026-10 audit (41.1 vs 42.0–55.0; not recorded twice)'


def edit(rel, reps):
    p = R + rel
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


D = 'docs\\data_policy_mandatory_review\\'
edit(D + 'CHANGELOG_2026-11-10.md', [
    ("Three more were added on 2026-11-11 (external-source review, below). |", "Two more were added on 2026-11-11 (external-source review, below). |"),
    ("| 8 conflicts added | `conflicts[]` entry | 5 (2026-11-10) + 3 (2026-11-11) |", "| 7 conflicts added | `conflicts[]` entry | 5 (2026-11-10) + 2 (2026-11-11) |"),
    ("| 51 change-list rows | row of the change list | 39 selections + 2 list fills + 2 qualifier corrections + 8 conflicts |",
     "| 50 change-list rows | row of the change list | 39 selections + 2 list fills + 2 qualifier corrections + 7 conflicts |"),
    ("  - `EVR-2026-11-11-ULTRA8-kv40`: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt.",
     "  - not added: the aramcoULTRA 8 KV40 disagreement (S-OIL typical 41.10 cSt below the SDS range 42.0–55.0 cSt) was " + EXIST + "."),
    ("All 27 differences in the 18 changed files are pre-existing", "All 27 differences in the 17 changed files are pre-existing"),
])
edit(D + 'HANDOFF.md', [
    ("51 rows in `source_selection_changes.csv`", "50 rows in `source_selection_changes.csv`"),
    ("   - 8 disagreements recorded as unresolved conflicts: 5 from the archive review and 3 from the external review (PRIMA 230 Noack and density, aramcoULTRA 8 KV40).",
     "   - 7 disagreements recorded as unresolved conflicts: 5 from the archive review and 2 from the external review (PRIMA 230 Noack and density). The aramcoULTRA 8 KV40 disagreement was already a conflict (2026-10 audit) and is not recorded twice."),
    ("27 differences in 18 files, all pre-existing", "27 differences in 17 files, all pre-existing"),
    ("but its KV40 conflict stays open |", "but its KV40 conflict (2026-10 audit) stays open |"),
])
edit(D + 'evidence_review.md', [
    ("| `EVR-2026-11-11-ULTRA8-kv40` | S_OIL_ARAMCO_ULTRA_8 · KV40 | The S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt (field already pending). |\n", ""),
    ("  - **KV40 41.10 lies below the SDS range 42.0–55.0** (conflict `EVR-2026-11-11-ULTRA8-kv40`).",
     "  - **KV40 41.10 lies below the SDS range 42.0–55.0**: logically incompatible, and " + EXIST + "."),
])
edit(D + 'implementation_plan.md', [
    ("- **Product JSON:** conflict entries only:\n  - ARAMCO_LUBEREF_PRIMA_230 tier 1 (`EVR-2026-11-11-230-density-external`) and tier 2 (`EVR-2026-11-11-230-noack`);\n  - S_OIL_ARAMCO_ULTRA_8 tier 1 (`EVR-2026-11-11-ULTRA8-kv40`).",
     "- **Product JSON:** conflict entries only: ARAMCO_LUBEREF_PRIMA_230 tier 1 (`EVR-2026-11-11-230-density-external`) and tier 2 (`EVR-2026-11-11-230-noack`)."),
    ("  - `source_selection.py`: three conflict additions, updated pending reasons;", "  - `source_selection.py`: two conflict additions, updated pending reasons;"),
])
edit(D + 'requirements_review.md', [
    ("(conflict `EVR-2026-11-11-ULTRA8-kv40`)", "(an unresolved conflict recorded by the 2026-10 audit)"),
])
edit(D + 'source_review_coverage.md', [
    ("KV40 typical 41.10 lies below the SDS range (conflict EVR-2026-11-11-ULTRA8-kv40)", "KV40 typical 41.10 lies below the SDS range (unresolved conflict from the 2026-10 audit)"),
])
edit('open_questions_and_conflicts.md', [
    ("  - S_OIL_ARAMCO_ULTRA_8 KV40: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt (`EVR-2026-11-11-ULTRA8-kv40`). The field stays pending.",
     "- S_OIL_ARAMCO_ULTRA_8 KV40: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt. This is the existing 2026-10 audit conflict (edition difference); it is not recorded twice. The field stays pending."),
])
print('ok')
