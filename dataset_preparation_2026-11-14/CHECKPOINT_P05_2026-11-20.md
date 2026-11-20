# Dataset preparation, checkpoint P05 (2026-11-20): integration review of PR #8

## Basis

- **Reviewed source:** `origin/main` at `a636501`.
  - This is the merge of PR #8, branch `feat/dataset-preparation-continue`, whose tip is `f1bec54`.
  - The reported commit `07a50e4` (S22 Vanderbilt) is included.
- **Last published handoff before PR #8:** `ca1d4a7`.
- **Integration branch:** `integration/dataset-prep-audit-2026-11-20`.
- **Commits:**
  - `e795fc8`: restore the shared and production paths;
  - `d89083c`: audit, readiness rule, checks;
  - this checkpoint.

Three kinds of figure are kept apart below:
- **reported**: what the teammate's files state;
- **automatically checked**: the result of a script run;
- **source-verified**: read on the page image or the full page text by a reviewer.

## 1. What PR #8 contained

| Area | Content | Disposition |
|---|---|---|
| Identity batches S28–S60 | 278 supplier-labelled documents → 2,775 of 4,186 documents with a reviewed identity | kept. 6 pseudo-products (`*:UNKNOWN_*`) and 1 catalogue pseudo-product were removed; their documents keep their notes and are `unresolved_identity` / multi-product (finding F10) |
| Field evidence | 37 files, 18,485 rows (5,648 Reported, 12,837 Missing), 891 products | kept as **unfinished, unverified mappings** |
| Readiness | 878 conversion-ready on main (764 at `07a50e4`) | **downgraded to 0** (finding F02) |
| JSON conversion | 161 files for 104 products written to `json_output/` and merged into `Products_json/` (`92c7f50`, `8b2a119`) | **ingestion reverted** on main. Drafts kept unchanged in `json_output/`. `08_merge_into_products_json.py` disabled |
| Shared policy / checks / reports | `source_selection.py` lists the new files so that `test_only_declared_product_files_changed_since_baseline` passes; `document_classes.py`, `lead_review_decisions.json`, `test_data_policy.py`, `compare_eligibility.py`, `build_coverage_matrix.py`, eligibility / readiness reports, Coverage_Matrix workbooks | **restored to `ca1d4a7`** (outside the preparation scope; finding F01) |
| `__pycache__` files (including Part B `analysis/association_mining`) | committed bytecode | removed; `.gitignore` now excludes bytecode |

## 2. Readiness claim reconciled

| Batch commit | Ready after commit | Products in batch |
|---|---|---|
| S38–S60 small suppliers (`a19d0c9` … `0447d2d`) | 36 → 104 | 68 |
| S05 Richful (`d6b7ff1`) | 213 | +109 |
| S02 Afton (`9575c7f`) | 311 | +98 |
| S03 Infineum (`2e119a7`) | **387** (`product_stages.csv`; `stage_summary.json` was not regenerated in this commit) | +76 |
| S06 BASF (`592ad8c`) | **459** | +72 |
| S04 Lubrizol (`d9f3f30`) | **528** | +69 |
| S01 Oronite, S10 BRB, S07 LANXESS, S15 Lubimax, S18 Eni | 586, 637, 676, 709, 739 | |
| S22 Vanderbilt (`07a50e4`) | **764** | +25 |
| S12, S25, S26, S21, S13, S16 | 878 | |

**On "400 → 528" versus 69 Lubrizol products:**
- The count before Lubrizol was **459**, not 400.
- 459 + 69 = 528, so the step matches Lubrizol's 69 products.
- Batch identifiers: S03 = Infineum (`s03_infineum.csv`) and S05 = Richful (`s05_richful.csv`), as in the original batches.
- `tables/field_mapping_status.csv`: 891 unique products, no duplicate rows; each evidence product is in exactly one evidence file.

**Why the 878 were not ready:**
- Stage 5 "complete" only meant that every template field unit had a row.
- 283 of the 878 are **programmatic extractions** (Afton 98, Infineum 76, Richful 109). Their Missing rows may only mean that a pattern did not match.
- 85 products have no Reported row at all.
- **None was source-verified.**

## 3. Automated audit (`scripts/09_audit_evidence.py`, all 37 files, 18,485 rows)

| Reported rows (5,648) | Rows |
|---|---|
| number found on the cited page | 2,579 |
| text row, words found on the cited page | 897 |
| number NOT found on the cited page | 507 |
| no page cited (Afton 446, Infineum 623) | 1,069 |
| text row, words not found | 596 |

| Missing rows (12,837) | Rows |
|---|---|
| with an inspection note | 2,876 |
| without an inspection note | 9,961 |

**Row flags:**
- value form inconsistent: 430;
- numeric row without a unit: 267;
- dose row with an unspecified % basis: 193;
- SDS source in an element field: 5;
- OCR-derived pages cited: 0.

**Products passing every automated check: 33 of 891.** By evidence file:
- KangTai 28;
- Toholchem 3;
- King 1;
- micro-suppliers 1.

This is an automated result, not a source verification.

## 4. Source-verified defects (sample; not a full source audit)

| ID | Product / rows | Evidence says | Source shows | How checked |
|---|---|---|---|---|
| F04 | VANLUBE 0401 Mo | 1.7 % | Mo 2.1 %, Zn 1.7 % | page image DL2-13042 p.1 |
| F05 | RICHFUL RF2214 P, Zn | 5.5, 5.5 | P 7.4 m%, Zn 9.1 m%, **pH 5.5** (SDS p.4) | full cached text |
| F06 | LUBRIZOL 1038U P | 7 % | no P content printed in the SDS | full cached text |
| F07 | Eni MX 5003 Ca / Zn / P / N, flash point | single typical values, page 1 | **min–max columns** on page 2 (e.g. Ca 0.47–0.74) | page image DL2-11115 p.2 |
| F08 | 4 sampled "not found" rows | page 1 | value on page 2 / 5 / 6 of the same document | cached text |
| F09 | ADNOC ADbase grades | page 1 | five-grade column table on page 5; column assignment unchecked | cached text |

**What was not done.** No row-by-row source verification of any batch. The sample above was chosen from automated failures and flags, so it says nothing about the error rate of rows that passed.

## 5. Checks run (all in this worktree, caches from `C:\Users\windo\sf-wsA`, archive from the main checkout)

| Command | Exit | Result |
|---|---|---|
| `python scripts/03_register.py` | 0 | 4,186 documents, 2,775 identity-reviewed, 4,194 links |
| `python scripts/09_audit_evidence.py` | 0 | 37 files / 18,485 rows read; 0 discovery problems |
| `python scripts/05_stages.py` | 0 | conversion_ready 0 |
| `python scripts/04_checks.py --hash-archive` | 0 | **13 / 13** (C01–C12; C11 reports 1,069 invalid rows in unfinished mappings) |
| `python tools/data_policy/run_checks.py --out-dir <scratch>` | 0 | **PASS**: 27 steps pass, `verify_revision_v5` the documented expected failure |

**Notes on the shared run:**
- Output: `logs/shared_run_checks_2026-11-20.out`.
- The tracked reports it regenerated differed from `ca1d4a7` only in line endings (CRLF checkout); they were restored, not committed.
- C08: Products_json and json_templates are identical to the workstream base and clean.

## 6. Remaining work

See `tables/remediation_tasks.csv` (per evidence file) and `tables/integration_review_findings_2026-11-20.csv`.
1. Fix the open findings F04–F09 in the batch scripts. Re-run each script, then `09 --update-manifest`, then checks.
2. Add page citations to the Afton and Infineum Reported rows, or re-map those batches by reading.
3. Re-confirm the 9,961 Missing rows without an inspection note, or mark them "not assessed".
4. Source-verify products batch by batch. Record each sign-off in `tables/source_verification.csv`: who, date, scope, what was compared. Start with the 33 products that pass the audit (KangTai first).
5. The `json_output/` drafts were generated from unverified mappings. Regenerate them only after source verification. Ingestion into Products_json needs a separate project decision.
6. Identity queue: 1,411 unlabelled documents; 627 documents `unresolved_identity`.
7. The existing-product comparison backlog is unchanged:
   - 665 proposals, none approved;
   - 508 open links;
   - D3503 × DL2-11768;
   - six visual checks;
   - HiTEC 12210M claim dots;
   - OLOA 55603 slides.
