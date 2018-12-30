import json

from django.test import Client
from django.urls import reverse
import pytest

from db_layer.trip import create_trip, create_location
from db_layer.user import get_or_create_user
from .create_move import create_move_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def url():
    return reverse(create_move_handler)


@pytest.fixture
def call_endpoint(api_client, url):
    def _call_endpoint(user=None, data=None):
        headers = {"HTTP_TEST_USER_EXTERNAL_ID": user.external_id} if user else {}
        return api_client.post(url, content_type="application/json", data=json.dumps(data), **headers)

    return _call_endpoint


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip", "test description")


@pytest.mark.django_db
def test_create_move_success(call_endpoint, trip):
    location_1 = create_location(trip, "1", 51, 0)
    location_2 = create_location(trip, "2", 51, 0)
    response = call_endpoint(data={"start_location": "bar", "end_location": "foo"})
    assert response.status_code == 201
