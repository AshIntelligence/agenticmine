from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("entrypoint", ["app.py", "streamlit_app.py"])
def test_streamlit_apps_boot_without_exception(entrypoint):
    app = AppTest.from_file(str(ROOT / entrypoint))
    app.run(timeout=30)
    assert not app.exception
