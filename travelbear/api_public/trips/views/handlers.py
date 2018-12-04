from common.response import error_response

from .create_trip import create_trip_handler
from .list_trips import list_trips_handler


def index(request, *args, **kwargs):
    if request.method == "GET":
        return list_trips_handler(request, *args, **kwargs)
    if request.method == "POST":
        return create_trip_handler(request, *args, **kwargs)

    return error_response(status=404)
