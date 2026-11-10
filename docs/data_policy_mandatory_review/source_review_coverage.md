# Source-selection coverage (Rule 1): what was examined and what remains

Ledger: [reports/data_policy/source_coverage_ledger.csv](../../reports/data_policy/source_coverage_ledger.csv). It has one row per product × property: 2,175 rows for 259 base oils and packages, with these columns:
- documents examined, and how each is associated;
- technical and SDS pages that mention the property, with the first matching line;
- selected source and its class;
- selection status and reason;
- comparison status;
- documents that could not be searched.

Regenerate with `python tools/data_policy/source_coverage_ledger.py`. It writes the CSV and a `.meta.json` holding the data fingerprint the ledger was built from.

Properties covered:

| Class | Properties |
|---|---|
| Base oils | KV40, KV100, VI, density, specific gravity, CCS, flash point, pour point, Noack |
| Packages | KV40, KV100, density, specific gravity, flash point, pour point, TBN |

Components are not covered: their TDS/SDS-type values are shares and markers, reviewed by hand in Rule 1.

## Method, and why the ledger does not rely on the audit alone

For each product, the ledger collects every archive file cited **anywhere** in the product's records:
- values, alternates, conflicts and the product block;
- for 48 products, also archive files that name the product but are not cited. These come from the audit document map of 2026-10-27 and are flagged "name match (unverified)".

Every page is classified by content (`document_classes.classify_page`) and searched for the property label. A label hit means the document **mentions** the property. It does not mean a value for this grade was read: multi-product tables, "Report"/"N/A" cells and boilerplate also match. Image-only files are listed as unsearchable, except those whose class was read on a render (`document_classes.MANUAL`).

## Results (2026-11-10)

| Selection status | Rows | Of which mandatory (base-oil Tier 1) |
|---|---:|---:|
| technical value selected | 1,385 | 569 |
| SDS fallback, no associated technical page mentions the property | 46 | 6 |
| SDS fallback, reviewed: the technical document was read and does not give the property | 5 | 2 |
| exception: SDS kept for a recorded reason | 2 | 1 |
| pending: identity, conflicting editions, source reliability (with reason) | 26 | 11 |
| external (URL) source selected | 22 | 14 |
| Missing; no searchable associated document mentions the property | 463 | 186 |
| **Missing, but an associated document mentions the property (unreviewed lead)** | **165** | **89** |
| **Missing; some associated documents are image-only and were not read for this property** | **61** | **27** |
| SDS selected although a technical page mentions the property (unreviewed) | 0 | 0 |

This revision resolved 12 earlier "SDS selected, technical page unreviewed" rows:
- **FORMOSA 150N / 500N KV40 and specific gravity:** the specification prints "Report". SDS fallback reviewed.
- **INFINEUM_D3384 specific gravity:** the technical sheet was read on its render and gives density, not specific gravity.
- **Chevron N204 / N216:** the only document is their own image-only SDS, so no technical document exists.
- **FORMOSA KV100:** the specification range is now selected, with the SDS typical value as an alternate.

| Comparison status | Rows |
|---|---:|
| a TDS–SDS pair exists in the inventory (comparable, unknown, bound check, not comparable) | 58 |
| **gap: a technical page and an SDS page both mention the property; no comparison recorded** | **137** (32 mandatory) |
| not possible: only one document class, or no searchable document, mentions the property | 1,980 |

## Remaining coverage gaps (not reviewed in this workstream)

1. **137 comparison gaps.** By property: flash point 53, density 33, pour point 28, specific gravity 17, KV40 4, VI 2.
   - Many are expected to be leads without a comparable value for the grade, for example SDS boilerplate or a "Report" cell. They were not read one by one.
   - The TDS–SDS inventory is therefore **not exhaustive**.
2. **165 "Missing, label found" leads** (89 on mandatory base-oil properties).
   - A sample of 22 was inspected from the matching line, and 6 of them were read in the source:

     | Lead | What the source shows | Assessment |
     |---|---|---|
     | Chevron Group II table DL2-10004.pdf | "Report" / "N/A" in the cells | records correct |
     | ExxonMobil "Density Correction Factor", Formosa "Vapor Density", Nynas "Annex VI", S-OIL "Low CCS" | label noise | records correct |
     | ARAMCO DURA KV100 | "-" or "30/33" in a multi-column table; column mapping needed | unresolved |
     | Petro-Canada DL2-10020.pdf p.2 VI and CCS rows | values in a multi-grade table; column mapping needed | unresolved |
     | ExxonMobil APE Core 2500 | CCS maxima at −15 / −25 °C on DL2-13265.pdf | possible value; which product the document covers is unconfirmed |
     | Chevron Synfluid mPAO 50 | density 7.046 lb/gal with no temperature | value printed without its required condition |

   - These remain **absent** in the eligibility outcomes, because no value is recorded. Each needs a column-level reading before a value can be entered.
3. **61 Missing rows and 237 rows in total with image-only associated documents** that were not read for the property.
4. **External sources** (22 selected values) were not re-read in this workstream. AFTON_HITEC_8788B in particular is pending: its external PDS has not been reviewed against the SDS.
5. **Name-match associations** (48 products) come from a heuristic document map and are unverified.

## Pending source selections (field level)

Defined in `source_selection.PENDING` and `PENDING_FIELDS`. Mandatory fields that are pending become `unresolved_source_selection` in eligibility.

| Product | Fields | Reason |
|---|---|---|
| NESTE_NEXBASE_3043 | density, flash point, Noack | family TDS DL2-10962 (Edition 8) and the individual sheet disagree; both undated |
| NESTE_NEXBASE_3050 | density, pour point | same |
| NESTE_NEXBASE_3060 | KV40, KV100, density, Noack | same |
| NESTE_NEXBASE_3080 | KV40, KV100, VI, density, flash point, pour point | same |
| S_OIL_ARAMCO_ULTRA_8 | KV40, KV100, flash point | external S-OIL web table (typical) vs archived SDS (ranges); identity question ID-01 open |
| RICHFUL_RF6066 | density, KV100, TBN, Zn, Ca | two undated TDS disagree |
| RICHFUL_RF6069 | KV100 | supplier web page (142) vs archived TDS (118) |
| AFTON_HITEC_8788B | KV40, KV100, density, flash point | external PDS not reviewed |

FORMOSA 150N / 500N KV100 is no longer pending. Under the clarified rule, the specification range DL2-10001 / DL2-10003 (Min./Max.) is selected as printed, with the SDS typical value kept as an alternate (change log).
