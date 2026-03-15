"""
Download logs from the Streamlit Cloud management UI for a deployed app.

This script uses browser automation because Streamlit Cloud does not expose a
public logs API. It assumes the operator can authenticate interactively or via
an exported Playwright storage state file.
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--app-url",
        default="https://ginsim.streamlit.app/",
        help="Public Streamlit app URL",
    )
    parser.add_argument(
        "--storage-state",
        type=Path,
        help="Optional Playwright storage state JSON for an authenticated Streamlit session",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/streamlit_cloud_logs"),
        help="Directory where the downloaded logs should be stored",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run Chromium headlessly. Omit this flag for interactive login/debugging.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=60,
        help="Timeout for each UI action",
    )
    return parser


def _lazy_import_playwright():
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - exercised in real operator use
        msg = (
            "Playwright is required. Run this script with "
            "`uv run --with playwright python scripts/download_streamlit_cloud_logs.py ...` "
            "and install Chromium once with "
            "`uv run --with playwright python -m playwright install chromium`."
        )
        raise RuntimeError(msg) from exc
    return sync_playwright, PlaywrightTimeoutError


def _save_failure_artifacts(page, output_dir: Path, stem: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(output_dir / f"{stem}.png"), full_page=True)
    (output_dir / f"{stem}.html").write_text(page.content(), encoding="utf-8")


def _click_first(page, patterns: tuple[str, ...], timeout_ms: int) -> None:
    for pattern in patterns:
        for locator in (
            page.get_by_role("button", name=re.compile(pattern, re.IGNORECASE)),
            page.get_by_role("link", name=re.compile(pattern, re.IGNORECASE)),
            page.get_by_text(re.compile(pattern, re.IGNORECASE)),
        ):
            if locator.count():
                locator.first.click(timeout=timeout_ms)
                return

    msg = f"Could not find any UI element matching: {patterns!r}"
    raise RuntimeError(msg)


def _open_management_surface(page, timeout_ms: int, playwright_timeout):
    try:
        with page.context.expect_page(timeout=timeout_ms) as new_page:
            _click_first(page, (r"^Manage app$",), timeout_ms)
        manage_page = new_page.value
        manage_page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
        return manage_page
    except playwright_timeout:
        page.wait_for_load_state("domcontentloaded", timeout=timeout_ms)
        return page


def main() -> int:
    args = build_parser().parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    sync_playwright, playwright_timeout = _lazy_import_playwright()
    timeout_ms = args.timeout_seconds * 1000

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=args.headless)
        context_kwargs = {}
        if args.storage_state is not None:
            context_kwargs["storage_state"] = str(args.storage_state)
        context = browser.new_context(**context_kwargs)
        page = context.new_page()

        try:
            page.goto(args.app_url, wait_until="domcontentloaded", timeout=timeout_ms)
            manage_page = _open_management_surface(page, timeout_ms, playwright_timeout)
            _click_first(manage_page, (r"^Logs$", r"View logs"), timeout_ms)

            with manage_page.expect_download(timeout=timeout_ms) as download_info:
                _click_first(
                    manage_page,
                    (r"Download logs", r"Export logs", r"Download"),
                    timeout_ms,
                )
            download = download_info.value
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            suggested_name = download.suggested_filename or f"streamlit-cloud-logs-{timestamp}.zip"
            target_path = output_dir / suggested_name
            download.save_as(str(target_path))
            print(target_path)
            return 0
        except Exception:  # pragma: no cover - exercised in real operator use
            _save_failure_artifacts(page, output_dir, "streamlit-cloud-log-download-failure")
            raise
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
