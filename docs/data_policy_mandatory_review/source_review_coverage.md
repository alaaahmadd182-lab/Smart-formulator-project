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
| pending (identity, conflicting technical documents, reliability) | 37 | 19 |
| external (URL) source selected (all reviewed: see `external_review.csv`) | 22 | 14 |
| Missing, no associated document mentions the property | 457 | 183 |
| Missing, a document mentions the property (all reviewed: see `lead_review.csv`) | 154 | 86 |
| Missing, image-only associated document (all read on renders) | 67 | 29 |
| SDS selected although a technical page mentions the property | 0 | 0 |

| Comparison status (current data) | Rows |
|---|---:|
| a TDS–SDS pair exists in the inventory (comparable, unknown, bound check, not comparable) | 129 |
| both document classes mention the property but no pair: reviewed as unrelated, insufficient or unresolved identity (`lead_review.csv`) | 38 |
| not possible: only one document class, or no searchable document, mentions the property | 2,008 |

The TDS–SDS inventory (`tds_sds_comparisons.csv`) has 141 rows. 71 of them come from SDS values recorded in this review (70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs).

## Review state (`source_review_status.csv`; counting unit: ledger row)

| Review state | Rows | Mandatory |
|---|---:|---:|
| completed archive lead review (usable 81, already recorded 31, unrelated mention 71) | 183 | 61 |
| completed external-source review (confirmed on an identified copy) | 21 | 16 |
| evidence unavailable: the archive documents do not print the value (173), or no copy of the external source could be obtained (8) | 181 | 81 |
| evidence inconclusive: document identity not established | 7 | 2 |
| not individually reviewed: the state rests on the mechanical classification only | 1,783 | 745 |
| **Total** | **2,175** | **905** |

A recorded outcome for every one of the 363 frozen lead cases and the 29 external cases does **not** mean that all source verification is complete. 188 reviewed rows end without usable evidence, and 1,783 rows were never individually re-read.

## Pending source selections (field level; `source_selection.PENDING` / `PENDING_FIELDS`)

| Product | Fields | Reason |
|---|---|---|
| NESTE_NEXBASE_3043 / 3050 / 3060 / 3080 | 15 fields (densities; some KV40, KV100, VI, flash, pour, Noack) | family TDS DL2-10962 (Edition 8) vs individual sheets; both undated |
| PETRONAS_ETRO_4 | KV100, VI, CCS | PDS DL2-10230 vs DL2-12475 ETRO 4 column; both undated (conflict EVR-2026-11-10-ETRO4) |
| ARAMCO_LUBEREF_PRIMA_110 / 230 / 500 | density | spec DL2-12172 (no unit) vs brochure DL2-11773 (Kg/L); the brochure marks 110/230 typicals as provisional; for 230 the external Aramco sheet prints a third value, 0.8635 kg/L (conflict EVR-2026-11-11-230-density-external) |
| LUBRIZOL_CV2301 | flash point | the technical document prints 158 and 165 °C PMCC |
| FORMOSA_150N_GII_PLUS / 500N_GII | KV40, specific gravity | SDS fallback source names "150N/500N Base oil" without the grade (identity) |
| S_OIL_ARAMCO_ULTRA_8 | KV40, KV100, flash point | external S-OIL web table (values confirmed on the saved copies, 2026-11-11) vs archived SDS ranges: a policy decision on external technical sources; KV40 typical 41.10 lies below the SDS range (unresolved conflict from the 2026-10 audit); identity question ID-01 |
| RICHFUL_RF6066 | density, KV100, TBN, Zn, Ca | two undated TDS disagree |
| RICHFUL_RF6069 | KV100 | supplier web page (142) vs archived TDS (118) |
| AFTON_HITEC_8788B | KV40, KV100, density, flash point | external PDS (Internet Archive) could not be obtained on 2026-11-11; whether it prints these values is unknown |

## Remaining gaps

See [evidence_review.md](evidence_review.md), section 7. In short:
- values not printed for the grade;
- values lacking a required condition;
- inconsistent labels or units;
- provisional supplier typicals;
- unestablished identity;
- conflicting undated technical documents;
- **8 external-source cases without a copy** (Afton HiTEC 12204L and 8788B PDSs): the Internet Archive refused automated download; a manual download matching the registry SHA-256 would allow the review;
- external technical pages vs archived SDSs (a policy decision).

**The TDS–SDS check is not exhaustive.** It covers every pair in the audit, `conflicts[]`, `alternate_entries` and the reviewed SDS values, within the archive's text layers and the renders read.
