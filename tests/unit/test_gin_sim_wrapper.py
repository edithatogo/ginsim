import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
WRAPPER_PATH = ROOT / "gin-sim" / "app.py"


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

    def fake_run_path(path, run_name):
        called["path"] = path
        called["run_name"] = run_name

    monkeypatch.setattr(module, "SOURCE_APP", source_app)
    monkeypatch.setattr(module.runpy, "run_path", fake_run_path)

    original_sys_path = list(sys.path)
    try:
        module.main()
    finally:
        sys.path[:] = original_sys_path

    assert called == {"path": str(source_app), "run_name": "__main__"}


def test_wrapper_requires_source_app(monkeypatch, tmp_path):
    module = _load_wrapper_module()
    missing_source = tmp_path / "missing" / "app.py"
    monkeypatch.setattr(module, "SOURCE_APP", missing_source)

    with pytest.raises(FileNotFoundError, match="Source dashboard not found"):
        module.main()
