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
import collections, copy, csv, hashlib, importlib, io, json, os, subprocess, sys, unittest
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
                if 'SDS fallback' in ch.get('change_label', ''):
                    # declared SDS fallback: the value must come from an SDS page and no technical alternate may exist
                    self.assertEqual(_cls(self.classes, n['source']), 'SDS', n['source'])
                    continue
                if 'external technical source' in ch.get('change_label', ''):
                    # declared selection of a registered manufacturer source outside the archive; the replaced SDS value
                    # (a range, so expect.value is None) must be kept as an alternate
                    self.assertEqual(_cls(self.classes, n['source']), 'EXTERNAL', n['source'])
                    olds = [a for a in n.get('alternate_entries') or [] if (a.get('source') or {}).get('file') == ch['expect']['source']]
                    self.assertTrue(olds and olds[-1].get('selection_note'), 'replaced SDS value is not kept as an alternate')
                    continue
                self.assertEqual(_cls(self.classes, n['source']), 'TECHNICAL', n['source'])
                if ch['expect'].get('value') is None:  # previously Missing: there is no earlier value to keep
                    continue
                olds = [a for a in n.get('alternate_entries') or [] if a.get('value') == ch['expect']['value']]
                self.assertTrue(olds, 'replaced value is not kept as an alternate')
                self.assertEqual(olds[-1]['source']['file'], ch['expect']['source'])
                self.assertTrue(olds[-1].get('selection_note'))

    def test_no_undeclared_sds_selection_with_technical_alternate(self):
        declared = {(p, f.strip()) for p, fs, _ in self.S.EXCEPTIONS + self.S.PENDING for f in fs.split(',')}
        declared |= {(p, f) for p, f, _ in self.S.PENDING_FIELDS + self.S.SDS_FALLBACK_FIELDS}
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

    def test_technical_range_selected_without_conversion(self):
        for pid in ('FORMOSA_150N_GII_PLUS', 'FORMOSA_500N_GII'):
            n = next(d for d in self.prods[pid]['files'].values() if d.get('tier') == 1)['fields']['kv100']
            self.assertIsNone(n['value'], 'a specification range must not be converted to a single value')
            self.assertEqual(n['value_kind'], 'range')
            self.assertEqual(_cls(self.classes, n['source']), 'TECHNICAL')
            alt = n['alternate_entries'][-1]
            self.assertEqual(_cls(self.classes, alt['source']), 'SDS')
            self.assertIsNone(alt['min'], 'the SDS alternate must not carry the specification range')

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
        self.assertEqual(TH.screen('flash_point', r['comparability'], None, None, 'true', ''), TH.BOUND_OK)
        self.assertIn('not evidence of agreement', TH.BOUND_OK)

    def test_point_outside_bound_retained(self):
        self.assertEqual(TH.screen('flash_point', 'bound check only', None, None, 'false', ''), TH.BOUND_BAD)

    def test_label_unit_inconsistency_pending(self):
        r = INV.compare('kv100', {'value': 185, 'unit': 'mm2/s', 'printed_text': 'Kinematic Viscosity (100℃), mm2/s 185'},
                        {'value': 185, 'unit': 'mm²/s', 'printed_text': 'Viscosity, dynamic : 185 mm²/s (100 °C)'})
        self.assertEqual(r['comparability'], 'comparability unknown')

    def test_flash_cup_types_not_comparable(self):
        r = INV.compare('flash_point', {'value': 230, 'unit': '°C', 'method': 'ASTM D92'}, {'value': 210, 'unit': '°C', 'method': 'ASTM D93'})
        self.assertTrue(r['comparability'].startswith('not comparable'))

    def test_property_specific_thresholds(self):
        self.assertEqual(TH.screen('kv100', 'comparable', 1.5, 2.0, '', 'false'), TH.BELOW)
        self.assertEqual(TH.screen('kv100', 'comparable', 6.25, 10.0, '', 'false'), TH.ABOVE)
        self.assertEqual(TH.screen('kv100', 'comparable', 3.0, 3.0, '', 'false'), TH.ABOVE, 'at the threshold is retained for review')
        self.assertEqual(TH.screen('flash_point', 'comparable', 10.07, 28.0, '', 'false'), TH.ABOVE)
        self.assertEqual(TH.screen('flash_point', 'comparable', 3.1, 7.0, '', 'false'), TH.BELOW)
        self.assertEqual(TH.screen('kv100', 'comparable', 1.5, 2.0, '', 'true'), TH.ROUNDING)
        self.assertNotIn('ordinary', ' '.join([TH.BELOW, TH.ABOVE, TH.BOUND_OK, TH.BOUND_BAD]))
        self.assertTrue(all(r['basis'].startswith(('empirical', 'no threshold')) for r in TH.RULES.values()))
        self.assertEqual(TH.screen('kv100', 'comparable', 4.0, 0.2, '', 'false', threshold=5.0), TH.BELOW)
        self.assertEqual(TH.screen('tbn', 'comparable', 1.85, 2.0, '', 'false'), 'pending: no threshold proposed')

    def test_flash_point_needs_cup_type_on_both_sides(self):
        r = INV.compare('flash_point', {'value': 265, 'unit': '°C', 'printed_text': 'Flash Point (COC) 265'}, {'value': 255, 'unit': '°C'})
        self.assertEqual(r['comparability'], 'comparability unknown')
        self.assertNotIn('abs_diff', r)

    def test_zero_tds_value_uses_no_relative_difference(self):
        r = INV.compare('pour_point', {'value': 0, 'unit': '°C'}, {'value': -3, 'unit': '°C'})
        self.assertEqual(r['comparability'], 'comparable')
        self.assertIsNone(r['rel_diff_pct'])
        # absolute rule only: |0 - (-3)| = 3 °C is at the proposed threshold, so it is retained for review
        self.assertEqual(TH.screen('pour_point', 'comparable', r['rel_diff_pct'], r['abs_diff'], '', r['within_rounding']),
                         TH.ABOVE)
        r = INV.compare('pour_point', {'value': 0, 'unit': '°C'}, {'value': 0, 'unit': '°C'})
        self.assertEqual(TH.screen('pour_point', 'comparable', r['rel_diff_pct'], r['abs_diff'], '', r['within_rounding']),
                         TH.ROUNDING)

    def test_thresholds_not_approved_yet(self):
        self.assertEqual(TH.APPROVAL, 'proposed')


# The mandatory-requirement rules (valid and invalid inputs, categories, calculations) are tested in
# tools/mandatory_properties/tests/test_requirements.py.


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

    def test_package_without_published_formulation_ineligible(self):
        pk = [r for r in self.rows if r['material_class'] == 'additive_package']
        self.assertTrue(pk)
        self.assertTrue(all('published_formulations' in json.loads(r['missing_mandatory_properties'])
                            and r['formulation_eligible'] == 'false' for r in pk))

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
            self.assertEqual(r['tier1_complete'], r['formulation_eligible'], 'version .3: both mean all mandatory Tier 1 satisfied')
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
            c = sum(1 for r in self.rows if r['material_class'] == cls and r['tier1_complete'] == 'true')
            e = sum(1 for r in self.rows if r['material_class'] == cls and r['formulation_eligible'] == 'true')
            self.assertEqual(c, e, 'tier1_complete and formulation_eligible have the same meaning')
            with open(os.path.join(self.path, 'documentation_coverage.csv'), encoding='utf-8') as fh2:
                d = sum(1 for r in csv.DictReader(fh2) if r['material_class'] == cls and r['all_blocking_documented'] == 'true')
            self.assertIn(f'| {cls} | {n} | {c} | {d} |', md)
        with open(os.path.join(self.path, 'requirement_outcomes.csv'), encoding='utf-8') as fh:
            outcomes = list(csv.DictReader(fh))
        with open(os.path.join(self.path, 'missing_mandatory_properties.csv'), encoding='utf-8') as fh:
            unmet = list(csv.DictReader(fh))
        self.assertEqual(len(unmet), sum(1 for o in outcomes if o['category'] not in ('met', 'not_applicable_approved_rule')))
        blocking_unmet = collections.Counter(o['product_id'] for o in unmet if o['blocking'] == 'true')
        for r in self.rows:
            self.assertEqual(len(json.loads(r['missing_mandatory_properties'])), blocking_unmet[r['product_id']], r['product_id'])
        tab = collections.Counter((o['material_class'], o['requirement'], o['category']) for o in outcomes if o['blocking'] == 'true')
        for (cls, rid, cat), k in tab.items():
            line = next(x for x in md.splitlines() if x.startswith(f'| {cls} | `{rid}` |'))
            cells = [x.strip() for x in line.strip('|').split('|')][2:]
            self.assertEqual(cells[REQ.CATEGORIES.index(cat)], str(k), (cls, rid, cat))


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
                      'requirements', 'build_eligibility', 'source_coverage_ledger', 'treat_rate_basis_scan', 'verify_preserved',
                      'lead_review', 'association_review', 'co_component_evidence_scan'):
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
        allowed = ({ch['product'] for ch in S.CHANGES} | {u[0] for u in S.OPEN_QUESTION_UPDATES} | {c['product'] for c in S.LIST_FILLS}
                   | {c['product'] for c in S.QUALIFIER_FIXES} | {c[0] for c in S.CONFLICT_ADDS})
        changed = {f.split('/')[-2] for f in out.stdout.splitlines() if f}
        self.assertTrue(changed <= allowed, changed - allowed)

    def test_templates_unchanged_since_baseline(self):
        out = subprocess.run(['git', 'diff', '--name-only', BASELINE, '--', 'json_templates', 'Manual + Data to share.zip'],
                             cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if out.returncode != 0:
            self.skipTest('baseline commit not available')
        self.assertEqual(out.stdout.strip(), '')



class EvidenceReview(unittest.TestCase):
    """Revision 3: every lead case and name-match association has a recorded outcome; corrections are evidence-backed."""

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(P.REPORTS, 'data_policy', 'lead_review.csv'), encoding='utf-8') as fh:
            cls.leads = list(csv.DictReader(fh))
        with open(os.path.join(P.REPORTS, 'data_policy', 'name_match_review.csv'), encoding='utf-8') as fh:
            cls.assoc = list(csv.DictReader(fh))

    def test_every_lead_case_reviewed(self):
        self.assertGreaterEqual(len(self.leads), 352)
        self.assertEqual([r for r in self.leads if r['outcome'] == 'not_reviewed'], [])
        import lead_review as LR
        self.assertTrue(all(r['outcome'] in LR.OUTCOMES[:-1] for r in self.leads))
        self.assertEqual(len({(r['product'], r['property']) for r in self.leads}), len(self.leads), 'deduplicated by product x property')

    def test_usable_evidence_has_a_change_and_printed_value(self):
        for r in self.leads:
            if r['outcome'] == 'usable_evidence':
                self.assertTrue(r['printed'] and r['change'] and r['change'] != 'none', (r['product'], r['property']))

    def test_every_association_reviewed_and_wrong_ones_excluded(self):
        self.assertEqual([r for r in self.assoc if r['verdict'] == 'not_reviewed'], [])
        wrong = {(r['product'], r['document']) for r in self.assoc if r['usable_as_evidence'] == 'false'}
        self.assertIn(('NYNAS_BASE_STOCK_20', 'DL2-13379.pdf'), wrong)
        self.assertIn(('S_OIL_SUPER_S_8', 'DL2-11240.pdf'), wrong)
        with open(os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'), encoding='utf-8') as fh:
            for row in csv.DictReader(fh):
                for pid, doc in wrong:
                    if row['product'] == pid:
                        self.assertNotIn(doc + ' (name match', row['documents_examined'])

    def test_reviewed_comparisons_reach_the_inventory(self):
        with open(os.path.join(DP, 'lead_review_decisions.json'), encoding='utf-8') as fh:
            comps = json.load(fh)['comparisons']
        with open(os.path.join(P.REPORTS, 'data_policy', 'tds_sds_comparisons.csv'), encoding='utf-8') as fh:
            inv = list(csv.DictReader(fh))
        got = {(r['product'], r['property'], r['sds_file']) for r in inv}
        for c in comps:
            self.assertIn((c['product'], c['property'], c['sds']['file']), got)

    def test_ergon_qualifier_corrected_and_previous_kept(self):
        prods = P.load_products()
        for pid, lo in (('ERGON_HYGOLD_5000BS', 80), ('ERGON_HYGOLD_P70N', 60)):
            n = next(d for d in prods[pid]['files'].values() if d.get('tier') == 1)['fields']['viscosity_index']
            self.assertIsNone(n['qualifier'])
            self.assertEqual((n['value'], n['min'], n['qualifier_previous']), (81, lo, 'minimum'))
            self.assertEqual(REQ.representation(n)[0], 'point')

    def test_fills_cite_their_page_and_keep_sds_alternates(self):
        prods = P.load_products()
        f = next(d for d in prods['CHEVRON_SYNFLUID_MPAO_65']['files'].values() if d.get('tier') == 2)['fields']['flash_point']
        self.assertEqual((f['value'], f['qualifier'], f['source']['file']), (266, '>', 'DL2-11910.pdf'))
        self.assertTrue(any(a['source']['file'] == 'DL2-11908.PDF' and a['value'] == 270 for a in f['alternate_entries']))
        c = next(d for d in prods['PETRONAS_ETRO_6']['files'].values() if d.get('tier') == 1)['fields']['ccs']
        self.assertEqual([(x['value'], x['test_temperature_c']) for x in c], [(2088, -25), (3977, -30), (7422, -35)])
        k = next(d for d in prods['CHEVRON_GROUP_II_600R']['files'].values() if d.get('tier') == 1)['fields']['kv40']
        self.assertEqual((k['value'], k['min'], k['qualifier']), (None, 100, 'minimum'))

    def test_new_conflicts_recorded_unresolved(self):
        prods = P.load_products()
        for pid, cid in (('PETRONAS_ETRO_4', 'EVR-2026-11-10-ETRO4'), ('LUBRIZOL_CV2301', 'EVR-2026-11-10-CV2301')):
            hits = [c for d in prods[pid]['files'].values() for c in d.get('conflicts') or [] if isinstance(c, dict) and c.get('id') == cid]
            self.assertEqual(len(hits), 1)
            self.assertIs(hits[0]['resolved'], False)
            self.assertGreaterEqual(len(hits[0]['values']), 2)

    def test_formosa_identity_pending_not_fallback(self):
        import source_selection as S
        pend = {(p, f) for p, f, _ in S.PENDING_FIELDS}
        for pid in ('FORMOSA_150N_GII_PLUS', 'FORMOSA_500N_GII'):
            self.assertIn((pid, 'kv40'), pend)
            self.assertNotIn((pid, 'kv40'), {(p, f) for p, f, _ in S.SDS_FALLBACK_FIELDS})

    def test_preserved_and_evidence_bytes(self):
        import verify_preserved as V
        with redirect_stdout(io.StringIO()):
            self.assertEqual(V.main([]), 0)

    def test_association_universe_frozen_and_counted(self):
        verdicts = collections.Counter(r['verdict'] for r in self.assoc)
        self.assertEqual(sum(verdicts.values()), len({(r['product'], r['document']) for r in self.assoc}))
        self.assertEqual(set(verdicts) - {'same_product', 'same_document_copy', 'other_product', 'family_document', 'unresolved'}, set())
        cited = [r for r in self.assoc if r['now_cited'] == 'true']
        self.assertTrue(all(r['usable_as_evidence'] == 'true' for r in cited), 'a cited association must be a reviewed same-product one')

    def test_comparison_cases_are_usable_lead_cases(self):
        with open(os.path.join(DP, 'lead_review_decisions.json'), encoding='utf-8') as fh:
            comps = {(c['product'], c['property']) for c in json.load(fh)['comparisons']}
        cases = {(r['product'], r['property']): r['outcome'] for r in self.leads}
        for k in comps:
            self.assertEqual(cases.get(k), 'usable_evidence', k)


class ExternalReview(unittest.TestCase):
    """Review of 2026-11-11: every external-source value has an outcome; unavailable sources are never called confirmed."""

    @classmethod
    def setUpClass(cls):
        import external_review as ER
        cls.ER = ER
        with redirect_stdout(io.StringIO()):
            cls.rc = ER.main([])
        with open(os.path.join(P.REPORTS, 'data_policy', 'external_review.csv'), encoding='utf-8') as fh:
            cls.rows = list(csv.DictReader(fh))
        with open(ER.DECISIONS, encoding='utf-8') as fh:
            cls.dec = json.load(fh)

    def test_runs_clean_and_covers_every_external_selection(self):
        self.assertEqual(self.rc, 0)
        with open(os.path.join(P.REPORTS, 'data_policy', 'source_coverage_ledger.csv'), encoding='utf-8') as fh:
            ext = {(r['product'], r['property']) for r in csv.DictReader(fh) if r['selection_status'] == 'external_selected'}
        self.assertEqual(ext, {(r['product'], r['property']) for r in self.rows if r['kind'] == 'external_selected'})

    def test_unobtained_sources_are_not_confirmed(self):
        unobtained = {k for k, e in self.dec['evidence'].items() if not e.get('path') and not e.get('registry_sha256_match')}
        for c in self.dec['cases']:
            if set(c['evidence']) <= unobtained:
                self.assertEqual(c['outcome'], 'inconclusive_source_unavailable', (c['product'], c['property']))
        self.assertEqual({c['outcome'] for c in self.dec['cases'] if c['product'] == 'AFTON_HITEC_8788B'}, {'inconclusive_source_unavailable'})

    def test_each_source_assessed_separately(self):
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
        # a distributor-issued document is labelled as such; the aramcoULTRA 8 page names the exact grade, and the
        # separate merge question ID-01 is neither resolved nor used as a restriction on that source
        self.assertEqual(self.dec['evidence']['mogo_flyer_2025']['authority'], 'distributor_issued')
        self.assertEqual({r['identity_status'] for r in self.rows if r['product'] == 'S_OIL_ARAMCO_ULTRA_8'}, {'exact_grade_named_merge_question_separate'})
        self.assertNotIn('policy decision', json.dumps(self.dec))

    def test_stale_decision_is_an_error(self):
        c = self.dec['cases'][4]
        node = copy.deepcopy(self.ER.field(P.load_products(), c['product'], c['property']))
        self.assertTrue(self.ER.matches(node, c['expect']))
        if isinstance(node, dict):
            node['value'] = 'changed'
        else:
            node[0]['value'] = -1
        self.assertFalse(self.ER.matches(node, c['expect']))

    def test_8788b_stays_pending(self):
        import source_selection as S
        self.assertTrue(any(p == 'AFTON_HITEC_8788B' for p, *_ in S.PENDING))

    def test_conflicts_found_recorded_unresolved(self):
        prods = P.load_products()
        for pid, cid in (('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-noack'), ('ARAMCO_LUBEREF_PRIMA_230', 'EVR-2026-11-11-230-density-external')):
            hits = [c for d in prods[pid]['files'].values() for c in d.get('conflicts') or [] if isinstance(c, dict) and c.get('id') == cid]
            self.assertEqual(len(hits), 1, cid)
            self.assertIs(hits[0]['resolved'], False)
        # the aramcoULTRA 8 KV40 disagreement was already a conflict (2026-10 audit); it is not recorded twice
        u8 = [c for d in prods['S_OIL_ARAMCO_ULTRA_8']['files'].values() for c in d.get('conflicts') or []
              if isinstance(c, dict) and 'kv40' in str(c.get('field'))]
        self.assertEqual(len(u8), 1)

    def test_review_states_partition_the_ledger(self):
        import source_review_status as RS
        with redirect_stdout(io.StringIO()):
            self.assertEqual(RS.main(), 0)
        with open(os.path.join(P.REPORTS, 'data_policy', 'source_review_status.csv'), encoding='utf-8') as fh:
            st = list(csv.DictReader(fh))
        self.assertTrue(all(r['review_state'] in RS.STATES for r in st))
        for r in st:
            if r['external_outcome'] == 'inconclusive_source_unavailable':
                self.assertEqual(r['review_state'], 'evidence_unavailable')


class TechnicalSelectionKeepsDisagreement(unittest.TestCase):
    """aramcoULTRA 8 (2026-11-11): selecting the technical-source value keeps the SDS value as an alternate with its
    provenance, and never resolves, removes or duplicates the recorded disagreement."""

    SDS = {'kv40': (42.0, 55.0, '42.0 - 55.0 cSt @ 40°C (ASTM D 445)'), 'kv100': (7.0, 7.5, '7.0 - 7.5 cSt @ 100°C (ASTM D 445)'),
           'flash_point': (240, 260, '240 ~ 260°C (ASTM D 92)')}

    @classmethod
    def setUpClass(cls):
        import source_selection as S
        import verify_soil_table as V
        cls.S, cls.V = S, V
        cls.prods = P.load_products()
        cls.files = cls.prods['S_OIL_ARAMCO_ULTRA_8']['files']

    def _field(self, prop):
        return next(d['fields'][prop] for d in self.files.values() if prop in d.get('fields', {}))

    def test_selected_values_are_the_saved_manufacturer_table_cells(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(self.V.main(), 0)
        for path, sha in self.V.COPIES.items():
            got, cap, header, rows = self.V.read_table(path)
            self.assertEqual(got, sha)
            self.assertTrue(cap.startswith('Typical Properties of aramcoULTRA Base Oil'))
            j = header.index('aramcoULTRA 8')
            for prop, (label, astm, printed, *_rest) in self.V.EXPECTED.items():
                self.assertEqual((rows[label][1], rows[label][j]), (astm, printed), prop)

    def test_selection_and_exact_provenance(self):
        for prop, (label, astm, printed, value, unit, temp, method) in self.V.EXPECTED.items():
            n = self._field(prop)
            self.assertEqual((n['value'], n['unit'], n['test_temperature_c'], n['method'], n['value_kind'], n['qualifier'], n['status']),
                             (value, unit, temp, method, 'typical', None, 'Reported'), prop)
            self.assertEqual(n['printed_text'], f'{label}: {printed}')
            self.assertEqual(n['source'], {'file': self.V.URL, 'page': None, 'revision_date': None}, 'the edition date stays unknown')
            for sha in self.V.COPIES.values():
                self.assertIn(sha, n['calculation_note'])
            self.assertIn('edition date is unknown', n['calculation_note'])
        self.assertEqual(self._field('flash_point')['flash_method'], 'COC')

    def test_sds_value_kept_as_alternate_with_provenance(self):
        for prop, (lo, hi, printed) in self.SDS.items():
            alts = [a for a in self._field(prop)['alternate_entries'] if a['source']['file'] == 'DL2-14611.pdf']
            self.assertEqual(len(alts), 1, prop)
            a = alts[0]
            self.assertEqual((a['value'], a['min'], a['max'], a['value_kind'], a['printed_text'], a['status']), (None, lo, hi, 'range', printed, 'Reported'))
            self.assertEqual(a['source'], {'file': 'DL2-14611.pdf', 'page': 2, 'revision_date': '2018-09-07'})
            self.assertIn('Not judged erroneous', a['selection_note'])

    def test_disagreement_is_not_resolved_removed_or_duplicated(self):
        t1 = next(d for d in self.files.values() if d.get('tier') == 1)
        kv40 = [c for c in t1['conflicts'] if isinstance(c, dict) and 'kv40' in str(c.get('field'))]
        self.assertEqual(len(kv40), 1, 'exactly the existing conflict: not removed, not duplicated')
        c = kv40[0]
        self.assertIsNot(c.get('resolved'), True)
        self.assertFalse(c.get('final_resolution'))
        self.assertEqual({v['file'] for v in c['values']}, {'DL2-14611.pdf', self.V.URL}, 'both sides stay recorded')
        self.assertIn('Not resolved.]', c['note'])
        self.assertIn('not resolved (2026-10 audit)', c['note'], 'the historical note text is kept')
        # the selected typical really is outside the kept SDS range: the selection did not hide the disagreement
        n = self._field('kv40')
        a = next(x for x in n['alternate_entries'] if x['source']['file'] == 'DL2-14611.pdf')
        self.assertLess(n['value'], a['min'])

    def test_selection_mechanism_never_marks_a_conflict_resolved(self):
        # apply() on a copy of the record as it was before the selection: the alternate is created and the conflict untouched
        base = subprocess.run(['git', 'show', '43e7f8b:Products_json/Base_oils_json/S_OIL/S_OIL_ARAMCO_ULTRA_8/S_OIL_ARAMCO_ULTRA_8_tier1.json'],
                              cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if base.returncode != 0:
            self.skipTest('revision-3 commit not available')
        prods = copy.deepcopy(self.prods)
        rel = next(r for r, d in prods['S_OIL_ARAMCO_ULTRA_8']['files'].items() if d.get('tier') == 1)
        before = json.loads(base.stdout)
        prods['S_OIL_ARAMCO_ULTRA_8']['files'][rel] = copy.deepcopy(before)
        self.assertIsNone(before['fields']['kv40']['value'])
        spec = importlib.util.spec_from_file_location('integrate_products', os.path.join(ROOT, 'integrate_products.py'))
        integ = importlib.util.module_from_spec(spec); spec.loader.exec_module(integ)
        changed, errors, _log = self.S.apply(prods, integ)
        self.assertEqual(errors, [])
        after = prods['S_OIL_ARAMCO_ULTRA_8']['files'][rel]
        self.assertEqual(after['fields']['kv40']['value'], 41.1)
        self.assertEqual(after['fields']['kv40']['alternate_entries'][-1]['min'], 42.0)
        self.assertEqual(len(after['conflicts']), len(before['conflicts']))
        for old, new in zip(before['conflicts'], after['conflicts']):
            self.assertEqual({k: v for k, v in new.items() if k != 'note'}, {k: v for k, v in old.items() if k != 'note'})
            self.assertTrue(new['note'].startswith(old['note']))

    def test_no_longer_pending_and_other_state_preserved(self):
        self.assertFalse([p for p, *_ in self.S.PENDING if p == 'S_OIL_ARAMCO_ULTRA_8'])
        self.assertFalse([p for p, *_ in self.S.PENDING_FIELDS if p == 'S_OIL_ARAMCO_ULTRA_8'])
        self.assertIn('S_OIL_ULTRA_S_8', self.prods, 'both product records stay separate')
        out = subprocess.run(['git', 'diff', '--name-only', '43e7f8b', '--', 'Products_json/Base_oils_json/S_OIL/S_OIL_ULTRA_S_8',
                              'reconciliation'], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        if out.returncode == 0:
            self.assertEqual(out.stdout.strip(), '', 'the Ultra-S 8 record and the identity review (ID-01) are unchanged')
        self.assertEqual(TH.APPROVAL, 'proposed')
        self.assertEqual(REQ.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.6')


class ExternalComparisons(unittest.TestCase):
    """The comparison inventory includes registered external technical sources; every external-selected value is
    accounted for; unavailable evidence is never treated as verified; no duplicate pairs; point vs range is a check."""

    U8 = 'S_OIL_ARAMCO_ULTRA_8'
    SOIL = 'https://www.s-oil.com/en/energy/LubeBaseOil.aspx'

    @classmethod
    def setUpClass(cls):
        import external_comparison_accounting as ACC
        cls.ACC = ACC
        with redirect_stdout(io.StringIO()):
            cls.acc_rc = ACC.main()

        def read(name):
            with open(os.path.join(P.REPORTS, 'data_policy', name), encoding='utf-8') as fh:
                return list(csv.DictReader(fh))
        cls.inv, cls.acc, cls.ledger = read('tds_sds_comparisons.csv'), read('external_comparison_accounting.csv'), read('source_coverage_ledger.csv')
        cls.reg, cls.state = INV.load_external()

    def _row(self, prop):
        hits = [r for r in self.inv if r['product'] == self.U8 and r['property'] == prop and r['tds_file'] == self.SOIL]
        self.assertEqual(len(hits), 1, f'{prop}: exactly one pair')
        return hits[0]

    # ---- external-source inclusion
    def test_external_technical_pairs_are_in_the_inventory(self):
        ext = [r for r in self.inv if r['tds_source'] == 'external']
        self.assertGreaterEqual({(r['product'], r['property']) for r in ext},
                                {(self.U8, 'kv40'), (self.U8, 'kv100'), (self.U8, 'flash_point'), ('RICHFUL_RF6078', 'density')})
        self.assertGreater(len({r['product'] for r in ext}), 1, 'not restricted to aramcoULTRA 8')
        for r in ext:
            self.assertEqual(INV.external_class(r['tds_file'], self.reg), 'TECHNICAL', 'only registered technical URLs are paired')
            self.assertTrue(r['external_evidence'])
            self.assertEqual(r['sds_source'], 'archive')

    def test_pair_keeps_identity_conditions_and_provenance(self):
        r = self._row('kv40')
        self.assertEqual((r['tds_value'], r['tds_value_kind'], r['tds_unit'], r['tds_temp'], r['tds_method']), ('41.1', 'typical', 'cst', '40.0', 'ASTMD445'))
        self.assertEqual((r['sds_file'], r['sds_page'], r['sds_value_kind'], r['sds_unit'], r['sds_temp'], r['sds_method'], r['sds_revision_date']),
                         ('DL2-14611.pdf', '2', 'range', 'cst', '40.0', 'ASTMD445', '2018-09-07'))
        self.assertEqual(r['tds_revision_date'], '', 'the edition date of the page stays unknown')
        self.assertEqual(r['external_evidence'], 'copy read in the external review')

    def test_unregistered_url_and_external_sds_are_not_technical(self):
        self.assertIsNone(INV.external_class('https://example.com/not-registered.pdf', self.reg))
        self.assertEqual(INV.external_class('https://luberefapp.s3-accelerate.amazonaws.com/documents/prima230-1664376579.pdf', self.reg), 'SDS')

    # ---- point versus range
    def test_ultra8_point_versus_range(self):
        k40, k100, fp = self._row('kv40'), self._row('kv100'), self._row('flash_point')
        for r in (k40, k100, fp):
            self.assertEqual(r['comparability'], 'bound check only')
            self.assertEqual((r['abs_diff'], r['rel_diff_pct'], r['within_rounding']), ('', '', ''), 'a point is checked against a range, not differenced')
        self.assertEqual(k40['bound_satisfied'], 'false')
        self.assertIn('retain for review', k40['proposed_screen'])
        for r in (k100, fp):
            self.assertEqual(r['bound_satisfied'], 'true')
            self.assertIn('not evidence of agreement', r['proposed_screen'])

    def test_point_versus_range_rule(self):
        pt = dict(value=41.1, unit='cSt', test_temperature_c=40, method='ASTM D445', value_kind='typical')
        rng = dict(value=None, min=42.0, max=55.0, value_kind='range', unit='cSt', test_temperature_c=40, method='ASTM D445')
        r = INV.compare('kv40', pt, rng)
        self.assertEqual((r['comparability'], r['bound_satisfied']), ('bound check only', 'false'))
        self.assertNotIn('abs_diff', r)
        self.assertEqual(INV.compare('kv40', dict(pt, value=45.0), rng)['bound_satisfied'], 'true')

    # ---- duplicates
    def test_no_duplicate_pairs(self):
        keys = [(r['product'], r['property'], r['tds_file'], r['tds_value'], r['sds_file'], r['sds_value']) for r in self.inv]
        self.assertEqual(len(keys), len(set(keys)))
        # the two saved copies of the S-OIL page are one source: one URL, one state, one row per property
        with open(INV.EXTERNAL_DECISIONS, encoding='utf-8') as fh:
            ev = json.load(fh)['evidence']
        self.assertEqual(ev['soil_page_wayback']['registry_url'], ev['soil_page_live']['registry_url'])
        # KV40 is recorded in conflicts[] and as an alternate entry: one inventory row, one conflict record
        o = self._row('kv40')['origin']
        self.assertIn('conflicts[]', o); self.assertIn('alternate entry', o)
        t1 = next(d for d in P.load_products()[self.U8]['files'].values() if d.get('tier') == 1)
        self.assertEqual(len([c for c in t1['conflicts'] if 'kv40' in str(c.get('field'))]), 1)

    # ---- unavailable evidence
    def test_unobtained_source_is_never_verified(self):
        afton = next(u for u in self.reg if 'HiTEC-12204L' in u)
        self.assertEqual(INV.external_state(afton, self.reg, self.state), INV.NOT_OBTAINED)
        r = INV.apply_evidence_state(dict(comparability='comparable', reason='', abs_diff=0.0, rel_diff_pct=0.0, within_rounding='true'), [INV.NOT_OBTAINED, ''])
        self.assertEqual(r['comparability'], 'comparability unknown')
        self.assertNotIn('abs_diff', r); self.assertNotIn('within_rounding', r)
        self.assertIn('pending', TH.screen('kv100', r['comparability'], None, None, '', ''))
        self.assertFalse([x for x in self.inv if INV.NOT_OBTAINED in x['external_evidence'] and x['comparability'] != 'comparability unknown'])
        # accounting: an unobtained source is unresolved even if pairs exist, and never 'paired'
        n = dict(value=190, status='Reported')
        st, _ = self.ACC.decide(n, afton, 'kv100', 'TECHNICAL', INV.NOT_OBTAINED, None, [dict(sds_file='x', sds_page='1', comparability='comparable')], [], None, None)
        self.assertEqual(st, 'unresolved_external_source_not_obtained')
        for x in self.acc:
            if x['evidence_state'] == INV.NOT_OBTAINED:
                self.assertEqual(x['comparison_status'], 'unresolved_external_source_not_obtained', (x['product'], x['field']))

    def test_every_external_selected_value_is_accounted_for(self):
        self.assertEqual(self.acc_rc, 0)
        want = {(r['product'], r['property']) for r in self.ledger if r['selection_status'] == 'external_selected'}
        got = {(r['product'], r['property']) for r in self.acc if r['ledger_selection_status'] == 'external_selected'}
        self.assertEqual(want, got)
        for x in self.acc:
            self.assertIn(x['comparison_status'], self.ACC.STATUSES)
            self.assertNotEqual(x['comparison_status'], 'unresolved_not_reviewed')
            self.assertTrue(x['reason'])
            self.assertEqual(x['comparison_status'] == 'paired', int(x['inventory_pairs']) > 0 and x['evidence_state'] != INV.NOT_OBTAINED
                             and x['external_class'] == 'TECHNICAL', (x['product'], x['field']))

    def test_selection_and_disagreement_stay_separate(self):
        # the inventory records the relation only: the selected values and the conflict state are what the selection tests fixed
        t1 = next(d for d in P.load_products()[self.U8]['files'].values() if d.get('tier') == 1)
        self.assertEqual(t1['fields']['kv40']['value'], 41.1)
        self.assertIsNot(next(c for c in t1['conflicts'] if 'kv40' in str(c.get('field'))).get('resolved'), True)
        self.assertEqual(TH.APPROVAL, 'proposed')


class CheckRunner(unittest.TestCase):
    """The saved check runner records each command's own return code."""

    def test_return_codes_are_not_masked(self):
        import run_checks as RC
        bad = subprocess.run([sys.executable, '-c', 'import sys; print("x"); sys.exit(3)'], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 3)
        self.assertTrue(all(e in ('zero', 'by_design_nonzero') for _, _, e, _ in RC.STEPS))
        self.assertEqual([n for n, _, e, _ in RC.STEPS if e == 'by_design_nonzero'], ['verify_revision_v5'])


if __name__ == '__main__':
    unittest.main()
