"""Regression tests for the four policies approved on 2026-11-11 (ranges and bounds, co-components, percentage basis,
applicability), for the separation of evidence documentation, value selection, value form, percentage basis and
verification status, and for the gap fixes of the same day (route-level co-component completeness, selection status
independent of the outcome category, a narrowly defined basis flag, the unregistered conversion, evidence wording).
Synthetic inputs, except the tests marked "current data".

Run: python -m unittest discover -s tools/mandatory_properties/tests -v
"""
import contextlib, copy, csv, io, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import requirements as R  # noqa: E402
import build_eligibility as BE  # noqa: E402
import build_readiness as BR  # noqa: E402
import compare_eligibility as CE  # noqa: E402
from test_requirements import vo, ctx, base_oil, cats  # noqa: E402


def read_report(name):
    with open(os.path.join(BR.OUT, name), encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def pk(**f):
    return {1: dict(material_class='additive_package', tier=1, fields=f)}


def cx(**kw):
    return R.Context(product='P', material_class='additive_package', **kw)


def co(fields, **kw):
    return R.co_component_outcome(fields, cx(**kw))


BOOSTER = dict(role='Booster (API FA-4 route)', name='X', dose_wt_pct=vo(2.0, unit='wt.%'))
BOOSTER2 = dict(role='Booster (ACEA E4 route)', name='Z', dose_wt_pct=vo(1.5, unit='wt.%'))
VM_NO_DOSE = dict(role='Viscosity modifier', name=None, dose_wt_pct=vo(None, status='Missing', unit='wt.%'))
VM_DOSE = dict(role='Viscosity modifier', name='V', dose_wt_pct=vo(8.0, unit='wt.%'))
BARE = dict(role='Booster', name='Y', dose_wt_pct=vo(1.2, unit='%'))


def fields_of(*entries):
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


class Policy1RangesAndBounds(unittest.TestCase):
    def test_valid_range_and_bounds_are_documented_not_absent(self):
        for v, rep, form in ((vo(None, min=42.0, max=55.0, value_kind='range'), 'range', 'closed_range'),
                             (vo(121, qualifier='minimum', value_kind='minimum'), 'lower_bound', 'lower_bound'),
                             (vo(7000, qualifier='maximum', value_kind='maximum'), 'upper_bound', 'upper_bound')):
            o = R.check_value(v, 'kv40')
            self.assertEqual((o.category, o.representation), (R.BOUND, rep))
            self.assertEqual(BR.attributes(o.category, o.representation), ('documented', 'selected', form, 'no'))

    def test_range_does_not_satisfy_a_point_requirement_and_no_point_is_invented(self):
        outs = R.base_oil_requirements(base_oil(kv40=vo(None, min=42.0, max=55.0, value_kind='range', temp=40)))
        self.assertEqual(cats(outs)['kv40'], R.BOUND)
        self.assertEqual(R.summarize(outs), (False, False), 'a documented range is not a formulation approval')
        self.assertNotIn('value', R.Outcome._fields, 'an outcome carries no number, so no midpoint can be derived from a range')
        self.assertFalse([c for c in BR.ATTR_COLUMNS + BR.PRODUCT_COLUMNS if 'midpoint' in c or c in ('value', 'typical')])

    def test_invalid_range_is_not_documented(self):
        o = R.check_value(vo(None, min=10, max=2, value_kind='range'), 'kv40')
        self.assertEqual(o.category, R.INVALID)
        self.assertEqual(BR.attributes(o.category, o.representation)[0], 'invalid')

    def test_no_range_aware_calculation_or_conversion_is_registered(self):
        calcs = {r['calculation']: r['status'] for r in read_report('calculation_readiness.csv')}
        for name in ('any range-aware calculation', 'viscosity_index_from_kv40_kv100', 'volume_to_mass_percent'):
            self.assertTrue(calcs[name].startswith('not registered'), name)
        self.assertFalse([k for k, v in calcs.items() if 'ready' in v.lower()], 'no general readiness label')


class SelectionIndependentOfCategory(unittest.TestCase):
    """A pending source selection comes from the ledger and survives any other defect of the value."""
    PENDING = {('P', 'kv40'): 'pending: two technical documents disagree', ('P', 'density'): 'pending: spec vs brochure'}

    def test_pending_selection_on_an_otherwise_complete_value(self):
        o = next(x for x in R.base_oil_requirements(base_oil(), ctx(pending=self.PENDING)) if x.requirement == 'kv40')
        self.assertEqual((o.category, o.selection_pending), (R.SEL, True))
        ev, sel, form, point = BR.attributes(o.category, o.representation, o.selection_pending)
        self.assertEqual((ev, sel, form, point), ('documented', 'pending', 'point', 'no'), 'documented alternatives are not absent evidence')

    def test_pending_selection_combined_with_missing_metadata(self):
        # density without a unit AND with a pending selection (the aramcoPRIMA 110 / 230 / 500 case)
        d = vo(0.863, unit=None, temp=15)
        o = next(x for x in R.base_oil_requirements(base_oil(density=d), ctx(pending=self.PENDING)) if x.requirement == 'density')
        self.assertEqual(o.category, R.META, 'the metadata defect keeps its category')
        self.assertTrue(o.selection_pending, 'and the selection is still pending')
        self.assertIn('unit not recorded', o.reason); self.assertIn('source selection is pending', o.reason)
        ev, sel, form, point = BR.attributes(o.category, o.representation, o.selection_pending)
        self.assertEqual((ev, sel, point), ('documented_incomplete', 'pending', 'no'))

    def test_pending_selection_on_a_range(self):
        o = next(x for x in R.base_oil_requirements(base_oil(kv40=vo(None, min=42.0, max=55.0, value_kind='range', temp=40)),
                                                    ctx(pending=self.PENDING)) if x.requirement == 'kv40')
        self.assertEqual((o.category, o.selection_pending, o.representation), (R.SEL, True, 'range'))
        self.assertEqual(BR.attributes(o.category, o.representation, True)[1:3], ('pending', 'closed_range'))

    def test_no_pending_flag_without_a_ledger_entry(self):
        self.assertFalse(any(o.selection_pending for o in R.base_oil_requirements(base_oil(), ctx())))
        self.assertEqual(BR.attributes(R.MET, 'point', False), ('documented', 'selected', 'point', 'yes'))
        self.assertEqual(BR.attributes(R.MET, 'point', True)[3], 'no', 'a pending selection never yields a selected point value')

    def test_current_data_pending_selections_equal_the_ledger(self):
        with open(BE.LEDGER, encoding='utf-8') as fh:
            ledger = {(r['product'], r['property']) for r in csv.DictReader(fh)
                      if r['mandatory'] == 'true' and r['selection_status'] in BE.SELECTION_PENDING}
        outs = read_report('requirement_outcomes.csv')
        flagged = {(r['product_id'], r['requirement']) for r in outs if r['selection_pending'] == 'true'}
        self.assertEqual(flagged, ledger, 'every pending mandatory selection of the ledger is flagged, whatever the category')
        attrs = {(r['product_id'], r['requirement']) for r in read_report('property_attributes.csv') if r['value_selection'] == 'pending'}
        self.assertEqual(attrs, ledger)
        hidden = {k for k in ledger if next(r for r in outs if (r['product_id'], r['requirement']) == k)['category'] != R.SEL}
        self.assertEqual(hidden, {(f'ARAMCO_LUBEREF_PRIMA_{g}', 'density') for g in (110, 230, 500)},
                         'the three selections that the category precedence used to hide')


class SeparateAttributes(unittest.TestCase):
    def test_record_states_are_distinct(self):
        self.assertEqual(BR.attributes(R.ABSENT, '')[0], 'not_recorded')
        self.assertEqual(BR.attributes(R.UNKNOWN, '')[0], 'requirement_unknown')
        self.assertEqual(BR.attributes(R.ROUTE, '')[0], 'recorded_route_not_assessed')
        self.assertEqual(BR.attributes(R.META, 'point')[0], 'documented_incomplete')
        self.assertEqual(BR.attributes(R.APPL, '')[0], 'applicability_unresolved')
        self.assertEqual(BR.attributes(R.MET, 'text')[3], 'not_numeric')

    def test_form_basis_and_verification_are_separate_columns(self):
        for c in ('evidence_documentation', 'value_selection', 'value_form', 'percentage_basis', 'verification_status'):
            self.assertIn(c, BR.ATTR_COLUMNS)
        self.assertFalse([c for c in BR.PRODUCT_COLUMNS + BR.BASIS_COLUMNS if c.endswith('_ready') or 'usable' in c])


class Policy2CoComponentRoutes(unittest.TestCase):
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


class Policy3PercentageBasis(unittest.TestCase):
    def test_three_basis_classes(self):
        for unit, cls in (('wt.%', 'mass'), ('mass %', 'mass'), ('vol.%', 'volume'), ('% v/v', 'volume'), ('%', 'unspecified'), (None, 'unspecified')):
            self.assertEqual(R.percentage_basis(vo(10, unit=unit))[0], cls, unit)

    def test_basis_from_heading_footnote_or_document_convention(self):
        for kind, scope in (('heading', 'table'), ('footnote', 'value'), ('document_convention', 'document')):
            ev = dict(product='P', field='treat_rate_matrix', source_file='DL2-00000.pdf', page=1, values=None, basis='mass %',
                      basis_class='mass', evidence_kind=kind, scope=scope, quote='Mass %:')
            c = R.Context(basis_evidence=[ev], product='P')
            cls, how = c.basis_of('treat_rate_matrix', vo(10.3, unit='%'))
            self.assertEqual(cls, 'mass'); self.assertIn(kind, how); self.assertIn(scope, how)
        vol = dict(product='P', field='treat_rate_matrix', source_file='DL2-00000.pdf', page=1, values=None, basis='vol.%')
        self.assertEqual(R.Context(basis_evidence=[vol], product='P').basis_of('treat_rate_matrix', vo(10.3, unit='%'))[0], 'volume')
        nob = dict(vol, basis=None)
        self.assertEqual(R.Context(basis_evidence=[nob], product='P').basis_of('treat_rate_matrix', vo(10.3, unit='%'))[0], 'unspecified')

    def test_unspecified_and_volume_are_refused_where_wt_pct_is_required(self):
        o = R.check_value(vo(10.3, unit='%'), 'treat_rate_matrix', mass_basis=True)
        self.assertEqual((o.category, o.basis), (R.META, 'unspecified'))
        v = vo(10.3, unit='%')
        R.check_value(v, 'treat_rate_matrix', mass_basis=True)
        self.assertEqual(v['unit'], '%', 'the recorded unit is never rewritten')
        o = R.check_value(vo(8.0, unit='vol.%'), 'treat_rate_matrix', mass_basis=True)
        self.assertEqual((o.category, o.basis), (R.META, 'volume'))
        self.assertIn('no volume-to-mass conversion is registered', o.reason)

    def test_mass_basis_value_that_is_otherwise_unusable(self):
        # the basis flag is about the basis only: these values are on a mass basis and still not met
        nosrc = vo(10.3, unit='wt.%', source={'file': None, 'page': None})
        o = R.check_value(nosrc, 'treat_rate_matrix', mass_basis=True)
        self.assertEqual((o.basis, o.category), ('mass', R.META)); self.assertIn('no source file', o.reason)
        bound = vo(10.3, unit='wt.%', qualifier='maximum', value_kind='maximum')
        o = R.check_value(bound, 'treat_rate_matrix', mass_basis=True)
        self.assertEqual((o.basis, o.category), ('mass', R.BOUND))
        self.assertEqual(R.check_value(vo('ten', unit='wt.%'), 'treat_rate_matrix', mass_basis=True).category, R.INVALID)
        self.assertIn('basis_is_mass', BR.BASIS_COLUMNS); self.assertIn('value_outcome_category', BR.BASIS_COLUMNS)

    def test_current_data_basis_flag_is_narrow_and_volume_evidence_is_separate(self):
        basis = read_report('percentage_basis.csv')
        self.assertTrue(all((r['basis_is_mass'] == 'true') == (r['basis_class'] == 'mass') for r in basis))
        self.assertTrue([r for r in basis if r['basis_is_mass'] == 'true' and r['value_outcome_category'] != R.MET],
                        'a mass basis does not make a value usable')
        self.assertFalse([r for r in basis if r['basis_class'] not in R.BASIS_CLASSES])
        vol = read_report('volume_dose_evidence.csv')
        self.assertTrue(vol)
        for r in vol:
            self.assertEqual(r['product_id'], 'AFTON_HITEC_5748')
            self.assertTrue(r['grade_or_context'] and r['source'] and 'vol' in r['evidence_as_recorded'].lower())
            self.assertEqual(r['record_status'], 'Missing', 'the wt.% field stays Missing: it is not filled from volume evidence')
            self.assertIn('not converted', r['use'])
        self.assertFalse([r for r in basis if r['product_id'] == 'AFTON_HITEC_5748'], 'no wt.% value was created from the volume evidence')

    def test_conversion_is_unregistered_and_claims_only_arithmetic(self):
        doc = R.volume_to_mass_percent.__doc__
        self.assertIn('NOT REGISTERED AND NOT USED', doc)
        for claim in ('does NOT and cannot establish', 'same unit', 'applicable'):
            self.assertIn(claim, doc)
        self.assertAlmostEqual(R.volume_to_mass_percent(10.0, 0.90, 0.85, 15, 15)[0], 10.0 * 0.90 / 0.85, places=9)
        for args in ((10.0, None, 0.85, 15, 15), (10.0, 0.90, 0.85, 15, 20), (10.0, 0.90, 0.85, None, 15), (120.0, 0.90, 0.85, 15, 15)):
            self.assertIsNone(R.volume_to_mass_percent(*args)[0], args)
        with open(os.path.join(os.path.dirname(HERE), 'requirements.py'), encoding='utf-8') as fh:
            src = fh.read()
        self.assertEqual(src.count('volume_to_mass_percent('), 1, 'defined, never called')


class Policy4Applicability(unittest.TestCase):
    RULE = dict(id='TEST-1', material_class='base_oil', requirement='ccs', task=R.DEFAULT_TASK,
                authority='test document p.1: "CCS does not apply to process oils"', approved='2026-01-01')

    def test_no_rule_is_approved_in_production(self):
        self.assertEqual(R.APPROVED_APPLICABILITY_RULES, [])

    def test_label_without_rule_is_unresolved(self):
        c = R.Context(product='P', material_class='base_oil')
        self.assertEqual(R.check_value(vo(None, status='Not Required', unit='mPa.s'), 'ccs', c).category, R.APPL)
        self.assertEqual(R.check_value(vo(None, status='Not Applicable', unit='mPa.s'), 'ccs', c).category, R.APPL)

    def test_rule_applies_only_to_its_class_requirement_and_task(self):
        base = R.Context(product='P', material_class='base_oil')
        self.assertEqual(R.approved_rule('ccs', base, [self.RULE]), self.RULE)
        self.assertIsNone(R.approved_rule('kv40', base, [self.RULE]))
        self.assertIsNone(R.approved_rule('ccs', R.Context(product='P', material_class='additive_package'), [self.RULE]))
        self.assertIsNone(R.approved_rule('ccs', R.Context(product='P', material_class='base_oil', task='another task'), [self.RULE]))
        self.assertIsNone(R.approved_rule('ccs', None, [self.RULE]), 'no product class: no rule can apply')
        self.assertIsNone(R.approved_rule('ccs', base, [dict(self.RULE, authority='')]), 'a rule without a documented authority is not a rule')

    def test_missing_or_not_found_is_never_not_applicable(self):
        R.APPROVED_APPLICABILITY_RULES.append(self.RULE)
        try:
            c = R.Context(product='P', material_class='base_oil')
            self.assertEqual(R.check_value(vo(None, status='Not Required', unit='mPa.s'), 'ccs', c).category, R.NOT_APPLICABLE)
            self.assertEqual(R.check_value(vo(None, status='Missing', unit='mPa.s'), 'ccs', c).category, R.ABSENT)
            self.assertEqual(R.check_value(None, 'ccs', c).category, R.ABSENT)
            self.assertEqual(R.check_value(vo(None, status='Not Required', unit='cSt'), 'kv40', c).category, R.APPL)
        finally:
            R.APPROVED_APPLICABILITY_RULES.remove(self.RULE)
        self.assertEqual(R.APPROVED_APPLICABILITY_RULES, [])

    def test_no_property_changed_tier(self):
        ids = {o.requirement for o in R.base_oil_requirements(base_oil()) if o.blocking}
        self.assertEqual(ids, {'api_group_chemistry.api_group', 'api_group_chemistry.chemistry', 'kv40', 'kv100', 'viscosity_index', 'density', 'ccs'})
        f = dict(function=dict(primary=vo('Viscosity modifier', unit=None)), chemical_family=vo('OCP', unit=None))
        outs = R.additive_component_requirements({'general': dict(fields=f)})
        self.assertTrue(all(not o.blocking for o in outs if o.requirement.startswith('vm')), 'the VM block stays non-blocking')
        self.assertEqual(cats(R.additive_package_requirements(pk()))['published_formulations'], R.ABSENT,
                         'the published-formulation requirement is unchanged and blocking')


class InterfaceAndComparison(unittest.TestCase):
    def test_interface_columns_and_meaning_unchanged(self):
        self.assertEqual(BE.COLUMNS, ['product_id', 'material_class', 'product_name', 'supplier', 'tier1_complete', 'formulation_eligible',
                                      'missing_mandatory_properties', 'eligibility_reasons', 'calculated_mandatory_properties',
                                      'requirements_version', 'source_snapshot_sha256'])
        self.assertEqual(R.summarize(R.base_oil_requirements(base_oil())), (True, True))
        self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.6')

    def test_comparison_reports_changes_instead_of_requiring_identity(self):
        row = dict(product_id='P', material_class='base_oil', tier1_complete='false', formulation_eligible='false',
                   missing_mandatory_properties='["kv40"]', eligibility_reasons='["kv40 [absent]"]')
        after = dict(row, tier1_complete='true', formulation_eligible='true', missing_mandatory_properties='[]', eligibility_reasons='["all met"]')
        out_b = [dict(product_id='P', requirement='kv40', category='absent', blocking='true', reason='')]
        out_a = [dict(product_id='P', requirement='kv40', category='met', blocking='true', reason='')]
        counts, products, cs = CE.compare([row], out_b, [after], out_a)
        self.assertEqual([(c['before'], c['after']) for c in counts if c['field'] == 'formulation_eligible'], [(0, 1)])
        self.assertEqual(len(products), 1); self.assertIn('all met', products[0]['reasons_after'])
        self.assertEqual((cs[0]['category_before'], cs[0]['category_after']), ('absent', 'met'))
        with self.assertRaises(ValueError):
            CE.compare([row], out_b, [dict(after, product_id='Q')], out_a)

    def test_current_data_readiness_outputs_up_to_date_and_consistent(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(BR.main(['--check']), 0)
        attrs, prods = read_report('property_attributes.csv'), read_report('product_input_completeness.csv')
        elig = {r['product_id']: r for r in read_report('product_eligibility.csv')}
        for p in prods:   # the companion file copies the eligibility fields; it never redefines them
            self.assertEqual((p['tier1_complete'], p['formulation_eligible']), (elig[p['product_id']]['tier1_complete'], elig[p['product_id']]['formulation_eligible']))
        self.assertFalse([a for a in attrs if a['value_selection'] == 'pending' and a['selected_point_value'] == 'yes'])
        self.assertFalse([a for a in attrs if a['value_form'] in ('closed_range', 'lower_bound', 'upper_bound') and a['selected_point_value'] == 'yes'])
        packages = {p['product_id'] for p in prods if p['material_class'] == 'additive_package'}
        self.assertEqual({r['product_id'] for r in read_report('co_component_routes.csv')}, packages, 'every package has route-level rows')


if __name__ == '__main__':
    unittest.main()
