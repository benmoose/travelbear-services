from django.test import Client
from django.urls import reverse
import pytest

from db_layer.trip import create_trip, create_location, create_move
from db_layer.user import get_or_create_user
from .delete_move import delete_move_handler


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture
def get_url():
    def _get_url(move_id):
        return reverse(delete_move_handler, kwargs={"move_id": move_id})

    return _get_url


@pytest.fixture
def call_endpoint(api_client, get_url):
    def _call_endpoint(user, move_id):
        url = get_url(move_id)
        headers = {"HTTP_TEST_USER_EXTERNAL_ID": user.external_id} if user else {}
        return api_client.delete(url, content_type="application/json", **headers)

    return _call_endpoint


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip", "test description")


@pytest.fixture
def location_1(trip):
    return create_location(trip, "location one", lat=51, lng=0)


@pytest.fixture
def location_2(trip):
    return create_location(trip, "location two", lat=51, lng=0)


@pytest.fixture
def move(location_1, location_2):
    return create_move(location_1, location_2)


@pytest.mark.django_db
def test_delete_move_that_does_not_exist(user, call_endpoint):
    response = call_endpoint(user=user, move_id="i-dont-exist")
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_move(user, call_endpoint, move):
    move_id = move.move_id
    response = call_endpoint(
        user=user,
        move_id=move_id,
    )
    assert response.status_code == 204
    move.refresh_from_db()
    assert move.is_deleted


@pytest.mark.django_db
def test_delete_other_users_move(user, call_endpoint):
    someone_else, _ = get_or_create_user("someone-else")
    someone_elses_trip = create_trip(created_by=someone_else, title="Foo")
    someone_elses_location_1 = create_location(someone_elses_trip, "foo", 51, 0)
    someone_elses_location_2 = create_location(someone_elses_trip, "bar", 51, 0)
    someone_elses_move = create_move(someone_elses_location_1, someone_elses_location_2)

    response = call_endpoint(
        user=user,
        move_id=someone_elses_move.move_id,
    )
    assert response.status_code == 404
    someone_elses_move.refresh_from_db()
    assert someone_elses_move.is_deleted is False
