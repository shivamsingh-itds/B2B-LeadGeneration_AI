def validate_revenue(data, target_financial_year):
    """
    Validate extracted revenue before accepting it.
    """

    if not data:
        return False

    revenue = data.get("revenue")
    financial_year = data.get("financial_year")

    # Revenue must exist
    if revenue is None:
        return False

    # Financial year must match exactly
    if financial_year != target_financial_year:
        return False

    # Currency should exist
    if not data.get("currency"):
        return False

    # Unit should exist
    if not data.get("unit"):
        return False

    # Evidence should exist
    if not data.get("evidence"):
        return False

    return True