from financials.revenue_search import search_company_revenue


company = "Tata Steel"

print(f"\nSearching financial information for {company}...\n")

results = search_company_revenue(
    company,
    results_per_query=3
)


print(f"\nFound {len(results)} search results.\n")


for index, result in enumerate(results, start=1):

    print(f"Result {index}")
    print(f"Title   : {result['title']}")
    print(f"Content : {result['content']}")
    print(f"URL     : {result['url']}")
    print("-" * 80)