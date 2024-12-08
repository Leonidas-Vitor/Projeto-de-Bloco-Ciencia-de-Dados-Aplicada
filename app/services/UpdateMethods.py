import requests as req
import pandas as pd
from datetime import datetime
import streamlit as st


@st.cache_data
def GetLastDate(database, collection):
    response = eval(req.get(f'{st.session_state["config"]["API_URL"]}/mongodb/last', 
                                params={'database': database, 'collection': collection}).json())
    lastDate = datetime.strptime(response['year-month'], '%Y-%m').date()
    return lastDate

@st.cache_data
def GetLastDates():
    lastDates = {}
    lastDates['selic'] = GetLastDate(database='Indicators', collection='SELIC')
    lastDates['dolar'] = GetLastDate(database='Indicators', collection='Dollar')
    lastDates['ipca'] = GetLastDate(database='Indicators', collection='IPCA')
    lastDates['stock'] = GetLastDate(database='Stocks', collection='Prices')
    return lastDates


@st.cache_data
def GetStockLastPrices(ticker: str, lastdate : datetime.date) -> pd.DataFrame:
    try:
        response = req.get(f'{st.session_state["config"]["API_URL"]}/yfinance/stock-monthly-price', 
                            params={'ticker': ticker, 'start': lastdate}).json()
        df = pd.DataFrame(response['data'])
        return df
    except:
        return pd.DataFrame()

@st.cache_data
def GetIndicatorsLastValues(indicator: str, lastdate : datetime.date) -> pd.DataFrame:
    try:
        response = req.get(f'{st.session_state["config"]["API_URL"]}/bcb/{indicator}', 
                            params={'start_date': lastdate}).json()
        df = pd.DataFrame(response['data'])
        return df
    except:
        return pd.DataFrame()
    
@st.cache_data
def BCBStatus() -> bool:
    try:
        return req.get(f'{st.session_state["config"]["API_URL"]}/bcb').status_code == 200
    except:
        return False
    
@st.cache_data
def YFinanceStatus() -> bool:
    try:
        return req.get(f'{st.session_state["config"]["API_URL"]}/yfinance').status_code == 200
    except:
        return False
    
@st.cache_data
def GetStocksTickers() -> list:
    try:
        return eval(req.get(f'{st.session_state["config"]["API_URL"]}/mongodb/tickers').json())
    except:
        return []