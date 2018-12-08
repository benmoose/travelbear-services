from django.test import Client
import pytest


@pytest.fixture
def api_client():
    return Client()
