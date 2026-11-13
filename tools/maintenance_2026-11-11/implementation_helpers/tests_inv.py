R = 'C:\\Users\\windo\\sf-wsA\\'


def sub(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)


p = R + 'tools\\data_policy\\tests\\test_data_policy.py'
s = open(p, encoding='utf-8').read()
s = sub(s, "class CheckRunner(unittest.TestCase):", '''class ExternalComparisons(unittest.TestCase):
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


class CheckRunner(unittest.TestCase):''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = R + 'tools\\data_policy\\run_checks.py'
s = open(p, encoding='utf-8').read()
s = sub(s, "    ('source_review_status', ['tools/data_policy/source_review_status.py'], 'zero', None),\n",
        "    ('external_comparison_accounting', ['tools/data_policy/external_comparison_accounting.py'], 'zero', None),\n"
        "    ('source_review_status', ['tools/data_policy/source_review_status.py'], 'zero', None),\n")
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = R + 'tools\\data_policy\\external_comparison_accounting.py'
s = open(p, encoding='utf-8').read()
s = sub(s, """', '.join(f'{k.split(" (checked")[0]} {v}' for k, v in sorted(collections.Counter(r['evidence_state'] for r in rows).items())))""",
        """'; '.join(f'{k}: {v}' for k, v in sorted(collections.Counter(r['evidence_state'].split(' (checked')[0] for r in rows).items())))""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
