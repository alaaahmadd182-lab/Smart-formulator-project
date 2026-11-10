# Workstream A: implementation plan, dependency map and affected files

**Baseline.** origin/main `f4d97e71f72598df601b72403775581c34061ad1`, "Merge pull request #6". It contains the v5 audit
commit `f70a434`. Workstream B (association mining) starts from the same commit.

**Checkout.** A separate git worktree at `C:\Users\windo\sf-wsA` on branch `feat/data-policy-mandatory-review`. The main
checkout (`OneDrive\Desktop\Smart formulator project`, branch `docs/audit-report-review-2026-11-02`) was not changed; its
only untracked item, `tools/maintenance_2026-10-31/__pycache__/`, was left alone. `analysis/association_mining/` does not
exist on the baseline and is not touched.

## 1. Dependency map: current tools vs historical generators

| Script | Role | Writes | Safe to run on the new state? |
|---|---|---|---|
| `build_coverage_matrix.py` | Current generator | `--output` workbook only (refuses to overwrite without `--overwrite`) | **Yes.** Regenerated: `Coverage_Matrix.xlsx`. |
| `integrate_products.py` | Current; derives `*_final` keys and annotations | Product JSON, with `--write` only | **Dry run only.** A dry run would change 229 files (baseline: 230), because the data is deliberately not fully re-derived (README, "Data integration"). Changed records were kept consistent with `tools/data_policy/integration_diff.py`. **Never run `--write` on the whole repository.** |
| `build_conflicts_report.py` | Current; draft report | `conflicts_report_generated.md` only | Yes, but not needed. It refuses to write the curated log. |
| `tools/data_policy/*.py` | **New (this workstream)** | Only `reports/data_policy/*`. `source_selection.py --write` writes the declared product JSON fields. | Yes. Idempotent; checks the expected values before changing anything. |
| `tools/mandatory_properties/build_eligibility.py` | **New (this workstream)** | `reports/mandatory_properties/*` | Yes; `--check` writes nothing. |
| `tools/audit/review_2026-11-02/gen_report_v5.py`, `revise_findings.py`, `run_all_checks.py`, `verification_ledger.py` … | **Historical** (v5 audit, 2026-11-02) | The v5 report and CSV, `findings_v5.json`, verification results | **No.** They regenerate the v5 snapshot. The v5 report must stay a historical snapshot. |
| `tools/audit/review_2026-11-02/verify_revision.py` | Historical check | — | Compares protected files with `545fd3d`. It now **fails by design**: product JSON and the workbook changed after that commit. |
| `tools/audit/original_2026-10-27_to_30/*` | **Historical** (audit v1–v4) | Reports and intermediates; `audit_lib.py` hard-codes the main-checkout path | **No.** It would rebuild superseded findings. |
| `tools/corrections_2026-10-31/apply_corrections.py`, `update_curated_log.py` | **Historical** | Product JSON and curated log **in the main checkout** (hard-coded path) | **No.** It would restore the values selected before 2026-11-10. |
| `tools/integration_2026-10-24/resolve_json.py --write`, `log_section.py` | **Historical** | Product JSON, curated log | **No.** Same risk. |
| `tools/maintenance_2026-10-31/*` | Historical publishing helpers (hard-coded paths) | Backups, remote checks | Not relevant. |

## 2. Plan (as carried out)

1. **Rule 1, source selection.**
   - Classify every cited (file, page) by purpose and content (`document_classes.py`).
   - List every SDS-sourced selected value and read the technical documents for the same property (`tds_candidates.py`).
   - Declare each change, exception and pending case in `source_selection.py`, then apply it with provenance and alternates.
   - Keep `integrate_products.py`'s pinned annotations and conflict rules consistent. Three user decisions of 2026-10-18 are superseded; their conflicts are reopened.
2. **Rule 2, TDS–SDS comparisons, steps A–D.**
   - Build the inventory (`tds_sds_inventory.py`), decide comparability first, and propose property-specific thresholds (`thresholds.py`, `threshold_proposal.md`).
   - **Stop at the review checkpoint.** No finding is reclassified, and no successor of the v5 audit is written until the thresholds are approved.
3. **Rule 3, mandatory Tier 1.**
   - Write a versioned requirements definition (`requirements.py`), the eligibility build, and the interface CSV with its documentation.
4. **Consistency.**
   - Regenerate the coverage workbook.
   - Update CLAUDE.md, the README, the project file guide, tools/README, `requirements.txt`, the curated log (a dated section) and the change log.
5. **Protection.**
   - Regression tests (`tools/data_policy/tests/`).
   - Hash checks of the archive, the evidence and the preserved files; templates checked as unchanged.
   - A local commit. No push, merge or PR.

## 3. Affected files

**Product JSON (13 files).**
- Tier 2 of INFINEUM_D3424 and of RICHFUL RF6066, RF6069, RF6077, RF6078, RF6079, RF6088, RF6088F, RF6400 and RF6406.
- NESTE_NEXBASE_3020 tier 1, tier 2 and tier 3. Tier 3 changes only its product block and an open-question annotation.

**Scripts.**
- `integrate_products.py`: docstring rule; three `ANNOTATIONS`, re-pinned; three `CONFLICTS` rules reopened.
- New: `tools/data_policy/` and `tools/mandatory_properties/`.

**Generated outputs.**
- `Coverage_Matrix.xlsx`.
- `reports/data_policy/` (document classes, source-selection change list, TDS–SDS comparison inventory).
- `reports/mandatory_properties/` (eligibility CSV, missing-properties CSV and MD).

**Documentation.**
- `CLAUDE.md`, `README.md`, `PROJECT_FILE_GUIDE.md`, `tools/README.md`, `requirements.txt` (adds `pymupdf` for document classification).
- `open_questions_and_conflicts.md`: a dated section appended; nothing earlier is rewritten.
- This folder.

**Not changed (protected).**
- `Manual + Data to share.zip`, `reconciliation/` (including the v5 audit and `audit_evidence/`), `json_templates/`, `Property_Glossary.docx`, `tools/audit/`, `tools/corrections_2026-10-31/`, `tools/integration_2026-10-24/`, `tools/maintenance_2026-10-31/`, `docs/audit_review_2026-11-02/`, `source_registry.json`.

## 4. Deferred until the threshold review

- Rule 2 E: reclassifying ordinary TDS–SDS differences in a dated successor of the v5 audit (stable CF ids, an old-to-new state mapping, recalculated counts).
- The curated log and the conflict records stay as they are until then. Only the three reopened RF6077/RF6088F conflicts changed, because of Rule 1, not Rule 2.

## 5. Revision 2 (2026-11-10): additional affected files

- **Product JSON:**
  - `FORMOSA_150N_GII_PLUS_tier1.json` and `FORMOSA_500N_GII_tier1.json`: `kv100` set to the technical specification range; the SDS typical value is kept as an alternate.
- **Scripts:**
  - `tools/mandatory_properties/requirements.py`: rewritten, with validation, categories and calculation checks.
  - `build_eligibility.py`: categories, ledger dependency, new outputs.
  - `tools/data_policy/source_selection.py`: incremental apply, FORMOSA changes, `PENDING_FIELDS`, `SDS_FALLBACK_FIELDS`.
  - `thresholds.py` and `tds_sds_inventory.py`: wording, empirical basis, sensitivity.
  - `policy_lib.py`: closes files.
- **New tools:**
  - `tools/data_policy/source_coverage_ledger.py`
  - `tools/data_policy/verify_preserved.py`
  - `tools/mandatory_properties/treat_rate_basis_scan.py`
  - `tools/mandatory_properties/treat_rate_basis_evidence.json`
  - `tools/mandatory_properties/tests/test_requirements.py`
- **New reports:**
  - `reports/data_policy/source_coverage_ledger.csv` (+ `.meta.json`)
  - `reports/data_policy/threshold_sensitivity.csv`
  - `reports/mandatory_properties/requirement_outcomes.csv`
  - `reports/mandatory_properties/treat_rate_basis_scan.csv`
- **New documentation:**
  - `requirements_review.md`
  - `source_review_coverage.md`
  - `test_results/`
- **Updated:**
  - `Coverage_Matrix.xlsx`
  - every document in this folder
  - `CLAUDE.md`, `tools/README.md`, `PROJECT_FILE_GUIDE.md`
  - `open_questions_and_conflicts.md` (dated subsection appended)
- **Unchanged:** the protected paths listed in section 3.

The pipeline must be run in this order:

```
tds_sds_inventory.py → source_coverage_ledger.py → build_eligibility.py
```

The eligibility build stops if the ledger is stale.
