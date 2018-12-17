import json

from django.urls import reverse
from django.test import Client
import pytest

from db_layer.trip import create_trip, Trip
from db_layer.user import get_or_create_user
from .handlers import trip_id_endpoint


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
def trip(user):
    return create_trip(
        user, title="some title", description="some desc", tags=["roadtrip"]
    )


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
    response_body = json.loads(response.content)
    assert response_body == {
        "trip_id": str(trip.trip_id),
        "title": "new title",
        "description": "some desc",
        "tags": ["camping", "mountains"],
        "is_deleted": False,
    }

    response = call_endpoint(
        trip.created_by, trip.trip_id, data={"is_deleted": True, "title": "foo"}
    )
    assert 400 == response.status_code
    response_body = json.loads(response.content)
    assert Trip.objects.get(pk=trip.pk).is_deleted is False
    assert Trip.objects.get(pk=trip.pk).title != "foo"
    assert response_body["validation_errors"] == [
        "Cannot update one or more requested fields"
    ]


@pytest.mark.django_db
def test_update_unowned_trip(call_endpoint, trip):
    someone_else, _ = get_or_create_user("bar")
    response = call_endpoint(someone_else, trip.trip_id, data={"title": "mwahaha"})
    assert 404 == response.status_code
    assert Trip.objects.get(pk=trip.pk).title != "mwahaha"
