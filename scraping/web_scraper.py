import requests
from bs4 import BeautifulSoup

from scraping.pdf_scraper import scrape_pdf
from scraping.playwright_scraper import scrape_with_playwright


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def scrape_webpage(url):
    """
    Smart scraper.

    PDF       -> PyPDF
    HTML      -> Requests + BeautifulSoup
    Failure   -> Playwright
    """

    # ---------------------------------
    # PDF
    # ---------------------------------

    if url.lower().split("?")[0].endswith(".pdf"):

        print("   PDF detected → using PDF scraper")

        return scrape_pdf(url)

    # ---------------------------------
    # Normal webpage
    # ---------------------------------

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type",
            ""
        ).lower()

        # Sometimes PDF URL doesn't end with .pdf
        if "application/pdf" in content_type:

            print("   PDF content detected → using PDF scraper")

            return scrape_pdf(url)

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "noscript"
        ]):
            element.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Page returned but useful content wasn't available
        if len(text) < 200:

            print(
                "   Insufficient HTML → trying Playwright"
            )

            return scrape_with_playwright(url)

        return {
            "success": True,
            "type": "html",
            "text": text,
            "error": None
        }

    except requests.RequestException as e:

        print(
            f"   Requests failed → trying Playwright"
        )

        playwright_result = scrape_with_playwright(url)

        if playwright_result["success"]:
            return playwright_result

        return {
            "success": False,
            "type": "unknown",
            "text": "",
            "error": (
                f"Requests: {str(e)} | "
                f"Playwright: {playwright_result['error']}"
            )
        }