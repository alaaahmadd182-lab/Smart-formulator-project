"""Regression tests for Workstream A (source selection, TDS-SDS comparison rules, mandatory Tier 1 eligibility).

They prove that:
  1. TDS preference: every declared selection now holds the technical-document value, the replaced SDS value is kept
     as an alternate with its provenance, and no selected SDS value with a technical alternate is left undeclared;
  2. SDS fallback: an SDS value stays selected where no technical value exists, and a declared exception keeps the SDS;
  3. comparison rules: comparability is decided before any difference, units are converted, bounds are checked, not
     differenced, and a label/unit inconsistency or missing temperature keeps a pair pending;
  4. mandatory rules: nested requirements (CCS list, package lists, component subtype blocks), valid zero values,
     optional fields, calculated values (accepted only with a reproducible check) and ineligible products;
  5. outputs: exact interface columns, lowercase booleans, JSON arrays, the snapshot hash and the summary counts;
  6. no module writes on import, and the product data differs from the baseline only in the declared files.

Run: python -m unittest discover -s tools/data_policy/tests -v
"""
import copy, csv, hashlib, importlib, io, json, os, subprocess, sys, unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(DP))
MP = os.path.join(ROOT, 'tools', 'mandatory_properties')
sys.path[:0] = [DP, MP]
import policy_lib as P  # noqa: E402
import thresholds as TH  # noqa: E402
import tds_sds_inventory as INV  # noqa: E402
import requirements as REQ  # noqa: E402
import build_eligibility as BE  # noqa: E402

BASELINE = 'f4d97e71f72598df601b72403775581c34061ad1'
ALLOWED_STATUS = {'Reported', 'Calculated', 'Missing', 'Not Required', 'N/A', 'Not Applicable'}


def _classes():
    with open(os.path.join(P.REPORTS, 'data_policy', 'document_classes.csv'), encoding='utf-8') as fh:
        return {(r['file'], r['page']): r['class'] for r in csv.DictReader(fh)}


def _cls(classes, src):
    f, pg = src.get('file'), src.get('page')
    return classes.get((str(f), str(pg).split()[0] if pg not in (None, '') else ''))


def _node(doc, path):
    n = doc['fields']
    for k in path.split('.'):
        n = n[k]
    return n


class SourceSelection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import source_selection as S
        cls.S = S
        cls.prods = P.load_products()
        cls.classes = _classes()

    def _doc(self, pid, name):
        return next(d for rel, d in self.prods[pid]['files'].items() if rel.endswith('/' + name))

    def test_tds_value_selected_and_sds_kept_as_alternate(self):
        for ch in self.S.CHANGES:
            with self.subTest(product=ch['product'], path=ch['path']):
                n = _node(self._doc(ch['product'], ch['file']), ch['path'])
                self.assertEqual(n['value'], ch['new']['value'])
                self.assertEqual(n['status'], 'Reported')
                self.assertEqual(_cls(self.classes, n['source']), 'TECHNICAL', n['source'])
                if ch['expect'].get('value') is None:  # previously Missing: there is no earlier value to keep
                    continue
                olds = [a for a in n.get('alternate_entries') or [] if a.get('value') == ch['expect']['value']]
                self.assertTrue(olds, 'replaced value is not kept as an alternate')
                self.assertEqual(olds[-1]['source']['file'], ch['expect']['source'])
                self.assertTrue(olds[-1].get('selection_note'))

    def test_no_undeclared_sds_selection_with_technical_alternate(self):
        declared = {(p, f.strip()) for p, fs, _ in self.S.EXCEPTIONS + self.S.PENDING for f in fs.split(',')}
        for pid, p in self.prods.items():
            for rel, d in p['files'].items():
                for path, n in P.value_objects(d.get('fields', {})):
                    if _cls(self.classes, n.get('source') or {}) != 'SDS':
                        continue
                    tech = [a for a in n.get('alternate_entries') or [] if _cls(self.classes, a.get('source') or {}) == 'TECHNICAL'
                            and a.get('value') is not None]
                    if tech:
                        with self.subTest(product=pid, path=path):
                            self.assertIn((pid, path.split('.')[-1]), declared,
                                          'SDS value selected although a technical alternate exists, with no recorded exception')

    def test_exception_keeps_sds_value(self):
        n = _node(next(d for d in self.prods['PETRONAS_ETRO_6_PLUS']['files'].values() if d.get('tier') == 1), 'density')
        self.assertEqual(_cls(self.classes, n['source']), 'SDS')
        self.assertIsNotNone(n['test_temperature_c'])

    def test_sds_fallback_where_no_tds_value(self):
        # SDS-only package (SDS_FALLBACK_CONFIRMED): SDS-sourced values stay selected and Reported
        d = next(d for d in self.prods['CHEVRON_OLOA_59766']['files'].values() if d.get('tier') == 2)
        sds = [n for _, n in P.value_objects(d['fields']) if n.get('status') == 'Reported']
        self.assertTrue(sds)
        self.assertTrue(all(_cls(self.classes, n['source']) in ('SDS', 'EXTERNAL', None) for n in sds))

    def test_no_safety_margin_wording(self):
        for ch in self.S.CHANGES:
            text = json.dumps(ch, ensure_ascii=False).lower()
            self.assertNotIn('safety margin', text)
            self.assertNotIn('safety limit', text)


class ComparisonRules(unittest.TestCase):
    def test_units_converted_before_difference(self):
        r = INV.compare('density', {'value': 990, 'unit': 'kg/m3', 'printed_text': 'Density (20℃), kg/m3 990'},
                        {'value': 0.988, 'unit': 'g/cm³', 'printed_text': 'Density : 0.988 g/cm³ (20 °C)'})
        self.assertEqual(r['comparability'], 'comparable')
        self.assertAlmostEqual(r['abs_diff'], 0.002, places=6)

    def test_different_temperature_not_comparable(self):
        r = INV.compare('density', {'value': 998, 'unit': 'kg/m3', 'test_temperature_c': 20}, {'value': 0.991, 'unit': 'g/cm3', 'test_temperature_c': 15})
        self.assertEqual(r['comparability'], 'not comparable: condition')
        self.assertNotIn('abs_diff', r)

    def test_missing_temperature_pending(self):
        r = INV.compare('density', {'value': 806, 'unit': 'kg/m3'}, {'value': 803.5, 'unit': 'kg/m3'})
        self.assertEqual(r['comparability'], 'comparability unknown')
        self.assertTrue(TH.screen('density', r['comparability'], None, None, '', '').startswith('pending'))

    def test_bound_checked_not_differenced(self):
        r = INV.compare('flash_point', {'value': 220, 'unit': '°C', 'method': 'ASTM D92'},
                        {'value': 180, 'qualifier': '≥', 'value_kind': 'lower bound', 'unit': '°C', 'method': 'ASTM D92'})
        self.assertEqual(r['comparability'], 'bound check only')
        self.assertEqual(r['bound_satisfied'], 'true')
        self.assertNotIn('abs_diff', r)
        self.assertEqual(TH.screen('flash_point', r['comparability'], None, None, 'true', ''), 'ordinary: bound satisfied')

    def test_point_outside_bound_retained(self):
        self.assertEqual(TH.screen('flash_point', 'bound check only', None, None, 'false', ''), 'retain for review: outside bound')

    def test_label_unit_inconsistency_pending(self):
        r = INV.compare('kv100', {'value': 185, 'unit': 'mm2/s', 'printed_text': 'Kinematic Viscosity (100℃), mm2/s 185'},
                        {'value': 185, 'unit': 'mm²/s', 'printed_text': 'Viscosity, dynamic : 185 mm²/s (100 °C)'})
        self.assertEqual(r['comparability'], 'comparability unknown')

    def test_flash_cup_types_not_comparable(self):
        r = INV.compare('flash_point', {'value': 230, 'unit': '°C', 'method': 'ASTM D92'}, {'value': 210, 'unit': '°C', 'method': 'ASTM D93'})
        self.assertTrue(r['comparability'].startswith('not comparable'))

    def test_property_specific_thresholds(self):
        self.assertEqual(TH.screen('kv100', 'comparable', 1.5, 2.0, '', 'false'), 'ordinary: within screening threshold')
        self.assertEqual(TH.screen('kv100', 'comparable', 6.25, 10.0, '', 'false'), 'retain for review: exceeds screening threshold')
        self.assertEqual(TH.screen('flash_point', 'comparable', 10.07, 28.0, '', 'false'), 'retain for review: exceeds screening threshold')
        self.assertEqual(TH.screen('flash_point', 'comparable', 3.1, 7.0, '', 'false'), 'ordinary: within screening threshold')
        self.assertEqual(TH.screen('tbn', 'comparable', 1.85, 2.0, '', 'false'), 'pending: no threshold proposed')

    def test_zero_tds_value_uses_no_relative_difference(self):
        r = INV.compare('pour_point', {'value': 0, 'unit': '°C'}, {'value': -3, 'unit': '°C'})
        self.assertEqual(r['comparability'], 'comparable')
        self.assertIsNone(r['rel_diff_pct'])
        self.assertEqual(TH.screen('pour_point', 'comparable', r['rel_diff_pct'], r['abs_diff'], '', r['within_rounding']),
                         'ordinary: within screening threshold')

    def test_thresholds_not_approved_yet(self):
        self.assertEqual(TH.APPROVAL, 'proposed')


def _vo(value=None, status='Reported', unit='cSt', temp=None, **kw):
    d = dict(value=value, qualifier=None, min=None, max=None, value_kind=None, printed_text=str(value), unit=unit,
             test_temperature_c=temp, method=None, status=status, calculation_note=None,
             source={'file': 'DL2-00000.pdf', 'page': 1, 'revision_date': None})
    d.update(kw)
    return d


def _base_oil(**over):
    f = dict(api_group_chemistry=dict(api_group=_vo('Group III', unit=None), chemistry=_vo('hydrocracked', unit=None)),
             kv40=_vo(19.6, temp=40), kv100=_vo(4.2, temp=100), viscosity_index=_vo(125, unit=None),
             density=_vo(835, unit='kg/m3', temp=15), specific_gravity=_vo(None, status='Missing', unit=None),
             ccs=[_vo(1200, unit='mPa.s', temp=-30)])
    f.update(over)
    return {1: dict(material_class='base_oil', tier=1, fields=f, conflicts=[])}


def _ok(checks):
    return [rid for rid, ok, why, calc in checks if not ok]


class MandatoryRules(unittest.TestCase):
    def test_complete_base_oil_eligible_and_optional_sg_ignored(self):
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil())), [])

    def test_nested_ccs_list_requires_temperature(self):
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(ccs=[_vo(1200, unit='mPa.s', temp=None)]))), ['ccs'])
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(ccs=[]))), ['ccs'])
        two = [_vo(None, status='Missing', unit='mPa.s', temp=-25), _vo(3000, unit='mPa.s', temp=-20)]
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(ccs=two))), [])

    def test_nested_api_group_and_chemistry_both_required(self):
        agc = dict(api_group=_vo('Group II', unit=None), chemistry=_vo(None, status='Missing', unit=None))
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(api_group_chemistry=agc))), ['api_group_chemistry.chemistry'])

    def test_density_needs_reference_temperature(self):
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(density=_vo(835, unit='kg/m3', temp=None)))), ['density'])

    def test_specific_gravity_never_substitutes_density(self):
        b = _base_oil(density=_vo(None, status='Missing', unit='kg/m3', temp=15), specific_gravity=_vo(0.835, unit=None, temp=15.6))
        self.assertEqual(_ok(REQ.base_oil_requirements(b)), ['density'])

    def test_zero_is_a_valid_value(self):
        ok, why = REQ.has_number(_vo(0))
        self.assertTrue(ok, why)
        g = {'general': dict(fields=dict(
            function=dict(primary=_vo('Antiwear (ZDDP)', unit=None)), chemical_family=_vo('zinc dialkyldithiophosphate', unit=None),
            active_content=_vo(80, unit='wt.%'), carrier=dict(identity=_vo('mineral oil', unit=None)), treat_rate=_vo(1.0, unit='wt.%'),
            compatibility_restrictions=dict(base_oil_groups=['Group II'], status='Reported', source={'file': 'DL2-00000.pdf', 'page': 1}),
            function_specific_markers=dict(p=_vo(0, unit='wt.%'), zn=_vo(9.0, unit='wt.%'))))}
        self.assertEqual(_ok(REQ.additive_component_requirements(g)), [])

    def test_one_sided_bound_does_not_satisfy(self):
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(viscosity_index=_vo(121, unit=None, qualifier='minimum', value_kind='minimum')))),
                         ['viscosity_index'])
        self.assertEqual(_ok(REQ.base_oil_requirements(_base_oil(kv100=_vo([4.0, 4.4], temp=100)))), [])

    def test_not_required_label_without_approved_rule_blocks(self):
        b = _base_oil(ccs=[_vo(None, status='Not Required', unit='mPa.s')])
        res = REQ.base_oil_requirements(b)
        self.assertEqual(_ok(res), ['ccs'])
        self.assertIn('without an approved applicability rule', [w for r, ok, w, c in res if r == 'ccs'][0])

    def test_calculated_without_registered_check_rejected(self):
        res = REQ.base_oil_requirements(_base_oil(viscosity_index=_vo(125, unit=None, status='Calculated', calculation_note='from KV40/KV100')))
        self.assertEqual(_ok(res), ['viscosity_index'])
        self.assertTrue([c for r, ok, w, c in res if r == 'viscosity_index'][0])

    def test_calculated_response_checked_for_inputs_arithmetic_and_method(self):
        note = 'ΔKV100 = KV100 at 1% (5.77) - KV100 at 0% (5.23) in 150N = 0.54.'
        e = dict(reference_oil='150N', dose_wt_pct=1, method='ASTM D445',
                 delta_kv100_cst=_vo(0.54, status='Calculated', calculation_note=note))
        self.assertTrue(REQ.check_value(e['delta_kv100_cst'], 'x', calc_check=REQ.calc_delta_kv100(e))[0])
        bad = copy.deepcopy(e); bad['delta_kv100_cst']['value'] = 0.60
        self.assertFalse(REQ.check_value(bad['delta_kv100_cst'], 'x', calc_check=REQ.calc_delta_kv100(bad))[0])
        nometh = copy.deepcopy(e); nometh['method'] = None
        self.assertFalse(REQ.check_value(nometh['delta_kv100_cst'], 'x', calc_check=REQ.calc_delta_kv100(nometh))[0])

    def test_package_without_published_formulation_ineligible(self):
        rows, _, _, _ = BE.build()
        pk = [r for r in rows if r['material_class'] == 'additive_package']
        self.assertTrue(pk)
        self.assertTrue(all('published_formulations' in r['missing_mandatory_properties'] and not r['formulation_eligible'] for r in pk))

    def test_vm_component_needs_subtype_block(self):
        rows, _, _, _ = BE.build()
        rf = next(r for r in rows if r['product_id'] == 'RF6602')
        self.assertFalse(rf['formulation_eligible'])
        self.assertTrue(any(m.startswith('vm.') for m in rf['missing_mandatory_properties']))
        cv = next(r for r in rows if r['product_id'] == 'LUBRIZOL_CV6320')  # non-VM: embedded VM fields are ignored
        self.assertFalse(any(m.startswith('vm.') for m in cv['missing_mandatory_properties']))


class Outputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.path = os.path.join(ROOT, 'reports', 'mandatory_properties')
        with open(os.path.join(cls.path, 'product_eligibility.csv'), encoding='utf-8', newline='') as fh:
            cls.text = fh.read()
        cls.rows = list(csv.DictReader(io.StringIO(cls.text)))

    def test_outputs_up_to_date(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(BE.main(['--check']), 0)

    def test_exact_columns(self):
        self.assertEqual(self.text.splitlines()[0].split(','), BE.COLUMNS)

    def test_one_row_per_product_and_formats(self):
        ids = [r['product_id'] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), len(P.load_products()))
        for r in self.rows:
            self.assertIn(r['material_class'], ('base_oil', 'additive_package', 'additive_component'))
            for k in ('tier1_complete', 'formulation_eligible'):
                self.assertIn(r[k], ('true', 'false'))
            for k in ('missing_mandatory_properties', 'eligibility_reasons', 'calculated_mandatory_properties'):
                self.assertIsInstance(json.loads(r[k]), list)
            self.assertEqual(r['formulation_eligible'] == 'true', json.loads(r['missing_mandatory_properties']) == [])
            if r['formulation_eligible'] == 'false':
                self.assertTrue(json.loads(r['eligibility_reasons']), 'ineligible product without a reason')

    def test_snapshot_hash_independent(self):
        base = ROOT
        lines = []
        for d, _, fs in os.walk(os.path.join(base, 'Products_json')):
            for f in fs:
                if f.endswith('.json'):
                    full = os.path.join(d, f)
                    rel = os.path.relpath(full, base).replace(os.sep, '/')
                    with open(BE.lp(full), 'rb') as fh:
                        lines.append((rel, hashlib.sha256(fh.read()).hexdigest()))
        manifest = ''.join(f'{h}  {r}\n' for r, h in sorted(lines, key=lambda x: x[0].encode('utf-8')))
        want = hashlib.sha256(manifest.encode('utf-8')).hexdigest()
        self.assertEqual({r['source_snapshot_sha256'] for r in self.rows}, {want})

    def test_summary_counts_match_records(self):
        with open(os.path.join(self.path, 'missing_mandatory_properties.md'), encoding='utf-8') as fh:
            md = fh.read()
        for cls in ('base_oil', 'additive_package', 'additive_component'):
            n = sum(1 for r in self.rows if r['material_class'] == cls)
            e = sum(1 for r in self.rows if r['material_class'] == cls and r['formulation_eligible'] == 'true')
            self.assertIn(f'| {cls} | {n} | {e} | {n - e} |', md)
        with open(os.path.join(self.path, 'missing_mandatory_properties.csv'), encoding='utf-8') as fh:
            detail = list(csv.DictReader(fh))
        self.assertEqual(len(detail), sum(len(json.loads(r['missing_mandatory_properties'])) for r in self.rows))


class Safety(unittest.TestCase):
    def test_no_write_on_import(self):
        watched = [os.path.join(ROOT, 'reports'), os.path.join(ROOT, 'Products_json')]

        def snap():
            out = {}
            for w in watched:
                for d, _, fs in os.walk(BE.lp(w)):
                    for f in fs:
                        p = os.path.join(d, f)
                        out[p] = os.stat(p).st_mtime_ns
            return out
        before = snap()
        with redirect_stdout(io.StringIO()):
            for m in ('policy_lib', 'thresholds', 'tds_sds_inventory', 'document_classes', 'source_selection', 'integration_diff',
                      'requirements', 'build_eligibility'):
                importlib.reload(importlib.import_module(m))
        self.assertEqual(before, snap())

    def test_product_json_valid_statuses(self):
        for pid, p in P.load_products().items():
            for rel, d in p['files'].items():
                for path, n in P.value_objects(d.get('fields', {})):
                    self.assertIn(n.get('status'), ALLOWED_STATUS, f'{rel}#{path}')

    def test_only_declared_product_files_changed_since_baseline(self):
        out = subprocess.run(['git', 'diff', '--name-only', BASELINE, '--', 'Products_json'], cwd=ROOT, capture_output=True,
                             text=True, encoding='utf-8')
        if out.returncode != 0:
            self.skipTest('baseline commit not available')
        import source_selection as S
        allowed = {ch['product'] for ch in S.CHANGES} | {u[0] for u in S.OPEN_QUESTION_UPDATES}
        changed = {f.split('/')[-2] for f in out.stdout.splitlines() if f}
        self.assertTrue(changed <= allowed, changed - allowed)

    def test_templates_unchanged_since_baseline(self):
        out = subprocess.run(['git', 'diff', '--name-only', BASELINE, '--', 'json_templates', 'Manual + Data to share.zip'],
                             cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if out.returncode != 0:
            self.skipTest('baseline commit not available')
        self.assertEqual(out.stdout.strip(), '')


if __name__ == '__main__':
    unittest.main()
