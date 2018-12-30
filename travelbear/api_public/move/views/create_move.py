from common.response import success_response, error_response, validation_error_response
from common.parse import safe_parse_json
from db_layer.trip import create_move
from ..models import Move


def create_move_handler(request):
    request_data = safe_parse_json(request.body)
    if request_data is None:
        return error_response(message="Could not parse request body as JSON")
    move_request = Move.from_dict(request_data)
    if not move_request.is_valid:
        return validation_error_response(validation_errors=move_request.validation_errors)
    return success_response(data=move_request)
