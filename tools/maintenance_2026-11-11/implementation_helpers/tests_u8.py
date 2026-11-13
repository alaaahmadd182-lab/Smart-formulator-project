R = 'C:\\Users\\windo\\sf-wsA\\'
p = R + 'tools\\data_policy\\tests\\test_data_policy.py'
s = open(p, encoding='utf-8').read()


def sub(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)


s = sub(s, """                self.assertEqual(_cls(self.classes, n['source']), 'TECHNICAL', n['source'])
                if ch['expect'].get('value') is None:  # previously Missing: there is no earlier value to keep
                    continue
""", """                if 'external technical source' in ch.get('change_label', ''):
                    # declared selection of a registered manufacturer source outside the archive; the replaced SDS value
                    # (a range, so expect.value is None) must be kept as an alternate
                    self.assertEqual(_cls(self.classes, n['source']), 'EXTERNAL', n['source'])
                    olds = [a for a in n.get('alternate_entries') or [] if (a.get('source') or {}).get('file') == ch['expect']['source']]
                    self.assertTrue(olds and olds[-1].get('selection_note'), 'replaced SDS value is not kept as an alternate')
                    continue
                self.assertEqual(_cls(self.classes, n['source']), 'TECHNICAL', n['source'])
                if ch['expect'].get('value') is None:  # previously Missing: there is no earlier value to keep
                    continue
""")

s = sub(s, """class CheckRunner(unittest.TestCase):""", '''class TechnicalSelectionKeepsDisagreement(unittest.TestCase):
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
        self.assertEqual(REQ.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.3')


class CheckRunner(unittest.TestCase):''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
