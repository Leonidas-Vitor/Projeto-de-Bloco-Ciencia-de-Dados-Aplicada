import pandas as pd
import plotly.graph_objects as go


def plot_indicators(df_ipca, df_dolar, df_selic) -> go.Figure:
    fig = go.Figure()
    # adicionar % no eixo y
    fig.update_yaxes(tickformat=".2%")
    fig.add_trace(go.Scatter(x=df_ipca['year-month'], y=df_ipca['accumulated']*0.01, mode='lines', name='IPCA Acumulado'))
    fig.add_trace(go.Scatter(x=df_dolar['year-month'], y=df_dolar['valorization']*0.01, mode='lines', name='Valorização Dolar'))
    fig.add_trace(go.Scatter(x=df_selic['year-month'], y=df_selic['accumulated']*0.01, mode='lines', name='SELIC Acumulado'))
    return fig

def plot_stock_scatterplot(df_stock_info : pd.DataFrame, currentDollarValorization , meses) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_stock_info['months_above_dolar'], y=df_stock_info['currentValorization'] * 0.01, 
                             mode='markers', text=df_stock_info['ticker'], name='Ações'))
    
    min_valorization = df_stock_info['currentValorization'].min()*0.01
    max_valorization = df_stock_info['currentValorization'].max()*0.01

    currentDollarValorization = currentDollarValorization*0.01
    #plotar linha da valorização atual do dólar
    fig.add_trace(go.Scatter(x=[0, meses], y=[currentDollarValorization,currentDollarValorization], 
                             mode='lines', name='Dólar', line=dict(color='white', width=1, dash='dot')))
    #plotar linha vertical no meio do gráfico
    fig.add_shape(type='line', x0=meses/2, x1=meses/2, y0=-currentDollarValorization-abs(min_valorization)-0.5, y1=max_valorization+0.5, 
                  line=dict(color='white', width=1, dash='dot'))
    #Escrever texto no gráfico
    fig.add_annotation(x=meses/4, y=currentDollarValorization+1, text='< 50% dos meses acima do dólar', showarrow=False)
    fig.add_annotation(x=meses/4 * 3, y=currentDollarValorization+1, text='> 50% dos meses acima do dólar', showarrow=False)
    fig.add_annotation(x=28, y=currentDollarValorization-1, text='Valorização atual inferior ao dólar', showarrow=False)

    fig.update_yaxes(tickformat=".0%")
    fig.update_layout(title='Valorização das Ações',
                        xaxis_title='Meses acima do dólar',
                        yaxis_title='Valorização',
                        legend_title='Ações',
                        height=800)
    return fig

def plot_stock_timeline(df_stock_values : pd.DataFrame, colors) -> go.Figure:
    fig = go.Figure()
    for i, ticker in enumerate(df_stock_values['ticker'].unique()):
        df = df_stock_values[df_stock_values['ticker'] == ticker]
        fig.add_trace(go.Scatter(x=df['year-month'], y=df['price'], mode='lines', name=ticker, line=dict(color=colors[ticker])))
    fig.update_layout(title='Valor das Ações',
                        xaxis_title='Mês',
                        yaxis_title='Valor',
                        legend_title='Ações',
                        height=500)
    return fig

def plot_stock_boxplot(df_stock_values : pd.DataFrame, colors) -> go.Figure:
    fig = go.Figure()
    for i, ticker in enumerate(df_stock_values['ticker'].unique()):
        df = df_stock_values[df_stock_values['ticker'] == ticker]
        fig.add_trace(go.Box(y=df['price'], name=ticker, marker_color=colors[ticker]))
    fig.update_layout(title='Boxplot das Ações',
                        yaxis_title='Valor',
                        legend_title='Ações',
                        height=500)
    return fig