import os

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mydatasales_back_end.controllers.controllers import (
    get_item_controller,
    get_item_pictures_controller,
    get_item_prices_controller,
    home_controller,
    new_code_controller,
    new_token_w_code_controller,
)
from mydatasales_back_end.Modules.token import Token

""" import pandas as pd """

app = FastAPI()
origins = [
    'http://localhost:8000',
    'http://localhost:3000',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

dotenv.load_dotenv(dotenv.find_dotenv())
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = os.getenv("redirect_url")
refresh_token = os.getenv("refresh_token")
app_access = os.getenv("app_access")

global_token = Token(
    app_access, refresh_token, client_id, client_secret, redirect_uri
)

global_token.get_new_token_with_refresh()



@app.get("/")
def home():
    return home_controller()


@app.get("/getNewCode")
def get_new_code():
    return new_code_controller(client_id, redirect_uri)


@app.get("/getNewTokenWithCode")
def get_new_token_with_code() -> dict:
    return new_token_w_code_controller(
        global_token, client_id, client_secret, redirect_uri
    )


@app.get("/item/{item_id}")
async def getItem(item_id):
    return get_item_controller(item_id, global_token)


@app.get("/item/{item_id}/pictures")
async def getItemPictures(item_id):
    return get_item_pictures_controller(item_id, global_token)


@app.get("/item/{item_id}/prices")
async def getItemPrices(item_id):
    return get_item_prices_controller(item_id, global_token)


@app.get("/refresh-token")
def refresh_token():
    return global_token.get_new_token_with_refresh()
