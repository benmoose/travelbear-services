from datetime import datetime, timedelta

import pytest
from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_rfc3339
from common.test import count_models_in_db
from db_layer.trip import add_member_to_trip, create_trip
from db_layer.trip.models import Trip
from db_layer.user import get_or_create_user

from .handlers import root_endpoint


@pytest.fixture
def time():
    return safe_parse_rfc3339("2019-01-01T10:00:00Z")


@pytest.fixture
def user_1():
    user, _ = get_or_create_user("auth0-id-1", "user1@test.com")
    return user


@pytest.fixture
def user_2():
    user, _ = get_or_create_user("auth0-id-2", "user2@test.com")
    return user


@pytest.fixture
def user_1_trip(time, user_1):
    one_h_ago = time - timedelta(hours=1)
    return create_trip_at_time(user_1, one_h_ago, title="event 1", description="rick")


@pytest.fixture
def user_2_trip(time, user_2):
    two_h_ago = time - timedelta(hours=2)
    return create_trip_at_time(user_2, two_h_ago, title="event 2", description="summer")


@pytest.mark.django_db
def test_list_trips(user_1, user_1_trip, user_2_trip):
    assert 2 == count_models_in_db(Trip)

    response = call_list_endpoint(as_user=user_1)
    assert response.status_code == 200
    assert [
        {
            "title": "event 1",
            "description": "rick",
            "trip_id": str(user_1_trip.trip_id),
            "created_on": "2019-01-01T09:00:00Z",
        }
    ] == response.json()

    # trips user is member of should be returned
    add_member_to_trip(user_1, user_2_trip)

    response = call_list_endpoint(as_user=user_1)
    assert response.status_code == 200
    assert [
        {
            "title": "event 1",
            "description": "rick",
            "trip_id": str(user_1_trip.trip_id),
            "created_on": "2019-01-01T09:00:00Z",
        },
        {
            "title": "event 2",
            "description": "summer",
            "trip_id": str(user_2_trip.trip_id),
            "created_on": "2019-01-01T08:00:00Z",
        },
    ] == response.json()


def call_list_endpoint(as_user=None, mock_current_time=None):
    url = reverse(root_endpoint)
    client = Client()

    if isinstance(mock_current_time, datetime):
        mock_current_time = mock_current_time.isoformat()

    return client.get(
        url,
        HTTP_TEST_USER_EXTERNAL_ID=as_user.external_id,
        HTTP_MOCK_CURRENT_TIME=mock_current_time,
    )


def create_trip_at_time(created_by, created_on, title, description):
    trip = create_trip(created_by, title=title, description=description)
    trip.created_on = created_on
    trip.save()
    return trip
