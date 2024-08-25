import streamlit as st
import os
import pandas as pd

def display_data_summary_report():
    st.title('Data Summary Report')

    st.table(pd.DataFrame({
        'Dados': ['Ações', 'Inflação', 'Dólar', 'Selic'], 
        'Fonte': ['Yahoo Finance', 'Banco Central', 'Banco Central','Banco Central'], 
        'Descrição': ['Dados históricos de ações da bolsa brasileira', 
                    'Índice de Preços ao Consumidor Amplo (IPCA)', 
                    'Cotação do dólar em relação ao real',
                    'Taxa Selic mensal'] })) 
    #df = pd.DataFrame({'Inflação': [os.getenv('IPEA_API')], 'Dólar': [os.getenv('BANCO_CENTRAL_API')] })
display_data_summary_report()
