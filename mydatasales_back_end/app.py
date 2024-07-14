import os
from http import HTTPStatus

import dotenv
import requests
from fastapi import FastAPI

from mydatasales_back_end.Modules.token import Token

""" import pandas as pd """
import json

app = FastAPI()

dotenv.load_dotenv(dotenv.find_dotenv())
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_url")
global_token = Token(None, None, client_id, client_secret)


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
        "code": "TG-6693be58daf74e0001ae5695-1865120734",
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
    newAppAccess = data_response["access_token"]
    newRefreshToken = data_response["refresh_token"]

    global_token.set_app_access(newAppAccess)
    global_token.set_refresh_token(newRefreshToken)

    return {"Mensagem": "Token atualizado com sucesso", "status": "OK"}


@app.get("/getItem")
def getITem():
    item = "MLB964825686"
    headers = {"Authorization": f"Bearer {global_token.get_app_access()}"}
    response = requests.get(
        f"https://api.mercadolibre.com/items/{item}", headers=headers
    )
    if response.status_code == HTTPStatus.BAD_REQUEST:
        global_token.get_new_token_with_refresh()
        response = requests.get(
            f"https://api.mercadolibre.com/items/{item}", headers=headers
        )
        return response.json()
    return response.json()
