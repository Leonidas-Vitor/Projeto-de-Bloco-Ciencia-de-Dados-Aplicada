import streamlit as st
import requests as req
from datetime import datetime
import pandas as pd
from services import UpdateMethods as um

@st.cache_data
def GetLastDate(database, collection):
    response = eval(req.get(f'{st.session_state["config"]["API_URL"]}/mongodb/last', 
                                params={'database': database, 'collection': collection}).json())
    lastDate = datetime.strptime(response['year-month'], '%Y-%m').date()
    return lastDate

@st.cache_data
def GetLastDates():
    lastDates = {}
    lastDates['selic'] = GetLastDate(database='Indicators', collection='SELIC')
    lastDates['dolar'] = GetLastDate(database='Indicators', collection='Dollar')
    lastDates['ipca'] = GetLastDate(database='Indicators', collection='IPCA')
    lastDates['stock'] = GetLastDate(database='Stocks', collection='Prices')
    return lastDates

st.header('Atualizar Banco de Dados')

st.write('Nesta página você pode verificar a última atualização dos dados e atualizá-los se necessário.')
st.write('''
         Os dados são obtidos através de consultas via API de diversas fontes, portanto, 
         pode não ser possível obter dados atualizados regularmente.
         ''')

st.subheader('Última atualização dos dados:', divider=True)
with st.spinner('Consultando a última atualização dos dados...'):
    lastDates = GetLastDates()

current_date = datetime.now().date()
cols = st.columns(4)
with cols[0]:
    st.write('SELIC:')
    st.write(lastDates['selic'].strftime('%B de %Y'))
    if current_date.month-1 > lastDates['selic'].month:
        st.warning(f'Os dados de SELIC podem estar desatualizados.')
    else:
        st.success('Os dados de SELIC estão atualizados.')
with cols[1]:
    st.write('Dólar:')
    st.write(lastDates['dolar'].strftime('%B de %Y'))
    if current_date.month-1 > lastDates['dolar'].month:
        st.warning(f'Os dados de Dólar podem estar desatualizados.')
    else:
        st.success('Os dados de Dólar estão atualizados.')
with cols[2]:
    st.write('IPCA:')
    st.write(lastDates['ipca'].strftime('%B de %Y'))
    if current_date.month-1 > lastDates['ipca'].month:
        st.warning(f'Os dados de IPCA podem estar desatualizados.')
    else:
        st.success('Os dados de IPCA estão atualizados.')
with cols[3]:
    st.write('Ações:')
    st.write(lastDates['stock'].strftime('%B de %Y'))
    if current_date.month-1 > lastDates['stock'].month:
        st.warning(f'Os dados de Ações podem estar desatualizados.')
    else:
        st.success('Os dados de Ações estão atualizados.')

#---------------------------------------------

st.subheader('Atualizar os dados:', divider=True)
st.write('Clique no botão abaixo para atualizar os dados')

#st.write(req.get(f'{st.session_state["config"]["API_URL_LOCAL"]}/bcb/selic', 
#                        params={'start_date': lastDates['selic']}).json())

#st.write(req.get("https://api.bcb.gov.br/dados/serie/bcdata.sgs.3695/dados?formato=json").json())

if st.button('Atualizar Dados'):
    progress_bar = st.progress(0, text='Atualizando os dados...')
    with st.spinner('Testando a conexão com a API...'):
        try:
            st.write(req.get('https://api.bcb.gov.br/dados/serie/').json())
            api_disponivel = True
            progress_bar.progress(1)
        except:
            api_disponivel = False
            st.error('Não foi possível conectar com a API do BCB. Tente novamente mais tarde.')
            st.stop()
    with st.spinner('Coletando os dados de SELIC...'):
        df_selic = um.GetIndicatorsLastValues('selic', lastDates['selic'])
        progress_bar.progress(10)

    with st.spinner('Coletando os dados de Dólar...'):
        df_dolar = um.GetIndicatorsLastValues('dollar', lastDates['dolar'])
        progress_bar.progress(20)

    with st.spinner('Coletando os dados de IPCA...'):
        df_ipca = um.GetIndicatorsLastValues('ipca', lastDates['ipca'])
        progress_bar.progress(30)

    st.stop()

    with st.spinner('Listando os tickers de ações...'):
        tickers = eval(req.get(f'{st.session_state["config"]["API_URL"]}/mongodb/tickers').json())
        progress_bar.progress(40)
    with st.spinner('Coletando os dados de ações...'):
        df_stocks = pd.DataFrame()
        for i, ticker in enumerate(tickers):
            df_stocks = pd.concat(df_stocks, um.GetStockLastPrices(ticker, lastDates['stock']))
            progress_bar.progress(40 + i/len(tickers)*40)
            progress_bar.text(f'Coletando dados de {ticker}...')
        progress_bar.progress(80)
    with st.spinner('Adicionando os dados de indicadores ao banco de dados...'):
        cols = st.columns(3)
        with cols[0]:
            st.dataframe(df_selic,use_container_width=True)
        with cols[1]:
            st.dataframe(df_dolar,use_container_width=True)
        with cols[2]:
            st.dataframe(df_ipca,use_container_width=True)
        progress_bar.progress(90)
    with st.spinner('Adicionando os dados de ações ao banco de dados...'):
        st.dataframe(df_stocks,use_container_width=True)
        progress_bar.progress(100)
    

st.subheader('Adicionar novos tickers de ações:', divider=True)
st.write('Digite o ticker da ação que deseja adicionar e clique no botão abaixo para adicionar ao banco de dados.')
ticker = st.text_input('Ticker da ação:')
if st.button('Adicionar Ticker'):
    with st.spinner('Adicionando o ticker ao banco de dados...'):
        #req.post(f'{st.session_state["config"]["API_URL_LOCAL"]}/mongodb/tickers', params={'ticker': ticker})
        st.success(f'O ticker {ticker} foi adicionado com sucesso ao banco de dados.')