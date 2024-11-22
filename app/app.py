import streamlit as st
import yaml
import json

intro_page = st.Page("model/Intro.py", title="Introdução", icon="📑")
business_model_canvas = st.Page("model/BusinessModelCanvas.py", title="Business Model Canvas", icon="🗺️")
project_charter = st.Page("model/ProjectCharter.py", title="Project Charter", icon="🛣️")
data_summary_report = st.Page("model/DataSummaryReport.py", title="Data Summary Report", icon="📊")
about = st.Page("model/About.py", title="Sobre", icon="✨")
data_manipulation = st.Page("model/DataManipulation.py", title="Crescimento Real", icon="🧮")
doc_api = st.Page("model/DocAPI.py", title="Doc API", icon="📡")

pg = st.navigation([intro_page, business_model_canvas, project_charter, data_summary_report, about, data_manipulation, doc_api])

st.set_page_config(
        page_title="Intro",
        page_icon="image/Infnet_logo.png",
        layout="wide",
        initial_sidebar_state = "expanded")


#Carregar configurações
with open('app/config/config.json', 'r') as arquivo:
        st.session_state['config'] = json.loads(arquivo.read())

with open('app/config/gemini_config.yaml', 'r') as arquivo:
        st.session_state['gemini_config'] = yaml.safe_load(arquivo)


pg.run()
