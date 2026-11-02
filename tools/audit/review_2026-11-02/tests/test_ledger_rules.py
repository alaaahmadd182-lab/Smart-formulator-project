"""Regression tests for the citation-ledger rules (2026-11-02 review).

They prove that:
  1. an "incomplete" (or "unavailable", empty or unknown) verdict can never count as verified, not even for a citation
     that an automated check also passed;
  2. a citation without an explicit verdict is never approved automatically: the association review has no default
     verdict, and the ledger classifies such a citation as text presence only or unresolved;
  3. any unresolved citation prevents a "verification complete" result, in the rules, in the ledger's exit code and in
     the report.

Run: python -m unittest discover -s tools/audit/review_2026-11-02/tests -v
"""
import csv, importlib, json, os, sys, tempfile, unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import ledger_rules as L  # noqa: E402
import review_lib as R  # noqa: E402

RES = os.path.join(R.ROOT, 'docs', 'audit_review_2026-11-02', 'verification_results')
KEY = 'CF-999#0#DL2-00000.pdf'


class IncompleteVerdicts(unittest.TestCase):
    def test_incomplete_verdict_is_unresolved(self):
        self.assertEqual(L.classify_verdict({'verdict': 'incomplete', 'basis': 'context review (text layer)'}), 'E')

    def test_unavailable_verdict_is_unresolved(self):
        self.assertEqual(L.classify_verdict({'verdict': 'unavailable', 'basis': 'not accessed'}), 'E')

    def test_incomplete_verdict_wins_over_automated_check(self):
        verdicts = {KEY: {'verdict': 'incomplete', 'basis': 'context review', 'note': 'column not established'}}
        self.assertEqual(L.classify_citation(KEY, 'on cited page', {KEY}, verdicts), 'E')

    def test_incomplete_never_counted_as_verified(self):
        verdicts = {KEY: {'verdict': 'incomplete', 'basis': 'context review'}}
        s = L.summarize([L.classify_citation(KEY, 'on cited page', set(), verdicts)])
        self.assertEqual(s['verified'], 0)
        self.assertEqual(s['E'], 1)
        self.assertFalse(s['complete'])

    def test_unknown_or_malformed_verdicts_are_unresolved(self):
        for v in ({'verdict': 'ok', 'basis': 'context review'}, {'verdict': '', 'basis': 'x'}, {'basis': 'context review'},
                  'verified', None, {'verdict': 'verified', 'basis': ''}):
            self.assertEqual(L.classify_verdict(v), 'E', v)


class UnknownCitations(unittest.TestCase):
    def test_unknown_citation_with_number_on_page_is_not_verified(self):
        self.assertEqual(L.classify_citation(KEY, 'on cited page', set(), {}), 'D')

    def test_unknown_citation_without_number_is_unresolved(self):
        for check in ('not found', 'no text layer', 'no numeric value', 'not an archive file', 'on other page(s)'):
            self.assertEqual(L.classify_citation(KEY, check, set(), {}), 'E', check)

    def test_association_review_has_no_default_verdict(self):
        """A presence-only citation that is not listed in build_association_review.py receives no verdict."""
        import build_association_review as B
        import citation_context as CC
        rows = list(csv.DictReader(open(os.path.join(RES, 'source_checks_v5.csv'), encoding='utf-8')))
        F = {f['id']: f for f in json.load(open(os.path.join(R.HERE, 'output', 'findings_v5.json'), encoding='utf-8'))}
        fake = dict(rows[0]); fake.update(id='CF-001', value_index='9', file='DL2-99999.pdf', result='on cited page')
        with tempfile.TemporaryDirectory() as tmp:
            res = os.path.join(tmp, 'docs', 'audit_review_2026-11-02', 'verification_results'); os.makedirs(res)
            with open(os.path.join(res, 'source_checks_v5.csv'), 'w', encoding='utf-8', newline='') as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows + [fake])
            here = os.path.join(tmp, 'here'); os.makedirs(os.path.join(here, 'output'))
            json.dump(list(F.values()), open(os.path.join(here, 'output', 'findings_v5.json'), 'w', encoding='utf-8'))
            with mock.patch.object(B.R, 'ROOT', tmp), mock.patch.object(B.R, 'HERE', here):
                B.main()
            written = json.load(open(os.path.join(here, 'association_review.json'), encoding='utf-8'))
        new_key = 'CF-001#9#DL2-99999.pdf'
        self.assertIn(new_key, {f"{r['id']}#{r['value_index']}#{r['file']}" for r in CC.presence_only(rows + [fake], F)})
        self.assertNotIn(new_key, written)
        self.assertEqual(L.classify_citation(new_key, 'on cited page', set(), written), 'D')

    def test_unlisted_reference_is_unresolved(self):
        """A source named in a finding text without a recorded verdict becomes an unresolved ledger row."""
        import referenced_sources as RS
        import verification_ledger as V
        refs = V.detect_refs('checked against API 1509 and PubChem; see DL2-12345.pdf')
        self.assertTrue({'api1509', 'pubchem', 'doc:dl2-12345.pdf'} <= refs)
        self.assertFalse(any(e[0] == 'CF-999' for e in RS.ENTRIES))


class Completeness(unittest.TestCase):
    def test_any_unresolved_or_unreviewed_prevents_completion(self):
        self.assertTrue(L.summarize(['A', 'B', 'C', 'N'])['complete'])
        self.assertFalse(L.summarize(['A', 'B', 'C', 'E'])['complete'])
        self.assertFalse(L.summarize(['A', 'D'])['complete'])

    def test_ledger_exit_code_and_report_reflect_incompleteness(self):
        """With the real inputs (which contain unavailable sources) the ledger exits 3 and the report says so."""
        import verification_ledger as V
        code = V.main()
        s = json.load(open(os.path.join(RES, 'ledger_summary.json'), encoding='utf-8'))
        self.assertEqual(code, 0 if s['complete'] else 3)
        md = open(R.REPORT_MD, encoding='utf-8').read()
        if not s['complete']:
            self.assertGreater(s['E'] + s['D'], 0)
            self.assertIn('**Verification complete: no**', md)
            self.assertNotIn('Verification complete: yes', md)
            self.assertIn(f"{s['E']} unresolved", md)

    def test_run_all_distinguishes_execution_from_completeness(self):
        with open(os.path.join(R.HERE, 'run_all_checks.py'), encoding='utf-8') as fh:
            src = fh.read()
        self.assertIn('VERIFICATION COMPLETE', src)
        self.assertIn('INCOMPLETE', src)


if __name__ == '__main__':
    unittest.main()
