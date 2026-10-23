# Task 3 inventory reconciliation (2026-10-23)

This folder compares the full raw-material inventory
(`Raw_Material_Missing_Properties_2026-10-13.xlsx`, sheets *Base oils*, *Additive packages* and
*Additive components*) with the product JSON files in `Products_json/` (repository state `f343a29`).
It is documentation only: no product JSON, template, coverage workbook or source-registry file was
changed.

| File | Contents |
|---|---|
| `inventory_reconciliation.csv` | One row per inventory material (453 rows): sheet row, Material ID, name, supplier, register documents, category, matching JSON folder, match evidence and confidence, identity flag, external lead, reconciliation history |
| `base_oil_ingestion_queue.md` | The 9 base oils that had no JSON but an archived supplier datasheet, with their ingestion status |
| `identity_review.md` | Uncertain identities, the possible duplicate S-OIL JSONs and supplier-name issues (nothing merged) |
| `richful_feed_leads.csv` | 103 Richful product-feed records for 52 materials without JSON; unverified research leads, not approved sources |

## Counts

Current state, after the ingestion of NYNAS T 22 (pilot), NYNAS T 110, aramcoPRIMA 150, aramcoPRIMA 100, aramcoPRIMA 220, aramcoPRIMA 600, aramcoPRIMA 500L, NEXBASE 3030 and FPCC 70N GII (all nine category-B base oils), and of HiTEC 12250, HiTEC 5748 and HiTEC 12204L (category-C materials with verified manufacturer sources):

| | Base oils | Additive packages | Additive components | Total |
|---|---|---|---|---|
| Inventory materials | 202 | 130 | 121 | **453** |
| JSON product folders | 181 | 78 | 5 | **264** |
| Inventory materials represented by JSON (category A) | 180 | 78 | 5 | **263** |
| Inventory materials without JSON | 22 | 52 | 116 | **190** |
| of which: archived supplier datasheet (category B) | 0 | 0 | 0 | **0** |
| of which: mentioned only in other documents (category C) | 0 | 2 | 18 | **20** |
| of which: no archived source located (category D) | 22 | 50 | 98 | **170** |

At the reconciliation of 2026-10-23 (commit `da4f2b3`), the counts were 252 folders, 251 represented
materials, 202 without JSON and 9 in category B. NYNAS T 22 (`BO-NYNAS-NYNAS-T-22`), NYNAS T 110
(`BO-NYNAS-NYNAS-T-110`), aramcoPRIMA 150 (`BO-ARAMCO-ARAMCOPRIMA-150N`), aramcoPRIMA 100
(`BO-ARAMCO-ARAMCOPRIMA-100`), aramcoPRIMA 220 (`BO-ARAMCO-ARAMCOPRIMA-220`), aramcoPRIMA 600 (`BO-ARAMCO-ARAMCOPRIMA-600`), aramcoPRIMA 500L (`BO-ARAMCO-ARAMCOPRIMA-500L`), NEXBASE 3030 (`BO-NESTE-NEXBASE-3030`) and FPCC 70N GII (`BO-FORMOSA-FPCC-70N-GII`) have since moved from category B to A, and HiTEC 12250 (`AC-AFTON-HITEC-12250`), HiTEC 5748 (`AC-AFTON-HITEC-5748`) and HiTEC 12204L (`PK-AFTON-HITEC-12204L`) from category C to A; their CSV rows record this in `reconciliation_history`.

`Coverage_Matrix.xlsx` and the scope table in the main `README.md` describe the state synchronized at commit
`53fb90e` (261 folders, 260 materials, 193 without JSON) and do not yet include HiTEC 12250, HiTEC 5748 or HiTEC 12204L, until the coverage
workbook is regenerated.

The 264 JSON folders represent 263 inventory materials because two S-OIL folders, `S_OIL_ULTRA_S_8` and
`S_OIL_ARAMCO_ULTRA_8`, both correspond to `BO-S-OIL-ULTRA-S-8` (see `identity_review.md`, ID-01). Every
JSON folder corresponds to an inventory material; no JSON product is missing from the inventory.

## Categories (column `category`, mutually exclusive)

- **A JSON present** (263; 251 at the reconciliation): at least one `Products_json` folder represents the material.
- **B no JSON - archived supplier datasheet** (0; 9 at the reconciliation; all nine ingested): a supplier document in `Manual + Data to share.zip`
  prints grade-level values for this material, in its own data sheet or in its own column of a
  multi-grade table.
- **C no JSON - mentioned only in other documents** (20; 23 at the reconciliation): the material is named only inside another
  product's data sheet, for example as a booster, premix, viscosity modifier or co-component dose;
  there is no data sheet of its own. Lubrizol 7077 and RF0206 are named in package data sheets
  but are not linked to them in the inventory's Document register.
- **D no JSON - no archived source located** (170): the inventory marks the material "legacy only",
  and no archive document mentions it.

## How the matching was done

1. **Document evidence:** each JSON folder's cited archive files were mapped through the inventory's
   *Document register* (including its "Identical copies" column) to Material IDs.
2. **Name evidence:** a candidate was accepted only within the same material class and only when:
   - the normalized names were equal (170 matches);
   - one name contained the other with the same grade code, such as a supplier prefix or a descriptive suffix (67);
   - the folder name equalled the Material ID (8);
   - or the supplier document printed only the grade code (6 Chevron grades: the inventory says
     "Neutral Oil 100R", the JSON "Chevron Base Oil 100R", and DL2-10004 prints only "100R").
3. **Filename similarity alone was never accepted.**
4. **Coverage:** all 359 archive datasheets are in the Document register. The three remaining archive
   files are README.md, `Smart_Formulator_Minimum_Property_Set.pdf` and `package_company_mapping.csv`.
5. **Text search:** for every material without JSON, I also searched the text of the 316 archive PDFs
   that have a text layer. The 31 image-only PDFs and 13 image files could only be checked through the
   register.

The intermediate scripts were run outside the repository; the CSV is the record of the result.

**Correction to the earlier chat report:** the 7 family-sheet grades in category B have sibling grades
with JSON, but those siblings were built from other documents, not from the same family sheets (see
`base_oil_ingestion_queue.md`).

## Proposed ingestion order (awaiting approval)

1. **Category B, the 9 queued base oils** in `base_oil_ingestion_queue.md` (all ingested 2026-10-23):
   - Nynas T 22 (ingested 2026-10-23 as a pilot) and Nynas T 110 (ingested 2026-10-23), both from product-specific data sheets;
   - aramcoPRIMA 150 (priority A), aramcoPRIMA 100, 220, 600 and 500L (all ingested 2026-10-23; the 500L values are provisional "*" typicals);
   - NEXBASE 3030 (ingested 2026-10-23);
   - FPCC 70N GII (ingested 2026-10-23).
2. **Manual decisions in `identity_review.md`** that affect existing JSON (ID-01 duplicate, ID-12 and
   ID-14 supplier fields), before any further JSON work.
3. **Category C (20 remaining)**, only where a verified manufacturer source gives the product its own data, or if JSON
   records that are mostly Missing are approved for products known only from other documents (precedent:
   `AFTON_HITEC_8767B`). HiTEC 12250 was ingested 2026-10-23 from the archived Afton HiTEC 12204L PDS (06/17), and HiTEC 5748
   from Afton's own archived HiTEC 5748 PDS (05/23). HiTEC 12204L was ingested 2026-10-23 from the same Afton HiTEC 12204L
   PDS (its own column); the DL2-14639 premix formula is kept as an open question. Remaining priority A: SV261, Lubrizol
   7077, RF0206.
4. **Category D (170)**, only after manufacturer sources are found and verified. The Richful leads in
   `richful_feed_leads.csv` are candidates for that research; none is an approved source.

## Richful product-feed leads

`richful_feed_leads.csv` lists records from Richful's product data feed
(`https://www.richful.com/rfapi/api/product/getproductbyid?productId=N`, shown on
`catalogueDetail.html?id=N`), retrieved 2026-10-23, whose product code equals an inventory material
without JSON. All of them have feed status 0, and none appears in Richful's public catalogue listing.
They are research leads only.

Before any of them is used as a source, four things must be verified and recorded in
`source_registry.json`:

- **Authenticity:** the record is published by Richful.
- **Product identity:** the record is the inventory product.
- **Document content:** the values it holds.
- **Accessibility:** a reader can retrieve it.

Until then, the columns `authenticity`, `product_identity`, `document_content` and `accessibility`
read "not verified" or "not reviewed", and `approved_as_source` is "no".

Still open: whether Task 3 requires a JSON for every inventory material even without any source. The
answer decides whether 0, 20 (category C) or up to 190 more JSON products are needed.
