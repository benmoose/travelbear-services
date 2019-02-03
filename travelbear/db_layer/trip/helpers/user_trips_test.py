import pytest

from db_layer.user import get_or_create_user
from db_layer.trip import create_trip, add_member_to_trip
from .user_trips import user_trips_qs


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.mark.django_db
def test_user_trips_qs(user):
    trip_1 = create_trip(user, "trip 1")
    trip_2 = create_trip(user, "trip 2")

    someone_else, _ = get_or_create_user("someone-else")
    trip_3 = create_trip(someone_else, "trip 3")
    add_member_to_trip(user, trip_3)

    _ = create_trip(someone_else, "unrelated trip")

    assert set(user_trips_qs(user)) == {trip_1, trip_2, trip_3}
