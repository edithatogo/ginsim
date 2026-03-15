import os
import time
from contextlib import suppress

import pytest
from loguru import logger
from playwright.sync_api import Frame, Page, sync_playwright

from tests.e2e.remote_app_cases import REMOTE_SMOKE_CASES

REMOTE_DASHBOARD_URL = os.environ.get("GDPE_REMOTE_DASHBOARD_URL")
REMOTE_DASHBOARD_TIMEOUT_MS = int(os.environ.get("GDPE_REMOTE_DASHBOARD_TIMEOUT_MS", "420000"))
EXPECTED_HEADING = "Genetic Discrimination: Global Policy Explorer"
EXPECTED_RESULT_LABELS = (
    "Testing Uptake",
    "Net Social Benefit",
)
KNOWN_ERROR_TEXT = (
    "Error installing requirements.",
    "Error running app",
    "This app has encountered an error",
    "TypeError:",
    "Traceback:",
    "Could not find page:",
    "Please contact support.",
)

FATAL_REMOTE_ERROR_TEXT = (
    "Error installing requirements.",
    "Error running app",
    "This app has encountered an error",
    "TypeError:",
    "Traceback:",
    "Could not find page:",
)


def _surface_text(surface: Page | Frame) -> str:
    """Read outer page text defensively for smoke assertions."""
    try:
        return surface.locator("body").inner_text(timeout=10_000)
    except Exception:
        return ""


def _dashboard_surface_and_text(page: Page) -> tuple[Page | Frame | None, str]:
    """Return the Streamlit app surface and its text when available."""
    for frame in page.frames:
        body_text = _surface_text(frame)
        if EXPECTED_HEADING in body_text or "Adjust Assumptions" in body_text:
            return frame, body_text

    body_text = _surface_text(page)
    if EXPECTED_HEADING in body_text or "Adjust Assumptions" in body_text:
        return page, body_text

    return None, body_text


def _wait_for_surface_text(
    surface: Page | Frame, expected_text: str, timeout_ms: int = 30_000
) -> str:
    """Wait until expected text appears in the dashboard surface."""
    deadline = time.time() + (timeout_ms / 1000)
    last_text = ""

    while time.time() < deadline:
        body_text = _surface_text(surface)
        if expected_text in body_text:
            return body_text

        last_text = body_text[:500]
        if isinstance(surface, Frame):
            surface.page.wait_for_timeout(1_500)
        else:
            surface.wait_for_timeout(1_500)

    pytest.fail(f"Timed out waiting for {expected_text!r}. Last frame text: {last_text}")


def _click_and_wait(
    surface: Page | Frame, button_name: str, expected_text: str, timeout_ms: int = 45_000
) -> str:
    """Click a button and wait for the expected output text to appear."""
    surface.get_by_role("button", name=button_name).click(timeout=30_000)
    if isinstance(surface, Frame):
        surface.page.wait_for_timeout(3_000)
    else:
        surface.wait_for_timeout(3_000)
    return _wait_for_surface_text(surface, expected_text, timeout_ms=timeout_ms)


def _wait_for_dashboard(page: Page, remote_url: str) -> tuple[Page | Frame, str]:
    """Poll until the deployed dashboard becomes available or timeout expires."""
    deadline = time.time() + (REMOTE_DASHBOARD_TIMEOUT_MS / 1000)
    last_state = "dashboard did not render"

    while time.time() < deadline:
        with suppress(Exception):
            page.goto(remote_url, wait_until="domcontentloaded", timeout=120_000)

        page.wait_for_timeout(8_000)
        dashboard_surface, body_text = _dashboard_surface_and_text(page)

        if dashboard_surface is not None:
            return dashboard_surface, body_text

        matched_error = next((text for text in KNOWN_ERROR_TEXT if text in body_text), None)
        if matched_error is not None:
            last_state = matched_error
            if matched_error in FATAL_REMOTE_ERROR_TEXT:
                pytest.fail(
                    f"Remote dashboard at {remote_url} returned a fatal app error: {matched_error}"
                )
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
            dashboard_surface, body_text = _wait_for_dashboard(page, REMOTE_DASHBOARD_URL)

            assert EXPECTED_HEADING in body_text
            assert "Adjust Assumptions" in body_text
            assert "Distributional Equity" in body_text

            run_btn = dashboard_surface.get_by_role("button", name="🔬 Run Evaluation")
            run_btn.click(timeout=30_000)
            page.wait_for_timeout(8_000)

            body_text = _surface_text(dashboard_surface)
            for label in EXPECTED_RESULT_LABELS:
                assert label in body_text

            sidebar_nav = dashboard_surface.get_by_test_id("stSidebarNavItems")
            for case in REMOTE_SMOKE_CASES:
                sidebar_nav.get_by_role("link", name=case.sidebar_label).click(timeout=30_000)
                page.wait_for_timeout(5_000)
                body_text = _wait_for_surface_text(dashboard_surface, case.expected_heading)
                assert case.expected_heading in body_text

                if case.action_button and case.expected_text:
                    body_text = _click_and_wait(
                        dashboard_surface,
                        case.action_button,
                        case.expected_text,
                    )

                for expected_fragment in case.additional_assertions:
                    body_text = _wait_for_surface_text(
                        dashboard_surface,
                        expected_fragment,
                        timeout_ms=60_000,
                    )
                    assert expected_fragment in body_text

            logger.success("Remote verification passed.")
        finally:
            browser.close()


if __name__ == "__main__":
    test_remote_app_loads()
