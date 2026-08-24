import pytest

from ui.demo_adapters import CATALOG, default_payload, run_product, verify_catalog


def test_catalog_maps_exactly_twenty_unique_engines():
    check = verify_catalog()
    assert check == {"count": 20, "unique": True, "missing": []}


@pytest.mark.parametrize("slug", [item["slug"] for item in CATALOG])
def test_default_interaction_runs_against_original_engine(slug):
    result = run_product(slug, default_payload(slug))
    assert result is not None
