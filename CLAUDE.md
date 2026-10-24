# CLAUDE.md — Smart Formulator Project

## What this project is
Final-year project (FYP): a **Smart Formulator** for lubricant (engine oil) blending.
The current stage is building a **structured, source-traceable raw-material database** as JSON:
base oils, additive packages and additive components, each extracted from supplier
documents (TDS, SDS, product bulletins, spec sheets). Later stages use this data to build
and check formulations (recipes).

Git remote: `https://github.com/alaaahmadd182-lab/Smart-formulator-project.git` (branch `main`).

## Folder layout
```
json_templates/          Empty JSON templates (template_version 1.0), one per class + tier
Products_json/
  Base_oils_json/<SUPPLIER>/<PRODUCT_ID>/          3 tiers per product
  Additive_packages_json/<Supplier>/<PRODUCT_ID>/  2 tiers per product
  Additive_components_json/<Supplier>/<ID>/        general.json (+ subtype file e.g. vm.json, ppd.json)
build_coverage_matrix.py           Builds the coverage matrix (Task 4) from a ZIP of Products_json
Coverage_Matrix.xlsx               Output of the script above
open_questions_and_conflicts.md    Collected open_questions + conflicts from every product JSON
Property_Glossary.docx             Definitions of every property/field
Raw_Material_Missing_Properties_2026-10-13.xlsx   Missing-property report
Manual + Data to share.zip         Source documents (PDF/JPG datasheets, ~90 MB) — do not modify
```

## Material classes and tiers
| material_class | Tiers | Template files |
|---|---|---|
| `base_oil` | 1 Blocking (api_group_chemistry, kv40, kv100, viscosity_index, density, ccs), 2 Verification, 3 Substitution | `base_oil_tier{1,2,3}_*.json` |
| `additive_package` | 1 Route-defining (package type, performance claims, SAE grades, permitted base oils, treat-rate matrix, co-components, published formulations), 2 Numeric contribution (TBN, ash, elements, density, pour point…) | `additive_package_tier{1,2}_*.json` |
| `additive_component` | 1 General block (+ subtype block: VM, PPD) | `additive_component_*.json` |

## JSON rules (follow these strictly)
- Every file has: `template_version`, `material_class`, `tier`, `tier_label`, `record_id`, `product{}`, `fields{}`, `open_questions[]`, `conflicts[]`. Product files (v1.1) also have `source_documents[]`.
- Every numeric property uses the same value object:
  `value, qualifier, min, max, value_kind, printed_text, unit, test_temperature_c, method, status, calculation_note, source{file, page, revision_date}` (+ optional `notes`, `basis`, `alternate_entries`).
- `status` must be one of: **`Reported`**, **`Calculated`**, **`Missing`**, **`Not Required`** / `N/A`. Anything else is flagged by the coverage script.
- **Never invent or infer values.** If a value is not printed in a source document, leave `value: null` and `status: "Missing"`, and explain in `open_questions`.
- Every non-missing value must cite its `source` (file + page). Keep `printed_text` exactly as printed and keep the printed unit.
- If something comes from general knowledge (not the document), set `basis: "general_knowledge"` and say so in `notes`.
- When documents disagree, record it in `conflicts` (both values, both sources), use the newer document in `fields`, and do not silently resolve it.
- Component shares from an SDS (e.g. "ZDDP 10–15 %") are **not** element contents — do not put them in Zn/P/Ca fields.
- Do not edit the source documents or the templates when filling product data.

## Known inconsistencies (be careful)
- File naming is not uniform:
  - most base oils: `<ID>__base_oil_tier1_blocking.json`, `..._tier2_verification.json`, `..._tier3_substitution.json`
  - CALTEX and ERGON base oils: `<ID>_tier1.json`, `_tier2.json`, `_tier3.json`
  - additive packages: `tier1_route_defining.json`, `tier2_numeric_contribution.json`
  - additive components: `general.json`, `vm.json`, …
  Code that reads files should rely on the `material_class` and `tier` keys inside the JSON, not on file names.
- Templates are `template_version` 1.0; product files are 1.1 (extra `source_documents`, `notes`, `basis`, `alternate_entries`).
- Folder names contain spaces and punctuation (e.g. `KangTai . Lubricant Addtives`, `JINZHOU DONGGONG PETROCHEMICAL PRODUCTS CO., LTD`). Always quote paths.

## build_coverage_matrix.py
- Usage: `python build_coverage_matrix.py <Products_json.zip> <output.xlsx>`
- Input is a **ZIP** of `Products_json`, not the folder itself.
- It imports `artifact_tool` (a tool from Claude's sandbox, not a pip package). To run it locally, replace it with `openpyxl`.
- It reports per-product, per-property status, expected tiers, and a "Validation Issues" sheet. It never changes the input JSON.

## Working conventions
- Environment: Windows, VS Code, Python 3.
- Workflow: planning/review happens in the Claude desktop app; implementation in Claude Code (VS Code). Plans may be saved in `docs/plan.md` — read it when asked to "implement the plan".
- Keep changes small and commit with clear messages. Don't commit large generated files or new ZIPs without asking.
- After editing any product JSON, check it is valid JSON and that `status` values are from the allowed list.
