from datetime import datetime, timedelta

import pytest
import pytz

from db_layer.trip import TripMember, create_trip
from db_layer.user import get_or_create_user

from .trip_member_layer import (
    UserIsAlreadyMember,
    add_member_to_trip,
    get_members_of_trip,
    get_trips_for_user,
    is_user_member_of_trip,
)


@pytest.fixture
def time():
    return datetime(2019, 1, 1, tzinfo=pytz.UTC)


@pytest.fixture
def trip_owner():
    user, _ = get_or_create_user("user-1")
    return user


@pytest.fixture
def trip(trip_owner):
    return create_trip(trip_owner, "test-trip")


@pytest.mark.django_db
def test_add_member_to_trip(trip):
    somebody, _ = get_or_create_user("test-user")

    assert 1 == len(TripMember.objects.all())
    add_member_to_trip(somebody, trip, is_admin=False)
    assert 2 == len(TripMember.objects.all())

    object_in_db = TripMember.objects.get(user=somebody, trip=trip)
    assert object_in_db.user == somebody
    assert object_in_db.trip == trip
    assert object_in_db.is_admin is False


@pytest.mark.django_db
def test_add_duplicate_member_to_trip(trip):
    somebody, _ = get_or_create_user("test-user")

    add_member_to_trip(somebody, trip)
    with pytest.raises(UserIsAlreadyMember):
        add_member_to_trip(somebody, trip)

    object_in_db = TripMember.objects.get(user=somebody, trip=trip)
    assert object_in_db.is_admin is False


@pytest.mark.django_db
def test_get_members_of_trip(trip_owner, trip):
    member_1, _ = get_or_create_user("member-1")
    member_2, _ = get_or_create_user("member-2")
    member_3, _ = get_or_create_user("member-of-another-trip")

    other_trip = create_trip(trip_owner, "other-trip")
    add_member_to_trip(member_3, other_trip)

    add_member_to_trip(member_1, trip)
    add_member_to_trip(member_2, trip)

    members_of_trip = [member.user for member in get_members_of_trip(trip)]
    assert 3 == len(members_of_trip)
    assert {trip_owner, member_1, member_2} == set(members_of_trip)


@pytest.mark.django_db
def test_get_trips_for_user(time, django_assert_num_queries):
    one_h_ago = time - timedelta(hours=1)
    two_h_ago = time - timedelta(hours=2)

    user_1, _ = get_or_create_user("user-1")
    user_2, _ = get_or_create_user("user-2")

    trip_1 = create_trip_at_time(user_1, one_h_ago, title="trip-1")
    trip_2 = create_trip_at_time(user_2, two_h_ago, title="trip-2")
    create_trip_at_time(user_2, two_h_ago, title="trip-3", is_deleted=True)
    add_member_to_trip(user_1, trip_2)

    with django_assert_num_queries(1):
        get_trips_for_user(user_1)

    assert [trip_1, trip_2] == get_trips_for_user(user_1, ascending=False)
    assert [trip_2, trip_1] == get_trips_for_user(user_1, ascending=True)

    assert [trip_2] == get_trips_for_user(user_2)


@pytest.mark.django_db
def test_is_user_member_of_trip(trip_owner, trip):
    somebody, _ = get_or_create_user("test-user")

    assert is_user_member_of_trip(trip_owner, trip) is True
    assert is_user_member_of_trip(somebody, trip) is False


def create_trip_at_time(user, created_on, title="test-trip", is_deleted=False):
    trip = create_trip(user, title)
    trip.created_on = created_on
    trip.is_deleted = is_deleted
    trip.save()
    return trip
