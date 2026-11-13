# Checkpoint 7 — old-versus-new comparison (seventh pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-6 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON or production file changed, nothing staged or committed. `logs/03_checks.log`: 55 of 55 (structural).
**Not complete:** 516 of 1,068 non-duplicate links not yet assessed.

## 1. Corrections made first

**Yubase old sources.** The earlier statement "re-read manually … entries as recorded in the JSON" did not show that the
original PDFs were read. Now read: `DL2-11304.pdf` (Yubase 4), `DL2-11306.pdf` (Yubase 6), `DL2-11303.pdf` (Yubase 3) —
each one page, whole text layer; Yubase 4 also as a page image. The `old_rev` of every Yubase row now names that scope.
Readiness was recomputed only after these reads.

**Name-hit reviews.** 253 earlier links plus 141 new EHC links were classified from captured name-hit passages.
Coverage for all of them is now "NOT ASSESSED: only the passages around the name hits were inspected …"; the content
status says "LIMITED to the FIRST name-hit passage … other hits, tables and the rest of the document NOT reviewed".
The 30 HiTEC 5748 links carry the same limitation. The Yubase 6/3 and EHC passages had first been classified on titles
only; the reviewer then read every captured passage (all 253 printed) and reclassified those that were not recipe shares:
two EHC certificates, the Richful base-stock tables (RF6079 / 6067 / 6088 / 6508), an Afton characterisation (HiTEC 22300
p.14), a PPD-response table (`DL2-15005.pdf`), an Afton component-density table (`DL2-15690.pdf`), and a solution test
in the HiTEC 5825K bulletin. Two Yubase 3 links had no captured passage; their hits were read (p.1: "in Yubase (Yubase 3 +
Yubase 6) or S-Oil … base stocks"), recipe statements.

## 2. HiTEC 12200 — percentage basis per route (proposals, not applied)

Rows matched individually (product, grade, base-oil group, booster, API level) to explicit "% wt" evidence; the
bulletin's printed "%" and its citation are kept, the supporting document is cited separately:

| treat_rate_matrix row | Supporting evidence |
|---|---|
| [1] 11.7 % + 0.9 % 12260, 10W-30, GP II | `DL2-13364.pdf` p.7 "11.7% wt + 0.9% wt HiTEC 12260" |
| [3] 10.8 % + 0.9 % 12260, 10W-40, GP II/III | p.7 "10.8% wt + 0.9% wt HiTEC 12260 (30% group III)" |
| [6] / [7] 10.8 %, 15W-40 / 20W-50, GP II | p.7 "10.8% wt" (Group II, CI-4) |
| [8] / [9] 9.7 %, 15W-40 / 20W-50, GP II | p.7 "9.7% wt" (Group II, CH-4) |
| [13] 10.8 % + 0.35 % 9552, 15W-40, GP I | p.7 "10.8% wt + 0.35% wt* HiTEC 9552" (Group I) |
| [15] / [16] 10.8 %, 15W-40 / 20W-50, GP I | p.7 "10.8% wt" (Group I, CH-4) |
| [0] 10.3 % + 4.2 % 12250, 15W-40, GP II | `DL2-14862.pdf` p.2 "HiTEC 12200 @ 10.3 %wt with a booster of HiTEC 12250 at 4.2 %wt" |

**Left unresolved** (no individually matching "% wt" route evidence): [2] 10.8 + 12260 in 10W-30; [4] 10.8 % 10W-40 GP II/III
without booster; [5] 10.8 + 9552 0.6 (only a recipe matches); [10] 8.2 %; [11] 6.1 %; [12] 10.3 + 12255 5.0 (footnote prints
"%"); [14] 10.8 + 9552 0.35 in 20W-50 GP I (p.7 says "% wt" for 15W-40 only). Booster doses: mass basis proposed for 12250 4.2,
12260 0.9, 9552 0.35; 12255 5.0 and 9552 0.6 left unresolved.

## 3. Yubase 4 density (decision applied to the proposal, not to the JSON)

Mandatory density stays **unresolved (Missing)**. 834 kg/m3 at 15 C is preserved as an alternate entry with source
class "third-party reference", the Shell Cargo Handling Sheet's date (12 May 2023, Revision 3) and its qualification
verbatim. Not promoted to a manufacturer value. Specific gravity (SDS 0.834, no temperature; distributor 0,8338 at 15 C
labelled "g/m3") is a different quantity and is not converted.

## 4. Rounded and calculated values — explained, not asserted

Yubase rows now give the evidence and conditions: e.g. SDS KV40 "19.5 mm2/s (calculated value)" vs measured 19,57 (D445)
— neither called equal (19.57 rounds to 19.6) nor a conflict (calculated, basis unstated); flash points 230 (D92) vs 220
(COC) are both open-cup and are recorded as a conflict; specific gravities agree at the SDS's three printed decimals,
which does not establish the SDS temperature.

## 5. ExxonMobil EHC family

- `DL2-12130.pdf` (2-2017, "sales specifications and availability expected in 2019") is an **earlier, prospective edition**
  of the 03-2019 specification set the records cite (`DL2-11785.pdf`, read in full). EHC 45 / 65 / 120 limits are equal;
  EHC 50 differs (CCS -20 C max 1500 vs 1,700; Noack 13.5 vs 15; pour -18 vs -15) and EHC 110 differs (VI 95-110 vs 95-119;
  pour -15 vs -12): proposed as edition history only; the 2019 limits stay.
- SAMA Lubricants certificates for "EHC-50" and "EHC-120" (21 April 2019): batch actuals including density at 15 C
  (0.8520 / 0.8662 g/ml, D4052). Mandatory densities stay Missing; open-question notes only. The certificates print
  "Flash Point (PMC) … ASTM D92" (closed-cup label, open-cup method): inconsistent as printed.

## 6. Status (three separate measures)

| | Value |
|---|---|
| Non-duplicate links, relationship settled | 531 (+2 excluded, 20 unresolved) |
| of which content review limited (name-hit passages, unread pages) | 402 |
| of which source-to-JSON coverage "not assessed" | 448 |
| Not yet assessed | 516 |
| Proposals | 133, all with a completed three-way comparison as recorded (0 provisional) |

Check change this pass: the batch-evidence check now also accepts note-only actions (which set no value); a
regression case proves that update, selection-review and route-bound actions on batch data are still caught.

## 7. Next steps

1. `NESTE_NEXBASE_3043` (55), `CHEVRON_GROUP_II_220R` (46), `CHEVRON_GROUP_II_600R` (30), `S_OIL_ULTRA_S_4` (28),
   `CHEVRON_GROUP_II_100R` (26), `NESTE_NEXBASE_3060` (26), `NESTE_NEXBASE_3080` (25), … — find product-specific documents
   first; read every captured first-hit passage before accepting a generated classification.
2. Unread content (checkpoint 4 §3, plus the 402 limited reviews). 3. Duplicate-source coverage (223 documents).
