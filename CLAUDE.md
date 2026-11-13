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
build_coverage_matrix.py           Builds the coverage matrix (Task 4) from the Products_json folder
integrate_products.py              Adds normalised *_final keys and conflict annotations (under review)
build_conflicts_report.py          Generates a Task 5 conflicts report from the JSON (under review)
source_registry.json               External (non-archive) sources cited in Products_json, with verification status
reconciliation/                    Task 3 identity review and inventory reconciliation
tools/data_policy/                 Source selection (Rule 1), TDS–SDS comparison inventory and proposed thresholds (Rule 2), tests
tools/mandatory_properties/        Mandatory Tier 1 requirements and the eligibility build (Rule 3)
reports/                           Generated outputs of the two tool folders above
docs/data_policy_mandatory_review/ Policy, threshold proposal, eligibility interface, change log, HANDOFF
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
- When documents disagree, record it in `conflicts` (both values, both sources) and do not silently resolve it.
- Data rules approved 2026-10-24 (rule 2 replaced on 2026-11-10):
  1. Never automatically average conflicting datasheet values. Keep both values and their sources; leave the conflict unresolved unless authoritative evidence supports a resolution.
  2. **Source selection (2026-11-10):** select the applicable technical-document value (TDS, PDS, bulletin, specification sheet; classified by purpose and content per page, not by file name); if no technical document gives the property, select the applicable SDS value. Keep the selected value's printed text, unit, qualifier, method, conditions, source, page and revision; keep the other value in `alternate_entries[]` and keep the conflict entry. Selecting the TDS is not a finding that the SDS is wrong, and does not resolve the conflict. Record an exception (unreadable, inconsistent, demonstrably erroneous TDS value, or one lacking a required condition such as a density temperature) instead of selecting a known error. Do not call an SDS bound a "safety margin" unless its wording says so. Edition rule: newest dated edition of the same product/grade/region; undated disagreeing editions stay pending. Full policy: `docs/data_policy_mandatory_review/source_selection_policy.md`; tool: `tools/data_policy/source_selection.py`. (Rule 2 of 2026-10-24, "never automatically prefer TDS over SDS or vice versa", is superseded.)
  3. The coverage matrix reflects the validated `status` of the selected property; never substitute `status_final` for `status`.
- A source-selection change never makes incomplete or unknown evidence count as verified; keep the unresolved-evidence distinction of the v5 audit.
- TDS–SDS screening thresholds (Rule 2) are **proposed, not approved** (`tools/data_policy/thresholds.py`, `APPROVAL = 'proposed'`); do not reclassify findings with them until approved. They are empirical project screening choices, not technical tolerances: say "below the proposed review threshold", never "ordinary"; a point inside a bound is only "logically compatible", not agreement.
- A technical specification range or bound can be the selected value: select it as printed, never convert it to a single value, and keep the SDS typical as an alternate. A pending source selection needs an explicit reason (identity, applicability, conflicting editions, reliability); a different value kind alone is not one.
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
- Usage: `python build_coverage_matrix.py --output Coverage_Matrix_new.xlsx` (options `--input`, default `Products_json`; `--sources`, default `source_registry.json`; `--overwrite`). Uses `openpyxl` (`requirements.txt`).
- It reads the `Products_json` folder directly and reports per-product, per-property status, expected tiers, and "Validation Issues", "Status Detail" and "Traceability Audit" sheets. It never changes the input JSON.

## integrate_products.py and build_conflicts_report.py
- See README "Data integration". `integrate_products.py` is a dry run unless `--write` is given, and writes nothing if any check fails. Test a run on a temporary copy of `Products_json` before running it on the repository.
- Its `*_final` keys are derived, informational data; a value object whose original keys change must have its `*_final` keys removed or re-derived (the script re-derives them on every run).
- Its `ANNOTATIONS` may carry only a reviewed `resolution` note pinned to the field values in `expect`; `CONFLICTS` rules may mark an entry resolved only on a basis in `RESOLVING_BASES`. Never add averaged values or document-type preferences.
- `build_conflicts_report.py` writes `conflicts_report_generated.md` and refuses to write `open_questions_and_conflicts.md`, which is curated by hand.
- Status vocabulary: the templates also define `Not Applicable` (the property does not apply to this product type), used by LUBRIZOL_CV6320.
- Never run `integrate_products.py --write` on the whole repository (a dry run would change 229 files that are deliberately not re-derived). For changed records use `tools/data_policy/integration_diff.py`.

## Mandatory Tier 1 eligibility (2026-11-10)
- `python tools/mandatory_properties/build_eligibility.py` writes `reports/mandatory_properties/product_eligibility.csv` (interface for Workstream B: `docs/data_policy_mandatory_review/eligibility_interface.md`) and the missing-properties CSV/MD; `--check` writes nothing. Regenerate after any product JSON change (the rows carry a snapshot hash of `Products_json`).
- `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied under the requirements version (version `.6`; the meaning is unchanged since `.3`); documented-but-unusable information is reported only in `documentation_coverage.csv`. A product missing any mandatory Tier 1 requirement is not formulation-eligible but stays in the database. Tier 2/3 gaps never block (the VM/PPD subtype blocks are tier 2/3 files: reported, not blocking). `Not Required` / `Not Applicable` satisfy a requirement only under an approved applicability rule; a calculated value only through a registered check that reproduces it from inputs printed on the cited page. "Eligible" is not a statement of chemical suitability.
- A keyword mention in a document is only a lead. Evidence review: `tools/data_policy/lead_review.py` (decisions in `lead_review_decisions.json`, one rule per document group with what was read); name-match document links must be reviewed (`association_review.py`) before their evidence is used. Values from external (URL) sources are reviewed in `external_review.py` (decisions and evidence hashes in `external_review_decisions.json`); an external source that cannot be obtained is "inconclusive", never confirmed. External evidence is admissible, with no blanket rule for or against it: assess each source separately on authority (manufacturer vs distributor), authenticity, exact product identity, applicability and provenance; never accept a distributor description automatically, and keep two questions apart: whether a source names the record's exact grade, and whether two records should be merged (ID-01, aramcoULTRA 8 vs Ultra-S 8: open, never resolved as a side effect, and not a restriction on a source that names the grade). Fill a Missing field only from exact product-specific printed evidence, declared in `source_selection.py` with its expected current state.
- Every requirement outcome has a category (absent, bound/range needing assessment, missing unit/condition/provenance, invalid value, unreproducible calculation, unresolved applicability, unresolved source selection). Do not call every unmet requirement "missing". Authority and open decisions: `docs/data_policy_mandatory_review/requirements_review.md`. Build order: `tds_sds_inventory.py` → `source_coverage_ledger.py` → `build_eligibility.py` (the build stops on a stale ledger).
- Policies approved 2026-11-11 (`requirements_review.md` §4a): (1) a valid sourced range or bound is documented evidence, never absent, never replaced by a point or midpoint, and not enough where a point is required; (2) co-components: completeness is per evidenced route (`co_component_route_evidence.json`); every requirement of the route needs a usable dose and the route's requirement list must be confirmed by source review; one usable component never completes a route; keep independent routes separate; never map a route from role text, and report an unestablished association as not assessed; route evidence is bound to the complete records by fingerprint (`record_fingerprint`), so after changing a bound record re-review the route instead of refreshing its hash; a component may belong to several routes; never treat a list as exhaustive because it names some components; "none required" needs an explicit reviewed assessment (product, meaning, unconditional, qualification verbatim, scope, conditions) in `co_component_statements.json`, a missing field proves nothing, and free text never counts; (3) percentage basis is mass, volume or unspecified, from the unit or reviewed evidence; never use an unspecified or volume "%" as wt.%; no conversion is registered (`volume_to_mass_percent` is unused code), and volume evidence never fills a wt.% field (`volume_dose_evidence.csv`); (4) N/A needs a rule approved for the product class, requirement and task (`APPROVED_APPLICABILITY_RULES`, empty); Missing or "not found" is never N/A; never move a property between tiers.
- Keep evidence documentation, value selection, value form, percentage basis and verification status apart (`build_readiness.py`, `property_attributes.csv`). Take the selection status from the source-selection ledger, never from the outcome category: a value can have a metadata defect and a pending selection at once. A pending selection is documented evidence but blocks any use that needs a selected value.
- Evidence wording: "not recorded" (the record), "not found in the inspected text/pages" (a search, with what was inspected), "source unavailable / not inspected" and "confirmed by source review" are four different statements. Never infer supplier silence from an empty JSON field, and keep supplier qualifications ("should be needed") as printed. Never add a general "calculation ready" label: state readiness only against a named, registered calculation. The attribute files are not the association-mining feature inventory.
- After a rule or data change, run `compare_eligibility.py` against a saved baseline and explain every change; never require results to stay identical, and never change the meaning of `tier1_complete` / `formulation_eligible` without a new version and a note.
- Line endings: this machine checks files out with CRLF (`core.autocrlf=true`, system config), while product JSON is committed with LF. The eligibility fingerprint is over exact checkout bytes: regenerate in each checkout and never bypass a mismatch. Verify preserved files and evidence with `python tools/data_policy/verify_preserved.py` (form-aware), not a bare `sha256sum -c` in a CRLF checkout.
- Whenever a technical value and an SDS value exist for the same product and property, the pair belongs in the comparison inventory, also when the technical source is a registered external URL (`tds_sds_inventory.py`). Account for every external-sourced value with `external_comparison_accounting.py` (paired, or why not). A source that could not be obtained is unresolved, never verified. The inventory never selects a source or resolves a disagreement.
- Before regenerating reports for a new task, save the current reports and test results under `docs/data_policy_mandatory_review/baselines/`; freeze a reviewed state with `python tools/data_policy/make_review_snapshot.py --name <name>` (never overwritten; `--verify` checks it).
- Run every check with `python tools/data_policy/run_checks.py` (separate subprocesses, real return codes, full output saved in `docs/data_policy_mandatory_review/test_results/`). Never pipe a check through a filter when its return code matters.

## Historical generators (do not run against the current data)
- `tools/corrections_2026-10-31/`, `tools/integration_2026-10-24/`, `tools/audit/original_2026-10-27_to_30/` and `tools/audit/review_2026-11-02/` (report generators) rebuild superseded values or the v5 audit snapshot; several hard-code the main checkout path. See `docs/data_policy_mandatory_review/implementation_plan.md`, section 1.
- Workstream B (association mining) owns `analysis/association_mining/`; do not edit it from this workstream.

## Working conventions
- Environment: Windows, VS Code, Python 3.
- Workflow: planning/review happens in the Claude desktop app; implementation in Claude Code (VS Code). Plans may be saved in `docs/plan.md` — read it when asked to "implement the plan".
- Keep changes small and commit with clear messages. Don't commit large generated files or new ZIPs without asking.
- After editing any product JSON, check it is valid JSON and that `status` values are from the allowed list.
