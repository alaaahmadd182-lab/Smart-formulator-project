# Mandatory requirements: authority map and open decisions

Requirements version: `mandatory-tier1-2026-11-10.6` (four policies approved on 2026-11-11; gap fixes `.5`; route-evidence binding, statement review and the route review of eight packages `.6`: section 4a) ([tools/mandatory_properties/requirements.py](../../tools/mandatory_properties/requirements.py)).

**Interface meaning (restored in revision 3).** `tier1_complete` means "all mandatory Tier 1 requirements satisfied under the requirements version", and `formulation_eligible` has the same meaning.
- A range or bound awaiting a use decision, a pending source selection, or unresolved applicability is **not** complete.
- Information that is documented but not usable is reported separately, in `documentation_coverage.csv`.
- **Gates.** Every gate is a requirement listed below; no other eligibility gate exists.
  - The "unresolved source selection" category applies Rule 1 (the selected source must be established) and your instruction "if a requirement … cannot be established, do not mark the product eligible".
  - It does not add a requirement; it decides whether an existing requirement is satisfied.

Counts are blocking outcomes from [reports/mandatory_properties/requirement_outcomes.csv](../../reports/mandatory_properties/requirement_outcomes.csv) at the current snapshot. Products: 181 base oils, 78 packages, 5 components.

**Sources.**

| Abbreviation | Document |
|---|---|
| MPS | `Smart_Formulator_Minimum_Property_Set.pdf` in the source archive (slide = page) |
| GL | `Property_Glossary.docx` |
| T | `json_templates/` |

**Status words.**

| Status | Meaning |
|---|---|
| explicit | The source lists the item as Tier 1 / blocking |
| conditional | The source makes it depend on something |
| optional | The source says "opt." |
| interpretation | The implementation adds a reading the sources do not state. An interpretation is provisional until reviewed; I-1, I-6, I-8 and I-9 became approved policies on 2026-11-11 (section 4a). |

**Outcome categories** (see requirements.py):

| Code | Category |
|---|---|
| met | met |
| abs | absent |
| bnd | bound/range needing use-specific assessment |
| meta | unit / condition / provenance missing |
| inv | invalid value |
| calc | invalid or unreproducible calculation |
| appl | unresolved applicability |
| sel | unresolved source selection |

## 1. Base oils (MPS slide 2 "TIER 1 — BLOCKING, all six required"; GL table A, Tier 1; T `base_oil_tier1_blocking.json` "Blocking - all six required")

| Requirement (JSON path, tier-1 file) | Authority and wording | Status | Interpretation added | Products not met (by category) | Decision still required |
|---|---|---|---|---|---|
| `fields.api_group_chemistry.api_group` | MPS 2: "API base-oil group + chemistry · Group I–V; mineral / hydrocracked / PAO / ester"; GL: "API group / chemistry · Base-stock classification (I–V) and oil family" | explicit | none | 76 (abs 73, appl 3: Shell Risella X 415/420/430 labelled "Not Required" under an unapproved rule) | F: Risella applicability |
| `fields.api_group_chemistry.chemistry` | same | explicit | none | 31 (abs 31) | — |
| `fields.kv40`, `fields.kv100` | MPS 2: "KV40 cSt (mm²/s) at 40 °C", "KV100 … at 100 °C"; GL: "Kinematic viscosity at two reference temperatures" | explicit | I-1 (a range or bound is documented but needs a use decision) | kv40: 31 (abs 13, bnd 14, sel 4); kv100: 32 (abs 12, bnd 17, sel 3) | B-REP |
| `fields.viscosity_index` | MPS 2: "Viscosity index · dimensionless, from KV40 / KV100"; GL: "Unitless; derived from KV40/KV100" | explicit | I-1. "Derived from KV40/KV100" allows a calculated VI only through a registered, reproducible ASTM D2270 check. None is registered (the D2270 tables are not in the repository), so a calculated VI cannot be accepted. No record has one. | 75 (abs 46, bnd 27, sel 2); the 2 ERGON invalid values were corrected against the source (section 6) | B-REP |
| `fields.density` (with `test_temperature_c`) | MPS 2: "Density + reference temperature · kg/m³ at stated °C, usually 15 °C"; GL: "record reference °C" | explicit | Specific gravity never substitutes for density (GL: "never used as, or converted to, density") | 102 (abs 95, meta 3: aramcoPRIMA 110/230/500 printed without a unit, also pending; sel 4) | — |
| `fields.ccs[]` (value + `test_temperature_c`) | MPS 2: "CCS vs temperature · mPa·s, paired with −15 / −20 / −25 / −30 °C"; GL: "mPa·s; stated subzero °C" | explicit | I-2: one temperature point is enough | 145 (abs 130, bnd 12, appl 2, sel 1) | D: applicability |
| `fields.specific_gravity` | GL: "opt."; T: optional | optional | — | never blocks | — |

## 2. Additive packages (MPS slide 3 "TIER 1 — ROUTE-DEFINING … these make a generated recipe legitimate or invalid"; "Its route fields are as blocking as its numbers"; GL table B, Tier 1)

| Requirement (tier-1 file) | Authority and wording | Status | Interpretation added | Products not met | Decision still required |
|---|---|---|---|---|---|
| `fields.package_type_application.package_type`, `.intended_service` | MPS 3: "Package type + intended application · engine PVL / CVL, gear, ATF, hydraulic, industrial"; GL: "Type / application" | explicit | none | package_type 6, intended_service 1 (abs) | — |
| `fields.performance_claims[]` | MPS 3: "Performance claims + claim semantics · API · ACEA · JASO · ILSAC · OEM, each with type and scope"; GL: "distinguish approval vs recommendation and scope" | explicit | One claim with a designation, a claim type and a source is enough | 8 (abs) | — |
| `fields.sae_grades_documented[]` | MPS 3: "SAE grades the route is documented for"; GL: "SAE grades / restrictions" | explicit | One grade is enough. All 78 packages are engine-oil packages, so SAE grading applies. | 22 (abs) | — |
| `fields.treat_rate_matrix[].treat_rate_wt_pct` | MPS 3: "Treat rate — min / max / typical · wt.% — a matrix per claim and per grade, not one number"; GL: "Min / max / typical wt.%" | explicit; the source names a range or a typical value as acceptable | I-6: a mass basis is required (E). One matrix entry is enough (the slide asks for a matrix, but a one-entry matrix is not rejected). | 21 (abs 6, meta 15: bare "%") | E |
| `fields.permitted_base_oils_restrictions` | MPS 3: "Permitted or required base oils · group, and exact grades where the supplier names them" | explicit | A reported block with content and a source | 48 (abs) | — |
| `fields.required_co_components[]` | MPS 3: "Required VM / PPD / booster architecture · wt.% per co-component"; GL: "required VM, PPD or booster doses" | explicit wording, conditional in effect: required where the route needs co-components | I-8 (approved policy 2): met only by a current, evidenced route in which every applicable requirement has a usable mass-basis dose and whose requirement list is confirmed by source review, **or** by an explicit, reviewed, unconditional, product-wide statement that none is required | 78 (abs 39: a documented requirement has no usable dose; unknown 31: nothing recorded; route 4: usable doses, list not confirmed; meta 4: doses with a bare "%") | which further packages to review |
| `fields.route_selector_restrictions` | MPS 3: "Application restrictions / route selector · explicit limits, exclusions, allowed combinations" | explicit | A reported block with content and a source | 44 (abs) | — |
| `fields.published_formulations[]` | MPS 3: "Exact published formulation + its results · complete recipe summing to 100.00 wt.%"; GL Tier 1: "Published formulation · Exact supplier recipe and measured results · Each ingredient wt.%; total 100 wt.%" | explicit (listed under Tier 1 route-defining) | none; results required (both sources say "+ its results" / "measured results") | 78 (abs 78) | A |

## 3. Additive components (MPS slide 4 "A · EVERY COMPONENT", "B · VISCOSITY MODIFIER — ADDS", "C · POUR POINT DEPRESSANT — ADDS"; GL table C "All / VM / PPD", **no tier numbers**; T `additive_component_all_general.json` tier 1, `_vm.json` tier 2, `_ppd.json` tier 3)

| Requirement | Authority and wording | Status | Interpretation added | Products not met | Decision still required |
|---|---|---|---|---|---|
| `general.json fields.function.primary` | MPS 4: "Functional category + primary and secondary function"; GL: "Primary/secondary function" | explicit | I-3: the secondary function is optional | 1 (abs) | — |
| `fields.chemical_family` | MPS 4: "Chemical family — calcium sulfonate, ZDDP, phenolic AO, OCP, PMA" | explicit | none | 3 (abs) | — |
| `fields.active_content` | MPS 4: "Active content + basis, and carrier-oil identity · wt.%"; GL: "wt.% with basis" | explicit | The basis must be named in the record; a range is bnd (I-1) | 5 (abs 4, bnd 1) | B-REP |
| `fields.carrier.identity` | same | explicit | none | 3 (abs) | — |
| `fields.treat_rate` | MPS 4: "Treat rate — min / max / typical wt.%" | explicit; range accepted | I-6 | 4 (abs 2, meta 2: bare "%") | E |
| `fields.compatibility_restrictions` | MPS 4: "Compatibility and restrictions — base-oil groups, co-additives, seals" | explicit | none | 4 (abs) | — |
| `fields.function_specific_markers.*` | MPS 4: "Function-specific marker — TBN + Ca/Mg for detergents · P + Zn for ZDDP · Mo for moly"; GL: "relevant TBN, Ca/Mg, P/Zn or Mo" | conditional on function | I-4: other functions are unresolved, not inapplicable | 5 (appl 5: booster, antiwear booster, VM ×2, function missing ×1) | G |
| `vm.json` block (polymer chemistry and form, active polymer + carrier, treat range by SAE grade, ΔKV100 response, SSI/PSSI, post-shear KV100/HTHS, CCS/MRV/gelation, dissolution temperature) | MPS 4 B "VISCOSITY MODIFIER — ADDS"; "VMs and PPDs stay components, but need response data on top"; GL: "A component response needs reference oil, dose and method" | conditional (VMs) | I-5: reported, **not blocking** (C) | 2 VMs (RF6602, AFTON_HITEC_5748): 22 of 24 subtype outcomes unmet | C |
| `ppd.json` block | MPS 4 C | conditional (PPDs) | I-5: reported, not blocking | no PPD in the data | C |

## 4. Decisions A–E (as requested) and the related F, G

**Status, 2026-11-11.** B, B-REP, D, E and F were decided by the four approved policies; section 4a states the rules in force. The text of those items below is the earlier analysis, kept for the record; where it says "Decision required", the decision has been taken unless section 4a lists a remainder. A, C and G are still open.

**A. Published formulation.**
- MPS slide 3 and the glossary both list "Exact published formulation + its results" under Tier 1 route-defining. It is therefore explicitly mandatory for every additive package as written. Nothing in either source exempts a package.
- The wording describes a **finished-lubricant recipe** that uses the package: "complete recipe summing to 100.00 wt.%", "each ingredient wt.%", with measured results. It is **not** the proprietary composition of the additive package itself, which suppliers do not publish and which the requirement does not ask for. The implementation checks a finished-oil recipe: ingredients, sum to 100.00 ± 0.005 wt.%, at least one measured result, and a source.
- **Evidence from the sources:**
  - No cited package document's text layer contains a complete recipe ("balance" base oil, or base-oil percentages).
  - The Afton dosage tables give package + booster doses for a grade and a base-oil group (for example "10.3% HiTEC 12200 + 4.2% HiTEC 12250, SAE 15W-40, GP II"). These are not complete recipes.
  - Image-only package documents were not searched.
- **Effect:** all 78 packages are not eligible because of this requirement alone. It is not relaxed here.
- **Decision required:** keep it as written, or reclassify it. For example, it could be made conditional on the supplier publishing a recipe, with the formulation evidence used where it exists.

**B. "No additional co-component required".**
- The schema has a list of co-components, but no way to record a sourced "none required".
- The implementation does not require a co-component merely because of that gap:
  - a package with no reported co-component is **unresolved applicability** (66), not absent;
  - a sourced statement is accepted if it is recorded in a proposed field `fields.co_component_requirement_statement`. This is an ordinary value object with value, printed_text, source and status Reported.
- No record has such a field.
- **Supplier statements searched (revision 3; `co_component_evidence.csv`).**
  - 2 packages state that no supplemental PPD is needed: HiTEC 12210 and 12210M. This covers the PPD only.
  - 13 packages name or require co-components, mostly without a dose. For example Infineum: "in combination with approved base stocks and viscosity modifiers".
  - 63 packages have no explicit statement.
  - An empty list is not evidence of absence.
- **Decision required:** approve the field (a template change, which this workstream does not make), or choose another representation.

**C. VM/PPD subtype blocks vs "missing Tier 2/3 does not block".**
- The sources conflict:
  - MPS slide 4 says VMs and PPDs "need response data on top" of block A;
  - the templates file the blocks as tier 2 (vm.json) and tier 3 (ppd.json);
  - the glossary gives them no tier ("All / VM / PPD");
  - your rule says missing Tier 2/3 data never blocks.
- The previous version (I-5 of revision 1) made the subtype blocks blocking. That silently reinterpreted the template tier numbers, and it has been withdrawn.
- **Now:** the blocks are evaluated and reported as **non-blocking**. Under your rule, the JSON tier numbers decide whether a block is blocking. No eligibility count changes: both VMs also fail block A.
- **Decision required:** confirm non-blocking, or declare the VM/PPD blocks Tier 1 for VMs/PPDs. The latter would mean changing the template tier numbering, which this workstream does not do.

**D. CCS applicability (process oils).**
- MPS slide 2 lists CCS among "all six required" with no exception.
- **Evidence that applicability varies by intended use:**
  - The NEXBASE family TDS (DL2-10962.pdf, read on its render) states: "NEXBASE 3020 and NEXBASE 3030 are used in hydraulic and transmission oil formulations. The other grades are suitable for … 5W/X and 10W/X engine oils".
  - The Chevron Group II table (DL2-10004.pdf) prints "N/A" in its CCS rows for several grades.
  - Shell Risella X 415/420/430 are GTL process/white oils. Their records label CCS (420/430) and API group (415/420/430) "Not Required", citing a "proposed project applicability rule".
- **Implementation:** no applicability rule is approved. The Risella labels therefore give **unresolved applicability**, and every Missing CCS stays **absent**. Nothing is relaxed.
- **Decision required:** keep CCS mandatory for all base oils, or approve a product-level intended-use rule. For example: "CCS not applicable to a base oil whose own technical document limits it to non-engine uses". Each case would be listed with its quotation.

**E. Mass basis of treat rates.**
- Every bare-"%" treat rate and dose was checked on its cited page: 93 values, 21 products (`treat_rate_basis_scan.py`, `reports/mandatory_properties/treat_rate_basis_scan.csv`).
- **Mass basis established from the page** (recorded in `tools/mandatory_properties/treat_rate_basis_evidence.json`):

  | Product | Field | Evidence on the page |
  |---|---|---|
  | INFINEUM_D3384 | co-component doses | column heading "Mass %:" (DL2-10218.pdf p.1, read on the render) |
  | INFINEUM_D3451 | co-component doses | column heading "Mass %:" and "11.9 mass%" (DL2-12029.pdf p.1) |
  | AFTON_HITEC_12360 | treat rate 16.1 | "treat rate @ 16.1% w.t" (DL2-13692.pdf p.2) |

- **Basis not established** for the others: the Afton 12200, 8766B/8767B and 12250 dosage tables, Eni MX 5212/5217, Bettchem BT 3088, Minglan T3161 (no unit printed) and the Richful TDS. Their pages print "%" with no basis.
  - Afton 12200 footnote 3 ("Up to 0.6% wt maybe required…") concerns one booster row only.
- The basis is not guessed. The recorded units stay as printed.
- **Decision required:** accept these as unknown-basis, or obtain supplier documents that state the basis. Unknown-basis currently leaves these requirements unmet:
  - treat-rate matrix: 15 packages;
  - co-component dose: 4 packages;
  - treat rate: 2 components.

**F. Shell Risella API group "Not Required".** See D. The same decision covers the API group label on the three Risella records.

**G. Function-specific markers for functions the slide does not name** (boosters, antiwear boosters, VMs).
- The slide lists detergent / ZDDP / moly markers. Whether other functions need a marker, or none, is not stated.
- **Decision required:** confirm "no marker required for functions not named", or name the markers.

**B-REP. Acceptable representations per property.**
- Representation rules for each requirement are in `REPRESENTATIONS`:

  | Property | Accepted | Documented, but needs a use decision (bnd) |
  |---|---|---|
  | KV40, KV100, VI, density, CCS, active content, markers | point value | range, bound |
  | Treat rates and doses (source: "min / max / typical") | point or range | — |
  | Blend / dissolution temperatures (interpretation) | point or range | — |

- For each property, a bound may support a conservative use. For example, a CCS maximum gives an upper estimate for a cold-cranking check, and a VI minimum supports a VI-minimum check. Neither supports a blend calculation.
- **Decision required:** for each property, which representations are acceptable for its intended use. Until then, a range or bound leaves the requirement unmet (category `bound_or_range_needs_assessment`): the product is neither Tier 1 complete nor formulation-eligible, and the information is reported in `documentation_coverage.csv`. (Corrected 2026-11-11: an earlier sentence here still used the revision-2 meaning, "complete but not formulation-eligible".) If all ranges and bounds were accepted today, the eligible count would stay 11 (sensitivity table in `missing_mandatory_properties.md`).

**External evidence is not a decision item** (corrected 2026-11-11).
- An earlier draft listed "H: may an external technical document be selected over an archived SDS?" as a decision. It is withdrawn: reliable external evidence was already authorised. The templates define `source.file` as an archive file or a URL listed in `source_registry.json`, and 22 selected values come from registered URLs.
- There is no blanket rule for or against an external source. Each one is assessed separately, and the assessments are recorded in `external_review_decisions.json` and `external_review.csv`:

  | Criterion | Question | Recorded as |
  |---|---|---|
  | Authority | Who issued the document: the manufacturer, a distributor, a third party? | `authority` (per source) |
  | Authenticity | How is the copy tied to the source: registry hash, saved copy with a verified hash, an unhashed live feed, or not obtained? | `authenticity` (per source) |
  | Exact product identity | Does the document name this record's exact product or grade? (A question about merging two records is kept apart.) | `identity_status` (per case) |
  | Applicability | Does the printed value apply to this record: typical or specification, plant, edition and date, conflicts? | `applicability` (per case) |
  | Provenance | URL, retrieval, hash, edition | `provenance` (per source) |

- "Confirmed" in the external review means only that the value is printed as recorded. It is not an approval to select the source.
- A distributor-issued document is never treated as manufacturer-issued, and a distributor description is not accepted automatically. The one case is the Ergon/MOGO flyer for BAPbase 4: its specific gravity is not filled.
- **S_OIL_ARAMCO_ULTRA_8: two separate uncertainties.**

  | | Merging two product identities (ID-01) | Using the S-OIL table that names aramcoULTRA 8 |
  |---|---|---|
  | Question | Are the records `S_OIL_ARAMCO_ULTRA_8` and `S_OIL_ULTRA_S_8` one product (a rebrand), to be kept as one folder with an alias? | May the S-OIL page's "aramcoULTRA 8" column be used for the record named aramcoULTRA 8? |
  | Evidence | The inventory treats both SDSs as one material ("rebrand"). Both SDSs print "(250 Neutral)", the same KV ranges and relative density 0.847. The S-OIL page prints identical tables for Ultra-S and aramcoULTRA grades. No document states that the two names designate one product (audit CF-177: suggestive only, needs the supplier). | The page is manufacturer-issued (S-OIL), and two saved copies with verified hashes agree. Its table "Typical Properties of aramcoULTRA Base Oil" has a column headed "aramcoULTRA 8", the record's own name. The page does not print "250 Neutral", and it is undated. |
  | Status | Open. Not resolved here. | The source-to-record link is by exact grade name. ID-01 does not restrict it. |
  | What it restricts | Using Ultra-S 8 documents (the 2009 brochure, the 2015 SDS) for the aramcoULTRA 8 record, or the reverse; merging the folders. | Per value, by the evidence: see below. |

  **Selected on 2026-11-11** (technical source first; the disagreement with the SDS is recorded separately and is not a selection veto):
  - **KV40:** 41.10 cSt at 40 °C (D445), typical. It lies below the SDS range 42.0–55.0 cSt; that disagreement is the existing 2026-10 audit conflict, kept unresolved.
  - **KV100:** 7.1 cSt at 100 °C (D445), typical. Inside the SDS range 7.0–7.5: logically compatible, not agreement.
  - **Flash point:** 250 °C, COC (D92), typical. Inside the SDS range 240–260: logically compatible, not agreement.
  - The SDS ranges are alternate entries with their provenance. The page prints no publication or revision date, so its edition date is unknown; each value says so.
  - Calculated effect: all mandatory requirements of this product are met, so it is Tier 1 complete and eligible (11 base oils), with a KV40 open-conflict warning. No requirement was changed to obtain this.
  - ID-01 stays open, and both records stay separate.

## 4a. Policies approved on 2026-11-11 and how they are implemented (version `.6`)

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

| | Before (`.3`) | After (`.5`) |
|---|---:|---:|
| Base oils: `tier1_complete` = `formulation_eligible` | 11 of 181 | 11 of 181 |
| Packages | 0 of 78 | 0 of 78 |
| Components | 0 of 5 | 0 of 5 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 8 |
| Requirement outcomes whose category changed | — | 74 |

- **8 packages** gained `required_co_components` in their missing list: INFINEUM_D3354, D3384 and D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100 and CV1103. In `.3` (and in `.4`) each counted as met because one recorded co-component had a usable dose. That is not a complete route: 5 of the 8 also record a viscosity modifier without a dose, and for LUBRIZOL_3700 the source page says "when formulated with appropriate base oils and viscosity modifier" although the record lists only the booster. They are now `unresolved_route_association`. All 8 were ineligible before and stay ineligible (each also lacks the published formulation).
- **35 outcomes** moved from `unresolved_applicability` to `absent`: a co-component requirement is recorded and none of its doses is recorded, so no route that includes it can be complete.
- **31 outcomes** moved from `unresolved_applicability` to `requirement_unknown`: nothing is recorded in the record.
- No base oil and no component outcome changed category.

**Route review of 2026-11-12 (version `.6`), against the baseline saved before it** (`baselines/pre_route_review_2026-11-12/`, comparison in `baselines/eligibility_changes__route_review_2026-11-12.csv`):

| | Before (`.5`) | After (`.6`) |
|---|---:|---:|
| Base oils / packages / components: `tier1_complete` = `formulation_eligible` | 11 / 0 / 0 | 11 / 0 / 0 |
| Products whose eligibility booleans changed | — | 0 |
| Products whose `missing_mandatory_properties` list changed | — | 0 |
| Requirement outcomes whose category changed | — | 4 |

The 4 category changes are `required_co_components`, from `unresolved_route_association` to `absent`:
- **INFINEUM_D3384, INFINEUM_D3451, LUBRIZOL_CV1100, LUBRIZOL_CV1103.** Their routes are now reviewed, and every one requires a viscosity modifier for which the datasheet prints no dose. The association is no longer unresolved; a documented requirement lacks its dose.
- **INFINEUM_D3354, LUBRIZOL_3589C, 3700, 3700D** stay `unresolved_route_association`: at least one of their routes has usable recorded doses but a requirement list that cannot be confirmed complete.
- All eight were unmet before and are unmet now. Detail per route: [co_component_route_review_2026-11-12.md](co_component_route_review_2026-11-12.md).

**Rules added in `.6`.**
- **Route evidence is bound to the complete input records.** Each record a route relies on (the co-component entries, and its treat-rate entry) is stored with the SHA-256 of the whole record: values, range endpoints, unit, qualifier, conditions, role text and source reference. A change to any of them makes the route `route_evidence_stale` until it is reviewed again. A change elsewhere in the product does not.
- **Stale or invalid evidence is a historical review, not a current confirmation.** It is reported as `historical_source_review_not_current`, and the entries it names have no current route association.
- **Every membership is kept.** A recorded requirement can belong to several independent routes; each membership is reported with that route's own assessment. 7 recorded requirements belong to more than one route.
- **Alternatives.** A group of requirements is `all`, `one_of` (supplier-stated alternatives) or `unresolved` (the source does not say). An unresolved group never completes a route.
- **Requirements the source states and the record lacks** keep the route incomplete and are listed as proposed corrections (4: the viscosity modifier of the first block of LUBRIZOL_3700 and 3700D, in two routes each).
- **"None required" needs an explicit reviewed assessment**: product, meaning, unconditional (true/false), the qualification verbatim, scope (component types and routes) and conditions. A missing field proves nothing; contradictory or incomplete metadata is rejected; a statement limited to one route or component type is never product-wide. Inline and side-file statements pass through the same check against the current product.

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
- 47 packages record 73 requirements: 17 with a usable dose, 9 with a dose whose basis is unspecified, 47 without a dose. 8 packages have reviewed routes (29 routes: 21 incomplete, 8 with usable recorded doses but an unconfirmed list, 0 complete). The 51 requirements of the other 39 packages have no route association.
- 31 packages record no requirement. For 27 the keyword search found nothing in the inspected text; for 1 it found a lead that is not reviewed (TIANHE_P_TEC_3232); for 2 the cited files have no text layer and were not inspected (CHEVRON_N204, N216); for 1 the source could not be obtained (AFTON_HITEC_12204L).
- 2 reviewed supplier statements (HiTEC 12210, 12210M): "no supplemental PPD should be needed". Their reviewed assessment records the qualification "should be needed" verbatim and a scope of one component type, so they are not "none required".

**Percentage basis.** Scope: the 271 reported values in the dose and treat-rate fields. 187 mass, 84 unspecified, 0 volume. `basis_is_mass` says only that; 2 mass-basis values are not usable for another reason (MINGLAN_T3161A, status Reported with no number). Outside those fields, 5 volume-basis dosage entries for AFTON_HITEC_5748 (SAE grade, vol.%, source and conditions as recorded) are listed in `volume_dose_evidence.csv`; its wt.% fields stay Missing.

**Applicability.** 0 approved rules; 18 labelled values in 4 products and 10 requirement outcomes stay unresolved.

**Still open:** which further co-component routes to review (8 of 47 packages are done); which applicability rules to approve (none is); which calculations may be registered; decision A (published formulation); decision C; decision G.

## 5. Rules the implementation does not add

- No requirement is relaxed to raise eligibility.
- No interpretation is promoted to an approved rule by the implementation. Four policies were approved by you on 2026-11-11 (section 4a); the other interpretations stay provisional. `APPROVED_APPLICABILITY_RULES` is empty: no exemption is assumed.
- `Not Required` / `Not Applicable` labels never satisfy a requirement without an approved rule.

## 6. Record corrections (applied in revision 3, after checking the source pages)

**ERGON_HYGOLD_5000BS** and **ERGON_HYGOLD_P70N** `viscosity_index`. The rendered pages DL2-10409.pdf and DL2-13346.pdf (p.1) print Viscosity Index with a specification MIN of 80 / 60 and a TYPICAL value of 81. The changes:
- `qualifier` "minimum" was set to null;
- `qualifier_previous` keeps the old label;
- the specification minimum stays in `min`;
- a dated note records the correction.

The value is now a typical (point) value. Neither product is eligible, because both still lack API group and CCS.
