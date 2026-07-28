import io
import requests
from pypdf import PdfReader


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


def scrape_pdf(url):
    """
    Download a PDF and extract its text.
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=60
        )

        response.raise_for_status()

        pdf_file = io.BytesIO(response.content)

        reader = PdfReader(pdf_file)

        text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text_parts.append(page_text)

        text = "\n".join(text_parts)

        return {
            "success": True,
            "type": "pdf",
            "text": text,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "type": "pdf",
            "text": "",
            "error": str(e)
        }