# Product eligibility interface (Workstream A → Workstream B)

**File.** `reports/mandatory_properties/product_eligibility.csv`.
- Generate it with `python tools/mandatory_properties/build_eligibility.py`.
- Check it without writing with `--check`.
- The build needs a current coverage ledger (`python tools/data_policy/source_coverage_ledger.py`). It stops with exit 3 if the ledger was built from different data.

**Meaning.** `tier1_complete = true` and `formulation_eligible = true` both mean only one thing: all mandatory Tier 1 requirements are satisfied under `requirements_version`.
- It is not a statement of chemical suitability, compatibility or performance.
- Products that are not eligible stay in the database with all their data.
- Four policies were approved on 2026-11-11 (ranges and bounds, co-components, percentage basis, applicability; `requirements_review.md` §4a). The remaining interpretations are provisional.

## Published state (2026-11-13, on `main`)

- **Published for the Part B handoff** with HANDOFF revision 4 (see [HANDOFF.md](HANDOFF.md) section 0).
  `requirements_version` is `mandatory-tier1-2026-11-10.6`. In the published data, 11 of 264 products are
  `formulation_eligible`:
  - all are base oils;
  - 0 of 78 packages;
  - 0 of 5 components.
- **Provisional.** Only Rule 1 and the four policies of 2026-11-11 are approved. The Rule 2 thresholds and interpretations
  I-2 to I-5 and I-7 are proposed and not applied, and no applicability rule is approved. Treat the file as a checkpoint of
  provisional rules, not a final classification.
- **Freshness.** After pulling, run `python tools/data_policy/run_checks.py` (or at least the build order in HANDOFF section 7).
  Then confirm `python tools/mandatory_properties/build_eligibility.py --check` reports up to date. Consume only a file whose
  `source_snapshot_sha256` equals your own checkout's exact-byte fingerprint (see `source_snapshot_sha256` below).
- **What Part B should consume.** This file, plus `requirement_outcomes.csv` and `documentation_coverage.csv`. The attribute
  files are optional companions and not a feature inventory.
- **What this interface does not cover.** New-dataset ingestion ("Downloaded lubricants sheets") is a separate, ongoing task
  and is not reflected here. When it changes `Products_json`, the fingerprint changes and this file must be rebuilt.

## Format

UTF-8, comma-separated, RFC 4180 quoting, `\n` line ends, one header row, one row per product folder, sorted by `product_id`. The columns are unchanged since the first version.

| Column | Type | Content |
|---|---|---|
| `product_id` | string | The stable id: the product folder name in `Products_json`. |
| `material_class` | enum | `base_oil`, `additive_package`, `additive_component`. |
| `product_name`, `supplier` | string | From `product{}` of the Tier 1 (or component `general`) file. |
| `tier1_complete` | `true`/`false` | All mandatory Tier 1 requirements are **satisfied** under `requirements_version`: each is met, or not applicable under an approved rule (none approved yet). A range or bound awaiting a use decision, a pending source selection, or unresolved applicability is **not** complete. Documentation coverage is reported separately (`documentation_coverage.csv`). |
| `formulation_eligible` | `true`/`false` | Same value as `tier1_complete`. No other eligibility gate exists; a new gate would need a documented authority (`requirements_review.md`) and a new version. |
| `missing_mandatory_properties` | JSON array of strings | Ids of blocking requirements that are **not met**, whatever the reason. Not every id is an absent property: the category of each one is in `eligibility_reasons` and in `requirement_outcomes.csv`. |
| `eligibility_reasons` | JSON array of strings | One entry per unmet blocking requirement, as `"<id> [<category>]: <reason>"`. Then notes: non-blocking subtype gaps, and warnings about unresolved conflicts on satisfied properties. For an eligible product the first entry states the rule version. |
| `calculated_mandatory_properties` | JSON array of strings | Blocking requirements met by a `Calculated` value that a registered check reproduced from inputs printed on the cited page. None at present. |
| `requirements_version` | string | `mandatory-tier1-2026-11-10.6` |
| `source_snapshot_sha256` | hex string | The data snapshot the row was computed from (see below). |

- Booleans are lowercase.
- The list columns are always valid JSON arrays.
- If a requirement or calculation cannot be established, the product is never eligible, and the reason says why.

**What changed in version `.6`** (2026-11-12; current).
- **The meaning of `tier1_complete` and `formulation_eligible` is unchanged**, and the eleven columns are unchanged.
- No eligibility boolean and no `missing_mandatory_properties` list changed against `.5`.
- 4 outcomes of `required_co_components` changed category, from `unresolved_route_association` to `absent` (INFINEUM_D3384, D3451; LUBRIZOL_CV1100, CV1103): their routes are reviewed and each lacks the viscosity-modifier dose. Their text in `eligibility_reasons` now lists every reviewed route with its state.
- Route evidence is bound to the records by fingerprint; "none required" statements need an explicit reviewed assessment.

**What changed in versions `.4` and `.5`** (2026-11-11).
- **The meaning of `tier1_complete` and `formulation_eligible` is unchanged**, and the eleven columns are unchanged.
- The four approved policies are implemented (`.4`), and five gaps found in the review of `.4` are corrected (`.5`).
- **Eligibility booleans: no product changed.** 11 base oils, 0 packages, 0 components, before and after.
- **`missing_mandatory_properties` changed for 8 packages** (INFINEUM_D3354, D3384, D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100, CV1103): `required_co_components` is now listed. One usable co-component does not complete a route; the route association of the recorded requirements is not established. All 8 were and remain ineligible.
- 74 outcomes of `required_co_components` changed category against `.3`: 8 `met` → `unresolved_route_association`; 35 `unresolved_applicability` → `absent`; 31 `unresolved_applicability` → `requirement_unknown`.
- `requirement_outcomes.csv` has two new last columns: `percentage_basis` and `selection_pending`.
- New companion files (below) report evidence documentation, value selection, value form, percentage basis and verification status separately. They never redefine the two eligibility fields.
- A legitimate change of results is reported by `compare_eligibility.py`, product by product, with its reasons; results are not required to stay numerically identical.

**What changed in version `.3`**.
- `tier1_complete` again means "all mandatory Tier 1 requirements satisfied". In `.2` it meant "documented", which counted unresolved bounds and pending selections as complete.
- Documented-but-unusable information moved to the companion file `documentation_coverage.csv`.
- On the data of revision 3 (commit `43e7f8b`), 10 products were complete and eligible, and 11 fully documented. Since the aramcoULTRA 8 selections of 2026-11-11 the calculated result is 11.

**What changed in version `.2`.**
- Previously `tier1_complete` was always equal to `formulation_eligible`.
- Ranges and one-sided bounds are now documented information: Tier 1 complete, but not eligible. They were previously treated as unmet without distinction.
- Pending Rule 1 selections now block eligibility.
- Calculations are validated against their inputs.
- VM/PPD subtype blocks no longer block.

## Categories (companion reports)

| Category | Meaning |
|---|---|
| `met` | Satisfied |
| `not_applicable_approved_rule` | Satisfied by an approved applicability rule (none approved yet) |
| `absent` | No value recorded |
| `bound_or_range_needs_assessment` | A reported range, one-sided bound or direction-less specification value. Documented evidence, never an absent value; never converted to an exact value and never given a midpoint. It does not satisfy a requirement that needs a point value. |
| `missing_unit_condition_provenance` | Value present, but its unit, test/reference temperature, source file or page is missing, or its percentage basis is unspecified or volume where wt.% is required |
| `invalid_value` | Not a valid measurement: non-finite, boolean, reversed range, unsupported or conflicting qualifier, or a value outside its own range |
| `invalid_or_unreproducible_calculation` | A `Calculated` value that no registered check reproduces from traceable inputs with matching conditions |
| `unresolved_applicability` | Whether or how the requirement applies is not established (a Not Required / Not Applicable label without an approved rule; a component marker the specification does not name) |
| `requirement_unknown` | No co-component requirement is recorded and no explicit statement says that none is required. A statement about the record, not about the supplier documents |
| `unresolved_route_association` | Co-component requirements are recorded, at least one with a usable dose, but which route each belongs to is not established by reviewed evidence, so the completeness of a route is not assessed |
| `unresolved_source_selection` | A value exists, but its Rule 1 source selection is pending or unreviewed |

## `source_snapshot_sha256`

How it is computed:
1. List every `Products_json/**/*.json` file by its project-relative POSIX path.
2. Sort the list by the UTF-8 bytes of the path.
3. Write one line per file: `<sha256 of the exact file bytes><two spaces><path>\n`.
4. Hash the UTF-8 manifest with SHA-256.

**Line endings.** The files are committed with LF line ends (`git ls-files --eol`: `i/lf`). This machine's Git configuration (`core.autocrlf=true`, set system-wide) checks them out with CRLF, so the exact bytes, and the hash, depend on the checkout.
- The interface value is always the exact-byte hash of the checkout that produced the file.
- `missing_mandatory_properties.md` also prints an **informational** LF-normalised fingerprint (CRLF written as LF). Checkouts with different conversion can use it to confirm they hold the same data. It is never a substitute for the interface value.
- **A consumer whose own exact-byte hash differs must regenerate the outputs in its checkout, or reject the file. It must never bypass the mismatch.**

## Requirement ids

Each requirement's authority, interpretation and open decision are in [requirements_review.md](requirements_review.md).

| Class | Blocking requirement ids |
|---|---|
| Base oil | `api_group_chemistry.api_group`, `api_group_chemistry.chemistry`, `kv40`, `kv100`, `viscosity_index`, `density`, `ccs` |
| Additive package | `package_type_application.package_type`, `package_type_application.intended_service`, `performance_claims`, `sae_grades_documented`, `treat_rate_matrix`, `permitted_base_oils_restrictions`, `route_selector_restrictions`, `required_co_components`, `published_formulations` |
| Additive component | `function.primary`, `chemical_family`, `active_content`, `carrier.identity`, `treat_rate`, `compatibility_restrictions`, `function_specific_markers` (or `function_specific_markers.tbn`, `.ca\|mg`, `.p`, `.zn`, `.mo` by function) |

Non-blocking ids (VM / PPD subtype blocks, reported only) start with `vm.` or `ppd.`.

## Companion files

| File | Content |
|---|---|
| `requirement_outcomes.csv` | Every product × requirement. Columns: `product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason, percentage_basis, selection_pending` |
| `missing_mandatory_properties.csv` | The same columns, unmet rows only (blocking and non-blocking) |
| `missing_mandatory_properties.md` | Counts per class (products, Tier 1 complete = eligible, fully documented), the outcome table by requirement and category, the sensitivity table, the interpretations used, and both fingerprints |
| `documentation_coverage.csv` | Per product: blocking requirements, satisfied, documented-not-usable (range/bound, pending selection), not documented, `all_blocking_documented`, `tier1_complete` and the category counts. **A companion measure, never completeness.** |

### Attribute files (`python tools/mandatory_properties/build_readiness.py`; `readiness_version` `readiness-2026-11-12.1`)

Additive files. A consumer of `product_eligibility.csv` alone is not affected by them.

| File | One row per | Content |
|---|---|---|
| `property_attributes.csv` | product × requirement | `evidence_documentation`, `value_selection`, `value_form`, `percentage_basis`, `verification_status`, `open_conflict`, `selected_point_value`, with the outcome category and reason |
| `product_input_completeness.csv` | product | Counts of those attributes over the mandatory requirements, `all_mandatory_evidence_documented`, and a copy of `tier1_complete` and `formulation_eligible` |
| `co_component_routes.csv` | route membership of a recorded requirement (one row per requirement and route), recorded requirement without a route, reviewed route, requirement stated by the source but not in the record, reviewed statement, or package with no recorded requirement | `requirement_state`, `route_id`, `route_state`, `review_validity` (current / stale / invalid), `reviewed_on`, `group`, `group_combination`, `group_state`, `requirement_list_confirmed`, `record_state`, `source_inspection`, `inspected`, `qualification`, `limitations`, and the product-level outcome |
| `percentage_basis.csv` | reported value in a dose or treat-rate field | Unit as recorded, basis class, how it is established, `basis_is_mass`, and the outcome of the value's own check |
| `volume_dose_evidence.csv` | volume-basis dosage entry kept in `external_fill_notes` | Product, grade, source and the evidence as recorded. Evidence only: it fills no wt.% field and nothing is converted |
| `applicability_review.csv` | N/A label or unresolved outcome | The label, the approved rule (none) and the result |
| `calculation_readiness.csv` | named calculation | Registered (with what it assessed) or not registered |
| `readiness_summary.md` | — | Counts, each with its scope |

| Attribute | Values | Meaning |
|---|---|---|
| `evidence_documentation` | `documented`, `documented_incomplete`, `not_recorded`, `invalid`, `calculated_not_reproduced`, `requirement_unknown`, `recorded_route_not_assessed`, `applicability_unresolved`, `not_applicable_approved_rule` | What the record holds. `not_recorded` says nothing about the source. A valid range or bound is documented |
| `value_selection` | `selected`, `pending`, `none` | From the source-selection ledger, independent of the category. A value can be `documented_incomplete` and `pending` at once. `pending` blocks every use that needs a selected value |
| `value_form` | `point`, `closed_range`, `lower_bound`, `upper_bound`, `specification_value_no_direction`, `text`, `structured`, `none` | The form as printed. A range or bound is never turned into a point |
| `percentage_basis` | `mass`, `volume`, `unspecified`, blank | For dose and treat-rate requirements only |
| `verification_status` | the review states of `source_review_status.csv`, or `not_individually_reviewed` | The review state of the source. Only base-oil properties in the coverage ledger have one |
| `selected_point_value` | `yes`, `no`, `not_numeric` | Scoped indicator: this one requirement has a selected point value with its unit, condition and source, and no pending selection. Not a readiness statement for any calculation |
| `basis_is_mass` | `true`, `false` | Only that the basis of the percentage is mass. Not a usability verdict: see `value_outcome_category` |
| `source_inspection` | `confirmed_by_source_review`, `historical_source_review_not_current`, `recorded_from_cited_page_not_re_reviewed`, `lead_in_inspected_text_not_reviewed`, `not_found_in_inspected_text`, `source_unavailable`, `not_inspected` | What is known about the source for a co-component row. Only a review whose bound records are unchanged is "confirmed"; a stale or invalid review is historical. "Not found in the inspected text" never means the supplier is silent |
| `route_state` | `route_complete`, `route_incomplete`, `recorded_requirements_usable_list_not_confirmed`, `route_evidence_stale`, `route_evidence_invalid`, `route_association_not_established` | The assessment of one route. Routes are independent; with no target route specified, no state is a statement of formulation readiness |

- **Co-component completeness is per route.** A route exists only through reviewed evidence bound to the record by fingerprint. 8 packages have reviewed routes (29 routes, none complete); the recorded requirements of the other 39 packages have `route_state = route_association_not_established`. The count of usable doses is informational.
- **No general readiness field exists**, and no conversion is registered. `volume_to_mass_percent` is kept as unused code.
- **Not a feature inventory.** These files cover the mandatory Tier 1 requirements and the VM/PPD subtype blocks. The association-mining dataset may also use suitable Tier 2 and Tier 3 properties; nothing here limits it.

## Stability promise to Workstream B

- The column names, their order and the encodings are fixed for every `requirements_version` that starts with `mandatory-tier1-`.
- A change of meaning gets a new version, as `.2` did.
- New requirement ids or categories may appear, so consumers should not assume a closed set.
