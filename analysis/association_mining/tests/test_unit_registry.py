import pytest
from analysis.association_mining.unit_registry import (
    normalize_unit, needs_conversion, convert_value, is_informational,
    unit_family, UNIT_VISCOSITY, UNIT_MASS_PCT, UNIT_KG_M3, UNIT_PPM, UNIT_TEMP_C,
)


class TestNormalizeUnit:
    def test_cst_becomes_mm2_s(self):
        assert normalize_unit("cSt") == UNIT_VISCOSITY

    def test_mm2_s_ascii_becomes_canonical(self):
        assert normalize_unit("mm2/s") == UNIT_VISCOSITY

    def test_mm2_s_superscript_becomes_canonical(self):
        assert normalize_unit("mm²/s") == UNIT_VISCOSITY

    def test_mm2_sec_becomes_canonical(self):
        assert normalize_unit("mm2/sec") == UNIT_VISCOSITY

    def test_wt_pct_variants(self):
        for raw in ("wt.%", "wt%", "wt.% loss", "mass%", "mass %", "%M/M", "wt.% as printed"):
            assert normalize_unit(raw) == UNIT_MASS_PCT, f"failed for {raw!r}"

    def test_temperature_roundtrip(self):
        assert normalize_unit("°C") == UNIT_TEMP_C
        assert normalize_unit("°C") == UNIT_TEMP_C

    def test_density_kg_m3_variants(self):
        assert normalize_unit("kg/m3") == UNIT_KG_M3
        assert normalize_unit("kg/m³") == UNIT_KG_M3

    def test_ppm_family(self):
        for raw in ("ppm", "ppm (wt)", "wt ppm", "mg/kg"):
            assert normalize_unit(raw) == UNIT_PPM, f"failed for {raw!r}"

    def test_not_printed_returns_none(self):
        assert normalize_unit("not printed") is None

    def test_unknown_unit_returned_unchanged(self):
        assert normalize_unit("furlongs/fortnight") == "furlongs/fortnight"

    def test_none_returns_none(self):
        assert normalize_unit(None) is None


class TestNeedsConversion:
    def test_density_g_cm3_needs_conversion(self):
        assert needs_conversion("g/cm3")

    def test_density_kg_l_needs_conversion(self):
        assert needs_conversion("kg/L")

    def test_viscosity_does_not_need_conversion(self):
        assert not needs_conversion("cSt")

    def test_wt_pct_does_not_need_conversion(self):
        assert not needs_conversion("wt.%")


class TestConvertValue:
    def test_g_cm3_to_kg_m3(self):
        result = convert_value(0.870, "g/cm3", UNIT_KG_M3)
        assert abs(result - 870.0) < 0.001

    def test_kg_L_to_kg_m3(self):
        result = convert_value(0.870, "kg/L", UNIT_KG_M3)
        assert abs(result - 870.0) < 0.001

    def test_ppm_to_wt_pct(self):
        result = convert_value(100.0, "ppm", UNIT_MASS_PCT)
        assert abs(result - 0.01) < 1e-9

    def test_unknown_raises(self):
        with pytest.raises(ValueError):
            convert_value(1.0, "furlongs", UNIT_KG_M3)


class TestIsInformational:
    def test_wt_pct_or_ppm(self):
        assert is_informational("wt.% or ppm as printed")

    def test_relative_density(self):
        assert is_informational("relative density")

    def test_normal_unit_not_informational(self):
        assert not is_informational("kg/m3")


class TestUnitFamily:
    def test_viscosity_family(self):
        assert unit_family("cSt") == "viscosity"
        assert unit_family("mm2/s") == "viscosity"

    def test_density_family(self):
        assert unit_family("kg/m3") == "density"
        assert unit_family("g/cm3") == "density"
        assert unit_family("g/ml") == "density"

    def test_mass_pct_family(self):
        assert unit_family("wt.%") == "mass_pct"
        assert unit_family("wt%") == "mass_pct"

    def test_temperature_family(self):
        assert unit_family("°C") == "temperature"

    def test_ppm_family(self):
        assert unit_family("ppm") == "ppm"
        assert unit_family("mg/kg") == "ppm"
