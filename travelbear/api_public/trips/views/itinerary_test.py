import pytest
from django.test import Client
from django.urls import reverse

from db_layer.user import get_or_create_user

from .itinerary import itinerary_handler


def call_endpoint(user, trip_id):
    client = Client()
    url = reverse(itinerary_handler, kwargs={"trip_id": trip_id})
    return client.get(path=url, HTTP_TEST_USER_EXTERNAL_ID=user.external_id)


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.mark.django_db
def test_itinerary_handler_bad_trip(user):
    random_uuid = "cfbaaf7d-f146-432b-95ca-7e423397347c"
    response = call_endpoint(user, random_uuid)
    assert response.status_code == 404
