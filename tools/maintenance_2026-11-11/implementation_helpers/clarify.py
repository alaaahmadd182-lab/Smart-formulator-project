import json
R = 'C:\\Users\\windo\\sf-wsA\\'
D = 'docs\\data_policy_mandatory_review\\'
OLD, NEW = 'grade_named_identity_question_open', 'exact_grade_named_merge_question_separate'


def load(rel):
    return open(R + rel, encoding='utf-8').read()


def save(rel, s):
    open(R + rel, 'w', encoding='utf-8', newline='\n').write(s)


def sub(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a))
    return s.replace(a, b)


def line(s, prefix, new):
    ls = s.split('\n')
    hit = [i for i, x in enumerate(ls) if x.startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    ls[hit[0]] = new
    return '\n'.join(ls)


# ---------------------------------------------------------------- review records and tools
p = 'tools\\data_policy\\external_review_decisions.json'
d = json.loads(load(p))
for c in d['cases']:
    if c['product'] == 'S_OIL_ARAMCO_ULTRA_8':
        assert c['identity_status'] == OLD
        c['identity_status'] = NEW
        c['applicability'] = ("typical value on an undated manufacturer page, in the table 'Typical Properties of aramcoULTRA Base Oil', "
                              "column 'aramcoULTRA 8': the page names this record's grade explicitly (it does not print '250 Neutral'). "
                              "Identity question ID-01 is a different matter: it asks whether the two records S_OIL_ARAMCO_ULTRA_8 and "
                              "S_OIL_ULTRA_S_8 should be merged; it is open, is not resolved here, and does not concern this source-to-record link")
        if c['property'] == 'kv40':
            c['applicability'] += '. The typical 41.10 lies outside the archived SDS range 42.0-55.0 (unresolved conflict, 2026-10 audit)'
        c['reason'] = (c['reason']
                       .replace("The field stays pending on the source-specific assessment: identity question ID-01 is open and the value conflicts with the archived SDS range.",
                                "The field stays pending because the undated page's typical conflicts with the dated SDS range (unresolved conflict); ID-01 is not the reason.")
                       .replace("The field stays pending on the source-specific assessment: identity question ID-01 is open.",
                                "No conflict with the SDS range was found for this property, and ID-01 is not a restriction on this source. The selected SDS value is left unchanged for the user's review; the page is undated."))
        assert 'ID-01 is open' not in c['reason'], c['reason']
d['description'] = sub(d['description'], "a distributor-issued document is never treated as manufacturer-issued.",
                       "a distributor-issued document is never treated as manufacturer-issued. identity_status concerns only the link "
                       "between this source and this record; a question about merging two records (ID-01) is recorded apart from it.")
save(p, json.dumps(d, ensure_ascii=False, indent=1) + '\n')

p = 'tools\\data_policy\\external_review.py'
s = load(p)
s = sub(s, f"'{OLD}'", f"'{NEW}'")
s = sub(s, "manufacturer-issued, and an open identity question stays open.",
        "manufacturer-issued. identity_status concerns only the link between the source and the record: a source that names\n"
        "the record's exact grade is 'exact_grade_named_merge_question_separate' when a separate question about merging two\n"
        "records (ID-01) is open; that question is not resolved here and does not restrict the use of the source.")
save(p, s)

p = 'tools\\data_policy\\tests\\test_data_policy.py'
s = load(p)
s = sub(s, "        # a distributor-issued document is labelled as such, and the open aramcoULTRA 8 identity question is not closed",
        "        # a distributor-issued document is labelled as such; the aramcoULTRA 8 page names the exact grade, and the\n"
        "        # separate merge question ID-01 is neither resolved nor used as a restriction on that source")
s = sub(s, f"{{'{OLD}'}}", f"{{'{NEW}'}}")
save(p, s)

p = 'tools\\data_policy\\source_selection.py'
s = load(p)
s = sub(s, "the selection stays pending on the source-specific assessment: identity question ID-01 (aramcoULTRA 8 vs Ultra-S 8) is open, the page is undated, and the KV40 typical 41.10 lies below the SDS range 42.0-55.0 (already recorded as an unresolved conflict by the 2026-10 audit).'",
        "the page names aramcoULTRA 8 explicitly, so the merge question ID-01 (aramcoULTRA 8 vs Ultra-S 8 records) is not the restriction. The restriction with evidence is on KV40: the undated page's typical 41.10 lies below the dated SDS range 42.0-55.0 (unresolved conflict, 2026-10 audit). For KV100 and flash point the typicals lie inside the SDS ranges; the SDS values are kept selected, unchanged, for review.'")
save(p, s)

# ---------------------------------------------------------------- the brief (points 1 and 2)
p = D + 'decision_brief_published_formulation.md'
s = load(p)
s = sub(s, "- at least one measured result that passes the ordinary value checks.\n",
        "- at least one measured result that passes the ordinary value checks.\n\n"
        "**What one measured result does not establish.** The checker asks for one valid result only so that a recipe is not recorded "
        "without any measurement. Passing it does **not** show that the recipe meets the finished-oil requirements of slide 5 "
        "(viscometrics, low-temperature, chemistry and volatility), and it does **not** establish any performance claim or approval. "
        "Approvals belong to the tested composition and to the claim records (\"A measured result belongs to its tested composition only\"). "
        "The checker does not check which properties are reported, or whether they pass any limit.\n")
s = sub(s, "**Current data.** All 78 packages have the requirement in category `absent`; no record holds a formulation entry. No cited package document's text layer contains a complete recipe. The Afton dosage tables give package and booster doses for a grade and a base-oil group, which is not a complete recipe. Image-only package documents were not searched for recipes.",
        "**Current data.** No qualifying complete recipe is currently recorded: all 78 packages have the requirement in category `absent`, and no record holds a formulation entry.\n\n"
        "**Limits of the search behind that statement.** It is a statement about the records and about a limited search, not proof that no supplier recipe exists:\n"
        "- The search was a keyword search of the text layers of the archive documents the package records cite (recipe markers such as a \"balance\" base oil or base-oil percentages). It was not a page-by-page reading for recipes.\n"
        "- Of the 87 archive files cited by package values, 5 have no text layer (5 packages). They were read on renders for property values, but were not checked for recipes.\n"
        "- Archive documents that no package record cites, and documents outside the archive (supplier bulletins, approval lists, external sources), were not searched for recipes.\n"
        "- What was found: dosage tables, for example Afton's package and booster doses for a grade and a base-oil group. These are not complete recipes, and nothing was built from them.")
s = sub(s, "| Can better extraction change the result? | No. Only a supplier publishing a recipe can | Yes, for the route items |",
        "| What can change the result? | Only a qualifying recipe being found and recorded. None is recorded now; the search had the limits in section 2, so a targeted search of the image-only and uncited documents could still find one | Recording missing route items, and for the separate assessment, a recipe being found |")
s = sub(s, "| Risk | The gate measures supplier publishing practice rather than data quality; package eligibility stays at zero indefinitely |",
        "| Risk | The gate depends on whether a recipe is published and found, not on the quality of the route data; package eligibility stays at zero until a qualifying recipe is recorded |")
save(p, s)

# ---------------------------------------------------------------- docs (point 3)
U8 = """- **S_OIL_ARAMCO_ULTRA_8: two separate uncertainties.**

  | | Merging two product identities (ID-01) | Using the S-OIL table that names aramcoULTRA 8 |
  |---|---|---|
  | Question | Are the records `S_OIL_ARAMCO_ULTRA_8` and `S_OIL_ULTRA_S_8` one product (a rebrand), to be kept as one folder with an alias? | May the S-OIL page's "aramcoULTRA 8" column be used for the record named aramcoULTRA 8? |
  | Evidence | The inventory treats both SDSs as one material ("rebrand"). Both SDSs print "(250 Neutral)", the same KV ranges and relative density 0.847. The S-OIL page prints identical tables for Ultra-S and aramcoULTRA grades. No document states that the two names designate one product (audit CF-177: suggestive only, needs the supplier). | The page is manufacturer-issued (S-OIL), and two saved copies with verified hashes agree. Its table "Typical Properties of aramcoULTRA Base Oil" has a column headed "aramcoULTRA 8", the record's own name. The page does not print "250 Neutral", and it is undated. |
  | Status | Open. Not resolved here. | The source-to-record link is by exact grade name. ID-01 does not restrict it. |
  | What it restricts | Using Ultra-S 8 documents (the 2009 brochure, the 2015 SDS) for the aramcoULTRA 8 record, or the reverse; merging the folders. | Per value, by the evidence: see below. |

  Restrictions on the aramcoULTRA 8 table values, each with its evidence:
  - **KV40:** the page's typical 41.10 cSt lies below the SDS range 42.0–55.0 cSt (SDS DL2-14611.pdf, dated 2018-09-07; the page is undated). This is an unresolved conflict (2026-10 audit), so the selection stays pending.
  - **KV100 and flash point:** the typicals 7.1 cSt and 250 °C lie inside the SDS ranges, and the Aramco 2024 catalog prints the same KV100 range. No conflict was found. Under Rule 1 the manufacturer table would be the technical source; the only reservation is that the page is undated. The SDS ranges are kept selected, unchanged, for your review.
  - **VI, density, CCS, pour point, Noack (already selected from this page):** no SDS value exists for the same property, so nothing contradicts them. They are unchanged.
  - No selected value was changed. This product is the only one whose sole unmet requirements are pending source selections (KV40, KV100)."""

p = D + 'requirements_review.md'
s = load(p)
a = s.index('- **S_OIL_ARAMCO_ULTRA_8.** KV40, KV100 and flash point stay pending')
b = s.index('## 5. Rules the implementation does not add')
s = s[:a] + U8 + '\n\n' + s[b:]
s = sub(s, "| Exact product identity | Does the document name this exact product or grade, and is any identity question open? |",
        "| Exact product identity | Does the document name this record's exact product or grade? (A question about merging two records is kept apart.) |")
save(p, s)

p = D + 'HANDOFF.md'
s = load(p)
s = sub(s, '13 name the exact grade with no open identity question, 8 are aramcoULTRA 8 with ID-01 open.',
        '21 name the record\'s exact grade; for the 8 aramcoULTRA 8 cases among them, the separate merge question ID-01 is open but does not restrict the use of the table (`requirements_review.md` §4).')
s = sub(s, 'and their source selection is pending (identity question ID-01 open; KV40 conflicts with the S-OIL typical).',
        'and their source selection is pending (KV40: the S-OIL typical conflicts with the SDS range; KV100: no conflict, kept unchanged for review).')
s = sub(s, "- aramcoULTRA 8: identity question ID-01 is open, so its external S-OIL values are not selected over the SDS ranges. Its 5 already-selected S-OIL values (VI, density, CCS, pour point, Noack) rest on the same open question and are unchanged;",
        "- aramcoULTRA 8, two separate points: (1) the merge question ID-01 (one product with Ultra-S 8?) is open and unresolved; (2) the S-OIL table names aramcoULTRA 8 explicitly, so ID-01 does not restrict it. Its KV40 typical conflicts with the SDS range (pending); KV100 and flash point show no conflict and are kept unchanged for review;")
s = line(s, '- **Identity not established:**', '- **Identity not established:** FORMOSA SDSs, ID-15. **Merge question open:** ID-01 (aramcoULTRA 8 and Ultra-S 8 records).')
save(p, s)

p = D + 'evidence_review.md'
s = load(p)
s = line(s, '| Exact product identity | exact grade named, no open question 13;',
         '| Exact product identity | the record\'s exact grade is named 21 (for the 8 aramcoULTRA 8 cases the separate merge question ID-01 is open; it does not concern the source-to-record link); not assessed, source not obtained 8 |')
s = sub(s, 'It is not an approval to select the source, and ID-01 is not resolved by this review.',
        'It is not an approval to select the source, and the merge question ID-01 is not resolved by this review. The two aramcoULTRA 8 uncertainties (merging two records vs using the table that names aramcoULTRA 8) are set out in `requirements_review.md` §4.')
s = line(s, '| Source-specific open points on external evidence',
         '| Source-specific open points on external evidence (aramcoULTRA 8 KV40: conflict with the SDS range; BAPbase 4: distributor-issued flyer) | 3 pending fields + 1 unfilled field | Values confirmed as printed. External evidence is admissible. The aramcoULTRA 8 table names the grade explicitly; its KV40 conflicts with the SDS range, KV100 and flash point do not. A distributor description is not accepted automatically. |')
save(p, s)

p = D + 'source_review_coverage.md'
s = load(p)
s = sub(s, 'vs archived SDS ranges: identity question ID-01 is open and not resolved here; KV40 typical',
        'vs archived SDS ranges. The table names aramcoULTRA 8 explicitly (the merge question ID-01 is separate and not the restriction); KV100 and flash point show no conflict and are kept unchanged for review; KV40 typical')
s = sub(s, '- source-specific open points on external evidence: identity question ID-01 (aramcoULTRA 8) and the distributor-issued flyer for BAPbase 4.',
        '- source-specific open points on external evidence: the aramcoULTRA 8 KV40 conflict and the distributor-issued flyer for BAPbase 4; separately, the merge question ID-01.')
save(p, s)

p = 'CLAUDE.md'
s = load(p)
s = sub(s, 'and do not resolve an open identity question (e.g. ID-01, aramcoULTRA 8) as a side effect.',
        'and keep two questions apart: whether a source names the record\'s exact grade, and whether two records should be merged (ID-01, aramcoULTRA 8 vs Ultra-S 8: open, never resolved as a side effect, and not a restriction on a source that names the grade).')
save(p, s)

p = 'open_questions_and_conflicts.md'
s = load(p)
s = line(s, '- S_OIL_ARAMCO_ULTRA_8: KV40, KV100 and flash point stay pending because identity question ID-01',
         '- S_OIL_ARAMCO_ULTRA_8: two separate points. (1) ID-01 asks whether the aramcoULTRA 8 and Ultra-S 8 records are one product; it is open and not resolved. (2) The S-OIL table names aramcoULTRA 8 explicitly, so ID-01 does not restrict its use. KV40 stays pending because the undated page\'s typical 41.10 conflicts with the dated SDS range 42.0–55.0; KV100 and flash point show no conflict, and the SDS ranges are kept selected, unchanged, for review. The 5 values already taken from the page (VI, density, CCS, pour point, Noack) are unchanged.')
save(p, s)

p = D + 'CHANGELOG_2026-11-10.md'
s = load(p)
s = sub(s, '  - Result over the 29 cases: 28 manufacturer-issued and 1 distributor-issued; 13 with the exact grade named and no open question, 8 aramcoULTRA 8 cases with identity question ID-01 open, 8 not assessed (source not obtained).',
        '  - Result over the 29 cases: 28 manufacturer-issued and 1 distributor-issued; 21 name the record\'s exact grade, 8 not assessed (source not obtained).\n'
        '  - aramcoULTRA 8: the merge question ID-01 (one product with Ultra-S 8?) is kept apart from the use of the S-OIL table that names aramcoULTRA 8. ID-01 stays open and does not restrict that table; the evidence-based restriction is the KV40 conflict with the SDS range.')
s = sub(s, 'Neither option is implemented; the checker, the requirements version and the shared interface are unchanged.',
        'Neither option is implemented; the checker, the requirements version and the shared interface are unchanged. It states that no qualifying complete recipe is currently recorded, with the limits of the search, and that one accepted measured result establishes neither the finished-oil requirements nor any approval.')
save(p, s)
print('ok')
