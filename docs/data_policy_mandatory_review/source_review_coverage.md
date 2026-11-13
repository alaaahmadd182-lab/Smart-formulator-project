# Source-selection coverage (Rule 1): what was examined and what remains

Revision 3, 2026-11-10; completed 2026-11-11. The case-by-case review of the archive leads and of the external sources is in [evidence_review.md](evidence_review.md) (sections 1 and 8).

**Ledger.** [reports/data_policy/source_coverage_ledger.csv](../../reports/data_policy/source_coverage_ledger.csv) has one row per product × property: 2,175 rows covering 259 base oils and packages.
- Regenerate it with `python tools/data_policy/source_coverage_ledger.py`. That also writes `.meta.json` with the data fingerprint.
- **Properties covered:** for base oils, KV40, KV100, VI, density, specific gravity, CCS, flash point, pour point and Noack. For packages, KV40, KV100, density, specific gravity, flash point, pour point and TBN.

## Method

For each product, the ledger collects:
- every archive file cited anywhere in the product's records;
- every file linked to the product by name, **if that association was reviewed as the same product or a byte-identical copy** (`association_review_decisions.json`).

Associations reviewed as another product are excluded and listed in `excluded_associations`. Each page is classified by content (`document_classes.py`) and searched for the property label.

The ledger labels rows mechanically. Its lead labels ("Missing, label found", "not searchable", "gap") are **leads**. The reviewed outcome of every such case is in `reports/data_policy/lead_review.csv`; the outcome of every external-source value is in `reports/data_policy/external_review.csv`; and the review state of every ledger row is in `reports/data_policy/source_review_status.csv` (section "Review state" below).

## Selection status (current data)

| Selection status | Rows | Mandatory |
|---|---:|---:|
| technical value selected | 1,385 | 567 |
| SDS fallback, no associated technical page mentions the property | 49 | 6 |
| SDS fallback, technical document read and does not print the property | 2 | 0 |
| exception (SDS kept, reason recorded) | 2 | 1 |
| pending (identity, conflicting technical documents, reliability) | 34 | 17 |
| external (URL) source selected (all reviewed: see `external_review.csv`) | 25 | 16 |
| Missing, no associated document mentions the property | 457 | 183 |
| Missing, a document mentions the property (all reviewed: see `lead_review.csv`) | 154 | 86 |
| Missing, image-only associated document (all read on renders) | 67 | 29 |
| SDS selected although a technical page mentions the property | 0 | 0 |

| Comparison status (current data) | Rows |
|---|---:|
| a TDS–SDS pair exists in the inventory (comparable, unknown, bound check, not comparable) | 132 |
| both document classes mention the property but no pair: reviewed as unrelated, insufficient or unresolved identity (`lead_review.csv`) | 38 |
| not possible: only one document class, or no searchable document, mentions the property | 2,005 |

The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 151 rows. 71 of them come from SDS values recorded in this review (70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs), and 10 have a registered external technical source on the technical side (added 2026-11-11).

## External selected values and their SDS comparison (`external_comparison_accounting.csv`)

Counting unit: a value object whose selected source is a URL (product × field). There are 114; 29 are properties of the coverage ledger (25 `external_selected`, 4 pending). Every one has exactly one status, from `tools/data_policy/external_comparison_accounting.py`:

| Comparison status | All 114 values | The 25 ledger `external_selected` values |
|---|---:|---:|
| paired with an SDS value in the inventory | 8 | 4 |
| inapplicable: text, classification, claim or block (no numeric comparison) | 41 | 0 |
| inapplicable: the external source is itself an SDS | 11 | 0 |
| inapplicable: the SDS prints a different quantity (reviewed) | 2 | 2 |
| unavailable: no SDS document is associated with the product | 1 | 1 |
| unavailable: no SDS page mentions the property | 14 | 14 |
| unresolved: the external source could not be obtained (value not verified) | 31 | 4 |
| unresolved: numeric property outside the coverage ledger, not assessed | 6 | 0 |
| **Total** | **114** | **25** |

- **Evidence state, reported separately and never upgraded:** copy read in the external review 26; registry-verified but not re-read in the external review 57; external source not obtained 31 (the Afton HiTEC 12204L / 12250 and 8788B data sheets).
- The 8 paired values give 10 inventory rows: aramcoULTRA 8 KV40, KV100 and flash point; RF6078 density; RF6066 density (2), KV100 (2) and TBN; RF6069 KV100.
- "No SDS page mentions the property" is a text-layer finding over the documents associated with the product.
- The 6 numeric values outside the ledger (RF6066 Ca and Zn, an RF6406 treat rate, HiTEC 5748 shear stability, aramcoULTRA 8 sulfur and saturates) were not assessed against an SDS; they are listed as unresolved, not as compared.

## Review state (`source_review_status.csv`; counting unit: ledger row)

| Review state | Rows | Mandatory |
|---|---:|---:|
| completed archive lead review (usable 81, already recorded 31, unrelated mention 71) | 183 | 61 |
| completed external-source review (confirmed on an identified copy) | 21 | 16 |
| evidence unavailable, read: the archive documents were read and do not give sufficient information | 173 | 81 |
| evidence unavailable, not obtained: no copy of the external source could be obtained, so nothing was read | 8 | 0 |
| evidence inconclusive: document identity not established | 7 | 2 |
| not individually reviewed: the state rests on the mechanical classification only | 1,783 | 745 |
| **Total** | **2,175** | **905** |

The two "evidence unavailable" lines share one state in `source_review_status.csv` (181 rows) and are told apart by its `lead_outcome` and `external_outcome` columns; `evidence_review.md` section 10 explains them.

A recorded outcome for every one of the 363 frozen lead cases and the 29 external cases does **not** mean that all source verification is complete. 188 reviewed rows end without usable evidence, and 1,783 rows were never individually re-read.

## Pending source selections (field level; `source_selection.PENDING` / `PENDING_FIELDS`)

| Product | Fields | Reason |
|---|---|---|
| NESTE_NEXBASE_3043 / 3050 / 3060 / 3080 | 15 fields (densities; some KV40, KV100, VI, flash, pour, Noack) | family TDS DL2-10962 (Edition 8) vs individual sheets; both undated |
| PETRONAS_ETRO_4 | KV100, VI, CCS | PDS DL2-10230 vs DL2-12475 ETRO 4 column; both undated (conflict EVR-2026-11-10-ETRO4) |
| ARAMCO_LUBEREF_PRIMA_110 / 230 / 500 | density | spec DL2-12172 (no unit) vs brochure DL2-11773 (Kg/L); the brochure marks 110/230 typicals as provisional; for 230 the external Aramco sheet prints a third value, 0.8635 kg/L (conflict EVR-2026-11-11-230-density-external) |
| LUBRIZOL_CV2301 | flash point | the technical document prints 158 and 165 °C PMCC |
| FORMOSA_150N_GII_PLUS / 500N_GII | KV40, specific gravity | SDS fallback source names "150N/500N Base oil" without the grade (identity) |
| RICHFUL_RF6066 | density, KV100, TBN, Zn, Ca | two undated TDS disagree |
| RICHFUL_RF6069 | KV100 | supplier web page (142) vs archived TDS (118) |
| AFTON_HITEC_8788B | KV40, KV100, density, flash point | external PDS (Internet Archive) could not be obtained on 2026-11-11; whether it prints these values is unknown |

**No longer pending (2026-11-11):** S_OIL_ARAMCO_ULTRA_8 KV40, KV100 and flash point. The S-OIL manufacturer-table typicals are selected; the SDS ranges are alternates; the KV40 disagreement stays an unresolved conflict; the edition date of the page is unknown (`recommendation_aramcoULTRA8_source_selection.md`).

## Remaining gaps

See [evidence_review.md](evidence_review.md), section 7. In short:
- values not printed for the grade;
- values lacking a required condition;
- inconsistent labels or units;
- provisional supplier typicals;
- unestablished identity;
- conflicting undated technical documents;
- **8 external-source cases without a copy** (Afton HiTEC 12204L and 8788B PDSs): the Internet Archive refused automated download; a manual download matching the registry SHA-256 would allow the review;
- open points on external evidence: the unresolved aramcoULTRA 8 KV40 conflict, the unknown edition date of the S-OIL page, and the distributor-issued flyer for BAPbase 4; separately, the merge question ID-01.

**The TDS–SDS check is not exhaustive.** It covers every pair in the audit, `conflicts[]`, `alternate_entries` and the reviewed SDS values, within the archive's text layers and the renders read.
