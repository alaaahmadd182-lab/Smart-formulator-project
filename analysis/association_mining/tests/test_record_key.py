import json
import pathlib
import tempfile
import pytest
from analysis.association_mining.record_key import (
    ProductKey, key_from_path, group_by_product, strip_tier_suffix,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def products_root(tmp_path):
    """Minimal Products_json tree with both record_id schemes."""
    root = tmp_path / "Products_json"

    # Scheme A: shared record_id across tiers (ADNOC style)
    adnoc = root / "Base_oils_json" / "ADNOC" / "ADNOC_ADBASE_2CST"
    adnoc.mkdir(parents=True)
    for tier, label in [(1, "blocking"), (2, "verification"), (3, "substitution")]:
        (adnoc / f"ADNOC_ADBASE_2CST__base_oil_tier{tier}_{label}.json").write_text(
            json.dumps({
                "material_class": "base_oil",
                "tier": tier,
                "record_id": "BO-ADNOC-ADBASE-2-CST",
                "fields": {},
                "open_questions": [],
                "conflicts": [],
            }),
            encoding="utf-8",
        )

    # Scheme B: tier-suffixed record_ids (ExxonMobil style)
    emmo = root / "Base_oils_json" / "ExxonMobil" / "EMMO_EHC_120"
    emmo.mkdir(parents=True)
    for tier in [1, 2, 3]:
        (emmo / f"EMMO_EHC_120__base_oil_tier{tier}.json").write_text(
            json.dumps({
                "material_class": "base_oil",
                "tier": tier,
                "record_id": f"BO-EMMO-EHC-120__T{tier}",
                "fields": {},
                "open_questions": [],
                "conflicts": [],
            }),
            encoding="utf-8",
        )

    # Additive package (2 tiers)
    pkg = root / "Additive_packages_json" / "Infineum" / "INF_P6150"
    pkg.mkdir(parents=True)
    for tier, label in [(1, "route_defining"), (2, "numeric_contribution")]:
        (pkg / f"tier{tier}_{label}.json").write_text(
            json.dumps({
                "material_class": "additive_package",
                "tier": tier,
                "record_id": "AP-INF-P6150",
                "fields": {},
                "open_questions": [],
                "conflicts": [],
            }),
            encoding="utf-8",
        )

    return root


# ---------------------------------------------------------------------------
# ProductKey
# ---------------------------------------------------------------------------

class TestProductKey:
    def test_folder_path_format(self):
        k = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        assert k.folder_path == "Base_oils_json/ADNOC/ADNOC_ADBASE_2CST"

    def test_str_representation(self):
        k = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        assert str(k) == "base_oil::ADNOC/ADNOC_ADBASE_2CST"

    def test_equality(self):
        k1 = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        k2 = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        assert k1 == k2

    def test_different_suppliers_not_equal(self):
        k1 = ProductKey("base_oil", "ADNOC", "X")
        k2 = ProductKey("base_oil", "ExxonMobil", "X")
        assert k1 != k2

    def test_hashable(self):
        k = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        d = {k: "ok"}
        assert d[k] == "ok"


# ---------------------------------------------------------------------------
# key_from_path
# ---------------------------------------------------------------------------

class TestKeyFromPath:
    def test_base_oil(self, products_root):
        f = products_root / "Base_oils_json/ADNOC/ADNOC_ADBASE_2CST/ADNOC_ADBASE_2CST__base_oil_tier1_blocking.json"
        k = key_from_path(f, products_root)
        assert k.material_class == "base_oil"
        assert k.supplier == "ADNOC"
        assert k.product_id == "ADNOC_ADBASE_2CST"

    def test_additive_package(self, products_root):
        f = products_root / "Additive_packages_json/Infineum/INF_P6150/tier1_route_defining.json"
        k = key_from_path(f, products_root)
        assert k.material_class == "additive_package"
        assert k.supplier == "Infineum"

    def test_tier_suffix_scheme_gives_same_key(self, products_root):
        f1 = products_root / "Base_oils_json/ExxonMobil/EMMO_EHC_120/EMMO_EHC_120__base_oil_tier1.json"
        f2 = products_root / "Base_oils_json/ExxonMobil/EMMO_EHC_120/EMMO_EHC_120__base_oil_tier2.json"
        assert key_from_path(f1, products_root) == key_from_path(f2, products_root)


# ---------------------------------------------------------------------------
# group_by_product
# ---------------------------------------------------------------------------

class TestGroupByProduct:
    def test_groups_all_tiers_under_one_key(self, products_root):
        groups = group_by_product(products_root)
        adnoc_key = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        assert adnoc_key in groups
        assert set(groups[adnoc_key].tiers.keys()) == {1, 2, 3}

    def test_tier_suffix_scheme_joins_correctly(self, products_root):
        groups = group_by_product(products_root)
        emmo_key = ProductKey("base_oil", "ExxonMobil", "EMMO_EHC_120")
        assert emmo_key in groups
        assert set(groups[emmo_key].tiers.keys()) == {1, 2, 3}

    def test_package_has_two_tiers(self, products_root):
        groups = group_by_product(products_root)
        pkg_key = ProductKey("additive_package", "Infineum", "INF_P6150")
        assert pkg_key in groups
        assert set(groups[pkg_key].tiers.keys()) == {1, 2}

    def test_total_product_count(self, products_root):
        groups = group_by_product(products_root)
        assert len(groups) == 3

    def test_load_tier_returns_dict(self, products_root):
        groups = group_by_product(products_root)
        adnoc_key = ProductKey("base_oil", "ADNOC", "ADNOC_ADBASE_2CST")
        data = groups[adnoc_key].load_tier(1)
        assert isinstance(data, dict)
        assert data["tier"] == 1

    def test_load_missing_tier_returns_none(self, products_root):
        groups = group_by_product(products_root)
        pkg_key = ProductKey("additive_package", "Infineum", "INF_P6150")
        assert groups[pkg_key].load_tier(3) is None


# ---------------------------------------------------------------------------
# strip_tier_suffix
# ---------------------------------------------------------------------------

class TestStripTierSuffix:
    def test_strips_t1(self):
        assert strip_tier_suffix("BO-ADNOC-X__T1") == "BO-ADNOC-X"

    def test_strips_t3(self):
        assert strip_tier_suffix("BO-EMMO-EHC-120__T3") == "BO-EMMO-EHC-120"

    def test_no_suffix_unchanged(self):
        assert strip_tier_suffix("BO-ADNOC-X") == "BO-ADNOC-X"
