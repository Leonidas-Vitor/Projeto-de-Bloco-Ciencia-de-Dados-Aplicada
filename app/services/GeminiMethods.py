import streamlit as st
import google.generativeai as genai

@st.cache_data
def TranslateStocksInfo(industry:str, sector:str, description:str):
    '''
    Traduz as informações de uma ação para o português
    '''
    genai.configure(api_key=st.secrets['GEMINI_KEY'])
    model = genai.GenerativeModel(st.session_state['gemini_config']['TRANSLATE_CONFIG']['model']
                              ,system_instruction = st.session_state['gemini_config']['TRANSLATE_CONFIG']['system_instruction']
                              ,safety_settings = st.session_state['gemini_config']['TRANSLATE_CONFIG']['safety_settings']
                              ,generation_config = st.session_state['gemini_config']['TRANSLATE_CONFIG']['generation_config'])
    
    pt_industry = model.generate_content(industry).text
    pt_sector = model.generate_content(sector).text
    pt_description = model.generate_content(description).text
    return pt_industry, pt_sector, pt_description

@st.cache_data
def GenerateReport(acoes_selecionadas, df_acoes_selecionadas, df_acoes_valores, df_dolar, df_ipca, df_selic):
    '''
    Gera um relatório sobre o mercado de ações
    '''
    genai.configure(api_key=st.secrets['GEMINI_KEY'])
    model = genai.GenerativeModel(st.session_state['gemini_config']['REPORT_CONFIG']['model']
                              ,system_instruction = st.session_state['gemini_config']['REPORT_CONFIG']['system_instruction']
                              ,safety_settings = st.session_state['gemini_config']['REPORT_CONFIG']['safety_settings']
                              ,generation_config = st.session_state['gemini_config']['REPORT_CONFIG']['generation_config'])
    
    content = model.generate_content([
        df_acoes_selecionadas.to_json(),
        df_acoes_valores[df_acoes_valores['ticker'].isin(acoes_selecionadas)].to_json(), 
        df_dolar.to_json(), 
        df_ipca.to_json(), 
        df_selic.to_json()])
    
    return content.text, content.usage_metadata