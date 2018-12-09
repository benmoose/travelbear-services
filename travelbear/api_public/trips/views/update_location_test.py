import json

from django.test import Client
from django.urls import reverse
import pytest

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


@pytest.mark.django_db
def update_location_unowned_trip(call_endpoint):
    pass
