"""
Step 5 — EDA analysis functions for Pipeline B.

Operates on the CSV outputs produced by run_extraction.py.
Returns plain Python dicts/lists ready for JSON serialisation.
No external dependencies — stdlib only.
"""

from __future__ import annotations

import csv
import math
import collections
import pathlib


# ---------------------------------------------------------------------------
# CSV reader
# ---------------------------------------------------------------------------

def load(path: str | pathlib.Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _f(s: str | None) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _b(s: str | None) -> bool:
    return s in ("True", "true", "1")


# ---------------------------------------------------------------------------
# Descriptive statistics
# ---------------------------------------------------------------------------

def describe(rows: list[dict], col: str) -> dict:
    vals = [v for v in (_f(r.get(col)) for r in rows) if v is not None]
    n = len(vals)
    if n == 0:
        return {"col": col, "n": 0, "n_total": len(rows)}
    s = sorted(vals)
    mu = sum(vals) / n
    var = sum((x - mu) ** 2 for x in vals) / (n - 1) if n > 1 else 0.0
    sd = math.sqrt(var)
    def pct(p: float) -> float:
        idx = (n - 1) * p / 100
        lo, hi = int(idx), min(int(idx) + 1, n - 1)
        return s[lo] + (s[hi] - s[lo]) * (idx - lo)
    return {
        "col": col, "n": n, "n_total": len(rows),
        "pct_present": round(100 * n / len(rows), 1),
        "mean": round(mu, 4),
        "median": round(pct(50), 4),
        "std": round(sd, 4),
        "min": round(s[0], 4),
        "q25": round(pct(25), 4),
        "q75": round(pct(75), 4),
        "max": round(s[-1], 4),
    }


def pearson(rows: list[dict], cx: str, cy: str,
            log_x: bool = False, log_y: bool = False) -> dict:
    pairs = []
    for r in rows:
        x, y = _f(r.get(cx)), _f(r.get(cy))
        if x is None or y is None:
            continue
        if (log_x or log_y) and (x <= 0 or y <= 0):
            continue
        pairs.append((math.log(x) if log_x else x, math.log(y) if log_y else y))
    n = len(pairs)
    if n < 3:
        return {"n": n, "r": None}
    xs, ys = [p[0] for p in pairs], [p[1] for p in pairs]
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    r = num / (dx * dy) if dx * dy > 0 else None
    return {"n": n, "r": round(r, 4) if r is not None else None}


# ---------------------------------------------------------------------------
# Scatter / histogram data for JS charts
# ---------------------------------------------------------------------------

def scatter_data(rows: list[dict], cx: str, cy: str,
                 color_col: str | None = None,
                 max_points: int = 300) -> dict:
    """Return {points: [{x,y,label},...], color_map: {...}}"""
    pts = []
    for r in rows:
        x, y = _f(r.get(cx)), _f(r.get(cy))
        if x is None or y is None:
            continue
        pt: dict = {"x": x, "y": y}
        if color_col:
            pt["c"] = r.get(color_col) or "unknown"
        pts.append(pt)
    if len(pts) > max_points:
        step = len(pts) / max_points
        pts = [pts[int(i * step)] for i in range(max_points)]
    color_map: dict = {}
    if color_col:
        cats = sorted(set(p["c"] for p in pts))
        palette = ["#2552c0", "#e55a2b", "#167045", "#9b3fa0", "#c08020",
                   "#1b8ca0", "#a02020", "#407020", "#705090", "#204070"]
        color_map = {c: palette[i % len(palette)] for i, c in enumerate(cats)}
    return {"points": pts, "color_map": color_map}


def histogram_data(rows: list[dict], col: str,
                   n_bins: int = 20, log_scale: bool = False) -> dict:
    vals = [v for v in (_f(r.get(col)) for r in rows) if v is not None]
    if not vals:
        return {"bins": [], "counts": []}
    if log_scale:
        pos = [v for v in vals if v > 0]
        if not pos:
            return {"bins": [], "counts": []}
        lo, hi = math.log10(min(pos)), math.log10(max(pos))
        edges = [10 ** (lo + i * (hi - lo) / n_bins) for i in range(n_bins + 1)]
    else:
        lo, hi = min(vals), max(vals)
        w = (hi - lo) / n_bins if hi != lo else 1
        edges = [lo + i * w for i in range(n_bins + 1)]
    counts = [0] * n_bins
    for v in vals:
        for i in range(n_bins):
            if edges[i] <= v < edges[i + 1] or (i == n_bins - 1 and v == edges[-1]):
                counts[i] += 1
                break
    labels = [f"{edges[i]:.3g}–{edges[i+1]:.3g}" for i in range(n_bins)]
    return {"bins": labels, "counts": counts, "edges": [round(e, 4) for e in edges]}


def value_counts(rows: list[dict], col: str, top_n: int = 20) -> list[dict]:
    ctr = collections.Counter(r.get(col) or "Missing" for r in rows)
    return [{"label": k, "count": v} for k, v in ctr.most_common(top_n)]


# ---------------------------------------------------------------------------
# Coverage matrix (supplier × property)
# ---------------------------------------------------------------------------

def coverage_matrix(rows: list[dict], supplier_col: str,
                    props: list[str]) -> dict:
    suppliers = sorted(set(r.get(supplier_col, "") for r in rows))
    result: list[dict] = []
    for sup in suppliers:
        sub = [r for r in rows if r.get(supplier_col) == sup]
        row_data = {"supplier": sup, "n": len(sub)}
        for p in props:
            n_rep = sum(1 for r in sub if _f(r.get(p)) is not None)
            row_data[p] = round(100 * n_rep / len(sub)) if sub else 0
        result.append(row_data)
    return {"matrix": result, "props": props}


# ---------------------------------------------------------------------------
# Main EDA computation
# ---------------------------------------------------------------------------

def run_eda(outputs_dir: str | pathlib.Path) -> dict:
    """Run all EDA computations and return a single JSON-serialisable dict."""
    d = pathlib.Path(outputs_dir)
    bo = load(d / "bo_features.csv")
    ap = load(d / "ap_features.csv")
    tr = load(d / "treat_rate.csv")

    # --- Base oil stats ---
    bo_props = ["kv40", "kv100", "vi", "density_t1",
                "flash_point", "pour_point", "noack", "sulfur"]
    bo_stats = [describe(bo, p) for p in bo_props]

    # --- AP stats ---
    ap_props = ["tbn", "sulfated_ash", "ca", "zn", "p", "n", "s", "mg", "mo",
                "kv100", "density_t2", "flash_point", "pour_point"]
    ap_stats = [describe(ap, p) for p in ap_props]

    # --- Correlations ---
    correlations = [
        {"label": "log(kv40) vs log(kv100)",  "cls": "base_oil",
         **pearson(bo, "kv40", "kv100", log_x=True, log_y=True)},
        {"label": "log(kv100) vs VI",          "cls": "base_oil",
         **pearson(bo, "kv100", "vi", log_x=True)},
        {"label": "log(kv40) vs VI",           "cls": "base_oil",
         **pearson(bo, "kv40", "vi", log_x=True)},
        {"label": "Ca vs TBN",                 "cls": "additive_pkg",
         **pearson(ap, "ca", "tbn")},
        {"label": "Zn vs P",                   "cls": "additive_pkg",
         **pearson(ap, "zn", "p")},
        {"label": "TBN vs Sulfated Ash",        "cls": "additive_pkg",
         **pearson(ap, "tbn", "sulfated_ash")},
        {"label": "Ca vs Zn",                   "cls": "additive_pkg",
         **pearson(ap, "ca", "zn")},
    ]

    # --- Scatter data ---
    kv_scatter = scatter_data(bo, "kv40", "kv100", color_col="api_group")
    kv_vi_scatter = scatter_data(bo, "kv100", "vi", color_col="api_group")

    # --- Histograms ---
    kv40_hist  = histogram_data(bo, "kv40",  n_bins=18, log_scale=True)
    kv100_hist = histogram_data(bo, "kv100", n_bins=18, log_scale=True)
    vi_hist    = histogram_data(bo, "vi",    n_bins=16)
    tbn_hist   = histogram_data(ap, "tbn",   n_bins=12)
    tr_hist    = histogram_data(tr, "treat_rate", n_bins=14)

    # --- Categorical ---
    api_group_vc  = value_counts(bo, "api_group", top_n=10)
    supplier_vc   = value_counts(bo, "supplier",  top_n=15)
    pkg_type_vc   = _normalise_pkg_types(ap)

    # --- Performance claims ---
    all_claims: list[str] = []
    for r in ap:
        c = r.get("performance_claims", "")
        if c:
            all_claims.extend(c.split("|"))
    claims_vc = [{"label": k, "count": v}
                 for k, v in collections.Counter(all_claims).most_common(20)]

    # --- SAE grades ---
    all_grades: list[str] = []
    for r in ap:
        g = r.get("sae_grades_canon", "")
        if g:
            all_grades.extend(g.split("|"))
    grades_vc = [{"label": k, "count": v}
                 for k, v in collections.Counter(all_grades).most_common(15)]

    # --- Value kind summary ---
    vk_summary = {}
    for col in ("kv40_vk", "kv100_vk", "vi_vk", "pour_point_vk",
                "noack_vk", "flash_point_vk"):
        vk_summary[col] = value_counts(bo, col, top_n=8)

    # --- Coverage matrix (base oils) ---
    bo_coverage = coverage_matrix(
        bo, "supplier",
        ["kv40", "kv100", "vi", "density_t1", "flash_point", "pour_point", "noack"],
    )

    # --- Density unit breakdown ---
    bo_density_units = value_counts(bo, "density_t1_unit", top_n=15)
    n_bo_needs_conv  = sum(1 for r in bo if _b(r.get("density_t1_needs_conv")))
    n_bo_density_ok  = sum(1 for r in bo if r.get("density_t1") not in ("", None, "None")
                           and not _b(r.get("density_t1_needs_conv")))

    # --- Treat rate by grade ---
    tr_by_grade = value_counts(tr, "sae_grade", top_n=10)
    tr_vals = [_f(r.get("treat_rate")) for r in tr]
    tr_vals = [v for v in tr_vals if v]

    return {
        "meta": {
            "n_base_oil":     len(bo),
            "n_additive_pkg": len(ap),
            "n_treat_rate":   len(tr),
        },
        "bo_stats":    bo_stats,
        "ap_stats":    ap_stats,
        "correlations": correlations,
        "kv_scatter":   kv_scatter,
        "kv_vi_scatter": kv_vi_scatter,
        "kv40_hist":   kv40_hist,
        "kv100_hist":  kv100_hist,
        "vi_hist":     vi_hist,
        "tbn_hist":    tbn_hist,
        "tr_hist":     tr_hist,
        "api_group_vc": api_group_vc,
        "supplier_vc":  supplier_vc,
        "pkg_type_vc":  pkg_type_vc,
        "claims_vc":    claims_vc,
        "grades_vc":    grades_vc,
        "vk_summary":   vk_summary,
        "bo_coverage":  bo_coverage,
        "density": {
            "bo_unit_counts": bo_density_units,
            "n_needs_conv": n_bo_needs_conv,
            "n_already_kg_m3": n_bo_density_ok,
            "n_total_reported": sum(1 for r in bo if r.get("density_t1") not in ("","None",None)),
        },
        "treat_rate": {
            "by_grade": tr_by_grade,
            "n_rows": len(tr_vals),
            "mean": round(sum(tr_vals) / len(tr_vals), 2) if tr_vals else None,
            "min": round(min(tr_vals), 1) if tr_vals else None,
            "max": round(max(tr_vals), 1) if tr_vals else None,
        },
    }


def _normalise_pkg_types(ap: list[dict]) -> list[dict]:
    """Coerce the 40+ free-text package type strings into ~6 broad categories."""
    def cat(s: str | None) -> str:
        if not s:
            return "Missing"
        s_low = s.lower()
        if any(k in s_low for k in ("ck-4", "cj-4", "ci-4", "ch-4", "cf-4",
                                     "hdeo", "heavy duty", "hdd")):
            return "HDEO (diesel)"
        if "passenger" in s_low or "pceo" in s_low or "gasoline" in s_low:
            return "PCEO (gasoline)"
        if "universal" in s_low or "multi" in s_low:
            return "Universal / multi-purpose"
        if "gear" in s_low:
            return "Gear oil"
        if "atf" in s_low or "automatic" in s_low:
            return "ATF"
        return "Other / unspecified"
    ctr = collections.Counter(cat(r.get("package_type")) for r in ap)
    return [{"label": k, "count": v} for k, v in ctr.most_common()]
