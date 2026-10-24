# Identity review: open items (nothing merged, renamed or deleted)

Each item is cross-referenced in the `identity_flag` column of `inventory_reconciliation.csv`.
Where the inventory records an explicit decision ("NOT merged", "NOT assumed"), that decision stands
until the supplier or the professor confirms otherwise.

Scope basis (2026-10-24): Task 3 covers products supported by supplier datasheets in `Manual + Data to share.zip`.
Items that concern only names in the supplementary Excel workbook are labelled **outside the current datasheet scope**;
open items on archive-supported products are ID-01, ID-05, ID-10, ID-11, ID-12, ID-14 and ID-15.

## ID-01: Possible duplicate S-OIL JSON products (manual review)

| | `Base_oils_json/S_OIL/S_OIL_ULTRA_S_8` | `Base_oils_json/S_OIL/S_OIL_ARAMCO_ULTRA_8` |
|---|---|---|
| JSON product name | Ultra-S 8 (250 Neutral) | aramcoULTRA 8 (250 Neutral) |
| Archive documents cited | DL2-11177.pdf (Ultra-S brochure), DL2-15238.pdf (SDS Ultra-S 8, Rev. 5, 2015-06-10) | DL2-14611.pdf (SDS, Rev. 0, 2018-09-07) |
| Inventory row | Base oils sheet row 203, `BO-S-OIL-ULTRA-S-8` "Ultra-S 8" | same material |

- **The inventory's view:** the Document register assigns both SDSs to `BO-S-OIL-ULTRA-S-8`. The inventory
  review item says DL2-14611 was "issued under the name 'Base Oil aramcoULTRA 8 (250 Neutral)'; identical
  data to the Ultra-S 8 SDS - treated as the same product (rebrand)".
- **Which data each folder holds:** `S_OIL_ARAMCO_ULTRA_8` also holds values from S-OIL's current
  aramcoULTRA web table and an API Group from the Aramco 2024 catalogue. `S_OIL_ULTRA_S_8` holds values
  from the Ultra-S brochure and the 2015 SDS.
- **Decision needed:** keep one folder and record the other name as an alias (and decide which data
  editions it keeps), or keep both as separate products. Neither folder has been changed.

## ID-02: Luberef 110HC / 230HC / 500HC vs aramcoPRIMA 110 / 230 / 500

- **Scope (2026-10-24):** Excel-only legacy names (no supplier datasheet in the archive); outside the current datasheet scope. Kept for reference; no Task 3 action.
- **Status:** the legacy rows `BO-ARAMCO-LUBEREF-110HC`, `-230HC` and `-500HC` (sheet rows 6-8, no source
  document) may be the same products as aramcoPRIMA 110, 230 and 500 (JSON present).
- **The inventory's decision:** "Possible identity with legacy 'Luberef 110HC' (LUBEREF110HC) - NOT merged;
  confirm with supplier" (DL2-12172, DL2-11773), and likewise for 230HC and 500HC.
- **Action:** keep them separate. Ask Saudi Aramco / Luberef to confirm.

## ID-03: XOM APE 150 / 600 vs AP/E CORE 150 / 600

- **Scope (2026-10-24):** Excel-only legacy names (no supplier datasheet in the archive); outside the current datasheet scope. Kept for reference; no Task 3 action.
- **The inventory's decision:** "Possible identity with legacy 'XOM APE 150/600' naming is NOT assumed;
  AP/E CORE 150/600 kept as separate records" (DL2-13265, DL2-15467).
- **Status:** the legacy rows `BO-EXXONMOBIL-XOM-APE-150` and `-600` (rows 23-24) have no source.
  AP/E CORE 150 and 600 have JSON.
- **Action:** keep them separate.

## ID-04: aramcoPRIMA 150 / 500 matched to legacy names

- **Scope (2026-10-24):** the JSON records stand on the archive datasheet DL2-11773.pdf; only the Excel legacy naming is in question, and that naming is outside the current datasheet scope.
- **The inventory's note:** "Matched to legacy PRIMA150N ('Aramco Prima 150N' ...) by product name -
  confirm the grade naming with the supplier", and the same for PRIMA500N.
- **Status:** aramcoPRIMA 150 was ingested on 2026-10-23 from DL2-11773.pdf without merging any legacy name.
  The naming question remains open in its JSON open questions; confirm with Aramco.

## ID-05: S-OIL Super S-31 vs aramcoPRIMA 150

- **The JSON's note:** `S_OIL_SUPER_S_31` says "manufacturer mapping to aramcoPRIMA 150 requires
  classification reconciliation".
- **Status:** the inventory lists them as different products. Super S-31 is "Super series:
  low-aromatic, high-naphthenic mineral base oil"; aramcoPRIMA 150 is Group II.
- **Action:** no mapping is verified; keep them separate.

## ID-06: Placeholder ExxonMobil names

- **Scope (2026-10-24):** Excel-only placeholder names (no supplier datasheet in the archive); outside the current datasheet scope. Kept for reference; no Task 3 action.
- **Status:** `BO-EXXONMOBIL-150N-PER-FILENAME` and `-600N-PER-FILENAME` are named "150N (per filename)"
  and "600N (per filename)", Group II, legacy only.
- **Decision needed:** are these real products, and if so which ExxonMobil grades are they? Do not
  map them to any existing JSON without supplier evidence.

## ID-07: Materials without a stated manufacturer

- **Scope (2026-10-24):** Excel-only generic materials (no supplier datasheet in the archive); outside the current datasheet scope. Kept for reference; no Task 3 action.
- **Materials:** `BO-GENERIC-CTL-4`, `BO-GENERIC-GTL-4`, the three generic carrier oils
  (`BO-GENERIC-GROUP-II-110N-...`, `-150N-...`, `BO-GENERIC-VHVI-4-...`) and `AC-GENERIC-FOAMBAN-130B`.
- **Decision needed:** include them in Task 3 as products, or record them as generic formulation inputs
  outside the one-JSON-per-product scope.

## ID-08: HiTEC 5748 vs HiTEC 5748A

- **Scope (2026-10-24):** `AFTON_HITEC_5748` is one of the 3 records sourced from Afton's own data sheet outside the archive; HiTEC 5748A is only named in archive datasheets and is outside the datasheet scope.
- **Where they appear:**
  - HiTEC 12210 (DL2-11418) and 12210M 05/18 (DL2-11796) name "OCP Viscosity Modifier, HiTEC® 5748A".
  - 12210M 04/22 (DL2-15568) names "HiTEC® 5748A or HiTEC® 5748".
  - HiTEC 12360 (DL2-13692) names HiTEC 5748.
- **Status:** the inventory has only `AC-AFTON-HITEC-5748`. 5748A has no inventory row.
- **Update (2026-10-23):** HiTEC 5748 was ingested from Afton's own HiTEC 5748 PDS (05/23) as
  `AFTON_HITEC_5748`; no 5748A data was used. The Internet Archive index also lists a separate Afton
  `HiTEC-5748A_PDS.pdf` (snapshot 2023-03-23, not retrieved), consistent with 5748A being a distinct grade.
  Nothing merged; whether 5748A needs an inventory row remains open.

## ID-09: Possible variant pairs (kept as separate inventory rows)

- **Scope (2026-10-24):** none of these materials has a supplier datasheet of its own in the archive (SV261 is only named in Infineum D3354 / D3384 datasheets); outside the current datasheet scope.
- `AC-INFINEUM-SV261` / `AC-INFINEUM-SV261L`
- `AC-RICHFUL-RF8248` / `AC-RICHFUL-RF8248B`
- `AC-SINOPEC-JILIN-0010-SOLID-POLYMER` / `AC-SINOPEC-JILIN-THICKENER-0010-OCP-CONCENTRATE` (same grade
  code, different physical form)

## ID-10: HiTEC 12400 vs HiTEC 12360

- **The inventory's note** (DL2-15365): "Typical characteristics (0.951 / 150 / 133 / 61) are identical to
  HiTEC 12360; possible regional variant of the same chemistry - confirm with Afton."
- **Status:** both have JSON and are kept separate.

## ID-11: Formosa SDS grade naming

- **The inventory's note:** DL2-10011 names "150N Base oil" (assigned to Base Oil 150N GII+), and
  DL2-10017 names "500N Base oil" (assigned to Base Oil 500N GII). Both assignments are to be confirmed.
- **Status:** both have JSON.
- **See also ID-15** for the FPCC GII table's 150N and 500N columns.

## ID-12: Supplier differs between JSON and inventory

- **Status:** `CHEVRON_N204` and `CHEVRON_N216` record supplier "Indian Additives Ltd."; the inventory
  says "Chevron Oronite" (`PK-ORONITE-N-204`, `PK-ORONITE-N216`).
- **Decision needed:** which party the JSON should name. The document issuer may be an Oronite affiliate;
  this is not verified.
- **Spelling differences** (same company, no action proposed): ExxonMobil Chemical / ExxonMobil,
  Saudi Aramco / Luberef / Saudi Aramco Luberef, Eni S.p.A. / Eni spa, Ergon Refining / Ergon - West
  Virginia, Inc., Mingyue Keji / MINGYUEKEJI, Jinzhou Kangtai / KangTai.
- **YUBASE 3/4/5/6** record the distributor NARMAK TRADE as the document issuer; the inventory names SK Enmove.

## ID-13: Afton premixes

- **Status:** HiTEC 12204L, 12204Y and 12252 appear only in the HiTEC 12200 leaflet DL2-14639 (and the 05/18
  bulletin DL2-11412), which defines them as premixes. For example, "11.15% HiTEC® 12252 = 10.8% HiTEC® 12200
  + 0.35% HiTEC® 9552".
- **Decision needed:** are they products to record in their own right (category C)?
- **Update (2026-10-23):** HiTEC 12204L has its own Afton PDS (06/17, archived; the HiTEC 12250 source), which
  presents it as an HDEO additive package with its own typical characteristics and treat rate. It was ingested
  as `AFTON_HITEC_12204L`; the premix formula is recorded as an open question, not as its composition or treat
  rate. HiTEC 12204Y and 12252 are unchanged (category C); the decision for them remains open.
- **Scope (2026-10-24):** HiTEC 12204Y and 12252 are named only in DL2-14639 / DL2-11412 and have no datasheet of their own in the
  archive; outside the current datasheet scope. `AFTON_HITEC_12204L` is kept as one of the 3 externally sourced Afton records.

## ID-14: JSON products with no supplier recorded

- **Status:** `product.supplier` is null in `RICHFUL_RF6071L`, `RICHFUL_RF6406`, `RICHFUL_RF6408`, `SAMA_P2021A`,
  `WUXI_WX3118` and `WUXI_WX3326`. The inventory names the supplier in each case.
- **Action:** a data correction, to be proposed separately; not changed here.
- **Update (2026-10-24):** the six records' archive documents were checked; none prints a supplier or company name
  (the Wuxi sheets print only a web address), so `product.supplier` stays null. Whether the inventory's supplier names may be used is open.

## ID-15: FPCC GII 150N / 500N vs Formosa Base Oil 150N GII+ / 500N GII (unresolved)

- **FPCC table:** DL2-12108.jpeg p.1 (image only; re-saved copies DL2-12109.jpeg and DL2-12111.jpeg, same table): "Specification
  of FPCC API GII Base Oil", columns 70N / 150N / 500N under "Specification" and "Typical (2017 AUG)". It prints no product code,
  no company name beyond "FPCC" and no other date. The 70N column is recorded as `FORMOSA_FPCC_70N_GII`.
- **150N:** FPCC 150N specification KV100 5.0~5.6 cSt, VI min 105 (pour max -15, flash min 210, Noack max 15, sulfur max 10).
  `FORMOSA_150N_GII_PLUS` rests on DL2-10001.pdf p.1, "Formosa PetroChemical Corporation", Product Name "Base Oil 150N GII+",
  Product NO. B150N GII+, issued Oct 21, 2009: KV100 5.0-5.4, VI 110 (pour -15, flash 210, Noack 15, sulfur 10), and on the SDS
  DL2-10011.pdf p.1 ("150N Base oil", revised 5 May 2011). The designation (GII+ vs GII) and two limits differ.
- **500N:** FPCC 500N specification KV100 10~12 cSt, VI min 95, pour max -12, flash min 230, sulfur max 10. `FORMOSA_500N_GII`
  rests on DL2-10003.pdf p.1, "Base Oil 500N GII", Product NO. B500N GII, issued Oct 21, 2009, with the same limits, and on the
  SDS DL2-10017.pdf p.1 ("500N Base oil", revised 5 May 2011). The FPCC table also prints Noack "Report", saturates, aromatics
  and water limits and 2017 typicals.
- **Why unresolved:** no archive document expands "FPCC" or links the FPCC grades to the Formosa product names, and both
  Formosa specifications state "We won't notice customers when the specifications revise". Identical limits (500N) do not
  prove identity, and different limits (150N) do not prove separate products.
- **Action:** existing records kept; no record created for the FPCC 150N or 500N columns and nothing merged. Ask Formosa
  or the professor. If 150N is confirmed distinct, it would be recorded as `FORMOSA_FPCC_150N_GII` (three tier files, like
  `FORMOSA_FPCC_70N_GII`); if 500N is confirmed the same product, DL2-12108 would be added to `FORMOSA_500N_GII` as a second source.
