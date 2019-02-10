from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import error_response, success_response
from db_layer.trip import get_trip_by_id


@require_http_methods(["GET"])
@require_jwt_auth
def itinerary_handler(request, trip_id):
    trip = get_trip_by_id(request.user, trip_id)
    if trip is None:
        return error_response(status=404)

    itinerary = get_itinerary_for_trip(request.user, trip)
    return success_response(data=itinerary)


def get_itinerary_for_trip(user, trip):
    raise NotImplemented
