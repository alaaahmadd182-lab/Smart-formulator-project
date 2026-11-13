# tools/: saved scripts of the audits and reviews

Every script used for the conflicts audit, its later data corrections and its 2026-11-02 review is kept here, so that
no script exists only in a temporary folder.

**Not recovered: the ingestion pipeline.** The code that originally extracted supplier documents into
`Products_json/` was not found and is not in this folder. Nothing here re-creates the product data.

## Where the scripts came from

The folders dated 2026-10-24 to 2026-10-31 hold scripts written in earlier Claude Code sessions. They were recovered on
2026-11-02 from that session's temporary working folder and copied **unchanged**: `PRESERVED_SHA256.txt` lists their
hashes (49 files). To check them:

```
cd tools
sha256sum -c PRESERVED_SHA256.txt
```

Each script's purpose below is taken from its own docstring. These scripts were run from the temporary folder, so they
have two path assumptions:

- the repository path is hard-coded as `REPO = r'C:\Users\windo\OneDrive\Desktop\Smart formulator project'`;
- intermediate data lives in an `audit/` folder beside `tools/`.

They are kept as a record and are not edited. To re-run one, copy it and adjust the paths. The 2026-11-02 review
scripts do this with repository-relative paths.

## `audit/original_2026-10-27_to_30/`: the comprehensive conflicts audit (versions 1 to 4)

| Script | Original purpose |
|---|---|
| `audit_lib.py` | Read-only data model: products, value objects, sources and the archive text index |
| `index_pdfs.py` | Index the text of every PDF page in the source ZIP (writes `pdf_index.json`; re-run on 2026-11-02, the output was byte-identical, so the 3.2 MB index is not kept) |
| `audit_docmap.py` | Map every archive document to the JSON products it names (`docmap.json`) |
| `audit_detect.py` | Independent detectors over the dataset (`candidates.json`) |
| `audit_crossdoc.py` | Cross-document screen: does every other archive document naming a product print the JSON value? (`crossdoc.json`) |
| `audit_documented.py` | Normalise every documented JSON conflict entry and check each value on its cited page (`documented.json`) |
| `audit_compile.py` | Compile documented and new findings into one list (`findings.json`, version 1) |
| `qa_evidence.py` | QA: re-check every finding value against its cited archive page (`qa_evidence.json`) |
| `gen_reports_v1.py`, `gen_reports.py` | Write the report and CSV from `findings.json` (first draft; quality-reviewed version 2 of 2026-10-27) |
| `recheck.py` | Context-level recheck of every archive value (`recheck.json`) |
| `verify_pc.py`, `verify_soil.py` | Column-level verification of the Petro-Canada and S-OIL edition findings (`verify_pc.json`, `verify_soil.json`) |
| `audit_v3.py`, `gen_reports_v3.py` | Version 3 (2026-10-30): source-verified corrections (`findings_v3.json`, `corrections_v3.json`) and its report |
| `audit_v4.py`, `gen_reports_v4.py` | Version 4 (2026-10-30): classification split, follow-up categories (`findings_v4.json`, `corrections_v4.json`) and the report published in PR #4 |
| `gen_manifest.py` | Write `reconciliation/audit_evidence/evidence_manifest.md` (hashes computed from the saved files) |
| `check_final.py` | Consistency checks between the final Markdown and CSV reports |

**`intermediate/`** holds the data files these scripts wrote, as recovered: `findings*.json`, `corrections_v3/v4.json`,
`candidates.json`, `documented.json`, `crossdoc.json`, `docmap.json`, `recheck.json`, `verify_pc/soil.json`,
`qa_evidence.json`, `old28.json`, plus the version-2 report and CSV (`comprehensive_conflicts_audit_v2_2026-10-27.*`).

`findings_v4.json` is the structured source of the version-4 report. On 2026-11-02, re-running the original
`gen_reports_v4.py` on it reproduced the committed version-4 CSV byte for byte, and the Markdown except one line. That
line is the section-9 status count: it is computed from the live product JSON, which changed with the 2026-10-31
corrections.

## `corrections_2026-10-31/`: the source-backed data corrections (commit `28265fd`)

| Script | Original purpose |
|---|---|
| `apply_corrections.py` | Apply the approved corrections (CF-136, CF-142/143 with Zn/S, CF-159, CF-180), asserting the prior state |
| `update_curated_log.py` | Exact, single-occurrence edits to `open_questions_and_conflicts.md` |
| `validate_corrections.py` | Read-only validation of that batch (92 checks; exit 0/1/2). It also asserts that the audit report is unchanged against its base, so it now reports the version-5 revision as a difference, by design |
| `count_ash.py` | CF-144 count: selected Calculated sulfated-ash estimates vs historical alternates |
| `cmp_xlsx.py` | Compare two coverage workbooks sheet by sheet |
| `lubwords.py` | Word positions of the Lubrizol CV1100 and CV3515 data-sheet tables (column check) |

## `integration_2026-10-24/`: merge of PR #2 into the reconciled Task 3 data

| Script | Original purpose |
|---|---|
| `resolve_json.py` | Resolve `Products_json` for the origin/main → integration/reconcile-task3 merge (nothing averaged, no original key changed) |
| `validate.py` | Validate the reconciled `Products_json` against HEAD, origin/main and the templates |
| `log_section.py` | Write the "Integration of origin/main" section of `open_questions_and_conflicts.md` |

## `maintenance_2026-10-31/`: folder organisation and publishing

| Script | Original purpose |
|---|---|
| `org_inspect.py` | Files on disk vs tracked, empty folders, inventory of Desktop ZIPs (read-only) |
| `org_verify.py` | Verification after the folder organisation (read-only) |
| `backup_git_check.py` | Test whether every git object of a Desktop backup ZIP exists in the repository (read-only) |
| `verify_remote_main.py` | Verify a fresh clone of `origin/main` (35 checks) |
| `gh_api.py` | Minimal GitHub REST helper. The token comes from Git Credential Manager at run time; no token is stored in the file |

## `audit/review_2026-11-02/`: the 2026-11-02 review (version 5 of the report)

These were written for this review. They use repository-relative paths and are described in
`docs/audit_review_2026-11-02/README.md`.

| Script | Purpose |
|---|---|
| `review_lib.py` | Shared read-only helpers (archive text from the ZIP, CSV reading, git access) |
| `pdf_pages.py` | Print, search, list word positions of, or render pages of an archive document |
| `show_finding.py` | Print every CSV column of chosen findings |
| `check_sources.py` | Every archive value of every finding looked up on its cited page; known results need a recorded reason (`expected_source_results.json`) |
| `check_columns.py` | Column- and row-level check of the Petro-Canada, S-OIL and Cosan multi-grade tables |
| `check_report.py` | Report-level consistency: IDs, placement, every summary count, JSON paths and anchors, verbatim quotations, the 147 raw conflict entries / 125 distinct conflicts / 125 finding records, classification and follow-up rules |
| `afton_matrices.py` | Extract the Afton claims matrices (vector dots assigned to row and column labels through the cell separators), write them as CSV grids, render the tables and the CF-001/CF-002 cells, and print the cells the findings depend on |
| `citation_context.py` | For every citation accepted only by number presence: the same-row words, the column header above and the neighbouring lines, for the reviewer |
| `build_association_review.py` | Write the reviewer's explicit verdicts (`association_review.json`) for the citations listed in it; there is no default, so an unlisted citation gets no verdict |
| `referenced_sources.py` | The sources findings name in their texts (API 1509, PubChem, ASTM D874, identity review, Internet Archive captures, ...), the patterns that find them, and an explicit verdict for each (verified, unavailable or not used as evidence) |
| `ledger_rules.py` | The classification rules (pure functions): only explicit verdicts or a passed automated check verify a source; incomplete, unavailable, unknown or missing verdicts never do; completeness requires no unresolved source |
| `verification_ledger.py` | Classify every source of every finding → `citation_ledger.csv`, `ledger_summary.json`; exit 0 complete, 3 ran but incomplete, 1 missing input |
| `tests/test_ledger_rules.py` | Regression tests (12): incomplete verdicts cannot count as verified; unknown citations cannot be approved automatically; unresolved sources prevent a "verification complete" result |
| `revise_findings.py` | Apply the declared version-5 changes (each asserts its "before" text) → `output/findings_v5.json`, `docs/.../finding_changes.csv` |
| `gen_report_v5.py` | Write the version-5 report and CSV (derived from `gen_reports_v4.py`) |
| `verify_revision.py` | Every changed CSV cell is a declared change; the D 5950 correction; protected files unchanged; 11 evidence hashes |
| `run_all_checks.py` | Run all of the above in order and save the output to `docs/audit_review_2026-11-02/verification_results/`; reports execution and verification completeness separately (exit 0, 3 or 1) |
| `make_review_zip.py` | Build the review package (report, CSV, correction log, `tools/`, `docs/audit_review_2026-11-02/`), excluding `.git`, the source archive, product data and evidence |

Dependencies: Python 3.12, `pymupdf` (tested 1.28.2) and `openpyxl` (3.1.5). See
`docs/audit_review_2026-11-02/README.md` for the exact commands.

## `data_policy/` and `mandatory_properties/`: Workstream A of 2026-11-10 (current tools)

Written for the source-selection, TDS-SDS comparison and mandatory Tier 1 review. They use repository-relative paths,
never write on import, and write only the files named below. Policy and interface:
`docs/data_policy_mandatory_review/`.

| Script | Purpose | Writes |
|---|---|---|
| `data_policy/policy_lib.py` | Shared read-only helpers (product loading, value objects, archive pages) | nothing |
| `data_policy/document_classes.py` | Classify every cited (file, page) as SDS / TECHNICAL (tds, specification, bulletin, catalog) / COA / EXTERNAL by content; exit 1 if any page is unclassified | `reports/data_policy/document_classes.csv` |
| `data_policy/tds_candidates.py` | Reading aid: technical-document lines for every SDS-sourced selected value | nothing (stdout) |
| `data_policy/source_selection.py` | Rule 1: the declared selections, exceptions and pending cases; dry run unless `--write`; idempotent; asserts the expected current value and source | product JSON (declared fields only) with `--write`; `reports/data_policy/source_selection_changes.csv` with `--report` on a fresh apply |
| `data_policy/integration_diff.py` | What `integrate_products.py` would change in given files (or `--changed`), in memory; with `--against REF` each difference is labelled pre-existing (same difference at REF) or NEW, and the exit code is 1 only for NEW ones | nothing |
| `data_policy/tds_sds_inventory.py` | Rule 2 A-B: every TDS-SDS comparison, comparability first, differences, proposed screen; registered external (URL) technical sources are paired like archive documents, and a pair with a source that could not be obtained is never screened | `reports/data_policy/tds_sds_comparisons.csv` |
| `data_policy/thresholds.py` | Rule 2 C: the proposed property-specific screening rules (`APPROVAL = 'proposed'`; empirical choices) and the sensitivity function | nothing |
| `data_policy/source_coverage_ledger.py` | Rule 1 coverage, per product × property: the technical and SDS documents examined, selection status and reason, comparison status, unsearchable documents | `reports/data_policy/source_coverage_ledger.csv` + `.meta.json` |
| `data_policy/verify_preserved.py` | Checks the 49 preserved files and 11 evidence copies against their manifests, form-aware (worktree / committed blob / blob with CRLF); checks the archive against HEAD and the baseline | only `--out`, if given |
| `mandatory_properties/build_readiness.py` | Separate attributes of every requirement outcome (evidence documentation, value selection, value form, percentage basis, verification status), co-component rows per recorded requirement, the basis of every dose value, applicability labels, and named calculations (registered or not assessed); `--check` | `reports/mandatory_properties/property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `volume_dose_evidence.csv`, `applicability_review.csv`, `calculation_readiness.csv`, `readiness_summary.md` |
| `mandatory_properties/compare_eligibility.py` | Before/after report of the eligibility outputs against saved baselines: counts, each changed product with its reasons, each changed outcome category | `docs/data_policy_mandatory_review/baselines/eligibility_changes__*.csv` |
| `mandatory_properties/co_component_statements.json` | Reviewed supplier statements about co-components (kind, scope, page, quoted wording) | (data) |
| `mandatory_properties/simulate_policy_decisions.py` | The read-only simulation written for the implementation plan of 2026-11-11 (kept for the record) | optional text copy |
| `mandatory_properties/tests/test_policies.py` | Regression tests (43; incl. route evidence bound by fingerprint, one component in two routes, stale evidence reported as historical, and reviewed "none required" statements) for the four approved policies and their gap fixes: two required components in one route, independent routes, unestablished route association, free-text and qualified statements, a pending selection combined with missing metadata, a mass-basis value that is otherwise unusable, the unregistered conversion, the separate attributes, the unchanged interface meaning and the before/after comparison | nothing |
| `mandatory_properties/co_component_route_evidence.json` | Reviewed evidence of co-component routes for 8 packages (29 routes): conditions and quotes as printed, required groups, fingerprints of the bound records, unrecorded requirements, limitations, proposed record corrections | (data) |
| `data_policy/make_review_snapshot.py` | Freezes a dated review snapshot (code, policy inputs, product JSON, reports, documentation, test results) with a SHA-256 manifest; references the source archive by hash; `--verify` | `review_snapshots/<name>/` |
| `maintenance_2026-11-11/implementation_helpers/` | One-off scripts used to apply edits during this work, kept for the record. Hard-coded paths; already applied; do not rerun | nothing |
| `mandatory_properties/treat_rate_basis_scan.py` | Reading aid: the basis wording on the cited page of every bare-"%" treat rate, and document-wide convention leads over every page of the source document | `reports/mandatory_properties/treat_rate_basis_scan.csv` |
| `mandatory_properties/treat_rate_basis_evidence.json` | Reviewed page evidence of a mass basis (3 cases) | (data) |
| `data_policy/lead_review.py` | Review of the outstanding source leads: the case set frozen at revision 2 (plus cases found during the review), extracts per page, reviewed outcomes from `lead_review_decisions.json` (rules with what was read, and the reviewed SDS comparisons) | `reports/data_policy/lead_review.csv` |
| `data_policy/association_review.py` | Identity review of the name-match document associations (universe frozen at revision 2 plus the current ledger; verdicts in `association_review_decisions.json`; byte-identical copies detected; `now_cited` marks associations later used as sources) | `reports/data_policy/name_match_review.csv` |
| `data_policy/external_review.py` | Review of every value from an external (URL) source and of pending fields with an external alternative; each source assessed separately on authority, authenticity, exact identity, applicability and provenance (decisions and evidence hashes in `external_review_decisions.json`); exits 1 on a stale decision or a changed evidence hash | `reports/data_policy/external_review.csv` |
| `data_policy/external_comparison_accounting.py` | One row per value whose selected source is a URL: paired with an SDS value in the inventory, or the reason a comparison is inapplicable, unavailable or unresolved; the evidence state is reported separately; exits 1 on an unaccounted value | `reports/data_policy/external_comparison_accounting.csv` |
| `data_policy/verify_soil_table.py` | Confirms the S_OIL_ARAMCO_ULTRA_8 KV40, KV100 and flash-point values against both saved copies of the S-OIL manufacturer table (caption, column, row label, ASTM cell, printed cell; copy hashes against the manifest); exits 1 on a mismatch | nothing |
| `data_policy/source_review_status.py` | Review state of every ledger row (archive lead review complete, external review complete, evidence unavailable, inconclusive, not individually reviewed) | `reports/data_policy/source_review_status.csv` |
| `data_policy/run_checks.py` | Runs the whole pipeline and every required check as separate subprocesses; saves each real return code and full output; PASS only if every step meets its expectation (`verify_revision.py` is an expected, by-design failure) | `docs/data_policy_mandatory_review/test_results/` |
| `mandatory_properties/co_component_evidence_scan.py` | Supplier statements about required (or not required) co-components in each package's cited pages | `reports/mandatory_properties/co_component_evidence.csv` |
| `mandatory_properties/tests/test_requirements.py` | Regression tests (31): the five reported validation bugs with their valid counterparts, categories, calculations, nested rules | nothing |
| `data_policy/tests/test_data_policy.py` | Regression tests (61): external technical sources in the comparison inventory (inclusion, unavailable evidence, duplicate prevention, point versus range) and the accounting of every external-sourced value; technical-source selection keeps the SDS alternate and never resolves a disagreement (aramcoULTRA 8), Rule 1, comparison rules, the outputs and counts, the evidence review (every case reviewed, wrong associations excluded, comparisons reach the inventory and are usable cases, fills and corrections), the external review (coverage, unobtained sources never confirmed, stale decisions rejected, new conflicts unresolved), review states, the check runner, protected bytes, safety | nothing |
| `mandatory_properties/requirements.py` | Rule 3: versioned mandatory Tier 1 requirements and checks | nothing |
| `mandatory_properties/build_eligibility.py` | Eligibility outputs (needs a current coverage ledger); `--check` compares without writing | `reports/mandatory_properties/*` |

Dependencies: Python 3.12, `pymupdf` (document classification and archive pages) and `openpyxl` (coverage workbook).

**Historical generators.** After 2026-11-10 do not run `corrections_2026-10-31/apply_corrections.py`,
`integration_2026-10-24/resolve_json.py --write`, the `audit/original_2026-10-27_to_30/` generators or the
`audit/review_2026-11-02/` report generators (`revise_findings.py`, `gen_report_v5.py`, `run_all_checks.py`) against the
current data: they would restore superseded values or rewrite the v5 snapshot. `audit/review_2026-11-02/verify_revision.py`
compares protected files with commit `545fd3d` and now fails by design, because product JSON and the workbook changed.

**Line endings.** The manifest records the original bytes, which differ in their line endings:

| Files | Original line ends | How committed |
|---:|---|---|
| 31 | LF | byte-exact |
| 17 | CRLF | normalised to LF |
| 1 | none | byte-exact |

No single `core.autocrlf` setting therefore reproduces all 49 on disk. A bare `sha256sum -c PRESERVED_SHA256.txt` fails for 31 files in a CRLF checkout, and for 17 in an LF checkout.

Use `python tools/data_policy/verify_preserved.py` instead. It checks each file against the worktree bytes, the committed blob, and the blob written with CRLF, and names the form that reproduces the original. On 2026-11-10: 49/49 preserved files and 11/11 evidence copies verified.
