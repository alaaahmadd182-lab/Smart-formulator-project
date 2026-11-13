"""One-off helper (2026-11-11, gap fixes): documentation updates. Already applied; do not rerun (each replacement asserts
that its target occurs exactly once)."""
R = 'C:\\Users\\windo\\sf-wsA\\'
D = 'docs\\data_policy_mandatory_review\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a))
    return s.replace(a, b)


def line(s, prefix, new):
    ls = s.split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    if new is None:
        del ls[hit[0]]
    else:
        ls[hit[0]] = new
    return '\n'.join(ls)


def block(s, start, end, new):
    a, b = s.index(start), s.index(end)
    assert a < b
    return s[:a] + new + s[b:]


COUNTS = """| | Before (`.3`) | After (`.5`) |
|---|---:|---:|
| Base oils: `tier1_complete` = `formulation_eligible` | 11 of 181 | 11 of 181 |
| Packages | 0 of 78 | 0 of 78 |
| Components | 0 of 5 | 0 of 5 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 8 |
| Requirement outcomes whose category changed | — | 74 |"""

CHANGES = """- **8 packages** gained `required_co_components` in their missing list: INFINEUM_D3354, D3384 and D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100 and CV1103. In `.3` (and in `.4`) each counted as met because one recorded co-component had a usable dose. That is not a complete route: 5 of the 8 also record a viscosity modifier without a dose, and for LUBRIZOL_3700 the source page says "when formulated with appropriate base oils and viscosity modifier" although the record lists only the booster. They are now `unresolved_route_association`. All 8 were ineligible before and stay ineligible (each also lacks the published formulation).
- **35 outcomes** moved from `unresolved_applicability` to `absent`: a co-component requirement is recorded and none of its doses is recorded, so no route that includes it can be complete.
- **31 outcomes** moved from `unresolved_applicability` to `requirement_unknown`: nothing is recorded in the record.
- No base oil and no component outcome changed category."""

# ------------------------------------------------------------------ requirements_review.md
rel = D + 'requirements_review.md'
s = load(rel)
s = sub(s, 'Requirements version: `mandatory-tier1-2026-11-10.4` (four policies approved on 2026-11-11: section 4a)',
        'Requirements version: `mandatory-tier1-2026-11-10.5` (four policies approved on 2026-11-11, with the gap fixes of the same day: section 4a)')
s = line(s, '| `fields.required_co_components[]` |',
         '| `fields.required_co_components[]` | MPS 3: "Required VM / PPD / booster architecture · wt.% per co-component"; GL: "required VM, PPD or booster doses" | explicit wording, conditional in effect: required where the route needs co-components | I-8 (approved policy 2): met only by an evidenced route in which every applicable requirement has a usable mass-basis dose and whose requirement list is confirmed by source review, **or** by an explicit, unqualified, applicable statement that none is required | 78 (abs 35: requirements recorded, no dose recorded; unknown 31: nothing recorded; route 8: usable doses recorded, route association not established; meta 4: doses with a bare "%") | which routes to review first |')
s = block(s, '## 4a. Policies approved on 2026-11-11', '## 5. Rules the implementation does not add', """## 4a. Policies approved on 2026-11-11 and how they are implemented (version `.5`)

These close decisions B, B-REP, D, E and F as questions of principle. They change no requirement, no tier and no threshold, and the published-formulation requirement (decision A) is unchanged. `tier1_complete` and `formulation_eligible` keep their meaning. Version `.4` was the first implementation; `.5` corrects five gaps found in its review the same day.

| Policy | Rule in force | Implementation |
|---|---|---|
| 1. Ranges and bounds | A valid, sourced range or bound is documented evidence. It is never reported as absent, never replaced by a point, and never given a midpoint. It does not satisfy a requirement that needs a point value | Category `bound_or_range_needs_assessment` is kept; value form is a separate attribute. No range-aware method is registered |
| 2. Co-components | Completeness is assessed per evidenced route. Every requirement that applies to the route needs a usable dose, and the route's requirement list must be confirmed by source review. One usable component never completes a route that needs others. Independent routes are assessed separately. Without reviewed route evidence the association is not established and completeness is not assessed. "None required" needs an explicit, unqualified, applicable statement | `co_component_routes`, `co_component_outcome` and `explicit_none_required` in `requirements.py`; reviewed routes in `co_component_route_evidence.json` (empty: no route reviewed); reviewed statements in `co_component_statements.json`; `co_component_routes.csv`. Categories `requirement_unknown` and `unresolved_route_association` |
| 3. Percentage basis | Mass, volume or unspecified, from the recorded unit or from reviewed source evidence. An unspecified or volume percentage does not satisfy a wt.% requirement. No conversion is registered or used; volume evidence is listed separately and fills no wt.% field | `percentage_basis` in `requirements.py`; `percentage_basis.csv` with the narrow flag `basis_is_mass`; `volume_dose_evidence.csv` |
| 4. Applicability | A Not Required / Not Applicable label counts only under a rule approved for the product class, the requirement and the task. A Missing value or a failed search is never N/A. No property changes tier | `APPROVED_APPLICABILITY_RULES` (empty) and `approved_rule`; `applicability_review.csv` |

**Separate attributes** (`build_readiness.py`, per requirement): `evidence_documentation`, `value_selection`, `value_form`, `percentage_basis`, `verification_status`.
- **Selection is independent of the category.** It comes from the source-selection ledger. A value can have incomplete metadata and a pending selection at once; both are reported.
- A pending selection is documented evidence (alternatives exist) and still blocks every use that needs a selected value.
- There is no general "calculation ready" label. Readiness is stated only for a named, registered calculation; no conversion and no range-aware method is registered.
- These files do not define the feature inventory of the association-mining dataset.

**Four different statements about evidence, never merged:**

| Statement | Meaning | Where |
|---|---|---|
| not recorded | The record holds no value or entry. Says nothing about the source | `evidence_documentation = not_recorded`; `record_state` |
| not found in the inspected text | A keyword search of text layers found nothing; the columns say which documents and pages were inspected. Not a source review, and never "the supplier is silent" | `source_inspection = not_found_in_inspected_text`; `inspected` |
| source unavailable / not inspected | The source could not be obtained, or it has no text layer and was not read by the search | `source_inspection`; `verification_status = evidence_unavailable` |
| confirmed by source review | A reviewer read the page and the quoted wording is recorded | reviewed statements, reviewed routes, lead and external reviews |

**Effect on the current data** (`baselines/eligibility_changes__policy_implementation_2026-11-11.csv`):

""" + COUNTS + """

""" + CHANGES + """

**Pending selections: 17, not 14.** The source-selection ledger lists 17 mandatory properties as pending. The first implementation derived the selection status from the outcome category and showed 14, because three values (aramcoPRIMA 110, 230 and 500 density) have no unit, and that category took precedence. Nothing was resolved. All 17 are now reported:

| Property | Pending | Products |
|---|---:|---|
| KV40 | 4 | FORMOSA_150N_GII_PLUS, FORMOSA_500N_GII, NESTE_NEXBASE_3060, NESTE_NEXBASE_3080 |
| KV100 | 3 | NESTE_NEXBASE_3060, NESTE_NEXBASE_3080, PETRONAS_ETRO_4 |
| Viscosity index | 2 | NESTE_NEXBASE_3080, PETRONAS_ETRO_4 |
| Density | 7 | NESTE_NEXBASE_3043, 3050, 3060, 3080; **ARAMCO_LUBEREF_PRIMA_110, 230, 500 (also: unit not recorded; the three that were hidden)** |
| CCS | 1 | PETRONAS_ETRO_4 |

The ledger holds 34 pending rows in all; the other 17 are non-mandatory properties, outside the mandatory-requirement files.

**Co-components** (78 packages):
- 47 packages record 73 requirements: 17 with a usable dose, 9 with a dose whose basis is unspecified, 47 without a dose. No route has been reviewed, so the route association of all 73 is "not established".
- 31 packages record no requirement. For 27 the keyword search found nothing in the inspected text; for 1 it found a lead that is not reviewed (TIANHE_P_TEC_3232); for 2 the cited files have no text layer and were not inspected (CHEVRON_N204, N216); for 1 the source could not be obtained (AFTON_HITEC_12204L).
- 2 reviewed supplier statements (HiTEC 12210, 12210M): "no supplemental PPD should be needed". They cover the PPD only and are qualified by "should", so they are kept as printed and are not "none required".

**Percentage basis.** Scope: the 271 reported values in the dose and treat-rate fields. 187 mass, 84 unspecified, 0 volume. `basis_is_mass` says only that; 2 mass-basis values are not usable for another reason (MINGLAN_T3161A, status Reported with no number). Outside those fields, 5 volume-basis dosage entries for AFTON_HITEC_5748 (SAE grade, vol.%, source and conditions as recorded) are listed in `volume_dose_evidence.csv`; its wt.% fields stay Missing.

**Applicability.** 0 approved rules; 18 labelled values in 4 products and 10 requirement outcomes stay unresolved.

**Still open:** which co-component routes to review; which applicability rules to approve (none is); which calculations may be registered; decision A (published formulation); decision C; decision G.

""")
save(rel, s)

# ------------------------------------------------------------------ eligibility_interface.md
rel = D + 'eligibility_interface.md'
s = load(rel)
s = sub(s, '| `requirements_version` | string | `mandatory-tier1-2026-11-10.4` |', '| `requirements_version` | string | `mandatory-tier1-2026-11-10.5` |')
s = block(s, '**What changed in version `.4`** (current; 2026-11-11).', '**What changed in version `.3`**.', """**What changed in versions `.4` and `.5`** (2026-11-11; `.5` is current).
- **The meaning of `tier1_complete` and `formulation_eligible` is unchanged**, and the eleven columns are unchanged.
- The four approved policies are implemented (`.4`), and five gaps found in the review of `.4` are corrected (`.5`).
- **Eligibility booleans: no product changed.** 11 base oils, 0 packages, 0 components, before and after.
- **`missing_mandatory_properties` changed for 8 packages** (INFINEUM_D3354, D3384, D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100, CV1103): `required_co_components` is now listed. One usable co-component does not complete a route; the route association of the recorded requirements is not established. All 8 were and remain ineligible.
- 74 outcomes of `required_co_components` changed category against `.3`: 8 `met` → `unresolved_route_association`; 35 `unresolved_applicability` → `absent`; 31 `unresolved_applicability` → `requirement_unknown`.
- `requirement_outcomes.csv` has two new last columns: `percentage_basis` and `selection_pending`.
- New companion files (below) report evidence documentation, value selection, value form, percentage basis and verification status separately. They never redefine the two eligibility fields.
- A legitimate change of results is reported by `compare_eligibility.py`, product by product, with its reasons; results are not required to stay numerically identical.

""")
s = sub(s, '| `requirement_unknown` | Whether a requirement exists is not known: the supplier documents are silent about co-components. Silence is never read as "none required" |',
        '| `requirement_unknown` | No co-component requirement is recorded and no explicit statement says that none is required. A statement about the record, not about the supplier documents |\n| `unresolved_route_association` | Co-component requirements are recorded, at least one with a usable dose, but which route each belongs to is not established by reviewed evidence, so the completeness of a route is not assessed |')
s = sub(s, '`product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason, percentage_basis` |',
        '`product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason, percentage_basis, selection_pending` |')
s = block(s, '### Attribute files (`python tools/mandatory_properties/build_readiness.py`', '## Stability promise to Workstream B', """### Attribute files (`python tools/mandatory_properties/build_readiness.py`; `readiness_version` `readiness-2026-11-11.2`)

Additive files. A consumer of `product_eligibility.csv` alone is not affected by them.

| File | One row per | Content |
|---|---|---|
| `property_attributes.csv` | product × requirement | `evidence_documentation`, `value_selection`, `value_form`, `percentage_basis`, `verification_status`, `open_conflict`, `selected_point_value`, with the outcome category and reason |
| `product_input_completeness.csv` | product | Counts of those attributes over the mandatory requirements, `all_mandatory_evidence_documented`, and a copy of `tier1_complete` and `formulation_eligible` |
| `co_component_routes.csv` | recorded co-component requirement, reviewed route, reviewed statement, or package with no recorded requirement | `requirement_state` (dose usable / not usable / not recorded), `route_id` and `route_state`, `record_state`, `source_inspection` and what was `inspected`, `qualification` of a supplier statement, and the product-level outcome |
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
| `source_inspection` | `confirmed_by_source_review`, `recorded_from_cited_page_not_re_reviewed`, `lead_in_inspected_text_not_reviewed`, `not_found_in_inspected_text`, `source_unavailable`, `not_inspected` | What is known about the source for a co-component row. "Not found in the inspected text" is a keyword search of text layers and never means the supplier is silent |

- **Co-component completeness is per route.** A route exists only through reviewed evidence. None has been reviewed, so every recorded requirement has `route_state = route_association_not_established` and no route is called complete. The count of usable doses is informational.
- **No general readiness field exists**, and no conversion is registered. `volume_to_mass_percent` is kept as unused code.
- **Not a feature inventory.** These files cover the mandatory Tier 1 requirements and the VM/PPD subtype blocks. The association-mining dataset may also use suitable Tier 2 and Tier 3 properties; nothing here limits it.

""")
save(rel, s)

# ------------------------------------------------------------------ HANDOFF.md
rel = D + 'HANDOFF.md'
s = load(rel)
s = line(s, '8. **Four approved policies implemented',
         '8. **Four approved policies implemented (requirements version `.5`; `requirements_review.md` §4a).** Ranges and bounds are documented evidence and never become points. Co-component completeness is assessed per evidenced route: one usable component does not complete a route, and without reviewed route evidence completeness is not assessed. Percentage basis is mass, volume or unspecified, and no conversion is registered. N/A needs an approved rule (none exists). Evidence documentation, value selection (from the ledger, independent of the category), value form, percentage basis and verification status are separate attributes (`build_readiness.py`). The meaning of `tier1_complete` and `formulation_eligible` is unchanged; no eligibility boolean changed (section 3).')
s = block(s, '**Before and after the policy implementation**', '**Earlier changes (calculated by the eligibility build, not assumed).**',
          '**Before and after the policy implementation** (`compare_eligibility.py`; saved in `baselines/`):\n\n' + COUNTS + '\n\n' + CHANGES + '\n\n')
s = sub(s, '| | co-component requirement recorded without a dose | 35 |\n| | co-component requirement unknown (documents silent) | 31 |',
        '| | co-component requirements recorded, none with a dose | 35 |\n| | no co-component requirement recorded (not the same as supplier silence) | 31 |\n| | co-component route association not established | 8 |')
s = sub(s, '| | unresolved source selection | 14 |', '| | unresolved source selection (category) | 14; the ledger lists 17 pending mandatory selections, 3 of them on values that also lack a unit |')
s = sub(s, '| 17 | `compare_eligibility.py` | 0 | pass: interface columns identical; 0 products changed; 66 outcome categories changed (all co-components) |',
        '| 17 | `compare_eligibility.py` | 0 | pass: interface columns identical; 0 eligibility booleans changed; 8 missing lists and 74 outcome categories changed (all co-components) |')
s = sub(s, '| 24 | `tools/mandatory_properties/tests` | 0 | 58 OK (27 new policy tests) |', '| 24 | `tools/mandatory_properties/tests` | 0 | 66 OK (35 policy tests) |')
s = sub(s, '- In version `.4`, as in `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied. The meaning is unchanged.',
        '- In version `.5`, as in `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied. The meaning is unchanged.')
s = sub(s, '## 3. Eligibility (version `.4`)', '## 3. Eligibility (version `.5`)')
s = sub(s, '**External values not compared with an SDS**',
        '**Co-component routes not reviewed.** No route has reviewed evidence, so the route association of all 73 recorded requirements is "not established" and no package\'s co-component requirement is met. Reviewing a route means reading its page, listing every co-component the supplier requires for it, and recording that in `co_component_route_evidence.json`.\n\n**External values not compared with an SDS**')
save(rel, s)

# ------------------------------------------------------------------ CLAUDE.md
rel = 'CLAUDE.md'
s = load(rel)
s = sub(s, '(version `.4`; the meaning is unchanged since `.3`)', '(version `.5`; the meaning is unchanged since `.3`)')
s = sub(s, '(2) co-components: a recorded supplier requirement without a usable dose leaves its route incomplete, "none required" needs an explicit applicable statement (`co_component_statements.json`), silence is `requirement_unknown`; assess per route and condition, never a product-wide "all routes" rule;',
        '(2) co-components: completeness is per evidenced route (`co_component_route_evidence.json`); every requirement of the route needs a usable dose and the route\'s requirement list must be confirmed by source review; one usable component never completes a route; keep independent routes separate; never map a route from role text, and report an unestablished association as not assessed; "none required" needs an explicit, unqualified, applicable statement (`co_component_statements.json`), and free text never counts;')
s = sub(s, 'never use an unspecified or volume "%" as wt.%; convert volume only with `volume_to_mass_percent` and stated densities;',
        'never use an unspecified or volume "%" as wt.%; no conversion is registered (`volume_to_mass_percent` is unused code), and volume evidence never fills a wt.% field (`volume_dose_evidence.csv`);')
s = sub(s, '- Keep evidence documentation, value selection, value form, percentage basis and verification status apart (`build_readiness.py`, `property_attributes.csv`). A pending selection is documented evidence but blocks any use that needs a selected value.',
        '- Keep evidence documentation, value selection, value form, percentage basis and verification status apart (`build_readiness.py`, `property_attributes.csv`). Take the selection status from the source-selection ledger, never from the outcome category: a value can have a metadata defect and a pending selection at once. A pending selection is documented evidence but blocks any use that needs a selected value.\n'
        '- Evidence wording: "not recorded" (the record), "not found in the inspected text/pages" (a search, with what was inspected), "source unavailable / not inspected" and "confirmed by source review" are four different statements. Never infer supplier silence from an empty JSON field, and keep supplier qualifications ("should be needed") as printed.')
save(rel, s)

# ------------------------------------------------------------------ tools/README.md and PROJECT_FILE_GUIDE.md
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, '| `mandatory_properties/tests/test_policies.py` | Regression tests (27) for the four approved policies, the separate attributes, the unchanged interface meaning and the before/after comparison | nothing |',
        '| `mandatory_properties/tests/test_policies.py` | Regression tests (35) for the four approved policies and their gap fixes: two required components in one route, independent routes, unestablished route association, free-text and qualified statements, a pending selection combined with missing metadata, a mass-basis value that is otherwise unusable, the unregistered conversion, the separate attributes, the unchanged interface meaning and the before/after comparison | nothing |\n'
        '| `mandatory_properties/co_component_route_evidence.json` | Reviewed evidence of co-component routes (members and whether the requirement list is confirmed); empty until routes are reviewed | (data) |\n'
        '| `maintenance_2026-11-11/implementation_helpers/` | One-off scripts used to apply edits during this work, kept for the record. Hard-coded paths; already applied; do not rerun | nothing |')
s = sub(s, '`reports/mandatory_properties/property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`',
        '`reports/mandatory_properties/property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `volume_dose_evidence.csv`, `applicability_review.csv`')
save(rel, s)
rel = 'PROJECT_FILE_GUIDE.md'
s = load(rel)
s = sub(s, '`co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`', '`co_component_routes.csv`, `percentage_basis.csv`, `volume_dose_evidence.csv`, `applicability_review.csv`')
save(rel, s)

# ------------------------------------------------------------------ helper folder README
save('tools\\maintenance_2026-11-11\\implementation_helpers\\README.md', """# Implementation helper scripts (historical)

One-off scripts used between 2026-11-10 and 2026-11-11 to apply edits to tools, tests and documentation, and to survey the data while doing so. They were written in a temporary scratch folder and are kept here for the record.

- **Do not rerun them.** They have been applied. Most replace exact text and stop with an assertion if the text is no longer there; the survey scripts only print.
- They contain hard-coded paths to the worktree `C:\\Users\\windo\\sf-wsA`.
- They are not part of the pipeline and not part of `run_checks.py`. The tools they edited are the source of truth.
- The `fix_gaps_*.py` scripts belong to the gap fixes of 2026-11-11 (requirements version `.5`).
""")

# ------------------------------------------------------------------ changelog
rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel).rstrip('\n') + """

---

# Gap fixes to the policy implementation (2026-11-11, requirements version `.5`, uncommitted)

Five gaps in the `.4` implementation were corrected. No product JSON, template, datasheet or evidence file changed; the data fingerprint is unchanged (`93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`).

## What was wrong and what changed

1. **Co-component completeness.** `.4` (like `.3`) counted the requirement as met when one recorded co-component had a usable dose. Completeness is now assessed per evidenced route: every requirement that applies to the route needs a usable dose, and the route's requirement list must be confirmed by source review. Routes come only from reviewed evidence (`co_component_route_evidence.json`, empty); nothing is mapped from role text; an unestablished association is reported as not assessed (new category `unresolved_route_association`). The "at least one usable dose" count is kept in the reason as information only. Free text in `co_component_requirement_statement` no longer passes: a "none required" statement must be structured, sourced, unqualified and cover all co-components (`explicit_none_required`).
2. **Selection status.** It is taken from the source-selection ledger for every outcome (`Outcome.selection_pending`, column `selection_pending`), not from the category.
3. **Percentage reporting.** `usable_where_wt_pct_is_required` is replaced by `basis_is_mass`, with the value's own check outcome beside it. Volume-basis dosage evidence kept in `external_fill_notes` is listed in the new `volume_dose_evidence.csv`. Counts state their scope.
4. **Conversion.** `volume_to_mass_percent` is unregistered and unused. Its code is kept; its documentation says it is arithmetic only and cannot establish the source, unit or applicability of its inputs.
5. **Evidence wording.** "Not recorded", "not found in the inspected text", "source unavailable / not inspected" and "confirmed by source review" are reported separately. The co-component scan now records which documents and pages it inspected and which it could not. Supplier qualifications are kept: the two PPD statements carry `qualification: 'should be needed'`.

## Changed counts, with reasons

""" + COUNTS + """

""" + CHANGES + """

| Count | `.4` | `.5` | Reason |
|---|---:|---:|---|
| Pending selections (mandatory) | 14 | 17 | The status now comes from the ledger. The 3 added are aramcoPRIMA 110 / 230 / 500 density, which also lack a unit; that category had hidden them. Nothing was resolved in between |
| Co-component requirement met (packages) | 8 | 0 | One usable component is not a complete route; no route is reviewed |
| `unresolved_route_association` (packages) | — | 8 | The same 8 packages |
| Evidence "documented" (mandatory outcomes) | 1,274 | 1,266 | The same 8 outcomes are now `recorded_route_not_assessed` |
| Selected point values | 624 | 616 | The same 8 outcomes no longer count as a met point value |
| "none required" statements treated as partial | 2 | 2 | Unchanged in number; now also marked as qualified ("should be needed") |
| Co-component leads found by the scan (packages) | 13 | 16 | The search also matches "formulated with … viscosity modifier" |
| Packages with no recorded requirement | 31 | 31 | Now split by inspection: 27 not found in the inspected text, 1 unreviewed lead, 2 not inspected (no text layer), 1 source unavailable |
| Volume-basis evidence entries listed | 0 | 5 | AFTON_HITEC_5748 dosages in vol.%, kept in `external_fill_notes`; its wt.% fields stay Missing |
| Values in the dose fields: mass / unspecified / volume | 187 / 84 / 0 | 187 / 84 / 0 | Unchanged; the scope is now stated |

## Files

- Changed: `requirements.py`, `build_eligibility.py`, `build_readiness.py` (readiness version `.2`), `co_component_evidence_scan.py`, `co_component_statements.json`, tests.
- New: `co_component_route_evidence.json` (empty), `volume_dose_evidence.csv`, `tools/maintenance_2026-11-11/implementation_helpers/` (the helper scripts that were only in the scratch folder, with a README).
- Tests: `tools/mandatory_properties/tests` 66 (35 policy tests): two required components in one route, independent routes, unestablished association, stale or unsourced route evidence, free-text and qualified statements, a pending selection combined with missing metadata, a mass-basis value that is otherwise unusable, the unregistered conversion.
"""
save(rel, s)
print('ok')
