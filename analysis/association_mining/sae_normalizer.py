"""
SAE viscosity grade normalization for Pipeline B.

Maps the 33 raw grade strings observed in sae_grades_documented to canonical
forms.  Categories:
  - Multi-grade (e.g. 15W-40, 10W-30) → canonical xW-yy string
  - Mono-grade (e.g. 40, SAE 30) → canonical SAE-less integer string
  - Broad category (Multi, Mono, all monogrades, …) → category token

Normalization is case-insensitive and strips the 'SAE ' prefix.
Separator variants ('-', '/', '') for multi-grades are all collapsed to '-'.
"""

import re

# ---------------------------------------------------------------------------
# Canonical grade names
# ---------------------------------------------------------------------------
MULTIGRADE_PATTERN = re.compile(
    r"(?:SAE\s*)?(\d+)[Ww][-/]?(\d+)",
    re.IGNORECASE,
)
MONOGRADE_PATTERN = re.compile(
    r"(?:SAE\s*)?(\d+)$",
    re.IGNORECASE,
)

# Category tokens for non-specific entries
CAT_MULTI  = "multi-grade"
CAT_MONO   = "mono-grade"
CAT_UNKNOWN = None   # unrecognised string

# Explicit overrides for strings the regex cannot parse
_OVERRIDES: dict[str, str | None] = {
    "Multi-grade":   CAT_MULTI,
    "Multi":         CAT_MULTI,
    "MULTI":         CAT_MULTI,
    "multi-grades":  CAT_MULTI,
    "Mono-grade":    CAT_MONO,
    "Mono":          CAT_MONO,
    "MONO":          CAT_MONO,
    "mono-grades":   CAT_MONO,
    "Mono grade":    CAT_MONO,
    "all monogrades": CAT_MONO,
}


def normalize_grade(raw: str | None) -> str | None:
    """Return the canonical SAE grade string for *raw*.

    Returns:
        'xW-yy'   for a multi-grade (e.g. '15W-40', '10W-30')
        'yy'      for a mono-grade (e.g. '40', '30')
        'multi-grade' or 'mono-grade' for broad category strings
        None      for unrecognised input
    """
    if raw is None:
        return None
    raw_stripped = raw.strip()
    if raw_stripped in _OVERRIDES:
        return _OVERRIDES[raw_stripped]

    m = MULTIGRADE_PATTERN.fullmatch(raw_stripped)
    if m:
        w, hi = m.group(1), m.group(2)
        return f"{w}W-{hi}"

    m = MONOGRADE_PATTERN.fullmatch(raw_stripped)
    if m:
        return m.group(1)

    # Fallback: strip 'SAE ' prefix and retry once
    stripped = re.sub(r"^SAE\s*", "", raw_stripped, flags=re.IGNORECASE).strip()
    if stripped != raw_stripped:
        return normalize_grade(stripped)

    return CAT_UNKNOWN


def normalize_grades(raw_list: list[str | None]) -> list[str]:
    """Normalize a list of raw grade strings; silently drops None results."""
    out = []
    for g in raw_list:
        c = normalize_grade(g)
        if c is not None:
            out.append(c)
    return out


def canonical_grades() -> frozenset[str]:
    """Return the set of all canonical grade strings inferred from observed data."""
    observed = [
        "15W-40", "10W-30", "10W-40", "20W-50", "15W-50",
        "5W-30", "20W-40",
        "40", "50", "30",
        CAT_MULTI, CAT_MONO,
    ]
    return frozenset(observed)
