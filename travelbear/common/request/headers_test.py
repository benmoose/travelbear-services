import pytest
from django.test import RequestFactory

from .headers import get_authorization_header


@pytest.fixture
def request_factory():
    return RequestFactory()


def test_get_authorization_header(request_factory):
    request = request_factory.get("/", HTTP_AUTHORIZATION="Bearer: foo")
    assert get_authorization_header(request) == "Bearer: foo"
