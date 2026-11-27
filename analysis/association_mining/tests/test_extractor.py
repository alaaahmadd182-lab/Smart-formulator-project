"""
Tests for the Step 4 extractor.

All fixtures use synthetic TierGroups built from tmp_path JSON files —
no dependency on Products_json.
"""

import json
import pathlib
import pytest

from analysis.association_mining.record_key import TierGroup, ProductKey
from analysis.association_mining.extractor import (
    extract_base_oil,
    extract_additive_package,
    extract_treat_rate_rows,
    extract_all,
)
from analysis.association_mining.value_kind import VK_TYPICAL, VK_MINIMUM, VK_MAXIMUM


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _src(file="TDS.pdf", page="2"):
    return {"file": file, "page": page, "revision_date": None}


def _vo(value=None, vk="typical", status="Reported", unit="cSt",
        min_=None, max_=None, temp=None, source=None):
    return {
        "value": value, "qualifier": None,
        "min": min_, "max": max_,
        "value_kind": vk, "printed_text": str(value),
        "unit": unit, "test_temperature_c": temp,
        "method": "ASTM D445", "status": status,
        "calculation_note": None,
        "source": source or _src(),
        "notes": None,
        # Deliberately include value_final / unit_final to prove they are ignored
        "value_final": 999,
        "unit_final": "WRONG",
        "alternate_entries": [],
    }


def _make_tier_file(tmp_path: pathlib.Path, key: ProductKey, tier: int, fields: dict,
                    record_id="TEST-001", conflicts=None) -> pathlib.Path:
    class_dirs = {
        "base_oil": "Base_oils_json",
        "additive_package": "Additive_packages_json",
        "additive_component": "Additive_components_json",
    }
    d = tmp_path / class_dirs[key.material_class] / key.supplier / key.product_id
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"tier{tier}.json"
    path.write_text(
        json.dumps({
            "template_version": "1.1",
            "material_class": key.material_class,
            "tier": tier,
            "record_id": record_id,
            "fields": fields,
            "open_questions": [],
            "conflicts": conflicts or [],
        }),
        encoding="utf-8",
    )
    return path


def _build_bo_group(tmp_path: pathlib.Path, t1_fields=None, t2_fields=None,
                    t3_fields=None, conflicts=None) -> TierGroup:
    root = tmp_path / "Products_json"
    key = ProductKey("base_oil", "TestSupplier", "TESTPROD_1")
    _make_tier_file(root, key, 1, t1_fields or {}, conflicts=conflicts)
    _make_tier_file(root, key, 2, t2_fields or {})
    _make_tier_file(root, key, 3, t3_fields or {})
    from analysis.association_mining.record_key import group_by_product
    groups = group_by_product(root)
    return groups[key]


def _build_ap_group(tmp_path: pathlib.Path, t1_fields=None, t2_fields=None,
                    record_id="AP-001") -> TierGroup:
    root = tmp_path / "Products_json"
    key = ProductKey("additive_package", "TestPkg", "TESTPKG_1")
    _make_tier_file(root, key, 1, t1_fields or {}, record_id=record_id)
    _make_tier_file(root, key, 2, t2_fields or {}, record_id=record_id)
    from analysis.association_mining.record_key import group_by_product
    groups = group_by_product(root)
    return groups[key]


# ---------------------------------------------------------------------------
# Base oil extraction
# ---------------------------------------------------------------------------

class TestExtractBaseOil:
    def test_basic_t1_fields(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "kv40": _vo(value=100.0, unit="cSt"),
            "kv100": _vo(value=14.5, unit="cSt"),
            "viscosity_index": _vo(value=132, unit="dimensionless"),
        })
        row = extract_base_oil(group)
        assert row is not None
        assert row["kv40"] == 100.0
        assert row["kv100"] == 14.5
        assert row["vi"] == 132

    def test_value_final_is_ignored(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "kv40": _vo(value=100.0),
        })
        row = extract_base_oil(group)
        # value_final=999 must NOT appear as the extracted value
        assert row["kv40"] == 100.0

    def test_missing_vo_gives_none(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "kv40": _vo(value=None, status="Missing"),
        })
        row = extract_base_oil(group)
        assert row["kv40"] is None

    def test_minimum_bound_encoded_as_lb(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "viscosity_index": _vo(value=90.0, vk="minimum", unit="dimensionless"),
        })
        row = extract_base_oil(group)
        assert row["vi"] is None        # no point value for a bound
        assert row["vi_lb"] == 90.0

    def test_maximum_bound_encoded_as_ub(self, tmp_path):
        group = _build_bo_group(tmp_path, t2_fields={
            "pour_point": _vo(value=-20.0, vk="maximum", unit="°C"),
        })
        row = extract_base_oil(group)
        assert row["pour_point"] is None
        assert row["pour_point_ub"] == -20.0

    def test_density_temperature_preserved(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "density": _vo(value=870.0, unit="kg/m3", temp=15.0),
        })
        row = extract_base_oil(group)
        assert row["density_t1"] == 870.0
        assert row["density_t1_temp_c"] == 15.0

    def test_density_needs_conversion_flag(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "density": _vo(value=0.870, unit="g/cm3", temp=15.0),
        })
        row = extract_base_oil(group)
        assert row["density_t1_needs_conv"] is True
        # Value is extracted as-is; conversion is not applied silently
        assert row["density_t1"] == 0.870

    def test_conflict_flag_set(self, tmp_path):
        group = _build_bo_group(tmp_path,
            t1_fields={"kv40": _vo(value=100.0)},
            conflicts=[{"field": "kv40", "value_a": 100.0, "value_b": 102.0}],
        )
        row = extract_base_oil(group)
        assert row["kv40_conflict"] is True

    def test_no_conflict_flag_clear(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={"kv40": _vo(value=100.0)})
        row = extract_base_oil(group)
        assert row["kv40_conflict"] is False

    def test_t3_sulfur_extracted(self, tmp_path):
        group = _build_bo_group(tmp_path, t3_fields={
            "sulfur": _vo(value=250.0, unit="ppm"),
        })
        row = extract_base_oil(group)
        assert row["sulfur"] == 250.0
        assert row["sulfur_unit"] == "ppm"

    def test_identity_columns(self, tmp_path):
        group = _build_bo_group(tmp_path)
        row = extract_base_oil(group)
        assert row["supplier"] == "TestSupplier"
        assert row["product_id"] == "TESTPROD_1"
        assert "1" in row["tiers_present"]

    def test_no_tier1_returns_none(self, tmp_path):
        root = tmp_path / "Products_json"
        key = ProductKey("base_oil", "X", "Y")
        _make_tier_file(root, key, 2, {})  # only T2
        from analysis.association_mining.record_key import group_by_product
        groups = group_by_product(root)
        group = groups[key]
        assert extract_base_oil(group) is None

    def test_unit_normalized_in_row(self, tmp_path):
        group = _build_bo_group(tmp_path, t1_fields={
            "kv40": _vo(value=100.0, unit="mm2/s"),
        })
        row = extract_base_oil(group)
        assert row["kv40_unit"] == "mm²/s"  # canonical UNIT_VISCOSITY


# ---------------------------------------------------------------------------
# Additive package extraction
# ---------------------------------------------------------------------------

class TestExtractAdditivePackage:
    def test_sae_grades_normalized(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "sae_grades_documented": [
                {"sae_grade": "15W-40", "status": "Reported",
                 "source": _src(), "value": None},
                {"sae_grade": "SAE 15W-40", "status": "Reported",
                 "source": _src(), "value": None},
                {"sae_grade": "15W/40", "status": "Reported",
                 "source": _src(), "value": None},
            ]
        })
        row = extract_additive_package(group)
        assert row is not None
        grades = set(row["sae_grades_canon"].split("|"))
        assert grades == {"15W-40"}    # all three collapse to one canonical grade
        assert row["n_sae_grades"] == 3  # three entries, even if same canonical

    def test_performance_claims_extracted(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "performance_claims": [
                {"designation": "API CI-4", "claim_type": "meets",
                 "status": "Reported", "source": _src(), "value": None},
                {"designation": "API CH-4", "claim_type": "meets",
                 "status": "Reported", "source": _src(), "value": None},
                {"designation": "MISSING", "claim_type": "meets",
                 "status": "Missing", "source": _src(), "value": None},
            ]
        })
        row = extract_additive_package(group)
        claims = set(row["performance_claims"].split("|"))
        assert "API CI-4" in claims
        assert "API CH-4" in claims
        assert "MISSING" not in claims   # Missing status excluded
        assert row["n_performance_claims"] == 2

    def test_elements_extracted(self, tmp_path):
        group = _build_ap_group(tmp_path, t2_fields={
            "elements": {
                "Ca": _vo(value=2.5, unit="wt.%"),
                "Zn": _vo(value=0.9, unit="wt.%"),
                "P":  _vo(value=0.8, unit="wt.%"),
            }
        })
        row = extract_additive_package(group)
        assert row["ca"] == 2.5
        assert row["zn"] == 0.9
        assert row["p"] == 0.8

    def test_mo_ppm_flagged(self, tmp_path):
        group = _build_ap_group(tmp_path, t2_fields={
            "elements": {
                "Mo": _vo(value=400.0, unit="ppm"),
            }
        })
        row = extract_additive_package(group)
        assert row["mo"] == 400.0
        assert row["mo_needs_conv"] is True

    def test_has_treat_rate_data(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "treat_rate_matrix": [{
                "claim": "API CI-4",
                "sae_grade": "15W-40",
                "treat_rate_wt_pct": _vo(value=10.5, unit="wt.%"),
            }]
        })
        row = extract_additive_package(group)
        assert row["has_treat_rate_data"] is True
        assert row["n_treat_rate_entries"] == 1


# ---------------------------------------------------------------------------
# Treat rate rows
# ---------------------------------------------------------------------------

class TestExtractTreatRateRows:
    def test_reported_entries_extracted(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "treat_rate_matrix": [
                {"claim": "API CI-4", "sae_grade": "SAE 15W-40",
                 "treat_rate_wt_pct": _vo(value=10.5, unit="wt.%")},
                {"claim": "API CH-4", "sae_grade": "SAE 10W-30",
                 "treat_rate_wt_pct": _vo(value=9.8, unit="wt.%")},
            ]
        })
        rows = extract_treat_rate_rows(group)
        assert len(rows) == 2
        assert rows[0]["treat_rate"] == 10.5
        assert rows[0]["sae_grade"] == "15W-40"  # normalised
        assert rows[1]["sae_grade"] == "10W-30"

    def test_missing_treat_rate_excluded(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "treat_rate_matrix": [
                {"claim": None, "sae_grade": None,
                 "treat_rate_wt_pct": _vo(value=None, status="Missing", unit="wt.%")},
            ]
        })
        rows = extract_treat_rate_rows(group)
        assert rows == []

    def test_product_identity_in_rows(self, tmp_path):
        group = _build_ap_group(tmp_path, t1_fields={
            "treat_rate_matrix": [
                {"claim": "API CI-4", "sae_grade": "15W-40",
                 "treat_rate_wt_pct": _vo(value=10.5, unit="wt.%")},
            ]
        })
        rows = extract_treat_rate_rows(group)
        assert rows[0]["supplier"] == "TestPkg"
        assert rows[0]["product_id"] == "TESTPKG_1"


# ---------------------------------------------------------------------------
# extract_all integration
# ---------------------------------------------------------------------------

class TestExtractAll:
    def _build_tree(self, tmp_path: pathlib.Path) -> pathlib.Path:
        root = tmp_path / "Products_json"
        # one base oil
        bo_key = ProductKey("base_oil", "SUP_A", "BO_001")
        _make_tier_file(root, bo_key, 1, {"kv40": _vo(value=100.0)})
        _make_tier_file(root, bo_key, 2, {})
        _make_tier_file(root, bo_key, 3, {})
        # one additive package with treat rate
        ap_key = ProductKey("additive_package", "SUP_B", "AP_001")
        _make_tier_file(root, ap_key, 1, {
            "treat_rate_matrix": [
                {"claim": "API CI-4", "sae_grade": "15W-40",
                 "treat_rate_wt_pct": _vo(value=10.5, unit="wt.%")},
            ]
        })
        _make_tier_file(root, ap_key, 2, {})
        return root

    def test_returns_three_tables(self, tmp_path):
        root = self._build_tree(tmp_path)
        tables = extract_all(root)
        assert set(tables.keys()) == {"base_oil", "additive_pkg", "treat_rate"}

    def test_base_oil_count(self, tmp_path):
        root = self._build_tree(tmp_path)
        tables = extract_all(root)
        assert len(tables["base_oil"]) == 1

    def test_additive_pkg_count(self, tmp_path):
        root = self._build_tree(tmp_path)
        tables = extract_all(root)
        assert len(tables["additive_pkg"]) == 1

    def test_treat_rate_rows(self, tmp_path):
        root = self._build_tree(tmp_path)
        tables = extract_all(root)
        assert len(tables["treat_rate"]) == 1
        assert tables["treat_rate"][0]["treat_rate"] == 10.5
