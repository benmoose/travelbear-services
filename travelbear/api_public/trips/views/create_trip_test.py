import json

import pytest
from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_json
from db_layer.trip.models import Trip
from db_layer.user import get_or_create_user

from .handlers import root_endpoint


def count_trips_in_db():
    return len(Trip.objects.all())


@pytest.fixture
def api_client():
    return Client(HTTP_TEST_USER_EXTERNAL_ID="foo")


@pytest.fixture
def endpoint_url():
    return reverse(root_endpoint)


@pytest.fixture
def call_create_trip_endpoint(api_client, endpoint_url):
    def _call_create_trip_endpoint(data=None):
        return api_client.post(
            endpoint_url, content_type="application/json", data=json.dumps(data)
        )

    return _call_create_trip_endpoint


@pytest.mark.django_db
def test_create_trip_bad_request(call_create_trip_endpoint):
    get_or_create_user(external_id="foo")

    assert 0 == count_trips_in_db()
    response = call_create_trip_endpoint(data={"title": 0})
    assert response.status_code == 400
    assert 0 == count_trips_in_db()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "data",
    argvalues=[
        dict(title="title"),
        dict(title="title", description=""),
        dict(title="title", description="Some description"),
        dict(title="title", description="Some description", tags=["t1", "t2"]),
    ],
)
def test_create_trip(call_create_trip_endpoint, data):
    get_or_create_user(external_id="foo")

    assert 0 == count_trips_in_db()
    response = call_create_trip_endpoint(data=data)
    assert response.status_code == 201
    assert 1 == count_trips_in_db()

    response_json = safe_parse_json(response.content)
    expected_response_data = {
        "trip_id": response_json.get("trip_id"),
        "created_on": response_json.get("created_on"),
        "title": data["title"],
    }
    if data.get("description", "") != "":
        expected_response_data["description"] = data["description"]
    if "tags" in data:
        expected_response_data["tags"] = data["tags"]

    assert response_json == expected_response_data
