from datetime import datetime
import pytest
import pytz

from db_layer.user import get_or_create_user
from ..models.trip import Trip
from .trip_layer import create_trip, list_trips_for_user


@pytest.fixture
def create_user():
    def _create_user(user_id):
        user, _ = get_or_create_user(user_id, f"{user_id}@test.com")
        return user

    return _create_user


@pytest.mark.django_db
def test_create_trip(create_user):
    user = create_user("foo")

    assert 0 == len(Trip.objects.all())
    trip = create_trip(created_by=user, title="test trip")
    assert 1 == len(Trip.objects.all())

    trip_in_db = Trip.objects.all()[0]
    assert trip == trip_in_db
    assert trip.created_by == trip_in_db.created_by  # only compares pk
    assert trip.title == trip_in_db.title


@pytest.mark.django_db
def test_list_trips_for_user(create_user):
    user_1 = create_user("1")
    someone_else = create_user("2")

    _ = create_trip(created_by=someone_else, title="other secret trip we shouldn't see")

    trip_1 = create_trip(created_by=user_1, title="trip 1")
    trip_1.save_with_times(created_on=datetime(2018, 1, 1, tzinfo=pytz.UTC))
    trip_2 = create_trip(created_by=user_1, title="trip 2")
    trip_2.save_with_times(created_on=datetime(2018, 1, 2, tzinfo=pytz.UTC))

    trips = list_trips_for_user(user=user_1)
    assert trips == [trip_2, trip_1]
    trips = list_trips_for_user(user=user_1, ascending=True)
    assert trips == [trip_1, trip_2]

    trip_1.is_deleted = True
    trip_1.save()
    assert [trip_2] == list_trips_for_user(user=user_1)
    assert [trip_2, trip_1] == list_trips_for_user(user=user_1, include_deleted=True)
