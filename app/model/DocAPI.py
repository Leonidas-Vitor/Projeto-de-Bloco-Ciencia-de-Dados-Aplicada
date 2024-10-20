import streamlit as st
import requests
#from services import DataExtraction
#from services import API

st.title("Aplicação Streamlit com API Embutida")
#st.header("Documentação da API (Swagger UI)")
#swagger_url = "http://127.0.0.1:8000/docs"

#st.components.v1.iframe(swagger_url, height=600)

API_URL = "http://127.0.0.1:8000"

#API.run_api()

st.write('**Documentação da API**')
st.write('A API possui dois endpoints: um para requisições GET e outro para requisições POST.')
st.write('### GET /stock/{ticker}')
st.write('Retorna informações sobre uma ação específica.')
with st.expander('**Exemplo de uso:**'):
    ticker = st.text_input('Digite o ticker da ação', key='ticker1')
    if (st.button('Buscar')):
        response = requests.get(f'{API_URL}/stock/{ticker}')
        st.write(response.json())

st.write('### POST /newStock/')
st.write('Adiciona uma nova ação ao banco de dados.')
with st.expander('**Exemplo de uso:**'):
    stock_name = st.text_input('Digite o nome da ação')
    stock_ticker = st.text_input('Digite o ticker da ação', key='ticker2')
    if (st.button('Adicionar')):
        response = requests.post(f'{API_URL}/newStock/', json={"stock_name": 'stock_name', "stock_ticker": 'ITUB'})
        st.write(response.json())
