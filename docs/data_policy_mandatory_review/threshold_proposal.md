# TDS–SDS screening thresholds: proposal for review (Rule 2)

**Status: PROPOSED, revision 2 of the rules; inventory updated in the revision-3 evidence review (2026-11-10); sensitivity re-checked on 2026-11-11. Nothing has been applied.**
- No audit finding and no product-JSON conflict has been reclassified, and no successor of the v5 audit has been written.
- `tools/data_policy/thresholds.py` keeps `APPROVAL = 'proposed'` (version `thresholds-2026-11-10-proposed.2`).

Data and code:
- Inventory: [reports/data_policy/tds_sds_comparisons.csv](../../reports/data_policy/tds_sds_comparisons.csv) (141 comparison rows; 71 of them pair an SDS value recorded in the evidence review with the record's technical value: 70 product × property cases, S_OIL_ULTRA_S_3 flash point having two SDSs), from `python tools/data_policy/tds_sds_inventory.py`.
- Sensitivity: [reports/data_policy/threshold_sensitivity.csv](../../reports/data_policy/threshold_sensitivity.csv).
- Coverage of the TDS–SDS checking: [reports/data_policy/source_coverage_ledger.csv](../../reports/data_policy/source_coverage_ledger.csv). See section 6 for what the inventory does **not** cover.

**Changes in revision 2.**
- **Wording.** "Ordinary difference" is replaced by "below the proposed project review threshold". "Bound satisfied" is replaced by "logically compatible with the bound (not evidence of agreement)".
- **Basis.** Every threshold is labelled an empirical project screening choice. The unverified ASTM precision and reporting-increment statements are removed as justification (section 3).
- **Pour point.** The 3 °C reporting increment is no longer used as a tolerance.
- **Comparisons.** FORMOSA 150N / 500N KV100 are now specification range vs SDS typical bound checks, following the clarified Rule 1.
- **Boundary.** "At or above the threshold" is now retained for review; it was "> threshold" in revision 1.

## 1. What is compared (step A)

A comparison pairs one technical-document value with one SDS value for the same product and property. The pairs come from four places, duplicates merged:
- v5 audit findings;
- `conflicts[]` entries;
- a selected value paired with an `alternate_entries` item of the other class;
- **(revision 3)** SDS values recorded in the evidence review (`lead_review_decisions.json`, 'comparisons'), each paired with the record's selected technical value.

| Property group | Comparisons | Comparable | Bound / range check | Comparability unknown | Not comparable |
|---|---:|---:|---:|---:|---:|
| viscosity (KV40, KV100) | 19 | 15 | 2 | 2 | 0 |
| density, specific gravity | 46 | 13 | 1 | 31 | 1 |
| flash point | 59 | 10 | 42 | 5 | 2 |
| pour point | 12 | 6 | 6 | 0 | 0 |
| viscosity index | 2 | 0 | 2 | 0 | 0 |
| Noack volatility | 1 | 1 | 0 | 0 | 0 |
| TBN | 2 | 2 | 0 | 0 | 0 |
| **Total** | **141** | **47** | **53** | **38** | **3** |

There are no TDS–SDS comparisons for CCS, the elements, sulfated ash or sulfur.

**Revision 3 correction.** A flash-point pair is now comparable only if the cup type is known on both sides; otherwise it is "comparability unknown". Before this correction, Chevron mPAO 100 (TDS COC 265 °C vs SDS 255 °C, no method) had been screened.

## 2. Value kinds, methods and conditions come before any number (step B)

`compare()` in the inventory script decides comparability first, and computes a difference only for comparable pairs. For a pair to be comparable:
- both sides are point values of a typical/single kind, so a specification limit is never differenced against a typical value;
- the quantity is the same (kinematic viscosity, density and relative density are not mixed);
- the units are convertible;
- the temperature or reference condition is the same;
- for flash point, the cup type is the same, COC (D92) or PMCC (D93).

| Outcome | When |
|---|---|
| not comparable: condition | Different temperature (density 20 °C vs 15 °C, RF6077) or different relative-density reference pairs |
| not comparable: method | Both methods printed and different, or COC vs PMCC (no current case) |
| not comparable: quantity | e.g. kinematic vs dynamic viscosity |
| comparability unknown | Shown for information only and kept pending. One of:<br>• temperature not printed;<br>• relative-density reference not printed on both sides;<br>• the label contradicts the unit ("Viscosity, dynamic … mm²/s"; "Relative density … g/cm³");<br>• unit not printed. |
| bound check only | One side is a bound, range or specification limit. No difference is computed. |
| comparable | Same product, property, quantity, convertible unit, same condition, both points of the same kind. A method missing on one side is allowed only for viscosity, density and pour point, and is flagged. |

How the differences are computed:
- Canonical units are mm²/s, g/cm³ (kg/m³ ÷ 1000), dimensionless for specific gravity, and °C.
- `abs_diff = |TDS − SDS|`.
- `rel_diff_pct = |TDS − SDS| / |TDS| × 100`. It is undefined when the TDS value is 0, and only an absolute rule then applies.
- A difference within half a unit of the last printed digit of the less precise value is reported as print rounding.

## 3. Proposed screening rules (step C): empirical choices, not technical tolerances

Every threshold below is an **empirical project screening choice**. It is set from the spread of the comparable pairs in this inventory, so that clearly larger differences are retained for review.
- **None is an independently supported technical tolerance, and none is an industry standard.**
- Being below a threshold does not show that the documents agree, or that either value is verified.
- Being at or above a threshold is not a confirmed contradiction.

| Property | Conditions for comparison | Canonical unit | Calculation | Proposed review threshold | Zero / ranges / inequalities | Missing metadata |
|---|---|---|---|---|---|---|
| KV40, KV100 | Same temperature; kinematic; both points of the same kind | mm²/s | relative to TDS | review at **≥ 3 %** | 0 treated as unparsed; ranges and bounds use the bound rule | Method missing: flagged; label/unit inconsistency: pending |
| Density | Same reference temperature printed on both sides | g/cm³ | absolute | review at **≥ 0.005 g/cm³** | Bound rule | Temperature missing: pending |
| Specific gravity / relative density | Same reference pair printed on both sides | dimensionless | absolute | review at **≥ 0.005** (dimensionless) | Bound rule | Reference pair missing: pending. Never converted to density. |
| Flash point | Same cup type on both sides | °C | absolute | review at **≥ 10 °C** | 0 valid; bound rule | Cup type unknown: pending |
| Pour point | Both points of the same kind | °C | absolute | review at **≥ 3 °C** (empirical; see the note below) | 0 °C valid; bound rule | Method missing: flagged |
| Noack, TBN, all others | — | — | — | **none: pending** | — | — |

**Bound rule.**
- A point value inside the other document's bound or range is **logically compatible** with it. That is all it shows. It is not agreement, and it verifies neither source.
- A point value outside the bound is retained for review.
- Two bounds or two ranges are kept pending.
- An SDS bound is called a lower or upper bound. It is never called a "safety margin" unless its wording says so.

### Verification of technical references (not used as justification)

| Claim considered | Source sought | Result |
|---|---|---|
| ASTM D445 repeatability / reproducibility (kinematic viscosity) | ASTM standard text | **Not verified.** astm.org returned HTTP 403, and no accessible authoritative copy was found. Not used. |
| ASTM D92 (COC) and D93 (PMCC) flash-point reproducibility | ASTM standard text | **Not verified.** HTTP 403. Not used. |
| ASTM D4052 density precision | ASTM standard text | **Not verified.** Not used. |
| ASTM D97: the specimen is examined at 3 °C intervals | ASTM D97 summary of test method | **Not verified from the standard.** A web search returned extracts of preview copies quoting D97-09 §4.1: "examined at intervals of 3 °C for flow characteristics". The official page returned HTTP 403 and the preview PDFs returned HTTP 404 on 2026-11-10. Even if confirmed, this is a **reporting increment, not a tolerance**: two values one step apart may still be measurably different. The 3 °C pour-point threshold is therefore only an empirical choice, and there is no pour-point pair to which it applies today. |

## 4. Sensitivity of the classifications (comparable pairs not explained by print rounding)

From `threshold_sensitivity.csv`. "At/above" is the number of pairs retained for review; the proposed threshold is marked with ◆.

| Property | Pairs (difference) | Candidate thresholds → pairs below / at-or-above |
|---|---|---|
| KV40 | SpectraSyn 2: 4.0 %; ETRO 6+: 6.88 % | 1–3 %◆: 0 / 2 · 5 %: 1 / 1 · 7 %, 10 %: 2 / 0 |
| KV100 | 0.68, 1.52, 6.25, 8.11, 11.89, 20.34 % (Richful) | 1 %: 1 / 5 · 2–5 %◆: 2 / 4 · 7 %: 3 / 3 · 10 %: 4 / 2 |
| Density | 0.002, 0.003, 0.003 g/cm³ (Richful) | 0.001, 0.002: 0 / 3 · 0.003: 1 / 2 · 0.005◆, 0.010: 3 / 0 |
| Specific gravity | none comparable: the reference pairs are not printed on both sides (all pending) | — |
| Flash point | 1, 3.1, 4, 5, 7, 7, 28, 31 °C (Chevron PAO/mPAO, ERGON L350E, SpectraSyn Elite 150) | 3 °C: 1 / 7 · 5 °C: 3 / 5 · 8–20 °C◆: 6 / 2 · 30 °C: 7 / 1 |
| Pour point | no comparable pair outside print rounding | — |

**Re-checked 2026-11-11 against the current inventory** (141 rows; 47 comparable; 26 of them within print rounding). The 21 comparable pairs outside rounding are exactly the ones in the table above, plus one Noack pair (ETRO 6+, 7.0 %) and one TBN pair (RF6066, 1.85 %), which have no proposed threshold. The external-source review of 2026-11-11 added no TDS–SDS pair: the values it re-read are either selected values without an SDS value for the same property, or external alternatives that are not in the records (the logical incompatibilities it found are `conflicts[]` entries, not inventory rows: aramcoPRIMA 230 Noack, technical vs technical, is new; aramcoULTRA 8 KV40, external page vs SDS range, is the existing 2026-10 audit conflict, which is not an inventory row either). The conclusions below therefore still hold.

What the sensitivity shows:
- **KV100.** Any threshold from just above 1.52 % up to 6.25 % gives the same split.
- **Flash point.** Any threshold from just above 7 °C up to 28 °C gives the same split.
- **KV40.** The split depends on whether the threshold is above 4 %: SpectraSyn 2 is 5.0 vs 5.2 cSt, with the SDS by an in-house method.
- **Density.** Any threshold above 0.003 g/cm³ puts all three pairs below it, so the data give no reason to prefer 0.005 over 0.004 or 0.010.

## 5. Preview: what approval would change (nothing applied)

The preview lists the v5 audit findings only. The 71 pairs recorded in the evidence review are not v5 findings, and their proposed screen is in `tds_sds_comparisons.csv` (origin "lead review"). Among them, these are retained for review under the proposal:
- SpectraSyn Elite 150 flash point: TDS 277 vs SDS 246 °C, both COC (31 °C);
- SpectraSyn 2 KV40: 5.0 vs 5.2 cSt (4.0 %);
- NYFROST 32: the PMCC typical 176 °C is not above the SDS closed-cup bound "> 180 °C";
- Esterex P81: the pour point −33 °C is not below the SDS bound "< −34 °C".

A finding could be closed as "below the review threshold" only if **every** value pair in it is below the threshold or within print rounding.
- Findings that also contain TDS–TDS or SDS–SDS differences keep those parts.
- Identity, unit and calculation findings are untouched.

| Finding | Product · property | Proposed screen of its TDS–SDS pairs | Preview effect |
|---|---|---|---|
| CF-003 | INFINEUM_D3424 flash point | point compatible with SDS bound | could be closed as "compatible with bound" (not agreement) |
| CF-004 | LUBRIZOL_CV2301 density | pending (comparability unknown) | stays active |
| CF-008 | RICHFUL_RF6066 density | below threshold / rounding + pending | stays active (pending part; TDS–TDS 990 vs 988 kept) |
| CF-009 | RICHFUL_RF6066 KV100 | at/above threshold + pending | stays active |
| CF-010 | RICHFUL_RF6066 TBN | rounding + no threshold | stays active |
| CF-013, CF-015 | RF6069 / RF6077 KV100 | at/above (20.3 %, 6.25 %) | stay active |
| CF-014 | RF6077 density | not comparable (20 °C vs 15 °C) | stays active as a condition difference |
| CF-017, CF-018, CF-020 | RF6078 density, RF6081 KV100, RF6088F KV100 | below threshold | could be closed as "below review threshold" |
| CF-019 | RF6088F density | pending (label/unit) | stays active |
| CF-026 | FORMOSA 150N flash point | two bounds | stays active |
| CF-033 | ETRO 6+ KV40 | at/above (6.88 %) | stays active |
| CF-035 / CF-036 | ETRO 6+ Noack / density | no threshold / temperature missing | stay active |
| CF-099, CF-100, CF-172 | Risella X 415/420 density; Ultra-S 6 specific gravity | pending | stay active |
| CF-127 | Chevron mPAO 150 flash point | at/above (28 °C) | stays active |
| CF-128, CF-129, CF-130 | Chevron PAO 4/6/8 flash point | below threshold | could be closed as "below review threshold" |
| CF-131 | Chevron PAO 2 flash point | below threshold | TDS–TDS edition difference (159 vs 164) kept |
| CF-140 | aramcoPRIMA 70 flash point | outside the TDS minimum | stays active |
| CF-148 … CF-156 | Richful flash points (7) | compatible with SDS bound | could be closed as "compatible with bound" |

"Could be closed" means that, on approval, a dated successor of the v5 report would record the state "screened: below proposed review threshold (thresholds v…)" or "compatible with bound", with a stable CF id and an old-to-new mapping. v5 stays unchanged.

## 6. Limits of the inventory (coverage)

The evidence review (revision 3) read every case where a technical page and an SDS page both mention a property but no pair existed (139 product × property cases: the 138 of the revision-2 ledger plus NEXBASE 3080 flash point, which appeared when the classifier stopped treating its SDS page 4 as technical):
- **71 cases, usable evidence:** 70 had the SDS value recorded as a comparison (in one of them, CV2301 flash point, the technical document also disagrees with itself: conflict `EVR-2026-11-10-CV2301`); 1 (mPAO 65 flash point) was filled from the technical sheet, with the SDS value kept as an alternate.
- **31 cases, already recorded:** same-document pages (Lubrizol handling pages) or a recorded exception.
- **18 cases:** an unrelated mention (another quantity or product).
- **12 cases:** insufficient evidence.
- **7 cases:** unresolved identity (FORMOSA).

The inventory is still **not an exhaustive TDS–SDS check**. It is limited to the archive's text layers, the renders read, and the documents whose identity is established.

## 7. Decisions requested

1. Adopt, change or reject each empirical threshold. Density in particular cannot be located from the data.
2. Should a finding with a below-threshold TDS–SDS part and a TDS–TDS part be split, or kept as one finding with a note? The proposal is to keep it with a note.
3. Do label/unit inconsistencies on SDS pages (RF6066, RF6079, RF6088, RF6088F) stay pending? The proposal is yes.
