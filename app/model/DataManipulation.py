import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go


@st.cache_data
def load_data():
    df_ipca = pd.read_csv('data/ipca.csv')
    df_dolar = pd.read_csv('data/dolar.csv')
    df_selic = pd.read_csv('data/selic.csv')
    df_acoes = pd.read_csv('data/media_mensal_acoes.csv')
    return df_ipca, df_dolar, df_selic, df_acoes

df_ipca, df_dolar, df_selic, df_acoes = load_data()

#Transformação dos dados
#df_dolar['valor'] = df_dolar['valor'].apply(lambda x: x/df_dolar['valor'].iloc[0])#Valorização do dólar desde 2019

df_selic['data'] = df_selic['mes_ano'].apply(lambda x: x + '-01')
df_selic['valor'] = df_selic['valor'].apply(lambda x: x/12) # Transforma a taxa anual em mensal
df_selic = df_selic.drop(columns=['mes_ano'])

df_acoes['data'] = df_acoes['Month'].apply(lambda x: x + '-01')
df_acoes = df_acoes.drop(columns=['Month'])
df_acoes = pd.melt(df_acoes, id_vars='data', var_name='Ações', value_name='Valor')
df_acoes.dropna(inplace=True)
#df_acoes['valorização'] = df_acoes['Valor']/df_acoes['Valor'].iloc[0]-1

dataframes = {'IPCA': df_ipca, 'Dólar': df_dolar, 'Selic': df_selic, 'Ações': df_acoes}

# Título
st.title('Visualização e Manipulação de Dados')

# Descrição
st.subheader('Dados disponíveis', divider=True)

cols = st.columns(4)

with cols[0]:
    st.write('**IPCA**')
    st.write(f'{df_ipca['data'].min()} a 'f'{df_ipca['data'].max()}')

with cols[1]:
    st.write('**Dólar**')
    st.write(f'{df_dolar['data'].min()} a 'f'{df_dolar['data'].max()}')

with cols[2]:
    st.write('**Selic**')
    st.write(f'{df_selic['data'].min()} a 'f'{df_selic['data'].max()}')

with cols[3]:
    st.write('**Ações**')
    st.write(f'{df_acoes['data'].min()} a 'f'{df_acoes['data'].max()}')

for key, df in dataframes.items():
    df['data'] = pd.to_datetime(df['data'])

st.subheader('Adicionar novos dados', divider=True)

with st.expander('Clique aqui para adicionar novos dados'):
    cols = st.columns(3)

    with cols[0]:
        tipo_dado = st.radio('Selecione o tipo de dado', ['IPCA', 'Dólar', 'Selic', 'Ações'])

    with cols[1]:
        tipo_upload = st.radio('Tipo de upload', ['Complementar', 'Substituir'])

    with cols[2]:
        uploaded_file = st.file_uploader('Selecione o arquivo CSV')
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            if df:
                try :
                    dataframes[tipo_dado] = df
                    if tipo_upload == 'Complementar':
                        dataframes[tipo_dado] = pd.concat([dataframes[tipo_dado], df], ignore_index=True)
                    elif tipo_upload == 'Substituir':
                        dataframes[tipo_dado] = df
                    st.success('Dados carregados com sucesso!', icon="✅")
                except:
                    st.error('Erro ao carregar os dados. Verifique o formato do arquivo.', icon="🚨")


st.subheader('Visualização dos dados', divider=True)

start_date = pd.to_datetime(st.date_input('Data Inicial', df_acoes['data'].min()))
end_date = pd.to_datetime(st.date_input('Data Final',  df_acoes['data'].max()))

dataframes['IPCA'] = dataframes['IPCA'][(dataframes['IPCA']['data'] >= start_date) & (dataframes['IPCA']['data'] <= end_date)]
dataframes['Dólar'] = dataframes['Dólar'][(dataframes['Dólar']['data'] >= start_date) & (dataframes['Dólar']['data'] <= end_date)]
dataframes['Selic'] = dataframes['Selic'][(dataframes['Selic']['data'] >= start_date) & (dataframes['Selic']['data'] <= end_date)]
dataframes['Ações'] = dataframes['Ações'][(dataframes['Ações']['data'] >= start_date) & (dataframes['Ações']['data'] <= end_date)]

fig = go.Figure()

fig.add_trace(go.Scatter(x=dataframes['IPCA'].data, y=dataframes['IPCA']['valor'], mode='lines', name='IPCA'))
fig.add_trace(go.Scatter(x=dataframes['Dólar'].data, y=dataframes['Dólar']['valor'], mode='lines', name='Dólar'))
fig.add_trace(go.Scatter(x=dataframes['Selic'].data, y=dataframes['Selic']['valor'], mode='lines', name='Selic'))

fig.update_layout(title='Indicadores Econômicos',
                  xaxis_title='Data',
                  yaxis_title='Valor',
                  legend_title='Indicadores')

st.plotly_chart(fig, use_container_width=True)

#Pegar primeira data, ultima data, preço inicial, preço final, valorização
datas_inicial_final = dataframes['Ações'].groupby('Ações').agg({'data': ['min', 'max']})
#datas_inicial_final.columns = datas_inicial_final.columns.droplevel()

for acao in datas_inicial_final.index:
    df = dataframes['Ações'] [dataframes['Ações'] ['Ações'] == acao]
    datas_inicial_final.loc[acao, 'Preço Inicial'] = df[df['data'] == datas_inicial_final.loc[acao, ('data', 'min')]]['Valor'].values[0]
    datas_inicial_final.loc[acao, 'Preço Final'] = df[df['data'] == datas_inicial_final.loc[acao, ('data', 'max')]]['Valor'].values[0]

datas_inicial_final['Valorização'] = datas_inicial_final['Preço Final']/datas_inicial_final['Preço Inicial']-1
datas_inicial_final.columns = datas_inicial_final.columns.droplevel()
datas_inicial_final.columns = ['Data Inicial', 'Data Final', 'Preço Inicial', 'Preço Final', 'Valorização']

#datas_inicial_final['Valorização'] = datas_inicial_final['Valorização'].apply(lambda x: f'{x * 100:.2f}%')

acoes_ranqueadas = datas_inicial_final.sort_values('Valorização', ascending=False).head(25)

st.write('**Ações Ranqueadas**')
st.dataframe(acoes_ranqueadas, use_container_width=True)





#boxplot ações
st.subheader('Boxplot de Ações', divider=True)

acoes = dataframes['Ações']['Ações'].unique()
acoes_selecionadas = st.multiselect('Selecione as ações', acoes)

cols = st.columns(2)
with cols[0]:
    fig = go.Figure()
    for acao in acoes_selecionadas:
        df = dataframes['Ações'][dataframes['Ações']['Ações'] == acao]
        fig.add_trace(go.Box(y=df['Valor'], name=acao))

    fig.update_layout(title='Boxplot de Ações',
                        yaxis_title='Valor',
                        legend_title='Ações')
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    fig = go.Figure()
    for acao in acoes_selecionadas:
        df = dataframes['Ações'][dataframes['Ações']['Ações'] == acao]
        fig.add_trace(go.Scatter(x=df['data'], y=df['Valor'], mode='lines', name=acao))
    
    fig.update_layout(title='Valor das Ações',
                        xaxis_title='Data',
                        yaxis_title='Valor',
                        legend_title='Ações')
                    
    st.plotly_chart(fig, use_container_width=True)



st.subheader('Donwloads', divider=True)

cols = st.columns(4)
with cols[0]:
    st.markdown('**IPCA**')
    st.download_button('Clique aqui para baixar os dados de IPCA', dataframes['IPCA'].to_csv(), 'ipca.csv', 'text/csv')

with cols[1]:
    st.markdown('**Dólar**')
    st.download_button('Clique aqui para baixar os dados de Dólar', dataframes['Dólar'].to_csv(), 'dolar.csv', 'text/csv')

with cols[2]:
    st.markdown('**Selic**')
    st.download_button('Clique aqui para baixar os dados de Selic', dataframes['Selic'].to_csv(), 'selic.csv', 'text/csv')

with cols[3]:
    st.markdown('**Ações**')
    st.download_button('Clique aqui para baixar os dados de Ações', dataframes['Ações'].to_csv(), 'acoes.csv', 'text/csv')

