import pytest
from analysis.association_mining.value_kind import (
    normalize_value_kind, encode_value_object, EncodedValue,
    VK_TYPICAL, VK_MINIMUM, VK_MAXIMUM, VK_RANGE, VK_SPEC, VK_UNKNOWN,
)


def _vo(value=None, min_=None, max_=None, vk="typical", status="Reported",
        unit="cSt", method=None, source=None, alternates=None):
    return {
        "value": value,
        "min": min_,
        "max": max_,
        "value_kind": vk,
        "status": status,
        "unit": unit,
        "method": method,
        "source": source or {"file": "doc.pdf", "page": "5", "revision_date": None},
        "alternate_entries": alternates or [],
    }


class TestNormalizeValueKind:
    def test_typical(self):
        assert normalize_value_kind("typical") == VK_TYPICAL

    def test_lower_bound_aliases(self):
        for raw in ("minimum", "lower bound", "lower_bound", "minimum / lower bound"):
            assert normalize_value_kind(raw) == VK_MINIMUM, f"failed for {raw!r}"

    def test_upper_bound_aliases(self):
        for raw in ("maximum", "upper bound", "upper_bound", "maximum / upper bound"):
            assert normalize_value_kind(raw) == VK_MAXIMUM, f"failed for {raw!r}"

    def test_sds_reported_flattened(self):
        for raw in ("SDS reported", "SDS Reported", "sds reported"):
            assert normalize_value_kind(raw) == VK_TYPICAL

    def test_calculated_lower_bound(self):
        assert normalize_value_kind("calculated lower bound") == VK_MINIMUM

    def test_none_returns_unknown(self):
        assert normalize_value_kind(None) == VK_UNKNOWN

    def test_unknown_string_returns_unknown(self):
        assert normalize_value_kind("some future kind") == VK_UNKNOWN


class TestEncodeValueObject:
    def test_typical_point(self):
        enc = encode_value_object(_vo(value=100.0, vk="typical"))
        assert enc is not None
        assert enc.value == 100.0
        assert enc.lb is None
        assert enc.ub is None
        assert enc.vk == VK_TYPICAL
        assert not enc.is_bound

    def test_minimum_becomes_lb(self):
        enc = encode_value_object(_vo(value=90.0, vk="minimum"))
        assert enc is not None
        assert enc.value is None
        assert enc.lb == 90.0
        assert enc.ub is None
        assert enc.vk == VK_MINIMUM
        assert enc.is_bound

    def test_maximum_becomes_ub(self):
        enc = encode_value_object(_vo(value=-20.0, vk="maximum"))
        assert enc is not None
        assert enc.value is None
        assert enc.lb is None
        assert enc.ub == -20.0
        assert enc.vk == VK_MAXIMUM
        assert enc.is_bound

    def test_range_produces_lb_ub_midpoint(self):
        enc = encode_value_object(_vo(value=None, min_=10.0, max_=20.0, vk="range"))
        assert enc is not None
        assert enc.lb == 10.0
        assert enc.ub == 20.0
        assert enc.value == pytest.approx(15.0)
        assert enc.is_range
        assert not enc.is_bound

    def test_missing_status_returns_none(self):
        assert encode_value_object(_vo(value=100.0, status="Missing")) is None

    def test_not_required_returns_none(self):
        assert encode_value_object(_vo(value=100.0, status="Not Required")) is None

    def test_calculated_status_included(self):
        enc = encode_value_object(_vo(value=55.0, status="Calculated", vk="typical"))
        assert enc is not None
        assert enc.value == 55.0

    def test_none_vo_returns_none(self):
        assert encode_value_object(None) is None

    def test_conflict_flag_set(self):
        enc = encode_value_object(_vo(value=100.0), field_conflicts=[{"field": "kv40"}])
        assert enc is not None
        assert enc.conflict_flag is True

    def test_no_conflict(self):
        enc = encode_value_object(_vo(value=100.0), field_conflicts=[])
        assert enc is not None
        assert enc.conflict_flag is False

    def test_alternate_flag_set(self):
        enc = encode_value_object(_vo(value=100.0, alternates=[{"value": 101.0}]))
        assert enc is not None
        assert enc.alternate_flag is True

    def test_source_provenance_preserved(self):
        enc = encode_value_object(_vo(value=100.0, source={"file": "TDS_v3.pdf", "page": "2"}))
        assert enc is not None
        assert enc.source_file == "TDS_v3.pdf"
        assert enc.source_page == "2"

    def test_to_dict_has_all_keys(self):
        enc = encode_value_object(_vo(value=100.0))
        d = enc.to_dict(prefix="kv40_")
        expected_keys = {"kv40_value", "kv40_lb", "kv40_ub", "kv40_vk",
                         "kv40_unit", "kv40_method", "kv40_source_file",
                         "kv40_source_page", "kv40_conflict", "kv40_alternate"}
        assert expected_keys == set(d.keys())
