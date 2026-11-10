# TDS–SDS screening thresholds: proposal for review (Rule 2)

**Status: PROPOSED. This is the review checkpoint.** No audit finding and no product-JSON conflict has been reclassified
with these thresholds. `tools/data_policy/thresholds.py` holds `APPROVAL = 'proposed'` until the table is approved.

- Inventory: [reports/data_policy/tds_sds_comparisons.csv](../../reports/data_policy/tds_sds_comparisons.csv), 65 comparisons.
- Generator: `python tools/data_policy/tds_sds_inventory.py`. It is read-only on the data.
- Rules: [tools/data_policy/thresholds.py](../../tools/data_policy/thresholds.py), version `thresholds-2026-11-10-proposed`.
- Document classes (TDS vs SDS, per page): [reports/data_policy/document_classes.csv](../../reports/data_policy/document_classes.csv).

## 1. What is compared (step A)

A comparison is one technical-document value paired with one SDS value for the same product and property. Pairs come
from three places, and duplicates are merged, keeping every origin:

1. pairs inside one v5 audit finding (`findings_v5.json`);
2. pairs inside one `conflicts[]` entry of a product file;
3. a selected value paired with an `alternate_entries` item from the other document class. This includes the
   alternates created by the 2026-11-10 source selection (Rule 1).

| Property group | Comparisons | Comparable | Bound / range check | Comparability unknown | Not comparable |
|---|---:|---:|---:|---:|---:|
| viscosity (kv40, kv100) | 15 | 13 | 0 | 2 | 0 |
| density, specific gravity | 27 | 7 | 1 | 18 | 1 |
| flash point | 19 | 6 | 13 | 0 | 0 |
| pour point | 1 | 0 | 1 | 0 | 0 |
| Noack volatility | 1 | 1 | 0 | 0 | 0 |
| TBN | 2 | 2 | 0 | 0 | 0 |
| **Total** | **65** | **29** | **15** | **20** | **1** |

There are no TDS–SDS comparisons for VI, CCS, the elements, sulfated ash or sulfur.

## 2. Comparability comes before any difference (step B)

`compare()` in the inventory script decides comparability first. It computes a difference only for comparable pairs.

| Outcome | When |
|---|---|
| not comparable: condition | Different temperature (density 20 °C vs 15 °C, RF6077), or different relative-density reference pairs. |
| not comparable: method | Both methods printed and different, or different flash-point cup types (COC/D92 vs PMCC/D93). No such case is in the current data. |
| not comparable: quantity | Different quantities, for example kinematic vs dynamic viscosity. |
| comparability unknown | Any of these. The numbers are shown for information only, and the pair stays pending.<br>• Temperature not printed on one side (density).<br>• Relative-density reference temperatures not printed on both sides.<br>• The printed label contradicts the printed unit: "Viscosity, dynamic … mm²/s" (RF6066 SDS), or "Relative density … g/cm³" (RF6079, RF6088, RF6088F SDS).<br>• Unit not printed on one side. |
| bound check only | One side is a bound (minimum, ≥, >, ≤) or a range. No difference is computed; the point value is checked against the bound. |
| comparable | Same product and property, convertible units, same condition, both point values. A method missing on one side is allowed for viscosity, density and pour point, and is flagged in `reason`. |

How the differences are computed:
- Canonical units are mm²/s, g/cm³ (kg/m³ ÷ 1000) and °C.
- `abs_diff = |TDS − SDS|`.
- `rel_diff_pct = |TDS − SDS| / |TDS| × 100`. It is undefined when the TDS value is 0; only an absolute rule then applies.
- `rounding_tolerance` is half a unit of the last printed digit of the less precise value. A difference inside it is ordinary print rounding.

## 3. Proposed property-specific screening rules (step C)

These are **project screening values, not industry standards.** A value below the threshold means only this: "the
difference is ordinary for typical values printed in two documents of one product." It does not confirm that the
documents agree. A value above the threshold means "retain for review", not "confirmed contradiction".

| Property | Conditions for comparison | Canonical unit | Calculation | Proposed threshold | Zero / ranges / inequalities | Missing metadata |
|---|---|---|---|---|---|---|
| KV40, KV100 | Same temperature; kinematic on both sides; both point values | mm²/s | relative to TDS | **≤ 3 %** ordinary | Viscosity is never 0; a 0 is treated as unparsed (pending). Ranges and bounds use the bound rule. | Method missing: allowed, flagged. Label/unit inconsistent: pending. |
| Density | Same reference temperature printed on both sides | g/cm³ | absolute | **≤ 0.005 g/cm³** (5 kg/m³) ordinary | Bound rule | Temperature missing: pending. "Relative density" label with a density unit: pending. |
| Specific gravity / relative density | Same reference pair (e.g. 15.6/15.6 °C) on both sides | — | absolute | **≤ 0.005** ordinary | Bound rule | Reference pair missing on either side: pending. Never converted to density (glossary rule). |
| Flash point | Same cup type on both sides (COC = D92, PMCC = D93) | °C | absolute | **≤ 10 °C** ordinary | 0 is valid (absolute only). Bound rule. | Cup type unknown on one side: pending. |
| Pour point | Both point values | °C | absolute | **≤ 3 °C** ordinary | 0 °C is valid. Bound rule. | Method missing: allowed, flagged. |
| Noack volatility | Same method and procedure | mass % | — | **none proposed** (pending) | — | — |
| TBN | Same method (D2896 vs D4739 differ) | mg KOH/g | — | **none proposed** (pending) | — | — |
| Others (VI, CCS, elements, ash, sulfur) | — | — | — | **none proposed** (pending) | — | — |

**Bound rule (all properties).**
- A point value that satisfies the other document's bound or range is ordinary. A typical value above an SDS minimum is not a contradiction.
- A point value outside the bound or range is retained for review.
- Two bounds or two ranges are reported and kept pending.
- An SDS bound is called a lower or upper bound. It is not called a "safety margin" unless its own wording says so.

### Justification and sensitivity

- **Viscosity, 3 %.**
  - The relative differences of the comparable pairs not explained by rounding are 0.68 % (RF6088F), 1.52 % (RF6081), 6.25 % (RF6077), 6.88 % (ETRO 6+ kv40), 8.11 % and 11.89 % (RF6066) and 20.34 % (RF6069).
  - Any threshold from 1.52 % to just below 6.25 % gives the same classification, so the choice of 3 % within that band does not change any outcome.
  - ASTM D445 states its own repeatability and reproducibility. I did not check those figures against the standard's text in this repository, so they are not used as the basis.
- **Density, 0.005 g/cm³.**
  - The comparable non-rounding pairs differ by 0.002 (RF6066) and 0.003 g/cm³ (RF6078).
  - No comparable case is above 0.003, so the data does not test the threshold. It is proposed as about 0.5 % of a typical base-oil density, a scale at which batch-to-batch typical values commonly differ.
  - **This needs a reviewer decision.**
- **Flash point, 10 °C.**
  - The comparable COC pairs differ by 1, 4, 5, 7 and 7 °C (Chevron PAO 2/4/6/8) and 28 °C (Chevron mPAO 150).
  - Any threshold from 7 °C up to 27 °C gives the same classification.
  - ASTM D92 publishes its own reproducibility, which was likewise not checked here.
- **Pour point, 3 °C.** ASTM D97 tests in 3 °C steps, so a one-step difference cannot be told apart from test resolution. The only current pair is a bound check.
- **Noack, TBN and the others: no threshold.** There are one or two cases each and no project basis, so these pairs stay pending.

## 4. What approval would change (preview only; nothing applied)

The table below shows each v5 finding that contains a TDS–SDS pair and the proposed screen of those pairs.

**A finding is only eligible for "no longer active" if *every* one of its value pairs is ordinary.**
- Findings that also contain TDS–TDS or SDS–SDS differences keep those parts. For example, CF-008, CF-009 and CF-010 (RF6066) contain the TDS–TDS pair 990 vs 988, 227 vs 185 and 106 vs 108.
- Identity, unit, calculation and other findings are not touched.

| Finding | Product · property | Proposed screen of its TDS–SDS pairs | Preview effect |
|---|---|---|---|
| CF-003 | INFINEUM_D3424 flash point | ordinary: bound satisfied | could be closed as ordinary |
| CF-004 | LUBRIZOL_CV2301 density | pending: comparability unknown | stays active |
| CF-008 | RICHFUL_RF6066 density | ordinary (rounding, threshold) + pending (SDS temperature not printed) | stays active (pending part; TDS–TDS 990 vs 988 kept) |
| CF-009 | RICHFUL_RF6066 kv100 | retain for review + pending (label/unit) | stays active |
| CF-010 | RICHFUL_RF6066 TBN | ordinary (rounding) + pending (no TBN threshold) | stays active |
| CF-013 | RICHFUL_RF6069 kv100 | retain for review (20.3 %) | stays active |
| CF-014 | RICHFUL_RF6077 density | not comparable: 20 °C vs 15 °C | stays active as a condition difference |
| CF-015 | RICHFUL_RF6077 kv100 | retain for review (6.25 %) | stays active |
| CF-017 | RICHFUL_RF6078 density | ordinary: 0.003 g/cm³ | could be closed if its third value is also ordinary |
| CF-018 | RICHFUL_RF6081 kv100 | ordinary: 1.52 % | could be closed as ordinary |
| CF-019 | RICHFUL_RF6088F density | pending: "relative density" label with g/cm³ | stays active |
| CF-020 | RICHFUL_RF6088F kv100 | ordinary: 0.68 % | could be closed as ordinary |
| CF-026 | FORMOSA_150N_GII_PLUS flash point | pending: two bounds | stays active |
| CF-033 | PETRONAS_ETRO_6_PLUS kv40 | retain for review (6.88 %) | stays active |
| CF-035 | PETRONAS_ETRO_6_PLUS Noack | pending: no threshold | stays active |
| CF-036 | PETRONAS_ETRO_6_PLUS density | pending: TDS temperature not printed | stays active |
| CF-099, CF-100 | SHELL_RISELLA_X_415 / 420 density | pending: temperature not printed | stay active |
| CF-127 | CHEVRON_SYNFLUID_MPAO_150 flash point | retain for review (28 °C) | stays active |
| CF-128, CF-129, CF-130 | CHEVRON_SYNFLUID_PAO_4 / 6 / 8 flash point | ordinary: 7 / 7 / 5 °C | could be closed as ordinary |
| CF-131 | CHEVRON_SYNFLUID_PAO_2 flash point | ordinary: 1 and 4 °C | TDS–TDS edition difference (159 vs 164) kept |
| CF-140 | ARAMCO_LUBEREF_PRIMA_70 flash point | retain for review: SDS 168 below TDS minimum 175 | stays active |
| CF-148 … CF-156 | Richful flash points (7 findings) | ordinary: bound satisfied | could be closed as ordinary |
| CF-172 | S_OIL_ULTRA_S_6 specific gravity | pending: SDS reference temperature not printed | stays active (catalog vs Cosan part kept) |

"Could be closed" means: on approval, the finding would move to a dated successor of the v5 report, with the state
"screened: ordinary TDS–SDS difference (thresholds v…)". The v5 report stays unchanged as a historical snapshot, and the
finding keeps its stable ID.

## 5. Decisions requested

1. Approve, change or reject each threshold in section 3, especially density (0.005 g/cm³), which the data does not test.
2. Should a finding whose TDS–SDS part is ordinary, but which also holds a TDS–TDS difference, be split? Or should it stay one finding with a note? The proposal is to keep it as one finding with a note.
3. Confirm that label/unit inconsistencies on SDS pages (RF6066, RF6079, RF6088, RF6088F) stay pending rather than being treated as typographical errors.
