from django.conf import settings
from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.time import get_current_utc_time
from common.parse import safe_parse_rfc_3339
from common.response import success_response
from db_layer.event import list_upcoming_events_for_user
from ..models.event import Event


@require_http_methods(["GET"])
@require_jwt_auth
def list_upcoming_events(request):
    current_time = get_current_utc_time()
    if settings.IS_TEST_ENVIRONMENT:
        mock_current_time = safe_parse_rfc_3339(
            request.META.get("HTTP_MOCK_CURRENT_TIME")
        )
        current_time = mock_current_time or get_current_utc_time()

    events = list_upcoming_events_for_user(request.user, current_time)
    response_events = [Event.from_db_model(event) for event in events]
    return success_response(data=response_events)
