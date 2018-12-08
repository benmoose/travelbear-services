import json
from uuid import uuid4

from django.test import Client
from django.urls import reverse
import pytest

from common.parse import safe_parse_json
from db_layer.trip import create_trip, Location
from db_layer.user import get_or_create_user
from .create_location import create_location_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def endpoint():
    def _endpoint(trip_id):
        return reverse(create_location_handler, kwargs={"trip_id": trip_id})

    return _endpoint


@pytest.fixture
def call_endpoint(api_client, endpoint, user):
    def _call_endpoint(trip_id, data=None):
        return api_client.post(
            endpoint(trip_id),
            data=json.dumps(data),
            content_type="application/json",
            HTTP_TEST_USER_EXTERNAL_ID=user.external_id,
        )

    return _call_endpoint


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.mark.django_db
def test_create_location_no_trip(call_endpoint):
    assert 0 == len(Location.objects.all())
    response = call_endpoint(uuid4())
    assert response.status_code == 404
    assert 0 == len(Location.objects.all())


@pytest.mark.django_db
def test_create_location_bad_request(call_endpoint, trip):
    assert 0 == len(Location.objects.all())
    response = call_endpoint(trip.trip_id, data={"display_name": 123})
    assert response.status_code == 400
    assert 0 == len(Location.objects.all())


@pytest.mark.django_db
def test_create_location_bad_request(call_endpoint, trip):
    assert 0 == len(Location.objects.all())
    response = call_endpoint(
        trip.trip_id,
        data={
            "display_name": "location name",
            "lat": 51.5,
            "lng": -0.12,
            "google_place_id": "foobar",
        },
    )
    assert response.status_code == 201
    response_body = safe_parse_json(response.content)
    assert response_body == {
        "location_id": response_body["location_id"],
        "display_name": "location name",
        "lat": 51.5,
        "lng": -0.12,
        "google_place_id": "foobar",
    }
    assert 1 == len(Location.objects.all())
