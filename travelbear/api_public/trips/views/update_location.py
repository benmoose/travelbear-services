from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import error_response, success_response, validation_error_response
from common.parse import safe_parse_json
from db_layer.helpers import UpdateNotAllowed
from db_layer.trip import get_trip_by_id, update_location
from ..models import Location


@require_http_methods(["PATCH"])
@require_jwt_auth
def update_location_handler(request, trip_id, location_id):
    db_trip = get_trip_by_id(request.user, trip_id)
    if not db_trip:
        return error_response(status=404)

    location = get_location_by_id_from_trip(db_trip, location_id)
    if not location:
        return error_response(status=404)

    request_body = safe_parse_json(request.body)
    updated_location, error = update_location_from_dict(
        request.user, location, request_body
    )
    if error:
        return validation_error_response([error])

    return success_response(data=Location.from_db_model(updated_location))


def get_location_by_id_from_trip(trip, location_id):
    for location in trip.locations:
        if str(location.location_id) == location_id:
            return location
    return None


def update_location_from_dict(user, location, data):
    try:
        return update_location(user, location, **data), None
    except UpdateNotAllowed as e:
        return None, str(e)
