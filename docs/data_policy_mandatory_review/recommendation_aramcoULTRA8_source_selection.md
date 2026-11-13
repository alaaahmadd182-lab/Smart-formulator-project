# Recommendation: source selection for S_OIL_ARAMCO_ULTRA_8 (KV40, KV100, flash point)

Date: 2026-11-11. Status: **accepted and implemented on 2026-11-11, with three corrections to this text (listed at the end).** The three selections are in the records; no requirement or threshold was changed. Both product records (`S_OIL_ARAMCO_ULTRA_8`, `S_OIL_ULTRA_S_8`) stay separate, and the merge question ID-01 stays open.

## Recommendation in one line

Select the S-OIL technical-table value for all three properties, and record each property's relation to the SDS separately. No property has an unresolved applicability or reliability issue that justifies keeping the selection pending. The KV40 disagreement stays an open, unresolved conflict.

## The distinction applied

1. **Selection.** Rule 1 selects the applicable technical-source value. It may stay pending only for a specific unresolved identity, applicability, edition or reliability problem.
2. **Disagreement with the SDS.** It is recorded and assessed on its own (alternate entry, conflict entry, comparison row). It is not a veto on the selection, and selecting the technical value does not say the SDS is wrong.

## The two sources

| | Technical source | SDS |
|---|---|---|
| Document | S-OIL "Lube Base Oil" web page, table "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8" | DL2-14611.pdf, "Base Oil aramcoULTRA 8 (250 Neutral)", p.2 |
| Issuer | S-OIL (manufacturer) | S-OIL |
| Edition date | **Unknown: the page prints no publication or revision date.** It was captured on 2026-06-10 (Internet Archive) and retrieved on 2026-10-30 (live); the two saved copies print identical tables. A capture or retrieval date shows only that the page existed then; it does not establish when it was published or revised | Rev. 0, revision date 2018-09-07 |
| Value kind | Typical (table title) | A range; the SDS does not say whether it is a specification or a typical range |
| Copy | Two saved copies in `reconciliation/audit_evidence/`, hashes verified | In the source archive |

## Property by property

| | KV40 | KV100 | Flash point |
|---|---|---|---|
| Technical value as printed | "Kinematic Viscosity @ 40℃, cSt \| D445 \| 41.10" | "Kinematic Viscosity @ 100℃, cSt \| D445 \| 7.1" | "Flash Point,COC ,℃ \| D92 \| 250" |
| SDS value as printed (selected now) | "42.0 - 55.0 cSt @ 40℃ (ASTM D 445)" | "7.0 - 7.5 cSt @ 100℃ (ASTM D 445)" | "240 ~ 260℃ (ASTM D 92)" |
| Unit | cSt on both sides | cSt on both sides | °C on both sides |
| Condition | 40 °C on both sides | 100 °C on both sides | none required |
| Test method | ASTM D445 on both sides | ASTM D445 on both sides | ASTM D92 on both sides. The page also prints "COC"; the SDS prints only the method number (the inventory already reads D92 as COC) |
| Value kinds | typical point vs range of unstated kind | typical point vs range of unstated kind | typical point vs range of unstated kind |
| How the pair is compared | Under our current comparison policy a point is checked against a range (inside or outside) and is not differenced. A distance from the range limit could be calculated (41.10 is 0.90 cSt below 42.0); the policy does not use it, and no threshold applies | Same policy: checked, not differenced | Same policy: checked, not differenced |
| Logical relation | **Incompatible:** 41.10 is below the lower limit 42.0 | Compatible: 7.1 is inside 7.0–7.5. This is not evidence of agreement | Compatible: 250 is inside 240–260. This is not evidence of agreement |
| Other evidence | None in the archive for this record | Aramco 2024 catalog p.25, aramcoULTRA slate, grade 8: "7.0 - 7.5" (ASTM D-445), a specification range equal to the SDS range | Aramco 2024 catalog p.25: "≥ 240" (COC, ASTM D-92) |
| **Selection recommended** | **S-OIL typical 41.10 cSt** | **S-OIL typical 7.1 cSt** | **S-OIL typical 250 °C (COC)** |
| SDS value | Kept as an alternate entry, with its page and revision date | Kept as an alternate entry | Kept as an alternate entry |
| Disagreement record | The existing 2026-10 audit conflict (41.1 vs 42.0–55.0) stays, **unresolved**. Its note should say the technical value is now selected and that this does not resolve it | No conflict. A bound-check comparison row: "logically compatible, not agreement" | No conflict. A bound-check comparison row, same wording |

## Why selection should not stay pending

Each possible reason was checked against the evidence:

| Possible reason | Finding |
|---|---|
| Exact product identity | The column is headed "aramcoULTRA 8", the record's own name. The page does not print "250 Neutral", but no other aramcoULTRA 8 grade exists on the page or in the catalog. Not an open issue. |
| Merge question ID-01 | Separate. It concerns whether this record and Ultra-S 8 are one product. It does not restrict a table that names aramcoULTRA 8, and it stays open. |
| Authority and authenticity | Manufacturer page; two saved copies with verified hashes agree. |
| Edition | The edition date of the page is unknown. Whether it is newer or older than the 2018 SDS cannot be established from the capture dates. This does not block the selection: Rule 1 prefers the technical source over the SDS by document class, not by date, and there is no second technical edition for this grade, so the "undated disagreeing editions" rule (technical vs technical) does not apply. The unknown date is kept as a caveat in each selected value. |
| Units, conditions, methods | Identical on both sides for all three properties (table above). Nothing required is missing from the technical value. |
| Consistency with current practice | Five values of this record (VI, density, CCS, pour point, Noack) are already selected from the same table. Keeping KV40, KV100 and flash point on the SDS mixes two sources for one grade without a stated reason. |
| The KV40 disagreement itself | Real and unexplained, but a disagreement alone is not a selection veto. It stays recorded as an unresolved conflict. |

No remaining item is a specific unresolved applicability or reliability issue. The weakest point is the unknown edition date of the page: you could require a dated technical document before selecting, which would keep all three pending and would, for consistency, also put the five already-selected values in question.

## What stays uncertain after selection

- **KV40.** Why the table typical lies below the 2018 SDS range is unknown, and so is which of the two documents is newer. Possible explanations (a changed product, a loosely drafted SDS range, a different site) are not supported by any document and are not assumed. Only the supplier can settle it.
- **KV100 and flash point.** "Inside the SDS range" shows only logical compatibility. The SDS range's kind is not stated, so no agreement is claimed.
- **Thresholds.** None applies: under the current comparison policy, point-vs-range pairs are bound checks.

## Implemented on 2026-11-11

- **Confirmation.** `tools/data_policy/verify_soil_table.py` read the three cells in both saved copies (hashes equal to the evidence manifest): table caption "Typical Properties of aramcoULTRA Base Oil", column "aramcoULTRA 8", the row labels and ASTM cells quoted above.
- **Selections** (declared in `source_selection.py`): KV40 41.10 cSt at 40 °C, D445; KV100 7.1 cSt at 100 °C, D445; flash point 250 °C, COC, D92. Each value is typical, cites the page URL with `revision_date` null, and names both saved copies with their SHA-256 and the unknown edition date.
- **SDS values.** The three SDS ranges are alternate entries with their page and revision date.
- **KV40 disagreement.** The existing 2026-10 audit conflict is kept, unresolved, with a dated note. It was not duplicated, and the v5 audit was not edited.
- **Pending.** The three fields are no longer pending.
- **Eligibility (calculated).** S_OIL_ARAMCO_ULTRA_8 is now Tier 1 complete and formulation-eligible, with an open-conflict warning on KV40: 11 of 181 base oils (10 before). Interface columns and requirements version are unchanged; one row and the data fingerprint changed.
- **Comparison inventory.** The three pairs are rows of the TDS–SDS inventory since the extension of 2026-11-11 (`evidence_review.md` §11): KV40 outside the SDS range (retained for review), KV100 and flash point numerically inside the range (logically compatible, no agreement claimed).

## Corrections made to this recommendation (2026-11-11)

1. An earlier version said the captures showed the page "was current in 2026, later than the 2018 SDS". A capture or retrieval date does not establish a publication or revision date. The edition date is unknown.
2. An earlier version cited an indicative viscosity-index calculation that used constants from memory. It is removed and is not selection evidence.
3. An earlier version said a point-vs-range difference was "not computable". The accurate statement is that our current comparison policy checks a point against a range and does not difference them.
