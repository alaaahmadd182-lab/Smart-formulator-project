# Mandatory requirements: authority map and open decisions

Requirements version: `mandatory-tier1-2026-11-10.3` ([tools/mandatory_properties/requirements.py](../../tools/mandatory_properties/requirements.py)).

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
| interpretation | The implementation adds a reading the sources do not state. Every interpretation is provisional until reviewed. |

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
| `fields.kv40`, `fields.kv100` | MPS 2: "KV40 cSt (mm²/s) at 40 °C", "KV100 … at 100 °C"; GL: "Kinematic viscosity at two reference temperatures" | explicit | I-1 (a range or bound is documented but needs a use decision) | kv40: 32 (abs 13, bnd 14, sel 5); kv100: 33 (abs 12, bnd 17, sel 4) | B-REP |
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
| `fields.required_co_components[]` | MPS 3: "Required VM / PPD / booster architecture · wt.% per co-component"; GL: "required VM, PPD or booster doses" | explicit wording, conditional in effect: required where the route needs co-components | I-8: met by a reported co-component with a wt.% dose, **or** by a sourced statement that none is required | 70 (appl 66: no co-component recorded and no "none required" statement; meta 4: bare "%") | B |
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

## 4. Decisions A–E (as requested) and the related F, G, H

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
- **Decision required:** for each property, which representations are acceptable for its intended use. Until then, a range or bound leaves the requirement unmet (category `bound_or_range_needs_assessment`): the product is neither Tier 1 complete nor formulation-eligible, and the information is reported in `documentation_coverage.csv`. (Corrected 2026-11-11: an earlier sentence here still used the revision-2 meaning, "complete but not formulation-eligible".) If all ranges and bounds were accepted today, the eligible count would stay 10 (sensitivity table in `missing_mandatory_properties.md`).

**H. External technical sources vs archived SDSs (new, 2026-11-11; Rule 1 scope).**
- Rule 1 says "technical document first, SDS fallback", but it does not say whether a technical document that is not in the archive qualifies. Examples are a registered supplier web page or a distributor flyer.
- The current data take both positions:
  - 22 values are already selected from registered URLs;
  - 3 aramcoULTRA 8 fields keep their archived SDS ranges, with the confirmed S-OIL typicals unused.
- **Effect.** S_OIL_ARAMCO_ULTRA_8 is the only product whose sole unmet requirements are pending source selections (KV40, KV100). If pending selections were accepted, it would be the 11th eligible product (sensitivity row "unresolved_source_selection").
  - Its KV40 has an unresolved logical incompatibility: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 (an unresolved conflict recorded by the 2026-10 audit).
  - Choosing a source would therefore not by itself make KV40 consistent.
- **Decision required:**
  - may a registered external technical document be selected over an archived SDS?
  - may a distributor-issued document fill a Missing field (for example the BAPbase 4 specific gravity in the MOGO flyer)?
  - Until decided, nothing changes.

## 5. Rules the implementation does not add

- No requirement is relaxed to raise eligibility.
- No interpretation is promoted to an approved rule. `APPROVED_APPLICABILITY_RULES` is empty, and every interpretation I-1 … I-8 is listed as provisional.
- `Not Required` / `Not Applicable` labels never satisfy a requirement without an approved rule.

## 6. Record corrections (applied in revision 3, after checking the source pages)

**ERGON_HYGOLD_5000BS** and **ERGON_HYGOLD_P70N** `viscosity_index`. The rendered pages DL2-10409.pdf and DL2-13346.pdf (p.1) print Viscosity Index with a specification MIN of 80 / 60 and a TYPICAL value of 81. The changes:
- `qualifier` "minimum" was set to null;
- `qualifier_previous` keeps the old label;
- the specification minimum stays in `min`;
- a dated note records the correction.

The value is now a typical (point) value. Neither product is eligible, because both still lack API group and CCS.
