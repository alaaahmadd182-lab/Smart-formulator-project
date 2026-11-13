"""One-off helper (2026-11-12, route review): rewrites the co-component tests in test_policies.py. Already applied."""
R = 'C:\\Users\\windo\\sf-wsA\\'


def edit(rel, reps):
    p = R + rel
    s = open(p, encoding='utf-8').read()
    for a, b in reps:
        assert s.count(a) == 1, (rel, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


for rel, old in (('tools\\mandatory_properties\\tests\\test_requirements.py', "self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.5')"),
                 ('tools\\data_policy\\tests\\test_data_policy.py', "self.assertEqual(REQ.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.5')"),
                 ('tools\\mandatory_properties\\tests\\test_policies.py', "self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.5')")):
    edit(rel, [(old, old.replace('.5', '.6'))])

p = R + 'tools\\mandatory_properties\\tests\\test_policies.py'
s = open(p, encoding='utf-8').read()
a, b = s.index('def member(i, e):'), s.index('class Policy1RangesAndBounds')
s = s[:a] + '''def fields_of(*entries):
    return dict(required_co_components=[copy.deepcopy(e) for e in entries])


def alt(f, i):
    return dict(path=f'required_co_components[{i}]', sha256=R.record_fingerprint(f['required_co_components'][i]))


def group(f, name, combination, *idx):
    return dict(group=name, combination=combination, alternatives=[alt(f, i) for i in idx], evidence='as printed')


def route(rid, required, confirmed=True, **kw):
    return dict(dict(product='P', route_id=rid, label=rid, conditions='as printed', source_file='DL2-1.pdf', page=1,
                     quote='Package at 10 wt.% + booster X at 2.0 wt.% + VM V at 8.0 wt.%', reviewed_on='2026-11-12',
                     association_basis='table row', required=required, bound_records=[], unrecorded_requirements=[],
                     requirement_list_confirmed=confirmed, list_assessment='the row lists every component', limitations=[]), **kw)


def states(f, routes):
    return {x['route']['route_id']: x['state'] for x in R.co_component_routes(f, cx(routes=routes))[0]}


REVIEW = dict(reviewed_on='2026-11-12', meaning='no_co_component_required', unconditional=True, qualification_verbatim='',
              scope=dict(component_types='all', routes='all'), conditions_verbatim='')
FULL = dict(product='P', kind='none_required', scope='all co-components', source_file='DL2-1.pdf', page=2,
            quote='No additional additive is required.', review=REVIEW)


''' + s[b:]
a, b = s.index('class Policy2CoComponentRoutes'), s.index('class Policy3PercentageBasis')
s = s[:a] + '''class Policy2CoComponentRoutes(unittest.TestCase):
    def test_one_usable_component_does_not_complete_a_route_that_needs_another(self):
        f = fields_of(BOOSTER, VM_NO_DOSE)
        r = [route('FA-4', [group(f, 'booster', 'all', 0), group(f, 'vm', 'all', 1)])]
        self.assertEqual(states(f, r), {'FA-4': 'route_incomplete'})
        o = co(f, routes=r)
        self.assertNotIn(o.category, R.SATISFIED)
        self.assertIn('informational only: 1 of 2', o.reason)
        f2 = fields_of(BOOSTER, BARE)   # the second required component has an unusable (bare %) dose
        self.assertEqual(states(f2, [route('FA-4', [group(f2, 'b', 'all', 0), group(f2, 'y', 'all', 1)])]), {'FA-4': 'route_incomplete'})

    def test_two_required_components_complete_the_route_only_if_the_list_is_confirmed(self):
        f = fields_of(BOOSTER, VM_DOSE)
        req = [group(f, 'booster', 'all', 0), group(f, 'vm', 'all', 1)]
        self.assertEqual(co(f, routes=[route('FA-4', req)]).category, R.MET)
        self.assertEqual(states(f, [route('FA-4', req, confirmed=False)]), {'FA-4': 'recorded_requirements_usable_list_not_confirmed'})
        self.assertEqual(co(f, routes=[route('FA-4', req, confirmed=False)]).category, R.ROUTE)

    def test_alternatives_and_unresolved_combinations(self):
        f = fields_of(BOOSTER, VM_NO_DOSE, BOOSTER2)
        self.assertEqual(states(f, [route('A', [group(f, 'one of', 'one_of', 0, 1)])]), {'A': 'route_complete'},
                         'supplier-stated alternatives: one usable alternative satisfies the group')
        self.assertEqual(states(f, [route('A', [group(f, 'both', 'all', 0, 1)])]), {'A': 'route_incomplete'})
        self.assertEqual(states(f, [route('A', [group(f, 'unclear', 'unresolved', 0, 2)])]),
                         {'A': 'recorded_requirements_usable_list_not_confirmed'}, 'the source does not say: never complete')

    def test_requirement_stated_by_the_source_but_not_recorded_keeps_the_route_incomplete(self):
        f = fields_of(BOOSTER)
        r = [route('A', [group(f, 'booster', 'all', 0)], unrecorded_requirements=[dict(component='viscosity modifier', quote='with VM', dose='not printed')])]
        self.assertEqual(states(f, r), {'A': 'route_incomplete'})

    def test_independent_routes_are_assessed_separately(self):
        f = fields_of(BOOSTER, BOOSTER2, VM_NO_DOSE)
        r = [route('FA-4', [group(f, 'b', 'all', 0)]), route('E4', [group(f, 'b', 'all', 1), group(f, 'vm', 'all', 2)])]
        self.assertEqual(states(f, r), {'FA-4': 'route_complete', 'E4': 'route_incomplete'})
        o = co(f, routes=r)
        self.assertEqual(o.category, R.MET)
        self.assertIn("'FA-4'", o.reason); self.assertIn('not a statement about any other route', o.reason); self.assertIn('E4: route_incomplete', o.reason)
        self.assertNotIn(co(f, routes=r[1:]).category, R.SATISFIED, 'a complete route elsewhere does not complete this one')

    def test_one_component_shared_by_two_routes_keeps_both_memberships(self):
        f = fields_of(VM_DOSE, BOOSTER, VM_NO_DOSE)
        r = [route('R1', [group(f, 'vm', 'all', 0)]), route('R2', [group(f, 'vm', 'all', 0), group(f, 'b', 'all', 1), group(f, 'vm2', 'all', 2)])]
        c = cx(routes=r)
        rts, unassigned, entries = R.co_component_routes(f, c)
        self.assertEqual({x['route']['route_id']: x['state'] for x in rts}, {'R1': 'route_complete', 'R2': 'route_incomplete'})
        self.assertEqual([e['index'] for e in unassigned], [])
        rows = BR.route_rows('P', c, rts, entries, [], 'lvl', dict.fromkeys(BR.ROUTE_COLUMNS, ''))
        shared = [(x['route_id'], x['route_state']) for x in rows if x['row_kind'] == 'recorded_requirement' and x['entry_index'] == 0]
        self.assertEqual(sorted(shared), [('R1', 'route_complete'), ('R2', 'route_incomplete')],
                         'one row per membership, each with its own route assessment; nothing overwritten or merged')

    def test_route_association_not_established_is_not_assessed(self):
        f = fields_of(BOOSTER, VM_NO_DOSE)
        o = co(f)   # no reviewed route evidence: the role text is never parsed into a route
        self.assertEqual(o.category, R.ROUTE); self.assertIn('not established', o.reason)
        self.assertEqual(co(fields_of(BOOSTER)).category, R.ROUTE, 'even a single usable requirement is not a complete route')
        part = [route('FA-4', [group(f, 'b', 'all', 0)], confirmed=False)]
        o = co(f, routes=part)
        self.assertEqual(o.category, R.ROUTE); self.assertIn('1 recorded requirement(s) have no current route association', o.reason)

    def test_route_evidence_is_bound_to_the_complete_record(self):
        base = fields_of(BOOSTER, dict(role='Booster', name='R', dose_wt_pct=vo(None, min=3.0, max=3.3, value_kind='range', unit='wt.%')))
        r = [route('A', [group(base, 'b', 'one_of', 0, 1)])]
        self.assertEqual(states(base, r), {'A': 'route_complete'})

        def changed(mut):
            f = copy.deepcopy(base); mut(f['required_co_components']); return R.co_component_routes(f, cx(routes=r))[0][0]
        for name, mut in (('range endpoint', lambda e: e[1]['dose_wt_pct'].update(max=3.5)),
                          ('unit', lambda e: e[0]['dose_wt_pct'].update(unit='%')),
                          ('source page', lambda e: e[0]['dose_wt_pct']['source'].update(page=2)),
                          ('source file', lambda e: e[0]['dose_wt_pct']['source'].update(file='DL2-9.pdf')),
                          ('qualifier', lambda e: e[0]['dose_wt_pct'].update(qualifier='maximum')),
                          ('role / condition', lambda e: e[0].update(role='Booster (another route)')),
                          ('entry removed', lambda e: e.pop(1))):
            x = changed(mut)
            self.assertEqual((x['state'], x['validity']), ('route_evidence_stale', 'stale_requires_re_review'), name)
        # a change the evidence does not rely on leaves it valid: an unrelated field, a derived key, another entry
        f = copy.deepcopy(base)
        f['treat_rate_matrix'] = [dict(claim='X', treat_rate_wt_pct=vo(9.9, unit='wt.%'))]
        f['required_co_components'][0]['dose_wt_pct']['value_final'] = 2.0
        f['required_co_components'].append(copy.deepcopy(VM_NO_DOSE))
        self.assertEqual(R.co_component_routes(f, cx(routes=r))[0][0]['validity'], 'current')
        # a bound treat-rate entry is part of the binding
        f = fields_of(BOOSTER); f['treat_rate_matrix'] = [dict(claim='X', treat_rate_wt_pct=vo(9.9, unit='wt.%'))]
        rt = [route('A', [group(f, 'b', 'all', 0)], bound_records=[dict(path='treat_rate_matrix[0]', sha256=R.record_fingerprint(f['treat_rate_matrix'][0]))])]
        self.assertEqual(states(f, rt), {'A': 'route_complete'})
        f['treat_rate_matrix'][0]['treat_rate_wt_pct']['value'] = 10.1
        self.assertEqual(states(f, rt), {'A': 'route_evidence_stale'})

    def test_stale_or_invalid_evidence_is_reported_as_historical_not_confirmed(self):
        f = fields_of(BOOSTER)
        r = [route('A', [group(f, 'b', 'all', 0)])]
        f['required_co_components'][0]['dose_wt_pct']['unit'] = '%'
        c = cx(routes=r)
        rts, unassigned, entries = R.co_component_routes(f, c)
        self.assertEqual([e['index'] for e in unassigned], [0], 'a stale association is not a current association')
        self.assertEqual(co(f, routes=r).category, R.ROUTE)
        rows = BR.route_rows('P', c, rts, entries, [], 'lvl', dict.fromkeys(BR.ROUTE_COLUMNS, ''))
        for x in rows:
            if x['route_id'] == 'A':
                self.assertEqual((x['review_validity'], x['source_inspection']), ('stale_requires_re_review', 'historical_source_review_not_current'))
        self.assertFalse([x for x in rows if x['source_inspection'] == 'confirmed_by_source_review'])
        self.assertTrue([x for x in rows if x['route_state'] == 'route_association_not_established' and x['entry_index'] == 0])
        bad = [route('B', [group(fields_of(BOOSTER), 'b', 'all', 0)], quote='')]
        x = R.co_component_routes(fields_of(BOOSTER), cx(routes=bad))[0][0]
        self.assertEqual((x['state'], x['validity']), ('route_evidence_invalid', 'invalid'))
        self.assertEqual(co(fields_of(BOOSTER), routes=[route('C', [group(fields_of(BOOSTER), 'b', 'all', 0)], product='OTHER')]).category, R.ROUTE,
                         'evidence for another product does not apply')

    def test_no_usable_dose_at_all(self):
        self.assertEqual(co(fields_of(VM_NO_DOSE)).category, R.ABSENT)
        self.assertEqual(co(fields_of(BARE)).category, R.META)

    # ---- "none required"
    def test_explicit_reviewed_applicable_statement(self):
        self.assertEqual(R.explicit_none_required(FULL, 'P'), (True, ''))
        self.assertEqual(co({}, statements=[FULL]).category, R.MET)
        inline = dict(FULL, status='Reported', source={'file': 'DL2-1.pdf', 'page': 2})
        self.assertEqual(co(dict(co_component_requirement_statement=inline)).category, R.MET)
        self.assertNotIn(co(dict(co_component_requirement_statement=dict(inline, status='Missing'))).category, R.SATISFIED)
        self.assertNotIn(co(dict(fields_of(VM_NO_DOSE), co_component_requirement_statement=inline)).category, R.SATISFIED,
                         'a recorded requirement contradicts "none required"')

    def test_qualified_wording_with_the_qualification_metadata_omitted(self):
        hedged = dict(FULL, quote='No supplemental PPD should be needed.')
        no_review = {k: v for k, v in hedged.items() if k != 'review'}
        ok, why = R.explicit_none_required(no_review, 'P')
        self.assertFalse(ok); self.assertIn('no reviewed assessment', why)
        partial = dict(hedged, review={k: v for k, v in REVIEW.items() if k not in ('qualification_verbatim', 'unconditional')})
        ok, why = R.explicit_none_required(partial, 'P')
        self.assertFalse(ok); self.assertIn('incomplete', why)
        ok, why = R.explicit_none_required(hedged, 'P')   # the review claims "unconditional" although the quote hedges
        self.assertFalse(ok); self.assertIn('contradictory', why)
        honest = dict(hedged, review=dict(REVIEW, unconditional=False, qualification_verbatim='should be needed'))
        ok, why = R.explicit_none_required(honest, 'P')
        self.assertFalse(ok); self.assertIn("'should be needed'", why, 'the supplier qualification is kept verbatim')
        self.assertEqual(co({}, statements=[honest]).category, R.UNKNOWN)

    def test_contradictory_or_incomplete_review_metadata_is_rejected(self):
        for rv in (dict(REVIEW, qualification_verbatim='normally'), dict(REVIEW, unconditional=False), dict(REVIEW, unconditional='yes'),
                   dict(REVIEW, meaning=''), dict(REVIEW, scope=dict(component_types='all')),
                   dict(REVIEW, unconditional=False, qualification_verbatim='words that are not in the quote')):
            self.assertFalse(R.explicit_none_required(dict(FULL, review=rv), 'P')[0], rv)
        self.assertFalse(R.explicit_none_required(dict(FULL, scope='pour point depressant'), 'P')[0], 'statement scope contradicts the reviewed scope')
        self.assertFalse(R.explicit_none_required(dict(FULL, review=dict(REVIEW, meaning='no_supplemental_ppd_expected')), 'P')[0])
        for bad in (dict(FULL, quote=''), dict(FULL, page=None)):
            self.assertFalse(R.explicit_none_required(bad, 'P')[0])

    def test_statement_belonging_to_another_product(self):
        other = dict(FULL, product='OTHER')
        self.assertFalse(R.explicit_none_required(other, 'P')[0])
        self.assertEqual(co({}, statements=[other]).category, R.UNKNOWN)
        inline = dict(other, status='Reported', source={'file': 'DL2-1.pdf', 'page': 2})
        self.assertNotIn(co(dict(co_component_requirement_statement=inline)).category, R.SATISFIED, 'inline statements are checked against the product too')
        unnamed = {k: v for k, v in inline.items() if k != 'product'}
        self.assertNotIn(co(dict(co_component_requirement_statement=unnamed)).category, R.SATISFIED, 'a statement that names no product is not applicable')

    def test_statement_limited_to_one_route_or_component_type_is_not_product_wide(self):
        for scope in (dict(component_types=['pour point depressant'], routes='all'), dict(component_types='all', routes=['API FA-4 route'])):
            st = dict(FULL, scope='', review=dict(REVIEW, scope=scope))
            ok, why = R.explicit_none_required(st, 'P')
            self.assertFalse(ok); self.assertIn('not a product-wide statement', why)
            self.assertEqual(co({}, statements=[st]).category, R.UNKNOWN)

    def test_arbitrary_statement_text_is_not_none_required(self):
        for stmt in (vo('no additional co-component required', unit=None), vo('n/a', unit=None), 'none', {'value': 'not needed'}):
            self.assertNotIn(co(dict(co_component_requirement_statement=stmt)).category, R.SATISFIED, stmt)

    def test_empty_record_is_not_supplier_silence(self):
        o = co(dict(required_co_components=[]))
        self.assertEqual(o.category, R.UNKNOWN)
        self.assertIn('describes the record, not the supplier documents', o.reason); self.assertNotIn('silent', o.reason)

    def test_current_data_reviewed_routes_and_statements(self):
        routes = BE.load_routes()
        reviewed = {'INFINEUM_D3354', 'INFINEUM_D3384', 'INFINEUM_D3451', 'LUBRIZOL_3589C', 'LUBRIZOL_3700', 'LUBRIZOL_3700D',
                    'LUBRIZOL_CV1100', 'LUBRIZOL_CV1103'}
        self.assertEqual({r['product'] for r in routes}, reviewed, 'only the eight reviewed packages have routes')
        self.assertFalse([r for r in routes if r['requirement_list_confirmed']], 'no list could be confirmed complete')
        for s in BE.load_statements():
            self.assertIn('should be needed', s['quote'], 'the supplier wording is kept as printed')
            self.assertEqual((s['review']['unconditional'], s['review']['qualification_verbatim']), (False, 'should be needed'))
            self.assertFalse(R.explicit_none_required(s, s['product'])[0])
        rows = read_report('co_component_routes.csv')
        rev = [r for r in rows if r['row_kind'] == 'reviewed_route']
        self.assertEqual(len(rev), len(routes))
        self.assertTrue(all(r['review_validity'] == 'current' and r['source_inspection'] == 'confirmed_by_source_review' for r in rev),
                        'every stored fingerprint still matches the product records')
        self.assertFalse([r for r in rev if r['route_state'] == 'route_complete'])
        mem = [r for r in rows if r['row_kind'] == 'recorded_requirement' and r['route_id']]
        shared = {(r['product_id'], r['entry_index']) for r in mem}
        self.assertGreater(len(mem), len(shared), 'components shared by several routes keep every membership')
        d3384 = [r['route_id'] for r in mem if r['product_id'] == 'INFINEUM_D3384' and r['entry_index'] == '2']
        self.assertEqual(sorted(d3384), ['D3384-row4', 'D3384-row9'], 'Infineum C9274 at 0.5 % belongs to the 20W-50 and the 10W-30 rows')
        for r in rows:
            if r['row_kind'] == 'recorded_requirement' and r['product_id'] not in reviewed:
                self.assertEqual(r['route_state'], 'route_association_not_established')
        outs = [r for r in read_report('requirement_outcomes.csv') if r['requirement'] == 'required_co_components']
        self.assertFalse([r for r in outs if r['category'] == R.MET])
        none = [r for r in rows if r['row_kind'] == 'no_recorded_requirement']
        self.assertTrue(all(r['record_state'] == 'not_recorded' and r['source_inspection'] in BR.SOURCE_INSPECTION and r['inspected'] for r in none))
        self.assertFalse([r for r in rows if 'silen' in (r['detail'] + r['product_level_outcome']).lower()])


''' + s[b:]
s = s.replace("import contextlib, csv, io, os, sys, unittest", "import contextlib, copy, csv, io, os, sys, unittest", 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
