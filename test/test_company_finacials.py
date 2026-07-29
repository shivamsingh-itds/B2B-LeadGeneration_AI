import json

from financials.company_financials import get_company_revenue


result = get_company_revenue(
    company_name="Tata Steel",
    financial_year="2024-25"
)

print("\nFINAL RESULT\n")

print(
    json.dumps(
        result,
        indent=4,
        ensure_ascii=False
    )
)