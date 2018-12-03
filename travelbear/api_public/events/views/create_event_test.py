import pytest

from django.urls import reverse
from django.test import Client

from db_layer.event import Event
from db_layer.user import get_or_create_user
from ..urls import root


def count_events_in_db():
    return len(Event.objects.all())


@pytest.fixture
def api_client():
    return Client(HTTP_MOCK_USER_SUB="foo")


@pytest.fixture
def endpoint_url():
    return reverse(root)


@pytest.mark.django_db
def test_create_event_bad_request(api_client, endpoint_url):
    get_or_create_user(external_id="foo")

    assert 0 == count_events_in_db()
    response = api_client.post(endpoint_url, data={"title": 0, "max_guests": "3.6"})
    assert response.status_code == 400
    assert 0 == count_events_in_db()


@pytest.mark.django_db
def test_create_event(api_client, endpoint_url):
    get_or_create_user(external_id="foo")

    assert 0 == count_events_in_db()
    response = api_client.post(
        endpoint_url,
        data={
            "title": "title",
            "description": "some description",
            "start_time": "2018-01-01T00:00:00Z",
            "end_time": "2018-01-01T10:00:00Z",
            "max_guests": 10,
        },
    )
    assert response.status_code == 201
    assert 1 == count_events_in_db()
