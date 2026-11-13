import os
os.chdir(r'C:\Users\windo\sf-wsA')

p = 'tools/mandatory_properties/tests/test_requirements.py'
s = open(p, encoding='utf-8').read()
rep = [("""        complete, eligible = R.summarize(R.base_oil_requirements(base_oil(viscosity_index=vo(121, qualifier='minimum', unit=None))))
        self.assertEqual((complete, eligible), (True, False))""",
        """        outs = R.base_oil_requirements(base_oil(viscosity_index=vo(121, qualifier='minimum', unit=None)))
        # interface meaning (version .3): documented but not satisfied is NOT Tier 1 complete
        self.assertEqual(R.summarize(outs), (False, False))
        self.assertTrue(R.documentation_status(outs))"""),
       ("""        self.assertEqual(cats(outs)['kv40'], R.SEL)
        self.assertEqual(R.summarize(outs), (True, False))""",
        """        self.assertEqual(cats(outs)['kv40'], R.SEL)
        self.assertEqual(R.summarize(outs), (False, False))
        self.assertTrue(R.documentation_status(outs))"""),
       ("""        self.assertEqual(cats(outs)['ccs'], R.APPL)
        self.assertEqual(R.summarize(outs), (False, False))""",
        """        self.assertEqual(cats(outs)['ccs'], R.APPL)
        self.assertEqual(R.summarize(outs), (False, False))
        self.assertFalse(R.documentation_status(outs))

    def test_tier1_complete_means_all_satisfied(self):
        self.assertEqual(R.summarize(R.base_oil_requirements(base_oil())), (True, True))
        self.assertEqual(R.REQUIREMENTS_VERSION, 'mandatory-tier1-2026-11-10.3')""")]
for a, b in rep:
    assert a in s, a[:60]
    s = s.replace(a, b, 1)
open(p, 'w', encoding='utf-8', newline='\n').write(s)

p = 'tools/data_policy/tests/test_data_policy.py'
s = open(p, encoding='utf-8').read()
rep = [("""            self.assertIn(f'| {cls} | {n} | {c} | {e} |', md)""",
        """            self.assertEqual(c, e, 'tier1_complete and formulation_eligible have the same meaning')
            with open(os.path.join(self.path, 'documentation_coverage.csv'), encoding='utf-8') as fh2:
                d = sum(1 for r in csv.DictReader(fh2) if r['material_class'] == cls and r['all_blocking_documented'] == 'true')
            self.assertIn(f'| {cls} | {n} | {c} | {d} |', md)"""),
       ("""            if r['formulation_eligible'] == 'true':
                self.assertEqual(r['tier1_complete'], 'true', 'eligible implies Tier 1 complete')""",
        """            self.assertEqual(r['tier1_complete'], r['formulation_eligible'], 'version .3: both mean all mandatory Tier 1 satisfied')"""),
       ("""        import source_selection as S
        allowed = {ch['product'] for ch in S.CHANGES} | {u[0] for u in S.OPEN_QUESTION_UPDATES}""",
        """        import source_selection as S
        allowed = ({ch['product'] for ch in S.CHANGES} | {u[0] for u in S.OPEN_QUESTION_UPDATES} | {c['product'] for c in S.LIST_FILLS}
                   | {c['product'] for c in S.QUALIFIER_FIXES} | {c[0] for c in S.CONFLICT_ADDS})"""),
       ("""    def test_zero_tds_value_uses_no_relative_difference(self):""",
        """    def test_flash_point_needs_cup_type_on_both_sides(self):
        r = INV.compare('flash_point', {'value': 265, 'unit': '°C', 'printed_text': 'Flash Point (COC) 265'}, {'value': 255, 'unit': '°C'})
        self.assertEqual(r['comparability'], 'comparability unknown')
        self.assertNotIn('abs_diff', r)

    def test_zero_tds_value_uses_no_relative_difference(self):"""),
       ("""                      'requirements', 'build_eligibility', 'source_coverage_ledger', 'treat_rate_basis_scan', 'verify_preserved'):""",
        """                      'requirements', 'build_eligibility', 'source_coverage_ledger', 'treat_rate_basis_scan', 'verify_preserved',
                      'lead_review', 'association_review', 'co_component_evidence_scan'):""")]
for a, b in rep:
    assert a in s, a[:60]
    s = s.replace(a, b, 1)
tail = "\n\nif __name__ == '__main__':\n    unittest.main()\n"
assert s.endswith(tail)
s = s[:-len(tail)]
s += open(r'C:\Users\windo\AppData\Local\Temp\claude\c--Users-windo-OneDrive-Desktop-Smart-formulator-project\3f66f328-3708-42fd-ad6b-a350bfb79529\scratchpad\wsA\evidence_tests.py', encoding='utf-8').read()
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
