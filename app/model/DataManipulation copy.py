import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go



@st.cache_data
def load_data():
    df_ipca = pd.read_csv('data/ipca_acumulado.csv')
    #df_ipca_referencia = pd.read_csv('data/ipca_valor_referencia.csv')

    #df_dolar = pd.read_csv('data/dolar_valores.csv')
    df_dolar = pd.read_csv('data/dolar_valorizacao.csv')
    #df_dolar_referencia = pd.read_csv('data/dolar_valor_referencia.csv')

    df_selic = pd.read_csv('data/selic_acumulada.csv')
    #df_selic_referencia = pd.read_csv('data/selic_valor_referencia.csv')

    df_acoes = pd.read_csv('data/acoes_valorizacao.csv')
    df_acoes_referencia = pd.read_csv('data/acoes_valor_referencia.csv')
    df_acoes_valores = pd.read_csv('data/acoes_valores.csv')

    return df_ipca, df_dolar, df_selic, df_acoes, df_acoes_referencia, df_acoes_valores

df_ipca, df_dolar, df_selic, df_acoes, df_acoes_referencia, df_acoes_valores = load_data()

total_meses = df_acoes['Ano-Mes'].nunique()

#Transformação dos dados
#df_dolar['valor'] = df_dolar['valor'].apply(lambda x: x/df_dolar['valor'].iloc[0])#Valorização do dólar desde 2019

#df_selic['data'] = df_selic['mes_ano'].apply(lambda x: x + '-01')
#df_selic['valor'] = df_selic['valor'].apply(lambda x: x/12) # Transforma a taxa anual em mensal
#df_selic = df_selic.drop(columns=['mes_ano'])

#df_acoes['data'] = df_acoes['Month'].apply(lambda x: x + '-01')
#df_acoes = df_acoes.drop(columns=['Month'])
df_acoes = pd.melt(df_acoes, id_vars='Ano-Mes', var_name='Ações', value_name='Valorização')
df_acoes_valores = pd.melt(df_acoes_valores, id_vars='Ano-Mes', var_name='Ações', value_name='Valor')
#df_acoes.dropna(inplace=True)
#df_acoes['valorização'] = df_acoes['Valor']/df_acoes['Valor'].iloc[0]-1

#dataframes = {'IPCA': df_ipca, 'Dólar': df_dolar, 'Selic': df_selic, 'Ações': df_acoes}

# Título
st.title('Visualização e Manipulação de Dados')

# Descrição
st.subheader('Índices', divider=True)

# Gráficos
#Plotar a valorização dos três indices
cols = st.columns([0.8,0.2])
with cols[0]:
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_ipca['Ano-Mes'], y=df_ipca['valor'], mode='lines', name='IPCA'))
    fig.add_trace(go.Scatter(x=df_dolar['Ano-Mes'], y=df_dolar['valor']*100, mode='lines', name='Dólar'))
    fig.add_trace(go.Scatter(x=df_selic['Ano-Mes'], y=df_selic['valor'], mode='lines', name='Selic'))

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with cols[1]:
    st.write('''Ao lado pode-se ver a valorização do dólar em relação ao real desde janeiro de 2020, a inflação acumulada e a taxa Selic acumulada.''')
    st.write('''Os dados de inflação e taxa Selic foram acumulados para facilitar a comparação com a valorização do dólar.''')
    st.metric('Valor do dólar em janeiro de 2020', f'R${4.2689:.2f}')
    st.metric(f'Valor do dólar em {(df_dolar["Ano-Mes"].iloc[-1])}',f'R${(df_dolar["valor"].iloc[-1]+1)*4.2689:.2f}' ,f'{df_dolar["valor"].iloc[-1]*100:.2f}%')


st.subheader('Ações', divider=True)

df_acoes.fillna(0, inplace=True)



min_valorizacao, max_valorizacao = st.select_slider('Selecione o intervalo de valorização', 
    options=df_acoes.sort_values('Valorização', ascending=True)['Valorização'].unique(), value=(df_acoes['Valorização'].min(), df_acoes['Valorização'].max()))

df_acoes_filtradas = df_acoes[df_acoes['Ano-Mes'] == df_acoes['Ano-Mes'].max()]
df_acoes_filtradas = df_acoes_filtradas[(df_acoes_filtradas['Valorização'] >= min_valorizacao) & (df_acoes_filtradas['Valorização'] <= max_valorizacao)]

#acoes_validas = df_acoes[([df_acoes['Ano-Mes'] == df_acoes['Ano-Mes'].max()]) & (df_acoes['Valorização'] >= min_valorizacao) & (df_acoes['Valorização'] <= max_valorizacao)]['Ações'].unique()
st.write(f'Foram encontradas {df_acoes_filtradas.shape[0]} ações com valorização entre {min_valorizacao:.2f} e {max_valorizacao:.2f}.')
st.write('**Valorização atual**')
cols = st.columns([0.2,0.8])
with cols[0]:
    #st.write('**Boxplot das ações filtradas**')
    fig = go.Figure()
    fig.add_trace(go.Box(y=df_acoes_filtradas['Valorização'], name='Valorização'))
    fig.update_layout(title='Boxplot de Ações',
                        yaxis_title='Valorização',
                        legend_title='Ações')
    st.plotly_chart(fig, use_container_width=True)

with cols[1]:
    #st.write('**Meses acima do dólar por valorização atual**')

    fig = go.Figure()
    acoes_ranqueadas = df_acoes_filtradas.sort_values('Valorização', ascending=False)#.head(25)
    acoes_ranqueadas['Valor Inicial'] = df_acoes_referencia[acoes_ranqueadas['Ações']].iloc[0].values
    acoes_ranqueadas['Valor Atual'] = acoes_ranqueadas['Valor Inicial'] * (1 + acoes_ranqueadas['Valorização'])
    acoes_ranqueadas.reset_index(drop=True, inplace=True)

    acoes_ranqueadas['MesesAcimaDolar'] = 0

    for i in acoes_ranqueadas.index:
        acao = acoes_ranqueadas.loc[i, 'Ações']
        meses_acima = df_acoes[(df_acoes['Ações'] == acao) & (df_acoes['Valorização'] > df_dolar['valor'].iloc[0])].shape[0]
        acoes_ranqueadas.loc[i, 'MesesAcimaDolar'] = meses_acima
        
    for acao in acoes_ranqueadas['Ações']:
        df = acoes_ranqueadas[acoes_ranqueadas['Ações'] == acao]
        df['Valorização'] = df['Valorização'].apply(lambda x: f'{x:.0%}')
        fig.add_trace(go.Scatter(x=df['MesesAcimaDolar'], y=df['Valorização'], mode='markers', name=acao))
        
    #plotar linha da valorização atual do dólar
    fig.add_trace(go.Scatter(x=[0, total_meses], y=[df_dolar["valor"].iloc[-1]*100,df_dolar["valor"].iloc[-1]*100], mode='lines', name='Dólar', line=dict(color='white', width=1, dash='dot')))
    #plotar linha vertical no meio do gráfico
    fig.add_shape(type='line', x0=total_meses/2, x1=total_meses/2, y0=-acoes_ranqueadas['Valorização'].max()*100, y1=acoes_ranqueadas['Valorização'].max()*100, line=dict(color='white', width=1, dash='dot'))
    #Escrever texto no gráfico
    fig.add_annotation(x=13, y=250, text='< 50% dos meses acima do dólar', showarrow=False)
    fig.add_annotation(x=43, y=250, text='> 50% dos meses acima do dólar', showarrow=False)
    fig.add_annotation(x=28, y=-50, text='Valorização atual inferior ao dólar', showarrow=False)
    #fig.add_annotation(x=43, y=-50, text='Valorização atual inferior ao dólar', showarrow=False)
        #fig.add_trace(go.Scatter(x=df_dolar['Ano-Mes'], y=df_dolar['valor']*100, mode='lines', name='Dólar', line=dict(color='white', width=1, dash='dot'), line_shape='spline'))
    fig.update_layout(title='Valorização das Ações',
                        xaxis_title='Meses acima do dólar',
                        yaxis_title='Valorização',
                        legend_title='Ações')
    st.plotly_chart(fig, use_container_width=True)

#valorização média de cada ação
acoes_ranqueadas['ValorizacaoMedia'] = 0
#df_acoes[df_acoes['Ações'].isin(acoes_ranqueadas['Ações'])].groupby('Ações')['Valorização'].mean()
for i in acoes_ranqueadas.index:
    acoes_ranqueadas.loc[i, 'ValorizacaoMedia'] = df_acoes[df_acoes['Ações'] == acoes_ranqueadas.loc[i, 'Ações']]['Valorização'].mean()
#st.write(df_acoes[df_acoes['Ações'].isin(acoes_ranqueadas['Ações'])].groupby('Ações')['Valorização'].mean())
st.dataframe(acoes_ranqueadas, use_container_width=True)


#Gráfico de dispersão com a valorização das ações
st.write('**Valorização das Ações**')


#Scatter plot
#for i in acoes_ranqueadas.index:
#    fig.add_trace(go.Scatter(x=acoes_ranqueadas.iloc[i]['Valor Atual'], y=acoes_ranqueadas.iloc[i]['Valorização'], mode='markers', name=acoes_ranqueadas.iloc[i]['Ações']))
#Contar quantos meses a ação ficou acima do dólar


#st.write(acoes_ranqueadas)
#fig.add_trace(go.Scatter(x=acoes_ranqueadas['MesesAcimaDolar'], y=acoes_ranqueadas['Valorização'], mode='markers', 
#    text = acoes_ranqueadas['Ações']))#, marker_color= acoes_ranqueadas['Valorização'],))	




#boxplot ações
st.subheader('Boxplot de Ações', divider=True)

acoes = df_acoes['Ações'].unique()
acoes_selecionadas = st.multiselect('Selecione ações para compará-las', acoes, max_selections=5)

import services.ColorMethods as cm
#Seleção de cor para cada ação selecionada
cols = st.columns(5)
cor_acoes = {}
for c in range(5):
    with cols[c]:
        if (c < len(acoes_selecionadas)):
            color = st.color_picker(f'Escolha uma cor para a ação {acoes_selecionadas[c]}', key=f'color_picker_{c}', value=cm.gerar_cor_hex())
            cor_acoes[acoes_selecionadas[c]] = color



#Substituir por coleta da API
df_acoes_selecionadas = df_acoes_valores[df_acoes_valores['Ações'].isin(acoes_selecionadas)]

cols = st.columns(2)

#Gráfico de linhas com a valorização das ações
with cols[0]:
    fig = go.Figure()
    for acao in acoes_selecionadas:
        df = df_acoes[df_acoes['Ações'] == acao]
        fig.add_trace(go.Scatter(x=df['Ano-Mes'], y=df['Valorização']*100, mode='lines', name=acao, line=dict(color=cor_acoes[acao], width=2)))
    if(st.checkbox('Mostrar valorização do dólar')):
        fig.add_trace(go.Scatter(x=df_dolar['Ano-Mes'], y=df_dolar['valor']*100, mode='lines', name='Dólar', line=dict(color='white', width=1, dash='dot'), line_shape='spline'))
    
    fig.update_layout(title='Valor das Ações',
                        xaxis_title='Data',
                        yaxis_title='Valor',
                        legend_title='Ações')
                    
    st.plotly_chart(fig, use_container_width=True)

#Boxplot das ações selecionadas
with cols[1]:
    fig = go.Figure()
    for acao in df_acoes_selecionadas['Ações'].unique():
        df = df_acoes_selecionadas[df_acoes_selecionadas['Ações'] == acao]
        fig.add_trace(go.Box(y=df['Valor'], name=acao, marker_color=cor_acoes[acao]))


    fig.update_layout(title='Boxplot de Ações',
                        yaxis_title='Valor',
                        legend_title='Ações')
    st.plotly_chart(fig, use_container_width=True)



#LLM gera um relatório com as ações selecionadas e a valorização do dólar
