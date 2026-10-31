# Project file guide

A plain-language map of the Smart Formulator project folder: what each file is, why it exists, and whether it is an
input, a record you edit, a generated output or a historical record. Written 2026-10-31; it describes the
repository after the data-correction commit `28265fd`.

The project builds a **raw-material database** for lubricant (engine oil) formulation. Every base oil, additive
package and additive component is a set of JSON files, and every value in them is traced to a page of a supplier
document.

## Folder structure

```
Smart formulator project/
├── CLAUDE.md                                  working rules for AI-assisted editing
├── README.md                                  project overview, scope and how to run the scripts
├── PROJECT_FILE_GUIDE.md                      this guide
├── requirements.txt                           Python dependency (openpyxl)
│
├── Manual + Data to share.zip                 ORIGINAL SOURCE ARCHIVE (supplier datasheets): never edit
├── Raw_Material_Missing_Properties_2026-10-13.xlsx   supplementary inventory workbook (453 materials)
├── Property_Glossary.docx                     Task 1: definitions of every property
├── json_templates/                            Task 2: 8 empty JSON templates
├── Products_json/                             Task 3: THE DATABASE (264 products, 706 JSON files)
│   ├── Base_oils_json/<SUPPLIER>/<PRODUCT_ID>/          3 tier files per product (181 products)
│   ├── Additive_packages_json/<Supplier>/<PRODUCT_ID>/  2 tier files per product (78 products)
│   └── Additive_components_json/<Supplier>/<ID>/        general.json (+ vm.json) (5 products)
├── source_registry.json                       external (non-archive) sources and their verification status
├── build_coverage_matrix.py                   Task 4 script  ─┐
├── Coverage_Matrix.xlsx                       Task 4 output  ─┘ (generated)
├── open_questions_and_conflicts.md            Task 5: curated log of open questions and conflicts
├── integrate_products.py                      normalisation / conflict-annotation script (dry run by default)
├── build_conflicts_report.py                  generates a draft conflicts report (not the curated log)
│
└── reconciliation/                            reviews, audits and their evidence
    ├── README.md                              explains the inventory reconciliation
    ├── comprehensive_conflicts_audit.md       STANDALONE CONFLICTS AND CONTRADICTIONS REPORT (2026-10-30)
    ├── comprehensive_conflicts_audit.csv      the same report, one row per finding (CF-001 … CF-180)
    ├── audit_evidence/                        external evidence copies for the audit + evidence_manifest.md
    ├── comprehensive_conflicts_audit_corrections_2026-10-31.md   LATER CORRECTION LOG
    ├── identity_review.md                     open product-identity questions
    ├── inventory_reconciliation.csv           inventory vs JSON comparison (historical)
    ├── deferred_products.csv / .md            materials without JSON, outside scope (historical)
    ├── base_oil_ingestion_queue.md            closed ingestion queue (historical)
    └── richful_feed_leads.csv                 unverified Richful web-feed leads (historical)
```

A `.git` folder (hidden) holds the version history. Do not delete it.

## What kind of file is it?

| Kind | Meaning | Files |
|---|---|---|
| **Authoritative input** | Original evidence. Read it, never edit it. | `Manual + Data to share.zip`; the copies in `reconciliation/audit_evidence/` |
| **Editable record** | Maintained by hand; changes must follow the rules in `CLAUDE.md`. | `Products_json/`, `open_questions_and_conflicts.md`, `source_registry.json`, `reconciliation/identity_review.md`, `README.md`, `CLAUDE.md`, this guide |
| **Specification** | Fixed design; do not edit while filling data. | `json_templates/`, `Property_Glossary.docx` |
| **Generated output** | Produced by a script; regenerate it instead of editing it. | `Coverage_Matrix.xlsx` (and `conflicts_report_generated.md` if `build_conflicts_report.py` is run; not present now) |
| **Historical record** | A dated snapshot, kept as evidence of what was found or decided. Do not rewrite it; add a new dated record instead. | `reconciliation/comprehensive_conflicts_audit.md` / `.csv`, `audit_evidence/evidence_manifest.md`, the 2026-10-31 correction log, `inventory_reconciliation.csv`, `deferred_products.*`, `base_oil_ingestion_queue.md`, `richful_feed_leads.csv` |
| **Supplementary reference** | Useful background, not evidence for values. | `Raw_Material_Missing_Properties_2026-10-13.xlsx` |
| **Tool** | Scripts and their dependency list. | `build_coverage_matrix.py`, `integrate_products.py`, `build_conflicts_report.py`, `requirements.txt` |

## Top-level files

| File | What it contains | Why it exists |
|---|---|---|
| `CLAUDE.md` | Project rules: JSON structure, the allowed `status` words, "never invent values", the three data rules of 2026-10-24 (no averaging; no automatic TDS-over-SDS preference or the reverse; coverage uses `status`, never `status_final`), naming quirks. | So that every editor, human or AI, follows the same rules. |
| `README.md` | Scope (261 archive-supported products + 3 Afton records = 264), how the coverage matrix is built, what the integration script does, the source-registry rules. | The main entry point for a reader. |
| `PROJECT_FILE_GUIDE.md` | This guide, including the cleanup record. | Folder orientation. |
| `requirements.txt` | `openpyxl>=3.1`. | The only package the scripts need beyond standard Python. |
| `Manual + Data to share.zip` | The original supplier documents, about 91 MB, 362 files. See "Source archive" below. | Every `source.file` in the JSON points into this archive. It is the evidence base and must stay unchanged. |
| `Raw_Material_Missing_Properties_2026-10-13.xlsx` | An inventory of 453 raw materials with missing-property status, as of 2026-10-13. | Supplementary reference used for the inventory comparison in `reconciliation/`. It is not the Task 3 scope and its values are not used as datasheet evidence. |
| `Property_Glossary.docx` | Definition of every property and field (Task 1). | Shared vocabulary for the templates and the JSON. |
| `source_registry.json` | Every external URL cited in `Products_json`: publisher, issuer, format, edition, verification status, date checked, and SHA-256 for PDFs. | The coverage script reports an external source as a warning until it is registered and verified here. |
| `build_coverage_matrix.py` | Script (Task 4). Reads `Products_json` and `source_registry.json` and writes the coverage workbook. Never changes the JSON. Usage: `python build_coverage_matrix.py --output Coverage_Matrix_new.xlsx` (add `--overwrite` to replace a file). | Produces the coverage matrix. |
| `Coverage_Matrix.xlsx` | Generated output. Sheets: Overview, Base Oils, Additive Packages, Additive Components (one cell per product × property: reported / calculated / missing / not_applicable), Validation Issues, Status Detail (every nested status with value, unit and source), Traceability Audit. Last regenerated 2026-10-31 (commit `28265fd`). | Task 4 deliverable. Regenerate it after any JSON change; do not edit it by hand. |
| `open_questions_and_conflicts.md` | The curated Task 5 log: per product, every open question and every documented conflict between documents; then audit summaries, the review of the integration proposals and a human-review list. | The day-to-day record of unresolved questions. It is curated by hand; `build_conflicts_report.py` refuses to overwrite it. |
| `integrate_products.py` | Script. Adds informational normalised keys (`value_final`, `unit_final`, `min_final`, `max_final`, `unit_conversion`, `integration_flags`) beside the original values and applies reviewed conflict annotations. Dry run unless `--write`; refuses to write if any check fails. | Unit normalisation for later formulation stages, under the 2026-10-24 data rules. Under review: test it on a copy before using `--write`. |
| `build_conflicts_report.py` | Script. Writes a draft `conflicts_report_generated.md` from the JSON conflict entries. | A machine-generated companion to the curated log; it never replaces it. |

## The database: `Products_json/`

There is one folder per product, inside one folder per supplier, inside one folder per material class. Each folder
holds one JSON file per **tier**. The code identifies files by the `material_class` and `tier` keys inside each
JSON, not by file name.

| Material class | Folder | Products | Tier files | What each tier holds |
|---|---|---|---|---|
| Base oil | `Base_oils_json/<SUPPLIER>/<ID>/` | 181 (15 suppliers) | 3 | **Tier 1, Blocking:** API group/chemistry, KV40, KV100, viscosity index, density, CCS (all six are required before a formulation can start), plus optional specific gravity. **Tier 2, Verification** of the finished oil (cold flow and volatility): MRV, Noack volatility, pour point, flash point. **Tier 3, Substitution**, used only when swapping one base stock for another: sulfur, saturates, aromatics, cloud point, wax content. |
| Additive package | `Additive_packages_json/<Supplier>/<ID>/` | 78 (16 suppliers) | 2 | **Tier 1, Route-defining:** package type, performance claims, SAE grades, permitted base oils, treat-rate matrix, co-components, published formulations. **Tier 2, Numeric contribution** to the finished oil: TBN, sulfated ash, element contents (Ca, Mg, Zn, P, B, Mo, N, S), KV40, KV100, density, optional specific gravity, flash point, pour point. |
| Additive component | `Additive_components_json/<Supplier>/<ID>/` | 5 (3 suppliers) | 1–2 | `general.json`: function, chemical family, active content, carrier, treat rate, compatibility restrictions, function-specific markers. `vm.json`: extra viscosity-modifier block (HiTEC 5748, RF6602). A `ppd` (pour-point depressant) template exists; no product uses it yet. |

**File naming** (not uniform, for historical reasons):

| Pattern | Used by |
|---|---|
| `<ID>__base_oil_tier1_blocking.json`, `…_tier2_verification.json`, `…_tier3_substitution.json` | Base oils from ADNOC, ARAMCO LUBEREF, BAPCO, CHEVRON, EXXON_MOBIL (87 products) |
| `<ID>_tier1.json`, `_tier2.json`, `_tier3.json` | Base oils from CALTEX, ERGON, FORMOSA, NESTE, NYNAS, PETRONAS, PETRO_CANADA, SHELL, S_OIL, YUBASE (94 products) |
| `tier1_route_defining.json`, `tier2_numeric_contribution.json` | All additive packages |
| `general.json`, `vm.json` | Additive components |

Some folder names contain spaces and punctuation (for example `KangTai . Lubricant Addtives`). Always quote paths.

**Inside every JSON file:**
- **Header keys:** `template_version`, `material_class`, `tier`, `record_id`, `product{}`, `fields{}`,
  `open_questions[]`, `conflicts[]` and `source_documents[]`.
- **Value objects:** every property uses the same object: `value`, `qualifier`, `min`, `max`, `value_kind`,
  `printed_text` (exactly as printed), `unit`, `test_temperature_c`, `method`, `status` and `source{file, page,
  revision_date}`.
- **`status`** is one of Reported, Calculated, Missing, Not Required / N/A, or Not Applicable.
- **Optional keys:** `notes`, `basis`, `alternate_entries`, and the informational `*_final` keys.
- **Conflicts:** when documents disagree, both values stay in `conflicts[]`; nothing is averaged.

## Templates and glossary

| File | Contents |
|---|---|
| `json_templates/base_oil_tier1_blocking.json`, `base_oil_tier2_verification.json`, `base_oil_tier3_substitution.json` | Empty base-oil tiers (template_version 1.0) |
| `json_templates/additive_package_tier1_route_defining.json`, `additive_package_tier2_numeric_contribution.json` | Empty additive-package tiers |
| `json_templates/additive_component_all_general.json`, `additive_component_vm.json`, `additive_component_ppd.json` | Empty additive-component blocks |
| `Property_Glossary.docx` | Definition of each property used in the templates |

Product files are version 1.1: the 1.0 templates plus `source_documents`, `notes`, `basis` and `alternate_entries`.

## Source archive: `Manual + Data to share.zip`

| Inside the ZIP | Contents |
|---|---|
| `Manual + Data to share/Smart_Formulator_Minimum_Property_Set.pdf` | The project brief: the minimum property set the database must cover |
| `…/Raw Lubrincats Datasheets/Base oils/<Supplier>/` | Base-oil TDS, SDS and product sheets (15 supplier folders; PDF, plus a few JPG/JPEG images) |
| `…/Raw Lubrincats Datasheets/Additive packages/<Supplier>/` | Additive-package TDS/SDS (16 supplier folders) and `package_company_mapping.csv` |
| `…/Raw Lubrincats Datasheets/Additive components/Richful Lube Additive/` | Component datasheets |
| `…/Raw Lubrincats Datasheets/README.md` | The archive's own note |

Most files are named `DL2-<number>.pdf`; the JSON cites them by that name and page. Seven file names are stored in
the ZIP with a replacement character where `%` should be (for example `RF6078<U+FFFD>20-<U+FFFD>20TDS.pdf`); the JSON
cites them with `%` restored.

## `reconciliation/`: reviews, audits and evidence

### The conflicts and contradictions audit (complete; historical snapshot)

| File | What it is |
|---|---|
| `comprehensive_conflicts_audit.md` | **The standalone conflicts and contradictions report**, dated 2026-10-30 (PR #4). It contains: a supervisor summary; 180 findings, CF-001 to CF-180 (179 distinct issues), grouped by type (32 confirmed contradictions, 13 potential, 100 edition differences, 18 explainable differences, 17 data-quality issues); the verification status; follow-up categories; and the report's own correction log. It changed no product data. |
| `comprehensive_conflicts_audit.csv` | The same findings, one row per CF-ID: values, units, sources and pages, JSON paths, comparability, verification, follow-up and provenance. |
| `audit_evidence/` | Copies of the external sources the audit used: Petro-Canada PURITY 2023 brochure, S-OIL web table (live and Internet Archive), API 1509 Annex E, Chevron Phillips Dimer C12 sheet, ADNOC specification, two Afton HiTEC 5748 data sheets, PubChem records and a Richful feed record. |
| `audit_evidence/evidence_manifest.md` | For each evidence file: URL, how it was retrieved, edition, pages used, size, SHA-256 and SHA-1, and which findings it supports. |
| `audit_evidence/.gitattributes` | `* -text`, so git stores the evidence files byte for byte (their hashes match the manifest). |

### The later correction log

| File | What it is |
|---|---|
| `comprehensive_conflicts_audit_corrections_2026-10-31.md` | The data corrections made after the audit (commit `28265fd`). CF-136: Dimer C12 pour point −63 → −53 °C. CF-142/143: Lubrizol CV1100/CV3515 sulfated ash, now the printed values 7 and 10, with the omitted Zn and S added. CF-159/180: Richful conflict notes clarified; both conflicts still unresolved. It also records the effect on CF-144 (26 → 24 calculated estimates) and on the coverage workbook. The audit report itself was deliberately left unchanged. |

### Inventory reconciliation (2026-10-23/24, mostly historical)

| File | What it is |
|---|---|
| `README.md` | Explains the comparison of the 453-material inventory workbook with the JSON, its categories (A–D) and the ingestion history. |
| `inventory_reconciliation.csv` | Historical. One row per inventory material: matching JSON folder, evidence, confidence. |
| `identity_review.md` | **Still open.** Identity questions such as ID-01 (Ultra-S 8 vs aramcoULTRA 8) and ID-15 (FPCC GII columns), plus supplier-name issues. Nothing was merged. |
| `deferred_products.csv`, `deferred_products.md` | Historical. The 190 inventory materials without JSON; outside the datasheet scope, not unfinished work. |
| `base_oil_ingestion_queue.md` | Closed. The 9 base oils that were queued; all were ingested on 2026-10-23. |
| `richful_feed_leads.csv` | Historical. Unverified Richful web-feed records for inventory-only materials; none is an approved source. |

## Version history (git)

The work reached `main` in this order:

| Step | Commits | Contents |
|---|---|---|
| PR #2, PR #3 | up to `77ba590` | Data integration and the reconciled Task 3 data |
| PR #4 (branch `audit/comprehensive-conflicts`) | `b1ca3c6`, `e6617ca` | The comprehensive conflicts audit: report, CSV, evidence and manifest |
| Branch `fix/audit-source-corrections` | `28265fd` and the following documentation commit | The 2026-10-31 data corrections, the synchronised coverage workbook and the correction log; this guide and the README updates |

To get the current state, pull `main`. Older branches (`fix/task3-data-quality`, `integration/reconcile-task3`,
and on the project owner's computer only, `backup/reconcile-task3-pre-merge-2026-10-24`) are kept for history.

## Desktop packages outside the project folder

These ZIP files are on the project owner's own Desktop. They are not part of the repository, so pulling the
repository neither adds them nor deletes anything on anyone else's computer.

| File on the owner's Desktop | What it is | Kept? |
|---|---|---|
| `Smart formulator project (2).zip` (196 MB, 2026-10-27) | A full project backup, including `.git`, taken during the audit. Its git history is fully contained in the current repository, but it holds the **only copy of the first draft of the conflicts audit** (2026-10-27 versions of `comprehensive_conflicts_audit.md` and `.csv`, never committed). | **Kept**, as the only record of that draft. Delete it only if the draft is no longer wanted. |
| `SmartFormulator_source_corrections_review_v2_2026-10-31.zip` (1.2 MB) | The review package approved before commit `28265fd`: the changed files, the full diff, the validation script (`tools/validate_corrections.py`) and its output, and a coverage comparison. | **Kept**: it is the reviewed record, and the validation script and its output exist nowhere else. |

## Cleanup record (2026-10-31)

**Moved or renamed: nothing.** The layout already matches what the scripts (default relative paths such as
`Products_json` and `source_registry.json`), `README.md` and `CLAUDE.md` expect. Moving files would break those
references without making the folder clearer.

**Deleted inside the project: nothing.** The folder held exactly the 749 files tracked by git: no caches, temporary
files, backups or empty folders.

**Deleted from the project owner's Desktop** (outside the repository; this affects only that computer):

| File | SHA-256 | Why it was redundant |
|---|---|---|
| `Smart formulator project.zip` (184,487,491 bytes, 2026-10-18) | `57e623e9b884066d5a90eddb516b8d8371e28ea7ecd48c46b1646404db34ffd0` | An older full project backup. All 981 git objects, both refs (`main`, `origin/main` at `90c3d3f`) and its reflog exist in the current repository; it had no stash; all 688 project files match blobs in the current git history byte for byte; nothing was staged that is not committed. |
| `SmartFormulator_conflicts_audit_review_2026-10-30.zip` (2,050,764 bytes) | `8bccc704b4cd2f5110d9526d1fa3402eaf4f1b63efde89c131fad6eae1e3cb95` | Review package of the conflicts audit. All 14 files (report, CSV, 11 evidence files, manifest) are byte-identical to the committed versions (commits `b1ca3c6` and `e6617ca`, PR #4). |
| `SmartFormulator_source_corrections_review_2026-10-31.zip` (28,452 bytes) | `b6288d56b875c0023e4bcb7aaa498204de0ff3fe9f25b24dd3a2b180f67aa42e` | First correction review package, superseded by v2. Its five JSON files are committed byte for byte. Each section of its diff appears unchanged in v2's diff, which can also be reproduced with `git diff e6617ca 28265fd`. Its change log and earlier validation script and output were replaced by v2's summary, v2's validation script and output, and the committed correction log. |

**Left untouched:** `AGG WEBSITE.zip` on the same Desktop, which is not part of this project. Inside the project,
`Manual + Data to share.zip` is the original source archive and is never deleted.
