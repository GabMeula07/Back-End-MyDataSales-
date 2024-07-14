from http import HTTPStatus

from fastapi.testclient import TestClient

from mydatasales_back_end.app import app


def test_read_root_return_OK():
    client = TestClient(app)  # Arrange (organização do teste)
    response = client.get("/")  # Act (ação)
    assert response.status_code == HTTPStatus.OK  # assert (certifique)
    assert response.json() == {"message": "Olá Mundo!"}
