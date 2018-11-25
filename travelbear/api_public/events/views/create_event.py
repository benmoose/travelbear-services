from django.views.decorators.http import require_http_methods

from api_public.auth import require_jwt_auth
from common.response import validation_error_response, success_response
from ..models.event import Event


@require_http_methods(["POST"])
@require_jwt_auth
def create_event(request):
    event = get_event_from_request(request)
    print("event", event)
    if not event.is_valid:
        return validation_error_response(validation_errors=event.validation_errors)

    return success_response(status=201, data=event.to_dict())


def get_event_from_request(request):
    return Event.from_dict(request.POST)
