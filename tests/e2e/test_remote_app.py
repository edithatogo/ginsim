import os

import pytest
from playwright.sync_api import sync_playwright

REMOTE_DASHBOARD_URL = os.environ.get("GDPE_REMOTE_DASHBOARD_URL")


@pytest.mark.slow
def test_remote_app_loads():
    """Verify that an explicitly configured remote Streamlit deployment loads."""
    if not REMOTE_DASHBOARD_URL:
        pytest.skip("Set GDPE_REMOTE_DASHBOARD_URL to run remote dashboard smoke checks.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(REMOTE_DASHBOARD_URL, wait_until="networkidle", timeout=120000)
            page.wait_for_timeout(5000)

            assert "Genetic Discrimination" in page.title()

            heading = page.locator("h1").first
            expect_text = "Genetic Discrimination Policy Dashboard"
            assert heading.count() > 0
            assert expect_text in heading.inner_text()
        finally:
            browser.close()


if __name__ == "__main__":
    test_remote_app_loads()
