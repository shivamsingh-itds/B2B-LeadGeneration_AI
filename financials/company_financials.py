from financials.revenue_search import (
    search_company_revenue,
    rank_financial_results
)

from financials.revenue_extractor import extract_revenue
from financials.validator import validate_revenue
from scraping.web_scraper import scrape_webpage


def get_company_revenue(
    company_name,
    financial_year="2024-25",
    max_sources=5
):
    """
    Find and validate revenue for one company.
    """

    print(f"\nResearching revenue: {company_name}")

    # Step 1: Search financial information
    # search_results = search_company_revenue(
    #     company_name,
    #     financial_year=financial_year,
    #     results_per_query=5
    # )

    # if not search_results:
    #     print("   No financial search results found.")

    #     return {
    #         "company_name": company_name,
    #         "financial_year": financial_year,
    #         "revenue": None,
    #         "currency": None,
    #         "unit": None,
    #         "revenue_type": None,
    #         "evidence": None,
    #         "source_url": None,
    #         "status": "Not Found"
    #     }
    search_response = search_company_revenue(
    company_name,
    financial_year=financial_year,
    results_per_query=5
)


    # Search infrastructure failed
    if not search_response["success"]:

        print(
            "   Financial search unavailable."
        )

        return {
            "company_name": company_name,
            "financial_year": financial_year,
            "revenue": None,
            "currency": None,
            "unit": None,
            "revenue_type": None,
            "evidence": None,
            "source_url": None,
            "status": "Search Error"
        }


    search_results = search_response["results"]


    # Search worked but found nothing
    if not search_results:

        print(
            "   No financial information found."
        )

        return {
            "company_name": company_name,
            "financial_year": financial_year,
            "revenue": None,
            "currency": None,
            "unit": None,
            "revenue_type": None,
            "evidence": None,
            "source_url": None,
            "status": "Not Found"
        }
    
    # Step 2: Rank financial sources
    ranked_results = rank_financial_results(
        search_results
    )

    # Step 3: Try best sources
    for result in ranked_results[:max_sources]:

        url = result.get("url")

        if not url:
            continue

        print(f"   Checking: {url}")

        scraped = scrape_webpage(url)

        if not scraped["success"]:
            print("   Scraping failed.")
            continue

        if len(scraped["text"]) < 200:
            print("   Not enough content.")
            continue

        # Step 4: LLM extraction
        revenue_data = extract_revenue(
            company_name=company_name,
            financial_year=financial_year,
            source_text=scraped["text"],
            source_url=url
        )

        # Step 5: Validate
        if validate_revenue(
            revenue_data,
            financial_year
        ):

            revenue_data["status"] = "Found"

            print("   Revenue found.")

            return revenue_data

        print("   Valid revenue not found in this source.")

    # Nothing reliable found
    return {
        "company_name": company_name,
        "financial_year": financial_year,
        "revenue": None,
        "currency": None,
        "unit": None,
        "revenue_type": None,
        "evidence": None,
        "source_url": None,
        "status": "Not Found"
    }