# Implementation plan: four approved policy decisions

Date: 2026-11-11. Status: **implemented on 2026-11-11 with five corrections to this plan** (listed next). The text below is the plan as written, kept for the record; where it differs from the corrections, the corrections apply. What was built is described in `requirements_review.md` §4a and `eligibility_interface.md`.

**Corrections applied at implementation.**
1. Eligibility results are not required to stay numerically identical. The established meanings are preserved, and every change is reported and explained (`compare_eligibility.py`). The acceptance test "both booleans identical" in section 6 is withdrawn.
2. Co-components are assessed for the relevant route and condition. The proposal in section 8, item 5 ("unmet until every recorded route is complete") was not adopted; there is no product-wide all-routes rule.
3. Evidence documentation, value selection and calculation readiness are separate. A pending source selection is documented evidence (section 8, item 1 proposed the opposite) and still blocks any use that needs a selected value.
4. No `point_calculation_ready` field exists. A scoped indicator (`selected_point_value`, per requirement) and a list of named calculations replace it; unregistered methods are reported as not assessed.
5. Value form, percentage basis and verification status are separate attributes, and the attribute files are not the association-mining feature inventory (the plan's `association_mining_form` field was not created).

- Branch `feat/data-policy-mandatory-review`, worktree `C:\Users\windo\sf-wsA`, HEAD `43e7f8b` (revision 3) plus the existing uncommitted work, which is preserved.
- Requirements version in force: `mandatory-tier1-2026-11-10.3`. Data fingerprint: `93b704a7…1f3530`.
- Unchanged by this plan: the published-formulation requirement, the conflict thresholds (still proposed, not applied), the tiers of all properties.
- Not started: association mining, ingestion of the new batch.

## 1. The decisions, and the principle the plan follows

| # | Decision (approved 2026-11-11) |
|---|---|
| 1 | A valid, sourced range or bound is documented information, not a missing value. It is not automatically usable in every calculation. No midpoint is invented. |
| 2 | Co-components: record supplier-supported requirements, doses and conditions. "None required" needs explicit, applicable evidence. Silence means unknown. A required co-component without a usable dose leaves that route incomplete. |
| 3 | Percentage basis: mass or volume is established from the source. An unspecified "%" stays unspecified and is not used where wt.% is needed. Volume is converted to mass only by a reproducible calculation with sufficient inputs. |
| 4 | Applicability: N/A needs a documented rule for the product class and task. A failed search is not N/A. Uncertain applicability stays unresolved. No property changes tier to raise eligibility. |

**Principle.** `tier1_complete` and `formulation_eligible` keep their current definitions, word for word. The decisions are implemented by **adding** separately named assessments beside them, not by changing what the two existing fields mean.

## 2. Current behaviour versus proposed behaviour

### Decision 1: ranges and bounds

| | Current (`.3`) | Proposed |
|---|---|---|
| Classification | A valid range or bound gets the outcome category `bound_or_range_needs_assessment`. It is never converted to a point (interpretation I-1, provisional) | Same category and same no-conversion rule, now an approved rule instead of a provisional interpretation |
| Is it "missing"? | No, but the interface column `missing_mandatory_properties` lists it, and readers take that as missing | Unchanged column. A new field states documentation completeness separately, so a documented range is visibly not missing |
| Use in calculations | No distinction: a range simply leaves the requirement unmet | Three separate assessments: documentation completeness, point-calculation readiness, and range-aware readiness per registered method |
| Midpoints | Never computed | Never computed; a test forbids any derived point labelled typical |
| Range-aware methods | None exists | A registry of range-aware methods, empty at first. A range counts as usable only for a method listed there, with the forms it accepts (closed range, lower bound, upper bound) |

### Decision 2: required co-components

| | Current (`.3`) | Proposed |
|---|---|---|
| States | Three outcomes: met (a co-component with a mass-basis dose), missing basis (dose with a bare "%"), unresolved applicability (anything else) | Five explicit states: required with a usable dose; required without a usable dose (route incomplete); none required (explicit, applicable evidence); partial statement (covers one co-component type only); unknown (silence) |
| Silence | "unresolved applicability" (66 packages) | "unknown". Still unmet; the wording no longer suggests an applicability question |
| "None required" | Accepted only through a field no record has (`co_component_requirement_statement`) | Accepted only from a reviewed statement with its page, quoted wording and scope (which co-component types, which routes). A statement about one type (for example PPD only) does not cover the others |
| Conditions | Not evaluated | The supplier's conditions (grade, base-oil group, claim) are recorded with each requirement, and the assessment is per route where the record has routes |
| Evidence | A text-layer scan produces leads (`co_component_evidence.csv`) | The leads are reviewed; only reviewed statements count |

### Decision 3: percentage basis

| | Current (`.3`) | Proposed |
|---|---|---|
| Basis classes | Two: mass (stated in the unit, or in reviewed page evidence) and "no mass basis" | Three: mass, volume, unspecified |
| Evidence accepted | Unit text; page heading or wording for the recorded value (3 reviewed cases) | Unit text; heading; footnote; an explicit document-wide convention. Each evidence entry records its scope (value, table or document) and the quoted wording |
| Unspecified "%" | Kept as printed; the requirement is unmet (`missing_unit_condition_provenance`) | Same, with an explicit reason "basis unspecified". Never used where wt.% is required |
| Volume basis | Not recognised: a vol.% value would be reported as "no mass basis", the same as unspecified | Recognised as volume. Not usable where wt.% is required unless converted |
| Conversion | None | Volume to mass only as a registered calculation: stated inputs (densities with their temperatures, from applicable sources), status `Calculated`, reproduced by a check. Without it, the value stays volume |

### Decision 4: applicability

| | Current (`.3`) | Proposed |
|---|---|---|
| Rule store | `APPROVED_APPLICABILITY_RULES`, keyed by requirement only; empty | A rule registry keyed by product class, requirement and intended task, each rule with its documented authority, wording and approval date; empty until a rule is approved |
| N/A labels | `Not Required` / `Not Applicable` without a rule give "unresolved applicability" | Same |
| Failed search | Never treated as N/A | Same, now tested explicitly |
| Tiers | Fixed by the templates | Fixed; a test asserts that no requirement changes tier or blocking state |

## 3. Proposed definitions of the completeness and eligibility fields

| Field | Where | Definition | Status |
|---|---|---|---|
| `tier1_complete` | `product_eligibility.csv` | **Unchanged.** All mandatory Tier 1 requirements are satisfied under `requirements_version`: each is met, or not applicable under an approved rule | existing |
| `formulation_eligible` | `product_eligibility.csv` | **Unchanged.** Same value as `tier1_complete`; no other gate | existing |
| `documentation_complete` | new companion file | Every mandatory requirement has valid, sourced information: it is met, not applicable under an approved rule, or a valid sourced range or bound. Absent values, invalid values, missing unit/condition/basis, unknown co-component requirements and unresolved applicability are not documented. Proposed: a pending source selection is **not** counted (decision needed, section 8) | new |
| `point_calculation_ready` | new companion file | Every mandatory numeric requirement has an accepted point input with its unit, condition and source. On base oils this equals `tier1_complete` today; it is named separately so that the two can diverge without redefining either | new |
| `range_aware_ready` | new companion file, one column per registered method | For a registered range-aware method: every input the method needs is a point, or a form the method accepts. Blank while no method is registered. Never true by default | new |
| `association_mining_form` | new per-property companion file | Not a yes/no verdict. For each product and mandatory property: `point`, `closed_range`, `lower_bound`, `upper_bound`, `unspecified_basis`, `unknown` or `none`, with unit and condition. Workstream B decides which forms its method accepts | new |
| `all_blocking_documented` | `documentation_coverage.csv` | Existing companion measure (counts pending selections as documented). Kept for one version, then replaced by `documentation_complete` | existing, to retire |

A documented range is therefore never a formulation approval: it can make `documentation_complete` true, and nothing else.

## 4. Files affected

**Scripts.**
- `tools/mandatory_properties/requirements.py`: approved-rule wording for I-1, I-6, I-8; basis classifier (mass / volume / unspecified); co-component states; applicability registry structure; readiness functions. The functions that compute `tier1_complete` and `formulation_eligible` are not edited.
- `tools/mandatory_properties/build_eligibility.py`: writes the two new companion files and their summary section.
- `tools/mandatory_properties/treat_rate_basis_scan.py`: reports volume wording and document-wide statements as leads.
- `tools/mandatory_properties/co_component_evidence_scan.py`: unchanged logic; its output becomes the lead list for the reviewed decisions.
- `tools/data_policy/run_checks.py`: no new step is needed; the existing build, `--check` and test steps cover the new outputs.
- `tools/mandatory_properties/simulate_policy_decisions.py`: the read-only simulation of this plan; removed or kept as a check once the implementation lands.

**Schemas and reviewed-evidence files.**
- `tools/mandatory_properties/treat_rate_basis_evidence.json`: each entry gains `basis` (`mass` / `volume`), `scope` (`value` / `table` / `document`) and `evidence_kind` (`unit`, `heading`, `footnote`, `document_convention`).
- New `tools/mandatory_properties/co_component_evidence_decisions.json`: reviewed statements (product, page, quoted wording, kind, co-component types covered, conditions).
- New applicability rule registry (inside `requirements.py` or a JSON beside it): empty.
- **No template change and no product JSON change** in this plan. Reviewed statements live in the sidecar files above (see decision 4 in section 8).

**Interfaces.**
- `reports/mandatory_properties/product_eligibility.csv`: columns and definitions unchanged.
- New `reports/mandatory_properties/product_readiness.csv` (one row per product) and `property_readiness.csv` (one row per product and mandatory property).

**Reports.** `requirement_outcomes.csv` and `missing_mandatory_properties.csv/.md` (reason wording, new summary section), `documentation_coverage.csv` (kept one version), `co_component_evidence.csv`, `treat_rate_basis_scan.csv`.

**Workbook.** `Coverage_Matrix.xlsx` is not affected: it reports the validated `status` of each property and has no eligibility field. It is regenerated only because it is part of the check run.

**Documentation.** `requirements_review.md` (approved rules, closed decisions), `eligibility_interface.md` (new files, compatibility statement), `HANDOFF.md`, `CHANGELOG`, `CLAUDE.md`, `tools/README.md`, `PROJECT_FILE_GUIDE.md`, the curated log (dated note).

## 5. Compatibility and versioning

- **Existing consumers.** `product_eligibility.csv` keeps its eleven columns, their order, formats and definitions. A consumer that reads only this file sees no schema change.
- **Row values.** The plan is designed so that both booleans stay identical for every product on the current data. An acceptance test compares them row by row with the current file.
- **Version.** The checker code changes (reason wording, new basis class, new co-component states), so `requirements_version` moves to `mandatory-tier1-2026-11-10.4` when the implementation lands. The change note states that the definitions of `tier1_complete` and `formulation_eligible` are unchanged. Workstream B recomputes on the version change, as the interface already requires.
- **New files are additive** and carry their own version (`readiness_version`) and the same data fingerprint, so they can change later without touching the eligibility file.
- **Teammate handoff.** `eligibility_interface.md` gets a section describing the two new files and stating which forms each property has. No field the teammate already uses changes meaning.

## 6. Regression tests and acceptance criteria

| Rule | Tests | Accepted when |
|---|---|---|
| Interface | Columns of `product_eligibility.csv` identical; both booleans identical to the pre-implementation file for all 264 products; no requirement changed tier or blocking state | All pass on the current fingerprint |
| 1 | A valid range and each bound form are `documentation_complete` but not `point_calculation_ready`; no output contains a derived midpoint; `range_aware_ready` is blank with an empty registry and true only for a form the registered method accepts; an invalid range (reversed, missing endpoint) is not documented | All pass; the five earlier validation regressions still pass |
| 2 | Silence gives `unknown`; a statement about PPD only does not cover a VM; "none required" without page and wording is rejected; a required co-component with a bare "%" dose gives route incomplete; a dose under a condition applies only to that route | All pass; every package has exactly one state |
| 3 | A unit, a heading, a footnote and a document-wide statement each establish the basis with their scope; bare "%" stays unspecified and is refused where wt.% is required; vol.% is classed volume, not unspecified; a conversion without densities is refused; a conversion with stated inputs is reproduced by its check | All pass; no recorded unit in any product JSON is changed |
| 4 | An N/A label without a rule stays unresolved; a rule for another product class or task does not apply; "not found" never yields N/A; an approved test rule yields not-applicable only for its class and task | All pass with the registry empty in production |
| General | The full `run_checks.py` run; protected-file verification; the simulation counts of section 7 reproduced by the real build | Overall PASS; the only expected failure is `verify_revision.py` |

## 7. Read-only impact assessment (SIMULATION, not eligibility results)

Produced by `python tools/mandatory_properties/simulate_policy_decisions.py` from the current reports. Full output: [policy_decisions_simulation_2026-11-11.txt](policy_decisions_simulation_2026-11-11.txt). The eligibility results in force are unchanged: 11 of 181 base oils, 0 of 78 packages, 0 of 5 components.

**Decision 1.** 71 mandatory outcomes in 29 products are ranges or bounds:

| Property | Closed range | Lower bound | Upper bound |
|---|---:|---:|---:|
| KV40 | 13 | 1 | 0 |
| KV100 | 17 | 0 | 0 |
| Viscosity index | 6 | 21 | 0 |
| CCS | 0 | 0 | 12 |
| Active content (components) | 1 | 0 | 0 |

| Candidate field (simulated) | Base oils | Packages | Components |
|---|---:|---:|---:|
| `point_calculation_ready` | 11 | 0 | 0 |
| `documentation_complete`, pending selections not counted | 11 | 0 | 0 |
| `documentation_complete`, pending selections counted | 11 | 0 | 0 |
| ready for a method accepting closed ranges only (illustration) | 11 | 0 | 0 |

- No product-level count moves. All 28 base oils that hold a range or bound also lack something else: 26 have an absent value, 3 a missing unit, 2 a pending source selection.
- The effect of the decision is at property level: those 71 outcomes become visibly "documented", and the per-property forms become available to Workstream B.

**Decision 2.** 78 packages:

| Simulated state | Packages | Current category |
|---|---:|---|
| required, usable dose recorded | 8 | met |
| required, dose without a usable basis: route incomplete | 4 | missing unit/condition |
| supplier names or requires a co-component, no usable dose recorded: route incomplete | 10 | unresolved applicability |
| silence: unknown | 56 | unresolved applicability |

- The 10 and the 56 come from a text-layer search, so they are leads until the statements are reviewed. The two "no supplemental PPD needed" statements (HiTEC 12210 / 12210M) cover the PPD only; the same search also flags a co-component mention in both, so they are counted among the 10 until reviewed.
- No package becomes met or eligible; all 78 still fail the unchanged published-formulation requirement.

**Decision 3.** 271 reported dose values in the records:

| Field | Mass (unit) | Mass (page evidence) | Volume | Unspecified |
|---|---:|---:|---:|---:|
| Package treat-rate matrix | 166 | 3 | 0 | 73 |
| Required co-component dose | 11 | 6 | 0 | 9 |
| Component treat rate | 1 | 0 | 0 | 2 |

- 84 values are unspecified (80 with a bare "%", 4 with no unit). They stay unspecified.
- No recorded value has a volume unit today, so the volume class and the conversion path change no current result.
- Current treat-rate outcome for the 78 packages: 57 met, 15 missing basis, 6 absent. Unchanged in the simulation.

**Decision 4.** No applicability rule is approved, so the simulated result equals the current one.
- 18 value objects carry an N/A label: `Not Required` on 11 base-oil values (SHELL_RISELLA_X_415 / 420 / 430), `Not Applicable` on 7 component values (LUBRIZOL_CV6320).
- 76 mandatory outcomes are "unresolved applicability": 66 are the co-component cases above (renamed "unknown" by decision 2), 5 are component markers, 3 are API group and 2 are CCS (Risella).

## 8. Decisions that cannot be inferred from the approvals

1. **Pending source selection.** Does a value whose source selection is pending count toward `documentation_complete`? Proposed: no. It changes no count today.
2. **Range-aware methods.** Which calculations may take a range or bound, and in which form? None is registered, so `range_aware_ready` stays blank until you name one.
3. **Association-mining suitability.** Which forms does the teammate's method accept: only points, also closed ranges, also one-sided bounds? The plan delivers the per-property forms; the acceptance rule should be agreed with Workstream B.
4. **Where "none required" and reviewed co-component statements are stored.** Proposed: a reviewed sidecar file, so that no template changes. The alternative is a new optional record field, which needs a template version change.
5. **Product level or route level for co-components.** If one route is complete and another is not, is the package's requirement met? Proposed: report per route, and keep the product-level requirement unmet until every recorded route is complete.
6. **Scope of the percentage rule.** Does it also cover composition percentages (saturates, aromatics and similar; 123 values are flagged as "%" with no stated basis), or only treat rates and doses? Proposed: doses first; composition values reported only.
7. **Volume-to-mass inputs.** Which density is acceptable (the product's own, at which temperature, from which document class)? No current value needs it.
8. **Applicability rules themselves.** No rule is approved. Candidates you may want to document: CCS and API group for the Risella process oils; the CV6320 labels; component markers for functions the specification does not name. Each needs its authority and the task it applies to.
9. **Version bump.** Is moving to `.4` at implementation acceptable, given identical booleans?

## 9. Known stale item to correct during implementation

`eligibility_interface.md` still says "10 products are complete and eligible" in its version-`.3` note. The current calculated result is 11 since the aramcoULTRA 8 selections. It was not edited now, because this task changes no existing document.

## 10. Suggested order of work

1. Applicability registry and tests (no data effect).
2. Basis classifier, evidence schema and tests.
3. Co-component states, review of the 15 packages whose pages carry a statement, sidecar decisions file.
4. Readiness fields and the two companion files; interface document.
5. Full check run; comparison of both booleans with the current file; documentation and changelog.
