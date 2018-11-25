import pytest

from django.urls import reverse
from django.test import Client

from db_layer.event import Event
from .create_events import create_event


def count_events_in_db():
    return len(Event.objects.all())


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def endpoint_url():
    return reverse(create_event)


def test_create_event_bad_request(api_client, endpoint_url):
    assert 0 == count_events_in_db()
    response = api_client.post(endpoint_url, data=None)
    assert response.status_code == 400
    assert 0 == count_events_in_db()
