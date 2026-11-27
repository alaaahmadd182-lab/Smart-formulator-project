"""Tests for scorer.py — Step 9 formulation candidate scoring."""

import sys
import pathlib
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.scorer import (
    api_group_score,
    treat_rate_score,
    bo_completeness_score,
    ap_completeness_score,
    pkg_type_score,
    score_pair,
    WEIGHTS,
    _BO_KEY_COLS,
    _AP_KEY_COLS,
)


# ---------------------------------------------------------------------------
# TestApiGroupScore
# ---------------------------------------------------------------------------

class TestApiGroupScore(unittest.TestCase):

    def test_group_iv_is_max(self):
        self.assertAlmostEqual(api_group_score("Group IV"), 1.0)

    def test_group_iii_less_than_iv(self):
        self.assertLess(api_group_score("Group III"), api_group_score("Group IV"))

    def test_group_ii_less_than_iii(self):
        self.assertLess(api_group_score("Group II"), api_group_score("Group III"))

    def test_group_i_low(self):
        self.assertLess(api_group_score("Group I"), api_group_score("Group II"))

    def test_group_ii_plus(self):
        s = api_group_score("Group II+")
        self.assertGreater(s, api_group_score("Group II"))
        self.assertLess(s, api_group_score("Group III"))

    def test_unknown_returns_low_score(self):
        s = api_group_score("Unknown")
        self.assertLessEqual(s, 0.3)

    def test_none_returns_low_score(self):
        self.assertLessEqual(api_group_score(None), 0.3)

    def test_empty_string_returns_low_score(self):
        self.assertLessEqual(api_group_score(""), 0.3)

    def test_score_in_range(self):
        for grp in ("Group I", "Group II", "Group II+", "Group III", "Group IV", "Group V"):
            with self.subTest(grp=grp):
                s = api_group_score(grp)
                self.assertGreaterEqual(s, 0.0)
                self.assertLessEqual(s, 1.0)

    def test_whitespace_stripped(self):
        self.assertAlmostEqual(api_group_score("  Group IV  "), 1.0)


# ---------------------------------------------------------------------------
# TestTreatRateScore
# ---------------------------------------------------------------------------

class TestTreatRateScore(unittest.TestCase):

    def test_numeric_string_returns_one(self):
        self.assertAlmostEqual(treat_rate_score("10.5"), 1.0)

    def test_float_returns_one(self):
        self.assertAlmostEqual(treat_rate_score(10.5), 1.0)

    def test_zero_returns_one(self):
        # 0.0 treat rate is a valid (if unusual) number
        self.assertAlmostEqual(treat_rate_score("0.0"), 1.0)

    def test_empty_string_returns_zero(self):
        self.assertAlmostEqual(treat_rate_score(""), 0.0)

    def test_none_returns_zero(self):
        self.assertAlmostEqual(treat_rate_score(None), 0.0)

    def test_none_string_returns_zero(self):
        self.assertAlmostEqual(treat_rate_score("None"), 0.0)


# ---------------------------------------------------------------------------
# TestBoCompletenessScore
# ---------------------------------------------------------------------------

class TestBoCompletenessScore(unittest.TestCase):

    def _full_row(self):
        return {col: "5.0" for col in _BO_KEY_COLS}

    def test_all_present_returns_one(self):
        self.assertAlmostEqual(bo_completeness_score(self._full_row()), 1.0)

    def test_none_present_returns_zero(self):
        row = {col: "" for col in _BO_KEY_COLS}
        self.assertAlmostEqual(bo_completeness_score(row), 0.0)

    def test_half_present(self):
        row = {col: "" for col in _BO_KEY_COLS}
        half = len(_BO_KEY_COLS) // 2
        for col in list(_BO_KEY_COLS)[:half]:
            row[col] = "5.0"
        s = bo_completeness_score(row)
        self.assertAlmostEqual(s, half / len(_BO_KEY_COLS))

    def test_empty_dict_returns_zero(self):
        self.assertAlmostEqual(bo_completeness_score({}), 0.0)

    def test_score_between_zero_and_one(self):
        row = self._full_row()
        s = bo_completeness_score(row)
        self.assertGreaterEqual(s, 0.0)
        self.assertLessEqual(s, 1.0)


# ---------------------------------------------------------------------------
# TestApCompletenessScore
# ---------------------------------------------------------------------------

class TestApCompletenessScore(unittest.TestCase):

    def _full_row(self):
        return {col: "1.0" for col in _AP_KEY_COLS}

    def test_all_present_returns_one(self):
        self.assertAlmostEqual(ap_completeness_score(self._full_row()), 1.0)

    def test_none_present_returns_zero(self):
        row = {col: "" for col in _AP_KEY_COLS}
        self.assertAlmostEqual(ap_completeness_score(row), 0.0)

    def test_one_missing(self):
        row = self._full_row()
        row[list(_AP_KEY_COLS)[0]] = ""
        expected = (len(_AP_KEY_COLS) - 1) / len(_AP_KEY_COLS)
        self.assertAlmostEqual(ap_completeness_score(row), expected)

    def test_empty_dict_returns_zero(self):
        self.assertAlmostEqual(ap_completeness_score({}), 0.0)


# ---------------------------------------------------------------------------
# TestPkgTypeScore
# ---------------------------------------------------------------------------

class TestPkgTypeScore(unittest.TestCase):

    def test_hdeo_returns_one(self):
        self.assertAlmostEqual(pkg_type_score("hdeo"), 1.0)

    def test_pceo_returns_one(self):
        self.assertAlmostEqual(pkg_type_score("pceo"), 1.0)

    def test_universal_returns_one(self):
        self.assertAlmostEqual(pkg_type_score("universal"), 1.0)

    def test_gear_returns_one(self):
        self.assertAlmostEqual(pkg_type_score("gear"), 1.0)

    def test_atf_returns_one(self):
        self.assertAlmostEqual(pkg_type_score("atf"), 1.0)

    def test_other_returns_zero(self):
        self.assertAlmostEqual(pkg_type_score("other"), 0.0)

    def test_missing_returns_zero(self):
        self.assertAlmostEqual(pkg_type_score("missing"), 0.0)

    def test_none_returns_zero(self):
        self.assertAlmostEqual(pkg_type_score(None), 0.0)

    def test_empty_returns_zero(self):
        self.assertAlmostEqual(pkg_type_score(""), 0.0)


# ---------------------------------------------------------------------------
# TestScorePair
# ---------------------------------------------------------------------------

class TestScorePair(unittest.TestCase):

    def _best_bo(self):
        return {
            "api_group": "Group IV",
            **{col: "5.0" for col in _BO_KEY_COLS},
        }

    def _best_ap(self):
        return {
            "package_type_canon": "hdeo",
            **{col: "1.0" for col in _AP_KEY_COLS},
        }

    def _best_cand(self):
        return {
            "bo_api_group": "Group IV",
            "ap_package_type": "hdeo",
            "treat_rate_pct_med": "10.0",
        }

    def test_returns_all_keys(self):
        result = score_pair(self._best_bo(), self._best_ap(), self._best_cand())
        for key in ("score_treat_rate", "score_api_group", "score_bo_complete",
                    "score_ap_complete", "score_pkg_type", "score"):
            self.assertIn(key, result)

    def test_best_possible_score(self):
        result = score_pair(self._best_bo(), self._best_ap(), self._best_cand())
        self.assertAlmostEqual(result["score"], 100.0)

    def test_worst_possible_score(self):
        worst_cand = {"treat_rate_pct_med": "", "bo_api_group": "", "ap_package_type": ""}
        result = score_pair({}, {}, worst_cand)
        # api_group unknown = 0.3; all else zero
        expected = round(WEIGHTS["api_group"] * 0.3 * 100, 1)
        self.assertAlmostEqual(result["score"], expected)

    def test_score_range_0_to_100(self):
        result = score_pair(self._best_bo(), self._best_ap(), self._best_cand())
        self.assertGreaterEqual(result["score"], 0.0)
        self.assertLessEqual(result["score"], 100.0)

    def test_no_treat_rate_lowers_score(self):
        cand_with    = {**self._best_cand(), "treat_rate_pct_med": "10.0"}
        cand_without = {**self._best_cand(), "treat_rate_pct_med": ""}
        s_with    = score_pair(self._best_bo(), self._best_ap(), cand_with)["score"]
        s_without = score_pair(self._best_bo(), self._best_ap(), cand_without)["score"]
        self.assertGreater(s_with, s_without)

    def test_group_iii_lower_than_iv(self):
        bo_iii = {**self._best_bo(), "api_group": "Group III"}
        s_iv  = score_pair(self._best_bo(), self._best_ap(), self._best_cand())["score"]
        s_iii = score_pair(bo_iii,          self._best_ap(), self._best_cand())["score"]
        self.assertGreater(s_iv, s_iii)

    def test_missing_data_lowers_completeness(self):
        bo_sparse = {"api_group": "Group IV"}  # no feature values
        s_full   = score_pair(self._best_bo(), self._best_ap(), self._best_cand())["score"]
        s_sparse = score_pair(bo_sparse,        self._best_ap(), self._best_cand())["score"]
        self.assertGreater(s_full, s_sparse)

    def test_weights_sum_to_one(self):
        total = sum(WEIGHTS.values())
        self.assertAlmostEqual(total, 1.0, places=10)

    def test_cand_fallback_for_api_group(self):
        # bo_row has no api_group; cand carries bo_api_group
        cand = {**self._best_cand(), "bo_api_group": "Group IV"}
        result = score_pair({}, self._best_ap(), cand)
        self.assertAlmostEqual(result["score_api_group"], 1.0)

    def test_cand_fallback_for_pkg_type(self):
        # ap_row empty; cand carries ap_package_type
        cand = {**self._best_cand(), "ap_package_type": "hdeo"}
        result = score_pair(self._best_bo(), {}, cand)
        self.assertAlmostEqual(result["score_pkg_type"], 1.0)


if __name__ == "__main__":
    unittest.main()
