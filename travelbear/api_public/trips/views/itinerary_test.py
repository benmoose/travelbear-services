from datetime import datetime, timedelta

import pytest
from django.test import Client
from django.urls import reverse
from pytz import utc

from common.time import get_day_from_datetime
from db_layer.trip import create_location, create_move, create_place, create_trip
from db_layer.user import get_or_create_user

from ..models.move import MoveArrival, MoveDeparture
from ..models.place import Place
from .itinerary import (
    get_departures_and_arrivals_for_location,
    get_itinerary_events_by_day_for_locations,
    group_events_by_day,
    itinerary_handler,
)


def call_endpoint(user, trip_id):
    client = Client()
    url = reverse(itinerary_handler, kwargs={"trip_id": trip_id})
    return client.get(path=url, HTTP_TEST_USER_EXTERNAL_ID=user.external_id)


@pytest.fixture
def trip_start_time():
    return datetime(2019, 1, 1, tzinfo=utc)


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.fixture
def location_1(trip):
    return create_location(trip, "location 1", 1.1, 1.2, google_place_id="goog123")


@pytest.fixture
def location_2(trip):
    return create_location(trip, "location 2", 2.1, 2.2)


@pytest.fixture
def move_1(location_1, location_2, trip_start_time):
    return create_move(
        start_location=location_1,
        end_location=location_2,
        depart_time=trip_start_time,
        arrive_time=trip_start_time + timedelta(hours=1),
        travel_method="flight",
    )


@pytest.fixture
def move_2(location_1, location_2, trip_start_time):
    return create_move(
        start_location=location_2,
        end_location=location_1,
        depart_time=trip_start_time + timedelta(days=1, hours=8),
        arrive_time=trip_start_time + timedelta(days=1, hours=10),
        travel_method="flight",
    )


@pytest.fixture
def place_1(location_2, trip_start_time):
    return create_place(
        location=location_2,
        lat=3.1,
        lng=3.2,
        display_name="test place",
        start_time=trip_start_time + timedelta(days=1, hours=2),
    )


@pytest.mark.django_db
def test_itinerary_handler_bad_trip(user):
    random_uuid = "cfbaaf7d-f146-432b-95ca-7e423397347c"
    response = call_endpoint(user, random_uuid)
    assert response.status_code == 404


@pytest.mark.django_db
def test_itinerary_handler_no_events(user, trip):
    response = call_endpoint(user, trip.trip_id)
    assert 200 == response.status_code
    assert {"itinerary": []} == response.json()


@pytest.mark.django_db
def test_get_itinerary_events_by_day_for_locations_num_db_queries(
    django_assert_num_queries,
    user,
    trip,
    location_1,
    location_2,
    move_1,
    move_2,
    place_1,
):
    # expect 2 queries per location
    with django_assert_num_queries(2 * 2):
        get_itinerary_events_by_day_for_locations([location_1, location_2])


@pytest.mark.django_db
def test_itinerary_handler(user, trip, location_1, location_2, move_1, move_2, place_1):
    # unbooked places don't show on itinerary
    _ = create_place(location_2, "unbooked", 51, 0)

    response = call_endpoint(user, trip.trip_id)

    assert 200 == response.status_code
    assert {
        "itinerary": [
            {
                "date": "2019-01-01",
                "events": [
                    {
                        "type": "travel.departure",
                        "event": {
                            "move_id": str(move_1.move_id),
                            "start_location_id": str(location_1.location_id),
                            "end_location_id": str(location_2.location_id),
                            "travel_method": "flight",
                            "depart_time": "2019-01-01T00:00:00Z",
                            "arrive_time": "2019-01-01T01:00:00Z",
                        },
                    },
                    {
                        "type": "travel.arrival",
                        "event": {
                            "move_id": str(move_1.move_id),
                            "start_location_id": str(location_1.location_id),
                            "end_location_id": str(location_2.location_id),
                            "travel_method": "flight",
                            "depart_time": "2019-01-01T00:00:00Z",
                            "arrive_time": "2019-01-01T01:00:00Z",
                        },
                    },
                ],
            },
            {
                "date": "2019-01-02",
                "events": [
                    {
                        "type": "place",
                        "event": {
                            "place_id": str(place_1.place_id),
                            "location_id": str(location_2.location_id),
                            "display_name": "test place",
                            "coords": [3.1, 3.2],
                            "start_time": "2019-01-02T02:00:00Z",
                        },
                    },
                    {
                        "type": "travel.departure",
                        "event": {
                            "move_id": str(move_2.move_id),
                            "start_location_id": str(location_2.location_id),
                            "end_location_id": str(location_1.location_id),
                            "travel_method": "flight",
                            "depart_time": "2019-01-02T08:00:00Z",
                            "arrive_time": "2019-01-02T10:00:00Z",
                        },
                    },
                    {
                        "type": "travel.arrival",
                        "event": {
                            "move_id": str(move_2.move_id),
                            "start_location_id": str(location_2.location_id),
                            "end_location_id": str(location_1.location_id),
                            "travel_method": "flight",
                            "depart_time": "2019-01-02T08:00:00Z",
                            "arrive_time": "2019-01-02T10:00:00Z",
                        },
                    },
                ],
            },
        ]
    } == response.json()


@pytest.mark.django_db
def test_get_itinerary_events_by_day_for_locations(
    location_1, location_2, move_1, move_2, place_1
):
    _ = create_place(location_1, "unbooked", 51, 0, start_time=None)

    assert {
        get_day_from_datetime(move_1.depart_time): [
            MoveDeparture.from_db_model(move_1, location_1, location_2),
            MoveArrival.from_db_model(move_1, location_1, location_2),
        ],
        get_day_from_datetime(move_2.depart_time): [
            Place.from_db_model(place_1),
            MoveDeparture.from_db_model(move_2, location_2, location_1),
            MoveArrival.from_db_model(move_2, location_2, location_1),
        ],
    } == get_itinerary_events_by_day_for_locations([location_1, location_2])


@pytest.mark.django_db
def test_group_items_by_day(location_1, location_2, move_1, move_2, place_1):
    move_1_model = MoveDeparture.from_db_model(move_1, location_1, location_2)
    move_2_model = MoveDeparture.from_db_model(move_2, location_2, location_1)
    place_1_model = Place.from_db_model(place_1)

    assert {} == group_events_by_day([])

    assert {
        get_day_from_datetime(move_1.depart_time): [move_1_model],
        get_day_from_datetime(move_2.depart_time): [place_1_model, move_2_model],
    } == group_events_by_day([move_1_model, place_1_model, move_2_model])


@pytest.mark.django_db
def test_get_departures_and_arrivals_for_location_makes_one_query(
    django_assert_num_queries,
    user,
    trip,
    location_1,
    location_2,
    move_1,
    move_2,
    place_1,
):
    locations_by_id = {location.id: location for location in [location_1, location_2]}
    with django_assert_num_queries(1):
        get_departures_and_arrivals_for_location(locations_by_id, location_1)
