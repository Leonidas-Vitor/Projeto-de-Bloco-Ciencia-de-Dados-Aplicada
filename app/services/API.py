from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn
from threading import Thread
import DataExtraction

import pandas as pd
import yfinance as yf


api = FastAPI()

# Endpoint GET
@api.get("/stock/{ticker}")
def read_item(ticker: str):
    ''' 
        Retorna os dados da ação solicitada.
    '''
    print(ticker)
    return DataExtraction.GetStockData('NaN', ticker)


# Modelo para adicionar uma nova ação ao dashboard
class NewStock(BaseModel):
    name: str = Field(alias='stock_name')
    ticker: str = Field(alias='stock_ticker')
    
    class Config:
        populate_by_name = True

# Endpoint POST
@api.post("/newStock/")
def add_newStock(newStock: NewStock):
    ''' 
        Adiciona uma nova ação ao dashboard.
    '''
    try:
        return DataExtraction.GetStockData(newStock.name, newStock.ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000)

def start_api():
    api_thread = Thread(target=run_api)
    api_thread.start()
