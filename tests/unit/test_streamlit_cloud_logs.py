from pathlib import Path
from zipfile import ZipFile

from src.utils.streamlit_cloud_logs import summarise_streamlit_cloud_log


def test_summarise_streamlit_cloud_log_groups_repeated_tracebacks(tmp_path: Path) -> None:
    log_path = tmp_path / "streamlit.log"
    log_path.write_text(
        """
Traceback (most recent call last):
  File "/mount/src/ginsim/streamlit_app/pages/3_Scenarios.py", line 18, in <module>
    from src.model.scenario_analysis import load_scenarios
ModuleNotFoundError: No module named 'src'

Traceback (most recent call last):
  File "/mount/src/ginsim/streamlit_app/pages/3_Scenarios.py", line 18, in <module>
    from src.model.scenario_analysis import load_scenarios
ModuleNotFoundError: No module named 'src'
""".strip(),
        encoding="utf-8",
    )

    findings = summarise_streamlit_cloud_log(log_path)

    assert len(findings) == 1
    assert findings[0].count == 2
    assert findings[0].signature.startswith(
        "/mount/src/ginsim/streamlit_app/pages/3_Scenarios.py -> ModuleNotFoundError"
    )


def test_summarise_streamlit_cloud_log_reads_zip_archives(tmp_path: Path) -> None:
    archive_path = tmp_path / "logs.zip"
    inner_name = "app.log"
    with ZipFile(archive_path, "w") as archive:
        archive.writestr(
            inner_name,
            """
2026-03-15 00:00:00 Error running app
TypeError: unexpected config value
""".strip(),
        )

    findings = summarise_streamlit_cloud_log(archive_path)

    assert len(findings) == 2
    assert findings[0].sources == (inner_name,)
    assert findings[0].signature == "Error running app"
