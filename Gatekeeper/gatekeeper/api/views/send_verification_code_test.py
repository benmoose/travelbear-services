import pytest
from django.test import Client
from django.urls import reverse

from .send_verification_code import send_verification_code


@pytest.fixture(scope="module")
def api_client():
    return Client()


@pytest.fixture
def url():
    return reverse(send_verification_code)


def test_send_verification_code(api_client, url):
    response = api_client.post(url)
    assert 200 == response.status_code
