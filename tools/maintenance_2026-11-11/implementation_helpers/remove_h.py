R = 'C:\\Users\\windo\\sf-wsA\\'
D = 'docs\\data_policy_mandatory_review\\'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def line(s, prefix, new):
    """Replace the single line starting with prefix (new=None deletes it)."""
    ls = s.split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    if new is None:
        del ls[hit[0]]
    else:
        ls[hit[0]] = new
    return '\n'.join(ls)


def sub(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)


# ------------------------------------------------------------------ requirements_review.md
rel = D + 'requirements_review.md'
s = load(rel)
s = sub(s, '## 4. Decisions A–E (as requested) and the related F, G, H', '## 4. Decisions A–E (as requested) and the related F, G')
a = s.index('**H. External technical sources vs archived SDSs')
b = s.index('## 5. Rules the implementation does not add')
s = s[:a] + """**External evidence is not a decision item** (corrected 2026-11-11).
- An earlier draft listed "H: may an external technical document be selected over an archived SDS?" as a decision. It is withdrawn: reliable external evidence was already authorised. The templates define `source.file` as an archive file or a URL listed in `source_registry.json`, and 22 selected values come from registered URLs.
- There is no blanket rule for or against an external source. Each one is assessed separately, and the assessments are recorded in `external_review_decisions.json` and `external_review.csv`:

  | Criterion | Question | Recorded as |
  |---|---|---|
  | Authority | Who issued the document: the manufacturer, a distributor, a third party? | `authority` (per source) |
  | Authenticity | How is the copy tied to the source: registry hash, saved copy with a verified hash, an unhashed live feed, or not obtained? | `authenticity` (per source) |
  | Exact product identity | Does the document name this exact product or grade, and is any identity question open? | `identity_status` (per case) |
  | Applicability | Does the printed value apply to this record: typical or specification, plant, edition and date, conflicts? | `applicability` (per case) |
  | Provenance | URL, retrieval, hash, edition | `provenance` (per source) |

- "Confirmed" in the external review means only that the value is printed as recorded. It is not an approval to select the source.
- A distributor-issued document is never treated as manufacturer-issued, and a distributor description is not accepted automatically. The one case is the Ergon/MOGO flyer for BAPbase 4: its specific gravity is not filled.
- **S_OIL_ARAMCO_ULTRA_8.** KV40, KV100 and flash point stay pending because of the source-specific assessment, not because of a permission question: identity question ID-01 (aramcoULTRA 8 vs Ultra-S 8) is open, the S-OIL page is undated, and its KV40 typical conflicts with the archived SDS range. ID-01 is not resolved here. This product is the only one whose sole unmet requirements are pending source selections (sensitivity row "unresolved_source_selection": 11 instead of 10).

""" + s[b:]
save(rel, s)

# ------------------------------------------------------------------ HANDOFF.md
rel = D + 'HANDOFF.md'
s = load(rel)
s = line(s, '| Rule 1 (technical first, SDS fallback; range/bound selected as printed) |',
         '| Rule 1 (technical first, SDS fallback; range/bound selected as printed) | Given by you; applied: 39 declared selections, plus list fills, qualifier fixes and conflict additions. External evidence is admissible; each external source is assessed separately on authority, authenticity, exact identity, applicability and provenance (`external_review.csv`) |')
s = line(s, '| H | External technical source vs archived SDS', None)
s = line(s, '| A | Keep "published formulation" mandatory',
         '| A | Keep "published formulation" mandatory for packages as written, or assess it separately from route-data completeness | All 78 packages fail it today; 1 of 78 has complete route data otherwise | [decision_brief_published_formulation.md](decision_brief_published_formulation.md) |')
s = sub(s, 'and their source selection is pending (decision H).', 'and their source selection is pending (identity question ID-01 open; KV40 conflicts with the S-OIL typical).')
s = sub(s, '- external technical page vs archived SDS (decision H).',
        '- aramcoULTRA 8: identity question ID-01 is open, so its external S-OIL values are not selected over the SDS ranges. Its 5 already-selected S-OIL values (VI, density, CCS, pour point, Noack) rest on the same open question and are unchanged;\n- BAPbase 4: the only KV40 comes from a distributor-issued flyer (labelled as such); the same flyer\'s specific gravity is not filled.')
s = sub(s, '   | evidence unavailable | 181 | 81 |',
        '   | evidence unavailable: read, information insufficient (173) | 173 | 81 |\n   | evidence unavailable: source could not be obtained (8) | 8 | 0 |')
s = sub(s, 'Run on 2026-11-11, before the revision-3 commit, on the final working tree.', 'Run on 2026-11-11 at revision-3 commit `43e7f8b` plus the uncommitted policy-decision changes of the same day.')
s = sub(s, "| 20 | `tools/data_policy/tests` | 0 | 45 OK |", "| 20 | `tools/data_policy/tests` | 0 | 46 OK |")
s = sub(s, '2. **External-source review** ([evidence_review.md](evidence_review.md) §8; `external_review.csv`).',
        '2. **External-source review** ([evidence_review.md](evidence_review.md) §8; `external_review.csv`). External evidence is admissible; each source is assessed separately (authority, authenticity, exact identity, applicability, provenance).')
s = sub(s, '   - **Confirmed: 21** (18 selected, 3 pending). Each was re-read on a copy whose identity is established: registry SHA-256 match, a saved evidence copy with a verified hash, or the Richful data feed agreeing with the archived TDS.',
        '   - **Confirmed as printed: 21** (18 selected, 3 pending). "Confirmed" is not an approval to select the source. Of the 21: 20 manufacturer-issued, 1 distributor-issued (BAPbase 4 KV40); 13 name the exact grade with no open identity question, 8 are aramcoULTRA 8 with ID-01 open.')
save(rel, s)

# ------------------------------------------------------------------ evidence_review.md
rel = D + 'evidence_review.md'
s = load(rel)
s = line(s, '| External technical page vs archived SDS (aramcoULTRA 8',
         '| Source-specific open points on external evidence (aramcoULTRA 8: identity question ID-01; BAPbase 4: distributor-issued flyer) | 3 pending fields + 1 unfilled field | Values confirmed as printed. External evidence is admissible, but ID-01 is not resolved, and a distributor description is not accepted automatically. |')
s = sub(s, '- 181 reviewed rows end as evidence unavailable and 7 as inconclusive (section 9);',
        '- 181 reviewed rows end as evidence unavailable (173 read but insufficient, 8 source not obtained) and 7 as inconclusive (section 9);')
s = sub(s, '- BAPbase 4 specific gravity 15/4 °C 0.834 (MOGO flyer): not filled. Whether a distributor-issued external document may fill a Missing field is a policy decision.',
        '- BAPbase 4 specific gravity 15/4 °C 0.834 (MOGO flyer): not filled. The flyer is distributor-issued, and a distributor description is not accepted automatically.')
s = sub(s, """**Method.** For each value: obtain a copy whose identity is established, then check the product (grade column), property, unit, qualifier, conditions and page against the record. Then compare with the applicable SDS.""",
        """**Admissibility.** External evidence is admissible; there is no blanket rule for or against it (an earlier "decision H" is withdrawn). Each source is assessed separately on five criteria, recorded in `external_review.csv`:

| Criterion | Result over the 29 cases |
|---|---|
| Authority | manufacturer-issued 28; distributor-issued 1 (Ergon/MOGO flyer, BAPbase 4 KV40) |
| Authenticity | registry hash match 3; saved copy with verified hash 16 (2 of them also checked against a registry-hash catalog); live Richful feed, not hashed in the registry, 2; not obtained 8 |
| Exact product identity | exact grade named, no open question 13; grade named but identity question ID-01 open 8 (all aramcoULTRA 8: 5 selected values and 3 pending fields); not assessed, source not obtained 8 |
| Applicability | recorded per case: typical or specification, plant (the PRIMA 230 sheet is headed "Yanbu"), edition and date (the S-OIL page is undated), conflicts |
| Provenance | URL, retrieval, hash and edition per source |

"Confirmed" below means only that the value is printed as recorded. It is not an approval to select the source, and ID-01 is not resolved by this review.

**Method.** For each value: obtain a copy, then check the product (grade column), property, unit, qualifier, conditions and page against the record. Then compare with the applicable SDS.""")
s = line(s, '| evidence unavailable | 181 | 81 | reviewed, and the evidence',
         '| evidence unavailable | 181 | 81 | two different situations under one label (section 10): 173 archive cases where the documents were read and do not give sufficient information, and 8 external cases where the document could not be obtained |')
s = s.rstrip('\n') + """

## 10. What "evidence unavailable" covers (181 rows)

**Counting unit.** One row is one product × property pair of the coverage ledger: one property of one product, not a document and not a value. The 181 rows cover 106 products. A document that is read for several properties or grades appears in several rows.

The label joins two situations that must not be read as one:

| Situation | Rows | Mandatory | Was a document read? | Record state |
|---|---:|---:|---|---|
| **Read, information insufficient** (lead outcome `insufficient_evidence`) | 173 | 81 | Yes: 112 on page renders, 61 from the text layer | 127 fields Missing; 42 optional specific-gravity fields not present in the record; 4 fields Reported from another page (comparison leads) |
| **Source could not be obtained** (external outcome `inconclusive_source_unavailable`) | 8 | 0 | No | all 8 Reported: 4 selected from the external source, 4 selected from the SDS and pending |

**Read, information insufficient (173).** The associated archive documents mention the property, or are image-only, and were read; they do not support a value for this product:

| Why | Rows |
|---|---:|
| No value printed for this grade or property (cell shows "Report", "-", "N/A", "To be reported", blank, or the property is not in the document) | 143 |
| Value printed without a condition the property requires (density with no reference temperature) | 20 |
| Label and unit contradict each other, or the notation is undefined | 8 |
| Supplier marks the typical value as provisional | 2 |

For these rows the review is finished: re-reading the same documents will not change the outcome. Only a different document could.

**Source could not be obtained (8).** The Afton HiTEC 12204L PDS (KV100, density, flash point, TBN) and the Afton HiTEC 8788B PDS (KV40, KV100, density, flash point). Nothing was read, so nothing is known about what they print. These rows are **unverified**, not "insufficient": obtaining the two files would allow the review.

**Not included in the 181.**
- 457 Missing rows where no associated document mentions the property were never lead cases; they are in "not individually reviewed".
- 7 rows are "evidence inconclusive" (identity).

The verification status of none of these rows has been changed; the two situations stay distinguishable through the columns `lead_outcome` and `external_outcome` of `source_review_status.csv`.
"""
save(rel, s)

# ------------------------------------------------------------------ source_review_coverage.md
rel = D + 'source_review_coverage.md'
s = load(rel)
s = sub(s, '| evidence unavailable: the archive documents do not print the value (173), or no copy of the external source could be obtained (8) | 181 | 81 |',
        '| evidence unavailable, read: the archive documents were read and do not give sufficient information | 173 | 81 |\n| evidence unavailable, not obtained: no copy of the external source could be obtained, so nothing was read | 8 | 0 |')
s = sub(s, 'vs archived SDS ranges: a policy decision on external technical sources; KV40 typical', 'vs archived SDS ranges: identity question ID-01 is open and not resolved here; KV40 typical')
s = sub(s, '- external technical pages vs archived SDSs (a policy decision).', '- source-specific open points on external evidence: identity question ID-01 (aramcoULTRA 8) and the distributor-issued flyer for BAPbase 4.')
s = sub(s, 'A recorded outcome for every one of the 363 frozen lead cases', 'The two "evidence unavailable" lines share one state in `source_review_status.csv` (181 rows) and are told apart by its `lead_outcome` and `external_outcome` columns; `evidence_review.md` section 10 explains them.\n\nA recorded outcome for every one of the 363 frozen lead cases')
save(rel, s)

# ------------------------------------------------------------------ CLAUDE.md
rel = 'CLAUDE.md'
s = load(rel)
s = sub(s, 'an external source that cannot be obtained is "inconclusive", never confirmed. Whether an external (non-archive) technical document may be selected over an archived SDS is an open decision (`requirements_review.md` H).',
        'an external source that cannot be obtained is "inconclusive", never confirmed. External evidence is admissible, with no blanket rule for or against it: assess each source separately on authority (manufacturer vs distributor), authenticity, exact product identity, applicability and provenance; never accept a distributor description automatically, and do not resolve an open identity question (e.g. ID-01, aramcoULTRA 8) as a side effect.')
save(rel, s)

# ------------------------------------------------------------------ tools/README.md
rel = 'tools\\README.md'
s = load(rel)
s = sub(s, '| Regression tests (45): Rule 1,', '| Regression tests (46): Rule 1,')
s = sub(s, 'and of pending fields with an external alternative (decisions and evidence hashes in `external_review_decisions.json`)',
        'and of pending fields with an external alternative; each source assessed separately on authority, authenticity, exact identity, applicability and provenance (decisions and evidence hashes in `external_review_decisions.json`)')
save(rel, s)

# ------------------------------------------------------------------ curated log and changelog (appended, earlier text kept)
rel = 'open_questions_and_conflicts.md'
s = load(rel).rstrip('\n') + """

### 2026-11-11 (later): correction on external evidence

- The open question above ("may an external technical document be selected over an archived SDS, or fill a Missing field?") is withdrawn. Reliable external evidence was already authorised; it is not a blanket permission question.
- Each external source is assessed separately on authority, authenticity, exact product identity, applicability and provenance (`reports/data_policy/external_review.csv`).
- S_OIL_ARAMCO_ULTRA_8: KV40, KV100 and flash point stay pending because identity question ID-01 (aramcoULTRA 8 vs Ultra-S 8) is open; it is not resolved. The 5 values already taken from the S-OIL page (VI, density, CCS, pour point, Noack) rest on the same open question and are unchanged.
- BAPCO_BAPBASE_4: the MOGO flyer is distributor-issued (Ergon/MOGO), not a Bapco document. Its specific gravity is not filled; a distributor description is not accepted automatically. The existing KV40 from the same flyer is unchanged and labelled distributor-issued in the review.
"""
save(rel, s)

rel = D + 'CHANGELOG_2026-11-10.md'
s = load(rel).rstrip('\n') + """

---

# After revision 3, 2026-11-11: policy-decision preparation (no rule, threshold or requirement changed)

Revision 3 is commit `43e7f8b`. The changes below sit on top of it.

- **"Decision H" withdrawn.** Reliable external evidence was already authorised, so it is not a blanket permission question. `external_review_decisions.json` and `external_review.csv` now record, for each source, authority, authenticity and provenance, and for each case exact product identity and applicability. `external_review.py` rejects a decision without them.
  - Result over the 29 cases: 28 manufacturer-issued and 1 distributor-issued; 13 with the exact grade named and no open question, 8 aramcoULTRA 8 cases with identity question ID-01 open, 8 not assessed (source not obtained).
  - No outcome, value or status changed. ID-01 is not resolved, and the distributor flyer's specific gravity for BAPbase 4 is not filled.
  - The pending reason of S_OIL_ARAMCO_ULTRA_8 in `source_selection.PENDING` is reworded (the ledger's `selection_reason` text changes with it).
- **New document:** [decision_brief_published_formulation.md](decision_brief_published_formulation.md). Neither option is implemented; the checker, the requirements version and the shared interface are unchanged.
- **"Evidence unavailable" (181 rows) explained** in `evidence_review.md` section 10: 173 rows where documents were read and are insufficient, and 8 rows where the source could not be obtained. No verification status changed.
- Tests: `tools/data_policy/tests` 46 (one added: each source assessed separately).
"""
save(rel, s)
print('ok')
