import os
from datetime import datetime

import pandas as pd


def export_to_csv(results, filename=None):
    """
    Export company financial results to CSV.
    """

    os.makedirs("data", exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"company_revenue_{timestamp}.csv"

    filepath = os.path.join(
        "data",
        filename
    )

    df = pd.DataFrame(results)

    df.to_csv(
        filepath,
        index=False
    )

    return filepath