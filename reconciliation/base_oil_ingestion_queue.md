# Ingestion queue: 9 base oils with archived supplier datasheets

At the reconciliation, these inventory materials had no JSON, but a supplier document in
`Manual + Data to share.zip` prints values for each grade.

Ingestion status:

- **#1 NYNAS T 22:** ingested 2026-10-23 (pilot) as `NYNAS/NYNAS_T_22`.
- **#2 NYNAS T 110:** ingested 2026-10-23 as `NYNAS/NYNAS_T_110`. The sheet prints no issuing date.
- **#3 aramcoPRIMA 150:** ingested 2026-10-23 as `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_150` (brochure typicals only; no specification sheet in the archive).
- **#4 aramcoPRIMA 100:** ingested 2026-10-23 as `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_100` (brochure typicals only; Noack and CCS at -20 °C cells blank).
- **#5 aramcoPRIMA 220:** ingested 2026-10-23 as `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_220` (brochure typicals only; saturates and CCS at -25 °C cells blank).
- **#6 aramcoPRIMA 600:** ingested 2026-10-23 as `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_600` (brochure typicals only; Noack cell blank).
- **#7 aramcoPRIMA 500L:** ingested 2026-10-23 as `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_500L`. All values are provisional typicals under the footnote '*Typicals are subject to confirmation upon startup of the new Group II plant.'
- **#8 NEXBASE 3030:** ingested 2026-10-23 as `NESTE/NESTE_NEXBASE_3030` (family TDS 'Edition 8', no date; no test methods printed; API Group not stated for this grade).
- **#9 FPCC 70N GII:** ingested 2026-10-23 as `FORMOSA/FORMOSA_FPCC_70N_GII` (no document date printed; '2017 AUG' dates the typical column only; DL2-12109/DL2-12111 confirmed pixel-identical copies of DL2-12108).

All nine queue items are ingested.

Each product gets one folder with three tier files, built from the base-oil templates:

- `json_templates/base_oil_tier1_blocking.json`
- `json_templates/base_oil_tier2_verification.json`
- `json_templates/base_oil_tier3_substitution.json`

All five source documents are scans or images without a text layer, so values must be read from the
rendered page, as the existing scanned-document records were. The page numbers below are PDF page
indices; printed page numbers are given where they differ. No existing JSON cites any of these five
documents: the sibling grades already in JSON were built from other documents (listed per entry).

| # | Sheet row (Base oils) | Material ID | Product | Priority | Source document (archive path under `Raw Lubrincats Datasheets/Base oils/`) | Location in document | Revision / date printed |
|---|---|---|---|---|---|---|---|
| 1 | 182 | BO-NYNAS-NYNAS-T-22 | NYNAS T 22 | C | `NYNAS/DL2-12371.pdf`, Nynas product data sheet | p.1 (single page): "Specification limits" Min/Max and "Typical data" columns | "Issuing date: 2012-08-10" |
| 2 | 181 | BO-NYNAS-NYNAS-T-110 | NYNAS T 110 | C | `NYNAS/DL2-12370.pdf`, Nynas product data sheet | p.1 (single page): "Guaranteed data" Min/Max and "Typical data" columns | none printed |
| 3 | 9 | BO-ARAMCO-ARAMCOPRIMA-150N | aramcoPRIMA 150 | A | `Aramco Luberef/DL2-11773.pdf`, aramcoPRIMA brochure "Group II" table (identical copies per register: DL2-11774, DL2-11781 to DL2-11784) | p.1 (printed brochure pp. 8-9): column "aramcoPRIMA 150 / Typical" | none printed |
| 4 | 42 | BO-ARAMCO-ARAMCOPRIMA-100 | aramcoPRIMA 100 | B | same as #3 | p.1 (printed pp. 8-9): column "aramcoPRIMA 100 / Typical" | none printed |
| 5 | 44 | BO-ARAMCO-ARAMCOPRIMA-220 | aramcoPRIMA 220 | B | same as #3 | p.1 (printed pp. 8-9): column "aramcoPRIMA 220 / Typical" | none printed |
| 6 | 47 | BO-ARAMCO-ARAMCOPRIMA-600 | aramcoPRIMA 600 | B | same as #3 | p.1 (printed pp. 8-9): column "aramcoPRIMA 600 / Typical" | none printed |
| 7 | 46 | BO-ARAMCO-ARAMCOPRIMA-500L | aramcoPRIMA 500L | B | same as #3 | p.1 (printed pp. 8-9): column "aramcoPRIMA 500L* / Typical"; footnote "*Typicals are subject to confirmation upon startup of the new Group II plant." | none printed |
| 8 | 95 | BO-NESTE-NEXBASE-3030 | NEXBASE 3030 | B | `NESTE OIL/DL2-10962.pdf`, Neste Oil technical data sheet for NEXBASE 3020, 3030, 3043, 3050, 3060 and 3080 | p.1: "Technical Data" table, column "Nexbase 3030" (Spec and Typ) | "Edition 8", no date |
| 9 | 87 | BO-FORMOSA-FPCC-70N-GII | FPCC 70N GII | B | `FORMOSA/DL2-12108.jpeg`, "Specification of FPCC API GII Base Oil" (pixel-identical copies per register: DL2-12109.jpeg, DL2-12111.jpeg) | single image: columns "Specification 70N" and "Typical (2017 AUG) 70N" | typical values dated "2017 AUG" |

## Notes per document

- **DL2-12371 / DL2-12370 (Nynas T 22 / T 110):**
  - Both are product-specific; each describes itself as "a naphthenic base oil", "hydrotreated".
  - No API Group is printed.
  - T 22 carries the footnote "Severely Hydrotreated Base Oil"; no equivalent footnote is visible on T 110.
  - Existing Nynas folders use the `<ID>_tier1.json` form, e.g. `NYNAS/NYNAS_T_3/`.
- **DL2-11773 (aramcoPRIMA):**
  - The heading "Group II" covers all eight grades.
  - Existing sibling JSONs `ARAMCO_LUBEREF_PRIMA_110`, `_230` and `_500` are built from DL2-12172 (specification), not from this brochure.
  - Some cells are blank for some grades (for example Noack, Brookfield and saturates), so those properties will stay Missing.
  - Inventory naming is inconsistent: aramcoPRIMA 150 has manufacturer "Saudi Aramco" and Material ID suffix `-150N`; the other grades have "Saudi Aramco / Luberef".
  - Folders in `ARAMCO LUBEREF/` use the `<ID>__base_oil_tier1_blocking.json` form.
- **DL2-10962 (NEXBASE family sheet):**
  - The register notes that this is an older family sheet whose densities differ from the individual-grade TDSs used for NEXBASE 3020/3043 to 3080.
  - It says "NEXBASE 3020 and NEXBASE 3030 are used in hydraulic and transmission oil formulations"; only the other grades "conform to ACEA Group III".
  - Neste folders use the `<ID>_tier1.json` form.
- **DL2-12108.jpeg (FPCC):**
  - Sibling JSONs `FORMOSA_150N_GII_PLUS` and `FORMOSA_500N_GII` are built from DL2-10001/DL2-10011 and DL2-10003/DL2-10017, not from this image.
  - Formosa folders use the `<ID>_tier1.json` form.

## Proposed folder names (to confirm before creation)

These follow the sibling folders in the same supplier directory:

- `NYNAS/NYNAS_T_22`
- `NYNAS/NYNAS_T_110`
- `ARAMCO LUBEREF/ARAMCO_LUBEREF_PRIMA_150`, `_PRIMA_100`, `_PRIMA_220`, `_PRIMA_600` and `_PRIMA_500L`
- `NESTE/NESTE_NEXBASE_3030`
- `FORMOSA/FORMOSA_FPCC_70N_GII`

After creation, each record needs an entry in `open_questions_and_conflicts.md`, and the coverage
workbook must be regenerated through the usual temporary-file comparison.
