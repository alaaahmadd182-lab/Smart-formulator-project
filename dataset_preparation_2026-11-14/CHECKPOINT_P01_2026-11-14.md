# Dataset preparation, checkpoint P01 (2026-11-14)

Workstream: prepare the **whole** incoming archive for JSON conversion, supplier by supplier.
- It starts from `existing_product_comparison_2026-11-12` checkpoint 20 (`ecd4ee3`), which is preserved and referenced, not repeated.
- No production JSON or template changed; no proposal was applied; nothing was pushed or merged; no ZIP was created.

## 1. Baseline (re-verified against the archive)

- Archive SHA-256: `62565d5c…cf2c78b1` (unchanged).
- 4,422 files; 4,186 unique documents; 176 duplicate groups / 236 redundant copies.
- The inventory hash set is identical to the archive.
- `tables/file_register.csv` maps every file to its canonical document; 4,186 files are canonical.

## 2. What exists now

| Component | Status |
|---|---|
| OCR of pages without a text layer (`01_ocr.py`) | **Running in the background** (resumable): 109 of about 502 documents done. Cache in `_cache/ocr/` (not committed). Accuracy was checked on a visually verified page. |
| Automated identity (`02_identify.py`) | All 4,186 documents: high 1,118 / medium 1,487 / low 77 / none 1,504. **Provisional only.** |
| Reviewed identity decisions (supplier batches) | **1,210 of 4,186 documents** (S01–S05) |
| Registers (`03_register.py`) | file, document, document–product link, product and supplier registers, regenerated after each batch |

## 3. Supplier batches done (identity only; no property value was read)

| Batch | Supplier (provisional label) | Documents | Products | Existing matched | New candidates | Out of template scope | Unresolved |
|---|---|---|---|---|---|---|---|
| S01 `1c6252d` | Chevron Oronite | 125 | 67 | 4 | 61 | 0 | 2 customer codes (GA 2536 / GA 2537); 2 certificates with a redacted name |
| S02 `7a9150f` | Afton Chemical | 305 | 131 | 14 | ~104 | 9 fuel additives (OTR, HiTEC 4133G / 4139G / 6431) | UA4158, UA4159, P3010; 2 certificates without a legible name |
| S03 `98e09fc` | Infineum | 241 | 99 | 14 | ~81 | 0 | UA 5113 / 5161 / 5800 / 5803 (customer codes) |
| S04 `38164aa` | Lubrizol | 196 | 127 | 8 | 87 | 32 (SLF finished fluids; ULTRAZOL gasoline additives) | none |
| S05 `fbf1482` | Richful | 343 | 143 | 15 | 124 | 4 (RF12xx gasoline detergents) | 1 SDS without an RF code; 3 products with class unresolved |

**Method.** For each document:
- the page-1 identity card or listing was read;
- longer cards were read where the name was not clear;
- the page-1 image was viewed where the name is printed as graphics (Oronite and Afton bulletins, Infineum customer specifications, Lubrizol Advanced Materials).

The rules applied per supplier, and every exception, are written in `scripts/decisions/gen_s0*.py`. OCR and text-layer artefacts were corrected only where the card shows the true code (e.g. `87888` → 8788B, `lnfineum 03451` → D3451, `RF6077CI` → RF6077).

**Multi-product presentations and company catalogues** are linked without a subject list. Their next action is to list the products presented inside during the package review.

## 4. Product register (`tables/product_register.csv`)

| Status | Count |
|---|---|
| existing (production records) | 264 |
| new_candidate | 461 |
| unresolved (identity or nature) | 9 |
| out_of_scope (no template: finished lubricants, fuel additives) | 47 |

A new candidate is identified by its printed name and supplier. It is **not yet `new_confirmed`**: its documents have not been reviewed for content, and its material class rests on the printed title or code series.

**Schema gaps found:**
- finished lubricants (Lubrizol SLF fluids);
- fuel / gasoline additives;
- metalworking products (kept as component candidates with a scope question);
- process intermediates (OLOA 15500 PIBSA);
- customer-labelled codes whose nature is unstated.

## 5. Known issues (to fix before conversion)

- **Cross-supplier keys.** A product can appear under the batch where it was found, e.g. `AFTON:Jilin J0030` and `LUBRIZOL:JILIN J0010` (PetroChina Jilin), or Oronite products filed under other provisional suppliers. A consolidation step must merge product keys across batches by printed name and supplier, never by values.
- **Generic printed families** (Infineum D339X / D341X / D345X, HiTEC 9300C / 9300G / 9387/88 series) are kept as family keys.

## 6. Remaining work (exact)

1. **Identity review: 2,976 documents**, in this order:
   - BASF 204, LANXESS / Rhein Chemie 125, Sama 118, Croda 102, BRB 90, Clariant 73, INEOS 55, Jinzhou Donggong 50, ExxonMobil 48, Lubimax / Coraplus 47, Kusa 46, KangTai 40, Eni 37, Dow 35, Chevron Phillips 33, Mingyue 30, Vanderbilt 29, Goncord 29, Yasho 27, Wuxi South 26, then the smaller suppliers;
   - **then the 1,411 documents with no recognised supplier**, which include most image-only files: use the OCR text once the run finishes, otherwise page images.
2. **Product consolidation** across batches (§5), then confirmation of the material class and template per product.
3. **Field-level preparation per product** (TDS / PDS, SDS, specifications, certificates, formulations → template fields, with value class, units, methods, conditions, pages). For existing products this reuses the 665 existing-comparison proposals (**none approved**) and the 508 open links listed in `existing_product_comparison_2026-11-12/CHECKPOINT_20`.
4. **Package reviews left open:**
   - D3503 × DL2-11768;
   - the six outstanding visual checks;
   - the HiTEC 12210M claim dots;
   - the OLOA 55603 slide rendering (slide XML already read; no renderer).

**Exact next batch:** S06 BASF (204 documents), using `cards.py "BASF"` and a compact listing.

## 7. Readiness statement

No product is declared ready for conversion yet:
- identity is reviewed for 1,210 documents;
- field-level preparation has not started in this workstream;
- 2,976 documents could still change the product inventory.
