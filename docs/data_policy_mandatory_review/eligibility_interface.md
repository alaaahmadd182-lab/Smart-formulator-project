# Product eligibility interface (Workstream A → Workstream B)

**File.** `reports/mandatory_properties/product_eligibility.csv`.
- Generate it with `python tools/mandatory_properties/build_eligibility.py`.
- Check it without writing with `--check`.
- The build needs a current coverage ledger (`python tools/data_policy/source_coverage_ledger.py`). It stops with exit 3 if the ledger was built from different data.

**Meaning.** `tier1_complete = true` and `formulation_eligible = true` both mean only one thing: all mandatory Tier 1 requirements are satisfied under `requirements_version`.
- It is not a statement of chemical suitability, compatibility or performance.
- Products that are not eligible stay in the database with all their data.
- **These rules are provisional.** The interpretations and decisions listed in `requirements_review.md` are not yet approved.

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
| `requirements_version` | string | `mandatory-tier1-2026-11-10.3` |
| `source_snapshot_sha256` | hex string | The data snapshot the row was computed from (see below). |

- Booleans are lowercase.
- The list columns are always valid JSON arrays.
- If a requirement or calculation cannot be established, the product is never eligible, and the reason says why.

**What changed in version `.3`** (current).
- `tier1_complete` again means "all mandatory Tier 1 requirements satisfied". In `.2` it meant "documented", which counted unresolved bounds and pending selections as complete.
- Documented-but-unusable information moved to the companion file `documentation_coverage.csv`.
- On the current data, 10 products are complete and eligible, and 11 are fully documented.

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
| `bound_or_range_needs_assessment` | A reported range, one-sided bound or direction-less specification value. Never converted to an exact value. Whether it serves the property's use is a provisional decision. |
| `missing_unit_condition_provenance` | Value present, but its unit, mass basis, test/reference temperature, source file or page is missing |
| `invalid_value` | Not a valid measurement: non-finite, boolean, reversed range, unsupported or conflicting qualifier, or a value outside its own range |
| `invalid_or_unreproducible_calculation` | A `Calculated` value that no registered check reproduces from traceable inputs with matching conditions |
| `unresolved_applicability` | Whether or how the requirement applies is not established |
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
| `requirement_outcomes.csv` | Every product × requirement. Columns: `product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason` |
| `missing_mandatory_properties.csv` | The same columns, unmet rows only (blocking and non-blocking) |
| `missing_mandatory_properties.md` | Counts per class (products, Tier 1 complete = eligible, fully documented), the outcome table by requirement and category, the sensitivity table, the interpretations used, and both fingerprints |
| `documentation_coverage.csv` | Per product: blocking requirements, satisfied, documented-not-usable (range/bound, pending selection), not documented, `all_blocking_documented`, `tier1_complete` and the category counts. **A companion measure, never completeness.** |

## Stability promise to Workstream B

- The column names, their order and the encodings are fixed for every `requirements_version` that starts with `mandatory-tier1-`.
- A change of meaning gets a new version, as `.2` did.
- New requirement ids or categories may appear, so consumers should not assume a closed set.
