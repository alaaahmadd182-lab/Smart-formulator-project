"""
Step 8 — SAE J300 grade mapping for Pipeline B.

Maps base oil kv100 → SAE high-temp grade and parses package SAE grade strings,
so the compatibility runner can cross-join base oils with additive packages on
shared grades.

SAE J300 (2015) kv100 bands used:
  Grade 20 : 5.6  <= kv100 < 9.3   cSt
  Grade 30 : 9.3  <= kv100 < 12.5  cSt
  Grade 40 : 12.5 <= kv100 < 16.3  cSt
  Grade 50 : 16.3 <= kv100 < 21.9  cSt
  Grade 60 : 21.9 <= kv100          cSt

The winter (W) grade is determined by CCS / MRV low-temperature measurements,
which are not in the current dataset, so only the high-temp grade is mapped here.

Public API
----------
kv100_to_ht_grade(kv100)                -> str | None
parse_package_ht_grades(grades_canon)   -> frozenset[str]
ht_grade_overlap(bo_grades, ap_grades)  -> list[str]
treat_rate_ht_grade(sae_grade_str)      -> str | None
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# SAE J300 kv100 thresholds (monograde high-temp grades)
# ---------------------------------------------------------------------------

# (grade_label, kv100_min_inclusive, kv100_max_exclusive)
HT_BANDS: tuple[tuple[str, float, float], ...] = (
    ("20",  5.6,   9.3),
    ("30",  9.3,  12.5),
    ("40", 12.5,  16.3),
    ("50", 16.3,  21.9),
    ("60", 21.9,  float("inf")),
)

# Ordered list of valid high-temp grade labels (for sorting and validation)
HT_GRADES: tuple[str, ...] = tuple(band[0] for band in HT_BANDS)

# ---------------------------------------------------------------------------
# Base oil grade mapping
# ---------------------------------------------------------------------------

def kv100_to_ht_grade(kv100: float) -> str | None:
    """Map kv100 (cSt at 100 °C) to the SAE J300 high-temp grade label.

    Returns None when kv100 < 5.6 (below SAE 20 lower limit) or when
    kv100 is not a positive finite number.
    """
    if not isinstance(kv100, (int, float)) or kv100 != kv100:  # NaN guard
        return None
    for grade, lo, hi in HT_BANDS:
        if lo <= kv100 < hi:
            return grade
    return None   # < 5.6


# ---------------------------------------------------------------------------
# Package grade parsing
# ---------------------------------------------------------------------------

def parse_package_ht_grades(grades_canon: str | None) -> frozenset[str]:
    """Extract high-temp grade labels from a pipe-separated SAE grade string.

    Examples
    --------
    "10W-30|15W-40"  -> frozenset({"30", "40"})
    "20W-50"         -> frozenset({"50"})
    "SAE 40"         -> frozenset({"40"})
    "multi-grade"    -> frozenset()
    ""               -> frozenset()
    """
    if not grades_canon or not grades_canon.strip():
        return frozenset()

    grades: set[str] = set()
    for token in grades_canon.split("|"):
        token = token.strip()
        # Multi-grade: xW-y  (e.g. "10W-30", "15W-40", "20W-50")
        if "W-" in token:
            ht = token.split("W-", 1)[1].strip()
            if ht in HT_GRADES:
                grades.add(ht)
        else:
            # Monograde or plain number: "SAE 40", "40", "SAE 30"
            digits = token.replace("SAE", "").strip()
            if digits in HT_GRADES:
                grades.add(digits)

    return frozenset(grades)


# ---------------------------------------------------------------------------
# Treat-rate record grade extraction
# ---------------------------------------------------------------------------

def treat_rate_ht_grade(sae_grade_str: str | None) -> str | None:
    """Extract the high-temp grade label from a treat-rate SAE grade string.

    "15W-40" -> "40";  "10W-30" -> "30";  "20W-50" -> "50"
    "mono-grade" / "multi-grade" / "" -> None
    """
    if not sae_grade_str or not sae_grade_str.strip():
        return None
    s = sae_grade_str.strip()
    if "W-" in s:
        ht = s.split("W-", 1)[1].strip()
        return ht if ht in HT_GRADES else None
    if s in HT_GRADES:
        return s
    return None


# ---------------------------------------------------------------------------
# Grade overlap
# ---------------------------------------------------------------------------

def ht_grade_overlap(
    bo_grades: frozenset[str] | set[str],
    ap_grades: frozenset[str] | set[str],
) -> list[str]:
    """Return shared high-temp grade labels, sorted by ascending grade number."""
    shared = set(bo_grades) & set(ap_grades)
    return sorted(shared, key=lambda g: int(g))
