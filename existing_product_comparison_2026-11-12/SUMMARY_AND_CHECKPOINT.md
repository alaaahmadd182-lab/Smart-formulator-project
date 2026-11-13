# Old-versus-new source comparison for existing products — summary and checkpoint (2026-11-12)

**Comparison and preparation only. Nothing was ingested and no JSON was changed.** No product file, production report,
source selection, archive, evidence file or snapshot was modified; nothing was staged or committed
(`logs/03_checks.log`, 32 of 32 checks pass).

**This comparison is NOT complete.** Afton is largely reviewed, Lubrizol is about one third reviewed, Infineum has
barely started and the other suppliers have not been started. The exact position is in the checkpoint at the end and in
`tables/progress_ledger.csv`.

## 1. Corrected inventory counts (originals preserved)

The automated inventory reports in `incoming_dataset_review_2026-11-12/` are untouched. Corrections are in
`tables/corrected_inventory_statistics.json` and `decisions/inventory_dispositions.json`.

| Statistic | Links | Products | Note |
|---|---|---|---|
| Original "new documents naming an existing product in field or title" | 88 | 42 | includes files already in the existing archive |
| of which byte-identical to an existing archive file | 22 | – | not new documents |
| New documents only (59 additional-evidence + 7 revision candidates) | 66 | 25 | provisional, automated |
| After the two reviewed exclusions | 64 | 25 | 5 revision candidates remain |

Reviewed exclusions (false product matches, category G), each with its useful link preserved as formulation evidence (D):
- `DL2-11779.pdf` is the OLOA 65770 booster bulletin, not an OLOA 59766 revision.
- The Oronite OLOA 55603 presentation is not a Yubase 6 revision; it names Yubase 6 as a formulation base oil.

Product linkage, both methods kept: 202 products have a cited source that is byte-identical to a file of the new
archive; 194 products are named in the searched text. 174 are in both, 28 only by hash, 20 only by text, 42 in neither
(`tables/product_link_reconciliation.csv`). The ledger holds 1,349 links: all 443 earlier inventory links (82 of them
not found by the text search, each with the reason) and all 1,267 full-text candidates.

Search limits: 3,687 of 4,186 unique documents have a usable text layer and were searched on every page; 499 could not
be searched (no OCR engine) and nothing is concluded about them (`tables/unsearchable_documents.csv`). Five absence
statements of the inventory summary and the "scope" wording are corrected in `decisions/inventory_dispositions.json`.

## 2. What is reviewed

Three statuses are kept apart for every link: relationship, field verification, source-to-JSON coverage.

| Supplier batch | Non-duplicate links | Relationship reviewed | Unresolved | Not yet assessed |
|---|---|---|---|---|
| Afton | 90 | 40 | 20 | 30 |
| Lubrizol | 22 | 8 | 0 | 14 |
| Infineum | 44 | 3 | 1 | 40 |
| All other suppliers | 912 | 2 excluded (the false matches) | 0 | 910 |
| **Total** | **1,068** | **53** | **21** | **994** |

Exact byte duplicates: 281 links (223 documents, 207 products), relationship settled by hash. **Source-to-JSON coverage
of those duplicates has not been assessed**; it was checked only for the two old Lubrizol data sheets re-read below.

99 field-level rows: 64 additional, 23 already captured, 10 changed or conflicting, 2 not comparable. 84 proposals,
none applied (`tables/proposed_json_changes_NOT_APPLIED.csv`). 9 pages verified visually, 11 visual checks outstanding
(`tables/visual_verification.csv`).

## 3. Findings so far

**Verified later editions** (established from printed edition dates on the same document type and template):
- Lubrizol 16008: `DL2-11514.pdf` "Effective 1/19/2018" replaces the cited `DL2-10871.pdf` "Effective 6/12/2013". The
  treat-rate cascade grew from one rate (4.4 %) to seven (6.21 / 5.35 / 4.4 / 3.75 / 2.8 / 2.5 / 1.6 % by weight) with
  11 further claims; the 1.6 % block prints no claim; TBN changed from the sentence "greater than 182" to a typical 182.
  All physical and chemical characteristics are identical.
- Lubrizol CV1103: `DL2-15753.pdf` "Published on 13 May, 2022" replaces `DL2-14978.pdf` "11 Jan, 2021". Added claim
  ACEA E11-22; the second column is now headed "14.30 + 2.00% by weight CV6320"; the two sentences naming Lubrizol 7077
  are gone (an omission, not a statement that it is no longer needed); "embedded PPD" is new. Typicals identical.

**Verified earlier editions** (no change; historical evidence): HiTEC 12210M SDS `DL2-15019.pdf` (version 1, 1/3/2019;
cited: version 3.03, 10/11/2022; density 0.947 vs 0.95 g/cm3); HiTEC 5748 bulletins `DL2-11428.pdf` (07/11) and
`DL2-15572.pdf` (04/21) against the cited 05/23 edition.

**Documents that genuinely add information:**
- HiTEC 12204L: `DL2-14862.pdf` (Afton programme book, May-19) gives Ca 2.56, Zn 0.77, P 0.70, N 0.87, S 2.10,
  Mo 0.03 %wt, density 0.972 g/ml at 15 C, an API SL claim with stated scope, and a complete formulation
  (LBB-020473-A). The SDS `DL2-13579.pdf` gives KV40 (42.38 cm2/s), printed by no technical source.
- HiTEC 12200: `DL2-12084.pdf` (Afton report 2019-06) gives typical Ca, P, Zn, S, B, Mo, N; certificate `DL2-14386.pdf`
  gives the sales-specification limits. 26 complete formulations across `DL2-13364`, `DL2-12084`, `DL2-11706`,
  `DL2-12905` (the record has none).
- HiTEC 8788B: sales-specification limits for TBN, Ca, P, Zn, N (four certificates) and two complete formulations.
- HiTEC 12010: `DL2-13295.pdf` is its first technical bulletin: TBN 175, Ca 6.26, Zn 1.53, P 1.38, six treat rates.
- HiTEC 12210 (KV40 from SDS; viscosity modifier named as HiTEC 5748A), 12210M (31 formulations, all with 5748A),
  12400 (2 formulations), 12250 (its own bulletin), 8766B (8 formulations in a Chevron summary).
- Lubrizol CV1100 (6 formulations, one printing mass % and volume % side by side), CV2301 (doses of one formulation).
- Infineum D3451 (one formulation; certificate limits whose targets equal the recorded typicals) and D3453.

**Conflicts found** (recorded, not resolved): HiTEC 12010 KV100 73 mm2/s (bulletin) vs 64 cSt (SDS, currently
selected); Afton oil code LBB-019000-A printed with AP/E Core base oils in one document and aramcoDURA in another;
HiTEC 12400 formulation LBR-20963-B adds to 99.9; HiTEC 8788B slide title "Grp I" vs row label "API Group III" for
AP/E Core 600. Full list: `tables/conflicts_and_unresolved.csv`.

**Mention only** (reviewed): HiTEC 12204L and 12200 in the 12250 bulletin footnotes, 12200 and 8799B(+) on a portfolio
slide, 12210 in a support table.

**Corrections this review made to earlier leads:** the visual read of `DL2-13136.pdf` shows Infineum D3451 11.9 % goes
with SV261 **6.7** %, not 7.0 % as the text-layer order had suggested. HiTEC 12210M and 12210 use HiTEC 5748A, which
is not the HiTEC 5748 record.

**Old-source information never captured in JSON:** none established yet. The assessment was made only for the two old
Lubrizol data sheets (numeric typicals captured; whether printed min/max limits of Lubrizol 16008 are stored was not
checked). `tables/existing_source_information_not_captured.csv` is therefore empty and must not be read as "none".

## 4. Rules applied in the proposals

- Recipe ingredients are proposed only as route-bound entries, never as universally required components.
- Certificate targets and limits are proposed as alternate specification entries; a data-sheet typical stays the
  general product value. Batch results are never proposed as typicals.
- No SDS value is preferred over technical evidence; SDS values are proposed only where no technical source prints the
  property. No threshold was applied; nothing was averaged.
- Edition changes keep the earlier wording as history.

## 5. Checkpoint — outstanding work, in order

1. **Afton (30 links not assessed, 20 unresolved):** 29 documents naming HiTEC 5748 in other packages' formulations
   (dose evidence, not read); SDS `DL2-15631.pdf` section 9; the 18 "GE220 (HiTEC 12200)" certificates (identity
   unresolved); "HiTEC 8799B(+)". Unread pages: `DL2-11706.pdf` pp.4-35, `DL2-12084.pdf` pp.7-18, `DL2-14862.pdf`
   pp.10-12 and 17-21. Seven visual checks outstanding (approval dots, `DL2-14862.pdf` p.15, 12210M totals).
2. **Lubrizol (14 links):** 16008 — `DL2-11898.pdf`, `DL2-12103.pdf` (SDS), `DL2-11897.pdf`, `DL2-12416.pdf`;
   CV1100 — `DL2-11853.pdf` (SDS), `DL2-12610.pdf`, `DL2-12609.pdf`; CV1103 — `DL2-15705.pdf` (SDS);
   CV2301 — `DL2-12187`, `DL2-13620`, `DL2-12189`, `DL2-12185`, `DL2-12169`, `DL2-12188`.
3. **Infineum (40 links, 1 unresolved):** D3320, D3384, D3396, D3398, D3416, D3417, D3453, D3463, D3503, D3511 and the
   rest of D3451; `DL2-13312.pdf` p.2 needs a visual read.
4. **Remaining revision candidates:** `DL2-13111.pdf` (OLOA 59766) and `DL2-14994.pdf` (Synfluid PAO 4 sales
   specification), plus 6 further F candidates from the full-text search.
5. **Other suppliers (910 links):** 813 are base oils or components named in formulations of other products
   (Yubase, EHC, Nexbase, Chevron, Ultra-S, HiTEC 5748 ...), 121 mention candidates, 44 additional-evidence candidates.
6. **Source-to-JSON coverage** of the 223 exact-duplicate documents: not assessed.
7. **New-product queue** (`tables/new_product_candidate_queue.csv`): 14 names from the reviewed documents only.

To resume: read `decisions/*.json`, add a decision file per batch, run `scripts/02_build.py` then `scripts/03_checks.py`.
