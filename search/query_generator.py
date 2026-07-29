def generate_company_queries(industry, location):
    """
    Generate multiple search queries to discover companies
    belonging to an industry in a specific location.
    """

    queries = [
        f"{industry} companies in {location}",
        f"{industry} manufacturers in {location}",
        f"{industry} industry companies in {location}",
        f"top {industry} companies in {location}",
        f"{industry} private limited companies in {location}",
    ]

    return queries