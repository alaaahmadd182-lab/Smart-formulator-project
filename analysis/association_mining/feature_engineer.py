"""
Step 6 — Feature engineering transforms for Pipeline B.

Operates on the CSV row-dicts produced by run_extraction.py and applies:
  1. Density normalisation  — all density values -> kg/m³
  2. Sulfur normalisation   — base oil sulfur -> wt.%
  3. Mo normalisation       — additive package Mo ppm outlier -> wt.%
  4. API group ordinal      — Group I=1 … Group V=5; unknown=None
  5. Package type canonical — 40+ free-text strings -> 6 categories
  6. ZDDP combined feature  — Zn+P sum and Zn/P ratio
  7. Alkalinity ratio       — Ca/TBN

All original columns are preserved; engineering adds new columns.
No source JSON or extracted CSV is modified.
"""

from __future__ import annotations

from analysis.association_mining.unit_registry import (
    convert_value, UNIT_KG_M3, UNIT_MASS_PCT, UNIT_PPM,
)

# ---------------------------------------------------------------------------
# API group ordinal encoding
# ---------------------------------------------------------------------------

API_GROUP_ORD: dict[str, float] = {
    "Group I":   1.0,
    "Group II":  2.0,
    "Group II+": 2.5,
    "Group III": 3.0,
    "Group IV":  4.0,
    "Group V":   5.0,
}

# ---------------------------------------------------------------------------
# Package type canonical categories
# ---------------------------------------------------------------------------

_PKG_KW: dict[str, tuple[str, ...]] = {
    "hdeo": (
        "hdeo", "heavy duty", "heavy-duty", "hdd", "diesel engine",
        "ci-4", "cj-4", "ck-4", "ch-4", "cf-4", "cf-2",
        "ci4", "cj4", "ck4", "ch4", "cf4",
        "heavy duty engine", "diesel",
    ),
    "pceo": (
        "pceo", "passenger car", "gasoline engine", "petrol",
        "api sl", "api sm", "api sn", "api sp",
        "ilsac", "gf-", "passenger",
    ),
    "universal": (
        "universal", "multi-purpose", "multipurpose",
        "multifuel", "mixed fleet",
    ),
    "gear": ("gear", "gl-", "mt-1", "axle"),
    "atf": ("atf", "automatic transmission", "dexron", "mercon", "cvt"),
}

PKG_CATEGORIES = ("hdeo", "pceo", "universal", "gear", "atf", "other", "missing")


def canon_pkg_type(raw: str | None) -> str:
    """Map a free-text package_type string to one of 7 canonical categories."""
    if not raw or not raw.strip():
        return "missing"
    s = raw.lower()
    for cat, kws in _PKG_KW.items():
        if any(kw in s for kw in kws):
            return cat
    return "other"


# ---------------------------------------------------------------------------
# Value helpers
# ---------------------------------------------------------------------------

def _f(s) -> float | None:
    if s in (None, "", "None"):
        return None
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _b(s) -> bool:
    return str(s).lower() in ("true", "1")


def _safe_div(a: float | None, b: float | None) -> float | None:
    if a is None or b is None or b == 0.0:
        return None
    return round(a / b, 6)


def _safe_add(a: float | None, b: float | None) -> float | None:
    if a is None or b is None:
        return None
    return round(a + b, 6)


# ---------------------------------------------------------------------------
# Density unit conversion
# ---------------------------------------------------------------------------

def convert_density(
    value_str, unit_str: str | None, needs_conv_str
) -> tuple[float | None, bool]:
    """Return (density_kg_m3, conversion_applied).

    Returns (value, False) when the unit is already kg/m³.
    Returns (converted_value, True) when a registered conversion exists.
    Returns (None, False) when the value is absent or the unit is unregistered
    (e.g. 'relative density').
    """
    v = _f(value_str)
    if v is None:
        return None, False
    unit = (unit_str or "").strip()
    # Already canonical
    if unit == UNIT_KG_M3:
        return v, False
    # Registered numerical conversion
    if _b(needs_conv_str):
        try:
            return round(convert_value(v, unit, UNIT_KG_M3), 3), True
        except ValueError:
            return None, False
    # needs_conv=False but not kg/m³ (e.g. relative density or no rule)
    return None, False


# ---------------------------------------------------------------------------
# Sulfur unit normalisation (base oil)
# ---------------------------------------------------------------------------

def normalise_sulfur(
    value_str, unit_str: str | None
) -> tuple[float | None, str | None]:
    """Return (sulfur_wt_pct, source_unit).

    Converts ppm -> wt.% (factor 1e-4). Leaves wt.% unchanged.
    Returns (None, None) when value is absent or unit is unrecognised.
    """
    v = _f(value_str)
    if v is None:
        return None, None
    u = (unit_str or "").strip()
    if u == UNIT_PPM:
        return round(v * 1e-4, 7), "ppm"
    if u == UNIT_MASS_PCT:
        return v, "wt.%"
    return None, u or None


# ---------------------------------------------------------------------------
# Base oil row engineering
# ---------------------------------------------------------------------------

def engineer_base_oil_row(row: dict) -> dict:
    """Return a copy of *row* with added feature-engineering columns."""
    out = dict(row)

    # 1. Density -> kg/m³
    d_kg, d_applied = convert_density(
        row.get("density_t1"),
        row.get("density_t1_unit"),
        row.get("density_t1_needs_conv"),
    )
    out["density_kg_m3"]        = d_kg
    out["density_conv_applied"] = d_applied

    # 2. API group ordinal
    ag = (row.get("api_group") or "").strip()
    out["api_group_ord"]   = API_GROUP_ORD.get(ag)
    out["api_group_known"] = ag in API_GROUP_ORD

    # 3. Sulfur -> wt.%
    s_wt, s_src = normalise_sulfur(row.get("sulfur"), row.get("sulfur_unit"))
    out["sulfur_wt_pct"]   = s_wt
    out["sulfur_unit_src"] = s_src

    # 4. VI encoding: separate point from lower bound
    vk = (row.get("vi_vk") or "").strip()
    vi_pt = _f(row.get("vi"))
    vi_lb = _f(row.get("vi_lb"))
    out["vi_point"]     = vi_pt
    out["vi_lb_bound"]  = vi_lb
    if vk == "minimum" and vi_lb is not None:
        out["vi_bound_type"] = "lower_bound"
    elif vk == "range" and vi_lb is not None:
        out["vi_bound_type"] = "range"
    elif vi_pt is not None:
        out["vi_bound_type"] = "point"
    else:
        out["vi_bound_type"] = None

    # 5. Pour point: flag spec/maximum entries (actual value <= reported)
    pp_vk = (row.get("pour_point_vk") or "").strip()
    out["pour_point_is_max"] = pp_vk == "maximum" and _f(row.get("pour_point_ub")) is not None

    return out


def engineer_base_oils(rows: list[dict]) -> list[dict]:
    return [engineer_base_oil_row(r) for r in rows]


# ---------------------------------------------------------------------------
# Additive package row engineering
# ---------------------------------------------------------------------------

def engineer_package_row(row: dict) -> dict:
    """Return a copy of *row* with added feature-engineering columns."""
    out = dict(row)

    # 1. Density -> kg/m³
    d_kg, d_applied = convert_density(
        row.get("density_t2"),
        row.get("density_t2_unit"),
        row.get("density_t2_needs_conv"),
    )
    out["density_kg_m3"]        = d_kg
    out["density_conv_applied"] = d_applied

    # 2. Mo -> wt.%
    # Note: mo_needs_conv=True for both 'ppm' AND 'wt.%' (bidirectional rule in
    # unit_registry).  Only apply the 1e-4 factor when the stored unit is ppm.
    mo_val  = _f(row.get("mo"))
    mo_unit = (row.get("mo_unit") or "").strip()
    if mo_val is None:
        out["mo_wt_pct"]       = None
        out["mo_conv_applied"] = False
    elif mo_unit == UNIT_PPM:
        out["mo_wt_pct"]       = round(mo_val * 1e-4, 7)
        out["mo_conv_applied"] = True
    else:
        out["mo_wt_pct"]       = mo_val
        out["mo_conv_applied"] = False

    # 3. Package type canonical
    out["package_type_canon"] = canon_pkg_type(row.get("package_type"))

    # 4. ZDDP combined feature (Zn and P are always co-added in ZDDP)
    zn = _f(row.get("zn"))
    p  = _f(row.get("p"))
    out["zn_p_sum"]   = _safe_add(zn, p)
    out["zn_p_ratio"] = _safe_div(zn, p)

    # 5. Ca/TBN alkalinity ratio
    ca  = _f(row.get("ca"))
    tbn = _f(row.get("tbn"))
    out["ca_tbn_ratio"] = _safe_div(ca, tbn)

    return out


def engineer_packages(rows: list[dict]) -> list[dict]:
    return [engineer_package_row(r) for r in rows]
