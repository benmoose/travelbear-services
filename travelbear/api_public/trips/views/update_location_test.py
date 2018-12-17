import json

from django.test import Client
from django.urls import reverse
import pytest

from db_layer.trip import create_trip, create_location
from db_layer.user import get_or_create_user
from .update_location import update_location_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def call_endpoint(api_client):
    def _call_endpoint(user, trip, location, data=None):
        url = reverse(
            update_location_handler,
            kwargs={"trip_id": trip.trip_id, "location_id": location.location_id},
        )
        return api_client.patch(
            url, data=json.dumps(data), HTTP_TEST_USER_EXTERNAL_ID=user.external_id
        )

    return _call_endpoint


@pytest.fixture
def user():
    user, _ = get_or_create_user(external_id="test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, title="test trip")


@pytest.mark.django_db
def test_update_location_unowned_trip(call_endpoint, trip):
    someone_else, _ = get_or_create_user(external_id="someone-else")
    location = create_location(trip, display_name="test location", lat=0, lng=0)

    response = call_endpoint(someone_else, trip, location, data={"title": "mwahaha"})
    assert response.status_code == 404

    location.refresh_from_db()
    assert location.display_name != "mwahaha"


@pytest.mark.django_db
def test_update_location(call_endpoint, user, trip):
    location = create_location(
        trip, display_name="London", lat=51, lng=-0.12, google_place_id="google-id-1"
    )
    response = call_endpoint(
        user, trip, location, data={"display_name": "Ilkley", "lat": 53, "lng": -1.8}
    )
    assert response.status_code == 200
    response_body = json.loads(response.content)
    assert response_body == {
        "location_id": str(location.location_id),
        "display_name": "Ilkley",
        "google_place_id": "google-id-1",
        "lat": 53,
        "lng": -1.8,
    }


@pytest.mark.django_db
def test_update_invalid_fields(call_endpoint, user, trip):
    location = create_location(trip, display_name="test location", lat=0, lng=0)
    response = call_endpoint(user, trip, location, data={
        "is_deleted": True,
        "foo": "bar",
        "lat": 99.99,
    })
    assert response.status_code == 400
    assert "Cannot update fields:" in str(response.content)

    location.refresh_from_db()
    assert location.lat == 0
