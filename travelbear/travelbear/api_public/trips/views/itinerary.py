import logging
from collections import defaultdict
from datetime import datetime
from typing import List, Optional

from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import error_response, success_response
from common.time import get_day_from_datetime
from db_layer.trip import (
    get_locations_for_trip,
    get_moves_departing_from_location,
    get_places_for_location,
    get_trip_by_id,
)
from db_layer.trip.models import Location, Trip

from ..models.move import MoveArrival, MoveDeparture
from ..models.place import Place

logger = logging.getLogger(__name__)

EVENT_TYPE_MAP = {
    Place: "place",
    MoveArrival: "travel.arrival",
    MoveDeparture: "travel.departure",
}


@require_http_methods(["GET"])
@require_jwt_auth
def itinerary_handler(request, trip_id):
    trip = get_trip_by_id(request.user, trip_id)
    if trip is None:
        return error_response(status=404)

    locations = get_locations_for_trip(trip)

    logger.info(
        "constructing itinerary for trip '%s' with %d locations",
        trip.trip_id,
        len(locations),
    )
    itinerary = get_itinerary_events_by_day_for_locations(locations)
    return success_response(data={"itinerary": to_response_shape(itinerary)})


def get_itinerary_events_by_day_for_locations(locations: List[Location]) -> dict:
    events = get_sorted_itinerary_events_for_locations(locations)
    return group_events_by_day(events)


def get_sorted_itinerary_events_for_locations(locations: List[Location]) -> list:
    items = []
    locations_by_pk = {location.pk: location for location in locations}
    for location in locations:
        places = [
            Place.from_db_model(model)
            for model in get_places_for_location(location, with_times_only=True)
        ]
        departures, arrivals = get_departures_and_arrivals_for_location(
            locations_by_pk, location
        )
        items.extend(places + departures + arrivals)

    return sorted(items, key=lambda i: get_time_from_item(i))


def get_departures_and_arrivals_for_location(
    locations_by_id: dict, location: Location
) -> (List[MoveDeparture], List[MoveArrival]):
    moves = get_moves_departing_from_location(location)
    departures = [
        MoveDeparture.from_db_model(
            db_model=move,
            start_location=locations_by_id[move.start_location_id],
            end_location=locations_by_id[move.end_location_id],
        )
        for move in moves
        if move.depart_time
    ]
    arrivals = [
        MoveArrival.from_db_model(
            db_model=move,
            start_location=locations_by_id[move.start_location_id],
            end_location=locations_by_id[move.end_location_id],
        )
        for move in moves
        if move.arrive_time
    ]
    return departures, arrivals


def group_events_by_day(items: list) -> dict:
    items_by_day = defaultdict(list)
    for item in items:
        day = get_day_from_datetime(get_time_from_item(item))
        items_by_day[day].append(item)
    return dict(items_by_day)


def get_time_from_item(item) -> Optional[datetime]:
    if isinstance(item, MoveDeparture):
        return item.depart_time
    if isinstance(item, MoveArrival):
        return item.arrive_time
    if isinstance(item, Place):
        return item.start_time
    return None


def to_response_shape(itinerary_by_day: dict) -> List[dict]:
    ordered_days = sorted(itinerary_by_day)
    return [
        {
            "date": day,
            "events": itinerary_events_to_response_events(itinerary_by_day[day]),
        }
        for day in ordered_days
    ]


def itinerary_events_to_response_events(events):
    return [itinerary_event_to_response_dict(event) for event in events]


def itinerary_event_to_response_dict(event) -> dict:
    return {"type": get_event_type(event), "event": event}


def get_event_type(item_model) -> str:
    """
    >>> get_event_type(Place())
    'place'
    >>> get_event_type(MoveArrival())
    'travel.arrival'
    >>> get_event_type(MoveDeparture())
    'travel.departure'
    """
    return EVENT_TYPE_MAP[item_model.__class__]
