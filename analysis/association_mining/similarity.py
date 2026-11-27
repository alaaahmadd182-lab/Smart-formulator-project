"""
Step 7 — Pairwise cosine similarity and k-means clustering for Pipeline B.

Operates on the ML-ready CSV row-dicts produced by run_feature_engineering.py.
Pure functions; no I/O.  Stdlib only.

Public API
----------
feature_matrix(rows, kind)              -> list[list[float|None]]
normalise(matrix)                       -> (norm_none, norm_imp, stats)
cosine_sim(a, b)                        -> (float|None, int)
euclidean(a, b)                         -> float
pairwise_cosine(norm_none)              -> list[list[float|None]]
top_pairs(sim, ids, n)                  -> list[dict]
kmeans(matrix, k, seed, max_iter)       -> list[int]
silhouette_score(matrix, labels)        -> float
best_k(matrix, ks, seed)               -> (int, dict[int, float])

BO_FEATURE_COLS / AP_FEATURE_COLS       feature name tuples
"""

from __future__ import annotations

import math
import random

# ---------------------------------------------------------------------------
# Feature definitions
# ---------------------------------------------------------------------------

# 'vi_eff' = vi_point if present, else vi_lb_bound  (synthetic, resolved in _bo_row)
# 'pour_point_eff' = pour_point if present, else pour_point_ub
BO_FEATURE_COLS: tuple[str, ...] = (
    "kv100",
    "kv40",
    "vi_eff",
    "density_kg_m3",
    "api_group_ord",
    "sulfur_wt_pct",
    "pour_point_eff",
)

AP_FEATURE_COLS: tuple[str, ...] = (
    "tbn",
    "sulfated_ash",
    "ca",
    "zn",
    "p",
    "density_kg_m3",
    "zn_p_sum",
    "ca_tbn_ratio",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _f(s) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _bo_row(row: dict) -> list[float | None]:
    vi_pt = _f(row.get("vi_point"))
    vi_lb = _f(row.get("vi_lb_bound"))
    vi_eff = vi_pt if vi_pt is not None else vi_lb

    pp = _f(row.get("pour_point"))
    pp_ub = _f(row.get("pour_point_ub"))
    pp_eff = pp if pp is not None else pp_ub

    return [
        _f(row.get("kv100")),
        _f(row.get("kv40")),
        vi_eff,
        _f(row.get("density_kg_m3")),
        _f(row.get("api_group_ord")),
        _f(row.get("sulfur_wt_pct")),
        pp_eff,
    ]


def _ap_row(row: dict) -> list[float | None]:
    return [
        _f(row.get("tbn")),
        _f(row.get("sulfated_ash")),
        _f(row.get("ca")),
        _f(row.get("zn")),
        _f(row.get("p")),
        _f(row.get("density_kg_m3")),
        _f(row.get("zn_p_sum")),
        _f(row.get("ca_tbn_ratio")),
    ]


# ---------------------------------------------------------------------------
# Feature extraction
# ---------------------------------------------------------------------------

def feature_matrix(rows: list[dict], kind: str) -> list[list[float | None]]:
    """Extract a feature matrix from CSV row-dicts.

    kind must be 'bo' or 'ap'.
    Returns one vector per row; values may be None for missing features.
    """
    if kind == "bo":
        return [_bo_row(r) for r in rows]
    if kind == "ap":
        return [_ap_row(r) for r in rows]
    raise ValueError(f"Unknown kind: {kind!r}")


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

def _col_stats(matrix: list[list[float | None]]) -> list[tuple[float, float, float]]:
    """Return (mean, min, max) per column, ignoring None values."""
    if not matrix:
        return []
    n_cols = len(matrix[0])
    out = []
    for j in range(n_cols):
        vals = [row[j] for row in matrix if row[j] is not None]
        if not vals:
            out.append((0.0, 0.0, 1.0))
        else:
            mean = sum(vals) / len(vals)
            out.append((mean, min(vals), max(vals)))
    return out


def normalise(
    matrix: list[list[float | None]],
) -> tuple[
    list[list[float | None]],        # norm_none: scaled [0,1], None preserved
    list[list[float]],               # norm_imp:  scaled [0,1], None → 0.5
    list[tuple[float, float, float]],# stats: (mean, min, max) per column
]:
    """Min-max scale each column to [0, 1].

    Returns two matrices:
      norm_none  — Nones preserved; used for pairwise cosine.
      norm_imp   — Nones replaced with 0.5 (midpoint); used for k-means.
    """
    stats = _col_stats(matrix)
    norm_none: list[list[float | None]] = []
    norm_imp:  list[list[float]]        = []

    for row in matrix:
        rn: list[float | None] = []
        ri: list[float]        = []
        for j, v in enumerate(row):
            _, lo, hi = stats[j]
            rng = hi - lo
            if v is None:
                rn.append(None)
                ri.append(0.5)
            elif rng == 0.0:
                rn.append(0.0)
                ri.append(0.0)
            else:
                scaled = (v - lo) / rng
                rn.append(scaled)
                ri.append(scaled)
        norm_none.append(rn)
        norm_imp.append(ri)

    return norm_none, norm_imp, stats


# ---------------------------------------------------------------------------
# Similarity and distance
# ---------------------------------------------------------------------------

def cosine_sim(
    a: list[float | None],
    b: list[float | None],
) -> tuple[float | None, int]:
    """Cosine similarity using only dimensions where both a[i] and b[i] are non-None.

    Returns (similarity, n_shared_dims).
    Returns (None, n_shared) when n_shared < 2 or either vector is zero.
    """
    dot = sq_a = sq_b = 0.0
    n = 0
    for ai, bi in zip(a, b):
        if ai is None or bi is None:
            continue
        dot  += ai * bi
        sq_a += ai * ai
        sq_b += bi * bi
        n    += 1
    if n < 2 or sq_a == 0.0 or sq_b == 0.0:
        return None, n
    return dot / (math.sqrt(sq_a) * math.sqrt(sq_b)), n


def euclidean(a: list[float], b: list[float]) -> float:
    """Euclidean distance between two fully-numeric vectors."""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))


# ---------------------------------------------------------------------------
# Pairwise similarity matrix
# ---------------------------------------------------------------------------

def pairwise_cosine(
    norm_none: list[list[float | None]],
) -> list[list[float | None]]:
    """Return N×N symmetric cosine similarity matrix.

    Diagonal is 1.0.  Off-diagonal is None where insufficient shared dimensions.
    """
    n = len(norm_none)
    sim: list[list[float | None]] = [[None] * n for _ in range(n)]
    for i in range(n):
        sim[i][i] = 1.0
        for j in range(i + 1, n):
            s, _ = cosine_sim(norm_none[i], norm_none[j])
            sim[i][j] = s
            sim[j][i] = s
    return sim


def top_pairs(
    sim: list[list[float | None]],
    ids: list[str],
    n: int = 50,
) -> list[dict]:
    """Return up to n most similar pairs (upper triangle, no diagonal), descending."""
    pairs = []
    for i in range(len(sim)):
        for j in range(i + 1, len(sim)):
            s = sim[i][j]
            if s is not None:
                pairs.append({"id_a": ids[i], "id_b": ids[j], "similarity": round(s, 6)})
    pairs.sort(key=lambda p: p["similarity"], reverse=True)
    return pairs[:n]


# ---------------------------------------------------------------------------
# K-means (Lloyd's algorithm with k-means++ initialisation)
# ---------------------------------------------------------------------------

def _kpp_init(
    matrix: list[list[float]],
    k: int,
    rng: random.Random,
) -> list[list[float]]:
    n = len(matrix)
    idx = rng.randrange(n)
    centroids = [matrix[idx][:]]
    for _ in range(k - 1):
        dists = [min(euclidean(row, c) ** 2 for c in centroids) for row in matrix]
        total = sum(dists)
        if total == 0.0:
            centroids.append(matrix[rng.randrange(n)][:])
            continue
        threshold = rng.random() * total
        cumsum = 0.0
        chosen = len(matrix) - 1
        for i, d in enumerate(dists):
            cumsum += d
            if cumsum >= threshold:
                chosen = i
                break
        centroids.append(matrix[chosen][:])
    return centroids


def kmeans(
    matrix: list[list[float]],
    k: int,
    seed: int = 42,
    max_iter: int = 100,
) -> list[int]:
    """Lloyd's k-means with k-means++ initialisation.

    Returns a list of cluster labels (0 … k-1), one per row.
    k is clamped to len(matrix) to avoid empty centroids.
    """
    n = len(matrix)
    if n == 0:
        return []
    k = max(1, min(k, n))
    n_dims = len(matrix[0])
    rng = random.Random(seed)
    centroids = _kpp_init(matrix, k, rng)
    labels = [0] * n

    for _ in range(max_iter):
        new_labels = [
            min(range(k), key=lambda c, row=row: euclidean(row, centroids[c]))
            for row in matrix
        ]
        if new_labels == labels:
            break
        labels = new_labels

        for c in range(k):
            members = [matrix[i] for i, lbl in enumerate(labels) if lbl == c]
            if not members:
                continue
            centroids[c] = [
                sum(row[j] for row in members) / len(members)
                for j in range(n_dims)
            ]

    return labels


# ---------------------------------------------------------------------------
# Silhouette score
# ---------------------------------------------------------------------------

def silhouette_score(matrix: list[list[float]], labels: list[int]) -> float:
    """Mean silhouette coefficient.  Returns 0.0 for a single cluster."""
    clusters: dict[int, list[int]] = {}
    for i, lbl in enumerate(labels):
        clusters.setdefault(lbl, []).append(i)

    unique = list(clusters.keys())
    if len(unique) < 2:
        return 0.0

    scores: list[float] = []
    for i, lbl in enumerate(labels):
        same = [j for j in clusters[lbl] if j != i]
        a = (
            sum(euclidean(matrix[i], matrix[j]) for j in same) / len(same)
            if same else 0.0
        )
        b_vals = [
            sum(euclidean(matrix[i], matrix[j]) for j in clusters[other]) / len(clusters[other])
            for other in unique if other != lbl
        ]
        b = min(b_vals) if b_vals else 0.0
        denom = max(a, b)
        scores.append((b - a) / denom if denom > 0.0 else 0.0)

    return sum(scores) / len(scores) if scores else 0.0


def best_k(
    matrix: list[list[float]],
    ks: tuple[int, ...] = (3, 4, 5, 6),
    seed: int = 42,
) -> tuple[int, dict[int, float]]:
    """Try several k values; return (best_k, {k: silhouette}).

    best_k maximises mean silhouette.  Ties broken by smallest k.
    k values >= len(matrix) are skipped.
    """
    scores: dict[int, float] = {}
    for k in ks:
        if k >= len(matrix):
            continue
        labels = kmeans(matrix, k, seed=seed)
        scores[k] = round(silhouette_score(matrix, labels), 6)
    if not scores:
        return ks[0], {}
    return max(scores, key=lambda k: (scores[k], -k)), scores
