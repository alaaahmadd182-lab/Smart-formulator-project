"""Tests for association_miner.py — Step 10 association rule mining."""

import sys
import pathlib
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.association_miner import (
    discretise_bo,
    discretise_ap,
    mine_rules,
    enumerate_antecedents,
    enumerate_consequents,
    TBN_LOW_MAX,
    TBN_HIGH_MIN,
)


# ---------------------------------------------------------------------------
# TestDiscretiseBo
# ---------------------------------------------------------------------------

class TestDiscretiseBo(unittest.TestCase):

    def _row(self, grade="30", api="Group II"):
        return {"bo_ht_grade": grade, "bo_api_group": api}

    def test_grade_30_present(self):
        items = discretise_bo(self._row(grade="30"))
        self.assertIn("grade_30", items)

    def test_grade_40_present(self):
        items = discretise_bo(self._row(grade="40"))
        self.assertIn("grade_40", items)

    def test_grade_50_present(self):
        items = discretise_bo(self._row(grade="50"))
        self.assertIn("grade_50", items)

    def test_missing_grade_produces_no_grade_item(self):
        items = discretise_bo({"bo_ht_grade": "", "bo_api_group": "Group II"})
        self.assertFalse(any(i.startswith("grade_") for i in items))

    def test_api_group_iv_mapped(self):
        items = discretise_bo(self._row(api="Group IV"))
        self.assertIn("api_IV", items)

    def test_api_group_ii_plus_mapped(self):
        items = discretise_bo(self._row(api="Group II+"))
        self.assertIn("api_IIp", items)

    def test_unknown_api_mapped_to_unk(self):
        items = discretise_bo(self._row(api=""))
        self.assertIn("api_unk", items)

    def test_none_api_mapped_to_unk(self):
        items = discretise_bo({"bo_ht_grade": "30", "bo_api_group": None})
        self.assertIn("api_unk", items)

    def test_returns_frozenset(self):
        self.assertIsInstance(discretise_bo(self._row()), frozenset)

    def test_fallback_key_ht_grade(self):
        # 'ht_grade' (without 'bo_' prefix) also works
        items = discretise_bo({"ht_grade": "30", "api_group": "Group III"})
        self.assertIn("grade_30", items)
        self.assertIn("api_III", items)


# ---------------------------------------------------------------------------
# TestDiscretiseAp
# ---------------------------------------------------------------------------

class TestDiscretiseAp(unittest.TestCase):

    def _row(self, pkg="hdeo", tbn="85"):
        return {"ap_package_type": pkg, "ap_tbn": tbn}

    def test_hdeo_mapped(self):
        self.assertIn("pkg_hdeo", discretise_ap(self._row(pkg="hdeo")))

    def test_pceo_mapped(self):
        self.assertIn("pkg_pceo", discretise_ap(self._row(pkg="pceo")))

    def test_other_mapped_to_pkg_other(self):
        self.assertIn("pkg_other", discretise_ap(self._row(pkg="other")))

    def test_missing_pkg_mapped_to_pkg_unk(self):
        self.assertIn("pkg_unk", discretise_ap({"ap_package_type": "", "ap_tbn": "80"}))

    def test_tbn_low(self):
        items = discretise_ap(self._row(tbn=str(TBN_LOW_MAX - 1)))
        self.assertIn("tbn_low", items)

    def test_tbn_at_boundary_is_med(self):
        # TBN_LOW_MAX itself is NOT low (< threshold)
        items = discretise_ap(self._row(tbn=str(TBN_LOW_MAX)))
        self.assertIn("tbn_med", items)

    def test_tbn_high(self):
        items = discretise_ap(self._row(tbn=str(TBN_HIGH_MIN + 1)))
        self.assertIn("tbn_high", items)

    def test_tbn_at_high_min_boundary_is_med(self):
        # TBN_HIGH_MIN itself is medium (<=)
        items = discretise_ap(self._row(tbn=str(TBN_HIGH_MIN)))
        self.assertIn("tbn_med", items)

    def test_missing_tbn_gives_tbn_unk(self):
        items = discretise_ap({"ap_package_type": "hdeo", "ap_tbn": ""})
        self.assertIn("tbn_unk", items)

    def test_returns_frozenset(self):
        self.assertIsInstance(discretise_ap(self._row()), frozenset)


# ---------------------------------------------------------------------------
# TestEnumerateAntecedents
# ---------------------------------------------------------------------------

class TestEnumerateAntecedents(unittest.TestCase):

    def test_size1_returns_grade_and_api_items(self):
        ants = enumerate_antecedents(max_size=1)
        all_items = {item for ant in ants for item in ant}
        self.assertTrue(any(i.startswith("grade_") for i in all_items))
        self.assertTrue(any(i.startswith("api_") for i in all_items))

    def test_size2_includes_grade_api_combos(self):
        ants = enumerate_antecedents(max_size=2)
        combos = [a for a in ants if len(a) == 2]
        self.assertGreater(len(combos), 0)
        # Every 2-item antecedent must contain one grade and one api item
        for c in combos:
            grades = [i for i in c if i.startswith("grade_")]
            apis   = [i for i in c if i.startswith("api_")]
            self.assertEqual(len(grades), 1)
            self.assertEqual(len(apis),   1)

    def test_no_duplicates(self):
        ants = enumerate_antecedents()
        self.assertEqual(len(ants), len(set(ants)))


# ---------------------------------------------------------------------------
# TestEnumerateConsequents
# ---------------------------------------------------------------------------

class TestEnumerateConsequents(unittest.TestCase):

    def test_includes_single_pkg_items(self):
        cons = enumerate_consequents(max_size=1)
        self.assertTrue(any("pkg_hdeo" in c for c in cons))

    def test_includes_single_tbn_items(self):
        cons = enumerate_consequents(max_size=1)
        self.assertTrue(any("tbn_high" in c for c in cons))

    def test_size2_includes_pkg_tbn_combos(self):
        cons = enumerate_consequents(max_size=2)
        combos = [c for c in cons if len(c) == 2]
        self.assertGreater(len(combos), 0)

    def test_no_duplicates(self):
        cons = enumerate_consequents()
        self.assertEqual(len(cons), len(set(cons)))


# ---------------------------------------------------------------------------
# TestMineRules
# ---------------------------------------------------------------------------

class TestMineRules(unittest.TestCase):

    def _tx(self, bo_items, ap_items):
        return (frozenset(bo_items), frozenset(ap_items))

    def test_basic_rule_found(self):
        # 10 pairs: grade_30 + api_II -> pkg_hdeo + tbn_high (perfect rule)
        txs = [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 10
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        ants = [r["antecedent"] for r in rules]
        self.assertIn(frozenset(["grade_30"]), ants)

    def test_support_calculation(self):
        # 8 pairs match, 2 do not
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 8
            + [self._tx(["grade_40", "api_IV"], ["pkg_other", "tbn_low"])] * 2
        )
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        # Find rule antecedent=grade_30, consequent=pkg_hdeo
        matched = [
            r for r in rules
            if r["antecedent"] == frozenset(["grade_30"])
            and r["consequent"] == frozenset(["pkg_hdeo"])
        ]
        self.assertTrue(matched)
        self.assertAlmostEqual(matched[0]["support"], 0.8, places=4)

    def test_confidence_calculation(self):
        # 6 pairs grade_30->pkg_hdeo, 2 pairs grade_30->pkg_other
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 6
            + [self._tx(["grade_30", "api_II"], ["pkg_other", "tbn_low"])] * 2
        )
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        matched = [
            r for r in rules
            if r["antecedent"] == frozenset(["grade_30"])
            and r["consequent"] == frozenset(["pkg_hdeo"])
        ]
        self.assertTrue(matched)
        # 6/8 = 0.75 confidence
        self.assertAlmostEqual(matched[0]["confidence"], 0.75, places=4)

    def test_lift_above_one_for_associated_pair(self):
        # grade_30 always comes with pkg_hdeo, but grade_40 comes with pkg_other
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 8
            + [self._tx(["grade_40", "api_IV"], ["pkg_other", "tbn_low"])] * 8
        )
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        matched = [
            r for r in rules
            if r["antecedent"] == frozenset(["grade_30"])
            and r["consequent"] == frozenset(["pkg_hdeo"])
        ]
        self.assertTrue(matched)
        self.assertGreater(matched[0]["lift"], 1.0)

    def test_min_support_filters(self):
        # 1 matching pair out of 20 (5%)
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 1
            + [self._tx(["grade_40", "api_IV"], ["pkg_other", "tbn_low"])] * 19
        )
        rules_strict = mine_rules(txs, min_support=0.10, min_confidence=0.5)
        rules_loose  = mine_rules(txs, min_support=0.03, min_confidence=0.5)
        # The rare rule (grade_30->pkg_hdeo, 5%) should appear with loose but not strict
        def has_rare(rules):
            return any(
                r["antecedent"] == frozenset(["grade_30"])
                and r["consequent"] == frozenset(["pkg_hdeo"])
                for r in rules
            )
        self.assertFalse(has_rare(rules_strict))
        self.assertTrue(has_rare(rules_loose))

    def test_min_confidence_filters(self):
        # grade_30: 5 -> pkg_hdeo, 5 -> pkg_other (confidence 50%)
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 5
            + [self._tx(["grade_30", "api_II"], ["pkg_other", "tbn_low"])] * 5
        )
        rules_strict = mine_rules(txs, min_support=0.05, min_confidence=0.80)
        rules_loose  = mine_rules(txs, min_support=0.05, min_confidence=0.40)
        def has_hdeo(rules):
            return any(
                r["antecedent"] == frozenset(["grade_30"])
                and r["consequent"] == frozenset(["pkg_hdeo"])
                for r in rules
            )
        self.assertFalse(has_hdeo(rules_strict))
        self.assertTrue(has_hdeo(rules_loose))

    def test_sorted_by_lift_descending(self):
        txs = (
            [self._tx(["grade_30", "api_IV"], ["pkg_hdeo", "tbn_high"])] * 10
            + [self._tx(["grade_40", "api_II"], ["pkg_other", "tbn_low"])] * 10
        )
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        lifts = [r["lift"] for r in rules]
        self.assertEqual(lifts, sorted(lifts, reverse=True))

    def test_empty_transactions_returns_empty(self):
        self.assertEqual(mine_rules([], min_support=0.05, min_confidence=0.5), [])

    def test_rule_dict_has_required_keys(self):
        txs = [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 5
        rules = mine_rules(txs, min_support=0.05, min_confidence=0.5)
        if rules:
            for key in ("antecedent", "consequent", "support",
                        "confidence", "lift", "count", "count_ant"):
                self.assertIn(key, rules[0])

    def test_support_confidence_in_range(self):
        txs = (
            [self._tx(["grade_30", "api_II"], ["pkg_hdeo", "tbn_high"])] * 7
            + [self._tx(["grade_30", "api_II"], ["pkg_other", "tbn_low"])] * 3
        )
        rules = mine_rules(txs, min_support=0.0, min_confidence=0.0)
        for r in rules:
            self.assertGreaterEqual(r["support"],    0.0)
            self.assertLessEqual(r["support"],       1.0)
            self.assertGreaterEqual(r["confidence"], 0.0)
            self.assertLessEqual(r["confidence"],    1.0)


if __name__ == "__main__":
    unittest.main()
