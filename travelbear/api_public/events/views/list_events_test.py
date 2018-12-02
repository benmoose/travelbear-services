import pytest

from django.test import Client
from django.urls import reverse

from db_layer.event import create_event
from db_layer.user import get_or_create_user
from .list_events import list_events


@pytest.fixture
def call_list_endpoint():
    url = reverse(list_events)
    client = Client()

    def _call_list_endpoint(user_id=None, data=None):
        return client.post(url, data=data, HTTP_MOCK_USER_SUB=user_id)

    return _call_list_endpoint


@pytest.fixture
def user_1():
    user, _ = get_or_create_user('auth0-id-1', 'user1@test.com')
    return user


@pytest.fixture
def user_2():
    user, _ = get_or_create_user('auth0-id-2', 'user2@test.com')
    return user


@pytest.fixture
def create_event_for_user():
    def _create_event_for_user(user):
        return create_event(
            created_by=user,
            title='title',
        )
    return _create_event_for_user


@pytest.mark.django_db
def test_list_events(call_list_endpoint, user_1, user_2, create_event_for_user):
    user_1_event = create_event_for_user(user_1)
    user_2_event = create_event_for_user(user_2)

    response = call_list_endpoint(user_id=user_1.auth0_id)
    assert response.status_code == 200
    # check correct events returned
