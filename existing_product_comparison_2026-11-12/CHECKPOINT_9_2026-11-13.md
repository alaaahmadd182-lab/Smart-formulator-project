# Checkpoint 9 — old-versus-new comparison (ninth pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-8 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON or production file changed, nothing staged or committed. `logs/03_checks.log`: 55 of 55 (structural).
**Not complete:** 143 ledger links not yet assessed, plus 18 product/document pairs that the candidate search never linked
(§6). "Ready for reviewer decision" means that the three-way comparison of that proposal is recorded. It does not mean
the proposal is approved, and it does not mean the comparison of the product or the document is complete.

## 1. Corrections requested for NEXBASE (file `decisions/zzzzzzzzz_nexbase_corrections_ninth_pass.json`)

- **Identifiers checked.** The certificate pairs share no identifier:
  - NEXBASE 3043:
    - `DL2-14398.pdf` (Tree Trading FIZ LLC): Buyer Ref 98104026/08, Batch B201369, PL 253-10918/1287, 30 Jun 2020;
    - `DL2-14397.pdf`: Order 14762, vessel DS COUGAR, TANK 0772, Certified By 700476, 30-JUN-2020.
  - NEXBASE 3080:
    - `DL2-14402.pdf`: Buyer Ref 98104027/08, B201368, PL 253-10917/1222, 26 Jul 2020;
    - `DL2-14401.pdf`: TANK 0775, 700443, 26-JUL-2020.
- **Relabelled.** All four links are now "LIKELY RELATED OR REPRODUCED RESULTS; INDEPENDENCE UNVERIFIED". Both sources are
  kept and are not counted as independent corroboration. The eighth-pass wording "same measurement re-issued" is withdrawn.
- **Full text read.** The earlier reads had been cut at 1,500 characters. The full text of `DL2-14398.pdf` (1,469
  characters) and `DL2-14402.pdf` (1,384 characters) has now been read, together with both page images. Coverage status:
  every printed value is accounted for, as batch evidence only. The two sulfur field rows now cite both certificates of
  each pair.

## 2. Products reviewed in this pass (three-way comparison where a document characterises the product)

**Chevron Group II.**
- `DL2-10004.pdf` (1/2018) was read. It prints "Report" for KV100 and sulphur of 220R and 100R.
- `DL2-14862.pdf` p.19 holds Afton batch characterisations of 220R, 100R and 600R. They are proposed as open-question
  notes only (220R, 100R).
- All 117 mention passages were read.

**S-OIL.**
- Brochure `DL2-12545.pdf` (scan, viewed as images).
  - Ultra-S p.5: equal to the JSON and to the cited spread `DL2-11177.pdf` (B,E).
  - Premium/Super p.6: the legible cells are equal.
  - S-8 pour "L 40.0" recurs → proposed open-question addition.
- All 62 Ultra-S mention passages were read. `DL2-15813.pdf` p.49 prints "Aramco Ultra S 4/6/8": a third-party label
  that is relevant to ID-01 but does not resolve it.

**ExxonMobil AP/E Core 150/600.**
- Old source: `DL2-13265.pdf` (05-2020) was read; it prints limits only.
- New third-party characterisations:
  - Afton HiTEC 22300 CDP p.14, lots TSU23-00052/-00053;
  - Richful RF6508 booklet p.7 (no lot number).
  - Proposed: open-question notes. The two sources differ, for example Core 600 saturates 67.4 vs 53.2 %. They are not averaged.
- The CDP labels the Core grades "Group II" on p.12 but "Group I" on p.14 and pp.18-19. This is noted only.

**PETRONAS ETRO 6.**
- The TDS `DL2-12475.pdf` was read as an image.
- SAMA certificate `DL2-15356.pdf` (Oct-2023):
  - Its sulphur specification is "15 Max"; the TDS prints "< 30" ppm. Because the origin of SAMA's specification column
    is not stated, this is proposed as an open question, not as a conflict.
  - Its density 0.8448 kg/L and KV40 34.35 are batch evidence and are proposed as an open-question note.

**aramcoPRIMA (records filed under "Saudi Aramco Luberef").**
- Old brochure `DL2-11773.pdf` re-read as an image.
- New: Motiva sheet `DL2-15131.pdf` (effective 11/01/2018; read as an image), with Spec and Typical columns for PRIMA
  60/100/220/600.
  - **Identity is not established:** the issuer is Motiva, while the JSON supplier is Luberef.
  - In addition, Afton labels "aramcoPRIMA 220 (Luberef 230HC)" in `DL2-13364.pdf`.
  - Proposals are open questions only.
  - Main discrepancy: aramcoPRIMA 600 flash. The brochure typical is 230 °C; the Motiva minimum is 250 °C (typical 263).
    If the reviewer confirms identity, record a conflict.
- Prima 230/500 batch data (`DL2-14862.pdf` p.19) were compared; this is an observation only.

**Richful booklets** (`decisions/zzzzzzzzz_richful_booklets_ninth_pass.json`).
- **RF6079.** CDP C-H-2303 (27 July 2023):
  - Final CI-4 15W-40 formulation: RF6079 9.15, LZ7077 7.3, Viscoplex 1-248 0.2.
  - **The EHC 50 / EHC 110 shares are swapped between p.8 and p.11 for the same oil code RX210314101** (verified on the
    page images). Proposal: add the formulation and record a conflict; the two base-oil shares stay unresolved.
  - Package composition "9.15% RF6079 = 8.5% RF6067 + top-treats" → note.
  - VM and PPD named → route-bound only.
- **RF6088.** CDP C-H-2405 (15 May 2024):
  - Final CK-4 15W-40 formulation (consistent across pages); co-components route-bound.
  - Treat-rate basis: the CDP gives wt.% for 15W-40 only, so the row keeps "%" (note, following the HiTEC 12200 basis
    policy). ACEA E11 is not covered by this CDP.
- **RF6066.** Sheet dated 2026/1/30:
  - Values equal to `DL2-15451.pdf` → source addition with the date.
  - The five TDS-vs-TDS conflicts are not marked resolved.
  - Field-trial formulation (evidence class "field trial").
- **RF6400.** Field-test report: CF-4 15W-40 field-trial formulation at 5.5 %.

**Richful catalogues** `DL2-15743.pdf` / `DL2-15764.pdf` (two undated editions; word-level and number-level comparison).
- RF6071L, RF6077 and RF6088F pages are the same content (B) as the cited TDS.
- RF6069: `DL2-15743.pdf` prints KV100 **142** and `DL2-15764.pdf` prints **118**. Both citations are proposed for the
  existing unresolved conflict.
- Flagged in the JSON: that conflict's note says "field left null", while the field holds 142 from richful.com.

## 3. Checks corrected by changing decision text, not the checks

- ETRO 6 sulphur: was proposed as `propose_record_conflict` on a batch certificate. This was caught by the batch-evidence
  check and changed to an open question.
- Field-trial formulation rows: now name their single formulation column.
- RF6066 tier-2 row: its value form is now labelled "specification limits and typicals".

## 4. Status (separate measures)

| Measure | Value |
|---|---|
| Relationship settled (non-duplicate) | 904 (+2 excluded, 20 unresolved) |
| … of which content review limited (name-hit passage or unread pages) | 741 |
| … of which source-to-JSON coverage "not assessed" | 778 |
| Not yet assessed (ledger) | 143 (checkpoint 8: 383) |
| Pairs never linked by the candidate search (§6) | 18 genuine (not in the ledger) |
| Proposals | 157 (all with a recorded three-way comparison; 0 provisional) |
| Duplicate-source coverage (223 documents) | not started |

Classification progress (relationship settled) is not completed content comparison. Most settled links are mentions whose
review is limited to the first name-hit passage.

## 5. Exact resume point

1. **Richful decks:** `DL2-15763`, `DL2-15767`, `DL2-15543`, `DL2-15813` (6 products), `DL2-15765`, `DL2-15546`, `DL2-15768`.
   Remaining Richful links: RF6079 5, RF6077 4, RF6088 4, RF6066/6069/6078/6080/6081/6089/6400 3 each, RF6602 2.
2. Then: `GS_CALTEX_150N` (5) and `600N` (4); `EXXONMOBIL_APE_CORE_2500` (4); `ARAMCO_LUBEREF_PRIMA_*` mentions
   (11 left; the Motiva sheet and DL2-14862 are done); ADNOC ADBASE; SpectraSyn / Synfluid; etc.
   Method: `scripts/hits.py <id>` → read the product-specific documents against the cited old source and the JSON →
   `scripts/helpers/write_base_oil_mentions.py` for the rest → print and READ every captured passage before saving.
3. The 18 unlinked pairs in `gap_analysis_2026-11-13/generic_alias_pairs_not_linked.csv` need ledger links; adding them
   requires a change to `01_candidates.py`, which is not done yet. Thirteen are Richful catalogue pages: RF6066, RF6078 and
   RF6400 in `DL2-15743`, `DL2-15764` and `DL2-15546`; RF6079 and RF6088 in `DL2-15743` and `DL2-15764`. The others are
   RF6400 in `DL2-12243`, RF6602 in `DL2-15744`, `DL2-15766` and `RF5016-Booklet.pdf`, and S-OIL P-31 in `DL2-12545`.
4. Unread content (checkpoint 4 §3 and the 741 limited reviews); duplicate-source coverage (223 documents).
