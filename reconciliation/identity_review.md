# Identity review: open items (nothing merged, renamed or deleted)

Each item is cross-referenced in the `identity_flag` column of `inventory_reconciliation.csv`.
Where the inventory records an explicit decision ("NOT merged", "NOT assumed"), that decision stands
until the supplier or the professor confirms otherwise.

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

- **Status:** the legacy rows `BO-ARAMCO-LUBEREF-110HC`, `-230HC` and `-500HC` (sheet rows 6-8, no source
  document) may be the same products as aramcoPRIMA 110, 230 and 500 (JSON present).
- **The inventory's decision:** "Possible identity with legacy 'Luberef 110HC' (LUBEREF110HC) - NOT merged;
  confirm with supplier" (DL2-12172, DL2-11773), and likewise for 230HC and 500HC.
- **Action:** keep them separate. Ask Saudi Aramco / Luberef to confirm.

## ID-03: XOM APE 150 / 600 vs AP/E CORE 150 / 600

- **The inventory's decision:** "Possible identity with legacy 'XOM APE 150/600' naming is NOT assumed;
  AP/E CORE 150/600 kept as separate records" (DL2-13265, DL2-15467).
- **Status:** the legacy rows `BO-EXXONMOBIL-XOM-APE-150` and `-600` (rows 23-24) have no source.
  AP/E CORE 150 and 600 have JSON.
- **Action:** keep them separate.

## ID-04: aramcoPRIMA 150 / 500 matched to legacy names

- **The inventory's note:** "Matched to legacy PRIMA150N ('Aramco Prima 150N' ...) by product name -
  confirm the grade naming with the supplier", and the same for PRIMA500N.
- **Status:** aramcoPRIMA 150 is category B in the ingestion queue. Confirm the naming with Aramco
  before or while creating it.

## ID-05: S-OIL Super S-31 vs aramcoPRIMA 150

- **The JSON's note:** `S_OIL_SUPER_S_31` says "manufacturer mapping to aramcoPRIMA 150 requires
  classification reconciliation".
- **Status:** the inventory lists them as different products. Super S-31 is "Super series:
  low-aromatic, high-naphthenic mineral base oil"; aramcoPRIMA 150 is Group II.
- **Action:** no mapping is verified; keep them separate.

## ID-06: Placeholder ExxonMobil names

- **Status:** `BO-EXXONMOBIL-150N-PER-FILENAME` and `-600N-PER-FILENAME` are named "150N (per filename)"
  and "600N (per filename)", Group II, legacy only.
- **Decision needed:** are these real products, and if so which ExxonMobil grades are they? Do not
  map them to any existing JSON without supplier evidence.

## ID-07: Materials without a stated manufacturer

- **Materials:** `BO-GENERIC-CTL-4`, `BO-GENERIC-GTL-4`, the three generic carrier oils
  (`BO-GENERIC-GROUP-II-110N-...`, `-150N-...`, `BO-GENERIC-VHVI-4-...`) and `AC-GENERIC-FOAMBAN-130B`.
- **Decision needed:** include them in Task 3 as products, or record them as generic formulation inputs
  outside the one-JSON-per-product scope.

## ID-08: HiTEC 5748 vs HiTEC 5748A

- **Where they appear:**
  - HiTEC 12210 (DL2-11418) and 12210M 05/18 (DL2-11796) name "OCP Viscosity Modifier, HiTEC® 5748A".
  - 12210M 04/22 (DL2-15568) names "HiTEC® 5748A or HiTEC® 5748".
  - HiTEC 12360 (DL2-13692) names HiTEC 5748.
- **Status:** the inventory has only `AC-AFTON-HITEC-5748`. 5748A has no inventory row.

## ID-09: Possible variant pairs (kept as separate inventory rows)

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

## ID-14: JSON products with no supplier recorded

- **Status:** `product.supplier` is null in `RICHFUL_RF6071L`, `RICHFUL_RF6406`, `RICHFUL_RF6408`, `SAMA_P2021A`,
  `WUXI_WX3118` and `WUXI_WX3326`. The inventory names the supplier in each case.
- **Action:** a data correction, to be proposed separately; not changed here.
