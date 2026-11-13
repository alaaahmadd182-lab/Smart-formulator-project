# Decision brief: the "published formulation" requirement for additive packages

Date: 2026-11-11. Status: **for decision. Neither option is implemented.** The checker, the requirements version (`mandatory-tier1-2026-11-10.3`) and the shared interface `product_eligibility.csv` are unchanged.

**The decision.** Should a supplier-published finished-oil recipe stay one of the conditions for a package to be Tier 1 complete, or should it be assessed separately from the package's route data?

## 1. Exact wording and location

| Source | Location | Wording |
|---|---|---|
| Specification: `Smart_Formulator_Minimum_Property_Set.pdf` (in the source archive) | Slide 3 of 5, "03 · ADDITIVE PACKAGES", subtitle | "A package is a technology route, not just a fluid. Its route fields are as blocking as its numbers." |
| | Slide 3, heading of the first block | "TIER 1 — ROUTE-DEFINING" / "these make a generated recipe legitimate or invalid" |
| | Slide 3, eighth and last item of that block | "Exact published formulation + its results" / "complete recipe summing to 100.00 wt.%" |
| Glossary: `Property_Glossary.docx` | Table "B ADDITIVE PACKAGES — Route-defining fields / Numeric contribution", row with Tier = 1 | Property: "Published formulation". Meaning: "Exact supplier recipe and measured results." Unit / test condition: "Each ingredient wt.%; total 100 wt.%" |
| Template: `json_templates/additive_package_tier1_route_defining.json` | `tier_label`; field `published_formulations[]` | "Route-defining - makes a recipe legitimate or invalid"; each entry has `ingredients[] {name, wt_pct}`, `total_wt_pct`, `results[] {property, result}`, `status`, `source` |

What the sources do not say:
- Neither source says what applies when a supplier publishes no recipe. Neither exempts any package.
- The base-oil slide heads its Tier 1 block "all six required". The package slide has no matching "all eight required" line; its force comes from the subtitle ("as blocking as its numbers") and the block heading.
- Slide 5 (finished-formula verification) states the related principle: "A measured result belongs to its tested composition only" and "A modified recipe never inherits the parent's approval".

## 2. What the current checker requires

`tools/mandatory_properties/requirements.py` treats `published_formulations` as one of nine blocking requirement outcomes for a package. It is met only if at least one entry satisfies all of these:

- status `Reported` (a calculated entry is not accepted) and a cited source;
- at least one ingredient, each with a name and a finite, non-negative wt.%;
- ingredients summing to 100.00 ± 0.005 wt.%, and a recorded total that agrees with the sum;
- at least one measured result that passes the ordinary value checks.

**What one measured result does not establish.** The checker asks for one valid result only so that a recipe is not recorded without any measurement. Passing it does **not** show that the recipe meets the finished-oil requirements of slide 5 (viscometrics, low-temperature, chemistry and volatility), and it does **not** establish any performance claim or approval. Approvals belong to the tested composition and to the claim records ("A measured result belongs to its tested composition only"). The checker does not check which properties are reported, or whether they pass any limit.

The checker reads the requirement as a **finished-lubricant recipe that uses the package**, not as the package's own proprietary composition.

**Current data.** No qualifying complete recipe is currently recorded: all 78 packages have the requirement in category `absent`, and no record holds a formulation entry.

**Limits of the search behind that statement.** It is a statement about the records and about a limited search, not proof that no supplier recipe exists:
- The search was a keyword search of the text layers of the archive documents the package records cite (recipe markers such as a "balance" base oil or base-oil percentages). It was not a page-by-page reading for recipes.
- Of the 87 archive files cited by package values, 5 have no text layer (5 packages). They were read on renders for property values, but were not checked for recipes.
- Archive documents that no package record cites, and documents outside the archive (supplier bulletins, approval lists, external sources), were not searched for recipes.
- What was found: dosage tables, for example Afton's package and booster doses for a grade and a base-oil group. These are not complete recipes, and nothing was built from them.

## 3. Two different things under one gate

| | Package route-data completeness | Availability of a published finished-oil recipe with results |
|---|---|---|
| What it describes | The package itself: how the supplier says it may be used | One tested finished oil that contains the package |
| Items | The other eight blocking outcomes: package type, intended service, performance claims, SAE grades, treat-rate matrix, permitted base oils, co-component architecture, route restrictions | `published_formulations[]`: a complete recipe plus measured results |
| Who controls it | Mostly the quality of the supplier documents and of the extraction | Whether the supplier chose to publish a recipe at all |
| What it supports | Deciding whether a generated recipe stays inside the documented route | A reference point: a composition with measured results that a generated recipe can be compared with (slide 5) |
| Current data | 1 of 78 complete (LUBRIZOL_CV1100); 11 more lack exactly one item | 0 of 78 |

Under the current gate the second column decides the result for every package, so the first column has no visible effect: a package with complete route data and a package with almost none are both "not Tier 1 complete".

Distribution of the other unmet route requirements per package (excluding the formulation):

| Other unmet route requirements | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Packages | 1 | 11 | 27 | 20 | 10 | 3 | 2 | 4 |

Of the 11 packages with one gap, 7 lack only the co-component architecture (decision B) and 4 lack only the permitted base oils.

## 4. Consequences

| | Option 1: keep the requirement as it is | Option 2: assess the two separately |
|---|---|---|
| Fidelity to the sources | Follows the specification and glossary as written | Departs from the written Tier 1 list; needs approval from whoever owns the specification |
| Package eligibility on current data | 0 of 78, whatever else is recorded | 1 of 78 (LUBRIZOL_CV1100). The other 77 stay ineligible on route data; up to 11 more depend on decision B and on base-oil statements |
| What can change the result? | Only a qualifying recipe being found and recorded. None is recorded now; the search had the limits in section 2, so a targeted search of the image-only and uncited documents could still find one | Recording missing route items, and for the separate assessment, a recipe being found |
| Information for Workstream B | No eligible package for any step that filters on eligibility | A small eligible set, plus a visible ranking of how complete each package's route data is |
| Reference-formulation evidence | Enforced, but uniformly absent, so it does not discriminate | Reported per package as its own assessment (today: absent for all 78); it does not block |
| Risk | The gate depends on whether a recipe is published and found, not on the quality of the route data; package eligibility stays at zero until a qualifying recipe is recorded | A package can be eligible without any tested reference recipe. Slide 5 still applies: a generated recipe would carry no inherited approval and would need its own verification |
| Shared interface | Unchanged | Columns can stay unchanged. `tier1_complete` for packages would mean "route data complete" under a new `requirements_version`; formulation availability would go in a companion file, as documentation coverage does now. Workstream B would recompute on the version change |
| Work needed | None | A new requirements version, a changed package rule, a companion output, tests, and an update of the interface document |

## 5. Points to settle if option 2 is chosen

- Does formulation availability gate anything later, for example the validation of a generated recipe, or is it reported only?
- Does the wording of `tier1_complete` in the interface document need the specification owner's agreement before it changes for packages?
- Should a partial supplier statement (package dose plus booster dose for a named grade) be recorded as formulation evidence of a lower class, without being called a recipe?

## 6. What stays the same under either option

- No recipe is constructed, inferred or completed from dosage tables.
- The proprietary composition of a package is never required.
- The other package requirements, and decisions B, C and E, are unaffected.
