# Change log, 2026-11-10 (Workstream A)

Baseline: `f4d97e71f72598df601b72403775581c34061ad1`. Every change below can be reproduced with the commands in
[HANDOFF.md](HANDOFF.md).

## Product data (Rule 1, source selection)

The full per-field list, with before and after values, sources and printed evidence, is in
[reports/data_policy/source_selection_changes.csv](../../reports/data_policy/source_selection_changes.csv) (28 rows).

| Product (file) | Field | Before (source) | After (source) |
|---|---|---|---|
| INFINEUM_D3424 (tier 2) | flash_point | > 110 °C, SDS bound (DL2-10204 p.6) | 190 °C PMCC, ASTM D 93 (DL2-10204 p.1, TDS 2004-11-09) |
| RICHFUL RF6066 / 6069 / 6077 / 6078 / 6079 / 6088 / 6088F / 6400 / 6406 (tier 2) | flash_point | ≥ 180 or ≮ 180 °C, SDS bound | TDS typical 220 / 216 / 210 / 220 / 214 / 203 / 218 / 226 / 223 °C (COC, ASTM D92) |
| RICHFUL RF6069 / 6077 / 6079 / 6088 / 6400 / 6406 (tier 2) | density | SDS value | TDS typical at 20 °C: 981 / 998 / 1000 / 955 / 1039 / 1060 kg/m³ (the index range is kept in min/max) |
| RICHFUL RF6077 / 6078 / 6079 / 6088 / 6088F / 6400 / 6406 (tier 2) | kv100 | SDS value | TDS typical: 160 / 146 / 140 / 100 / 177 / 109 / 72 mm²/s |
| NESTE_NEXBASE_3020 (tier 1) | kv40, kv100, density | 7.5 (SDS); Missing; Missing | 7.5 / 2.2 mm²/s; 834 kg/m³ at 15 °C (DL2-10962.pdf, Edition 8) |
| NESTE_NEXBASE_3020 (tier 2) | pour_point, flash_point | ≤ −42 °C; > 150 °C (SDS bounds) | −45 °C; 160 °C (DL2-10962.pdf) |
| NESTE_NEXBASE_3020 (tiers 1–3) | product.source_file, document_type | SDS files only | DL2-10962.pdf added; "Safety Data Sheet; Technical Data Sheet" |

How each replaced value was handled:
- The replaced value is kept in `alternate_entries[]` with a `selection_note`.
- Its old value kind is relabelled as a lower or upper bound where it was printed as one. The previous label is kept in `value_kind_previous_label`.
- `*_final` keys are derived for the changed nodes by the same function that `integrate_products.py` uses.

Conflicts and open questions:
- **Reopened** (`resolved: false`): RICHFUL_RF6077 `tier2.density` and `tier2.kv100`, and RICHFUL_RF6088F `tier2.kv100`. Their 2026-10-18 user decisions are superseded by the policy and await the user's confirmation.
- **Notes appended**: conflict notes on D3424 flash point, RF6077 density/kv100 and RF6088F kv100.
- **Open questions**: two NEXBASE 3020 open questions are annotated with dated corrections. The record wrongly said that no TDS exists.

## Scripts

- `integrate_products.py`:
  - docstring rule 2 replaced (the old text is kept in parentheses);
  - the RF6077 density/kv100 and RF6088F kv100 `ANNOTATIONS` are re-pinned to the new values with new notes;
  - the matching `CONFLICTS` rules set `False` with the basis "source-selection policy 2026-11-10".
  - Dry run: no errors, 10/10 annotations, 16/16 conflict rules.
- New, under `tools/data_policy/`: `policy_lib.py`, `document_classes.py`, `tds_candidates.py`, `source_selection.py`, `integration_diff.py`, `tds_sds_inventory.py`, `thresholds.py` and `tests/`.
- New, under `tools/mandatory_properties/`: `requirements.py` and `build_eligibility.py`.

## Generated outputs

- `Coverage_Matrix.xlsx` (regenerated):
  - Base Oils: reported +2 and missing −2 (NEXBASE 3020 kv100 and density);
  - Status Detail: 6320 → 6346 rows (the new alternate entries);
  - Validation Issues: unchanged (30).
- `reports/data_policy/document_classes.csv`, `source_selection_changes.csv`, `tds_sds_comparisons.csv`.
- `reports/mandatory_properties/product_eligibility.csv`, `missing_mandatory_properties.csv` / `.md`.

## Documentation

- `CLAUDE.md`, `README.md`, `PROJECT_FILE_GUIDE.md`, `tools/README.md` and `requirements.txt` are updated.
- `open_questions_and_conflicts.md` has a new dated section at the end. Earlier sections, including the 2026-10-24 integration review, are historical and unchanged.

## Not changed

- The v5 audit (`reconciliation/comprehensive_conflicts_audit.md` / `.csv`, `findings_v5.json`) is a historical snapshot.
- No finding has been reclassified (Rule 2 review checkpoint).
- The archive, evidence copies, templates and glossary are unchanged.

---

# Revision 2, 2026-11-10 (provisional checkpoint corrections)

Content commit of revision 1: `8702228`. The changes below are uncommitted until the revision-2 commit recorded in HANDOFF.md.

## Validation bugs fixed (`tools/mandatory_properties/requirements.py`)

An independent review found five invalid synthetic inputs that the checker accepted. Each was reproduced, now fails, and is kept as a regression test in `tools/mandatory_properties/tests/test_requirements.py`, alongside a valid counterpart:

| Input | Before | Now |
|---|---|---|
| reversed range `[10, 2]` | accepted | `invalid_value` |
| infinity as a value | accepted | `invalid_value` |
| `≮ 180` | read as an exact value | lower bound: `bound_or_range_needs_assessment` |
| shear-loss note gives 10, stored 999, no source | accepted | `invalid_or_unreproducible_calculation` |
| thickening for Oil A at 1 % on an Oil B at 9 % record | accepted | `invalid_or_unreproducible_calculation` |

All numeric checks now cover:
- finite, non-boolean numbers and ordered ranges;
- a supported qualifier and value-kind vocabulary, including the Unicode inequalities ≥ ≤ ≮ ≯ ⩾ ⩽; unknown or conflicting qualifiers are invalid and never become exact values;
- a value lying inside its own recorded range.

Calculated values:
- They are accepted only through a registered check: ΔKV100, SSI, % viscosity loss.
- Each check:
  - recomputes the result and compares it with the stored and stated values;
  - matches the reference oil, dose, cycles, temperature and units with the response record;
  - requires the inputs to be printed on the cited page (archive text);
  - requires an index type that fits the requirement (a % viscosity loss is not an SSI);
  - rejects zero denominators without crashing.
- A `Calculated` status on blocks, claims and formulations is rejected; it cannot bypass these checks.

**Effect on actual products.** None of these fixes changed an actual eligibility decision.
- RF6602's calculated shear value, previously accepted, is now rejected: its index is a % viscosity loss, not an SSI.
- Its ΔKV100 values are rejected: no method is recorded, and the printed unit is "mm/s2".
- RF6602 was not eligible before and is not eligible now.

## Outcome categories and semantics (requirements version `mandatory-tier1-2026-11-10.2`)

- Every requirement outcome now has a category. The categories separate an absent value from a range or bound, a missing unit, condition or source, an invalid value, an unreproducible calculation, unresolved applicability, and a pending source selection.
- `tier1_complete`: every blocking requirement has documented information. `formulation_eligible`: every blocking requirement is met.
- **Ranges and bounds** are documented, but provisional per property (`REPRESENTATIONS`). Treat rates and doses accept a range, because the source says "min / max / typical".
- **Withdrawn interpretations:**
  - The VM/PPD subtype blocks are no longer blocking: they are tier 2 / tier 3 files, under your rule (decision C).
  - Markers for functions the slide does not name are now "unresolved applicability" instead of "not applicable".
  - A package with no co-component is now "unresolved applicability" instead of "absent". A sourced "none required" statement is accepted in the proposed field `co_component_requirement_statement`.
- **Mass basis.** It is accepted when established on the cited page, from `treat_rate_basis_evidence.json`: INFINEUM_D3384, INFINEUM_D3451, AFTON_HITEC_12360. For the other 18 products' bare "%" values it is not established and is not guessed.
- **New output** `requirement_outcomes.csv`. `missing_mandatory_properties.csv/.md` now carry the categories and a sensitivity table.

**Revised counts.**

| | Revision 1 | Revision 2 |
|---|---:|---:|
| Base oils eligible | 11 | 10 |
| Base oils Tier 1 complete | 11 | 11 |
| Packages eligible | 0 | 0 |
| Components eligible | 0 | 0 |

- **S_OIL_ARAMCO_ULTRA_8** is no longer eligible. Its KV40 and KV100 are SDS ranges, which revision 1 accepted, and its Rule 1 source selection is pending (an external web table vs the archived SDS; identity question ID-01).

## Rule 1 (source selection)

- **Clarified rule applied.** A technical specification range is selected as printed.
  - FORMOSA_150N_GII_PLUS KV100: 5.0–5.4 mm²/s, DL2-10001.pdf p.1, issued 2009-10-21.
  - FORMOSA_500N_GII KV100: 10–12 mm²/s, DL2-10003.pdf p.1.
  - The SDS typical values (5.2, 11 cSt) are kept as alternates, with their exact SDS lines. The old entry had mixed the specification range into the SDS record.
- **Field-level pending list.** `PENDING_FIELDS` was added: NEXBASE 3043–3080 now list the 15 fields where the family TDS and the individual sheets disagree.
- **Reviewed SDS fallbacks.** `SDS_FALLBACK_FIELDS` was added: FORMOSA KV40 and SG, and D3384 SG.
- **Selection tool.** `source_selection.py` now applies declared changes incrementally. It writes a file only when the content changes, and `--report` regenerates the full change list (30 rows).
- **Coverage ledger.** New tool `tools/data_policy/source_coverage_ledger.py` and outputs `reports/data_policy/source_coverage_ledger.csv` and `.meta.json`. The remaining gaps are listed in `source_review_coverage.md`.

## Thresholds (still PROPOSED)

`thresholds.py` is now `thresholds-2026-11-10-proposed.2`:
- "Ordinary" wording was replaced by "below the proposed project review threshold". A point compatible with a bound is "logically compatible (not evidence of agreement)".
- All thresholds are labelled empirical. The unverified ASTM statements are removed as justification.
- A value at the threshold is retained for review.
- A sensitivity output was added: `reports/data_policy/threshold_sensitivity.csv`.
- The inventory now has 67 comparisons; the FORMOSA KV100 pairs became bound checks.

## Reproducibility

- **New check** `tools/data_policy/verify_preserved.py` compares three byte forms per file: worktree, committed blob, and blob with CRLF.
  - Preserved files: 49/49 verified. 31 match the committed blob and 17 match the CRLF form. 1 file has no line endings and matches every form.
  - Evidence copies: 11/11 verified.
  - The archive equals both the HEAD and the baseline blobs.
  - No manifest was edited.
- **Informational LF-normalised data fingerprint** added to `missing_mandatory_properties.md`. The interface column keeps the exact-byte convention.
- **Eligibility build** stops if the coverage ledger was built from different data.

## Other

- `policy_lib.load` closes its file.
- Test results are saved in `docs/data_policy_mandatory_review/test_results/`.
- **Proposed record correction (not applied):** the qualifier on ERGON_HYGOLD_5000BS and P70N VI (`requirements_review.md` §6).
