from discovery.company_finder import (
    discover_company_sources,
    extract_companies
)

from financials.company_financials import (
    get_company_revenue
)

from output.exporter import export_to_csv


def run_pipeline(
    industry,
    location,
    financial_year="2024-25",
    max_companies=3,
):

    # -----------------------------
    # COMPANY DISCOVERY
    # -----------------------------

    search_results = discover_company_sources(
        industry,
        location,
        results_per_query=10
    )

    companies = extract_companies(
        search_results,
        industry,
        location
    )

    companies = companies[:max_companies]

    final_results = []

    for company in companies:

        company_name = company["company_name"]

        financial_data = get_company_revenue(
            company_name,
            financial_year
        )

        financial_data["industry"] = industry
        financial_data["location"] = location

        final_results.append(financial_data)

    filepath = export_to_csv(final_results)

    return {
        "results": final_results,
        "filepath": filepath,
        "companies": companies
    }


def main():

    print("=" * 60)
    print("LeadIntel AI")
    print("=" * 60)

    industry = input("Enter industry: ").strip()

    location = input("Enter location: ").strip()

    financial_year = input(
        "Enter Financial Year: "
    ).strip()

    if not financial_year:
        financial_year = "2024-25"

    output = run_pipeline(
        industry,
        location,
        financial_year,
        max_companies=3
    )

    results = output["results"]

    found = sum(
        1
        for r in results
        if r["status"] == "Found"
    )

    print("\nResearch Completed\n")

    print(
        f"Companies : {len(results)}"
    )

    print(
        f"Revenue Found : {found}"
    )

    print(
        f"CSV : {output['filepath']}"
    )


if __name__ == "__main__":
    main()