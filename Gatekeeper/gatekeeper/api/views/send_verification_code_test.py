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


@pytest.mark.parametrize("request_data", [{}, {"foo": "bar"}])
def test_send_verification_code_bad_request(api_client, url, request_data):
    response = api_client.post(url, data=request_data)
    assert 400 == response.status_code
