# Evidence review of the outstanding source leads (revision 3, 2026-11-10; completed 2026-11-11)

This review covers every outstanding lead from the revision-2 coverage ledger, every name-match document association, the identity of the FORMOSA KV100 selections, and (2026-11-11) every value taken from an external (URL) source.

**Tools**
- `tools/data_policy/lead_review.py`: decisions in `lead_review_decisions.json`; output in `reports/data_policy/lead_review.csv`.
- `tools/data_policy/association_review.py`: decisions in `association_review_decisions.json`; output in `reports/data_policy/name_match_review.csv`.
- `tools/data_policy/external_review.py`: decisions in `external_review_decisions.json`; output in `reports/data_policy/external_review.csv` (section 8).
- `tools/data_policy/source_review_status.py`: the review state of every ledger row; output in `reports/data_policy/source_review_status.csv` (section 9).
- The resulting data changes are declared in `tools/data_policy/source_selection.py` (fills, `LIST_FILLS`, `QUALIFIER_FIXES`, `CONFLICT_ADDS`, `PENDING_FIELDS`) and listed in `reports/data_policy/source_selection_changes.csv`.

**How pages were read**
- Where a cell's column or row had to be established, pages were read on their render (multi-grade tables, image-only files). Otherwise they were read from the text layer.
- A keyword mention was treated as a lead only, never as proof of a product-specific value.
- No source document or evidence byte was changed.

## 1. Cases and outcomes (deduplicated by product × property)

**The case set** (counting unit: product × property, deduplicated). It is frozen at the 352 cases of the revision-2 ledger (commit `4e83652`). Cases are added when they appear during the review, 11 in all:
- 8 appeared because corrections linked new documents to products: ETRO 4 and the aramcoPRIMA 110/230/500 grades.
- 2 (PRIMA 500 KV40 and CCS) are listed in `added_cases` so that they remain reported after being filled.
- 1 (NEXBASE 3080 flash point, added 2026-11-11) appeared when its SDS page 4 stopped being classified as technical; it is closed by its reviewed SDS comparison.

A case can sit in several lists; it is reviewed once, so the list rows add up to more than 363.

| List | Cases | usable evidence | already recorded | unrelated mention | insufficient evidence | unavailable source | unresolved identity |
|---|---:|---:|---:|---:|---:|---:|---:|
| mandatory property Missing, document mentions it | 89 | 1 | 0 | 37 | 51 | 0 | 0 |
| mandatory property Missing, image-only document | 32 | 3 | 0 | 0 | 29 | 0 | 0 |
| other property Missing, document mentions it | 76 | 7 | 0 | 18 | 51 | 0 | 0 |
| other property Missing, image-only document | 38 | 0 | 0 | 0 | 38 | 0 | 0 |
| technical and SDS pages both mention it, no comparison | 139 | 71 | 31 | 18 | 12 | 0 | 7 |
| **All cases (deduplicated)** | **363** | **81** | **31** | **71** | **173** | **0** | **7** |

Every case has a recorded outcome; none is "not reviewed". Many cases are no longer open in the current ledger, because they were closed by a fill, a recorded comparison or a classifier correction; `lead_review.csv` column `in_current_ledger` says which.

**Corrections of 2026-11-11.** The earlier figures (362 cases; 79 usable; 32 already recorded) were wrong in two places. LUBRIZOL_CV2301 pour point has a reviewed SDS comparison, but it fell under the generic Lubrizol "already recorded" rule; that rule now skips cases with a reviewed comparison. NEXBASE 3080 flash point had a reviewed comparison but no case. Now every one of the 70 product × property cases with a reviewed comparison is a usable-evidence case (regression test `test_comparison_cases_are_usable_lead_cases`).

What the outcomes mean:

| Outcome | Meaning |
|---|---|
| **insufficient evidence** | The cell for this grade is "Report", "-", "N/A", "To be reported", "Not available" or blank; or the value lacks a condition the property requires (density in lb/gal or kg/L with no temperature); or the label and unit contradict each other ("Specific gravity … g/m3", "Relative density … g/cm3"); or the supplier marks the typical value as provisional (aramcoPRIMA 110). Nothing to enter. |
| **unrelated mention** | The keyword belongs to something else. Examples: "Density Correction Factor", "Vapour density", "Annex VI"; prose ("Low CCS viscosity …"); evaporation loss by ASTM D972 (not Noack); finished-oil TBN; a table for other grades; another product's document. |
| **already recorded** | The value is already in the record (Lubrizol handling pages of the same technical sheet; the HiTEC 12210M density exception). |
| **unresolved identity** | FORMOSA: the SDS names "150N/500N Base oil" without the GII+/GII grade. |
| **usable evidence** | 81 cases in total:<br>• 11 cases led to 11 field fills (section 2). One of them, the mPAO 65 flash point, sits in the comparison-gap list, but its SDS value was kept as an alternate, not as a comparison row.<br>• 70 cases had their SDS value recorded as a TDS–SDS comparison: 69 with no data change, and CV2301 flash point, which is also a conflict (section 2). These 70 cases give 71 comparison rows, because S_OIL_ULTRA_S_3 flash point has two SDSs.<br>The ERGON qualifier correction came from re-reading the source page, not from a lead case. |

## 2. Data changes supported by the evidence (all declared, idempotent, before/after in the change list)

| Product · field | Before | After | Evidence (read) |
|---|---|---|---|
| CHEVRON_GROUP_II_600R · kv40 | Missing | ≥ 100 cSt at 40 °C (specification minimum) | DL2-10004.pdf p.1, 600R column "100 (MIN)" (render) |
| PETRONAS_ETRO_6 · ccs | Missing | 2,088 / 3,977 / 7,422 cP at −25 / −30 / −35 °C (typical) | the record's own TDS DL2-12475.pdf (image, render) |
| ARAMCO_LUBEREF_PRIMA_500 · kv40, ccs | Missing | 96.4 cSt; 14,550 / 26,000 mPa·s at −20 / −25 °C (typical) | brochure DL2-11773.pdf, column "aramcoPRIMA 500" (render; no provisional mark) |
| CHEVRON_SYNFLUID_MPAO_65 · flash_point | Missing | > 266 °C (COC); SDS 270 °C (ASTM D-92) kept as an alternate | DL2-11910.pdf p.1; SDS DL2-11908.PDF p.3 |
| ERGON_HYGOLD_P150BS · noack_volatility | Missing | 1.1 wt% (typical, ASTM D5800) | DL2-10961.pdf p.1 (render) |
| EXXONMOBIL_SPECTRASYN_ULTRA_1000 · specific_gravity | field absent | 0.855 at 15.6 °C (typical) | DL2-13746.pdf p.1 (© 2011 sheet of the same product) |
| NESTE_NEXBASE_3020 / 3043 / 3060 / 3080 · specific_gravity | field absent | 0.82; 0.82–0.84; 0.83–0.85; 0.84 at 15 °C (SDS fallback) | each grade's SDS, section 9; no technical document prints specific gravity |
| ERGON_HYGOLD_5000BS / P70N · viscosity_index.qualifier | "minimum" on the typical value 81 | null (minimum 80 / 60 kept in `min`; `qualifier_previous` kept) | DL2-10409.pdf / DL2-13346.pdf p.1 (render): specification MIN 80 / 60, TYPICAL 81 |

The review also recorded these disagreements as conflicts. None is resolved, and every affected field is pending:

| Conflict | Product · fields | Disagreement |
|---|---|---|
| `EVR-2026-11-10-ETRO4` | PETRONAS_ETRO_4 · KV100, VI, CCS | PDS DL2-10230.pdf vs the ETRO 4 column of DL2-12475.pdf: 4.22 vs 4.26; 129 vs 130; 810/1,390/2,500 vs 886/1,442/2,419. Both documents are undated. |
| `EVR-2026-11-10-CV2301` | LUBRIZOL_CV2301 · flash point | The technical document DL2-13065.pdf prints 158 °C (p.2) and 165 °C PMCC (p.3); the SDS prints 158 °C. |
| `EVR-2026-11-10-110/230/500-density` | ARAMCO_LUBEREF_PRIMA_110 / 230 / 500 · density | The specification DL2-12172.pdf (no unit) vs the brochure DL2-11773.pdf (Kg/L at 15 °C): 0.8500 vs 0.8510; 0.8630 vs 0.8625; 0.867 vs 0.8720. The brochure marks the 110 and 230 typicals "subject to confirmation". |
| `EVR-2026-11-11-230-density-external` | ARAMCO_LUBEREF_PRIMA_230 · density | The Aramco PRIMA 230 sheet (external; bytes equal to the registry hash) prints 0.8635 kg/L at 15 °C: a third value (section 8). |
| `EVR-2026-11-11-230-noack` | ARAMCO_LUBEREF_PRIMA_230 · Noack | The same sheet prints a typical 7.5 wt%, above the DL2-12172.pdf maximum 7 (logically incompatible). The selected value is unchanged; Noack is not a pending field. |

Not changed:
- Nothing was entered from a family document without a grade column, a provisional typical, a value without its required condition, or an undefined notation (S-8 pour point "L-40.0").
- Specific gravity was never converted to density.
- No mass basis was assumed.

## 3. Document identity (item 2)

### Name-match associations

All 174 (product, document) pairs that the ledger had linked by name only were checked against the document's own identity text (`name_match_review.csv`). The set is frozen at the revision-2 ledger (`4e83652`) and unioned with the current ledger, as for the lead cases.

| Verdict | Pairs | Notes |
|---|---:|---|
| same product | 87 | The document names this exact product, or has a column or row headed with this grade. 3 of them were then used as fill sources and are now cited (`now_cited = true`): SpectraSyn Ultra 1000 / DL2-13746.pdf, NEXBASE 3060 / DL2-12735.pdf, NEXBASE 3080 / DL2-14512.pdf |
| byte-identical copy of a cited file | 78 | |
| other product | 9 | NYNAS Base Stock 20 ↔ the NYNAS S 3B SDS and the NS 3 sheet; S-OIL S-8 (Super 60N) ↔ seven Ultra-S series sheets |
| **Total** | **174** | 87 + 78 + 9 |

The earlier "84 same product" (which left 3 of the 174 unaccounted for) came from reading only the current ledger, where the 3 now-cited pairs are no longer name matches. The ledger excludes the 9 other-product associations (column `excluded_associations`). No evidence was taken from them.

### FORMOSA KV100 selections

- **FORMOSA_150N_GII_PLUS.** DL2-10001.pdf names "Product Name: Base Oil 150N GII+", Product NO. B150N GII+ (issued 2009-10-21). This is identical to the record's product name, "Base Oil 150N GII+". The selected 5.0–5.4 mm²/s specification range therefore applies to this exact record.
- **FORMOSA_500N_GII.** DL2-10003.pdf names "Base Oil 500N GII", B500N GII. This is identical to the record. The selected 10–12 mm²/s applies.
- **The FPCC table DL2-12108.jpeg (ID-15) was not used.** Its "150N" specification KV100 is 5.0–5.6, not 5.4, which supports keeping ID-15 open.
- **The FORMOSA SDSs** (DL2-10011, DL2-10017) name only "150N Base oil" / "500N Base oil". Formosa supplies 150N as both GII and GII+, so the SDS link to the exact grade is not established.
  - The SDS-fallback KV40 and specific-gravity values of both records are therefore now **pending (identity)**. They were not removed.
  - The SDS KV100 values stay as alternates with their provenance.

## 4. Co-component statements (decision B evidence; no data change)

`tools/mandatory_properties/co_component_evidence_scan.py` searched the text layer of each package's cited pages; output in `reports/mandatory_properties/co_component_evidence.csv`.

| Finding | Packages | Detail |
|---|---:|---|
| Explicit "none required" statement | 2 | AFTON_HITEC_12210 and 12210M: "already contains a pour point depressant (PPD) so no supplemental PPD should be needed". This covers the PPD only; nothing is said about a VM. |
| Co-components named or required | 13 | For example Infineum: "in combination with approved base stocks and viscosity modifiers"; Lubrizol 3700: "Addition of a 0.25 % by weight TBN booster required to claim MTU Type 1"; dosage rows "… + Infineum D2359 at 1.93 %". Most give no name or wt.% dose. |
| No explicit statement found | 63 | |

An empty co-component list is not treated as evidence of absence.

## 5. Treat-rate mass basis (decision E; unchanged)

- All 93 bare-"%" values were rechecked on their pages, including headings and footnotes. Only the three cases in `treat_rate_basis_evidence.json` state a mass basis.
- No other source context resolves the basis, and none is assumed.

## 6. Classifier corrections found by the review

- **Lubrizol "Unloading, storage and blending instructions" pages** were classified as SDS, because their text refers to the Safety Data Sheet. They are now TECHNICAL/handling.
  - 28 apparent TDS–SDS comparison gaps were in fact the same technical document printing the same value.
  - One exception is CV2301, recorded as a conflict.
- **NEXBASE 3080 SDS p.4** was classified as technical, because SDS section 9 prints "typical value". Inside an SDS file, only an explicit technical-sheet heading now makes a page technical.
- The cited-page classification changed for only these pages.

## 7. Remaining evidence gaps (reviewable only with information not in the archive, or needing a decision)

| Gap | Cases | Why it remains |
|---|---:|---|
| Values not printed for the grade ("Report", "-", "N/A", blank, "To be reported") | majority of the 173 insufficient | Nothing to extract; needs a supplier document that prints the value. |
| Values without a required condition (density in lb/gal or kg/L with no temperature; relative density on an SDS without the water reference) | Chevron Synfluid, PETRONAS ETRO 4 / 4+, PRIMA 110 / 230 / 500 (no unit), several SDSs | No conversion or inference allowed. |
| Inconsistent label and unit (YUBASE specific gravity in g/m³; Richful SDS "relative density … g/cm³") | 6 | A correction would be an interpretation. |
| Provisional supplier typicals (aramcoPRIMA 110 / 230 brochure columns) | 2 + density conflicts | The supplier marks them as subject to confirmation. |
| Identity not established (FORMOSA SDSs; ID-15 FPCC table; ID-01 Ultra-S 8 vs aramcoULTRA 8) | 7 lead cases + pending fields | Needs a grade-specific document. |
| Conflicting undated technical documents (ETRO 4; NEXBASE family vs individual sheets; PRIMA densities; RF6066; RF6069) | pending fields | Needs a dated edition or a supplier statement. |
| External sources that could not be obtained (Afton HiTEC 12204L and 8788B PDSs, Internet Archive) | 8 (4 selected values, 4 pending fields) | On 2026-11-11 the Internet Archive refused automated download and the fetch tool cannot open web.archive.org; no saved copy exists. A manual download whose bytes match the registry SHA-256 would allow the review. |
| External technical page vs archived SDS (aramcoULTRA 8 KV40/KV100/flash; distributor flyer for BAPbase 4) | 3 pending fields + 1 unfilled field | Values confirmed as printed; whether an external document may be selected over an archived SDS, or fill a Missing field, is a policy decision. |
| SDS values recorded as comparisons but not screened | the "pending" rows in `tds_sds_comparisons.csv` | They await the threshold decisions. |

**Is the evidence review complete?** The **archive lead review** (363 cases) and the **external-source review** (29 cases) are complete in the sense that every case has a recorded outcome. That does **not** mean all source verification is complete:
- 181 reviewed rows end as evidence unavailable and 7 as inconclusive (section 9);
- 1,783 ledger rows were never individually re-read; their state rests on the mechanical page classification;
- the decision-dependent items above depend on decisions or documents that the archive does not contain.

## 8. External-source review (2026-11-11)

**Scope** (counting unit: product × property). 29 cases:
- the 22 values the ledger marks `external_selected` (selected from a URL registered in `source_registry.json`);
- the 7 pending fields whose open question is an external technical source: AFTON_HITEC_8788B KV40/KV100/density/flash point, and S_OIL_ARAMCO_ULTRA_8 KV40/KV100/flash point.

**Method.** For each value: obtain a copy whose identity is established, then check the product (grade column), property, unit, qualifier, conditions and page against the record. Then compare with the applicable SDS.
- Copy identity was established in one of three ways:
  - the bytes equal the registry SHA-256;
  - a saved evidence copy with a verified hash;
  - for the Richful data feeds, which the registry does not hash, a retrieval on 2026-11-11 that agrees with the archived TDS.
- Decisions pin the reviewed record values (`expect`). `external_review.py` stops if a record or a stored evidence hash changes.

| Source | Cases | Copy | Outcome |
|---|---:|---|---|
| S-OIL Lube Base Oil page (Ultra-S 2/3/4/6/8; aramcoULTRA 8) | 13 selected + 3 pending | the saved Internet Archive capture 2026-06-10 and the live copy 2026-10-30 (`reconciliation/audit_evidence/`, hashes verified; the two tables are identical) | confirmed (16) |
| Aramco aramcoPRIMA 230 (Yanbu) sheet | 2 (KV100 6.65 cSt; CCS −25 °C 5,900 mPa-s) | bytes = registry SHA-256 `977c8fee…`; stored | confirmed |
| Ergon/MOGO 2025 flyer p.4 (BAPbase 4) | 1 (KV40 19.54 cSt) | bytes = registry SHA-256 `9a8728c3…`; not stored (15 MB) | confirmed |
| Richful data feeds 109 (RF6078) and 130 (RF6406) | 2 (density 952–992 / 972 kg/m³ at 20 °C; TBN 168–198 / 185) | retrieved 2026-11-11, stored; the same rows are in the archived TDS DL2-15832.pdf / RF6078 TDS and DL2-15456.pdf | confirmed |
| Afton HiTEC 12204L PDS 06/17 (Internet Archive) | 4 (KV100, density, flash point, TBN) | **not obtained**: automated download refused; the fetch tool cannot open web.archive.org; no saved copy | inconclusive: source unavailable (the registry check of 2026-10-23 is reported, not repeated) |
| Afton HiTEC 8788B PDS (Internet Archive) | 4 pending (KV40, KV100, density, flash point) | **not obtained** (same reason) | inconclusive: source unavailable; the fields stay pending |

**SDS comparison.**
- Most re-read values have no SDS value for the same property and condition, so no comparison was possible. Examples:
  - the PRIMA 230 SDS prints only KV40 45 mm²/s and flash point 235 °C;
  - the aramcoULTRA 8 SDS prints a relative density, which is a different property from density;
  - the Ultra-S 3 SDS prints only a vapour density.
- RF6078 density is already an inventory pair.
- No new TDS–SDS inventory row resulted.
- The aramcoULTRA 8 external typicals sit as follows against the archived SDS ranges and the Aramco 2024 catalog bounds (catalog bytes equal to the registry hash):
  - KV100 7.1 and flash point 250 °C lie inside the SDS ranges and are logically compatible with the catalog;
  - **KV40 41.10 lies below the SDS range 42.0–55.0**: logically incompatible, and already recorded as an unresolved edition-difference conflict by the 2026-10 audit (41.1 vs 42.0–55.0; not recorded twice).

**Further evidence found on the re-read documents** (recorded, not used as fills):
- PRIMA 230 Noack typical 7.5 vs specification maximum 7 → conflict `EVR-2026-11-11-230-noack`.
- PRIMA 230 density 0.8635 kg/L → conflict `EVR-2026-11-11-230-density-external`. The field stays pending.
- PRIMA 230 CCS at −20 °C 3,200 mPa-s: not added. The record's CCS list is not Missing, and the fill rule covers Missing fields only.
- BAPbase 4 specific gravity 15/4 °C 0.834 (MOGO flyer): not filled. Whether a distributor-issued external document may fill a Missing field is a policy decision.
- Representation notes, not changed because both read as point values in every check:
  - BAPbase 4 KV40 has value_kind "single" under a column headed "typical";
  - aramcoULTRA 8 CCS has qualifier "Typical" with value_kind "single".

## 9. Review state of every ledger row (`source_review_status.csv`)

Counting unit: coverage-ledger row (product × property; 2,175 rows, 259 products).

| Review state | Rows | Mandatory | What it means |
|---|---:|---:|---|
| archive lead review complete | 183 | 61 | lead case with a definite outcome: usable 81, already recorded 31, unrelated mention 71 |
| external review complete | 21 | 16 | external value confirmed on an identified copy (18 selected + 3 pending) |
| evidence unavailable | 181 | 81 | reviewed, and the evidence is not where it was sought: 173 archive cases where the documents do not print the value, plus 8 external cases where no copy could be obtained |
| evidence inconclusive | 7 | 2 | document identity not established (FORMOSA SDSs) |
| not individually reviewed | 1,783 | 745 | the row's state rests on the mechanical classification only (for example a technical value selected by page class, or Missing with no mention in any associated document) |

The 392 reviewed rows are exactly the 363 lead cases plus the 29 external cases; no row is in both.
