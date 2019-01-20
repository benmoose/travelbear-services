import pytest

from db_layer.trip import TripMember, create_trip
from db_layer.user import get_or_create_user
from .trip_member_layer import (
    UserIsAlreadyMember,
    add_member_to_trip,
    get_members_of_trip,
    is_user_member_of_trip,
)


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
    not_a_member, _ = get_or_create_user("not-member-1")

    add_member_to_trip(member_1, trip)
    add_member_to_trip(member_2, trip)

    members_of_trip = [member.user for member in get_members_of_trip(trip)]
    assert 3 == len(members_of_trip)
    assert trip_owner in members_of_trip
    assert member_1 in members_of_trip
    assert member_2 in members_of_trip
    assert not_a_member not in members_of_trip


@pytest.mark.django_db
def test_is_user_member_of_trip(trip_owner, trip):
    somebody, _ = get_or_create_user("test-user")

    assert is_user_member_of_trip(trip_owner, trip) is True
    assert is_user_member_of_trip(somebody, trip) is False
