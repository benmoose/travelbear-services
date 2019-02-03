import pytest

from common.test import count_models_in_db, no_models_in_db
from db_layer.trip import Place, create_trip, create_location
from db_layer.user import get_or_create_user
from .place_layer import create_place


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.fixture
def location(trip):
    return create_location(trip, "test location", 51, 0)


@pytest.mark.django_db
def test_create_place(location):
    assert no_models_in_db(Place)
    create_place(location, "test place", 51, 0)
    assert 1 == count_models_in_db(Place)
