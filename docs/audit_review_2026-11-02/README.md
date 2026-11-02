# Review of the conflicts audit documentation (2026-11-02)

This folder records a review of the standalone conflicts and contradictions report:
`reconciliation/comprehensive_conflicts_audit.md` and its CSV. The review produced **version 5** of both files. That is
the version to use (reviewed; committed locally on branch `docs/audit-report-review-2026-11-02`, not pushed or merged).

| Version | Date | Where it is |
|---|---|---|
| 1 (first draft), 2 (quality review) | 2026-10-27 | Version 2 report and CSV kept in `tools/audit/original_2026-10-27_to_30/intermediate/` |
| 3, 4 (source verification, reporting corrections) | 2026-10-30 | Version 4 published in PR #4. Git history: `git show e6617ca:reconciliation/comprehensive_conflicts_audit.md` (and `.csv`) |
| **5 (this review)** | **2026-11-02** | `reconciliation/comprehensive_conflicts_audit.md` / `.csv`. Section 4 gives the citation-level verification; section 8.3 summarises the changes; section 8.4 lists the later data corrections |

The findings still describe the database at the 2026-10-30 snapshot (`e6617ca`). The data corrections of 2026-10-31
(commit `28265fd`) are reported as the later state of CF-136, CF-142, CF-143, CF-144, CF-159 and CF-180, in section 8.4
and in the CSV column `later_state_2026_10_31`. They do not change any recorded value.

Not changed by this review:

- product JSON, templates, `Coverage_Matrix.xlsx`;
- the source ZIP, `source_registry.json`, the curated log `open_questions_and_conflicts.md`;
- `reconciliation/audit_evidence/` (including the manifest and its hashes) and the project scripts.

No supplier disagreement was resolved and no supplier was contacted.

## Files

| File | Contents |
|---|---|
| `README.md` | This review and change log |
| `finding_changes.csv` | One row per changed field: finding, field, before, after, reason, evidence (152 rows, 124 findings) |
| `source_reading_log.csv` | Checks made by reading sources (43 entries): document, page, how it was read, what is printed, result |
| `verification_results/` | Saved output of every check (`run_all_checks.py`, files 01–12), plus `source_checks_v5.csv`, `column_checked_citations.json`, `citation_ledger.csv`, `ledger_summary.json` and `afton/` |
| `verification_results/citation_ledger.csv` | One row per source used by a finding (424): value citations, documents cited in explanations and sources named in the finding texts; how each was verified, or why it is unresolved |
| `verification_results/afton/` | The four Afton claims matrices as CSV grids (row × column, "dot" or "icon"), 220 dpi renders of the tables and 300 dpi renders with the CF-001 and CF-002 cells outlined |

## Verification summary

**Verification complete: no.** Every required check runs successfully, but 5 sources could not be obtained and stay
unresolved (listed below). Successful execution and complete verification are reported separately: `run_all_checks.py`
prints both and exits 3 in this state (0 only when the verification is also complete).

### Sources

The inventory covers every source a finding uses:

- each value citation (one document and page cited for one value);
- each document cited only in an explanation (the Afton claims tables of CF-166 and CF-167);
- each source a finding names in its explanation, verification, comparability, nature or follow-up text. These are
  found by `verification_ledger.py` with the patterns in `referenced_sources.py`, for example API 1509, PubChem,
  ASTM D874, identity_review.md and the Internet Archive captures. A named source that has no recorded verdict
  becomes an unresolved row.

A source counts as **fully verified** only through an automated check that passed for that exact source, or an
explicit reviewer verdict "verified" with its basis. Nothing is verified by default. An "incomplete" or "unavailable"
verdict, an unknown verdict or a missing verdict is never counted as verified. These rules are in `ledger_rules.py` and
are held by regression tests (`tests/test_ledger_rules.py`).

| Category | Sources | How |
|---|---|---|
| Sources examined | **424** | In all 180 findings: 351 value citations, 4 documents cited in explanations, 69 sources named in finding texts |
| Fully verified: automated check | 221 | 174 value citations in multi-grade table columns (`check_columns.py`: Petro-Canada 2015.07/2023.03, S-OIL catalog and web table, Cosan sheet); 25 S-OIL findings whose Internet Archive capture equals the live page; 22 quoted `final_resolution` texts equal to the JSON (`check_report.py`) |
| Fully verified: visual check | 23 | Pages without a usable text layer (scanned, vector or encoded-font SDS pages, the aramcoPRIMA brochure, the FPCC image) and the Afton claims matrices (vector dots extracted, then read on renders) |
| Fully verified: context review | 174 | Text read in context (row label, unit, method, column header; `citation_context.py`), one explicit verdict per source: 158 value citations, 16 named sources (API 1509 ×3, PubChem ×2, CPChem 2012 sheet, DL2-15238, DL2-14611, identity_review.md ×3, README ×2, CF-160's integration flag, CF-179's supplier fields and printed names) |
| **Fully verified, total** | **418** | |
| Automated text-presence check only | **0** | |
| **Unresolved** | **5** | ASTM D874, named in CF-142, CF-143 and CF-144 (sold by ASTM; not accessed); Afton HiTEC 5748 data sheets 03/18 and 04/21, named in CF-164 (not retrieved) |
| Not used as evidence | 1 | CAS Common Chemistry, which CF-171 names only to say it was not consulted |

What the unresolved sources mean:

- **CF-144 depends on ASTM D874.** Its validation stays pending.
- **CF-142 and CF-143 only use "ASTM D874-type" to describe the factors in the JSON calculation notes.** Their
  findings, the printed typical values, are verified. The standard itself is still unresolved, and it is counted.
- **CF-164's two missing editions are quoted in the open question but were never seen.** The finding stays
  "partially verified".

### Findings

Of the 180 findings, 176 are verified, 3 partially verified and 1 pending. The 8 pending items are listed in
section 4 of the report: High 1, Medium 5, Low 2. They concern evidence that could not be obtained, not citations that
were left unchecked:

- ASTM D874 (CF-144);
- supplier-only questions (CF-140, CF-146, CF-147, CF-177, CF-178);
- two HiTEC 5748 editions (CF-164);
- the value kind of the ADbase 3 cSt VI 120 (CF-145).

### Conflict entries, distinct conflicts and finding records

These three counts are easily confused:

| Count | Number | Meaning |
|---|---|---|
| Raw JSON conflict entries | 147 | Entries in `conflicts[]` across the tier files of 37 products at `e6617ca`. Some conflicts are copied into each tier file of a product: 11 conflicts appear in 3 tier files each |
| Distinct conflicts | 125 | The 147 entries, with each copied conflict counted once |
| Audit finding records | 125 | One finding per distinct conflict (provenance "Previously documented (JSON conflicts[])"); the other 55 findings come from open questions, field notes, other files or are new |

All 147 entries are cited, each by exactly one finding (`check_report.py` checks these numbers). The report states
this correctly ("The 147 conflict entries already recorded in the JSON (125 distinct conflicts)").

> **Correction.** The first version of this review README, and the review summary given with it, said "147 findings
> taken from JSON conflict entries". That was wrong. The value check compared the **125 finding records** with the
> **147 entries** they cite: every number matched, except the SDS value 0,92 in CF-025, which the audit itself had added.

## Automated checks (scripts in `tools/audit/review_2026-11-02/`)

| Check | Scope | Result |
|---|---|---|
| Report consistency (`check_report.py`) | IDs; table placement; every summary count; `duplicate_of` / `related_ids`; JSON paths and anchors, now and at `e6617ca`; verbatim open-question quotations; every quoted `final_resolution` against the JSON; the 147 / 125 / 125 conflict counts | 2,199 checks, all pass on version 5 |
| Classification and follow-up rules (part of `check_report.py`) | Comparability agrees with the type; no confirmed contradiction called "not a confirmed contradiction"; next step agrees with the follow-up; no open item under "no follow-up"; no "Verified" with "not re-read"; no "dated editions" for undated documents | Version 4 failed 100 rule checks. Version 5 passes, with 2 reviewed waivers (CF-024, CF-159) |
| Numbers on cited pages (`check_sources.py`) | 351 value citations | Input to the ledger. Every result other than "on the cited page" has a recorded explanation |
| Multi-grade tables (`check_columns.py`) | 62 Petro-Canada findings; 23 S-OIL catalog-vs-web findings; CF-141; CF-102's web value | All values in their own grade column and property row. The S-OIL capture of 2026-06-10 equals the live page of 2026-10-30. The Cosan sheet equals the catalog for Ultra-S 4 and 8 |
| Claims matrices (`afton_matrices.py`) | The four Afton HiTEC 12200 / 12210M tables | Every mark assigned to a row and column through the cell separators; the cells of CF-001, CF-002, CF-166 and CF-167 confirmed |
| Ledger (`verification_ledger.py`, rules in `ledger_rules.py`) | All 424 sources | Exit 0 only if every source is fully verified; exit 3 (ran, incomplete) now: 5 unresolved |
| Regression tests (`tests/test_ledger_rules.py`) | 12 tests | Incomplete or unknown verdicts never count as verified; citations without a verdict are never approved (no default in `build_association_review.py`); unresolved sources prevent "verification complete" in the rules, the ledger exit code and the report. All pass |
| Revision integrity (`verify_revision.py`) | Version-4 vs version-5 CSV | 151 changed cells in 120 findings, all declared in `finding_changes.csv`; two new columns; the D 5950 correction |
| Protected files (`verify_revision.py`) | Product JSON, templates, workbook, ZIP, registry, curated log, evidence and scripts, against `545fd3d` | Unchanged; the 11 evidence files match their manifest SHA-256 |
| Regeneration (`run_all_checks.py`) | Version-5 report and CSV regenerated from the declared changes | Identical to the files in `reconciliation/` |

## Errors corrected

Every changed field is in `finding_changes.csv` with its before and after text, reason and evidence.

**Items named in the first review request**

- **CF-031, CF-032 (NYFROST 32):** the SDS values are on p.7 of DL2-13444.pdf (folio 7/12, Section 9), not on the p.6
  cited in the JSON. The source column now reads "p.7 (cited in the JSON as p.6)"; the JSON is unchanged.
- **CF-170 (aramcoPRIMA 500 density): confirmed → potential.** DL2-12172 prints no unit for 0.867 and neither document is
  dated; the record itself says "not a confirmed numerical contradiction". The unit is not assumed.
- **CF-172 (Ultra-S 6 specific gravity): confirmed → potential.** The two tables with the same stated conditions
  (catalog 0.843, Cosan 0.840, both undated) are separated from the SDS value 0.841, whose basis is not stated.
- **CF-145 (ADbase 3 cSt): explainable difference → potential.** Supplier contact is optional in every field.
  - Version 4 explained the Group II label as "a specification minimum vs a typical value".
  - DL2-12221 prints VI 120 as a single value under "PRODUCT SPECIFICATIONS", with no min/max/typical label and no date.
  - DL2-12221 does not identify 120 as a typical, minimum or maximum value, so the explanation rested on an assumption,
    and the relation of 120 to the Group II specification and to the API 1509 Group III threshold cannot be established.
  - Follow-up: a dated ADNOC document identifying the kind of value (standard or further source needed).
  - This was found while verifying the citations. The first version-5 draft had kept the "typical" wording.
  - A later draft said that a specification "limit" of 120 would place every lot at the Group III threshold. That was
    removed: a maximum of 120 would not, and the document does not say which kind of value 120 is.
- **CF-146 (aramcoPRIMA 70): confirmed → potential.**
  - VI 76 is a specification minimum, and no measured VI is printed.
  - The comparison shows only that the specification does not guarantee the API 1509 Group II VI floor (80). It does
    not show that the product's VI is below 80 or that the label is wrong.
- **2026-10-31 correction log (CF-136):** the claim "ASTM D5950 appears only in the 2012 sheet" was wrong. DL2-13200
  prints ASTM D 5950 for the pour-point row covering the C12 Dimer column. The sentence is corrected, with an errata
  section.

**Found in the full review**

- **CF-141: edition difference → potential.** Neither archive sheet is dated; PDF metadata (2009-06-01, 2012-08-27)
  only suggests an order. Follow-up: dated editions needed.
- **CF-164: edition difference → potential.** No edition prints the SSI method, and one value comes from another
  product's bulletin. Evidence pages (p.2) added.
- **CF-033 to CF-036:** page 1 added for DL2-10234.pdf, which the JSON cites without a page.
- **CF-150, CF-152 to CF-156:** version 4 marked them "Verified" with the SDS value "not re-read". The values have now
  been read on their pages.
- **CF-001, CF-002, CF-005 to CF-007, CF-166, CF-167 (claims matrices):** the verification texts now state the
  cell-level checks.
  - The statement in CF-166 that the dots agree in the shared columns had never been checked dot by dot. It now has been, and it holds for all 45 shared cells.
- **CF-024:** the printed text now includes the row's method column (ASTM D5453) beside the note "‡ - D 2622".
- **CF-163:** the comparability names the blending limit as the basis of the confirmed contradiction.
- **Next steps (CSV only):** 96 entries changed; 94 had contradicted their follow-up category. Examples:
  - edition-selection records required supplier contact;
  - CF-015 and CF-020 said "none required" under supplier clarification.
- **Supervisor summary:**
  - the RF6066 classification;
  - the aramcoPRIMA 70 wording;
  - the snapshot state of the Dimer C12 and sulfated-ash items.
- **Section 4 of the report:** the citation-level verification table was added.

## Updated counts and why

| Count | Version 4 | Version 5 | Reason |
|---|---|---|---|
| Confirmed contradiction | 32 | 29 | CF-146, CF-170, CF-172 → potential |
| Potential contradiction | 13 | 19 | + CF-146, CF-170, CF-172 (from confirmed); CF-141, CF-164 (from edition difference); CF-145 (from explainable) |
| Edition difference | 100 | 98 | CF-141, CF-164 → potential |
| Explainable difference | 18 | 17 | CF-145 → potential |
| Data-quality issue | 17 | 17 | unchanged |
| Follow-up: edition-selection policy | 97 | 96 | CF-141 |
| Follow-up: standard or further source needed | 7 | 9 | CF-141, CF-145 |
| Follow-up: no follow-up beyond documentation | 11 | 10 | CF-145 |
| Pending verification items | 8 (Low 2) | 8 (Low 2) | CF-145's item now names the missing value kind (the first v5 draft had removed it) |
| Distinct issues, records, IDs | 179, 180, CF-001…CF-180 | unchanged | no finding added or removed |

## Remaining limitations

- **Unresolved sources (5); the verification is not complete.**
  - ASTM D874 was not accessed: CF-144 depends on it, and CF-142 and CF-143 name it.
  - The HiTEC 5748 editions 03/18 and 04/21 were not retrieved (CF-164).
  - Supplier-only questions stay open. Suppliers were not contacted.
- **Context review is reading, not proof.** It is recorded per citation, so it can be re-checked:
  `citation_context.py` reproduces what was read.
- **Matrix extraction assumptions.** The extraction relies on the claims tables being drawn with vector marks and cell
  separators. The four Afton pages are; any other claims table would need its own check.
- **Data-owner actions, not taken here:**
  - the NYFROST 32 JSON still cites p.6;
  - NS 3 records 0.860 as 0.86;
  - the corrections listed under "Correctable from existing evidence".
- **No search for new findings.** The review checked the 180 findings; it did not look for problems they do not record.
- **`validate_corrections.py`** (2026-10-31) asserts that the audit report is unchanged, so after version 5 it reports
  a difference by design.
- **Missing Desktop backup.** `Smart formulator project (2).zip`, described in the file guide as the only copy of the
  first audit draft, was no longer on the Desktop when this review started. The review did not delete it.
- **Ingestion pipeline.** The code that originally built `Products_json` was not found.

## Reproducing the checks

Requirements: Python 3.12 with `pymupdf` (tested 1.28.2) and `openpyxl` (3.1.5). From the project folder:

```
python -m pip install pymupdf==1.28.2 openpyxl==3.1.5
python tools/audit/review_2026-11-02/run_all_checks.py
```

`run_all_checks.py` runs the chain in order and prints two separate results: whether every required check ran
successfully, and whether the verification is complete. Exit codes: 0 if both hold; 3 if every check ran
successfully but the verification is incomplete (the current state: 5 unresolved sources); 1 if a required check
failed. The steps:

1. revise the findings;
2. check numbers on pages;
3. check the multi-grade tables (writes `column_checked_citations.json`);
4. extract the claims matrices;
5. record the association review (explicit verdicts only);
6. build the ledger (exit 3 = ran, incomplete);
7. generate the report;
8. compare the regenerated report with the files in `reconciliation/`;
9. check the report;
10. check the version-4 report (informational; it fails by design);
11. verify the revision and the protected files;
12. run the regression tests.

Individual commands:

```
python tools/audit/review_2026-11-02/revise_findings.py             # input: tools/audit/original_2026-10-27_to_30/intermediate/findings_v4.json
python tools/audit/review_2026-11-02/check_sources.py --findings tools/audit/review_2026-11-02/output/findings_v5.json --out docs/audit_review_2026-11-02/verification_results/source_checks_v5.csv
python tools/audit/review_2026-11-02/check_columns.py --findings tools/audit/review_2026-11-02/output/findings_v5.json --out docs/audit_review_2026-11-02/verification_results/column_checked_citations.json
python tools/audit/review_2026-11-02/afton_matrices.py              # matrices, renders, cell checks
python tools/audit/review_2026-11-02/citation_context.py > context.txt   # what the reviewer read for each presence-only citation
python tools/audit/review_2026-11-02/build_association_review.py    # records the verdicts
python tools/audit/review_2026-11-02/verification_ledger.py         # exit 0 complete, 3 ran but incomplete, 1 missing input
python tools/audit/review_2026-11-02/gen_report_v5.py               # writes reconciliation/comprehensive_conflicts_audit.md and .csv
python tools/audit/review_2026-11-02/check_report.py
python tools/audit/review_2026-11-02/verify_revision.py             # protected files against 545fd3d and the 11 evidence hashes
python -m unittest discover -s tools/audit/review_2026-11-02/tests -v   # regression tests
(cd tools && sha256sum -c PRESERVED_SHA256.txt)                     # the 49 preserved original files
```

**Inputs:**

- `Manual + Data to share.zip` (read in memory);
- `reconciliation/audit_evidence/`;
- the product JSON at `e6617ca` and in the working tree;
- `tools/audit/original_2026-10-27_to_30/intermediate/`.

**Outputs:**

- `tools/audit/review_2026-11-02/output/findings_v5.json` and `association_review.json`;
- `docs/audit_review_2026-11-02/finding_changes.csv`;
- the two report files;
- `verification_results/`.
