# Incoming dataset inventory: "Downloaded lubricants sheets.zip" (2026-11-12)

**Inventory only. Nothing was ingested.** No product JSON, source-selection input, eligibility report, evidence file or snapshot was changed (`logs/04_state_verification.log`). The archive was read in place, in memory; it was not modified, copied or extracted.

**How to read the numbers.** Hashes, sizes, page counts and byte duplicates are exact. Document type, supplier, printed product name and product matches are **automated and provisional**: they come from phrases and names on the first two pages, not from a reading of each document. I read about 20 documents myself (the leads in section 6 and a visual sample of 8 unread files). Three counting units are kept apart: files, unique documents (by SHA-256), and products.

## 1. Archive integrity

| | |
|---|---|
| Path | `C:\Users\windo\OneDrive\Desktop\Smart formulator project\Downloaded lubricants sheets.zip` |
| Available locally | yes (file attribute "Archive"; not a OneDrive placeholder) |
| Size | 1,447,945,916 bytes |
| SHA-256 | `62565d5c7a2afc2203536c241004cd4af7f62866a4bfe4f70801b378cf2c78b1` (identical before and after the inventory) |
| Zip integrity test | passed: no bad member, no encrypted member |
| Structure | one top-level folder, `Downloaded lubricants sheets/`, holding 4,422 files with no subfolders and no nested archives |
| Uncompressed size | 1,652,640,680 bytes |

File names are URL-encoded as downloaded (for example `%20` for a space); they are recorded as they are.

## 2. Files and unique documents

| | Count |
|---|---:|
| Files | 4,422 |
| Unique documents (distinct SHA-256) | 4,186 |
| Redundant copies inside the batch | 236, in 176 duplicate groups (largest group: 12 copies) |
| PDF pages | 22,985 |

| File type by content | Files |
|---|---:|
| PDF | 4,339 |
| JPEG (including 2 `.jfif` and 1 file named `.crdownload` that is a complete JPEG) | 55 |
| Excel `.xlsx` | 13 |
| PNG | 8 |
| Old Excel `.xls` (not read: no reader installed) | 5 |
| Word `.docx`, PowerPoint `.pptx` | 1 each |

| Readability (files) | Files |
|---|---:|
| Text layer on every page | 3,875 |
| Text layer on some pages | 116 |
| Image only (PDF pages or picture files) | 425 |
| Not read (`.xls`) or no text extracted | 6 |

No OCR engine is installed, so image-only files were **not read**. That is not the same as empty: a visual sample of 8 unread files showed 5 certificates of analysis (one for Infineum D3451), 2 datasheets and 1 numeric table, all legible to a person.

## 3. Document types (unique documents; automated, provisional)

| Type | Unique documents | Files |
|---|---:|---:|
| SDS | 1,462 | 1,487 |
| TDS / PDS | 1,052 | 1,112 |
| Brochure or presentation | 135 | 158 |
| Other | 729 | 767 |
| Unresolved | 808 | 898 |
| **Total** | **4,186** | **4,422** |

"Other" is 662 certificates of analysis, 64 formulation or performance data documents (candidate data packages, bench-test sheets, engine-test reports) and 3 shipping or commercial papers.

"Unresolved" is 398 documents with no text layer, 101 whose text layer is not legible or is mostly numbers, and 309 with readable text but no recognised type phrase. All are listed in `tables/unreadable_or_unclassified.csv` (1,204 rows, which also includes documents with a type but no recognised product or supplier).

## 4. Duplicates and relation to the existing archive

| Relation | Unique documents | Files |
|---|---:|---:|
| Byte-identical to a file in `Manual + Data to share.zip` | 252 | 287 |
| Not in the existing archive | 3,934 | 4,135 |

- **Same names, same bytes.** 271 new files have the name of an existing archive member, and every one is byte-identical to it. No file has an existing name with different content.
- **Coverage of the old archive.** 252 of its 316 unique files are in the new batch. 79 existing members are not, 48 of them cited by product records (`tables/existing_archive_coverage.csv`). The new batch does not replace the old archive.
- **Same text, different bytes.** 33 groups of documents have an identical text layer but different bytes (31 pairs, 2 triples). One group involves the existing archive: `DL2-12395`, `DL2-12399` and `DL2-12400` have the same text as existing `DL2-12377.pdf`. Images and layout were not compared.
- **Registered sources.** One file, `Yubase_6-SDS.pdf`, has the SHA-256 recorded in `source_registry.json` for the Hilditch Yubase 6 SDS. None matches a locally saved evidence copy.

## 5. Products (a separate count from files and documents)

Current database: 264 products.

| Link between new documents and existing products | Product × document rows | Products | Reliability |
|---|---:|---:|---|
| Byte-identical copy of a source the product already cites | 227 | 202 | exact |
| Byte-identical copy of an archive file not cited by a value of the product | 41 | — | exact; not a new document |
| Product named in the document's product field or title, with its supplier | 66 | 25 | automated, provisional: 59 "additional evidence", 7 "revision candidate" |
| Product only mentioned on the first pages | 109 | — | weak: often a document about another product |

- **Confirmed existing-product matches** are the byte-identical ones: 202 of the 264 products have at least one of their cited sources in the new batch.
- **New documents that appear to be about an existing product:** 66 rows for 25 products. They need reading before use. Examples I checked are in section 6.
- **Revision candidates (7 rows, all provisional, none assumed newer).** I looked at their titles: `DL2-15753.pdf` is a LUBRIZOL CV1103 data sheet "Published on 13 May, 2022", against the cited `DL2-14978.pdf` published 11 Jan 2021; `DL2-15019.pdf` is a HiTEC 12210M SDS; `DL2-11514.pdf` a LUBRIZOL 16008 sheet; `DL2-14994.pdf` a Synfluid PAO 4 sales specification. Two rows are false matches by title (`DL2-11779.pdf` is about OLOA 65770, and the OLOA 55603 document only mentions Yubase 6), and `DL2-13111.pdf` is not checked.
- **New products.** 2,847 unique documents name no existing product. They carry 546 distinct printed product-name strings that match nothing in the database, and many more documents print no product field. The number of genuinely new products **cannot be stated** from this pass: one product can have several documents and one document several products, and the names were not read. Most of these documents are for material classes outside the current database (antioxidants, corrosion inhibitors, PIB, esters, fuel additives, greases, polymers).
- **Unresolved identity:** 953 unique documents (463 not machine-read and not otherwise linked, 490 with text but no product field and no recognised supplier).

## 6. Evidence leads (for later verification; no record was changed)

`tables/evidence_leads.csv` has 413 rows. The ones I read:

| Topic | Document | What it prints |
|---|---|---|
| HiTEC 12204L | `DL2-13579.pdf` | Afton SDS for HiTEC 12204L, date of revision 4/18/2019: relative density 0.972; flash point closed cup 135 °C (Pensky-Martens, minimum); viscosity 190 cSt at 100 °C; density 0.972 g/cm³ |
| HiTEC 12204L | `DL2-14862.pdf` | Afton presentation "HiTEC 12204L HDEO package for API CI-4", May 2019, 21 pages: typicals (TBN 82.2; viscosity at 100 °C 190 cSt; flash point PMC min. 135 °C; density at 15.0 °C 0.972 g/ml) and a formulation: 12204L 14.2 + HiTEC 672 0.1 + HiTEC 5748 4.8 + Aramco Prima 230 70.9 + Prima 500 10.0 = 100.0 %wt |
| HiTEC 12250 | `DL2-14863.pdf` | Afton bulletin 04/19 for the HiTEC 12250 booster: density at 15 °C 0.920 g/ml, flash point PMCC > 135 °C, KV100 175 |
| HiTEC 8788B | `DL2-13364.pdf` | Afton presentation "Product information and Formulations", 18 pages; pp. 16–18 introduce HiTEC 8788B ("designed to be using with conventional OCP VM along with a group I and group III base oil mix"). Four certificates of analysis for 8788B are also present |
| Co-component dose | `DL2-12202.pdf` p.6 | Lubrizol: CV1100 14.2 % + CV6320 2.0 % + Lubrizol 7077 1.5 % + base oils, for API FA-4 10W-30 |
| Co-component dose | `DL2-12169.pdf`, `DL2-12188.pdf` | Lubrizol CV2301 11.70 % + Lubrizol 7077 8.00 % + 7749B 0.20 % b.w. |
| Co-component dose | `DL2-13136.pdf` | Infineum formulations (% wt) with D3451 11.9 and Infineum SV261 7.0 |
| Route review corrections | `DL2-13000.pdf`, `DL2-13139.pdf`, `DL2-13080.pdf` | Infineum D3384 / D3451 cascade and booster pages (D2358, D2359, D2367, C9274) |

- **The Afton sources that could not be obtained are not in the batch**, but equivalent Afton documents for the same products are. They would allow the eight "source unavailable" cases to be reviewed against other evidence.
- **Pending source selections** (130 lead rows): mostly mentions inside other suppliers' formulations (NEXBASE 69 new documents, Formosa 17, ETRO 4 9, aramcoPRIMA 7, RF6066/6069 8, CV2301 8). I found no new stand-alone datasheet for NEXBASE 3043–3080, ETRO 4 or aramcoPRIMA 110/230/500 among the ones I read; the rows need reading.
- **Finished-oil formulations.** 93 documents are flagged as possible formulation or performance data. Several print complete recipes summing to 100 % with test results, which bears on the published-formulation question.
- **The five proposed corrections of the route review:** leads exist for Infineum D3354/D3384/D3451 (17 documents) and CV1103 (`DL2-15753.pdf`). No document in the batch names LUBRIZOL 3589C, 3700 or 3700D (their existing datasheets are among the 79 archive members that the batch does not contain).

## 7. Proposed ingestion order (supplier by supplier)

| # | Supplier | Unique documents | Why this position |
|---:|---|---:|---|
| 1 | Afton Chemical | 305 | Closes the HiTEC 12204L / 12250 / 8788B source gap; 70 documents name existing products; small enough to read fully |
| 2 | Lubrizol | 196 | CV1100 / CV1103 / CV2301 formulations with viscosity-modifier doses; one dated newer-looking CV1103 sheet; 18 formulation documents |
| 3 | Infineum | 241 | D3354 / D3384 / D3451 cascades and booster doses; candidate data packages; many are SDSs |
| 4 | Base-oil suppliers already in the database (Neste, PETRONAS, Aramco/Luberef, Formosa, SK, S-OIL, ExxonMobil, Chevron Phillips, Nynas, Shell) | about 200 | Mostly byte duplicates; check for datasheets that bear on the 17 pending selections |
| 5 | Richful | 343 | Largest named supplier; RF6066 / RF6069 are pending; includes product booklets |
| 6 | Chevron Oronite, Eni, BRB, Jinzhou, KangTai and other suppliers already present | about 350 | Additional evidence; no open item depends on them |
| 7 | Suppliers and material classes not in the database (BASF, LANXESS, Croda, Clariant, INEOS, Sama, Lubimax and others) | about 900 | A scope decision first: these are mostly components and other lubricant types |
| 8 | Certificates of analysis (662) and unread or unidentified documents (953) | about 1,600 | Batch-level data, not product specifications; needs a decision on whether and how they count as evidence, and OCR or reading for the unread ones |

Supplier figures are from `tables/supplier_summary.csv`; 1,411 unique documents have no recognised supplier.

## 8. Limits

- No OCR: 499 unique documents have no usable text layer (463 of them have no other link to a known file). Five `.xls` files were not read.
- Type, supplier and product matches are pattern-based. I saw false matches at the title level (two of seven revision candidates), so every automated match needs a reading before use.
- Printed dates were captured as printed and not interpreted. No document was assumed newer than an existing one.
- Same-text comparison covers the text layer only.

## 9. Files in this directory

| File | Content |
|---|---|
| `scripts/01_extract.py`, `02_reference.py`, `03_classify_compare.py` | The inventory scripts |
| `logs/` | Execution logs of each pass and the state verification |
| `manifest/file_manifest.csv` | One row per file (4,422): path, type, size, CRC, SHA-256, pages, readability, provisional type, supplier, printed product, dates, relationship |
| `tables/unique_documents.csv` | One row per unique document (4,186) |
| `tables/duplicate_groups_within_batch.csv` | 176 duplicate groups |
| `tables/duplicates_of_existing_archive.csv` | 287 files byte-identical to existing archive members |
| `tables/same_text_different_bytes.csv` | 33 groups |
| `tables/existing_archive_coverage.csv` | Which existing members are in the new batch |
| `tables/existing_product_matches.csv`, `revision_candidates.csv` | Product × document links, with their level |
| `tables/evidence_leads.csv` | 413 lead rows |
| `tables/unreadable_or_unclassified.csv` | 1,204 documents needing reading |
| `tables/supplier_summary.csv`, `inventory_statistics.json` | Counts |
| `_cache/` | Extracted text and reference data (27 MB, ignored by Git, reproducible with the scripts) |
