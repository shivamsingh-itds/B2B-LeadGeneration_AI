import json

from search.searx_client import search_searxng
from search.query_generator import generate_company_queries
from llm.client import get_llm_response


def discover_company_sources(industry, location, results_per_query=10):
    """
    Collect search results from multiple SearXNG queries.
    """

    queries = generate_company_queries(industry, location)

    all_results = []

    for query in queries:

        print(f"Searching: {query}")

        results = search_searxng(
            query,
            limit=results_per_query
        )

        all_results.extend(results)

    return all_results


def extract_companies(search_results, industry, location):
    """
    Use the LLM to extract actual company names
    from SearXNG search results.
    """

    search_text = ""

    for index, result in enumerate(search_results, start=1):

        search_text += f"""
Result {index}
Title: {result['title']}
Content: {result['content']}
URL: {result['url']}

"""

    prompt = f"""
You are a company research assistant.

The user wants companies from:

Industry: {industry}
Location: {location}

Below are web search results.

Your job is to identify actual company names that appear
in these search results and are relevant to the requested
industry and location.

Rules:

1. Only extract real company names supported by the search results.
2. Do not invent companies.
3. Do not return directory websites such as Justdial,
   IndiaMART or Yellow Pages as companies.
4. Remove duplicate companies.
5. The company should be relevant to the requested industry.
6. The company should have a reasonable connection to the
   requested location.
7. If you are uncertain whether something is a company,
   do not include it.

Return a valid JSON object following the required schema.
Do not include explanations, markdown formatting, or additional text.

Required format:

{{
    "companies": [
        {{
            "company_name": "Example Steel Ltd",
            "source_url": "https://example.com"
        }}
    ]
}}

SEARCH RESULTS:

{search_text}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = get_llm_response(messages)

    try:
        data = json.loads(response)

        return data.get("companies", [])

    except json.JSONDecodeError:

        print("\nCould not parse LLM JSON response:")
        print(response)

        return []