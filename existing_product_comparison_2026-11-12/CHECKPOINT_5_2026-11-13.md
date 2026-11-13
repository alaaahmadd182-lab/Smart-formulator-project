# Checkpoint 5 — old-versus-new comparison (fifth pass, 2026-11-13)

Supersedes the status sections of checkpoints 1-4 (kept unchanged). Comparison and proposal preparation only: nothing
ingested, no JSON or production file changed, nothing staged or committed. `logs/03_checks.log`: 54 of 54 checks pass
(structural checks; manual verification is recorded per row).

**Not complete:** 895 of 1,068 non-duplicate links (other suppliers) are not yet assessed.

## 1. Retrieval of the two registered Afton PDS (authorized, read-only)

| File (in `retrieved_evidence_2026-11-13/`) | HTTP | Bytes | SHA-256 | Registered hash |
|---|---|---|---|---|
| `HiTEC-12204L_PDS__registered_url.pdf` (edition 06/17) | 200 | 257,189 | 7a1e57d8…a74183e | match |
| `HiTEC-8788B_PDS__registered_url.pdf` (edition 02/19) | 200 | 438,400 | c09305fb…6fd811fe | match |

Bytes saved as downloaded; `source_registry.json` and the existing evidence were not touched (`RETRIEVAL_LOG.txt`).
`scripts/02_build.py` now also looks in this folder for local copies (only files whose hash equals a registered hash).

**Findings.**
- HiTEC 12204L PDS: confirms what the record holds (TBN 82, 8.11 lbs/gal, SG 0.972, KV100 190, flash 135 min, 14.2 % wt)
  and prints no element content, KV40, density in g/ml, API SL, formulation or named co-component. The proposals from
  the May-19 programme book and the SDS therefore remain genuinely new.
- **HiTEC 8788B PDS: information in a source the record already cites was never captured** — typical TBN 71 mg KOH/g;
  two 17.7 % SAE 10W-40 routes (Group I/III mix: 14 claims; Group III: 12 claims, no Cummins CES 20078 / Detroit
  DDC93K215) with the footnote "OEM claim availability dependent on VM choice"; technical typicals for KV100, density and
  flash point (now taken from the SDS). Listed in `tables/existing_source_information_not_captured.csv` (3 reviewed rows).
  The certificate TBN limits (68-79, target 73) are now an alternate specification entry beside the typical 71.

## 2. Reconciliation of the 28 provisional proposals of checkpoint 4

Provisional reasons can overlap (one proposal can have several). At checkpoint 4 there were 31 reason instances on
28 proposals: 13 HiTEC 12204L "primary old source not available"; 4 HiTEC 12250 "old source not reviewed"; 4 HiTEC 8788B
(3 "PDS not re-checked" + 1 duplicate instance from the treat-rate row's two-part reason); 1 HiTEC 12250 "current JSON not
compared"; 9 "possible overlap". Overlaps: the 12204L claims row had two reasons; the 8788B treat-rate row was counted
twice; the 12250 no-template-field row had two reasons. 31 − 3 = 28.

The 20 proposals that depended on the two unavailable PDS, after reading them (not automatically):

| Product | Rows | Now ready | Other result |
|---|---|---|---|
| HiTEC 12204L | 13 | 13 | the claims row's overlap flag came from tokens it does not propose (API CI-4 Plus already present); narrowed to the claim actually proposed (API SL), checked against the PDS and the `DL2-13364.pdf` p.8 image |
| HiTEC 12250 | 4 | 3 | 1 still provisional: a property without template field ("current JSON not compared") |
| HiTEC 8788B | 3 | 2 | the treat-rate row is withdrawn (`no_change`): the cited PDS already prints the 17.7 % routes, now proposed as uncaptured old-source information |

Before marking them ready, the table pages used were verified as images: `DL2-14862.pdf` pp.5-6 (neat vs "@ 14.2 %wt"
column), `DL2-13364.pdf` p.17 (8788B formulation and claim dots).

Of the other 8 overlap-flagged proposals, none changed status in this pass. Now: **9 provisional = 8 "possible overlap with existing entries" + 1 "current
JSON not compared"; no proposal currently has more than one reason.** 125 proposals in total, 116 ready for a reviewer
decision.

## 3. Safeguard correction (HiTEC 5748 / 5748A)

`scripts/03_checks.py` lines 104-125. The identity check now covers every proposing action (`propose_*`, including
`propose_update_with_history`, `propose_selection_review*`, `propose_record_conflict`, `propose_historical_note`, unscoped
`propose_note`). The only exception is a note whose reason states the interchangeability, its scope, and that no 5748A data
is used. Regression rows: a value update of HiTEC 5748 from 5748A text via `propose_update_with_history` is caught, as are
selection review, conflict, historical note and an unscoped note; the scoped interchangeability note and `no_change` pass.
The earlier, narrower regression (add / alternate) is kept.

## 4. Other suppliers started

- **Petronas ETRO 4+ / ETRO 6+:** every mention is third-party (Afton, Infineum). Neat batch analyses by Afton
  (RIC25-01607 / -01608; one batch each, also repeated in `DL2-15799.pdf`) are recorded as batch evidence, no change.
  `DL2-14915.pdf` prints "Etro plus 4 / Etro plus 6" (identity probable, not established) with densities 0.8290 / 0.8416
  at 15.6 C, **no unit**, unknown basis. ETRO 4+'s mandatory density stays Missing (the Petronas PDS prints 0.8306 kg/L
  without temperature); only an open-question note is proposed. Infineum recipes: recipe evidence only.
- **aramcoULTRA 8:** an Afton batch analysis (KV40 41.180, KV100 7.131) is recorded as third-party batch evidence and does
  not resolve the open KV40 conflict. `DL2-15747.pdf` labels it "AramcoULTRA 8 (Ultra S)": recorded as identity evidence for
  the open ID-01 question, not as a resolution. Other mentions are recipe shares.

## 5. Process notes

- A reading command run without `PYTHONDONTWRITEBYTECODE` created `tools/data_policy/__pycache__/`; the preservation
  check caught the Git-state change; the generated cache was removed and the state hash is back to 2de292fe3eabccb9.
- The certificate check caught a decision whose wording ("not … a batch result") was read as a batch value; the wording
  was corrected, the check was not changed.

## 6. Exact next steps

1. Other suppliers in ledger order of volume: `YUBASE_4` (114 links), `YUBASE_6` (86), `EXXONMOBIL_EHC_50` (62),
   `NESTE_NEXBASE_3043` (55), `EXXONMOBIL_EHC_110` (49), `CHEVRON_GROUP_II_220R` (46), … (`scripts/hits.py <id>`). The Afton
   base-stock tables (HiTEC 11356 p.16; HiTEC 11455 p.20) hold batch analyses for many of these: batch evidence only.
2. Unread content listed in checkpoint 4 §3 (unchanged).
3. Unresolved identity: 18 GE220 certificates; "HiTEC 8799B(+)".
4. Source-to-JSON coverage of the 223 exact-duplicate documents: not assessed.
