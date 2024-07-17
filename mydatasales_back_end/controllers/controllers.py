import json
from http import HTTPStatus

import requests


def home_controller():
    return {"message": "Olá Mundo!"}


def get_make_request_autorized(url, data, global_token):
    headers = {"Authorization": f"Bearer {global_token.get_app_access()}"}
    response = requests.get(url, headers=headers, data=data)
    return response


def fix_no_authorized_request(item_id, global_token):
    global_token.get_new_token_with_refresh()
    new_response = get_make_request_autorized(
        f"https://api.mercadolibre.com/items/{item_id}", None, global_token
    )
    return new_response


def get_make_request(url, headers, data):
    response = requests.get(url, headers=headers, data=data)
    return response


def post_make_request(url, headers, data):
    response = requests.post(url, headers=headers, data=data)
    return response


def new_code_controller(client_id, redirect_uri):
    response = get_make_request(
        f"https://auth.mercadolivre.com.br/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}",
        None,
        None,
    )
    return response.url


def new_token_w_code_controller(
    global_token, client_id, client_secret, redirect_uri
):
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": "TG-669463642c4c2d0001dba80a-1865120734",
        "redirect_uri": redirect_uri,
    }

    response = post_make_request(
        "https://api.mercadolibre.com/oauth/token", headers=None, data=data
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


def get_item_controller(item_id, global_token):
    response = get_make_request_autorized(
        f"https://api.mercadolibre.com/items/{item_id}", None, global_token
    )

    if (response.status_code == HTTPStatus.BAD_REQUEST):
        return fix_no_authorized_request.json()

    return response.json()


def filter_pictures_item(response):
    data_response = response.json()
    urls = []
    for item in data_response["pictures"]:
        urls.append(item["url"])
    return {"pictures":urls}

def get_item_pictures_controller(item_id, global_token): 
    response = get_make_request_autorized(
        f"https://api.mercadolibre.com/items/{item_id}", None, global_token
    )
    if (response.status_code == HTTPStatus.BAD_REQUEST):
        return filter_pictures_item(fix_no_authorized_request(item_id, global_token))
    return filter_pictures_item(response)

def get_item_prices_controller(item_id, global_token):
    return get_make_request_autorized( f"https://api.mercadolibre.com/items/{item_id}/prices",None, global_token).json()