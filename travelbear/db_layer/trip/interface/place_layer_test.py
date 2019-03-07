import pytest

from common.test import count_models_in_db, no_models_in_db
from db_layer.trip import create_location, create_trip
from db_layer.user import get_or_create_user

from ..models import Place
from .place_layer import create_place, delete_place, update_place


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
    p = create_place(location, "test place", lat=51, lng=0)

    assert isinstance(p, Place)
    assert 1 == count_models_in_db(Place)
    assert p.pk == Place.objects.all()[0].pk


@pytest.mark.django_db
def test_delete_place(location):
    place = create_place(location, "test place", lat=51, lng=0)
    assert place.is_deleted is False

    delete_place(place)
    place.refresh_from_db()
    assert place.is_deleted


@pytest.mark.django_db
def test_update_place(location):
    place = create_place(location, display_name="test place", lat=51, lng=0)
    update_place(
        place, display_name="cool new name", lat=100, display_address="Old Street"
    )

    place.refresh_from_db()
    assert place.display_name == "cool new name"
    assert place.lat == 100
    assert place.lng == 0
    assert place.display_address == "Old Street"
