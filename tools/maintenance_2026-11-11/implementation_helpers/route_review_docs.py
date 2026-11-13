"""One-off helper (2026-11-12, route review): documentation updates. Already applied; do not rerun."""
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
    ls[hit[0]] = new
    return '\n'.join(ls)


CHANGE = """**Route review of 2026-11-12 (version `.6`), against the baseline saved before it** (`baselines/pre_route_review_2026-11-12/`, comparison in `baselines/eligibility_changes__route_review_2026-11-12.csv`):

| | Before (`.5`) | After (`.6`) |
|---|---:|---:|
| Base oils / packages / components: `tier1_complete` = `formulation_eligible` | 11 / 0 / 0 | 11 / 0 / 0 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 0 |
| Requirement outcomes whose category changed | — | 4 |

The 4 category changes are `required_co_components`, from `unresolved_route_association` to `absent`:
- **INFINEUM_D3384, INFINEUM_D3451, LUBRIZOL_CV1100, LUBRIZOL_CV1103.** Their routes are now reviewed, and every one requires a viscosity modifier for which the datasheet prints no dose. The association is no longer unresolved; a documented requirement lacks its dose.
- **INFINEUM_D3354, LUBRIZOL_3589C, 3700, 3700D** stay `unresolved_route_association`: at least one of their routes has usable recorded doses but a requirement list that cannot be confirmed complete.
- All eight were unmet before and are unmet now. Detail per route: [co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md)."""

# ------------------------------------------------------------------ requirements_review.md
rel = D + 'requirements_review.md'
s = load(rel)
s = sub(s, 'Requirements version: `mandatory-tier1-2026-11-10.5` (four policies approved on 2026-11-11, with the gap fixes of the same day: section 4a)',
        'Requirements version: `mandatory-tier1-2026-11-10.6` (four policies approved on 2026-11-11; gap fixes `.5`; route-evidence binding, statement review and the route review of eight packages `.6`: section 4a)')
s = sub(s, '## 4a. Policies approved on 2026-11-11 and how they are implemented (version `.5`)', '## 4a. Policies approved on 2026-11-11 and how they are implemented (version `.6`)')
s = line(s, '| `fields.required_co_components[]` |',
         '| `fields.required_co_components[]` | MPS 3: "Required VM / PPD / booster architecture · wt.% per co-component"; GL: "required VM, PPD or booster doses" | explicit wording, conditional in effect: required where the route needs co-components | I-8 (approved policy 2): met only by a current, evidenced route in which every applicable requirement has a usable mass-basis dose and whose requirement list is confirmed by source review, **or** by an explicit, reviewed, unconditional, product-wide statement that none is required | 78 (abs 39: a documented requirement has no usable dose; unknown 31: nothing recorded; route 4: usable doses, list not confirmed; meta 4: doses with a bare "%") | which further packages to review |')
s = line(s, '- 47 packages record 73 requirements:',
         '- 47 packages record 73 requirements: 17 with a usable dose, 9 with a dose whose basis is unspecified, 47 without a dose. 8 packages have reviewed routes (29 routes: 21 incomplete, 8 with usable recorded doses but an unconfirmed list, 0 complete). The 51 requirements of the other 39 packages have no route association.')
s = line(s, '- 2 reviewed supplier statements',
         '- 2 reviewed supplier statements (HiTEC 12210, 12210M): "no supplemental PPD should be needed". Their reviewed assessment records the qualification "should be needed" verbatim and a scope of one component type, so they are not "none required".')
s = sub(s, '**Still open:** which co-component routes to review;', '**Still open:** which further co-component routes to review (8 of 47 packages are done);')
s = sub(s, '**Pending selections: 17, not 14.**', CHANGE + """

**Rules added in `.6`.**
- **Route evidence is bound to the complete input records.** Each record a route relies on (the co-component entries, and its treat-rate entry) is stored with the SHA-256 of the whole record: values, range endpoints, unit, qualifier, conditions, role text and source reference. A change to any of them makes the route `route_evidence_stale` until it is reviewed again. A change elsewhere in the product does not.
- **Stale or invalid evidence is a historical review, not a current confirmation.** It is reported as `historical_source_review_not_current`, and the entries it names have no current route association.
- **Every membership is kept.** A recorded requirement can belong to several independent routes; each membership is reported with that route's own assessment. 7 recorded requirements belong to more than one route.
- **Alternatives.** A group of requirements is `all`, `one_of` (supplier-stated alternatives) or `unresolved` (the source does not say). An unresolved group never completes a route.
- **Requirements the source states and the record lacks** keep the route incomplete and are listed as proposed corrections (4: the viscosity modifier of the first block of LUBRIZOL_3700 and 3700D, in two routes each).
- **"None required" needs an explicit reviewed assessment**: product, meaning, unconditional (true/false), the qualification verbatim, scope (component types and routes) and conditions. A missing field proves nothing; contradictory or incomplete metadata is rejected; a statement limited to one route or component type is never product-wide. Inline and side-file statements pass through the same check against the current product.

**Pending selections: 17, not 14.**""")
save(rel, s)

# ------------------------------------------------------------------ eligibility_interface.md
rel = D + 'eligibility_interface.md'
s = load(rel)
s = sub(s, '| `requirements_version` | string | `mandatory-tier1-2026-11-10.5` |', '| `requirements_version` | string | `mandatory-tier1-2026-11-10.6` |')
s = sub(s, '**What changed in versions `.4` and `.5`** (2026-11-11; `.5` is current).', """**What changed in version `.6`** (2026-11-12; current).
- **The meaning of `tier1_complete` and `formulation_eligible` is unchanged**, and the eleven columns are unchanged.
- No eligibility boolean and no `missing_mandatory_properties` list changed against `.5`.
- 4 outcomes of `required_co_components` changed category, from `unresolved_route_association` to `absent` (INFINEUM_D3384, D3451; LUBRIZOL_CV1100, CV1103): their routes are reviewed and each lacks the viscosity-modifier dose. Their text in `eligibility_reasons` now lists every reviewed route with its state.
- Route evidence is bound to the records by fingerprint; "none required" statements need an explicit reviewed assessment.

**What changed in versions `.4` and `.5`** (2026-11-11).""")
s = sub(s, '`readiness_version` `readiness-2026-11-11.2`)', '`readiness_version` `readiness-2026-11-12.1`)')
s = line(s, '| `co_component_routes.csv` |',
         '| `co_component_routes.csv` | route membership of a recorded requirement (one row per requirement and route), recorded requirement without a route, reviewed route, requirement stated by the source but not in the record, reviewed statement, or package with no recorded requirement | `requirement_state`, `route_id`, `route_state`, `review_validity` (current / stale / invalid), `reviewed_on`, `group`, `group_combination`, `group_state`, `requirement_list_confirmed`, `record_state`, `source_inspection`, `inspected`, `qualification`, `limitations`, and the product-level outcome |')
s = line(s, '| `source_inspection` |',
         '| `source_inspection` | `confirmed_by_source_review`, `historical_source_review_not_current`, `recorded_from_cited_page_not_re_reviewed`, `lead_in_inspected_text_not_reviewed`, `not_found_in_inspected_text`, `source_unavailable`, `not_inspected` | What is known about the source for a co-component row. Only a review whose bound records are unchanged is "confirmed"; a stale or invalid review is historical. "Not found in the inspected text" never means the supplier is silent |\n'
         '| `route_state` | `route_complete`, `route_incomplete`, `recorded_requirements_usable_list_not_confirmed`, `route_evidence_stale`, `route_evidence_invalid`, `route_association_not_established` | The assessment of one route. Routes are independent; with no target route specified, no state is a statement of formulation readiness |')
s = line(s, '- **Co-component completeness is per route.**',
         '- **Co-component completeness is per route.** A route exists only through reviewed evidence bound to the record by fingerprint. 8 packages have reviewed routes (29 routes, none complete); the recorded requirements of the other 39 packages have `route_state = route_association_not_established`. The count of usable doses is informational.')
save(rel, s)

# ------------------------------------------------------------------ HANDOFF.md
rel = D + 'HANDOFF.md'
s = load(rel)
s = sub(s, '(requirements version `.5`; `requirements_review.md` §4a).**', '(requirements version `.6`; `requirements_review.md` §4a).**')
s = sub(s, '## 3. Eligibility (version `.5`)', '## 3. Eligibility (version `.6`)')
s = sub(s, '- In version `.5`, as in `.3`,', '- In version `.6`, as in `.3`,')
s = sub(s, '**Earlier changes (calculated by the eligibility build, not assumed).**', CHANGE + '\n\n**Earlier changes (calculated by the eligibility build, not assumed).**')
s = sub(s, '| | co-component requirements recorded, none with a dose | 35 |', '| | co-component: a documented requirement has no usable dose (35 not route-reviewed; 4 with every reviewed route incomplete) | 39 |')
s = sub(s, '| | co-component route association not established | 8 |', '| | co-component: recorded doses usable, route list not confirmed | 4 |')
a = s.index('**Co-component routes not reviewed.**')
b = s.index('**External values not compared with an SDS**')
s = s[:a] + """**Co-component routes.** 8 packages are reviewed ([co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md)): 29 routes, 21 incomplete, 8 with usable recorded doses but an unconfirmed requirement list, 0 complete. The evidence cannot resolve: the dose of any viscosity modifier; the identity of the boosters of LUBRIZOL_3589C, 3700 and 3700D; whether the D3354 footnote-4 boosters are alternatives; whether any list is exhaustive; which CV1103 table column is the CV6320 route. The other 39 packages with recorded requirements (51 requirements) have no reviewed route. Five record corrections are proposed and not applied.

""" + s[b:]
a = s.index('Run on 2026-11-11 at revision-3 commit')
b = s.index('- **Expected incomplete verification is not an execution failure.**')
s = s[:a] + """Run on 2026-11-12 at revision-3 commit `43e7f8b` plus the uncommitted work since. Full output per step is in `test_results/NN_<step>.txt`; the summary is in `summary.md` / `summary.json`. The results as they were before this run are kept in `baselines/pre_route_review_2026-11-12/test_results/`. **Overall: PASS** (every required step met its expectation).

| # | Step | Return code | Verdict |
|---:|---|---:|---|
| 1–13 | pipeline (document classes → eligibility), incl. `external_comparison_accounting.py` and `verify_soil_table.py` | 0 each | pass |
| 14 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 15, 16 | `build_readiness.py` and `--check` | 0 | pass (up to date) |
| 17 | `compare_eligibility.py` (against `.3`) | 0 | pass: columns identical; 0 booleans, 8 missing lists and 74 categories changed (all co-components) |
| 18 | `compare_eligibility.py` (against the pre-route-review baseline, `.5`) | 0 | pass: 0 booleans, 0 missing lists, 4 categories changed |
| 19 | coverage matrix | 0 | pass (validation issues 30) |
| 20 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 21 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 13 differences in the 2 product files changed since `43e7f8b`, all pre-existing at the baseline, 0 new |
| 22 | `verify_preserved.py` | 0 | pass (section 6) |
| 23 | protected paths vs baseline | 0 | pass (no differences) |
| 24 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 25 | `tools/mandatory_properties/tests` | 0 | 74 OK (43 policy tests) |
| 26 | `tools/data_policy/tests` | 0 | 61 OK |
| 27 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 28 | `verify_revision.py` (v5) | 1 | **expected legacy failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

No unexpected failure. **Snapshot:** `review_snapshots/review_snapshot_2026-11-12/` (`MANIFEST.sha256`, `REFERENCES.txt`); made after this run with `python tools/data_policy/make_review_snapshot.py`.

""" + s[b:]
save(rel, s)

# ------------------------------------------------------------------ CLAUDE.md, README, file guide
rel = 'CLAUDE.md'
s = load(rel)
s = sub(s, '(version `.5`; the meaning is unchanged since `.3`)', '(version `.6`; the meaning is unchanged since `.3`)')
s = sub(s, 'never map a route from role text, and report an unestablished association as not assessed; "none required" needs an explicit, unqualified, applicable statement (`co_component_statements.json`), and free text never counts;',
        'never map a route from role text, and report an unestablished association as not assessed; route evidence is bound to the complete records by fingerprint (`record_fingerprint`), so after changing a bound record re-review the route instead of refreshing its hash; a component may belong to several routes; never treat a list as exhaustive because it names some components; "none required" needs an explicit reviewed assessment (product, meaning, unconditional, qualification verbatim, scope, conditions) in `co_component_statements.json`, a missing field proves nothing, and free text never counts;')
s = sub(s, '- Run every check with `python tools/data_policy/run_checks.py`',
        '- Before regenerating reports for a new task, save the current reports and test results under `docs/data_policy_mandatory_review/baselines/`; freeze a reviewed state with `python tools/data_policy/make_review_snapshot.py --name <name>` (never overwritten; `--verify` checks it).\n- Run every check with `python tools/data_policy/run_checks.py`')
save(rel, s)
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, '| `mandatory_properties/tests/test_policies.py` | Regression tests (35)', '| `mandatory_properties/tests/test_policies.py` | Regression tests (43; incl. route evidence bound by fingerprint, one component in two routes, stale evidence reported as historical, and reviewed "none required" statements)')
s = sub(s, '| `mandatory_properties/co_component_route_evidence.json` | Reviewed evidence of co-component routes (members and whether the requirement list is confirmed); empty until routes are reviewed | (data) |',
        '| `mandatory_properties/co_component_route_evidence.json` | Reviewed evidence of co-component routes for 8 packages (29 routes): conditions and quotes as printed, required groups, fingerprints of the bound records, unrecorded requirements, limitations, proposed record corrections | (data) |\n'
        '| `data_policy/make_review_snapshot.py` | Freezes a dated review snapshot (code, policy inputs, product JSON, reports, documentation, test results) with a SHA-256 manifest; references the source archive by hash; `--verify` | `review_snapshots/<name>/` |')
save(rel, s)
rel = 'PROJECT_FILE_GUIDE.md'
s = load(rel)
s = sub(s, '| `tools/data_policy/`, `tools/mandatory_properties/` | Tool |', '| `review_snapshots/` | Frozen record | Dated review snapshots with a SHA-256 manifest (`make_review_snapshot.py`); never edited |\n| `tools/data_policy/`, `tools/mandatory_properties/` | Tool |')
save(rel, s)

# ------------------------------------------------------------------ changelog
rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel).rstrip('\n') + """

---

# Route-evidence binding, statement review and the route review of eight packages (2026-11-12, requirements version `.6`, uncommitted)

No product JSON, template, datasheet or evidence file changed. Data fingerprint unchanged: `93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530`. The reports and check results as they were before this work are in `baselines/pre_route_review_2026-11-12/`.

## Fixes

1. **Route-evidence freshness.** A route's evidence stored only the entry identity and `dose.value`. It now stores the SHA-256 of each complete record it relies on (`record_fingerprint`: values, range endpoints, unit, qualifier, conditions, role text, source file, page and revision; derived `*_final` keys excluded), for the co-component entries and the treat-rate entry. A change makes the route `route_evidence_stale`; unrelated product fields do not.
2. **Route memberships.** A recorded requirement can belong to several routes. `co_component_routes.csv` has one row per requirement and route, each with that route's assessment. Stale or invalid evidence is reported as `historical_source_review_not_current`, never as confirmed, and gives no current association.
3. **"None required".** `explicit_none_required` now needs an explicit reviewed assessment (product, meaning, unconditional, qualification verbatim, scope by component type and route, conditions). A missing qualification is no longer read as "unconditional"; contradictory or incomplete metadata is rejected; a hedge word in the quote together with "unconditional" is a contradiction (a guard, not the basis of the meaning). Inline and side-file statements pass the same check against the current product.
4. **Source review of eight packages**: [co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md). 29 routes recorded; 0 complete, 21 incomplete, 8 with usable recorded doses but an unconfirmed list. Five record corrections proposed, none applied.
5. **Baseline.** New `make_review_snapshot.py`; snapshot `review_snapshots/review_snapshot_2026-11-12/`.

## Before and after

""" + CHANGE + """

Pending selections are unchanged and still independently represented: 17 mandatory (14 in category `unresolved_source_selection`, 3 with a metadata defect).

## Files

- Changed: `requirements.py`, `build_readiness.py` (readiness version `readiness-2026-11-12.1`), `co_component_route_evidence.json`, `co_component_statements.json`, `run_checks.py` (28 steps), tests.
- New: `make_review_snapshot.py`, the route review document, helper scripts `route_review_*.py` in `tools/maintenance_2026-11-11/implementation_helpers/`.
- Tests: `tools/mandatory_properties/tests` 74.
"""
save(rel, s)
print('ok')
