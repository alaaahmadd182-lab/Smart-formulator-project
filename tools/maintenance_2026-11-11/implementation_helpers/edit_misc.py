R = r'C:\Users\windo\sf-wsA'


def edit(rel, reps, append=None):
    p = R + '\\' + rel
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:60])
        s = s.replace(a, b)
    if append:
        s = s.rstrip('\n') + '\n' + append
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


edit('tools\\README.md', [
    ("| `data_policy/integration_diff.py` | What `integrate_products.py` would change in given files (or `--changed`), in memory | nothing |",
     "| `data_policy/integration_diff.py` | What `integrate_products.py` would change in given files (or `--changed`), in memory; with `--against REF` each difference is labelled pre-existing (same difference at REF) or NEW, and the exit code is 1 only for NEW ones | nothing |"),
    ("| `data_policy/association_review.py` | Identity review of the name-match document associations (verdicts in `association_review_decisions.json`; byte-identical copies detected) | `reports/data_policy/name_match_review.csv` |",
     "| `data_policy/association_review.py` | Identity review of the name-match document associations (universe frozen at revision 2 plus the current ledger; verdicts in `association_review_decisions.json`; byte-identical copies detected; `now_cited` marks associations later used as sources) | `reports/data_policy/name_match_review.csv` |\n"
     "| `data_policy/external_review.py` | Review of every value from an external (URL) source and of pending fields with an external alternative (decisions and evidence hashes in `external_review_decisions.json`); exits 1 on a stale decision or a changed evidence hash | `reports/data_policy/external_review.csv` |\n"
     "| `data_policy/source_review_status.py` | Review state of every ledger row (archive lead review complete, external review complete, evidence unavailable, inconclusive, not individually reviewed) | `reports/data_policy/source_review_status.csv` |\n"
     "| `data_policy/run_checks.py` | Runs the whole pipeline and every required check as separate subprocesses; saves each real return code and full output; PASS only if every step meets its expectation (`verify_revision.py` is an expected, by-design failure) | `docs/data_policy_mandatory_review/test_results/` |"),
    ("| `data_policy/tests/test_data_policy.py` | Regression tests (36): Rule 1, comparison rules, the outputs and counts, the evidence review (every case reviewed, wrong associations excluded, comparisons reach the inventory, fills and corrections), protected bytes, safety | nothing |",
     "| `data_policy/tests/test_data_policy.py` | Regression tests (45): Rule 1, comparison rules, the outputs and counts, the evidence review (every case reviewed, wrong associations excluded, comparisons reach the inventory and are usable cases, fills and corrections), the external review (coverage, unobtained sources never confirmed, stale decisions rejected, new conflicts unresolved), review states, the check runner, protected bytes, safety | nothing |"),
])

edit('PROJECT_FILE_GUIDE.md', [
    ("`lead_review.csv` (every reviewed lead), `name_match_review.csv` (identity of name-matched documents) |",
     "`lead_review.csv` (every reviewed lead), `name_match_review.csv` (identity of name-matched documents), `external_review.csv` (every external-source value), `source_review_status.csv` (review state of every ledger row), `external_evidence/` (small copies of external sources, with recorded SHA-256) |"),
    ("| `docs/data_policy_mandatory_review/test_results/` | Historical record | Saved outputs of the pipeline, the tests and the protected-file checks |",
     "| `docs/data_policy_mandatory_review/test_results/` | Check record | Output of `tools/data_policy/run_checks.py`: one file per step with its real return code and full output, plus `summary.md` / `summary.json` |"),
])

edit('CLAUDE.md', [
    ("name-match document links must be reviewed (`association_review.py`) before their evidence is used.",
     "name-match document links must be reviewed (`association_review.py`) before their evidence is used. Values from external (URL) sources are reviewed in `external_review.py` (decisions and evidence hashes in `external_review_decisions.json`); an external source that cannot be obtained is \"inconclusive\", never confirmed. Whether an external (non-archive) technical document may be selected over an archived SDS is an open decision (`requirements_review.md` H)."),
    ("Verify preserved files and evidence with `python tools/data_policy/verify_preserved.py` (form-aware), not a bare `sha256sum -c` in a CRLF checkout.",
     "Verify preserved files and evidence with `python tools/data_policy/verify_preserved.py` (form-aware), not a bare `sha256sum -c` in a CRLF checkout.\n- Run every check with `python tools/data_policy/run_checks.py` (separate subprocesses, real return codes, full output saved in `docs/data_policy_mandatory_review/test_results/`). Never pipe a check through a filter when its return code matters."),
])

edit('docs\\data_policy_mandatory_review\\implementation_plan.md', [], append="""
## 7. Revision 3 completion (2026-11-11): additional affected files

- **Product JSON:** conflict entries only:
  - ARAMCO_LUBEREF_PRIMA_230 tier 1 (`EVR-2026-11-11-230-density-external`) and tier 2 (`EVR-2026-11-11-230-noack`);
  - S_OIL_ARAMCO_ULTRA_8 tier 1 (`EVR-2026-11-11-ULTRA8-kv40`).
- **New tools:**
  - `tools/data_policy/external_review.py` (+ `external_review_decisions.json`);
  - `tools/data_policy/source_review_status.py`;
  - `tools/data_policy/run_checks.py`.
- **Changed tools:**
  - `association_review.py`: universe frozen at `4e83652`, plus a `now_cited` column;
  - `lead_review.py` (+ decisions): `exclude_if_comparison`; NEXBASE 3080 flash point added;
  - `source_selection.py`: three conflict additions, updated pending reasons;
  - `integration_diff.py`: `--against REF`.
- **New reports:**
  - `reports/data_policy/external_review.csv`, `source_review_status.csv`;
  - `reports/data_policy/external_evidence/` (4 small source copies, `-text`).
- **Check results:** `test_results/` is now written by `run_checks.py`. The four earlier piped outputs are replaced; Git history keeps them.
""")
print('ok')
