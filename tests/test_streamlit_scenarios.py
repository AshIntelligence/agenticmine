from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from ui.demo_adapters import CATALOG
from ui.demo_ux import GUIDANCE, SCENARIOS

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "streamlit_app.py"


@pytest.mark.parametrize("item", CATALOG, ids=lambda item: item["slug"])
def test_each_product_explains_inputs_and_runs_two_guided_scenarios(item):
    slug = item["slug"]
    app = AppTest.from_file(str(HUB))
    app.query_params["product"] = slug
    app.run(timeout=30)

    assert not app.exception
    markdown_text = " ".join(str(block.value) for block in app.markdown)
    visible_text = " ".join(str(block.value) for block in [*app.markdown, *app.info])
    assert "How to use this demo" in markdown_text
    assert "What it does" in markdown_text
    assert "Inputs" in markdown_text
    assert "Output" in markdown_text
    assert GUIDANCE[slug]["what"] in visible_text

    outputs = []
    for scenario in SCENARIOS[slug]:
        sample_button = next(button for button in app.button if button.label == f"Load: {scenario['label']}")
        sample_button.click().run(timeout=30)
        assert not app.exception

        run_button = next(button for button in app.button if button.label == "Run system")
        run_button.click().run(timeout=30)
        assert not app.exception
        assert f"demo-error:{slug}" not in app.session_state
        result = app.session_state[f"demo-result:{slug}"]
        assert result is not None
        outputs.append(repr(result))

    assert outputs[0] != outputs[1], "The two guided scenarios should exercise observably different product behavior."


def test_stable_telemetry_result_is_explained_in_plain_english():
    slug = "telemetry-anomaly-to-action"
    app = AppTest.from_file(str(HUB))
    app.query_params["product"] = slug
    app.run(timeout=30)

    stable = next(button for button in app.button if button.label == "Load: Stable metric")
    stable.click().run(timeout=30)
    run_button = next(button for button in app.button if button.label == "Run system")
    run_button.click().run(timeout=30)

    assert not app.exception
    assert app.session_state[f"demo-result:{slug}"] == []
    assert any("No anomalies detected" in str(message.value) for message in app.success)
