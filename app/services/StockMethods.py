import pandas as pd
import numpy as np

#Funções para processamento de dados de ações

# Função para substituir valores em casos complexos
def replace_nested_nan(value):
    if value == {"$numberDouble": "NaN"}:
        return np.nan
    return value

def GetStockValorization(stockPrices : pd.DataFrame, year_month = '2020-01') -> pd.DataFrame:
    '''
    Retorna a valorização de um ativo em relação a um determinado mês.
    Se o ticker for None, retorna a valorização de todos os ativos em relação a um determinado mês.
    '''

    df = stockPrices.copy()
    df = df.sort_values(by=['ticker','year-month'])
    df_ticker = pd.DataFrame()
    df_filtered = pd.DataFrame()
    for ticker in df['ticker'].unique():
        referenceValue = df[(df['ticker'] == ticker) & (df['year-month'] == year_month)]['price']
        ##SE O TICKER NÃO EXISTIR NO MÊS, RETORNA ERRO
        try:
            referenceValue = float(referenceValue.values[0])
        except:
            referenceValue = np.nan

        #year_month_index = df[df['year-month'] == year_month].index[0]
            
        df_ticker = df[(df['ticker'] == ticker) & (df['year-month'] >= year_month)].copy()
        df_ticker['valorization'] = (df_ticker['price'].apply(lambda x: float(x) / referenceValue - 1) * 100)
        df_ticker = df_ticker[['ticker', 'year-month', 'price', 'valorization']]
        df_filtered = pd.concat([df_filtered, df_ticker])
    return df_filtered

def GetStockCurrentValorization(stockPrices : pd.DataFrame, year_month = '2020-01') -> pd.DataFrame:
    '''
    Retorna a valorização de um ativo em relação ao mês informado. Se o preço da ação no mês informado for NaN, usar o último valor disponível.
    '''
    df = stockPrices.copy()
    df = df.sort_values(by=['ticker','year-month'])
    df_ticker = pd.DataFrame()
    df_filtered = pd.DataFrame()

    for ticker in df['ticker'].unique():
        df_ticker = df[(df['ticker'] == ticker)].copy()
        referenceValue = df_ticker[(df_ticker['year-month'] == year_month)]['price']
        currentValue = df_ticker[(df_ticker['year-month'] == df_ticker['year-month'].max())]['price']
        if referenceValue.values[0] is np.nan:
            referenceValue = df_ticker[(df_ticker['year-month'] is not np.nan)].sort_values(by='year-month').iloc[0]['price']
        else:
            referenceValue = float(referenceValue.values[0])
        if currentValue.values[0] is np.nan:
            currentValue = df_ticker[(df_ticker['year-month'] is not np.nan)].sort_values(by='year-month').iloc[-1]['price']
        else:
            currentValue = float(currentValue.values[0])

        df_result = pd.DataFrame({'ticker': [ticker], 'currentValorization': (currentValue / referenceValue - 1) * 100})
        df_filtered = pd.concat([df_filtered, df_result])
    return df_filtered

def IsBDR(stockInfo : pd.DataFrame) -> pd.DataFrame:
    '''
    Retorna se a ação é um BDR ou não. Retorna um dataframe com a coluna 'is_bdr' que indica se a ação é um BDR ou não.
    '''
    df = stockInfo[['ticker','financialCurrency']].copy()
    df['BDR'] = df['financialCurrency'].apply(lambda x: True if x is not None and 'BRL' not in x else False)
    return df[['ticker','BDR']]


def GetStockMonthsAboveDolar(stockPrices : pd.DataFrame, dollar : pd.DataFrame) -> pd.DataFrame:
    '''
    Retorna a quantidade de meses que a ação valorizou mais que o dólar. Retornando um dataframe de ticker e quantidade de meses.
    '''
    stockPrices = stockPrices.copy()
    dollar = dollar.copy()
    dollar.rename(columns={'valorization':'dollar_valorization'}, inplace=True)
    stockPrices = stockPrices.sort_values(by=['ticker','year-month'])
    dollar = dollar.sort_values(by=['year-month'])
    df_ticker = pd.DataFrame()
    df_filtered = pd.DataFrame()

    for ticker in stockPrices['ticker'].unique():
        df_ticker = stockPrices[stockPrices['ticker'] == ticker].copy()
        df_ticker = df_ticker.merge(dollar[['year-month','dollar_valorization']], on='year-month', how='left')

        df_ticker['months_above_dolar'] = df_ticker['dollar_valorization'] < df_ticker['valorization']
        df_ticker = df_ticker[df_ticker['months_above_dolar'] == True]
        df_filtered = pd.concat([df_filtered, df_ticker])

    df_filtered = df_filtered.groupby('ticker').count().reset_index()
    df_filtered = df_filtered[['ticker','year-month']]
    df_filtered.columns = ['ticker', 'months_above_dolar']
    return df_filtered

def GetStockMonthAboveDolar(stockPrices : pd.DataFrame, dollar : pd.DataFrame) -> pd.DataFrame:
    '''
    Retorna se a ação valorizou mais que o dólar em um determinado mês. Retornando um dataframe com tycker, year-month e se a valorização foi acima ou não ao dólar.
    '''
    stockPrices = stockPrices.copy()
    dollar = dollar.copy()
    dollar.rename(columns={'valorization':'dollar_valorization'}, inplace=True)
    stockPrices = stockPrices.sort_values(by=['ticker','year-month'])
    dollar = dollar.sort_values(by=['year-month'])
    df_ticker = pd.DataFrame()
    df_filtered = pd.DataFrame()

    for ticker in stockPrices['ticker'].unique():
        df_ticker = stockPrices[stockPrices['ticker'] == ticker].copy()
        df_ticker = df_ticker.merge(dollar[['year-month','dollar_valorization']], on='year-month', how='left')

        df_ticker['above_dolar'] = df_ticker['dollar_valorization'] < df_ticker['valorization']
        df_ticker = df_ticker[['ticker','year-month','above_dolar']]
        df_filtered = pd.concat([df_filtered, df_ticker])

    return df_filtered
    


