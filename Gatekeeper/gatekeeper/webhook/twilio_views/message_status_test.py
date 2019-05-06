import pytest

from django.urls import reverse
from django.test import Client

from .message_status import message_status_webhook


@pytest.fixture(scope="module")
def api_client():
    return Client()


@pytest.fixture
def url():
    return reverse(message_status_webhook)


def test_message_status(api_client, url):
    response = api_client.post(url, {"message_sid": "foo", "sms_sid": "bar"})
    assert 200 == response.status_code
