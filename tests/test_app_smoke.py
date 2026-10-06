from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_SCRIPTS = [PROJECT_ROOT / "Overview.py", *sorted((PROJECT_ROOT / "pages").glob("*.py"))]


@pytest.mark.parametrize("script_path", APP_SCRIPTS, ids=lambda path: path.stem)
def test_app_script_runs_without_exception(script_path: Path) -> None:
    app = AppTest.from_file(str(script_path)).run(timeout=60)
    assert not app.exception, "\n".join(str(error) for error in app.exception)