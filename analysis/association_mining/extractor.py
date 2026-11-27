"""
Step 4 — Structured table extractor for Pipeline B.

Reads Products_json via group_by_product() and produces flat row dicts
for three output tables:
  - base_oil     : one row per product, Tier 1-3 properties
  - additive_pkg : one row per product, Tier 1-2 properties + element profile
  - treat_rate   : one row per (package × SAE-grade × claim) tuple

Design rules:
  - Products_json is never modified.
  - value_final, unit_final, integration_flags keys are explicitly excluded.
  - Each numeric column is encoded via EncodedValue (point, lb, ub, vk, unit, src).
  - Density columns carry the measurement temperature as a separate column.
  - Conflicts are propagated per field, not rolled up silently.
  - SAE grades are normalised via sae_normalizer before storage.
  - Mo ppm is flagged but not silently converted (conversion registered in unit_registry).
"""

from __future__ import annotations

import pathlib
from typing import Any

from analysis.association_mining.record_key import (
    TierGroup, group_by_product, strip_tier_suffix,
)
from analysis.association_mining.value_kind import encode_value_object, EncodedValue
from analysis.association_mining.unit_registry import normalize_unit, needs_conversion
from analysis.association_mining.sae_normalizer import normalize_grade

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

# Keys never extracted from value objects
_SKIP_KEYS = frozenset({"value_final", "unit_final", "integration_flags"})


def _field_conflicts(conflicts_list: list[dict], field_name: str) -> list[dict]:
    """Return conflict entries that name *field_name* (or whose field is None).

    Skips non-dict entries (some JSON files store free-text strings in conflicts[]).
    """
    out = []
    for c in conflicts_list:
        if not isinstance(c, dict):
            continue
        f = c.get("field") or ""
        if f in (field_name, "", "?") or f.endswith(f".{field_name}"):
            out.append(c)
    return out


def _extract_vo(
    vo: dict | None,
    field_name: str,
    conflicts: list[dict],
) -> dict[str, Any]:
    """
    Extract columns from a standard value object.

    Returns a dict with keys: {field_name}, {field_name}_lb, {field_name}_ub,
    {field_name}_vk, {field_name}_unit, {field_name}_src, {field_name}_conflict.
    All values are None / False when the field is missing or status ≠ Reported/Calculated.
    """
    p = field_name
    null = {
        p: None, f"{p}_lb": None, f"{p}_ub": None,
        f"{p}_vk": None, f"{p}_unit": None, f"{p}_src": None, f"{p}_conflict": False,
    }
    if vo is None:
        return null

    fc = _field_conflicts(conflicts, field_name)
    enc: EncodedValue | None = encode_value_object(vo, field_conflicts=fc)
    if enc is None:
        return null

    unit_canon = normalize_unit(enc.unit)
    return {
        p:               enc.value,
        f"{p}_lb":       enc.lb,
        f"{p}_ub":       enc.ub,
        f"{p}_vk":       enc.vk,
        f"{p}_unit":     unit_canon,
        f"{p}_src":      _short_src(enc.source_file),
        f"{p}_conflict": enc.conflict_flag,
    }


def _extract_density(
    vo: dict | None,
    prefix: str,
    conflicts: list[dict],
) -> dict[str, Any]:
    """Like _extract_vo but preserves test_temperature_c as a separate column."""
    base = _extract_vo(vo, prefix, conflicts)
    temp = None
    if vo is not None:
        raw_t = vo.get("test_temperature_c")
        if raw_t is not None:
            try:
                temp = float(raw_t)
            except (TypeError, ValueError):
                pass
    base[f"{prefix}_temp_c"] = temp
    # Flag when the printed unit needs a numerical conversion to reach kg/m³
    base[f"{prefix}_needs_conv"] = needs_conversion(vo.get("unit") if vo else None)
    return base


def _short_src(path: str | None) -> str | None:
    """Abbreviate a source file path to its basename."""
    if not path:
        return None
    return pathlib.Path(path).name if "/" not in path.replace("\\", "/")[:-1] else path


def _get_text_field(fields: dict, key: str) -> str | None:
    """Extract the value from a simple text value object (status not checked)."""
    vo = fields.get(key, {})
    if not isinstance(vo, dict):
        return None
    v = vo.get("value")
    return str(v).strip() if v else None


# ---------------------------------------------------------------------------
# Base oil extractor
# ---------------------------------------------------------------------------

BO_ELEM_COLS: list[str] = []  # base oils have no element fields


def extract_base_oil(group: TierGroup) -> dict[str, Any] | None:
    """Return a flat row dict for one base oil product, or None on failure."""
    t1 = group.load_tier(1)
    t2 = group.load_tier(2)
    t3 = group.load_tier(3)
    if t1 is None:
        return None  # Tier 1 is mandatory

    record_id_raw = t1.get("record_id", "")
    conflicts_all: list[dict] = []
    for td in (t1, t2, t3):
        if td:
            conflicts_all.extend(td.get("conflicts", []))

    f1 = t1.get("fields", {})
    f2 = (t2 or {}).get("fields", {})
    f3 = (t3 or {}).get("fields", {})

    row: dict[str, Any] = {
        "product_key":   str(group.key),
        "supplier":      group.key.supplier,
        "product_id":    group.key.product_id,
        "record_id":     strip_tier_suffix(record_id_raw),
        "tiers_present": ",".join(str(t) for t in sorted(group.tiers)),
        "n_conflicts":   len(conflicts_all),
    }

    # --- T1: api_group and chemistry ---
    agc = f1.get("api_group_chemistry", {})
    row["api_group"] = _get_text_field(agc, "api_group") if isinstance(agc, dict) else None
    row["chemistry"]  = _get_text_field(agc, "chemistry") if isinstance(agc, dict) else None

    # --- T1: kv40, kv100, viscosity_index, density ---
    for prop in ("kv40", "kv100"):
        row.update(_extract_vo(f1.get(prop), prop, conflicts_all))
    row.update(_extract_vo(f1.get("viscosity_index"), "vi", conflicts_all))
    row.update(_extract_density(f1.get("density"), "density_t1", conflicts_all))

    # --- T2: flash_point, pour_point, noack_volatility, specific_gravity ---
    row.update(_extract_vo(f2.get("flash_point"), "flash_point", conflicts_all))
    row.update(_extract_vo(f2.get("pour_point"), "pour_point", conflicts_all))
    row.update(_extract_vo(f2.get("noack_volatility"), "noack", conflicts_all))
    row.update(_extract_vo(f2.get("specific_gravity"), "specific_gravity", conflicts_all))
    # density may also appear in T2 for some products
    if f2.get("density"):
        row.update(_extract_density(f2.get("density"), "density_t2", conflicts_all))
    else:
        for col in ("density_t2", "density_t2_lb", "density_t2_ub", "density_t2_vk",
                    "density_t2_unit", "density_t2_src", "density_t2_conflict",
                    "density_t2_temp_c", "density_t2_needs_conv"):
            row[col] = None

    # --- T3: sulfur, saturates, aromatics (cloud_point/wax_content excluded: 0% coverage) ---
    row.update(_extract_vo(f3.get("sulfur"), "sulfur", conflicts_all))
    row.update(_extract_vo(f3.get("saturates"), "saturates", conflicts_all))
    row.update(_extract_vo(f3.get("aromatics"), "aromatics", conflicts_all))

    return row


# ---------------------------------------------------------------------------
# Additive package extractor
# ---------------------------------------------------------------------------

AP_ELEMENTS: list[str] = ["Ca", "Zn", "P", "N", "S", "Mg", "Mo", "B"]


def extract_additive_package(group: TierGroup) -> dict[str, Any] | None:
    """Return a flat row dict for one additive package, or None on failure."""
    t1 = group.load_tier(1)
    t2 = group.load_tier(2)
    if t1 is None:
        return None

    record_id_raw = t1.get("record_id", "")
    conflicts_all: list[dict] = []
    for td in (t1, t2):
        if td:
            conflicts_all.extend(td.get("conflicts", []))

    f1 = t1.get("fields", {})
    f2 = (t2 or {}).get("fields", {})

    row: dict[str, Any] = {
        "product_key":   str(group.key),
        "supplier":      group.key.supplier,
        "product_id":    group.key.product_id,
        "record_id":     strip_tier_suffix(record_id_raw),
        "tiers_present": ",".join(str(t) for t in sorted(group.tiers)),
        "n_conflicts":   len(conflicts_all),
    }

    # --- T1 categorical ---
    pat = f1.get("package_type_application", {})
    row["package_type"]     = _get_text_field(pat, "package_type") if isinstance(pat, dict) else None
    row["intended_service"] = _get_text_field(pat, "intended_service") if isinstance(pat, dict) else None

    # --- T1 SAE grades ---
    sae_raw = f1.get("sae_grades_documented", [])
    sae_canon = _extract_sae_grades(sae_raw)
    row["sae_grades_canon"] = "|".join(sae_canon) if sae_canon else None
    row["n_sae_grades"]     = len(sae_canon)

    # --- T1 performance claims ---
    claims_raw = f1.get("performance_claims", [])
    claims_reported = _extract_claims(claims_raw)
    row["performance_claims"] = "|".join(claims_reported) if claims_reported else None
    row["n_performance_claims"] = len(claims_reported)

    # --- T1 treat rate matrix ---
    treat_rows = _extract_treat_rates(f1.get("treat_rate_matrix", []))
    row["n_treat_rate_entries"] = len(treat_rows)
    row["has_treat_rate_data"]  = len(treat_rows) > 0

    # --- T2 numeric ---
    row.update(_extract_vo(f2.get("kv100"), "kv100", conflicts_all))
    row.update(_extract_density(f2.get("density"), "density_t2", conflicts_all))
    row.update(_extract_vo(f2.get("flash_point"), "flash_point", conflicts_all))
    row.update(_extract_vo(f2.get("pour_point"), "pour_point", conflicts_all))
    row.update(_extract_vo(f2.get("tbn"), "tbn", conflicts_all))
    row.update(_extract_vo(f2.get("sulfated_ash"), "sulfated_ash", conflicts_all))

    # --- T2 elements ---
    elements = f2.get("elements", {}) or {}
    for el in AP_ELEMENTS:
        col = el.lower()
        vo = elements.get(el)
        row.update(_extract_vo(vo, col, conflicts_all))
        # Flag Mo ppm unit (needs explicit conversion, not done silently)
        if el == "Mo" and vo:
            row["mo_unit_raw"] = vo.get("unit")
            row["mo_needs_conv"] = needs_conversion(vo.get("unit"))
        else:
            if el == "Mo":
                row["mo_unit_raw"] = None
                row["mo_needs_conv"] = False

    return row


# ---------------------------------------------------------------------------
# Treat rate table extractor (long format: one row per entry)
# ---------------------------------------------------------------------------

def extract_treat_rate_rows(group: TierGroup) -> list[dict[str, Any]]:
    """Return a list of treat-rate row dicts for one additive package."""
    t1 = group.load_tier(1)
    if t1 is None:
        return []
    f1 = t1.get("fields", {})
    entries = f1.get("treat_rate_matrix", [])
    if not entries:
        return []

    out = []
    for entry in entries:
        vo = entry.get("treat_rate_wt_pct", {})
        if not isinstance(vo, dict) or vo.get("status") != "Reported":
            continue
        raw_grade = entry.get("sae_grade")
        grade_canon = normalize_grade(str(raw_grade)) if raw_grade else None
        out.append({
            "product_key":   str(group.key),
            "supplier":      group.key.supplier,
            "product_id":    group.key.product_id,
            "claim":         entry.get("claim"),
            "sae_grade_raw": raw_grade,
            "sae_grade":     grade_canon,
            "treat_rate":    vo.get("value"),
            "treat_rate_unit": vo.get("unit"),
            "printed_text":  vo.get("printed_text"),
            "source_file":   _short_src((vo.get("source") or {}).get("file")),
            "source_page":   (vo.get("source") or {}).get("page"),
        })
    return out


# ---------------------------------------------------------------------------
# List-field helpers
# ---------------------------------------------------------------------------

def _extract_sae_grades(raw_list: list | None) -> list[str]:
    """Return canonical SAE grade strings from sae_grades_documented entries."""
    if not raw_list:
        return []
    out = []
    for entry in raw_list:
        if not isinstance(entry, dict) or entry.get("status") != "Reported":
            continue
        g = entry.get("sae_grade") or entry.get("value")
        if g:
            canon = normalize_grade(str(g))
            if canon:
                out.append(canon)
    return out


def _extract_claims(raw_list: list | None) -> list[str]:
    """Return Reported performance claim designation strings."""
    if not raw_list:
        return []
    out = []
    for entry in raw_list:
        if not isinstance(entry, dict) or entry.get("status") != "Reported":
            continue
        d = entry.get("designation")
        if d:
            out.append(str(d).strip())
    return out


def _extract_treat_rates(raw_list: list | None) -> list[dict]:
    """Return Reported treat rate entries (helper for has_treat_rate_data count)."""
    if not raw_list:
        return []
    return [
        e for e in raw_list
        if isinstance(e, dict)
        and isinstance(e.get("treat_rate_wt_pct"), dict)
        and e["treat_rate_wt_pct"].get("status") == "Reported"
    ]


# ---------------------------------------------------------------------------
# Main extraction entry point
# ---------------------------------------------------------------------------

def extract_all(products_root: pathlib.Path) -> dict[str, list[dict]]:
    """
    Scan Products_json and return three structured tables as lists of row dicts.

    Returns:
        {
            'base_oil':     [row, ...],  # one row per base oil product
            'additive_pkg': [row, ...],  # one row per additive package
            'treat_rate':   [row, ...],  # one row per (pkg × SAE grade × claim)
        }
    """
    groups = group_by_product(products_root)

    bo_rows:   list[dict] = []
    ap_rows:   list[dict] = []
    tr_rows:   list[dict] = []
    errors:    list[str]  = []

    for key, group in sorted(groups.items(), key=lambda kv: str(kv[0])):
        try:
            if key.material_class == "base_oil":
                row = extract_base_oil(group)
                if row:
                    bo_rows.append(row)
            elif key.material_class == "additive_package":
                row = extract_additive_package(group)
                if row:
                    ap_rows.append(row)
                tr_rows.extend(extract_treat_rate_rows(group))
        except Exception as exc:
            errors.append(f"{key}: {exc}")

    if errors:
        import warnings
        for e in errors:
            warnings.warn(f"[extractor] {e}")

    return {
        "base_oil":     bo_rows,
        "additive_pkg": ap_rows,
        "treat_rate":   tr_rows,
    }
