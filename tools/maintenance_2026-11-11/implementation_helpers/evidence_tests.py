


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


if __name__ == '__main__':
    unittest.main()
