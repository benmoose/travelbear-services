from datetime import datetime, timedelta
import pytest
import pytz

from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_json
from db_layer.trip import create_trip, Trip
from db_layer.user import get_or_create_user
from ..urls import root


@pytest.fixture
def call_list_endpoint():
    url = reverse(root)
    client = Client()

    def _call_list_endpoint(as_user=None, mock_current_time=None):
        if isinstance(mock_current_time, datetime):
            mock_current_time = mock_current_time.isoformat()
        return client.get(
            url,
            HTTP_TEST_USER_EXTERNAL_ID=as_user.external_id,
            HTTP_MOCK_CURRENT_TIME=mock_current_time,
        )

    return _call_list_endpoint


@pytest.fixture
def user_1():
    user, _ = get_or_create_user("auth0-id-1", "user1@test.com")
    return user


@pytest.fixture
def user_2():
    user, _ = get_or_create_user("auth0-id-2", "user2@test.com")
    return user


@pytest.mark.django_db
def test_list_trips(call_list_endpoint, user_1, user_2):
    create_trip(user_1, title="event 1", description="a description")
    create_trip(user_2, title="event 2")
    assert 2 == len(Trip.objects.all())

    response = call_list_endpoint(as_user=user_1)
    assert response.status_code == 200
    response_body = safe_parse_json(response.content)
    assert response_body == [
        {
            "title": "event 1",
            "description": "a description",
            "is_deleted": False,
            "trip_id": response_body[0].get("trip_id"),
        }
    ]
