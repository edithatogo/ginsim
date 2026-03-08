import os
import time

import pytest
from loguru import logger
from playwright.sync_api import Frame, Page, sync_playwright

REMOTE_DASHBOARD_URL = os.environ.get("GDPE_REMOTE_DASHBOARD_URL")
REMOTE_DASHBOARD_TIMEOUT_MS = int(os.environ.get("GDPE_REMOTE_DASHBOARD_TIMEOUT_MS", "420000"))
EXPECTED_HEADING = "Policy Impact Explorer"
EXPECTED_NAV_BUTTONS = (
    "Main Dashboard",
    "Evidence Explorer",
)
EXPECTED_SIDEBAR_PAGES = (
    ("Game Diagrams", "Game Diagrams"),
    ("Sensitivity", "Sensitivity Analysis"),
    ("Scenarios", "Policy Scenarios & Stories"),
    ("Extended Games", "Extended Strategic Games"),
    ("Delta View", "Fairness Audit"),
)
EXPECTED_RESULT_LABELS = (
    "People Choosing to Test",
    "Net Social Benefit",
    "Technical Evidence",
)
KNOWN_ERROR_TEXT = (
    "Error installing requirements.",
    "Error running app",
    "This app has encountered an error",
    "Could not find page:",
    "Please contact support.",
)


def _surface_text(page: Page) -> str:
    """Read outer page text defensively for smoke assertions."""
    try:
        return page.locator("body").inner_text(timeout=10_000)
    except Exception:
        return ""


def _frame_body_text(frame: Frame) -> str:
    """Read a frame body if it is accessible and rendered."""
    try:
        return frame.locator("body").inner_text(timeout=5_000)
    except Exception:
        return ""


def _dashboard_frame_and_text(page: Page) -> tuple[Frame | None, str]:
    """Return the Streamlit app frame and its text when available."""
    for frame in page.frames:
        body_text = _frame_body_text(frame)
        if EXPECTED_HEADING in body_text:
            return frame, body_text

    return None, _surface_text(page)


def _wait_for_frame_text(frame: Frame, expected_text: str, timeout_ms: int = 30_000) -> str:
    """Wait until expected text appears in the dashboard frame."""
    deadline = time.time() + (timeout_ms / 1000)
    last_text = ""

    while time.time() < deadline:
        body_text = _frame_body_text(frame)
        if expected_text in body_text:
            return body_text

        last_text = body_text[:500]
        frame.page.wait_for_timeout(1_500)

    pytest.fail(f"Timed out waiting for {expected_text!r}. Last frame text: {last_text}")


def _wait_for_dashboard(page: Page, remote_url: str) -> tuple[Frame, str]:
    """Poll until the deployed dashboard becomes available or timeout expires."""
    deadline = time.time() + (REMOTE_DASHBOARD_TIMEOUT_MS / 1000)
    last_state = "dashboard did not render"

    while time.time() < deadline:
        try:
            page.goto(remote_url, wait_until="domcontentloaded", timeout=120_000)
        except:
            pass
        page.wait_for_timeout(8_000)
        dashboard_frame, body_text = _dashboard_frame_and_text(page)

        if dashboard_frame is not None:
            return dashboard_frame, body_text

        matched_error = next((text for text in KNOWN_ERROR_TEXT if text in body_text), None)
        if matched_error is not None:
            last_state = matched_error
            page.wait_for_timeout(15_000)
            continue

        last_state = body_text[:500]
        page.wait_for_timeout(10_000)

    pytest.fail(
        f"Remote dashboard at {remote_url} never became ready within "
        f"{REMOTE_DASHBOARD_TIMEOUT_MS / 1000:.0f}s. Last state: {last_state}"
    )


@pytest.mark.slow()
def test_remote_app_loads():
    """Verify the deployed Streamlit app loads and core controls execute."""
    if not REMOTE_DASHBOARD_URL:
        pytest.skip("Set GDPE_REMOTE_DASHBOARD_URL to run remote dashboard smoke checks.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            dashboard_frame, body_text = _wait_for_dashboard(page, REMOTE_DASHBOARD_URL)

            assert EXPECTED_HEADING in body_text
            assert "Adjust Assumptions" in body_text
            assert "Advanced Numerical Controls" in body_text

            # Run the model
            run_btn = dashboard_frame.get_by_role("button", name="🔬 Run Model")
            run_btn.click(timeout=30_000)
            page.wait_for_timeout(8_000)

            body_text = _frame_body_text(dashboard_frame)
            for label in EXPECTED_RESULT_LABELS:
                assert label in body_text

            # Check sidebar navigation
            sidebar_nav = dashboard_frame.get_by_test_id("stSidebarNavItems")
            for sidebar_label, expected_heading in EXPECTED_SIDEBAR_PAGES:
                sidebar_nav.get_by_role("link", name=sidebar_label).click(timeout=30_000)
                page.wait_for_timeout(5_000)
                body_text = _wait_for_frame_text(dashboard_frame, expected_heading)
                assert expected_heading in body_text

            logger.success("Remote verification passed.")
        finally:
            browser.close()


if __name__ == "__main__":
    test_remote_app_loads()
