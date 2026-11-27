"""
Step 10 — Directed association rule mining for Pipeline B.

Mines rules of the form:
    {base oil properties} -> {additive package properties}

Each (bo, ap) candidate pair is a "transaction".  Antecedent items are drawn
from the base oil side (grade, API group); consequent items from the package
side (package type, TBN band).  Support, confidence and lift are computed by
direct enumeration over the item space — no Apriori candidate generation is
needed because the item space is small.

TBN bands (mg KOH/g)
---------------------
  low    :  TBN < 70
  medium :  70 <= TBN <= 100
  high   :  TBN > 100

Public API
----------
discretise_bo(row)                       -> frozenset[str]
discretise_ap(row)                       -> frozenset[str]
mine_rules(transactions, min_sup, min_conf, max_ant, max_con)
                                         -> list[dict]
"""

from __future__ import annotations

import itertools

# ---------------------------------------------------------------------------
# TBN discretisation thresholds
# ---------------------------------------------------------------------------

TBN_LOW_MAX:  float = 70.0   # TBN < 70  → "tbn_low"
TBN_HIGH_MIN: float = 100.0  # TBN > 100 → "tbn_high"

# ---------------------------------------------------------------------------
# Item vocabularies (used by enumerate_antecedents / enumerate_consequents)
# ---------------------------------------------------------------------------

_GRADE_ITEMS:   tuple[str, ...] = ("grade_30", "grade_40", "grade_50")
_API_ITEMS:     tuple[str, ...] = (
    "api_I", "api_II", "api_IIp", "api_III", "api_IV", "api_V", "api_unk",
)
_PKG_ITEMS:     tuple[str, ...] = (
    "pkg_hdeo", "pkg_pceo", "pkg_universal", "pkg_gear", "pkg_atf",
    "pkg_other", "pkg_unk",
)
_TBN_ITEMS:     tuple[str, ...] = ("tbn_low", "tbn_med", "tbn_high", "tbn_unk")

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


_API_ITEM_MAP: dict[str, str] = {
    "Group I":   "api_I",
    "Group II":  "api_II",
    "Group II+": "api_IIp",
    "Group III": "api_III",
    "Group IV":  "api_IV",
    "Group V":   "api_V",
}

_PKG_ITEM_MAP: dict[str, str] = {
    "hdeo":      "pkg_hdeo",
    "pceo":      "pkg_pceo",
    "universal": "pkg_universal",
    "gear":      "pkg_gear",
    "atf":       "pkg_atf",
    "other":     "pkg_other",
}


# ---------------------------------------------------------------------------
# Discretisation
# ---------------------------------------------------------------------------

def discretise_bo(row: dict) -> frozenset[str]:
    """Convert a base oil row to a frozenset of item strings.

    Items produced (all always present, using _unk / absent sentinel when data
    is missing):
        grade_30 / grade_40 / grade_50          from bo_ht_grade
        api_I / api_II / api_IIp / api_III /
        api_IV / api_V / api_unk                from bo_api_group
    """
    items: set[str] = set()

    # SAE high-temp grade
    grade = (row.get("bo_ht_grade") or row.get("ht_grade") or "").strip()
    if grade in ("30", "40", "50"):
        items.add(f"grade_{grade}")

    # API group
    ag = (row.get("bo_api_group") or row.get("api_group") or "").strip()
    items.add(_API_ITEM_MAP.get(ag, "api_unk"))

    return frozenset(items)


def discretise_ap(row: dict) -> frozenset[str]:
    """Convert an additive package row to a frozenset of item strings.

    Items produced:
        pkg_hdeo / pkg_pceo / pkg_universal /
        pkg_gear / pkg_atf / pkg_other / pkg_unk  from ap_package_type
        tbn_low / tbn_med / tbn_high / tbn_unk     from ap_tbn
    """
    items: set[str] = set()

    # Package type
    pt = (row.get("ap_package_type") or row.get("package_type_canon") or "").strip()
    items.add(_PKG_ITEM_MAP.get(pt, "pkg_unk"))

    # TBN band
    tbn = _f(row.get("ap_tbn") or row.get("tbn"))
    if tbn is None:
        items.add("tbn_unk")
    elif tbn < TBN_LOW_MAX:
        items.add("tbn_low")
    elif tbn <= TBN_HIGH_MIN:
        items.add("tbn_med")
    else:
        items.add("tbn_high")

    return frozenset(items)


# ---------------------------------------------------------------------------
# Antecedent / consequent enumeration
# ---------------------------------------------------------------------------

def _subsets_up_to(items: tuple[str, ...], max_size: int) -> list[frozenset[str]]:
    """All non-empty subsets of *items* with size <= max_size."""
    result: list[frozenset[str]] = []
    for size in range(1, max_size + 1):
        for combo in itertools.combinations(items, size):
            result.append(frozenset(combo))
    return result


def enumerate_antecedents(max_size: int = 2) -> list[frozenset[str]]:
    """All grade × api antecedent combinations up to max_size items.

    Each antecedent contains at most one grade item and at most one api item,
    so we cross the two vocabularies rather than taking arbitrary subsets.
    """
    result: list[frozenset[str]] = []
    # size-1: single grade or single api
    for item in (*_GRADE_ITEMS, *_API_ITEMS):
        result.append(frozenset([item]))
    # size-2: one grade + one api (if max_size >= 2)
    if max_size >= 2:
        for g in _GRADE_ITEMS:
            for a in _API_ITEMS:
                result.append(frozenset([g, a]))
    return result


def enumerate_consequents(max_size: int = 2) -> list[frozenset[str]]:
    """All pkg × tbn consequent combinations up to max_size items."""
    result: list[frozenset[str]] = []
    for item in (*_PKG_ITEMS, *_TBN_ITEMS):
        result.append(frozenset([item]))
    if max_size >= 2:
        for p in _PKG_ITEMS:
            for t in _TBN_ITEMS:
                result.append(frozenset([p, t]))
    return result


# ---------------------------------------------------------------------------
# Rule mining
# ---------------------------------------------------------------------------

def mine_rules(
    transactions: list[tuple[frozenset[str], frozenset[str]]],
    min_support:    float = 0.05,
    min_confidence: float = 0.50,
    max_ant:        int   = 2,
    max_con:        int   = 2,
) -> list[dict]:
    """Mine directed association rules: antecedent (BO) → consequent (AP).

    Parameters
    ----------
    transactions   List of (bo_items, ap_items) frozenset pairs.
    min_support    Minimum support (fraction of all pairs), default 5%.
    min_confidence Minimum confidence, default 50%.
    max_ant        Maximum antecedent size (1 or 2).
    max_con        Maximum consequent size (1 or 2).

    Returns
    -------
    List of rule dicts, sorted by lift descending:
        antecedent  frozenset[str]
        consequent  frozenset[str]
        support     float
        confidence  float
        lift        float
        count       int   (number of pairs satisfying ant ∪ con)
        count_ant   int   (number of pairs satisfying antecedent alone)
    """
    n = len(transactions)
    if n == 0:
        return []

    antecedents = enumerate_antecedents(max_ant)
    consequents = enumerate_consequents(max_con)

    # Pre-count consequent frequencies (for lift denominator)
    con_counts: dict[frozenset[str], int] = {}
    for con in consequents:
        con_counts[con] = sum(1 for _, ap in transactions if con <= ap)

    rules: list[dict] = []
    for ant in antecedents:
        ant_pairs = [(bo, ap) for bo, ap in transactions if ant <= bo]
        count_ant = len(ant_pairs)
        if count_ant == 0:
            continue

        for con in consequents:
            count = sum(1 for _, ap in ant_pairs if con <= ap)
            support = count / n
            if support < min_support:
                continue
            confidence = count / count_ant
            if confidence < min_confidence:
                continue
            count_con = con_counts.get(con, 0)
            base_rate = count_con / n if n > 0 else 0.0
            lift = confidence / base_rate if base_rate > 0.0 else 0.0

            rules.append({
                "antecedent": ant,
                "consequent": con,
                "support":    round(support,    4),
                "confidence": round(confidence, 4),
                "lift":       round(lift,       4),
                "count":      count,
                "count_ant":  count_ant,
            })

    rules.sort(key=lambda r: (-r["lift"], -r["confidence"], -r["support"]))
    return rules
