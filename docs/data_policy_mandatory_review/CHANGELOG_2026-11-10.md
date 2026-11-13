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

---

# After revision 3, 2026-11-11: policy-decision preparation (no rule, threshold or requirement changed)

Revision 3 is commit `43e7f8b`. The changes below sit on top of it.

- **"Decision H" withdrawn.** Reliable external evidence was already authorised, so it is not a blanket permission question. `external_review_decisions.json` and `external_review.csv` now record, for each source, authority, authenticity and provenance, and for each case exact product identity and applicability. `external_review.py` rejects a decision without them.
  - Result over the 29 cases: 28 manufacturer-issued and 1 distributor-issued; 21 name the record's exact grade, 8 not assessed (source not obtained).
  - aramcoULTRA 8: the merge question ID-01 (one product with Ultra-S 8?) is kept apart from the use of the S-OIL table that names aramcoULTRA 8. ID-01 stays open and does not restrict that table; the evidence-based restriction is the KV40 conflict with the SDS range.
  - No outcome, value or status changed. ID-01 is not resolved, and the distributor flyer's specific gravity for BAPbase 4 is not filled.
  - The pending reason of S_OIL_ARAMCO_ULTRA_8 in `source_selection.PENDING` is reworded (the ledger's `selection_reason` text changes with it).
- **New document:** [decision_brief_published_formulation.md](decision_brief_published_formulation.md). Neither option is implemented; the checker, the requirements version and the shared interface are unchanged. It states that no qualifying complete recipe is currently recorded, with the limits of the search, and that one accepted measured result establishes neither the finished-oil requirements nor any approval.
- **"Evidence unavailable" (181 rows) explained** in `evidence_review.md` section 10: 173 rows where documents were read and are insufficient, and 8 rows where the source could not be obtained. No verification status changed.
- Tests: `tools/data_policy/tests` 46 (one added: each source assessed separately).

## aramcoULTRA 8 technical-source selections (2026-11-11, uncommitted)

Decision: select the applicable technical-source value; record and assess its disagreement with the SDS separately. A disagreement is not a selection veto.

- **Confirmed** on both saved copies of the S-OIL manufacturer table (new tool `verify_soil_table.py`; hashes equal to the evidence manifest): caption "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8", row labels, ASTM cells and printed cells.
- **Selected** (three `CHANGES` entries; `S_OIL_ARAMCO_ULTRA_8` tier 1 and tier 2):

  | Field | Before (SDS DL2-14611.pdf p.2, 2018-09-07) | After (S-OIL table, typical) |
  |---|---|---|
  | KV40 | range 42.0–55.0 cSt at 40 °C, ASTM D445 | 41.10 cSt at 40 °C, ASTM D445 |
  | KV100 | range 7.0–7.5 cSt at 100 °C, ASTM D445 | 7.1 cSt at 100 °C, ASTM D445 |
  | Flash point | range 240–260 °C, ASTM D92 | 250 °C, COC, ASTM D92 |

  - Each SDS range is kept in `alternate_entries` with its page and revision date.
  - Each selected value cites the page URL with `revision_date` null, both saved copies with their SHA-256, and the caveat that the edition date of the page is unknown (a capture or retrieval date is not an edition date).
- **KV40 disagreement:** the existing 2026-10 audit conflict in `conflicts[]` is kept unresolved, with a dated note appended. Nothing was duplicated, and the v5 audit files are unchanged.
- **Pending:** the `PENDING` entry for these three fields is removed. ID-01 stays open; `S_OIL_ULTRA_S_8` and `reconciliation/` are unchanged.
- **Recommendation document** added and then corrected (unknown edition date; the VI calculation from memory removed; point-vs-range described as the current comparison policy): [recommendation_aramcoULTRA8_source_selection.md](recommendation_aramcoULTRA8_source_selection.md).

Counts after the change, all from the generated outputs:

| Number | Before (`43e7f8b`) | Now | Counting unit |
|---|---:|---:|---|
| Declared selections (`CHANGES`) | 39 | 42 | value object |
| Change-list rows | 50 | 53 | row (42 selections + 2 list fills + 2 qualifier corrections + 7 conflicts) |
| Pending fields in the ledger | 37 (19 mandatory) | 34 (17) | ledger row |
| External source selected | 22 (14 mandatory) | 25 (16) | ledger row |
| External review cases | 22 selected + 7 pending | 25 selected + 4 pending | product × property; outcomes unchanged (21 confirmed, 8 inconclusive) |
| Base oils with unresolved source selection, KV40 / KV100 | 5 / 4 | 4 / 3 | product |
| Tier 1 complete = eligible base oils | 10 | 11 | product |
| Fully documented (companion) | 11 | 11 | product |
| TDS–SDS inventory rows | 141 | 141 at this step; 151 after the extension below | pair |
| Product JSON files changed since revision 2 (`4e83652`) | 17 | 19 | file |

- **Interface.** `product_eligibility.csv`: same columns, same requirements version. One row changed, S_OIL_ARAMCO_ULTRA_8: `tier1_complete` and `formulation_eligible` false → true, `missing_mandatory_properties` `["kv40", "kv100"]` → `[]`, with a KV40 open-conflict warning in `eligibility_reasons`. The fingerprint column changed in every row.
- **Fingerprint.** Exact bytes: `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`. LF-normalised (informational): `6440b6800a2946ad8de0c419af5458695702c7e8fb0dced5230d086794a9474d`.
- **Tests.** `tools/data_policy/tests` 52 (six added in `TechnicalSelectionKeepsDisagreement`). `run_checks.py` had 23 steps at this step (new: `verify_soil_table`) and removes the step files of an earlier run.
- **Not changed.** Mandatory requirements, the published-formulation rule, the thresholds (still proposed), the review states of the ledger rows.

## Comparison inventory extended to external technical sources (2026-11-11, uncommitted)

Instruction: check SDS values whenever applicable technical evidence also exists, including external technical evidence.

- **`tds_sds_inventory.py`.**
  - A URL registered in `source_registry.json` is paired like an archive document: technical, or SDS when its registry title names a safety data sheet. An unregistered URL is never paired.
  - Each selected external technical value is also paired with every SDS value the inventory already holds for the same product and property.
  - New columns: `tds_value_kind`, `sds_value_kind`, `tds_source`, `sds_source`, `tds_revision_date`, `sds_revision_date`, `external_evidence`.
  - A pair whose external source could not be obtained becomes "comparability unknown" and is not screened.
  - One URL is one source however many saved copies exist; a pair found in `conflicts[]` and through an alternate entry is one row.
- **New tool `external_comparison_accounting.py`** → `reports/data_policy/external_comparison_accounting.csv`: every value whose selected source is a URL, with one comparison status and a reason. Two reviewed reasons are recorded in `external_review_decisions.json` (`comparison_reviews`): Ultra-S 3 density (the SDS prints only a vapour density) and aramcoULTRA 8 density (the SDS prints a relative density).
- **No product value, requirement or threshold changed.** The data fingerprint and the eligibility result are the same as after the aramcoULTRA 8 selections (11 of 181 base oils).

Calculated counts:

| Number | Before the extension | Now | Counting unit |
|---|---:|---:|---|
| Inventory rows | 141 | 151 | pair of a technical value and an SDS value |
| Rows with an external technical side | 0 | 10 | pair |
| Comparable / bound check / comparability unknown / not comparable | 47 / 53 / 38 / 3 | 52 / 56 / 40 / 3 | pair |
| Comparable pairs within print rounding | 26 | 28 | pair |
| Bound checks: compatible / outside / not parsed | 44 / 3 / 6 | 46 / 4 / 6 | pair |
| Ledger rows with a pair | 129 | 132 | product × property |
| Values with an external selected source, accounted for | — | 114 | value object |

The 10 external pairs: aramcoULTRA 8 KV40 (outside the SDS range; the existing unresolved conflict, one row), KV100 and flash point (numerically inside the SDS range; logically compatible, no agreement claimed); RF6078 density; RF6066 density (2), KV100 (2) and TBN; RF6069 KV100. The 141 earlier rows are unchanged in every earlier column.

Accounting of the 114 values:

| Comparison status | All 114 values | The 25 ledger `external_selected` values |
|---|---:|---:|
| paired with an SDS value in the inventory | 8 | 4 |
| inapplicable: text, classification, claim or block (no numeric comparison) | 41 | 0 |
| inapplicable: the external source is itself an SDS | 11 | 0 |
| inapplicable: the SDS prints a different quantity (reviewed) | 2 | 2 |
| unavailable: no SDS document is associated with the product | 1 | 1 |
| unavailable: no SDS page mentions the property | 14 | 14 |
| unresolved: the external source could not be obtained (value not verified) | 31 | 4 |
| unresolved: numeric property outside the coverage ledger, not assessed | 6 | 0 |
| **Total** | **114** | **25** |

- **Sensitivity** (`threshold_proposal.md` §4, re-checked): KV100 at the proposed 3 %: 2 below / 5 at or above (was 2 / 4); density at the proposed 0.005 g/cm³: 4 below / 0 (was 3 / 0). Both additions repeat a difference already present, through a second technical source. The conclusions are unchanged, and no threshold was applied.
- **Tests.** `tools/data_policy/tests` 61 (nine added in `ExternalComparisons`). `run_checks.py` has 24 steps (new: `external_comparison_accounting`).

---

# Four approved policies implemented (2026-11-11, requirements version `.4`, uncommitted)

Approved by you on 2026-11-11: ranges and bounds, co-component requirements, percentage basis, applicability. Plan and its corrections: [implementation_plan_policy_decisions_2026-11-11.md](implementation_plan_policy_decisions_2026-11-11.md). Rules in force: `requirements_review.md` §4a.

## What changed

- **`tools/mandatory_properties/requirements.py`** (version `mandatory-tier1-2026-11-10.4`):
  - new category `requirement_unknown`; new `Outcome.basis`;
  - `co_component_outcome` / `co_component_entries`: recorded supplier requirements are assessed one by one; a requirement recorded without a dose is no longer ignored;
  - `percentage_basis` (mass / volume / unspecified) and `volume_to_mass_percent` (refuses without both densities at one temperature);
  - `APPROVED_APPLICABILITY_RULES` is a list of rules keyed by product class, requirement and task, with `approved_rule`; it is empty;
  - I-1, I-6, I-8 and the new I-9 are marked as approved policies.
- **`build_eligibility.py`:** passes the product class and the reviewed statements to the checks; `requirement_outcomes.csv` gains a last column `percentage_basis`. The eleven interface columns are unchanged.
- **New `build_readiness.py`** and seven attribute files (`property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`, `calculation_readiness.csv`, `readiness_summary.md`).
- **New `compare_eligibility.py`** and saved baselines in `baselines/` (the eligibility file, the outcomes and the documentation coverage as they were before the implementation; the change report).
- **New `co_component_statements.json`:** two reviewed statements (HiTEC 12210 and 12210M: no supplemental PPD needed), scope PPD only.
- **`treat_rate_basis_evidence.json`:** each entry has `basis_class`, `evidence_kind` and `scope`; the result of the document-wide convention search is recorded.
- **`treat_rate_basis_scan.py`:** searches every page of each source document for a document-wide convention.
- **Tests:** `test_policies.py` (27 new); two older tests adjusted (silence is `requirement_unknown`; an evidence entry must name its basis).
- **`run_checks.py`:** 27 steps (new: `build_readiness`, its `--check`, `compare_eligibility`).
- **Not changed:** product JSON, templates, the workbook structure, the published-formulation requirement, the thresholds (still proposed), tiers. The simulation script is kept.

## Before and after (`compare_eligibility.py`)

| | Before (`.3`) | After (`.4`) |
|---|---:|---:|
| Base oils: `tier1_complete` = `formulation_eligible` | 11 of 181 | 11 of 181 |
| Packages | 0 of 78 | 0 of 78 |
| Components | 0 of 5 | 0 of 5 |
| Products whose eligibility fields or missing list changed | — | 0 |
| Requirement outcomes whose category changed | — | 66 |

- Data fingerprint unchanged: `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`.
- The 66 category changes are all `required_co_components`: `unresolved_applicability` → `absent` (35) or → `requirement_unknown` (31). They were unmet before and are unmet now.

## Current-data figures (from `readiness_summary.md`)

| | Count |
|---|---:|
| Mandatory requirement outcomes | 2,004 in 264 products |
| Evidence documented | 1,274 |
| Documented but incomplete (unit, condition, basis or source missing) | 24 |
| Not documented | 665 |
| Requirement unknown (co-components, silence) | 31 |
| Applicability unresolved | 10 |
| Documented ranges and bounds | 71 in 29 products (37 closed ranges, 22 lower bounds, 12 upper bounds) |
| Unresolved selections | 14 in 7 products |
| Dose values with an unspecified basis | 84 of 271, in 18 products |
| Dose values with a volume basis | 0 |
| N/A labels without a rule | 18 value objects in 4 products |
| Approved applicability rules | 0 |

---

# Gap fixes to the policy implementation (2026-11-11, requirements version `.5`, uncommitted)

Five gaps in the `.4` implementation were corrected. No product JSON, template, datasheet or evidence file changed; the data fingerprint is unchanged (`93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`).

## What was wrong and what changed

1. **Co-component completeness.** `.4` (like `.3`) counted the requirement as met when one recorded co-component had a usable dose. Completeness is now assessed per evidenced route: every requirement that applies to the route needs a usable dose, and the route's requirement list must be confirmed by source review. Routes come only from reviewed evidence (`co_component_route_evidence.json`, empty); nothing is mapped from role text; an unestablished association is reported as not assessed (new category `unresolved_route_association`). The "at least one usable dose" count is kept in the reason as information only. Free text in `co_component_requirement_statement` no longer passes: a "none required" statement must be structured, sourced, unqualified and cover all co-components (`explicit_none_required`).
2. **Selection status.** It is taken from the source-selection ledger for every outcome (`Outcome.selection_pending`, column `selection_pending`), not from the category.
3. **Percentage reporting.** `usable_where_wt_pct_is_required` is replaced by `basis_is_mass`, with the value's own check outcome beside it. Volume-basis dosage evidence kept in `external_fill_notes` is listed in the new `volume_dose_evidence.csv`. Counts state their scope.
4. **Conversion.** `volume_to_mass_percent` is unregistered and unused. Its code is kept; its documentation says it is arithmetic only and cannot establish the source, unit or applicability of its inputs.
5. **Evidence wording.** "Not recorded", "not found in the inspected text", "source unavailable / not inspected" and "confirmed by source review" are reported separately. The co-component scan now records which documents and pages it inspected and which it could not. Supplier qualifications are kept: the two PPD statements carry `qualification: 'should be needed'`.

## Changed counts, with reasons

| | Before (`.3`) | After (`.5`) |
|---|---:|---:|
| Base oils: `tier1_complete` = `formulation_eligible` | 11 of 181 | 11 of 181 |
| Packages | 0 of 78 | 0 of 78 |
| Components | 0 of 5 | 0 of 5 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 8 |
| Requirement outcomes whose category changed | — | 74 |

- **8 packages** gained `required_co_components` in their missing list: INFINEUM_D3354, D3384 and D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100 and CV1103. In `.3` (and in `.4`) each counted as met because one recorded co-component had a usable dose. That is not a complete route: 5 of the 8 also record a viscosity modifier without a dose, and for LUBRIZOL_3700 the source page says "when formulated with appropriate base oils and viscosity modifier" although the record lists only the booster. They are now `unresolved_route_association`. All 8 were ineligible before and stay ineligible (each also lacks the published formulation).
- **35 outcomes** moved from `unresolved_applicability` to `absent`: a co-component requirement is recorded and none of its doses is recorded, so no route that includes it can be complete.
- **31 outcomes** moved from `unresolved_applicability` to `requirement_unknown`: nothing is recorded in the record.
- No base oil and no component outcome changed category.

| Count | `.4` | `.5` | Reason |
|---|---:|---:|---|
| Pending selections (mandatory) | 14 | 17 | The status now comes from the ledger. The 3 added are aramcoPRIMA 110 / 230 / 500 density, which also lack a unit; that category had hidden them. Nothing was resolved in between |
| Co-component requirement met (packages) | 8 | 0 | One usable component is not a complete route; no route is reviewed |
| `unresolved_route_association` (packages) | — | 8 | The same 8 packages |
| Evidence "documented" (mandatory outcomes) | 1,274 | 1,266 | The same 8 outcomes are now `recorded_route_not_assessed` |
| Selected point values | 624 | 616 | The same 8 outcomes no longer count as a met point value |
| "none required" statements treated as partial | 2 | 2 | Unchanged in number; now also marked as qualified ("should be needed") |
| Co-component leads found by the scan (packages) | 13 | 16 | The search also matches "formulated with … viscosity modifier" |
| Packages with no recorded requirement | 31 | 31 | Now split by inspection: 27 not found in the inspected text, 1 unreviewed lead, 2 not inspected (no text layer), 1 source unavailable |
| Volume-basis evidence entries listed | 0 | 5 | AFTON_HITEC_5748 dosages in vol.%, kept in `external_fill_notes`; its wt.% fields stay Missing |
| Values in the dose fields: mass / unspecified / volume | 187 / 84 / 0 | 187 / 84 / 0 | Unchanged; the scope is now stated |

## Files

- Changed: `requirements.py`, `build_eligibility.py`, `build_readiness.py` (readiness version `.2`), `co_component_evidence_scan.py`, `co_component_statements.json`, tests.
- New: `co_component_route_evidence.json` (empty), `volume_dose_evidence.csv`, `tools/maintenance_2026-11-11/implementation_helpers/` (the helper scripts that were only in the scratch folder, with a README).
- Tests: `tools/mandatory_properties/tests` 66 (35 policy tests): two required components in one route, independent routes, unestablished association, stale or unsourced route evidence, free-text and qualified statements, a pending selection combined with missing metadata, a mass-basis value that is otherwise unusable, the unregistered conversion.

---

# Route-evidence binding, statement review and the route review of eight packages (2026-11-12, requirements version `.6`, uncommitted)

No product JSON, template, datasheet or evidence file changed. Data fingerprint unchanged: `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`. The reports and check results as they were before this work are in `baselines/pre_route_review_2026-11-12/`.

## Fixes

1. **Route-evidence freshness.** A route's evidence stored only the entry identity and `dose.value`. It now stores the SHA-256 of each complete record it relies on (`record_fingerprint`: values, range endpoints, unit, qualifier, conditions, role text, source file, page and revision; derived `*_final` keys excluded), for the co-component entries and the treat-rate entry. A change makes the route `route_evidence_stale`; unrelated product fields do not.
2. **Route memberships.** A recorded requirement can belong to several routes. `co_component_routes.csv` has one row per requirement and route, each with that route's assessment. Stale or invalid evidence is reported as `historical_source_review_not_current`, never as confirmed, and gives no current association.
3. **"None required".** `explicit_none_required` now needs an explicit reviewed assessment (product, meaning, unconditional, qualification verbatim, scope by component type and route, conditions). A missing qualification is no longer read as "unconditional"; contradictory or incomplete metadata is rejected; a hedge word in the quote together with "unconditional" is a contradiction (a guard, not the basis of the meaning). Inline and side-file statements pass the same check against the current product.
4. **Source review of eight packages**: [co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md). 29 routes recorded; 0 complete, 21 incomplete, 8 with usable recorded doses but an unconfirmed list. Five record corrections proposed, none applied.
5. **Baseline.** New `make_review_snapshot.py`; snapshot `review_snapshots/review_snapshot_2026-11-12/`. The snapshot is created after this document is final, so this text cannot contain its manifest hash: see `REFERENCES.txt` inside the snapshot, and `snapshot_verification_2026-11-12.txt` in this folder for the verification output and exit code (written after the snapshot, so it is not part of it).

## Before and after

**Route review of 2026-11-12 (version `.6`), against the baseline saved before it** (`baselines/pre_route_review_2026-11-12/`, comparison in `baselines/eligibility_changes__route_review_2026-11-12.csv`):

| | Before (`.5`) | After (`.6`) |
|---|---:|---:|
| Base oils / packages / components: `tier1_complete` = `formulation_eligible` | 11 / 0 / 0 | 11 / 0 / 0 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 0 |
| Requirement outcomes whose category changed | — | 4 |

The 4 category changes are `required_co_components`, from `unresolved_route_association` to `absent`:
- **INFINEUM_D3384, INFINEUM_D3451, LUBRIZOL_CV1100, LUBRIZOL_CV1103.** Their routes are now reviewed, and every one requires a viscosity modifier for which the datasheet prints no dose. The association is no longer unresolved; a documented requirement lacks its dose.
- **INFINEUM_D3354, LUBRIZOL_3589C, 3700, 3700D** stay `unresolved_route_association`: at least one of their routes has usable recorded doses but a requirement list that cannot be confirmed complete.
- All eight were unmet before and are unmet now. Detail per route: [co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md).

Pending selections are unchanged and still independently represented: 17 mandatory (14 in category `unresolved_source_selection`, 3 with a metadata defect).

## Files

- Changed: `requirements.py`, `build_readiness.py` (readiness version `readiness-2026-11-12.1`), `co_component_route_evidence.json`, `co_component_statements.json`, `run_checks.py` (28 steps), tests.
- New: `make_review_snapshot.py`, the route review document, helper scripts `route_review_*.py` in `tools/maintenance_2026-11-11/implementation_helpers/`.
- Tests: `tools/mandatory_properties/tests` 74.
