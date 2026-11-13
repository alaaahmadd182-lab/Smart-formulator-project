# Checkpoint 6 — old-versus-new comparison (sixth pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-5 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON or production file changed, nothing staged or committed. `logs/03_checks.log`: 54 of 54 checks pass
(structural; manual verification recorded per row). **Not complete:** 667 of 1,068 non-duplicate links not yet assessed.

## 1. The eight "possible overlap" proposals — resolved entry by entry

| Product / field | Existing JSON entries | Result |
|---|---|---|
| HiTEC 12200 treat_rate_matrix | all routes of `DL2-13364.pdf` pp.7-9 already present (9.7; 10.8; 11.7 + 12260 0.9; 10.8 + 12260 0.9; 10.8 + 9552 0.35; 10.8 GP I), printed '%' | routes **duplicate, not proposed**; narrowed to a provenance note that the 2019 presentation prints the same doses as '% wt' (basis unchanged — question 1) |
| HiTEC 12210M required_co_components | 'HiTEC 5748A or HiTEC 5748', dose Missing | **withdrawn**: name already present; recipe doses carried by the 31-formulation proposal |
| Lubrizol 16008 treat_rate_matrix | one row 4.4 % (API CF; API SF) | 4.4 % row **duplicate**; narrowed to six new routes (6.21, 5.35, 3.75, 2.8, 2.5, 1.6 %) |
| Lubrizol 16008 performance_claims | API CF, API SF (4.4 % block) | both **duplicate**; narrowed to 11 new claims + scope extension of CF (3.75 %) and SF (5.35 %) |
| Lubrizol CV1103 required_co_components | CV6320 2.0 % (FA-4); 'Lubrizol 7077 series', dose Missing | both **duplicate**; narrowed to an open-question note that the 13 May 2022 edition omits the 7077 sentences |
| Lubrizol CV1100 required_co_components | CV6320 2.0 %; unnamed VM entry | **withdrawn**: CV6320 duplicate; 7077 recipe doses carried by the formulation proposal; the generic VM entry is not filled with one recipe's product |
| HiTEC 5748 shear_stability | SSI 22, usable false; note already cites "25SSI" (DL2-13692.pdf) | value and discrepancy **already recorded**; narrowed to one added citation (DL2-15465.pdf) |
| Infineum D3396 performance_claims | API CI-4, API SL ('meets'), unqualified | claims **duplicate**; narrowed to a note on API SL's 'bench testing in progress' qualification (2018 deck) |

## 2. The property without a template field (HiTEC 12250)

`json_templates/additive_component_all_general.json` has fields function, chemical_family, active_content, carrier,
treat_rate, compatibility_restrictions and function_specific_markers (tbn, ca, mg, p, zn, mo) only: **no field for
density, kinematic viscosity, flash point, storage or handling (schema gap; template not changed).** The record already
keeps these in two `open_questions` entries, the established place. Compared entry by entry with the 04/19 bulletin:
already present: KV100 175, max handling 70 C, 36 months at ambient. New: density 0.920 **g/ml at 15 C** (the old note
holds 0.920 as specific gravity 15.6/15.6 C, a different quantity), flash point printed '>135' (old '135 min.'),
'Max Storage Temp: 50 C', and the absence of the '3 months @ 45 C' line. Proposal: update those two open questions only.

## 3. HiTEC 8788B — three evidence classes kept apart (proposals, not applied)

| Class | Items | Source |
|---|---|---|
| In the cited old PDS, not captured in JSON | typical TBN **71** mg KOH/g; two 17.7 % SAE 10W-40 routes with 14 / 12 claims and the VM footnote; typical KV100 145 mm2/s, density 0.958 g/ml at 15 C, flash 135 (PMC) as the technical source for values now cited to the SDS | Afton PDS 02/19 (retrieved, hash-verified) |
| Additional information from new documents | Ca, P, Zn, N (certificate specification limits); two complete formulations with Lubrizol 7077 / HiTEC 672 (route-bound) | certificates; `DL2-13364.pdf` pp.17-18 |
| Alternate certificate specification | TBN min **68** / target **73** / max **79** (D2896); density target 0.958; KV100 target 145 | four certificates |
| Batch results (not entered) | TBN 70.9 / 71.3 / 72.0 / 72.1 and per-lot Ca, P, Zn, N, density, KV100 | four certificate lots |

Typical 71 and target 73 are different kinds of value; neither is averaged, reconciled or preferred automatically.

## 4. Other suppliers

- **YUBASE 4:** the manufacturer's SDS (SK Enmove, revised 2026-06-30) prints specific gravity 0.834 without temperature and "Density: Not available"; a Shell cargo handling sheet prints 834 kg/m3 at 15 C "for reference only". Mandatory density stays Missing pending question 2. Flash point 230 / 220 / 200 C and pour point -15 / -12 C recorded as conflicts. 112 mention links classified (recipe shares, formulators' component values, test-oil uses).
- **YUBASE 6:** manufacturer SDS 2026 (SG 0.842 without temperature; flash 230 vs recorded 240: conflict). `Yubase_6-SDS.pdf` is byte-identical to a registered external source already cited (coverage not assessed).
- **YUBASE 3:** manufacturer SDS 2014 (relative density 0.830 without temperature; flash 200 vs recorded 204: conflict).
- 111 Yubase 6 / 3 mention links classified.

## 5. Status (three separate measures)

| | Relationship settled | Unresolved | Not assessed |
|---|---|---|---|
| Afton / Lubrizol / Infineum | 136 | 20 | 0 |
| Other suppliers | 244 (+2 excluded) | 0 | 667 |

Proposals: 128; **127 ready for a reviewer decision; 1 provisional (YUBASE 4 density, question 2)**. Content-review gaps
listed in checkpoint 4 §3 are unchanged in this pass. Source-to-JSON coverage of the duplicate documents: not assessed.

## 6. Policy questions (only these need you)

1. **Percentage basis from another document (HiTEC 12200).** The 08/18 bulletin prints the route doses as '%'; Afton's
   2019 presentation prints the same doses as '% wt'. (a) keep '%' (unspecified) and add the provenance note only
   [current proposal]; (b) set the basis to mass for those rows, citing `DL2-13364.pdf` p.7.
2. **Mandatory density from a third-party shipping document (YUBASE 4).** (a) keep Missing; (b) fill 834 kg/m3 at 15 C
   from the Shell cargo handling sheet with a 'third-party reference' source class; (c) keep Missing and record the
   cargo-sheet value as alternate evidence only. Evidence: manufacturer SDS SG 0.834 (no temperature); distributor sheet
   SG 0.8338 at 15 C with a garbled unit.

## 7. Next steps

1. Other suppliers: `EXXONMOBIL_EHC_50` (62 links), `NESTE_NEXBASE_3043` (55), `EXXONMOBIL_EHC_110` (49),
   `CHEVRON_GROUP_II_220R` (46), `CHEVRON_GROUP_II_600R` (30), `S_OIL_ULTRA_S_4` (28), … — find product-specific
   documents first, then `scripts/helpers/write_base_oil_mentions.py` for the rest (it refuses to shrink an existing file).
2. Unread content (checkpoint 4 §3). 3. Duplicate-source coverage (223 documents).
