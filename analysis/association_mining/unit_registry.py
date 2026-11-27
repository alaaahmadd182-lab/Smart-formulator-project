"""
Unit string normalization registry for Pipeline B.

Rules:
- String-alias normalization only: variants that mean the same unit with no
  numerical conversion (e.g. cSt == mm²/s, wt% == wt.%).
- Numerical conversions (density g/cm³ → kg/m³, sulfur ppm → wt.%, Mo ppm → wt.%)
  are registered separately in CONVERSION_RULES and are never applied silently.
- Original source JSON is never modified.
- 'not printed' is a data-entry note, not a unit; normalize to None.
- 'wt.% or ppm as printed' on a Missing record stays as-is (no value to convert).
"""

# ---------------------------------------------------------------------------
# Canonical unit names
# ---------------------------------------------------------------------------
UNIT_VISCOSITY = "mm²/s"   # mm²/s  (1 cSt = 1 mm²/s)
UNIT_MASS_PCT  = "wt.%"
UNIT_KG_M3     = "kg/m³"   # kg/m³  (canonical density for base oils)
UNIT_PPM       = "ppm"
UNIT_TEMP_C    = "°C"       # °C  (U+00B0 + C — already stored this way)
UNIT_DIMLESS   = "dimensionless"
UNIT_MG_KOH_G  = "mg KOH/g"
UNIT_MPA_S     = "mPa·s"   # mPa·s  (MRV viscosity)

# ---------------------------------------------------------------------------
# String-alias table  {raw_unit: canonical_unit}
# None canonical means "discard / not a unit string"
# ---------------------------------------------------------------------------
_ALIASES: dict[str, str | None] = {
    # --- Kinematic viscosity (cSt == mm²/s numerically) ---
    "cSt":                   UNIT_VISCOSITY,
    "mm2/s":                 UNIT_VISCOSITY,
    "mm²/s":            UNIT_VISCOSITY,  # mm²/s with superscript 2
    "mm2/sec":               UNIT_VISCOSITY,
    # --- Temperature (already stored as °C, included for completeness) ---
    "°C":               UNIT_TEMP_C,
    "°C":                    UNIT_TEMP_C,
    # --- Mass percent family (string aliases, same scale) ---
    "wt.%":                  UNIT_MASS_PCT,
    "wt%":                   UNIT_MASS_PCT,
    "wt.% loss":             UNIT_MASS_PCT,
    "mass%":                 UNIT_MASS_PCT,
    "mass %":                UNIT_MASS_PCT,
    "%M/M":                  UNIT_MASS_PCT,
    "wt.% as printed":       UNIT_MASS_PCT,
    # Note: '%' alone is ambiguous; kept as-is — caller must decide
    # --- Density string aliases (same magnitude, different notation) ---
    "kg/m3":                 UNIT_KG_M3,
    "kg/m³":            UNIT_KG_M3,       # kg/m³ with superscript 3
    # Non-kg/m³ density variants are NOT aliased here — they require
    # numerical conversion; see CONVERSION_RULES below.
    # --- Sulfur/ppm family (string aliases) ---
    "ppm":                   UNIT_PPM,
    "ppm (wt)":              UNIT_PPM,
    "wt ppm":                UNIT_PPM,
    "mg/kg":                 UNIT_PPM,         # 1 mg/kg == 1 ppm (mass)
    # --- TBN / alkalinity ---
    "mg KOH/g":              UNIT_MG_KOH_G,
    # --- Viscosity-resistance (MRV) ---
    "mPa·s":            UNIT_MPA_S,       # mPa·s
    "mPas":                  UNIT_MPA_S,
    # --- Data-entry notes that are not units ---
    "not printed":           None,
    "not applicable":        None,
}

# Variants that require a note but no alias change
_INFORMATIONAL = frozenset({
    "wt.% or ppm as printed",   # Missing records only; no value to convert
    "kg/m3 (or as printed)",    # Ambiguous; handle per-record
    "relative density",         # Dimensionless ratio ≠ kg/m³; flag for review
})

# ---------------------------------------------------------------------------
# Numerical conversion rules
# Each entry: (from_unit, to_unit, factor)
# value_in_to_unit = value_in_from_unit * factor
# ---------------------------------------------------------------------------
CONVERSION_RULES: list[tuple[str, str, float]] = [
    # Density: convert to kg/m³
    ("g/cm3",     UNIT_KG_M3, 1000.0),   # g/cm³ = 1000 kg/m³
    ("g/cm³", UNIT_KG_M3, 1000.0),  # g/cm³ with superscript
    ("g/ml",      UNIT_KG_M3, 1000.0),   # g/mL = g/cm³ = 1000 kg/m³
    ("kg/L",      UNIT_KG_M3, 1000.0),   # kg/L = 1000 kg/m³
    ("kg/l",      UNIT_KG_M3, 1000.0),
    ("kg/dm3",    UNIT_KG_M3, 1000.0),   # kg/dm³ = kg/L = 1000 kg/m³
    ("lbs/gal",   UNIT_KG_M3, 119.826),  # US gal: 1 lb/gal = 119.826 kg/m³
    ("lbs/US gal", UNIT_KG_M3, 119.826),
    # Sulfur: ppm ↔ wt.%
    (UNIT_PPM,    UNIT_MASS_PCT, 1e-4),   # 1 ppm = 0.0001 wt.%
    (UNIT_MASS_PCT, UNIT_PPM, 1e4),       # 1 wt.% = 10,000 ppm
    # Mo: ppm → wt.%
    ("ppm",       UNIT_MASS_PCT, 1e-4),   # same as sulfur rule (ppm == UNIT_PPM)
]

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def normalize_unit(raw: str | None) -> str | None:
    """Return the canonical unit for *raw*, or the original if no alias exists.

    Returns None for data-entry notes ('not printed').
    Returns the original string if it is in the informational set (caller decides).
    Never raises; unknown units are returned unchanged.
    """
    if raw is None:
        return None
    result = _ALIASES.get(raw, raw)
    return result  # may be None for 'not printed'


def needs_conversion(raw: str | None) -> bool:
    """True when *raw* has a registered numerical conversion rule."""
    if raw is None:
        return False
    canon = normalize_unit(raw)
    return any(r[0] == (canon if canon else raw) for r in CONVERSION_RULES)


def convert_value(value: float | int, from_unit: str, to_unit: str) -> float:
    """Apply a registered conversion.  Raises ValueError if no rule exists."""
    from_canon = normalize_unit(from_unit)
    for src, dst, factor in CONVERSION_RULES:
        if (src == from_canon or src == from_unit) and dst == to_unit:
            return value * factor
    raise ValueError(f"No conversion rule from {from_unit!r} to {to_unit!r}")


def is_informational(raw: str | None) -> bool:
    """True when the unit needs manual review before use (not a simple alias)."""
    return raw in _INFORMATIONAL


def unit_family(raw: str | None) -> str | None:
    """Return a broad family tag for grouping: 'viscosity', 'mass_pct',
    'density', 'temperature', 'ppm', 'dimensionless', or None."""
    canon = normalize_unit(raw)
    if canon == UNIT_VISCOSITY:        return "viscosity"
    if canon == UNIT_MASS_PCT:         return "mass_pct"
    if canon == UNIT_KG_M3:            return "density"
    if raw in ("g/cm3", "g/cm³", "g/ml", "kg/L", "kg/l", "kg/dm3",
               "lbs/gal", "lbs/US gal", "relative density"):
        return "density"
    if canon == UNIT_TEMP_C:           return "temperature"
    if canon == UNIT_PPM:              return "ppm"
    if canon == UNIT_DIMLESS:          return "dimensionless"
    return None
