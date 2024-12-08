import streamlit as st
import yaml
import json
from streamlit_extras.app_logo import add_logo

intro_page = st.Page("model/Intro.py", title="Introdução", icon="📑")

business_model_canvas = st.Page("model/BusinessModelCanvas.py", title="Business Model Canvas", icon="🗺️")
project_charter = st.Page("model/ProjectCharter.py", title="Project Charter", icon="🛣️")
about = st.Page("model/About.py", title="Sobre", icon="✨")

main_aplication = st.Page("model/CrescimentoReal.py", title="Crescimento Real", icon="🧮")
update_db = st.Page("model/UpdateDB.py", title="Atualizar Banco de Dados", icon="🔄")
doc_api = st.Page("model/DocAPI.py", title="Doc API", icon="📡")

pages = {
        'Introdução': [intro_page],
        'Sobre': [about, business_model_canvas, project_charter],
        'Crescimento Real': [main_aplication, update_db, doc_api, ]
}


pg = st.navigation(pages)

st.set_page_config(
        page_title="Intro",
        page_icon="app/image/Infnet_logo.png",
        layout="wide",
        initial_sidebar_state = "expanded")


#Carregar configurações
with open('app/config/config.json', 'r') as arquivo:
        st.session_state['config'] = json.loads(arquivo.read())

with open('app/config/gemini_config.yaml', 'r') as arquivo:
        st.session_state['gemini_config'] = yaml.safe_load(arquivo)

add_logo("images/infnet-30-horizontal-branco.png", height=156)

pg.run()

