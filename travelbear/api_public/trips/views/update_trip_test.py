import json

import pytest
from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_rfc3339
from db_layer.trip import create_trip
from db_layer.trip.models import Trip
from db_layer.user import get_or_create_user

from .handlers import trip_id_endpoint


@pytest.fixture
def time():
    return safe_parse_rfc3339("2019-01-01T00:00:00Z")


@pytest.fixture
def api_client(user):
    return Client()


@pytest.fixture
def call_endpoint(api_client):
    def _call_endpoint(user, trip_id, data):
        url = reverse(trip_id_endpoint, kwargs={"trip_id": trip_id})
        return api_client.patch(
            url, data=json.dumps(data), HTTP_TEST_USER_EXTERNAL_ID=user.external_id
        )

    return _call_endpoint


@pytest.fixture
def user():
    user, _ = get_or_create_user(external_id="foo")
    return user


@pytest.fixture
def trip(time, user):
    trip = create_trip(
        user, title="some title", description="some desc", tags=["roadtrip"]
    )
    trip.created_on = time
    trip.save()
    return trip


@pytest.mark.django_db
def test_update_trip(call_endpoint, trip):
    assert 1 == len(Trip.objects.all())

    response = call_endpoint(trip.created_by, trip.trip_id, data=None)
    assert 400 == response.status_code

    response = call_endpoint(
        trip.created_by,
        trip.trip_id,
        data={"title": "new title", "tags": ["camping", "mountains"]},
    )
    assert 200 == response.status_code
    assert {
        "trip_id": str(trip.trip_id),
        "title": "new title",
        "description": "some desc",
        "tags": ["camping", "mountains"],
        "created_on": "2019-01-01T00:00:00Z",
    } == response.json()

    response = call_endpoint(
        trip.created_by, trip.trip_id, data={"is_deleted": True, "title": "foo"}
    )
    assert 400 == response.status_code
    assert Trip.objects.get(pk=trip.pk).is_deleted is False
    assert Trip.objects.get(pk=trip.pk).title != "foo"
    assert response.json()["validation_errors"] == [
        "Cannot update one or more requested fields"
    ]


@pytest.mark.django_db
def test_update_unowned_trip(call_endpoint, trip):
    someone_else, _ = get_or_create_user("bar")
    response = call_endpoint(someone_else, trip.trip_id, data={"title": "mwahaha"})
    assert 404 == response.status_code
    assert Trip.objects.get(pk=trip.pk).title != "mwahaha"
