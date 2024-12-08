import streamlit as st
import pandas as pd

# Título
st.title('Crescimento Real :moneybag:')


# Descrição
st.subheader('Descrição', divider=True)

columns = st.columns([0.8, 0.2])

with columns[0]:
    st.markdown('''
        Este projeto tem como objetivo desenvolver um dashboard interativo que permita analisar o desempenho de ações da bolsa brasileira em relação à inflação, ao dólar e a Selic.
        Os dados serão coletados de fontes públicas como Yahoo Finance, IPEA e Banco Central, e a análise será realizada com base em indicadores econômicos e financeiros.
        O dashboard será desenvolvido utilizando a biblioteca Streamlit e terá funcionalidades para visualização de dados, comparação de ativos e análise de tendências.
    ''')

with columns[1]:
    st.image('https://midias.correiobraziliense.com.br/_midias/png/2020/08/07/viralata-5075146.png', width=300)

# Links úteis
st.subheader('Links Úteis', divider=True)
st.markdown('''
**Links Úteis:**
- [Banco Central SGS](https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Kaggle Dataset](https://www.kaggle.com/datasets/felsal/ibovespa-stocks/data)
- [Banco Central Série História](https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/)
- [Biblioteca yfinance](https://github.com/ranaroussi/yfinance)
- [Biblioteca bovespa2csv](https://github.com/felipessalvatore/bovespa2csv)
- API do Banco Central: https://api.bcb.gov.br/dados/serie/bcdata.sgs.xxxx/dados?formato=json
''')

#Amostra dos Dados
st.subheader('Data Summary Report',divider=True)

st.table(pd.DataFrame({
    'Dados': ['Ações', 'Inflação', 'Dólar', 'Selic'], 
    'Fonte': ['Yahoo Finance', 'Banco Central', 'Banco Central','Banco Central'], 
    'Descrição': ['Dados históricos de ações da bolsa brasileira', 
                'Índice de Preços ao Consumidor Amplo (IPCA)', 
                'Cotação do dólar em relação ao real',
                'Taxa Selic mensal'] })) 
