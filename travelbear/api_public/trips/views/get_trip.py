from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import success_response
from db_layer.trip import get_trip_by_id
from ..models.trip import Trip


@require_http_methods(['GET'])
@require_jwt_auth
def get_trip_handler(request, trip_id):
    db_trip = get_trip_by_id(request.user, trip_id)
    trip = get_response_trip(db_trip)

    return success_response(data=trip)


def get_response_trip(db_trip):
    return Trip.from_db_model(db_trip)
