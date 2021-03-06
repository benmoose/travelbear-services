from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
import pytz

from db_layer.helpers import UpdateNotAllowed
from db_layer.trip import create_place
from db_layer.user import get_or_create_user

from ..models import Location
from .location_layer import (
    create_location,
    delete_location,
    get_location_by_id,
    get_locations_for_trip,
    get_places_for_location,
    update_location,
)
from .trip_layer import create_trip


@pytest.fixture
def user():
    user, _ = get_or_create_user(external_id="test-id")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, title="test trip")


@pytest.mark.django_db
def test_create_location(trip):
    assert 0 == len(Location.objects.all())
    create_location(
        trip,
        display_name="London",
        lat=51.0056459234001,
        lng=0.00000145,
        google_place_id="foobar",
    )
    assert 1 == len(Location.objects.all())

    location_in_db = Location.objects.all()[0]
    assert location_in_db.display_name == "London"
    assert location_in_db.lat == Decimal("51.005646")  # truncated to 6 dp
    assert location_in_db.lng == Decimal("0.000001")
    assert location_in_db.google_place_id == "foobar"


@pytest.mark.django_db
def test_delete_location(trip):
    location = create_location(trip, display_name="London", lat=51, lng=0)
    assert not location.is_deleted

    returned_location = delete_location(location)

    assert returned_location.pk == location.pk
    assert returned_location.is_deleted
    location.refresh_from_db()
    assert location.is_deleted


@pytest.mark.django_db
def test_get_location_by_id(user, trip):
    location_in_db = create_location(trip, "test location", lat=0, lng=0)

    retrieved_location = get_location_by_id(user, location_in_db.location_id)
    assert retrieved_location.pk == location_in_db.pk
    assert retrieved_location.display_name == "test location"

    assert get_location_by_id(user, uuid4()) is None


@pytest.mark.django_db
def test_can_not_get_unowned_locations(trip):
    someone_else, _ = get_or_create_user("someone-else")
    location_1 = create_location(trip, "test location", lat=0, lng=0)
    assert get_location_by_id(someone_else, location_1.location_id) is None


@pytest.mark.django_db
def test_update_location(trip):
    original_location = create_location(
        trip, display_name="original name", lat=51, lng=1
    )
    update_1 = update_location(
        original_location,
        display_name="new name",
        lat=52,
        lng=2,
        google_place_id="new field",
    )

    assert original_location.pk == update_1.pk
    assert update_1.display_name == "new name"
    assert update_1.google_place_id == "new field"
    assert update_1.lat == 52
    assert update_1.lng == 2


@pytest.mark.django_db
def test_get_locations_for_trip(trip):
    assert [] == get_locations_for_trip(trip)

    location_1 = create_location(trip, "location-1", 51, 0)
    location_2 = create_location(trip, "location-1", 51, 0)

    assert {location_1, location_2} == set(get_locations_for_trip(trip))


@pytest.mark.django_db
def test_update_location_not_allowed_fields(trip):
    location = create_location(trip, display_name="location", lat=51, lng=1)
    with pytest.raises(UpdateNotAllowed):
        update_location(location, is_deleted=True)


@pytest.mark.django_db
def test_get_locations_for_trip(trip):
    assert [] == get_locations_for_trip(trip)

    location_1 = create_location(trip, "location-1", 51, 0)
    location_2 = create_location(trip, "location-1", 51, 0)

    assert {location_1, location_2} == set(get_locations_for_trip(trip))


@pytest.mark.django_db
def test_get_places_for_location(trip):
    location = create_location(trip, "location", 51, 0)
    assert [] == get_places_for_location(location)

    earlier_time = datetime(2019, 1, 1, tzinfo=pytz.UTC)
    later_time = earlier_time + timedelta(hours=1)

    place_1 = create_place(location, "place 1", 51, 0, start_time=earlier_time)
    place_2 = create_place(location, "place 2", 51, 0, start_time=later_time)
    place_3 = create_place(location, "place 2", 51, 0, start_time=None)

    assert [place_1, place_2, place_3] == get_places_for_location(location)

    place_1.is_deleted = True
    place_1.save()

    assert [place_2] == get_places_for_location(location, with_times_only=True)
