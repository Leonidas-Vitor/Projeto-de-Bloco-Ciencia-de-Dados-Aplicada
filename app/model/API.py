import streamlit as st
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from threading import Thread

api = FastAPI()

# Definindo o modelo para a requisição POST
class Item(BaseModel):
    name: str
    value: float

# Endpoint GET
@api.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}", "value": 42.0}

# Endpoint POST
@api.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "value": item.value}

def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8502)

api_thread = Thread(target=run_api, daemon=True)
api_thread.start()

st.title('API')

st.write('**Documentação da API**')
st.write('A API possui dois endpoints: um para requisições GET e outro para requisições POST.')
st.write('### GET /items/{item_id}')
st.write('Retorna um item com o id especificado.')
st.write('### POST /items/')
st.write('Cria um item com o nome e valor especificados.')
