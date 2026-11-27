"""
Tests for Step 6 feature engineering transforms.

All tests use synthetic row dicts — no dependency on Products_json or CSV files.
"""

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from analysis.association_mining.feature_engineer import (
    convert_density,
    normalise_sulfur,
    canon_pkg_type,
    engineer_base_oil_row,
    engineer_package_row,
    API_GROUP_ORD,
    PKG_CATEGORIES,
)


# ---------------------------------------------------------------------------
# Density conversion
# ---------------------------------------------------------------------------

class TestConvertDensity:
    def test_already_kg_m3(self):
        v, applied = convert_density("870.0", "kg/m³", "False")
        assert v == 870.0
        assert applied is False

    def test_g_cm3_to_kg_m3(self):
        v, applied = convert_density("0.870", "g/cm3", "True")
        assert abs(v - 870.0) < 0.01
        assert applied is True

    def test_kg_L_to_kg_m3(self):
        v, applied = convert_density("0.870", "kg/L", "True")
        assert abs(v - 870.0) < 0.01
        assert applied is True

    def test_lbs_gal_to_kg_m3(self):
        v, applied = convert_density("7.3", "lbs/gal", "True")
        # 7.3 * 119.826 = 874.73
        assert abs(v - 874.73) < 0.5
        assert applied is True

    def test_missing_value_returns_none(self):
        v, applied = convert_density(None, "g/cm3", "True")
        assert v is None
        assert applied is False

    def test_empty_value_returns_none(self):
        v, applied = convert_density("", "g/cm3", "True")
        assert v is None
        assert applied is False

    def test_relative_density_not_converted(self):
        # needs_conv=False, unit is not kg/m³ -> (None, False)
        v, applied = convert_density("1.02", "relative density", "False")
        assert v is None
        assert applied is False

    def test_unregistered_unit_needs_conv_true(self):
        # needs_conv=True but unit unknown -> (None, False)
        v, applied = convert_density("1.0", "unknown_unit", "True")
        assert v is None
        assert applied is False

    def test_kg_dm3_to_kg_m3(self):
        v, applied = convert_density("0.870", "kg/dm3", "True")
        assert abs(v - 870.0) < 0.01
        assert applied is True

    def test_g_ml_to_kg_m3(self):
        v, applied = convert_density("0.870", "g/ml", "True")
        assert abs(v - 870.0) < 0.01
        assert applied is True


# ---------------------------------------------------------------------------
# Sulfur normalisation
# ---------------------------------------------------------------------------

class TestNormaliseSulfur:
    def test_ppm_to_wt_pct(self):
        v, src = normalise_sulfur("100.0", "ppm")
        assert abs(v - 0.01) < 1e-7
        assert src == "ppm"

    def test_wt_pct_unchanged(self):
        v, src = normalise_sulfur("0.3", "wt.%")
        assert v == 0.3
        assert src == "wt.%"

    def test_missing_value(self):
        v, src = normalise_sulfur(None, "ppm")
        assert v is None
        assert src is None

    def test_unknown_unit(self):
        v, src = normalise_sulfur("0.3", "volume%")
        assert v is None
        assert src == "volume%"

    def test_low_sulfur_ppm(self):
        v, src = normalise_sulfur("4.0", "ppm")
        assert abs(v - 0.0004) < 1e-9
        assert src == "ppm"


# ---------------------------------------------------------------------------
# Package type canonicalisation
# ---------------------------------------------------------------------------

class TestCanonPkgType:
    def test_hdeo_ci4(self):
        assert canon_pkg_type("HDEO CI-4 Package") == "hdeo"

    def test_hdeo_ck4(self):
        assert canon_pkg_type("Heavy Duty Diesel Engine Oil Package CK-4") == "hdeo"

    def test_hdeo_keyword(self):
        assert canon_pkg_type("heavy duty engine oil additive") == "hdeo"

    def test_pceo_passenger(self):
        assert canon_pkg_type("Passenger Car Engine Oil Package") == "pceo"

    def test_pceo_ilsac(self):
        assert canon_pkg_type("ILSAC GF-6 Package") == "pceo"

    def test_universal(self):
        assert canon_pkg_type("Universal Engine Oil Package") == "universal"

    def test_gear(self):
        assert canon_pkg_type("Gear Oil GL-5 Additive Package") == "gear"

    def test_atf(self):
        assert canon_pkg_type("ATF Dexron-III Package") == "atf"

    def test_missing_none(self):
        assert canon_pkg_type(None) == "missing"

    def test_missing_empty(self):
        assert canon_pkg_type("") == "missing"

    def test_other(self):
        assert canon_pkg_type("Specialty Compressor Additive") == "other"

    def test_all_categories_valid(self):
        # Every possible return value is in PKG_CATEGORIES
        cases = [None, "", "HDEO CI-4", "PCEO", "Universal", "Gear", "ATF", "Other"]
        for c in cases:
            assert canon_pkg_type(c) in PKG_CATEGORIES


# ---------------------------------------------------------------------------
# Base oil row engineering
# ---------------------------------------------------------------------------

def _bo_row(**kwargs) -> dict:
    base = {
        "product_key": "base_oil/SUP/PROD", "supplier": "SUP", "product_id": "PROD",
        "record_id": "PROD", "tiers_present": "1,2,3", "n_conflicts": "0",
        "api_group": None, "chemistry": None,
        "kv40": None, "kv40_lb": None, "kv40_ub": None, "kv40_vk": None,
        "kv40_unit": None, "kv40_src": None, "kv40_conflict": "False",
        "kv100": None, "kv100_lb": None, "kv100_ub": None, "kv100_vk": None,
        "kv100_unit": None, "kv100_src": None, "kv100_conflict": "False",
        "vi": None, "vi_lb": None, "vi_ub": None, "vi_vk": None,
        "vi_unit": None, "vi_src": None, "vi_conflict": "False",
        "density_t1": None, "density_t1_lb": None, "density_t1_ub": None,
        "density_t1_vk": None, "density_t1_unit": None, "density_t1_src": None,
        "density_t1_conflict": "False", "density_t1_temp_c": None, "density_t1_needs_conv": "False",
        "flash_point": None, "flash_point_lb": None, "flash_point_ub": None,
        "flash_point_vk": None, "flash_point_unit": None, "flash_point_src": None,
        "flash_point_conflict": "False",
        "pour_point": None, "pour_point_lb": None, "pour_point_ub": None,
        "pour_point_vk": None, "pour_point_unit": None, "pour_point_src": None,
        "pour_point_conflict": "False",
        "noack": None, "noack_lb": None, "noack_ub": None, "noack_vk": None,
        "noack_unit": None, "noack_src": None, "noack_conflict": "False",
        "specific_gravity": None, "specific_gravity_lb": None, "specific_gravity_ub": None,
        "specific_gravity_vk": None, "specific_gravity_unit": None,
        "specific_gravity_src": None, "specific_gravity_conflict": "False",
        "sulfur": None, "sulfur_lb": None, "sulfur_ub": None, "sulfur_vk": None,
        "sulfur_unit": None, "sulfur_src": None, "sulfur_conflict": "False",
        "saturates": None, "aromatics": None,
    }
    base.update(kwargs)
    return base


class TestEngineerBaseOilRow:
    def test_density_g_cm3_converted(self):
        row = _bo_row(density_t1="0.870", density_t1_unit="g/cm3", density_t1_needs_conv="True")
        out = engineer_base_oil_row(row)
        assert abs(out["density_kg_m3"] - 870.0) < 0.01
        assert out["density_conv_applied"] is True

    def test_density_already_kg_m3(self):
        row = _bo_row(density_t1="870.0", density_t1_unit="kg/m³", density_t1_needs_conv="False")
        out = engineer_base_oil_row(row)
        assert out["density_kg_m3"] == 870.0
        assert out["density_conv_applied"] is False

    def test_density_missing(self):
        row = _bo_row()
        out = engineer_base_oil_row(row)
        assert out["density_kg_m3"] is None
        assert out["density_conv_applied"] is False

    def test_api_group_i_encoded(self):
        row = _bo_row(api_group="Group I")
        out = engineer_base_oil_row(row)
        assert out["api_group_ord"] == 1.0
        assert out["api_group_known"] is True

    def test_api_group_iv_encoded(self):
        row = _bo_row(api_group="Group IV")
        out = engineer_base_oil_row(row)
        assert out["api_group_ord"] == 4.0

    def test_api_group_ii_plus(self):
        row = _bo_row(api_group="Group II+")
        out = engineer_base_oil_row(row)
        assert out["api_group_ord"] == 2.5

    def test_api_group_missing(self):
        row = _bo_row(api_group="Missing")
        out = engineer_base_oil_row(row)
        assert out["api_group_ord"] is None
        assert out["api_group_known"] is False

    def test_api_group_none(self):
        row = _bo_row(api_group=None)
        out = engineer_base_oil_row(row)
        assert out["api_group_ord"] is None
        assert out["api_group_known"] is False

    def test_sulfur_ppm_to_wt_pct(self):
        row = _bo_row(sulfur="4.0", sulfur_unit="ppm")
        out = engineer_base_oil_row(row)
        assert abs(out["sulfur_wt_pct"] - 0.0004) < 1e-9
        assert out["sulfur_unit_src"] == "ppm"

    def test_sulfur_wt_pct_unchanged(self):
        row = _bo_row(sulfur="0.3", sulfur_unit="wt.%")
        out = engineer_base_oil_row(row)
        assert out["sulfur_wt_pct"] == 0.3
        assert out["sulfur_unit_src"] == "wt.%"

    def test_vi_point_typical(self):
        row = _bo_row(vi="130.0", vi_vk="typical")
        out = engineer_base_oil_row(row)
        assert out["vi_point"] == 130.0
        assert out["vi_lb_bound"] is None
        assert out["vi_bound_type"] == "point"

    def test_vi_minimum_bound(self):
        row = _bo_row(vi=None, vi_lb="90.0", vi_vk="minimum")
        out = engineer_base_oil_row(row)
        assert out["vi_point"] is None
        assert out["vi_lb_bound"] == 90.0
        assert out["vi_bound_type"] == "lower_bound"

    def test_pour_point_maximum_flagged(self):
        row = _bo_row(pour_point=None, pour_point_ub="-15.0", pour_point_vk="maximum")
        out = engineer_base_oil_row(row)
        assert out["pour_point_is_max"] is True

    def test_pour_point_typical_not_flagged(self):
        row = _bo_row(pour_point="-30.0", pour_point_vk="typical")
        out = engineer_base_oil_row(row)
        assert out["pour_point_is_max"] is False

    def test_original_columns_preserved(self):
        row = _bo_row(kv40="100.0", kv40_vk="typical")
        out = engineer_base_oil_row(row)
        assert out["kv40"] == "100.0"  # preserved as-is from source CSV


# ---------------------------------------------------------------------------
# Additive package row engineering
# ---------------------------------------------------------------------------

def _ap_row(**kwargs) -> dict:
    base = {
        "product_key": "additive_package/SUP/PKG", "supplier": "SUP",
        "product_id": "PKG", "record_id": "PKG", "tiers_present": "1,2",
        "n_conflicts": "0", "package_type": None, "intended_service": None,
        "sae_grades_canon": None, "n_sae_grades": "0",
        "performance_claims": None, "n_performance_claims": "0",
        "n_treat_rate_entries": "0", "has_treat_rate_data": "False",
        "kv100": None, "kv100_lb": None, "kv100_ub": None, "kv100_vk": None,
        "kv100_unit": None, "kv100_src": None, "kv100_conflict": "False",
        "density_t2": None, "density_t2_lb": None, "density_t2_ub": None,
        "density_t2_vk": None, "density_t2_unit": None, "density_t2_src": None,
        "density_t2_conflict": "False", "density_t2_temp_c": None,
        "density_t2_needs_conv": "False",
        "flash_point": None, "pour_point": None,
        "tbn": None, "tbn_lb": None, "tbn_ub": None, "tbn_vk": None,
        "tbn_unit": None, "tbn_src": None, "tbn_conflict": "False",
        "sulfated_ash": None, "sulfated_ash_lb": None, "sulfated_ash_ub": None,
        "sulfated_ash_vk": None, "sulfated_ash_unit": None,
        "sulfated_ash_src": None, "sulfated_ash_conflict": "False",
        "ca": None, "ca_lb": None, "ca_ub": None, "ca_vk": None,
        "ca_unit": None, "ca_src": None, "ca_conflict": "False",
        "zn": None, "zn_lb": None, "zn_ub": None, "zn_vk": None,
        "zn_unit": None, "zn_src": None, "zn_conflict": "False",
        "p": None, "p_lb": None, "p_ub": None, "p_vk": None,
        "p_unit": None, "p_src": None, "p_conflict": "False",
        "n": None, "s": None, "mg": None,
        "mo": None, "mo_lb": None, "mo_ub": None, "mo_vk": None,
        "mo_unit": None, "mo_src": None, "mo_conflict": "False",
        "mo_unit_raw": None, "mo_needs_conv": "False",
        "b": None,
    }
    base.update(kwargs)
    return base


class TestEngineerPackageRow:
    def test_density_g_cm3_converted(self):
        row = _ap_row(density_t2="1.07", density_t2_unit="g/cm3",
                      density_t2_needs_conv="True")
        out = engineer_package_row(row)
        assert abs(out["density_kg_m3"] - 1070.0) < 0.5
        assert out["density_conv_applied"] is True

    def test_density_already_kg_m3(self):
        row = _ap_row(density_t2="1070.0", density_t2_unit="kg/m³",
                      density_t2_needs_conv="False")
        out = engineer_package_row(row)
        assert out["density_kg_m3"] == 1070.0
        assert out["density_conv_applied"] is False

    def test_mo_ppm_converted(self):
        # mo_unit='ppm' triggers the 1e-4 conversion regardless of mo_needs_conv flag
        row = _ap_row(mo="400.0", mo_unit="ppm", mo_needs_conv="True")
        out = engineer_package_row(row)
        assert abs(out["mo_wt_pct"] - 0.04) < 1e-7
        assert out["mo_conv_applied"] is True

    def test_mo_wt_pct_unchanged(self):
        # wt.% unit: no conversion even though mo_needs_conv may be True
        # (needs_conversion('wt.%') is True due to bidirectional ppm<->wt.% rule)
        row = _ap_row(mo="0.05", mo_unit="wt.%", mo_needs_conv="True")
        out = engineer_package_row(row)
        assert out["mo_wt_pct"] == 0.05
        assert out["mo_conv_applied"] is False

    def test_mo_wt_pct_needs_conv_false(self):
        row = _ap_row(mo="0.05", mo_unit="wt.%", mo_needs_conv="False")
        out = engineer_package_row(row)
        assert out["mo_wt_pct"] == 0.05
        assert out["mo_conv_applied"] is False

    def test_mo_missing(self):
        row = _ap_row()
        out = engineer_package_row(row)
        assert out["mo_wt_pct"] is None
        assert out["mo_conv_applied"] is False

    def test_package_type_hdeo(self):
        row = _ap_row(package_type="HDEO CI-4 Plus Package")
        out = engineer_package_row(row)
        assert out["package_type_canon"] == "hdeo"

    def test_package_type_missing(self):
        row = _ap_row(package_type=None)
        out = engineer_package_row(row)
        assert out["package_type_canon"] == "missing"

    def test_zn_p_sum(self):
        row = _ap_row(zn="1.1", p="0.9")
        out = engineer_package_row(row)
        assert abs(out["zn_p_sum"] - 2.0) < 1e-6

    def test_zn_p_ratio(self):
        row = _ap_row(zn="1.1", p="1.0")
        out = engineer_package_row(row)
        assert abs(out["zn_p_ratio"] - 1.1) < 1e-5

    def test_zn_p_sum_missing_one(self):
        row = _ap_row(zn="1.1", p=None)
        out = engineer_package_row(row)
        assert out["zn_p_sum"] is None
        assert out["zn_p_ratio"] is None

    def test_ca_tbn_ratio(self):
        row = _ap_row(ca="2.5", tbn="100.0")
        out = engineer_package_row(row)
        assert abs(out["ca_tbn_ratio"] - 0.025) < 1e-7

    def test_ca_tbn_ratio_tbn_zero(self):
        row = _ap_row(ca="2.5", tbn="0.0")
        out = engineer_package_row(row)
        assert out["ca_tbn_ratio"] is None

    def test_original_columns_preserved(self):
        row = _ap_row(tbn="91.0", tbn_vk="typical")
        out = engineer_package_row(row)
        assert out["tbn"] == "91.0"

    def test_zddp_stoichiometry_ratio_near_1(self):
        # Zn:P ratio should be ~1.0 for ZDDP (molar Zn:P ≈ 1:1 → mass ratio ≈ Zn_at/P_at ≈ 65.4/31.0 ≈ 2.11)
        # In wt.% the mass ratio Zn/P ≈ 1.0 to 1.2 in real data
        row = _ap_row(zn="1.1", p="1.0")
        out = engineer_package_row(row)
        assert 0.9 < out["zn_p_ratio"] < 1.5


# ---------------------------------------------------------------------------
# API group ordinal completeness check
# ---------------------------------------------------------------------------

class TestApiGroupOrd:
    def test_all_groups_present(self):
        expected = {"Group I", "Group II", "Group II+", "Group III", "Group IV", "Group V"}
        assert set(API_GROUP_ORD.keys()) == expected

    def test_ordinal_order_preserved(self):
        vals = list(API_GROUP_ORD.values())
        assert vals == sorted(vals), "ordinal values must be monotonically increasing"

    def test_group_ii_plus_between_ii_and_iii(self):
        assert API_GROUP_ORD["Group II"] < API_GROUP_ORD["Group II+"] < API_GROUP_ORD["Group III"]


if __name__ == "__main__":
    import traceback, sys
    failures = []
    suites = [
        TestConvertDensity, TestNormaliseSulfur, TestCanonPkgType,
        TestEngineerBaseOilRow, TestEngineerPackageRow, TestApiGroupOrd,
    ]
    for cls in suites:
        obj = cls()
        for name in [n for n in dir(cls) if n.startswith("test_")]:
            try:
                getattr(obj, name)()
                print(f"  PASS  {cls.__name__}.{name}")
            except Exception as e:
                failures.append(f"{cls.__name__}.{name}: {e}")
                print(f"  FAIL  {cls.__name__}.{name}: {e}")
    print(f"\n{len(failures)} failure(s)")
    if failures:
        sys.exit(1)
