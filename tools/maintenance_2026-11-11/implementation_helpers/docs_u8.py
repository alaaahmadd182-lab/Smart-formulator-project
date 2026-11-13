R = 'C:\\Users\\windo\\sf-wsA\\'
D = 'docs\\data_policy_mandatory_review\\'
FP = '93b704a79b5844430af87d15f53058ec3df106ad262af4236fb52da1621f3530'
LF = '6440b6800a2946ad8de0c419af5458695702c7e8fb0dced5230d086794a9474d'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b):
    assert s.count(a) == 1, (a[:80], s.count(a))
    return s.replace(a, b)


def line(s, prefix, new):
    ls = s.split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    if new is None:
        del ls[hit[0]]
    else:
        ls[hit[0]] = new
    return '\n'.join(ls)


# =================================================================== recommendation (three corrections + status)
rel = D + 'recommendation_aramcoULTRA8_source_selection.md'
s = load(rel)
s = sub(s, 'Date: 2026-11-11. Status: **recommendation for review. No value, record, requirement or threshold has been changed.** Both product records (`S_OIL_ARAMCO_ULTRA_8`, `S_OIL_ULTRA_S_8`) and the open merge question ID-01 are untouched.',
        'Date: 2026-11-11. Status: **accepted and implemented on 2026-11-11, with three corrections to this text (listed at the end).** The three selections are in the records; no requirement or threshold was changed. Both product records (`S_OIL_ARAMCO_ULTRA_8`, `S_OIL_ULTRA_S_8`) stay separate, and the merge question ID-01 stays open.')
s = line(s, '| Date | Undated. Captured',
         '| Edition date | **Unknown: the page prints no publication or revision date.** It was captured on 2026-06-10 (Internet Archive) and retrieved on 2026-10-30 (live); the two saved copies print identical tables. A capture or retrieval date shows only that the page existed then; it does not establish when it was published or revised | Rev. 0, revision date 2018-09-07 |')
s = line(s, '| Is a difference computable? |',
         '| How the pair is compared | Under our current comparison policy a point is checked against a range (inside or outside) and is not differenced. A distance from the range limit could be calculated (41.10 is 0.90 cSt below 42.0); the policy does not use it, and no threshold applies | Same policy: checked, not differenced | Same policy: checked, not differenced |')
s = line(s, '| Edition | The page is undated, but the captures show',
         '| Edition | The edition date of the page is unknown. Whether it is newer or older than the 2018 SDS cannot be established from the capture dates. This does not block the selection: Rule 1 prefers the technical source over the SDS by document class, not by date, and there is no second technical edition for this grade, so the "undated disagreeing editions" rule (technical vs technical) does not apply. The unknown date is kept as a caveat in each selected value. |')
s = line(s, '| Internal consistency of the technical table |', None)
s = sub(s, 'If you disagree on one point, the weakest one is the undated page:', 'The weakest point is the unknown edition date of the page:')
s = sub(s, '- **KV40.** Why a current typical lies below the 2018 SDS range is unknown.', '- **KV40.** Why the table typical lies below the 2018 SDS range is unknown, and so is which of the two documents is newer.')
s = sub(s, '- **Thresholds.** None applies: point-vs-range pairs are bound checks, not differences.', '- **Thresholds.** None applies: under the current comparison policy, point-vs-range pairs are bound checks.')
a = s.index('## Effect if implemented (nothing is implemented now)')
s = s[:a] + """## Implemented on 2026-11-11

- **Confirmation.** `tools/data_policy/verify_soil_table.py` read the three cells in both saved copies (hashes equal to the evidence manifest): table caption "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8", the row labels and ASTM cells quoted above.
- **Selections** (declared in `source_selection.py`): KV40 41.10 cSt at 40 °C, D445; KV100 7.1 cSt at 100 °C, D445; flash point 250 °C, COC, D92. Each value is typical, cites the page URL with `revision_date` null, and names both saved copies with their SHA-256 and the unknown edition date.
- **SDS values.** The three SDS ranges are alternate entries with their page and revision date.
- **KV40 disagreement.** The existing 2026-10 audit conflict is kept, unresolved, with a dated note. It was not duplicated, and the v5 audit was not edited.
- **Pending.** The three fields are no longer pending.
- **Eligibility (calculated).** S_OIL_ARAMCO_ULTRA_8 is now Tier 1 complete and formulation-eligible, with an open-conflict warning on KV40: 11 of 181 base oils (10 before). Interface columns and requirements version are unchanged; one row and the data fingerprint changed.
- **Not done.** The KV100 and flash-point point-vs-range relations are recorded in each value's note and in `external_review.csv`, not as rows of the TDS–SDS inventory: the inventory pairs archive technical values with SDS values and does not yet pair external technical values.

## Corrections made to this recommendation (2026-11-11)

1. An earlier version said the captures showed the page "was current in 2026, later than the 2018 SDS". A capture or retrieval date does not establish a publication or revision date. The edition date is unknown.
2. An earlier version cited an indicative viscosity-index calculation that used constants from memory. It is removed and is not selection evidence.
3. An earlier version said a point-vs-range difference was "not computable". The accurate statement is that our current comparison policy checks a point against a range and does not difference them.
"""
save(rel, s)

# =================================================================== HANDOFF
rel = D + 'HANDOFF.md'
s = load(rel)
s = line(s, '   - **Cases.** 29 product × property cases:',
         '   - **Cases.** 29 product × property cases: 25 values selected from registered URLs (22 at the time of the review, plus the 3 aramcoULTRA 8 selections of 2026-11-11), and 4 pending fields whose open question is an external source (AFTON_HITEC_8788B).')
s = line(s, '   - **Confirmed as printed: 21**',
         '   - **Confirmed as printed: 21**, all of them selected values now. "Confirmed" is not an approval to select a source; each selection is a separate declared decision. Of the 21: 20 manufacturer-issued, 1 distributor-issued (BAPbase 4 KV40); all 21 name the record\'s exact grade. For the 8 aramcoULTRA 8 cases the separate merge question ID-01 is open and does not restrict the use of the table (`requirements_review.md` §4).')
s = line(s, '4. **Evidence-supported corrections only**',
         '4. **Evidence-supported corrections only** (declared, idempotent, 53 rows in `source_selection_changes.csv`):\n'
         '   - **3 aramcoULTRA 8 selections (2026-11-11):** KV40 41.10 cSt, KV100 7.1 cSt and flash point 250 °C (COC) from the S-OIL manufacturer table, confirmed on both saved copies; the SDS ranges are kept as alternates; the KV40 disagreement stays an unresolved conflict; the edition date of the page is unknown ([recommendation](recommendation_aramcoULTRA8_source_selection.md));')
s = sub(s, 'applied: 39 declared selections, plus list fills', 'applied: 42 declared selections, plus list fills')
s = sub(s, '| Pending source selections | 37 fields, each with a reason', '| Pending source selections | 34 fields, each with a reason')
s = sub(s, 'Accepting all ranges and bounds: still 10 eligible', 'Accepting all ranges and bounds: still 11 eligible')
s = line(s, '- **Data fingerprint, exact bytes**', f'- **Data fingerprint, exact bytes** (authoritative; CRLF checkout): `{FP}`.')
s = line(s, '- **LF-normalised fingerprint**', f'- **LF-normalised fingerprint** (informational only): `{LF}`.')
s = sub(s, '| base_oil | 181 | 10 | 11 |', '| base_oil | 181 | 11 | 11 |')
s = sub(s, '| **Total** | **264** | **10** | **11** |', '| **Total** | **264** | **11** | **11** |')
s = line(s, '**Eligible:**', '**Eligible:** ADNOC_ADBASE_4CST, 6CST and 8CST; PETRONAS_EQUINAS_8; PETRONAS_ETRO_6_PLUS (open-conflict warnings on KV40 and density); PETRO_CANADA_PURITY_VHVI_2, 3, 4, 6 and 8; S_OIL_ARAMCO_ULTRA_8 (open-conflict warning on KV40).')
s = sub(s, '**Change from revision 2.**', '**Changes (calculated by the eligibility build, not assumed).**')
s = line(s, '- S_OIL_ARAMCO_ULTRA_8 `tier1_complete` changes from true to false',
         '- **Revision 2 → revision 3 (`43e7f8b`): 10 eligible.** S_OIL_ARAMCO_ULTRA_8 `tier1_complete` went from true to false, because the interface meaning was restored and its KV40/KV100 source selection was pending.\n'
         '- **Revision 3 → current working tree (2026-11-11, uncommitted): 11 eligible.** The three aramcoULTRA 8 technical-source selections make its KV40 and KV100 typical point values, so all its mandatory requirements are met. Only this row changed: `tier1_complete` and `formulation_eligible` false → true, `missing_mandatory_properties` now empty, with a KV40 open-conflict warning in `eligibility_reasons`.')
s = line(s, '- The eligible products are unchanged.', '- No other product changed. The columns and the requirements version are unchanged; the data fingerprint changed, so Workstream B must recompute.')
s = sub(s, '| | unresolved source selection | 16 |', '| | unresolved source selection | 14 |')
s = line(s, '- aramcoULTRA 8, two separate points:',
         '- aramcoULTRA 8: the KV40 disagreement between the selected table typical (41.10 cSt) and the SDS range (42.0–55.0 cSt) is unresolved, and the edition date of the S-OIL page is unknown. Only the supplier can settle either. The merge question ID-01 (one product with Ultra-S 8?) is open; both records stay separate;')
s = sub(s, 'Run on 2026-11-11 at revision-3 commit `43e7f8b` plus the uncommitted policy-decision changes of the same day.',
        'Run on 2026-11-11 at revision-3 commit `43e7f8b` plus the uncommitted changes of the same day (policy-decision preparation and the aramcoULTRA 8 selections).')
a = s.index('| 1–11 | pipeline (document classes → eligibility) | 0 each | pass |')
b = s.index('- **Expected incomplete verification is not an execution failure.**')
s = s[:a] + """| 1–8, 10–12 | pipeline (document classes → eligibility) | 0 each | pass |
| 9 | `verify_soil_table.py` | 0 | pass: the three aramcoULTRA 8 cells read in both saved copies; hashes match the manifest; the record holds them |
| 13 | `build_eligibility.py --check` | 0 | pass (up to date) |
| 14 | coverage matrix | 0 | pass (validation issues 30) |
| 15 | `integrate_products.py` dry run | 0 | pass (annotations 10/10, conflict rules 16/16; **do not `--write`**) |
| 16 | `integration_diff.py --changed --against f4d97e7` | 0 | pass: 13 differences in the 2 product files changed since `43e7f8b`, all pre-existing at the baseline, 0 new |
| 17 | `verify_preserved.py` | 0 | pass (section 6) |
| 18 | protected paths vs baseline | 0 | pass (no differences) |
| 19 | product JSON valid, status vocabulary | 0 | pass (706 files) |
| 20 | `tools/mandatory_properties/tests` | 0 | 31 OK |
| 21 | `tools/data_policy/tests` | 0 | 52 OK |
| 22 | `tools/audit/review_2026-11-02/tests` (v5) | 0 | 12 OK |
| 23 | `verify_revision.py` (v5) | 1 | **expected failure (by design):** it compares with `545fd3d`, and product JSON and the workbook changed since |

""" + s[b:]
s = sub(s, 'are outcomes inside steps 6–8, which return 0.', 'are outcomes inside steps 6–8, which return 0. The runner deletes the step files of an earlier run before it starts, so no stale result remains.')
s = sub(s, 'python tools/data_policy/source_review_status.py             # source_review_status.csv\n',
        'python tools/data_policy/source_review_status.py             # source_review_status.csv\n'
        'python tools/data_policy/verify_soil_table.py                # aramcoULTRA 8 values against the saved manufacturer table\n')
save(rel, s)

# =================================================================== source_review_coverage.md
rel = D + 'source_review_coverage.md'
s = load(rel)
s = sub(s, '| pending (identity, conflicting technical documents, reliability) | 37 | 19 |', '| pending (identity, conflicting technical documents, reliability) | 34 | 17 |')
s = sub(s, '| external (URL) source selected (all reviewed: see `external_review.csv`) | 22 | 14 |', '| external (URL) source selected (all reviewed: see `external_review.csv`) | 25 | 16 |')
s = line(s, '| S_OIL_ARAMCO_ULTRA_8 | KV40, KV100, flash point |', None)
s = sub(s, '## Remaining gaps',
        '**No longer pending (2026-11-11):** S_OIL_ARAMCO_ULTRA_8 KV40, KV100 and flash point. The S-OIL manufacturer-table typicals are selected; the SDS ranges are alternates; the KV40 disagreement stays an unresolved conflict; the edition date of the page is unknown (`recommendation_aramcoULTRA8_source_selection.md`).\n\n## Remaining gaps')
s = sub(s, '- source-specific open points on external evidence: the aramcoULTRA 8 KV40 conflict and the distributor-issued flyer for BAPbase 4; separately, the merge question ID-01.',
        '- open points on external evidence: the unresolved aramcoULTRA 8 KV40 conflict, the unknown edition date of the S-OIL page, and the distributor-issued flyer for BAPbase 4; separately, the merge question ID-01.')
save(rel, s)

# =================================================================== evidence_review.md
rel = D + 'evidence_review.md'
s = load(rel)
s = line(s, '| Source-specific open points on external evidence',
         '| Open points on external evidence (aramcoULTRA 8: unresolved KV40 conflict and unknown edition date of the S-OIL page; BAPbase 4: distributor-issued flyer) | 1 conflict + 1 unfilled field | The aramcoULTRA 8 table typicals were selected on 2026-11-11 (technical source first); the disagreement is recorded separately and only the supplier can settle it. A distributor description is not accepted automatically. |')
s = sub(s, '- the 22 values the ledger marks `external_selected` (selected from a URL registered in `source_registry.json`);\n- the 7 pending fields whose open question is an external technical source: AFTON_HITEC_8788B KV40/KV100/density/flash point, and S_OIL_ARAMCO_ULTRA_8 KV40/KV100/flash point.',
        '- the 22 values the ledger marked `external_selected` at the time of the review (selected from a URL registered in `source_registry.json`);\n- the 7 fields that were pending with an external technical source as their open question: AFTON_HITEC_8788B KV40/KV100/density/flash point, and S_OIL_ARAMCO_ULTRA_8 KV40/KV100/flash point.\n\n**Update of 2026-11-11.** The three aramcoULTRA 8 fields were then selected from the S-OIL table (technical source first), so the ledger now has 25 `external_selected` values and 4 pending fields with an external alternative. Outcomes are unchanged: 21 confirmed as printed, 8 inconclusive.')
save(rel, s)

# =================================================================== requirements_review.md
rel = D + 'requirements_review.md'
s = load(rel)
s = sub(s, 'kv40: 32 (abs 13, bnd 14, sel 5); kv100: 33 (abs 12, bnd 17, sel 4)', 'kv40: 31 (abs 13, bnd 14, sel 4); kv100: 32 (abs 12, bnd 17, sel 3)')
s = sub(s, 'If all ranges and bounds were accepted today, the eligible count would stay 10', 'If all ranges and bounds were accepted today, the eligible count would stay 11')
a = s.index('  Restrictions on the aramcoULTRA 8 table values, each with its evidence:')
b = s.index('## 5. Rules the implementation does not add')
s = s[:a] + """  **Selected on 2026-11-11** (technical source first; the disagreement with the SDS is recorded separately and is not a selection veto):
  - **KV40:** 41.10 cSt at 40 °C (D445), typical. It lies below the SDS range 42.0–55.0 cSt; that disagreement is the existing 2026-10 audit conflict, kept unresolved.
  - **KV100:** 7.1 cSt at 100 °C (D445), typical. Inside the SDS range 7.0–7.5: logically compatible, not agreement.
  - **Flash point:** 250 °C, COC (D92), typical. Inside the SDS range 240–260: logically compatible, not agreement.
  - The SDS ranges are alternate entries with their provenance. The page prints no publication or revision date, so its edition date is unknown; each value says so.
  - Calculated effect: all mandatory requirements of this product are met, so it is Tier 1 complete and eligible (11 base oils), with a KV40 open-conflict warning. No requirement was changed to obtain this.
  - ID-01 stays open, and both records stay separate.

""" + s[b:]
save(rel, s)

# =================================================================== source_selection_policy.md (dated note; table kept as written)
rel = D + 'source_selection_policy.md'
s = load(rel).rstrip('\n') + """

## Update of 2026-11-11: S_OIL_ARAMCO_ULTRA_8

The table above lists S_OIL_ARAMCO_ULTRA_8 as pending ("external web table vs SDS ranges"). That is superseded. External evidence is admissible, and each source is assessed on authority, authenticity, exact product identity, applicability and provenance. The S-OIL manufacturer table names aramcoULTRA 8, so its typical values for KV40, KV100 and flash point are selected under the technical-source-first rule, with the SDS ranges kept as alternates. The KV40 disagreement with the SDS stays an unresolved conflict: a disagreement is recorded and assessed separately and is not a selection veto. The edition date of the page is unknown. Declared selections are now 42, and pending fields 34.
"""
save(rel, s)

# =================================================================== tools/README.md
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, '| Regression tests (46): Rule 1,', '| Regression tests (52): technical-source selection keeps the SDS alternate and never resolves a disagreement (aramcoULTRA 8), Rule 1,')
s = sub(s, "| `data_policy/source_review_status.py` |", "| `data_policy/verify_soil_table.py` | Confirms the S_OIL_ARAMCO_ULTRA_8 KV40, KV100 and flash-point values against both saved copies of the S-OIL manufacturer table (caption, column, row label, ASTM cell, printed cell; copy hashes against the manifest); exits 1 on a mismatch | nothing |\n| `data_policy/source_review_status.py` |")
save(rel, s)

# =================================================================== curated log and changelog (appended)
rel = 'open_questions_and_conflicts.md'
s = load(rel).rstrip('\n') + """

### 2026-11-11: S_OIL_ARAMCO_ULTRA_8 technical-source selections

- KV40, KV100 and flash point now hold the typical values of the S-OIL manufacturer table "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8": 41.10 cSt at 40 °C (D445), 7.1 cSt at 100 °C (D445) and 250 °C COC (D92). They were confirmed on both saved copies (`tools/data_policy/verify_soil_table.py`).
- The SDS ranges of DL2-14611.pdf (42.0–55.0 cSt, 7.0–7.5 cSt, 240–260 °C; 2018-09-07) are kept as alternate entries.
- **Conflict, still unresolved:** KV40 typical 41.10 cSt vs SDS range 42.0–55.0 cSt (the 2026-10 audit entry; a dated note was added, nothing was duplicated). Selecting the technical value does not resolve it and does not judge the SDS wrong.
- **Open:** the S-OIL page prints no publication or revision date, so its edition date is unknown. Which document is newer cannot be established.
- **Open:** ID-01 (are aramcoULTRA 8 and Ultra-S 8 one product?). Both records stay separate.
- Eligibility, as calculated: S_OIL_ARAMCO_ULTRA_8 is Tier 1 complete and formulation-eligible, with a KV40 open-conflict warning. 11 of 181 base oils; 0 packages; 0 components.
"""
save(rel, s)

rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel)
s = line(s, '- **New document:** [recommendation_aramcoULTRA8_source_selection.md]', None)
s = s.rstrip('\n') + f"""

## aramcoULTRA 8 technical-source selections (2026-11-11, uncommitted)

Decision: select the applicable technical-source value; record and assess its disagreement with the SDS separately. A disagreement is not a selection veto.

- **Confirmed** on both saved copies of the S-OIL manufacturer table (new tool `verify_soil_table.py`; hashes equal to the evidence manifest): caption "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8", row labels, ASTM cells and printed cells.
- **Selected** (three `CHANGES` entries; `S_OIL_ARAMCO_ULTRA_8` tier 1 and tier 2):

  | Field | Before (SDS DL2-14611.pdf p.2, 2018-09-07) | After (S-OIL table, typical) |
  |---|---|---|
  | KV40 | range 42.0–55.0 cSt at 40 °C, ASTM D445 | 41.10 cSt at 40 °C, ASTM D445 |
  | KV100 | range 7.0–7.5 cSt at 100 °C, ASTM D445 | 7.1 cSt at 100 °C, ASTM D445 |
  | Flash point | range 240–260 °C, ASTM D92 | 250 °C, COC, ASTM D92 |

  - Each SDS range is kept in `alternate_entries` with its page and revision date.
  - Each selected value cites the page URL with `revision_date` null, both saved copies with their SHA-256, and the caveat that the edition date of the page is unknown (a capture or retrieval date is not an edition date).
- **KV40 disagreement:** the existing 2026-10 audit conflict in `conflicts[]` is kept unresolved, with a dated note appended. Nothing was duplicated, and the v5 audit files are unchanged.
- **Pending:** the `PENDING` entry for these three fields is removed. ID-01 stays open; `S_OIL_ULTRA_S_8` and `reconciliation/` are unchanged.
- **Recommendation document** added and then corrected (unknown edition date; the VI calculation from memory removed; point-vs-range described as the current comparison policy): [recommendation_aramcoULTRA8_source_selection.md](recommendation_aramcoULTRA8_source_selection.md).

Counts after the change, all from the generated outputs:

| Number | Before (`43e7f8b`) | Now | Counting unit |
|---|---:|---:|---|
| Declared selections (`CHANGES`) | 39 | 42 | value object |
| Change-list rows | 50 | 53 | row (42 selections + 2 list fills + 2 qualifier corrections + 7 conflicts) |
| Pending fields in the ledger | 37 (19 mandatory) | 34 (17) | ledger row |
| External source selected | 22 (14 mandatory) | 25 (16) | ledger row |
| External review cases | 22 selected + 7 pending | 25 selected + 4 pending | product × property; outcomes unchanged (21 confirmed, 8 inconclusive) |
| Base oils with unresolved source selection, KV40 / KV100 | 5 / 4 | 4 / 3 | product |
| Tier 1 complete = eligible base oils | 10 | 11 | product |
| Fully documented (companion) | 11 | 11 | product |
| TDS–SDS inventory rows | 141 | 141 | pair (the inventory does not pair external technical values with SDS values) |
| Product JSON files changed since the baseline | 17 | 19 | file |

- **Interface.** `product_eligibility.csv`: same columns, same requirements version. One row changed, S_OIL_ARAMCO_ULTRA_8: `tier1_complete` and `formulation_eligible` false → true, `missing_mandatory_properties` `["kv40", "kv100"]` → `[]`, with a KV40 open-conflict warning in `eligibility_reasons`. The fingerprint column changed in every row.
- **Fingerprint.** Exact bytes: `{FP}`. LF-normalised (informational): `{LF}`.
- **Tests.** `tools/data_policy/tests` 52 (six added in `TechnicalSelectionKeepsDisagreement`). `run_checks.py` has 23 steps (new: `verify_soil_table`) and removes the step files of an earlier run.
- **Not changed.** Mandatory requirements, the published-formulation rule, the thresholds (still proposed), the review states of the ledger rows.
"""
save(rel, s)
print('ok')
