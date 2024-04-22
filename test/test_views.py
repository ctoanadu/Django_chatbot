import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client_api():
    return APIClient()


def test_get_endpoint(client_api):
    response = client_api.get("")
    assert response.status_code == 200


def test_get_invalid_endpoint(client_api):
    response = client_api.get("/home")
    assert response.status_code == 404
