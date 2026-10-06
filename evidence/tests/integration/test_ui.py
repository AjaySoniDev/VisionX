from pathlib import Path

import pytest


def test_local_ui_loads_and_reports_missing_inputs_accessibly():
    pytest.importorskip("streamlit")
    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(Path(__file__).resolve().parents[2] / "apps/streamlit_app.py")).run()
    assert not app.exception
    assert "exploration-order" in app.warning[0].value
    app.button[0].click().run()
    assert not app.exception
    assert "Provide one learning journey" in app.error[0].value
