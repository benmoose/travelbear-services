from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.parse import safe_parse_json
from common.response import success_response, validation_error_response
from db_layer.trip import create_trip

from ..models.trip import Trip


@require_http_methods(["POST"])
@require_jwt_auth
def create_trip_handler(request):
    trip = get_trip_from_request_body(request.body)
    if not trip.is_valid:
        return validation_error_response(trip.validation_errors)

    created_trip = persist_trip(trip, created_by=request.user)
    return success_response(status=201, data=created_trip)


def get_trip_from_request_body(request_body):
    parsed_body = safe_parse_json(request_body) or {}
    return Trip.from_dict(parsed_body)


def persist_trip(trip, created_by):
    trip = create_trip(
        created_by=created_by,
        title=trip.title,
        description=trip.description,
        tags=trip.tags,
    )
    return Trip.from_db_model(trip)
