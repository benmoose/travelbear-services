from api_public.auth import require_jwt_auth
from common.response import success_response, error_response, validation_error_response
from common.parse import safe_parse_json
from db_layer.trip import create_move, get_location_by_id
from ..models import Move


@require_jwt_auth
def create_move_handler(request):
    request_data = safe_parse_json(request.body)
    if request_data is None:
        return error_response(message="Could not parse request body as JSON")
    move_model = Move.from_dict(request_data)
    if not move_model.is_valid:
        return validation_error_response(move_model.validation_errors)

    start_location, end_location = get_locations_from_location_ids(
        request.user, move_model.start_location_id, move_model.end_location_id
    )
    if not start_location or not end_location:
        validation_errors = get_location_not_found_validation_errors(
            start_location_id=move_model.start_location_id,
            end_location_id=move_model.end_location_id,
            start_location=start_location,
            end_location=end_location,
        )
        return validation_error_response(validation_errors)

    db_move = create_move(start_location, end_location)

    response_dict = Move.from_db_model(db_move)
    return success_response(status=201, data=response_dict)


def get_locations_from_location_ids(user, start_location_id, end_location_id):
    start_location = get_location_by_id(user, start_location_id)
    end_location = get_location_by_id(user, end_location_id)
    return start_location, end_location


def get_location_not_found_validation_errors(
    start_location_id, end_location_id, start_location, end_location
):
    """
    >>> get_location_not_found_validation_errors("id-1", "id-2", None, True)
    ["Location with location-id 'id-1' does not exist"]
    >>> get_location_not_found_validation_errors("id-1", "id-2", True, True)
    []
    """
    return [
        f"Location with location-id '{location_id}' does not exist"
        for (location_id, location) in zip(
            [start_location_id, end_location_id], [start_location, end_location]
        )
        if not location
    ]
