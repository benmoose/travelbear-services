from datetime import datetime, timedelta
import pytest
import pytz

from django.test import Client
from django.urls import reverse

from common.parse import safe_parse_json
from db_layer.event import create_event, Event
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
            HTTP_MOCK_USER_SUB=as_user.external_id,
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
def test_list_events(call_list_endpoint, user_1, user_2):
    current_time = datetime(2018, 1, 1, tzinfo=pytz.UTC)

    create_event(user_1, title="event 1", start_time=current_time + timedelta(hours=1))
    create_event(user_2, title="event 2", start_time=current_time + timedelta(hours=1))

    assert 2 == len(Event.objects.all())
    response = call_list_endpoint(as_user=user_1, mock_current_time=current_time)
    assert response.status_code == 200
    response_body = safe_parse_json(response.content)
    assert response_body == [
        {
            "title": "event 1",
            "description": "",
            "start_time": "2018-01-01T01:00:00Z",
            "display_address": "",
            "approx_display_address": "",
            "protect_real_address": True,
            "is_deleted": False,
        }
    ]
