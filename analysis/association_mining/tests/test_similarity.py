"""Tests for similarity.py — Step 7 similarity and clustering."""

import math
import sys
import pathlib
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.similarity import (
    BO_FEATURE_COLS,
    AP_FEATURE_COLS,
    feature_matrix,
    normalise,
    cosine_sim,
    euclidean,
    pairwise_cosine,
    top_pairs,
    kmeans,
    silhouette_score,
    best_k,
)


# ---------------------------------------------------------------------------
# TestCosimeSim
# ---------------------------------------------------------------------------

class TestCosimeSim(unittest.TestCase):

    def test_identical_vectors(self):
        s, n = cosine_sim([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
        self.assertAlmostEqual(s, 1.0, places=10)
        self.assertEqual(n, 3)

    def test_scaled_vector_still_1(self):
        # Cosine is scale-invariant
        s, n = cosine_sim([1.0, 2.0, 3.0], [2.0, 4.0, 6.0])
        self.assertAlmostEqual(s, 1.0, places=10)

    def test_orthogonal_vectors(self):
        s, n = cosine_sim([1.0, 0.0], [0.0, 1.0])
        self.assertAlmostEqual(s, 0.0, places=10)

    def test_opposite_vectors(self):
        s, n = cosine_sim([1.0, 0.0], [-1.0, 0.0])
        self.assertAlmostEqual(s, -1.0, places=10)

    def test_one_none_dimension_skipped(self):
        # Dimension 1 is None in both — skipped; dims 0 and 2 used
        s, n = cosine_sim([1.0, None, 0.0], [1.0, None, 0.0])
        self.assertAlmostEqual(s, 1.0, places=10)
        self.assertEqual(n, 2)

    def test_none_in_only_one_vector(self):
        # None on one side → that dimension skipped
        s, n = cosine_sim([1.0, None, 1.0], [1.0, 1.0, 1.0])
        # Uses dims 0 and 2: dot=2, norms=sqrt(2)*sqrt(2)=2 → 1.0
        self.assertAlmostEqual(s, 1.0, places=10)
        self.assertEqual(n, 2)

    def test_all_none_returns_none(self):
        s, n = cosine_sim([None, None], [None, None])
        self.assertIsNone(s)
        self.assertEqual(n, 0)

    def test_single_shared_dim_returns_none(self):
        s, n = cosine_sim([1.0, None], [1.0, None])
        self.assertIsNone(s)   # n_shared=1 < 2
        self.assertEqual(n, 1)

    def test_zero_vector_returns_none(self):
        s, n = cosine_sim([0.0, 0.0], [1.0, 1.0])
        self.assertIsNone(s)


# ---------------------------------------------------------------------------
# TestEuclidean
# ---------------------------------------------------------------------------

class TestEuclidean(unittest.TestCase):

    def test_zero_distance(self):
        self.assertAlmostEqual(euclidean([1.0, 2.0], [1.0, 2.0]), 0.0)

    def test_unit_distance(self):
        self.assertAlmostEqual(euclidean([0.0, 0.0], [1.0, 0.0]), 1.0)

    def test_pythagorean(self):
        self.assertAlmostEqual(euclidean([0.0, 0.0], [3.0, 4.0]), 5.0)


# ---------------------------------------------------------------------------
# TestNormalise
# ---------------------------------------------------------------------------

class TestNormalise(unittest.TestCase):

    def _mat(self, *rows):
        return [list(r) for r in rows]

    def test_simple_two_cols(self):
        mat = self._mat([0.0, 10.0], [1.0, 20.0])
        nn, ni, stats = normalise(mat)
        # col 0: min=0, max=1 → 0→0.0, 1→1.0
        self.assertAlmostEqual(nn[0][0], 0.0)
        self.assertAlmostEqual(nn[1][0], 1.0)
        # col 1: min=10, max=20 → 10→0.0, 20→1.0
        self.assertAlmostEqual(nn[0][1], 0.0)
        self.assertAlmostEqual(nn[1][1], 1.0)

    def test_constant_column_maps_to_zero(self):
        mat = self._mat([5.0, 1.0], [5.0, 2.0])
        nn, ni, stats = normalise(mat)
        self.assertAlmostEqual(nn[0][0], 0.0)
        self.assertAlmostEqual(nn[1][0], 0.0)

    def test_none_preserved_in_norm_none(self):
        mat = [[1.0, None], [2.0, 3.0]]
        nn, ni, stats = normalise(mat)
        self.assertIsNone(nn[0][1])
        self.assertIsNotNone(nn[1][1])

    def test_none_becomes_half_in_norm_imp(self):
        mat = [[None, 1.0], [1.0, 2.0]]
        nn, ni, stats = normalise(mat)
        self.assertAlmostEqual(ni[0][0], 0.5)

    def test_stats_shape(self):
        mat = [[1.0, 2.0], [3.0, 4.0]]
        _, _, stats = normalise(mat)
        self.assertEqual(len(stats), 2)
        mean, lo, hi = stats[0]
        self.assertAlmostEqual(lo, 1.0)
        self.assertAlmostEqual(hi, 3.0)

    def test_all_none_column(self):
        mat = [[None, 1.0], [None, 2.0]]
        nn, ni, stats = normalise(mat)
        # all-None column → 0.5 imputed, 0.0 as normalized (constant default)
        self.assertIsNone(nn[0][0])
        self.assertIsNone(nn[1][0])
        self.assertAlmostEqual(ni[0][0], 0.5)
        self.assertAlmostEqual(ni[1][0], 0.5)


# ---------------------------------------------------------------------------
# TestPairwiseCosine
# ---------------------------------------------------------------------------

class TestPairwiseCosine(unittest.TestCase):

    def test_diagonal_is_one(self):
        mat = [[1.0, 0.0], [0.0, 1.0], [0.5, 0.5]]
        sim = pairwise_cosine(mat)
        for i in range(3):
            self.assertAlmostEqual(sim[i][i], 1.0)

    def test_symmetry(self):
        mat = [[1.0, 2.0], [3.0, 1.0], [0.5, 0.5]]
        sim = pairwise_cosine(mat)
        for i in range(3):
            for j in range(3):
                if sim[i][j] is not None and sim[j][i] is not None:
                    self.assertAlmostEqual(sim[i][j], sim[j][i], places=10)

    def test_shape(self):
        mat = [[1.0], [2.0], [3.0]]
        sim = pairwise_cosine(mat)
        self.assertEqual(len(sim), 3)
        self.assertEqual(len(sim[0]), 3)

    def test_all_none_row_gives_none_off_diag(self):
        # Row 0 is all None → cosine with any other row returns None
        mat = [[None, None], [1.0, 0.0], [0.0, 1.0]]
        sim = pairwise_cosine(mat)
        self.assertIsNone(sim[0][1])
        self.assertIsNone(sim[1][0])
        self.assertAlmostEqual(sim[0][0], 1.0)


# ---------------------------------------------------------------------------
# TestTopPairs
# ---------------------------------------------------------------------------

class TestTopPairs(unittest.TestCase):

    def test_sorted_descending(self):
        sim = [
            [1.0,  0.9,  0.5],
            [0.9,  1.0,  0.3],
            [0.5,  0.3,  1.0],
        ]
        pairs = top_pairs(sim, ["a", "b", "c"], n=10)
        sims = [p["similarity"] for p in pairs]
        self.assertEqual(sims, sorted(sims, reverse=True))

    def test_excludes_diagonal(self):
        sim = [[1.0, 0.8], [0.8, 1.0]]
        pairs = top_pairs(sim, ["x", "y"], n=10)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["id_a"], "x")
        self.assertEqual(pairs[0]["id_b"], "y")

    def test_respects_n_limit(self):
        n = 4
        sim = [[1.0 if i == j else 0.5 for j in range(n)] for i in range(n)]
        pairs = top_pairs(sim, [str(i) for i in range(n)], n=3)
        self.assertLessEqual(len(pairs), 3)

    def test_none_pairs_excluded(self):
        sim = [[1.0, None], [None, 1.0]]
        pairs = top_pairs(sim, ["a", "b"], n=10)
        self.assertEqual(len(pairs), 0)


# ---------------------------------------------------------------------------
# TestKmeans
# ---------------------------------------------------------------------------

class TestKmeans(unittest.TestCase):

    def _two_clusters(self):
        # Two well-separated clusters in 1D
        cluster_a = [[0.0, 0.0]] * 5
        cluster_b = [[1.0, 1.0]] * 5
        return cluster_a + cluster_b

    def test_two_clear_clusters(self):
        mat = self._two_clusters()
        labels = kmeans(mat, k=2, seed=0)
        # Both clusters should be internally consistent
        a_labels = set(labels[:5])
        b_labels = set(labels[5:])
        self.assertEqual(len(a_labels), 1)
        self.assertEqual(len(b_labels), 1)
        self.assertNotEqual(a_labels, b_labels)

    def test_k_one_all_same_cluster(self):
        mat = [[0.1, 0.2], [0.3, 0.4], [0.9, 0.8]]
        labels = kmeans(mat, k=1)
        self.assertEqual(set(labels), {0})

    def test_labels_length_matches_input(self):
        mat = [[float(i), float(i)] for i in range(10)]
        labels = kmeans(mat, k=3)
        self.assertEqual(len(labels), 10)

    def test_k_clamped_to_n(self):
        mat = [[0.0, 0.0], [1.0, 1.0]]
        labels = kmeans(mat, k=100)   # clamped to 2
        self.assertEqual(len(labels), 2)

    def test_all_same_point(self):
        mat = [[0.5, 0.5]] * 8
        labels = kmeans(mat, k=3, seed=0)
        # All assigned to some cluster (no crash)
        self.assertEqual(len(labels), 8)

    def test_empty_matrix(self):
        self.assertEqual(kmeans([], k=3), [])


# ---------------------------------------------------------------------------
# TestSilhouette
# ---------------------------------------------------------------------------

class TestSilhouette(unittest.TestCase):

    def test_perfect_separation_near_one(self):
        # Two well-separated clusters
        mat  = [[0.0, 0.0]] * 5 + [[10.0, 10.0]] * 5
        lbls = [0] * 5 + [1] * 5
        s = silhouette_score(mat, lbls)
        self.assertGreater(s, 0.8)

    def test_single_cluster_returns_zero(self):
        mat  = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
        lbls = [0, 0, 0]
        self.assertAlmostEqual(silhouette_score(mat, lbls), 0.0)

    def test_overlapping_clusters_lower_score(self):
        # Points from two clusters interleaved
        mat  = [[float(i), float(i)] for i in range(6)]
        lbls = [0, 1, 0, 1, 0, 1]
        s = silhouette_score(mat, lbls)
        self.assertLess(s, 0.5)


# ---------------------------------------------------------------------------
# TestBestK
# ---------------------------------------------------------------------------

class TestBestK(unittest.TestCase):

    def test_returns_int_and_dict(self):
        mat = [[float(i), float(i)] for i in range(20)]
        k, scores = best_k(mat, ks=(3, 4, 5), seed=0)
        self.assertIsInstance(k, int)
        self.assertIn(k, scores)

    def test_skips_k_ge_n(self):
        mat = [[0.0, 0.0], [1.0, 1.0]]  # n=2
        k, scores = best_k(mat, ks=(2, 3, 4), seed=0)
        # k=2,3,4 all >= n=2 so none are tried → falls back to ks[0]
        self.assertEqual(k, 2)
        self.assertEqual(scores, {})

    def test_clear_best_k_chosen(self):
        # 3 tight clusters, far apart
        mat = ([[0.0, 0.0]] * 10 +
               [[5.0, 0.0]] * 10 +
               [[0.0, 5.0]] * 10)
        k, scores = best_k(mat, ks=(2, 3, 4, 5), seed=42)
        self.assertEqual(k, 3)


# ---------------------------------------------------------------------------
# TestFeatureMatrix
# ---------------------------------------------------------------------------

class TestFeatureMatrix(unittest.TestCase):

    def _bo_row(self, **kw):
        defaults = {
            "kv100": "5.0", "kv40": "30.0",
            "vi_point": "120.0", "vi_lb_bound": "",
            "density_kg_m3": "870.0", "api_group_ord": "3.0",
            "sulfur_wt_pct": "0.001", "pour_point": "-15.0",
            "pour_point_ub": "",
        }
        defaults.update(kw)
        return defaults

    def _ap_row(self, **kw):
        defaults = {
            "tbn": "80.0", "sulfated_ash": "1.2",
            "ca": "2.0", "zn": "0.1", "p": "0.09",
            "density_kg_m3": "920.0", "zn_p_sum": "0.19", "ca_tbn_ratio": "0.025",
        }
        defaults.update(kw)
        return defaults

    def test_bo_vector_length(self):
        rows = [self._bo_row()]
        mat = feature_matrix(rows, "bo")
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), len(BO_FEATURE_COLS))

    def test_ap_vector_length(self):
        rows = [self._ap_row()]
        mat = feature_matrix(rows, "ap")
        self.assertEqual(len(mat), 1)
        self.assertEqual(len(mat[0]), len(AP_FEATURE_COLS))

    def test_vi_eff_uses_point_first(self):
        row = self._bo_row(vi_point="130.0", vi_lb_bound="120.0")
        mat = feature_matrix([row], "bo")
        vi_idx = list(("kv100","kv40","vi_eff","density_kg_m3","api_group_ord","sulfur_wt_pct","pour_point_eff")).index("vi_eff")
        self.assertAlmostEqual(mat[0][vi_idx], 130.0)

    def test_vi_eff_falls_back_to_lb(self):
        row = self._bo_row(vi_point="", vi_lb_bound="110.0")
        mat = feature_matrix([row], "bo")
        vi_idx = 2  # 'vi_eff' is index 2 in BO_FEATURE_COLS
        self.assertAlmostEqual(mat[0][vi_idx], 110.0)

    def test_pour_point_eff_falls_back_to_ub(self):
        row = self._bo_row(pour_point="", pour_point_ub="-18.0")
        mat = feature_matrix([row], "bo")
        pp_idx = 6  # 'pour_point_eff' is last in BO_FEATURE_COLS
        self.assertAlmostEqual(mat[0][pp_idx], -18.0)

    def test_missing_values_become_none(self):
        row = self._bo_row(kv100="", kv40="None")
        mat = feature_matrix([row], "bo")
        self.assertIsNone(mat[0][0])  # kv100
        self.assertIsNone(mat[0][1])  # kv40

    def test_unknown_kind_raises(self):
        with self.assertRaises(ValueError):
            feature_matrix([{}], "unknown")


if __name__ == "__main__":
    unittest.main()
