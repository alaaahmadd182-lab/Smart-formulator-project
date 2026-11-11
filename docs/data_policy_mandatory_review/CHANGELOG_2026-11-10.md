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

---

# Revision 3, 2026-11-10 (evidence review; still provisional)

Revision 2 content commit: `4e83652`. The full review is in [evidence_review.md](evidence_review.md).

## Evidence review

- **Lead cases.** 363 product × property cases were reviewed: the 352 frozen from the revision-2 ledger plus 11 found during the review (corrected 2026-11-11 from "362"; see "Count reconciliation" below). Every case has a recorded outcome, with the source and page read (text layer or render), what is printed, the identity finding and the resulting change.

  | Outcome | Cases |
  |---|---:|
  | usable evidence | 81 |
  | already recorded | 31 |
  | unrelated mention | 71 |
  | insufficient evidence | 173 |
  | unresolved identity | 7 |

  Tool: `tools/data_policy/lead_review.py`. Output: `reports/data_policy/lead_review.csv`.
- **Name-match document links.** All 174 (product, document) pairs were reviewed: 87 same product, 78 byte-identical copies, 9 other product (87 + 78 + 9 = 174; the earlier "84" omitted 3 same-product pairs, see below). The 9 are excluded from the coverage ledger. Tool: `association_review.py`. Output: `name_match_review.csv`.
- **FORMOSA identity.** The KV100 specifications name the exact products ("Base Oil 150N GII+", "Base Oil 500N GII"), so the selections stand. The SDS fallbacks for KV40 and specific gravity move to pending, because the SDSs do not name the grade. The FPCC table (ID-15) was not used.

## Data changes (all declared in `source_selection.py`, idempotent, listed in `source_selection_changes.csv`)

| Change | Products and fields |
|---|---|
| Filled (11 fields: 9 single value objects + 2 CCS lists with 5 points) | CHEVRON_GROUP_II_600R KV40 (≥ 100); PETRONAS_ETRO_6 CCS (3 points); ARAMCO_LUBEREF_PRIMA_500 KV40 and CCS (2 points); CHEVRON_SYNFLUID_MPAO_65 flash (> 266 °C COC, SDS 270 °C as an alternate); ERGON_HYGOLD_P150BS Noack 1.1; EXXONMOBIL_SPECTRASYN_ULTRA_1000 SG 0.855; NEXBASE 3020/3043/3060/3080 SG (SDS fallback). Optional SG fields were created in the template's shape where absent. |
| Corrected | ERGON_HYGOLD_5000BS and P70N VI qualifier "minimum" → null (`qualifier_previous` kept). Checked against the rendered pages. |
| Conflicts added (not resolved) | `EVR-2026-11-10-ETRO4`, `-CV2301`, `-110-density`, `-230-density`, `-500-density`. The fields are added to `PENDING_FIELDS`. Two more were added on 2026-11-11 (external-source review, below). |
| Moved from reviewed SDS fallback to pending (identity) | FORMOSA 150N GII+ / 500N GII: KV40 and specific gravity. |

## Interface (version `mandatory-tier1-2026-11-10.3`)

- `tier1_complete` is restored to "all mandatory Tier 1 requirements satisfied" and equals `formulation_eligible`. The columns are unchanged.
- New companion file: `documentation_coverage.csv` (documented-but-unusable information; never completeness).
- **Counts.**

  | | Revision 2 | Revision 3 |
  |---|---:|---:|
  | Base oils complete and eligible | 10 | 10 |
  | Base oils "complete" (the `.2` meaning) | 11 | — |
  | Base oils fully documented (companion) | — | 11 |
  | Packages / components eligible | 0 | 0 |

  The only interface change on the current data is S_OIL_ARAMCO_ULTRA_8 `tier1_complete`: true (`.2` meaning) → false. The fills improved individual records but completed no product, because each still lacks another mandatory item.

## Tools and classifiers

- `document_classes.py`:
  - Lubrizol "Unloading, storage and blending instructions" pages are TECHNICAL/handling, not SDS.
  - Inside an SDS file, only an explicit technical-sheet heading makes a page technical (NEXBASE 3080 SDS p.4).
- `tds_sds_inventory.py`:
  - adds the SDS values recorded in the review (71 comparison rows for 70 product × property cases; 141 rows in total);
  - a flash-point pair needs the cup type on both sides before a difference is screened.
- `verify_preserved.py` reports separately:
  - worktree bytes matching the manifest (18/49 preserved, 11/11 evidence);
  - committed blobs matching (32/49, 11/11);
  - originals reproduced only by a CRLF write of the blob (17/49).
- New tools: `lead_review.py`, `association_review.py`, `co_component_evidence_scan.py`.

## Co-component evidence (no data change)

- 2 packages state that no supplemental PPD is needed (HiTEC 12210 / 12210M; PPD only).
- 13 packages name or require co-components, mostly without a dose.
- 63 packages have no explicit statement.

## Unchanged

- The v5 audit, the archive, the evidence copies, the templates and the glossary.
- The thresholds remain PROPOSED, and nothing has been reclassified.

## Count reconciliation (2026-11-11; every number recomputed from the generated records)

| Number | Counting unit | Composition | Generated record |
|---|---|---|---|
| 174 associations | (product, document) pair linked by name only, in the revision-2 ledger (`4e83652`) or the current one | 87 same product + 78 byte-identical copies + 9 other product | `name_match_review.csv` |
| 3 (the missing three) | associations reviewed as the same product and then used as fill sources, so the current ledger lists them as cited, not as name matches | EXXONMOBIL_SPECTRASYN_ULTRA_1000 / DL2-13746.pdf, NESTE_NEXBASE_3060 / DL2-12735.pdf, NESTE_NEXBASE_3080 / DL2-14512.pdf (column `now_cited`) | `name_match_review.csv` |
| 363 lead cases | product × property, deduplicated | 352 (revision-2 ledger) + 11 added: 8 linked by corrections (ETRO 4, PRIMA 110/230/500), PRIMA 500 KV40 and CCS (kept after their fill), NEXBASE 3080 flash point (appeared when its SDS p.4 stopped being classified as technical) | `lead_review.csv` |
| 81 usable evidence | lead case | 11 fill cases + 70 comparison cases (69 "comparison added" + CV2301 flash point, also a conflict) | `lead_review.csv` |
| 71 comparison rows | (product, property, SDS document) row added to the inventory | 70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs | `lead_review_decisions.json` → `tds_sds_comparisons.csv` (origin "lead review") |
| 141 comparison rows | TDS–SDS pair | 71 from the lead review + 70 from the audit, `conflicts[]` and `alternate_entries` | `tds_sds_comparisons.csv` |
| 11 filled fields | field (a value object or a whole CCS list) | 9 single-field fills (`CHANGES`) + 2 list fills (ETRO 6 CCS with 3 points, PRIMA 500 CCS with 2 points) | `source_selection_changes.csv` |
| 39 declared selections | `CHANGES` entry (one value object each) | 28 (revision 1: Richful, D3424, NEXBASE 3020) + 2 (revision 2: FORMOSA KV100) + 9 (revision 3 fills) | `source_selection.py` |
| 2 qualifier corrections | value object | ERGON 5000BS and P70N VI | `source_selection_changes.csv` |
| 7 conflicts added | `conflicts[]` entry | 5 (2026-11-10) + 2 (2026-11-11) | `source_selection_changes.csv` |
| 50 change-list rows | row of the change list | 39 selections + 2 list fills + 2 qualifier corrections + 7 conflicts | `source_selection_changes.csv` |

Corrected errors:
- "84 same product" omitted the 3 now-cited pairs, because the association review read only the current ledger. The review universe is now frozen at `4e83652` (as for the lead cases), and the pairs stay reported with `now_cited = true`.
- LUBRIZOL_CV2301 pour point had a reviewed SDS comparison, but its case fell under the generic Lubrizol "already recorded" rule. That rule now excludes cases with a reviewed comparison (`exclude_if_comparison`), so the case is usable evidence. Already recorded: 32 → 31; usable: 79 → 81 (with the added NEXBASE 3080 case).
- NEXBASE 3080 flash point had a reviewed comparison but no lead case; it is now in `added_cases`.

---

# Revision 3 completion, 2026-11-11 (external-source review, count reconciliation, check runner)

## External-source review

- **New tool** `tools/data_policy/external_review.py` with `external_review_decisions.json`; output `reports/data_policy/external_review.csv`. It stops if a decision no longer matches the record or a stored evidence hash changes.
- **Cases.** 29 product × property cases: the 22 values the ledger marks `external_selected`, plus 7 pending fields whose open question is an external technical source (AFTON_HITEC_8788B KV40/KV100/density/flash point; S_OIL_ARAMCO_ULTRA_8 KV40/KV100/flash point).

  | | Confirmed | Inconclusive: source unavailable |
  |---|---:|---:|
  | external selected values (22) | 18 | 4 (AFTON_HITEC_12204L KV100, density, flash point, TBN) |
  | pending, external alternative (7) | 3 (aramcoULTRA 8) | 4 (AFTON_HITEC_8788B) |

- **Evidence.** The aramcoPRIMA 230 sheet, the PRIMA 230 SDS, the MOGO 2025 flyer and the Aramco 2024 catalog were obtained with bytes equal to their `source_registry.json` SHA-256. The Richful data feeds were retrieved on 2026-11-11 and agree with the archived TDS. The S-OIL values were read on the two saved copies in `reconciliation/audit_evidence/` (hashes verified). The two Afton PDSs could not be obtained: the Internet Archive refused automated download and the fetch tool cannot open web.archive.org, so their values were **not** re-read.
- **Stored copies** (small files only): `reports/data_policy/external_evidence/` (4 files, marked `-text` so line endings are never converted). The 15 MB flyer and the catalog are not stored; their hashes are recorded.
- **Conflicts recorded (not resolved):**
  - `EVR-2026-11-11-230-noack`: the Aramco sheet's typical Noack 7.5 lies above the DL2-12172.pdf maximum 7;
  - `EVR-2026-11-11-230-density-external`: the Aramco sheet's 0.8635 kg/L is a third PRIMA 230 density (the field is already pending);
  - not added: the aramcoULTRA 8 KV40 disagreement (S-OIL typical 41.10 cSt below the SDS range 42.0–55.0 cSt) was already recorded as an unresolved edition-difference conflict by the 2026-10 audit (41.1 vs 42.0–55.0; not recorded twice).
- **Not changed:**
  - two representation notes (BAPbase 4 KV40 value_kind "single" under a "typical" column; aramcoULTRA 8 CCS qualifier "Typical"), because both read as point values in every check;
  - the PRIMA 230 CCS −20 °C point, because the fill rule covers Missing fields only;
  - the BAPbase 4 specific gravity printed by the distributor flyer (a policy decision on external sources).
- The `source_selection.PENDING` reasons for AFTON_HITEC_8788B and S_OIL_ARAMCO_ULTRA_8 now state the review result.

## Review states

- **New tool** `tools/data_policy/source_review_status.py`; output `reports/data_policy/source_review_status.csv`. Each of the 2,175 ledger rows gets one state:

  | State | Rows | Mandatory |
  |---|---:|---:|
  | archive lead review complete | 183 | 61 |
  | external review complete | 21 | 16 |
  | evidence unavailable (173 archive cases not printed + 8 external cases without a copy) | 181 | 81 |
  | evidence inconclusive (identity) | 7 | 2 |
  | not individually reviewed (mechanical classification only) | 1,783 | 745 |

## Check runner

- **New tool** `tools/data_policy/run_checks.py`. Each step is its own subprocess; its real return code and full output are saved in `test_results/NN_<step>.txt`, with `summary.md` / `summary.json`. A by-design failure (`verify_revision.py`) is reported as "expected failure", never as a pass.
- The four earlier result files (`01_pipeline.txt` … `04_protected_files.txt`) were produced through pipes that hid return codes. They are replaced; Git history keeps them.
- The runner exposed a masked non-zero return code: `integration_diff.py --changed` exits 1 whenever any derivation difference exists. It now takes `--against REF` and labels each difference pre-existing or NEW. All 20 differences in the 17 changed files are pre-existing at the baseline `f4d97e7`; none is new.

## Data fingerprint after these changes

- Exact bytes: `7600b30d8df614b669ff8fb4e5f0489c897c19ebdb0c35d9ab455bddf185cc8e`. LF-normalised (informational): `71481595b8e6ad80d010c5f08881e0a02d62c6f124eebbc8336ab6eeb963d578`.
- Eligibility is unchanged: 10 of 181 base oils, 0 packages, 0 components. The only interface change against revision 2 remains S_OIL_ARAMCO_ULTRA_8 `tier1_complete` true → false.
