import streamlit as st
import requests as req
from datetime import datetime
import pandas as pd
from services import UpdateMethods as um
import json

st.header('Atualizar Banco de Dados')

st.write('Nesta página você pode verificar a última atualização dos dados e atualizá-los se necessário.')
st.write('''
         Os dados são obtidos através de consultas via API de diversas fontes, portanto, 
         pode não ser possível obter dados atualizados regularmente.
         ''')

st.subheader('Última atualização dos dados:', divider=True)
with st.spinner('Consultando a última atualização dos dados...'):
    lastDates = um.GetLastDates()

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
cols = st.columns(2)
with cols[0]:
    st.spinner('Checando a conexão com a API...')
    bcb_status = um.BCBStatus()
    if not bcb_status:
        st.error(f'Não foi possível conectar com a API do BCB. Tente novamente mais tarde. Status code: {bcb_status}')
    else:
        st.success('API do BCB está disponível.')

with cols[1]:
    st.spinner('Checando a conexão com a API...')
    yfs_status = um.YFinanceStatus()
    if not yfs_status:
        st.error('Não foi possível conectar com a API do Yahoo Finance. Tente novamente mais tarde.')
    else:
        st.success('API do Yahoo Finance está disponível.')

#df_teste = pd.DataFrame(req.get(f'{st.session_state["config"]["API_URL"]}/yfinance/stock-monthly-price', 
#                            params={'ticker': 'WEGE3.SA', 'start': lastDates['stock']}).json()['data'])

#df_teste = um.GetStockLastPrices('WEGE3.SA', lastDates['stock'])

#st.dataframe(df_teste[df_teste['year-month'] != lastDates['stock'].strftime('%Y-%m')])
#st.write(df_teste.to_dict('records'))

#df_dolar = um.GetIndicatorsLastValues('selic', lastDates['selic'])
#st.dataframe(df_dolar)

if st.button('Atualizar Dados'):
    progress_bar = st.progress(0.0, text='Atualizando os dados...')
    if bcb_status:
        with st.spinner('Coletando os dados de SELIC...'):
            df_selic = um.GetIndicatorsLastValues('selic', lastDates['selic'])
            df_selic = df_selic[df_selic['year-month'] != lastDates['selic'].strftime('%Y-%m')]
            progress_bar.progress(0.1)

        with st.spinner('Coletando os dados de Dólar...'):
            df_dolar = um.GetIndicatorsLastValues('dollar', lastDates['dolar'])
            df_dolar = df_dolar[df_dolar['year-month'] != lastDates['dolar'].strftime('%Y-%m')]
            progress_bar.progress(0.2)

        with st.spinner('Coletando os dados de IPCA...'):
            df_ipca = um.GetIndicatorsLastValues('ipca', lastDates['ipca'])
            df_ipca = df_ipca[df_ipca['year-month'] != lastDates['ipca'].strftime('%Y-%m')]
            progress_bar.progress(0.3)
    else:
        st.warning('API do BCB não disponível. Não foi possível coletar os dados de SELIC, Dólar e IPCA.')
        progress_bar.progress(0.3)

    if yfs_status:
        with st.spinner('Listando os tickers de ações...'):
            tickers = um.GetStocksTickers()
            progress_bar.progress(0.4)
        with st.spinner('Coletando os dados de ações...'):
            stocks = []
            stocks_not_found = []
            for i, ticker in enumerate(tickers):
                progress_bar.progress(0.4 + (i/len(tickers))*0.4, text=f'Coletando dados de {ticker} - {i+1}/{len(tickers)}...')
                try:
                    df_stock = um.GetStockLastPrices(ticker, lastDates['stock'])
                    df_stock = df_stock[df_stock['year-month'] != lastDates['stock'].strftime('%Y-%m')]
                    if not (df_stock.empty):
                        stocks.append(df_stock.to_dict('records'))
                        st.write(stocks)
                except:
                    stocks_not_found.append(ticker)
            progress_bar.progress(0.8)


        with st.spinner('Adicionando os dados de indicadores ao banco de dados...'):
            st.write('**Dados de SELIC, Dólar e IPCA:**')
            cols = st.columns(3)
            with cols[0]:
                #Checar se o dataframe tá vazio
                if not df_selic.empty:
                    df_selic.rename(columns={'price':'value'}, inplace=True)
                    result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Indicators/SELIC/',
                            params={'data': json.dumps(df_selic.to_dict('records'))}).json())
                    if result['status'] != 'Data inserted successfully!':
                        st.error(f'Status: {result["status"]}')
                        st.error(f'Error: {result["error"]}')
                        st.stop()
                else:
                    st.warning('Não há novos dados de SELIC para serem adicionados.')
                st.dataframe(df_selic,use_container_width=True)

            with cols[1]:
                if not df_dolar.empty:
                    result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Indicators/Dollar/',
                            params={'data': json.dumps(df_dolar.to_dict('records'))}).json())
                    if result['status'] != 'Data inserted successfully!':
                        st.error(f'Status: {result["status"]}')
                        st.error(f'Error: {result["error"]}')
                        st.stop()
                else:
                    st.warning('Não há novos dados de Dólar para serem adicionados.')
                st.dataframe(df_dolar,use_container_width=True)

            with cols[2]:
                if not df_ipca.empty:
                    df_ipca.rename(columns={'price':'value'}, inplace=True)
                    result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Indicators/IPCA/',
                            params={'data': json.dumps(df_ipca.to_dict('records'))}).json())
                    if result['status'] != 'Data inserted successfully!':
                        st.error(f'Status: {result["status"]}')
                        st.error(f'Error: {result["error"]}')
                        st.stop()
                else:
                    st.warning('Não há novos dados de IPCA para serem adicionados.')
                st.dataframe(df_ipca,use_container_width=True)

            progress_bar.progress(0.9, text='Atualizando os dados...')

        with st.spinner('Adicionando os dados de ações ao banco de dados...'):
            st.write('**Dados de Ações:**')
            st.expander('Tickers não encontrados:', expanded=True).write(stocks_not_found)
            #st.write(stocks)
            #st.write(json.dumps(df_stocks.to_dict('records')))
            #Mandar todo o dataframe estava dando erro de json encoder, mandar um de cada vez foi a solução
            if stocks != []:
                for p, stock in enumerate(stocks):
                    progress_bar.progress(0.9 + (p/len(stocks))*0.1, text=f'Adicionando dados de ações - {p+1}/{len(stocks)}...')
                    df_stocks = pd.DataFrame(stock)
                    result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Stocks/Prices/', 
                        params={'data' : json.dumps(df_stocks.to_dict('records'))}).json())

                
                if result['status'] != 'Data inserted successfully!':
                    st.error(f'Status: {result["status"]}')
                    st.error(f'Error: {result["error"]}')
                    st.stop()
            else:
                st.warning('Não há novos dados de Ações para serem adicionados.')

            
            lastDates = um.GetLastDates()

            progress_bar.progress(1.0)
            st.success('Os dados foram atualizados com sucesso!')
            st.download_button('Baixar tickers não encontrados', json.dumps(stocks_not_found), 'tickers_not_found.json')
    else:
        st.warning('API do Yahoo Finance não disponível. Não foi possível coletar os dados de ações.')
        progress_bar.progress(1.0)
    
#---------------------------------------------

st.subheader('Adicionar novos tickers de ações:', divider=True)
st.write('Digite o ticker da ação que deseja adicionar e clique no botão abaixo para adicionar ao banco de dados.')
ticker = st.text_input('Ticker da ação:')

if st.button('Adicionar Ticker'):
    with st.spinner('Adicionando o ticker ao banco de dados...'):
        container = st.container()
        container.write(f'1. Verificando se o ticker {ticker} já existe no banco de dados...')
        response = req.get(f'{st.session_state["config"]["API_URL"]}/mongodb/Stocks/Info/check', 
                           params={'filter': json.dumps({'ticker': ticker})}).json()
        if response:
            container.warning(f'O ticker {ticker} já existe no banco de dados.')
            st.stop()

        container.write(f'2. Buscando informações sobre o ticker {ticker}...')
        try:
            info = req.get(f'{st.session_state["config"]["API_URL"]}/yfinance/stock-info', 
                                params={'ticker': ticker}).json()
            df_info = pd.DataFrame([info])
            container.dataframe(df_info,use_container_width=True)
        except:
            st.error(f'Não foi possível encontrar informações sobre o ticker {ticker}.')
            st.stop()

        container.write(f'3. Buscando valorização do ticker {ticker}...')
        try:
            price = req.get(f'{st.session_state["config"]["API_URL"]}/yfinance/stock-monthly-price', 
                                params={'ticker': ticker, 'start':'2020-01-01'}).json()
            df_price = pd.DataFrame(price['data'])
            df_price = df_price[df_price['year-month'] != lastDates['stock'].strftime('%Y-%m')]
            container.dataframe(df_price,use_container_width=True)
        except:
            st.error(f'Não foi possível encontrar informações sobre a valorização do ticker {ticker}.')
            st.stop()
            
            import json
        container.write(f'4. Adicionando o ticker {ticker} ao banco de dados...')
        result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Stocks/Info/',
                    params={'data' : json.dumps(df_info.to_dict('records'))}).json())
        
        #st.write(result)
        if result['status'] != 'Data inserted successfully!':
            container.error(f'Status: {result["status"]}')
            container.error(f'Error: {result["error"]}')
            st.stop()
            
        result = eval(req.post(f'{st.session_state["config"]["API_URL"]}/mongodb/Stocks/Prices/',
                    params={'data' : json.dumps(df_price.to_dict('records'))}).json())
        if result['status'] != 'Data inserted successfully!':
            container.error(f'Status: {result["status"]}')
            container.error(f'Error: {result["error"]}')
            st.stop()
        
        container.success(f'O ticker {ticker} foi adicionado com sucesso ao banco de dados.')
        #st.write(response.json())
        #st.success(f'O ticker {ticker} foi adicionado com sucesso ao banco de dados.')