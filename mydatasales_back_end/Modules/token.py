import json

import requests


class Token:
    def __init__(
        self,
        app_acess,
        refresh_token,
        client_id,
        client_secret,
    ) -> None:
        self.__app_access = app_acess
        self.__refresh_token = refresh_token
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
        data_response = json.loads(response.txt)
        if response.status_code == 400:
            return "Erro de autorização"

        newAppAccess = data_response["access_token"]
        newRefreshToken = data_response["refresh_token"]

        self.set_app_access(newAppAccess)
        self.set_refresh_token(newRefreshToken)

        return "OK"

    def get_app_access(self) -> str:
        return self.__app_access

    def get_refresh_token(self) -> str:
        return self.__refresh_token

    def set_app_access(self, app_access) -> None:
        self.__app_access = app_access

    def set_refresh_token(self, refresh_token) -> None:
        self.__refresh_token = refresh_token
