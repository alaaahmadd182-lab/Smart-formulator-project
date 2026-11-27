"""
value_kind encoding for Pipeline B.

Each value object in the JSON can carry a value_kind string that describes
whether the recorded value is a point measurement, a lower bound, an upper
bound, or a range.  Silently merging these into a single numeric column
introduces systematic bias (see Step 2 ML Readiness Assessment §4).

This module:
1. Maps raw value_kind strings to a canonical set.
2. Provides an encoder that splits a value object into typed columns:
     _value   — the central point (None if the kind is a pure bound)
     _lb      — lower bound (None if not applicable)
     _ub      — upper bound (None if not applicable)
     _vk      — canonical value_kind string (always set when value exists)
3. Never modifies the source JSON.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Canonical value_kind vocabulary
# ---------------------------------------------------------------------------
VK_TYPICAL   = "typical"      # representative point measurement
VK_SINGLE    = "single"       # single-measured point
VK_MINIMUM   = "minimum"      # value is a lower bound (≥)
VK_MAXIMUM   = "maximum"      # value is an upper bound (≤)
VK_RANGE     = "range"        # min+max both populated; value is midpoint only
VK_SPEC      = "specification" # a datasheet limit/requirement, not a measurement
VK_CALC      = "calculated"   # derived from other values
VK_UNKNOWN   = "unknown"

# Aliases observed in the dataset → canonical
_VK_ALIASES: dict[str, str] = {
    "typical":                     VK_TYPICAL,
    "single":                      VK_SINGLE,
    "minimum":                     VK_MINIMUM,
    "lower bound":                 VK_MINIMUM,
    "lower_bound":                 VK_MINIMUM,
    "minimum / lower bound":       VK_MINIMUM,
    "maximum":                     VK_MAXIMUM,
    "upper bound":                 VK_MAXIMUM,
    "upper_bound":                 VK_MAXIMUM,
    "maximum / upper bound":       VK_MAXIMUM,
    "range":                       VK_RANGE,
    "specification":               VK_SPEC,
    "spec":                        VK_SPEC,
    "calculated":                  VK_CALC,
    "calculated lower bound":      VK_MINIMUM,  # treat as a minimum
    "SDS reported":                VK_TYPICAL,  # source tag, not a kind; flatten
    "SDS Reported":                VK_TYPICAL,
    "sds reported":                VK_TYPICAL,
}

# Which canonical kinds represent bound-only observations (no reliable midpoint)
BOUND_KINDS = frozenset({VK_MINIMUM, VK_MAXIMUM})
# Which kinds carry both min and max
RANGE_KINDS = frozenset({VK_RANGE})


def normalize_value_kind(raw: str | None) -> str:
    """Return canonical value_kind for *raw*; falls back to VK_UNKNOWN."""
    if raw is None:
        return VK_UNKNOWN
    return _VK_ALIASES.get(raw, VK_UNKNOWN)


# ---------------------------------------------------------------------------
# Encoded result
# ---------------------------------------------------------------------------

@dataclass
class EncodedValue:
    """Typed columns produced from a single value object."""
    value:  float | None   # point value; None for pure bounds
    lb:     float | None   # lower bound; None if not a bound
    ub:     float | None   # upper bound; None if not a bound
    vk:     str            # canonical value_kind
    unit:   str | None     # unit string (after unit_registry normalization if desired)
    method: str | None
    source_file:    str | None
    source_page:    str | None
    conflict_flag:  bool   # True when this field has an unresolved conflict entry
    alternate_flag: bool   # True when alternate_entries[] is non-empty

    @property
    def is_bound(self) -> bool:
        return self.vk in BOUND_KINDS

    @property
    def is_range(self) -> bool:
        return self.vk in RANGE_KINDS

    @property
    def has_point(self) -> bool:
        return self.value is not None and not self.is_bound

    def to_dict(self, prefix: str = "") -> dict[str, Any]:
        """Flat dict suitable for a DataFrame row, with optional column prefix."""
        p = prefix
        return {
            f"{p}value":         self.value,
            f"{p}lb":            self.lb,
            f"{p}ub":            self.ub,
            f"{p}vk":            self.vk,
            f"{p}unit":          self.unit,
            f"{p}method":        self.method,
            f"{p}source_file":   self.source_file,
            f"{p}source_page":   self.source_page,
            f"{p}conflict":      self.conflict_flag,
            f"{p}alternate":     self.alternate_flag,
        }


# ---------------------------------------------------------------------------
# Encoder
# ---------------------------------------------------------------------------

def encode_value_object(
    vo: dict[str, Any] | None,
    field_conflicts: list[dict] | None = None,
) -> EncodedValue | None:
    """Encode one value-object dict into an EncodedValue.

    *field_conflicts*: list of conflict entries from the same field (from the
    top-level conflicts[] array where field matches).  Used to set conflict_flag.

    Returns None when *vo* is None or status is not Reported/Calculated.
    """
    if vo is None:
        return None
    status = vo.get("status", "")
    if status not in ("Reported", "Calculated"):
        return None

    raw_vk = vo.get("value_kind")
    vk = normalize_value_kind(raw_vk)

    raw_value = vo.get("value")
    raw_min   = vo.get("min")
    raw_max   = vo.get("max")

    # Determine point, lb, ub
    point: float | None = None
    lb:    float | None = None
    ub:    float | None = None

    if vk == VK_MINIMUM:
        lb = _to_float(raw_value)
    elif vk == VK_MAXIMUM:
        ub = _to_float(raw_value)
    elif vk == VK_RANGE:
        lb = _to_float(raw_min)
        ub = _to_float(raw_max)
        # midpoint only as an approximation; callers decide whether to use it
        if lb is not None and ub is not None:
            point = (lb + ub) / 2.0
    else:
        point = _to_float(raw_value)

    src = vo.get("source") or {}
    alternates = vo.get("alternate_entries") or []

    return EncodedValue(
        value  = point,
        lb     = lb,
        ub     = ub,
        vk     = vk,
        unit   = vo.get("unit"),
        method = vo.get("method"),
        source_file  = src.get("file"),
        source_page  = src.get("page"),
        conflict_flag  = bool(field_conflicts),
        alternate_flag = bool(alternates),
    )


def _to_float(v: Any) -> float | None:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
