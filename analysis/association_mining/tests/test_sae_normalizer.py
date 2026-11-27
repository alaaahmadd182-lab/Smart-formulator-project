import pytest
from analysis.association_mining.sae_normalizer import (
    normalize_grade, normalize_grades, CAT_MULTI, CAT_MONO,
)


class TestNormalizeGrade:
    # --- Multi-grade: dash separator ---
    def test_15w40_dash(self):
        assert normalize_grade("15W-40") == "15W-40"

    def test_sae_prefix_stripped(self):
        assert normalize_grade("SAE 15W-40") == "15W-40"

    def test_10w30_dash(self):
        assert normalize_grade("10W-30") == "10W-30"

    def test_20w50_dash(self):
        assert normalize_grade("20W-50") == "20W-50"

    # --- Multi-grade: slash separator ---
    def test_15w40_slash(self):
        assert normalize_grade("15W/40") == "15W-40"

    def test_10w30_slash(self):
        assert normalize_grade("10W/30") == "10W-30"

    def test_sae_10w40_slash(self):
        assert normalize_grade("SAE 10W-40") == "10W-40"

    # --- Multi-grade: no separator ---
    def test_15w40_no_sep(self):
        assert normalize_grade("15W40") == "15W-40"

    def test_10w40_no_sep(self):
        assert normalize_grade("10W40") == "10W-40"

    # --- Mono-grades ---
    def test_monograde_40(self):
        assert normalize_grade("40") == "40"

    def test_monograde_sae30(self):
        assert normalize_grade("30") == "30"

    # --- Broad category strings ---
    def test_multi_tokens(self):
        for raw in ("Multi-grade", "Multi", "MULTI"):
            assert normalize_grade(raw) == CAT_MULTI, f"failed for {raw!r}"

    def test_mono_tokens(self):
        for raw in ("Mono-grade", "Mono", "MONO", "mono-grades", "all monogrades"):
            assert normalize_grade(raw) == CAT_MONO, f"failed for {raw!r}"

    # --- Edge cases ---
    def test_none_returns_none(self):
        assert normalize_grade(None) is None

    def test_5w30(self):
        assert normalize_grade("5W-30") == "5W-30"
        assert normalize_grade("5W/30") == "5W-30"
        assert normalize_grade("SAE 5W-30") == "5W-30"

    def test_15w50(self):
        assert normalize_grade("SAE 15W-50") == "15W-50"
        assert normalize_grade("15W-50") == "15W-50"

    def test_20w40(self):
        assert normalize_grade("20W-40") == "20W-40"
        assert normalize_grade("20W/40") == "20W-40"


class TestNormalizeGrades:
    def test_list_normalization(self):
        raw = ["15W-40", "SAE 15W-40", "15W/40", "15W40"]
        result = normalize_grades(raw)
        assert all(g == "15W-40" for g in result)

    def test_none_values_dropped(self):
        result = normalize_grades([None, "15W-40", None])
        assert result == ["15W-40"]

    def test_empty_list(self):
        assert normalize_grades([]) == []
