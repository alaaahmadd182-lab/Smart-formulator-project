"""Tests for sae_grader.py — Step 8 SAE J300 grade mapping."""

import sys
import pathlib
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.sae_grader import (
    kv100_to_ht_grade,
    parse_package_ht_grades,
    treat_rate_ht_grade,
    ht_grade_overlap,
    HT_GRADES,
    HT_BANDS,
)


# ---------------------------------------------------------------------------
# TestKv100ToHtGrade
# ---------------------------------------------------------------------------

class TestKv100ToHtGrade(unittest.TestCase):

    def test_sae20_lower_boundary(self):
        self.assertEqual(kv100_to_ht_grade(5.6), "20")

    def test_sae20_mid(self):
        self.assertEqual(kv100_to_ht_grade(7.0), "20")

    def test_sae20_upper_boundary_exclusive(self):
        # 9.3 is the start of SAE 30
        self.assertEqual(kv100_to_ht_grade(9.3), "30")

    def test_sae30_mid(self):
        self.assertEqual(kv100_to_ht_grade(10.5), "30")

    def test_sae40_mid(self):
        self.assertEqual(kv100_to_ht_grade(14.0), "40")

    def test_sae50_mid(self):
        self.assertEqual(kv100_to_ht_grade(18.0), "50")

    def test_sae60_lower_boundary(self):
        self.assertEqual(kv100_to_ht_grade(21.9), "60")

    def test_sae60_very_high(self):
        self.assertEqual(kv100_to_ht_grade(300.0), "60")

    def test_below_sae20_returns_none(self):
        self.assertIsNone(kv100_to_ht_grade(3.0))

    def test_exactly_at_sae20_min(self):
        # 5.6 is the inclusive lower bound of SAE 20
        self.assertEqual(kv100_to_ht_grade(5.6), "20")

    def test_just_below_sae20_min(self):
        self.assertIsNone(kv100_to_ht_grade(5.59))

    def test_all_bands_covered(self):
        # Verify one representative value per band
        expected = [("20", 7.0), ("30", 11.0), ("40", 14.0), ("50", 18.0), ("60", 25.0)]
        for grade, kv in expected:
            with self.subTest(grade=grade):
                self.assertEqual(kv100_to_ht_grade(kv), grade)

    def test_ht_grades_tuple_matches_bands(self):
        self.assertEqual(HT_GRADES, tuple(b[0] for b in HT_BANDS))


# ---------------------------------------------------------------------------
# TestParsePackageHtGrades
# ---------------------------------------------------------------------------

class TestParsePackageHtGrades(unittest.TestCase):

    def test_single_multigrade(self):
        self.assertEqual(parse_package_ht_grades("15W-40"), frozenset({"40"}))

    def test_multiple_multigrades(self):
        result = parse_package_ht_grades("10W-30|15W-40|20W-50")
        self.assertEqual(result, frozenset({"30", "40", "50"}))

    def test_monograde_sae_prefix(self):
        self.assertEqual(parse_package_ht_grades("SAE 40"), frozenset({"40"}))

    def test_monograde_bare_number(self):
        self.assertEqual(parse_package_ht_grades("40"), frozenset({"40"}))

    def test_multi_grade_keyword_returns_empty(self):
        # "multi-grade" has no parseable ht grade
        self.assertEqual(parse_package_ht_grades("multi-grade"), frozenset())

    def test_empty_string_returns_empty(self):
        self.assertEqual(parse_package_ht_grades(""), frozenset())

    def test_none_returns_empty(self):
        self.assertEqual(parse_package_ht_grades(None), frozenset())

    def test_mixed_valid_and_keyword(self):
        result = parse_package_ht_grades("15W-40|mono-grade")
        self.assertEqual(result, frozenset({"40"}))

    def test_sae_30_included(self):
        result = parse_package_ht_grades("10W-30|10W-40")
        self.assertIn("30", result)
        self.assertIn("40", result)

    def test_whitespace_stripped(self):
        result = parse_package_ht_grades(" 15W-40 | 10W-30 ")
        self.assertEqual(result, frozenset({"40", "30"}))


# ---------------------------------------------------------------------------
# TestTreatRateHtGrade
# ---------------------------------------------------------------------------

class TestTreatRateHtGrade(unittest.TestCase):

    def test_15w40(self):
        self.assertEqual(treat_rate_ht_grade("15W-40"), "40")

    def test_10w30(self):
        self.assertEqual(treat_rate_ht_grade("10W-30"), "30")

    def test_20w50(self):
        self.assertEqual(treat_rate_ht_grade("20W-50"), "50")

    def test_mono_grade_keyword(self):
        self.assertIsNone(treat_rate_ht_grade("mono-grade"))

    def test_multi_grade_keyword(self):
        self.assertIsNone(treat_rate_ht_grade("multi-grade"))

    def test_empty_returns_none(self):
        self.assertIsNone(treat_rate_ht_grade(""))

    def test_none_returns_none(self):
        self.assertIsNone(treat_rate_ht_grade(None))


# ---------------------------------------------------------------------------
# TestHtGradeOverlap
# ---------------------------------------------------------------------------

class TestHtGradeOverlap(unittest.TestCase):

    def test_common_grade_returned(self):
        result = ht_grade_overlap({"30", "40"}, {"40", "50"})
        self.assertEqual(result, ["40"])

    def test_no_overlap_returns_empty(self):
        self.assertEqual(ht_grade_overlap({"30"}, {"40"}), [])

    def test_multiple_shared_sorted(self):
        result = ht_grade_overlap({"30", "40", "50"}, {"20", "30", "40"})
        self.assertEqual(result, ["30", "40"])

    def test_identical_sets(self):
        result = ht_grade_overlap({"20", "30"}, {"20", "30"})
        self.assertEqual(sorted(result), ["20", "30"])

    def test_empty_inputs(self):
        self.assertEqual(ht_grade_overlap(set(), {"40"}), [])
        self.assertEqual(ht_grade_overlap({"40"}, set()), [])
        self.assertEqual(ht_grade_overlap(set(), set()), [])

    def test_frozenset_accepted(self):
        result = ht_grade_overlap(frozenset({"40"}), frozenset({"40"}))
        self.assertEqual(result, ["40"])


if __name__ == "__main__":
    unittest.main()
