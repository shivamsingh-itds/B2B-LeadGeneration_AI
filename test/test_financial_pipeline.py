import json
from financials.validator import validate_revenue

from financials.revenue_search import (
    search_company_revenue,
    rank_financial_results
)

from scraping.web_scraper import scrape_webpage
from financials.revenue_extractor import extract_revenue

company = "Tata Steel"
target_financial_year = "2024-25"

print(f"\nSearching revenue information for: {company}\n")

search_results = search_company_revenue(
    company,
    financial_year=target_financial_year,
    results_per_query=5
)


print(
    f"\nCollected {len(search_results)} search results."
)


ranked_results = rank_financial_results(
    search_results
)


print("\nTop financial sources:\n")

for i, result in enumerate(
    ranked_results[:5],
    start=1
):
    print(
        f"{i}. [{result['financial_score']}] "
        f"{result['title']}"
    )
    print(result["url"])
    print()


print("\nTrying to extract revenue...\n")


for result in ranked_results[:5]:

    url = result["url"]

    print(f"Checking: {url}")

    scraped = scrape_webpage(url)

    if not scraped["success"]:

        print(
            f"Skipped: {scraped['error']}\n"
        )
        continue


    if len(scraped["text"]) < 200:

        print(
            "Skipped: Not enough webpage content.\n"
        )
        continue


    revenue_data = extract_revenue(
    company_name=company,
    financial_year=target_financial_year,
    source_text=scraped["text"],
    source_url=url
)


    if validate_revenue(
    revenue_data,
    target_financial_year
):
        print("\nValid revenue found!\n")

        print(
            json.dumps(
                revenue_data,
                indent=4,
                ensure_ascii=False
            )
        )

        break

    else:
        print(
            f"No valid FY {target_financial_year} "
            f"revenue found on this page.\n"
        )