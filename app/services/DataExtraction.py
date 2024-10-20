import pandas as pd
import yfinance as yf
from tqdm import tqdm


def GetStockData(stock_ticker, period='5y'):
    acao = yf.Ticker(stock_ticker)
    historico = acao.history(period=period)
    print('Fsdasdsadsadasd')
    if not historico.empty:
        # Remover informações de fuso horário, se existirem
        if historico.index.tz is not None:
            historico.index = historico.index.tz_localize(None)
        historico['Month'] = historico.index.to_period('M')

        media_mensal = historico.groupby('Month')['Close'].mean()
        media_mensal = pd.DataFrame(media_mensal)
        media_mensal['Ticker'] = stock_ticker
        media_mensal = media_mensal.rename(columns={'Close': 'CloseMean'})
        media_mensal.sort_index(inplace=True)

        # Converta o DataFrame para uma lista de dicionários para evitar problemas de serialização
        return media_mensal.reset_index().to_dict(orient='records')
    else:
        print(f"Não foi possível coletar dados para a ação {stock_ticker}")
        return []

def GetStockData(stock_name, stock_ticker, period='5y'):
    acao = yf.Ticker(stock_ticker)
    historico = acao.history(period=period)

    if not historico.empty:
        # Remover informações de fuso horário, se existirem
        if historico.index.tz is not None:
            historico.index = historico.index.tz_localize(None)
        historico['Month'] = historico.index.to_period('M')

        media_mensal = historico.groupby('Month')['Close'].mean()
        media_mensal = pd.DataFrame(media_mensal)
        media_mensal['Stock'] = stock_name
        media_mensal['Ticker'] = stock_ticker
        media_mensal = media_mensal.rename(columns={'Close': 'CloseMean'})
        media_mensal.sort_index(inplace=True)

        # Converta o DataFrame para uma lista de dicionários para evitar problemas de serialização
        return media_mensal.reset_index().to_dict(orient='records')
    else:
        print(f"Não foi possível coletar dados para a ação {stock_name} ({stock_ticker})")
        return []
