import json
import os
from http import HTTPStatus

import dotenv
import requests
from fastapi import FastAPI

from mydatasales_back_end.Modules.token import Token

""" import pandas as pd """

app = FastAPI()

dotenv.load_dotenv(dotenv.find_dotenv())
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_url")
refresh_token = os.getenv("refresh_token")
app_access = os.getenv("app_access")

global_token = Token(app_access, refresh_token, client_id, client_secret, redirect_uri)


@app.get("/")
def read_root():
    return {"message": "Olá Mundo!"}


@app.get("/getNewCode")
def get_new_code():
    response = requests.get(
        f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"
    )
    return response.url


@app.get("/getNewTokenWithCode")
def get_new_token_with_code() -> dict:
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": "TG-669463642c4c2d0001dba80a-1865120734",
        "redirect_uri": redirect_uri,
    }
    response = requests.post(
        "https://api.mercadolibre.com/oauth/token", data=data
    )

    data_response = json.loads(response.text)
    if response.status_code != HTTPStatus.OK:
        return {
            "erro": data_response["error"],
            "status": data_response["status"],
        }

    global_token.set_app_access(data_response["access_token"])
    global_token.set_refresh_token(data_response["refresh_token"])

    global_token.update_env(
        data_response["refresh_token"], data_response["access_token"]
    )

    return {"Mensagem": "Token atualizado com sucesso", "status": "OK"}


@app.get("/getItem/{item_id}")
async def getITem(item_id):
    headers = {"Authorization": f"Bearer {global_token.get_app_access()}"}
    response = requests.get(
        f"https://api.mercadolibre.com/items/{item_id}", headers=headers
    )
    print(global_token.get_app_access())
    print(response.status_code)
    if response.status_code == HTTPStatus.BAD_REQUEST:
        global_token.get_new_token_with_refresh()
        response = requests.get(
            f"https://api.mercadolibre.com/items/{item_id}", headers=headers
        )
        return response.json()
    return response.json()
