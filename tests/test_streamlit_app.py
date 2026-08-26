from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from ui.demo_adapters import CATALOG

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "streamlit_app.py"


@pytest.mark.parametrize("entrypoint", ["app.py", "streamlit_app.py"])
def test_streamlit_apps_boot_without_exception(entrypoint):
    app = AppTest.from_file(str(ROOT / entrypoint))
    app.run(timeout=30)
    assert not app.exception


@pytest.mark.parametrize("item", CATALOG, ids=lambda item: item["slug"])
def test_every_product_deep_link_renders_and_submits(item):
    slug = item["slug"]
    app = AppTest.from_file(str(HUB))
    app.query_params["product"] = slug
    app.run(timeout=30)

    assert not app.exception
    assert any(item["title"] in block.value for block in app.markdown)

    run_button = next(button for button in app.button if button.label == "Run system")
    run_button.click().run(timeout=30)

    assert not app.exception
    assert app.session_state[f"demo-result:{slug}"] is not None


def test_grounded_agent_accepts_a_question_and_returns_evidence():
    app = AppTest.from_file(str(HUB))
    app.session_state["selected_product"] = "__agent__"
    app.run(timeout=30)

    assert not app.exception
    ask_button = next(button for button in app.button if button.label == "Run grounded Q&A")
    ask_button.click().run(timeout=30)

    assert not app.exception
    result = app.session_state["grounded-agent-result"]
    assert result["answer"]
    assert result["evidence"]
    assert result["evals"]


def test_unknown_product_route_falls_back_to_curated_hub():
    app = AppTest.from_file(str(HUB))
    app.query_params["product"] = "not-a-real-product"
    app.run(timeout=30)

    assert not app.exception
    assert any(metric.label == "Runnable systems" and metric.value == "20" for metric in app.metric)
    assert any(metric.label == "Areas" and metric.value == "3" for metric in app.metric)
    assert any("AI product decisions" in block.value for block in app.markdown)
