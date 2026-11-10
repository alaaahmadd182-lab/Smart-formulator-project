# Source-selection policy (Rule 1), 2026-11-10

This policy replaces data rule 2 of 2026-10-24 ("TDS is never preferred over SDS automatically, nor the reverse"). Data rules 1 (never
average) and 3 (the coverage matrix uses `status`, never `status_final`) are unchanged.

- Implementation: [tools/data_policy/source_selection.py](../../tools/data_policy/source_selection.py). It is a dry run unless `--write` is given; it is idempotent, and it checks the expected current value and source before it changes anything.
- Change list: [reports/data_policy/source_selection_changes.csv](../../reports/data_policy/source_selection_changes.csv) (28 field selections).
- Document classes: [reports/data_policy/document_classes.csv](../../reports/data_policy/document_classes.csv), from [tools/data_policy/document_classes.py](../../tools/data_policy/document_classes.py).

## 1. The rule

1. **Technical document first.** For each property, the value from the applicable technical document (TDS, PDS, bulletin, specification sheet; see section 2) is selected when that document provides the property for the same product, grade and conditions.
2. **SDS fallback.** If no technical document provides the property, the applicable SDS value is selected.
3. **Provenance is kept.** The selected value keeps its exact printed text, unit, qualifier, value kind, method, conditions, source file, page and revision date.
4. **Alternates are kept.** The previously selected or other-class value is moved to `alternate_entries[]` with a `selection_note`, and every conflict entry stays in `conflicts[]`. An SDS bound is recorded as a lower or upper bound. It is called a "safety margin" only if its own wording says so, and no current SDS wording does.
5. **Selection is not a verdict.** Choosing the TDS value does not establish that the SDS value is wrong. Conflicts that a user decision had marked resolved are reopened (`resolved: false`), because the selection does not resolve them.
6. **Exceptions.** The TDS value is not selected when it is unreadable, internally inconsistent, demonstrably erroneous, or lacks a condition that the property definition requires (for example, a density with no reference temperature). Each exception is recorded with its reason (section 4). A known error is never silently selected.
7. **Ranges and bounds (clarified 2026-11-10).** A technical specification range or bound can be the selected information. It is selected as printed and never converted to a single value. The SDS typical value is kept as an alternate.
   - A different value kind alone is not a reason to keep the SDS.
   - Whether a range or bound is usable for a calculation is assessed separately, under the mandatory-property rules (category `bound_or_range_needs_assessment`).
   - Genuine identity, applicability, conflicting-edition or source-reliability problems stay pending, with their reasons.

The SDS is inspected when both document types give the property: [tools/data_policy/tds_candidates.py](../../tools/data_policy/tds_candidates.py) prints the technical-document lines for every SDS-sourced selected value.

Coverage is recorded per product and property in [reports/data_policy/source_coverage_ledger.csv](../../reports/data_policy/source_coverage_ledger.csv), for technical- and SDS-selected values alike. The remaining gaps are listed in [source_review_coverage.md](source_review_coverage.md). **The check is not exhaustive.**

## 2. Document classes: purpose and content, not file name

Each cited (file, page) pair is classified separately, because some files combine a TDS and an SDS (for example DL2-10204.pdf: p.1 TDS, p.6 SDS).

| Class | Sub-class | Recognised by (text of the page) |
|---|---|---|
| SDS | — | A safety-data-sheet heading (SDS, MSDS, "Safety Data Sheet", GHS/REACH section structure), or a continuation page of such a file that has no technical heading of its own. |
| TECHNICAL | tds | A technical / product data sheet heading ("Technical Data Sheet", "Product Data Sheet", "Typical properties / characteristics"). |
| TECHNICAL | specification | A specification table with limit columns (min / max, "Specification", "Limits"). |
| TECHNICAL | bulletin | A product bulletin or technical bulletin, or an additive-package brochure with a dosage table. |
| TECHNICAL | catalog | A multi-product catalogue table. |
| COA | — | A certificate of analysis (batch result). None is cited by a selected value. |
| EXTERNAL | — | A URL source (supplier web page, Internet Archive copy), handled through `source_registry.json`. |

How the classification was established and checked:
- 20 image-only or text-less files were classified by reading their renders (the `MANUAL` table in `document_classes.py`).
- Result: 506 cited (file, page) pairs. TECHNICAL 248, SDS 223, EXTERNAL 35, UNKNOWN 0.
- The classification agrees with all 231 document-type labels in the v5 audit findings (192 TECHNICAL, 39 SDS).

A **PDS** (Afton "Product Data Sheet") and a **technical bulletin** are technical documents. A **specification sheet** is a
technical document of value kind "specification" (limits), and rule 7 applies to it.

## 3. Multiple technical editions

- **The newest dated edition is selected** if the editions are for the same product, grade, region and formulation, with the same conditions.
- **Undated editions** that print the same value are interchangeable. Undated editions that disagree are a TDS–TDS conflict: no edition is chosen, and the case is pending (RICHFUL_RF6066, NEXBASE 3043–3080).
- **Product identity is checked first.** Unrelated grades, regions or formulations are not mixed. For example, the FPCC GII table columns and FORMOSA 150N/500N (identity question ID-15) stay separate.
- **A current supplier web page** that is cited for a field is listed. It is not replaced automatically by an archived edition (RICHFUL_RF6069 kv100 is pending).

## 4. Outcome of the review (2026-11-10)

The review covered 130 selected values that came from SDS pages.

| Outcome | Count | Fields |
|---|---:|---|
| **Switched to the technical value** | 30 | Flash point: RF6066, RF6069, RF6077, RF6078, RF6079, RF6088, RF6088F, RF6400, RF6406 (the TDS typical replaces the SDS lower bound ≥/≮ 180 °C) and INFINEUM_D3424 (TDS PMCC 190 °C replaces SDS > 110 °C).<br>Density at 20 °C: RF6069, RF6077, RF6079, RF6088, RF6400, RF6406.<br>KV100: RF6077, RF6078, RF6079, RF6088, RF6088F, RF6400, RF6406.<br>NESTE_NEXBASE_3020 (TDS DL2-10962.pdf Edition 8, image): kv40, kv100 and density, which were Missing before (kv100, density), plus pour point and flash point.<br>FORMOSA_150N_GII_PLUS and FORMOSA_500N_GII KV100: the specification range (DL2-10001 / DL2-10003, 2009-10-21, Min./Max. 5.0–5.4 and 10–12 mm²/s) is selected as printed. The SDS typical values (5.2, 11 cSt) are kept as alternates with their exact SDS lines. The old record had mixed the specification range into the SDS entry. |
| SDS fallback confirmed | — | No technical document provides the property. This covers SDS-only packages and base oils, specific gravity where the TDS gives only a density, CAS chemistry names, and component carrier and active shares (full list in `SDS_FALLBACK_CONFIRMED`). Field-level reviewed fallbacks are in `SDS_FALLBACK_FIELDS`: FORMOSA KV40 and specific gravity (the specification prints "Report"), and INFINEUM_D3384 specific gravity (the technical sheet gives none). |
| Exception (SDS kept) | 2 | PETRONAS_ETRO_6_PLUS density (TDS 0.8429 kg/L with no temperature); AFTON_HITEC_12210M density (bulletin 7.90 lbs/gal with no temperature). |
| Pending (not changed) | 6 groups (field level in `PENDING_FIELDS`) | RICHFUL_RF6066 (two undated TDS); RICHFUL_RF6069 kv100 (web page vs archived TDS); S_OIL_ARAMCO_ULTRA_8 (external web table vs SDS ranges); AFTON_HITEC_8788B (external PDS not reviewed); NEXBASE 3043–3080: the family TDS ed. 8 and the individual sheets disagree on the 15 fields listed in [source_review_coverage.md](source_review_coverage.md). Fields on which they agree are not pending. |

**Superseded user decisions.** The user decisions of 2026-10-18 for RICHFUL_RF6077 density and kv100, and for RICHFUL_RF6088F kv100, kept the SDS values. Under this policy the TDS values are selected:
- RF6077: 998 kg/m³ at 20 °C, and 160 mm²/s;
- RF6088F: 177 mm²/s.

The SDS values stay as alternates, and the three conflicts are reopened. **This supersession needs the user's confirmation** (HANDOFF).

## 5. What the policy does not do

- It does not mark any value as verified. The unresolved-evidence distinction of the v5 audit (verified, text presence only, unresolved, not consulted) is unchanged.
- It does not change `status`, which stays `Reported`. It does not change the original source documents, the templates or the historical audit.
- It does not resolve TDS–SDS conflicts. Screening of ordinary differences is Rule 2, and its thresholds await review ([threshold_proposal.md](threshold_proposal.md)).
