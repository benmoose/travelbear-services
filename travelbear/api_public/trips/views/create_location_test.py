import json
from uuid import uuid4

import pytest
from django.test import Client
from django.urls import reverse

from common.test import count_models_in_db, no_models_in_db
from db_layer.trip import Location, create_trip
from db_layer.user import get_or_create_user

from .create_location import create_location_handler


def call_endpoint(user, trip_id, data=None):
    client = Client()
    url = reverse(create_location_handler, kwargs={"trip_id": trip_id})
    return client.post(
        path=url,
        data=json.dumps(data),
        content_type="application/json",
        HTTP_TEST_USER_EXTERNAL_ID=user.external_id,
    )


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.mark.django_db
def test_create_location_no_trip(user):
    assert no_models_in_db(Location)
    response = call_endpoint(user, uuid4())
    assert response.status_code == 404
    assert no_models_in_db(Location)


@pytest.mark.django_db
def test_create_location_bad_request(user, trip):
    assert no_models_in_db(Location)
    response = call_endpoint(user, trip.trip_id, data={"display_name": 123})
    assert response.status_code == 400
    assert no_models_in_db(Location)


@pytest.mark.django_db
def test_create_location(user, trip):
    assert no_models_in_db(Location)
    response = call_endpoint(
        user=user,
        trip_id=trip.trip_id,
        data={
            "display_name": "location name",
            "lat": 51.5,
            "lng": -0.12,
            "google_place_id": "foobar",
        },
    )
    assert response.status_code == 201
    assert {
        "location_id": response.json().get("location_id"),
        "display_name": "location name",
        "lat": 51.5,
        "lng": -0.12,
        "google_place_id": "foobar",
    } == response.json()

    assert 1 == count_models_in_db(Location)


@pytest.mark.django_db
def test_create_location_for_other_users_trip(trip):
    assert no_models_in_db(Location)
    someone_else, _ = get_or_create_user("someone-else")
    response = call_endpoint(
        user=someone_else,
        trip_id=trip.trip_id,
        data={"display_name": "location name", "lat": 51.5, "lng": -0.12},
    )

    assert response.status_code == 404
    assert no_models_in_db(Location)
