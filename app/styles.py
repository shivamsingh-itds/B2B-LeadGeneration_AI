import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        /* Hide Streamlit default menu */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }

        /* Main App */
        .main {
            background-color: #0E1117;
        }

        /* Title */
        .title {
            font-size: 42px;
            font-weight: 700;
            color: white;
            margin-bottom: 0;
        }

        .subtitle {
            font-size:18px;
            color:#A6A6A6;
            margin-bottom:30px;
        }

        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color:#1E1E1E;
            border:1px solid #2E2E2E;
            padding:15px;
            border-radius:12px;
            box-shadow:0px 2px 8px rgba(0,0,0,0.25);
        }

        /* Buttons */
        .stButton>button {
            width:100%;
            border-radius:10px;
            height:50px;
            font-size:17px;
            font-weight:600;
        }

        /* Sidebar */
        section[data-testid="stSidebar"]{
            background:#111827;
        }

        /* Expander */
        .streamlit-expanderHeader{
            font-size:18px;
            font-weight:600;
        }

        /* DataFrame */
        div[data-testid="stDataFrame"]{
            border-radius:10px;
            border:1px solid #2E2E2E;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )