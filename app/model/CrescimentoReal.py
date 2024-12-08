import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests as req
from services import ColorMethods as cm, IndicatorsMethods as im, StockMethods as sm, PlotlyMethods as pm, GeminiMethods as gm
from io import StringIO

st.title('Crescimento Real')

# Descrição
st.subheader('Inicialização', divider=True)

@st.cache_data
def load_data():
    with st.expander('', expanded=True):
        api_url = st.session_state['config']['API_URL']
        with st.spinner('Inicializando API'):
            if req.get(f'{api_url}/mongodb').json()['status'] == "Successfully connected to MongoDB!":
                st.success('API inicializada com sucesso!')
            else:
                st.error('Erro ao inicializar a API!')
            loading_bar = st.progress(0)
            loading_bar.progress(10)
        with st.spinner('Carregando valores das ações...'):
            df_acoes_valores = pd.read_json(StringIO(req.get(f'{api_url}/mongodb/Stocks/Prices').json()))
            loading_bar.progress(40)
        with st.spinner('Carregando informações das ações...'):
            df_acoes_infos = pd.read_json(StringIO(req.get(f'{api_url}/mongodb/Stocks/Info').json()))
            loading_bar.progress(60)
        with st.spinner('Carregando dados do Dollar...'):
            df_dolar = pd.read_json(StringIO(req.get(f'{api_url}/mongodb/Indicators/Dollar').json()))
            loading_bar.progress(70)
        with st.spinner('Carregando dados do IPCA...'):
            df_ipca = pd.read_json(StringIO(req.get(f'{api_url}/mongodb/Indicators/IPCA').json()))
            loading_bar.progress(80)
        with st.spinner('Carregando dados da Selic...'):
            df_selic = pd.read_json(StringIO(req.get(f'{api_url}/mongodb/Indicators/SELIC').json()))
            loading_bar.progress(90)
        with st.spinner('Finalizando carregamento...'):

            df_acoes_valores['price'] = df_acoes_valores['price'].map(sm.replace_nested_nan)
            df_acoes_valores.sort_values(by=['ticker','year-month'], inplace=True, ignore_index=True)
            #st.dataframe(df_acoes_valores,use_container_width=True)
            df_acoes_valores = sm.GetStockValorization(df_acoes_valores)

            df_dolar = im.GetDollarVariationData(df_dolar)
            df_ipca = im.GetIpcaAccumulatedData(df_ipca)
            df_selic = im.GetSelicAccumulatedData(df_selic)

            df_acoes_infos = df_acoes_infos.merge(sm.GetStockMonthsAboveDolar(df_acoes_valores, df_dolar), on='ticker', how='left')
            df_acoes_valores = df_acoes_valores.merge(sm.GetStockMonthAboveDolar(df_acoes_valores, df_dolar), on=['ticker','year-month'], how='left')

            df_acoes_infos = df_acoes_infos.merge(sm.GetStockCurrentValorization(df_acoes_valores), on='ticker', how='left')
            df_acoes_infos = df_acoes_infos.merge(sm.IsBDR(df_acoes_infos), on='ticker', how='left')

            loading_bar.progress(100)

        st.success('Dados carregados com sucesso!')
    return df_ipca, df_dolar, df_selic, df_acoes_valores, df_acoes_infos

#@st.cache_data
def filter_data():
    df_filtered = df_acoes_infos.copy()
    if esconder_acoes_sem_dados:
        df_filtered = df_filtered[df_filtered['financialCurrency'].notnull()]
    if 'BDR' not in tipo_de_acao:
        df_filtered = df_filtered[df_filtered['BDR'] == False]
    if 'Regular' not in tipo_de_acao:
        df_filtered = df_filtered[df_filtered['BDR'] == True]
    if len(estado) > 0:
        df_filtered = df_filtered[df_filtered['state'].isin(estado)]
    if len(pais) > 0:
        df_filtered = df_filtered[df_filtered['country'].isin(pais)]
    if len(industria) > 0:
        df_filtered = df_filtered[df_filtered['industry'].isin(industria)]
    if len(setor) > 0:
        df_filtered = df_filtered[df_filtered['sector'].isin(setor)]
    
    df_filtered = df_filtered[(df_filtered['currentValorization'] >= valorizacao_min) & (df_filtered['currentValorization'] <= valorizacao_max)]
    df_filtered = df_filtered[(df_filtered['months_above_dolar'] >= intervalo_meses_acima_dolar[0]) & (df_filtered['months_above_dolar'] <= intervalo_meses_acima_dolar[1])]
    return df_filtered
    

df_ipca, df_dolar, df_selic, df_acoes_valores, df_acoes_infos = load_data()

st.dataframe(df_selic, use_container_width=True)

df_acoes_infos_filtrado = df_acoes_infos.copy()

#Filtros de ações
cidades = df_acoes_infos['city'].unique()
estados = df_acoes_infos['state'].unique()
paises = df_acoes_infos['country'].unique()
industrias = df_acoes_infos['industry'].unique()
setores = df_acoes_infos['sector'].unique()
meses = df_acoes_valores['year-month'].nunique()

#------------------------------------------------------------
st.subheader('Índices', divider=True)

cols = st.columns([0.8,0.2])

with cols[0]:
    fig = pm.plot_indicators(df_ipca, df_dolar, df_selic)
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    st.write('''Ao lado pode-se ver a valorização do dólar em relação ao real desde janeiro de 2020, a inflação acumulada e a taxa Selic acumulada.''')
    st.write('''Os dados de inflação e taxa Selic foram acumulados para facilitar a comparação com a valorização do dólar.''')
    st.metric('Valor do dólar em janeiro de 2020', f'R${4.2689:.2f}')
    st.metric(f'Valor do dólar em {(df_dolar["year-month"].iloc[-1])}',f'R${(df_dolar["price"].iloc[-1]):.2f}' ,f'{df_dolar["valorization"].iloc[-1]:.2f}%')

#------------------------------------------------------------
st.subheader('Ações', divider=True)
cols = st.columns([0.2,0.8])
with cols[0]:
    st.write('Filtros')
    esconder_acoes_sem_dados = st.checkbox('Esconder ações sem dados', value=True)
    tipo_de_acao = st.multiselect('Tipo de ação', ['BDR','Regular'], default=['BDR','Regular'])
    #cidade = st.multiselect('Cidade', cidades)
    estado = st.multiselect('Estado', estados, default=[])
    pais = st.multiselect('País', paises, default=[])
    industria = st.multiselect('Indústria', industrias, default=[])
    setor = st.multiselect('Setor', setores, default=[])
    #mes = st.select_slider('Mês', options=meses)

    #intervalo_valorizacao = st.slider('Valorização mínima', min_value=df_acoes_infos_filtrado['currentValorization'].min(), 
    #                            max_value=df_acoes_infos_filtrado['currentValorization'].max(), 
    #                            value=(df_acoes_infos_filtrado['currentValorization'].min(), df_acoes_infos_filtrado['currentValorization'].max()))
    
    #adicionar um % no número
    valorizacao_min = st.number_input('Valorização mínima', value=df_acoes_infos_filtrado['currentValorization'].min(), step=5.0, format='%.0f') 
    valorizacao_max = st.number_input('Valorização máxima', value=df_acoes_infos_filtrado['currentValorization'].max(), step=5.0, format='%.0f')

    intervalo_meses_acima_dolar = st.slider('Meses acima do dólar', min_value=int(df_acoes_infos_filtrado['months_above_dolar'].min()),
                                        max_value=int(df_acoes_infos_filtrado['months_above_dolar'].max()),
                                        value=(int(df_acoes_infos_filtrado['months_above_dolar'].min()), int(df_acoes_infos_filtrado['months_above_dolar'].max())))

    df_acoes_infos_filtrado = filter_data()

with cols[1]:
    fig = pm.plot_stock_scatterplot(df_acoes_infos_filtrado, df_dolar['valorization'].iloc[-1], meses)
    st.plotly_chart(fig, use_container_width=True)

#------------------------------------------------------------

st.subheader('Tabela de Ações', divider=True)
cols = st.columns([0.2,0.8])
with cols[0]:
    #Métrica de ações filtradas
    st.metric('Ações filtradas', f'{df_acoes_infos_filtrado.shape[0]}')
    st.metric('Valorização média', f'{df_acoes_infos_filtrado["currentValorization"].mean():.2f}%')
    st.metric('Meses acima do dólar médio', f'{df_acoes_infos_filtrado["months_above_dolar"].mean():.2f}')
    st.metric('Valorização mínima', f'{df_acoes_infos_filtrado["currentValorization"].min():.2f}%')
    st.metric('Valorização máxima', f'{df_acoes_infos_filtrado["currentValorization"].max():.2f}%')


with cols[1]:
    st.dataframe(df_acoes_infos_filtrado[['ticker','longName','country','industry','sector','currentValorization','months_above_dolar']].rename(
        columns={'longName':'Nome','country':'País','industry':'Indústria','sector':'Setor','currentValorization':'Valorização Atual',
                'months_above_dolar':'Meses Acima do Dólar'}), height=500, use_container_width=True)

#------------------------------------------------------------

st.subheader('Aprofundamento', divider=True)

st.write('Selecione até 5 ações para aprofundar a análise')

selecionadas = st.multiselect('Selecione ações para compará-las', df_acoes_infos_filtrado['ticker'].unique(), max_selections=5)

#Seleção de cor para cada ação selecionada
cols = st.columns(5)
cor_acoes = st.session_state.get('cor_acoes', {})
for c in range(5):
    with cols[c]:
        if (c < len(selecionadas)):
            if selecionadas[c] not in cor_acoes:
                color = st.color_picker(f'Escolha uma cor para a ação {selecionadas[c]}', key=f'color_picker_{c}', value=cm.gerar_cor_hex())
            else:
                color = st.color_picker(f'Escolha uma cor para a ação {selecionadas[c]}', key=f'color_picker_{c}', value=cor_acoes[selecionadas[c]])
            cor_acoes[selecionadas[c]] = color
    st.session_state['cor_acoes'] = cor_acoes

df_acoes_selecionadas = df_acoes_infos_filtrado[df_acoes_infos_filtrado['ticker'].isin(selecionadas)]
cols = st.columns(2)

with cols[0]:
    fig = pm.plot_stock_boxplot(df_acoes_valores[df_acoes_valores['ticker'].isin(selecionadas)], cor_acoes)
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    fig = pm.plot_stock_timeline(df_acoes_valores[df_acoes_valores['ticker'].isin(selecionadas)], cor_acoes)
    #if(st.checkbox('Mostrar valorização do dólar')):
    #   fig.add_trace(go.Scatter(x=df_dolar['year-month'], y=df_dolar['price'], mode='lines', name='Dólar', 
    #    line=dict(color='white', width=1, dash='dot'), line_shape='spline'))
    st.plotly_chart(fig, use_container_width=True)


with st.spinner('Traduzindo textos...'):
    #Exibir os detalhes de cada ação na sua cor correspondente
    for acao in selecionadas:
        with st.expander(f'Detalhes da ação {acao}', expanded=False):
            st.write(f'**{acao}**', unsafe_allow_html=True)
            
            longName = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["longName"].values[0]
            st.write(f'<span style="color:{cor_acoes[acao]}">Nome: {longName}</span>', unsafe_allow_html=True)

            country = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["country"].values[0]
            st.write(f'<span style="color:{cor_acoes[acao]}">País: {country}</span>', unsafe_allow_html=True)

            state = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["state"].values[0]
            st.write(f'<span style="color:{cor_acoes[acao]}">Estado: {state}</span>', unsafe_allow_html=True)

            try:
                industry = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["industry"].values[0]
            except:
                industry = 'Not available'
            try:
                sector = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["sector"].values[0]
            except:
                sector = 'Not available'
            try:
                longBusinessSummary = df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["longBusinessSummary"].values[0]
            except:
                longBusinessSummary = 'Not available'

            industry_pt, sector_pt, longBusinessSummary_pt = gm.TranslateStocksInfo(industry, sector, longBusinessSummary)

            st.write(f'<span style="color:{cor_acoes[acao]}">Indústria: {industry_pt}</span>', unsafe_allow_html=True)
            st.write(f'<span style="color:{cor_acoes[acao]}">Setor: {sector_pt}</span>', unsafe_allow_html=True)
            st.write(f'<span style="color:{cor_acoes[acao]}">Descrição: {longBusinessSummary_pt}</span>', unsafe_allow_html=True)

            st.write(f'<span style="color:{cor_acoes[acao]}">Website: {df_acoes_selecionadas[df_acoes_selecionadas["ticker"] == acao]["website"].values[0]}</span>', unsafe_allow_html=True)

#------------------------------------------------------------

st.subheader('Relatório',divider=True)

#st.write(st.session_state)



#st.markdown('R\$ 20,00 e vender em torno de R\$ 26,00')

if st.button('Gerar relatório'):
    with st.spinner('Gerando relatório...'):
        #Incluir função de buscar no google
        report, usage = gm.GenerateReport(selecionadas, df_acoes_selecionadas, df_acoes_valores, df_dolar, df_ipca, df_selic)
        st.markdown(report.replace('$','\$'))
        st.download_button('Baixar relatório', data=report, file_name='relatorio.txt', mime='text/plain')
        st.write(usage)



# pegar latitude e longitude de cada ação para plotar um mapa
#st.map(df_acoes_infos_filtrado[['latitude','longitude']])




#st.write('Ações')
#st.dataframe(df_acoes_infos)
#st.dataframe(df_acoes_valores)
#st.write('Dolar')
#st.dataframe(df_dolar)
#st.write('IPCA')
#st.dataframe(df_ipca)
#st.write('Selic')
#st.dataframe(df_selic)