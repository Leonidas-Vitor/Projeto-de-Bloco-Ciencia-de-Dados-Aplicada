import requests as req
import pandas as pd
from datetime import datetime
import streamlit as st

@st.cache_data
def GetStockLastPrices(ticker: str, lastdate : datetime.date) -> pd.DataFrame:
    response = eval(req.get(f'{st.session_state["config"]["API_URL"]}/yfinance/stock-monthly-price', 
                        params={'ticker': ticker, 'start': lastdate}).json())
    df = pd.DataFrame(response)
    return df

@st.cache_data
def GetIndicatorsLastValues(indicator: str, lastdate : datetime.date) -> pd.DataFrame:
    try:
        response = eval(req.get(f'{st.session_state["config"]["API_URL"]}/bcb/{indicator}', 
                            params={'start_date': lastdate}).json())
        df = pd.DataFrame(response)
        return df
    except:
        return pd.DataFrame()