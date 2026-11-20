# Dataset preparation package (2026-11-14 onward)

Preparation of the **whole** incoming archive (`Downloaded lubricants sheets.zip`) for systematic JSON conversion, supplier by supplier.
Nothing here creates or changes a production product JSON, applies a proposal or changes a shared policy.

## Baseline (re-verified 2026-11-14 against the archive itself)

| | |
|---|---|
| Archive SHA-256 | `62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1` |
| Files | 4,422 |
| Unique documents (SHA-256) | 4,186 |
| Duplicate groups / redundant copies | 176 / 236 |
| Inventory hash set (`incoming_dataset_review_2026-11-12/tables/unique_documents.csv`) | identical to the archive |

The archive is read in place (ZIP, read-only). No file is extracted into the repository; no ZIP is created.

## Layout

| Path | Content | Authority |
|---|---|---|
| `scripts/01_ocr.py` | OCR of every page without a text layer (150 dpi), `.docx` / `.xls` text | reading aid only (`_cache/ocr/`, not committed) |
| `scripts/02_identify.py` | automated identity extraction per document | provisional (`tables/document_identity_auto.csv`) |
| `scripts/cards.py` | page-1 identity cards per supplier group | reading aid |
| `scripts/decisions/gen_*.py` → `decisions/*.json` | reviewed identity decisions per supplier batch | **authoritative for identity** |
| `scripts/03_register.py` → `tables/*` | registers built from the above | generated |
| `CHECKPOINT_*.md` | dated progress and remaining work | |

Registers (`tables/`):

- **`file_register.csv`**: every file (4,422) mapped to its canonical document. It records whether the file is the canonical copy or a byte duplicate, and whether it is byte-identical to an old-archive file.
- **`document_register.csv`**: one row per unique document (4,186). Each row carries:
  - document type and supplier, each marked *provisional* unless reviewed;
  - linked products;
  - relation (`product` / `non_product` / `unresolved_identity` / `unreadable` / `automated`);
  - identity status, saying exactly what was read;
  - links from the existing-product comparison, and that comparison's reading scope;
  - dates, notes and next action.
- **`document_product_links.csv`**: one row per (document, product), with its role and source (an identity decision, or an existing-product comparison link).
- **`product_register.csv`**:
  - existing records (264), new candidates, confirmed new products and unresolved identities;
  - material class and applicable template;
  - number of linked documents and aliases.
- **`supplier_register.csv`**: documents, reviewed identities and unresolved items per supplier.

The existing-product field comparison (665 proposals, **none approved**) stays in `existing_product_comparison_2026-11-12/`. It is referenced here, not duplicated.

## Status vocabulary

| Term | Meaning |
|---|---|
| automated identity only (not reviewed) | from `02_identify.py`; not a reading |
| identity reviewed (batch): page-1 identity card read | the product name / grade, supplier and document type were read on page 1. Where the name is printed as graphics, the page-1 header image was also viewed. **No property value was read.** |
| `new_candidate` | a product without an existing record, identified by its printed name. It becomes `new_confirmed` once its documents have been reviewed for content and the material class and template are confirmed. |
| `unresolved` | identity or material class not established (e.g. a customer product code without a description) |
| `unreadable` | no text layer and no OCR text yet; the OCR run (`01_ocr.py`) is in progress |

## Readiness for JSON conversion (definition used in the checkpoints)

A product is **ready** when all of the following hold:
- its identity and material class are established;
- the applicable template is identified;
- the relevant available evidence has been reviewed;
- each proposed field has a traceable value or an explicit Missing / unresolved disposition.

Unknown properties do not block creating a record. Unresolved identity, or a material class without a fitting template, blocks final conversion of that product. The dataset is **not** described as ready while documents remain unidentified or unreviewed.

**How the rule is applied (since the integration review of 2026-11-20, `scripts/05_stages.py`).** A product counts as `conversion_ready` only when all of these hold:
- stage 2 is `verified`;
- stage 3 is `established`;
- its evidence was **read**, not programmatically extracted;
- a person has signed it off in `tables/source_verification.csv`;
- the automated audit (`scripts/09_audit_evidence.py`) passes;
- it has no blockers.

The automated audit passes only when:
- every Reported number is found on its cited page;
- no OCR-derived row lacks a visual check;
- no SDS row sits in an element field;
- no value-form, unit or percentage-basis flag remains;
- every Missing row states what was inspected.

A generated mapping, meaning every template field has a row, is only `mapped (generated; not source-verified)`. A parser that found nothing does not make a property Missing.

## Running the checks in another worktree

The archive and the page-text caches are not in git. Point the scripts at them (`scripts/paths.py`), then run:

```bash
export SF_ARCHIVE_ZIP=".../Downloaded lubricants sheets.zip"
export SF_TEXT_CACHE=".../incoming_dataset_review_2026-11-12/_cache/text"
export SF_OCR_CACHE=".../dataset_preparation_2026-11-14/_cache/ocr"
python scripts/03_register.py
python scripts/09_audit_evidence.py
python scripts/05_stages.py
python scripts/04_checks.py --hash-archive
```

`09_audit_evidence.py --update-manifest` is run only after a reviewed change to `field_evidence/`; it rewrites `field_evidence/MANIFEST.json`, which C10 checks.

## Tools (versions recorded in every OCR cache file)

- Python 3.12.4.
- PyMuPDF 1.28.2 (rendering, text layer).
- rapidocr-onnxruntime 1.4.4 with onnxruntime 1.32.0 (OCR).
- xlrd 2.0.2 (`.xls`), openpyxl 3.1.5, numpy 2.4.0, Pillow 12.1.0.

**OCR accuracy check.** Tested on N204 MSDS p.5, which had been verified visually earlier. Values and dates were read correctly, with character confusions such as `kg/I` for `kg/l`. OCR text is used to identify documents and locate evidence. Any value taken as evidence is checked on the page image.
