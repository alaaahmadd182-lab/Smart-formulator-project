# Checkpoint 2 — old-versus-new comparison (second pass, 2026-11-12)

Supersedes the status section of `SUMMARY_AND_CHECKPOINT.md` (kept unchanged as the first checkpoint). Comparison and
proposal preparation only: nothing ingested, no JSON changed, no production selection or report changed, nothing
staged or committed. `logs/03_checks.log`: 46 of 46 checks pass.

**The comparison is still NOT complete.** 989 of 1,068 non-duplicate links are not yet assessed.

## Reconciliation with checkpoint 1

| | Checkpoint 1 | Now | Change |
|---|---|---|---|
| Ledger links | 1,349 | 1,349 | – |
| Exact-duplicate links (hash) | 281 | 281 | – |
| Non-duplicate, relationship completed | 51 | 57 | +5 Lubrizol (3 SDS, 2 CV2301 approval forms), +1 Infineum D3384 cascade (was unresolved) |
| Excluded with reason | 2 | 2 | – |
| Unresolved | 21 | 20 | D3384 / `DL2-13312.pdf` resolved by a visual read |
| Not yet assessed | 994 | 989 | −5 Lubrizol |

By batch (non-duplicate): Afton 40 completed / 20 unresolved / 30 not assessed; Lubrizol 13 / 0 / 9; Infineum 4 / 0 / 40;
other suppliers 2 excluded / 910 not assessed.

## What changed in this pass

1. **Five independent statuses per proposal** (`tables/field_level_comparison.csv`): document relationship, new-source
   verification, old-source review, current-JSON comparison, action readiness. Of 87 proposals, **2 are ready for a
   reviewer decision and 85 are provisional**, each with the missing parts named. Main reasons: the old source was only
   searched automatically, not read (74); a visual check is outstanding (21); a cited old source is not available
   locally (15 + 5); possible overlap with existing entries (8).
2. **Actual current JSON** replaces "list of N": every row shows the current value object or the existing entries, and
   `current_json_excerpts/` holds the full pruned content with file path and SHA-256.
3. **Old-source references resolved** (`tables/old_source_references.csv`): 22 archive members with SHA-256; the
   Afton HiTEC 12204L PDS (Internet Archive) has a registered SHA-256 but **no local copy**, so it was not re-checked
   and the 12204L / 12250 rows say so. The "old-source search" column is a mechanical text search, not a reading.
4. **Overlap found by comparing with the actual JSON** (proposals narrowed, not additions):
   - HiTEC 12210 and 12210M: `required_co_components` already names HiTEC 5748A.
   - Lubrizol CV1103 already holds CV6320 and Lubrizol 7077; CV1100 already holds CV6320.
   - HiTEC 12200 treat-rate matrix already holds the HiTEC 12260 and 9552 routes.
   - Lubrizol 16008 already holds API CF and API SF; HiTEC 12204L already holds API CI-4 Plus.
   - Lubrizol 16008 TBN: the JSON already stores the 2013 statement correctly as qualifier ">" with min 182. The 2018
     edition's typical 182 is a different statement and is proposed as a separate, dated entry.
5. **Visual checks done in this pass:** `DL2-13579.pdf` p.5 (KV40 is printed "42.38 cm²/s"; KV100 "190 cSt");
   `DL2-14862.pdf` p.15 formulation block; `DL2-13312.pdf` p.2 (D3384 cascade); `DL2-12485.pdf` vs `DL2-12486.pdf`
   (pixel-identical renderings on all 32 pages, so the same-content relationship is now established, not provisional).
   All 31 HiTEC 12210M totals added: 30 give 100.0, page 18 gives 100.1 as printed.
6. **Automated old-source leads** (`tables/existing_source_information_not_captured.csv`, 19 rows): read by the
   reviewer in the search extracts. All are SDS component names or fire-hazard wording ("calcium salts", "zinc salts",
   "phosphorus oxides", "Boron compounds 5 - 10"), or a neighbouring product's value (the 4100 mm2/s KV40 in
   `DL2-14639.pdf` is HiTEC 12200's, not 12204L's). None is an uncaptured element content. This is a finding for those
   19 rows only; source-to-JSON coverage of the old sources in general remains unassessed.

## Visual checks still outstanding (9)
`DL2-14862.pdf` p.15 analytical rows; `DL2-13364.pdf` pp.2, 8, 9 (approval marks); `DL2-14863.pdf` p.2 (approval dots);
`DL2-11421.pdf` p.8 (X marks); `DL2-13146.pdf` pp.2-3 (claim graphics); `DL2-14235 / 14237 / 14239` p.1 (same template
as the verified `DL2-13961.pdf`, not viewed); `DL2-15753.pdf` pp.1-2 (claim letters); `DL2-12611.pdf` p.1 (bench
results); `DL2-12202.pdf` pp.2-6 (claim status superscripts).

## Exact next steps, in order

1. **Afton — next document: `DL2-11597.pdf`** (HiTEC 9450 book; HiTEC 5748 on pp.4, 10, 11, 18, 23, 27), then the other
   28 documents that name HiTEC 5748 in other packages' formulations (ledger rows `AFTON_HITEC_5748`, status "not yet
   assessed"). Then: read old sources `DL2-14639.pdf`, `DL2-11412.PDF`, `DL2-12074.pdf`, `DL2-15016.pdf`,
   `DL2-11418.pdf`, `DL2-15021.pdf`, `DL2-15365.pdf`, `DL2-10367.pdf`, `DL2-15568.pdf`, `DL2-11796.pdf` manually so the
   74 "automated search only" rows can become ready; obtain a local copy of the HiTEC 12204L PDS (registered SHA-256
   7a1e57d8...). Unresolved: 18 GE220 certificates, "HiTEC 8799B(+)".
2. **Lubrizol — next document: `DL2-11898.pdf`** (C-12787 Issue 2, Lubrizol 16008 engine-test report, 22 pp.), then
   `DL2-11897.pdf`, `DL2-12416.pdf`, `DL2-12610.pdf`, `DL2-12609.pdf`, `DL2-12187.pdf`, `DL2-13620.pdf`,
   `DL2-12189.pdf`, `DL2-12185.pdf`. Re-read old sources `DL2-11503.pdf`, `DL2-13065.pdf`, `DL2-13713.pdf`.
3. **Infineum — next document: `DL2-13079.pdf`** (D3320, 22 pp.), then D3384 (`DL2-13000`, `13080`, `13081`, `13082`,
   `13139`, `12997`, `13682`), D3396 / D3398, D3416 / D3417 (`DL2-15564`, `15332`), D3451 (`DL2-12856`, `13311`,
   `13801`, `12623`), D3453 (read the record and its sources: proposal provisional), D3463, D3503 (`DL2-11679` SDS,
   `15685`, `11768`, `12772`), D3511 (`DL2-15388`).
4. **Revision candidates:** `DL2-13111.pdf` (OLOA 59766), `DL2-14994.pdf` (Synfluid PAO 4), and the F candidates of the
   text search still listed in the ledger.
5. **Other suppliers (910 links)** in ledger order; most are base oils named in other products' formulations.
6. **Source-to-JSON coverage** of the 223 exact-duplicate documents: not assessed.

To resume: add a decision file in `decisions/` (later files override earlier links; `field_overrides` patch rows),
run `scripts/02_build.py`, `scripts/03_checks.py`, then `scripts/04_make_zip.py` (numbered ZIPs, never overwrites).
