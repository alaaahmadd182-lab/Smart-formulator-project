# Dataset preparation handoff - 2026-11-14 (updated by the integration review of 2026-11-20)

## Integration review 2026-11-20: read this first

Full record: `CHECKPOINT_P05_2026-11-20.md`. Findings: `tables/integration_review_findings_2026-11-20.csv`. Per-batch work: `tables/remediation_tasks.csv`.

**Verified state after the review** (kept apart: reported / automatically checked / source-verified).

| Measure | Value | Basis |
|---|---|---|
| Documents with a reviewed identity | 2,775 of 4,186 (1,411 unlabelled not yet reviewed; 627 `unresolved_identity`) | registers, automatically checked (C01–C06) |
| Products: new candidates / unresolved / out of scope / existing | 1,327 / 9 / 185 / 264 | register |
| Identity verified + template established | 936 | stages |
| Products with generated field mappings | 891 (18,485 rows in 37 files) | reported; discovery automatically checked (C10) |
| Products passing the automated evidence audit | 33 | automatically checked (`09_audit_evidence.py`) |
| Products source-verified | **0** | `tables/source_verification.csv` is empty |
| **Conversion-ready** | **0** | rule in README "Readiness"; the earlier figure of 878 (764 at `07a50e4`) counted generated mappings only |

**Not done in the review:** no full source audit. Four extraction errors were confirmed on the source pages from a sample chosen by the automated audit (F04–F07):
- VANLUBE 0401 Mo;
- RF2214, where the pH value was mapped to P and Zn;
- LUBRIZOL 1038U P, which has no source;
- Eni MX 5003, where min–max ranges were recorded as typical values.

**Production data.**
- The 161 drafts merged into Products_json by PR #8 were removed again.
- So were the shared-policy edits that made the shared tests accept them; all shared paths are back at `ca1d4a7`.
- The drafts stay in `json_output/` and are **unverified**.
- `08_merge_into_products_json.py` is disabled.

**Setup.**
- Set `SF_ARCHIVE_ZIP`, `SF_TEXT_CACHE` and `SF_OCR_CACHE` (see `scripts/paths.py`). The caches are not in git: copy them, or rebuild them with `01_ocr.py` / `01_text_cache.py` from the archive (SHA-256 below).
- In this review they were read from `C:\Users\windo\sf-wsA` (3,802 text-cache files, 501 OCR files). The archive was read from the main checkout.

**Exact next task.**
1. Fix F04–F09 in `scripts/field_mapping/fm_s22_vanderbilt.py`, `fm_s05_richful.py`, `fm_s04_lubrizol.py`, `fm_s18_eni.py` and `fm_s47_adnoc.py`, re-reading the cited pages.
2. Re-run each script, then run `09_audit_evidence.py --update-manifest`, `05_stages.py` and `04_checks.py`.
3. Source-verify the KangTai batch (28 products pass the audit) row by row and record each sign-off in `tables/source_verification.csv`.
4. Only then continue with the other batches in the order of `tables/remediation_tasks.csv`.

Afton (S02) and Infineum (S03) Reported rows have no page citation and must be re-mapped by reading.

**Boundaries (unchanged).**
- No Products_json or template change.
- No proposal application.
- No shared-policy edit: `tools/`, `reports/`, `docs/data_policy_mandatory_review/`.
- No Part B work; no ZIPs.
- Never edit a shared check to make it pass.

## Starting point

Read CLAUDE.md, this folder's README.md and CHECKPOINT_P03_2026-11-14.md.
Part A policy and mandatory-property work was already merged into main in PR #7.
Its handoff is docs/data_policy_mandatory_review/HANDOFF.md.

Dataset preparation checkpoint: 824bf1e (P03).
Subsequent recovery commit: b6ecaf8, preserving unfinished KangTai mapping.
Publishing these records does not approve proposals or establish conversion readiness.

## Recorded state

Incoming archive: 4,422 files, 4,186 unique documents.
P03: 2,497 document identities reviewed; 1,689 remain.
Remaining identity queue: 278 supplier-labelled documents and 1,411 unlabelled.
Identity review is not technical-property review.

Existing production inventory: 264 products.
Non-existing product entries: 1,394, including unresolved and out-of-template entries.
868 have verified identities and established templates, making them candidates for technical review.
P03 conversion-ready count: zero. Do not advance stages just because mappings exist.

Existing-product comparison: 665 proposals, none approved or applied;
508 open non-duplicate links. Preserve its separate review queues.

## First task: validate the interrupted KangTai pilot

Saved files:
- field_evidence/s17_kangtai.csv
- scripts/field_mapping/fm_common.py
- scripts/field_mapping/fm_s17_kangtai.py

Recorded output: 1,031 rows across 39 products; 498 Reported and 533 Missing.
These counts describe generated evidence rows, not validated properties.

Verify field destinations, units, qualifiers, conditions, dosage relationships,
product applicability and page references against the sources.
Recover and explicitly document the three discrepancies mentioned in the
interrupted run; their details are not established by this handoff.
Verify the merged KT33232 dosage cell against DL2-12971 page 1.
Distinguish parser misses and unread sources from genuinely unreported information.

Preserve unmapped properties. Separate aliases from genuine template gaps;
propose extensions separately without editing shared templates.
Check the output paths expected by validation/stage scripts: the pilot is in
field_evidence/, while P03 proposed tables/field_evidence.csv.
Reconcile this deliberately; do not assume the pilot is included in existing checks.

Run appropriate mapping checks and preparation checks, update stages only on
verified evidence, and save a new checkpoint with scoped commits.

## Continue preparation

Proceed supplier by supplier through both identity review and technical mapping.
Keep document counts, candidate products, verified identities, technically
reviewed products and conversion-ready products separate.

Follow up 26 empty OCR pages and the failed JPEG with ID 747b0e9f661a.
Record whether each is blank, unreadable or requires another reading approach.
Cached OCR does not establish successful reading or reliable numeric evidence.

Preserve cross-supplier reconciliation questions and the YALUB ZDD identity conflict.
Do not merge similar names without evidence.

Preserve existing-product queues, including D3503 / DL2-11768, the six pending
visual checks, HiTEC 12210M claim dots and OLOA 55603 slides.
Use the comparison checkpoint and tables for their exact scope.

## Evidence rules and boundaries

Follow the approved source-selection policy and retain conflicting alternatives.
Preserve printed ranges, bounds, units, conditions and percentage basis.
Do not substitute SDS component percentages for elemental contents.
Do not infer exact-product values from family names or related grades.
Record sources, reading scope, exclusions, blockers and decision rationales.

Current continuation scope is preparation only:
no production JSON creation/modification, proposal application, shared-policy
changes or Part B association-mining work.
Continue batches without asking permission between them.
Commit scoped checkpoints; do not push or merge subsequent work without instruction.
Do not generate additional ZIPs.

## Teammate setup and reproducibility

Pull the published main branch, then create a separate continuation branch.
Inspect git status first and preserve any local work.

Obtain Downloaded lubricants sheets.zip separately:
SHA-256 62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1
Also ensure Manual + Data to share.zip is available for old-source comparisons.
Keep source archives unchanged.

Inspect script paths before running: some may refer to the original Windows
checkout or archive location. Configure paths for this checkout and document changes.
Ignored extraction/OCR caches are not supplied by Git; regenerate them using the
recorded scripts or obtain matching caches and verify their provenance.
Do not rerun historical generators against production data.

Local review_snapshots remain outside this publication. Check whether a particular
baseline/snapshot is required before attempting a dependent check.
Local Claude settings, Python caches and the oddly named untracked file are excluded.

Record tool versions, actual commands, exit codes and any setup blockers.
P03 reports 10/10 checks passed at that checkpoint; this does not validate the
subsequently saved KangTai mapping or certify a fresh checkout.
