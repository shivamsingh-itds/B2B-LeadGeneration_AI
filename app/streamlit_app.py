import streamlit as st
import pandas as pd

from main import run_pipeline


st.set_page_config(
    page_title="LeadIntel AI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 LeadIntel AI")

st.caption(
    "AI Powered Company Intelligence Platform"
)

st.sidebar.header("Search Parameters")

industry = st.sidebar.text_input(
    "Industry",
    "Steel"
)

location = st.sidebar.text_input(
    "Location",
    "India"
)

financial_year = st.sidebar.text_input(
    "Financial Year",
    "2024-25"
)

max_companies = st.sidebar.slider(
    "Maximum Companies",
    1,
    20,
    5
)

run = st.sidebar.button(
    "Generate Intelligence"
)

if run:

    with st.spinner(
        "Researching companies..."
    ):

        output = run_pipeline(
            industry,
            location,
            financial_year,
            max_companies
        )

    results = output["results"]

    df = pd.DataFrame(results)

    st.success("Research Completed")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Companies",
        len(df)
    )

    col2.metric(
        "Revenue Found",
        len(df[df["status"] == "Found"])
    )

    col3.metric(
        "Not Found",
        len(df[df["status"] != "Found"])
    )

    st.divider()

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        "Download CSV",
        csv,
        "company_revenue.csv",
        "text/csv"
    )

    st.divider()

    st.subheader("Company Details")

    for _, row in df.iterrows():

        with st.expander(row["company_name"]):

            st.write(
                f"Revenue : {row['revenue']}"
            )

            st.write(
                f"Financial Year : {row['financial_year']}"
            )

            st.write(
                f"Revenue Type : {row['revenue_type']}"
            )

            st.write(
                f"Status : {row['status']}"
            )

            st.write(
                f"Source : {row['source_url']}"
            )

            st.write(
                f"Evidence : {row['evidence']}"
            )