from uuid import uuid4

import pytest
from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_rfc3339
from db_layer.trip import add_member_to_trip, create_location, create_trip
from db_layer.user import get_or_create_user

from .handlers import trip_id_endpoint


@pytest.fixture
def time():
    return safe_parse_rfc3339("2019-01-01T10:00:00Z")


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(time, user):
    trip = create_trip(user, "some trip")
    trip.created_on = time
    trip.save()
    return trip


@pytest.mark.django_db
def test_return_trip_no_trip(user):
    response = call_endpoint(user, str(uuid4()))
    assert response.status_code == 404


@pytest.mark.django_db
def test_return_trip_without_locations(user, trip):
    response = call_endpoint(user, trip.trip_id)
    assert response.status_code == 200
    assert {
        "trip_id": str(trip.trip_id),
        "title": "some trip",
        "created_on": "2019-01-01T10:00:00Z",
        "locations": [],
    } == response.json()


@pytest.mark.django_db
def test_return_trip_with_locations(user, trip):
    location = create_location(trip, display_name="London", lat=51.105667, lng=-0.12)

    response = call_endpoint(user, trip.trip_id)
    assert response.status_code == 200
    assert {
        "trip_id": str(trip.trip_id),
        "title": "some trip",
        "created_on": "2019-01-01T10:00:00Z",
        "locations": [
            {
                "location_id": str(location.location_id),
                "display_name": "London",
                "coords": [51.105667, -0.120000],
            }
        ],
    } == response.json()


@pytest.mark.django_db
def test_can_get_details_if_trip_member(trip):
    member, _ = get_or_create_user("member")

    add_member_to_trip(member, trip)

    response = call_endpoint(member, trip.trip_id)
    assert response.status_code == 200
    assert {
        "trip_id": str(trip.trip_id),
        "title": "some trip",
        "locations": [],
        "created_on": "2019-01-01T10:00:00Z",
    } == response.json()


def call_endpoint(as_user, trip_id):
    client = Client()
    url = reverse(trip_id_endpoint, kwargs={"trip_id": trip_id})
    return client.get(url, HTTP_TEST_USER_EXTERNAL_ID=as_user.external_id)
