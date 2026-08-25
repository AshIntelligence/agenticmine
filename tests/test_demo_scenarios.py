import json

import pytest

from ui.demo_adapters import CATALOG, CATALOG_BY_SLUG, default_payload, run_product
from ui.demo_ux import GUIDANCE, SCENARIOS, validate_payload


def _scenario_cases():
    cases = []
    for item in CATALOG:
        slug = item["slug"]
        for index, scenario in enumerate(SCENARIOS[slug], start=1):
            cases.append(pytest.param(slug, scenario, id=f"{slug}-sample-{index}"))
    return cases


def test_guidance_and_scenarios_cover_every_product():
    expected = set(CATALOG_BY_SLUG)
    assert set(GUIDANCE) == expected
    assert set(SCENARIOS) == expected
    assert all(len(SCENARIOS[slug]) == 2 for slug in expected)
    assert all(set(GUIDANCE[slug]) == {"what", "inputs", "output"} for slug in expected)


@pytest.mark.parametrize("slug,scenario", _scenario_cases())
def test_each_alternate_dataset_runs_the_original_engine(slug, scenario):
    payload = default_payload(slug)
    payload.update(scenario["payload"])
    assert validate_payload(slug, payload) == []
    result = run_product(slug, payload)
    assert result is not None

    # For anomaly detection, an empty list is a meaningful healthy result: no
    # point crossed the configured threshold. Every other guided scenario is
    # expected to produce a non-empty structured result.
    if slug == "telemetry-anomaly-to-action" and scenario["label"] == "Stable metric":
        assert result == []
    elif isinstance(result, (dict, list, str)):
        assert result


@pytest.mark.parametrize(
    "slug,changes,expected_message",
    [
        ("experiment-analysis-copilot", {"control_success": 101, "control_n": 100}, "Control conversions cannot exceed control users"),
        ("fraud-signal-decision-engine", {"review_threshold": 0.80, "block_threshold": 0.70}, "Review threshold must be lower than block threshold"),
        ("support-knowledge-os", {"articles_json": "not-json"}, "must be valid JSON"),
        ("telemetry-anomaly-to-action", {"values": "1,2,3", "window": 5}, "Rolling window"),
        ("rag-quality-gate", {"evidence": "one passage", "citations": "3"}, "citation index"),
        ("prfaq-product-spec-agent", {"problem": ""}, "Customer problem cannot be empty"),
    ],
)
def test_common_bad_inputs_get_plain_english_validation(slug, changes, expected_message):
    payload = default_payload(slug)
    payload.update(changes)
    errors = validate_payload(slug, payload)
    assert errors
    assert expected_message.lower() in " ".join(errors).lower()


def test_json_samples_are_real_json_lists():
    json_fields = {
        "instagram-intentional-discovery": "items_json",
        "linkedin-career-discovery": "jobs_json",
        "product-prioritization-engine": "items_json",
        "support-knowledge-os": "articles_json",
    }
    for slug, field in json_fields.items():
        for scenario in SCENARIOS[slug]:
            parsed = json.loads(scenario["payload"][field])
            assert isinstance(parsed, list)
            assert parsed
