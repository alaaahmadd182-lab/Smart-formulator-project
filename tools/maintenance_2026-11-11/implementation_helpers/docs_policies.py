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


COUNTS = """| | Before (`.3`) | After (`.4`) |
|---|---:|---:|
| Base oils: `tier1_complete` = `formulation_eligible` | 11 of 181 | 11 of 181 |
| Packages | 0 of 78 | 0 of 78 |
| Components | 0 of 5 | 0 of 5 |
| Products whose eligibility fields or missing list changed | — | 0 |
| Requirement outcomes whose category changed | — | 66 |"""

# ------------------------------------------------------------------ requirements_review.md
rel = D + 'requirements_review.md'
s = load(rel)
s = sub(s, 'Requirements version: `mandatory-tier1-2026-11-10.3`', 'Requirements version: `mandatory-tier1-2026-11-10.4` (four policies approved on 2026-11-11: section 4a)')
s = sub(s, '| interpretation | The implementation adds a reading the sources do not state. Every interpretation is provisional until reviewed. |',
        '| interpretation | The implementation adds a reading the sources do not state. An interpretation is provisional until reviewed; I-1, I-6, I-8 and I-9 became approved policies on 2026-11-11 (section 4a). |')
s = sub(s, '| I-8: met by a reported co-component with a wt.% dose, **or** by a sourced statement that none is required | 70 (appl 66: no co-component recorded and no "none required" statement; meta 4: bare "%") | B |',
        '| I-8 (approved policy 2): met by a recorded supplier requirement with a usable mass-basis dose, **or** by an explicit, applicable statement that none is required. Assessed per recorded requirement; the product-level outcome says only that at least one is usable | 70 (abs 35: a supplier requirement is recorded without a dose; unknown 31: the documents are silent; meta 4: dose with a bare "%") | — (decided 2026-11-11) |')
s = sub(s, '- No interpretation is promoted to an approved rule. `APPROVED_APPLICABILITY_RULES` is empty, and every interpretation I-1 … I-8 is listed as provisional.',
        '- No interpretation is promoted to an approved rule by the implementation. Four policies were approved by you on 2026-11-11 (section 4a); the other interpretations stay provisional. `APPROVED_APPLICABILITY_RULES` is empty: no exemption is assumed.')
a = s.index('## 5. Rules the implementation does not add')
s = s[:a] + """## 4a. Policies approved on 2026-11-11 and how they are implemented (version `.4`)

These close decisions B, B-REP, D, E and F as questions of principle. They change no requirement, no tier and no threshold, and the published-formulation requirement (decision A) is unchanged. `tier1_complete` and `formulation_eligible` keep their meaning.

| Policy | Rule in force | Implementation |
|---|---|---|
| 1. Ranges and bounds | A valid, sourced range or bound is documented evidence. It is never reported as absent, never replaced by a point, and never given a midpoint. It does not satisfy a requirement that needs a point value. A calculation may use it only where a registered method accepts that form | Category `bound_or_range_needs_assessment` is kept. `property_attributes.csv` reports evidence documentation and value form separately. No range-aware method is registered |
| 2. Co-components | A recorded supplier requirement with a usable dose is met. A recorded requirement without a usable dose leaves that route incomplete. "None required" needs an explicit, applicable statement with its page and wording. Silence is unknown | `co_component_outcome` and `co_component_entries` in `requirements.py`; reviewed statements in `co_component_statements.json`; one row per recorded requirement in `co_component_routes.csv`, with the supplier's condition as recorded. New category `requirement_unknown` |
| 3. Percentage basis | Mass, volume or unspecified, from the recorded unit or from reviewed source evidence (heading, footnote, text, document-wide convention). An unspecified or volume percentage does not satisfy a wt.% requirement. Volume is converted only by a reproducible calculation with stated densities | `percentage_basis` and `volume_to_mass_percent` in `requirements.py`; evidence schema with `basis_class`, `evidence_kind`, `scope`; `percentage_basis.csv` lists every dose value |
| 4. Applicability | A Not Required / Not Applicable label counts only under a rule approved for the product class, the requirement and the task. A Missing value or a failed search is never N/A. No property changes tier | `APPROVED_APPLICABILITY_RULES` (empty) and `approved_rule`; `applicability_review.csv` lists every label and every unresolved outcome |

**Separate attributes.** One verdict cannot show whether information is written down, whether a value has been selected, and what form it has. `build_readiness.py` reports these apart, per requirement: `evidence_documentation`, `value_selection`, `value_form`, `percentage_basis`, `verification_status`.
- A pending source selection is **documented** evidence (alternatives exist) with `value_selection = pending`. It still blocks every use that needs a selected value.
- There is no general "calculation ready" label. `selected_point_value` says only that one requirement has a selected point value. Readiness is stated only for a named, registered calculation (`calculation_readiness.csv`); unregistered methods are listed as not assessed.
- These files cover the mandatory Tier 1 requirements and the VM/PPD subtype blocks. They do not define the feature inventory of the association-mining dataset, which may also use suitable Tier 2 and Tier 3 properties.

**Effect on the current data** (`baselines/eligibility_changes__policy_implementation_2026-11-11.csv`):

""" + COUNTS + """

- The 66 changed outcomes are all `required_co_components`, formerly "unresolved applicability": 35 are now `absent` (the record names a supplier-required co-component, usually a viscosity modifier, without a dose) and 31 are `requirement_unknown` (silence). All 66 were unmet before and are unmet now.
- Co-component rows: 17 recorded requirements with a usable dose, 9 with a dose whose basis is unspecified, 47 without a dose, 2 partial "none required" statements (PPD only, HiTEC 12210 / 12210M), 31 silent packages.
- Percentage basis of the 271 reported dose values: 187 mass, 84 unspecified, 0 volume. No document-wide convention was found.
- Applicability: 0 approved rules; 18 labelled values in 4 products and 10 requirement outcomes stay unresolved (3 API group and 2 CCS for the Risella oils, 5 component markers).

**Still open after these approvals:** which applicability rules to approve (none is); which calculations may be registered, including any range-aware one; decision A (published formulation); decision C (VM/PPD blocks stay non-blocking unless you decide otherwise); decision G (markers for functions the specification does not name).

""" + s[a:]
save(rel, s)

# ------------------------------------------------------------------ eligibility_interface.md
rel = D + 'eligibility_interface.md'
s = load(rel)
s = sub(s, '- **These rules are provisional.** The interpretations and decisions listed in `requirements_review.md` are not yet approved.',
        '- Four policies were approved on 2026-11-11 (ranges and bounds, co-components, percentage basis, applicability; `requirements_review.md` §4a). The remaining interpretations are provisional.')
s = sub(s, '| `requirements_version` | string | `mandatory-tier1-2026-11-10.3` |', '| `requirements_version` | string | `mandatory-tier1-2026-11-10.4` |')
s = sub(s, '**What changed in version `.3`** (current).', """**What changed in version `.4`** (current; 2026-11-11).
- **The meaning of `tier1_complete` and `formulation_eligible` is unchanged**, and the eleven columns are unchanged.
- The four approved policies are implemented. On the current data no product's eligibility fields changed: 11 base oils, 0 packages, 0 components, before and after.
- 66 outcomes of `required_co_components` changed category, from `unresolved_applicability` to `absent` (35: a supplier requirement is recorded without a dose) or to the new category `requirement_unknown` (31: silence). Their text in `eligibility_reasons` changed accordingly.
- Reason wording changed for ranges, bounds and percentage bases. `requirement_outcomes.csv` has one new last column, `percentage_basis`.
- New companion files (below) report evidence documentation, value selection, value form, percentage basis and verification status separately. They never redefine the two eligibility fields.
- A future legitimate change of results is reported by `compare_eligibility.py`, product by product, with its reasons; results are not required to stay numerically identical.

**What changed in version `.3`**.""")
s = sub(s, '- On the current data, 10 products are complete and eligible, and 11 are fully documented.',
        '- On the data of revision 3 (commit `43e7f8b`), 10 products were complete and eligible, and 11 fully documented. Since the aramcoULTRA 8 selections of 2026-11-11 the calculated result is 11.')
s = sub(s, '| `bound_or_range_needs_assessment` | A reported range, one-sided bound or direction-less specification value. Never converted to an exact value. Whether it serves the property\'s use is a provisional decision. |',
        '| `bound_or_range_needs_assessment` | A reported range, one-sided bound or direction-less specification value. Documented evidence, never an absent value; never converted to an exact value and never given a midpoint. It does not satisfy a requirement that needs a point value. |')
s = sub(s, '| `missing_unit_condition_provenance` | Value present, but its unit, mass basis, test/reference temperature, source file or page is missing |',
        '| `missing_unit_condition_provenance` | Value present, but its unit, test/reference temperature, source file or page is missing, or its percentage basis is unspecified or volume where wt.% is required |')
s = sub(s, '| `unresolved_applicability` | Whether or how the requirement applies is not established |',
        '| `unresolved_applicability` | Whether or how the requirement applies is not established (a Not Required / Not Applicable label without an approved rule; a component marker the specification does not name) |\n| `requirement_unknown` | Whether a requirement exists is not known: the supplier documents are silent about co-components. Silence is never read as "none required" |')
s = sub(s, '`product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason` |',
        '`product_id, material_class, product_name, requirement, category, blocking, representation, calculated, reason, percentage_basis` |')
a = s.index('## Stability promise to Workstream B')
s = s[:a] + """### Attribute files (`python tools/mandatory_properties/build_readiness.py`; `readiness_version` `readiness-2026-11-11.1`)

Additive files. A consumer of `product_eligibility.csv` alone is not affected by them.

| File | One row per | Content |
|---|---|---|
| `property_attributes.csv` | product × requirement | `evidence_documentation`, `value_selection`, `value_form`, `percentage_basis`, `verification_status`, `open_conflict`, `selected_point_value`, with the outcome category and reason |
| `product_input_completeness.csv` | product | Counts of those attributes over the mandatory requirements, `all_mandatory_evidence_documented`, and a copy of `tier1_complete` and `formulation_eligible` |
| `co_component_routes.csv` | recorded co-component requirement, reviewed statement, or silent package | State per requirement, with the supplier's condition as recorded in the role text, the dose, its basis and source |
| `percentage_basis.csv` | reported dose or treat-rate value | Unit as recorded, basis class (mass / volume / unspecified), how it is established, and whether it is usable where wt.% is required |
| `applicability_review.csv` | N/A label or unresolved outcome | The label, the approved rule (none) and the result |
| `calculation_readiness.csv` | named calculation | Registered (with what it assessed) or not assessed |
| `readiness_summary.md` | — | Counts |

| Attribute | Values | Meaning |
|---|---|---|
| `evidence_documentation` | `documented`, `documented_incomplete`, `not_documented`, `invalid`, `calculated_not_reproduced`, `requirement_unknown`, `applicability_unresolved`, `not_applicable_approved_rule` | Whether valid, sourced evidence exists. A valid range or bound is documented. Documented alternatives awaiting a source selection are documented |
| `value_selection` | `selected`, `pending`, `none` | Whether the value to use has been selected. `pending` blocks every use that needs a selected value |
| `value_form` | `point`, `closed_range`, `lower_bound`, `upper_bound`, `specification_value_no_direction`, `text`, `structured`, `none` | The form as printed. A range or bound is never turned into a point |
| `percentage_basis` | `mass`, `volume`, `unspecified`, blank | For dose and treat-rate requirements only |
| `verification_status` | the review states of `source_review_status.csv`, or `not_individually_reviewed` | The review state of the source, where the property is in the coverage ledger |
| `selected_point_value` | `yes`, `no`, `not_numeric` | Scoped indicator: this one requirement has a selected point value with its unit, condition and source. It is not a readiness statement for any calculation |

- **No general readiness field exists.** Readiness is stated only against a named, registered calculation. Today those are two verification checks for recorded calculated values and the volume-to-mass conversion; the viscosity-index calculation, mass balance, batch mass and every range-aware method are listed as not assessed.
- **Not a feature inventory.** These files cover the mandatory Tier 1 requirements and the VM/PPD subtype blocks. The association-mining dataset may also use suitable Tier 2 and Tier 3 properties; nothing here limits it. The form, basis and verification attributes are meant to be reused for those properties.

""" + s[a:]
save(rel, s)

# ------------------------------------------------------------------ HANDOFF.md
rel = D + 'HANDOFF.md'
s = load(rel)
s = sub(s, '8. **Reliable check runner**',
        '8. **Four approved policies implemented (requirements version `.4`; `requirements_review.md` §4a).** Ranges and bounds are documented evidence and never become points; co-components are assessed per recorded requirement, and silence is unknown; percentage basis is mass, volume or unspecified; N/A needs an approved rule (none exists). Evidence documentation, value selection, value form, percentage basis and verification status are separate attributes (`build_readiness.py`). The meaning of `tier1_complete` and `formulation_eligible` is unchanged, and on the current data no product\'s eligibility changed (section 3).\n9. **Reliable check runner**')
s = sub(s, '9. **Corrections found by the review.**', '10. **Corrections found by the review.**')
s = line(s, '| Rule 3 requirements |', '| Rule 3 requirements | Items explicit in the spec PDF and glossary. Four policies **approved on 2026-11-11** and implemented: ranges and bounds, co-components, percentage basis, applicability. The other interpretations (I-2 to I-5, I-7) stay provisional. No applicability rule is approved. |')
s = line(s, '| B / B-REP |', '| B / B-REP | **Decided 2026-11-11** (policies 1 and 2). Open remainder: which calculation, if any, may use a range or bound | No range-aware method is registered | `requirements_review.md` §4a |')
s = line(s, '| D |', '| D | **Principle decided 2026-11-11** (policy 4). Open remainder: whether to approve a rule for CCS / API group on the Risella process oils, with its authority | 3 products stay "unresolved applicability" | §4a |')
s = line(s, '| E |', '| E | **Decided 2026-11-11** (policy 3): an unspecified "%" stays unspecified | 84 dose values unspecified; 15 package treat-rate requirements and 4 co-component requirements unmet for that reason | §4a |')
s = line(s, '| F, G |', '| F, G | F decided with D. G open: markers for functions the specification does not name. No template field was added for co-components (reviewed statements are in a side file) | 5 components | §4 |')
s = sub(s, '## 3. Eligibility (version `.3`)', '## 3. Eligibility (version `.4`)')
s = sub(s, '**Changes (calculated by the eligibility build, not assumed).**',
        '**Before and after the policy implementation** (`compare_eligibility.py`; saved in `baselines/`):\n\n' + COUNTS +
        '\n\nThe 66 changed outcomes are co-component outcomes that were "unresolved applicability": 35 are now `absent` (a supplier requirement is recorded without a dose) and 31 `requirement_unknown` (silence). All were unmet before and after, so no eligibility field moved.\n\n**Earlier changes (calculated by the eligibility build, not assumed).**')
s = sub(s, '| | co-component architecture unresolved | 66 |', '| | co-component requirement recorded without a dose | 35 |\n| | co-component requirement unknown (documents silent) | 31 |')
a = s.index('| 1–7, 9, 11–13 | pipeline (document classes → eligibility) | 0 each | pass |')
b = s.index('- **Expected incomplete verification is not an execution failure.**')
s = s[:a] + """| 1–7, 9, 11–13 | pipeline (document classes → eligibility) | 0 each | pass |
| 8 | `external_comparison_accounting.py` | 0 | pass: 114 external-sourced values, each with one status |
| 10 | `verify_soil_table.py` | 0 | pass: the three aramcoULTRA 8 cells read in both saved copies |
| 14 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 15, 16 | `build_readiness.py` and `--check` | 0 | pass (up to date) |
| 17 | `compare_eligibility.py` | 0 | pass: interface columns identical; 0 products changed; 66 outcome categories changed (all co-components) |
| 18 | coverage matrix | 0 | pass (validation issues 30) |
| 19 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 20 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 13 differences in the 2 product files changed since `43e7f8b`, all pre-existing at the baseline, 0 new |
| 21 | `verify_preserved.py` | 0 | pass (section 6) |
| 22 | protected paths vs baseline | 0 | pass (no differences) |
| 23 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 24 | `tools/mandatory_properties/tests` | 0 | 58 OK (27 new policy tests) |
| 25 | `tools/data_policy/tests` | 0 | 61 OK |
| 26 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 27 | `verify_revision.py` (v5) | 1 | **expected failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

""" + s[b:]
s = sub(s, 'python tools/mandatory_properties/build_eligibility.py       # --check compares without writing; exit 3 = stale ledger\n',
        'python tools/mandatory_properties/build_eligibility.py       # --check compares without writing; exit 3 = stale ledger\n'
        'python tools/mandatory_properties/build_readiness.py         # attribute files (evidence, selection, form, basis, verification); --check\n'
        'python tools/mandatory_properties/compare_eligibility.py     # before/after report against the saved baselines\n')
s = sub(s, '- In version `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied.',
        '- In version `.4`, as in `.3`, `tier1_complete` = `formulation_eligible` = all mandatory Tier 1 requirements satisfied. The meaning is unchanged.\n- New additive attribute files report evidence documentation, value selection, value form, percentage basis and verification status. They are not a readiness verdict and not the feature inventory for association mining.')
save(rel, s)

# ------------------------------------------------------------------ CLAUDE.md
rel = 'CLAUDE.md'
s = load(rel)
s = sub(s, 'all mandatory Tier 1 requirements satisfied under the requirements version (version `.3`);',
        'all mandatory Tier 1 requirements satisfied under the requirements version (version `.4`; the meaning is unchanged since `.3`);')
s = sub(s, '- Line endings: this machine checks files out with CRLF',
        '- Policies approved 2026-11-11 (`requirements_review.md` §4a): (1) a valid sourced range or bound is documented evidence, never absent, never replaced by a point or midpoint, and not enough where a point is required; (2) co-components: a recorded supplier requirement without a usable dose leaves its route incomplete, "none required" needs an explicit applicable statement (`co_component_statements.json`), silence is `requirement_unknown`; assess per route and condition, never a product-wide "all routes" rule; (3) percentage basis is mass, volume or unspecified, from the unit or reviewed evidence; never use an unspecified or volume "%" as wt.%; convert volume only with `volume_to_mass_percent` and stated densities; (4) N/A needs a rule approved for the product class, requirement and task (`APPROVED_APPLICABILITY_RULES`, empty); Missing or "not found" is never N/A; never move a property between tiers.\n'
        '- Keep evidence documentation, value selection, value form, percentage basis and verification status apart (`build_readiness.py`, `property_attributes.csv`). A pending selection is documented evidence but blocks any use that needs a selected value. Never add a general "calculation ready" label: state readiness only against a named, registered calculation. The attribute files are not the association-mining feature inventory.\n'
        '- After a rule or data change, run `compare_eligibility.py` against a saved baseline and explain every change; never require results to stay identical, and never change the meaning of `tier1_complete` / `formulation_eligible` without a new version and a note.\n'
        '- Line endings: this machine checks files out with CRLF')
save(rel, s)

# ------------------------------------------------------------------ tools/README.md and PROJECT_FILE_GUIDE.md
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, "| `mandatory_properties/treat_rate_basis_scan.py` | Reading aid: the basis wording on the cited page of every bare-\"%\" treat rate |",
        "| `mandatory_properties/build_readiness.py` | Separate attributes of every requirement outcome (evidence documentation, value selection, value form, percentage basis, verification status), co-component rows per recorded requirement, the basis of every dose value, applicability labels, and named calculations (registered or not assessed); `--check` | `reports/mandatory_properties/property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`, `calculation_readiness.csv`, `readiness_summary.md` |\n"
        "| `mandatory_properties/compare_eligibility.py` | Before/after report of the eligibility outputs against saved baselines: counts, each changed product with its reasons, each changed outcome category | `docs/data_policy_mandatory_review/baselines/eligibility_changes__*.csv` |\n"
        "| `mandatory_properties/co_component_statements.json` | Reviewed supplier statements about co-components (kind, scope, page, quoted wording) | (data) |\n"
        "| `mandatory_properties/simulate_policy_decisions.py` | The read-only simulation written for the implementation plan of 2026-11-11 (kept for the record) | optional text copy |\n"
        "| `mandatory_properties/tests/test_policies.py` | Regression tests (27) for the four approved policies, the separate attributes, the unchanged interface meaning and the before/after comparison | nothing |\n"
        "| `mandatory_properties/treat_rate_basis_scan.py` | Reading aid: the basis wording on the cited page of every bare-\"%\" treat rate, and document-wide convention leads over every page of the source document |")
save(rel, s)

rel = 'PROJECT_FILE_GUIDE.md'
s = load(rel)
s = sub(s, '`treat_rate_basis_scan.csv`, `co_component_evidence.csv` |',
        '`treat_rate_basis_scan.csv`, `co_component_evidence.csv`; attribute files from `build_readiness.py`: `property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`, `calculation_readiness.csv`, `readiness_summary.md` |')
save(rel, s)

# ------------------------------------------------------------------ plan: status note
rel = D + 'implementation_plan_policy_decisions_2026-11-11.md'
s = load(rel)
s = sub(s, 'Date: 2026-11-11. Status: **plan only. Nothing in this plan is implemented.** No product JSON, template, checker, generated report or workbook was changed to write it.',
        'Date: 2026-11-11. Status: **implemented on 2026-11-11 with five corrections to this plan** (listed next). The text below is the plan as written, kept for the record; where it differs from the corrections, the corrections apply. What was built is described in `requirements_review.md` §4a and `eligibility_interface.md`.\n\n'
        '**Corrections applied at implementation.**\n'
        '1. Eligibility results are not required to stay numerically identical. The established meanings are preserved, and every change is reported and explained (`compare_eligibility.py`). The acceptance test "both booleans identical" in section 6 is withdrawn.\n'
        '2. Co-components are assessed for the relevant route and condition. The proposal in section 8, item 5 ("unmet until every recorded route is complete") was not adopted; there is no product-wide all-routes rule.\n'
        '3. Evidence documentation, value selection and calculation readiness are separate. A pending source selection is documented evidence (section 8, item 1 proposed the opposite) and still blocks any use that needs a selected value.\n'
        '4. No `point_calculation_ready` field exists. A scoped indicator (`selected_point_value`, per requirement) and a list of named calculations replace it; unregistered methods are reported as not assessed.\n'
        '5. Value form, percentage basis and verification status are separate attributes, and the attribute files are not the association-mining feature inventory (the plan\'s `association_mining_form` field was not created).')
save(rel, s)

# ------------------------------------------------------------------ changelog
rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel).rstrip('\n') + """

---

# Four approved policies implemented (2026-11-11, requirements version `.4`, uncommitted)

Approved by you on 2026-11-11: ranges and bounds, co-component requirements, percentage basis, applicability. Plan and its corrections: [implementation_plan_policy_decisions_2026-11-11.md](implementation_plan_policy_decisions_2026-11-11.md). Rules in force: `requirements_review.md` §4a.

## What changed

- **`tools/mandatory_properties/requirements.py`** (version `mandatory-tier1-2026-11-10.4`):
  - new category `requirement_unknown`; new `Outcome.basis`;
  - `co_component_outcome` / `co_component_entries`: recorded supplier requirements are assessed one by one; a requirement recorded without a dose is no longer ignored;
  - `percentage_basis` (mass / volume / unspecified) and `volume_to_mass_percent` (refuses without both densities at one temperature);
  - `APPROVED_APPLICABILITY_RULES` is a list of rules keyed by product class, requirement and task, with `approved_rule`; it is empty;
  - I-1, I-6, I-8 and the new I-9 are marked as approved policies.
- **`build_eligibility.py`:** passes the product class and the reviewed statements to the checks; `requirement_outcomes.csv` gains a last column `percentage_basis`. The eleven interface columns are unchanged.
- **New `build_readiness.py`** and seven attribute files (`property_attributes.csv`, `product_input_completeness.csv`, `co_component_routes.csv`, `percentage_basis.csv`, `applicability_review.csv`, `calculation_readiness.csv`, `readiness_summary.md`).
- **New `compare_eligibility.py`** and saved baselines in `baselines/` (the eligibility file, the outcomes and the documentation coverage as they were before the implementation; the change report).
- **New `co_component_statements.json`:** two reviewed statements (HiTEC 12210 and 12210M: no supplemental PPD needed), scope PPD only.
- **`treat_rate_basis_evidence.json`:** each entry has `basis_class`, `evidence_kind` and `scope`; the result of the document-wide convention search is recorded.
- **`treat_rate_basis_scan.py`:** searches every page of each source document for a document-wide convention.
- **Tests:** `test_policies.py` (27 new); two older tests adjusted (silence is `requirement_unknown`; an evidence entry must name its basis).
- **`run_checks.py`:** 27 steps (new: `build_readiness`, its `--check`, `compare_eligibility`).
- **Not changed:** product JSON, templates, the workbook structure, the published-formulation requirement, the thresholds (still proposed), tiers. The simulation script is kept.

## Before and after (`compare_eligibility.py`)

""" + COUNTS + """

- Data fingerprint unchanged: `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`.
- The 66 category changes are all `required_co_components`: `unresolved_applicability` → `absent` (35) or → `requirement_unknown` (31). They were unmet before and are unmet now.

## Current-data figures (from `readiness_summary.md`)

| | Count |
|---|---:|
| Mandatory requirement outcomes | 2,004 in 264 products |
| Evidence documented | 1,274 |
| Documented but incomplete (unit, condition, basis or source missing) | 24 |
| Not documented | 665 |
| Requirement unknown (co-components, silence) | 31 |
| Applicability unresolved | 10 |
| Documented ranges and bounds | 71 in 29 products (37 closed ranges, 22 lower bounds, 12 upper bounds) |
| Unresolved selections | 14 in 7 products |
| Dose values with an unspecified basis | 84 of 271, in 18 products |
| Dose values with a volume basis | 0 |
| N/A labels without a rule | 18 value objects in 4 products |
| Approved applicability rules | 0 |
"""
save(rel, s)
print('ok')
