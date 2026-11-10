"""Regression tests for the mandatory-requirement rules (tools/mandatory_properties/requirements.py).

The five inputs an independent review found to be wrongly accepted on 2026-11-10 are reproduced here (synthetic test
inputs, not product data): a reversed range [10, 2]; infinity as a value; the qualifier '≮' read as an exact value; a
shear-loss calculation whose note gives 10 while 999 is stored, with no source; a thickening calculation for Oil A at
1 % stored on a response record for Oil B at 9 %. Each has a valid counterpart that must still be accepted.

Run: python -m unittest discover -s tools/mandatory_properties/tests -v
"""
import copy, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import requirements as R  # noqa: E402

PAGE = ('Typical data. 1% KV40/100(mm2/s) 32.077/5.77; 0% 29.22/5.23. In 150N (10% of RF) Before Shear KV100 10.24; '
        'after 30 cycles 10.00; base oil 5.23')


def vo(value=None, status='Reported', unit='cSt', temp=None, **kw):
    d = dict(value=value, qualifier=None, min=None, max=None, value_kind=None, printed_text=str(value), unit=unit,
             test_temperature_c=temp, method=None, status=status, calculation_note=None,
             source={'file': 'DL2-00000.pdf', 'page': 1, 'revision_date': None})
    d.update(kw)
    return d


def ctx(pending=None, basis=None, page=PAGE, product='P'):
    return R.Context(page_text=lambda f, p: page if f == 'DL2-00000.pdf' else None, pending=pending, basis_evidence=basis, product=product)


def base_oil(**over):
    f = dict(api_group_chemistry=dict(api_group=vo('Group III', unit=None), chemistry=vo('hydrocracked', unit=None)),
             kv40=vo(19.6, temp=40), kv100=vo(4.2, temp=100), viscosity_index=vo(125, unit=None),
             density=vo(835, unit='kg/m3', temp=15), specific_gravity=vo(None, status='Missing', unit=None),
             ccs=[vo(1200, unit='mPa.s', temp=-30)])
    f.update(over)
    return {1: dict(material_class='base_oil', tier=1, fields=f, conflicts=[])}


def cats(outs):
    return {o.requirement: o.category for o in outs}


def unmet(outs):
    return sorted(o.requirement for o in outs if o.blocking and o.category not in R.SATISFIED)


class ReportedBugs(unittest.TestCase):
    """The five reproduced acceptances, now rejected; each with a valid counterpart."""

    def test_reversed_range_rejected(self):
        self.assertEqual(R.check_value(vo([10, 2]), 'treat_rate').category, R.INVALID)
        self.assertEqual(R.check_value(vo(None, min=10, max=2), 'treat_rate').category, R.INVALID)
        self.assertEqual(R.check_value(vo([2, 10], unit='wt.%'), 'treat_rate', mass_basis=True).category, R.MET)

    def test_infinity_rejected(self):
        for bad in (float('inf'), float('-inf'), float('nan')):
            self.assertEqual(R.check_value(vo(bad), 'kv100').category, R.INVALID, bad)
        self.assertEqual(R.check_value(vo(None, min=float('-inf'), max=5), 'treat_rate').category, R.INVALID)
        self.assertEqual(R.check_value(vo(4.2), 'kv100').category, R.MET)

    def test_not_less_than_is_a_bound_not_an_exact_value(self):
        o = R.check_value(vo(180, qualifier='≮', unit='°C'), 'kv100')
        self.assertEqual((o.category, o.representation), (R.BOUND, 'lower_bound'))
        o = R.check_value(vo(30, qualifier='≯', unit='°C'), 'kv100')
        self.assertEqual((o.category, o.representation), (R.BOUND, 'upper_bound'))
        self.assertEqual(R.check_value(vo(180, qualifier='typical', unit='°C'), 'kv100').category, R.MET)

    def test_shear_loss_note_10_stored_999_without_source_rejected(self):
        bad = vo(999, status='Calculated', unit='%', source={}, calculation_note='(10 - 9) / 10 x 100 = 10')
        ok, why = R.calc_viscosity_loss({})(bad, ctx())
        self.assertFalse(ok)
        self.assertIn('differs from the result stated', why)
        e = dict(index_type='SSI', method='ASTM D6278', cycle_count=30, value=bad)
        self.assertEqual(cats(R.vm_requirements({'fields': {'shear_stability': [e]}}, ctx()))['vm.shear_stability'], R.CALC)
        good = vo(2.34, status='Calculated', unit='%', calculation_note='(10.24 - 10.0) / 10.24 x 100 = 2.34 % (30 cycles)')
        self.assertTrue(R.calc_viscosity_loss({})(good, ctx(page=PAGE.replace('10.00', '10.0')))[0])

    def test_thickening_for_another_oil_and_dose_rejected(self):
        note = 'ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in Oil A = 0.54'
        e = dict(reference_oil='Oil B', dose_wt_pct=9, method='ASTM D445',
                 delta_kv100_cst=vo(0.54, status='Calculated', temp=100, calculation_note=note, printed_text='mm2/s'))
        o = R.check_value(e['delta_kv100_cst'], 'vm.thickening_response', ctx(), calc=R.calc_delta_kv100(e))
        self.assertEqual(o.category, R.CALC)
        self.assertIn('dose', o.reason)
        e2 = dict(e, dose_wt_pct=1)
        o = R.check_value(e2['delta_kv100_cst'], 'vm.thickening_response', ctx(), calc=R.calc_delta_kv100(e2))
        self.assertIn('reference oil', o.reason)
        good = dict(reference_oil='150N', dose_wt_pct=1, method='ASTM D445', delta_kv100_cst=vo(
            0.54, status='Calculated', temp=100, printed_text='1% KV40/100(mm2/s) 32.077/5.77; 0% 29.22/5.23',
            calculation_note='ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in 150N = 0.54'))
        o = R.check_value(good['delta_kv100_cst'], 'vm.thickening_response', ctx(), calc=R.calc_delta_kv100(good))
        self.assertEqual((o.category, o.calculated), (R.MET, True))


class NumericValidation(unittest.TestCase):
    def test_booleans_are_not_measurements(self):
        self.assertEqual(R.check_value(vo(True), 'kv100').category, R.INVALID)
        self.assertFalse(R.finite(True))

    def test_text_in_numeric_field_invalid(self):
        self.assertEqual(R.check_value(vo('4.2 - 4.6'), 'kv100').category, R.INVALID)

    def test_unicode_inequalities(self):
        for q, rep in (('≥', 'lower_bound'), ('⩾', 'lower_bound'), ('>', 'lower_bound'), ('≤', 'upper_bound'), ('<', 'upper_bound'),
                       ('Max', 'upper_bound'), ('minimum', 'lower_bound')):
            self.assertEqual(R.representation(vo(5, qualifier=q))[0], rep, q)

    def test_unknown_and_conflicting_qualifiers_never_exact(self):
        self.assertEqual(R.check_value(vo(5, qualifier='±'), 'kv100').category, R.INVALID)
        self.assertEqual(R.check_value(vo(5, value_kind='guess'), 'kv100').category, R.INVALID)
        self.assertEqual(R.check_value(vo(5, qualifier='minimum', value_kind='maximum'), 'kv100').category, R.INVALID)
        o = R.check_value(vo(5, qualifier='>', value_kind='typical'), 'kv100')
        self.assertEqual(o.category, R.BOUND)
        self.assertIn('qualifier', o.reason)

    def test_value_outside_its_own_range_invalid(self):
        self.assertEqual(R.check_value(vo(12, min=5, max=10, value_kind='typical'), 'kv100').category, R.INVALID)
        self.assertEqual(R.check_value(vo(7, min=5, max=10, value_kind='typical'), 'kv100').category, R.MET)

    def test_bound_with_two_different_numbers_invalid(self):
        self.assertEqual(R.check_value(vo(81, qualifier='minimum', min=80, value_kind='single', unit=None), 'viscosity_index').category,
                         R.INVALID)

    def test_zero_is_valid(self):
        self.assertEqual(R.check_value(vo(0, unit='°C'), 'pour_point').category, R.MET)
        self.assertEqual(R.check_value(vo([0, 0.5], unit='wt.%'), 'treat_rate', mass_basis=True).category, R.MET)


class Categories(unittest.TestCase):
    def test_absent_vs_unusable(self):
        self.assertEqual(R.check_value(vo(None, status='Missing'), 'kv100').category, R.ABSENT)
        self.assertEqual(R.check_value(vo(4.2, unit=None), 'kv100').category, R.META)
        self.assertEqual(R.check_value(vo(835, unit='kg/m3'), 'density', need_temp=True).category, R.META)
        self.assertEqual(R.check_value(vo(4.2, source={'file': 'DL2-1.pdf', 'page': None}), 'kv100').category, R.META)
        self.assertEqual(R.check_value(vo(4.2, source={'file': 'https://example.org/x', 'page': None}), 'kv100').category, R.MET)
        self.assertEqual(R.check_value(vo(4.2, status='Not Required'), 'kv100').category, R.APPL)
        self.assertEqual(R.check_value(vo(4.2, status='Approved'), 'kv100').category, R.INVALID)

    def test_one_sided_bound_is_documented_not_absent(self):
        o = R.check_value(vo(121, qualifier='minimum', value_kind='minimum', unit=None), 'viscosity_index', need_unit=False)
        self.assertEqual(o.category, R.BOUND)
        complete, eligible = R.summarize(R.base_oil_requirements(base_oil(viscosity_index=vo(121, qualifier='minimum', unit=None))))
        self.assertEqual((complete, eligible), (True, False))

    def test_range_accepted_where_the_source_names_it(self):
        self.assertEqual(R.check_value(vo(None, min=4, max=6, value_kind='range', unit='wt.%'), 'treat_rate', mass_basis=True).category, R.MET)
        self.assertEqual(R.check_value(vo(None, min=4, max=6, value_kind='range'), 'kv100').category, R.BOUND)

    def test_pending_selection(self):
        outs = R.base_oil_requirements(base_oil(), ctx(pending={('P', 'kv40'): 'pending: test'}))
        self.assertEqual(cats(outs)['kv40'], R.SEL)
        self.assertEqual(R.summarize(outs), (True, False))

    def test_unresolved_applicability_not_complete(self):
        outs = R.base_oil_requirements(base_oil(ccs=[vo(None, status='Not Required', unit='mPa.s')]))
        self.assertEqual(cats(outs)['ccs'], R.APPL)
        self.assertEqual(R.summarize(outs), (False, False))


class Calculations(unittest.TestCase):
    def test_no_registered_check(self):
        o = R.check_value(vo(125, unit=None, status='Calculated', calculation_note='from KV40/KV100'), 'viscosity_index', need_unit=False)
        self.assertEqual((o.category, o.calculated), (R.CALC, True))

    def test_calculated_status_cannot_bypass_through_blocks_claims_formulations(self):
        blk = dict(base_oil_groups=['Group II'], status='Calculated', source={'file': 'DL2-0.pdf', 'page': 1})
        self.assertEqual(R.check_block(blk, 'compatibility_restrictions').category, R.CALC)
        pk = {1: dict(fields=dict(
            package_type_application=dict(package_type=vo('engine', unit=None), intended_service=vo('HDDO', unit=None)),
            performance_claims=[dict(designation='API CK-4', claim_type='claim', status='Calculated', source={'file': 'a.pdf', 'page': 1})],
            published_formulations=[dict(ingredients=[dict(name='a', wt_pct=100)], status='Calculated', results=[],
                                         source={'file': 'a.pdf', 'page': 1})]))}
        c = cats(R.additive_package_requirements(pk))
        self.assertEqual(c['performance_claims'], R.CALC)
        self.assertEqual(c['published_formulations'], R.CALC)

    def test_stored_result_must_match_recomputed(self):
        v = vo(0.60, status='Calculated', temp=100, printed_text='mm2/s',
               calculation_note='ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in 150N = 0.60')
        e = dict(reference_oil='150N', dose_wt_pct=1, method='D445', delta_kv100_cst=v)
        o = R.check_value(v, 'x', ctx(), calc=R.calc_delta_kv100(e))
        self.assertEqual(o.category, R.CALC)
        self.assertIn('recomputed', o.reason)

    def test_inputs_must_be_on_the_cited_page(self):
        v = vo(0.54, status='Calculated', temp=100, printed_text='mm2/s',
               calculation_note='ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in 150N = 0.54')
        e = dict(reference_oil='150N', dose_wt_pct=1, method='D445', delta_kv100_cst=v)
        self.assertIn('not found', R.check_value(v, 'x', ctx(page='nothing here'), calc=R.calc_delta_kv100(e)).reason)
        self.assertIn('cannot be verified', R.check_value(v, 'x', R.Context(), calc=R.calc_delta_kv100(e)).reason)

    def test_unestablished_input_unit_rejected(self):
        v = vo(0.54, status='Calculated', temp=100, printed_text='1% KV40/100℃(mm/s2) 32.077/5.77; 0% 29.22/5.23',
               calculation_note='ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in 150N = 0.54')
        e = dict(reference_oil='150N', dose_wt_pct=1, method='D445', delta_kv100_cst=v)
        self.assertIn('unit', R.check_value(v, 'x', ctx(), calc=R.calc_delta_kv100(e)).reason)

    def test_ssi_formula_index_type_and_zero_denominator(self):
        note = '(10.24 - 10.0) / (10.24 - 5.23) x 100 = 4.79 (30 cycles)'
        e = dict(index_type='SSI', method='ASTM D6278', cycle_count=30, value=vo(4.79, status='Calculated', unit=None, calculation_note=note))
        self.assertEqual(R.check_value(e['value'], 'vm.shear_stability', ctx(page=PAGE.replace('10.00', '10.0')), need_unit=False,
                                       calc=R.calc_shear_index(e)).category, R.MET)
        loss = dict(e, index_type='KV100 viscosity loss, % (calculated; no SSI printed)')
        self.assertIn('not SSI', R.calc_shear_index(loss)(e['value'], ctx())[1])
        self.assertEqual(R.index_kind('KV100 viscosity loss, % (calculated; no SSI printed)'), 'viscosity_loss')
        zero = dict(e, value=vo(1, status='Calculated', calculation_note='(5 - 4) / (5 - 5) x 100 = 1'))
        self.assertIn('zero', R.calc_shear_index(zero)(zero['value'], ctx())[1])
        self.assertIn('zero', R.calc_viscosity_loss({})(vo(1, status='Calculated', calculation_note='(0 - 0) / 0 x 100 = 1'), ctx())[1])
        other = dict(e, cycle_count=250)
        self.assertIn('cycle', R.calc_shear_index(other)(e['value'], ctx())[1])

    def test_invalid_inputs_do_not_crash(self):
        e = dict(reference_oil='150N', dose_wt_pct='abc', method='D445', delta_kv100_cst=vo(0.54, status='Calculated', calculation_note='x'))
        self.assertEqual(cats(R.vm_requirements({'fields': {'thickening_response': [e]}}, ctx()))['vm.thickening_response'], R.INVALID)
        self.assertFalse(R.calc_delta_kv100(e)(e['delta_kv100_cst'], ctx())[0])


class Nested(unittest.TestCase):
    def test_complete_base_oil_and_optional_specific_gravity(self):
        self.assertEqual(unmet(R.base_oil_requirements(base_oil())), [])

    def test_ccs_list(self):
        self.assertEqual(unmet(R.base_oil_requirements(base_oil(ccs=[]))), ['ccs'])
        two = [vo(None, status='Missing', unit='mPa.s', temp=-25), vo(3000, unit='mPa.s', temp=-20)]
        self.assertEqual(unmet(R.base_oil_requirements(base_oil(ccs=two))), [])
        self.assertEqual(cats(R.base_oil_requirements(base_oil(ccs=[vo(1200, unit='mPa.s')])))['ccs'], R.META)

    def test_specific_gravity_never_substitutes_density(self):
        b = base_oil(density=vo(None, status='Missing', unit='kg/m3', temp=15), specific_gravity=vo(0.835, unit=None, temp=15.6))
        self.assertEqual(unmet(R.base_oil_requirements(b)), ['density'])

    def test_formulation_rules(self):
        def pk(form):
            return {1: dict(fields=dict(published_formulations=[form]))}
        res = [dict(property='KV100', result=vo(14.5, temp=100))]
        src = {'file': 'a.pdf', 'page': 2}
        f99 = dict(ingredients=[dict(name='pkg', wt_pct=10), dict(name='oil', wt_pct=89)], status='Reported', results=res, source=src)
        self.assertEqual(cats(R.additive_package_requirements(pk(f99)))['published_formulations'], R.INVALID)
        f100 = dict(f99, ingredients=[dict(name='pkg', wt_pct=10), dict(name='oil', wt_pct=90)])
        self.assertEqual(cats(R.additive_package_requirements(pk(f100)))['published_formulations'], R.MET)
        self.assertEqual(cats(R.additive_package_requirements(pk(dict(f100, total_wt_pct=99))))['published_formulations'], R.INVALID)
        self.assertEqual(cats(R.additive_package_requirements(pk(dict(f100, results=[]))))['published_formulations'], R.ABSENT)

    def test_co_component_architecture(self):
        def pk(**f):
            return {1: dict(fields=f)}
        self.assertEqual(cats(R.additive_package_requirements(pk(required_co_components=[])))['required_co_components'], R.APPL)
        stmt = vo('no additional co-component required', unit=None)
        self.assertEqual(cats(R.additive_package_requirements(pk(co_component_requirement_statement=stmt)))['required_co_components'], R.MET)
        e = dict(role='VM', name='X', dose_wt_pct=vo(1.2, unit='%'))
        self.assertEqual(cats(R.additive_package_requirements(pk(required_co_components=[e])))['required_co_components'], R.META)
        basis = [dict(product='P', field='required_co_components', source_file='DL2-00000.pdf', page=1, values=None)]
        outs = R.additive_package_requirements(pk(required_co_components=[e]), ctx(basis=basis))
        self.assertEqual(cats(outs)['required_co_components'], R.MET)

    def test_component_markers_and_subtypes(self):
        def comp(primary, family, markers, extra=None):
            f = dict(function=dict(primary=vo(primary, unit=None) if primary else vo(None, status='Missing', unit=None)),
                     chemical_family=vo(family, unit=None), active_content=vo(80, unit='wt.%', notes='basis: as supplied'),
                     carrier=dict(identity=vo('mineral oil', unit=None)), treat_rate=vo(1.0, unit='wt.%'),
                     compatibility_restrictions=dict(base_oil_groups=['Group II'], status='Reported', source={'file': 'a.pdf', 'page': 1}),
                     function_specific_markers=markers)
            return dict({'general': dict(fields=f)}, **(extra or {}))
        z = comp('Antiwear (ZDDP)', 'zinc dialkyldithiophosphate', dict(p=vo(0, unit='wt.%'), zn=vo(9.0, unit='wt.%')))
        self.assertEqual(unmet(R.additive_component_requirements(z)), [])
        x = comp('Friction modifier', 'ester', {})
        self.assertEqual(cats(R.additive_component_requirements(x))['function_specific_markers'], R.APPL)
        n = comp(None, 'ester', {})
        self.assertEqual(cats(R.additive_component_requirements(n))['function_specific_markers'], R.APPL)
        vm = comp('Viscosity modifier', 'OCP', {}, extra={'vm': dict(fields={})})
        outs = R.additive_component_requirements(vm)
        sub = [o for o in outs if o.requirement.startswith('vm.')]
        self.assertTrue(sub and all(not o.blocking for o in sub))
        self.assertTrue(all(o.requirement.startswith('vm.') or o.requirement == 'function_specific_markers' for o in outs
                            if o.category not in R.SATISFIED))


if __name__ == '__main__':
    unittest.main()
