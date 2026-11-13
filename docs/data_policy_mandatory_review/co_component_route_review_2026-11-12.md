# Co-component route review of eight packages (2026-11-12)

Scope: INFINEUM_D3354, D3384 and D3451; LUBRIZOL_3589C, 3700, 3700D, CV1100 and CV1103. These are the eight packages that record at least one co-component with a usable dose. No other package was reviewed.

- **What was read.** The datasheet pages the records cite: tables, headings, footnotes and qualifications. Pages were read from the text layer and checked on page renders where the association depends on layout (footnote markers, table columns). DL2-10218.pdf (D3384) has no text layer and was read on its render.
- **What was recorded.** Only associations the page evidences, in `tools/mandatory_properties/co_component_route_evidence.json` (29 routes). Each route is bound to the records it relies on by fingerprint.
- **What was not done.** No product JSON was changed. No dose, percentage basis, mapping or exemption was invented. Proposed record corrections are listed in section 3 and in the evidence file; none is applied.
- **No target route is specified**, so the results are route-level findings. None is a statement of formulation readiness.

## 1. Result in one table

| Package | Routes reviewed | Complete | Incomplete (documented requirement without a usable dose) | Recorded doses usable, list not confirmed | Product-level outcome |
|---|---:|---:|---:|---:|---|
| INFINEUM_D3354 | 3 | 0 | 1 | 2 | unresolved route association |
| INFINEUM_D3384 | 9 | 0 | 9 | 0 | absent (every route lacks the viscosity-modifier dose) |
| INFINEUM_D3451 | 3 | 0 | 3 | 0 | absent |
| LUBRIZOL_3589C | 2 | 0 | 0 | 2 | unresolved route association |
| LUBRIZOL_3700 | 4 | 0 | 2 | 2 | unresolved route association |
| LUBRIZOL_3700D | 4 | 0 | 2 | 2 | unresolved route association |
| LUBRIZOL_CV1100 | 2 | 0 | 2 | 0 | absent |
| LUBRIZOL_CV1103 | 2 | 0 | 2 | 0 | absent |
| **Total** | **29** | **0** | **21** | **8** | |

No requirement list could be confirmed complete: no page states that the components it names are the only ones required.

## 2. Findings per package

"Usable dose" means a recorded dose on a mass basis with its source. "List not confirmed" means the page names components without saying that nothing else is required.

### INFINEUM_D3354 (DL2-10203.pdf p.1; text layer and render)

| Route | Requirements evidenced | State | Limitation |
|---|---|---|---|
| Row 1: API CI-4/CF/SL, ACEA A3/B4/E7, MB p228.3 (PA), Volvo VDS-3; 15W-40; "11.8 + 3.0 Booster(3)" | One of three boosters (footnote 3: "tuned for different base stock qualities"): D2332 at 2.8, D2333 at 4.5, D2334 at 3.0 to 3.3 mass%. All three doses usable | Doses usable, list not confirmed | The table prints "3.0 Booster" while the footnote gives 2.8 / 4.5 / 3.0–3.3. Which base stock quality each booster suits is not printed. Whether Infineum SV261 belongs to this row is not printed |
| Row 2: "As below plus Volvo VDS-2"; 15W-40; "11.8 + 0.8 Booster(4)" | Footnote 4: "Use Infineum D2332 at 0.75 mass%, Infineum D2333 at 0.75 mass% and Infineum D2334 at 0.80 mass%". All three doses usable | Doses usable, list not confirmed; **combination unresolved** | The footnote joins the three with "and" while the table prints one "0.8 Booster". Alternatives or all three together is not stated |
| Description: "API CG-4/CF-4/CF/SJ, MB p228.1/3 (package approved) performance level with Infineum SV261" | Viscosity modifier Infineum SV261; **no dose printed** | Incomplete | Which of the five table rows without a booster this sentence covers is not printed row by row |

### INFINEUM_D3384 (DL2-10218.pdf p.1; image-only, read on the render)

The Description says: "When treated at the recommended treat rate in combination with approved base stocks and viscosity modifier, Infineum D3384 can be used to formulate diesel engine oils meeting the API performance category CH-4, among others." The viscosity modifier is not named and has no dose, so all nine rows are **incomplete**.

| Rows | Booster evidenced in the row (mass % column) | Booster dose |
|---|---|---|
| 1: API CI-4/SL, 15W-40 | Infineum D2359 at 1.93 % | usable |
| 2: API CI-4/SL (10 TBN), 15W-40 | Infineum D2353 at 2.23 % | usable |
| 4: API CH-4/SJ, 20W-50; and 9: API CH-4, 10W-30 | Infineum C9274 at 0.5 % (one recorded entry, member of both routes) | usable |
| 5: API CG-4/SJ …, 15W-40 | Infineum D2358 at 0.7 % | usable |
| 7: API CF-4/SJ …, 15W-40 | Infineum D2358 at 1.4 % | usable |
| 3, 6, 8 | none named in the row | — |

Limitation: the viscosity-modifier requirement comes from the document-level Description, which is not repeated per row. "Claims are base stock and viscosity grade specific."

### INFINEUM_D3451 (DL2-12029.pdf p.1; text layer and render)

Description: "Used at the recommended treat rate of 11.9 mass% in combination with approved base stocks and viscosity modifier …". The viscosity modifier is not named and has no dose, so all three rows are **incomplete**.

| Route | Booster | Note |
|---|---|---|
| Row 1: API CI-4/SL, ACEA E7-12; 10W-30, 15W-40, 20W-50; 11.9 | none named | |
| Row 2: API CH-4/SL, ACEA E7-12; 10W-40; "11.9 + Infineum D2367 at 1.2 %" | D2367 at 1.2 % (mass % column), usable | |
| Row 3: API CH-4; 15W-40; 11.0 | none named | The Description states the viscosity modifier for the 11.9 mass% treat rate; this row is at 11.0 |

### LUBRIZOL_3589C (DL2-10629.pdf p.1; text layer)

| Route | Requirements evidenced | State | Limitation |
|---|---|---|---|
| "Recommended for use at: 6.15 % by weight"; "When formulated with appropriate base oils" (monograde lubricants) | No co-component is named | List not confirmed | Naming only base oils is not a statement that no co-component is required |
| Kolomna M-14D2: "2) Product approved by Kolomna railroad at 6.2 % by weight plus a 0.8 % by weight booster." | Booster at 0.8 % by weight, usable dose | Doses usable, list not confirmed | The booster is not named. The footnote gives the package at 6.2 %, while the record lists Kolomna under its single 6.15 % entry |

### LUBRIZOL_3700 (DL2-10632.pdf p.1) and LUBRIZOL_3700D (DL2-10633.pdf p.1); text layer and render

Both sheets have the same structure. Footnote: "1) Addition of a 0.25 % by weight TBN booster required to claim MTU Type 1".

| Route | Requirements evidenced | State |
|---|---|---|
| First block (3700: 8.5 %; 3700D: 8 % by weight): "appropriate base oils and viscosity modifier"; claims other than MTU Type 1 | Viscosity modifier, not named, no dose. **Not in the record** | Incomplete |
| First block, MTU Type 1 claim | The same viscosity modifier, plus a TBN booster at 0.25 % by weight (usable dose, not named) | Incomplete |
| Second block (3700: 7.7 %; 3700D: 7.25 % by weight): "appropriate base oils"; claims other than MTU Type 1 | No co-component is named | List not confirmed |
| Second block, MTU Type 1 claim | TBN booster at 0.25 % by weight (usable dose, not named). The one recorded booster entry is a member of both MTU Type 1 routes | Doses usable, list not confirmed |

Limitation: the footnote is numbered "1)" but no claim on the page carries a marker. It is tied to the blocks only through the claim name "MTU Type 1", which both blocks list.

### LUBRIZOL_CV1100 (DL2-11503.pdf p.1; text layer)

| Route | Requirements evidenced | State |
|---|---|---|
| First block, 14.2 % by weight: "appropriate base oils and viscosity modifier"; API CK-4 and others; SAE 15W-40 and 10W-30 | Viscosity modifier, not named, no dose | Incomplete |
| Second block: "When 2.0wt% CV6320 is top treated in addition to 14.2wt% CV1100 and blended with appropriate base oils and viscosity modifier"; API FA-4, Cummins CES 20087, Detroit Diesel DFS93K223; SAE 10W-30 | CV6320 at 2.0 wt% (usable) and the viscosity modifier (no dose). The viscosity-modifier entry is a member of both routes | Incomplete |

### LUBRIZOL_CV1103 (DL2-14978.pdf pp.1–2; text layer and render)

| Route | Requirements evidenced | State |
|---|---|---|
| First table column (14.30% by weight): API CK-4 and the other marked claims | "Formulated and approved in combination with Lubrizol® 7077 performance polymer"; no dose | Incomplete |
| API FA-4, SAE 10W-30: "When 2.0wt% CV6320 is top treated in addition to 14.3wt% CV1103 and blended with appropriate base oils and performance polymer, Lubrizol 7077 series" | CV6320 at 2.0 wt% (usable) and the Lubrizol 7077 polymer (no dose). The polymer entry is a member of both routes | Incomplete |

Limitations:
- The table footnote on p.2 says claims apply only "when the additive package is used with defined base oil(s), viscosity modifier(s) and **other required components**". The list is therefore expressly not exhaustive.
- Both table columns are headed "14.30% by weight" and carry no other label. The second column marks only the three FA-4 claims; the first also marks API FA-4. Which column is the CV6320 route is not printed.

## 3. Proposed record corrections (not applied)

| Product | Proposal | Source |
|---|---|---|
| LUBRIZOL_3700 | Add a viscosity-modifier requirement for the 8.5 % block, with its dose Missing | DL2-10632.pdf p.1 |
| LUBRIZOL_3700D | Add a viscosity-modifier requirement for the 8 % block, with its dose Missing | DL2-10633.pdf p.1 |
| LUBRIZOL_3589C | Consider a separate treat-rate entry for the Kolomna approval at 6.2 % by weight | DL2-10629.pdf p.1 |
| INFINEUM_D3354 | Note the "3.0 Booster" vs footnote doses, and the unresolved wording of footnote 4. No value change | DL2-10203.pdf p.1 |
| LUBRIZOL_CV1103 | Note the "other required components" footnote and the unlabelled columns. No value change | DL2-14978.pdf pp.1–2 |

Applying a correction changes the record, which makes the routes bound to it stale until they are reviewed again. That is intended.

## 4. What the evidence cannot resolve

- The dose of any viscosity modifier. None of the eight datasheets prints one.
- The identity of the boosters in LUBRIZOL_3589C, 3700 and 3700D.
- Whether the D3354 footnote-4 boosters are alternatives or are used together.
- Whether any list of components is exhaustive.
- Which CV1103 table column is the CV6320 route.

These need supplier documents the archive does not hold. The review stops there.
