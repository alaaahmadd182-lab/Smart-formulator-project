# Change log, 2026-11-10 (Workstream A)

Baseline: `f4d97e71f72598df601b72403775581c34061ad1`. Every change below can be reproduced with the commands in
[HANDOFF.md](HANDOFF.md).

## Product data (Rule 1, source selection)

The full per-field list, with before and after values, sources and printed evidence, is in
[reports/data_policy/source_selection_changes.csv](../../reports/data_policy/source_selection_changes.csv) (28 rows).

| Product (file) | Field | Before (source) | After (source) |
|---|---|---|---|
| INFINEUM_D3424 (tier 2) | flash_point | > 110 °C, SDS bound (DL2-10204 p.6) | 190 °C PMCC, ASTM D 93 (DL2-10204 p.1, TDS 2004-11-09) |
| RICHFUL RF6066 / 6069 / 6077 / 6078 / 6079 / 6088 / 6088F / 6400 / 6406 (tier 2) | flash_point | ≥ 180 or ≮ 180 °C, SDS bound | TDS typical 220 / 216 / 210 / 220 / 214 / 203 / 218 / 226 / 223 °C (COC, ASTM D92) |
| RICHFUL RF6069 / 6077 / 6079 / 6088 / 6400 / 6406 (tier 2) | density | SDS value | TDS typical at 20 °C: 981 / 998 / 1000 / 955 / 1039 / 1060 kg/m³ (the index range is kept in min/max) |
| RICHFUL RF6077 / 6078 / 6079 / 6088 / 6088F / 6400 / 6406 (tier 2) | kv100 | SDS value | TDS typical: 160 / 146 / 140 / 100 / 177 / 109 / 72 mm²/s |
| NESTE_NEXBASE_3020 (tier 1) | kv40, kv100, density | 7.5 (SDS); Missing; Missing | 7.5 / 2.2 mm²/s; 834 kg/m³ at 15 °C (DL2-10962.pdf, Edition 8) |
| NESTE_NEXBASE_3020 (tier 2) | pour_point, flash_point | ≤ −42 °C; > 150 °C (SDS bounds) | −45 °C; 160 °C (DL2-10962.pdf) |
| NESTE_NEXBASE_3020 (tiers 1–3) | product.source_file, document_type | SDS files only | DL2-10962.pdf added; "Safety Data Sheet; Technical Data Sheet" |

How each replaced value was handled:
- The replaced value is kept in `alternate_entries[]` with a `selection_note`.
- Its old value kind is relabelled as a lower or upper bound where it was printed as one. The previous label is kept in `value_kind_previous_label`.
- `*_final` keys are derived for the changed nodes by the same function that `integrate_products.py` uses.

Conflicts and open questions:
- **Reopened** (`resolved: false`): RICHFUL_RF6077 `tier2.density` and `tier2.kv100`, and RICHFUL_RF6088F `tier2.kv100`. Their 2026-10-18 user decisions are superseded by the policy and await the user's confirmation.
- **Notes appended**: conflict notes on D3424 flash point, RF6077 density/kv100 and RF6088F kv100.
- **Open questions**: two NEXBASE 3020 open questions are annotated with dated corrections. The record wrongly said that no TDS exists.

## Scripts

- `integrate_products.py`:
  - docstring rule 2 replaced (the old text is kept in parentheses);
  - the RF6077 density/kv100 and RF6088F kv100 `ANNOTATIONS` are re-pinned to the new values with new notes;
  - the matching `CONFLICTS` rules set `False` with the basis "source-selection policy 2026-11-10".
  - Dry run: no errors, 10/10 annotations, 16/16 conflict rules.
- New, under `tools/data_policy/`: `policy_lib.py`, `document_classes.py`, `tds_candidates.py`, `source_selection.py`, `integration_diff.py`, `tds_sds_inventory.py`, `thresholds.py` and `tests/`.
- New, under `tools/mandatory_properties/`: `requirements.py` and `build_eligibility.py`.

## Generated outputs

- `Coverage_Matrix.xlsx` (regenerated):
  - Base Oils: reported +2 and missing −2 (NEXBASE 3020 kv100 and density);
  - Status Detail: 6320 → 6346 rows (the new alternate entries);
  - Validation Issues: unchanged (30).
- `reports/data_policy/document_classes.csv`, `source_selection_changes.csv`, `tds_sds_comparisons.csv`.
- `reports/mandatory_properties/product_eligibility.csv`, `missing_mandatory_properties.csv` / `.md`.

## Documentation

- `CLAUDE.md`, `README.md`, `PROJECT_FILE_GUIDE.md`, `tools/README.md` and `requirements.txt` are updated.
- `open_questions_and_conflicts.md` has a new dated section at the end. Earlier sections, including the 2026-10-24 integration review, are historical and unchanged.

## Not changed

- The v5 audit (`reconciliation/comprehensive_conflicts_audit.md` / `.csv`, `findings_v5.json`) is a historical snapshot.
- No finding has been reclassified (Rule 2 review checkpoint).
- The archive, evidence copies, templates and glossary are unchanged.
