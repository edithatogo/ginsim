from playwright.sync_api import sync_playwright


def test_remote_app_loads():
    """Verify that the remote Streamlit app loads and has correct title."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Go to the deployed app
        # Streamlit apps can be slow to wake up
        page.goto("https://ginsim.streamlit.app/", wait_until="networkidle", timeout=120000)

        # Check the page title (set in set_page_config)
        assert "Genetic Discrimination" in page.title()

        # Try to find the h1
        h1 = page.locator("h1").first
        # Wait a bit for Streamlit to render the content
        page.wait_for_timeout(5000)

        if h1.count() > 0:
            assert "Genetic Discrimination" in h1.inner_text()

        browser.close()


if __name__ == "__main__":
    test_remote_app_loads()
