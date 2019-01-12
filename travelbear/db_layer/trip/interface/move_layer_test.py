import pytest

from db_layer.trip import Move
from db_layer.user import get_or_create_user
from .location_layer import create_location
from .trip_layer import create_trip
from .move_layer import create_move, delete_move, get_move_by_move_id


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(created_by=user, title="test trip")


@pytest.fixture
def location_1(trip):
    return create_location(trip, display_name="London", lat=51, lng=0)


@pytest.fixture
def location_2(trip):
    return create_location(trip, display_name="Ilkley", lat=53, lng=1.8)


@pytest.mark.django_db
def test_create_move(location_1, location_2):
    assert 0 == len(Move.objects.all())
    move = create_move(location_1, location_2, "plane")
    assert 1 == len(Move.objects.all())

    move_in_db = Move.objects.all()[0]
    assert move_in_db.pk == move.pk
    assert move_in_db.start_location == location_1
    assert move_in_db.end_location == location_2
    assert move_in_db.travel_method == "plane"


@pytest.mark.django_db
def test_reverse_lookup(location_1, location_2):
    move = create_move(location_1, location_2)
    create_move(location_2, location_1)

    assert list(location_1.start_location_for.all()) == [move]
    assert list(location_2.end_location_for.all()) == [move]


@pytest.mark.django_db
def test_delete_move(location_1, location_2):
    move = create_move(location_1, location_2)
    assert not move.is_deleted

    returned_move = delete_move(move)
    assert returned_move.pk == move.pk
    assert returned_move.is_deleted
    move.refresh_from_db()
    assert move.is_deleted


@pytest.mark.django_db
def test_get_move_by_move_id(user, location_1, location_2):
    db_move = create_move(location_1, location_2)

    retrieved_move = get_move_by_move_id(user, db_move.move_id)
    assert retrieved_move.pk == db_move.pk

    someone_else, _ = get_or_create_user("someone-else")
    assert get_move_by_move_id(someone_else, db_move.move_id) is None
