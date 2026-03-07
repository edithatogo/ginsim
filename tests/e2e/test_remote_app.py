import os
import time

import pytest
from playwright.sync_api import Page, sync_playwright

REMOTE_DASHBOARD_URL = os.environ.get("GDPE_REMOTE_DASHBOARD_URL")
REMOTE_DASHBOARD_TIMEOUT_MS = int(os.environ.get("GDPE_REMOTE_DASHBOARD_TIMEOUT_MS", "420000"))
EXPECTED_HEADING = "Genetic Discrimination Policy Dashboard"
EXPECTED_NAV_BUTTONS = (
    "🎮 Go to Game Diagrams",
    "📊 Go to Sensitivity Analysis",
    "🎯 Go to Scenario Analysis",
)
EXPECTED_RESULT_LABELS = (
    "Testing Uptake",
    "Long-run Net Welfare",
    "Compliance Rate",
    "Average Premium Index",
)
KNOWN_ERROR_TEXT = (
    "Error installing requirements.",
    "This app has encountered an error",
    "Could not find page:",
    "Manage app",
)


def _body_text(page: Page) -> str:
    """Read page body text defensively for smoke assertions."""
    return page.locator("body").inner_text(timeout=10_000)


def _wait_for_dashboard(page: Page, remote_url: str) -> str:
    """Poll until the deployed dashboard becomes available or timeout expires."""
    deadline = time.time() + (REMOTE_DASHBOARD_TIMEOUT_MS / 1000)
    last_state = "dashboard did not render"

    while time.time() < deadline:
        page.goto(remote_url, wait_until="domcontentloaded", timeout=120_000)
        page.wait_for_timeout(8_000)
        body_text = _body_text(page)

        if EXPECTED_HEADING in body_text:
            return body_text

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


@pytest.mark.slow
def test_remote_app_loads():
    """Verify the deployed Streamlit app loads and core controls execute."""
    if not REMOTE_DASHBOARD_URL:
        pytest.skip("Set GDPE_REMOTE_DASHBOARD_URL to run remote dashboard smoke checks.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            body_text = _wait_for_dashboard(page, REMOTE_DASHBOARD_URL)

            assert EXPECTED_HEADING in body_text
            assert "Plain-language guide and glossary" in body_text
            assert "Jurisdiction" in body_text
            assert "Policy Regime" in body_text

            for nav_button in EXPECTED_NAV_BUTTONS:
                assert nav_button in body_text

            page.get_by_role("button", name="🔬 Run Model").click(timeout=30_000)
            page.wait_for_timeout(5_000)
            body_text = _body_text(page)

            assert "Model evaluation complete!" in body_text
            for label in EXPECTED_RESULT_LABELS:
                assert label in body_text

            page.get_by_role("button", name="📊 Go to Sensitivity Analysis").click(timeout=30_000)
            page.wait_for_timeout(5_000)
            body_text = _body_text(page)
            assert "Comprehensive Sensitivity Analysis" in body_text
        finally:
            browser.close()


if __name__ == "__main__":
    test_remote_app_loads()
