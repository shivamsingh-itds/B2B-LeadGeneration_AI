import time
from search.searx_client import search_searxng


def generate_revenue_queries(company_name):
    """
    Generate targeted queries for finding
    company revenue and financial information.
    """

    queries = [
        f'"{company_name}" revenue 2025',
        f'"{company_name}" revenue FY 2024-25',
        f'"{company_name}" annual report 2025',
        f'"{company_name}" turnover 2025',
        f'"{company_name}" financial results 2025'
    ]

    return queries


def search_company_revenue(company_name, results_per_query=5):
    """
    Search SearXNG for revenue-related information
    about a company.
    """

    queries = generate_revenue_queries(company_name)

    all_results = []

    for query in queries:

        print(f"   Searching: {query}")

        results = search_searxng(
            query,
            limit=results_per_query
        )

        all_results.extend(results)

    return all_results

def rank_financial_results(results):

    keywords = {
        "annual report": 5,
        "financial results": 5,
        "revenue": 4,
        "revenue from operations": 5,
        "financial statements": 4,
        "investor relations": 4,
        "turnover": 3,
        "fy 2024-25": 3,
        "2024-25": 3,
        "fy25": 3,
        "results": 2
    }

    # Remove duplicate URLs
    unique_results = []
    seen_urls = set()

    for result in results:

        url = result.get("url", "")

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)
        unique_results.append(result)

    # Rank unique results
    ranked_results = []

    for result in unique_results:

        text = (
            result.get("title", "")
            + " "
            + result.get("content", "")
        ).lower()

        score = 0

        for keyword, points in keywords.items():
            if keyword in text:
                score += points

        result["financial_score"] = score
        ranked_results.append(result)

    ranked_results.sort(
        key=lambda x: x["financial_score"],
        reverse=True
    )

    return ranked_results

# def generate_revenue_queries(company_name, financial_year="2024-25"):
#     """
#     Generate targeted queries for a specific financial year.
#     """

#     queries = [
#         f'"{company_name}" revenue FY {financial_year}',
#         f'"{company_name}" revenue from operations FY {financial_year}',
#         f'"{company_name}" annual report {financial_year}',
#         f'"{company_name}" turnover FY {financial_year}',
#         f'"{company_name}" financial results FY {financial_year}'
#     ]

#     return queries

def generate_revenue_queries(
    company_name,
    financial_year="2024-25"
):

    return [
        (
            f'"{company_name}" '
            f'annual report {financial_year}'
        ),

        (
            f'"{company_name}" '
            f'financial results {financial_year}'
        ),

        (
            f'"{company_name}" '
            f'revenue from operations '
            f'{financial_year}'
        )
    ]

# def search_company_revenue(
#     company_name,
#     financial_year="2024-25",
#     results_per_query=5
# ):
#     queries = generate_revenue_queries(
#         company_name,
#         financial_year
#     )

#     all_results = []

#     for query in queries:

#         print(f"   Searching: {query}")

#         results = search_searxng(
#             query,
#             limit=results_per_query
#         )

#         all_results.extend(results)

#     return all_results

def search_company_revenue(
    company_name,
    financial_year="2024-25",
    results_per_query=5
):

    queries = generate_revenue_queries(
        company_name,
        financial_year
    )

    all_results = []

    for query in queries:

        print(f"   Searching: {query}")

        search_response = search_searxng(
            query,
            limit=results_per_query
        )

        # -----------------------------
        # SEARCH INFRASTRUCTURE FAILED
        # -----------------------------

        if not search_response["success"]:

            error_type = search_response[
                "error_type"
            ]

            print(
                f"   Search failed: {error_type}"
            )

            # Don't continue hammering engines
            if (
                error_type
                == "SEARCH_ENGINE_UNAVAILABLE"
            ):
                return {
                    "success": False,
                    "error_type": error_type,
                    "results": []
                }

            continue

        results = search_response["results"]

        # -----------------------------
        # RESULTS FOUND
        # -----------------------------

        if results:

            all_results.extend(results)

            print(
                f"   Found {len(results)} results."
            )

            # IMPORTANT:
            # enough results → stop searching
            if len(all_results) >= results_per_query:

                print(
                    "   Enough financial sources found. "
                    "Stopping additional searches."
                )

                break

        else:

            print(
                "   No results for this query."
            )

        # Small polite delay
        time.sleep(1)

    return {
        "success": True,
        "error_type": None,
        "results": all_results
    }