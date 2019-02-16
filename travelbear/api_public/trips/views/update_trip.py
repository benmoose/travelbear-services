from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.parse import safe_parse_json
from common.response import error_response, success_response, validation_error_response
from db_layer.helpers import UpdateNotAllowed
from db_layer.trip import get_trip_by_id, update_trip

from ..models import Trip


@require_http_methods(["PATCH"])
@require_jwt_auth
def update_trip_handler(request, trip_id):
    db_trip = get_trip_by_id(request.user, trip_id)
    if not db_trip:
        return error_response(status=404)

    parsed_body = safe_parse_json(request.body)
    if parsed_body is None:
        return error_response(message="Could not parse JSON body")
    try:
        updated_trip = update_trip(request.user, db_trip, **parsed_body)
    except UpdateNotAllowed:
        return validation_error_response(["Cannot update one or more requested fields"])
    return success_response(data=Trip.from_db_model(updated_trip))
