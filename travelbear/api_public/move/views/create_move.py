from django.db import IntegrityError

from api_public.auth import require_jwt_auth
from common.response import success_response, error_response, validation_error_response
from common.parse import safe_parse_json
from db_layer.trip import create_move, get_location_by_id
from ..models import Move


class LocationDoesNotExist(ValueError):
    pass


@require_jwt_auth
def create_move_handler(request):
    request_data = safe_parse_json(request.body)
    if request_data is None:
        return error_response(message="Could not parse request body as JSON")
    move_model = Move.from_dict(request_data)
    if not move_model.is_valid:
        return validation_error_response(move_model.validation_errors)
    try:
        db_move = persist_move(move_model)
        response_dict = Move.from_db_model(db_move)
        return success_response(status=201, data=response_dict)
    except LocationDoesNotExist as e:
        return error_response(message=str(e))


def persist_move(move_model):
    start_location, end_location = get_locations_from_location_ids(
        move_model.start_location_id, move_model.end_location_id
    )
    try:
        return create_move(start_location, end_location)
    except IntegrityError:
        raise LocationDoesNotExist(f"One or both location IDs do not exist")


def get_locations_from_location_ids(start_location_id, end_location_id):
    start_location = get_location_by_id(start_location_id)
    end_location = get_location_by_id(end_location_id)
    if not start_location or not end_location:
        raise LocationDoesNotExist(
            "One or more of the specified locations does not exist"
        )
    return start_location, end_location
