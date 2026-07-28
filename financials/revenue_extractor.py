import json

from llm.client import get_llm_response


def extract_revenue(company_name,financial_year, source_text, source_url):
    """
    Extract revenue information from financial webpage text
    using the LLM.
    """

    # Prevent sending extremely large webpages to the LLM
    source_text = find_financial_text(source_text)

    prompt = f"""
You are a financial data extraction system.

Company: {company_name}
TARGET FINANCIAL YEAR: {financial_year}

Extract revenue ONLY for the target financial year.

IMPORTANT RULES:

1. The financial year MUST be {financial_year}.
2. If revenue for {financial_year} is not explicitly available,
   return revenue as null.
3. Never return revenue from another financial year.
4. Never guess or estimate revenue.
5. Do not confuse revenue with:
   - profit
   - EBITDA
   - market capitalization
   - valuation
   - assets
   - expenses
6. Prefer consolidated figures when available.
7. Prefer Revenue from Operations over unrelated income.
8. Preserve the currency and unit reported by the source.

Return a valid JSON object only.

Required format:

{{
    "company_name": "{company_name}",
    "financial_year": "{financial_year}",
    "revenue": null,
    "currency": null,
    "unit": null,
    "revenue_type": null,
    "evidence": null,
    "source_url": "{source_url}"
}}

SOURCE TEXT:

{source_text}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = get_llm_response(messages)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        print("Failed to parse revenue extraction response.")
        print(response)
        return None

def find_financial_text(text, max_chars=20000):
    """
    Extract sections surrounding revenue-related keywords.
    """

    keywords = [
        "revenue from operations",
        "total revenue",
        "revenue",
        "turnover",
        "sales",
        "income from operations"
    ]

    text_lower = text.lower()

    chunks = []

    for keyword in keywords:

        start = 0

        while True:

            position = text_lower.find(
                keyword,
                start
            )

            if position == -1:
                break

            chunk_start = max(
                0,
                position - 1500
            )

            chunk_end = min(
                len(text),
                position + 3000
            )

            chunks.append(
                text[chunk_start:chunk_end]
            )

            start = position + len(keyword)

            if len(
                "\n\n".join(chunks)
            ) >= max_chars:
                break

        if len(
            "\n\n".join(chunks)
        ) >= max_chars:
            break

    if not chunks:
        return text[:max_chars]

    return "\n\n--- FINANCIAL SECTION ---\n\n".join(
        chunks
    )[:max_chars]