from django.test import Client
from django.urls import reverse
import pytest

from common.parse import safe_parse_json
from db_layer.trip import create_trip, create_location
from db_layer.user import get_or_create_user

from .get_trip import get_trip_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "some trip")


@pytest.fixture
def location(trip):
    return create_location(trip, display_name="London", lat=51.105667, lng=-0.12)


@pytest.fixture
def endpoint(trip):
    return reverse(get_trip_handler, kwargs={"trip_id": trip.trip_id})


@pytest.fixture
def call_endpoint(api_client, endpoint):
    def _call_endpoint():
        return api_client.get(endpoint, HTTP_TEST_USER_EXTERNAL_ID="test-user")
    return _call_endpoint


@pytest.mark.django_db
def test_return_trip_without_locations(call_endpoint, trip):
    response = call_endpoint()
    assert response.status_code == 200
    response_body = safe_parse_json(response.content)
    assert response_body == {
        "trip_id": str(trip.trip_id),
        "title": "some trip",
        "description": "",
        "locations": [],
        "is_deleted": False,
    }


@pytest.mark.django_db
def test_return_trip_with_locations(call_endpoint, trip, location):
    response = call_endpoint()
    assert response.status_code == 200
    response_body = safe_parse_json(response.content)
    assert response_body == {
        "trip_id": str(trip.trip_id),
        "title": "some trip",
        "description": "",
        "locations": [
            {
                "location_id": str(location.location_id),
                "display_name": "London",
                "lat": "51.105667",
                "lng": "-0.120000",
            },
        ],
        "is_deleted": False,
    }
