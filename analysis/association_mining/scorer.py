"""
Step 9 — Formulation candidate scoring for Pipeline B.

Assigns a composite 0-100 score to each (base oil, additive package) candidate
pair from run_compatibility.py so formulators can prioritise which combinations
to investigate first.

Score components (weights sum to 1.0)
--------------------------------------
  treat_rate    (0.30)  Treat rate available for the matched SAE grade
  api_group     (0.25)  API group quality of the base oil
  bo_complete   (0.20)  Fraction of key Tier 1 BO properties present
  ap_complete   (0.15)  Fraction of key AP element/property fields present
  pkg_type      (0.10)  Package type is a known category (not 'other'/'missing')

Final score = weighted sum × 100, rounded to 1 d.p.

Public API
----------
api_group_score(api_group)          -> float [0, 1]
treat_rate_score(treat_rate_med)    -> float [0, 1]
bo_completeness_score(bo_row)       -> float [0, 1]
ap_completeness_score(ap_row)       -> float [0, 1]
pkg_type_score(package_type_canon)  -> float [0, 1]
score_pair(bo_row, ap_row, cand)    -> dict   (all components + 'score')
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

WEIGHTS: dict[str, float] = {
    "treat_rate": 0.30,
    "api_group":  0.25,
    "bo_complete": 0.20,
    "ap_complete": 0.15,
    "pkg_type":    0.10,
}

# ---------------------------------------------------------------------------
# API group quality scores
# ---------------------------------------------------------------------------

_API_SCORES: dict[str, float] = {
    "Group I":   0.40,
    "Group II":  0.70,
    "Group II+": 0.80,
    "Group III": 0.90,
    "Group IV":  1.00,
    "Group V":   0.60,   # specialty; score depends on application
}

# ---------------------------------------------------------------------------
# Key property columns used for completeness checks
# ---------------------------------------------------------------------------

_BO_KEY_COLS: tuple[str, ...] = (
    "kv40", "kv100", "vi_point", "density_kg_m3",
    "api_group_ord", "pour_point",
)

_AP_KEY_COLS: tuple[str, ...] = (
    "tbn", "ca", "zn", "p", "density_kg_m3",
)

# Package types that have enough domain specificity to be useful
_KNOWN_PKG_TYPES: frozenset[str] = frozenset(
    {"hdeo", "pceo", "universal", "gear", "atf"}
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


# ---------------------------------------------------------------------------
# Individual scoring functions
# ---------------------------------------------------------------------------

def api_group_score(api_group: str | None) -> float:
    """Score the API group quality of a base oil.

    Group IV (PAO) = 1.0, Group III = 0.9, Group II = 0.7, etc.
    Unknown or missing = 0.3.
    """
    if not api_group or not api_group.strip():
        return 0.3
    return _API_SCORES.get(api_group.strip(), 0.3)


def treat_rate_score(treat_rate_med: str | float | None) -> float:
    """Score treat-rate availability.

    1.0 when a median treat rate is present (data is actionable),
    0.0 when absent.
    """
    return 1.0 if _f(treat_rate_med) is not None else 0.0


def bo_completeness_score(bo_row: dict) -> float:
    """Fraction of key Tier 1 base oil properties present."""
    if not bo_row:
        return 0.0
    present = sum(1 for col in _BO_KEY_COLS if _f(bo_row.get(col)) is not None)
    return present / len(_BO_KEY_COLS)


def ap_completeness_score(ap_row: dict) -> float:
    """Fraction of key additive package properties present."""
    if not ap_row:
        return 0.0
    present = sum(1 for col in _AP_KEY_COLS if _f(ap_row.get(col)) is not None)
    return present / len(_AP_KEY_COLS)


def pkg_type_score(package_type_canon: str | None) -> float:
    """1.0 when the package type is a known category, 0.0 when 'other' or 'missing'."""
    if not package_type_canon or package_type_canon.strip() not in _KNOWN_PKG_TYPES:
        return 0.0
    return 1.0


# ---------------------------------------------------------------------------
# Composite scorer
# ---------------------------------------------------------------------------

def score_pair(
    bo_row:  dict,
    ap_row:  dict,
    cand:    dict,
) -> dict:
    """Compute all score components and the final 0-100 composite score.

    Parameters
    ----------
    bo_row   Row from bo_ml.csv for this base oil.
    ap_row   Row from ap_ml.csv for this additive package.
    cand     Row from formulation_candidates.csv.

    Returns
    -------
    dict with keys:
        score_treat_rate, score_api_group, score_bo_complete,
        score_ap_complete, score_pkg_type, score  (0-100, 1 d.p.)
    """
    s_tr  = treat_rate_score(cand.get("treat_rate_pct_med"))
    s_ag  = api_group_score(bo_row.get("api_group") or cand.get("bo_api_group"))
    s_boc = bo_completeness_score(bo_row)
    s_apc = ap_completeness_score(ap_row)
    s_pt  = pkg_type_score(ap_row.get("package_type_canon") or cand.get("ap_package_type"))

    composite = (
        WEIGHTS["treat_rate"]  * s_tr
        + WEIGHTS["api_group"] * s_ag
        + WEIGHTS["bo_complete"] * s_boc
        + WEIGHTS["ap_complete"] * s_apc
        + WEIGHTS["pkg_type"]  * s_pt
    ) * 100.0

    return {
        "score_treat_rate":  round(s_tr,  4),
        "score_api_group":   round(s_ag,  4),
        "score_bo_complete": round(s_boc, 4),
        "score_ap_complete": round(s_apc, 4),
        "score_pkg_type":    round(s_pt,  4),
        "score":             round(composite, 1),
    }
