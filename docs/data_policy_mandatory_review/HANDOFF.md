# HANDOFF: Part A / Workstream A (source selection, TDS–SDS review, mandatory Tier 1)

Date: 2026-11-13. **Revision 4: published to `main` for the Part B handoff. Published does not mean approved or complete.**

## 0. Published state (read this first)

**What is published.** The Part A implementation, from branch `feat/data-policy-mandatory-review` merged into `main`
through a pull request:
- the source-selection policy and tools (`tools/data_policy/`);
- the TDS/SDS comparison inventory and reports;
- the evidence, lead and external-source reviews;
- the mandatory-property and eligibility tools (`tools/mandatory_properties/`);
- the declared, evidence-supported product corrections (in this revision: the three aramcoULTRA 8 technical-source
  selections, section 1 item 4);
- the tests and the check runner;
- the saved baselines used by `compare_eligibility.py` (`baselines/`);
- the check record of the published candidate (`test_results/`), and this documentation.

**What is NOT published**, and stays outside `main`:
- **New-dataset work.** The new-dataset ("Downloaded lubricants sheets") comparison and its unapplied proposals
  (`existing_product_comparison_2026-11-12/`, `incoming_dataset_review_2026-11-12/`), and any future ingestion pipeline.
  This is a separate, ongoing task. It stays untracked in the Part A worktree `C:\Users\windo\sf-wsA`. None of its proposals
  has been applied to `Products_json`.
- **`review_snapshots/`.** The local frozen copy of the reviewed state (2026-11-12). The published commit is the shared frozen
  state; the snapshot folder stays in the worktree as local evidence.

**Status of the rules** (detail in section 2):
- **Approved and implemented:** Rule 1 (technical source first, SDS fallback, range/bound selected as printed), as given by the
  project owner, and the four policies approved on 2026-11-11 (ranges and bounds, co-component routes, percentage basis,
  applicability).
- **Proposed, NOT approved and NOT applied:**
  - the Rule 2 screening thresholds (`threshold_proposal.md`);
  - interpretations I-2 to I-5 and I-7;
  - decisions A, C and G, and the open remainders of B and D (section 2);
  - five co-component record corrections (`co_component_route_review_2026-11-12.md`).
- **No applicability (N/A) rule is approved.**

**Scientific questions stay open.** Publishing the implementation resolves none of them.
- The open conflicts are listed in the product JSON `conflicts[]`, `open_questions_and_conflicts.md` and section 4. Examples:
  the aramcoULTRA 8 KV40 disagreement, ETRO 6+ KV40 / density, PRIMA density, and the undated conflicting documents.
- The evidence gaps are in section 4: 8 unavailable external cases, 173 insufficient archive cases, 7 unresolved identities, and
  1,783 ledger rows not individually reviewed.

**What Part B should consume.**
- **Main file.** `reports/mandatory_properties/product_eligibility.csv`. The interface is in
  [eligibility_interface.md](eligibility_interface.md): eleven fixed columns, `requirements_version`
  `mandatory-tier1-2026-11-10.6`.
- **Companions.** `requirement_outcomes.csv` and `documentation_coverage.csv`. The attribute files from `build_readiness.py`
  are optional.
- **Freshness rule.** Each row carries `source_snapshot_sha256`, the exact-byte fingerprint of `Products_json` in the checkout
  that built it. After pulling `main`, rebuild in your own checkout and use the rebuilt file:

  ```
  python tools/data_policy/run_checks.py
  python tools/mandatory_properties/build_eligibility.py --check
  ```

  The second command must report "up to date". Line endings change the bytes (section 3), so a different machine may need a
  rebuild. Never consume a file whose fingerprint does not match your checkout's data.
- **Meaning of eligibility.** `formulation_eligible` means only that all mandatory Tier 1 requirements are met under the current,
  partly provisional rules. It is not a statement of chemical suitability. Ineligible products stay in the database with all
  their data, and Tier 2/3 properties may be used by Part B.
- **Recompute when Part A changes.** If Part A data or rules change later, the fingerprint and possibly the version change, and
  Part B must recompute.

**Inputs and outputs.**
- **Inputs:** `Products_json/`, `source_registry.json`, the archive `Manual + Data to share.zip` (never modified), the templates,
  and the declared decision files in `tools/data_policy/*.json` and `tools/mandatory_properties/*.json`.
- **Outputs:**
  - `reports/data_policy/` (ledger, comparisons, reviews);
  - `reports/mandatory_properties/` (eligibility and companions);
  - `Coverage_Matrix.xlsx`;
  - `docs/data_policy_mandatory_review/test_results/`.

**Build order.** Section 7. `run_checks.py` runs it all and saves each step's return code.

**Publication validation (2026-11-13), on the exact publication candidate.**
- `run_checks.py`: overall PASS. Steps 1-27 returned 0. Step 28, `verify_revision.py`, returned 1, which is the by-design
  legacy failure: it compares with `545fd3d`.
- Every file under `reports/` was byte-identical after regeneration, so the reports match the committed product JSON.
- `verify_preserved.py` passed. The evidence and archive bytes are preserved (section 6).

The candidate was then re-checked in a fresh checkout of the published commit; see the pull-request description.

| | Commit |
|---|---|
| Baseline (shared with Workstream B) | `f4d97e71f72598df601b72403775581c34061ad1` (origin/main) |
| Revision 1 | `8702228` (+ `f9529a2`) |
| Revision 2 | `4e83652` |
| Revision 3 | `43e7f8b` |
| Revision 4 (published) | the commit after `43e7f8b` that adds this section: `git log --oneline 43e7f8b..HEAD` |

Sections 1-9 below are the review record of revisions 3 and 4. Their counts are unchanged by publication. Association mining
(Part B) is not started; `analysis/association_mining/` does not exist on this branch.

## 1. Completed in revisions 3 and 4

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
2. **External-source review** ([evidence_review.md](evidence_review.md) §8; `external_review.csv`). External evidence is admissible; each source is assessed separately (authority, authenticity, exact identity, applicability, provenance).
   - **Cases.** 29 product × property cases: 25 values selected from registered URLs (22 at the time of the review, plus the 3 aramcoULTRA 8 selections of 2026-11-11), and 4 pending fields whose open question is an external source (AFTON_HITEC_8788B).
   - **Confirmed as printed: 21**, all of them selected values now. "Confirmed" is not an approval to select a source; each selection is a separate declared decision. Of the 21: 20 manufacturer-issued, 1 distributor-issued (BAPbase 4 KV40); all 21 name the record's exact grade. For the 8 aramcoULTRA 8 cases the separate merge question ID-01 is open and does not restrict the use of the table (`requirements_review.md` §4).
   - **Inconclusive, source unavailable: 8.** These are the Afton HiTEC 12204L PDS (4 selected values) and the HiTEC 8788B PDS (4 pending fields). The Internet Archive refused automated download, and no saved copy exists. Their values were **not** re-read.
3. **Document identity.**
   - All 174 name-match associations were reviewed: 87 same product, 78 byte-identical copies, 9 other product. The 9 are excluded.
   - The earlier "84 same product" omitted the 3 same-product pairs that later became fill sources; the association universe is now frozen at `4e83652`, as the lead cases are.
   - FORMOSA KV100: each specification names the exact product, so the selections stand. ID-15 was not used, and the FORMOSA SDS fallbacks are pending (identity).
4. **Evidence-supported corrections only** (declared, idempotent, 53 rows in `source_selection_changes.csv`):
   - **3 aramcoULTRA 8 selections (2026-11-11):** KV40 41.10 cSt, KV100 7.1 cSt and flash point 250 °C (COC) from the S-OIL manufacturer table, confirmed on both saved copies; the SDS ranges are kept as alternates; the KV40 disagreement stays an unresolved conflict; the edition date of the page is unknown ([recommendation](recommendation_aramcoULTRA8_source_selection.md));
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
   | evidence unavailable: read, information insufficient (173) | 173 | 81 |
   | evidence unavailable: source could not be obtained (8) | 8 | 0 |
   | evidence inconclusive | 7 | 2 |
   | not individually reviewed | 1,783 | 745 |

   A recorded outcome for every case is **not** a claim that all source verification is complete.
7. **External technical values compared with the SDS** ([evidence_review.md](evidence_review.md) §11). The inventory now includes registered external technical sources: 151 rows, 10 of them external. All 114 values with an external selected source are accounted for (`external_comparison_accounting.csv`): 8 paired; 54 inapplicable; 15 unavailable (no SDS document, or no SDS page prints the property); 37 unresolved (31 because the source could not be obtained, 6 numeric values outside the coverage ledger). Of the 25 ledger `external_selected` values: 4 paired, 2 inapplicable, 15 unavailable, 4 unresolved.
8. **Four approved policies implemented (requirements version `.6`; `requirements_review.md` §4a).** Ranges and bounds are documented evidence and never become points. Co-component completeness is assessed per evidenced route: one usable component does not complete a route, and without reviewed route evidence completeness is not assessed. Percentage basis is mass, volume or unspecified, and no conversion is registered. N/A needs an approved rule (none exists). Evidence documentation, value selection (from the ledger, independent of the category), value form, percentage basis and verification status are separate attributes (`build_readiness.py`). The meaning of `tier1_complete` and `formulation_eligible` is unchanged; no eligibility boolean changed (section 3).
9. **Reliable check runner** (`tools/data_policy/run_checks.py`). Every step runs as its own subprocess, and its real return code and full output are saved (section 5).
10. **Corrections found by the review.**
   - **Classifiers:** Lubrizol handling pages are now technical; inside an SDS file, only a strong technical heading makes a page technical.
   - **Inventory rule:** a flash-point pair needs the cup type on both sides.
   - **Lead rules:** CV2301 pour point is now usable evidence, and NEXBASE 3080 flash point has a case.
   - **Docs:** a revision-2 sentence in `requirements_review.md` ("complete but not formulation-eligible") is corrected.

## 2. Rules and decisions: provisional vs approved

| Rule | Status |
|---|---|
| Rule 1 (technical first, SDS fallback; range/bound selected as printed) | Given by you; applied: 42 declared selections, plus list fills, qualifier fixes and conflict additions. External evidence is admissible; each external source is assessed separately on authority, authenticity, exact identity, applicability and provenance (`external_review.csv`) |
| Pending source selections | 34 fields, each with a reason (`source_review_coverage.md`) |
| Rule 2 thresholds | **PROPOSED**, not applied. KV40/KV100 3 %; density 0.005 g/cm³; specific gravity 0.005 (dimensionless); flash point 10 °C; pour point 3 °C; Noack and TBN none. All empirical; the ASTM claims are unverified. Sensitivity re-checked on the 151-row inventory (10 rows with an external technical side): the conclusions hold. |
| Rule 3 requirements | Items explicit in the spec PDF and glossary. Four policies **approved on 2026-11-11** and implemented: ranges and bounds, co-components, percentage basis, applicability. The other interpretations (I-2 to I-5, I-7) stay provisional. No applicability rule is approved. |

**Policy decisions requiring your approval** (none applied):

| # | Decision | Effect on the current data | Where |
|---|---|---|---|
| A | Keep "published formulation" mandatory for packages as written, or assess it separately from route-data completeness | All 78 packages fail it today; 1 of 78 has complete route data otherwise | [decision_brief_published_formulation.md](decision_brief_published_formulation.md) |
| B / B-REP | **Decided 2026-11-11** (policies 1 and 2). Open remainder: which calculation, if any, may use a range or bound | No range-aware method is registered | `requirements_review.md` §4a |
| C | VM/PPD subtype blocks: stay non-blocking? | Non-blocking now; making them blocking could only lower eligibility (0 components are eligible today) | §4 |
| D | **Principle decided 2026-11-11** (policy 4). Open remainder: whether to approve a rule for CCS / API group on the Risella process oils, with its authority | 3 products stay "unresolved applicability" | §4a |
| E | **Decided 2026-11-11** (policy 3): an unspecified "%" stays unspecified | 84 dose values unspecified; 15 package treat-rate requirements and 4 co-component requirements unmet for that reason | §4a |
| F, G | F decided with D. G open: markers for functions the specification does not name. No template field was added for co-components (reviewed statements are in a side file) | 5 components | §4 |
| Rule 2 | Adopt, change or reject each screening threshold; split mixed findings? | Nothing reclassified until approved | `threshold_proposal.md` §7 |

## 3. Eligibility (version `.6`)

- **Data fingerprint, exact bytes** (authoritative; CRLF checkout): `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`.
- **LF-normalised fingerprint** (informational only): `6440b6800a2946ad8de0c419af5458695702c7e8fb0dced5230d086794a9474d`.

| Class | Products | Tier 1 complete = formulation-eligible | Fully documented (companion, not completeness) |
|---|---:|---:|---:|
| base_oil | 181 | 11 | 11 |
| additive_package | 78 | 0 | 0 |
| additive_component | 5 | 0 | 0 |
| **Total** | **264** | **11** | **11** |

**Eligible:** ADNOC_ADBASE_4CST, 6CST and 8CST; PETRONAS_EQUINAS_8; PETRONAS_ETRO_6_PLUS (open-conflict warnings on KV40 and density); PETRO_CANADA_PURITY_VHVI_2, 3, 4, 6 and 8; S_OIL_ARAMCO_ULTRA_8 (open-conflict warning on KV40).

**Before and after the policy implementation** (`compare_eligibility.py`; saved in `baselines/`):

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

**Earlier changes (calculated by the eligibility build, not assumed).**
- **Revision 2 → revision 3 (`43e7f8b`): 10 eligible.** S_OIL_ARAMCO_ULTRA_8 `tier1_complete` went from true to false, because the interface meaning was restored and its KV40/KV100 source selection was pending.
- **Revision 3 → current working tree (2026-11-11, uncommitted): 11 eligible.** The three aramcoULTRA 8 technical-source selections make its KV40 and KV100 typical point values, so all its mandatory requirements are met. Only this row changed: `tier1_complete` and `formulation_eligible` false → true, `missing_mandatory_properties` now empty, with a KV40 open-conflict warning in `eligibility_reasons`.
- No other product changed. The columns and the requirements version are unchanged; the data fingerprint changed, so Workstream B must recompute.
- The fills completed no product, because each filled product still lacks another mandatory item. For example: ETRO 6 lacks KV40 and density; PRIMA 500 has a KV100 range and pending density; 600R lacks density and CCS.

**Main reasons, by category** (`missing_mandatory_properties.md`):

| Class | Category | Unmet requirements |
|---|---|---|
| Base oils | absent | CCS 130, density 95, API group 73, VI 46 |
| | bound / range needing assessment | VI 27, KV100 17, KV40 14, CCS 12 |
| | unresolved source selection (category) | 14; the ledger lists 17 pending mandatory selections, 3 of them on values that also lack a unit |
| | unresolved applicability | 5 |
| | missing unit | 3 |
| Packages | published formulation absent | 78 |
| | co-component: a documented requirement has no usable dose (35 not route-reviewed; 4 with every reviewed route incomplete) | 39 |
| | no co-component requirement recorded (not the same as supplier silence) | 31 |
| | co-component: recorded doses usable, route list not confirmed | 4 |
| | treat-rate mass basis not stated | 15 |
| Components | function-specific marker applicability unresolved | 5 |

## 4. Remaining evidence gaps

**Unavailable or inconclusive (8 external cases + 181 + 7 reviewed rows):**
- **Afton HiTEC 12204L and 8788B PDSs (Internet Archive):** not obtainable by the tools in this session. A manual download whose bytes match the registry SHA-256 (`7a1e57d8…`, `c09305fb…`) would allow both reviews. 8788B KV40/KV100/density/flash point stay pending until then.
- **Not printed for the grade** in the archive documents (173 cases).
- **Identity not established:** FORMOSA SDSs, ID-15. **Merge question open:** ID-01 (aramcoULTRA 8 and Ultra-S 8 records).

**Not resolvable from the archive** (needs supplier documents or a decision):
- values lacking a required condition (density with no temperature or unit);
- inconsistent labels or units;
- provisional typicals (aramcoPRIMA 110/230);
- conflicting undated technical documents (ETRO 4, NEXBASE, PRIMA density, RF6066, RF6069, CV2301);
- aramcoULTRA 8: the KV40 disagreement between the selected table typical (41.10 cSt) and the SDS range (42.0–55.0 cSt) is unresolved, and the edition date of the S-OIL page is unknown. Only the supplier can settle either. The merge question ID-01 (one product with Ultra-S 8?) is open; both records stay separate;
- BAPbase 4: the only KV40 comes from a distributor-issued flyer (labelled as such); the same flyer's specific gravity is not filled.

**Co-component routes.** 8 packages are reviewed ([co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md)): 29 routes, 21 incomplete, 8 with usable recorded doses but an unconfirmed requirement list, 0 complete. The evidence cannot resolve: the dose of any viscosity modifier; the identity of the boosters of LUBRIZOL_3589C, 3700 and 3700D; whether the D3354 footnote-4 boosters are alternatives; whether any list is exhaustive; which CV1103 table column is the CV6320 route. The other 39 packages with recorded requirements (51 requirements) have no reviewed route. Five record corrections are proposed and not applied.

**External values not compared with an SDS** (`external_comparison_accounting.csv`): 31 values of sources that could not be obtained; 6 numeric values outside the coverage ledger, not assessed; the Richful pages for RF6066 and RF6069 are registry-verified but were not re-read in the external review.

**Not individually reviewed:** 1,783 ledger rows rest on the mechanical page classification only.

## 5. Checks (`python tools/data_policy/run_checks.py`; saved in `test_results/`)

Last run on 2026-11-13 on the revision-4 publication candidate (`43e7f8b` plus the revision-4 changes, exactly as committed); the step numbers and verdicts below are unchanged from the 2026-11-12 run. Full output per step is in `test_results/NN_<step>.txt`; the summary is in `summary.md` / `summary.json`. The results as they were before this run are kept in `baselines/pre_route_review_2026-11-12/test_results/`. **Overall: PASS** (every required step met its expectation).

| # | Step | Return code | Verdict |
|---:|---|---:|---|
| 1–13 | pipeline (document classes → eligibility), incl. `external_comparison_accounting.py` and `verify_soil_table.py` | 0 each | pass |
| 14 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 15, 16 | `build_readiness.py` and `--check` | 0 | pass (up to date) |
| 17 | `compare_eligibility.py` (against `.3`) | 0 | pass: columns identical; 0 booleans, 8 missing lists and 74 categories changed (all co-components) |
| 18 | `compare_eligibility.py` (against the pre-route-review baseline, `.5`) | 0 | pass: 0 booleans, 0 missing lists, 4 categories changed |
| 19 | coverage matrix | 0 | pass (validation issues 30) |
| 20 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 21 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 13 differences in the 2 product files changed since `43e7f8b`, all pre-existing at the baseline, 0 new |
| 22 | `verify_preserved.py` | 0 | pass (section 6) |
| 23 | protected paths vs baseline | 0 | pass (no differences) |
| 24 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 25 | `tools/mandatory_properties/tests` | 0 | 74 OK (43 policy tests) |
| 26 | `tools/data_policy/tests` | 0 | 61 OK |
| 27 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 28 | `verify_revision.py` (v5) | 1 | **expected legacy failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

No unexpected failure. **Snapshot (local only; not published to `main`, see section 0):** `review_snapshots/review_snapshot_2026-11-12/` in the worktree `C:\Users\windo\sf-wsA` (`MANIFEST.sha256`, `REFERENCES.txt`), made with `python tools/data_policy/make_review_snapshot.py --name review_snapshot_2026-11-12` and never overwritten. The snapshot is created after this document is final, so this text cannot contain its manifest hash: see `REFERENCES.txt` inside the snapshot, and `snapshot_verification_2026-11-12.txt` in this folder for the verification output and exit code (written after the snapshot, so it is not part of it).

- **Expected incomplete verification is not an execution failure.** The 8 unavailable external cases and the insufficient archive evidence are outcomes inside steps 6–9, which return 0. The runner deletes the step files of an earlier run before it starts, so no stale result remains.
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
python tools/data_policy/external_comparison_accounting.py   # every external-sourced value: paired, or why not
python tools/data_policy/source_review_status.py             # source_review_status.csv
python tools/data_policy/verify_soil_table.py                # aramcoULTRA 8 values against the saved manufacturer table
python tools/mandatory_properties/treat_rate_basis_scan.py
python tools/mandatory_properties/co_component_evidence_scan.py
python tools/mandatory_properties/build_eligibility.py       # --check compares without writing; exit 3 = stale ledger
python tools/mandatory_properties/build_readiness.py         # attribute files (evidence, selection, form, basis, verification); --check
python tools/mandatory_properties/compare_eligibility.py     # before/after report against the saved baselines
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
- In version `.6`, as in `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied. The meaning is unchanged.
- New additive attribute files report evidence documentation, value selection, value form, percentage basis and verification status. They are not a readiness verdict and not the feature inventory for association mining.
- **The rules are provisional.** Treat the file as a checkpoint, and recompute it on a fingerprint mismatch (the exact-byte fingerprint is authoritative).

## 9. Warnings: historical generators

Do not run any of the following against the current data:
- `tools/corrections_2026-10-31/*` and `tools/integration_2026-10-24/resolve_json.py --write`;
- the `tools/audit/original_2026-10-27_to_30/` generators;
- the `tools/audit/review_2026-11-02/` report generators;
- the one-off editing helpers in `tools/maintenance_2026-11-11/implementation_helpers/` (kept only as a record of how revision 4 was made);
- `integrate_products.py --write` on the whole repository.

`verify_revision.py` fails by design, because it compares with `545fd3d`.
