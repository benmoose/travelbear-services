from datetime import datetime
import pytest
import pytz
from uuid import uuid4

from db_layer.user import get_or_create_user
from db_layer.utils import UpdateNotAllowed
from db_layer.trip import (
    Trip,
    TripMember,
    create_trip,
    create_location,
    delete_trip,
    get_trips_created_by_user,
    get_trip_by_id,
    update_trip,
)


@pytest.fixture
def create_user():
    def _create_user(external_id):
        user, _ = get_or_create_user(external_id, f"{external_id}@test.com")
        return user

    return _create_user


@pytest.mark.django_db
def test_create_trip(create_user):
    user = create_user("foo")

    assert 0 == len(Trip.objects.all())
    assert 0 == len(TripMember.objects.all())
    trip = create_trip(user, title="test trip")
    assert 1 == len(Trip.objects.all())
    assert 1 == len(TripMember.objects.all())

    trip_in_db = Trip.objects.all()[0]
    assert trip == trip_in_db
    assert trip.created_by == trip_in_db.created_by  # only compares pk
    assert trip.title == trip_in_db.title

    trip_member_in_db = TripMember.objects.all()[0]
    assert trip_member_in_db.user == user
    assert trip_member_in_db.trip == trip_in_db
    assert trip_member_in_db.is_admin


@pytest.mark.django_db
def test_delete_trip(create_user):
    user = create_user("test-user")
    someone_else = create_user("someone-else")

    trip = create_trip(user, title="test trip")
    assert not trip.is_deleted

    assert delete_trip(someone_else, trip) is None

    returned_trip = delete_trip(user, trip)

    assert returned_trip.pk == trip.pk
    assert returned_trip.is_deleted
    trip.refresh_from_db()
    assert trip.is_deleted


@pytest.mark.django_db
def test_get_trips_for_user(create_user):
    user_1 = create_user("1")
    someone_else = create_user("2")

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
def test_get_trip_by_id(django_assert_num_queries, create_user):
    user = create_user("test-user")
    trip = create_trip(user, "test trip")
    location = create_location(trip, "location", lat=4, lng=2)

    with django_assert_num_queries(2):
        trip = get_trip_by_id(user, trip.trip_id)
        assert trip.title == "test trip"
        assert trip.locations == [location]

    assert get_trip_by_id(user, uuid4()) is None

    someone_else = create_user("someone-else")
    assert get_trip_by_id(someone_else, uuid4()) is None


@pytest.mark.django_db
def test_update_trip(create_user):
    user = create_user("foo")
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
def test_update_trip_not_allowed_fields(create_user):
    user = create_user("foo")
    trip = create_trip(user, title="original title")
    with pytest.raises(UpdateNotAllowed):
        update_trip(
            user, trip, title="updated title", foo="wtf is this field", bar=[1, 2, 3]
        )

    trip.refresh_from_db()
    assert trip.title == "original title"


@pytest.mark.django_db
def test_update_other_users_trip(create_user):
    user = create_user("foo")
    someone_else = create_user("bar")
    trip = create_trip(user, title="unspoilt")

    with pytest.raises(Exception):
        update_trip(someone_else, trip, title="mwahaha")

    trip.refresh_from_db()
    assert trip.title == "unspoilt"
