import json
from http import HTTPStatus

import requests


class Token:
    def __init__(
        self, app_acess, refresh_token, client_id, client_secret, redirect_uri
    ) -> None:
        self.__app_access = app_acess
        self.__refresh_token = refresh_token
        self.__redirect_uri = redirect_uri
        self.__client_id = client_id
        self.__client_secret = client_secret

    def get_new_token_with_refresh(self):
        data = {
            "grant_type": "authorization_code",
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
            "refresh_token": self.__refresh_token,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
        }
        response = requests.post(
            "https://api.mercadolibre.com/oauth/token",
            headers=headers,
            data=data,
        )
        data_response = json.loads(response.text)
        if response.status_code == HTTPStatus.BAD_REQUEST:
            return "Erro de autorização"

        newAppAccess = data_response["access_token"]
        newRefreshToken = data_response["refresh_token"]

        self.set_app_access(newAppAccess)
        self.set_refresh_token(newRefreshToken)

        self.update_env(newRefreshToken, newAppAccess)

        return "OK"

    def get_app_access(self) -> str:
        return self.__app_access

    def get_refresh_token(self) -> str:
        return self.__refresh_token

    def set_app_access(self, app_access) -> None:
        self.__app_access = app_access

    def set_refresh_token(self, refresh_token) -> None:
        self.__refresh_token = refresh_token

    def update_env(self, refresh_token: str, app_access: str):
        env = open("./mydatasales_back_end/.env", "w")
        lines = [
            f"client_secret='{self.__client_secret}'",
            f"client_id='{self.__client_id}'",
            f"redirect_url='{self.__redirect_uri}'",
            f"refresh_token='{refresh_token}'",
            f"app_access='{app_access}'",
        ]
        print('passei aqui')
        env.writelines(lines)
        env.close()
