p = r'C:\Users\windo\sf-wsA\docs\data_policy_mandatory_review\CHANGELOG_2026-11-10.md'
s = open(p, encoding='utf-8').read()
reps = [
("""- **Lead cases.** 362 product × property cases were reviewed: the 352 frozen from the revision-2 ledger plus 10 found during the review. Every case has a recorded outcome, with the source and page read (text layer or render), what is printed, the identity finding and the resulting change.

  | Outcome | Cases |
  |---|---:|
  | usable evidence | 79 |
  | already recorded | 32 |
  | unrelated mention | 71 |
  | insufficient evidence | 173 |
  | unresolved identity | 7 |
""",
"""- **Lead cases.** 363 product × property cases were reviewed: the 352 frozen from the revision-2 ledger plus 11 found during the review (corrected 2026-11-11 from "362"; see "Count reconciliation" below). Every case has a recorded outcome, with the source and page read (text layer or render), what is printed, the identity finding and the resulting change.

  | Outcome | Cases |
  |---|---:|
  | usable evidence | 81 |
  | already recorded | 31 |
  | unrelated mention | 71 |
  | insufficient evidence | 173 |
  | unresolved identity | 7 |
"""),
("""- **Name-match document links.** All 174 were reviewed: 84 same product, 78 byte-identical copies, 9 other product. The 9 are excluded from the coverage ledger.""",
"""- **Name-match document links.** All 174 (product, document) pairs were reviewed: 87 same product, 78 byte-identical copies, 9 other product (87 + 78 + 9 = 174; the earlier "84" omitted 3 same-product pairs, see below). The 9 are excluded from the coverage ledger."""),
("""| Filled (11 fields) |""", """| Filled (11 fields: 9 single value objects + 2 CCS lists with 5 points) |"""),
("""| Conflicts added (not resolved) | `EVR-2026-11-10-ETRO4`, `-CV2301`, `-110-density`, `-230-density`, `-500-density`. The fields are added to `PENDING_FIELDS`. |""",
"""| Conflicts added (not resolved) | `EVR-2026-11-10-ETRO4`, `-CV2301`, `-110-density`, `-230-density`, `-500-density`. The fields are added to `PENDING_FIELDS`. Three more were added on 2026-11-11 (external-source review, below). |"""),
("""  - adds the SDS values recorded in the review (70 pairs; 141 in total);""",
"""  - adds the SDS values recorded in the review (71 comparison rows for 70 product × property cases; 141 rows in total);"""),
]
for a, b in reps:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
s = s.rstrip('\n') + '\n' + """
## Count reconciliation (2026-11-11; every number recomputed from the generated records)

| Number | Counting unit | Composition | Generated record |
|---|---|---|---|
| 174 associations | (product, document) pair linked by name only, in the revision-2 ledger (`4e83652`) or the current one | 87 same product + 78 byte-identical copies + 9 other product | `name_match_review.csv` |
| 3 (the missing three) | associations reviewed as the same product and then used as fill sources, so the current ledger lists them as cited, not as name matches | EXXONMOBIL_SPECTRASYN_ULTRA_1000 / DL2-13746.pdf, NESTE_NEXBASE_3060 / DL2-12735.pdf, NESTE_NEXBASE_3080 / DL2-14512.pdf (column `now_cited`) | `name_match_review.csv` |
| 363 lead cases | product × property, deduplicated | 352 (revision-2 ledger) + 11 added: 8 linked by corrections (ETRO 4, PRIMA 110/230/500), PRIMA 500 KV40 and CCS (kept after their fill), NEXBASE 3080 flash point (appeared when its SDS p.4 stopped being classified as technical) | `lead_review.csv` |
| 81 usable evidence | lead case | 11 fill cases + 70 comparison cases (69 "comparison added" + CV2301 flash point, also a conflict) | `lead_review.csv` |
| 71 comparison rows | (product, property, SDS document) row added to the inventory | 70 product × property cases; S_OIL_ULTRA_S_3 flash point has two SDSs | `lead_review_decisions.json` → `tds_sds_comparisons.csv` (origin "lead review") |
| 141 comparison rows | TDS–SDS pair | 71 from the lead review + 70 from the audit, `conflicts[]` and `alternate_entries` | `tds_sds_comparisons.csv` |
| 11 filled fields | field (a value object or a whole CCS list) | 9 single-field fills (`CHANGES`) + 2 list fills (ETRO 6 CCS with 3 points, PRIMA 500 CCS with 2 points) | `source_selection_changes.csv` |
| 39 declared selections | `CHANGES` entry (one value object each) | 28 (revision 1: Richful, D3424, NEXBASE 3020) + 2 (revision 2: FORMOSA KV100) + 9 (revision 3 fills) | `source_selection.py` |
| 2 qualifier corrections | value object | ERGON 5000BS and P70N VI | `source_selection_changes.csv` |
| 8 conflicts added | `conflicts[]` entry | 5 (2026-11-10) + 3 (2026-11-11) | `source_selection_changes.csv` |
| 51 change-list rows | row of the change list | 39 selections + 2 list fills + 2 qualifier corrections + 8 conflicts | `source_selection_changes.csv` |

Corrected errors:
- "84 same product" omitted the 3 now-cited pairs, because the association review read only the current ledger. The review universe is now frozen at `4e83652` (as for the lead cases), and the pairs stay reported with `now_cited = true`.
- LUBRIZOL_CV2301 pour point had a reviewed SDS comparison, but its case fell under the generic Lubrizol "already recorded" rule. That rule now excludes cases with a reviewed comparison (`exclude_if_comparison`), so the case is usable evidence. Already recorded: 32 → 31; usable: 79 → 81 (with the added NEXBASE 3080 case).
- NEXBASE 3080 flash point had a reviewed comparison but no lead case; it is now in `added_cases`.

---

# Revision 3 completion, 2026-11-11 (external-source review, count reconciliation, check runner)

## External-source review

- **New tool** `tools/data_policy/external_review.py` with `external_review_decisions.json`; output `reports/data_policy/external_review.csv`. It stops if a decision no longer matches the record or a stored evidence hash changes.
- **Cases.** 29 product × property cases: the 22 values the ledger marks `external_selected`, plus 7 pending fields whose open question is an external technical source (AFTON_HITEC_8788B KV40/KV100/density/flash point; S_OIL_ARAMCO_ULTRA_8 KV40/KV100/flash point).

  | | Confirmed | Inconclusive: source unavailable |
  |---|---:|---:|
  | external selected values (22) | 18 | 4 (AFTON_HITEC_12204L KV100, density, flash point, TBN) |
  | pending, external alternative (7) | 3 (aramcoULTRA 8) | 4 (AFTON_HITEC_8788B) |

- **Evidence.** The aramcoPRIMA 230 sheet, the PRIMA 230 SDS, the MOGO 2025 flyer and the Aramco 2024 catalog were obtained with bytes equal to their `source_registry.json` SHA-256. The Richful data feeds were retrieved on 2026-11-11 and agree with the archived TDS. The S-OIL values were read on the two saved copies in `reconciliation/audit_evidence/` (hashes verified). The two Afton PDSs could not be obtained: the Internet Archive refused automated download and the fetch tool cannot open web.archive.org, so their values were **not** re-read.
- **Stored copies** (small files only): `reports/data_policy/external_evidence/` (4 files, marked `-text` so line endings are never converted). The 15 MB flyer and the catalog are not stored; their hashes are recorded.
- **Conflicts recorded (not resolved):**
  - `EVR-2026-11-11-230-noack`: the Aramco sheet's typical Noack 7.5 lies above the DL2-12172.pdf maximum 7;
  - `EVR-2026-11-11-230-density-external`: the Aramco sheet's 0.8635 kg/L is a third PRIMA 230 density (the field is already pending);
  - `EVR-2026-11-11-ULTRA8-kv40`: the S-OIL typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt.
- **Not changed:**
  - two representation notes (BAPbase 4 KV40 value_kind "single" under a "typical" column; aramcoULTRA 8 CCS qualifier "Typical"), because both read as point values in every check;
  - the PRIMA 230 CCS −20 °C point, because the fill rule covers Missing fields only;
  - the BAPbase 4 specific gravity printed by the distributor flyer (a policy decision on external sources).
- The `source_selection.PENDING` reasons for AFTON_HITEC_8788B and S_OIL_ARAMCO_ULTRA_8 now state the review result.

## Review states

- **New tool** `tools/data_policy/source_review_status.py`; output `reports/data_policy/source_review_status.csv`. Each of the 2,175 ledger rows gets one state:

  | State | Rows | Mandatory |
  |---|---:|---:|
  | archive lead review complete | 183 | 61 |
  | external review complete | 21 | 16 |
  | evidence unavailable (173 archive cases not printed + 8 external cases without a copy) | 181 | 81 |
  | evidence inconclusive (identity) | 7 | 2 |
  | not individually reviewed (mechanical classification only) | 1,783 | 745 |

## Check runner

- **New tool** `tools/data_policy/run_checks.py`. Each step is its own subprocess; its real return code and full output are saved in `test_results/NN_<step>.txt`, with `summary.md` / `summary.json`. A by-design failure (`verify_revision.py`) is reported as "expected failure", never as a pass.
- The four earlier result files (`01_pipeline.txt` … `04_protected_files.txt`) were produced through pipes that hid return codes. They are replaced; Git history keeps them.
- The runner exposed a masked non-zero return code: `integration_diff.py --changed` exits 1 whenever any derivation difference exists. It now takes `--against REF` and labels each difference pre-existing or NEW. All 27 differences in the 18 changed files are pre-existing at the baseline `f4d97e7`; none is new.

## Data fingerprint after these changes

- Exact bytes: `58093014f2e6da28a4b24ef3b14cb835f48beb559e9c5a3fff2463472bc8828f`. LF-normalised (informational): `9826e935d42d8fa7ede95eb42a9eac4b613e39aad166fc9e9f6a832fcb093ae7`.
- Eligibility is unchanged: 10 of 181 base oils, 0 packages, 0 components. The only interface change against revision 2 remains S_OIL_ARAMCO_ULTRA_8 `tier1_complete` true → false.
"""
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
