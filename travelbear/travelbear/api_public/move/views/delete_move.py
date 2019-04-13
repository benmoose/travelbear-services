from uuid import UUID

from api_public.auth import require_jwt_auth
from common.response import error_response, success_response
from db_layer.trip import delete_move, get_move_by_move_id


@require_jwt_auth
def delete_move_handler(request, move_id):
    uuid_move_id = parse_move_id_as_uuid(move_id)
    if uuid_move_id is None:
        return error_response(status=404)

    move = get_move_by_move_id(request.user, uuid_move_id)
    if move is None:
        return error_response(status=404)

    delete_move(move)
    return success_response(status=204)


def parse_move_id_as_uuid(move_id):
    try:
        return UUID(move_id)
    except ValueError:
        return None
