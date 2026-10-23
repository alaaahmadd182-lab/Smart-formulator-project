# Task 3 inventory reconciliation (2026-10-23)

This folder compares the full raw-material inventory
(`Raw_Material_Missing_Properties_2026-10-13.xlsx`, sheets *Base oils*, *Additive packages* and
*Additive components*) with the product JSON files in `Products_json/` (repository state `f343a29`).
It is documentation only: no product JSON, template, coverage workbook or source-registry file was
changed.

| File | Contents |
|---|---|
| `inventory_reconciliation.csv` | One row per inventory material (453 rows): sheet row, Material ID, name, supplier, register documents, category, matching JSON folder, match evidence and confidence, identity flag, external lead |
| `base_oil_ingestion_queue.md` | The 9 base oils without JSON that have an archived supplier datasheet |
| `identity_review.md` | Uncertain identities, the possible duplicate S-OIL JSONs and supplier-name issues (nothing merged) |
| `richful_feed_leads.csv` | 103 Richful product-feed records for 52 materials without JSON; unverified research leads, not approved sources |

## Counts

| | Base oils | Additive packages | Additive components | Total |
|---|---|---|---|---|
| Inventory materials | 202 | 130 | 121 | **453** |
| JSON product folders | 172 | 77 | 3 | **252** |
| Inventory materials represented by JSON | 171 | 77 | 3 | **251** |
| Inventory materials without JSON | 31 | 53 | 118 | **202** |
| of which: archived supplier datasheet (category B) | 9 | 0 | 0 | **9** |
| of which: mentioned only in other documents (category C) | 0 | 3 | 20 | **23** |
| of which: no archived source located (category D) | 22 | 50 | 98 | **170** |

The 252 JSON folders represent 251 inventory materials because two S-OIL folders, `S_OIL_ULTRA_S_8` and
`S_OIL_ARAMCO_ULTRA_8`, both correspond to `BO-S-OIL-ULTRA-S-8` (see `identity_review.md`, ID-01). Every
JSON folder corresponds to an inventory material; no JSON product is missing from the inventory.

## Categories (column `category`, mutually exclusive)

- **A JSON present** (251): at least one `Products_json` folder represents the material.
- **B no JSON - archived supplier datasheet** (9): a supplier document in `Manual + Data to share.zip`
  prints grade-level values for this material, in its own data sheet or in its own column of a
  multi-grade table.
- **C no JSON - mentioned only in other documents** (23): the material is named only inside another
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

1. **Category B, the 9 base oils** in `base_oil_ingestion_queue.md`:
   - Nynas T 22, then Nynas T 110 (product-specific data sheets);
   - aramcoPRIMA 150 (priority A), then aramcoPRIMA 100, 220, 600 and 500L ("*" typicals);
   - NEXBASE 3030;
   - FPCC 70N GII.
2. **Manual decisions in `identity_review.md`** that affect existing JSON (ID-01 duplicate, ID-12 and
   ID-14 supplier fields), before any further JSON work.
3. **Category C (23)**, only if JSON records that are mostly Missing are approved for products known
   only from other documents (precedent: `AFTON_HITEC_8767B`). Priority A first: HiTEC 12250, HiTEC 5748,
   SV261, HiTEC 12204L.
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
answer decides whether 9, 32 (B + C) or up to 202 more JSON products are needed.
