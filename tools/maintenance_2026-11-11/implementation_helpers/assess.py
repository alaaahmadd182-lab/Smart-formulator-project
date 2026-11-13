import json
R = 'C:\\Users\\windo\\sf-wsA\\'

# ---------------------------------------------------------------- decisions JSON
p = R + 'tools\\data_policy\\external_review_decisions.json'
d = json.load(open(p, encoding='utf-8'))
d['description'] = (
    "Reviewed outcome for every value selected from an external (URL) source and for every pending field whose open question is an "
    "external technical source (review of 2026-11-11). One entry per product x property. 'expect' pins the record as reviewed; "
    "external_review.py stops if the record has changed. Outcomes: confirmed = the value was re-read as printed on a copy that was "
    "obtained; inconclusive_source_unavailable = no copy of the source could be obtained, so the value was not re-read. External "
    "evidence is admissible (the templates define source.file as an archive file or a URL in source_registry.json); there is no "
    "blanket rule for or against it. Each source is assessed separately on authority, authenticity and provenance (per evidence "
    "item) and each case on exact product identity and applicability (per case). 'confirmed' states only that the value is printed "
    "as recorded: it is not an approval to select the source, and a distributor-issued document is never treated as "
    "manufacturer-issued. Nothing in this file changes product data.")
EV = {
    'aramco_prima230_sheet': ('manufacturer_issued', 'registry_hash_match',
                              'Saudi Aramco download URL in source_registry.json; stored copy with SHA-256; undated sheet (PDF created 2019-02-03, 2021-12 document set)'),
    'luberef_prima230_sds': ('manufacturer_issued', 'registry_hash_match',
                             'Luberef document storage URL in source_registry.json; stored copy with SHA-256; SDS revision 2.0, issue date 12/08/2020'),
    'mogo_flyer_2025': ('distributor_issued', 'registry_hash_match',
                        'Ergon/MOGO URL in source_registry.json (issuer: distributor, not Bapco); SHA-256 recorded, copy not stored (15 MB); PDF created 2025-08-18'),
    'aramco_catalog_2024': ('manufacturer_issued', 'registry_hash_match',
                            'Saudi Aramco URL in source_registry.json; SHA-256 recorded, copy not stored; PDF created 2024-12-10'),
    'richful_feed_109': ('manufacturer_issued', 'live_feed_unhashed_in_registry',
                         "Richful's own product data feed behind the registered product page; stored copy of the 2026-11-11 response with SHA-256; no edition or revision date; corroborated by the archived TDS"),
    'richful_feed_130': ('manufacturer_issued', 'live_feed_unhashed_in_registry',
                         "Richful's own product data feed behind the registered product page; stored copy of the 2026-11-11 response with SHA-256; no edition or revision date; corroborated by the archived TDS"),
    'soil_page_wayback': ('manufacturer_issued', 'saved_copy_hash_verified',
                          'S-OIL page, Internet Archive capture 2026-06-10 saved in reconciliation/audit_evidence (manifest SHA-256); the page is undated'),
    'soil_page_live': ('manufacturer_issued', 'saved_copy_hash_verified',
                       'S-OIL page, live copy of 2026-10-30 saved in reconciliation/audit_evidence (manifest SHA-256); the page is undated'),
    'afton_12204l_pds': ('manufacturer_issued', 'not_obtained',
                         'Internet Archive snapshot URL and SHA-256 in source_registry.json (checked 2026-10-23); no copy obtained in this review'),
    'afton_8788b_pds': ('manufacturer_issued', 'not_obtained',
                        'Internet Archive snapshot URL and SHA-256 in source_registry.json (checked 2026-10-22, base-oil statement only); no copy obtained in this review'),
}
assert set(EV) == set(d['evidence'])
for k, (au, ac, pr) in EV.items():
    d['evidence'][k].update(authority=au, authenticity=ac, provenance=pr)

NA = ('not_assessed_source_not_obtained', 'not assessed: the source could not be read')
for c in d['cases']:
    pid, prop = c['product'], c['property']
    if pid.startswith('AFTON_'):
        c['identity_status'], c['applicability'] = NA
    elif pid == 'ARAMCO_LUBEREF_PRIMA_230':
        c['identity_status'] = 'exact_grade_named'
        c['applicability'] = ("typical value on a single-grade sheet headed 'Yanbu' (plant-specific); the record does not name a plant; "
                              "the sheet is undated")
    elif pid == 'BAPCO_BAPBASE_4':
        c['identity_status'] = 'exact_grade_named'
        c['applicability'] = ("distributor-issued typical value in a column 'BAPbase 4'; the Bapco specification in the archive "
                              "(2017-08-17) prints no KV40; not a manufacturer statement")
    elif pid.startswith('RICHFUL_'):
        c['identity_status'] = 'exact_grade_named'
        c['applicability'] = 'specification range and typical value; the same row is printed by the archived TDS of the product'
    elif pid == 'S_OIL_ARAMCO_ULTRA_8':
        c['identity_status'] = 'grade_named_identity_question_open'
        c['applicability'] = ("typical value on an undated manufacturer page, column 'aramcoULTRA 8'; identity question ID-01 "
                              "(aramcoULTRA 8 vs Ultra-S 8; the page prints identical tables for both) is open and is not resolved here")
        if prop == 'kv40':
            c['applicability'] += '; the typical 41.10 lies outside the archived SDS range 42.0-55.0 (unresolved conflict, 2026-10 audit)'
    else:
        assert pid.startswith('S_OIL_ULTRA_S_'), pid
        c['identity_status'] = 'exact_grade_named'
        c['applicability'] = "typical value on an undated manufacturer page, column of this grade; the archived S-OIL sheet is from 2009"
    c['reason'] = (c['reason']
                   .replace("Selecting it over the archived SDS is a policy decision (external technical page vs archived SDS); the field stays pending.",
                            "The field stays pending on the source-specific assessment: identity question ID-01 is open and the value conflicts with the archived SDS range.")
                   .replace("Selection stays pending (policy decision on external technical sources).",
                            "The field stays pending on the source-specific assessment: identity question ID-01 is open."))
    assert 'policy decision' not in c['reason'], c['reason']
for o in d['observations']:
    o['text'] = o['text'].replace(
        "Not filled: outside the reviewed value set, and whether distributor-issued external documents may fill Missing fields is a policy decision.",
        "Not filled: the flyer is distributor-issued (Ergon/MOGO), not a Bapco document, and a distributor description is not accepted "
        "automatically; its authority for this grade has not been assessed further.")
    assert 'policy decision' not in o['text']
open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')


def edit(rel, reps):
    q = R + rel
    s = open(q, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:70])
        s = s.replace(a, b)
    open(q, 'w', encoding='utf-8', newline='\n').write(s)


# ---------------------------------------------------------------- external_review.py
edit('tools\\data_policy\\external_review.py', [
    ("""  confirmed                         re-read on a copy whose identity is established (registry SHA-256 match, saved
                                    evidence with a verified hash, or a live supplier data feed corroborated by the
                                    archived TDS); product, property, unit, qualifier, conditions and page agree
  inconclusive_source_unavailable   no copy could be obtained in the review: the value was not re-read
""",
     """  confirmed                         the value was re-read as printed on a copy that was obtained; property, unit,
                                    qualifier, conditions and page agree with the record
  inconclusive_source_unavailable   no copy could be obtained in the review: the value was not re-read

External evidence is admissible; there is no blanket rule for or against it. Each source is assessed separately:
  per evidence item   authority (who issued it), authenticity (how the copy is tied to the source), provenance
  per case            identity_status (exact product identity) and applicability
'confirmed' is not an approval to select a source: a distributor-issued document is never treated as
manufacturer-issued, and an open identity question stays open.
"""),
    ("""KINDS = ('external_selected', 'pending_external_alternative')
""",
     """KINDS = ('external_selected', 'pending_external_alternative')
AUTHORITY = ('manufacturer_issued', 'distributor_issued', 'third_party')
AUTHENTICITY = ('registry_hash_match', 'saved_copy_hash_verified', 'live_feed_unhashed_in_registry', 'not_obtained')
IDENTITY = ('exact_grade_named', 'grade_named_identity_question_open', 'not_assessed_source_not_obtained')
"""),
    ("""    cases = {(c['product'], c['property']): c for c in dec['cases']}
""",
     """    for key, e in dec['evidence'].items():
        if e.get('authority') not in AUTHORITY or e.get('authenticity') not in AUTHENTICITY or not e.get('provenance'):
            errors.append(f'evidence {key}: authority, authenticity and provenance must be assessed')
        if (e.get('authenticity') == 'not_obtained') != (ev_check[key] == 'no copy obtained'):
            errors.append(f'evidence {key}: authenticity {e.get("authenticity")!r} contradicts the copy state')
    cases = {(c['product'], c['property']): c for c in dec['cases']}
"""),
    ("""        if not matches(field(prods, pid, prop), c['expect']):
""",
     """        unread = all(dec['evidence'][e]['authenticity'] == 'not_obtained' for e in c['evidence'])
        if c.get('identity_status') not in IDENTITY or not c.get('applicability'):
            errors.append(f'{pid} {prop}: identity_status and applicability must be assessed')
        elif unread != (c['identity_status'] == 'not_assessed_source_not_obtained'):
            errors.append(f'{pid} {prop}: identity_status {c["identity_status"]!r} contradicts whether the source was read')
        if unread != (c['outcome'] == 'inconclusive_source_unavailable'):
            errors.append(f'{pid} {prop}: outcome {c["outcome"]!r} contradicts whether the source was read')
        if not matches(field(prods, pid, prop), c['expect']):
"""),
    ("""                         identity=c['identity'], printed=c['printed'], sds_comparison=c['sds'], change=c['change'], reason=c['reason']))""",
     """                         authority='; '.join(dict.fromkeys(dec['evidence'][e]['authority'] for e in c['evidence'])),
                         authenticity='; '.join(dict.fromkeys(dec['evidence'][e]['authenticity'] for e in c['evidence'])),
                         identity_status=c.get('identity_status', ''), identity=c['identity'], applicability=c.get('applicability', ''),
                         provenance=' | '.join(dec['evidence'][e]['provenance'] for e in c['evidence']),
                         printed=c['printed'], sds_comparison=c['sds'], change=c['change'], reason=c['reason']))"""),
    ("""    print('evidence: ' +""",
     """    for col in ('authority', 'authenticity', 'identity_status'):
        print(f'  {col}: ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(r[col] for r in rows).items())))
    print('evidence: ' +"""),
])

# ---------------------------------------------------------------- source_selection.py pending reason
edit('tools\\data_policy\\source_selection.py', [
    ("Whether an external technical page may be selected over the archived SDS is a policy decision; the KV40 typical 41.10 lies below the SDS range 42.0-55.0 (already recorded as an unresolved conflict by the 2026-10 audit).'",
     "External evidence is admissible, so this is not a question of permission; the selection stays pending on the source-specific assessment: identity question ID-01 (aramcoULTRA 8 vs Ultra-S 8) is open, the page is undated, and the KV40 typical 41.10 lies below the SDS range 42.0-55.0 (already recorded as an unresolved conflict by the 2026-10 audit).'"),
])

# ---------------------------------------------------------------- test
edit('tools\\data_policy\\tests\\test_data_policy.py', [
    ("""    def test_stale_decision_is_an_error(self):""",
     """    def test_each_source_assessed_separately(self):
        ER = self.ER
        for k, e in self.dec['evidence'].items():
            self.assertIn(e['authority'], ER.AUTHORITY, k)
            self.assertIn(e['authenticity'], ER.AUTHENTICITY, k)
            self.assertTrue(e['provenance'], k)
        for r in self.rows:
            self.assertIn(r['identity_status'], ER.IDENTITY)
            self.assertTrue(r['applicability'])
            if r['authenticity'] == 'not_obtained':
                self.assertEqual((r['identity_status'], r['outcome']), ('not_assessed_source_not_obtained', 'inconclusive_source_unavailable'))
        # a distributor-issued document is labelled as such, and the open aramcoULTRA 8 identity question is not closed
        self.assertEqual(self.dec['evidence']['mogo_flyer_2025']['authority'], 'distributor_issued')
        self.assertEqual({r['identity_status'] for r in self.rows if r['product'] == 'S_OIL_ARAMCO_ULTRA_8'}, {'grade_named_identity_question_open'})
        self.assertNotIn('policy decision', json.dumps(self.dec))

    def test_stale_decision_is_an_error(self):"""),
])
print('ok')
