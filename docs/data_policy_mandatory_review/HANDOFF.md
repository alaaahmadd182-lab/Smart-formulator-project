# HANDOFF: Workstream A (source selection, TDS–SDS review, mandatory Tier 1)

Date: 2026-11-11. **Revision 3: a provisional checkpoint, not approved and not complete.**

- Branch `feat/data-policy-mandatory-review`, in the worktree `C:\Users\windo\sf-wsA`.
- Not pushed, merged or opened as a PR.
- Association mining is not started; `analysis/association_mining/` is untouched (it does not exist on this branch).
- **Workstream A is not complete.** Source gaps and policy decisions remain (sections 4 and 2).

| | Commit |
|---|---|
| Baseline (shared with Workstream B) | `f4d97e71f72598df601b72403775581c34061ad1` (origin/main) |
| Revision 1 | `8702228` (+ `f9529a2`) |
| Revision 2 | `4e83652` |
| Revision 3 | the commit after `4e83652` that adds this text: `git log --oneline 4e83652..HEAD` |

## 1. Completed in revision 3

Every count below has its counting unit and composition in the changelog, section "Count reconciliation".

1. **Archive lead review** ([evidence_review.md](evidence_review.md) §1).
   - **Cases.** 363 product × property cases: the 352 of the revision-2 ledger, frozen, plus 11 found during the review.
   - **Order.** Mandatory leads first, then image-only cases, then the other leads, then the comparison gaps.
   - **Recorded per case.** Source and page; identity; what is printed (unit, qualifier, method, conditions); the outcome; and the resulting change or the reason for none.
   - **Outcomes.**

     | Outcome | Cases |
     |---|---:|
     | usable evidence (11 fills + 70 comparison cases) | 81 |
     | already recorded | 31 |
     | unrelated mention | 71 |
     | insufficient evidence | 173 |
     | unresolved identity | 7 |
     | unavailable source | 0 |
     | not reviewed | 0 |

   - Multi-grade tables and image-only files were read on renders.
2. **External-source review** ([evidence_review.md](evidence_review.md) §8; `external_review.csv`).
   - **Cases.** 29 product × property cases: the 22 values selected from registered URLs, plus 7 pending fields whose open question is an external source.
   - **Confirmed: 21** (18 selected, 3 pending). Each was re-read on a copy whose identity is established: registry SHA-256 match, a saved evidence copy with a verified hash, or the Richful data feed agreeing with the archived TDS.
   - **Inconclusive, source unavailable: 8.** These are the Afton HiTEC 12204L PDS (4 selected values) and the HiTEC 8788B PDS (4 pending fields). The Internet Archive refused automated download, and no saved copy exists. Their values were **not** re-read.
3. **Document identity.**
   - All 174 name-match associations were reviewed: 87 same product, 78 byte-identical copies, 9 other product. The 9 are excluded.
   - The earlier "84 same product" omitted the 3 same-product pairs that later became fill sources; the association universe is now frozen at `4e83652`, as the lead cases are.
   - FORMOSA KV100: each specification names the exact product, so the selections stand. ID-15 was not used, and the FORMOSA SDS fallbacks are pending (identity).
4. **Evidence-supported corrections only** (declared, idempotent, 50 rows in `source_selection_changes.csv`):
   - 11 fields filled from exact product-specific printed evidence (9 single fields + 2 CCS lists);
   - 2 ERGON VI qualifiers corrected against the rendered pages;
   - 7 disagreements recorded as unresolved conflicts: 5 from the archive review and 2 from the external review (PRIMA 230 Noack and density). The aramcoULTRA 8 KV40 disagreement was already a conflict (2026-10 audit) and is not recorded twice.
   - No value was invented, no basis assumed, nothing inferred from a family document, no unit or condition converted, and no formulation constructed.
5. **Interface meaning restored (version `mandatory-tier1-2026-11-10.3`).**
   - `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied.
   - Documentation coverage is a separate companion, `documentation_coverage.csv`.
   - No new gate was added; the authority of each gate is in `requirements_review.md`.
6. **Review state of every ledger row** (`source_review_status.csv`; 2,175 rows):

   | State | Rows | Mandatory |
   |---|---:|---:|
   | archive lead review complete | 183 | 61 |
   | external review complete | 21 | 16 |
   | evidence unavailable | 181 | 81 |
   | evidence inconclusive | 7 | 2 |
   | not individually reviewed | 1,783 | 745 |

   A recorded outcome for every case is **not** a claim that all source verification is complete.
7. **Reliable check runner** (`tools/data_policy/run_checks.py`). Every step runs as its own subprocess, and its real return code and full output are saved (section 5).
8. **Corrections found by the review.**
   - **Classifiers:** Lubrizol handling pages are now technical; inside an SDS file, only a strong technical heading makes a page technical.
   - **Inventory rule:** a flash-point pair needs the cup type on both sides.
   - **Lead rules:** CV2301 pour point is now usable evidence, and NEXBASE 3080 flash point has a case.
   - **Docs:** a revision-2 sentence in `requirements_review.md` ("complete but not formulation-eligible") is corrected.

## 2. Rules and decisions: provisional vs approved

| Rule | Status |
|---|---|
| Rule 1 (technical first, SDS fallback; range/bound selected as printed) | Given by you; applied: 39 declared selections, plus list fills, qualifier fixes and conflict additions. **Open:** whether an external (non-archive) technical document qualifies (decision H) |
| Pending source selections | 37 fields, each with a reason (`source_review_coverage.md`) |
| Rule 2 thresholds | **PROPOSED**, not applied. KV40/KV100 3 %; density 0.005 g/cm³; specific gravity 0.005 (dimensionless); flash point 10 °C; pour point 3 °C; Noack and TBN none. All empirical; the ASTM claims are unverified. Sensitivity re-checked on the 141-row inventory: the conclusions hold. |
| Rule 3 requirements | Items explicit in the spec PDF and glossary. Interpretations I-1 … I-8, the representations, and the subtype/marker/co-component handling are **provisional**. No applicability rule is approved. |

**Policy decisions requiring your approval** (none applied):

| # | Decision | Effect on the current data | Where |
|---|---|---|---|
| A | Keep "published formulation" mandatory for packages as written, or reclassify it | All 78 packages fail it today | `requirements_review.md` §4 |
| B / B-REP | Co-component evidence, and acceptable representations (ranges, bounds) per property | Accepting all ranges and bounds: still 10 eligible | §4 |
| C | VM/PPD subtype blocks: stay non-blocking? | Non-blocking now; making them blocking could only lower eligibility (0 components are eligible today) | §4 |
| D | CCS / API-group applicability for non-engine base oils (Shell Risella "Not Required") | 3 products in "unresolved applicability" | §4 |
| E | Unknown treat-rate mass basis | 15 package requirements unmet | §4 |
| F, G | Marker applicability; template field for co-components | 5 components; template change | §4 |
| H | External technical source vs archived SDS; distributor documents filling Missing fields | aramcoULTRA 8 KV40/KV100/flash point pending. It would be the 11th eligible product if its pending selections were accepted, but its KV40 conflict (2026-10 audit) stays open | §4 H |
| Rule 2 | Adopt, change or reject each screening threshold; split mixed findings? | Nothing reclassified until approved | `threshold_proposal.md` §7 |

## 3. Eligibility (version `.3`)

- **Data fingerprint, exact bytes** (authoritative; CRLF checkout): `7600b30d8df614b669ff8fb4e5f0489c897c19ebdb0c35d9ab455bddf185cc8e`.
- **LF-normalised fingerprint** (informational only): `71481595b8e6ad80d010c5f08881e0a02d62c6f124eebbc8336ab6eeb963d578`.

| Class | Products | Tier 1 complete = formulation-eligible | Fully documented (companion, not completeness) |
|---|---:|---:|---:|
| base_oil | 181 | 10 | 11 |
| additive_package | 78 | 0 | 0 |
| additive_component | 5 | 0 | 0 |
| **Total** | **264** | **10** | **11** |

**Eligible:** ADNOC_ADBASE_4CST, 6CST and 8CST; PETRONAS_EQUINAS_8; PETRONAS_ETRO_6_PLUS (open-conflict warnings on KV40 and density); PETRO_CANADA_PURITY_VHVI_2, 3, 4, 6 and 8.

**Change from revision 2.**
- S_OIL_ARAMCO_ULTRA_8 `tier1_complete` changes from true to false, because the interface meaning is restored. It is documented but not satisfied: its KV40/KV100 are SDS ranges, and their source selection is pending (decision H).
- The eligible products are unchanged. The 2026-11-11 changes (conflict entries only) changed no eligibility.
- The fills completed no product, because each filled product still lacks another mandatory item. For example: ETRO 6 lacks KV40 and density; PRIMA 500 has a KV100 range and pending density; 600R lacks density and CCS.

**Main reasons, by category** (`missing_mandatory_properties.md`):

| Class | Category | Unmet requirements |
|---|---|---|
| Base oils | absent | CCS 130, density 95, API group 73, VI 46 |
| | bound / range needing assessment | VI 27, KV100 17, KV40 14, CCS 12 |
| | unresolved source selection | 16 |
| | unresolved applicability | 5 |
| | missing unit | 3 |
| Packages | published formulation absent | 78 |
| | co-component architecture unresolved | 66 |
| | treat-rate mass basis not stated | 15 |
| Components | function-specific marker applicability unresolved | 5 |

## 4. Remaining evidence gaps

**Unavailable or inconclusive (8 external cases + 181 + 7 reviewed rows):**
- **Afton HiTEC 12204L and 8788B PDSs (Internet Archive):** not obtainable by the tools in this session. A manual download whose bytes match the registry SHA-256 (`7a1e57d8…`, `c09305fb…`) would allow both reviews. 8788B KV40/KV100/density/flash point stay pending until then.
- **Not printed for the grade** in the archive documents (173 cases).
- **Identity not established:** FORMOSA SDSs, ID-15, ID-01.

**Not resolvable from the archive** (needs supplier documents or a decision):
- values lacking a required condition (density with no temperature or unit);
- inconsistent labels or units;
- provisional typicals (aramcoPRIMA 110/230);
- conflicting undated technical documents (ETRO 4, NEXBASE, PRIMA density, RF6066, RF6069, CV2301);
- external technical page vs archived SDS (decision H).

**Not individually reviewed:** 1,783 ledger rows rest on the mechanical page classification only.

## 5. Checks (`python tools/data_policy/run_checks.py`; saved in `test_results/`)

Run on 2026-11-11, before the revision-3 commit, on the final working tree. Full output per step is in `test_results/NN_<step>.txt`; the summary is in `summary.md` / `summary.json`. **Overall: PASS** (every required step met its expectation).

| # | Step | Return code | Verdict |
|---:|---|---:|---|
| 1–11 | pipeline (document classes → eligibility) | 0 each | pass |
| 12 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 13 | coverage matrix | 0 | pass (validation issues 30) |
| 14 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 15 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 20 differences in 17 files, all pre-existing at the baseline, 0 new |
| 16 | `verify_preserved.py` | 0 | pass (section 6) |
| 17 | protected paths vs baseline | 0 | pass (no differences) |
| 18 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 19 | `tools/mandatory_properties/tests` | 0 | 31 OK |
| 20 | `tools/data_policy/tests` | 0 | 45 OK |
| 21 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 22 | `verify_revision.py` (v5) | 1 | **expected failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

- **Expected incomplete verification is not an execution failure.** The 8 unavailable external cases and the insufficient archive evidence are outcomes inside steps 6–8, which return 0.
- **Masked return code found and fixed.** The earlier saved results used pipes, which hid one non-zero return code (`integration_diff.py --changed` returns 1 whenever any difference exists). It now separates pre-existing differences from new ones.

## 6. Protected files (`verify_preserved.py`)

| Kind | Exact original-byte representation | Worktree bytes = manifest | Committed blob = manifest | Reproduced only by writing the blob with CRLF |
|---|---:|---:|---:|---:|
| preserved files | 49/49 | **18/49** | 32/49 | 17/49 |
| evidence | 11/11 | 11/11 | 11/11 | 0/11 |

- **31 worktree files in this checkout are not byte-identical to the originals.** The cause is CRLF conversion at checkout, not a content change. A reconstructed match is not proof that the local worktree files are original bytes.
- **Archive:** worktree = HEAD blob = baseline blob.
- **No diff against the baseline** in the archive, templates, glossary, `reconciliation/` (v5 and evidence), the historical `tools/` folders, `docs/audit_review_2026-11-02/` or `source_registry.json`. No manifest was edited.
- **New external evidence copies** (`reports/data_policy/external_evidence/`, 4 files, `-text`): their SHA-256 values are recorded in `external_review_decisions.json` and checked on every run.

## 7. Reproduce

From the repository root (Python 3.12, `pip install -r requirements.txt`):

```
python tools/data_policy/run_checks.py        # runs everything below in order and saves each return code and output
```

The order of the pipeline steps:

```
python tools/data_policy/document_classes.py
python tools/data_policy/source_selection.py                 # dry run; --write applies declared changes; --report writes the change list
python tools/data_policy/tds_sds_inventory.py                # comparisons (incl. reviewed SDS values) + threshold_sensitivity.csv
python tools/data_policy/source_coverage_ledger.py           # ledger + .meta.json (uses reviewed associations)
python tools/data_policy/association_review.py               # name_match_review.csv (universe frozen at 4e83652 + current)
python tools/data_policy/lead_review.py                      # lead_review.csv (case set frozen at 4e83652 + added cases)
python tools/data_policy/external_review.py                  # external_review.csv (stops on a stale decision or evidence hash)
python tools/data_policy/source_review_status.py             # source_review_status.csv
python tools/mandatory_properties/treat_rate_basis_scan.py
python tools/mandatory_properties/co_component_evidence_scan.py
python tools/mandatory_properties/build_eligibility.py       # --check compares without writing; exit 3 = stale ledger
python build_coverage_matrix.py --output Coverage_Matrix.xlsx --overwrite
python integrate_products.py                                 # dry run only
python tools/data_policy/integration_diff.py --changed --against f4d97e71f72598df601b72403775581c34061ad1
python tools/data_policy/verify_preserved.py
python -m unittest discover -s tools/mandatory_properties/tests -v
python -m unittest discover -s tools/data_policy/tests -v
python -m unittest discover -s tools/audit/review_2026-11-02/tests -v
```

## 8. Interface for Workstream B

See [eligibility_interface.md](eligibility_interface.md).
- The columns are unchanged.
- In version `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied.
- **The rules are provisional.** Treat the file as a checkpoint, and recompute it on a fingerprint mismatch (the exact-byte fingerprint is authoritative).

## 9. Warnings: historical generators

Do not run any of the following against the current data:
- `tools/corrections_2026-10-31/*` and `tools/integration_2026-10-24/resolve_json.py --write`;
- the `tools/audit/original_2026-10-27_to_30/` generators;
- the `tools/audit/review_2026-11-02/` report generators;
- `integrate_products.py --write` on the whole repository.

`verify_revision.py` fails by design, because it compares with `545fd3d`.
