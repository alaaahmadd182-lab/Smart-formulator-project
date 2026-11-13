# Checkpoint 3 — old-versus-new comparison (third pass, 2026-11-12)

Supersedes the status sections of `SUMMARY_AND_CHECKPOINT.md` and `CHECKPOINT_2_2026-11-12.md` (both kept unchanged).
Comparison and proposal preparation only: nothing ingested, no JSON changed, no production selection or report changed,
nothing staged or committed. `logs/03_checks.log`: 48 of 48 checks pass (structural checks; they do not verify values
scientifically — manual verification is recorded per row).

**The comparison is still NOT complete.** 938 of 1,068 non-duplicate links are not yet assessed.

## Reconciliation

| Non-duplicate links | Checkpoint 2 | Now | Change |
|---|---|---|---|
| Relationship completed | 57 | 106 | +30 Afton (HiTEC 5748 documents), +7 Lubrizol, +12 Infineum |
| Excluded with reason | 2 | 2 | – |
| Unresolved | 20 | 22 | +2 Lubrizol forms whose cells need a visual read |
| Not yet assessed | 989 | 938 | −51 |

By batch: **Afton 70 completed / 20 unresolved / 0 not assessed**; **Lubrizol 20 / 2 / 0**; Infineum 16 / 0 / 28;
other suppliers 2 excluded / 910 not assessed. Ledger total 1,349; exact duplicates 281 (coverage not assessed).

Proposals: 92, of which **33 ready for a reviewer decision** and 59 provisional (was 2 and 85). A proposal is ready only
when the reviewer read the old source, the current JSON entry was compared, the document relationship is completed, no
visual check is outstanding and no overlap with existing entries is flagged.

## Done in this pass

**Afton — relationship review finished.**
- HiTEC 5748 is named in 30 documents of other products. All are dose or pairing evidence inside other packages'
  recipes and stay with those recipes; none changes the HiTEC 5748 record's treat range. Three statements concern the
  product itself (cited 05/23 bulletin re-read from its local evidence copy):
  - "25 SSI" (`DL2-15465.pdf`): **already recorded** in the record's open question (from `DL2-13692.pdf`); adds one citation.
  - Liquid HiTEC 5748 is made by dissolving solid HiTEC 5825K in base oil (`HiTEC-5825K_PDS.pdf`): new, proposed as a note.
    Polymer content stays Missing.
  - Conditional interchange with HiTEC 5748A in one programme (`DL2-11597.pdf` p.4): proposed as a scoped note.
  - `DL2-11395.pdf` describes a modifier "analogous to" HiTEC 5748: not a property of the product, nothing used.
- Old sources read manually: `DL2-14639.pdf`, `DL2-11418.pdf`, `DL2-15365.pdf`, `DL2-10367.pdf`, `DL2-15568.pdf` (p.2 text).
  Results: the HiTEC 12200 bulletin prints no element content and no formulation (20 proposals now ready);
  HiTEC 12210's old source and JSON **already name HiTEC 5748A**, so that proposal is withdrawn (already captured);
  HiTEC 12210M's old source names "HiTEC 5748A or HiTEC 5748" without dose, so only the 31 recipe doses are new;
  HiTEC 8766B's recorded 3.3 % is the HiTEC 8767B booster, unrelated to the recipe ingredients of `DL2-12905.pdf`.
- `DL2-12485.pdf` p.18 (LBR-019256-A) adds to **100.1 as printed**; flagged, to be entered with the total check failed,
  never normalised (a check enforces the flag). `DL2-12485.pdf` and `DL2-12486.pdf` have identical extracted text and
  identical page renderings at the tested 60 dpi; their bytes differ.

**Lubrizol — relationship review finished.**
- `DL2-12416.pdf` p.14 (Lubrizol 16008 cascade, 2017): genuinely new are the claim of the 1.6 % rate (API SB / CB
  Monograde, blank in the 2018 data sheet), a 2.7 % rate (API CD Monograde), API SD at 2.8 %, and the
  multigrade / monograde condition of each rate. It also states "typical TBN 188": a third TBN statement beside
  "> 182" (2013) and "typical 182" (2018); recorded as a conflict, not resolved.
- `DL2-11898.pdf` (Lubrizol 16008's own technical report, Dec 2013): relationship settled, **pages 5-22 unread**.
- CV2301: four further forms; one (`DL2-12189.pdf`) and one CV1100 table (`DL2-12610.pdf`) need a visual read.

**Infineum — partial.**
- `DL2-12772.pdf` (D3503 data sheet, "17 October 2018 (1.0)") against the cited `DL2-11404.pdf` ("25 May 2016 (3.0)"):
  content identical line by line; the sequence is **not established** (later date, lower version number). No change.
- `DL2-12856.pdf` is the data sheet of the booster Infineum D2376, not a D3451 document (false match, link preserved):
  route D2376 3.5 mass % + D3451 10.7 mass % for API CJ-4, distinct from the recorded D2367 route; provisional.
- D3320, D3511, D3503 presentations and the D3503 data package: relationship settled, **content unread**.

## Exact next steps, in order

1. **Infineum, next document: `DL2-13000.pdf`** (28 pp.; D3384 pp.16-21, D3396 / D3398 pp.3-10), then `DL2-13682.pdf`
   (same hit pages), `DL2-13139.pdf` (D3450 series, 22 pp.), `DL2-13080 / 13081 / 13082.pdf` for D3384 / D3451 / D3453,
   `DL2-12997.pdf` (D3390 series), `DL2-15564.pdf` / `DL2-15332.pdf` (D3416 / D3417), `DL2-13311.pdf` p.48,
   `DL2-12623.pdf`, `DL2-13801.pdf` pp.3-5. Then read the unread content: `DL2-11768.pdf` (D3503 data package),
   `DL2-15685.pdf`, `DL2-11679.pdf` section 9, `DL2-13079.pdf`, `DL2-13796.pdf` p.11 (visual), `DL2-15388.pdf`.
   D3453: read the record and its sources before its proposal can leave provisional.
2. **Lubrizol content still to read:** `DL2-11898.pdf` pp.5-22 (final formulations, section 4); visual reads of
   `DL2-12189.pdf` p.6 and `DL2-12610.pdf` p.4; old sources `DL2-11503.pdf`, `DL2-13065.pdf`, `DL2-13713.pdf`.
3. **Afton content still to resolve (59 provisional proposals overall):** obtain a local copy of the HiTEC 12204L PDS
   (registered SHA-256 7a1e57d8...) for the 12204L / 12250 rows; read `DL2-15016.pdf` and the 8788B PDS for 8788B,
   `DL2-15021.pdf` for 12010; outstanding visual checks in `tables/visual_verification.csv`; unread pages of
   `DL2-11706.pdf` (4-35), `DL2-12084.pdf` (7-18), `DL2-14862.pdf` (10-12, 17-21). Unresolved identity: 18 GE220
   certificates, "HiTEC 8799B(+)".
4. **Revision candidates:** `DL2-13111.pdf` (OLOA 59766), `DL2-14994.pdf` (Synfluid PAO 4).
5. **Other suppliers (910 links):** start with `PETRONAS_ETRO_4_PLUS` / `ETRO_6_PLUS` (lead: `DL2-14915.pdf` prints
   "Etro plus 4" kV100 4.137, density 0.8290 and "Etro plus 6" 6.057, 0.8416), then the ledger in product order.
6. **Source-to-JSON coverage** of the 223 exact-duplicate documents: not assessed.

To resume: add a decision file in `decisions/` (later files override earlier links; `field_overrides` patch rows and
accept `*` for path or file), run `scripts/02_build.py`, `scripts/03_checks.py`, `scripts/04_make_zip.py`.
`scripts/hits.py <product_id>` lists the unassessed documents of a product with the text around each hit.
