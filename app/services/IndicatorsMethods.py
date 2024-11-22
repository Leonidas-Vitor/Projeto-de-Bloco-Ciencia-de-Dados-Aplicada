import pandas as pd
import numpy as np


def GetDollarVariationData(dollar : pd.DataFrame, year_month = '2020-01') -> pd.DataFrame:
    '''
    Retorna a variação do dólar em relação a um determinado mês.
    '''
    df = dollar.copy()
    df = df.sort_values(by='year-month')
    df = df[df['year-month'] >= year_month].copy()
    df['valorization'] = (df['price'] / dollar[dollar['year-month'] == year_month]['price'].values[0] - 1) * 100
    return df

#----------------------------------------------

def GetSelicAccumulatedData(selic : pd.DataFrame, year_month = '2020-01') -> pd.DataFrame:
    '''
    Retorna a taxa Selic acumulada em relação a um determinado mês.
    '''
    df = selic.copy()
    df = df.sort_values(by='year-month')
    df = df[df['year-month'] >= year_month].copy()
    df['accumulated'] = df['value'].cumsum().round(2)
    return df

#----------------------------------------------

def GetIpcaAccumulatedData(ipca : pd.DataFrame, year_month = '2020-01') -> pd.DataFrame:
    '''
    Retorna o IPCA acumulado em relação a um determinado mês.
    '''
    df = ipca.copy()
    df = df.sort_values(by='year-month')
    df = df[df['year-month'] >= year_month]
    df['accumulated'] = df['value'].cumsum().round(2)
    return df