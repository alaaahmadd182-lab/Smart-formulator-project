# HANDOFF: Workstream A (source selection, TDS–SDS review, mandatory Tier 1)

Date: 2026-11-10. Revision 2: a provisional checkpoint, **not approved final output**.

- Branch `feat/data-policy-mandatory-review`, in the worktree `C:\Users\windo\sf-wsA`.
- Not pushed, merged or opened as a PR.
- Association mining is not implemented. `analysis/association_mining/` is untouched (it does not exist on this branch).

| | Commit |
|---|---|
| Baseline (shared with Workstream B) | `f4d97e71f72598df601b72403775581c34061ad1` (origin/main, "Merge pull request #6") |
| Revision 1 content commit | `8702228ff8e465131a2a286c67775259214bb983` (+ `f9529a2`, which records it here) |
| Revision 2 content commit | the commit after `f9529a2` that adds this text: `git log --oneline f9529a2..HEAD` |

## 1. Completed in revision 2

1. **Validation bugs.** Five invalid inputs were reproduced, fixed and kept as regression tests with valid counterparts:
   - a reversed range;
   - infinity;
   - `≮` read as an exact value;
   - a shear-loss calculation with stored 999 vs stated 10, and no source;
   - a thickening calculation for another oil and dose.

   The checks now cover:
   - finite, non-boolean numbers and ordered ranges;
   - a supported qualifier / value-kind vocabulary, including Unicode inequalities; conflicting or unknown qualifiers are invalid;
   - registered calculation checks: recomputed result, matching oil, dose, cycles and units, inputs printed on the cited page, an applicable index type, zero denominators.
   - A `Calculated` status cannot bypass these checks through blocks, claims or formulations.
   - **None of these fixes changed an actual product decision** (CHANGELOG, revision 2).
2. **Outcome categories.** Every requirement outcome is now one of: met, absent, bound/range needing assessment, missing unit/condition/provenance, invalid value, unreproducible calculation, unresolved applicability, unresolved source selection.
   - `tier1_complete` (documented) and `formulation_eligible` (met) are now distinct. The interface columns are unchanged; the version is `mandatory-tier1-2026-11-10.2`.
   - A new detail report `requirement_outcomes.csv` was added.
3. **Authority map** ([requirements_review.md](requirements_review.md)). Every requirement is mapped to its source wording, status (explicit / conditional / optional), interpretation, affected products and open decision. Decisions A–E are worked through, plus F, G and per-property representations (B-REP).
   - Withdrawn: VM/PPD subtype blocks are no longer blocking (they are tier 2/3 files). Markers for functions the slide does not name, and missing co-component architecture, are now "unresolved applicability".
   - Mass basis: established from the page for 3 products. For the other 18 it is not established and not guessed.
4. **Source-selection coverage.**
   - A new ledger covers every base-oil and package property, whether currently selected from a technical document or from an SDS ([source_review_coverage.md](source_review_coverage.md)).
   - FORMOSA 150N / 500N KV100: the technical specification range is now selected as printed, with the SDS typical kept as an alternate.
   - NEXBASE pending cases are now field-level (15 fields).
   - Reviewed SDS fallbacks are recorded.
5. **Threshold proposal, revision 2** ([threshold_proposal.md](threshold_proposal.md)).
   - Wording corrected ("below proposed project review threshold"; "logically compatible, not agreement").
   - All thresholds are labelled empirical. The ASTM claims are unverified and are no longer used as justification.
   - The reporting increment is not used as a tolerance.
   - A sensitivity table was added.
   - Specific gravity is dimensionless; the units in this file are corrected.
6. **Reproducibility.**
   - A form-aware check of the preserved files and evidence was added.
   - An informational LF-normalised data fingerprint was added.
   - The eligibility build refuses a stale ledger.
   - Test and check outputs are saved in `test_results/`.

## 2. Rules: provisional vs approved

| Rule | Status |
|---|---|
| Rule 1 source selection: technical first, SDS fallback, technical range/bound selected as printed | Given by you; applied (30 field selections) |
| Exceptions (2), pending field list, reviewed SDS fallbacks | Applied with recorded reasons; the pending cases await a decision |
| Rule 2 screening thresholds | **PROPOSED**: KV40/KV100 3 %, density 0.005 g/cm³, specific gravity 0.005 (dimensionless), flash point 10 °C, pour point 3 °C; Noack and TBN none. Not applied; no finding reclassified; v5 unchanged. |
| Rule 3 mandatory requirements | Explicit items are from the MPS and glossary. Interpretations I-1 … I-8, the representation rules and the subtype/marker/co-component handling are **provisional**. No applicability rule is approved. |

## 3. Eligibility (provisional rules `mandatory-tier1-2026-11-10.2`)

Fingerprints of the data:
- Exact-byte snapshot (CRLF checkout): `63537ed984b2402f264bb9b5975187492962e1d8513bb1f1bfdb9fc35911bf38`.
- Informational LF-normalised fingerprint: `6237a76d86c8145e1b307e9b653b4caa41558f29bcf42033ae89ce18be7cdb4b`.

| Class | Products | Tier 1 complete | Formulation-eligible |
|---|---:|---:|---:|
| base_oil | 181 | 11 | 10 |
| additive_package | 78 | 0 | 0 |
| additive_component | 5 | 0 | 0 |
| **Total** | **264** | **11** | **10** |

**Eligible base oils:** ADNOC_ADBASE_4CST, _6CST and _8CST; PETRONAS_EQUINAS_8; PETRONAS_ETRO_6_PLUS (with open-conflict warnings on KV40 and density); PETRO_CANADA_PURITY_VHVI_2, _3, _4, _6 and _8.

**Change from revision 1** (11 eligible):
- S_OIL_ARAMCO_ULTRA_8 is now Tier 1 complete but not eligible.
- Its KV40 and KV100 are SDS ranges, which revision 1 accepted and which are now documented but provisional.
- Its Rule 1 selection is also pending: an external web table vs the archived SDS, plus identity question ID-01.
- The validation-bug fixes did not change this or any other decision.

**Main reasons, by category** (full table in `reports/mandatory_properties/missing_mandatory_properties.md`):

| Class | Category | Unmet requirements |
|---|---|---|
| Base oils | absent | CCS 132, density 95, API group 73, VI 46 |
| | bound / range needing assessment | VI 27, KV100 17, KV40 13, CCS 12 |
| | unresolved source selection | 11 |
| | unresolved applicability | 5 (Risella "Not Required") |
| Packages | published formulation absent | all 78 |
| | co-component architecture unresolved | 66 |
| | treat-rate mass basis missing | 15 |
| Components | function-specific marker applicability unresolved | all 5 |

## 4. Remaining source-review gaps (not done; see source_review_coverage.md)

- **137 comparison gaps** (32 mandatory): a technical page and an SDS page both mention the property, but no comparison is recorded. **The TDS–SDS check is not exhaustive.**
- **165 "Missing, label found" leads** (89 mandatory), not reviewed. A sample of 22 was inspected: most are "Report"/"N/A" cells or label noise. Some need column-level reading: ARAMCO DURA, the Petro-Canada multi-grade table, APE Core 2500 CCS, and a lb/gal density without temperature.
- **61 Missing rows** with image-only associated documents that were not read for the property.
- **External sources** were not re-read. The AFTON_HITEC_8788B external PDS has not been reviewed.
- **Name-match document associations** (48 products) are unverified.
- **Proposed record correction, not applied:** ERGON_HYGOLD_5000BS / P70N VI qualifier.

## 5. Tests and checks (saved in `test_results/`)

| Check | Result |
|---|---|
| `tools/mandatory_properties/tests` | 30 tests OK |
| `tools/data_policy/tests` | 26 tests OK |
| `tools/audit/review_2026-11-02/tests` (v5) | OK, unchanged |
| `source_selection.py` (dry run) | 30/30 declared selections in the data, nothing to write |
| `build_eligibility.py --check` | up to date |
| `integrate_products.py` (dry run) | no errors; annotations 10/10, conflict rules 16/16; would change 229 files (baseline 230); **do not `--write`** |
| `integration_diff.py --changed` | 6 differences in the 2 FORMOSA files, all earlier gaps in untouched fields (density, specific gravity) |
| `Coverage_Matrix.xlsx` | regenerated; validation issues 30 (unchanged) |

**Protected files** (`verify_preserved.py`):

| Item | Result |
|---|---|
| Preserved files | 49/49 verified: 31 = committed blob, 17 = blob with CRLF (original CRLF bytes), 1 = all forms |
| Evidence copies | 11/11 verified |
| Archive ZIP (SHA-256 `6488b08f…5497a`) | worktree = HEAD blob = baseline blob |

- No diff against the baseline in the archive, the templates, the glossary, `reconciliation/` (v5 audit and evidence), `tools/audit/`, the historical `tools/` folders, `docs/audit_review_2026-11-02/` or `source_registry.json`.
- **Cause of the 31 "failures" in revision 1:** this machine's system Git config (`core.autocrlf=true`) checks LF originals out with CRLF. No file changed.
- **Safe procedure:** run `python tools/data_policy/verify_preserved.py` in any checkout. In a CRLF checkout, do not use a bare `sha256sum -c`. No manifest was edited, and no evidence was normalised.

## 6. Reproduce

Run from the repository root (Python 3.12, `pip install -r requirements.txt`), in this order:

```
python tools/data_policy/document_classes.py
python tools/data_policy/source_selection.py                 # dry run; --write applies declared selections; --report writes the change list
python tools/data_policy/tds_sds_inventory.py                # comparisons + threshold_sensitivity.csv
python tools/data_policy/source_coverage_ledger.py           # ledger + .meta.json (fingerprint)
python tools/mandatory_properties/treat_rate_basis_scan.py   # reading aid for the mass basis
python tools/mandatory_properties/build_eligibility.py       # --check to compare without writing; exit 3 = stale ledger
python build_coverage_matrix.py --output Coverage_Matrix.xlsx --overwrite
python integrate_products.py                                 # dry run only
python tools/data_policy/verify_preserved.py
python -m unittest discover -s tools/mandatory_properties/tests -v
python -m unittest discover -s tools/data_policy/tests -v
python -m unittest discover -s tools/audit/review_2026-11-02/tests -v
```

Regenerate the ledger and the eligibility outputs after any product-JSON change, and after any checkout whose byte conversion differs.

## 7. Interface for Workstream B

See [eligibility_interface.md](eligibility_interface.md).
- The columns are unchanged.
- `tier1_complete` and `formulation_eligible` can now differ.
- The list columns are JSON arrays, and each reason is prefixed with its category.
- **The rules are provisional.** Treat the file as a checkpoint, not a final list, and recompute it on a fingerprint mismatch.

## 8. Warnings: historical generators

Do not run any of the following against the current data:
- `tools/corrections_2026-10-31/apply_corrections.py` and `update_curated_log.py` (hard-coded main-checkout path);
- `tools/integration_2026-10-24/resolve_json.py --write`;
- the `tools/audit/original_2026-10-27_to_30/` generators;
- the `tools/audit/review_2026-11-02/` report generators (`revise_findings.py`, `gen_report_v5.py`, `run_all_checks.py`);
- `integrate_products.py --write` on the whole repository.

`verify_revision.py` compares the protected files with `545fd3d` and now fails by design.
