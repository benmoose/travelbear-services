from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import error_response, success_response, validation_error_response
from common.parse import safe_parse_json
from db_layer.trip import get_trip_by_id, create_location
from ..models.location import Location


@require_http_methods(["POST"])
@require_jwt_auth
def create_location_handler(request, trip_id):
    db_trip = get_trip_by_id(request.user, trip_id)
    if not db_trip:
        return error_response(status=404)

    event = parse_location_from_request_body(request.body)
    if not event.is_valid:
        return validation_error_response(event.validation_errors)

    location = persist_location(db_trip, event)
    return success_response(status=201, data=location)


def parse_location_from_request_body(request_body):
    data = safe_parse_json(request_body)
    return Location.from_dict(data)


def persist_location(trip, event):
    location = create_location(
        trip=trip,
        display_name=event.display_name,
        lat=event.lat,
        lng=event.lng,
        google_place_id=event.google_place_id,
    )
    return Location.from_db_model(location)
