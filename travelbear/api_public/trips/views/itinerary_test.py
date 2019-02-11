from datetime import datetime, timedelta

import pytest
from pytz import UTC
from django.test import Client
from django.urls import reverse

from db_layer.trip import create_trip, create_location, create_move, create_place
from db_layer.user import get_or_create_user

from .itinerary import itinerary_handler


def call_endpoint(user, trip_id):
    client = Client()
    url = reverse(itinerary_handler, kwargs={"trip_id": trip_id})
    return client.get(path=url, HTTP_TEST_USER_EXTERNAL_ID=user.external_id)


@pytest.fixture
def trip_start_time():
    return datetime(2019, 1, 1, tzinfo=UTC)


@pytest.fixture
def user():
    user, _ = get_or_create_user("test-user")
    return user


@pytest.fixture
def trip(user):
    return create_trip(user, "test trip")


@pytest.fixture
def location_1(trip):
    return create_location(trip, "location 1", 1, 1)


@pytest.fixture
def location_2(trip):
    return create_location(trip, "location 2", 2, 2)


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
        depart_time=trip_start_time + timedelta(days=1),
        arrive_time=trip_start_time + timedelta(days=1, hours=1),
        travel_method="flight",
    )


@pytest.fixture
def place_1(location_1, trip_start_time):
    return create_place(
        location=location_1,
        lat=2.1,
        lng=2.2,
        display_name="test place",
        start_time=trip_start_time + timedelta(hours=3),
    )


@pytest.mark.django_db
def test_itinerary_handler_bad_trip(user):
    random_uuid = "cfbaaf7d-f146-432b-95ca-7e423397347c"
    response = call_endpoint(user, random_uuid)
    assert response.status_code == 404


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
                        "type": "move_departure",
                        "event": {
                            "start_time": move_1.depart_time.isoformat(),
                            "travel_method": "flight",
                            "start_location": location_1.location_id,
                            "end_location": location_2.location_id,
                        },
                    },
                    {
                        "type": "move_arrival",
                        "event": {
                            "start_time": move_1.arrive_time.isoformat(),
                            "travel_method": "flight",
                            "start_location": location_1.location_id,
                            "end_location": location_2.location_id,
                        },
                    },
                    {
                        "type": "place",
                        "event": {
                            "location": location_1.location_id,
                            "start_time": place_1.start_time.isoformat(),
                            "lat": 2.1,
                            "lng": 2.2,
                            "display_name": "test place",
                        },
                    },
                ],
            },
            {
                "date": "2019-01-02",
                "events": [
                    {
                        "type": "move_departure",
                        "event": {
                            "start_time": move_2.depart_time.isoformat(),
                            "travel_method": "flight",
                            "start_location": location_2.location_id,
                            "end_location": location_1.location_id,
                        },
                    },
                    {
                        "type": "move_arrival",
                        "event": {
                            "start_time": move_2.arrive_time.isoformat(),
                            "travel_method": "flight",
                            "start_location": location_2.location_id,
                            "end_location": location_1.location_id,
                        },
                    },
                ],
            },
        ]
    } == response.json()
