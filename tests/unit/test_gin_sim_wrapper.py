import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WRAPPER_PATH = ROOT / "gin-sim" / "app.py"
PAGES_DIR = ROOT / "gin-sim" / "pages"
ROOT_REQUIREMENTS = ROOT / "requirements.txt"
GIN_SIM_REQUIREMENTS = ROOT / "gin-sim" / "requirements.txt"


def _load_wrapper_module():
    spec = importlib.util.spec_from_file_location("gin_sim_app", WRAPPER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_wrapper_runs_source_app(monkeypatch, tmp_path):
    module = _load_wrapper_module()
    source_app = tmp_path / "streamlit_app" / "app.py"
    source_app.parent.mkdir(parents=True)
    source_app.write_text("pass\n", encoding="utf-8")

    called = {}

    def fake_run_source_path(path):
        called["path"] = path

    monkeypatch.setattr(module, "SOURCE_APP", source_app)
    monkeypatch.setattr(module, "run_source_path", fake_run_source_path)

    original_sys_path = list(sys.path)
    try:
        module.main()
    finally:
        sys.path[:] = original_sys_path

    assert called == {"path": source_app}


def test_wrapper_requires_source_app(monkeypatch, tmp_path):
    module = _load_wrapper_module()
    missing_source = tmp_path / "missing" / "app.py"
    monkeypatch.setattr(module, "SOURCE_APP", missing_source)

    with pytest.raises(FileNotFoundError, match="Source dashboard not found"):
        module.main()


@pytest.mark.parametrize(
    ("wrapper_name", "expected_target"),
    [
        ("1_Game_Diagrams.py", "streamlit_app/pages/1_Game_Diagrams.py"),
        ("2_Sensitivity.py", "streamlit_app/pages/2_Sensitivity.py"),
        ("3_Scenarios.py", "streamlit_app/pages/3_Scenarios.py"),
        ("4_Extended_Games.py", "streamlit_app/pages/4_Extended_Games.py"),
        ("5_Delta_View.py", "streamlit_app/pages/5_Delta_View.py"),
    ],
)
def test_page_wrappers_exist_and_reference_source(wrapper_name, expected_target):
    wrapper_path = PAGES_DIR / wrapper_name
    assert wrapper_path.exists()
    content = wrapper_path.read_text(encoding="utf-8")
    assert "SOURCE_PAGE" in content
    assert expected_target.split("/")[-1] in content


def test_deployment_requirements_install_project_runtime():
    root_requirements = ROOT_REQUIREMENTS.read_text(encoding="utf-8").splitlines()
    gin_sim_requirements = GIN_SIM_REQUIREMENTS.read_text(encoding="utf-8").splitlines()

    assert "-e ." in root_requirements
    assert "-e ." in gin_sim_requirements


def test_gin_sim_requirements_delegate_to_dashboard_runtime():
    gin_sim_requirements = GIN_SIM_REQUIREMENTS.read_text(encoding="utf-8")

    assert "-r ../streamlit_app/requirements.txt" in gin_sim_requirements
