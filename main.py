from discovery.company_finder import (
    discover_company_sources,
    extract_companies
)

from financials.company_financials import (
    get_company_revenue
)

from output.exporter import export_to_csv


def main():

    print("=" * 60)
    print("              LeadGen AI")
    print("=" * 60)

    industry = input(
        "\nEnter industry: "
    ).strip()

    location = input(
        "Enter location: "
    ).strip()

    financial_year = input(
        "Enter financial year : "
    ).strip()

    if not financial_year:
        financial_year = "2024-25"

    # --------------------------------
    # COMPANY DISCOVERY
    # --------------------------------

    print("\n[1/4] Discovering companies...\n")

    search_results = discover_company_sources(
        industry,
        location,
        results_per_query=10
    )

    print(
        f"\nCollected {len(search_results)} "
        f"search results."
    )

    # --------------------------------
    # LLM COMPANY EXTRACTION
    # --------------------------------

    print("\n[2/4] Extracting company names...\n")

    companies = extract_companies(
        search_results,
        industry,
        location
    )
    # companies = companies[:3]

    print(
        f"Found {len(companies)} companies.\n"
    )

    for index, company in enumerate(
        companies,
        start=1
    ):
        print(
            f"{index}. {company['company_name']}"
        )

    # --------------------------------
    # REVENUE RESEARCH
    # --------------------------------

    print("\n[3/4] Researching company revenues...\n")

    final_results = []

    for index, company in enumerate(
        companies,
        start=1
    ):

        company_name = company["company_name"]

        print(
            f"\n[{index}/{len(companies)}] "
            f"{company_name}"
        )

        financial_data = get_company_revenue(
            company_name,
            financial_year
        )

        financial_data["industry"] = industry
        financial_data["location"] = location

        final_results.append(
            financial_data
        )

    # --------------------------------
    # EXPORT
    # --------------------------------

    print("\n[4/4] Exporting results...\n")

    filepath = export_to_csv(
        final_results
    )

    # --------------------------------
    # SUMMARY
    # --------------------------------

    found = sum(
        1
        for result in final_results
        if result["status"] == "Found"
    )

    print("=" * 60)

    print("Research completed.")

    print(
        f"Companies researched : "
        f"{len(final_results)}"
    )

    print(
        f"Revenue found        : {found}"
    )

    print(
        f"Revenue not found    : "
        f"{len(final_results) - found}"
    )

    print(
        f"CSV saved            : {filepath}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()