# Checkpoint 4 — old-versus-new comparison (fourth pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-3 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON changed, no production selection or report changed, nothing staged or committed.
`logs/03_checks.log`: 53 of 53 checks pass. These are structural checks; they do not verify any value scientifically —
the manual verification is recorded per row (`new_source_verification`, `old_source_review`).

**The comparison is still NOT complete.** 908 of 1,068 non-duplicate links (other suppliers) are not yet assessed.

## 1. Status, kept as three separate measures

| Batch | Relationship reviewed | of which content only partly reviewed | Unresolved | Not assessed |
|---|---|---|---|---|
| Afton | 70 | 32 (see §3) | 20 | 0 |
| Lubrizol | 22 | 4 | 0 | 0 |
| Infineum | 44 | 11 | 0 | 0 |
| Other suppliers | 2 (+2 excluded) | 0 | 0 | 908 |

Relationship completed means the document's identity and type relative to the product are settled. It does **not**
mean the document was read in full, or that a three-way comparison was done. Content coverage is in
`progress_ledger.csv` (`field_verification_status`); three-way readiness is per proposal in `field_level_comparison.csv`.

Proposals: 124, of which **96 ready for a reviewer decision** and 28 provisional. Ready = old source read by the
reviewer (or read as a page image), current JSON entry shown and compared, relationship completed, no visual check
outstanding, no overlap flag. Remaining provisional reasons:
- 13 HiTEC 12204L + 4 HiTEC 12250 + 4 HiTEC 8788B: the primary old source (Afton PDS, registered hash, **no local copy**) was not re-checked;
- 1 HiTEC 12250: current JSON not compared (a no-template-field row);
- 10 rows flagged for overlap with existing entries (notes on existing claims or co-components; by design the reviewer decides).

## 2. Done in this pass

**Infineum (relationship review finished, 44 links).**
- `DL2-13000.pdf` (D339X deck, 2018; `DL2-13682.pdf` same page renderings at 50 dpi): cascade, claims, formulations and
  product signature read as images. D3398 gains API SL (footnoted "bench testing in progress") and 13 grade-scoped OEM /
  ACEA claims; D3396 and D3398 gain three formulations each and D2360 booster routes. The product signature (finished-oil
  values at 9.45 / 9.7 / 10.2 %m, TBN by D4739 **and** D2896 printed separately) and the field-trial charts are kept out
  of the package records.
- Old sheets read: D3396 `DL2-13383.pdf`, D3398 `DL2-13348.pdf`, D3451 `DL2-12029.pdf` (full), and the image-only scans
  D3384 `DL2-10218.pdf` p.1 and D3453 `DL2-10220.pdf` (read as page images). With D3453's old sheet read, its
  formulation proposal has now completed the three-way comparison.
- D3384: the 2015 cascade slide prints claim sets that **differ** from the 2015 data sheet for the 9.2 and 8.05 + D2358
  routes (MB 228.3 / MTU Cat 2 / MAN 3275 vs MB 228.1 / MTU Cat 1 / MAN 270/271): recorded as a conflict. New: ">82.3 % sats"
  condition at CH-4/SJ; three booster routes D2382 / D2383 / D2384 (no doses printed).
- D3451 / D3453: neat D4739 TBN (68 / 82) as separate entries from D2896 (77 / 91); small 2013-slide differences in Ca, N,
  ash recorded as conflicts, not averaged; finished-oil values at 11.9 / 12.2 mass % kept out. New D2360 route D3451 → D3453
  level; second D3451 formulation IME1401827-A (read as an image).
- D3416 / D3417 (`DL2-15564.pdf`, same renderings as `DL2-15332.pdf` at 40 dpi): D3416 gains API CH-4/SJ; D3417 gains CH-4/SJ
  and 13 OEM / ACEA claims; booster routes (D2360, D2395); six formulations.
- `DL2-13080 / 13081 / 13082.pdf` are one deck with three different title lines (text differs only in the title; renderings
  at 50 dpi differ on page 1 only).

**Lubrizol (now fully read for the proposals).**
- `DL2-11898.pdf` (Lubrizol 16008 report, Dec 2013) read in full; ten final formulations (pp.18-19 as images), all add to
  100.0. **Conflict inside the report:** the API SD formulation is printed with Chevron 220R + Lubrizol 7075F (p.14) and
  Chevron 150R + Lubrizol 7077 (p.19) at the same percentages. The report confirms the 1.6 % API SB/CB claim.
- `DL2-12189.pdf` p.6 (image): CV2301 formulation OS268035 with base oils. `DL2-12610.pdf` p.4: same oil OS411971 as
  `DL2-12611.pdf` (corroboration only).
- Old sheets read: CV2301 `DL2-13065.pdf`, CV1100 `DL2-11503.pdf`.

**Afton.** Old SDS read: HiTEC 12010 `DL2-15021.pdf` (KV40 printed "13.13 cm2/s (1313 cSt)"; no TBN or elements) and
8788B `DL2-15016.pdf`. Certificates `DL2-14235 / 14237 / 14239` and several claim pages verified as images.

**Revision candidates (other suppliers).**
- `DL2-13111.pdf` is an OLOA 59766 **technical bulletin** (2018), not a revision of the cited SDS: first TBN (90, D2896),
  elements, sulfated ash, KV100 135, claims, a 9.33 % route and named VIIs (PARATONE 24EX or 8900E).
- `DL2-14994.pdf` is a Synfluid PAO 4 **sales specification** (Europe, Beringen, 2017), not a revision: first density
  statement, a specification **range** 810-830 kg/m3 (recorded as a range, no point invented). The 2011 typical KV40 16.8
  lies below the 2017 specification minimum of 17: recorded, not resolved.

## 3. Content still unread (relationship settled, comparison NOT finished)

Afton: `DL2-11706.pdf` pp.4-35; `DL2-12084.pdf` pp.7-18; `DL2-14862.pdf` pp.10-12, 17-21 and the p.15 analytical rows;
30 HiTEC 5748 documents read only around the name hits (tables not verified); `DL2-11421.pdf` p.8 X marks; `DL2-13146.pdf`
claim symbols for Deutz DQC IV-18 LA and Renault RLD-3. Lubrizol: `DL2-12204.pdf` pp.2-4, `DL2-12187.pdf`, `DL2-12186.pdf`
base oils, `DL2-12169.pdf` applicant / base oils, `DL2-15753.pdf` p.2 as an image, `DL2-12202.pdf` pp.3-6 as images.
Infineum: `DL2-13079.pdf` (D3320, 22 pp.), `DL2-13796.pdf` p.11, `DL2-15388.pdf` (D3511), `DL2-15685.pdf` (D3503, 39 pp.),
`DL2-11768.pdf` (D3503 data package), `DL2-11679.pdf` section 9, `DL2-12623.pdf` engine-test pages, `DL2-13080.pdf`
pp.3-5, 7-10. Unresolved identity: 18 "GE220 (HiTEC 12200)" certificates; "HiTEC 8799B(+)".

## 4. The four checks that failed in the third pass, and what changed

In the third pass, after new decisions were added, four checks failed. Each was examined; three were checks whose
predicate was wider than the rule it was meant to enforce, one was a lookup ambiguity. **No check was removed.** Each
refined predicate is now also run against a synthetic row that reproduces the original failure case, so the
original protection stays under test (lines 157-187 of `scripts/03_checks.py`; extracted in
`logs/regression_tests_added_2026-11-13.txt`).

1. **"no proposal mixes HiTEC 5748A evidence into HiTEC 5748"** failed on the scoped *note* proposing that HiTEC 5748 and
   5748A are interchangeable in one programme (`DL2-11597.pdf` p.4): the note names both grades, which is the point of it.
   Rule kept: no **value or entry** for HiTEC 5748 may come from 5748A text.
   Before: `not [r for r in prop if r['product_id'] == 'AFTON_HITEC_5748' and '5748A' in r['new_source_printed']]`
   After: same, `and r['recommended_action'].startswith(('propose_add', 'propose_alternate'))`.
   Regression: a `propose_add` and a `propose_alternate_entry` built from 5748A text are still caught; a `propose_note` is not.
2. **"specification limits, typicals and batch results are labelled in value_form for every numeric tier-2 proposal"**
   failed on the HiTEC 5748 `polymer_chemistry` note: component files are tier 2, so a text field was treated as numeric.
   Before: applied to every tier-2 proposal. After: applied to tier-2 proposals whose field matches
   `tbn|kv\d|density|flash|pour|elements\.|sulfated`. Regression: an unlabelled `tbn` and an unlabelled `elements.Ca`
   proposal are still caught; `polymer_chemistry` is not.
3. **"no proposal is ready on an automated old-source search alone"** failed because the check looked for the word
   "automated" anywhere, and the reviewer's manual statements mention which *other* sources were only searched
   automatically. The original check was also too weak in the other direction: it did not catch "not available locally".
   Before: `'automated' in r['old_source_review']`. After (stricter): ready requires
   `r['old_source_review'].startswith('re-read manually')`; a fourth check was added: every ready proposal also needs a
   completed relationship, a compared current JSON and no overlap flag. Regression: "automated", "not available locally",
   and (added in this pass) "not available locally ... re-read manually" are caught; a manual reading that mentions an
   automated search of another edition is not.
4. **"Lubrizol 16008 old '> 182' and new typical 182 are kept distinct"** failed because a second TBN row (the 2017 slide's
   "typical TBN 188") made the lookup return two rows. After: the case check selects the row of `DL2-11514.pdf`, and a new
   regression check requires **every** 16008 TBN row to keep the 2013 lower bound visible and the 188 row to be recorded
   as a conflict.

Also in this pass:
- **Build defect found by check 3 and fixed in `scripts/02_build.py`:** the reviewer's old-source statement for HiTEC
  12204L begins "not available locally" but mentions that a second source was "re-read manually"; the build counted it as
  a reading because it tested `'re-read' in manual`. It now tests `manual.startswith('re-read')` and adds the reason
  "primary old source not available locally". 13 HiTEC 12204L proposals returned to provisional.
- **D3453 case check:** the checkpoint-2 rule "the D3453 formulation is provisional" became false legitimately once its
  old sheet was read. The check now enforces the rule as a condition (provisional **unless** old source read, JSON compared,
  relationship completed) and keeps two regression rows reproducing the original incomplete state.
- **New case check:** the 100.1 % HiTEC 12210M formulation (`DL2-12485.pdf` p.18) must carry the flag and "total_check_passed
  false"; it is not normalised.
- One proposal (OLOA 59766 VII) failed the route-condition check and was corrected in its decision file.

## 5. Exact next steps, in order

1. **Other suppliers (908 links), next product: `PETRONAS_ETRO_4_PLUS` / `ETRO_6_PLUS`** (lead: `DL2-14915.pdf` p.1 prints
   "Etro plus 4" kV100 4.137, density 0.8290 and "Etro plus 6" 6.057, 0.8416 in a formulation sheet), then the ledger in
   product order (`scripts/hits.py <product_id>`). Most links are base oils named inside other products' formulations.
2. Unread content listed in §3, Infineum and Lubrizol first.
3. Obtain local copies of the Afton HiTEC 12204L and HiTEC 8788B PDS (registered SHA-256 7a1e57d8... and c09305fb...) to
   finish 21 provisional Afton proposals; this needs the user's decision (external retrieval).
4. Source-to-JSON coverage of the 223 exact-duplicate documents: not assessed.

To resume: add a decision file in `decisions/`, run `scripts/02_build.py`, `scripts/03_checks.py`, `scripts/04_make_zip.py`.
