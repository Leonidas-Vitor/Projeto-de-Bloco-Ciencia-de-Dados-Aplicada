import streamlit as st


intro_page = st.Page("model/Intro.py", title="Introdução", icon="📑")
business_model_canvas = st.Page("model/BusinessModelCanvas.py", title="Business Model Canvas", icon="🗺️")
project_charter = st.Page("model/ProjectCharter.py", title="Project Charter", icon="🛣️")
data_summary_report = st.Page("model/DataSummaryReport.py", title="Data Summary Report", icon="📊")

pg = st.navigation([intro_page, business_model_canvas, project_charter, data_summary_report])

st.set_page_config(
        page_title="Intro",
        page_icon="image/Infnet_logo.png",
        layout="wide",
        initial_sidebar_state = "expanded")

pg.run()
