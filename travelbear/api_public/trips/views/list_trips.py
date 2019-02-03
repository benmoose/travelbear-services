from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import success_response
from db_layer.trip import get_trips_for_user
from ..models.trip import Trip


@require_http_methods(["GET"])
@require_jwt_auth
def list_trips_handler(request):
    trips = get_trips_for_user(request.user)
    response_trips = [Trip.from_db_model(trip) for trip in trips]
    return success_response(data=response_trips)
