from datetime import datetime
import pytest
import pytz
from uuid import uuid4

from common.test import count_models_in_db, no_models_in_db
from db_layer.user import get_or_create_user
from db_layer.utils import UpdateNotAllowed
from db_layer.trip import (
    Trip,
    TripMember,
    add_member_to_trip,
    create_trip,
    create_location,
    delete_trip,
    get_trips_created_by_user,
    get_trip_by_id,
    update_trip,
)


@pytest.mark.django_db
def test_create_trip():
    user, _ = get_or_create_user("foo")

    assert no_models_in_db(Trip)
    assert no_models_in_db(TripMember)
    trip = create_trip(user, title="test trip")
    assert 1 == count_models_in_db(Trip)
    assert 1 == count_models_in_db(TripMember)

    trip_in_db = Trip.objects.all()[0]
    assert trip == trip_in_db
    assert trip.created_by == trip_in_db.created_by  # only compares pk
    assert trip.title == trip_in_db.title

    trip_member_in_db = TripMember.objects.all()[0]
    assert trip_member_in_db.user == user
    assert trip_member_in_db.trip == trip_in_db
    assert trip_member_in_db.is_admin


@pytest.mark.django_db
def test_delete_trip():
    user, _ = get_or_create_user("trip-owner")
    trip = create_trip(user, title="test trip")
    assert not trip.is_deleted

    unrelated_user, _ = get_or_create_user("unrelated-user")
    assert delete_trip(unrelated_user, trip) is False
    trip.refresh_from_db()
    assert not trip.is_deleted

    trip_member, _ = get_or_create_user("trip-member")
    add_member_to_trip(trip_member, trip)
    assert delete_trip(trip_member, trip) is False
    trip.refresh_from_db()
    assert not trip.is_deleted

    success = delete_trip(user, trip)

    assert success
    trip.refresh_from_db()
    assert trip.is_deleted


@pytest.mark.django_db
def test_get_trips_for_user():
    user_1, _ = get_or_create_user("1")
    someone_else, _ = get_or_create_user("2")

    _ = create_trip(someone_else, title="other secret trip we shouldn't see")

    trip_1 = create_trip(user_1, title="trip 1")
    trip_1.save_with_times(created_on=datetime(2018, 1, 1, tzinfo=pytz.UTC))
    trip_2 = create_trip(user_1, title="trip 2")
    trip_2.save_with_times(created_on=datetime(2018, 1, 2, tzinfo=pytz.UTC))

    trips = get_trips_created_by_user(user=user_1)
    assert trips == [trip_2, trip_1]
    trips = get_trips_created_by_user(user=user_1, ascending=True)
    assert trips == [trip_1, trip_2]

    trip_1.is_deleted = True
    trip_1.save()
    assert [trip_2] == get_trips_created_by_user(user=user_1)
    assert [trip_2, trip_1] == get_trips_created_by_user(
        user=user_1, include_deleted=True
    )


@pytest.mark.django_db
def test_get_trip_by_id(django_assert_num_queries):
    trip_owner, _ = get_or_create_user("trip-owner")
    trip = create_trip(trip_owner, "test trip")
    location = create_location(trip, "location", lat=4, lng=2)

    trip_member, _ = get_or_create_user("trip-member")
    add_member_to_trip(trip_member, trip)

    for user in [trip_owner, trip_member]:
        with django_assert_num_queries(2):
            retrieved_trip = get_trip_by_id(user, trip.trip_id)
            assert retrieved_trip.pk == trip.pk
            assert retrieved_trip.locations == [location]

    assert get_trip_by_id(trip_owner, str(uuid4())) is None

    someone_else, _ = get_or_create_user("someone-else")
    assert get_trip_by_id(someone_else, uuid4()) is None


@pytest.mark.django_db
def test_update_trip():
    user, _ = get_or_create_user("foo")
    original_trip = create_trip(
        user, title="bad title", description="bad desc", tags=["a", "b"]
    )
    update_1 = update_trip(
        user,
        original_trip,
        title="good title",
        description="good desc",
        tags=["1", "2"],
    )

    assert original_trip.pk == update_1.pk
    assert update_1.title == "good title"
    assert update_1.description == "good desc"
    assert update_1.tags == ["1", "2"]

    update_2 = update_trip(user, update_1, description="even better desc", tags=[])
    assert original_trip.pk == update_2.pk
    assert update_2.title == "good title"
    assert update_2.description == "even better desc"
    assert update_2.tags == []

    assert 1 == len(Trip.objects.all())


@pytest.mark.django_db
def test_update_trip_member_of():
    trip_owner, _ = get_or_create_user("foo")
    trip_member, _ = get_or_create_user("bar")
    trip = create_trip(trip_owner, title="trip 1")
    add_member_to_trip(trip_member, trip)

    update_trip(trip_member, trip, title="another name")
    trip.refresh_from_db()
    assert trip.title == "another name"


@pytest.mark.django_db
def test_update_trip_not_allowed_fields():
    user, _ = get_or_create_user("foo")
    trip = create_trip(user, title="original title")
    with pytest.raises(UpdateNotAllowed):
        update_trip(
            user, trip, title="updated title", foo="wtf is this field", bar=[1, 2, 3]
        )

    trip.refresh_from_db()
    assert trip.title == "original title"


@pytest.mark.django_db
def test_update_other_users_trip():
    user, _ = get_or_create_user("foo")
    someone_else, _ = get_or_create_user("bar")
    trip = create_trip(user, title="unspoilt")

    with pytest.raises(Exception):
        update_trip(someone_else, trip, title="mwahaha")

    trip.refresh_from_db()
    assert trip.title == "unspoilt"
