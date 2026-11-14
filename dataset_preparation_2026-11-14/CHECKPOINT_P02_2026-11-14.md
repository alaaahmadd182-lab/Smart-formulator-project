# Dataset preparation, checkpoint P02 (2026-11-14)

This checkpoint continues from P01 (`18181ed`).
- No production JSON or template changed; no proposal was applied.
- Nothing was pushed or merged; no ZIP was created.
- Batches S06 to S12 are identity-only: no property value was read or transcribed.

## 1. Baseline

- Archive SHA-256 `62565d5c…cf2c78b1` (unchanged).
- 4,422 files / 4,186 unique documents.
- The OCR background run (`01_ocr.py`, resumable) has finished **151 of about 502** image-only documents. The cache is not committed.

## 2. Batches since P01

| Batch | Commit | Supplier label | Docs | Products | Existing | Out of template | Unresolved / blockers |
|---|---|---|---|---|---|---|---|
| S06 | `bbdbb12` | BASF | 204 | 137 | 0 | 44 (Glysantin coolants, Breox / Plurasafe finished fluids, etc.) | 5 documents unresolved identity; 6 non-product |
| S07 | `c007d63` | LANXESS / Rhein Chemie | 125 | 51 | 0 | 4 Diphyl heat-transfer fluids | 3 phosphate esters (class); RC 9321 vs 9321 D kept apart (see note 1) |
| S08 | `f2d036b` | Sama Lubricants (trader) | 118 | 99 + 1 Kusa | 0 | 20 (transformer oils, coolant dyes / inhibitors, grease raw materials, fuel additive, heat-transfer fluid) | see note 2 |
| S09 | `c008721` | Croda | 102 | 40 | 0 | 2 (dicarboxylic acid, dielectric ester) | 28 esters: base fluid vs component |
| S10 | `49eebfc`, `00f0ce7` | BRB International | 90 | 83 | 1 (BRB_PETROLAD_8099) | 14 (12 fuel additives, coolant package, STOP SMOKE) | 12 (Thixocal scope, boosters, Petrolad 8100) |
| S11 | `4b510bd` | Clariant | 73 | 51 | 0 | 5 (Antifrogen, Hostagel, Genamin) | many components carry a metalworking / HFC scope question |
| S12 | `77a5ced` | INEOS | 55 | 46 | 0 | 0 | 23 polybutenes (role not stated); 2 LANXESS RC 9330 reports re-attributed |

**Note 1 (S07).** RC 9321 and RC 9321 D are kept as separate products. The LANXESS letter says their performance "is equal"; that statement is recorded, not used to merge them.

**Note 2 (S08 Sama), three open points:**
- The A1011 SDS prints "A1010" in its Section 1. This is an identity conflict and a blocker.
- One LABORELEC laboratory report has no sample identity on page 1.
- C8090, P5050 and SE543 have no product type printed, so their class is not inferred from the values.

## 3. New rules applied (documented in each generator)

**Distributor-issued documents (Sama).**
- The manufacturer printed in the grade name is recorded: Pertamina, CEPSA, IRPC, Thai Lube, Aramco, Luberef, ADNOC, Bapco, Kusa.
- These documents are never treated as manufacturer sources, and never matched to manufacturer records here.

**Printed variants are separate products:**
- solution viscosity (Viscotech 6540 L 850 / 1000 / 1200 / 1300 / 1600 cSt; LP);
- suffix letters (6779 / 6779A, 164 / 164X, 162 / 162S, 180I / 180R);
- dilutions (Polyglykol P 41/12000 vs P 41/12000 M 80 N);
- "SP … MBAL".

**Site-coded names.** Croda `-LQ-(GD)` / `(CQ)` / `(SI)` / `(MV)` / `(SG)` names are linked to the base grade with the suffix kept as printed. They are not asserted to be identical; any value difference stays a conflict.

**Dated editions.** Editions of one printed name (Petrolad 336, 19002) are linked as editions of the same product; their differences are left for the field review.

**Identity is never inferred from values.** NT561 and P46 print identical typical values and are kept apart.

**Branding.**
- The Cargill-branded "Priolube 1939" sheet (DL2-15219, viewed) is recorded as printed.
- Sheets with the same layout are flagged as "brand not individually viewed".
- No ownership claim is made.

**Multi-grade SDSs** (INDOPOL) link each printed grade with the role "covered by multi-grade SDS".

## 4. Registers (`tables/`, regenerated)

| Measure | P01 | P02 |
|---|---|---|
| Documents with reviewed identity | 1,210 | **1,977** of 4,186 |
| new_candidate products | 461 | 878 |
| existing | 264 | 264 |
| out_of_scope | 47 | 136 |
| Document–product links | – | 3,284 |

**Product count caveat.** A product's `material_class` can be `unresolved` while its status is `new_candidate`; both are listed per product in `product_register.csv`. Ester base fluids, PAG fluids, polybutenes and gelled sulfonates are schema / scope questions, not confirmed template matches.

## 5. Schema gaps and scope questions (cumulative additions)

- **Non-API-group synthetic base fluids:** esters (Priolube, BN046 / 047, SE513), PAGs (Emkarox, Polyglykol, PAG SE VG180) and naphthenic oils (no API group).
- **Polybutenes** (Indopol, Panalane, M7002): role not stated.
- **Out of template:**
  - transformer and dielectric oils;
  - heat-transfer fluids and brines;
  - coolant additives;
  - fuel additives;
  - grease raw materials and thickeners.
- **Water-based metalworking / HFC components** (Clariant Hostacor, Emulsogen, etc.; BRB Petrolad 5608N; Thixocal).

## 6. Remaining work (exact)

1. **Identity review: 2,209 documents.**
   - **Supplier labels, 798 documents:** Jinzhou Donggong 50, ExxonMobil 48, Lubimax / Coraplus 47, Kusa 46, KangTai 40, Eni 37, Dow 35, Chevron Phillips 33, Mingyue 30, Vanderbilt 29, Goncord 29, Yasho 27, Wuxi South 26, Functional Products 23, Emery / Oleon 20, then the smaller suppliers.
   - **No supplier label: 1,411 documents.** Use OCR text when the run completes, otherwise page images.
2. **Product consolidation across batches** by printed name and supplier, e.g.:
   - `KUSA:KUSACRYL 2231` with the Kusa batch;
   - LANXESS documents filed under other labels;
   - PetroChina Jilin keys.
3. **Field-level preparation, Packages, open reviews** as listed in P01 §6 (unchanged): 665 proposals (none approved), 508 open links, D3503 × DL2-11768, 6 visual checks, HiTEC 12210M claim dots, OLOA 55603 slides.

**Exact next batch:** S13 Jinzhou Donggong (50), then ExxonMobil (48).

## 7. Readiness statement

**No product is declared ready for conversion:**
- 2,209 documents are still unreviewed for identity;
- field-level preparation has not started in this workstream;
- several class / template questions are open (§5).
