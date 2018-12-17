from common.response import error_response

from .create_trip import create_trip_handler
from .get_trip import get_trip_handler
from .list_trips import list_trips_handler
from .update_trip import update_trip_handler


def root_endpoint(request, *args, **kwargs):
    if request.method == "GET":
        return list_trips_handler(request, *args, **kwargs)
    if request.method == "POST":
        return create_trip_handler(request, *args, **kwargs)

    return error_response(status=404)


def trip_id_endpoint(request, *args, **kwargs):
    if request.method == "GET":
        return get_trip_handler(request, *args, **kwargs)
    if request.method == "PATCH":
        return update_trip_handler(request, *args, **kwargs)

    return error_response(status=404)
