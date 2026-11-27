"""
Stable product join key for Pipeline B.

The Products_json dataset uses two inconsistent record_id schemes:
  - 94 products share the same record_id across all 3 tiers (e.g. 'BO-X-Y')
  - 87 products have tier-suffixed record_ids (e.g. 'BO-X-Y__T1', '__T2', '__T3')

Using record_id as a join key fails for the 87-product group.  The correct
join key is the folder path relative to Products_json/ (see CLAUDE.md §Known
inconsistencies).

This module builds a ProductKey (the folder path) and provides helpers to
join tier files for the same product.
"""

from __future__ import annotations

import pathlib
import json
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# ProductKey
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProductKey:
    """Stable identifier derived from folder path, independent of record_id."""
    material_class: str    # 'base_oil', 'additive_package', 'additive_component'
    supplier:       str    # folder name under Products_json/<Class>/
    product_id:     str    # innermost folder name

    @property
    def folder_path(self) -> str:
        """Relative path: '<ClassFolder>/<supplier>/<product_id>'"""
        return f"{_CLASS_FOLDER[self.material_class]}/{self.supplier}/{self.product_id}"

    def __str__(self) -> str:
        return f"{self.material_class}::{self.supplier}/{self.product_id}"


_CLASS_FOLDER: dict[str, str] = {
    "base_oil":           "Base_oils_json",
    "additive_package":   "Additive_packages_json",
    "additive_component": "Additive_components_json",
}


def key_from_path(json_path: pathlib.Path, root: pathlib.Path) -> ProductKey:
    """Derive a ProductKey from the file path alone (no JSON read required).

    *root* is the Products_json directory.
    Path structure: <root>/<ClassFolder>/<supplier>/<product_id>/<file>.json
    """
    rel = json_path.relative_to(root)
    parts = rel.parts  # (ClassFolder, supplier, product_id, filename)
    if len(parts) < 4:
        raise ValueError(f"Unexpected path depth: {json_path}")
    class_folder, supplier, product_id = parts[0], parts[1], parts[2]
    mat_class = _FOLDER_CLASS.get(class_folder)
    if mat_class is None:
        raise ValueError(f"Unrecognised class folder: {class_folder!r}")
    return ProductKey(
        material_class=mat_class,
        supplier=supplier,
        product_id=product_id,
    )


_FOLDER_CLASS: dict[str, str] = {v: k for k, v in _CLASS_FOLDER.items()}


# ---------------------------------------------------------------------------
# Tier grouping
# ---------------------------------------------------------------------------

@dataclass
class TierGroup:
    """All tier files for one product, keyed by tier number."""
    key:   ProductKey
    tiers: dict[int, pathlib.Path] = field(default_factory=dict)

    def tier_path(self, tier: int) -> pathlib.Path | None:
        return self.tiers.get(tier)

    def load_tier(self, tier: int) -> dict | None:
        p = self.tiers.get(tier)
        if p is None:
            return None
        return json.loads(p.read_bytes())

    def load_all(self) -> dict[int, dict]:
        return {t: json.loads(p.read_bytes()) for t, p in sorted(self.tiers.items())}


def group_by_product(root: pathlib.Path) -> dict[ProductKey, TierGroup]:
    """Scan Products_json and return one TierGroup per unique product folder.

    Reads *tier* from inside each JSON (not from the filename), so both
    file-naming conventions are handled correctly.
    """
    groups: dict[ProductKey, TierGroup] = {}

    for json_file in sorted(root.rglob("*.json")):
        try:
            key = key_from_path(json_file, root)
        except ValueError:
            continue

        try:
            data = json.loads(json_file.read_bytes())
        except (json.JSONDecodeError, OSError):
            continue

        tier = data.get("tier")
        if tier is None:
            continue
        try:
            tier_int = int(tier)
        except (TypeError, ValueError):
            continue

        if key not in groups:
            groups[key] = TierGroup(key=key)
        groups[key].tiers[tier_int] = json_file

    return groups


# ---------------------------------------------------------------------------
# record_id → ProductKey  (for cross-reference only; not for joining)
# ---------------------------------------------------------------------------

def strip_tier_suffix(record_id: str) -> str:
    """Remove __T1, __T2, __T3 suffixes to get the base record_id."""
    for suffix in ("__T1", "__T2", "__T3"):
        if record_id.endswith(suffix):
            return record_id[: -len(suffix)]
    return record_id
