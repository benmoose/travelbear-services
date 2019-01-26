from django.test import Client
from django.urls import reverse
import pytest

from .health import health_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def health_endpoint():
    return reverse(health_handler)


def test_health_check(api_client, health_endpoint):
    response = api_client.get(health_endpoint)
    assert response.status_code == 200
    assert {"status": "ok"} == response.json()
