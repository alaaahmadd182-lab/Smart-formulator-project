# HANDOFF: Workstream A (source selection, TDS–SDS review, mandatory Tier 1)

Date: 2026-11-10. Branch `feat/data-policy-mandatory-review`, in the worktree `C:\Users\windo\sf-wsA`. **Not pushed, merged or
opened as a PR.**

| | Commit |
|---|---|
| Baseline (shared with Workstream B) | `f4d97e71f72598df601b72403775581c34061ad1` (origin/main, "Merge pull request #6") |
| Workstream A content commit | `8702228ff8e465131a2a286c67775259214bb983` |
| Final local commit | the commit that adds the content-commit hash to this file (`git log -1`) |

## 1. Changed files (summary)

The full list is in [implementation_plan.md](implementation_plan.md), section 3, and [CHANGELOG_2026-11-10.md](CHANGELOG_2026-11-10.md).

- **Product JSON, 13 files.** Tier 2 of INFINEUM_D3424 and of nine RICHFUL packages; NESTE_NEXBASE_3020 tiers 1–3.
- **`integrate_products.py`.** Rule text; three re-pinned annotations; three conflict rules reopened.
- **`Coverage_Matrix.xlsx`.** Regenerated.
- **Documentation.** CLAUDE.md, README.md, PROJECT_FILE_GUIDE.md, tools/README.md and requirements.txt are updated, and a dated section is appended to `open_questions_and_conflicts.md`.
- **New.** `tools/data_policy/`, `tools/mandatory_properties/`, `reports/data_policy/`, `reports/mandatory_properties/`, and this folder.

## 2. Rules

**Source selection (Rule 1), applied.** See [source_selection_policy.md](source_selection_policy.md).
- The technical-document value comes first: TDS, PDS, bulletin or specification sheet, classified per page by content. The SDS is the fallback.
- Provenance and alternates are kept, and conflicts stay open.
- Exceptions are recorded. Specification range vs SDS typical goes to pending.
- Edition rule: the newest dated edition of the same product, grade and region. Undated editions that disagree are pending.
- Result: 28 fields switched, 2 exceptions, 7 pending groups.

**TDS–SDS thresholds (Rule 2): PROPOSED, NOT APPROVED.** See [threshold_proposal.md](threshold_proposal.md).
- The inventory has 65 comparisons. Comparability is decided before any difference is computed.
- Proposed screening thresholds:

  | Property | Proposed threshold |
  |---|---|
  | KV40 / KV100 | ≤ 3 % (relative) |
  | Density, specific gravity | ≤ 0.005 g/cm³ (same reference conditions) |
  | Flash point | ≤ 10 °C (same cup type) |
  | Pour point | ≤ 3 °C |
  | Noack, TBN and all others | none: pending |

- Bound rule: a point value inside the other document's bound is ordinary.
- **No finding or conflict has been reclassified, and no v5 successor has been written.**

## 3. Product eligibility counts (mandatory-tier1-2026-11-10)

Source snapshot SHA-256: `5389436fa36b7988a4a7c2e52fc0190b7b4df31ca82b1c6b66460b9b2a7bf10a`. This is the worktree bytes with `core.autocrlf=true`.

| Class | Products | Eligible | Not eligible |
|---|---:|---:|---:|
| base_oil | 181 | 11 | 170 |
| additive_package | 78 | 0 | 78 |
| additive_component | 5 | 0 | 5 |
| **Total** | **264** | **11** | **253** |

The eligible base oils are ADNOC_ADBASE_4CST, _6CST and _8CST; PETRONAS_EQUINAS_8; PETRONAS_ETRO_6_PLUS; PETRO_CANADA_PURITY_VHVI_2, _3, _4, _6 and _8; and S_OIL_ARAMCO_ULTRA_8.
- ETRO 6+ and ULTRA 8 carry warnings: an unresolved conflict exists on kv40 and density, and on kv40, respectively.
- ULTRA 8's Tier 1 values are from its SDS ranges. Its Rule 1 case is pending, and identity question ID-01 is open.

Main blockers:
- **Base oils:** CCS (146 products), density (98), API group (76), VI (69), chemistry (31), kv40 (15), kv100 (12).
- **Packages:** every one lacks a published formulation and a wt.% co-component architecture.
- **Components:** active content, treat rate and compatibility are missing, and the VM subtype data is incomplete.

## 4. Unresolved questions and evidence (for the reviewer)

1. **Approve the thresholds** in threshold_proposal.md, section 5. Density is not tested by the data. Also decide the split-or-note handling and the treatment of label/unit inconsistencies.
2. **Confirm the superseded user decisions** of 2026-10-18: RF6077 density and kv100, RF6088F kv100. Their conflicts are reopened.
3. **Confirm the Rule 3 interpretations** I-1 … I-8 (requirements.py):
   - a one-sided bound does not satisfy a requirement;
   - one CCS point is enough;
   - the secondary function is optional;
   - the marker applicability rule;
   - VM and PPD subtype blocks are mandatory;
   - the wt.% basis is required (a bare "%" does not count; 22 packages and 2 components are affected);
   - the response usability rule;
   - a co-component "none required" statement has no place in the schema.
4. **Shell Risella X 415/420/430.** The `Not Required` labels cite an unapproved applicability rule. Decide whether to approve such a rule (process oils, not engine base oils).
5. **The pending Rule 1 cases** (source_selection_policy.md, section 4), especially RF6069 kv100 (web page 142 vs archived TDS 118) and the NEXBASE family TDS vs individual sheets.
6. **The VI calculation.** No reproducible ASTM D2270 check exists in the repository, so a calculated VI cannot satisfy Tier 1. No current record relies on one.

## 5. Commands to reproduce

Run them from the repository root, with Python 3.12, `pip install -r requirements.txt`.

```
python tools/data_policy/document_classes.py                # reports/data_policy/document_classes.csv (exit 1 if a page is unclassified)
python tools/data_policy/source_selection.py                # dry run; on this branch: "all 28 declared selections are already in the data ... 0 files"
python tools/data_policy/source_selection.py --write        # (only on the baseline) applies the 28 selections, notes, open questions, product blocks
python tools/data_policy/integration_diff.py --changed      # integrate derivation on changed files: 32 pre-existing differences in untouched fields
python integrate_products.py                                # dry run: no errors, 10/10 annotations, 16/16 conflict rules (would change 229 files: do NOT --write)
python tools/data_policy/tds_sds_inventory.py               # reports/data_policy/tds_sds_comparisons.csv (65 comparisons)
python tools/mandatory_properties/build_eligibility.py      # reports/mandatory_properties/* ; --check to compare without writing
python build_coverage_matrix.py --output Coverage_Matrix.xlsx --overwrite
python -m unittest discover -s tools/data_policy/tests -v   # 36 tests
python -m unittest discover -s tools/audit/review_2026-11-02/tests -v
```

`source_selection_changes.csv` is written by `source_selection.py --report` only on a fresh apply, when "before" values
exist. The committed file comes from the apply on this branch.

## 6. Interface for Workstream B

See [eligibility_interface.md](eligibility_interface.md). File: `reports/mandatory_properties/product_eligibility.csv`.

- Columns, in this exact order: `product_id, material_class, product_name, supplier, tier1_complete, formulation_eligible, missing_mandatory_properties, eligibility_reasons, calculated_mandatory_properties, requirements_version, source_snapshot_sha256`.
- Formats:
  - booleans are lowercase `true`/`false`;
  - the three list columns are JSON arrays;
  - `product_id` is the product folder name.
- **Recompute or reject on a snapshot mismatch.** The hash covers exact file bytes, which depend on line-ending conversion at checkout.

## 7. Warnings: historical generators

Do not run any of the following against the current data. They would restore superseded values or findings.

- `tools/corrections_2026-10-31/apply_corrections.py` and `update_curated_log.py`. They hard-code the main-checkout path, and would rewrite product JSON and the curated log there.
- `tools/integration_2026-10-24/resolve_json.py --write`.
- The `tools/audit/original_2026-10-27_to_30/` generators.
- The `tools/audit/review_2026-11-02/` report generators: `revise_findings.py`, `gen_report_v5.py`, `run_all_checks.py`. The v5 report is a historical snapshot.
- `integrate_products.py --write` on the whole repository.

Two checks are expected to fail:
- `tools/audit/review_2026-11-02/verify_revision.py` fails by design, because it compares with `545fd3d`.
- In this worktree, `sha256sum -c tools/PRESERVED_SHA256.txt` reports 31 of the 49 files as FAILED (18 pass). The cause is checkout line-ending conversion (`core.autocrlf=true`), not a change. The committed blobs are unchanged from the baseline, and the main checkout passes 49/49.

## 8. Protected-file checks (2026-11-10)

- **Archive.** `Manual + Data to share.zip`: SHA-256 `6488b08f…5497a` in the worktree, identical to the committed blob. No diff against the baseline.
- **Evidence.** The 11 files in `reconciliation/audit_evidence/` match `evidence_manifest.md`, both in the worktree and as git blobs.
- **Preserved files.** The 49 preserved files have no diff against the baseline. 49/49 hashes pass in the main checkout. In this worktree, each file matches either its committed blob or its checked-out bytes, according to how its line endings are converted.
- **No diff against the baseline** in `json_templates/`, `reconciliation/`, `tools/audit/`, `tools/corrections_2026-10-31/`, `tools/integration_2026-10-24/`, `tools/maintenance_2026-10-31/` or `docs/audit_review_2026-11-02/`.
- **`analysis/association_mining/`.** Not present and not touched.
