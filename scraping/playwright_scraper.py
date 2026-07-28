from playwright.sync_api import sync_playwright


def scrape_with_playwright(url):
    """
    Use a real browser for pages that requests
    cannot retrieve properly.
    """

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            text = page.locator("body").inner_text()

            browser.close()

            return {
                "success": True,
                "type": "playwright",
                "text": text,
                "error": None
            }

    except Exception as e:

        return {
            "success": False,
            "type": "playwright",
            "text": "",
            "error": str(e)
        }