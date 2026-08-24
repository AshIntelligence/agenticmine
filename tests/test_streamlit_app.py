from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_streamlit_app_boots_without_exception():
    app = AppTest.from_file(str(ROOT / "app.py"))
    app.run(timeout=30)
    assert not app.exception
